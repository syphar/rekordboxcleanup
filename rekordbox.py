#!/usr/bin/env python
import logging
from pathlib import PosixPath, Path
from pprint import pprint

import click

from commands.additional_files import additionalfiles
from commands.findduplicatetracks import findduplicatetracks
from commands.trackswithoutplaylist import trackswithoutplaylist

logging.basicConfig(level=logging.INFO, format='%(message)s')


@click.group()
def cli():
    pass


cli.add_command(findduplicatetracks)
cli.add_command(trackswithoutplaylist)
cli.add_command(additionalfiles)


if __name__ == '__main__':
    cli()
