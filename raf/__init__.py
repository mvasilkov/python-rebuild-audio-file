from enum import Enum
from functools import lru_cache
from os import access, chmod, R_OK
import os.path as path
from pathlib import Path
import platform
from shutil import copy as copy_file, which
import stat
from subprocess import check_call, check_output
import sys
from tempfile import TemporaryDirectory

from colorama import Back, Fore, Style
from compare_mp3 import compare, SAME_FILE, SAME_WAV
from mutagen.id3 import ID3
from videoprops import get_audio_properties

ffmpeg_options = ('-c', 'copy', '-bitexact', '-map', '0:a:0', '-map_metadata', '-1', '-y')
ffmpeg_options2 = (*ffmpeg_options[:2], '-write_xing', '0', *ffmpeg_options[2:])
flac_options = ('--best', '--delete-input-file', '-P', '4096', '-V', '-f')

binary_dependencies = Path(__file__).parent / 'binary_dependencies'
system = platform.system()


def which_prog(prog_name: str, prog_binary: str):
    if system == 'Darwin':
        a = str(binary_dependencies / prog_binary)
        set_executable(a)  # package built on Windows won't have executable bits set
        return a

    if system == 'Windows':
        return str(binary_dependencies / f'{prog_binary}.exe')

    prog = which(prog_binary)
    if not prog:
        raise RuntimeError(f'{prog_name} is not installed')

    return prog


@lru_cache(1)
def which_ffmpeg():
    return which_prog('FFmpeg', 'ffmpeg')


@lru_cache(1)
def which_flac():
    return which_prog('FLAC', 'flac')


def test_requirements():
    assert sys.version_info.major == 3 and sys.version_info.minor >= 6

    version = check_output([which_ffmpeg(), '-version'], encoding='utf-8')
    assert version.startswith('ffmpeg version')

    version = check_output([which_flac(), '-version'], encoding='utf-8')
    assert version.startswith('flac 1.3.2')


class Type(Enum):
    FLAC = '.flac'
    MP3 = '.mp3'


def rebuild_audio_file(filename: str, copy: str):
    filename_lower = filename.lower()
    filetype = (Type.FLAC if filename_lower.endswith(Type.FLAC.value) else
                Type.MP3 if filename_lower.endswith(Type.MP3.value) else None)

    if filetype is None:
        raise RuntimeError(f'Unknown file type: {filename}')

    if path.isdir(copy):
        copy = path.join(copy, path.basename(filename))
    elif not copy.lower().endswith(filetype.value):
        raise RuntimeError('Files should be of the same type')

    if not path.isfile(filename) or not access(filename, R_OK):
        raise RuntimeError(f'File not found or inaccessible: {filename}')

    if path.exists(copy):
        raise RuntimeError(f'Not overwriting existing file: {copy}')

    if filetype is Type.FLAC:
        with TemporaryDirectory('.w64') as tempdir:
            buf = tempdir + '/buf.w64'
            check_call([which_flac(), '-d', '-o', buf, filename])
            set_writable(buf)
            check_call([which_flac(), *flac_options, '-o', copy, buf])

        return

    assert filetype is Type.MP3

    props = get_audio_properties(filename)
    options = ffmpeg_options2 if props['start_time'] == '0.000000' else ffmpeg_options

    with TemporaryDirectory('.mp3') as tempdir:
        buf = tempdir + '/buf.mp3'
        copy_file(filename, buf)
        set_writable(buf)
        ID3(buf).delete()
        check_call([which_ffmpeg(), '-i', buf, *options, copy])

    if compare(filename, copy, check_tags=False) not in (SAME_FILE, SAME_WAV):
        print('---')
        print(f'{Back.BLACK}{Fore.RED}{Style.BRIGHT}Not lossless{Style.RESET_ALL}')
        raise RuntimeError('Not lossless')


def set_writable(a):
    if system == 'Windows':
        chmod(a, stat.S_IWRITE)


def noexcept(fun):
    def wrapped(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except:
            pass

    return wrapped


@noexcept
def set_executable(a):
    if system != 'Windows':
        chmod(a, 0o755)


def run():
    test_requirements()

    if len(sys.argv) == 3:
        rebuild_audio_file(*sys.argv[1:])
        print('---')
        print(f'{Back.BLACK}{Fore.GREEN}{Style.BRIGHT}Done{Style.RESET_ALL}')
    else:
        print(f'Usage: {sys.argv[0]} existing.mp3 new.mp3')


if __name__ == '__main__':
    run()
