import time
from functools import wraps

import pandas


def normalize(func):
    def clean():
        return []
    return clean


def to_pandas(func):
    def create_dataframe():
        return pandas.DataFrame(func())
    return create_dataframe()


def history(func):
    def wrapper():
        return []
    return wraps(wrapper, func)


@to_pandas
@normalize
def table(driver):
    dataset_columns = []
    table = driver.find_element_by_tag('tbody')
    if table is not None:
        rows = driver.find_element_by_tag('tr', multiple=True)

        for row in rows:
            columns = row.find_element_by_tag('td', multiple=True)
            for column in columns:
                dataset_columns.append(column.text)
    return dataset_columns


@history
def follow_links(driver, links:list, s=2):
    def wrapper(func=None, *args, **kwargs):
        for link in links:
            driver.get(link)
            if func is not None:
                if callable(func):
                    result = func(driver, *args, **kwargs)
                    return result
                else:
                    raise TypeError("'func' should be a callable")
            time.sleep(s)
    return wrapper

# follow_links('', [])(lambda x: x)
