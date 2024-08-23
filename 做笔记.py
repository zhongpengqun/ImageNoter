import os
import glob
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

from init_db import DB, TABLE

from settings import screenshot_folder_choices

def get_latest_screenshotimage_path():
    # project_root = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    # jietu_folder = os.path.abspath(os.path.join(project_root, "docs/assets/我的截图"))
    list_of_files = []

    for screenshot_folder in screenshot_folder_choices:
        list_of_files.extend(glob.glob(f'{screenshot_folder}/*'))
    latest_image = max(list_of_files, key=os.path.getctime)
    return latest_image


original_image = Image.open(get_latest_screenshotimage_path())

point_counter = 0

# 创建Tkinter窗口
root = tk.Tk()
root.title('点击图像获取坐标并显示红点编号')

# 将PIL图像转换为Tkinter PhotoImage对象
tk_image = ImageTk.PhotoImage(original_image)

# 创建Canvas并显示图像
canvas = tk.Canvas(root, width=tk_image.width(), height=tk_image.height())
canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
canvas.pack()

entry_pixel_position = tk.Entry(root, width=30)
entry_comment = tk.Entry(root, width=30)
entry_pixel_position.pack()
entry_comment.pack()


def load_new_image():
    global original_image

    canvas.delete("all")  # 清空Canvas以显示更新后的图像

    new_image = Image.open(get_latest_screenshotimage_path())

    original_image = new_image

    tk_image = ImageTk.PhotoImage(new_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    canvas.configure(width=tk_image.width(), height=tk_image.height())
    canvas.image = tk_image  # 保留对图像的引用


def onclick_submit_button():
    _comment = entry_comment.get()
    _entry_pixel_position = entry_pixel_position.get()

    if (not _comment) or (not _entry_pixel_position):
        return

    _x, _y = _entry_pixel_position.split(',')[0], _entry_pixel_position.split(',')[1]

    # 记录该点的笔记
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()

    cursor.execute(f"insert into {TABLE}(screenshot_path, comment_num, comment_num_x, comment_num_y, comment) values(?, ?, ?, ?, ?)", 
                   (original_image.filename, point_counter, _x, _y, _comment))
    connection.commit()

    cursor.close()
    connection.close()

    # Clear entries
    entry_pixel_position.delete(0, tk.END)
    entry_comment.delete(0, tk.END)


def on_canvas_click(event):
    global point_counter
    point_counter += 1

    x, y = event.x, event.y

    # 在图像上绘制红点和文本
    draw = ImageDraw.Draw(original_image)
    radius = 2
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill='red', outline='red')
    draw.text((x-10, y-10), str(point_counter), fill='red')

    canvas.delete("all")  # 清空Canvas以显示更新后的图像
    tk_image = ImageTk.PhotoImage(original_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    canvas.image = tk_image  # 保留对图像的引用

    entry_pixel_position.delete(0, tk.END)
    entry_pixel_position.insert(0, '%s,%s'%(x, y))


tk.Button(root, text="Submit", command=onclick_submit_button).pack()
tk.Button(root, text="Load New Image", command=load_new_image).pack()


# 绑定点击事件处理函数
canvas.bind("<Button-1>", on_canvas_click)

root.mainloop()
