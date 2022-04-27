from urllib import response
import requests,os,shutil
from tqdm import tqdm

def download(url: str, fname: str):
    # 用流stream的方式获取url的数据
    resp = requests.get(url, stream=True)
    # 拿到文件的长度，并把total初始化为0
    total = int(resp.headers.get('content-length', 0))
    # 打开当前目录的fname文件(名字你来传入)
    # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
    with open(fname, 'wb') as file, tqdm(
        desc='Downloading',
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

with open('url.txt','r',encoding='utf-8') as f:
    url = f.read()
    f.close()

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
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        f = os.popen('attrib +h ' + path)
        f.close()

        with open(os.path.join(path,'README.txt'),'w',encoding='utf-8') as f:
            f.write("aassddff\n这是filemanager更新用的临时文件夹。\n请不要更改这个文件夹下的任何文件，\n更新完成后会自动删除。")
            f.close()
        download('https://ajrkvs1g.fast-github.tk/' + response.json()["assets"][0]["browser_download_url"], os.path.join(path,response.json()["assets"][0]["name"]))
        download('https://gh.api.99988866.xyz/' + response.json()["assets"][0]["browser_download_url"], os.path.join(path,response.json()["assets"][0]["name"]))

        # os.system('endall.bat')

        print('Unpackaging......',end='')

        os.makedirs(os.path.join(path,'unpackage'))
        # shutil.unpack_archive(os.path.join(path,response.json()["assets"][0]["name"]), os.path.join(path,'unpackage'))

        print('Done.')
        print('Deleting the old......',end='')
        # shutil.rmtree(os.path.join(os.getcwd(),'monitor'))
        # shutil.rmtree(os.path.join(os.getcwd(),'fm'))
        print('Done.')

        with open(os.path.join(path, 'startinstall.bat'), 'w', encoding='utf-8') as f:
            f.write('start ' + str(path) + r'\unpackage\install.bat')
        os.system(os.path.join(path, 'startinstall.bat'))