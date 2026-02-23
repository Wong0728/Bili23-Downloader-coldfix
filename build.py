# -*- coding: utf-8 -*-
"""
Bili23 Downloader 打包脚本
使用 PyInstaller + UPX 压缩
"""

import os
import sys
import shutil
import subprocess

def clean_build():
    """清理之前的构建文件"""
    dirs_to_remove = ['build', 'dist']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"正在删除 {dir_name} 目录...")
            shutil.rmtree(dir_name)
    
    # 删除旧的spec文件
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            print(f"正在删除 {file}...")
            os.remove(file)

def get_upx_path():
    """获取UPX路径"""
    upx_path = os.path.join(os.path.dirname(__file__), 'upx.exe')
    if os.path.exists(upx_path):
        return os.path.dirname(upx_path)
    return None

def build():
    """执行打包"""
    print("=" * 60)
    print("Bili23 Downloader 打包工具")
    print("=" * 60)
    
    # 清理旧文件
    clean_build()
    
    # 获取UPX路径
    upx_dir = get_upx_path()
    if upx_dir:
        print(f"UPX 路径: {upx_dir}")
        os.environ['PATH'] = upx_dir + os.pathsep + os.environ.get('PATH', '')
    else:
        print("警告: 未找到 UPX，将不进行压缩")
    
    # PyInstaller 参数
    cmd = [
        'pyinstaller',
        '--name=Bili23',
        '--windowed',
        # '--onefile',  # 多文件模式，避免单文件打包问题
        '--icon=icon.ico',
        '--clean',
        '--noconfirm',
        '--workpath', os.path.join(os.path.dirname(__file__), 'build'),
        '--specpath', os.path.dirname(__file__),
    ]
    
    # 添加UPX参数
    if upx_dir:
        cmd.extend(['--upx-dir', upx_dir])
        # 排除某些在使用UPX压缩后可能出现问题的模块
        upx_excludes = ['cryptodome', 'Crypto', 'PIL']
        for item in upx_excludes:
            cmd.extend(['--upx-exclude', item])
    
    # 添加数据文件（非可执行文件）
    data_files = [
        ('src/Locale', 'Locale'),
        ('src/static', 'static'),
    ]
    
    for src, dst in data_files:
        if os.path.exists(src):
            src_normalized = os.path.normpath(src)
            cmd.extend(['--add-data', f'{src_normalized}{os.pathsep}{dst}'])
    
    # 添加二进制文件（可执行文件）
    binaries = [
        ('ffmpeg.exe', '.'),
        ('aria2c.exe', '.'),
    ]
    
    for src, dst in binaries:
        if os.path.exists(src):
            src_normalized = os.path.normpath(src)
            cmd.extend(['--add-binary', f'{src_normalized}{os.pathsep}{dst}'])
    
    # 隐藏导入模块
    hidden_imports = [
        'wx',
        'wx.svg',
        'requests',
        'requests.packages',
        'requests.packages.urllib3',
        'requests.packages.urllib3.exceptions',
        'qrcode',
        'qrcode.image.pil',
        'vlc',
        'google.protobuf',
        'google.protobuf.internal.builder',
        'google.protobuf.json_format',
        'google.protobuf.descriptor',
        'google.protobuf.descriptor_pool',
        'google.protobuf.runtime_version',
        'google.protobuf.symbol_database',
        'google.protobuf.internal',
        'websockets',
        'Cryptodome',
        'Cryptodome.Cipher',
        'Cryptodome.Util.Padding',
        'Cryptodome.PublicKey.RSA',
        'Cryptodome.Cipher.PKCS1_OAEP',
        'Crypto',
        'Crypto.Hash',
        'Crypto.Hash.SHA256',
        'Crypto.PublicKey',
        'Crypto.PublicKey.RSA',
        'Crypto.Cipher',
        'Crypto.Cipher.PKCS1_OAEP',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'base64',
        'json',
        're',
        'os',
        'sys',
        'time',
        'threading',
        'subprocess',
        'configparser',
        'gettext',
        'locale',
        'platform',
        'ctypes',
        'io',
        'enum',
        'dataclasses',
        'typing',
        'pathlib',
        'hashlib',
        'random',
        'string',
        'urllib',
        'urllib.parse',
        'urllib.request',
        'urllib.error',
        'urllib.response',
        'xml',
        'xml.etree',
        'xml.etree.ElementTree',
        'html',
        'html.parser',
        'copy',
        'math',
        'datetime',
        # email 相关模块 - urllib3 依赖
        'email',
        'email.mime',
        'email.mime.text',
        'email.mime.multipart',
        'email.mime.base',
        'email.mime.nonmultipart',
        'email.mime.message',
        'email.header',
        'email.utils',
        'email.parser',
        'email.generator',
        'email.encoders',
        'email.charset',
        'email.errors',
        'email.feedparser',
        'email.message',
        'email.iterators',
        'email.base64mime',
        'email.quoprimime',
        # http 相关模块
        'http',
        'http.client',
        'http.cookiejar',
        'http.cookies',
        # ssl 相关模块
        'ssl',
        'certifi',
        'idna',
        'idna.core',
        'idna.idnadata',
        'idna.intranges',
        'charset_normalizer',
        'charset_normalizer.md',
        # 其他可能被依赖的模块
        'queue',
        'socket',
        'selectors',
        'weakref',
        'traceback',
        'linecache',
        'warnings',
        'contextlib',
        'functools',
        'collections',
        'collections.abc',
        'importlib',
        'importlib.machinery',
        'importlib.util',
        'inspect',
        'textwrap',
        'numbers',
        'decimal',
        'fractions',
        'uuid',
        'bisect',
        'heapq',
        'keyword',
        'token',
        'tokenize',
        'codecs',
        'encodings',
        'encodings.utf_8',
        'encodings.latin_1',
        'encodings.ascii',
        'encodings.idna',
        'encodings.raw_unicode_escape',
        'encodings.unicode_escape',
        'encodings.utf_16',
        'encodings.utf_16_be',
        'encodings.utf_16_le',
        'encodings.utf_32',
        'encodings.utf_32_be',
        'encodings.utf_32_le',
        'encodings.mbcs',
        'encodings.cp437',
        'encodings.cp850',
        'encodings.cp1252',
        'fnmatch',
        'glob',
        'shutil',
        'tempfile',
        'zipfile',
        'tarfile',
        'gzip',
        'bz2',
        'lzma',
        'struct',
        'binascii',
        'base64',
        'mimetypes',
        'netrc',
        'nturl2path',
    ]
    
    for imp in hidden_imports:
        cmd.extend(['--hidden-import', imp])
    
    # 排除不必要的模块以减小体积
    # 注意：不要排除 Python 标准库中被 requests/urllib3 依赖的模块
    excludes = [
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'sklearn',
        'tensorflow',
        'torch',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'tkinter',
        'unittest',
        'pydoc',
        # 'email',  # 不能排除，urllib3 依赖此模块
        'http.server',
        'xmlrpc',
        'multiprocessing',
        # 'concurrent.futures',  # 不能排除，代码中使用了 ThreadPoolExecutor
        'setuptools',
        'pkg_resources',
        'pip',
        'wheel',
        'Cython',
        'jedi',
        'parso',
        'IPython',
        'jupyter',
        'notebook',
        'sphinx',
        'pytest',
        'mypy',
        'pylint',
        'black',
        'isort',
        'flake8',
        'mccabe',
        'pycodestyle',
        'pyflakes',
        'coverage',
        'tox',
        'nose',
        'mock',
        'docutils',
        'alabaster',
        'imagesize',
        'snowballstemmer',
        'babel',
        'MarkupSafe',
        'Jinja2',
        'PIL._tkinter_finder',
    ]
    
    for exc in excludes:
        cmd.extend(['--exclude-module', exc])
    
    # 收集所有子模块（确保第三方库完整打包）
    collect_all = [
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'PIL',
        'qrcode',
        'Cryptodome',
        'Crypto',
        'google.protobuf',
    ]
    
    for pkg in collect_all:
        cmd.extend(['--collect-all', pkg])
    
    # 收集二进制文件
    collect_binaries = [
        'Cryptodome',
    ]
    
    for pkg in collect_binaries:
        cmd.extend(['--collect-binaries', pkg])
    
    # 主程序入口
    cmd.append('src/main.py')
    
    print("\n执行命令:")
    print(' '.join(cmd))
    print()
    
    # 执行打包
    try:
        result = subprocess.run(cmd, shell=False, check=True, capture_output=True, text=True)
        print("\n打包成功！")
        return True
    except subprocess.CalledProcessError as e:
        print("\n打包失败！")
        print(f"错误码: {e.returncode}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False

def copy_additional_files():
    """复制额外文件到输出目录"""
    dist_dir = 'dist'
    if not os.path.exists(dist_dir):
        return
    
    print("\n复制额外文件...")
    
    # 创建必要的目录
    dirs_to_create = [
        os.path.join(dist_dir, 'data'),
    ]
    
    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)
    
    print("完成！")

if __name__ == '__main__':
    if build():
        copy_additional_files()
        print("\n" + "=" * 60)
        print("打包完成！输出目录: dist/Bili23/")
        print("可执行文件: dist/Bili23/Bili23.exe")
        print("=" * 60)
    else:
        sys.exit(1)
