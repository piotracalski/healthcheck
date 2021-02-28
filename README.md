# Website Healthcheck
Description: TBD

## Prerequisites

### Python
At the time of developing this script my version of Python was: 3.7.4

### Google service account credentials
To authenticate BigQuery request *Google service account credentials* are needed. Their default path is: *root/credentials/gsa.json*.<br>
For more info, please visit: https://cloud.google.com/docs/authentication/production

### PageSpeedInsights API key
To avoid request rate limiting *key* parameter is added to each request. By default, key string value should be placed in: *root/credentials/psi.json* under *API_KEY* key.<br>
For more info, please visit: https://developers.google.com/speed/docs/insights/v5/get-started?pli=1

## Executing the script
```
pip install -r requirements.txt
python .\main.py '{ORIGIN_URL}'
```

## Output
TBD