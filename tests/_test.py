from zacoby.driver import Zacoby
from zacoby.conditions import element_located

def callback(remote_connection):
    pass


driver = Zacoby('D:\\utils\\msedgedriver.exe')
# driver.get('http://example.com')
# element = driver.manager.get_element_by_tag_name('name')
instance = driver.wait('element').until(element_located, selector='selector', name='name')
# element.click()
# remote = driver.quit(callback=callback)
