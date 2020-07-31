import cryptography.fernet
from distutils.version import StrictVersion

class Upgrader(object):
    config = []
    app_dir = ''
    src_dir = ''
    version = '1.0.0'
    applied_version = '1.0.0'
    legacy = False
    def __init__(self, config, app_dir='/home/mailguardian/mailguardian', src_dir='/home/mailguardian/mailguardian/src', version='1.0.0'):
        super().__init__()
        self.config = config
        self.app_dir = app_dir
        self.src_dir = src_dir
        self.version = version

    def upgrade(self):
        raise NotImplementedError('The Upgrader.upgrade method has not been implemented on this implementation of the class')

    def applicable(self):
        return StrictVersion(self.version) < StrictVersion(self.applied_version)

def _generate_encryption_key():
    key = cryptography.fernet.Fernet.generate_key()
    return key.decode()