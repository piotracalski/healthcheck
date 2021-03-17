from selenium import webdriver
from axe_selenium_python import Axe
from pyvirtualdisplay import Display


def find_rule(violated_rules, tags):
  for rule in violated_rules:
    if rule in tags: return rule


def get_violations_number(collector, url, tags, browser):

  display = Display()
  display.start()
  user_browser = browser.lower().capitalize()

  print('COLLECT: number of accessibility violations')
  print(f'Browser: {user_browser}')

  if user_browser == 'Firefox':
    driver = webdriver.Firefox()

  elif user_browser == 'Chrome':
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(executable_path=r'/usr/local/bin/chromedriver', options=options)

  else:
    print('Wrong browser. Currently supported browsers: Chrome, Firefox')

  driver.set_window_size(1400, 900)

  issues = dict()

  try:
    driver.get(url)
    axe = Axe(driver)
    axe.inject()
    results = axe.run()
    driver.close()
    display.stop()

  except Exception as error:
    issues = {
      'error': str(error).replace('\n', '')
    }

  else:
    violations = list()
    count = 0

    for violation in results['violations']:
      if any(tag in violation['tags'] for tag in tags):

        rule = find_rule(violation['tags'], tags)

        count += 1
        violations.append({
          'description': violation['description'],
          'impact': violation['impact'],
          'rule': rule
        })
    
    issues = {
      'browser': user_browser,
      'violationsCount': count,
      'violations': violations
    }

  finally:
    collector.collection['accessibilityIssues'] = issues