import requests
import json

start = 69
end = 114  + 1


error_count = 0
# get data
for i in range(start, end):
  # create i.json
  file_name = 'train/' + str(i) + '.json'

  with open(file_name, 'w') as f:
    f.write('[')
  f.close()

  # start processing
  print('----------------------')
  print('Processing surah: ' + str(i))
  r = requests.get('https://equran.id/api/surat/' + str(i))
  data = json.loads(r.text)

  # get ayat details
  total = 6236
  for ayat in data['ayat']:
    index = ayat['id']
    identifier = str(ayat['surah']) + ':' + str(ayat['nomor'])
    print(str(index) + ' of ' + str(total))
    print('Processing ayat: ' + identifier)
    
    ayat_url = 'https://api.alquran.cloud/v1/ayah/' + identifier
    r = requests.get(ayat_url)
    ayat_data = json.loads(r.text)
    ar = ayat_data['data']['text']
    idn = ayat['idn']

    # import module from parent directory
    from setup import translate_text
    translated = translate_text('id', ar)['translatedText']

    if(identifier.split(':')[1] == '1'):
      translated = translated.replace('Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang ', '')

    import re
    if re.search(r'[\u0600-\u06FF]', translated):
      print('problem on translating, still contains arabic')  
      error_count += 1
    else:
      print('translated successfully, does not contain arabic')
    print('job ' + str(index) + ' done\n')

    ayat_details = {
      'index': index,
      'identifier': identifier,
      'translated': translated,
      'idn': idn,
      'ar': ar
    }

    # save to file
    with open(file_name, 'a') as f:
      json.dump(ayat_details, f)
      f.write(',\n')
    f.close()

  # close with ]
  with open(file_name, 'a') as f:
    f.write(']')

  print('total_error: ' + str(error_count))
  print('----------------------')
  print('\n')