from selenium import webdriver
from axe_selenium_python import Axe
from pyvirtualdisplay import Display


def find_rule(violated_rules, tags):
  for rule in violated_rules:
    if rule in tags: return rule


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

  count = 0
  violations = list()

  for violation in results['violations']:
    if any(tag in violation['tags'] for tag in tags):

      rule = find_rule(violation['tags'], tags)

      count += 1
      violations.append({
        'description': violation['description'],
        'impact': violation['impact'],
        'rule': rule
      })
  
  collector.collection['accessibilityIssues'] = {
    'violationsCount': count,
    'violations': violations
  }
