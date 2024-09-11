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
    cursor.execute(f"select * from {TABLE} where comment='{clipboard_text}';")
    rows = cursor.fetchall()

    result = {}
    img_names = []
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
        img_name = f"static/{str(int(time.time()*10000))}.{img_format}"
        img_names.append(img_name)
        image.save(img_name)

        result.setdefault(img_name, [])
        result[img_name].append({'num': num, 'comment': comment})

    cursor.close()
    connection.close()

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(port=8002, debug=True, host='0.0.0.0')
