import requests
import json

start = 1
end = 114 + 1

file_name = "surah_details.json"

# clear test.json
with open(file_name, 'w') as f:
  f.write('[')
f.close()

for i in range(start, end):
  print("Processing surah: " + str(i))
  r = requests.get('https://equran.id/api/surat/' + str(i))
  data = json.loads(r.text)

  # get surah details
  nomor = data['nomor']
  nama = data['nama']
  nama_latin = data['nama_latin']
  jumlah_ayat = data['jumlah_ayat']
  arti = data['arti']
  deskripsi = data['deskripsi']
  audio = data['audio']

  surah_details = {
    "nomor": nomor,
    "nama": nama,
    "nama_latin": nama_latin,
    "jumlah_ayat": jumlah_ayat,
    "arti": arti,
    "deskripsi": deskripsi,
    "audio": audio
  }

  print(surah_details)
    
  # save to file
  with open(file_name, 'a') as f:
    json.dump(surah_details, f)
    if(i != end - 1):
      f.write(',\n')
  f.close()

# close with ]
with open(file_name, 'a') as f:
  f.write(']')

