import os
import vlc
from functools import partial

print = partial(print, sep = '', end = '')

def remove_prefix_from_file(file: os.DirEntry[str], prefix: str) -> None:
    name: str = file.name
    if name[0:len(prefix)] == prefix:
        newName: str = name[len(prefix):]
        newPath: str = os.path.join(os.path.dirname(file.path), newName)
        os.rename(file.path, newPath)
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
            print("Current directory: ", dir_name, " with ", len(dir_list), " files\n")
            print("Do you wish to:")