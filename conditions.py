from zacoby.exceptions import ElementDoesNotExist
from zacoby.utils.decorators import require_DRIVER


@require_DRIVER
def element_located(driver, selector, name):
    try:
        element = driver.manager.get_element_by(name, selector)
    except AttributeError:
        raise ElementDoesNotExist()
    return element


@require_DRIVER
def element_visibility(driver, selector):
    try:
        element = driver.manager.get_element_by(selector)
    except AttributeError:
        raise ElementDoesNotExist()
    return element if element.is_visible else False


@require_DRIVER
def element_text_contains(driver, selector: str, text: str):
    try:
        element = driver.manager.get_element_by(selector)
    except AttributeError:
        raise ElementDoesNotExist()
    return text in element.text


@require_DRIVER
def element_is_clickable(driver, selector: str):
    is_visible = element_visibility(selector=selector)
    try:
        element = driver.manager.get_element_by(selector)
    except ElementDoesNotExist:
        raise
    if is_visible:
        return element.is_enabled
    return False


@require_DRIVER
def element_is_stale(driver, selector: str) -> bool:
    try:
        element = driver.manager.get_element_by(selector)
    except AttributeError:
        raise ElementDoesNotExist()
    return element.is_enabled
 

@require_DRIVER
def title_matches(driver, title: str) -> bool:
    return driver.manager.title == title


@require_DRIVER
def url_contains(driver, url: str) -> bool:
    return url in driver.manager.current_url


@require_DRIVER
def url_matches(driver, url: str) -> bool:
    return url == driver.manager.current_url


@require_DRIVER
def number_of_windows_matches(driver, n: int) -> bool:
    return len(driver.manager.window_handles) == n


@require_DRIVER
def new_window_opened(driver, handles) -> bool:
    return len(driver.manager.window_handles) > len(handles)
