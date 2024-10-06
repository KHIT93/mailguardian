import collections
import re
from typing import Any
import markupsafe
import logging
from lxml import etree, html
from lxml.html import clean, defs

# We want to avoid having LXML at some point. So we declare them here based on the following source code
# https://lxml.de/api/lxml.html.defs-pysrc.html
html_tags: frozenset[str] = frozenset([
    'html', 'head', 'body', 'frameset', # top_level_tags
    'base', 'isindex', 'link', 'meta', 'script', 'style', 'title', # head_tags
    'address', 'blockquote', 'center', 'del', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'ins', 'isindex', 'noscript', 'p', 'pre', # general_block_tags
    'dir', 'dl', 'dt', 'dd', 'li', 'menu', 'ol', 'ul', # list_tags
    'table', 'caption', 'colgroup', 'col', 'thead', 'tfoot', 'tbody', 'tr', 'td', 'th', # table_tags
    'form', 'button', 'fieldset', 'legend', 'input', 'label', 'select', 'optgroup', 'option', 'textarea', # form_tags
    'a', 'applet', 'basefont', 'bdo', 'br', 'embed', 'font', 'iframe', 'img', 'map', 'area', 'object', 'param', 'q', 'script', 'span', 'sub', 'sup', # special_inline_tags
    'abbr', 'acronym', 'cite', 'code', 'del', 'dfn', 'em', 'ins', 'kbd', 'samp', 'strong', 'var', # phrase_tags
    'b', 'big', 'i', 's', 'small', 'strike', 'tt', 'u', # font_style_tags
    'blink', 'marquee' # nonstandard_tags
    'article', 'aside', 'audio', 'canvas', 'command', 'datalist', 'details', 'embed', 'figcaption', 'figure', 'footer', 'header', 'hgroup', 'keygen', 'mark', 'math', 'meter', 'nav', 'output', 'progress', 'rp', 'rt', 'ruby', 'section', 'source', 'summary', 'svg', 'time', 'track', 'video', 'wbr' # html5_tags
])

safe_attrs: frozenset[str] = frozenset([
    'abbr', 'accept', 'accept-charset', 'accesskey', 'action', 'align', 
    'alt', 'axis', 'border', 'cellpadding', 'cellspacing', 'char', 'charoff', 
    'charset', 'checked', 'cite', 'class', 'clear', 'cols', 'colspan', 
    'color', 'compact', 'coords', 'datetime', 'dir', 'disabled', 'enctype', 
    'for', 'frame', 'headers', 'height', 'href', 'hreflang', 'hspace', 'id', 
    'ismap', 'label', 'lang', 'longdesc', 'maxlength', 'media', 'method', 
    'multiple', 'name', 'nohref', 'noshade', 'nowrap', 'prompt', 'readonly', 
    'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope', 'selected', 'shape', 
    'size', 'span', 'src', 'start', 'summary', 'tabindex', 'target', 'title', 
    'type', 'usemap', 'valign', 'value', 'vspace', 'width',
    'style',
    'data-o-mail-quote', 'data-o-mail-quote-node',  # quote detection
    'data-oe-model', 'data-oe-id', 'data-oe-field', 'data-oe-type', 'data-oe-expression', 'data-oe-translation-source-sha', 'data-oe-nodeid',
    'data-last-history-steps', 'data-oe-protected', 'data-embedded', 'data-embedded-editable', 'data-embedded-props',
    'data-oe-transient-content', 'data-behavior-props', 'data-prop-name',  # legacy editor
    'data-publish', 'data-id', 'data-res_id', 'data-interval', 'data-member_id', 'data-scroll-background-ratio', 'data-view-id',
    'data-class', 'data-mimetype', 'data-original-src', 'data-original-id', 'data-gl-filter', 'data-quality', 'data-resize-width',
    'data-shape', 'data-shape-colors', 'data-file-name', 'data-original-mimetype',
    'data-mimetype-before-conversion',
])

SANITIZE_TAGS: dict[str, Any] = {
    # allow new semantic HTML5 tags
    'allow_tags': html_tags | frozenset('article bdi section header footer hgroup nav aside figure main'.split()),
    'kill_tags': ['base', 'embed', 'frame', 'head', 'iframe', 'link', 'meta',
                  'noscript', 'object', 'script', 'style', 'title'],
    'remove_tags': ['html', 'body'],
}

class HtmlCleaner(clean.Cleaner):

    _style_re = re.compile(r'''([\w-]+)\s*:\s*((?:[^;"']|"[^";]*"|'[^';]*')+)''')

    _style_whitelist = [
        'font-size', 'font-family', 'font-weight', 'font-style', 'background-color', 'color', 'text-align',
        'line-height', 'letter-spacing', 'text-transform', 'text-decoration', 'text-decoration', 'opacity',
        'float', 'vertical-align', 'display',
        'padding', 'padding-top', 'padding-left', 'padding-bottom', 'padding-right',
        'margin', 'margin-top', 'margin-left', 'margin-bottom', 'margin-right',
        'white-space',
        # box model
        'border', 'border-color', 'border-radius', 'border-style', 'border-width', 'border-top', 'border-bottom',
        'height', 'width', 'max-width', 'min-width', 'min-height',
        # tables
        'border-collapse', 'border-spacing', 'caption-side', 'empty-cells', 'table-layout']

    _style_whitelist.extend(
        ['border-%s-%s' % (position, attribute)
            for position in ['top', 'bottom', 'left', 'right']
            for attribute in ('style', 'color', 'width', 'left-radius', 'right-radius')]
    )

    strip_classes = False
    sanitize_style = False

    def __call__(self, doc):
        super(HtmlCleaner, self).__call__(doc)

        # if we keep attributes but still remove classes
        if not getattr(self, 'safe_attrs_only', False) and self.strip_classes:
            for el in doc.iter(tag=etree.Element):
                self.strip_class(el)

        # if we keep style attribute, sanitize them
        if not self.style and self.sanitize_style:
            for el in doc.iter(tag=etree.Element):
                self.parse_style(el)

    def strip_class(self, el):
        if el.attrib.get('class'):
            del el.attrib['class']

    def parse_style(self, el):
        attributes = el.attrib
        styling = attributes.get('style')
        if styling:
            valid_styles = collections.OrderedDict()
            styles = self._style_re.findall(styling)
            for style in styles:
                if style[0].lower() in self._style_whitelist:
                    valid_styles[style[0].lower()] = style[1]
            if valid_styles:
                el.attrib['style'] = '; '.join('%s:%s' % (key, val) for (key, val) in valid_styles.items())
            else:
                del el.attrib['style']

def tag_quote(el):
    def _create_new_node(tag, text, tail=None, attrs=None):
        new_node = etree.Element(tag)
        new_node.text = text
        new_node.tail = tail
        if attrs:
            for key, val in attrs.items():
                new_node.set(key, val)
        return new_node

    def _tag_matching_regex_in_text(regex, node, tag='span', attrs=None):
        text = node.text or ''
        if not re.search(regex, text):
            return

        child_node = None
        idx, node_idx = 0, 0
        for item in re.finditer(regex, text):
            new_node = _create_new_node(tag, text[item.start():item.end()], None, attrs)
            if child_node is None:
                node.text = text[idx:item.start()]
                new_node.tail = text[item.end():]
                node.insert(node_idx, new_node)
            else:
                child_node.tail = text[idx:item.start()]
                new_node.tail = text[item.end():]
                node.insert(node_idx, new_node)
            child_node = new_node
            idx = item.end()
            node_idx = node_idx + 1

    el_class = el.get('class', '') or ''
    el_id = el.get('id', '') or ''

    # gmail or yahoo // # outlook, html // # msoffice
    if 'gmail_extra' in el_class or \
            'divRplyFwdMsg' in el_id or \
            ('SkyDrivePlaceholder' in el_class or 'SkyDrivePlaceholder' in el_class):
        el.set('data-o-mail-quote', '1')
        if el.getparent() is not None:
            el.getparent().set('data-o-mail-quote-container', '1')

    if (el.tag == 'hr' and ('stopSpelling' in el_class or 'stopSpelling' in el_id)) or \
       'yahoo_quoted' in el_class:
        # Quote all elements after this one
        el.set('data-o-mail-quote', '1')
        for sibling in el.itersiblings(preceding=False):
            sibling.set('data-o-mail-quote', '1')

    # html signature (-- <br />blah)
    signature_begin = re.compile(r"((?:(?:^|\n)[-]{2}[\s]?$))")
    if el.text and el.find('br') is not None and re.search(signature_begin, el.text):
        el.set('data-o-mail-quote', '1')
        if el.getparent() is not None:
            el.getparent().set('data-o-mail-quote-container', '1')

    # text-based quotes (>, >>) and signatures (-- Signature)
    text_complete_regex = re.compile(r"((?:\n[>]+[^\n\r]*)+|(?:(?:^|\n)[-]{2}[\s]?[\r\n]{1,2}[\s\S]+))")
    if not el.get('data-o-mail-quote'):
        _tag_matching_regex_in_text(text_complete_regex, el, 'span', {'data-o-mail-quote': '1'})

    if el.tag == 'blockquote':
        # remove single node
        el.set('data-o-mail-quote-node', '1')
        el.set('data-o-mail-quote', '1')
    if el.getparent() is not None and (el.getparent().get('data-o-mail-quote') or el.getparent().get('data-o-mail-quote-container')) and not el.getparent().get('data-o-mail-quote-node'):
        el.set('data-o-mail-quote', '1')

def html_normalize(src: str, filter_callback: callable = None) -> str:
    """ Normalize `src` for storage as an html field value.

    The string is parsed as an html tag soup, made valid, then decorated for
    "email quote" detection, and prepared for an optional filtering.
    The filtering step (e.g. sanitization) should be performed by the
    `filter_callback` function (to avoid multiple parsing operations, and
    normalize the result).

    :param src: the html string to normalize
    :param filter_callback: optional callable taking a single `etree._Element`
        document parameter, to be called during normalization in order to
        filter the output document
    """
    if not src:
        return src

    # html: remove encoding attribute inside tags
    src = re.sub(r'(<[^>]*\s)(encoding=(["\'][^"\']*?["\']|[^\s\n\r>]+)(\s[^>]*|/)?>)', "", src, re.IGNORECASE | re.DOTALL)

    src = src.replace('--!>', '-->')
    src = re.sub(r'(<!-->|<!--->)', '<!-- -->', src)
    # On the specific case of Outlook desktop it adds unnecessary '<o:.*></o:.*>' tags which are parsed
    # in '<p></p>' which may alter the appearance (eg. spacing) of the mail body
    src = re.sub(r'</?o:.*?>', '', src)

    try:
        doc = html.fromstring(src)
    except etree.ParserError as e:
        # HTML comment only string, whitespace only..
        if 'empty' in str(e):
            return ""
        raise

    # perform quote detection before cleaning and class removal
    if doc is not None:
        for el in doc.iter(tag=etree.Element):
            tag_quote(el)

    if filter_callback:
        doc = filter_callback(doc)

    src = html.tostring(doc, encoding='unicode')

    # this is ugly, but lxml/etree tostring want to put everything in a
    # 'div' that breaks the editor -> remove that
    if src.startswith('<div>') and src.endswith('</div>'):
        src = src[5:-6]

    # html considerations so real html content match database value
    src = src.replace(u'\xa0', u'&nbsp;')

    return src

def html_sanitize(src: str, silent: bool = True, sanitize_tags: bool = True, sanitize_attributes: bool = False, sanitize_style: bool = False, sanitize_form: bool = True, strip_style: bool = False, strip_classes: bool= False) -> markupsafe.Markup:
    if not src:
        return src

    logger = logging.getLogger(__name__ + '.html_sanitize')

    def sanitize_handler(doc):
        kwargs = {
            'page_structure': True,
            'style': strip_style,              # True = remove style tags/attrs
            'sanitize_style': sanitize_style,  # True = sanitize styling
            'forms': sanitize_form,            # True = remove form tags
            'remove_unknown_tags': False,
            'comments': False,
            'processing_instructions': False
        }
        if sanitize_tags:
            kwargs.update(SANITIZE_TAGS)

        if sanitize_attributes:  # We keep all attributes in order to keep "style"
            if strip_classes:
                current_safe_attrs = safe_attrs - frozenset(['class'])
            else:
                current_safe_attrs = safe_attrs
            kwargs.update({
                'safe_attrs_only': True,
                'safe_attrs': current_safe_attrs,
            })
        else:
            kwargs.update({
                'safe_attrs_only': False,  # keep oe-data attributes + style
                'strip_classes': strip_classes,  # remove classes, even when keeping other attributes
            })

        cleaner = HtmlCleaner(**kwargs)
        cleaner(doc)
        return doc

    try:
        sanitized = html_normalize(src, filter_callback=sanitize_handler)
    except etree.ParserError:
        if not silent:
            raise
        logger.warning(u'ParserError obtained when sanitizing %r', src, exc_info=True)
        sanitized = '<p>ParserError when sanitizing</p>'
    except Exception:
        if not silent:
            raise
        logger.warning(u'unknown error obtained when sanitizing %r', src, exc_info=True)
        sanitized = '<p>Unknown error when sanitizing</p>'

    return markupsafe.Markup(sanitized)