from zacoby.exceptions import ElementDoesNotExist


def element_located(selector):
    def wrapper(driver, name):
        try:
            element = driver.get_element_by(name, selector)
        except ElementDoesNotExist:
            raise
        else:
            return element
    return wrapper


def title_matches(driver, title):
    return driver.title == title
