import mutagen.mp3

def get_mp3_file(filename: str) -> mutagen.mp3.EasyMP3:
    fileHandle: mutagen.File = mutagen.File(filename, easy = True)
    if isinstance(fileHandle, mutagen.mp3.EasyMP3):
        return fileHandle
    else:
        raise RuntimeWarning('File wasn\'t opened as MP3')

def get_mp3_tag(fileHandle: mutagen.mp3.EasyMP3, tag: str) -> str:
    output = fileHandle[tag]
    if isinstance(output, list):
        return output[0]
    else:
        return output
    
def edit_mp3_tags(fileHandle: mutagen.mp3.EasyMP3, 
                  artist: str|None = None, 
                  album: str|None = None,
                  title: str|None = None) -> None:
    if artist is not None:
        fileHandle['artist'] = artist
    if album is not None:
        fileHandle['album'] = album
    if title is not None:
        fileHandle['title'] = title

def edit_mp3_artist(fileHandle: mutagen.mp3.EasyMP3, artistName: str) -> None:
    fileHandle['artist'] = artistName

def edit_mp3_album(fileHandle: mutagen.mp3.EasyMP3, albumName: str) -> None:
    fileHandle['album'] = albumName

def edit_mp3_name(fileHandle: mutagen.mp3.EasyMP3, name: str) -> None:
    fileHandle['title'] = name
    
def save_mp3_file(fileHandle: mutagen.mp3.EasyMP3, newFilename: str|None = None):
    if newFilename is not None:
        fileHandle.save(newFilename)
    else:
        fileHandle.save()
        
