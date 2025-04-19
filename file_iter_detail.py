import os
import inquirer
import vlc
from meta_edit import *
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
        'Enter the name of the prefix to remove')
    affected = remove_prefix_from_file(file, prefix)
    if not affected:
        print(f'\tFilename wasn\'t changed - "{prefix}" is not the start of the filename!\n')

def file_option_edit_filename(file: os.DirEntry) -> None:
    oldFilename: str = file.name
    newFilename: str = inquirer.text(
        'Enter the file\'s new filename',
        default = oldFilename
    )
    if not newFilename.endswith('.mp3'):
        rawFilename, extension = os.path.splitext(newFilename)
        newFilename = rawFilename + '.mp3'
    if len(newFilename) > 0 and newFilename != oldFilename:
        newPath: str = os.path.join(os.path.dirname(file.path), newFilename)
        os.rename(file.path, newPath)
        print(f'\tEdited filename to {newFilename}.\n')

def file_option_auto_change_name(file: os.DirEntry) -> None:
    filename, _ = os.path.splitext(file.name)
    mp3_handle = get_mp3_file(file.path)
    edit_mp3_name(mp3_handle, filename)
    save_mp3_file(mp3_handle)
    print(f'\tEdited file\'s metadata name to {filename}.\n')
    
def file_option_manual_edit(file: os.DirEntry) -> None:
    fields: list[str] = inquirer.checkbox('What fields do you want to change?', choices = [
        ('Artist name', 'artist'),
        ('Album name', 'album'),
        ('Song title', 'title'),
    ], default = ['artist', 'album'])
    function_input: dict[str, str|None] = {
        'title' : None, 'artist' : None, 'album' : None
    }
    mp3_handle = get_mp3_file(file.path)
    for field in fields:
        field_value: str = inquirer.text(f'Enter the song\'s new {field}',
                                         default=get_mp3_tag(mp3_handle, field))
        function_input[field] = field_value
    edit_mp3_tags(mp3_handle,
                  artist = function_input['artist'],
                  album  = function_input['album'],
                  title  = function_input['title'])
    save_mp3_file(mp3_handle)
    print(f'\tFile saved successfully.\n')
    

def dir_option_list_files_detail(dir_name: str) -> None:
    file_iter: os._ScandirIterator = os.scandir(dir_name)
    file = next(file_iter, None)
    while file is not None:
        _, file_extension = os.path.splitext(file.path)
        if file.is_file() and file_extension == ".mp3":
            print(f'-> \033[1;92mon MP3 file: {file.path}\n\033[0m')
            option: int = inquirer.list_input('Select an option', choices=[
                ('Skip to the next file', -1),
                ('Listen to the file briefly', 0),
                ('Remove a prefix from the file\'s filename', 1),
                ('Edit the file\'s filename manually', 4),
                ('Automatically change the song\'s metadata title to the filename', 2),
                ('Edit the file\'s metadata (artist, album, name...) manually', 3),
            ])
            match option:
                case -1:
                    file = next(file_iter, None)
                case 0:
                    audio: vlc.MediaPlayer = vlc.MediaPlayer(file.path)
                    audio.play()
                    _: str = inquirer.text('Press enter to stop...')
                    audio.stop()
                case 1:
                    file_option_remove_prefix(file)
                    print('\t\033[1;91mSkipping automatically to next file because filename was invalidated...\n\033[0m')
                    file = next(file_iter, None)
                case 2:
                    file_option_auto_change_name(file)
                case 3:
                    file_option_manual_edit(file)
                case 4:
                    file_option_edit_filename(file)
                    print('\t\033[1;91mSkipping automatically to next file because filename was invalidated...\n\033[0m')
                    file = next(file_iter, None)
                
                    
                    
