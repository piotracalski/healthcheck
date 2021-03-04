from google.oauth2 import service_account
import sys

from modules import common
from modules import crux
from modules import psi
from modules import accessibility


CONFIG = common.get_data_from_json('./config.json')

GSA_CREDENTIALS = service_account.Credentials.from_service_account_file(
  CONFIG['gsaCredentialsPath'],
  scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

PSI_API_KEY = common.get_data_from_json(CONFIG['psiApiKeyPath'])['API_KEY']

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
    return psi.get_lighthouse_results(samples, ORIGIN_URL, PSI_API_KEY, CONFIG['psiApiRequestInterval'])


class Accessibility():
  def visit(self, samples):
    return accessibility.get_violations_number(samples, ORIGIN_URL, CONFIG['accessibilityStandardTags'])


if __name__ == "__main__":

  print(ORIGIN_URL)

  collector = SampleCollector()

  contexts = [
    DeviceDistribution(),
    LighthouseScores(),
    Accessibility()
  ]

  for context in contexts:
    collector.accept(context)

  print(collector.collection)