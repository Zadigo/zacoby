from conditions import element_is_stale, element_visibility
from page.pipeline import EndIf
from zacoby.driver import Zacoby
from zacoby.conditions import title_matches
from zacoby.page.pipeline import GoToIf

z = Zacoby('D:\\utils\\msedgedriver.exe')
z.get('http://example.com')
element = z.manager.get_element_by_id('name')
z.run_sequence(EndIf('page__find_element_by_tag__a'))
element.click()
z.quit()
