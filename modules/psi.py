import requests
import json
import time
import os


def refine_labels(label):
  words = label.lower().split('_')
  del words[-1]
  return ''.join(list(map(lambda word: word.capitalize() if words.index(word) != 0 else word, words)))


def get_lighthouse_result(url, device, key):
  print(f'Task: get Lighthouse result for {device}')
  psi_data = requests.get(f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy={device.upper()}&key={key}')
  # print(f'Info: PSI API response code: {psi_data.status_code}')

  # below if statement can be deleted after implementing proper error handling
  if psi_data.status_code == 429:
    print(json.loads(psi_data.content))

  psi_data_json = json.loads(psi_data.content)

  score = psi_data_json['lighthouseResult']['categories']['performance']['score']
  origin_cwv = dict()

  metrics = psi_data_json['originLoadingExperience']['metrics']
  for metric in metrics.keys():
    label = refine_labels(metric)
    value = metrics[metric]['percentile']
    origin_cwv[label] = value if label != 'cumulativeLayoutShift' else int(value) / 100

  return {
    'score': int(float(score) * 100),
    'cwv': origin_cwv
    }


def get_lighthouse_results(collector, url, PSI_API_KEY, interval):

  print('COLLECT: Lighthouse results')
  devices = ['desktop', 'mobile']
  output = dict()

  for device in devices:
    result = get_lighthouse_result(url, device, PSI_API_KEY)
    # print(f'Info: LH score for {device}: {result["score"]}')
    output[device] = result

    if devices.index(device) < len(devices) - 1:
      print(f'Task: request interval: {interval} seconds')
      time.sleep(interval)

  
  collector.collection['lighthouseResults'] = output