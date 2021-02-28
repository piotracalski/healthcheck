import requests
import json
import time

from dotenv import load_dotenv

load_dotenv()

# URL = 'https://www.ford.co.uk'


def get_lighthouse_score(url, device):
  print(f'TASK: get Lighthouse score for {device}')
  psi_data = requests.get(f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy={device.upper()}&key=AIzaSyBjE1dkOwQjS9hBsh4BwBBXIIHDOeePnJY')
  print(f'INFO: PSI API response code: {psi_data.status_code}')
  if psi_data.status_code == 429:
    print(json.loads(psi_data.content))
  score = json.loads(psi_data.content)['lighthouseResult']['categories']['performance']['score']
  return int(float(score) * 100)


def get_lighthouse_scores(collector, url):

  print('COLLECT: Lighthouse scores')
  devices = ['desktop', 'mobile']
  output = dict()

  for device in devices:
    score = get_lighthouse_score(url, device)
    print(f'INFO: LH score for {device}: {score}')
    output[device] = score
    if devices.index(device) < len(devices) - 1:
      print('TASK: request interval: 5 seconds')
      time.sleep(5)

  
  collector.collection['lighthouse_scores'] = output