import errno
import os
import shutil
import stat
import sys
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)


def handleRemoveReadonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
        func(path)
    else:
        raise


def rm_mk_dir(directory, *args):
    if os.path.exists(directory):
        shutil.rmtree(directory, ignore_errors=False,
                      onerror=handleRemoveReadonly)
    if not os.path.exists(directory):
        os.mkdir(directory)
    for arg in args:
        if os.path.exists(arg):
            shutil.rmtree(arg, ignore_errors=False,
                          onerror=handleRemoveReadonly)
        if not os.path.exists(arg):
            os.mkdir(arg)


def rm_file(file, *args):
    if os.path.exists(file):
        os.remove(file)
    for arg in args:
        if os.path.exists(arg):
            os.remove(arg)

def rm_dir(directory, *args):
    if os.path.exists(directory):
        shutil.rmtree(directory, ignore_errors=False,
                      onerror=handleRemoveReadonly)
    for arg in args:
        if os.path.exists(arg):
            shutil.rmtree(arg, ignore_errors=False,
                          onerror=handleRemoveReadonly)

def copy_dir(source, destination):
    shutil.copytree(source, destination)
