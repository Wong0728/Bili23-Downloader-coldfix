# -*- coding: utf-8 -*-
import shutil
import os

# 清理构建目录
shutil.rmtree('build', ignore_errors=True)
shutil.rmtree('dist', ignore_errors=True)

# 删除 spec 文件
for f in os.listdir('.'):
    if f.endswith('.spec'):
        try:
            os.remove(f)
        except:
            pass

print('清理完成')
