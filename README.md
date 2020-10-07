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


