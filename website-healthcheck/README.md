# Website Healthcheck
Description: **Website Healthcheck** is an automated tool that gathers data about given URL.<br>
Current checks:
- Lighthouse score for mobiles and desktop - PageSpeedInsights API
- Core Web Vitals for mobiles and desktop - PageSpeedInsights API (CrUX data)
- Users' device distribution - BigQuery (CrUX data)
- Accessibility standards' violations (AXE + Firefox)

## Prerequisites
### Docker
Docker version 20.10.2, build 2291f61

### Google service account credentials
To authenticate BigQuery request *Google service account credentials* are needed. Their default path is: *root/credentials/gsa.json*.<br>
For more info, please visit: https://cloud.google.com/docs/authentication/production
*Prerequisites:* you have Google acocunt. **You don't need Google Cloud Platform trial activated!!**
1. Go to https://console.cloud.google.com/apis/credentials
1. Click Add Credentials > Service Account
1. Create a new service account (you can use default My First Project for this):
  1. Fill in Name and Description in step 1
  1. In step 2 select role **Big Query > Big Query Admin**
  1. Skip step 3
  1. Click Done
1. You're back in Credentials view https://console.cloud.google.com/apis/credentials
1. Find your service account in list and click Edit
1. Go to Keys tab
1. Click Add Key > Create New Key > JSON
1. Save this JSON locally in (root-project-dir)/credentials/gsa.json file
1. Now you have GSA credentials!

### PageSpeedInsights API key
To avoid request rate limiting *key* parameter is added to each request. By default, key string value should be placed in: *root/credentials/psi.json* under *API_KEY* key.<br>
For more info, please visit: https://developers.google.com/speed/docs/insights/v5/get-started?pli=1
1. Go to https://developers.google.com/speed/docs/insights/v5/get-started?pli=1#APIKey
1. Click "Get a Key"
1. Save the key in (root-project-dir)/credentials/psi.json file:
```
{
    "API_KEY": "your-key-here"
}
```

### Configuration
Currently all configuration variables are located in *root/config.json*.<br>
Default configuration:
```
{
  "accessibilityStandardTags": ["wcag2a", "wcag2aa", "wcag21aa"],
  "psiApiRequestInterval": 5,
  "gsaCredentialsPath": "./credentials/gsa.json",
  "psiApiKeyPath": "./credentials/psi.json"
}
```

## Executing the script
From the root folder:
Build docker image from Dockerfile
```
docker build -t website-healthcheck .
```
Run image as a container, execute script and save results
```
docker run -t -e url="<TESTED_URL>" -v ${PWD}:/website-healthcheck website-healthcheck
```

## Output
Currently results are saved to *root/output.json* file.

## Todos
- [ ] switch default browser do Chrome
- [ ] implement proper error handling

## Post MVP improvements:
- [ ] parametrize test module usage (e.g. run only accessibility check; all by default)
- [ ] parametrize browser choice
- [ ] present results in an user-readable way
- [ ] set date (from) as a parameter in crux module