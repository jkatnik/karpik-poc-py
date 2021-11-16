#!/usr/bin/python3

# Links:
# - https://github.com/jiaaro/pydub

from pydub import AudioSegment
from os import getcwd


def print_file_info(file_name, segment):
    print(f'Details of {file_name}')
    print(f'    File duration in seconds: {segment.duration_seconds}')


if __name__ == '__main__':
    cwd = (getcwd()).replace(chr(92), '/')

    audio1 = AudioSegment.from_mp3(f'{cwd}/input/beep-03.mp3')
    audio2 = AudioSegment.from_mp3(f'{cwd}/input/beep-08b.mp3')
    silence = AudioSegment.silent(duration=1500)

    output = audio1 + silence + audio2
    output_path = f'{cwd}/output/merged.mp3'
    output.export(output_path, format='mp3')

    print_file_info('merged.mp3', output)
    print_file_info('beep-03.mp3', audio1)
    print_file_info('beep-08b.mp3', audio2)

    print('\ndone!')

# OscarKuzniar