# MMMP3
MMMP3 is a basic Python utility for bulk editing mp3 file names and metadata, brought to you by the need to switch from Spotify (my alternative of choice was a physical MP3 player which sorted songs by the metadata in the MP3 files).
## Installation
To install the program, just get all the relevant `.py` files in one folder and install all the needed dependencies:
- `sys`, `os`, `functools`, `vlc` from standard library
- `mutagen` (for the whole metadata editing deal)
- `inquirer` (for the command line UI. A GUI is also planned)

Then just run `mmmp3.py`. 
## Running the program - functionality documentation
The intended syntax (as of now) is:
```
python3 mmmp3.py <dir_1> <dir_2> <dir_3> ... <dir_n>
```
Where each `<dir_i>` is the path to a directory from the working directory.
For each directory you will be given the choice to:
1. **Remove a prefix from the directory's files' names.**
    _For when annoying MP3 downloading sites put their own domain at the start of each downloaded MP3's filename. If some file doesn't start with the given prefix, it will be ignored._
2. **Change all the files' metadata at once.**
    _For when all the files in the directory are from the same artist or album, and you can't be bothered to put the same value in all of them individually. Don't worry if you mistype something, you can choose to save the changes or not._
3. **View all of the directory's files individually**
4. **Skip to the next directory**

If you chose option 3, for each MP3 file in the directory (other files will be skipped), you will have the choice to:
1. **Skip to the next file**
2. **Listen to the file**
    _Plays the file until you press_ `RETURN` _again. Useful for when you don't know what song it is just through the filename, for example._
3. **Remove a prefix from the filename**
    _The same as the option discussed previously, but for individual files._
4. **Automatically change the song's metadata title to the filename**
5. **Edit the file's metadata manually**
    _Allows you to set the MP3's saved title, artist and/or album manually if none of the other options satisfy you._

When you choose one of these options (except for 1), you wil not go automatically to the next file. This is to allow multiple changes to be made to each file (for example, it wouldn't be of much use if you automatically skipped to the next file after playing the MP3), and is also the reason why skipping to the next file is the first option.

## Planned updates
The following changes are planned to be released soon™:
- Filename editing (priority)
- Enabling edits to more metadata fields:
    - Comments for each track
    - Year of release
    - Genre (There are like 190 genres available in the ID3 standard, with gems such as `136: Christian Gangsta Rap`, `109: [REDACTED] Groove` and `167: Industro-Goth`. I'm not making these up.)
    - Album art, maybe? I don't know how many MP3 players support that.
- Command line options:
    - `--help`, obviously.
    - `-v` for **verbosity** (shows each MP3 file edited in a directory)
    - `-s` for **safety** level (the higher the safety level, the more confirmation is asked to edit files)
    - `-a` for **autoplay** (when editing MP3 files manually, plays each one of them automatically)
    - `-ñ` para hacerlo disponible en **español**
