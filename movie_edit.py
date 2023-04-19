from datetime import datetime

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip


def convert_to_seconds(time_string, format='%M:%S.%f'):
    return (datetime.strptime(time_string, format) - datetime(year=1900, month=1, day=1)).total_seconds()



def create_video(audio_path, start_time, end_time, picture_path, output_path):
    # Load the audio file and get the desired duration


    audio = AudioFileClip(audio_path)
    duration = end_time - start_time

    audio = audio.cutout(start_time, end_time)

    # Load the picture and set its duration to match the audio duration
    picture = ImageClip(picture_path).set_duration(duration)

    # Create a video clip with the picture and the audio
    video = CompositeVideoClip([picture, audio])

    # Write the output video file
    video.write_videofile(output_path, fps=24)
"""ATBBey26mXPWWnmSQB4CtFbGJHNV4FFE2468"""

if __name__ == "__main__":
    # Example usage: create a 10-second video starting from 5 seconds into the audio file, using a picture called "picture.jpg"
    # create_video("audio.wav", 5, 15, "picture.jpg", "output.mp4")
    print()