# organise_tv_shows
A python script to organise episodes of TV shows into your library.

## Installation (macOS)
```shell
$ brew install asdf
```
[Configure your shell](https://asdf-vm.com/guide/getting-started.html#_3-install-asdf) for asdf. You will need to
restart your terminal session.
```shell
$ asdf plugin add python
$ asdf install
$ pip install .
```

## Configure
Create a config file in its default location.
```shell
$ mkdir -p ~/.config/organise_tv_shows
$ cp config.yml.dist ~/.config/organise_tv_shows/config.yml
```
Configure the values in config.yml.

## Usage
```shell
$ organise_tv_shows

# Run with a different config file (~/.config/organise_tv_shows/config.other.yml)
$ organise_tv_shows --config-file config.other.yml

# Run with a config file outside of the default config directory
$ organise_tv_shows --config-file /usr/local/etc/organise_tv_shows/config.yml
```
