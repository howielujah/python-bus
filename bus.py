import requests
import json

response = requests.get(
    'https://tcgbusfs.blob.core.windows.net/blobbus/GetEstiamteTime.json')
print(response.status_code)
if response.status_code == requests.codes.ok:
    print("OK")
    data = response.json()
    filename = f'{data["EssentialInfo"]["UpdateTime"]}.json'.replace(':', '')
    print(f'filename = {filename}')
    with open(f'{filename}', 'w') as f:
        json.dump(data, f)
