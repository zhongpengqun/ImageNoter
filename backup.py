import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

#输入图像的地址path
#这儿还要注意定义缩小比例这个参数scale_factor = 0.5，有些图片尺寸太大导致超出电脑屏幕尺寸，所以设置了缩小比例


path=r"C:\Users\ASUS\frame2.jpg"
# 初始化计数器

point_counter = 1

def on_canvas_click(event):
    global point_counter
    x, y = event.x, event.y
    original_x = int(x / scale_factor)
    original_y = int(y / scale_factor)

    # 在图像上绘制红点和文本
    draw = ImageDraw.Draw(resized_image)
    draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill='red', outline='red')
    draw.text((x-10, y-10), str(point_counter), fill='red')

    canvas.delete("all")  # 清空Canvas以显示更新后的图像
    tk_image = ImageTk.PhotoImage(resized_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    canvas.image = tk_image  # 保留对图像的引用

    print(f'点击坐标 ({x}, {y}) 映射到原尺寸图像坐标 ({original_x}, {original_y})，编号为 {point_counter}')
    point_counter += 1

# 打开图像文件
original_image = Image.open(path)

# 定义缩小比例（0.5 表示缩小为原来的一半）
scale_factor = 0.5

# 计算缩小后的图像尺寸
new_width = int(original_image.width * scale_factor)
new_height = int(original_image.height * scale_factor)

# 缩小图像
resized_image = original_image.resize((new_width, new_height), Image.ANTIALIAS)

# 创建Tkinter窗口
root = tk.Tk()
root.title('点击图像获取坐标并显示红点编号')

# 将PIL图像转换为Tkinter PhotoImage对象
tk_image = ImageTk.PhotoImage(resized_image)

# 创建Canvas并显示图像
canvas = tk.Canvas(root, width=new_width, height=new_height)
canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
canvas.pack()

# 绑定点击事件处理函数
canvas.bind("<Button-1>", on_canvas_click)

root.mainloop()
