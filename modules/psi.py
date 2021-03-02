import requests
import json
import time
import os


def get_lighthouse_score(url, device, key):
  print(f'Task: get Lighthouse score for {device}')
  psi_data = requests.get(f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy={device.upper()}&key={key}')
  print(f'Info: PSI API response code: {psi_data.status_code}')
  # below if statement can be deleted after implementing proper error handling
  if psi_data.status_code == 429:
    print(json.loads(psi_data.content))
  score = json.loads(psi_data.content)['lighthouseResult']['categories']['performance']['score']
  return int(float(score) * 100)


def get_lighthouse_scores(collector, url, PSI_API_KEY, interval):

  print('COLLECT: Lighthouse scores')
  devices = ['desktop', 'mobile']
  output = dict()

  for device in devices:
    score = get_lighthouse_score(url, device, PSI_API_KEY)
    print(f'Info: LH score for {device}: {score}')
    output[device] = score

    if devices.index(device) < len(devices) - 1:
      print(f'Task: request interval: {interval} seconds')
      time.sleep(interval)

  
  collector.collection['lighthouse_scores'] = output