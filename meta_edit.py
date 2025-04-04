import mutagen.easyid3
import mutagen.mp3

def get_mp3_file(filename: str) -> mutagen.easyid3.EasyID3:
    fileHandle: mutagen.File = mutagen.File(filename, easy = True)
    if fileHandle is not mutagen.easyid3.EasyID3:
        raise RuntimeError("file wasn't loaded as MP3, are you sure this is an MP3 file?")
    else:
        return fileHandle
    
def edit_mp3_tags(fileHandle: mutagen.easyid3.EasyID3, 
                  artist: str|None = None, 
                  album: str|None = None) -> None:
    if artist is not None:
        fileHandle['artist'] = artist
    if album is not None:
        fileHandle['album'] = album

def edit_mp3_artist(fileHandle: mutagen.easyid3.EasyID3, artistName: str) -> None:
    fileHandle['artist'] = artistName

def edit_mp3_album(fileHandle: mutagen.easyid3.EasyID3, albumName: str) -> None:
    fileHandle['album'] = albumName
    
def save_mp3_file(fileHandle: mutagen.easyid3.EasyID3, newFilename: str|None = None):
    if newFilename is not None:
        fileHandle.save(newFilename)
    else:
        fileHandle.save()
        
