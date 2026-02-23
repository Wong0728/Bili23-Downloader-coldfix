# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_dynamic_libs
from PyInstaller.utils.hooks import collect_all

datas = [('src\\Locale', 'Locale'), ('src\\static', 'static')]
binaries = [('ffmpeg.exe', '.'), ('aria2c.exe', '.')]
hiddenimports = ['wx', 'wx.svg', 'requests', 'requests.packages', 'requests.packages.urllib3', 'requests.packages.urllib3.exceptions', 'qrcode', 'qrcode.image.pil', 'vlc', 'google.protobuf', 'google.protobuf.internal.builder', 'google.protobuf.json_format', 'google.protobuf.descriptor', 'google.protobuf.descriptor_pool', 'google.protobuf.runtime_version', 'google.protobuf.symbol_database', 'google.protobuf.internal', 'websockets', 'Cryptodome', 'Cryptodome.Cipher', 'Cryptodome.Util.Padding', 'Cryptodome.PublicKey.RSA', 'Cryptodome.Cipher.PKCS1_OAEP', 'Crypto', 'Crypto.Hash', 'Crypto.Hash.SHA256', 'Crypto.PublicKey', 'Crypto.PublicKey.RSA', 'Crypto.Cipher', 'Crypto.Cipher.PKCS1_OAEP', 'PIL', 'PIL.Image', 'PIL.ImageDraw', 'PIL.ImageFont', 'base64', 'json', 're', 'os', 'sys', 'time', 'threading', 'subprocess', 'configparser', 'gettext', 'locale', 'platform', 'ctypes', 'io', 'enum', 'dataclasses', 'typing', 'pathlib', 'hashlib', 'random', 'string', 'urllib', 'urllib.parse', 'urllib.request', 'urllib.error', 'urllib.response', 'xml', 'xml.etree', 'xml.etree.ElementTree', 'html', 'html.parser', 'copy', 'math', 'datetime', 'email', 'email.mime', 'email.mime.text', 'email.mime.multipart', 'email.mime.base', 'email.mime.nonmultipart', 'email.mime.message', 'email.header', 'email.utils', 'email.parser', 'email.generator', 'email.encoders', 'email.charset', 'email.errors', 'email.feedparser', 'email.message', 'email.iterators', 'email.base64mime', 'email.quoprimime', 'http', 'http.client', 'http.cookiejar', 'http.cookies', 'ssl', 'certifi', 'idna', 'idna.core', 'idna.idnadata', 'idna.intranges', 'charset_normalizer', 'charset_normalizer.md', 'queue', 'socket', 'selectors', 'weakref', 'traceback', 'linecache', 'warnings', 'contextlib', 'functools', 'collections', 'collections.abc', 'importlib', 'importlib.machinery', 'importlib.util', 'inspect', 'textwrap', 'numbers', 'decimal', 'fractions', 'uuid', 'bisect', 'heapq', 'keyword', 'token', 'tokenize', 'codecs', 'encodings', 'encodings.utf_8', 'encodings.latin_1', 'encodings.ascii', 'encodings.idna', 'encodings.raw_unicode_escape', 'encodings.unicode_escape', 'encodings.utf_16', 'encodings.utf_16_be', 'encodings.utf_16_le', 'encodings.utf_32', 'encodings.utf_32_be', 'encodings.utf_32_le', 'encodings.mbcs', 'encodings.cp437', 'encodings.cp850', 'encodings.cp1252', 'fnmatch', 'glob', 'shutil', 'tempfile', 'zipfile', 'tarfile', 'gzip', 'bz2', 'lzma', 'struct', 'binascii', 'base64', 'mimetypes', 'netrc', 'nturl2path']
binaries += collect_dynamic_libs('Cryptodome')
tmp_ret = collect_all('requests')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('urllib3')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('certifi')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('charset_normalizer')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('idna')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PIL')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('qrcode')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('Cryptodome')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('Crypto')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('google.protobuf')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'scipy', 'sklearn', 'tensorflow', 'torch', 'PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'tkinter', 'unittest', 'pydoc', 'http.server', 'xmlrpc', 'multiprocessing', 'setuptools', 'pkg_resources', 'pip', 'wheel', 'Cython', 'jedi', 'parso', 'IPython', 'jupyter', 'notebook', 'sphinx', 'pytest', 'mypy', 'pylint', 'black', 'isort', 'flake8', 'mccabe', 'pycodestyle', 'pyflakes', 'coverage', 'tox', 'nose', 'mock', 'docutils', 'alabaster', 'imagesize', 'snowballstemmer', 'babel', 'MarkupSafe', 'Jinja2', 'PIL._tkinter_finder'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Bili23',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=['cryptodome', 'Crypto', 'PIL'],
    name='Bili23',
)
