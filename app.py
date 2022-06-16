from setup import *

audio_file = "./audio/test_audio5.ogg"
flac_file = convert_to_flac(audio_file)

result = transcribe_file(flac_file['filename'], flac_file['sample_rate_hertz'])
print(result)