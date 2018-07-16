from setuptools import find_packages, setup

if __name__ == '__main__':
    setup(
        name='rebuild-audio-file',

        version='0.1.0',

        description='Losslessly rebuild audio files.',
        long_description='Losslessly rebuild audio files.',

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
            'compare-mp3>=0.1.0',
            'get-video-properties>=0.1.0',
            'mutagen>=1.41.1',
        ],

        entry_points={
            'console_scripts': [
                'raf=raf:run',
            ],
        },
    )
