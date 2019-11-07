from django import template
from django.templatetags.static import static
from django.conf import settings
import os, json

register = template.Library()

@register.simple_tag
def mix(asset):
    base_assets_dir = '/assets/dist/'
    mix_manifest = dict()
    if os.path.exists(os.path.join(os.path.dirname(settings.BASE_DIR), 'mix-manifest.json')):
        with open(os.path.join(os.path.dirname(settings.BASE_DIR), 'mix-manifest.json'), 'r') as f:
            mix_manifest = json.load(f)
        cache_hash = mix_manifest[base_assets_dir + asset].replace(base_assets_dir + asset, "")
        return static(asset) + cache_hash
    return static(asset)