from zacoby.browsers.list import EdgeBrowser
from zacoby.conditions import element_is_clickable

spider = EdgeBrowser('')
spider.get('http://example.com')

element = spider.manager.get_element_by_id('google')

spider.wait('a').until(element_is_clickable, selector='a')
element.click()

spider.manager.forward()

def my_callback():
    pass

remote = spider.pause(my_callback)
spider.manager.back()

spider.quit()
