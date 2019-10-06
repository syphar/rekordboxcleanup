import click
from lxml import etree

from commands.common import create_playlist, write_xml


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

    create_playlist(
        et,
        "tracks without playlist",
        all_track_ids - already_in_playlists
    )

    write_xml(et, destination_xml)
