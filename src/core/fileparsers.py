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
            if l[0] == '#':
                continue
            key, value = l.split('=')
            self.save(key, value, filepath)
        file.close()
            
class MailScannerConfFileParser(BaseFileParser):
    def parse(self, filepath):
        file = open(filepath, 'r')
        for l in file.readlines():
            if l[0] == '#':
                continue
            key, value = l.split(' = ')
            self.save(key, value, filepath)
        file.close()

class SpamassassinConfFileParser(BaseFileParser):
    def parse(self, filepath):
        file = open(filepath, 'r')
        for l in file.readlines():
            if l[0] == '#':
                continue
            key, value = l.split('\t')
            self.save(key, value, filepath)
        file.close()
    def save(key, value1, value2, filepath):
        qs = SpamAssassinConfiguration.objects.filter(key=key)
            if qs.exists():
                entity = qs.first()
                entity.value = value
                entity.save()
            else:
                SpamAssassinConfiguration.objects.create(key=key, value=value, filepath=filepath)