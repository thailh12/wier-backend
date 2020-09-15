from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

####################### for window
try:
	default_driver_path = ChromeDriverManager().install()
except:
	default_driver_path = None

####################### for ubuntu
#!apt-get update
#!apt install chromium-chromedriver
#!cp /usr/lib/chromium-browser/chromedriver /usr/bin
#import sys
#sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
#default_driver_path = "chromedriver"

def get_webdriver(driver_path = default_driver_path):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('window-size=1366x768')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	wd = webdriver.Chrome(driver_path,options=chrome_options)
	return wd