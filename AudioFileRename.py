import os
import re
import sys

def filter_tag_value(value):
    return value.translate(str.maketrans('~#%&*{}\:<>?/+|"', '________________'))

def get_artist(filename):
    command = "TaggerSharp \"" + filename + "\" --Artists"
    return os.popen(command).read().rstrip()

def get_title(filename):
    command = "TaggerSharp \"" + filename + "\" --Title"
    return os.popen(command).read().rstrip()

def get_track(filename):
    command = "TaggerSharp \"" + filename + "\" --Track"
    return os.popen(command).read().rstrip().zfill(2)

def get_album(filename):
    command = "TaggerSharp \"" + filename + "\" --Album"
    return os.popen(command).read().rstrip()

def set_artist(filename, new_value):
    update_command = "TaggerSharp \"" + filename + "\" --Artists=\"" + new_value + "\""
    os.system(update_command)

def validate_expected_fields_exist(full_filename, artist, album, title):
    if len(artist) == 0:
        print('Warning: No artist tag exists for %s' % full_filename)
    if len(album) == 0:
        print('Warning: No album tag exists for %s' % full_filename)
    if len(title) == 0:
        print('Warning: No title tag exists for %s' % full_filename)

def check_for_starting_the_in_artist(dirname, filename):
    full_filename = dirname + "\\" + filename
    artist = get_artist(full_filename)
    if re.match("^The ", artist):
        new_artist = artist[4:] + " (The)"
        set_artist(full_filename, new_artist)

def rename_file(dir_name, filename, file_extension):
    full_filename = dir_name + "\\" + filename
    artist = get_artist(full_filename)
    album = get_album(full_filename)
    title = get_title(full_filename)
    validate_expected_fields_exist(full_filename, artist, album, title)
    new_filename = dir_name + "\\" + \
        filter_tag_value(artist) + '-' + \
        filter_tag_value(album) + '-' + \
        get_track(full_filename) + '-' + \
        filter_tag_value(title) + file_extension.rstrip()
    os.rename(full_filename, new_filename)

if len(sys.argv) != 2:
    print('Usage: %s directory' % sys.argv[0])
    print('   directory = Directory path containing audio files')
    exit()

for dir_name, sub_dir_list, file_list in os.walk(sys.argv[1]):
    for filename in file_list:
        name_no_extension, file_extension = os.path.splitext(filename)
        file_extension.rstrip()  # Remove the newline
        if file_extension.lower() in ['.mp3', '.flac', '.m4a', '.wma']:
            check_for_starting_the_in_artist(dir_name, filename)
            rename_file(dir_name, filename, file_extension)
        else:
            full_filename = dir_name + "\\" + filename
            print('Warning: Found file with unexpected extension: %s' % full_filename)
