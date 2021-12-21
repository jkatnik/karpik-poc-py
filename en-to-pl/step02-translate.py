#!/usr/bin/python3

import boto3
import moviepy.editor as mpe
from botocore.exceptions import ClientError
import time
import urllib.request


def read_subtitles(config):
    with open(f"{config['subtitles_file_base']}_en.srt", 'r') as file:
        return file.read()


def translate(subtitles):
    translate_client = boto3.client(service_name='translate', region_name='eu-west-1', use_ssl=True)

    return translate_client.translate_text(Text=subtitles, SourceLanguageCode="en", TargetLanguageCode="pl")\
        .get('TranslatedText')


def save_subtitles(subtitles):
    text_file = open(f"{config['subtitles_file_base']}_pl.srt", "wt")
    text_file.write(subtitles)
    text_file.close()


def fix_time_format(subtitles):
    # AWS translate adds spaces before commas which breaks time format
    # e.g.: 00:00:13,860 —> 00:00:13 ,860
    return subtitles.replace(' ,', ',').replace('—>', '-->')


if __name__ == '__main__':
    config = {
        'input_file_name':  'ultimate_roman_empire_ep1.mp4',
        'audio_track_file_name': 'ultimate_roman_empire_ep1.mp3',
        'subtitles_file_base': 'ultimate_roman_empire_ep1',
        's3-bucket-name': 'karpik'
    }
    en_subtitles = read_subtitles(config)
    pl_subtitles = translate(en_subtitles)
    pl_subtitles = fix_time_format(pl_subtitles)

    save_subtitles(pl_subtitles)
