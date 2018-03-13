from .models import MailScannerConfiguration, SpamAssassinConfiguration

class BaseFileParser:
    def parse(self, filepath):
        pass
    def save(self, key, value, filepath):
        qs = MailScannerConfiguration.objects.filter(key=key)
        if qs.exists():
            entity = qs.first()
            entity.value = value
            entity.save()
        else:
            MailScannerConfiguration.objects.create(key=key, value=value, filepath=filepath)

class DefaultsFileParse(BaseFileParser):
    def parse(self, filepath):
        file = open(filepath, 'r')
        for l in file.readlines():
            if not l or (l.startswith('#') or l.startswith('include ')):
                continue
            key, value = l.split('=')
            self.save(key, value, filepath)
        file.close()
            
class MailscannerConfFileParser(BaseFileParser):
    def parse(self, filepath):
        file = open(filepath, 'r')
        for l in file.readlines():
            if not l or (l.startswith('#') or l.startswith('include ')):
                continue
            print('CURRENT STRING: ' + l)
            key, value = l.split(' = ')
            self.save(key, value, filepath)
        file.close()

class SpamassassinConfFileParser(BaseFileParser):
    def parse(self, filepath):
        file = open(filepath, 'r')
        for l in file.readlines():
            if not l or (l.startswith('#') or l.startswith('include ')):
                continue
            key, value = l.split('\t')
            self.save(key, value, filepath)
        file.close()
    def save(self, key, value1, value2, filepath):
        qs = SpamAssassinConfiguration.objects.filter(key=key)
        if qs.exists():
            entity = qs.first()
            entity.rule = value1
            entity.value = value2
            entity.save()
        else:
            SpamAssassinConfiguration.objects.create(key=key, rule=value1, value=value2, filepath=filepath)