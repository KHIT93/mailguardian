import os, time
from pathlib import Path
from pyotp import TOTP as BaseTOTP

class MailGuardianConfiguration:
    _configuration = {}

    def __init__(self, data, *args, **kwargs):
        if self._configuration == {}:
            self._configuration = self.dot(data)

    def accessible(self,key):
        if self.exists(key) and (self._configuration[key] and not self._configuration[key] == ''):
             return True
        else:
            return False
    
    def dot(self, data, prepend = ''):
        results = {}
        for key,value in data.items():
            if isinstance(value, dict):
                results.update(self.dot(value,prepend+key+'.'))
            else:
                results[prepend+key] = value
        return results

    def exists(self, key):
        if key in self._configuration:
            return True
        else:
            return False

    def get(self, key, default):
        if self.accessible(key):
            return self._configuration[key]
        else:
            return default

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

class TOTP(BaseTOTP):
    def timecode(self, for_time):
        if for_time.tzinfo:
            i = calendar.timegm(for_time.utctimetuple())
        else:
            i = time.mktime(for_time.timetuple())
        return int(i / self.interval)