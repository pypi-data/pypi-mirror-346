from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")
setup(
    name='dwt_audio_stego',
    version='0.1.5',
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
            'dwt_audio_stego = dwt_audio_stego.main:cli',
        ],
    },
    author='HVT',
    description='Audio steganography using DWT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    python_requires='>=3.6',
)
