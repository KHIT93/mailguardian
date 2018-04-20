import os

class MailWareConfiguration:
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
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None