from pathlib import Path
from setuptools import find_packages, setup

README = Path(__file__).resolve().parent / 'README.md'

if __name__ == '__main__':
    setup(
        name='rebuild-audio-file',

        version='0.1.1',

        description='Losslessly rebuild audio files.',
        long_description=README.read_text(encoding='utf-8'),
        long_description_content_type='text/markdown',

        url='https://github.com/mvasilkov/python-rebuild-audio-file',

        author='Mark Vasilkov',
        author_email='mvasilkov@gmail.com',

        license='MIT',

        classifiers=[
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Multimedia :: Sound/Audio',
        ],

        keywords='ffmpeg flac lame lossless mp3',

        packages=find_packages(),
        include_package_data=True,

        install_requires=[
            'colorama>=0.4.0',
            'compare-mp3>=0.1.1',
            'get-video-properties>=0.1.1',
            'mutagen>=1.41.1',
        ],

        entry_points={
            'console_scripts': [
                'raf=raf:run',
            ],
        },
    )
