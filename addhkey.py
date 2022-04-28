# -*- coding: utf-8 -*-

''' 为程序添加右键菜单打开方式 '''

import winreg as reg
import os

def add_context_menu_parent(parent_name,reg_root_key_path,reg_key_path,prog_path,icon_path):
    '''
    封装的添加一个右键一级菜单的方法
    :param parent_name: 显示的菜单名称
    :param reg_root_key_path: 注册表根键路径
    :param reg_key_path: 要添加到的注册表父键的路径（相对路径）
    :param shortcut_key: 菜单快捷键，如：'S'
    :return:
    '''
    # 打开名称父键
    key = reg.OpenKey(reg_root_key_path, reg_key_path)
    # 为key创建一个名称为menu_name的sub_key，并设置sub_key的值为menu_name加上快捷键，数据类型为REG_SZ字符串类型
    reg.SetValue(key, parent_name, reg.REG_SZ,'')

    # 打开刚刚创建的名为menu_name的sub_key
    sub_key = reg.OpenKey(key, parent_name,0,reg.KEY_ALL_ACCESS)
    reg.SetValue(sub_key, 'command', reg.REG_SZ, prog_path + ' %V')

    # 为sub_key设置成可添加二级菜单
    # reg.SetValueEx(sub_key, 'MUIVerb', 0, reg.REG_SZ, parent_name + '(&{0})'.format(shortcut_key))
    reg.SetValueEx(sub_key, 'icon', 0, reg.REG_SZ, icon_path)

    # 关闭sub_key和key
    reg.CloseKey(sub_key)
    reg.CloseKey(key)

if __name__ == '__main__':
    home = os.path.expanduser('~')
    # print(home)
    # os.system('pause')
    install_path = os.path.join(home, r'AppData\Local\Programs\FileManager\fm\fm.exe')
    add_context_menu_parent('在这里打开FileManager', reg.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell', install_path, install_path)
    