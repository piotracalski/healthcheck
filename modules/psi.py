import requests
import json
import time
import os

from dotenv import load_dotenv

load_dotenv()
REQUEST_INTERVAL = int(os.getenv('PSI_API_REQUEST_INTERVAL', 5))


def get_lighthouse_score(url, device, key):
  print(f'TASK: get Lighthouse score for {device}')
  psi_data = requests.get(f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy={device.upper()}&key={key}')
  print(f'INFO: PSI API response code: {psi_data.status_code}')
  # below if statement can be deleted after implementing proper error handling
  if psi_data.status_code == 429:
    print(json.loads(psi_data.content))
  score = json.loads(psi_data.content)['lighthouseResult']['categories']['performance']['score']
  return int(float(score) * 100)


def get_lighthouse_scores(collector, url, PSI_API_KEY):

  print('COLLECT: Lighthouse scores')
  devices = ['desktop', 'mobile']
  output = dict()

  for device in devices:
    score = get_lighthouse_score(url, device, PSI_API_KEY)
    print(f'INFO: LH score for {device}: {score}')
    output[device] = score

    if devices.index(device) < len(devices) - 1:
      print(f'TASK: request interval: {REQUEST_INTERVAL} seconds')
      time.sleep(REQUEST_INTERVAL)

  
  collector.collection['lighthouse_scores'] = output