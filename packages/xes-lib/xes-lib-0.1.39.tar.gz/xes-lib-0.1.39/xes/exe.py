import PyInstaller
import os
print("打包开始")


def replace_and_write(source_file, target_file, old_text, new_text, beforeCode):
    # 获取调用此函数的脚本所在的目录
    script_dir = os.getcwd()
    # 构建完整的源文件和目标文件路径
    source_path = os.path.join(script_dir, source_file)
    target_path = os.path.join(script_dir, target_file)
    with open(source_file, 'r',encoding='utf8') as file:
        data = file.read()

    data = data.replace(old_text, new_text)
    data = beforeCode + data
    with open(target_file, 'w',encoding='utf8') as file:
        file.write(data)

# 使用示例
beforeCode = '''
import tempfile
import os, sys
# 添加这段代码
from xes.cert import CERT_DATA
temp_cert = tempfile.NamedTemporaryFile(delete=False, encoding="utf-8", mode="w")
temp_cert.write(CERT_DATA)
temp_cert.flush()
os.environ['REQUESTS_CA_BUNDLE'] = temp_cert.name
import jinja2
import jinja2.ext
'''
replace_and_write('main.py', 'test.py', 'from xes.exe import *', '', beforeCode)


import subprocess, os
from xes.tool import xopen 
user_lib_path = os.path.expanduser(r"~\学而思直播\code\site-packages")
pyinstaller_path = os.path.join(user_lib_path,"bin","pyinstaller.exe" )

pgzero_data_path = os.path.join(user_lib_path,"pgzero","data")

spec2 = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['test.py'],
    pathex=['you_project_path/'],
    binaries=[],
    datas=[('pgzero_data_path', '/pgzero/data'),tpl_dirs],
    hiddenimports=['lxml'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='test',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

'''
path = xopen()
path = path.replace('\\','/')
# print(path)
path = path[:-1]


import os

def list_subdirectories(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

dirs = list_subdirectories(path)
# print(dirs)

dirs_str = ''
for d in dirs:
    
    dirs_str = dirs_str + "('you_project_path/"+d+"', '" +d+ "'),"


# def list_files_with_suffixes(suffixes):
#     files = []
#     for file in os.listdir('.'):
#         if file.endswith(tuple(suffixes)) == False:
#             files.append(file)
#     return files

# suffixes = ['.spec', '.py']
# files = list_files_with_suffixes(suffixes)
# for file in files:
#     print(file)
#     dirs_str = dirs_str + "('"+file+"', '.'),"


spec2 = spec2.replace('tpl_dirs', dirs_str)

spec2 = spec2.replace('you_project_path', path)

pgzero_data_path = pgzero_data_path.replace('\\','/')

spec2 = spec2.replace('pgzero_data_path', pgzero_data_path)

with open("test.spec","w",encoding="utf8") as f:
    f.write(spec2)
    f.close()
    
main_py_name = "test.spec"
args = [pyinstaller_path] + [main_py_name]
os.system(" ".join(args))

xopen()

print("打包完成")
exit(0) 


