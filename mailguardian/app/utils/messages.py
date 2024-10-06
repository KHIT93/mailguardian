import email
import email.message
import email.policy
from email import message_from_string, message_from_file
from email.message import EmailMessage
import logging
import markupsafe
from pathlib import Path
import re
from mailguardian.app.schemas.message import MessageDetail
from mailguardian.app.utils.sanitize import html_sanitize
_logger = logging.getLogger(__name__)

def html_keep_url(text: str) -> str:
    """ Transform the url into clickable link with <a/> tag """
    idx = 0
    final = ''
    link_tags = re.compile(r"""(?<!["'])((ftp|http|https):\/\/(\w+:{0,1}\w*@)?([^\s<"']+)(:[0-9]+)?(\/|\/([^\s<"']))?)(?![^\s<"']*["']|[^\s<"']*</a>)""")
    for item in re.finditer(link_tags, text):
        final += text[idx:item.start()]
        final += '<a href="%s" target="_blank" rel="noreferrer noopener">%s</a>' % (item.group(0), item.group(0))
        idx = item.end()
    final += text[idx:]
    return final

def plaintext2html(text: str, container_tag: str = None) -> markupsafe.Markup:
    r"""Convert plaintext into html. Content of the text is escaped to manage
    html entities, using :func:`~odoo.tools.misc.html_escape`.

    - all ``\n``, ``\r`` are replaced by ``<br/>``
    - enclose content into ``<p>``
    - convert url into clickable link
    - 2 or more consecutive ``<br/>`` are considered as paragraph breaks

    :param str text: plaintext to convert
    :param str container_tag: container of the html; by default the content is
        embedded into a ``<div>``
    :rtype: markupsafe.Markup
    """
    assert isinstance(text, str)
    text = markupsafe.escape(text)

    # 1. replace \n and \r
    text = re.sub(r'(\r\n|\r|\n)', '<br/>', text)

    # 2. clickable links
    text = html_keep_url(text)

    # 3-4: form paragraphs
    idx = 0
    final = '<p>'
    br_tags = re.compile(r'(([<]\s*[bB][rR]\s*/?[>]\s*){2,})')
    for item in re.finditer(br_tags, text):
        final += text[idx:item.start()] + '</p><p>'
        idx = item.end()
    final += text[idx:] + '</p>'

    # 5. container
    if container_tag: # FIXME: validate that container_tag is just a simple tag?
        final = '<%s>%s</%s>' % (container_tag, final, container_tag)
    return markupsafe.Markup(final)

def append_content_to_html(html: str, content: str, plaintext: bool = True, preserve: bool = False, container_tag: str = None) -> markupsafe.Markup:
    """ Append extra content at the end of an HTML snippet, trying
        to locate the end of the HTML document (</body>, </html>, or
        EOF), and converting the provided content in html unless ``plaintext``
        is ``False``.

        Content conversion can be done in two ways:

        - wrapping it into a pre (``preserve=True``)
        - use plaintext2html (``preserve=False``, using ``container_tag`` to
          wrap the whole content)

        A side-effect of this method is to coerce all HTML tags to
        lowercase in ``html``, and strip enclosing <html> or <body> tags in
        content if ``plaintext`` is False.

        :param str html: html tagsoup (doesn't have to be XHTML)
        :param str content: extra content to append
        :param bool plaintext: whether content is plaintext and should
            be wrapped in a <pre/> tag.
        :param bool preserve: if content is plaintext, wrap it into a <pre>
            instead of converting it into html
        :param str container_tag: tag to wrap the content into, defaults to `div`.
        :rtype: markupsafe.Markup
    """
    if plaintext and preserve:
        content = '\n<pre>%s</pre>\n' % markupsafe.escape(content)
    elif plaintext:
        content = '\n%s\n' % plaintext2html(content, container_tag)
    else:
        content = re.sub(r'(?i)(</?(?:html|body|head|!\s*DOCTYPE)[^>]*>)', '', content)
        content = '\n%s\n' % content
    # Force all tags to lowercase
    html = re.sub(r'(</?)(\w+)([ >])',
        lambda m: '%s%s%s' % (m[1], m[2].lower(), m[3]), html)
    insert_location = html.find('</body>')
    if insert_location == -1:
        insert_location = html.find('</html>')
    if insert_location == -1:
        return markupsafe.Markup('%s%s' % (html, content))
    return markupsafe.Markup('%s%s%s' % (html[:insert_location], content, html[insert_location:]))

def get_neutralized_message(message: Path) -> MessageDetail:
    body: str = ''
    attachments: list[str] = []
    with message.open('rb') as msg:
        email_message: email.message.EmailMessage = email.message_from_file(fp=msg, policy=email.policy.SMTP)
        

        if email_message.get_content_maintype() == 'text':
            body = email_message.get_content()
            if email_message.get_content_type() == 'text/plain':
                body = append_content_to_html('', body, preserve=True)
            elif email_message.get_content_type() == 'text/html':
                body = html_sanitize(body, sanitize_tags=False, strip_classes=True)
        else:
            alternative: bool = False
            mixed: bool = False
            html: bool = False

            for part in email_message.walk():
                if part.get_content_type() == 'binary/octet-stream':
                    _logger.warning("Message containing an unexpected Content-Type 'binary/octet-stream', assuming 'application/octet-stream'")
                    part.replace_header('Content-Type', 'application/octet-stream')
                if part.get_content_type() == 'multipart/alternative':
                    alternative = True
                if part.get_content_type() == 'multipart/mixed':
                    mixed = True
                if part.get_content_maintype() == 'multipart':
                    continue  # skip container
                
                filename = part.get_filename()
                if part.get_content_type() == 'text/xml' and not part.get_param('charset'):
                    # for text/xml with omitted charset, the charset is assumed to be ASCII by the `email` module
                    # although the payload might be in UTF8
                    part.set_charset('utf-8')
                encoding = part.get_content_charset()  # None if attachment

                # Correcting MIME type for PDF files
                if part.get('Content-Type', '').startswith('pdf;'):
                    part.replace_header('Content-Type', 'application/pdf' + part.get('Content-Type', '')[3:])

                content = part.get_content()
                info = {'encoding': encoding}
                # 0) Inline Attachments -> attachments, with a third part in the tuple to match cid / attachment
                if filename and part.get('content-id'):
                    info['cid'] = part.get('content-id').strip('><')
                    attachments.append(filename)
                    continue
                # 1) Explicit Attachments -> attachments
                if filename or part.get('content-disposition', '').strip().startswith('attachment'):
                    attachments.append(filename or 'attachment')
                    continue
                # 2) text/plain -> <pre/>
                if part.get_content_type() == 'text/plain' and not (alternative and body):
                    body = append_content_to_html(body, content, preserve=True)
                # 3) text/html -> raw
                elif part.get_content_type() == 'text/html':
                    # multipart/alternative have one text and a html part, keep only the second
                    if alternative and not (html and mixed):
                        body = content
                    else:
                        # mixed allows several html parts, append html content
                        body = append_content_to_html(body, content, plaintext=False)
                    # TODO: maybe just setting to `True` is enough?
                    html = html or bool(content)
                    # we only strip_classes here everything else will be done in by html field of mail.message
                    body = html_sanitize(body, sanitize_tags=False, strip_classes=True)
                # 4) Anything else -> attachment
                else:
                    attachments.append(filename or 'attachment')
    return MessageDetail(body=body, attachments=attachments)
