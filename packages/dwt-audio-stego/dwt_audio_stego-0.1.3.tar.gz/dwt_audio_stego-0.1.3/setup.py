from setuptools import setup, find_packages

setup(
    name='dwt-audio-stego',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'soundfile',
        'PyWavelets',
        'librosa',
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'dwt-audio-stego = dwt_audio_stego.main:cli',
        ],
    },
    author='HVT',
    description='Audio steganography using DWT',
    license='MIT',
    python_requires='>=3.6',
)
