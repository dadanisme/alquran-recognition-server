import requests
import json

start = 1
end = 114 + 1

file_name = 'ayat_details.json'

# clear test.json
with open(file_name, 'w') as f:
  f.write('[')
f.close()


# get data
for i in range(start, end):
  print('Processing surah: ' + str(i))
  r = requests.get('https://equran.id/api/surat/' + str(i))
  data = json.loads(r.text)

  # get ayat details
  for ayat in data['ayat']:
    index = ayat['id']
    identifier = str(ayat['surah']) + ':' + str(ayat['nomor'])
    print('Processing ayat: ' + identifier)
    ar = ayat['ar']
    idn = ayat['idn']

    # from setup import translate_text # too much consuming api
    # translated = translate_text('id', ar)
    ayat_details = {
      'index': index,
      'identifier': identifier,
      'ar': ar,
      'idn': idn,
      # 'translated': translated['translatedText']
    }

    # save to file
    with open(file_name, 'a') as f:
      json.dump(ayat_details, f)
      f.write(',\n')
    f.close()

# close with ]
with open(file_name, 'a') as f:
  f.write(']')
