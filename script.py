import sqlite3
import time
import sys, os
from flask import Flask, render_template, redirect, request
from PIL import Image, ImageDraw, ImageFont

sys.path.append(os.path.join(os.getcwd(), '..'))

from utils.clipboard import write_to_clipboard, read_from_clipboard

app = Flask(__name__)

# Database
from init_db import DB, TABLE


@app.route('/')
def index():
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()

    clipboard_text = read_from_clipboard()
    print(f'----------clipboard_text:{clipboard_text}')
    cursor.execute(f"select * from {TABLE} where lower(comment) like '%{clipboard_text.lower()}%';")
    rows = cursor.fetchall()

    result = {}
    # img_paths = []
    print('------------rows---------')
    print(rows)
    for row in rows:
        _, _, img_path, num, x, y, comment = row
        img_format = img_path.split('.')[-1]
        # 打开一个图片
        image = Image.open(img_path)
        # 创建一个可以在给定图片上绘图的对象
        draw = ImageDraw.Draw(image)
        # 在指定坐标上添加文字
        draw.text((x, y), str(num), fill=(255, 0, 0))
        # 保存修改后的图片
        img_name = str(int(time.time()*10000)) + '.' + img_format
        img_path = f"{os.path.join(os.getcwd(), 'static', img_name)}"
        print('---------img_path')
        print(img_path)
        # img_paths.append(img_path)
        image.save(img_path)

        result.setdefault(img_name, [])
        result[img_name].append({'num': num, 'comment': comment})

    cursor.close()
    connection.close()

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(port=8002, debug=True, host='0.0.0.0')
