# --------------------- ADD CHROME NEW UNDETECTED CHROMEDRIVER ---------------------
from undetected_chromedriver import Chrome, ChromeOptions
options = ChromeOptions()
driver = Chrome(options=options)
import time
time.sleep(1)
# --------------------------------------------------------
# --------------------- ADD GO TO URL https://facebook.com ---------------------
driver.get('https://facebook.com')
import time
time.sleep(1)
# --------------------------------------------------------
# --------------------- ADD SLEEP 10 + random.randint(-2, 2) ---------------------
import time
import random
time.sleep(10 - random.randint(-2, 2))
# --------------------------------------------------------