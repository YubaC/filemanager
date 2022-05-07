# import csv
# from concurrent.futures import thread
# from __future__ import print_function
import codecs
# from genericpath import isdir
# from glob import glob
# import encodings
# from glob import glob
import os
import csv
# from re import I
# import sys
import re
import time
import hashlib
# from tkinter import font
# from numpy import source
# from pymysql import Timestamp
# from rich.console import Console
# import wmi
# import win32api
# import win32con
import shutil
# import threading
import need.printlogo as printlogo
# import need.icon as icon

# import ctypes

# from rich.progress import Progress
import time

# import easygui

import difflib
import webbrowser

# console = Console()

import tkinter as tk
# from tkinter import Tk, Entry, Toplevel, Listbox
# from tkinter.scrolledtext import ScrolledText

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, Label, Radiobutton, simpledialog

import need.draw as draw

import json

from tkinter.messagebox import askokcancel

import windnd

help_url = "https://yubac.github.io/fmhelp/index.html"

# 列表中存储的是元素是元组
mode_to_select = [('添加文件', 0, '+'), ('移除文件', 1, '-')]

command_chosen = 0
adder_opened = False

exit_flag = False
now_path = ''

home = os.path.expanduser('~')
start_path = os.path.join(home, r'AppData\Local\Programs\FileManager\fm')
if start_path != os.getcwd():
    path_using = now_path = os.getcwd()
    os.chdir(start_path)
else:
    path_using = start_path

all_size = 0
all_number = 0

info_add = ''

s = 0

inited_all_number = 0
inited = False

# all_timestamp={}
changes = {'changes': [], 'delete': [], 'create': []}

process_path = {'changes': [], 'delete': [], 'create': []}

now_at = 0
now_branch = 0

window_opened = False

deletes = []

command_inputed = []

_TEXT_BOMS = (
    codecs.BOM_UTF16_BE,
    codecs.BOM_UTF16_LE,
    codecs.BOM_UTF32_BE,
    codecs.BOM_UTF32_LE,
    codecs.BOM_UTF8,
)


def hash(file_path, Bytes=1024):
    md5_1 = hashlib.md5()  # 创建一个md5算法对象
    with open(file_path, 'rb') as f:  # 打开一个文件，必须是'rb'模式打开
        while 1:
            data = f.read(Bytes)  # 由于是一个文件，每次只读取固定字节
            if data:  # 当读取内容不为空时对读取内容进行update
                md5_1.update(data)
            else:  # 当整个文件读完之后停止update
                break
    ret = md5_1.hexdigest()  # 获取这个文件的MD5值
    return ret


def writefilehash(path_list):
    global path_using
    top = Toplevel()
    top.title('Hashing......')
    icon_for_window(top)
    pb = Progressbar(top, length=200, mode="determinate", orient=HORIZONTAL)
    pb.pack(padx=10, pady=20)
    pb["maximum"] = len(path_list)
    pb["value"] = 0
    # pb["value"] += 1000
    top.protocol('WM_DELETE_WINDOW', callback)  # 窗体的通信协议方法
    top.update()

    # 读取timestamp
    with open(os.path.join(path_using, '.filemanager', 'main', 'timestamp.csv'), "r", encoding='utf-8') as p:
        timestamps = p.read().splitlines()
        p.close()
    timestamp = []
    for i in timestamps:
        timestamp.append(i.split(','))
    timestamps = []
    for i in path_list:
        try:
            file_hash = hash(os.path.join(path_using, i))
            for j in range(len(timestamp)):
                if timestamp[j][0] == i:
                    timestamp[j][2] = file_hash
                    pb["value"] += 1
                    top.update()
                    break
            # timestamp[timestamp.index(i)][2] = file_hash
        except:
            pass
    top.destroy()
    with open(os.path.join(path_using, '.filemanager', 'main', 'timestamp.csv'), "w", encoding='utf-8') as p:
        for i in timestamp:
            p.write('{0},{1},{2}\n'.format(i[0], i[1], i[2]))
        p.close()


def callback():
    pass  # 这个函数不做任何事，实际上让关闭按钮失效


def is_binary_file(file_path):
    with open(file_path, 'rb') as file:
        initial_bytes = file.read(8192)
        file.close()
        for bom in _TEXT_BOMS:
            if initial_bytes.startswith(bom):
                continue
            else:
                if b'\0' in initial_bytes:
                    return True
    return False


def update(terminal):
    global path_using
    if os.path.exists(os.path.join(path_using, '.filemanager', 'main', 'version.txt')):
        with open(os.path.join(path_using, '.filemanager', 'main', 'version.txt'), 'r', encoding='utf-8') as f:
            repo_version_loaded = f.read()
            repo_version = repo_version_loaded.split('.')
            f.close()
        with open(os.path.join(path_using, '.filemanager', 'main', 'version.txt'), 'w', encoding='utf-8') as f:
            f.write(terminal_infos.version)
            f.close()
        if int(repo_version[0]) == 1 and int(repo_version[1]) == 0:
            with open(os.path.join(path_using, '.filemanager', 'main', 'timestamp.csv'), 'r', encoding='utf-8') as f:
                timestamp = f.read().splitlines()
                f.close()

            del timestamp[0]

            paths = []
            for i in timestamp:
                paths.append(i.split(',')[0])

            with open(os.path.join(path_using, '.filemanager', 'main', 'timestamp.csv'), 'w', encoding='utf-8') as f:
                f.write('dir,timestamp,hash\n')
                for i in timestamp:
                    f.write('{0},-1\n'.format(i))
                f.close()
            writefilehash(paths)
    else:
        terminal.insert('end', "\nerror:这不是一个filemanager仓库", 'red')


def init(terminal):
    global id_read
    global inited
    global info_add
    global all_size
    global inited_all_number
    global path_using
    global changes
    global now_at

    if os.path.exists(os.path.join(path_using, '.filemanager', 'main', 'version.txt')):
        with open(os.path.join(path_using, '.filemanager', 'main', 'version.txt'), 'r', encoding='utf-8') as f:
            repo_version_loaded = f.read()
            repo_version = repo_version_loaded.split('.')
            f.close()
        if int(repo_version[0]) == 1 and int(repo_version[1]) == 0:
            terminal.insert('end', "\nerror:init失败", 'red')
            terminal.insert(
                'end', '\nWARNING:这个仓库是被版本{0}的FileManager创建的。使用"init -update"命令以加载这个仓库。'.format(repo_version_loaded), 'yellow')
        else:
            if os.path.exists(os.path.join(path_using, '.filemanager', 'main', 'branches.json')):
                # 起始提交位置
                f = open(os.path.join(path_using, '.filemanager',
                                      'main', 'branches.json'), 'r', encoding='utf-8')
                info_data = json.load(f)
                f.close()
                now_at = int(info_data['now_at'])

            # else:
            #     terminal.insert('end',"error:这不是一个filemanager仓库")
            # branch = []
            # now_at = len(os.listdir(os.path.join(path_using,'.filemanager','commits'))) - 1

            if os.path.exists(os.path.join(path_using, '.filemanager', 'main', 'id.txt')):

                with open(os.path.join(path_using, '.filemanager', 'main', 'id.txt'), "r", encoding='utf-8') as f:
                    id_read = f.read()
                    f.close()
                    # print(id_read)
                    # print(now_path)

                terminal.insert('end', '\nIniting......')
                terminal.update()

                inited_all_number = 0
                for root, dirs, files in os.walk(path_using):
                    if os.path.basename(root) == ".filemanager":
                        dirs[:] = []  # 忽略当前目录下的子目录
                        # os.mkdir(os.path.join(root,r'.filemnager/base'))
                    for name in files:
                        all_size += os.path.getsize(
                            os.path.join(root, name))/1024
                        inited_all_number += 1

                # reload(path_using)

                inited = True
                terminal.insert('end', 'Done.' + '\n')
                # terminal.insert('end',inited_all_number)
                info_add = '('+id_read[0:6]+'...)'
                # printchanges(changes, terminal)

                print_branch(terminal)
    else:
        terminal.insert('end', "\nerror:这不是一个filemanager仓库", 'red')


def add_to_monitor():
    global path_using
    with open('path.txt', 'r', encoding='utf-8') as f:
        paths = f.read().splitlines()
        f.close()
    if not path_using in paths:
        paths.append(path_using)
        with open('path.txt', 'w', encoding='utf-8') as f:
            for i in paths:
                f.write(i + '\n')
            f.close()
        os.system(os.path.join(os.getcwd(), 'restartmonitor.bat'))


def delete_from_monitor():
    global path_using
    with open('path.txt', 'r', encoding='utf-8') as f:
        paths = f.read().splitlines()
        f.close()
    if path_using in paths:
        paths.remove(path_using)
        with open('path.txt', 'w', encoding='utf-8') as f:
            for i in paths:
                f.write(i + '\n')
            f.close()
        os.system(os.path.join(os.getcwd(), 'restartmonitor.bat'))
# 复制文件
# def copy(path1, path2):
#     global exit_flag
#     # print(path2)
#     try:
#         shutil.copytree(path1, path2)
#         print('Done', flush=True)
#     except:
#         print('\nerror:无法复制文件。请手动删除当前文件夹下的.filemanager文件夹重试，或关机重启后重试。')
#     exit_flag = True


def create_id():
    m = hashlib.md5()
    m.update(bytes(str(time.perf_counter()), encoding='utf-8'))
    return m.hexdigest()


def copy(path1, path2):
    # global progress
    global exit_flag
    global all_size
    print(path1)
    # with Progress() as progress:
    top = Toplevel()
    top.title('Copying......')
    icon_for_window(top)

    pb = Progressbar(top, length=200, mode="determinate", orient=HORIZONTAL)
    pb.pack(padx=10, pady=20)
    pb["maximum"] = all_size
    pb["value"] = 0
    # pb["value"] += 1000
    top.protocol('WM_DELETE_WINDOW', callback)  # 窗体的通信协议方法
    top.update()

    for root, dirs, files in os.walk(path1):
        if os.path.basename(root) == ".filemanager":
            dirs[:] = []  # 忽略当前目录下的子目录
            # os.mkdir(os.path.join(root,r'.filemnager/base'))
        for name in files:
            sourname = os.path.join(root, name)
            targetname = os.path.join(path2, os.path.relpath(
                os.path.join(root, name), path1))
            if not os.path.exists(os.path.dirname(targetname)):
                os.makedirs(os.path.dirname(targetname))
            thisadd = os.path.getsize(sourname)/1024
            shutil.copy(sourname, targetname)
            # open(targetname,'wb').write(open(sourname,'rb').read())

            pb["value"] += thisadd
            top.update()
    top.destroy()

    exit_flag = True


def createtimestamp(path1, filename):
    # global progress
    global all_number
    # time.sleep(0.1)  # 等创建文件目录
    if not os.path.exists(os.path.join(path1, '.filemanager', 'main')):
        os.makedirs(os.path.join(path1, '.filemanager', 'main'))
    if not os.path.exists(os.path.join(path1, '.filemanager', 'commits')):
        os.makedirs(os.path.join(path1, '.filemanager', 'commits'))
    with open(os.path.join(path1, '.filemanager', 'main', filename), "w", encoding='utf-8') as p:
        p.write('dir,timestamp,hash' + "\n")
        p.close()
    # with Progress() as progress:

    top = Toplevel()
    top.title('Timestamping......')
    icon_for_window(top)
    pb = Progressbar(top, length=200, mode="determinate", orient=HORIZONTAL)
    pb.pack(padx=10, pady=20)
    pb["maximum"] = all_number
    pb["value"] = 0
    # pb["value"] += 1000
    top.protocol('WM_DELETE_WINDOW', callback)  # 窗体的通信协议方法
    top.update()
    print(2)
    with open(os.path.join(path1, '.filemanager', 'main', filename), "a", encoding='utf-8') as p:
        for root, dirs, files in os.walk(path1):
            if os.path.basename(root) == ".filemanager":
                dirs[:] = []  # 忽略当前目录下的子目录
            for name in files:
                p.write(os.path.relpath(os.path.join(root, name), path1) +
                        ','+str(round(os.stat(root + '/' + name).st_mtime))+',-1\n')
                pb["value"] += 1
                top.update()
        p.close()
    top.destroy()

# 等待动画
# def wait():
#     global exit_flag
#     while True:
#         for ch in ['-', '\\', '|', '/']:
#             print('\b%s' % ch, end='', flush=True)
#             time.sleep(0.1)
#             if exit_flag:
#                 break
#         if exit_flag:
#             break


def refreash(path_in, terminal):
    global inited_all_number, adder_opened
    global changes
    walk_loaded = {}
    csv_read = {}
    csv_read_hash = {}
    change = []
    deleted_files = {}
    new_files = {}
    delete = []
    create = []
    # 读取保存的时间戳
    f = csv.reader(open(os.path.join(path_in, '.filemanager',
                   'main', 'timestamp.csv'), 'r', encoding='utf-8'))
    for i in f:
        csv_read[i[0]] = i[1]
        csv_read_hash[i[0]] = i[2]

    top = Toplevel()
    top.title('Refreashing......')
    icon_for_window(top)

    pb = Progressbar(top, length=200, mode="determinate", orient=HORIZONTAL)
    pb.pack(padx=10, pady=20)
    pb["maximum"] = inited_all_number
    pb["value"] = 0
    # pb["value"] += 1000
    top.protocol('WM_DELETE_WINDOW', callback)  # 窗体的通信协议方法
    top.update()

    passed_files = 0
    for root, dirs, files in os.walk(path_in):
        if os.path.basename(root) == ".filemanager":
            dirs[:] = []  # 忽略当前目录下的子目录
        for name in files:
            pb["value"] = passed_files      # 每次更新1
            top.update()
            mtime = round(os.stat(os.path.join(root, name)).st_mtime)
            dir_path = os.path.relpath(os.path.join(root, name), path_in)
            walk_loaded[dir_path] = str(mtime)
            # progress.update(task3, advance=1)
            passed_files += 1
            # pb["value"] = passed_files      # 每次更新1
            # top.update()
            # print(passed_files)
            # terminal.insert('end','\n'+str(mtime))
        # progress.update(task3, advance=inited_all_number)
    top.destroy()

    # 比较不同
    diff = walk_loaded.keys() & csv_read
    # 路径一样，时间戳不一样→更改的文件
    diff_vals = [(k, walk_loaded[k], csv_read[k])
                 for k in diff if walk_loaded[k] != csv_read[k]]

    # 存在于存储得时间戳路径，现在不存在了→删除的文件
    deleted_files = csv_read.keys() - walk_loaded.keys()

    # 没有记录的文件→新建的文件
    new_files = walk_loaded.keys() - csv_read.keys()

    # deleted_files = csv_read.keys() - walk_loaded.keys()
    # new_files = walk_loaded.keys() - csv_read.keys()

    timestamp_to_change = []
    # 把文件写入数组
    for i in diff_vals:
        i_hash = hash(os.path.join(path_in, i[0]))
        if not i_hash == csv_read_hash[i[0]]:
            change.append(i[0])
        else:
            timestamp_to_change.append(i[0])

    with open(os.path.join(path_in, '.filemanager', 'main', 'timestamp.csv'), 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        f.close()
    timestamp_splited = []
    for i in lines:
        timestamp_splited.append(i.split(','))
    while True:
        for i in timestamp_to_change:
            for path in range(len(timestamp_splited)):
                # print(pth[0])
                # print(path)
                if i == timestamp_splited[path][0]:
                    mtime = str(
                        round(os.stat(os.path.join(path_using, timestamp_splited[path][0])).st_mtime))
                    timestamp_splited[path][1] = mtime
                    timestamp_to_change.remove(i)
                    break
        if timestamp_to_change == []:
            break
    with open(os.path.join(path_in, '.filemanager', 'main', 'timestamp.csv'), 'w', encoding='utf-8') as f:
        for i in timestamp_splited:
            f.write('{0},{1},{2}\n'.format(i[0], i[1], i[2]))

    for i in deleted_files:
        if not i == 'dir':
            delete.append(i)
    for i in new_files:
        create.append(i)

    # 忽略
    if os.path.exists(os.path.join(path_using, '.ignore')):
        with open(os.path.join(path_using, '.ignore'), 'r', encoding='utf-8-sig') as f:
            text = f.read().splitlines()
            f.close()
        patterns = []
        for s in text:
            # ^ $ .  +  -  = !     ( ) [ ] { }
            s = s.replace('?', '.').replace('*', '.*').replace('^', '\^').replace('$', '\$').replace('.', '\.').replace('+', '\+').replace('-', '\-').replace(
                '=', '\=').replace('!', '\!').replace(' ', '\s').replace('(', '\(').replace(')', '\)').replace('[', '\[').replace(']', '\]').replace('{', '\{').replace('}', '\}')
            if len(s) != 0 and s[0] != '#':
                if s[len(s)-1] == '\\':
                    temp = list(s)
                    del temp[len(temp)-1]
                    temp.append('\\\\.*')
                    s = ''.join(temp)
                    pattern = re.compile(f"{s}$")
                    patterns.append(pattern)

                if s[0] == '\\':
                    temp = list(s)
                    temp[0] = '.*\\\\'
                    s = ''.join(temp)
                    pattern = re.compile(f"{s}$")
                    patterns.append(pattern)
                    del temp[0]
                    s = ''.join(temp)
                    pattern = re.compile(f"{s}$")
                    patterns.append(pattern)

        remove_list = []
        for e in change:
            for pattern in patterns:
                if pattern.match(e):
                    remove_list.append(e)
                    break

        change = list(set(change) - set(remove_list))

        for e in delete:
            for pattern in patterns:
                if pattern.match(e):
                    remove_list.append(e)
                    break

        delete = list(set(delete) - set(remove_list))

        for e in create:
            for pattern in patterns:
                if pattern.match(e):
                    remove_list.append(e)
                    break

        create = list(set(create) - set(remove_list))

    changes['changes'] = change
    changes['delete'] = delete
    changes['create'] = create

    # 写入now_list_doing.csv,方便reload查找
    with open(os.path.join(path_in, '.filemanager', 'main', 'now_list_doing.csv'), 'w', encoding='utf-8') as f:
        for i in changes['changes']:
            f.write('file_modified,' + i + '\n')
        for i in changes['delete']:
            f.write('file_deleted,' + i + '\n')
        for i in changes['create']:
            f.write('file_created,' + i + '\n')
        f.close()

    # terminal.insert('end', '\n' + str(changes) + '\n')
    terminal.insert('end', 'Done')
    printchanges(changes, terminal, 'changes')

    walk_loaded = {}
    csv_read = {}
    change = []
    deleted_files = {}
    new_files = {}
    delete = []
    create = []


def reload(path_in, terminal):
    global changes
    csv_read = {}
    csv_read_hash = {}
    # 获取当前timestamp
    exit_flag = False
    while True:
        for ch in ['-', '\\', '|', '/']:
            terminal.insert('end', '\nWaiting......' + ch)
            # terminal.config(state='d')
            terminal.update()
            terminal.see('end')
            time.sleep(0.1)
            timestamp = round(time.time())
            m_time = round(os.stat(os.path.join(
                path_in, '.filemanager', 'main', 'now_list_doing.csv')).st_mtime)
            if timestamp - m_time > 10:
                exit_flag = True
                break
            else:
                print(int(terminal.index('end-1c').split('.')[0]))
                terminal.delete(terminal.index(
                    'end-1c').split('.')[0]+'.0', 'end')
        if exit_flag:
            terminal.delete(terminal.index('end-1c').split('.')[0]+'.0', 'end')
            terminal.insert('end', '\nWaiting......Done.')
            break
            # time.sleep(1)

    with open(os.path.join(path_in, '.filemanager', 'main', 'now_list_doing.csv'), 'r+', encoding='utf-8') as f:
        processed = f.read().splitlines()
    for i in processed:
        line = i.split(',')
        if len(line) == 3:
            if line[2] in changes['delete']:
                changes['delete'].remove(line[2])
            if line[2] in changes['changes']:
                changes['changes'].remove(line[2])
            changes['create'].append(line[2])

            if line[1] in changes['create']:
                changes['create'].remove(line[1])
            elif not line[1] in changes['delete']:
                changes['delete'].append(line[1])

        else:
            if line[0] == 'file_created':
                # if line[1] in changes['delete']:
                #     changes['create'].remove(line[1])
                # elif not line[1] in changes['delete']:
                #     changes['delete'].append(line[1])
                if line[1] in changes['delete']:
                    changes['delete'].remove(line[1])
                if line[1] in changes['changes']:
                    changes['changes'].remove(line[1])
                if line[1] not in changes['create']:
                    changes['create'].append(line[1])

            elif line[0] == 'file_deleted':
                if line[1] in changes['create']:
                    changes['create'].remove(line[1])
                elif not line[1] in changes['delete']:
                    changes['delete'].append(line[1])
                # if line[1] in changes['create']:
                #     changes['create'].remove(line[1])
                if line[1] in changes['changes']:
                    changes['changes'].remove(line[1])
                # elif not line[1] in changes['delete']:
                #     changes['delete'].append(line[1])

            elif line[0] == 'file_modified':
                if not line[1] in changes['changes'] and not line[1] in changes['create']:
                    changes['changes'].append(line[1])

    f = csv.reader(open(os.path.join(path_in, '.filemanager',
                   'main', 'timestamp.csv'), 'r', encoding='utf-8'))
    for i in f:
        csv_read[i[0]] = i[1]
        csv_read_hash[i[0]] = i[2]

    keys = list(csv_read.keys())

    num_new = 0
    num_old = 1
    timestamp_to_change = []
    while num_new != num_old:
        num_old = num_new
        for i in changes['changes']:
            i_hash = hash(os.path.join(path_in, i))
            if i in keys and i_hash != csv_read_hash[i]:
                mtime = round(os.stat(os.path.join(path_in, i)).st_mtime)
                if str(mtime) != csv_read[i]:
                    pass
            elif i in keys and i_hash == csv_read_hash[i]:
                timestamp_to_change.append(i)
            else:
                changes['changes'].remove(i)
                # processed.remove
        num_new = len(changes['changes'])

    num_new = 0
    num_old = 1
    while num_new != num_old:
        num_old = num_new
        for i in changes['delete']:  # 有BUG????
            if not i in keys:
                changes['delete'].remove(i)
        num_new = len(changes['delete'])

    num_new = 0
    num_old = 1
    while num_new != num_old:
        num_old = num_new
        for i in changes['create']:  # 有BUG????
            if not os.path.exists(os.path.join(path_in, i)):
                changes['create'].remove(i)
        num_new = len(changes['create'])

# 忽略
    if os.path.exists(os.path.join(path_using, '.ignore')):
        with open(os.path.join(path_using, '.ignore'), 'r', encoding='utf-8-sig') as f:
            text = f.read().splitlines()
            f.close()
        patterns = []
        for s in text:
            # ^ $ .  +  -  = !     ( ) [ ] { }
            s = s.replace('?', '.').replace('*', '.*').replace('^', '\^').replace('$', '\$').replace('.', '\.').replace('+', '\+').replace('-', '\-').replace(
                '=', '\=').replace('!', '\!').replace(' ', '\s').replace('(', '\(').replace(')', '\)').replace('[', '\[').replace(']', '\]').replace('{', '\{').replace('}', '\}')
            if len(s) != 0 and s[0] != '#':
                if s[len(s)-1] == '\\':
                    temp = list(s)
                    del temp[len(temp)-1]
                    temp.append('\\\\.*')
                    s = ''.join(temp)
                    pattern = re.compile(f"{s}$")
                    patterns.append(pattern)

                if s[0] == '\\':
                    temp = list(s)
                    temp[0] = '.*\\\\'
                    s = ''.join(temp)
                    pattern = re.compile(f"{s}$")
                    patterns.append(pattern)
                    del temp[0]
                    s = ''.join(temp)
                    pattern = re.compile(f"{s}$")
                    patterns.append(pattern)

            remove_list = []
            for e in changes['changes']:
                for pattern in patterns:
                    if pattern.match(e):
                        remove_list.append(e)
                        break

            changes['changes'] = list(
                set(changes['changes']) - set(remove_list))

            for e in changes['delete']:
                for pattern in patterns:
                    if pattern.match(e):
                        remove_list.append(e)
                        break

            changes['delete'] = list(set(changes['delete']) - set(remove_list))

            for e in changes['create']:
                for pattern in patterns:
                    if pattern.match(e):
                        remove_list.append(e)
                        break

            changes['create'] = list(set(changes['create']) - set(remove_list))

    # 更新timestamp.csv
    with open(os.path.join(path_in, '.filemanager', 'main', 'timestamp.csv'), 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        f.close()
    timestamp_splited = []
    for i in lines:
        timestamp_splited.append(i.split(','))
    while True:
        for i in timestamp_to_change:
            for path in range(len(timestamp_splited)):
                # print(pth[0])
                # print(path)
                if i == timestamp_splited[path][0]:
                    mtime = str(
                        round(os.stat(os.path.join(path_using, timestamp_splited[path][0])).st_mtime))
                    timestamp_splited[path][1] = mtime
                    timestamp_to_change.remove(i)
                    changes['changes'].remove(i)
                    break
        if timestamp_to_change == []:
            break
    with open(os.path.join(path_in, '.filemanager', 'main', 'timestamp.csv'), 'w', encoding='utf-8') as f:
        for i in timestamp_splited:
            f.write('{0},{1},{2}\n'.format(i[0], i[1], i[2]))

    with open(os.path.join(path_in, '.filemanager', 'main', 'now_list_doing.csv'), 'w', encoding='utf-8') as f:
        for i in changes['changes']:
            f.write('file_modified,' + i + '\n')
        for i in changes['delete']:
            f.write('file_deleted,' + i + '\n')
        for i in changes['create']:
            f.write('file_created,' + i + '\n')
        f.close()

    with open(f'{os.getcwd()}\path.txt', 'r', encoding='utf-8') as f:
        paths = f.read().splitlines()
        f.close()
    if not path_in in paths:
        terminal.insert('end', '\nWARNING:位于{0}的仓库并没有被monitor所监控，您的更改可能不会被察觉。请使用"refreash"命令以加载完整变更。'.format(
            str(path_in)), 'yellow')

# 新建仓库的命令


def newrepo(path_in, terminal):
    global info_add
    global exit_flag
    global all_size
    global all_number
    global start_path
    global inited
    # print(path_in)
    terminal.insert('end', '\nBuilding......')

    # 这已经是一个仓库了
    if os.path.exists(os.path.join(path_in, '.filemanager', 'main', 'id.txt')):
        # choose = input('这已经是一个filemanager仓库了。您想读取它吗？(y/N)')
        # if choose == 'y' or choose == 'Y':
        #     init(terminal)
        terminal.insert('end', '\nerror:这已经是一个filemanager仓库了', 'red')

    else:
        paths = []
        # 计算新仓库内文件总数
        for root, dirs, files in os.walk(path_in):
            if os.path.basename(root) == ".filemanager":
                dirs[:] = []  # 忽略当前目录下的子目录
            # os.mkdir(os.path.join(root,r'.filemnager/base'))
            for name in files:
                file_relpath = os.path.relpath(
                    os.path.join(root, name), path_in)
                paths.append(file_relpath)
                all_size += os.path.getsize(os.path.join(root, name))/1024
                all_number += 1

        timestamp = round(time.time()*100)
        str_timestamp = str(timestamp)
    # os.startfile("G:\TEST0\GIT\\filemanager\copier\copier.exe")
        # c1 = threading.Thread(target=copy,args=(path_in, os.path.join(path_in,r'.filemanager\base')))
        copy(path_in, os.path.join(path_in, r'.filemanager\commits', str_timestamp))
        createtimestamp(path_in, 'timestamp.csv')
        with open(os.path.join(path_in, '.filemanager', 'main', 'timestamp.csv'), "r", encoding='utf-8') as p:
            loaded_timestamp = p.read().splitlines()
            p.close()
        del loaded_timestamp[0]
        with open(os.path.join(path_in, '.filemanager', 'main', 'timestamp.csv'), "w", encoding='utf-8') as p:
            p.write('dir,timestamp,hash\n')
            for i in loaded_timestamp:
                p.write(i + ',-1\n')
            p.close()
        writefilehash(paths)
        # c1 = threading.Thread(target=copy, args=(
        #     path_in, os.path.join(path_in, r'.filemanager\base')))
        # c2 = threading.Thread(target=createtimestamp,
        #                         args=(path_in, 'timestamp.csv'))
        #     # c3 = threading.Thread(target=wait)

        # c1.start()
        # c2.start()
        # # c3.start()
        # c1.join()
        # c2.join()
        # c1.setDaemon(True)
        # c2.setDaemon(True)
        # c3.join()
        # gettimestamp(path_in, os.path.join(path_in,r'.filemanager\base'))
        # csvFile = open(csv_path, "r+", encoding='utf-8')
        # f = os.popen('attrib +h ' + os.path.join(path_in, '.filemanager'))
        # f.close()

        with open(os.path.join(path_in, 'hide.bat'), 'w', encoding='utf-8') as f:
            f.write('Attrib +h .filemanager\n')
            f.write('del /S /Q hide.bat')
            f.close()
        os.chdir(path_using)
        os.system('hide.bat')
        os.chdir(start_path)

        all_size = 0
        all_number = 0

        ok = False
        ids = 0

        new_id = create_id()
        with open(os.path.join(start_path, 'id.txt'), "r", encoding='utf-8') as f:
            id = f.read().splitlines()
            f.close()
        while ok:
            for i in id:
                if i != new_id:
                    ids += 1
                else:
                    new_id = create_id()
            if ids == len(id):
                ok = True
        with open(os.path.join(start_path, 'id.txt'), "a", encoding='utf-8') as f:
            f.write(new_id + "\n")
            f.close()

        with open(os.path.join(path_in, '.filemanager', 'main', 'id.txt'), "w", encoding='utf-8') as f:
            f.write(new_id)
            f.close()

        if not os.path.exists(os.path.join(path_in, '.filemanager', 'main', 'commits')):
            os.makedirs(os.path.join(
                path_in, '.filemanager', 'main', 'commits'))

        if not os.path.exists(os.path.join(path_in, '.filemanager', 'main', 'now_list_doing.csv')):
            with open(os.path.join(path_in, '.filemanager', 'main', 'now_list_doing.csv'), 'w', encoding='utf-8') as f:
                f.close()

        # 创建新分支
        new_branch = [{'start': -1, 'include': {0: "新建仓库"}, 'end': -1}]
        write_branch(new_branch)

        terminal.insert('end', 'Done\n')

        # 提交timestamp
        try:
            if not os.path.exists(os.path.join(path_in, '.filemanager', 'main', 'commits', str_timestamp)):
                os.makedirs(os.path.join(path_in, '.filemanager',
                            'main', 'commits', str_timestamp))
            shutil.copy(os.path.join(path_in, '.filemanager', 'main', 'timestamp.csv'), os.path.join(
                path_in, '.filemanager', 'main', 'commits', str_timestamp, 'timestamp.csv'))
        except:
            terminal.insert('end', '\nerror:提交文件' +
                            str(os.path.join(path_in, '.filemanager', 'main', 'timestamp.csv'))+'失败\n', 'red')

        # 写入版本
        with open(os.path.join(path_in, '.filemanager', 'main', 'version.txt'), "w", encoding='utf-8') as f:
            f.write(terminal_infos.version)
            f.close()


def adder(terminal, command):
    def callRB():
        global mode
        mode = mode_to_select[v.get()][2]

    def drag_files(urls):
        print(urls)
        paths = ''
        decodedpaths = []
        for i in urls:
            try:
                decodedpaths.append(i.decode("gb18030"))
            except:
                try:
                    decodedpaths.append(i.decode("utf-8"))
                except:
                    paths += 'error:添加:' + i + '失败\n'

        print(decodedpaths)
        # for i in urls:
        #     print((i).decode("utf-8"))
        # showinfo('确认路径', b'\n'.join(urls).decode())

        paths += '请确认:以下是' + mode + '路径:\n'
        paths += '\n'.join(decodedpaths)
        if askokcancel('请确认:' + mode + '路径', str(paths)):
            # 我也不知道为什么，这个延时不能再短了，不然它会崩溃...
            time.sleep(1)
            path_to_process_list = decodedpaths
            dirs = []
            files = []
            for i in path_to_process_list:
                if os.path.isdir(i):
                    if not '.filemanager' in i:
                        dirs.append(i)
                else:
                    files.append(i)
            if dirs != []:
                command_inputed = []
                command_inputed.append('add')
                command_inputed.append('-d')
                command_inputed.append(mode)
                add(terminal, dirs, command_inputed)

            if files != []:
                command_inputed = []
                command_inputed.append('add')
                command_inputed.append('-f')
                command_inputed.append(mode)
                add(terminal, files, command_inputed)

                # showinfo('确认路径', b'\n'.join(urls).decode())
    global mode, adder_opened, top

    def exitbutton():
        global adder_opened
        adder_opened = False
        top.destroy()

    if command == '!destroy':
        if adder_opened:
            exitbutton()

    else:
        if not adder_opened:
            adder_opened = True
            mode = '+'
            top = Toplevel()
            top.title('添加/移除文件(文件夹)')
            top.wm_attributes('-topmost', 1)
            top.geometry("350x100")
            top.resizable(False, False)
            icon_for_window(top)

            v = IntVar()

            # ent = tkinter.Entry(top).pack()
            # ent = tkinter.Entry(top, width=100).grid(row=0)
            label = Label(top, text='拖拽文件或文件夹至此', font=15, pady=20)
            label.pack()
            Radiobutton(top, text='添加文件', value=0, command=callRB,
                        variable=v).pack(side=LEFT, expand=True)
            Radiobutton(top, text='移除文件', value=1, command=callRB,
                        variable=v).pack(side=RIGHT, expand=True)

            windnd.hook_dropfiles(top, func=drag_files)
            # 进入消息循环
            # top.mainloop()
            top.protocol('WM_DELETE_WINDOW', exitbutton)


def add(terminal, paths, command_inputed):
    global inited, changes, process_path, path_using
    if inited:
        if len(command_inputed) == 1:
            adder(terminal, 'add')

        elif command_inputed[1] == '.':
            for i in changes['changes']:
                if not i in process_path['changes']:
                    process_path['changes'].append(i)
            for i in changes['delete']:
                if not i in process_path['delete']:
                    process_path['delete'].append(i)
            for i in changes['create']:
                if not i in process_path['create']:
                    process_path['create'].append(i)
            # process_path = changes
        elif command_inputed[1] == 'clear':
            process_path = {'changes': [], 'delete': [], 'create': []}

        # elif '+' in command_inputed:
        elif '-f' in command_inputed:
            if paths != []:
                file_path = paths
            else:
                file_path = filedialog.askopenfilenames(initialdir=path_using)
            if '+' in command_inputed:
                for i in file_path:
                    sourname = os.path.relpath(i, path_using)
                    if sourname in changes['changes'] and sourname not in process_path['changes']:
                        process_path['changes'].append(sourname)
                    if sourname in changes['delete'] and sourname not in process_path['delete']:
                        process_path['delete'].append(sourname)
                    if sourname in changes['create'] and sourname not in process_path['create']:
                        process_path['create'].append(sourname)

            elif '-' in command_inputed:
                for i in file_path:
                    sourname = os.path.relpath(i, path_using)
                    if sourname in process_path['changes']:
                        process_path['changes'].remove(sourname)
                    if sourname in process_path['delete']:
                        process_path['delete'].remove(sourname)
                    if sourname in process_path['create']:
                        process_path['create'].remove(sourname)

        elif '-d' in command_inputed:
            if paths != []:
                folder_path = paths
            else:
                folder_path = []
                folder_path.append(
                    filedialog.askdirectory(initialdir=path_using))
            if '+' in command_inputed:
                for i in folder_path:
                    for root, dirs, files in os.walk(i):
                        if os.path.basename(root) == ".filemanager":
                            dirs[:] = []  # 忽略当前目录下的子目录
                            # os.mkdir(os.path.join(root,r'.filemnager/base'))
                        for name in files:
                            sourname = os.path.relpath(
                                os.path.join(root, name), path_using)
                            if sourname in changes['changes'] and sourname not in process_path['changes']:
                                process_path['changes'].append(sourname)
                            if sourname in changes['delete'] and sourname not in process_path['delete']:
                                process_path['delete'].append(sourname)
                            if sourname in changes['create'] and sourname not in process_path['create']:
                                process_path['create'].append(sourname)

            elif '-' in command_inputed:
                for i in folder_path:
                    for root, dirs, files in os.walk(i):
                        if os.path.basename(root) == ".filemanager":
                            dirs[:] = []  # 忽略当前目录下的子目录
                            # os.mkdir(os.path.join(root,r'.filemnager/base'))
                        for name in files:
                            sourname = os.path.relpath(
                                os.path.join(root, name), path_using)
                            if sourname in process_path['changes']:
                                process_path['changes'].remove(sourname)
                            if sourname in process_path['delete']:
                                process_path['delete'].remove(sourname)
                            if sourname in process_path['create']:
                                process_path['create'].remove(sourname)

        printchanges(process_path, terminal, 'changes')

    else:
        terminal.insert('end', '\nerror:您还没有加载这个仓库', 'red')


def commit(terminal, str_timestamp_in):
    # print(changes['delete'])
    # print('True')
    global commit_text
    global process_path
    global path_using
    global now_at
    global changes
    commit_size = 0
    commit_files_number = 0
    changes_path = []
    delete_path = []
    copy_path = []

    # 计算提交的文件的大小
    for i in process_path['changes']:
        commit_size += os.path.getsize(os.path.join(path_using, i))/1024
        commit_files_number += 1
        copy_path.append(i)
    # for i in process_path['delete']:
    #     commit_size += os.path.getsize(os.path.join(path_using, i))/1024
    for i in process_path['create']:
        commit_size += os.path.getsize(os.path.join(path_using, i))/1024
        commit_files_number += 1
        copy_path.append(i)

    # 获取当前timestamp
    if str_timestamp_in != '':
        str_timestamp = str_timestamp_in
    else:
        timestamp = round(time.time()*100)
        str_timestamp = str(timestamp)

    # if os.path.exists(os.path.join(path_using, '.filemanager', 'commits', str_timestamp)):
    #     shutil.rmtree(os.path.join(path_using, '.filemanager', 'commits', str_timestamp))

    if not os.path.exists(os.path.join(path_using, '.filemanager', 'commits', str_timestamp)):
        os.makedirs(os.path.join(
            path_using, '.filemanager', 'commits', str_timestamp))

    # 复制文件进度条
    top = Toplevel()
    top.title('Committing......')
    icon_for_window(top)

    pb = Progressbar(top, length=200, mode="determinate", orient=HORIZONTAL)
    pb.pack(padx=10, pady=20)
    pb["maximum"] = commit_size
    pb["value"] = 0
    # pb["value"] += 1000
    top.protocol('WM_DELETE_WINDOW', callback)  # 窗体的通信协议方法
    top.update()

    for i in copy_path:
        if not os.path.exists(os.path.dirname(os.path.join(path_using, '.filemanager', 'commits', str_timestamp, i))):
            os.makedirs(os.path.dirname(os.path.join(
                path_using, '.filemanager', 'commits', str_timestamp, i)))
        try:
            shutil.copy(os.path.join(path_using, i), os.path.join(
                path_using, '.filemanager', 'commits', str_timestamp, i))
        except:
            terminal.insert('end', '\nerror:提交文件' +
                            str(os.path.join(path_using, i))+'失败\n', 'red')
        pb["value"] += os.path.getsize(os.path.join(path_using, i))/1024
        top.update()
    top.destroy()

    # 读取timestamp
    with open(os.path.join(path_using, '.filemanager', 'main', 'timestamp.csv'), "r", encoding='utf-8') as p:
        timestamps = p.read().splitlines()
        p.close()

    # 更新timestamp
    with open(os.path.join(path_using, '.filemanager', 'main', 'timestamp.csv'), "w", encoding='utf-8') as p:

        number = 0

        for i in process_path['changes']:
            changes_path.append(i)

        for i in process_path['delete']:
            delete_path.append(i)

        # 更新有改变的文件的timestamp
        while True:
            for i in timestamps:
                pth = i.split(',')
                for path in changes_path:
                    # print(pth[0])
                    # print(path)
                    if pth[0] == path:
                        mtime = str(
                            round(os.stat(os.path.join(path_using, path)).st_mtime))
                        pth[1] = mtime
                        changes_path.remove(path)
                        timestamps[number] = pth[0] + ',' + pth[1] + ',-1'
                        # print(number)
                number += 1
            if changes_path == []:
                break

        # 删除删除了的文件的timestamp
        while True:
            number = 0
            for i in timestamps:
                pth = i.split(',')
                for path2 in delete_path:
                    # for n in range(0,len(delete_path)):
                    if pth[0] == path2:
                        print(path2)
                        # changes_path.remove(path)
                        del timestamps[number]
                        delete_path.remove(path2)
                        # print(number)
                number += 1
            if delete_path == []:
                break

        # 为新建的文件添加timestamp
        for path in process_path['create']:
            mtime = str(
                round(os.stat(os.path.join(path_using, path)).st_mtime))
            timestamps.append(path + ',' + mtime + ',-1')

        for i in timestamps:
            p.write(i + '\n')
        p.close()

        # 更新hash值
        writefilehash(copy_path)

        # 记录提交注释
        if not os.path.exists(os.path.join(path_using, '.filemanager', 'main', 'commits', str_timestamp)):
            os.makedirs(os.path.join(path_using, '.filemanager',
                        'main', 'commits', str_timestamp))
        with open(os.path.join(path_using, '.filemanager', 'main', 'commits', str_timestamp, 'note'), 'w', encoding='utf-8') as f:
            f.write(commit_text)
            f.close()

        # 记录提交的变更
        with open(os.path.join(path_using, '.filemanager', 'main', 'commits', str_timestamp, 'changes'), 'w', encoding='utf-8') as f:
            for i in process_path['changes']:
                f.write(i + '\n')
            f.close()
        with open(os.path.join(path_using, '.filemanager', 'main', 'commits', str_timestamp, 'delete'), 'w', encoding='utf-8') as f:
            for i in process_path['delete']:
                f.write(i + '\n')
            f.close()
        with open(os.path.join(path_using, '.filemanager', 'main', 'commits', str_timestamp, 'create'), 'w', encoding='utf-8') as f:
            for i in process_path['create']:
                f.write(i + '\n')
            f.close()

        # 提交timestamp.csv
        # if os.path.exists(os.path.join(path_using, '.filemanager', 'main', 'commits', str_timestamp, 'create')):
    try:
        if os.path.exists(os.path.join(path_using, '.filemanager', 'main', 'commits', str_timestamp, 'timestamp.csv')):
            os.remove(os.path.join(path_using, '.filemanager', 'main',
                      'commits', str_timestamp, 'timestamp.csv'))
        shutil.copy(os.path.join(path_using, '.filemanager', 'main', 'timestamp.csv'), os.path.join(
            path_using, '.filemanager', 'main', 'commits', str_timestamp, 'timestamp.csv'))
    except:
        terminal.insert('end', '\nerror:提交timestamp失败', 'red')

    with open(os.path.join(path_using, '.filemanager', 'main', 'now_list_doing.csv'), 'r+', encoding='utf-8') as f:
        chan = f.read().splitlines()
        f.close()

    out = []
    for i in chan:
        out.append(i.split(','))

    for i in out:
        if i[1] in process_path['changes']:
            out.remove(i)

    for i in out:
        if i[1] in process_path['delete']:
            out.remove(i)

    for i in out:
        if i[1] in process_path['create']:
            out.remove(i)

    with open(os.path.join(path_using, '.filemanager', 'main', 'now_list_doing.csv'), 'w', encoding='utf-8') as f:
        if out != []:
            for i in out:
                f.write(i[0] + ',' + i[1] + '\n')
        else:
            f.write('')
        f.close()

    changes['changes'] = list(
        set(changes['changes']) - set(process_path['changes']))
    changes['delete'] = list(set(changes['delete']) -
                             set(process_path['delete']))
    changes['create'] = list(set(changes['create']) -
                             set(process_path['create']))
    process_path = {'changes': [], 'delete': [], 'create': []}

    f = open(os.path.join(path_using, '.filemanager',
             'main', 'branches.json'), 'r', encoding='utf-8')
    info_data = json.load(f)
    f.close()
    branch_input = info_data['branches']
    branch = []

    # 读取并写入分支
    branch_len = 0
    for i in range(len(branch_input)):
        branch.append({'start': int(branch_input[i]['start']), 'include': {
        }, 'end': int(branch_input[i]['end'])})
        for j in branch_input[i]['include'].keys():
            try:
                branch[i]['include'][int(j)] = branch_input[i]['include'][j]
                if int(j) > branch_len:
                    branch_len = int(j)
            except:
                pass

    if str_timestamp_in == '':

        now_branch_max_commit = 0

        for i in range(len(branch)):
            if now_at in list(branch[i]['include'].keys()):
                now_at_branch = i
                for j in list(branch[i]['include'].keys()):
                    if int(j) > now_branch_max_commit:
                        now_branch_max_commit = int(j)
                break
        # new_branch = [{'start': -1, 'include':{0:"新建仓库"}, 'end': -1}]
        if now_at == now_branch_max_commit:
            branch[now_at_branch]['include'][branch_len+1] = commit_text
        else:
            new_branch = {'start': now_at, 'include': {
                branch_len+1: commit_text}, 'end': -1}
            branch.append(new_branch)
        now_at = branch_len + 1
        branch_len = 0

    else:
        for i in range(len(branch)):
            if now_at in branch[i]['include'].keys():
                branch[i]['include'][now_at] = commit_text
                break

    write_branch(branch)
    print_branch(terminal)
    printchanges(changes, terminal, '!destroy')
    if changes == {'changes': [], 'delete': [], 'create': []}:
        adder(terminal, '!destory')
    else:
        printchanges(changes, terminal, 'changes')


def show_changes_in_box(inputen, terminal, mode):
    global deletes, path_using, window_opened, postwin, processlist, changeslist, changes
    v = StringVar()
    v2 = StringVar()

    def delete():
        global command_inputed, deletes
        items = list(map(int, processlist.curselection()))
        if(len(items) == 0):
            print("No items")
        else:
            print(items)
            before_delete = set(eval(v2.get()))
            for i in items:
                processlist.delete(i)
                for j in range(len(items)):
                    items[j] -= 1

            # print(v.get())

            after_delete = set(eval(v2.get()))

            for i in list(before_delete - after_delete):
                deletes.append(os.path.join(path_using, i))

            print(deletes)
            command_inputed = []
            command_inputed.append('add')
            command_inputed.append('-f')
            command_inputed.append('+')
            adds = []
            for i in list(after_delete):
                adds.append((os.path.join(path_using, i)))
            if adds != []:
                add(terminal, adds, command_inputed)
                command_inputed = []
                command_inputed.append('add')
                command_inputed.append('-f')
                command_inputed.append('-')
                add(terminal, deletes, command_inputed)
                deletes = []
            else:
                command_inputed[2] = '+'
                add(inputen, [], command_inputed)

    def add_():
        global command_inputed, deletes
        items = list(map(int, changeslist.curselection()))

        if(len(items) == 0):
            print("No items")
        else:
            print(items)
            lists = list(eval(v.get()))
            exists = list(eval(v2.get()))

            for i in items:
                if not lists[i] in exists:
                    processlist.insert('end', lists[i])

    def close():
        global window_opened
        window_opened = False
        postwin.destroy()

        # print(list(eval(v.get())))
    # 弹出效果展示中的命令列表
    if not window_opened:
        window_opened = True
        postwin = tk.Toplevel(root)
        icon_for_window(postwin)
        postwin.title('ChangesList')
        postwin.geometry('650x400')
        postwin.transient(root)
        postwin.protocol('WM_DELETE_WINDOW', close)

    #     TerminalText = tk.ScrolledText(root, state='d', fg='white', bg='black', insertbackground='white', font=(
    #     'consolas', 13), selectforeground='black', selectbackground='white', takefocus=False)
    # TerminalText.pack(fill='both', expand='yes')

        changeslist = tk.Listbox(postwin)
        yscrollbar = tk.Scrollbar(changeslist)

        changeslist.config(yscrollcommand=yscrollbar.set, fg='#ffffff', selectforeground='black',
                           selectbackground='#ffffff', bg='#000000', font=('terminal', 16), selectmode='multiple', listvariable=v)

        yscrollbar.config(command=changeslist.yview)

        yscrollbar.pack(side=RIGHT, fill=Y)
        changeslist.config(yscrollcommand=yscrollbar.set)
    # 原文链接：https://blog.csdn.net/qq_38002337/article/details/81475466

        # 让Listbox最大占据postwin的控件
        changeslist.pack(fill='both', expand=1)

        # 给Listbox插入已经输入的内容

        for temp in inputen:
            changeslist.insert('end', f'{temp}')

        processlist = tk.Listbox(postwin)
        yscrollbar2 = tk.Scrollbar(processlist)

        processlist.config(yscrollcommand=yscrollbar2.set, fg='#ffffff', selectforeground='black',
                           selectbackground='#ffffff', bg='#000000', font=('terminal', 16), selectmode='multiple', listvariable=v2)

        yscrollbar2.config(command=processlist.yview)

        yscrollbar2.pack(side=RIGHT, fill=Y)
        processlist.config(yscrollcommand=yscrollbar2.set)
    # 原文链接：https://blog.csdn.net/qq_38002337/article/details/81475466

        # 让Listbox最大占据postwin的控件
        # processlist.pack(fill='both', expand=1)
        processlist.pack(fill='both', expand=1)

        # 给Listbox插入已经输入的内容
        # if inputen[0] == '!destroy':
        #     postwin.destroy()
        for temp in inputen:
            processlist.insert('end', f'{temp}')

        deleter = Button(postwin, text="删除", command=delete)
        adder = Button(postwin, text="添加", command=add_)
        # theButton = Button(master, text="删除", command=lambda x=listbox: x.delete("active"))
        deleter.pack(side=LEFT)
        adder.pack(side=RIGHT)

        # 缓存文件
        command_inputed = []
        command_inputed.append('add')
        command_inputed.append('.')
        add(terminal, [], command_inputed)

    else:
        if mode == '!destroy':
            postwin.destroy()
            window_opened = False
        else:
            if mode == 'changes':
                changeslist.delete(0, 'end')
                for i in changes['changes']:
                    changeslist.insert('end', f'{i}')
                for i in changes['delete']:
                    changeslist.insert('end', f'{i}')
                for i in changes['create']:
                    changeslist.insert('end', f'{i}')
            processlist.delete(0, 'end')
            for temp in inputen:
                processlist.insert('end', f'{temp}')
        # commandlist.delete('1.0', END)


def printchanges(process_path_in, terminal, mode):
    global changes, path_using, adder_opened
    # changes_boolean = False
    # add_boolean = False
    out = []
    # dirs = os.path.listdir(process_path_in)
    for i in process_path_in['changes']:
        out.append(i)
    for i in process_path_in['delete']:
        out.append(i)
    for i in process_path_in['create']:
        out.append(i)

    if out == [] and mode != '!destroy' and changes == {'changes': [], 'delete': [], 'create': []}:
        terminal.insert('end', '\n没有最近更改的文件')
        if adder_opened:
            adder(terminal, '!destroy')
        if window_opened:
            show_changes_in_box(out, terminal, '!destroy')
        # terminal.delete('0.0','end')
        # terminal.insert('end', '\n没有文件\n')

    # elif len(out) < 10:
    #     terminal.insert('end', '\n更改的文件列表:\n')
    #     for i in out:
    #         terminal.insert('end', i + '\n')

    else:
        show_changes_in_box(out, terminal, mode)
        # with open(rf'{os.getcwd()}\cache.txt', 'w', encoding='utf-8') as f:
        #     f.write('更改的文件列表，确认后请关闭记事本:\n')
        #     for i in out:
        #         f.write(i + '\n')
        #     f.close()
        # os.system(rf'{os.getcwd()}\cache.txt')

# 创建打开文件函数，并按换行符分割内容


def readfile(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as fileHandle:
            text = fileHandle.read()
            text = text.splitlines()
        return text
    except:
        # print("error:Read file Error")
        # sys.exit()
        return False


def diff(terminal):
    global command_inputed, inited, now_at
    global path_using
    if not inited:
        # file_path1 = easygui.fileopenbox(default=os.path.join(path_using, '*.*'))
        # file_path2 = easygui.fileopenbox(default=os.path.join(path_using, '*.*'))
        file_path1 = filedialog.askopenfilename(initialdir=path_using)
        file_path2 = filedialog.askopenfilename(initialdir=path_using)

    else:
        file_path2 = filedialog.askopenfilename(initialdir=path_using)
        dirs = os.listdir(os.path.join(path_using, '.filemanager', 'commits'))
        float_dir = []
        for i in dirs:
            float_dir.append(round(float(i)))

        float_dir.sort()

        # findin = now_at
        # if os.path.exists(os.path.join(path_using, '.filemanager', 'main', 'branches.json')):
        # 起始提交位置
        f = open(os.path.join(path_using, '.filemanager',
                 'main', 'branches.json'), 'r', encoding='utf-8')
        info_data = json.load(f)
        f.close()
        branch = info_data['branches']

        commits_in_this_branch = []

        found = find_older_commit_in_branch(branch, now_at)

        # del commits_in_this_branch[len(commits_in_this_branch) - 1]

        dirs = []
        for i in found[0]:
            dirs.append(str(float_dir[i]))

        dirs.reverse()
        del dirs[0]
#         while True:
#             file_path1 = os.path.join(path_using, '.filemanager', 'commits', str(
#                 float_dir[findin - 1]), os.path.basename(file_path2))
# # 应改成在分支里寻找，记得修改
#             if os.path.exists(file_path1):
#                 break

#             findin -= 1
        file_path1 = ''

        for i in dirs:
            file_path1 = os.path.join(
                path_using, '.filemanager', 'commits', i, os.path.basename(file_path2))
            if os.path.exists(file_path1):
                break

    if os.path.exists(file_path1) and os.path.exists(file_path2):
        if not(is_binary_file(file_path1) or is_binary_file(file_path2)):
            text1_lines = readfile(file_path1)
            text2_lines = readfile(file_path2)
            if text1_lines != False and text2_lines != False:
                d = difflib.HtmlDiff()
                # context=True时只显示差异的上下文，默认显示5行，由numlines参数控制，context=False显示全文，差异部分颜色高亮，默认为显示全文
                if not inited:
                    result = d.make_file(
                        text1_lines, text2_lines, file_path1, file_path2, context=True)
                else:
                    result = d.make_file(text1_lines, text2_lines, os.path.basename(
                        file_path1) + '(old)', os.path.basename(file_path2) + '(new)', context=True)
                # 内容保存到result.html文件中
                if '-s' in command_inputed:
                    save_path = filedialog.asksaveasfilename(defaultextension='.py', filetypes=[(
                        "Python files", ".py")], initialfile=os.path.join(path_using, 'compare_result.html'))
                    # save_path = easygui.filesavebox(default=os.path.join(path_using, 'compare_result.html'))
                else:
                    save_path = rf'{os.getcwd()}\result.html'
                with open(save_path, 'w', encoding='utf-8') as resultfile:
                    resultfile.write(result)
                webbrowser.open_new_tab('file:///' + save_path)

            elif text1_lines == False:
                terminal.insert('end', '\nerror:Read ' +
                                file_path1 + ' Error', 'red')

            elif text2_lines == False:
                terminal.insert('end', '\nerror:Read ' +
                                file_path2 + ' Error', 'red')
        else:
            terminal.insert('end', '\nerror:这是一个二进制文件', 'red')

    elif inited:
        terminal.insert('end', '\nerror:文件' + file_path2 +
                        '是这次提交新建的，无法与上一次提交对比', 'red')
    else:
        terminal.insert('end', '\nerror:文件不存在', 'red')


def write_branch(tree_in):
    global path_using, now_at
    output = {'branches': tree_in, 'now_at': now_at}
    # dumps 将数据转换成字符串
    info_json = json.dumps(output, sort_keys=False,
                           indent=4, separators=(',', ': '))
    # 显示数据类型
    print(type(info_json))
    f = open(os.path.join(path_using, '.filemanager',
             'main', 'branches.json'), 'w', encoding='utf-8')
    f.write(info_json)
    f.close()


def find_older_commit_in_branch(branch_in, target):
    branch_in.reverse()
    commit_in_branch = []
    commit_after_that_commit = []
    starts = []

    for i in branch_in:
        in_start = False
        max_num = target
        for j in i['include'].keys():
            if int(j) in starts:
                in_start = True
                max_num = int(j)
                break
        if str(target) in i['include'].keys() or in_start:
            if str(target) in i['include'].keys():
                for j in i['include'].keys():
                    if int(j) > target:
                        commit_after_that_commit.append(int(j))

            if i['start'] != '-1':
                starts.append(int(i['start']))
            for j in i['include'].keys():
                if not int(j) > max_num:
                    commit_in_branch.append(int(j))
    commit_in_branch.sort()
    return [commit_in_branch, commit_after_that_commit]


def checkout(start, terminal):
    global path_using, now_at, changes

    dirs = os.listdir(os.path.join(path_using, '.filemanager', 'commits'))
    float_dir = []
    for i in dirs:
        float_dir.append(round(float(i)))

    float_dir.sort()

    # if os.path.exists(os.path.join(path_using, '.filemanager', 'main', 'branches.json')):
    # 起始提交位置
    f = open(os.path.join(path_using, '.filemanager',
                          'main', 'branches.json'), 'r', encoding='utf-8')
    info_data = json.load(f)
    f.close()

    found = find_older_commit_in_branch(info_data["branches"], start)

    before = []
    after = []

    for i in found[0]:
        before.append(str(float_dir[i]))
    for i in found[1]:
        after.append((float_dir[i]))

    # dir_using = float_dir[0:start]
    # dir_using = []  # 实际是文件目录，不是文件夹目录
    # dir_delete = []

    # for i in float_dir[0:start+1]:
    #     dir_using.append(str(i))

    # for i in float_dir[start:len(float_dir)]:
    #     dir_delete.append(str(i))

    # dir_path = []
    # file_delete = []

    with open(os.path.join(path_using, '.filemanager', 'main', 'commits', str(float_dir[start]), 'timestamp.csv'), "r", encoding='utf-8') as p:
        timestamps = p.read().splitlines()
        p.close()

    file_at_that_time = []
    file_hash_at_that_time = {}
    if len(timestamps[0].split(',')) > 2:
        for i in timestamps:
            file_at_that_time.append(i.split(',')[0])
            file_hash_at_that_time[i.split(',')[0]] = i.split(',')[2]
    else:
        for i in timestamps:
            file_at_that_time.append(i.split(',')[0])

    # 多出的文件加入删除列表
    file_to_delete = []
    for root, dirs, files in os.walk(path_using):
        if os.path.basename(root) == ".filemanager":
            dirs[:] = []  # 忽略当前目录下的子目录
        for name in files:
            file_realtive_path = os.path.relpath(
                os.path.join(root, name), path_using)
            if not file_realtive_path in file_at_that_time and file_realtive_path not in file_to_delete:
                file_to_delete.append(file_realtive_path)

    # 后面更改过的文件加入删除列表
    file_changed_in_dir_to_delete = []
    for i in float_dir[start:len(float_dir)]:
        # for i in after:
        file_changed_in_dir_to_delete.append(str(i))

    # 前面别的分支改动过的文件加入删除列表
    branch_changed_list = []
    for i in range(start):
        branch_changed_list.append(i)
    branch_changed_list = list(set(branch_changed_list) - set(before))

    for i in branch_changed_list:
        file_changed_in_dir_to_delete.append(str(float_dir[i]))

    for i in file_changed_in_dir_to_delete:
        for root, dirs, files in os.walk(os.path.join(path_using, '.filemanager', 'commits', i)):
            for name in files:
                file_realtive_path = os.path.relpath(os.path.join(
                    root, name), os.path.join(path_using, '.filemanager', 'commits', i))
                if file_realtive_path in file_at_that_time and file_realtive_path not in file_to_delete:
                    file_to_delete.append(file_realtive_path)

    # 计算并比较有更改的文件的hash值
    remove_from_delete_list = []
    for i in list(file_hash_at_that_time.keys()):
        if os.path.exists(os.path.join(path_using, i)):
            if hash(os.path.join(path_using, i)) == file_hash_at_that_time[i]:
                remove_from_delete_list.append(i)

    file_to_delete = set(file_to_delete) - set(remove_from_delete_list)

    # 删除文件
    for i in file_to_delete:
        if os.path.exists(os.path.join(path_using, i)):
            try:
                terminal.insert('end', '\nremoving:' +
                                str(os.path.join(path_using, i))+'\n')
                terminal.update()
                terminal.see('end')
                os.remove(os.path.join(path_using, i))
                if not os.listdir(os.path.dirname(os.path.join(path_using, i))):
                    try:
                        os.removedirs(os.path.dirname(
                            os.path.join(path_using, i)))
                    except:
                        pass
            except:
                terminal.insert('end', '\nerror:'+i+'删除失败\n', 'red')
                terminal.update()
                terminal.see('end')

    # 复制文件

    file_copy_dir = []
    # for i in float_dir[0:start+1]:
    for i in before:
        file_copy_dir.append(str(i))

    file_copy_dir.reverse()

    for i in file_copy_dir:
        for root, dirs, files in os.walk(os.path.join(path_using, '.filemanager', 'commits', i)):
            for name in files:
                file_realtive_path = os.path.relpath(os.path.join(
                    root, name), os.path.join(path_using, '.filemanager', 'commits', i))
                if file_realtive_path in file_at_that_time:
                    try:
                        target_dir = os.path.dirname(
                            os.path.join(path_using, file_realtive_path))
                        if target_dir != '' and not os.path.exists(target_dir):
                            os.makedirs(target_dir)
                        if not os.path.exists(os.path.join(path_using, file_realtive_path)):
                            shutil.copy(os.path.join(root, name), os.path.join(
                                path_using, file_realtive_path))
                            terminal.insert(
                                'end', '\nchecking out:'+str(os.path.join(path_using, file_realtive_path))+'\n')
                            terminal.update()
                            terminal.see('end')
                    except:
                        terminal.insert(
                            'end', '\nerror:'+str(os.path.join(root, name))+'导出失败\n', 'red')
                        terminal.update()
                        terminal.see('end')

    # for i in dir_using:
    #     for root, dirs, files in os.walk(os.path.join(path_using, '.filemanager', 'commits', i)):
    #         for name in files:
    #             if not os.path.relpath(os.path.join(root, name), os.path.join(path_using, '.filemanager', 'commits', root, name)) in dir_path:
    #                 # mtime = round(os.stat(os.path.join(root, name)).st_mtime)
    #                 dir_path.append(os.path.relpath(os.path.join(root, name), os.path.join(
    #                     path_using, '.filemanager', 'commits', i)))

    # for i in dir_delete:
    #     for root, dirs, files in os.walk(os.path.join(path_using, '.filemanager', 'commits', i)):
    #         for name in files:
    #             if not os.path.relpath(os.path.join(root, name), os.path.join(path_using, '.filemanager', 'commits', root, name)) in dir_path:
    #                 # mtime = round(os.stat(os.path.join(root, name)).st_mtime)
    #                 file_delete.append(os.path.relpath(os.path.join(root, name), os.path.join(
    #                     path_using, '.filemanager', 'commits', i)))

    # for i in file_delete:
    #     if os.path.exists(os.path.join(path_using, i)):
    #         try:
    #             terminal.insert('end', '\nremoving:'+str(os.path.join(path_using, i))+'\n')
    #             terminal.update()
    #             terminal.see('end')
    #             os.remove(os.path.join(path_using, i))
    #             if os.path.dirname(os.path.join(path_using, i)) != path_using:
    #                 try:
    #                     os.removedirs(os.path.dirname(os.path.join(path_using, i)))
    #                 except:
    #                     pass
    #         except:
    #             terminal.insert('end', '\nerror:'+i+'删除失败\n', 'red')
    #             terminal.update()
    #             terminal.see('end')

    # dir_using.reverse()

    # # for n in range(len(dir_using)-1,1,-1):
    # # i = dir_using[n]
    # for i in dir_using:
    #     for root, dirs, files in os.walk(os.path.join(path_using, '.filemanager', 'commits', i)):
    #         for name in files:
    #             print(os.path.join(root, name))
    #             if os.path.exists(os.path.join(root, name)):
    #                 # mtime = round(os.stat(os.path.join(root, name)).st_mtime)
    #                 # prit()
    #                 # print(os.path.join(os.path.relpath(os.path.join(root, name), os.path.join(path_using, '.filemanager', 'commits')), path_using, name))
    #                 target = os.path.join(path_using,os.path.relpath(os.path.join(root, name), os.path.join(
    #                             os.path.join(path_using, '.filemanager', 'commits', i))))
    #                 if not os.path.exists(target):
    #                     try:
    #                         # print(target)
    #                         target_dir = os.path.dirname(target)
    #                         if target_dir != '' and not os.path.exists(target_dir):
    #                             os.makedirs(target_dir)
    #                         shutil.copy(os.path.join(root, name),  target)
    #                         terminal.insert('end', '\nchecking out:'+str(target)+'\n')
    #                         terminal.update()
    #                         terminal.see('end')
    #                         dir_path.remove(os.path.relpath(os.path.join(root, name), os.path.join(
    #                             path_using, '.filemanager', 'commits', i)))
    #                     except:
    #                         terminal.insert(
    #                             'end', '\nerror:'+str(os.path.join(root, name))+'导出失败\n', 'red')
    #                         terminal.update()
    #                         terminal.see('end')

    exit_flag = False
    while True:
        for ch in ['-', '\\', '|', '/']:
            terminal.insert('end', '\nWaiting......' + ch)
            # terminal.config(state='d')
            terminal.update()
            terminal.see('end')
            time.sleep(0.1)
            timestamp = round(time.time())
            m_time = round(os.stat(os.path.join(
                path_using, '.filemanager', 'main', 'now_list_doing.csv')).st_mtime)
            if timestamp - m_time > 10:
                exit_flag = True
                break
            else:
                print(int(terminal.index('end-1c').split('.')[0]))
                terminal.delete(terminal.index(
                    'end-1c').split('.')[0]+'.0', 'end')
        if exit_flag:
            terminal.delete(terminal.index('end-1c').split('.')[0]+'.0', 'end')
            terminal.insert('end', '\nWaiting......Done.')
            break

    try:
        changes = {'changes': [], 'delete': [], 'create': []}
        os.remove(os.path.join(
            path_using, '.filemanager', 'main', 'timestamp.csv'))
        createtimestamp(path_using, 'timestamp.csv')
        # shutil.copy(os.path.join(path_using, '.filemanager', 'main', 'commits', str(float_dir[now_at]), 'timestamp.csv'),os.path.join(path_using, '.filemanager', 'main', 'timestamp.csv'))
        with open(os.path.join(path_using, '.filemanager', 'main', 'now_list_doing.csv'), 'w', encoding='utf-8') as f:
            f.write('')
            f.close()

        # 更新hash值
        with open(os.path.join(path_using, '.filemanager', 'main', 'timestamp.csv'), "r", encoding='utf-8') as p:
            timestamps = p.read().splitlines()
            p.close()
        timestamp = []
        for i in timestamps:
            timestamp.append(i.split(','))

        with open(os.path.join(path_using, '.filemanager', 'main', 'commits', str(float_dir[start]), 'timestamp.csv'), "r", encoding='utf-8') as p:
            timestamps = p.read().splitlines()
            p.close()
        hashes_old = []
        for i in timestamps:
            hashes_old.append(i.split(','))
        timestamps = []

        if len(hashes_old[0]) == 3:
            for i in range(len(timestamp)):
                if timestamp[i][0] == hashes_old[i][0]:
                    timestamp[i][2] = hashes_old[i][2]
                else:
                    for j in hashes_old:
                        if timestamp[i][0] == j[0]:
                            timestamp[i][2] = j[2]

            with open(os.path.join(path_using, '.filemanager', 'main', 'timestamp.csv'), "w", encoding='utf-8') as p:
                for i in timestamp:
                    p.write('{0},{1},{2}\n'.format(i[0], i[1], i[2]))

        else:
            csv_path = os.path.join(path_using, '.filemanager', 'main', 'commits', str(
                float_dir[start]), 'timestamp.csv')
            hash_path = []
            for i in hashes_old:
                hash_path.append(i[0])
            del hash_path[0]
            writefilehash(hash_path)
            os.remove(csv_path)
            shutil.copy(os.path.join(path_using, '.filemanager',
                        'main', 'timestamp.csv'), csv_path)

    except:
        terminal.insert('end', '\nerror:检出timestamp失败', 'red')

    f = open(os.path.join(path_using, '.filemanager',
             'main', 'branches.json'), 'r', encoding='utf-8')
    info_data = json.load(f)
    f.close()
    branch = info_data['branches']
    write_branch(branch)

    print_branch(terminal)


def help(inputten, terminal):
    global start_path
    with open(os.path.join(start_path, 'help', inputten+'.txt'), 'r') as f:
        help_command = f.read().splitlines()
        f.close()
    for i in help_command:
        terminal.insert('end', '\n' + i)

# def merge(merge_branch,merge_text):
#     d

# 引入一堆库


class tk:
    from tkinter import Tk, Entry, Toplevel, Listbox, Scrollbar
    from tkinter.scrolledtext import ScrolledText

# 设置信息，可选


class terminal_infos:
    with open('version.txt', 'r', encoding='utf-8') as f:
        version = f.read()
        f.close()
    # version = '1.0.1'  # 版本
    by = 'Yuba Technology'  # 作者
    running_space = {'__name__': '__console__'}  # 运行空间(用于存储变量的)
    exec('''def print(*value):
    return None
def input(*value):
    return None
def set(*value):
    return None
def Back(*value):
    pass
del input,print,set,Back''', running_space)  # 先把那些Python基础函数替换了
    input_list = []  # 这个是输入命令记载输入命令的列表
# class os:
    # from os import getcwd,chdir,startfile,popen
    # from os.path import isfile,isdir,join
# 新建函数以便将图标载入窗口中


def icon_for_window(tkwindow, temofilename='fm.ico'):
    tkwindow.iconbitmap(default=temofilename)

# def icon_for_window(tkwindow, filevalue, temofilename='tempicon.ico'):
#     try:
#         import base64
#         tmp = open(temofilename, "wb+")
#         tmp.write(base64.b64decode(filevalue))
#         tmp.close()
#         tkwindow.iconbitmap(temofilename)
#         from os import remove
#         remove(temofilename)
#     except:
#         pass

# 运行输入的内容调用的函数


def run_command(command, terminal, commandinput):
    global path_using, command_inputed, inited, now_path, start_path, info_add, commit_text, now_at, command_chosen, changes, process_path

    def contiune_command():
        terminal.insert('end', '\n')
        # print(info_add)
        # print(path_using + info_add)
        TerminalText.insert('end', path_using + info_add + '\n', 'green')
        terminal.insert('end', f'$ ')
        terminal.window_create('end', window=commandinput)
        commandinput.focus_set()  # """

        # win_width = terminal.winfo_reqwidth()
        # win_height = terminal.winfo_reqheight()
        # print(win_width,win_height)
    errortext = f'错误指令"{command.strip()}"。'

    command = str(command)  # 这玩意是应付编辑器不知道command是什么类型的
    command_chosen = len(terminal_infos.input_list)
    terminal.config(state='n')  # 解锁terminal(Text)

    terminal.delete('end')  # 删除输入控件
    commandinput.delete(0, 'end')  # 删除控件里输入的文本

    if command.strip() == '':  # 如果啥也没输入
        terminal.insert('end', command)  # 就复述输入内容

    else:
        terminal_infos.input_list.append(command)  # 增加输入了什么命令
        terminal.insert('end', command)
        if inited:
            info_add = '('+id_read[0:6]+'...)'
        else:
            info_add = ''
        if now_path == '':
            path_using = start_path
        else:
            path_using = now_path
        # console.print("FM "+path_using+">",end='', style='underline')
        # command_inputed = input().split()
        # command_inputed = input("FM " + path_using + info_add + ">")
        command_inputed = command

        # pattern1 = re.compile(r'"(\w+)"')
        # pattern2 = re.compile(r"'(\w+)'")
        # pth1=pattern1.findall(command_inputed)
        # pth2=pattern2.findall(command_inputed)
        if ',' in command_inputed:
            command_inputed = command_inputed.split(',')
        else:
            command_inputed = command_inputed.split()

        if command_inputed[0] == "?" or command_inputed[0] == "help":
            if len(command_inputed) > 1:
                if command_inputed[1] == '-?':
                    webbrowser.open(help_url, new=0, autoraise=True)
            else:
                help('help', terminal)
            contiune_command()

        elif command_inputed[0] == "init":
            if len(command_inputed) == 1:
                # terminal.insert('end', command)
                # terminal.update()
                init(terminal)
                # terminal.insert('end','Done')
            elif '-?' in command_inputed:
                help('init', terminal)
            elif command_inputed[1] == 'newrepo':
                # terminal.insert('end', command)
                newrepo(path_using, terminal)
            elif '-exit' in command_inputed:
                # terminal.insert('end', command)
                inited = False
            elif '-update' in command_inputed:
                update(terminal)
                init(terminal)
            elif '-m' in command_inputed:
                init(terminal)
                terminal.insert(
                    'end', '\nWARNING:命令"init -m"在fillemanager 1.1.0版本被弃用。使用命令"set monitor on"以替代。', 'yellow')
                # if inited:
                #     add_to_monitor()
                #     terminal.insert('end', '\n仓库"{0}"已被添加至监控目录\n'.format(path_using))
            elif '-rm' in command_inputed:
                init(terminal)
                terminal.insert(
                    'end', '\nWARNING:命令"init -rm"在fillemanager 1.1.0版本被弃用。使用命令"set monitor off"以替代。', 'yellow')
                # if inited:
                #     delete_from_monitor()
                #     terminal.insert('end', '\n仓库"{0}"已被从监控目录中移除\n'.format(path_using))
            # terminal.insert('end',command)
            contiune_command()

        elif command_inputed[0] == 'cd':
            if len(command_inputed) == 1:
                # terminal.insert('end', command)
                # contiune_command()
                terminal.insert('end', '\nerror:移动工作目录失败。\n', 'red')
                # print('\nerror:没有输入路径', 'red')
            elif '-?' in command_inputed:
                help('cd', terminal)
            else:
                # terminal.insert('end', command)
                try:
                    os.chdir(path_using)
                    os.chdir(command_inputed[1])
                    path_using = now_path = os.getcwd()
                    os.chdir(start_path)
                    inited = False
                    info_add = ''
                    changes = {'changes': [], 'delete': [], 'create': []}
                    process_path = {'changes': [], 'delete': [], 'create': []}

                except OSError as error:
                    terminal.insert('end', '\n'+error.args[1]+'\n', 'red')
                except:
                    terminal.insert('end', '\nerror:移动工作目录失败。\n', 'red')

            contiune_command()

        elif command_inputed[0] == 'refreash':
            if '-?' in command_inputed:
                help('refreash', terminal)
                contiune_command()
            elif inited:
                terminal.insert('end', '\nRefreashing......')
                terminal.update()
                refreash(path_using, terminal)
                contiune_command()
            else:
                terminal.insert('end', '\nerror:您还没有加载这个仓库', 'red')
                contiune_command()

        elif command_inputed[0] == 'add':
            if '-?' in command_inputed:
                help('add', terminal)
            # terminal.insert('end', command)
            else:
                add(terminal, [], command_inputed)
            contiune_command()

        elif command_inputed[0] == 'commit':
            if '-?' in command_inputed:
                help('commit', terminal)
                contiune_command()
            # terminal.insert('end', command)
            elif not process_path == {'changes': [], 'delete': [], 'create': []}:
                # pattern1 = re.compile(r"'(\w+)'")
                # pattern2 = re.compile(r'"(\w+)"')
                all_text = ''
                for i in command_inputed:
                    all_text += i + ' '
                print(all_text)
                # text1 = pattern1.findall(all_text)
                # text2 = pattern2.findall(all_text)
                commit_text = ''
                text1 = all_text.split("\"")
                text2 = all_text.split("\'")
                if len(text1) <= 1 and len(text2) <= 1:
                    terminal.insert('end', "\nerror:没有提交说明", 'red')
                elif len(text1) <= 1:
                    commit_text = text2[1]
                else:
                    commit_text = text1[1]
                if not commit_text == '':
                    commit(terminal, '')
                contiune_command()
            else:
                terminal.insert('end', '\nerror:没有要提交的内容', 'red')
                contiune_command()

        elif command_inputed[0] == 'diff':
            if '-?' in command_inputed:
                help('diff', terminal)
                contiune_command()
            else:
                # terminal.insert('end', command)
                diff(terminal)
                contiune_command()

        elif command_inputed[0] == 'branch':
            if '-?' in command_inputed:
                help('branch', terminal)
            elif inited:
                # terminal.insert('end', command)
                if '-s' in command_inputed or len(command_inputed) == 1 or '-m' in command_inputed:
                    if '-g' in command_inputed or '-m' in command_inputed or len(command_inputed) == 1:
                        if '-m' in command_inputed:
                            now_at = int(
                                command_inputed[command_inputed.index('-m') + 1])
                        print_branch(terminal)
            else:
                terminal.insert('end', '\nerror:您还没有加载这个仓库', 'red')

            contiune_command()

        elif command_inputed[0] == 'checkout':
            if '-?' in command_inputed:
                help('checkout', terminal)
            elif inited:
                if len(command_inputed) > 1:
                    try:
                        now_at = int(command_inputed[1])
                    except:
                        pass
                # terminal.insert('end', command)
                # if len(command_inputed) == 1:
                checkout(now_at, terminal)
                # else:
                # checkout(now_at,command_inputed[1],terminal)
            else:
                terminal.insert('end', '\nerror:您还没有加载这个仓库', 'red')
            contiune_command()

        elif command_inputed[0] == 'reload':
            if '-?' in command_inputed:
                help('init', terminal)
            elif inited:
                # terminal.insert('end', command)
                reload(path_using, terminal)
                printchanges(changes, terminal, 'changes')
            else:
                terminal.insert('end', '\nerror:您还没有加载这个仓库', 'red')
            contiune_command()

        elif command_inputed[0] == 'show':
            if '-?' in command_inputed:
                help('show', terminal)
            elif len(command_inputed) > 1:
                if command_inputed[1] == 'monitor':
                    with open(os.path.join(start_path, 'path.txt'), 'r', encoding='utf-8') as f:
                        monitored = f.read().splitlines()
                        f.close()
                    terminal.insert('end', '\n受monitor监控的目录列表:')
                    if monitored == []:
                        terminal.insert('end', '\n无')
                    else:
                        for i in monitored:
                            terminal.insert('end', '\n' + i)
            else:
                terminal.insert('end', '\nerror:无效的参数', 'red')
            contiune_command()

        elif command_inputed[0] == 'set':
            if '-?' in command_inputed:
                help('set', terminal)
            elif len(command_inputed) > 2:
                if command_inputed[1] == 'monitor':
                    if command_inputed[2] == 'on':
                        if inited:
                            add_to_monitor()
                            terminal.insert(
                                'end', '\n仓库"{0}"已被添加至监控目录\n'.format(path_using))
                        else:
                            terminal.insert('end', '\nerror:您还没有加载这个仓库', 'red')
                    elif command_inputed[2] == 'off':
                        if inited:
                            delete_from_monitor()
                            terminal.insert(
                                'end', '\n仓库"{0}"已被从监控目录中移除\n'.format(path_using))
                        else:
                            terminal.insert('end', '\nerror:您还没有加载这个仓库', 'red')
                    else:
                        terminal.insert('end', '\nerror:无效的参数', 'red')

            else:
                terminal.insert('end', '\nerror:无效的参数', 'red')
            contiune_command()

        elif command_inputed[0] == 'recommit':
            if '-?' in command_inputed:
                help('recommit', terminal)
                contiune_command()
            # terminal.insert('end', command)
            elif not process_path == {'changes': [], 'delete': [], 'create': []}:
                entry_str = simpledialog.askstring(
                    title='确认', prompt='为了确认，在下方输入:RECOMMIT ')
                # pattern1 = re.compile(r"'(\w+)'")
                # pattern2 = re.compile(r'"(\w+)"')
                if entry_str == 'recommit' or entry_str == 'RECOMMIT':
                    all_text = ''
                    for i in command_inputed:
                        all_text += i + ' '
                    print(all_text)
                    # text1 = pattern1.findall(all_text)
                    # text2 = pattern2.findall(all_text)
                    commit_text = ''
                    text1 = all_text.split("\"")
                    text2 = all_text.split("\'")
                    if len(text1) <= 1 and len(text2) <= 1:
                        terminal.insert('end', "\nerror:没有提交说明", 'red')
                    elif len(text1) <= 1:
                        commit_text = text2[1]
                    else:
                        commit_text = text1[1]
                    if not commit_text == '':
                        dirs = os.listdir(os.path.join(
                            path_using, '.filemanager', 'commits'))
                        float_dir = []
                        for i in dirs:
                            float_dir.append(round(float(i)))

                        float_dir.sort()
                        for i in process_path['changes']:
                            try:
                                os.remove(os.path.join(
                                    path_using, '.filemanager', 'commits', str(float_dir[now_at]), i))
                            except:
                                pass
                        for i in process_path['delete']:
                            try:
                                os.remove(os.path.join(
                                    path_using, '.filemanager', 'commits', str(float_dir[now_at]), i))
                            except:
                                pass
                        commit(terminal, str(float_dir[now_at]))
                contiune_command()
            else:
                terminal.insert('end', '\nerror:没有要提交的内容', 'red')
                contiune_command()

        else:
            # terminal.insert('end', command)
            terminal.insert('end', '\nerror:未知的命令', 'red')
            contiune_command()

        terminal.config(state='d')
        terminal.see('end')


def print_branch(terminal):
    global path_using, now_at
    f = open(os.path.join(path_using, '.filemanager',
             'main', 'branches.json'), 'r', encoding='utf-8')
    info_data = json.load(f)
    f.close()
    branch_input = info_data['branches']
    branch = []

    for i in range(len(branch_input)):
        branch.append({'start': int(branch_input[i]['start']), 'include': {
        }, 'end': int(branch_input[i]['end'])})
        for j in branch_input[i]['include'].keys():
            try:
                branch[i]['include'][int(j)] = branch_input[i]['include'][j]
            except:
                pass
                # branch = branch_input

    draw_branch = draw.draw(branch, now_at)

    colors = ['red', 'green', 'blue', 'cyan', 'yellow']
    k = {}
    for i in draw_branch:
        terminal.insert('end', '\n')
        # line:color
        for j in range(len(i)):
            if i[j] == "|":
                if not j in list(k.keys()):
                    l = len(k)
                    while l >= len(colors):
                        l -= len(colors)
                    k[j] = l
                terminal.insert('end', i[j], colors[k[j]])
            elif i[j] == '-' or i[j] == '\\' or i[j] == '/' or i[j] == '+':
                terminal.insert('end', i[j], 'slategray')
            else:
                terminal.insert('end', i[j])


def post_inputlist(inputen):
    # 弹出效果展示中的命令列表
    def setit(setmessage):
        inputen.delete(0, 'end')
        inputen.insert('end', setmessage)
        postwin.destroy()
    postwin = tk.Toplevel(root, bg='#ffffff')
    icon_for_window(postwin)
    postwin.title('CommandList')
    postwin.geometry('300x200')
    postwin.transient(root)

    commandlist = tk.Listbox(postwin, fg='#800080', selectforeground='white',
                             selectbackground='#800080', font=('terminal', 16))
    # 绑定确定命令的按键
    commandlist.bind('<Return>', lambda v=0: setit(
        commandlist.get(commandlist.curselection())))
    commandlist.bind('<Right>', lambda v=0: setit(
        commandlist.get(commandlist.curselection())))
    commandlist.bind('<Left>', lambda v=0: setit(
        commandlist.get(commandlist.curselection())))
    # 让Listbox最大占据postwin的控件
    commandlist.pack(fill='both', expand=1)

    # 给Listbox插入已经输入的内容
    for temp in terminal_infos.input_list:
        commandlist.insert('end', f'{temp}')


def commandup(inputen):
    global command_chosen, terminal_infos
    if len(terminal_infos.input_list) >= command_chosen:
        if command_chosen > 0:
            command_chosen -= 1
        else:
            command_chosen = len(terminal_infos.input_list) - 1

    inputen.delete(0, 'end')
    inputen.insert('end', terminal_infos.input_list[command_chosen])


def commanddown(inputen):
    global command_chosen, terminal_infos
    if len(terminal_infos.input_list) - 1 > command_chosen:
        command_chosen += 1
    else:
        command_chosen = 0

    inputen.delete(0, 'end')
    inputen.insert('end', terminal_infos.input_list[command_chosen])

# 检查更新
# 写入版本
# with open('version.txt', 'w', encoding='utf-8') as f:
#     f.write(terminal_infos.version)
#     f.close()


os.system('checkupdate.bat')


# 创建窗口
root = tk.Tk()
# 设置标题
root.title(f'FileManager(FM) {terminal_infos.version}')
# 设置图标(用这个方法是为了防止打包后找不到图标的)
icon_for_window(root)
# 设置默认大小
root.geometry('645x400')
# 让窗口不可改变大小
# root.resizable(False, False)

# 新建Text控件
TerminalText = tk.ScrolledText(root, state='d', fg='white', bg='black', insertbackground='white', font=(
    'consolas', 13), selectforeground='black', selectbackground='white', takefocus=False)
TerminalText.pack(fill='both', expand='yes')

# 实现不同颜色的效果，用于insert插入标记
TerminalText.tag_config('red', foreground='red',
                        selectforeground='#00ffff', selectbackground='#ffffff')
TerminalText.tag_config('green', foreground='green',
                        selectforeground='#ff7eff', selectbackground='#ffffff')
TerminalText.tag_config('blue', foreground='blue',
                        selectforeground='#ffff7e', selectbackground='#ffffff')
TerminalText.tag_config('cyan', foreground='cyan',
                        selectforeground='red', selectbackground='#ffffff')
TerminalText.tag_config('slategray', foreground='slategray',
                        selectforeground='#8f7f6f', selectbackground='#ffffff')
TerminalText.tag_config('yellow', foreground='#ffff7e',
                        selectforeground='blue', selectbackground='#ffffff')

TerminalText['state'] = 'n'
# TerminalText.insert('end',f'EasyTerminal {terminal_infos.version} By {terminal_infos.by}\n')
TerminalText.insert('end', f'FileManager(FM) {terminal_infos.version}\n')
logo = printlogo.logo()
for i in logo:
    TerminalText.insert('end', i + '\n')

# path_using = start_path
# 后面的'green'就是tag标记，他会应用green这个tag的属性
TerminalText.insert('end', path_using + info_add+'\n', 'green')
TerminalText.insert('end', f'$ ')

# 命令输入框
command_input = tk.Entry(TerminalText, font=('consolas', 13), fg='white', bg='black',
                         insertbackground='white', selectforeground='black', selectbackground='white', relief='flat', width=66)
command_input.bind('<Return>', lambda v=0: run_command(
    command_input.get(), TerminalText, command_input))
# 在命令输入框中按F7弹出命令列表窗口
command_input.bind('<F7>', lambda v=0: post_inputlist(command_input))

# 上下箭头选择命令
command_input.bind('<Up>', lambda v=0: commandup(command_input))
command_input.bind('<Down>', lambda v=0: commanddown(command_input))

# 插入命令输入框
TerminalText.window_create('end', window=command_input)

# 让终端Text不可编辑
TerminalText['state'] = 'd'


def click(event):
    command_input.focus_set()


# focus
root.bind("<Double-Button-1>", click)

# 循环窗口
root.mainloop()
