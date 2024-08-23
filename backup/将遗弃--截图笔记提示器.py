import os
import time
import platform
import tkinter as tk

from PIL import Image, ImageTk, ImageDraw

import sqlite3
import pyperclip
import subprocess

from init_db import DB, TABLE


RELATED_LINES_UP_COUNT = 5
RELATED_LINES_DOWN_COUNT = 10


current_clipboard_content = ""
pt = platform.platform()


def read_from_clipboard():
    if "Windows" in pt:
        data = pyperclip.paste()
        return data
    else:
        return subprocess.check_output(
            'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')


# init canvas
root = tk.Tk()
root.title('截图笔记提示器')
image = Image.open(r"lenna.png")
tk_image = ImageTk.PhotoImage(image)
canvas = tk.Canvas(root, width=tk_image.width(), height=tk_image.height())
canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
canvas.pack()

text = tk.Text(root)


matched_comments = []
index = 0


def on_refresh():
    clipboard_content = read_from_clipboard()

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # TODO: group will be better
    cursor.execute(f"select id, screenshot_path, comment_num, comment_num_x, comment_num_y, comment from {TABLE} where LOWER(comment) like ?;", ("%" + clipboard_content.lower() + "%",))
    matched_comments = cursor.fetchall()
    for matched_comment in matched_comments:
        global index
        index += 1

        _id, _screenshot_path, _comment_num, _comment_num_x, _comment_num_y, _comment = matched_comment
        _image = Image.open(_screenshot_path)

        image_copy = _image.copy()
        _image.close()
        draw_image = ImageDraw.Draw(image_copy)
        draw_image.ellipse((_comment_num_x - 4, _comment_num_y - 4, _comment_num_x + 4, _comment_num_y + 4), fill=(255, 255, 255), outline="#FF0000", width=3)
        image_copy.save("temp.png")

        print('------')
        print(matched_comment)
        print(clipboard_content)

        # Refresh canvas
        canvas.delete("all")
        tk_image = ImageTk.PhotoImage(image_copy)
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        canvas.configure(width=tk_image.width(), height=tk_image.height())
        canvas.image = tk_image

        # Show comments in text, and highlight keyword
        text.delete(1.0, tk.END)
        _start = _comment.find(clipboard_content)
        _end = _start + len(clipboard_content)
        text.insert(tk.INSERT, _comment)
        text.insert(tk.END, "")
        text.pack()
        text.tag_add("keyword", f"1.{_start}", f"1.{_end}")
        text.tag_config("keyword", background="yellow", foreground="blue")


def on_next_screenshot():
    pass
    # TODO


def fun():
    while True:
        print("Detecting...")
        time.sleep(2)
        on_refresh()


import threading
t1 = threading.Thread(target=fun,args=())
t1.setDaemon(True)
t1.start()
time.sleep(1)


tk.Button(root, text="Manually Refresh", command=on_refresh).pack()
tk.Button(root, text="Next Screenshot", command=on_next_screenshot).pack()

root.mainloop()
