import requests
import json
import logging
from datetime import date

today = date.today()

# YYmmdd
log_filename = today.strftime("%Y%m%d") + '.log'

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename=f'log/{log_filename}',
                    filemode='w', format=FORMAT)
try:
    response = requests.get(
        'https://tcgbusfs.blob.core.windows.net/blobbus/GetEstiamteTime.json')
    logging.info(response.status_code)
    if response.status_code == requests.codes.ok:
        data = response.json()
        filename = f'{data["EssentialInfo"]["UpdateTime"]}.json'.replace(
            ':', '')
        logging.info(f'filename = {filename}')
        with open(f'{filename}', 'w') as f:
            json.dump(data, f)
except:
    logging.exception('Catch an exception.')
