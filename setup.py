import os
from dotenv import load_dotenv
load_dotenv()

# get api key from .env file
api_key = os.environ.get('ZAMZAR_API_KEY')

# set environment variable for google cloud platform
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./google-credentials.json"

def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result

def transcribe_file(speech_file, sample_rate_hertz=44100):
    """Transcribe the given audio file asynchronously."""
    from google.cloud import speech

    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    """
     Note that transcription is limited to a 60 seconds audio file.
     Use a GCS file for audio longer than 1 minute.
    """
    audio = speech.RecognitionAudio(content=content) 

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=sample_rate_hertz,
        language_code="ar",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.

    results = []

    for result in response.results:
        # The first alternative is the most likely one for this portion.
        # reverse the text to make it readable
        translated = translate_text('id', result.alternatives[0].transcript)
        results.append({
            "transcript": result.alternatives[0].transcript,
            "translated": translated['translatedText'],
            "confidence": result.alternatives[0].confidence
        })
    
    return results
    
def convert_to_flac(source_file):
    import requests
    import time
    from requests.auth import HTTPBasicAuth

    file_format = source_file.split('.')[-1]
    endpoint = "https://sandbox.zamzar.com/v1/jobs"
    target_format = "flac"

    # upload
    file_content = {'source_file': open(source_file, 'rb')}
    data_content = {'target_format': target_format}
    res = requests.post(endpoint, data=data_content, files=file_content, auth=HTTPBasicAuth(api_key, ''))


    # wait for the job to finish
    job_id = res.json()['id']
    while True:
        endpoint = "https://sandbox.zamzar.com/v1/jobs/{}".format(job_id)
        response = requests.get(endpoint, auth=HTTPBasicAuth(api_key, ''))
        if response.json()['status'] == 'successful':
            break
        time.sleep(1)


    # get data
    job_id = res.json()['id']
    endpoint = "https://sandbox.zamzar.com/v1/jobs/{}".format(job_id)
    response = requests.get(endpoint, auth=HTTPBasicAuth(api_key, ''))

    # download data
    file_id = response.json()['target_files'][0]['id']
    local_filename = source_file.replace('.' + file_format, '.flac')
    endpoint = "https://sandbox.zamzar.com/v1/files/{}/content".format(file_id)
    response = requests.get(endpoint, auth=HTTPBasicAuth(api_key, ''))

    # save as flac
    with open(local_filename, 'wb') as f:
        f.write(response.content)
        f.close()

    # get sample rate depending on the file format
    if file_format == 'wav':
        sample_rate_hertz = 48000
    elif file_format == 'mp3':
        sample_rate_hertz = 44100
    elif file_format == 'ogg':
        sample_rate_hertz = 48000
    elif file_format == 'flac':
        sample_rate_hertz = 48000

    return {
        "status": "success",
        "filename": local_filename,
        "sample_rate_hertz": sample_rate_hertz
    }
