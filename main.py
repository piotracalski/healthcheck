from google.cloud import bigquery
from google.oauth2 import service_account

key_path = "./credentials.json"

credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# print(credentials)

def query_device_distribution():
  client = bigquery.Client(credentials=credentials, project=credentials.project_id)
  query_job = client.query(
    """
    SELECT
    form_factor.name AS Device,
    COUNT(form_factor.name) AS CountOf,
    ROUND(COUNT(form_factor.name) / (SELECT
        COUNT(origin)
        FROM `chrome-ux-report.all.202101`
        WHERE origin LIKE '%ford.co.uk'), 2) * 100 AS Percentage

    FROM 
    `chrome-ux-report.all.202101`

    WHERE origin LIKE '%ford.co.uk'

    GROUP BY form_factor.name
    """
  )

  results = query_job.result()


  for row in results:
    print(f'Device: {row[0]} | Count: {row[1]} | Percentage: {row[2]}')


if __name__ == "__main__":
    query_device_distribution()