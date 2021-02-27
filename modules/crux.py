from google.cloud import bigquery


def query_device_distribution(collector, GSA_CREDENTIALS, ORIGIN_URL):

  print('COLLECT: device distribution')
  client = bigquery.Client(credentials=GSA_CREDENTIALS, project=GSA_CREDENTIALS.project_id)
  query_job = client.query(
    f"""
    SELECT
    form_factor.name AS Device,
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

  # each query results row comes as a tuple and has following order: Device | Percentage
  query_results = query_job.result()
  output = dict()

  for row in query_results:
    output[row[0]] = row[1]
  
  collector.collection['device_distribution'] = output
