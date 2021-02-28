from google.oauth2 import service_account
from dotenv import load_dotenv
import os
import sys
import json

from modules import crux
from modules import psi


def get_data_from_json(path):
  with open(path) as f:
    data = json.load(f)
    return data


load_dotenv()

GSA_CREDENTIALS_PATH = os.getenv('GSA_CREDENTIALS_PATH', './credentials/gsa.json')
PSI_API_KEY_PATH = os.getenv('PSI_API_KEY_PATH', './credentials/psi.json')

GSA_CREDENTIALS = service_account.Credentials.from_service_account_file(
  GSA_CREDENTIALS_PATH,
  scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

PSI_API_KEY = get_data_from_json(PSI_API_KEY_PATH)['API_KEY']

ORIGIN_URL = sys.argv[1]


class SampleCollector:
  def __init__(self):
    self.collection = dict()

  def accept(self, visitor):
    visitor.visit(self)

  def __repr__(self):
    return self.collection


class DeviceDistribution():
  def visit(self, samples):
    return crux.query_device_distribution(samples, ORIGIN_URL, GSA_CREDENTIALS)


class LighthouseScores():
  def visit(self, samples):
    return psi.get_lighthouse_scores(samples, ORIGIN_URL, PSI_API_KEY)


if __name__ == "__main__":

  collector = SampleCollector()

  contexts = [
    DeviceDistribution(),
    LighthouseScores()
  ]

  for context in contexts:
    collector.accept(context)

  print(collector.collection)