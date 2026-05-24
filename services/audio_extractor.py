import os
import subprocess


def extract_audio(video_path):

    audio_path = (
        os.path.splitext(video_path)[0]
        + ".mp3"
    )

    command = (
        f'ffmpeg -i "{video_path}" '
        f'-q:a 0 -map a '
        f'"{audio_path}" -y'
    )

    subprocess.run(
    [
        "ffmpeg",
        "-i",
        video_path,
        "-q:a",
        "0",
        "-map",
        "a",
        audio_path,
        "-y"
    ],
    check=True
)

    return audio_path