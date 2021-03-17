from google.cloud import bigquery


def query_device_distribution(collector, ORIGIN_URL, GSA_CREDENTIALS):

  print('COLLECT: device distribution')
  client = bigquery.Client(credentials=GSA_CREDENTIALS, project=GSA_CREDENTIALS.project_id)

  output = dict()

  try:
    query_job = client.query(
      f"""
      SELECT
        device AS DEVICE,
        ROUND(((slow_lcp + avg_lcp + fast_lcp) *100 / 1), 0) AS PERCENTAGE

      FROM `chrome-ux-report.materialized.device_summary`

      WHERE date >= '2021-01-01' AND origin = '{ORIGIN_URL}'
      """
    )

    # each query results row comes as a tuple and has following order: Device | Percentage
    query_results = query_job.result()

  except Exception as error:
    output = {
      'error': str(error)
    }


  else:
    number_of_rows = int(query_results.total_rows)

    if number_of_rows > 0:
      for row in query_results:
        output[row[0]] = int(row[1])

    else:
      output = {
        'error': 'no results for given URL'
      }

  finally:
    collector.collection['deviceDistribution'] = output





  
