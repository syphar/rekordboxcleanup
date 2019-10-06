import collections
import re

import click
from lxml import etree

from commands.common import create_playlist, write_xml

REMIX_PATTERNS = (
    re.compile(r'^(.*)\((.*)remix\)$', re.IGNORECASE),
    re.compile(r'^(.*)\((.*)mix\)$', re.IGNORECASE),
    re.compile(r'^(.*)\-(.*)remix$', re.IGNORECASE),
    re.compile(r'^(.*)\-(.*)mix$', re.IGNORECASE),
)


def _normalize_key(string):
    return string.strip().lower()


def _split_song_title(title):
    for p in REMIX_PATTERNS:
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
    if ',' not in artist:
        return artist

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
def findduplicatetracks(rekordbox_xml, destination_xml):
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

    create_playlist(
        et,
        "duplicate tracks",
        duplicate_track_ids,
    )

    write_xml(et, destination_xml)
