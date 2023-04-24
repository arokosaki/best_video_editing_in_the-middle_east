import webbrowser
from datetime import datetime
from pathlib import Path

from requests_html import HTMLSession
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip

PODCAST_FOLDER = r'c:\podcast'
PROPERTIES = ['image', 'audio', 'title']
SUFFIXES = {
    'audio': '.mp3',
    'image': '.jpg'
}


def convert_to_seconds(time_string):
    formats = '%H:%M:%S.%f', '%H:%M:%S', '%M:%S.%f', '%M:%S'
    for format_ in formats:
        try:
            return (datetime.strptime(time_string, format_) - datetime(year=1900, month=1, day=1)).total_seconds()
        except ValueError:
            pass
    else:
        raise ValueError(f'time data \'{time_string}\' does not match allowed formats')



def create_video(audio_path, picture_path, start_time, end_time, output_path):
    duration = end_time - start_time
    audio = AudioFileClip(audio_path)
    audio = audio.subclip(t_start=start_time, t_end=end_time)
    picture = ImageClip(picture_path).set_duration(duration)
    picture.audio = audio
    picture.write_videofile(output_path, fps=24)
    audio.close()
    picture.close()


def get_media(track_no):
    s = HTMLSession()
    r = s.get(f'https://middleast.best/library/tracks/{track_no}/')
    fetch_property = lambda x: r.html.find(f'[property=og\:{x}]', first=True).attrs['content']
    properties = {propertea: fetch_property(propertea) for propertea in PROPERTIES}
    title = properties.pop(PROPERTIES[2])
    properties[PROPERTIES[0]] = properties[PROPERTIES[0]].replace('200x200', '600x600')
    path = Path(PODCAST_FOLDER) / f'{title}-{track_no}'
    if not path.exists():
        path.mkdir()
    for propertea in properties:
        file = path / (title + SUFFIXES[propertea])
        with file.open('wb') as f:
            f.write(s.get(properties[propertea]).content)
        properties[propertea] = file
    return properties


def check_mp3(track_no):
    result = {}
    revers_suffixes = {value: key for key, value in SUFFIXES.items()}
    path = Path(PODCAST_FOLDER)
    for folder in path.iterdir():
        track_num = int(folder.name.split('-')[-1])
        if track_num == track_no:
            for file in folder.iterdir():
                try:
                    result[revers_suffixes[file.suffix]] = file
                except KeyError:
                    pass
            if len(result) == 2:
                return result

def output_file_name(files,name):
    file = files[PROPERTIES[1]]
    file = file.with_stem(f'{file.stem}-{name}')
    file = file.with_suffix('.mp4')
    return file


def create_video_clip(name, start_time, end_time, track_no):
    files = check_mp3(track_no) or get_media(track_no)
    start_time = convert_to_seconds(start_time)
    end_time = convert_to_seconds(end_time)
    output_path = output_file_name(files, name)
    create_video(
        audio_path=str(files['audio']),
        picture_path=str(files['image']),
        start_time=start_time,
        end_time=end_time,
        output_path=str(output_path)
    )

def clean_filename(name):
    """Ensures each file name does not contain forbidden characters and is within the character limit"""
    # For some reason the file system (Windows at least) is having trouble saving files that are over 180ish
    # characters.  I'm not sure why this is, as the file name limit should be around 240. But either way, this
    # method has been adapted to work with the results that I am consistently getting.
    forbidden_chars = '"*\\/\'.|?:<>'
    filename = ''.join([x if x not in forbidden_chars else '#' for x in name])
    if len(filename) >= 176:
        filename = filename[:170] + '...'
    return filename



if __name__ == "__main__":
    create_video_clip(
        name='nisyon_rishon',
        start_time='54:00',
        end_time='59:00',
        track_no=39
    )