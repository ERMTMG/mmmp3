import os

from meta_edit import *
from file_iter_detail import *
import inquirer
from functools import partial

print = partial(print, sep = '', end = '')

def list_files_by_chunks(dir_name: str) -> None:
    _FILE_LIST_CHUNK_SIZE: int = 5
    
    items_listed: int = 0
    for file in os.scandir(dir_name):
        if file.is_file():
            print(f'\t-> {file.name}\n')
            items_listed += 1
            if items_listed % _FILE_LIST_CHUNK_SIZE == 0 and items_listed != 0:
                continue_listing: bool = inquirer.confirm(
                    f'{items_listed} files listed, continue listing?', default=True)
                if not continue_listing: 
                    break # maybe not the best thing but i don't really know how else to list files 5 by 5 being able to stop anytime
        
def dir_option_remove_prefix(dir_name: str) -> int:
    view_files: bool = inquirer.confirm(
        'Do you want to view the filenames of the directory first?', default=False)
    if view_files:
        list_files_by_chunks(dir_name)
    prefix: str = inquirer.text(
        'Enter the name of the prefix to remove')
    affected_files: int = 0
    for file in os.scandir(dir_name):
        _, file_extension = os.path.splitext(file.path)
        if(file.is_file() and file_extension == '.mp3'):
            affected: bool = remove_prefix_from_file(file, prefix)
            if affected: affected_files += 1
    return affected_files

def dir_option_change_in_all(dir_name: str) -> int:
    view_files: bool = inquirer.confirm(
        'Do you want to view the filenames of the directory first?', default=False)
    if view_files:
        list_files_by_chunks(dir_name)
    affected_files: int = 0
    field_changed: int = inquirer.list_input(
        'What field do you want to change in all files?', 
        choices = [
            ('Artist', 0),
            ('Album', 1),
            ('Both artist and album', 2)
        ])
    name: str | list[str]
    match field_changed:
        case 0:
            name = inquirer.text('Introduce the artist\'s name')
        case 1:
            name = inquirer.text('Introduce the album\'s name')
        case 2:
            questions: list = [inquirer.Text('artist', message='Introduce the artist\'s name'), 
                         inquirer.Text('album', message='Introduce the album\'s name')]
            answers: dict = inquirer.prompt(questions)
            name = [answers['artist'], answers['album']]
        case _:
            raise RuntimeError('Unrecognized option')
    handles: list[mutagen.mp3.EasyMP3] = []
    for file in os.scandir(dir_name):
        _, extension = os.path.splitext(file.path)
        if(file.is_file() and extension == '.mp3'):
            mp3_handle = get_mp3_file(file.path)
            handles.append(mp3_handle)
            match field_changed:
                case 0:
                    edit_mp3_artist(mp3_handle, name)
                case 1:
                    edit_mp3_album(mp3_handle, name)
                case 2:
                    artist, album = tuple(name)
                    edit_mp3_tags(mp3_handle, artist, album)
            affected_files += 1
    confirm_changes: bool = inquirer.confirm(
        f'Do you wish to save the changes? {affected_files} files will be affected', default=True)
    if confirm_changes:
        for handle in handles:
            save_mp3_file(handle)
    else:
        affected_files = 0
    return affected_files


def iter_directories(directories: list[str]):
    for dir_name in directories:
        if os.path.isdir(dir_name):
            dir_list = os.scandir(dir_name)
            _, _, files = next(os.walk(dir_name))
            file_count = len(files)
            mp3_file_count = len([file for file in files if file.endswith('.mp3')])
            if file_count == mp3_file_count:
                print(f"Current directory: {dir_name}, with {file_count} MP3 files\n")
            else:
                print(f"""Current directory: {dir_name}, 
                      with {file_count} files (of which {mp3_file_count} are MP3's)\n""")
            option: int = inquirer.list_input(
                f'What do you want to do in {dir_name}?',
                choices = [
                    ('Remove a prefix from all the files\' names', 0),
                    ('Change all the files\' metadata at once', 1),
                    (f'Go through the {mp3_file_count} files individually',2),
                    ('Skip to next directory', -1)
                ])
            match option:
                case 0:
                    affected_files: int = dir_option_remove_prefix(dir_name)
                    if affected_files == 0:
                        print('\tNo files affected.\n')
                    else:
                        print(f'\t{affected_files} files affected.\n')
                case 1:
                    affected_files: int = dir_option_change_in_all(dir_name)
                    if affected_files == 0:
                        print('\tNo files affected.\n')
                    else:
                        print(f'\t{affected_files} files affected.\n')
                case 2:
                    dir_option_list_files_detail(dir_name)
                case -1:
                    pass
                case _:
                    raise RuntimeWarning('Unrecognized directory option\n')
        else:
            print(f'{dir_name} is not a directory!\n')