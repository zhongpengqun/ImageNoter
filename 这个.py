#!/usr/bin/python
import os
import time
import platform
import glob

from PIL import Image, ImageTk, ImageGrab
from tkinter import Tk, Frame, Menu, Button, Text, IntVar, Toplevel, Canvas, PhotoImage, \
    BOTH, LEFT, TOP, X, FLAT, RAISED, END, INSERT, YES, NW


SCREENSHOT_SAVED_PATHS = [
    r"C:\Users\zlzk\Documents\GitHub\prompt\笔记生成器\screenshots",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots'),
    # f"{os.path.dirname(os.path.abspath(__file__))}{ '\\' if 'windows' in platform.platform().lower() else '/'}screenshots",
    r"C:\Users\zlzk\Documents\GitHub\notebook\docs\assets\我的截图"
]


# 用来显示全屏幕截图并响应二次截图的窗口类
class MyCapture:
    def __init__(self, filename):
        #变量X和Y用来记录鼠标左键按下的位置
        self.X = IntVar(value=0)
        self.Y = IntVar(value=0)

        #屏幕尺寸
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()

        #创建顶级组件容器
        self.top = Toplevel(root, width=screenWidth, height=screenHeight)

        #不显示最大化、最小化按钮
        self.top.overrideredirect(True)
        self.canvas = Canvas(self.top,bg='white', width=screenWidth, height=screenHeight)

        #显示全屏截图，在全屏截图上进行区域截图
        self.filename = filename
        self.image = PhotoImage(file=filename)
        self.canvas.create_image(screenWidth//2, screenHeight//2, image=self.image)
 
        self.canvas.bind('<Button-1>', self.onLeftButtonDown)
        self.canvas.bind('<B1-Motion>', self.onLeftButtonMove)
        self.canvas.bind('<ButtonRelease-1>', self.onLeftButtonUp)
        #让canvas充满窗口，并随窗口自动适应大小
        self.canvas.pack(fill=BOTH, expand=YES)

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
        time.sleep(0.1)
        #考虑鼠标左键从右下方按下而从左上方抬起的截图
        left, right = sorted([self.X.get(), event.x])
        top, bottom = sorted([self.Y.get(), event.y])
        image = Image.open(self.filename)
        # image.crop的参数为一个四元组，表示裁剪区域的左上角坐标和右下角坐标
        pic = image.crop((left, top, right, bottom))
        screenshot_folder = ""
        pic.save(os.path.join(f'{screenshot_folder}', f'{str(int(time.time()))}.png'))
        #弹出保存截图对话框
        # fileName = tkinter.filedialog.asksaveasfilename(title='保存截图', filetypes=[("PNG file", "*.png"),("JPEG file", "*.jpeg;*.jpg"),("GIF file","*.gif"),("BMP file","*.bmp")],initialfile=txt1,defaultextension='.png')
        # if fileName:
        # 	pic.save(fileName)
        # 	pic.close()
        #关闭当前窗口
        self.top.destroy()


class ImageNoter(Frame):
    def __init__(self):
        self.screenshot_saved_path = SCREENSHOT_SAVED_PATHS[0]
        self.screenshot_saved_path_hint_text = None
        self.button_do_screenshot = None
        super().__init__()
        self.initUI()


    def initUI(self):
        self.master.title("ImageNoter")

        toolbar = Frame(self.master, bd=1, relief=RAISED)

        self.button_window_minimize = Button(toolbar, text="窗口最小化", relief=FLAT, command=self.window_minimize)
        self.button_do_screenshot = Button(toolbar, text="截图", relief=FLAT, command=self.do_screenshot)
        button_switch_screenshot_saved_path = Button(toolbar, text="切换截图保存地址", relief=FLAT, command=self.switch_screenshot_saved_path)
        self.button_window_minimize.pack(side=LEFT, padx=2, pady=2)
        self.button_do_screenshot.pack(side=LEFT, padx=2, pady=2)
        button_switch_screenshot_saved_path.pack(side=LEFT, padx=2, pady=2)

        self.init_screenshot_saved_path_hint()
        self.init_canvas()

        toolbar.pack(side=TOP, fill=X)
        self.pack()


    def onExit(self):
        self.quit()

    def switch_screenshot_saved_path(self):
        def refresh_hint(new_hint):
            # Clear
            self.screenshot_saved_path_hint_text.delete(1.0, END)

            self.screenshot_saved_path_hint_text.insert(INSERT, new_hint)
            self.screenshot_saved_path_hint_text.insert(END, "")

            self.screenshot_saved_path_hint_text.pack()

        if not self.screenshot_saved_path:
            self.screenshot_saved_path = SCREENSHOT_SAVED_PATHS[0]
        else:
            self.screenshot_saved_path = SCREENSHOT_SAVED_PATHS[(SCREENSHOT_SAVED_PATHS.index(self.screenshot_saved_path) + 1) % len(SCREENSHOT_SAVED_PATHS)]

        refresh_hint(f'截图保存在：{self.screenshot_saved_path}')


    def init_screenshot_saved_path_hint(self):
        self.screenshot_saved_path_hint_text = Text(self, height=1, width=int(self.winfo_screenwidth()/2))
        self.switch_screenshot_saved_path()

    def get_latest_screenshotimage_path(self):
        # project_root = os.path.abspath(os.path.join(os.getcwd(), "../.."))
        # jietu_folder = os.path.abspath(os.path.join(project_root, "docs/assets/我的截图"))
        latest_image = max(glob.glob(f'{self.screenshot_saved_path}/*'), key=os.path.getctime)
        return latest_image

    def init_canvas(self):
        print(self.get_latest_screenshotimage_path())
        original_image = Image.open(self.get_latest_screenshotimage_path())
        # 将PIL图像转换为Tkinter PhotoImage对象
        tk_image = ImageTk.PhotoImage(original_image)
        # 创建Canvas并显示图像
        # canvas = Canvas(root, width=tk_image.width(), height=tk_image.height())
        canvas = Canvas(self, bg="red", width=100, height=100)
        canvas.create_image(0, 0, anchor=NW, image=tk_image)
        canvas.pack()

    # todo, 待研究
    def window_minimize(self):
        # print(self.button_window_minimize.cget('text'))
        # print(self.button_window_minimize.cget('text') == '窗口最小化')
        if self.button_window_minimize.cget('text') == "窗口最小化":
            root.geometry('100x20')
            self.button_window_minimize.config(text="窗口还原")
            time.sleep(0.5)

        elif self.button_window_minimize.cget('text') == '窗口还原':
            root.geometry(f'{int(root.winfo_screenwidth()/2)}x{root.winfo_screenheight() - 80}+{root.winfo_screenwidth() - int(root.winfo_screenwidth()/2)}+0')
            self.button_window_minimize.config(text="窗口最小化")

    # 开始截图
    def do_screenshot(self):
        filename = 'temp.png'
        #grab()方法默认对全屏幕进行截图
        im = ImageGrab.grab()
        im.save(filename)
        im.close()
        #显示全屏幕截图
        w = MyCapture(filename)
        self.button_do_screenshot.wait_window(w.top)
        #截图结束，恢复主窗口，并删除临时的全屏幕截图文件
        os.remove(filename)


if __name__ == '__main__':
    root = Tk()
    # Top-right
    root.geometry(f'{int(root.winfo_screenwidth()/2)}x{root.winfo_screenheight() - 80}+{root.winfo_screenwidth() - int(root.winfo_screenwidth()/2)}+0')
    ImageNoter()
    root.mainloop()
