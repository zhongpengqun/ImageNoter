import time
import sys, os
from flask import Flask, render_template, redirect, request

sys.path.append(os.path.join(os.getcwd(), '..'))

from settings import PORT
from utils.clipboard import write_to_clipboard, read_from_clipboard

app = Flask(__name__)

@app.route('/whisper')
def whisper():
    return render_template('whisper.html')


if __name__ == '__main__':
    app.run(port=8002, debug=True, host='0.0.0.0')
