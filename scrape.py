#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from getpass import getpass
from collections import defaultdict

PHANTOMJS_BIN = './node_modules/phantomjs/bin/phantomjs'
TRITONLINK_URL = 'http://mytritonlink.ucsd.edu/'
USERNAME_NAME = 'urn:mace:ucsd.edu:sso:username'
PASSWORD_NAME = 'urn:mace:ucsd.edu:sso:password'
TIMEOUT = 10
LOGIN_ERROR_CLASS = 'error'
CLASSES_CONTAINER_ID = 'class_schedule'
CLASSES_ELEM = 'td'
CLASSES_CLASS = 'class'
MON = 'Monday'
TUE = 'Tuesday'
WED = 'Wednesday'
THU = 'Thursday'
FRI = 'Friday'
WEEK_DAYS = (MON, TUE, WED, THU, FRI)

# For incorrect login info
class AuthenticationException(Exception):
  pass

# For TritonLink errors
class TritonLinkException(Exception):
  pass

def chunk(l, size):
  return [l[i:i+size] for i in xrange(0, len(l), size)]

def main():
  driver = webdriver.PhantomJS(PHANTOMJS_BIN)
  driver.implicitly_wait(TIMEOUT)

  driver.get(TRITONLINK_URL)

  # Get redirected to login page
  login_url = driver.current_url

  # Get creds
  username = raw_input('User ID / PID: ')
  password = getpass('Password / PAC: ')

  # Send to elements
  e_username = driver.find_element_by_name(USERNAME_NAME)
  e_password = driver.find_element_by_name(PASSWORD_NAME)
  e_username.send_keys(username)
  e_password.send_keys(password)
  e_password.send_keys(Keys.RETURN)

  try:
    WebDriverWait(driver, TIMEOUT).until(
      lambda driver: driver.find_element_by_css_selector("#%s, .%s" %
        (CLASSES_CONTAINER_ID, LOGIN_ERROR_CLASS)
      )
    )

    # Check if logged in
    if driver.current_url == login_url:
      raise AuthenticationException

    bs_mtl = BeautifulSoup(driver.page_source)
  except TimeoutException:
    raise TritonLinkException("Request timed out")
  finally:
    driver.quit()

  # Parse TritonLink

  # Get all class elements by weekday
  try:
    bs_classes_container = bs_mtl.find_all(id=CLASSES_CONTAINER_ID)[0]
  except IndexError:
    raise TritonLinkException("Classes container not found")

  bs_classes = bs_classes_container.find_all(CLASSES_ELEM)
  by_weekday = zip(*chunk(bs_classes, len(WEEK_DAYS)))

  # Proccess each td
  classes = defaultdict(list)
  for day_name, day in zip(WEEK_DAYS, by_weekday):
    for clazz in day:
      try:
        class_info = clazz.find_all(class_=CLASSES_CLASS)[0]
      # If empty, skip
      except IndexError:
        continue

      class_time, class_name, class_loc = list(class_info.stripped_strings)
      print('%s | %s | %s | %s' %
        (day_name, class_time, class_name, class_loc)
      )

main()
