from setuptools import setup, find_packages

setup(
    name='dwt_audio_stego',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'soundfile',
        'PyWavelets',
        'scipy',
    ],
    entry_points={
        'console_scripts': [
            'dwt_audio_stego = dwt_audio_stego.main:cli',
        ],
    },
    author='Your Name',
    description='Audio steganography using DWT',
    license='MIT',
    python_requires='>=3.6',
)
