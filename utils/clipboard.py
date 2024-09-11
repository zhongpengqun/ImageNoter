import platform
import pyperclip
import subprocess


pwd_mapper = {
}


def recognize_instruction(clipboard_text):
    if clipboard_text.startswith('pwd:'):
        raw_pwd = clipboard_text.replace('pwd:', '')
        return pwd_mapper.get(raw_pwd, '')

    return clipboard_text

def read_from_clipboard():
    pt = platform.platform()
    if "Windows" in pt:
        data = pyperclip.paste()
    else:
        data = subprocess.check_output(
            'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')
    return data

def write_to_clipboard(text):
    pyperclip.copy(text)
