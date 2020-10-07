# Zacoby

A web driver for Python with a focus for data mining and web scrapping.

# Getting started

The simple example below will simply just open your web browser.

```
import os
from zacoby.browsers.list import Edge

os.environ.setdefault("EDGE_DRIVER", "path/to/driver.exe")

driver = Edge(os.environ.get("EDGE_DRIVER"))
```

## Going to a specific address

```
driver.get("http://example.com")
```

## Interacting with the page

### Getting the title of the page

```
page_title = driver.title
```

## Interacting with the DOM

Each of these methods return a DomElement instance object on which you can also call additional defintions.

### Find an element by its ID 

```
element = driver.get_element_by_id("id name")
```

## Interacting with the DOM elements


Now, suppose you've found a given element on the DOM and want to do something with it. Then you can easily do any of these methods.

Each of these methods returns a DomElement instance object on which you can also call additional defintions.

```
element = driver.get_element_by_id("id name")

another_element = element.get_element_by_id("another id name")
```

