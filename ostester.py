import platform
get_os_data = False

try:
    get_os_data = platform.freedesktop_os_release
except AttributeError:
    print('*** Patching Python %s with platform.freedesktop_os_release from Python 3.10.x ***' % (platform.python_version(),))
    import re
    ### freedesktop.org os-release standard
    # https://www.freedesktop.org/software/systemd/man/os-release.html

    # NAME=value with optional quotes (' or "). The regular expression is less
    # strict than shell lexer, but that's ok.
    _os_release_line = re.compile(
        "^(?P<name>[a-zA-Z0-9_]+)=(?P<quote>[\"\']?)(?P<value>.*)(?P=quote)$"
    )
    # unescape five special characters mentioned in the standard
    _os_release_unescape = re.compile(r"\\([\\\$\"\'`])")
    # /etc takes precedence over /usr/lib
    _os_release_candidates = ("/etc/os-release", "/usr/lib/os-release")
    _os_release_cache = None
    def _parse_os_release(lines):
        # These fields are mandatory fields with well-known defaults
        # in practice all Linux distributions override NAME, ID, and PRETTY_NAME.
        info = {
            "NAME": "Linux",
            "ID": "linux",
            "PRETTY_NAME": "Linux",
        }

        for line in lines:
            mo = _os_release_line.match(line)
            if mo is not None:
                info[mo.group('name')] = _os_release_unescape.sub(
                    r"\1", mo.group('value')
                )

        return info
    def freedesktop_os_release():
        """Return operation system identification from freedesktop.org os-release
        """
        global _os_release_cache

        if _os_release_cache is None:
            errno = None
            for candidate in _os_release_candidates:
                try:
                    with open(candidate, encoding="utf-8") as f:
                        _os_release_cache = _parse_os_release(f)
                    break
                except OSError as e:
                    errno = e.errno
            else:
                raise OSError(
                    errno,
                    f"Unable to read files {', '.join(_os_release_candidates)}"
                )

        return _os_release_cache.copy()
    get_os_data = freedesktop_os_release
if __name__ == '__main__':
    print(get_os_data())