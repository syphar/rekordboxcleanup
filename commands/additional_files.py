import unicodedata
from pathlib import PosixPath
from urllib.parse import urlparse, unquote, quote

import click
from lxml import etree


def _compareable_path(text):
    # see https://stackoverflow.com/questions/50537636/converting-acombining-acute-accent-to-%c3%81
    # accents on characters on the filesystem are reprented with a different way than in the url in the xml.
    # so we have to normalize.
    return unicodedata.normalize('NFC', str(text))


def _find_additional_files(directory, all_files):
    for item in directory.iterdir():
        if item.is_dir():
            yield from _find_additional_files(item, all_files)
        elif _compareable_path(item) not in all_files:
            yield item


def _rekordbox_file_url_to_path(url):
    """needed, since rekordbox urls are shit"""

    # some characters are not encoded correctly in the urls
    for ch in ('#', '?'):
        url = url.replace(ch, quote(ch))

    return unquote(urlparse(url).path)


@click.command()
@click.argument('rekordbox_xml')
@click.argument('folder')
@click.option('--delete', is_flag=True)
def additionalfiles(rekordbox_xml, folder, delete):
    et = etree.parse(rekordbox_xml)
    root = et.getroot()
    tracks = root.find('COLLECTION')

    all_files = [
        _compareable_path(_rekordbox_file_url_to_path(track.attrib['Location']))
        for track in tracks.findall('TRACK')
    ]

    folder = PosixPath(folder)
    if not folder.exists() or not folder.is_dir():
        raise click.BadParameter(
            "folder doesn't exist or is not a folder",
            param='folder'
        )

    click.echo('files in directory but not in library')
    for item in _find_additional_files(folder, all_files):
        click.echo(item)

        if delete:
            click.echo('deleting')
            item.unlink()
