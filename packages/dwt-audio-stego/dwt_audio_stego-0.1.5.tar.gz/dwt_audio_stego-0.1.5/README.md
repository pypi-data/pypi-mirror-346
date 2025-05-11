# Audio Steganography

A simple Python tool to hide and extract secret text in audio files using Discrete Wavelet Transform (DWT).

## Usage

```bash
python3 -m dwt_audio_stego [options]

optional arguments:
  -h, --help                           show this help message and exit
  -s, --secret SECRET                  Specify secret text
  -i, --input INPUT                    Specify input filename
  -o, --output OUTPUT                  Specify output filename
  -e, --extract EXTRACT                Specify embedded filename to extract secret
