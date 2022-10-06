import json

start = 1
end = 114 + 1

error_count = 0
complete_data = []

for surat in range(start, end):
  # open surat.json as read
  file_name = 'train/' + str(surat) + '.json'
  with open(file_name, 'r') as f:
    data = json.load(f)
  
  print('processing: ' + str(surat) + ' of ' + str(end - 1))
  complete_data += data

# write to train.json
with open('train.json', 'w') as f:
  json.dump(complete_data, f)
  print('train.json written')
