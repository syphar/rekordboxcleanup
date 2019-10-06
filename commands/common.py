import os
from datetime import datetime

from lxml import etree


def create_playlist(et, title, track_ids):
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


def write_xml(et, destination):
    if os.path.exists(destination):
        os.remove(destination)

    et.write(destination)
