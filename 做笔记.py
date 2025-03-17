import os
import glob
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from utils.clipboard import read_from_clipboard, write_to_clipboard

from init_db import DB, TABLE

from settings import screenshot_folder_choices


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
TOP_FRAME_HEIGHT = 700
BOTTOM_FRAME_HEIGHT = 100

def get_latest_screenshotimage_path():
    list_of_files = []

    for screenshot_folder in screenshot_folder_choices:
        list_of_files.extend(glob.glob(f'{screenshot_folder}/*'))
    latest_image = max(list_of_files, key=os.path.getctime)
    return latest_image


def load_new_image():
    global original_image

    # 清空Canvas以显示更新后的图像
    canvas.delete("all")

    try:
        new_image = Image.open(read_from_clipboard())
        write_to_clipboard('')
    except:
        new_image = Image.open(get_latest_screenshotimage_path())

    original_image = new_image

    tk_image = ImageTk.PhotoImage(new_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    canvas.configure(width=tk_image.width(), height=tk_image.height())
    canvas.image = tk_image  # 保留对图像的引用


def onclick_submit_button():
    _comment = text_comment.get("1.0", tk.END)
    _label_pixel_position = label_pixel_position_string.get()

    if (not _comment) or (not _label_pixel_position):
        return

    _x, _y = _label_pixel_position.split(',')[0], _label_pixel_position.split(',')[1]

    # 记录该点的笔记
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()

    cursor.execute(f"insert into {TABLE}(screenshot_path, comment_num, comment_num_x, comment_num_y, comment) values(?, ?, ?, ?, ?)", 
                   (original_image.filename, point_counter, _x, _y, _comment))
    connection.commit()

    cursor.close()
    connection.close()

    # Clear
    label_pixel_position_string.set('')
    text_comment.delete('1.0', tk.END)


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

    label_pixel_position_string.set('')
    label_pixel_position_string.set('%s,%s'%(x, y))

# 
original_image = Image.open(get_latest_screenshotimage_path())
point_counter = 0

# 创建Tkinter窗口
root = tk.Tk()
# root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+10+10')
root.geometry(f'+10+10')
root.title('Image Noter')

# 将PIL图像转换为Tkinter PhotoImage对象
tk_image = ImageTk.PhotoImage(original_image)

# 创建Canvas并显示图像
canvas = tk.Canvas(root, width=tk_image.width(), height=tk_image.height())
canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
canvas.grid(row=0, column=0)

right_frame = tk.Frame(root
                  , width=200
                  , height=WINDOW_HEIGHT
                  , highlightbackground="black"
                  , highlightthickness=0
                  , bd=0)
right_frame.grid(row=0, column=1)

# entry_pixel_position = tk.Entry(root, width=30)
label_pixel_position_string = tk.StringVar()
label_pixel_position = tk.Label(right_frame, textvariable=label_pixel_position_string)
label_pixel_position.grid(row=0, column=0, columnspan=2, sticky=tk.NW)

# entry_comment = tk.Entry(root, width=30)
# entry_comment.grid(row=2, column=1)
text_comment = tk.Text(right_frame, width=30)
text_comment.grid(row=1, column=0, columnspan=2, sticky=tk.NW)

tk.Button(right_frame, text="Submit", command=onclick_submit_button, width=13).grid(row=2, column=0, sticky=tk.NW)
tk.Button(right_frame, text="Load New Image", command=load_new_image, width=15).grid(row=2, column=1, sticky=tk.NW)

# 绑定点击事件处理函数
canvas.bind("<Button-1>", on_canvas_click)

root.mainloop()
