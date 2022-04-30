# import sys
from urllib import response
import requests,os,shutil
from tqdm import tqdm

def download(url, file_path):
    # 重试计数
    count = 0
    # 第一次请求是为了得到文件总大小
    r1 = requests.get(url, stream=True, verify=True)
    total_size = int(r1.headers['Content-Length'])
 
    # 判断本地文件是否存在，存在则读取文件数据大小
    if os.path.exists(file_path):
        old_size = temp_size = os.path.getsize(file_path)  # 本地已经下载的文件大小
    else:
        old_size = temp_size = 0
        
    # 对比一下，是不是还没下完
    # print(temp_size)
    # print(total_size)
    
    # 开始下载
    while count < 10:
        if count != 0:
            temp_size = os.path.getsize(file_path)
        # 文件大小一致，跳出循环
        if temp_size >= total_size:
            break
        count += 1
        # print(
        #     "第[{}]次下载文件,已经下载数据大小:[{}],应下载数据大小:[{}]".format(
                # count, temp_size, total_size))
        # 重新请求网址，加入新的请求头的
        # 核心部分，这个是请求下载时，从本地文件已经下载过的后面下载
        headers = {"Range": f"bytes={temp_size}-{total_size}"}
        # r = requests.get(url, stream=True, verify=False)
        r = requests.get(url, stream=True, verify=True, headers=headers)
 
        # "ab"表示追加形式写入文件
        with open(file_path, "ab") as f, tqdm(
            desc='Downloading',
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024
        ) as bar:
            if count != 1:
                f.seek(temp_size)
            for chunk in r.iter_content(chunk_size=1024 * 64):
                if chunk:
                    if old_size:
                        bar.update(old_size)
                        old_size = 0
                    bar.update(len(chunk))
                    temp_size += len(chunk)
                    f.write(chunk)
                    f.flush()
                    ###这是下载实现进度显示####
                    # done = int(50 * temp_size / total_size)
                    # sys.stdout.write("\r|%s%s| %d%%" % (
                    #     '█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                    # sys.stdout.flush()
        # print("\n")
 
    return file_path

# def download(url: str, fname: str):
#     # 用流stream的方式获取url的数据
#     resp = requests.get(url, stream=True)
#     # 拿到文件的长度，并把total初始化为0
#     total = int(resp.headers.get('content-length', 0))
#     # 打开当前目录的fname文件(名字你来传入)
#     # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
#     with open(fname, 'wb') as file, tqdm(
#         desc='Downloading',
#         total=total,
#         unit='iB',
#         unit_scale=True,
#         unit_divisor=1024,
#     ) as bar:
#         for data in resp.iter_content(chunk_size=1024):
#             size = file.write(data)
#             bar.update(size)

# with open('url.txt','r',encoding='utf-8') as f:
#     url = f.read()
#     f.close()

url = 'https://api.github.com/repos/yubac/filemanager/releases/latest'

response = requests.get(url)
# response = requests.get("https://api.github.com/repos/yubac/filemanager/releases/latest")
# response = requests.get("https://api.github.com/repos/[用户名]/[仓库名]/releases/latest")
# print(response.json()["tag_name"])
# print(response.json()["assets"][0]["browser_download_url"])

with open ('version.txt','r') as f:
    version = f.read()
    f.close()

if version != response.json()["tag_name"]:
    print('有新的版本可用：{0}，是否下载？'.format(response.json()["tag_name"]))
    yn = input('(y/N)')
    if yn == 'y' or yn == 'Y':
        if os.path.exists('D:\\'):
            path = 'D:\\fmupdate'
        else:
            path = 'C:\\fmupdate'
        if os.path.exists(path) and not os.path.exists(os.path.join(path, 'not_finished.txt')):
            shutil.rmtree(path)
            os.makedirs(path)
            with open(os.path.join(path, 'not_finished.txt'), 'w', encoding='utf-8') as f:
                f.write('')
                f.close()
        elif not os.path.exists(os.path.join(path, 'not_finished.txt')):
            os.makedirs(path)
            f = os.popen('attrib +h ' + path)
            f.close()
            with open(os.path.join(path, 'not_finished.txt'), 'w', encoding='utf-8') as f:
                f.write('')
                f.close()

        with open(os.path.join(path,'README.txt'),'w',encoding='utf-8') as f:
            f.write("aassddff\n这是filemanager更新用的临时文件夹。\n请不要更改这个文件夹下的任何文件，\n更新完成后会自动删除。")
            f.close()
        # download('https://ajrkvs1g.fast-github.tk/' + response.json()["assets"][0]["browser_download_url"], os.path.join(path,response.json()["assets"][0]["name"]))
        download('https://ghproxy.com/' + response.json()["assets"][0]["browser_download_url"], os.path.join(path,response.json()["assets"][0]["name"]))

        # os.system('endall.bat')

        print('Unpackaging......',end='')

        os.makedirs(os.path.join(path,'unpackage'))
        shutil.unpack_archive(os.path.join(path,response.json()["assets"][0]["name"]), os.path.join(path,'unpackage'))

        print('Done.')
        # print('Deleting the old......',end='')
        # # shutil.rmtree(os.path.join(os.getcwd(),'monitor'))
        # # shutil.rmtree(os.path.join(os.getcwd(),'fm'))
        # print('Done.')

        with open(os.path.join(path, 'startinstall.bat'), 'w', encoding='utf-8') as f:
            f.write('start ' + str(path) + r'\unpackage\install.bat')
        os.remove(os.path.join(path, 'not_finished.txt'))
        os.system(os.path.join(path, 'startinstall.bat'))