#!/usr/bin/env python3

import filecmp
import os
import sys

from colorama import Back, Fore, Style
from mutagen.id3 import ID3
from raf import rebuild_audio_file


def copy_tags(a, b):
    a, b = ID3(a), ID3(b)
    [b.add(a[x]) for x in a]
    b.save()


def round_trip(a):
    assert a.endswith('.mp3')
    b = 'b.mp3'
    rebuild_audio_file(a, b)
    copy_tags(a, b)
    if not filecmp.cmp(a, b, False):
        raise RuntimeError('My sadness very big')
    os.unlink(b)


def run():
    if len(sys.argv) == 2:
        round_trip(sys.argv[1])
        print('---')
        print(f'{Back.BLACK}{Fore.GREEN}{Style.BRIGHT}Done{Style.RESET_ALL}')
    else:
        print(f'Usage: {sys.argv[0]} input.mp3')


if __name__ == '__main__':
    run()
