#!/usr/bin/env python
from datetime import datetime
import os
import logging
import random

import click
from lxml import etree

logging.basicConfig(level=logging.INFO, format='%(message)s')

logger = logging.getLogger(__name__)


# TODO: action - list playlists with id
# TODO: action - tracks shared in defined playlists (only manual lists)
# TODO: action - list of tracks in more than 1 pl (only manual lists)
# TODO: action - remove tracks from one PL that are in any other manual
# TODO: action - duplicate tracks by Artist/Title


@click.group()
def cli():
    pass


def _create_playlist(et, title, track_ids):
    root = et.getroot()
    playlists = root.find('PLAYLISTS')

    playlist_root = playlists.find('NODE')
    assert playlist_root.attrib['Name'] == 'ROOT'

    new_pl = etree.SubElement(playlist_root, 'NODE')
    new_pl.tail = '\n'
    new_pl.attrib['Name'] = '{} ({})'.format(title, datetime.now().isoformat())
    new_pl.attrib['Type'] = '1'
    new_pl.attrib['KeyType'] = '0'
    new_pl.attrib['Entries'] = str(len(track_ids))

    playlist_root.attrib['Count'] = str(int(playlist_root.attrib['Count']) + 1)

    for track_id in track_ids:
        child = etree.SubElement(new_pl, 'TRACK')
        child.tail = '\n'
        child.attrib['Key'] = str(track_id)


def _write_xml(et, destination):
    if os.path.exists(destination):
        os.remove(destination)

    et.write(destination)


@click.command()
@click.argument('rekordbox_xml')
@click.argument('destination_xml')
def trackswithoutplaylist(rekordbox_xml, destination_xml):
    et = etree.parse(rekordbox_xml)
    root = et.getroot()
    tracks = root.find('COLLECTION')
    playlists = root.find('PLAYLISTS')

    all_track_ids = {
        int(track.attrib['TrackID'])
        for track in tracks.findall('TRACK')
    }

    already_in_playlists = {
        int(item.attrib['Key'])
        for item in playlists.iter('TRACK')
    }

    _create_playlist(
        et,
        "tracks without playlist",
        all_track_ids - already_in_playlists
    )

    _write_xml(et, destination_xml)


cli.add_command(trackswithoutplaylist)

if __name__ == '__main__':
    cli()
