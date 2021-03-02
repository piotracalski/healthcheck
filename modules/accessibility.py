from selenium import webdriver
from axe_selenium_python import Axe


def get_violations_number(collector, ORIGIN_URL, tags, driver_path):

  print('COLLECT: number of accessibility violations')

  driver = webdriver.Firefox(executable_path=driver_path)
  driver.get(ORIGIN_URL)
  axe = Axe(driver)
  axe.inject()
  results = axe.run()
  driver.close()

  violations = 0

  for violation in results['violations']:
    if any(tag in violation['tags'] for tag in tags):
      violations += 1
      print(f'Violation: {violation["description"]}')
  
  collector.collection['accessibility_issues_number'] = violations
