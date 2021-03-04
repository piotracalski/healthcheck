from selenium import webdriver
from axe_selenium_python import Axe
from pyvirtualdisplay import Display


def get_violations_number(collector, ORIGIN_URL, tags):
  display = Display()
  display.start()  

  print('COLLECT: number of accessibility violations')

  driver = webdriver.Firefox()
  driver.set_window_size(1400, 900)
  driver.get(ORIGIN_URL)
  axe = Axe(driver)
  axe.inject()
  results = axe.run()
  driver.close()
  display.stop()

  violations = 0

  for violation in results['violations']:
    if any(tag in violation['tags'] for tag in tags):
      violations += 1
      print(f'Violation: {violation["description"]}, Impact: {violation["impact"]}, Rules: {violation["tags"]}')
  
  collector.collection['accessibility_issues_number'] = violations
