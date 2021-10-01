from conditions import element_is_stale, element_visibility
from zacoby.driver import Zacoby
from zacoby.conditions import title_matches

z = Zacoby('D:\\utils\\msedgedriver.exe')
z.get('http://example.com')
element = z.manager.get_element_by('id', 'Kendall')

element.click()
z.quit()
