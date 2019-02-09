#!/usr/bin/env python

import os
import logging
import random
from pprint import pprint

import click
from xml.etree import ElementTree

logging.basicConfig(level=logging.INFO, format='%(message)s')

logger = logging.getLogger(__name__)

@click.group()
def cli():
    pass

@click.command()
@click.argument('rekordbox_xml')
@click.argument('destination_xml', default='')
def unsorted_tracks(rekordbox_xml, destination_xml):
    et = ElementTree.parse(rekordbox_xml)
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

    without_playlist = all_track_ids - already_in_playlists

    if without_playlist:
        playlist_root = playlists.find('NODE')
        assert playlist_root.attrib['Name'] == 'ROOT'

        new_pl = ElementTree.SubElement(playlist_root, 'NODE')
        new_pl.tail = '\n'
        new_pl.attrib['Name'] = 'tracks without playlist ({0})'.format(random.randint(1000, 9999))
        new_pl.attrib['Type'] = '1'
        new_pl.attrib['KeyType'] = '1'
        new_pl.attrib['Entries'] = str(len(without_playlist))

        playlist_root.attrib['Count'] = str(int(playlist_root.attrib['Count']) + 1)

        for trackid in without_playlist :
            child = ElementTree.SubElement(new_pl, 'TRACK')
            child.tail = '\n'
            child.attrib['Key'] = str(trackid)


        destination = destination_xml or rekordbox_xml

        if os.path.exists(destination):
            os.remove(destination)

        et.write(destination)


cli.add_command(unsorted_tracks)

if __name__ == '__main__':
    cli()
