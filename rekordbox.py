#!/usr/bin/env python
import logging
from pathlib import PosixPath, Path
from pprint import pprint

import click

from commands.additional_files import additionalfiles
from commands.findduplicatetracks import findduplicatetracks
from commands.trackswithoutplaylist import trackswithoutplaylist

logging.basicConfig(level=logging.INFO, format='%(message)s')


# TODO: action - list playlists with id
# TODO: action - tracks shared in defined playlists (only manual lists)
# TODO: action - list of tracks in more than 1 pl (only manual lists)
# TODO: action - remove tracks from one PL that are in any other manual


@click.group()
def cli():
    pass


cli.add_command(findduplicatetracks)
cli.add_command(trackswithoutplaylist)
cli.add_command(additionalfiles)


@click.command()
@click.argument('folder')
def test(folder):
    f = Path(folder)
    for item in f.iterdir():
        pprint(item)
        pprint(str(item))
        pprint(list(str(item)))
        pprint(list(bytes(item).decode('utf-8')))
        pprint(list(bytes(item)))


cli.add_command(test)

if __name__ == '__main__':
    cli()
