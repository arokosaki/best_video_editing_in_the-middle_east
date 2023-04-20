from datetime import datetime

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip


def convert_to_seconds(time_string, format='%M:%S.%f'):
    return (datetime.strptime(time_string, format) - datetime(year=1900, month=1, day=1)).total_seconds()


def create_video(audio_path, picture_path, start_time, end_time, output_path):
    duration = end_time - start_time
    audio = AudioFileClip(audio_path)
    audio = audio.subclip(t_start=start_time, t_end=end_time)
    picture = ImageClip(picture_path).set_duration(duration)
    picture.audio = audio
    picture.write_videofile(output_path, fps=24)
    audio.close()
    picture.close()

path = r"C:\podcast\Best Podcast in the Middle East - הפודקאסט הטוב במזרח התיכון - Pusha T - It's Almost Dry.mp3"

if __name__ == "__main__":
    create_video(path, start_time=60, end_time=100,
                 picture_path=r'c:\podcast\i-it-s-almost-dry-i-cover-art-by-sterling-ruby.jpg',
                 output_path=r'output.mp4')
