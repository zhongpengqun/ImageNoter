import cv2
import tkinter
import threading
import tempfile
import time
from PIL import ImageGrab
import os
import numpy
import keyboard


#设置主界面
def set_init_window(self):
    # 去掉tkinter默认的标题
    self.tk.title('')
    # 隐藏默认图标
    self.tk.iconbitmap(self.icon_path())
    #获取屏幕的宽度
    screeWidth = self.tk.winfo_screenwidth()
    #获取屏幕高度
    screeHeight = self.tk.winfo_screenheight()
    
    width = int((screeWidth - 500) / 2)
    height = int((screeHeight - 300) / 2)
    # 设置主界面的大小和默认位置
    self.tk.geometry(f'500x100+{width}+{height}')
    
    #添加开始录制按钮，点击之后开启两个线程：一个录屏、一个监听键盘
    btn1 = tkinter.Button(self.tk, width=5, height=1, text='开始',
    command=lambda:[threading.Thread(target=self.video_record).start(),threading.Thread(target=self.start_listen).start()])
    btn1.pack()
    # 设置按钮位置
    btn1.place(x=110, y=50, anchor='n')
    
    #开启新线程设置录屏范围
    btn2 = tkinter.Button(self.tk, width=15, height=1, text='设置录制区域', command=lambda:threading.Thread(target=self.set_range).start())
    btn2.pack()
    btn2.place(x=230, y=50, anchor='n')


#生成透明的icon图标
def icon_path(self):
    ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
            b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
            b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x01\x00\x00\x00\x01') + b'\x00' * 1282 + b'\xff' * 64
    _, ICON_PATH = tempfile.mkstemp()
    with open(ICON_PATH, 'wb') as icon_file:
        icon_file.write(ICON)
    return ICON_PATH


#设置录屏范围
def set_range(self):
    #self.init_window.withdraw() #隐藏窗口
    self.tk.state('icon')#窗口最小化
    screeWidth = self.tk.winfo_screenwidth()
    screeHeight = self.tk.winfo_screenheight()

    self.newFrame = tkinter.Toplevel(self.tk,width=screeWidth,height=screeHeight,bg='white')#开启新窗口
    self.newFrame.attributes('-transparentcolor', 'white')  # 使白色为透明色
    self.newFrame.overrideredirect(True)  # 隐藏导航栏

    self.canvas = tkinter.Canvas(self.newFrame,bg='white',bd=0,width=screeWidth,height=screeHeight)
    self.canvas.bind('', self.onLeftButtonDown)#按下左键
    self.canvas.bind('', self.onLeftButtonMove)#移动鼠标
    self.canvas.bind('', self.onLeftButtonUp)#抬起左键
    self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    time.sleep(0.3)
    im = ImageGrab.grab()
    # 暂存全屏截图
    im.save('temp.png')
    im.close()
    self.image = tkinter.PhotoImage(file='temp.png')
    os.remove('temp.png')
    self.canvas.create_image(screeWidth//2, screeHeight//2, image=self.image)


#按下鼠标
def onLeftButtonDown(self,event):
    try:
        self.canvas.delete(self.lastDraw)
        self.canvas.delete(self.dot1)
        self.canvas.delete(self.dot2)
        self.btn3.destroy()
    except Exception as e:
        pass

    self.X = event.x
    self.Y = event.y
    self.X2 = 0
    self.Y2 = 0

#移动鼠标
def onLeftButtonMove(self,event):
    try:  # 删除刚画完的图形，不然所有画的框都会出现
        self.canvas.delete(self.lastDraw)
        self.canvas.delete(self.dot1)
        self.canvas.delete(self.dot2)
        self.btn3.destroy()
    except Exception as e:
        pass

    self.X2 = event.x
    self.Y2 = event.y
    self.lastDraw = self.canvas.create_rectangle(self.X, self.Y, event.x, event.y,width=2, outline='pink')

#松开鼠标
def onLeftButtonUp(self,event):
    print("起点", self.X, self.Y)
    print("终点", self.X2, self.Y2)

    if self.X2==0 and self.X2==0:
        return

    self.width, self.high = self.X2-self.X,self.Y2-self.Y
    self.region = (self.X, self.Y, self.X2, self.Y2)

    self.dot1=self.canvas.create_text(self.X, self.Y - 10, text=f'({self.X},{self.Y})', font=("Purisa", 12), fill="pink")
    self.dot2=self.canvas.create_text(self.X2, self.Y2 + 10, text=f'({self.X2},{self.Y2})', font=("Purisa", 12), fill="pink")

    # self.newFrame.destroy()#销毁窗口
    # self.init_window.deiconify()#显示窗口
    # self.tk.state('normal')  # 取消窗口最小化

    self.btn3 = tkinter.Button(self.canvas, width=15, height=1, text='确定录制区域',bg='pink',fg='#64854c',command=lambda:[self.newFrame.destroy(),self.tk.state('normal')])
    self.btn3.pack()
    self.btn3.place(x=self.X2-20, y=self.Y2+20, anchor='n')


# 开始监听
def start_listen(self):
    with keyboard.Listener(on_press=self.on_press) as listener:
        listener.join()
    # 监听按键
def on_press(self,key):
    if key == keyboard.Key.esc:
        self.flag = True  # 改变
        return False  # 返回False，键盘监听结束！


def video_record(self):
     fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
     out = cv2.VideoWriter('output.mp4', fourcc, 14, (self.width, self.high))  # 参数分别为 输出文件名，解码方式，帧数，录像范围
     self.count = 1
     while (True):
         img = ImageGrab.grab(self.region) #指定截取坐标(左边X，上边Y，右边X，下边Y)
         img_np = numpy.array(img)
         frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)  # ImageGrab获取的颜色为BGR排序，需转换为RGB
         out.write(frame)
         self.count += 1
         label = tkinter.Label(self.tk, text=f"{int(self.count / 14)}秒")
         label.pack()
         label.place(x=320, y=55, anchor='n')
         # 点击ESC退出
         if self.flag == True:
             tkinter.messagebox.showinfo('提示', '录屏结束')
             self.flag = False  # 改变录屏状态
             break
     out.release()
     cv2.destroyAllWindows()
