from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv
import os

load_dotenv()

GSA_CREDENTIALS_PATH = os.getenv('GSA_CREDENTIALS_PATH', './credentials.json')

GSA_CREDENTIALS = service_account.Credentials.from_service_account_file(
    GSA_CREDENTIALS_PATH,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

ORIGIN_URL = '%ford.co.uk'

class WebsiteHealthcheckWorker:
  def __init__(self):
    self.harvest = []
    
  def query_device_distribution(self):
    client = bigquery.Client(credentials=GSA_CREDENTIALS, project=GSA_CREDENTIALS.project_id)
    query_job = client.query(
      f"""
      SELECT
      form_factor.name AS Device,
      COUNT(form_factor.name) AS CountOf,
      ROUND(COUNT(form_factor.name) / (SELECT
          COUNT(origin)
          FROM `chrome-ux-report.all.202101`
          WHERE origin LIKE '{ORIGIN_URL}'), 2) * 100 AS Percentage

      FROM 
      `chrome-ux-report.all.202101`

      WHERE origin LIKE '{ORIGIN_URL}'

      GROUP BY form_factor.name
      """
    )

    results = query_job.result()


    for row in results:
      print(f'Device: {row[0]} | Count: {row[1]} | Percentage: {row[2]}')


if __name__ == "__main__":
  worker = WebsiteHealthcheckWorker()
  worker.query_device_distribution()