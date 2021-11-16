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
import webvtt # for subtitles parsing
import time
import moviepy.editor as mpe

def synthesize(text, max_duration):
    sentence = f'''
    <speak>
         <prosody rate="medium">
              {text}.
         </prosody>
    </speak>
    '''

    response = polly_client.synthesize_speech(
        Engine = 'standard', # standard|neural - neural nie obsługuje max-duration
        VoiceId='Matthew',
        LanguageCode='en-US',
        OutputFormat='mp3',
        TextType='ssml', # or text
        Text=sentence
    )


    raw = response['AudioStream'].read()
    response['AudioStream'].close()

    return AudioSegment.from_mp3(io.BytesIO(raw))

def caption_duration(caption):
    end = time.mktime(time.strptime(caption.end, '%H:%M:%S.%f'))
    start = time.mktime(time.strptime(caption.start, '%H:%M:%S.%f'))
    return (end - start)

def caption_start(caption):
    nums = [float(n) for n in caption.start.split(':')]
    seconds = nums[0] * 3600 + nums[1] * 60 + nums[2]
    return seconds

if __name__ == '__main__':
    polly_client = boto3.Session().client('polly')

    audio = AudioSegment.silent(duration=0)

    captions = webvtt.read('input/udemy_sample_01.vtt') #[:3]
    
    for caption in captions:
        expected_duration = caption_duration(caption)
        sentence = synthesize(caption.text, expected_duration)

        start = caption_start(caption)
        if audio.duration_seconds < start:
            break_length = (start - audio.duration_seconds) * 1000
            audio_break = AudioSegment.silent(break_length)
            audio = audio + audio_break
        audio = audio + sentence
    audio.export('output/udemy_sample_01.mp3', format='mp3')
    # # pydub.playback.play(audio)

    input_clip = mpe.VideoFileClip('input/udemy_sample_01.mp4')
    new_audio = mpe.AudioFileClip('output/udemy_sample_01.mp3')
    # new_audio = mpe.CompositeAudioClip([input_clip.audio, new_audio])
    final_clip = input_clip.set_audio(new_audio)
    final_clip.write_videofile("output/udemy_sample_01.mp4")

