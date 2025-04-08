import os
import inquirer
import vlc
from dir_iter import *
from functools import partial

print = partial(print, sep = '', end = '')

def remove_prefix_from_file(file: os.DirEntry[str], prefix: str) -> bool:
    removed: bool = False
    name: str = file.name
    if name[0:len(prefix)] == prefix:
        removed = True
        newName: str = name[len(prefix):]
        newPath: str = os.path.join(os.path.dirname(file.path), newName)
        os.rename(file.path, newPath)
    return removed

def file_option_remove_prefix(file: os.DirEntry) -> None:
    prefix: str = inquirer.text(
        '\t\t\tEnter the name of the prefix to remove')
    affected = remove_prefix_from_file(file, prefix)
    if not affected:
        print(f'\t\t\t\tFilename wasn\'t changed - "{prefix}" is not the start of the filename!\n')

        


def dir_option_list_files_detail(dir_name: str) -> None:
    file_iter: os._ScandirIterator = os.scandir(dir_name)
    file = next(file_iter, None)
    while file is not None:
        _, file_extension = os.path.splitext(file.path)
        if file.is_file() and file_extension == ".mp3":
            print(f'-> \033[1;92mon MP3 file: {file.path}\n\033[0m')
            option: int = inquirer.list_input('Select an option', choices=[
                ('\tSkip to the next file', -1),
                ('\tListen to the file briefly', 0),
                ('\tRemove a prefix from the file\'s filename', 1),
                ('\tAutomatically change the song\'s metadata name to the filename', 2),
                ('\tEdit the file\'s metadata (artist, album, name...) manually', 3),
            ])
            match option:
                case -1:
                    file = next(file_iter, None)
                case 0:
                    audio: vlc.MediaPlayer = vlc.MediaPlayer(file.path)
                    audio.play()
                    _: str = inquirer.text('\t\tPress enter to stop...')
                    audio.stop()
                case 1:
                    file_option_remove_prefix(file)
                    
                    
