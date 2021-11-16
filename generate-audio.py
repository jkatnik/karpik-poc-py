#!/usr/bin/python3

# Links:
# - https://docs.aws.amazon.com/polly/latest/dg/get-started-what-next.html
# - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html
# - https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html

# scloud account login s24-playground AdminAccess --write


import boto3
polly_client = boto3.Session().client('polly')

sentence = '''
<speak>
     <prosody amazon:max-duration="10s">
          Amazon Polly is a web service that makes it easy to synthesize speech from text.
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

file = open('output/speech-standard.mp3', 'wb')
file.write(response['AudioStream'].read())
file.close()
