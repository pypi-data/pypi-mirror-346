# realtime subtitle

This is an offline realtime subtitle program for M-series mac.

## install

require python >=3.9

```bash
# install dependencies
# if you don't have brew, install it from https://brew.sh/
brew install portaudio
brew upgrade python-tk


# install realtime-subtitle via pip
pip install realtime-subtitle
```

## usage

```bash
# to run with a ui
realtime-subtitle ui

# to parse a wav file
realtime-subtitle parse -f {your_wav_file_path}
```

you can find more whisper models [here](https://huggingface.co/collections/mlx-community/whisper-663256f9964fbb1177db93dc)

## troubleshooting

```bash
# chek if you tkinter verions is 8.6
python -m tkinter
# install one
conda  install tk=8.6
# or create a new environment
conda create -n subtitle python=3.9 tk=8.6
```
