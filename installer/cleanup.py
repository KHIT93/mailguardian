#!/usr/bin/env python3
#
# MailGuardian installation script
#
import os, sys, platform

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

if __name__ == "__main__":
    del os.environ['MAILGUARDIAN_APP_DIR']
    del os.environ['MAILGUARDIAN_DB_HOST']
    del os.environ['MAILGUARDIAN_DB_USER']
    del os.environ['MAILGUARDIAN_DB_PASS']
    del os.environ['MAILGUARDIAN_DB_NAME']
    del os.environ['MAILGUARDIAN_DB_PORT']
    del os.environ['MAILGUARDIAN_APP_HOSTNAME']
    del os.environ['MAILSCANNER_SHARE_DIR']
    del os.environ['MAILSCANNER_CONFIG_DIR']