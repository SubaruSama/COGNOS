import json

with open('/home/r0se/Documents/Programming/Scrapy/cisa_bulletins/cisa_bulletins/outputs/cisa_bulletins.json', 'r') as json_file:
    data = json.load(json_file)

with open('./normalized_json.json', 'w') as normalized_json:
    json.dump(data, normalized_json)

json_file.close()
normalized_json.close()