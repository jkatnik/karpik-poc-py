#!/usr/bin/python3

import boto3
import moviepy.editor as mpe
from botocore.exceptions import ClientError
import time
import urllib.request


def upload_file_to_s3(config):
    s3 = boto3.client('s3')

    try:
        s3.head_bucket(Bucket=config['s3-bucket-name'])
    except ClientError:
        s3.create_bucket(Bucket=config['s3-bucket-name'], CreateBucketConfiguration={
            'LocationConstraint': 'eu-west-1'
        })

    s3.upload_file(config['audio_track_file_name'], config['s3-bucket-name'], config['audio_track_file_name'])


def extract_audio_track(config):
    clip = mpe.VideoFileClip(config['input_file_name'])
    clip.audio.write_audiofile(config['audio_track_file_name'])

def transcribe(config):
    transcribe = boto3.client('transcribe')
    job_name = config['audio_track_file_name']
    s3_uri = f"s3://{config['s3-bucket-name']}/{config['audio_track_file_name']}"

    job_uri = s3_uri
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-GB',
        Subtitles={'Formats': ['srt']}
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    # {'TranscriptionJob': {'TranscriptionJobName': 'ultimate_roman_empire_ep1.mp3', 'TranscriptionJobStatus': 'COMPLETED', 'LanguageCode': 'en-GB', 'MediaSampleRateHertz': 44100, 'MediaFormat': 'mp3', 'Media': {'MediaFileUri': 's3://karpik/ultimate_roman_empire_ep1.mp3'}, 'Transcript': {'TranscriptFileUri': 'https://s3.eu-west-1.amazonaws.com/aws-transcribe-eu-west-1-prod/581698133795/ultimate_roman_empire_ep1.mp3/daf19665-8141-4352-84d8-b3fac6ca7ce1/asrOutput.json?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEOv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCWV1LXdlc3QtMSJGMEQCIHG4%2BfOJyVnfluulBGp4JcWAnXFaWFrtC3qzFLmzjukTAiAB5qoJkuFJvrc9Ab7XuJ6PoPqOOPxJaQZr12PATNna8yqDBAjU%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAIaDDU4NzAxNzY2MzQxNyIMbIPlFivuN1q07SxcKtcDGt%2FUvXzNRnSeD0Hoa2tCyXs6COdrJ%2FQ4ZuCD5A3mtOiNoH2tCwdm5%2BgU8sp0OiQ7cqbId0IYC608VKIXac23wVyQLZk%2FuuGDCtBnXh5cTmGNkleTOgOsw5LFg7yLlA8PbsyeN4sjYC%2FsVzqzTx0I54ivznUmWmsqV0PJ94JQgarMxn4Vwsbj9eh8cIzAy%2FnWViv6pIvq7C6ABELMQ9e8%2FIDBQDJNd1op8ej8SQhKDQxxo9Hu0VNIkbpLEqGeXiBidh41TTJm4ZClWNkw22BVJN8kq54bPIac7%2BuJ%2BhXLLqH1DnUWyuEVq%2BRqA94hfv8JDAuE5PQe2hpbKB85cujoqqHs9SmOR0ZYKzlPWnx1AJfcKcKXogISqLjH4c96hVQ28oekCqRJso52evs3b7er56KH1cNXPEzFC17RyCRjbj%2FK9ki9wDkxaldaT1PBMRQLILaIRIlOpuVYoPFwGk93GcIEg0FpnCo4aiE92gMgEZUv3FCThnUdQy9kCKOlxrrG9GFJLAELvT4KVwRVXOExN26R%2F1EJYaAIaesOs2%2B27siy8u3HLnELY7346UkzUsM%2FAdLiMpyPiI%2F0XKQ8QQqIDdaGTzjAUydP%2BxY%2B3JHc3aYkzVZyOEqtMJua%2FI0GOqYB58VyqZ9qQf5o3CEekUzuoYCNKXh7rg9CntbmH59Es5X2hmZbwMEtsFWXTV5uWP8dfrjsMT93q3bKfoYNi8%2FPhuohhBo8w%2BWthmRbN5knFd6A6CabOmeN%2B3%2BKVXT9iDX3EqLkrpWhSbA4JOy2pcfjjJSFI1GLnlNEnipQKDO%2B0br2aCrBedf%2FIQpgOr6CQVYcv6fgAN4oaX1%2Fv%2F8HQfr0UWglhyqyXg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20211219T113329Z&X-Amz-SignedHeaders=host&X-Amz-Expires=899&X-Amz-Credential=ASIAYRLH2WO4QXEJZEGX%2F20211219%2Feu-west-1%2Fs3%2Faws4_request&X-Amz-Signature=c85a1a3024d48b24464b16bc5db61d515df397dc1173c0e5561c8344b97869c3'}, 'StartTime': datetime.datetime(2021, 12, 19, 12, 33, 3, 405000, tzinfo=tzlocal()), 'CreationTime': datetime.datetime(2021, 12, 19, 12, 33, 3, 382000, tzinfo=tzlocal()), 'CompletionTime': datetime.datetime(2021, 12, 19, 12, 33, 24, 351000, tzinfo=tzlocal()), 'Settings': {'ChannelIdentification': False, 'ShowAlternatives': False}, 'Subtitles': {'Formats': ['srt'], 'SubtitleFileUris': ['https://s3.eu-west-1.amazonaws.com/aws-transcribe-eu-west-1-prod/581698133795/ultimate_roman_empire_ep1.mp3/daf19665-8141-4352-84d8-b3fac6ca7ce1/srtSubtitles.srt?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEOv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCWV1LXdlc3QtMSJGMEQCIHG4%2BfOJyVnfluulBGp4JcWAnXFaWFrtC3qzFLmzjukTAiAB5qoJkuFJvrc9Ab7XuJ6PoPqOOPxJaQZr12PATNna8yqDBAjU%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAIaDDU4NzAxNzY2MzQxNyIMbIPlFivuN1q07SxcKtcDGt%2FUvXzNRnSeD0Hoa2tCyXs6COdrJ%2FQ4ZuCD5A3mtOiNoH2tCwdm5%2BgU8sp0OiQ7cqbId0IYC608VKIXac23wVyQLZk%2FuuGDCtBnXh5cTmGNkleTOgOsw5LFg7yLlA8PbsyeN4sjYC%2FsVzqzTx0I54ivznUmWmsqV0PJ94JQgarMxn4Vwsbj9eh8cIzAy%2FnWViv6pIvq7C6ABELMQ9e8%2FIDBQDJNd1op8ej8SQhKDQxxo9Hu0VNIkbpLEqGeXiBidh41TTJm4ZClWNkw22BVJN8kq54bPIac7%2BuJ%2BhXLLqH1DnUWyuEVq%2BRqA94hfv8JDAuE5PQe2hpbKB85cujoqqHs9SmOR0ZYKzlPWnx1AJfcKcKXogISqLjH4c96hVQ28oekCqRJso52evs3b7er56KH1cNXPEzFC17RyCRjbj%2FK9ki9wDkxaldaT1PBMRQLILaIRIlOpuVYoPFwGk93GcIEg0FpnCo4aiE92gMgEZUv3FCThnUdQy9kCKOlxrrG9GFJLAELvT4KVwRVXOExN26R%2F1EJYaAIaesOs2%2B27siy8u3HLnELY7346UkzUsM%2FAdLiMpyPiI%2F0XKQ8QQqIDdaGTzjAUydP%2BxY%2B3JHc3aYkzVZyOEqtMJua%2FI0GOqYB58VyqZ9qQf5o3CEekUzuoYCNKXh7rg9CntbmH59Es5X2hmZbwMEtsFWXTV5uWP8dfrjsMT93q3bKfoYNi8%2FPhuohhBo8w%2BWthmRbN5knFd6A6CabOmeN%2B3%2BKVXT9iDX3EqLkrpWhSbA4JOy2pcfjjJSFI1GLnlNEnipQKDO%2B0br2aCrBedf%2FIQpgOr6CQVYcv6fgAN4oaX1%2Fv%2F8HQfr0UWglhyqyXg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20211219T113329Z&X-Amz-SignedHeaders=host&X-Amz-Expires=900&X-Amz-Credential=ASIAYRLH2WO4QXEJZEGX%2F20211219%2Feu-west-1%2Fs3%2Faws4_request&X-Amz-Signature=83ad5e7c3059e0244f532e9f6326ae1456ee5c1fc14873acbb9d30119f6753d5']}}, 'ResponseMetadata': {'RequestId': '5f77eaf7-a5e9-4160-9ef8-0a1b6cbfa1a7', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/x-amz-json-1.1', 'date': 'Sun, 19 Dec 2021 11:33:29 GMT', 'x-amzn-requestid': '5f77eaf7-a5e9-4160-9ef8-0a1b6cbfa1a7', 'content-length': '3740', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}
    subtitles_url = status['TranscriptionJob']['Subtitles']['SubtitleFileUris'][0]

    print(f"URL: {subtitles_url}")

    with urllib.request.urlopen(subtitles_url) as response, open(config['subtitles_file'], 'wb') as out_file:
        data = response.read()
        out_file.write(data)

    transcribe.delete_transcription_job(
        TranscriptionJobName=job_name
    )


if __name__ == '__main__':
    config = {
        'input_file_name':  'ultimate_roman_empire_ep1.mp4',
        'audio_track_file_name': 'ultimate_roman_empire_ep1.mp3',
        'subtitles_file': 'ultimate_roman_empire_ep1_en.srt',
        's3-bucket-name': 'karpik'
    }

    extract_audio_track(config)
    upload_file_to_s3(config)
    transcribe(config)



