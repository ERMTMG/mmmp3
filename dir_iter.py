import os
from meta_edit import *
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
                    f'{items_listed} files listed, continue liisting?', default=True)
                if not continue_listing: 
                    break # maybe not the best thing but i don't really know how else to list files 5 by 5 being able to stop anytime

def remove_prefix_from_file(file: os.DirEntry[str], prefix: str) -> bool:
    removed: bool = False
    name: str = file.name
    if name[0:len(prefix)] == prefix:
        removed = True
        newName: str = name[len(prefix):]
        newPath: str = os.path.join(os.path.dirname(file.path), newName)
        os.rename(file.path, newPath)
    return removed
        
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
        if(file.is_file() and file_extension == 'mp3'):
            affected: bool = remove_prefix_from_file(file, prefix)
            if affected: affected_files += 1
    return affected_files
            
        
                
            

"""
def list_directory(dir: str) -> None:
    for entry in os.scandir(dir):
        if(entry.is_file()):
            print('found file: ', entry.name, '\n')
            filename, extension = os.path.splitext(entry.path)
            if(extension == '.mp3'):
                print(f'\t{filename} is an mp3 file! Playing...\n')
                player: vlc.MediaPlayer = vlc.MediaPlayer(entry.path)
                player.play()
                print('\ttype \"stop\" to stop...\n')
                stop = input()
                while(stop != 'stop'):
                    stop = input()
                player.stop()
                remove_prefix_from_file(entry, "[SPOTDOWNLOADER.COM] ")
            else:
                print(f'\textension: {extension}\n')
        else:
            print('found something weird, probably a directory: ', entry, '\n')
"""



def iter_directories(directories: list[str]):
    for dir_name in directories:
        if os.path.isdir(dir_name):
            dir_list = os.scandir(dir_name)
            _, _, files = next(os.walk(dir_name))
            file_count = len(files)
            print("Current directory: ", dir_name, " with ", file_count, " files\n")
            option: int = inquirer.list_input(
                f'What do you want to do in {dir_name}?',
                choices = [
                    ('Remove a prefix from all the files\' names', 0),
                    ('Change all the files\' artist metadata', 1),
                    ('Change all the files\' album metadata', 2),
                    ('Continue to next file', -1),
                ])
            match option:
                case 0:
                    affected_files: int = dir_option_remove_prefix(dir_name)
                    if affected_files == 0:
                        print('\tNo files affected.\n')
                    else:
                        print(f'\t{affected_files} files affected.\n')
                case 1:
                    pass
                case 2:
                    pass
                case -1:
                    pass
                case _:
                    raise RuntimeWarning('Unrecognized directory option\n')