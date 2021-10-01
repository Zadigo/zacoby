# import time
# from pydispatch import dispatcher

# from zacoby.browsers.list import EdgeBrowser
# from zacoby.events.listeners import before_navigate_to, after_navigate_to
# # from zacoby.events.listeners import EventLissteners
# from zacoby.signals import signal
# from zacoby.conditions import element_located, element_is_clickable, element_is_stale, element_visibility


# @before_navigate_to
# def my_custom_signal(sender, signal, instance):
#     print('My custom signal')


# @after_navigate_to
# def my_other_custom_signal(sender, signal, instance):
#     pass


# # s = EdgeBrowser('D:\\utils\\edge_driver')
# s = EdgeBrowser('D:\\utils\\edge_driver\\msedgedriver.exe')
# # s.register_events(my_custom_signal, my_other_custom_signal)
# s.get('http://example.com')

# # # text = s.text

# element = s.get_element_by_tag_name('a')
# # is_enabled = element.is_enabled
# # is_visible = element.is_visible
# # print(is_enabled)
# print(element.get_attribute('href'))
# element.click()
# s.pause(timeout=3)
# # element.click()

# # tokens = element.tokenized_text()

# # s.wait('name').until(element_visibility)
# # s.wait('paris').until_not(element_is_clickable)
# # s.wait('paris').chains(element_is_clickable, element_is_stale)
# # s.wait('paris').logical_map({'until': element_is_stale, 'until_not': element_visibility})
# # s.back()
# # s.get_element_by_tag_name('a')
# # s.pause()
# # s.forward()

# # soup = s.as_beautiful_soup()
# s.quit()

from zacoby.wait import Wait, Pause

def some_condition(driver, name):
    print(driver, name)

w = Wait('name')
w.logical_map({'until': (some_condition, False), 'until_not': (some_condition, True)})
