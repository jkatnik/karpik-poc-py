#!/usr/bin/python3

import boto3
import moviepy.editor as mpe
import webvtt  # for subtitles parsing
from moviepy.audio.fx.volumex import volumex
from pydub import AudioSegment
import io

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
        VoiceId=config['voice'],
        LanguageCode='pl-PL',
        OutputFormat='mp3',
        TextType='ssml',  # or text
        Text=sentence
    )

    raw = response['AudioStream'].read()
    response['AudioStream'].close()

    return AudioSegment.from_mp3(io.BytesIO(raw))


def generate_audio_track(config, subtitles):
    audio = AudioSegment.silent(duration=0)

    for caption in subtitles:
        print(f'Processing {caption}')
        sentence_audio = synthesize(caption.text, config)

        start = caption_start(caption)
        if audio.duration_seconds < start:
            break_length = (start - audio.duration_seconds) * 1000
            audio_break = AudioSegment.silent(break_length)
            audio = audio + audio_break
        audio = audio + sentence_audio

    audio_file_name = f"{config['audio_file_name']}"
    audio.export(audio_file_name, format='mp3')
    return audio_file_name


def caption_start(caption):
    nums = [float(n) for n in caption.start.split(':')]
    seconds = nums[0] * 3600 + nums[1] * 60 + nums[2]
    return seconds


if __name__ == '__main__':
    config = {
        'input_file_name':  'ultimate_roman_empire_ep1.mp4',
        'output_file_name':  'ultimate_roman_empire_ep1_pl.mp4',
        'audio_file_name': 'ultimate_roman_empire_ep1_pl.mp3',
        'subtitles_file_name': 'ultimate_roman_empire_ep1_pl_fixed.srt',
        'voice': 'Ewa' # Ewa | Maja | Jacek | Jan
    }

    polly_client = boto3.Session().client('polly')

    subtitles = webvtt.from_srt(f"{config['subtitles_file_name']}")
    # TODO add "Czytała Krystyna Karpikówna" at the end of file.

    audio_file_name = generate_audio_track(config, subtitles)

    input_clip = mpe.VideoFileClip(config['input_file_name'])

    new_audio = mpe.AudioFileClip(audio_file_name).fx(volumex, 1.5)
    old_audio = input_clip.audio.fx(volumex, 0.5)
    mixed_audio = mpe.CompositeAudioClip([old_audio, new_audio])

    final_clip = input_clip.set_audio(mixed_audio)
    final_clip.write_videofile(f"{config['output_file_name']}")