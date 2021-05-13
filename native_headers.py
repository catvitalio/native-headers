#!/usr/bin/env python3

import subprocess
import re
from os.path import expanduser


def import_config():
    try:
        config = open(expanduser('~/.config/native-headers.conf'), 'r')
        windows = config.read().split('\n')
        windows = [empty for empty in windows if empty]
        config.close()
        return windows
    except FileNotFoundError:
        print('Configuration file not found! (~/.config/native-headers.conf)')
        exit()


def listen_windows():
    process = subprocess.Popen(
        'xprop -spy -root _NET_ACTIVE_WINDOW',
        shell=True,
        stdout=subprocess.PIPE
    )
    while True:
        window_must_native, window_id, wm_class = check_window(process)
        if window_must_native:
            set_native_headers(window_id, wm_class)


def check_window(process):
    native_windows = import_config()
    window_id = process.stdout.readline()
    window_id = str(re.search(r'0x[a-fA-F0-9]+', str(window_id)).group(0))
    if window_id != '0x0':
        wm_class = str(subprocess.check_output(
            'xprop WM_CLASS -id %s' % window_id,
            shell=True
        ))[21:-3]
        for window in native_windows:
            if window in wm_class:
                return True, window_id, wm_class
    return False, None, None


def set_native_headers(window_id, wm_class):
    subprocess.run(
        'xprop -format _MOTIF_WM_HINTS 32c -set _MOTIF_WM_HINTS 4 -id %s' % window_id,
        shell=True
    )
    print('Set native headers to window: ', window_id, ', ', wm_class, sep='')


if __name__ == "__main__":
    try:
        listen_windows()
    except KeyboardInterrupt:
        print('\nBye')
        exit()
