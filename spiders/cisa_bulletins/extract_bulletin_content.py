from dataclasses import dataclass
import json

# script para ler e escrever num arquivo de texto o conteudo com o json normalizado
# depois subir para o doccano

with open('normalized_json.json', 'r') as bulletin_content:
    data = json.load(bulletin_content)
    bulletin_content.close()

file_to_write = open('bulletins_sb22-080__sb22-073__sb22-066.txt', 'a')

for content in data:
    file_to_write.write('Primary Vendor - Product: {primary_vendor}\n'.format(primary_vendor=content['Primary Vendor -- Product'][0]))
    file_to_write.write('Descritption: {description}\n'.format(description=content['Descritption'][0]))
    file_to_write.write('Date publshed: {date}\n'.format(date=content['Date published'][0]))
    file_to_write.write('CVSS: {cvss}\n'.format(cvss=content['CVSS Score'][0]))
    file_to_write.write('Information: {info}\n'.format(info=content['Source and Patch info'][0]))
    file_to_write.write('='*75)
    file_to_write.write('\n')
