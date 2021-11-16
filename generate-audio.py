#!/usr/bin/python3

# Links:
# - https://docs.aws.amazon.com/polly/latest/dg/get-started-what-next.html
# - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html
# - https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html
# - https://pypi.org/project/webvtt-py/

# scloud account login s24-playground AdminAccess --write


import boto3
from pydub import AudioSegment
import pydub.playback
import io
import webvtt  # for subtitles parsing
import moviepy.editor as mpe


class InlineClass(object):
    def __init__(self, dict):
        self.__dict__ = dict


def synthesize(text, config):
    sentence = f'''
    <speak>
         <prosody>
              {text}
         </prosody>
    </speak>
    '''

    response = polly_client.synthesize_speech(
        Engine='standard',  # standard|neural - neural nie obsługuje max-duration
        VoiceId= config.voice,
        LanguageCode='en-US',
        OutputFormat='mp3',
        TextType='ssml',  # or text
        Text=sentence
    )

    raw = response['AudioStream'].read()
    response['AudioStream'].close()

    return AudioSegment.from_mp3(io.BytesIO(raw))


def caption_start(caption):
    nums = [float(n) for n in caption.start.split(':')]
    seconds = nums[0] * 3600 + nums[1] * 60 + nums[2]
    return seconds


def load_captions(config):
    if config.captions_format == 'ttv':
        return webvtt.read(f'input/{config.captions_file_name}')
    elif config.captions_format == 'srt':
        return webvtt.from_srt(f'input/{config.captions_file_name}')
    else:
        raise Exception('Unsupported subtitles format')


if __name__ == '__main__':
    config = InlineClass({
        'captions_file_name': 'udemy_sample_02.srt',
        'movie_file_name': 'udemy_sample_02.mp4',
        'audio_file_name': 'udemy_sample_02.mp3',
        'captions_format': 'srt',  # srt | ttv
        'voice': 'Joey',  # Joey | Matthew
    })

    polly_client = boto3.Session().client('polly')

    audio = AudioSegment.silent(duration=0)

    captions = load_captions(config)

    for caption in captions:
        print(f'Processing {caption}')
        sentence_audio = synthesize(caption.text, config)

        start = caption_start(caption)
        if audio.duration_seconds < start:
            break_length = (start - audio.duration_seconds) * 1000
            audio_break = AudioSegment.silent(break_length)
            audio = audio + audio_break
        audio = audio + sentence_audio
    audio.export(f'output/{config.audio_file_name}', format='mp3')

    input_clip = mpe.VideoFileClip(f'input/{config.movie_file_name}')
    new_audio = mpe.AudioFileClip(f'output/{config.audio_file_name}')
    # new_audio = mpe.CompositeAudioClip([input_clip.audio, new_audio])
    final_clip = input_clip.set_audio(new_audio)
    final_clip.write_videofile(f'output/{config.movie_file_name}')
