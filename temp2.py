import os

# set environment variable for google cloud platform
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/alquranrecognition/alquran/google-credentials.json"

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
	return result

def transcribe_file(speech_file):
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

	# get sample rate
	import scipy
	from scipy.io import wavfile
	sample_rate, data = wavfile.read(speech_file)

	config = speech.RecognitionConfig(
		encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
		sample_rate_hertz=sample_rate,
		language_code="ar",
		audio_channel_count=2,
	)

	operation = client.long_running_recognize(config=config, audio=audio)

	response = operation.result(timeout=300)

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

	# delete file after process
	import os
	os.remove(speech_file)
	return results

def search_in_ayat(text):
	# open ayat_details.json
	import json
	with open('/home/alquranrecognition/alquran/ayat_details.json') as f:
		ayat_details = json.load(f)

	from lunr import lunr
	idx = lunr(ref='index', fields=['idn', 'translated'], documents=ayat_details)
	result = idx.search(text)[0:10]

	response = []
	for r in result:
		print(r['ref'])
		response.append(ayat_details[int(r['ref']) - 1])

	return response
