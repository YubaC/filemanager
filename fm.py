# import csv
# from concurrent.futures import thread
# from __future__ import print_function
import codecs
# from ctypes import WinError
# from genericpath import isdir
# from glob import glob
# import encodings
# from glob import glob
import os
import csv
# from re import I
import sys
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
import threading
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
from tkinter import filedialog
# from tkinter import filedialog, Label, Radiobutton, simpledialog

import need.draw as draw

import json

# import traceback

# from tkinter.messagebox import askokcancel

# import windnd

# # 原文链接：https://blog.csdn.net/weixin_43849588/article/details/106911480
# import ctypes
# #告诉操作系统使用程序自身的dpi适配
# try:  # >= win 8.1
#     ctypes.windll.shcore.SetProcessDpiAwareness(2)

# except:  # win 8.0 or less
#     ctypes.windll.user32.SetProcessDPIAware()

command_inputed = []
asked_recommit = False
commit_text = ''

need_update = ''

# 现在所在的路径（进入的路径）
now_path = ''

# 软件所在的位置
# 获取程序所在文件夹
start_path = os.path.dirname(os.path.abspath(sys.argv[0]))

if start_path != os.getcwd():
    path_using = now_path = os.getcwd()
    os.chdir(start_path)
else:
    path_using = start_path

# 引入一堆库
class tk:
    from tkinter import Tk, Entry, Toplevel, Listbox
    # from tkinter import Tk, Entry, Toplevel, Listbox, Scrollbar
    from tkinter.scrolledtext import ScrolledText


# 设置信息，可选
class terminal_infos:
    with open(os.path.join(start_path, 'version.txt'), 'r', encoding='utf-8') as f:
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

# 进度展示
class ShowProgress(object):
    def __init__(self, terminal, title):
        self.terminal = terminal
        self.title = title
        # self.max_value = max_value
        terminal.insert('end', '\n')

    def update(self, now_value):
        terminal = self.terminal
        terminal.delete(terminal.index('end-1c').split('.')[0]+'.0', 'end')
        terminal.insert('end', '\n' + self.title.format(now_value))
        # terminal.insert('end', f'\n{self.title}({now_value} of )......')
        terminal.update()
        terminal.see('end')


# 核心代码
class FileManager(object):
    def __init__(self, terminal, command_input):
        self.terminal = terminal
        self.inputen = command_input

        self.start_path = ""
        self.path_using = ""

        # 仓库id
        self.id_read = ""

        # 帮助界面链接
        self.help_url = "https://yubac.github.io/fmhelp/index.html"

        # 列表中存储的是元素是元组
        self.mode_to_select = [('添加文件', 0, '+'), ('移除文件', 1, '-')]

        # 是否打开了文件暂存、移除窗口
        self.adder_opened = False

        self.exit_flag = False

        # 所有文件大小综合
        self.all_size = 0
        # 文件数目
        self.all_number = 0

        self.info_add = ''

        self.s = 0

        self.inited_all_number = 0

        # 是否加载了仓库
        self.inited = False

        # 所有的更改
        self.changes = {'changes': [], 'delete': [], 'create': []}

        # 需要提交的更改
        self.process_path = {'changes': [], 'delete': [], 'create': []}

        # 现在所在的提交位置
        self.now_at = 0

        # 现在所在的分支
        self.now_branch = 0

        self.window_opened = False

        self.deletes = []

        # 输入的命令
        # self.command_inputed = []

        self._TEXT_BOMS = (
            codecs.BOM_UTF16_BE,
            codecs.BOM_UTF16_LE,
            codecs.BOM_UTF32_BE,
            codecs.BOM_UTF32_LE,
            codecs.BOM_UTF8,
        )

    # 计算HASH值
    def hash(self, file_path, Bytes=1024):
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

    # 更新仓库的timestamp.csv文件里存储的文件Hash值
    def writefilehash(self, path_list):
        path_using = self.path_using

        terminal = self.terminal
        pb = ShowProgress(
            terminal, 'Calculating hash value({0[0]} of {0[1]})......')

        # 读取timestamp
        done = 0

        with open(os.path.join(path_using, '.filemanager', 'main', 'timestamp.csv'), "r", encoding='utf-8') as p:
            timestamps = p.read().splitlines()
            p.close()
        timestamp = []
        for i in timestamps:
            timestamp.append(i.split(','))
        timestamps = []
        for i in path_list:
            try:
                file_hash = self.hash(os.path.join(path_using, i))
                for j in range(len(timestamp)):
                    if timestamp[j][0] == i:
                        timestamp[j][2] = file_hash
                        done += 1
                        pb.update([done, len(path_list)])
                        break
                # timestamp[timestamp.index(i)][2] = file_hash
            except:
                pass
        # top.destroy()
        pb.update([len(path_list), len(path_list)])
        terminal.insert('end', 'Done.')
        terminal.update()
        with open(os.path.join(path_using, '.filemanager', 'main', 'timestamp.csv'), "w", encoding='utf-8') as p:
            for i in timestamp:
                p.write('{0},{1},{2}\n'.format(i[0], i[1], i[2]))
            p.close()

    def callback(self):
        pass  # 这个函数不做任何事，实际上让关闭按钮失效

    # 判断是否为二进制文件
    def is_binary_file(self, file_path):
        with open(file_path, 'rb') as file:
            initial_bytes = file.read(8192)
            file.close()
            for bom in self._TEXT_BOMS:
                if initial_bytes.startswith(bom):
                    continue
                else:
                    if b'\0' in initial_bytes:
                        return True
        return False

    # 升级仓库版本，添加Hash值
    def update(self):
        path_using = self.path_using
        terminal = self.terminal

        if os.path.exists(os.path.join(path_using, '.filemanager', 'main', 'version.txt')):
            with open(os.path.join(path_using, '.filemanager', 'main', 'version.txt'), 'r', encoding='utf-8') as f:
                repo_version_loaded = f.read()
                repo_version = repo_version_loaded.split('.')
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
                self.writefilehash(paths)
                with open(os.path.join(path_using, '.filemanager', 'main', 'version.txt'), 'w', encoding='utf-8') as f:
                    f.write(terminal_infos.version)
                    f.close()
        else:
            terminal.insert('end', "\nerror:这不是一个filemanager仓库", 'red')

    # 加载仓库
    def init(self):
        terminal = self.terminal
        # id_read = self.id_read
        # global inited
        # info_add = self.info_add
        # global all_size
        # global inited_all_number
        path_using = self.path_using
        # global self.now_at

        # 判断是否是一个仓库（检测version.txt）
        if os.path.exists(os.path.join(path_using, '.filemanager', 'main', 'version.txt')):
            with open(os.path.join(path_using, '.filemanager', 'main', 'version.txt'), 'r', encoding='utf-8') as f:
                repo_version_loaded = f.read()
                repo_version = repo_version_loaded.split('.')
                f.close()

            undone_commit_dirs = []

            try:
                already_commited_dirs = os.listdir(os.path.join(
                    path_using, '.filemanager', 'main', 'commits'))
                loaded_dirs = os.listdir(os.path.join(
                    path_using, '.filemanager', 'commits'))

                undone_commit_dirs = list(
                    set(loaded_dirs)-set(already_commited_dirs))
            except:
                pass

            if int(repo_version[0]) == 1 and int(repo_version[1]) == 0:
                terminal.insert('end', "\nerror:init失败", 'red')
                terminal.insert(
                    'end', '\nWARNING:这个仓库是被版本{0}的FileManager创建的。使用"init -update"命令以加载这个仓库。'.format(repo_version_loaded), 'yellow')
            else:
                # 如果有不正常的提交（没有记录的提交，会造成检出异常）
                if undone_commit_dirs != []:
                    unremoved_dirs = []
                    terminal.insert('end', "\nDeleting abnormal commits......")
                    terminal.update()
                    terminal.see('end')
                    for i in undone_commit_dirs:
                        try:
                            shutil.rmtree(os.path.join(
                                path_using, '.filemanager', 'commits', i))
                        except:
                            unremoved_dirs.append(os.path.join(
                                path_using, '.filemanager', 'commits', i))
                    if unremoved_dirs != []:
                        with open(os.path.join(path_using, 'deleter.bat'), 'w', encoding='utf-8') as f:
                            for i in unremoved_dirs:
                                f.write('rmdir /S /Q ' + i + '\\\n')
                            f.write('del /F /S /Q restartfm.bat\nexit')
                            f.close()
                        os.chdir(path_using)
                        os.system('deleter.bat')
                        os.chdir(start_path)
                    terminal.insert('end', "Done.")
                    terminal.update()

                if os.path.exists(os.path.join(path_using, '.filemanager', 'main', 'branches.json')):
                    # 起始提交位置
                    f = open(os.path.join(path_using, '.filemanager',
                                          'main', 'branches.json'), 'r', encoding='utf-8')
                    info_data = json.load(f)
                    f.close()
                    self.now_at = int(info_data['now_at'])

            # else:
            #     terminal.insert('end',"error:这不是一个filemanager仓库")
            # branch = []
            # self.now_at = len(os.listdir(os.path.join(path_using,'.filemanager','commits'))) - 1

                if os.path.exists(os.path.join(path_using, '.filemanager', 'main', 'id.txt')):

                    with open(os.path.join(path_using, '.filemanager', 'main', 'id.txt'), "r", encoding='utf-8') as f:
                        self.id_read = f.read()
                        f.close()
                        # # print(id_read)
                        # # print(now_path)

                    terminal.insert('end', '\nIniting......')
                    terminal.update()
                    terminal.see('end')

                    self.inited_all_number = 0
                    for root, dirs, files in os.walk(path_using):
                        if os.path.basename(root) == ".filemanager":
                            dirs[:] = []  # 忽略当前目录下的子目录
                            # os.mkdir(os.path.join(root,r'.filemnager/base'))
                        for name in files:
                            self.all_size += os.path.getsize(
                                os.path.join(root, name))/1024
                            self.inited_all_number += 1

                    # reload(path_using)

                    self.inited = True
                    terminal.insert('end', 'Done.' + '\n')
                    # terminal.insert('end',inited_all_number)
                    self.info_add = '('+self.id_read[0:6]+'...)'
                    # printchanges(self.changes, terminal)

                    fm.print_branch()

                # if askokcancel('ERROR', 'ERROR:FileManager没有足够的权限来执行命令。您希望以管理员权限重新启动FileManager吗？'):
                #     with open(os.path.join(path_using, 'restartfm.bat'), 'w', encoding='utf-8') as f:
                #         f.write('@echo off\n%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit\ntaskkill /f /pid fm.exe\n')
                #         f.write(path_using[0:2]+'\n')
                #         f.write('cd ' + path_using)
                #         f.write('\nstart %USERPROFILE%\AppData\Local\Programs\FileManager\\fm\\fm.exe\ndel /F /S /Q restartfm.bat\nexit')
                #         f.close()
                #     os.system(os.path.join(path_using, 'restartfm.bat'))
        else:
            terminal.insert('end', "\nerror:这不是一个filemanager仓库", 'red')

# 用监视器监视仓库

    def add_to_monitor(self):
        path_using = self.path_using
        start_path = self.start_path
        with open(os.path.join(start_path, 'path.txt'), 'r', encoding='utf-8') as f:
            paths = f.read().splitlines()
            f.close()
        if not path_using in paths:
            paths.append(path_using)
            with open(os.path.join(start_path, 'path.txt'), 'w', encoding='utf-8') as f:
                for i in paths:
                    f.write(i + '\n')
                f.close()
            os.system(os.path.join(start_path, 'restartmonitor.bat'))

    def delete_from_monitor(self):
        path_using = self.path_using
        start_path = self.start_path
        with open(os.path.join(start_path, 'path.txt'), 'r', encoding='utf-8') as f:
            paths = f.read().splitlines()
            f.close()
        if path_using in paths:
            paths.remove(path_using)
            with open(os.path.join(start_path, 'path.txt'), 'w', encoding='utf-8') as f:
                for i in paths:
                    f.write(i + '\n')
                f.close()
            os.system(os.path.join(start_path, 'restartmonitor.bat'))
    # 复制文件
    # def copy(path1, path2):
    #     global exit_flag
    #     # # print(path2)
    #     try:
    #         shutil.copytree(path1, path2)
    #         # print('Done', flush=True)
    #     except:
    #         # print('\nerror:无法复制文件。请手动删除当前文件夹下的.filemanager文件夹重试，或关机重启后重试。')
    #     exit_flag = True

    def create_id(self):
        m = hashlib.md5()
        m.update(bytes(str(time.perf_counter()), encoding='utf-8'))
        return m.hexdigest()

    def copy(self, path1, path2):
        # global progress
        # global exit_flag
        # global all_size
        # print(path1)
        # with Progress() as progress:
        total_size = self.convertSize(self.all_size)
        terminal = self.terminal

        pb = ShowProgress(
            terminal, 'Copying files({0[0]} of {0[1]} files, {0[2]} of {0[3]} in total)......')

        # terminal.insert('end', f'\nCopying {self.all_number} files, total size {total_size}......\n')
        # terminal.update()
        # terminal.see('end')

        done = 0
        done_size = 0
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
                thisadd = os.path.getsize(sourname)
                shutil.copy(sourname, targetname)
                # open(targetname,'wb').write(open(sourname,'rb').read())

                done += 1
                pb.update([done, self.all_number, self.convertSize(
                    done_size+thisadd), total_size])
                done_size += thisadd

        self.exit_flag = True
        pb.update([self.all_number, self.all_number, total_size, total_size])
        terminal.insert('end', 'Done.')
        terminal.update()
        terminal.see('end')

    # 创建timestamp.csv
    def createtimestamp(self, path1, filename):
        terminal = self.terminal
        # global progress
        # global all_number
        # time.sleep(0.1)  # 等创建文件目录
        if not os.path.exists(os.path.join(path1, '.filemanager', 'main')):
            os.makedirs(os.path.join(path1, '.filemanager', 'main'))
        if not os.path.exists(os.path.join(path1, '.filemanager', 'commits')):
            os.makedirs(os.path.join(path1, '.filemanager', 'commits'))
        with open(os.path.join(path1, '.filemanager', 'main', filename), "w", encoding='utf-8') as p:
            p.write('dir,timestamp,hash' + "\n")
            p.close()
        # with Progress() as progress:

        # top = Toplevel()
        # top.title('Timestamping......')
        pb = ShowProgress(
            terminal, 'Calculating timestamp value({0[0]} of {0[1]})......')
        # terminal.insert('end', f'\nCalculating timestamp value......(0 of {self.all_number})')
        # terminal.update()
        # terminal.see('end')

        # self.icon_for_window(top)
        # pb = Progressbar(top, length=200, mode="determinate",
        #                  orient=HORIZONTAL)
        # pb.pack(padx=10, pady=20)
        # pb["maximum"] = self.all_number
        # pb["value"] = 0
        # # pb["value"] += 1000
        # top.protocol('WM_DELETE_WINDOW', self.callback)  # 窗体的通信协议方法
        # top.update()
        # print(2)
        done = 0
        with open(os.path.join(path1, '.filemanager', 'main', filename), "a", encoding='utf-8') as p:
            for root, dirs, files in os.walk(path1):
                if os.path.basename(root) == ".filemanager":
                    dirs[:] = []  # 忽略当前目录下的子目录
                for name in files:
                    p.write(os.path.relpath(os.path.join(root, name), path1) +
                            ','+str(round(os.stat(root + '/' + name).st_mtime))+',-1\n')
                    # terminal.delete(terminal.index('end-1c').split('.')[0]+'.0', 'end')
                    # terminal.insert('end', f'\nCalculating timestamp value......({done} of {self.all_number})')
                    # terminal.update()
                    done += 1
                    pb.update([done, self.all_number])
            p.close()
        # terminal.delete(terminal.index('end-1c').split('.')[0]+'.0', 'end')
        # terminal.insert('end', f'\nCalculating timestamp value......({done} of {done})')
        pb.update([done, done])
        terminal.insert('end', 'Done.')
        terminal.update()
        terminal.see('end')

# 等待动画
# def wait():
#     global exit_flag
#     while True:
#         for ch in ['-', '\\', '|', '/']:
#             # print('\b%s' % ch, end='', flush=True)
#             time.sleep(0.1)
#             if exit_flag:
#                 break
#         if exit_flag:
#             break

    # 刷新
    def refresh(self):
        path_in = self.path_using
        terminal = self.terminal
        # inited_all_number = self.inited_all_number
        # self.adder_opened = self.adder_opened
        # global inited_all_number, self.adder_opened
        walk_loaded = {}
        csv_read = {}
        csv_read_hash = {}
        change = []
        deleted_files = {}
        new_files = {}
        delete = []
        create = []

        self.process_path = {'changes': [], 'delete': [], 'create': []}

        terminal.insert('end', '\nChecking Files number......')
        terminal.see('end')
        terminal.update()

        self.inited_all_number = 0
        for root, dirs, files in os.walk(path_in):
            if os.path.basename(root) == ".filemanager":
                dirs[:] = []  # 忽略当前目录下的子目录
                # os.mkdir(os.path.join(root,r'.filemnager/base'))
            for name in files:
                self.all_size += os.path.getsize(
                    os.path.join(root, name))/1024
                self.inited_all_number += 1

        terminal.insert('end', 'Done.')
        terminal.update()

        # 读取保存的时间戳
        f = csv.reader(open(os.path.join(path_in, '.filemanager',
                                         'main', 'timestamp.csv'), 'r', encoding='utf-8'))
        for i in f:
            csv_read[i[0]] = i[1]
            csv_read_hash[i[0]] = i[2]

            # terminal.config(state='d')

            # terminal.insert('end', '\nWaiting......Done.')
        # top = Toplevel()
        # top.title('Refreashing......')
        # self.icon_for_window(top)

        # pb = Progressbar(top, length=200, mode="determinate",
        #                  orient=HORIZONTAL)
        # pb.pack(padx=10, pady=20)
        # pb["maximum"] = inited_all_number
        # pb["value"] = 0
        # # pb["value"] += 1000
        # top.protocol('WM_DELETE_WINDOW', self.callback)  # 窗体的通信协议方法
        # top.update()
        pb = ShowProgress(terminal, 'Checking files({0[0]} of {0[1]})......')

        passed_files = 0
        for root, dirs, files in os.walk(path_in):
            if os.path.basename(root) == ".filemanager":
                dirs[:] = []  # 忽略当前目录下的子目录
            for name in files:
                # terminal.delete(terminal.index('end-1c').split('.')[0]+'.0', 'end')
                # terminal.see('end')
                # terminal.update()
                # terminal.delete(terminal.index('end-1c').split('.')[0]+'.0', 'end')
                # terminal.insert('end', f'\nChecking files......({passed_files}/{self.inited_all_number})')
                # terminal.update()
                # pb["value"] = passed_files      # 每次更新1
                # top.update()
                mtime = round(os.stat(os.path.join(root, name)).st_mtime)
                dir_path = os.path.relpath(os.path.join(root, name), path_in)
                walk_loaded[dir_path] = str(mtime)
                # progress.update(task3, advance=1)
                passed_files += 1
                pb.update([passed_files, self.inited_all_number])
                # pb["value"] = passed_files      # 每次更新1
                # top.update()
                # # print(passed_files)
                # terminal.insert('end','\n'+str(mtime))
            # progress.update(task3, advance=inited_all_number)
        # top.destroy()
        # terminal.delete(terminal.index('end-1c').split('.')[0]+'.0', 'end')
        # terminal.delete(terminal.index('end-1c').split('.')[0]+'.0', 'end')
        # terminal.insert('end', f'\nChecking files......({self.inited_all_number}/{self.inited_all_number})\n')
        # terminal.insert('end','Done.')
        # terminal.update()
        # terminal.see('end')

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
            i_hash = self.hash(os.path.join(path_in, i[0]))
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
                    # # print(pth[0])
                    # # print(path)
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
                s = s.replace('.', '\.').replace('?', '.').replace('*', '.*').replace('^', '\^').replace('$', '\$').replace('+', '\+').replace('-', '\-').replace(
                    '=', '\=').replace('!', '\!').replace(' ', '\s').replace('(', '\(').replace(')', '\)').replace('[', '\[').replace(']', '\]').replace('{', '\{').replace('}', '\}')
                if len(s) != 0 and s[0] != '#':
                    if s[0] == '\\':
                        temp = list(s)
                        temp[0] = '.*\\\\'
                        temp.append('\\.*')
                        s = ''.join(temp)
                        pattern = re.compile(f"{s}$")
                        patterns.append(pattern)
                        del temp[0]
                        s = ''.join(temp)
                        pattern = re.compile(f"{s}$")
                        patterns.append(pattern)

                    elif s[len(s)-1] == '\\':
                        temp = list(s)
                        del temp[len(temp)-1]
                        temp.append('\\\\.*')
                        s = ''.join(temp)
                        pattern = re.compile(f"{s}$")
                        patterns.append(pattern)

                    else:
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

        self.changes['changes'] = change
        self.changes['delete'] = delete
        self.changes['create'] = create

        # 写入now_list_doing.csv,方便reload查找
        with open(os.path.join(path_in, '.filemanager', 'main', 'now_list_doing.csv'), 'w', encoding='utf-8') as f:
            for i in self.changes['changes']:
                f.write('file_modified,' + i + '\n')
            for i in self.changes['delete']:
                f.write('file_deleted,' + i + '\n')
            for i in self.changes['create']:
                f.write('file_created,' + i + '\n')
            f.close()

        # terminal.insert('end', '\n' + str(self.changes) + '\n')
        terminal.insert('end', 'Done.')
        # self.printchanges(self.changes, terminal, 'changes')
        self.printchanges()

        walk_loaded = {}
        csv_read = {}
        change = []
        deleted_files = {}
        new_files = {}
        delete = []
        create = []

    # 刷新
    def reload(self):
        path_in = self.path_using
        terminal = self.terminal
        csv_read = {}
        csv_read_hash = {}

        self.process_path = {'changes': [], 'delete': [], 'create': []}

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
                    # print(int(terminal.index('end-1c').split('.')[0]))
                    terminal.delete(terminal.index(
                        'end-1c').split('.')[0]+'.0', 'end')
            if exit_flag:
                terminal.delete(terminal.index(
                    'end-1c').split('.')[0]+'.0', 'end')
                terminal.insert('end', '\nWaiting......Done.')
                break
                # time.sleep(1)

        with open(os.path.join(path_in, '.filemanager', 'main', 'now_list_doing.csv'), 'r+', encoding='utf-8') as f:
            processed = f.read().splitlines()
        for i in processed:
            line = i.split(',')
            if len(line) == 3:
                if line[2] in self.changes['delete']:
                    self.changes['delete'].remove(line[2])
                if line[2] in self.changes['changes']:
                    self.changes['changes'].remove(line[2])
                self.changes['create'].append(line[2])

                if line[1] in self.changes['create']:
                    self.changes['create'].remove(line[1])
                elif not line[1] in self.changes['delete']:
                    self.changes['delete'].append(line[1])

            else:
                if line[0] == 'file_created':
                    # if line[1] in self.changes['delete']:
                    #     self.changes['create'].remove(line[1])
                    # elif not line[1] in self.changes['delete']:
                    #     self.changes['delete'].append(line[1])
                    if line[1] in self.changes['delete']:
                        self.changes['delete'].remove(line[1])
                    if line[1] in self.changes['changes']:
                        self.changes['changes'].remove(line[1])
                    if line[1] not in self.changes['create']:
                        self.changes['create'].append(line[1])

                elif line[0] == 'file_deleted':
                    if line[1] in self.changes['create']:
                        self.changes['create'].remove(line[1])
                    elif not line[1] in self.changes['delete']:
                        self.changes['delete'].append(line[1])
                    # if line[1] in self.changes['create']:
                    #     self.changes['create'].remove(line[1])
                    if line[1] in self.changes['changes']:
                        self.changes['changes'].remove(line[1])
                    # elif not line[1] in self.changes['delete']:
                    #     self.changes['delete'].append(line[1])

                elif line[0] == 'file_modified':
                    if not line[1] in self.changes['changes'] and not line[1] in self.changes['create']:
                        self.changes['changes'].append(line[1])

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
            for i in self.changes['changes']:
                i_hash = self.hash(os.path.join(path_in, i))
                if i in keys and i_hash != csv_read_hash[i]:
                    mtime = round(os.stat(os.path.join(path_in, i)).st_mtime)
                    if str(mtime) != csv_read[i]:
                        pass
                elif i in keys and i_hash == csv_read_hash[i]:
                    timestamp_to_change.append(i)
                else:
                    self.changes['changes'].remove(i)
                    # processed.remove
            num_new = len(self.changes['changes'])

        num_new = 0
        num_old = 1
        while num_new != num_old:
            num_old = num_new
            for i in self.changes['delete']:  # 有BUG????
                if not i in keys:
                    self.changes['delete'].remove(i)
            num_new = len(self.changes['delete'])

        num_new = 0
        num_old = 1
        while num_new != num_old:
            num_old = num_new
            for i in self.changes['create']:  # 有BUG????
                if not os.path.exists(os.path.join(path_in, i)) or i in self.changes['delete'] or i in keys:
                    self.changes['create'].remove(i)
            num_new = len(self.changes['create'])

        # 忽略
        if os.path.exists(os.path.join(path_using, '.ignore')):
            with open(os.path.join(path_using, '.ignore'), 'r', encoding='utf-8-sig') as f:
                text = f.read().splitlines()
                f.close()
            patterns = []
            for s in text:
                # ^ $ .  +  -  = !     ( ) [ ] { }
                s = s.replace('.', '\.').replace('?', '.').replace('*', '.*').replace('^', '\^').replace('$', '\$').replace('+', '\+').replace('-', '\-').replace(
                    '=', '\=').replace('!', '\!').replace(' ', '\s').replace('(', '\(').replace(')', '\)').replace('[', '\[').replace(']', '\]').replace('{', '\{').replace('}', '\}')
                if len(s) != 0 and s[0] != '#':
                    if s[0] == '\\':
                        temp = list(s)
                        temp[0] = '.*\\\\'
                        temp.append('\\.*')
                        s = ''.join(temp)
                        pattern = re.compile(f"{s}$")
                        patterns.append(pattern)
                        del temp[0]
                        s = ''.join(temp)
                        pattern = re.compile(f"{s}$")
                        patterns.append(pattern)

                    elif s[len(s)-1] == '\\':
                        temp = list(s)
                        del temp[len(temp)-1]
                        temp.append('\\\\.*')
                        s = ''.join(temp)
                        pattern = re.compile(f"{s}$")
                        patterns.append(pattern)

                    else:
                        pattern = re.compile(f"{s}$")
                        patterns.append(pattern)

                remove_list = []
                for e in self.changes['changes']:
                    for pattern in patterns:
                        if pattern.match(e):
                            remove_list.append(e)
                            break

                self.changes['changes'] = list(
                    set(self.changes['changes']) - set(remove_list))

                for e in self.changes['delete']:
                    for pattern in patterns:
                        if pattern.match(e):
                            remove_list.append(e)
                            break

                self.changes['delete'] = list(
                    set(self.changes['delete']) - set(remove_list))

                for e in self.changes['create']:
                    for pattern in patterns:
                        if pattern.match(e):
                            remove_list.append(e)
                            break

                self.changes['create'] = list(
                    set(self.changes['create']) - set(remove_list))

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
                    # # print(pth[0])
                    # # print(path)
                    if i == timestamp_splited[path][0]:
                        mtime = str(
                            round(os.stat(os.path.join(path_using, timestamp_splited[path][0])).st_mtime))
                        timestamp_splited[path][1] = mtime
                        timestamp_to_change.remove(i)
                        self.changes['changes'].remove(i)
                        break
            if timestamp_to_change == []:
                break
        with open(os.path.join(path_in, '.filemanager', 'main', 'timestamp.csv'), 'w', encoding='utf-8') as f:
            for i in timestamp_splited:
                f.write('{0},{1},{2}\n'.format(i[0], i[1], i[2]))

        with open(os.path.join(path_in, '.filemanager', 'main', 'now_list_doing.csv'), 'w', encoding='utf-8') as f:
            for i in self.changes['changes']:
                f.write('file_modified,' + i + '\n')
            for i in self.changes['delete']:
                f.write('file_deleted,' + i + '\n')
            for i in self.changes['create']:
                f.write('file_created,' + i + '\n')
            f.close()

        with open(f'{os.getcwd()}\path.txt', 'r', encoding='utf-8') as f:
            paths = f.read().splitlines()
            f.close()
        if not path_in in paths:
            terminal.insert('end', '\nWARNING:位于{0}的仓库并没有被monitor所监控，您的更改可能不会被察觉。请使用"refresh"命令以加载完整变更。'.format(
                str(path_in)), 'yellow')

    # 新建仓库的命令

    def newrepo(self, path_in):
        terminal = self.terminal
        # global info_add
        # info_add = self.info_add
        # global exit_flag
        # exit_flag = self.exit_flag
        # global all_size
        all_size = 0
        all_number = 0
        start_path = self.start_path
        # global inited
        # # print(path_in)
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
                    all_size += os.path.getsize(os.path.join(root, name))
                    all_number += 1

            timestamp = round(time.time()*100)
            str_timestamp = str(timestamp)
            self.all_size = all_size
            self.all_number = all_number
        # os.startfile("G:\TEST0\GIT\\filemanager\copier\copier.exe")
            # c1 = threading.Thread(target=copy,args=(path_in, os.path.join(path_in,r'.filemanager\base')))
            self.copy(path_in, os.path.join(
                path_in, r'.filemanager\commits', str_timestamp))
            self.createtimestamp(path_in, 'timestamp.csv')
            with open(os.path.join(path_in, '.filemanager', 'main', 'timestamp.csv'), "r", encoding='utf-8') as p:
                loaded_timestamp = p.read().splitlines()
                p.close()
            del loaded_timestamp[0]
            with open(os.path.join(path_in, '.filemanager', 'main', 'timestamp.csv'), "w", encoding='utf-8') as p:
                p.write('dir,timestamp,hash\n')
                for i in loaded_timestamp:
                    p.write(i + ',-1\n')
                p.close()
            self.writefilehash(paths)
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
            os.system(f'"{os.getcwd()}\\hide.bat"')
            os.chdir(self.start_path)

            all_size = 0
            all_number = 0

            ok = False
            ids = 0

            new_id = self.create_id()
            with open(os.path.join(start_path, 'id.txt'), "r", encoding='utf-8') as f:
                id = f.read().splitlines()
                f.close()
            while ok:
                for i in id:
                    if i != new_id:
                        ids += 1
                    else:
                        new_id = self.create_id()
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
            self.write_branch(new_branch)

            # terminal.insert('end', 'Done.')

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

            terminal.insert('end', '\nDone.')

    # 暂存/取消暂存的窗口
    # def adder(self, command):
    #     terminal = self.terminal
    #     def callRB():
    #         self.mode = self.mode_to_select[v.get()][2]

    #     def drag_files(urls):
    #         # print(urls)
    #         paths = ''
    #         decodedpaths = []
    #         for i in urls:
    #             try:
    #                 decodedpaths.append(i.decode("gb18030"))
    #             except:
    #                 try:
    #                     decodedpaths.append(i.decode("utf-8"))
    #                 except:
    #                     paths += 'error:添加:' + i + '失败\n'

    #         # print(decodedpaths)
    #         # for i in urls:
    #         #     # print((i).decode("utf-8"))
    #         # showinfo('确认路径', b'\n'.join(urls).decode())

    #         paths += '请确认:以下是' + self.mode + '路径:\n'
    #         paths += '\n'.join(decodedpaths)
    #         if askokcancel('请确认:' + self.mode + '路径', str(paths)):
    #             # 我也不知道为什么，这个延时不能再短了，不然它会崩溃...
    #             time.sleep(1)
    #             path_to_process_list = decodedpaths
    #             dirs = []
    #             files = []
    #             for i in path_to_process_list:
    #                 if os.path.isdir(i):
    #                     if not '.filemanager' in i:
    #                         dirs.append(i)
    #                 else:
    #                     files.append(i)
    #             if dirs != []:
    #                 command_inputed = []
    #                 command_inputed.append('add')
    #                 command_inputed.append('-d')
    #                 command_inputed.append(self.mode)
    #                 self.add(terminal, dirs, command_inputed)

    #             if files != []:
    #                 command_inputed = []
    #                 command_inputed.append('add')
    #                 command_inputed.append('-f')
    #                 command_inputed.append(self.mode)
    #                 self.add(terminal, files, command_inputed)

    #                 # showinfo('确认路径', b'\n'.join(urls).decode())
    #     global top

    #     def exitbutton():
    #         self.adder_opened = False
    #         top.destroy()

    #     if command == '!destroy':
    #         if self.adder_opened:
    #             exitbutton()

    #     else:
    #         if not self.adder_opened:
    #             self.adder_opened = True
    #             self.mode = '+'
    #             top = Toplevel()
    #             top.title('添加/移除文件(文件夹)')
    #             top.wm_attributes('-topmost', 1)
    #             top.geometry("350x100")
    #             top.resizable(False, False)
    #             self.icon_for_window(top)

    #             v = IntVar()

    #             # ent = tkinter.Entry(top).pack()
    #             # ent = tkinter.Entry(top, width=100).grid(row=0)
    #             label = Label(top, text='拖拽文件或文件夹至此', font=15, pady=20)
    #             label.pack()
    #             Radiobutton(top, text='添加文件', value=0, command=callRB,
    #                         variable=v).pack(side=LEFT, expand=True)
    #             Radiobutton(top, text='移除文件', value=1, command=callRB,
    #                         variable=v).pack(side=RIGHT, expand=True)

    #             windnd.hook_dropfiles(top, func=drag_files)
    #             # 进入消息循环
    #             # top.mainloop()
    #             top.protocol('WM_DELETE_WINDOW', exitbutton)

    # 暂存

    def add(self, paths, command_inputed):
        terminal = self.terminal
        path_using = self.path_using

        if self.inited:
            if len(command_inputed) == 1:
                pass
                # self.adder('add')
                # self.printchanges()

            elif command_inputed[1] == '.':
                for i in self.changes['changes']:
                    if not i in self.process_path['changes']:
                        self.process_path['changes'].append(i)
                for i in self.changes['delete']:
                    if not i in self.process_path['delete']:
                        self.process_path['delete'].append(i)
                for i in self.changes['create']:
                    if not i in self.process_path['create']:
                        self.process_path['create'].append(i)
                # self.process_path = self.changes
            elif command_inputed[1] == 'clear':
                self.process_path = {'changes': [], 'delete': [], 'create': []}

            # elif '+' in command_inputed:
            elif '-f' in command_inputed:
                if paths != []:
                    file_path = paths
                else:
                    file_path = filedialog.askopenfilenames(
                        initialdir=path_using)
                if '+' in command_inputed:
                    for i in file_path:
                        try:
                            sourname = os.path.relpath(i, path_using)
                            if sourname in self.changes['changes'] and sourname not in self.process_path['changes']:
                                self.process_path['changes'].append(sourname)
                            if sourname in self.changes['delete'] and sourname not in self.process_path['delete']:
                                self.process_path['delete'].append(sourname)
                            if sourname in self.changes['create'] and sourname not in self.process_path['create']:
                                self.process_path['create'].append(sourname)
                        except:
                            pass
                elif '-' in command_inputed:
                    for i in file_path:
                        try:
                            sourname = os.path.relpath(i, path_using)
                            if sourname in self.process_path['changes']:
                                self.process_path['changes'].remove(sourname)
                            if sourname in self.process_path['delete']:
                                self.process_path['delete'].remove(sourname)
                            if sourname in self.process_path['create']:
                                self.process_path['create'].remove(sourname)
                        except:
                            pass
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
                                if sourname in self.changes['changes'] and sourname not in self.process_path['changes']:
                                    self.process_path['changes'].append(
                                        sourname)
                                if sourname in self.changes['delete'] and sourname not in self.process_path['delete']:
                                    self.process_path['delete'].append(
                                        sourname)
                                if sourname in self.changes['create'] and sourname not in self.process_path['create']:
                                    self.process_path['create'].append(
                                        sourname)

                elif '-' in command_inputed:
                    for i in folder_path:
                        for root, dirs, files in os.walk(i):
                            if os.path.basename(root) == ".filemanager":
                                dirs[:] = []  # 忽略当前目录下的子目录
                                # os.mkdir(os.path.join(root,r'.filemnager/base'))
                            for name in files:
                                sourname = os.path.relpath(
                                    os.path.join(root, name), path_using)
                                if sourname in self.process_path['changes']:
                                    self.process_path['changes'].remove(
                                        sourname)
                                if sourname in self.process_path['delete']:
                                    self.process_path['delete'].remove(
                                        sourname)
                                if sourname in self.process_path['create']:
                                    self.process_path['create'].remove(
                                        sourname)

            self.printchanges()
            # self.printchanges(self.process_path, terminal, 'changes')

        else:
            terminal.insert('end', '\nerror:您还没有加载这个仓库', 'red')

    # Byte换KB、MB、GB
    def convertSize(self, size):
        # Byte直接返回
        if size < 1024:
            return str(size) + "B"
        # KB取整后返回
        elif size < 1024 * 1024:
            return str(int(size / 1024)) + "KB"
        # MB保留一位小数
        elif size < 1024 * 1024 * 1024:
            return str(round(size / (1024 * 1024), 1)) + "MB"
        # GB保留两位小数
        else:
            return str(round(size / (1024 * 1024 * 1024), 2)) + "GB"

    # 提交
    def commit(self, commit_text, str_timestamp_in, attach=False):
        terminal = self.terminal
        # # print(self.changes['delete'])
        # # print('True')
        # global commit_text
        path_using = self.path_using
        # global self.now_at

        commit_size = 0
        commit_files_number = 0
        changes_path = []
        delete_path = []
        copy_path = []

        terminal.insert('end', '\nChecking Files......')
        terminal.see('end')
        terminal.update()

        # 如果有附件的话就读取附件
        if attach:
            attach_file = ''
            attach_file = filedialog.askopenfilename(initialdir=path_using)
            if attach_file != '' and not self.is_binary_file(attach_file):
                with open(attach_file, 'r', encoding='utf-8') as f:
                    attach_text = f.read()
                    f.close()
                commit_text ='#' + commit_text

        # 计算提交的文件的大小
        for i in self.process_path['changes']:
            commit_size += os.path.getsize(os.path.join(path_using, i))
            commit_files_number += 1
            copy_path.append(i)
        # for i in self.process_path['delete']:
        #     commit_size += os.path.getsize(os.path.join(path_using, i))/1024
        for i in self.process_path['create']:
            commit_size += os.path.getsize(os.path.join(path_using, i))
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

        terminal.insert('end', 'Done.')
        # terminal.see('end')
        # terminal.update()

        total_size = self.convertSize(commit_size)
        # terminal.insert('end', f'\nCommitting {commit_files_number} files, total size {total_size}......\n')

        # terminal.update()
        # terminal.see('end')

        pb = ShowProgress(
            terminal, 'Committing files({0[0]} of {0[1]} files, {0[2]} of {0[3]} in total)......')

        passed_files = 0
        bytes_done = 0
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
            # terminal.delete(terminal.index('end-1c').split('.')[0]+'.0', 'end')
            # terminal.insert('end', f'\nCommitting files......({passed_files} of {commit_files_number} files, {self.convertSize(bytes_done)} of {total_size} in total)')
            # terminal.update()
            passed_files += 1
            # pb["value"] += os.path.getsize(os.path.join(path_using, i))/1024
            # top.update()
            pb.update([passed_files, commit_files_number,
                      self.convertSize(bytes_done), total_size])
            bytes_done += os.path.getsize(os.path.join(path_using, i))

        # terminal.delete(terminal.index('end-1c').split('.')[0]+'.0', 'end')
        # terminal.insert('end', f'\nCommitting files......({commit_files_number} of {commit_files_number} files, {total_size} of {total_size} in total)')
        pb.update([commit_files_number, commit_files_number,
                  total_size, total_size])
        terminal.insert('end', '\nDone.')
        terminal.update()
        # top.destroy()

        # 读取timestamp
        with open(os.path.join(path_using, '.filemanager', 'main', 'timestamp.csv'), "r", encoding='utf-8') as p:
            timestamps = p.read().splitlines()
            p.close()

        # 更新timestamp
        with open(os.path.join(path_using, '.filemanager', 'main', 'timestamp.csv'), "w", encoding='utf-8') as p:

            number = 0

            for i in self.process_path['changes']:
                changes_path.append(i)

            for i in self.process_path['delete']:
                delete_path.append(i)

            # 更新有改变的文件的timestamp
            while True:
                for i in timestamps:
                    pth = i.split(',')
                    for path in changes_path:
                        # # print(pth[0])
                        # # print(path)
                        if pth[0] == path:
                            mtime = str(
                                round(os.stat(os.path.join(path_using, path)).st_mtime))
                            pth[1] = mtime
                            changes_path.remove(path)
                            timestamps[number] = pth[0] + ',' + pth[1] + ',-1'
                            # # print(number)
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
                            # print(path2)
                            # changes_path.remove(path)
                            del timestamps[number]
                            delete_path.remove(path2)
                            # # print(number)
                    number += 1
                if delete_path == []:
                    break

            # 为新建的文件添加timestamp
            for path in self.process_path['create']:
                mtime = str(
                    round(os.stat(os.path.join(path_using, path)).st_mtime))
                timestamps.append(path + ',' + mtime + ',-1')

            for i in timestamps:
                p.write(i + '\n')
            p.close()

            # 更新hash值
            self.writefilehash(copy_path)

            # 记录提交注释
            if not os.path.exists(os.path.join(path_using, '.filemanager', 'main', 'commits', str_timestamp)):
                os.makedirs(os.path.join(path_using, '.filemanager',
                            'main', 'commits', str_timestamp))
            with open(os.path.join(path_using, '.filemanager', 'main', 'commits', str_timestamp, 'note'), 'w', encoding='utf-8') as f:
                f.write(commit_text)
                f.close()

            # 记录提交的变更
            with open(os.path.join(path_using, '.filemanager', 'main', 'commits', str_timestamp, 'changes'), 'w', encoding='utf-8') as f:
                for i in self.process_path['changes']:
                    f.write(i + '\n')
                f.close()
            with open(os.path.join(path_using, '.filemanager', 'main', 'commits', str_timestamp, 'delete'), 'w', encoding='utf-8') as f:
                for i in self.process_path['delete']:
                    f.write(i + '\n')
                f.close()
            with open(os.path.join(path_using, '.filemanager', 'main', 'commits', str_timestamp, 'create'), 'w', encoding='utf-8') as f:
                for i in self.process_path['create']:
                    f.write(i + '\n')
                f.close()
            
            if attach:
                with open(os.path.join(path_using, '.filemanager', 'main', 'commits', str_timestamp, 'README.md'), 'w', encoding='utf-8') as f:
                    f.write(attach_text)
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
            if i[1] in self.process_path['changes']:
                out.remove(i)

        for i in out:
            if i[1] in self.process_path['delete']:
                out.remove(i)

        for i in out:
            if i[1] in self.process_path['create']:
                out.remove(i)

        with open(os.path.join(path_using, '.filemanager', 'main', 'now_list_doing.csv'), 'w', encoding='utf-8') as f:
            if out != []:
                for i in out:
                    f.write(i[0] + ',' + i[1] + '\n')
            else:
                f.write('')
            f.close()

        self.changes['changes'] = list(
            set(self.changes['changes']) - set(self.process_path['changes']))
        self.changes['delete'] = list(set(self.changes['delete']) -
                                      set(self.process_path['delete']))
        self.changes['create'] = list(set(self.changes['create']) -
                                      set(self.process_path['create']))
        self.process_path = {'changes': [], 'delete': [], 'create': []}

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
                    branch[i]['include'][int(
                        j)] = branch_input[i]['include'][j]
                    if int(j) > branch_len:
                        branch_len = int(j)
                except:
                    pass

        if str_timestamp_in == '':

            now_branch_max_commit = 0

            for i in range(len(branch)):
                if self.now_at in list(branch[i]['include'].keys()):
                    now_at_branch = i
                    for j in list(branch[i]['include'].keys()):
                        if int(j) > now_branch_max_commit:
                            now_branch_max_commit = int(j)
                    break
            # new_branch = [{'start': -1, 'include':{0:"新建仓库"}, 'end': -1}]
            if self.now_at == now_branch_max_commit:
                branch[now_at_branch]['include'][branch_len+1] = commit_text
            else:
                new_branch = {'start': self.now_at, 'include': {
                    branch_len+1: commit_text}, 'end': -1}
                branch.append(new_branch)
            self.now_at = branch_len + 1
            branch_len = 0

        else:
            for i in range(len(branch)):
                if self.now_at in branch[i]['include'].keys():
                    branch[i]['include'][self.now_at] = commit_text
                    break

        self.write_branch(branch)
        self.print_branch()
        # self.printchanges(self.changes, terminal, '!destroy')
        self.printchanges()

    # 重提交

    def recommit(self, commit_text, attach=False):
        if not commit_text == '':
            dirs = os.listdir(os.path.join(
                path_using, '.filemanager', 'commits'))
            float_dir = []
            for i in dirs:
                float_dir.append(round(float(i)))

            float_dir.sort()
            for i in self.process_path['changes']:
                try:
                    os.remove(os.path.join(
                        path_using, '.filemanager', 'commits', str(float_dir[self.now_at]), i))
                except:
                    pass
            for i in self.process_path['delete']:
                try:
                    os.remove(os.path.join(
                        path_using, '.filemanager', 'commits', str(float_dir[self.now_at]), i))
                except:
                    pass
            self.commit(commit_text, str(float_dir[self.now_at]), attach)

    def printchanges(self):
        terminal = self.terminal
        # 从process_path里合并changes, delete,create
        added = []
        for i in self.process_path['changes']:
            added.append(i)
        for i in self.process_path['delete']:
            added.append(i)
        for i in self.process_path['create']:
            added.append(i)

        # 从changes里合并changes, delete, create
        if len(self.changes['changes']) == 0 and len(self.changes['delete']) == 0 and len(self.changes['create']) == 0:
            terminal.insert('end', '\nNo changes.')
        else:
            out = []
            changed_number = 3
            if len(self.changes['changes']) != 0:
                out.append("\n----------------Changed Files----------------")
                for i in self.changes['changes']:
                    out.append(i)
            else:
                changed_number -= 1
            if len(self.changes['delete']) != 0:
                out.append("\n----------------Deleted Files----------------")
                for i in self.changes['delete']:
                    out.append(i)
            else:
                changed_number -= 1
            if len(self.changes['create']) != 0:
                out.append("\n----------------Created Files----------------")
                for i in self.changes['create']:
                    out.append(i)
            else:
                changed_number -= 1

            # 显示更改
            # 如果changed_number的长度小于200
            changed_number += len(out)
            if changed_number < 200:
                for i in out:
                    if i in added:
                        # 如果i在added里，就显示为cyan
                        terminal.insert('end', f'{i}\n', 'cyan')
                    else:
                        terminal.insert('end', f'{i}\n')
            else:
                changed_number = len(out)
                # 提示更改的文件太多了，已经禁用了显示功能
                terminal.insert(
                    'end', f'\nWarning:Too many files have been changed({changed_number} files),and all filenames will not be displayed.', 'yellow')
                terminal.update()

# # 展示分支树

    # 计算并绘制分支树

    def print_branch(self):
        terminal = self.terminal
        path_using = self.path_using
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
                    branch[i]['include'][int(
                        j)] = branch_input[i]['include'][j]
                except:
                    pass
                    # branch = branch_input

        draw_branch = draw.draw(branch, self.now_at)

        colors = ['red', 'green', 'blue', 'cyan', 'yellow']
        marks = [ '─', '┐', '┬', '└', '┘', '←', '→']
        k = {}
        for i in draw_branch:
            terminal.insert('end', '\n')
            # line:color
            for j in range(len(i)):
                if i[j] == "│":
                    if not j in list(k.keys()):
                        l = len(k)
                        while l >= len(colors):
                            l -= len(colors)
                        k[j] = l
                    terminal.insert('end', i[j], colors[k[j]])
                elif i[j] in marks:
                    terminal.insert('end', i[j], 'slategray')
                
                # --------------------------
                elif i[j] == '#':
                    # 提取id
                    # 反向检查字符串i，如果发现')'就截取直到前面'='的内容
                    for m in range(len(i)-1, -1, -1):
                        if i[m] == ')':
                            for l in range(m-1, -1, -1):
                                if i[l] == '=':
                                    id = i[l+1:m]
                                    break
                            break

                    configid = 'id>' + id

                    terminal.tag_configure(configid, foreground='#ffffff',
                        selectforeground='#000000', selectbackground='#ffffff', underline=True)
                    terminal.tag_bind('id>'+id, '<Button-1>', lambda event, id=id: self.InsertMDFromId(id))
                    # print(id)
                    # 显示#之后的部分
                    terminal.insert('end', i[j+1:], configid)
                    break
                # --------------------------

                else:
                    terminal.insert('end', i[j])

    def getMDFromId(self, id):
        # 从path_using/.filemanager/main/commits里找到排序为int(id)的文件夹
        dirs = os.listdir(os.path.join(self.path_using, '.filemanager', 'commits'))
        float_dir = []
        for l in dirs:
            float_dir.append(round(float(l)))
        float_dir.sort()
        open_path = os.path.join(self.path_using, '.filemanager', 'main', 'commits',str(float_dir[int(id)]), 'README.md')
        return open_path

    def InsertMDFromId(self, id):
        def onMouseUp():
            self.inputen.delete(0, 'end')
            self.inputen.insert('end', 'show detailedCommitText ' + id)
            self.inputen.focus_set()
            self.terminal.see('end')
            self.terminal.bind('<ButtonRelease-1>', lambda v=0: self.callback())
        self.terminal.bind('<ButtonRelease-1>', lambda v=0: onMouseUp())

# 创建打开文件函数，并按换行符分割内容
    # 解析MarkDown并显示
    def parseMarkDown(self, file_path):
        terminal = self.terminal
        line1 = '---------------------------------------------------------------------'
        line2 = '====================================================================='
        terminal.insert('end','\n')
        terminal.insert('end', line1 + '\n')
        terminal.insert('end',file_path + '\n')
        terminal.insert('end', line1 + '\n')
        # this_line = '—————————————————————————————————————————————————————————————————————'
        def insert_markdown(terminal, this_id, text, font_size=0, isbold=False, isitalic=False,  isstrikethrough=False, islink=False, ishighlight=False, isunderline=False):
            if text != '':
                this_id= str(this_id)
                bold=''
                italic=''
                if not ishighlight:
                    if font_size != 0:
                        terminal.tag_config(this_id, foreground='#ffffff',
                                    selectforeground='#000000', selectbackground='#ffffff', 
                                    underline=isunderline,overstrike=isstrikethrough,font=(
                                    'consolas', 13 + 6 - font_size, "bold"))
                    else:
                        if isbold:
                            bold = 'bold'
                        if isitalic:
                            italic = 'italic'
                        terminal.tag_config(this_id, foreground='#ffffff',
                                    selectforeground='#000000', selectbackground='#ffffff', 
                                    underline=isunderline,overstrike=isstrikethrough,font=(
                                    'consolas', 13 , bold + " " + italic))

                        # terminal.tag_config(this_id,background="#ffffff", foreground='#000000', selectforeground='#ffffff',
                        #              selectbackground='#000000', 
                        #             underline=isunderline,overstrike=isstrikethrough,font=(
                        #             'consolas', 13 , bold + " " + italic))
                else:
                    if font_size != 0:
                        terminal.tag_config(this_id,background="#ffffff", foreground='#000000',
                                    selectforeground='#ffffff', selectbackground='#000000', 
                                    underline=isunderline,overstrike=isstrikethrough,font=(
                                    'consolas', 13 + 6 - font_size, "bold"))
                    else:
                        if isbold:
                            bold = 'bold'
                        if isitalic:
                            italic = 'italic'
                        terminal.tag_config(this_id,background="#ffffff", foreground='#000000',
                                    selectforeground='#ffffff', selectbackground='#000000', 
                                    underline=isunderline,overstrike=isstrikethrough,font=(
                                    'consolas', 13 , bold + " " + italic))

                terminal.insert('end', text, this_id)
                terminal.update()
                terminal.see('end')

        # 反复循环拆解文字直到没有标签为止
        
        with open(file_path, 'r', encoding='utf-8') as f:
            Mlines = f.read()
            f.close()
        if Mlines.startswith("\ufeff"):
            # 删掉这个\ufeff
            Mlines = Mlines[1:]
            # with open(file_path, 'r', encoding='utf-8-sig') as f:
            #     Mlines = f.read()
            #     f.close()
        Mlines = Mlines.splitlines()

        lines = []
        # 将Mlines中没有''作为间隔的元素合并，并添加到新数组lines里
        for i in range(len(Mlines)):
            if Mlines[i] != '':
                if i != 0 and i-1>0 and Mlines[i-1] != '':
                    lines[-1] += '\n' + Mlines[i]
                else:
                    lines.append(Mlines[i])
                    # lines.append('')
        
        Mlines = lines

        # 将Mlines里的每两个元素之间插入一个空元素
        lines = []
        for i in Mlines:
            lines.append(i)
            lines.append('')
        
        Mlines = lines

            # if Mlines[i] != '':
            #     if i != 0 and i-1>0 and Mlines[i-1] != '':
        passed = 0
        for line in range(len(Mlines)):
            this_line = Mlines[line]

            font_size = 0

            gopass = False
            continuity = False

            # 判断是否是标题
            # 查找开头#的数量
            if this_line.startswith('#'):
                i = 0
                for i in range(len(this_line)):
                    if this_line[i] != '#':
                        break
                # 判断是否是标题
                if this_line[i] == ' ':
                    # 判断标题级别
                    font_size = i

                # 去除这一行首尾的所有#以及与之连接的空格
                this_line = this_line.strip('# ')
                gopass = True
                
            # 判断是否是列表
            # 如果这一行开头是空格和-或*，则是列表，或者是分界线
            # 列表的话后面一定会跟着空格
            # -前面的空格数是列表的级别
            # 如果开头是空格，就一直读取字符，直到不是空格，这时返回的i就是列表级别
            if this_line.startswith(' ') or this_line.startswith('-') or this_line.startswith('*') or this_line.startswith('+'):
                i = 0
                for i in range(len(this_line)):
                    if this_line[i] != ' ':
                        break
                if (this_line[i] == '-' or this_line[i] == '*' or this_line[i] == '+') and len(this_line) > i+1 and this_line[i+1] == ' ':
                    # 判断列表级别
                    # font_size = i
                    # 去除这一行第一个-或*，但保留前面的缩进
                    this_line = this_line[:i] + '·' + this_line[i+1:]

                else:
                    # 去除行内所有空格及tab
                    line_small = this_line.replace(' ', '')

                    # 判断是否是分界线
                    # 三个或更多的「减号 -」、「星号 *」、「下划线 -」的方式创建一条相当于 HTML 语法中<hr/>一样的分隔线。这三个符号之间可以包含空格
                    if line_small.startswith('---') or line_small.startswith('***') or line_small.startswith('___'):
                        # 去除这一行第一个-或*，但保留前面的缩进
                        # this_line = '—————————————————————————————————————————————————————————————————————'
                        this_line = line2
                        # this_line = '----------------------------------------'
                        gopass = True
            # 如果是>，则是引用
            elif this_line.startswith('>'):
                continuity = True

            # 引用的格式
            quote = 0
            for letter in range(len(this_line)):
                # this_line = this_line.replace('    ', '█')
                if this_line[letter] == '>' and continuity:
                # 判断引用级别
                # font_size = 1
                    quote += 1
                    # pass
                # 去除这一个>，但保留前面的缩进
                    # this_line = this_line[:letter] + ' █ ' + this_line[letter+1:]
                # break
                elif this_line[letter] != ' ':
                    break
                
            if continuity:
                this_line = ' █' * quote + ' ' + this_line[letter:]
                # 在每一行的开头加上引用符号
                this_line =this_line.replace('\n', '\n' + ' █' * quote + ' ')
                continuity = False

            # 加粗的格式
            # 1个星号或下划线包围的文本会被转换为斜体的文本
            # 2个星号或下划线包围的文本会被转换为加粗的文本
            # 3个星号或下划线包围的文本会被转换为加粗的斜体的文本

            # 删除线的格式
            # 2个波浪线包围的文本会被转换为删除线的文本

            # 高亮的格式
            # 2个等号包围的文本会被转换为高亮的文本

            # status字典用来记录当前的状态
            # 当status有改变的时候，就要插入文本
            status = {'bold': False, 'italic': False, 'underline': False, 'strikethrough': False, 'highlight': False}

            # 当读取到特殊字符的时候，就要改变status的值
            # 读取到特殊字符的时候，就要插入文本
            # 特殊字符为*、**、***、_、__、___、~~、==
            # 两个特殊字符为一对，当读取到一对中的第一个时，就把status中对应的值改为True，
            # 读取到第二个时，就把status中对应的值改为False

            text_to_insert = ''
            if not gopass:
                # time.sleep(1)
                while True:
                    # 如果没有特殊字符就直接插入
                    if '*' not in this_line and '_' not in this_line and '~' not in this_line and '=' not in this_line:
                        text_to_insert += this_line
                        insert_markdown(terminal, passed, text_to_insert, font_size=font_size, isbold=status['bold'], isitalic=status['italic'],  isstrikethrough=status['strikethrough'], ishighlight=status['highlight'], isunderline=status['underline'])
                        break
                    for letter in range(len(this_line)):
                        # 如果这个*后面还存在一个*那么这就是一对*，可以用来斜体，否则当做一般字符处理
                        # !https://zhidao.baidu.com/question/207742983427139605.html
                        old_status = status.copy()
                        if this_line[letter] == '*' and ('*' in this_line[letter+1:] or status['italic']):
                            if letter+1 < len(this_line) and this_line[letter+1] == '*' and ('**' in this_line[letter+2:] or status['bold']):
                                if letter+2 < len(this_line) and this_line[letter+2] == '*' and ('***' in this_line[letter+3:] or (status['bold'] and status['italic'])):
                                    status['bold'] = not status['bold']
                                    status['italic'] = not status['italic']
                                    this_line = this_line[letter+3:]
                                    # this_line = this_line[:letter] + this_line[letter+3:]
                                else:
                                    status['bold'] = not status['bold']
                                    this_line = this_line[letter+2:]
                                    # this_line = this_line[:letter] + this_line[letter+2:]
                            else:
                                status['italic'] = not status['italic']
                                this_line = this_line[letter+1:]
                                # this_line = this_line[:letter] + this_line[letter+1:]
                            # 插入文本
                            passed += 1
                            insert_markdown(terminal, passed, text_to_insert, font_size=font_size, isbold=old_status['bold'], isitalic=old_status['italic'],  isstrikethrough=old_status['strikethrough'], ishighlight=old_status['highlight'], isunderline=old_status['underline'])
                            text_to_insert = ''
                            break
                        elif '*' == this_line[letter]:
                            text_to_insert += this_line[letter]
                            this_line = this_line[letter+1:]
                            passed += 1
                            # this_line = this_line[:letter] + this_line[letter+1:]
                            break

                        # _与*等效
                        elif this_line[letter] == '_' and ('_' in this_line[letter+1:] or status['italic']):
                            if letter+1 < len(this_line) and this_line[letter+1] == '_' and ('__' in this_line[letter+2:] or status['bold']):
                                if letter+2 < len(this_line) and this_line[letter+2] == '_' and ('___' in this_line[letter+3:] or (status['bold'] and status['italic'])):
                                    status['bold'] = not status['bold']
                                    status['italic'] = not status['italic']
                                    this_line = this_line[letter+3:]
                                    # this_line = this_line[:letter] + this_line[letter+3:]
                                else:
                                    status['bold'] = not status['bold']
                                    this_line = this_line[letter+2:]
                                    # this_line = this_line[:letter] + this_line[letter+2:]
                            else:
                                status['italic'] = not status['italic']
                                this_line = this_line[letter+1:]
                                # this_line = this_line[:letter] + this_line[letter+1:]
                            # 插入文本
                            passed += 1
                            insert_markdown(terminal, passed, text_to_insert, font_size=font_size, isbold=old_status['bold'], isitalic=old_status['italic'],  isstrikethrough=old_status['strikethrough'], ishighlight=old_status['highlight'], isunderline=old_status['underline'])
                            text_to_insert = ''
                            break
                        elif '_' == this_line[letter]:
                            text_to_insert += this_line[letter]
                            this_line = this_line[letter+1:]
                            passed += 1
                            # this_line = this_line[:letter] + this_line[letter+1:]
                            break

                        # ~~为删除线
                        elif this_line[letter] == '~' and (letter+2 < len(this_line) and '~~' in this_line[letter+2:] or status['strikethrough']):
                            if letter+1 < len(this_line) and this_line[letter+1] == '~' and ('~~' in this_line[letter+2:] or status['strikethrough']):
                                status['strikethrough'] = not status['strikethrough']
                                this_line = this_line[letter+2:]
                                # this_line = this_line[:letter] + this_line[letter+2:]
                            else:
                                status['strikethrough'] = not status['strikethrough']
                                this_line = this_line[letter+1:]
                                # this_line = this_line[:letter] + this_line[letter+1:]
                            # 插入文本
                            passed += 1
                            insert_markdown(terminal, passed, text_to_insert, font_size=font_size, isbold=old_status['bold'], isitalic=old_status['italic'],  isstrikethrough=old_status['strikethrough'], ishighlight=old_status['highlight'], isunderline=old_status['underline'])
                            text_to_insert = ''
                            break
                        elif '~' == this_line[letter]:
                            text_to_insert += this_line[letter]
                            this_line = this_line[letter+1:]
                            passed += 1
                            # this_line = this_line[:letter] + this_line[letter+1:]
                            break

                        # ==为高亮
                        elif this_line[letter] == '=' and (letter+2 < len(this_line) and'==' in this_line[letter+1:] or status['highlight']):
                            if letter+1 < len(this_line) and this_line[letter+1] == '=' and ('==' in this_line[letter+2:] or status['highlight']):
                                status['highlight'] = not status['highlight']
                                this_line = this_line[letter+2:]
                                # this_line = this_line[:letter] + this_line[letter+2:]
                            else:
                                status['highlight'] = not status['highlight']
                                this_line = this_line[letter+1:]
                                # this_line = this_line[:letter] + this_line[letter+1:]
                            # 插入文本
                            passed += 1
                            insert_markdown(terminal, passed, text_to_insert, font_size=font_size, isbold=old_status['bold'], isitalic=old_status['italic'],  isstrikethrough=old_status['strikethrough'], ishighlight=old_status['highlight'], isunderline=old_status['underline'])
                            text_to_insert = ''
                            break
                        elif '=' == this_line[letter]:
                            text_to_insert += this_line[letter]
                            this_line = this_line[letter+1:]
                            passed += 1
                            # this_line = this_line[:letter] + this_line[letter+1:]
                            break

                        else:
                            text_to_insert += this_line[letter]
                passed += 1
                insert_markdown(terminal, passed, '\n', font_size=font_size, isbold=status['bold'], isitalic=status['italic'],  isstrikethrough=status['strikethrough'], ishighlight=status['highlight'], isunderline=status['underline'])

            if font_size != 0:
                this_line = (font_size - 1) * '  ' + this_line
                passed += 1
                insert_markdown(terminal, passed, this_line + '\n', font_size)
        
        # terminal.insert('end', line1 + '\n')
        # terminal.insert('end',"{:^{}}".format('File End',len(line1)) + '\n')
        # terminal.insert('end', line1 + '\n')
            # else:
            #     # text_to_insert = this_line
            #     insert_markdown(terminal, round(passed), this_line + '\n')


    def readfile(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as fileHandle:
                text = fileHandle.read()
                text = text.splitlines()
            return text
        except:
            # # print("error:Read file Error")
            # sys.exit()
            return False

    # 对比异同
    def diff(self, command_inputed):
        terminal = self.terminal
        path_using = self.path_using
        if not self.inited:
            # file_path1 = easygui.fileopenbox(default=os.path.join(path_using, '*.*'))
            # file_path2 = easygui.fileopenbox(default=os.path.join(path_using, '*.*'))
            file_path1 = filedialog.askopenfilename(initialdir=path_using)
            file_path2 = filedialog.askopenfilename(initialdir=path_using)

        else:
            file_path2 = filedialog.askopenfilename(initialdir=path_using)
            dirs = os.listdir(os.path.join(
                path_using, '.filemanager', 'commits'))
            float_dir = []
            for i in dirs:
                float_dir.append(round(float(i)))

            float_dir.sort()

            # findin = self.now_at
            # if os.path.exists(os.path.join(path_using, '.filemanager', 'main', 'branches.json')):
            # 起始提交位置
            f = open(os.path.join(path_using, '.filemanager',
                                  'main', 'branches.json'), 'r', encoding='utf-8')
            info_data = json.load(f)
            f.close()
            branch = info_data['branches']

            commits_in_this_branch = []

            found = self.find_older_commit_in_branch(branch, self.now_at)

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
            if not (self.is_binary_file(file_path1) or self.is_binary_file(file_path2)):
                text1_lines = self.readfile(file_path1)
                text2_lines = self.readfile(file_path2)
                if text1_lines != False and text2_lines != False:
                    d = difflib.HtmlDiff()
                    # context=True时只显示差异的上下文，默认显示5行，由numlines参数控制，context=False显示全文，差异部分颜色高亮，默认为显示全文
                    if not self.inited:
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

        elif self.inited:
            terminal.insert('end', '\nerror:文件' + file_path2 +
                            '是这次提交新建的，无法与上一次提交对比', 'red')
        else:
            terminal.insert('end', '\nerror:文件不存在', 'red')

    # 写分支
    def write_branch(self, tree_in):
        path_using = self.path_using
        output = {'branches': tree_in, 'now_at': self.now_at}
        # dumps 将数据转换成字符串
        info_json = json.dumps(output, sort_keys=False,
                               indent=4, separators=(',', ': '))
        # 显示数据类型
        # print(type(info_json))
        f = open(os.path.join(path_using, '.filemanager',
                              'main', 'branches.json'), 'w', encoding='utf-8')
        f.write(info_json)
        f.close()

    # 寻找目标提交的所有父提交（顺着一条线下来）
    def find_older_commit_in_branch(self, branch_in, target):
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

    # 检出

    def checkout(self, start):
        path_using = self.path_using
        terminal = self.terminal

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

        found = self.find_older_commit_in_branch(info_data["branches"], start)

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
                if self.hash(os.path.join(path_using, i)) == file_hash_at_that_time[i]:
                    remove_from_delete_list.append(i)

        file_to_delete = set(file_to_delete) - set(remove_from_delete_list)

        # 删除文件
        pb = ShowProgress(terminal, 'Removing files({0[0]} of {0[1]})......')
        pb.update([0, 0])
        done = 0
        for i in file_to_delete:
            if os.path.exists(os.path.join(path_using, i)):
                try:
                    done += 1
                    pb.update([done, len(file_to_delete)])

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

        pb.update([len(file_to_delete), len(file_to_delete)])
        terminal.insert('end', 'Done.')
        terminal.update()

        # 复制文件
        pb = ShowProgress(
            terminal, 'Checking out files from your earlier commits......{0[0]} files have been checked out......')
        pb.update([0])
        done = 0
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
                                done += 1
                                pb.update([done])
                                # terminal.insert(
                                #     'end', '\nchecking out:'+str(os.path.join(path_using, file_realtive_path))+'\n')
                                # terminal.update()
                                # terminal.see('end')
                        except:
                            terminal.insert(
                                'end', '\nerror:'+str(os.path.join(root, name))+'导出失败\n', 'red')
                            terminal.update()
                            terminal.see('end')
        # if len(file_copy_dir) != 0:
        terminal.insert('end', 'Done.')
        terminal.update()

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
                    # print(int(terminal.index('end-1c').split('.')[0]))
                    terminal.delete(terminal.index(
                        'end-1c').split('.')[0]+'.0', 'end')
            if exit_flag:
                terminal.delete(terminal.index(
                    'end-1c').split('.')[0]+'.0', 'end')
                terminal.insert('end', '\nWaiting......Done.')
                break

        try:
            self.changes = {'changes': [], 'delete': [], 'create': []}
            os.remove(os.path.join(
                path_using, '.filemanager', 'main', 'timestamp.csv'))
            self.createtimestamp(path_using, 'timestamp.csv')
            # shutil.copy(os.path.join(path_using, '.filemanager', 'main', 'commits', str(float_dir[self.now_at]), 'timestamp.csv'),os.path.join(path_using, '.filemanager', 'main', 'timestamp.csv'))
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
                self.writefilehash(hash_path)
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
        self.write_branch(branch)

        self.print_branch()

    def help(self, inputten):
        terminal = self.terminal
        start_path = self.start_path
        with open(os.path.join(start_path, 'help', inputten+'.txt'), 'r') as f:
            help_command = f.read().splitlines()
            f.close()
        for i in help_command:
            terminal.insert('end', '\n' + i)

    def icon_for_window(self, tkwindow, temofilename='fm.ico'):
        tkwindow.iconbitmap(default=temofilename)

    def get_lastest_commit(self):
        f = open(os.path.join(self.path_using, '.filemanager',
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
                    branch[i]['include'][int(
                        j)] = branch_input[i]['include'][j]
                    if int(j) > branch_len:
                        branch_len = int(j)
                except:
                    pass

        now_branch_max_commit = 0

        for i in range(len(branch)):
            if fm.now_at in list(branch[i]['include'].keys()):
                now_at_branch = i
                for j in list(branch[i]['include'].keys()):
                    if int(j) > now_branch_max_commit:
                        now_branch_max_commit = int(j)
                break

        return now_branch_max_commit

    # def merge(merge_branch,merge_text):
        


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
# 窗口代码
def run_command(command, terminal, commandinput, fm):
    global path_using, command_inputed,  now_path, start_path, commit_text, command_chosen, used_before_command, asked_recommit, commit_text, need_update
    global attach
    def contiune_command():
        terminal.insert('end', '\n')
        # # print(info_add)
        # # print(path_using + info_add)
        TerminalText.insert('end', path_using + fm.info_add + '\n', 'green')
        if need_update:
            TerminalText.insert(
                'end', f'Warning: You are using FileManager v{terminal_infos.version}, however FileManager v{need_update} is available.You should consider upgrading via the "update" command.' + '\n', 'yellow')
        terminal.insert('end', f'$ ')
        terminal.window_create('end', window=commandinput)
        commandinput.focus_set()  # """

        # win_width = terminal.winfo_reqwidth()
        # win_height = terminal.winfo_reqheight()
        # # print(win_width,win_height)
    try:
        command_chosen = len(terminal_infos.input_list)
        used_before_command = False

        errortext = f'错误指令"{command.strip()}"。'

        command = str(command)  # 这玩意是应付编辑器不知道command是什么类型的

        terminal.config(state='n')  # 解锁terminal(Text)

        terminal.delete('end')  # 删除输入控件
        commandinput.delete(0, 'end')  # 删除控件里输入的文本

        if command.strip() == '':  # 如果啥也没输入
            terminal.insert('end', command)  # 就复述输入内容

        else:
            terminal_infos.input_list.append(command)  # 增加输入了什么命令
            terminal.insert('end', command)
            if fm.inited:
                fm.info_add = '('+fm.id_read[0:6]+'...)'
            else:
                fm.info_add = ''
            if now_path == '':
                fm.path_using = start_path
            else:
                fm.path_using = now_path
            # console.# print("FM "+path_using+">",end='', style='underline')
            # command_inputed = input().split()
            # command_inputed = input("FM " + path_using + info_add + ">")
            command_inputed = command

            # pattern1 = re.compile(r'"(\w+)"')
            # pattern2 = re.compile(r"'(\w+)'")
            # pth1=pattern1.findall(command_inputed)
            # pth2=pattern2.findall(command_inputed)
            # if ',' in command_inputed:
            #     command_inputed = command_inputed.split(',')
            # else:
            command_inputed = command_inputed.split()

            if command_inputed[0] == "?" or command_inputed[0] == "help":
                if len(command_inputed) > 1:
                    if command_inputed[1] == '-?':
                        webbrowser.open(fm.help_url, new=0, autoraise=True)
                else:
                    fm.help('help')
                contiune_command()

            elif command_inputed[0] == "init":
                if len(command_inputed) == 1:
                    # terminal.insert('end', command)
                    # terminal.update()
                    fm.init()
                    # terminal.insert('end','Done')
                elif '-?' in command_inputed:
                    fm.help('init')
                elif command_inputed[1] == 'newrepo':
                    # terminal.insert('end', command)
                    fm.newrepo(path_using)
                elif '-exit' in command_inputed:
                    # terminal.insert('end', command)
                    fm.inited = False
                elif '-update' in command_inputed:
                    fm.update()
                    fm.init()
                elif '-m' in command_inputed:
                    fm.init()
                    terminal.insert(
                        'end', '\nWARNING:命令"init -m"在fillemanager 1.1.0版本被弃用。使用命令"set monitor on"以替代。', 'yellow')
                    # if self.inited:
                    #     add_to_monitor()
                    #     terminal.insert('end', '\n仓库"{0}"已被添加至监控目录\n'.format(path_using))
                elif '-rm' in command_inputed:
                    fm.init()
                    terminal.insert(
                        'end', '\nWARNING:命令"init -rm"在fillemanager 1.1.0版本被弃用。使用命令"set monitor off"以替代。', 'yellow')
                    # if self.inited:
                    #     delete_from_monitor()
                    #     terminal.insert('end', '\n仓库"{0}"已被从监控目录中移除\n'.format(path_using))
                # terminal.insert('end',command)
                contiune_command()

            elif command_inputed[0] == 'cd':
                if len(command_inputed) == 1:
                    # terminal.insert('end', command)
                    # contiune_command()
                    terminal.insert('end', '\nerror:移动工作目录失败。\n', 'red')
                    # # print('\nerror:没有输入路径', 'red')
                elif '-?' in command_inputed:
                    fm.help('cd')
                else:
                    new_path = ''
                    # 如果len(command_inputed) > 2, 则有可能是路径中存在空格
                    # 这时尝试提取引号内的内容
                    if '"' in command or "'" in command:
                        all_text = command
                        # print(all_text)
                        # text1 = pattern1.findall(all_text)
                        # text2 = pattern2.findall(all_text)
                        text1 = all_text.split("\"")
                        text2 = all_text.split("\'")
                        if len(text1) <= 1 and len(text2) <= 1:
                            terminal.insert('end', "\nerror:无效的文件名", 'red')
                        elif len(text1) <= 1:
                            new_path = text2[1]
                        else:
                            new_path = text1[1]
                    elif len(command_inputed) == 2:
                        new_path = command_inputed[1]
                        
                    if new_path != '':
                        try:
                            os.chdir(path_using)
                            os.chdir(new_path)
                            path_using = now_path = os.getcwd()
                            os.chdir(start_path)
                            fm.inited = False
                            fm.info_add = ''
                            fm.changes = {'changes': [],
                                        'delete': [], 'create': []}
                            fm.process_path = {'changes': [],
                                            'delete': [], 'create': []}

                        except OSError as error:
                            terminal.insert('end', '\nerror:'+error.args[1], 'red')
                        except:
                            terminal.insert('end', '\nerror:移动工作目录失败。', 'red')
                    else:
                        terminal.insert('end', '\nerror:无效的工作目录。', 'red')
                        terminal.insert('end', "\nWarning:这个错误可能是您的工作目录的路境内存在空格所致。请使用引号以解决此问题。", 'yellow')
                
                contiune_command()

            elif command_inputed[0] == 'refresh':
                if '-?' in command_inputed:
                    fm.help('refresh')
                    contiune_command()
                elif fm.inited:
                    fm.refresh()
                    contiune_command()
                else:
                    terminal.insert('end', '\nerror:您还没有加载这个仓库', 'red')
                    contiune_command()

            elif command_inputed[0] == 'add':
                if '-?' in command_inputed:
                    fm.help('add')
                # terminal.insert('end', command)
                elif '"' in command or "'" in command:
                    all_text = command
                    # print(all_text)
                    # text1 = pattern1.findall(all_text)
                    # text2 = pattern2.findall(all_text)
                    file_name = ''
                    text1 = all_text.split("\"")
                    text2 = all_text.split("\'")
                    if len(text1) <= 1 and len(text2) <= 1:
                        terminal.insert('end', "\nerror:无效的文件名", 'red')
                    elif len(text1) <= 1:
                        file_name = text2[1]
                    else:
                        file_name = text1[1]

                    if file_name != '':
                        fm.add([os.path.join(fm.path_using, file_name)], command_inputed)
                    else:
                        terminal.insert('end', "\nerror:无效的文件名", 'red')

                else:
                    fm.add([], command_inputed)
                contiune_command()

            elif command_inputed[0] == 'commit':
                if '-?' in command_inputed:
                    fm.help('commit')
                    contiune_command()
                # terminal.insert('end', command)
                elif not fm.process_path == {'changes': [], 'delete': [], 'create': []}:
                    # pattern1 = re.compile(r"'(\w+)'")
                    # pattern2 = re.compile(r'"(\w+)"')
                    all_text = command
                    # print(all_text)
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
                        if commit_text[0] == '#':
                            terminal.insert('end', "\nerror:提交说明不能以#开头。", 'red')
                        else:
                            if '-f' in command_inputed:
                                fm.commit(commit_text, '', attach=True)
                            else:
                                fm.commit(commit_text, '')
                    contiune_command()
                else:
                    terminal.insert('end', '\nerror:没有要提交的内容', 'red')
                    contiune_command()

            elif command_inputed[0] == 'diff':
                if '-?' in command_inputed:
                    fm.help('diff')
                    contiune_command()
                else:
                    # terminal.insert('end', command)
                    fm.diff(command_inputed)
                    contiune_command()

            elif command_inputed[0] == 'branch':
                if '-?' in command_inputed:
                    fm.help('branch')
                elif fm.inited:
                    # terminal.insert('end', command)
                    # if '-s' in command_inputed or len(command_inputed) == 1 or '-m' in command_inputed:
                    #     if '-g' in command_inputed or '-m' in command_inputed or len(command_inputed) == 1:
                    #         if '-m' in command_inputed:
                    #             fm.now_at = int(
                    #                 command_inputed[command_inputed.index('-m') + 1])
                    fm.print_branch()
                else:
                    terminal.insert('end', '\nerror:您还没有加载这个仓库', 'red')

                contiune_command()

            elif command_inputed[0] == 'checkout':
                if '-?' in command_inputed:
                    fm.help('checkout')
                elif fm.inited:
                    if len(command_inputed) > 1:
                        try:
                            if command_inputed[1] == '.':
                                
                                fm.now_at = fm.get_lastest_commit()
                            else:
                                fm.now_at = int(command_inputed[1])
                        except:
                            pass
                    # terminal.insert('end', command)
                    # if len(command_inputed) == 1:
                        fm.checkout(fm.now_at)
                    else:
                        terminal.insert('end', '\nerror:无效的参数', 'red')
                    # else:
                    # checkout(self.now_at,command_inputed[1],terminal)
                else:
                    terminal.insert('end', '\nerror:您还没有加载这个仓库', 'red')
                contiune_command()

            elif command_inputed[0] == 'reload':
                if '-?' in command_inputed:
                    fm.help('reload')
                elif fm.inited:
                    # terminal.insert('end', command)
                    fm.reload()
                    fm.printchanges()
                else:
                    terminal.insert('end', '\nerror:您还没有加载这个仓库', 'red')
                contiune_command()

            elif command_inputed[0] == 'show':
                if '-?' in command_inputed:
                    fm.help('show')
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
                    elif command_inputed[1] == 'detailedCommitText':
                        if len(command_inputed) > 2:
                            id = command_inputed[2]
                            open_path = fm.getMDFromId(id)
                            if os.path.exists(open_path):
                                fm.parseMarkDown(open_path)
                            else:
                                terminal.insert('end', '\nerror:无效的id', 'red')
                else:
                    terminal.insert('end', '\nerror:无效的参数', 'red')
                contiune_command()

            elif command_inputed[0] == 'set':
                if '-?' in command_inputed:
                    fm.help('set')
                elif fm.inited:
                    if len(command_inputed) == 2:
                        if command_inputed[1] == '.ignore':
                            if not os.path.exists(os.path.join(path_using, '.ignore')):
                                with open(os.path.join(path_using, '.ignore'), 'w', encoding='utf-8') as f:
                                    f.write(
                                        '# Please write down paths and files you want to ignore below：')
                                    f.close()
                                terminal.insert(
                                    'end', '\n在{0}目录下创建了.ignore文件'.format(path_using))
                            else:
                                terminal.insert(
                                    'end', '\nerror:.ignore文件已存在', 'red')
                        else:
                            terminal.insert('end', '\nerror:无效的参数', 'red')
                    elif len(command_inputed) > 2:
                        if command_inputed[1] == 'monitor':
                            if command_inputed[2] == 'on':
                                fm.add_to_monitor()
                                terminal.insert(
                                    'end', '\n仓库"{0}"已被添加至监控目录'.format(path_using))

                            elif command_inputed[2] == 'off':
                                fm.delete_from_monitor()
                                terminal.insert(
                                    'end', '\n仓库"{0}"已被从监控目录中移除'.format(path_using))
                            else:
                                terminal.insert('end', '\nerror:无效的参数', 'red')
                        else:
                            terminal.insert('end', '\nerror:无效的参数', 'red')
                    else:
                        terminal.insert('end', '\nerror:无效的参数', 'red')

                else:
                    terminal.insert('end', '\nerror:您还没有加载这个仓库', 'red')
                contiune_command()

            elif command_inputed[0] == 'recommit':
                if '-?' in command_inputed:
                    fm.help('recommit')
                    contiune_command()
                # terminal.insert('end', command)
                elif not fm.process_path == {'changes': [], 'delete': [], 'create': []}:
                    if asked_recommit:
                        terminal.config(state='n')  # 解锁terminal(Text)

                        terminal.delete('end')  # 删除输入控件
                        # commandinput.delete(0, 'end')  # 删除控件里输入的文本
                        terminal.update()
                        if str(command).strip() == '':  # 如果啥也没输入
                            terminal.insert('end', command)  # 就复述输入内容
                        else:
                            # terminal.insert('end', '\n' + command + '\n')
                            terminal.update()
                            if command == 'recommit':
                                if attach:
                                    fm.recommit(commit_text, attach=True)
                                else:
                                    fm.recommit(commit_text)
                        contiune_command()
                        asked_recommit = False
                    else:
                        all_text = command
                        # print(all_text)
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

                        if commit_text != '':
                            if commit_text[0] == '#':
                                terminal.insert('end', "\nerror:提交说明不能以#开头。", 'red')
                            else:
                                if '-f' in command_inputed:
                                    attach=True
                                else:
                                    attach=False

                            terminal.insert('end', '\n为了确认，在下方输入"recommit"\n')
                            terminal.window_create('end', window=commandinput)
                            commandinput.focus_set()
                            asked_recommit = True

                            if ('--no-confirm') in command_inputed:
                                asked_recommit = False
                                terminal.config(state='n')  # 解锁terminal(Text)

                                terminal.delete('end')  # 删除输入控件
                                # commandinput.delete(0, 'end')  # 删除控件里输入的文本
                                terminal.update()
                                if attach:
                                    fm.recommit(commit_text, attach=True)
                                else:
                                    fm.recommit(commit_text)
                                contiune_command()


                    # entry_str = simpledialog.askstring(
                    #     title='确认', prompt='为了确认，在下方输入:RECOMMIT ')
                    # pattern1 = re.compile(r"'(\w+)'")
                    # pattern2 = re.compile(r'"(\w+)"')
                else:
                    terminal.insert('end', '\nerror:没有要提交的内容', 'red')
                    contiune_command()

            # elif command_inputed[0] == 'reset':
            #     if '-?' in command_inputed:
            #         fm.help('reset')
            #         contiune_command()
            #     # terminal.insert('end', command)
            #     elif not fm.process_path == {'changes': [], 'delete': [], 'create': []}:
            #         if asked_recommit:
            #             terminal.config(state='n')  # 解锁terminal(Text)

            #             terminal.delete('end')  # 删除输入控件
            #             # commandinput.delete(0, 'end')  # 删除控件里输入的文本
            #             terminal.update()
            #             if str(command).strip() == '':  # 如果啥也没输入
            #                 terminal.insert('end', command)  # 就复述输入内容
            #             else:
            #                 # terminal.insert('end', '\n' + command + '\n')
            #                 terminal.update()
            #                 if command == 'reset':
            #                     if attach:
            #                         fm.recommit(commit_text, attach=True)
            #                     else:
            #                         fm.recommit(commit_text)
            #             contiune_command()
            #             asked_recommit = False
            #         else:
            #             all_text = command
            #             # print(all_text)
            #             # text1 = pattern1.findall(all_text)
            #             # text2 = pattern2.findall(all_text)
            #             commit_text = ''
            #             text1 = all_text.split("\"")
            #             text2 = all_text.split("\'")
            #             if len(text1) <= 1 and len(text2) <= 1:
            #                 terminal.insert('end', "\nerror:没有提交说明", 'red')
            #             elif len(text1) <= 1:
            #                 commit_text = text2[1]
            #             else:
            #                 commit_text = text1[1]

            #             if commit_text != '':
            #                 if commit_text[0] == '#':
            #                     terminal.insert('end', "\nerror:提交说明不能以#开头。", 'red')
            #                 else:
            #                     if '-f' in command_inputed:
            #                         attach=True
            #                     else:
            #                         attach=False

            #                 terminal.insert('end', '\n为了确认，在下方输入"recommit"\n')
            #                 terminal.window_create('end', window=commandinput)
            #                 commandinput.focus_set()
            #                 asked_recommit = True

            elif command_inputed[0] == 'update':
                if '-?' in command_inputed:
                    fm.help('update')
                elif need_update:
                    os.startfile('updater.exe')
                    sys.exit(0)
                else:
                    terminal.insert('end', '\nerror:没有更新', 'red')
                    contiune_command()

            elif command_inputed[0] == "run":
                # 如果len(command_inputed) == 1，说明没有输入文件名
                if '-?' in command_inputed:
                    fm.help('run')
                    contiune_command()
                elif len(command_inputed) == 1:
                    terminal.insert('end', '\nerror:没有输入文件名', 'red')
                    contiune_command()
                else:
                    # 判断文件是否存在
                    os.chdir(path_using)
                    if os.path.exists(command_inputed[1]):
                        # contiune_command()
                        # 如果command字符串里存在--values参数，则提取--values:后面的引号里值
                        if '--values' in command:
                            pattern = re.compile(r'--values:(.*)')
                            values = pattern.findall(command)
                            if len(values) == 1:
                                # 如果有值，就用这个值替换掉values.txt
                                value = '{' + values[0] +'}'
                                contiune_command()
                                try:
                                    run_command_from_file(command_inputed[1], values=value)
                                except Exception as e:
                                    # terminal.insert('end', traceback.format_exc(), 'red')
                                    terminal.insert('end', f'\nerror:{e}', 'red')
                                    contiune_command()

                            else:
                                terminal.insert('end', '\nerror:只能有一个参数"values"', 'red')
                                contiune_command()
                        else:
                            contiune_command()
                            try:
                                run_command_from_file(command_inputed[1])
                            except Exception as e:
                                # terminal.insert('end', traceback.format_exc(), 'red')
                                terminal.insert('end', f'\nerror:{e}', 'red')
                                contiune_command()
                    else:
                        terminal.insert('end', '\nerror:文件不存在', 'red')
                        contiune_command()
                os.chdir(start_path)

            elif command_inputed[0] == "exit":
                if '-?' in command_inputed:
                    fm.help('exit')
                else:
                    sys.exit(0)
            
            # elif command_inputed[0] == "pm":
            #     fm.parseMarkDown('s')

            else:
                # terminal.insert('end', command)
                terminal.insert('end', '\nerror:未知的命令', 'red')
                contiune_command()

    except Exception as e:
        # terminal.insert('end', traceback.format_exc(), 'red')
        terminal.insert('end', f'\nerror:{e}', 'red')
        contiune_command()

    terminal.config(state='d')
    terminal.see('end')


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

# 读取*.fmc文件，执行其中的命令
def run_command_from_file(file_path, values = ''):
    global path_using, start_path, command_input, TerminalText, command_input, fm
    work_dir = path_using
    start_dir = start_path

    if values != '':
        # 将'xx':'xxx'更改为"xx":"xxx"
        values = re.sub(r"'(.*?)':'(.*?)'", r'"\1":"\2"', values)

        values = values.replace("\\","/")
        # values = re.findall(, values)
        # 使用json解析value的字符串
        values = json.loads(values)
        # 将value的内容倒入locals()
        for key in values.keys():
            locals()[key] = values[key]

    os.chdir(path_using)
    command_file = open(file_path, 'r', encoding='utf-8')
    commands = command_file.read().splitlines()
    command_file.close()
    if commands[0].startswith("\ufeff"):
        # 删掉这个\ufeff
        commands[0] = commands[0][1:]
    os.chdir(start_path)

    for cmd in commands:
        # 如果是空行，就跳过
        # 如果以//开头，就跳过
        if cmd == '' or cmd.startswith('//'):
            pass
        # 如果以exec"""开头，就执行exec后面数行的内容直到结尾的"""

        elif cmd.startswith('exec"""'):
            # 读取exec后面的内容
            exec_content = []
            for cmd_line in range(commands.index(cmd) + 1, len(commands)):
            # for j in commands[commands.index(i)+1:]:
                if commands[cmd_line] == '"""':
                    # 从commands里删除commands.index(i)到j的内容
                    del commands[commands.index(cmd):cmd_line]
                    break
                elif commands[cmd_line] != '':
                    exec_content.append(commands[cmd_line])

            all_command = ''
            # 执行exec后面的内容
            all_command = '\n'.join(exec_content)
                # print(j)
            command_to_run = compile(all_command,'abc','exec')
            eval(command_to_run)
            # print(commands)

        else:
            # 替换i内所有的${{变量名}}为对应的变量内容
            for cmd_line in list(locals().keys()):
                # print(cmd_line)
                cmd = cmd.replace('${0}'.format('{{' + cmd_line + '}}'), str(locals()[cmd_line]))

            command_input.delete(0, 'end')
            command_input.insert('end', cmd)
            run_command(command_input.get(), TerminalText, command_input, fm)


command_chosen = 0
used_before_command = False

# 按键盘上的↑时，将输入框的内容替换为上一次输入的内容，再按就是上上次输入的内容
def commandup(inputen):
    # 如果上一次输入命令后还没有按过键盘的↑↓键
    global command_chosen, terminal_infos, used_before_command
    if not used_before_command:
        used_before_command = True
    elif command_chosen > 0:
        command_chosen -= 1
    else:
        command_chosen = len(terminal_infos.input_list) - 1
    inputen.delete(0, 'end')
    inputen.insert('end', terminal_infos.input_list[command_chosen])


def commanddown(inputen):
    global command_chosen, terminal_infos, used_before_command
    if not used_before_command:
        used_before_command = True
        command_chosen = 0
    elif len(terminal_infos.input_list) - 1 > command_chosen:
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

# print("start")
# 检查更新


def checkUpdate():
    global need_update
    # print("t1")
    # need_update不为空时，说明有更新
    need_update = os.popen('updater.exe --show-version').read()

    # print(os.popen(os.path.join(start_path, 'updater.exe')).read())
    # print(os.popen('updater.exe').read())
# 启动线程
checkupdate = threading.Thread(target=checkUpdate)
checkupdate.setDaemon(True)
checkupdate.start()

# 创建窗口
root = tk.Tk()
# 设置标题
root.title(f'FileManager(FM) v{terminal_infos.version}')

# print('done')
# print("start")
# print(os.popen(os.path.join(start_path, 'updater.py')).read())
# print('done')
# os.popen(os.path.join(start_path, 'checkupdate.bat'))

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
TerminalText.insert('end', f'FileManager(FM) v{terminal_infos.version}\n')
TerminalText.insert('end', 'Type "help" or "?" for help.\n')

# 命令输入框
command_input = tk.Entry(TerminalText, font=('consolas', 13), fg='white', bg='black',
                         insertbackground='white', selectforeground='black', selectbackground='white', relief='flat', width=66)
command_input.bind('<Return>', lambda v=0: run_command(
    command_input.get(), TerminalText, command_input, fm))
# 在命令输入框中按F7弹出命令列表窗口
command_input.bind('<F7>', lambda v=0: post_inputlist(command_input))

# 上下箭头选择命令
command_input.bind('<Up>', lambda v=0: commandup(command_input))
command_input.bind('<Down>', lambda v=0: commanddown(command_input))

fm = FileManager(TerminalText, command_input)
fm.start_path = start_path
fm.path_using = path_using

logo = printlogo.logo()
for i in logo:
    TerminalText.insert('end', i + '\n')

# path_using = start_path
# 后面的'green'就是tag标记，他会应用green这个tag的属性
TerminalText.insert('end', path_using + fm.info_add+'\n', 'green')
TerminalText.insert('end', f'$ ')


# 插入命令输入框
TerminalText.window_create('end', window=command_input)

# 让终端Text不可编辑
TerminalText['state'] = 'd'


def click(event):
    command_input.focus_set()

# 说明有参数
if len(sys.argv) > 1:
    # 如果是个文件 => 执行它
    if os.path.isfile(sys.argv[1]):
        command = 'run ' + sys.argv[1]
    else:
        # 将sys.argv第二位到最后一位的参数合并为一个字符串
        command = ' '.join(sys.argv[1:])
    if not os.path.isdir(command):
        # 传入参数
        command_input.insert('end', command)
        # 执行命令
        run_command(command_input.get(), TerminalText, command_input, fm)

# focus
root.bind("<Double-Button-1>", click)

# 循环窗口
root.mainloop()
