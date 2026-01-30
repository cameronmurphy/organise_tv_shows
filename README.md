# organise_tv_shows
A python script to organise episodes of TV shows into your library.

## Installation (macOS)
```sh
$ brew install mise
```
Ensure `mise activate` is [in your shell rc/profile](https://mise.jdx.dev/cli/activate.html). If it needed to be added,
restart your terminal session.
```sh
$ mise install
$ pip install .
```

## Configure
Create a config file in its default location.
```sh
$ mkdir -p ~/.config/organise_tv_shows
$ cp config.yml.dist ~/.config/organise_tv_shows/config.yml
```
Configure the values in config.yml.

## Running in development
```sh
$ python -m organise_tv_shows
```

## Building
```sh
$ ./scripts/build.sh
```

## Usage
```sh
$ organise_tv_shows

# Run with a different config file (~/.config/organise_tv_shows/config.other.yml)
$ organise_tv_shows --config-file config.other.yml

# Run with a config file outside of the default config directory
$ organise_tv_shows --config-file /usr/local/etc/organise_tv_shows/config.yml
```
