from .models import MailScannerConfiguration, SpamAssassinConfiguration
from django.conf import settings

class BaseFileParser:
    __seperator = ' = '
    __commentchar = '#'
    def parse(self, filepath):
        file = open(settings.MAILSCANNER_CONFIG_DIR + '/' + filepath, 'r')
        for l in file.readlines():
            if not l.rstrip() or (l.startswith(self.__commentchar) or l.startswith('include ')):
                continue
            l = l.replace('\n', '')
            data = l.split(self.__seperator)
            self.save(data, filepath)
        file.close()
    def save(self, data, filepath):
        qs = MailScannerConfiguration.objects.filter(key=data[0]).filter(filepath=filepath)
        if qs.exists():
            entity = qs.first()
            entity.value = data[1]
            entity.save()
        else:
            MailScannerConfiguration.objects.create(key=data[0], value=data[1], filepath=filepath)

class DefaultsFileParse(BaseFileParser):
    __seperator = '='
    # def parse(self, filepath):
    #     file = open(filepath, 'r')
    #     for l in file.readlines():
    #         if not l.rstrip() or (l.startswith('#') or l.startswith('include ')):
    #             continue
    #         print('CURRENT STRING: "' + l + '"')
    #         l = l.replace('\n', '')
    #         key, value = l.split('=')
    #         self.save(key, value, filepath)
    #     file.close()
            
class MailscannerConfFileParser(BaseFileParser):
    pass
    # def parse(self, filepath):
    #     file = open(filepath, 'r')
    #     for l in file.readlines():
    #         if not l.rstrip() or (l.startswith('#') or l.startswith('include ')):
    #             continue
    #         print('CURRENT STRING: "' + l + '"')
    #         l = l.replace('\n', '')
    #         key, value = l.split(' = ')
    #         self.save(key, value, filepath)
    #     file.close()

# class SpamassassinConfFileParser(BaseFileParser):
#     def parse(self, filepath):
#         file = open(filepath, 'r')
#         for l in file.readlines():
#             if not l.rstrip() or (l.startswith('#') or l.startswith('include ')):
#                 continue
#             print('CURRENT STRING: "' + l + '"')
#             key = None
#             value1 = ""
#             value2 = ""
#             key, value1, value2 = l.split(' ')
#             self.save(key, value1, value2, filepath)
#         file.close()
#     def save(self, key, value1, value2, filepath):
#         qs = SpamAssassinConfiguration.objects.filter(key=key)
#         if qs.exists():
#             entity = qs.first()
#             entity.rule = value1
#             entity.value = value2
#             entity.save()
#         else:
#             SpamAssassinConfiguration.objects.create(key=key, rule=value1, value=value2, filepath=filepath)