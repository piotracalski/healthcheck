from google.oauth2 import service_account
from dotenv import load_dotenv
import os
import sys

from modules import crux

load_dotenv()

GSA_CREDENTIALS_PATH = os.getenv('GSA_CREDENTIALS_PATH', './credentials.json')

GSA_CREDENTIALS = service_account.Credentials.from_service_account_file(
    GSA_CREDENTIALS_PATH,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# ORIGIN_URL = '%ford.co.uk'
ORIGIN_URL = sys.argv[1]

class SampleCollector:
  def __init__(self):
    self.collection = dict()

  def accept(self, visitor):
    visitor.visit(self)
    # self.collection[visitor.sample_name()] = visitor.visit(self)

  def __repr__(self):
    return self.collection


# class Sample():
#   def sample_name(self):
#     return self.__class__.__name__


# class DeviceDistribution(Sample):
class DeviceDistribution():
  def visit(self, samples):
    return crux.query_device_distribution(samples, GSA_CREDENTIALS, ORIGIN_URL)



if __name__ == "__main__":

  collector = SampleCollector()

  contexts = [
    DeviceDistribution()
  ]

  for context in contexts:
    collector.accept(context)

  print(collector.collection)