import os
from pathlib import Path

def which(program):
    def is_exe(fpath):
        return Path(fpath).is_file() and os.access(fpath, os.X_OK)
    fpath = Path(program)
    if fpath.is_absolute():
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = Path(path, program)
            if is_exe(exe_file):
                return str(exe_file)
    return None