import tkinter
import tkinter.filedialog
import os
from PIL import ImageGrab,Image
from time import sleep
import time

from settings import screenshot_folder_choices


# 截图保存在该文件夹
project_root = os.path.abspath(os.path.join(os.getcwd(), "../.."))
screenshot_folder = ""
# screenshot_folder = os.path.abspath(os.path.join(project_root, "docs/assets/我的截图"))

#用来显示全屏幕截图并响应二次截图的窗口类
class MyCapture:
    def __init__(self, filename):
        #变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)

        #屏幕尺寸
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()

        #创建顶级组件容器
        self.top = tkinter.Toplevel(root, width=screenWidth, height=screenHeight)

        #不显示最大化、最小化按钮
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top,bg='white', width=screenWidth, height=screenHeight)

        #显示全屏截图，在全屏截图上进行区域截图
        self.filename = filename
        self.image = tkinter.PhotoImage(file=filename)
        self.canvas.create_image(screenWidth//2, screenHeight//2, image=self.image)
 
        self.canvas.bind('<Button-1>', self.onLeftButtonDown)
        self.canvas.bind('<B1-Motion>', self.onLeftButtonMove)
        self.canvas.bind('<ButtonRelease-1>', self.onLeftButtonUp)
        #让canvas充满窗口，并随窗口自动适应大小
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    #鼠标左键按下的位置
    def onLeftButtonDown(self, event):
        self.X.set(event.x)
        self.Y.set(event.y)
        #开始截图
        self.sel = True

    #鼠标左键移动，显示选取的区域
    def onLeftButtonMove(self, event):
        if not self.sel:
            return
        global lastDraw
        try:
            #删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
            self.canvas.delete(lastDraw)
        except Exception as e:
            pass
        lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='red')

    #获取鼠标左键抬起的位置，保存区域截图
    def onLeftButtonUp(self, event):
        self.sel = False
        try:
            self.canvas.delete(lastDraw)
        except Exception as e:
            pass
        sleep(0.1)
        #考虑鼠标左键从右下方按下而从左上方抬起的截图
        left, right = sorted([self.X.get(), event.x])
        top, bottom = sorted([self.Y.get(), event.y])
        image = Image.open(self.filename)
        # image.crop的参数为一个四元组，表示裁剪区域的左上角坐标和右下角坐标
        pic = image.crop((left, top, right, bottom))
        pic.save(os.path.join(f'{screenshot_folder}', f'{str(int(time.time()))}.png'))
        #弹出保存截图对话框
        # fileName = tkinter.filedialog.asksaveasfilename(title='保存截图', filetypes=[("PNG file", "*.png"),("JPEG file", "*.jpeg;*.jpg"),("GIF file","*.gif"),("BMP file","*.bmp")],initialfile=txt1,defaultextension='.png')
        # if fileName:
        # 	pic.save(fileName)
        # 	pic.close()
        #关闭当前窗口
        self.top.destroy()


 
#开始截图
def buttonCaptureClick():
	#最小化主窗口
	root.state('icon')
	sleep(0.2)
	filename = 'temp.png'
	#grab()方法默认对全屏幕进行截图
	im = ImageGrab.grab()
	im.save(filename)
	im.close()
	#显示全屏幕截图
	w = MyCapture(filename)
	buttonCapture.wait_window(w.top)
	#截图结束，恢复主窗口，并删除临时的全屏幕截图文件
	root.state('normal')
	os.remove(filename)


def reflesh_text():
    text.delete('1.0', tkinter.END)
    text.insert(tkinter.END, 'Saved:')
    text.insert(tkinter.INSERT, screenshot_folder)


def choose_screenshot_folder():
    global screenshot_folder

    if screenshot_folder:
        screenshot_folder = screenshot_folder_choices[(screenshot_folder_choices.index(screenshot_folder)
 + 1) % len(screenshot_folder_choices) ]
    else:
        screenshot_folder = screenshot_folder_choices[0]

    reflesh_text()


root = tkinter.Tk()
#设置窗口大小与位置
#root.geometry(f'100x50+{root.winfo_screenwidth() - 100}+0')
root.geometry(f'200x100+{root.winfo_screenwidth() - 200}+0')
#center_window(root,95,40)
#设置窗口大小不可改变
root.resizable(False, False)
buttonCapture = tkinter.Button(root, text='截图', command=buttonCaptureClick)
buttonCapture.place(x=10, y=10, width=80, height=20)

buttonCapture = tkinter.Button(root, text='更换截图保存地址', command=choose_screenshot_folder)
buttonCapture.place(x=10, y=40, width=80, height=20)

text = tkinter.Text(root, height=2, width=25)
text.insert(tkinter.END, 'Saved:')
text.insert(tkinter.INSERT, screenshot_folder)
text.place(x=0, y=70)

#启动消息主循环
root.mainloop()
