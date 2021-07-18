from pathlib import Path
import re
import json
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.templatetags.static import static

register = template.Library()

DEV_SERVER_ROOT = 'http://localhost:3000'

is_absolute_url = lambda url: re.match("^https?://", url)

def vite_manifest(entries_name):
    app_name = 'frontend',
    manifest_filepath = Path(settings.ASSETS_DIR, 'manifest.json')

    if settings.DEBUG:
        scripts = [
            "{root}/@vite/client".format(root=DEV_SERVER_ROOT)
        ]

        for name in entries_name:
            scripts.append("{root}/{name}".format(root=DEV_SERVER_ROOT, name=name))

        styles = []
        return scripts, styles
    else:
        with open(manifest_filepath, 'r') as fp:
            manifest = json.load(fp)
        _processed = set()

        def _process_entries(names):
            scripts = []
            styles = []
            for name in names:
                if name in _processed:
                    continue
                chunk = manifest[name]
                import_scripts, import_styles = _process_entries(chunk.get('imports', []))
                scripts += import_scripts
                styles += import_styles
                scripts += [chunk['file']]
                styles += [css for css in chunk.get('css', [])]

                _processed.add(name)
            
            return scripts, styles
        return _process_entries(entries_name)

@register.simple_tag
def vite(asset):
    manifest = vite_manifest([asset])
    return "{root}/{name}".format(root=DEV_SERVER_ROOT, name=asset) if settings.DEBUG else asset
