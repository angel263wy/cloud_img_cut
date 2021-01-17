# -*- coding: UTF-8 -*-
# Author      : WangYi
# Date        : 2021/01/17
# Description : 

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from gui import Ui_Form

import time
import struct
import numpy as np
import matplotlib.pyplot as plt

import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False 



class Test(QWidget, Ui_Form):
    def __init__(self):
        super(Test, self).__init__()        
        self.setupUi(self)
        
        # 自定义内部对象
        self.all_865P2_img = np.empty(0)  # 文件中所有云判数据
        self.img_mean_865P2 = np.empty(0)  # 所有云判区域按像素求平均值
        self.dict_img_mean_865P2 = {'Vmax' : 0, 'Vmin' : 0, 'Vmean':0}
        
    # 清除日志函数
    def click_log_clear(self):
        self.textEdit_log.clear()
    
    # 打开并处理函数
    def click_open(self):
        try:
            # 读入所有文件数据
            fname, _ = QFileDialog.getOpenFileName(self,  \
                        filter='raw file(*.*)', caption='打开原始LVDS文件')            
            if len(fname) == 0:
                self.log_show('未选择文件')
                return
            else:
                self.log_show(f'打开文件{fname}')
            # 读入文件
            raw_data = np.fromfile(fname, dtype=np.uint8)
            # 格式正确性判断
            if (raw_data[0] != 0x0A) and (raw_data[1] != 0x4A) :
                self.log_show('文件头错误,处理结束')
                self.pushButton_show_img.setEnabled(False)
                return
            # 检查文件长度
            img_cnt = int(len(raw_data) / 342900)
            if img_cnt < 15:
                self.log_show('文件中图像小于15, 不进行处理') 
                self.pushButton_show_img.setEnabled(False)
                return
            else:
                self.log_show(f'文件帧头标识正确，共计图像{img_cnt}幅')

            # 读入并挑选865P2数据
            foo_list = list()
            for i in range(img_cnt):
                img = raw_data[i*342900 : (i+1)*342900]  # 取出一幅图片
                # 文件合法性检查
                if (img[0] != 0x0A) and (img[1] != 0x4A) :
                    self.log_show(f'第{i}幅图像帧头错误,处理结束')
                    return
                # 属于865P2波段 取数据              
                if img[328] == 12 : 
                    foo_list.append(self.pick_data(img))
                    
            # 检查文件数量是否合适
            if len(foo_list) == 0 :
                self.log_show(f'没有找到865P2的图像,处理结束')
                self.pushButton_show_img.setEnabled(False)
                return
            else:
                self.log_show(f'找到865P2图片共计{len(foo_list)}幅')
                self.spinBox_img_cnt.setMaximum(len(foo_list)-1)
                self.pushButton_show_img.setEnabled(True)
            # 数据保存
            self.all_865P2_img = np.array(foo_list)
            # 图像求平均
            self.img_mean_865P2 = np.mean(self.all_865P2_img, axis=0)
            # 输出图像信息 保留两位小数
            self.log_show(f'云判区域数据挑选成功,点击显示图像查看')

        except Exception as e:
            self.log_show('处理过程出现异常')
            self.log_show('异常信息: '+ repr(e))  
    
    def click_show_img(self):
        # 显示平均值图像
        if self.checkBox_show_mean_img.isChecked():
            plt.figure()
            foo_img = np.reshape(self.img_mean_865P2, (8, 36)) 
            a,b,c = np.max(foo_img), np.min(foo_img), np.mean(foo_img)
            foo_title = f'平均值图像 灰度值最大{round(a)} 最小{round(b)} 平均{round(c)}'
            plt.title(foo_title)
            plt.imshow(foo_img, cmap = 'Greys_r')
            self.log_show(foo_title)
            
        # 显示单幅图像
        img_cnt = self.spinBox_img_cnt.value()  # 获取编号
        if img_cnt == -1:
            pass  # 编号为-1 表示不显示单幅图像
        else:            
            plt.figure() 
            fo2_img = np.reshape(self.all_865P2_img[img_cnt, :], (8, 36))  # 取数 成图
            a,b,c = np.max(fo2_img), np.min(fo2_img), np.mean(fo2_img)
            foo_title = f'第{img_cnt}幅图像 灰度值最大{round(a)} 最小{round(b)} 平均{round(c)}'
            plt.title(foo_title)            
            plt.imshow(fo2_img, cmap = 'Greys_r')
            self.log_show(foo_title)
        
        plt.show()        
        plt.close('all') 
        


# ----------------内部函数----------------
    # 记录日志函数
    def log_show(self, foo_txt):
        now = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
        txt_out = now + foo_txt
        self.textEdit_log.append(txt_out)
        
        with open('log.txt', 'a+', encoding='utf-8') as f:
            f.write(txt_out)
            f.write('\n')

    
    ''' 
    8字节 转7像素16bit 函数
    输入 data_arr 7个字节 56 bit的序列
    输出 4个int类型数组 表示4个像素的双字节灰度值
    '''
    def pixel_get(self, data_arr):
        ret_value = np.zeros(4)
        if len(data_arr) != 7:  # 字节长度合法性判断
            print('非4像素字节')
        else:
            foo = list()
            # 拼成56bit
            for cnt, vlaue in enumerate(data_arr):
                # 首字符直接复制 之后数据增加
                foo = foo + f'{vlaue:b}'.zfill(8) if cnt!=0 \
                        else f'{vlaue:b}'.zfill(8)

            for i in range(4):  # range(4)表示4个像素
                # 每隔14bit取数据 转换为十进制数据
                ret_value[i] = int(foo[i*14:14*(i+1)], base=2)
        
        return ret_value


    # 挑数函数 取出特定区域 转换为图像灰度值
    def pick_data(self, img):
        img = np.reshape(img, (381, 900)) # 形成一张图片
        # 取图 按4像素-56bit-7字节计算 取第68像元到103像元
        foo_area = img[197:204+1, 123:123+63]
        foo_area = foo_area.flatten()  # 变为一维数组 504字节
        
        cloud_area = np.empty(0)
        for i in range(72):  # 504字节 分为72组 每组7字节 解算后放入cloud_area中
            cloud_area = np.append(cloud_area, self.pixel_get(foo_area[i*7 : (i+1)*7]))
            # cloud_area.append(self.pixel_get(foo_area[i*7 : (i+1)*7]))
        
        return cloud_area



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = Test()
    mywidget.show()
    sys.exit(app.exec_())


