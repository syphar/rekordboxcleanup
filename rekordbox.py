#!/usr/bin/env python
import collections
import re
from datetime import datetime
import os
import logging
from pprint import pprint

import click
from lxml import etree

logging.basicConfig(level=logging.INFO, format='%(message)s')

logger = logging.getLogger(__name__)


# TODO: action - list playlists with id
# TODO: action - tracks shared in defined playlists (only manual lists)
# TODO: action - list of tracks in more than 1 pl (only manual lists)
# TODO: action - remove tracks from one PL that are in any other manual


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


def _normalize_key(string):
    return string.strip().lower()


remix_patterns = (
    re.compile(r'^(.*)\((.*)remix\)$', re.IGNORECASE),
    re.compile(r'^(.*)\((.*)mix\)$', re.IGNORECASE),
    re.compile(r'^(.*)\-(.*)remix$', re.IGNORECASE),
    re.compile(r'^(.*)\-(.*)mix$', re.IGNORECASE),
)


def _split_song_title(title):
    for p in remix_patterns:
        match = p.match(title)
        if not match:
            continue

        return (
            match.group(1),
            match.group(2),
        )

    return (
        title,
        'original',
    )


def _sort_artist(artist):
    artists = artist.split(',')

    return ','.join(
        sorted([
            a.strip()
            for a in artists
        ])
    )


@click.command()
@click.argument('rekordbox_xml')
@click.argument('destination_xml')
def duplicatetracks(rekordbox_xml, destination_xml):
    et = etree.parse(rekordbox_xml)
    root = et.getroot()
    tracks = root.find('COLLECTION')

    counter = collections.Counter()
    tracks_by_key = collections.defaultdict(list)

    for track in tracks.findall('TRACK'):
        name, mix = _split_song_title(track.attrib['Name'])
        artist = _sort_artist(track.attrib['Artist'])

        key = (
            _normalize_key(artist),
            _normalize_key(name),
            _normalize_key(mix),
        )

        counter[key] = counter[key] + 1
        tracks_by_key[key].append(int(track.attrib['TrackID']))

    duplicate_track_ids = []

    for key, count in counter.items():
        if count <= 1:
            continue

        duplicate_track_ids.extend(tracks_by_key[key])

    _create_playlist(
        et,
        "duplicate tracks",
        duplicate_track_ids,
    )

    _write_xml(et, destination_xml)


cli.add_command(duplicatetracks)


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
