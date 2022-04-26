from watchdog.observers import Observer
from watchdog.events import *
import time
import os

with open(f'{os.getcwd()}\path.txt', "r", encoding='utf-8') as p:
    path = p.read().splitlines()
    p.close()
    #print(path)

csv_path = r".filemanager\main\now_list_dong.csv"

def write(data):
    global path
    if not data[2] == '':
        # if '\\.filemanager' in data[1]:
        # 不是moved
        if '\\.filemanager' in data[1] and '\\.filemanager' in data[2]:
            pass

        elif '\\.filemanager' not in data[1] and '\\.filemanager' in data[2]:
            if data[0] == 'file_moved':
                data[0] = 'file_deleted'
            else:
                data[0] = 'dir_deleted'
            for k in path:
                if len(data[1]) > len(k):
                    if data[1][0:len(k)] == k:
                        with open (os.path.join(k,'.filemanager','main','now_list_doing.csv'),'a',encoding='utf-8') as f:
                            f.write(data[0] + ',' + os.path.relpath(data[1],k) + '\n')
                            break
            
        
        elif '\\.filemanager' in data[1] and '\\.filemanager' not in data[2]:
            if data[0] == 'file_moved':
                data[0] = 'file_created'
            else:
                data[0] = 'dir_created'
            for k in path:
                if len(data[1]) > len(k):
                    if data[1][0:len(k)] == k:
                        with open (os.path.join(k,'.filemanager','main','now_list_doing.csv'),'a',encoding='utf-8') as f:
                            f.write(data[0] + ',' + os.path.relpath(data[2],k) + '\n')
                            break

        elif '\\.filemanager' not in data[1] and '\\.filemanager' not in data[2]:
            for k in path:
                if len(data[1]) > len(k):
                    if data[1][0:len(k)] == k:
                        with open (os.path.join(k,'.filemanager','main','now_list_doing.csv'),'a',encoding='utf-8') as f:
                            f.write(data[0] + ',' + os.path.relpath(data[1],k) + ',' + os.path.relpath(data[2],k) + '\n')
                            break
    elif '\\.filemanager' not in data[1]:
        for k in path:
            if len(data[1]) > len(k):
                if data[1][0:len(k)] == k:
                    with open (os.path.join(k,'.filemanager','main','now_list_doing.csv'),'a',encoding='utf-8') as f:
                        f.write(data[0] + ',' + os.path.relpath(data[1],k) + '\n')
                        break

##if not os.path.exists(csv_path):
##    write(['operation type', 'from', 'to'])

class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            #print("directory moved from {0} to {1}".format(
                # event.src_path, event.dest_path))
            write(
                ['dir_moved', event.src_path, event.dest_path])
        else:
            #print("file moved from {0} to {1}".format(
                # event.src_path, event.dest_path))
            write(['file_moved', event.src_path, event.dest_path])

    def on_created(self, event):
        if event.is_directory:
            #print("directory created:{0}".format(event.src_path))
            write(['dir_created', event.src_path, ''])
        else:
            #print("file created:{0}".format(event.src_path))
            write(['file_created', event.src_path, ''])

    def on_deleted(self, event):
        if event.is_directory:
            #print("directory deleted:{0}".format(event.src_path))
            write(['dir_deleted', event.src_path, ''])
        else:
            #print("file deleted:{0}".format(event.src_path))
            write(['file_deleted', event.src_path, ''])

    def on_modified(self, event):
        if event.is_directory:
            pass
            #print("directory modified:{0}".format(event.src_path))
        else:
            #print("file modified:{0}".format(event.src_path))
            write(['file_modified', event.src_path, ''])


if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    for i in path:
        if os.path.exists(os.path.join(i,'.filemanager','main','now_list_doing.csv')):
            observer.schedule(event_handler, i, True)
    observer.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
