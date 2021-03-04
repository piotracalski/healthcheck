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

### PageSpeedInsights API key
To avoid request rate limiting *key* parameter is added to each request. By default, key string value should be placed in: *root/credentials/psi.json* under *API_KEY* key.<br>
For more info, please visit: https://developers.google.com/speed/docs/insights/v5/get-started?pli=1

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
- [x] prepare .dockerignore file
- [x] refine accessibility check response
- [ ] implement proper error handling
- [x] save results to .json file
- [ ] present results in an readable way