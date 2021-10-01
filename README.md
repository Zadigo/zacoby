# Zacoby

A web driver for Python with a focus for data mining and web scrapping.

# Getting started

To open a new session, do the following:

```
import os
from zacoby.utils.browsers import Edge

driver = Edge('path/to/drive')
driver.quit()
```

## Going to a specific address

To go to a specific url in the browser, you can use the `get` or `conditional_get` methods:

```
driver.get('http://example.com')
```

The conditional get will try the first address and then default to the default url on failure.

```
driver.condition_get('http://example.com', 'http://default-address.com')
```

## Interacting with the page

The driver implements a default manager than can be used to interact with elements on the web page.

### Page title

```
page_title = driver.manager.title
```

## Interacting with the DOM

In addition to the basic methods above, the following ones will allow you to interract directly with elements on the DOM. Each of the following methods return a `DomElement` instance object on which you can also call additional defintions.

### Find an element by its ID

```
element = driver.get_element_by_id('name')
```

### Find an element by its class

```
element = driver.get_element_by_class('name')
```

### Move forward

```
driver.manager.foward()
```

### Move backwards

```
driver.manager.back()
```

## Interacting with elements

Via the `DOMElement` interface, you'll also have the possibility to interact directly with with the element.

### Click

```
element = driver.get_element_by_id('name')
element.click()
```

### Text

```
element.text
```

## Conditions

You can perform actions with the driver based on certain specific conditions.

To run a condition, use `wait` or `pause` function wich will return either a `Wait` or `Pause` instance on which additional actions can be run.

```
driver.wait('name', timeout=10)
```

The wait instance implements three main functions: `until`, `until_not`, `chains` and `logical_map`.

### Until

Waits until the element answers to a specific condition.

`driver.wait('name').until(...)`

### Until not

Waits until the element does not answer to a specific condition.

`driver.wait('name').until_not(...)`

### Chains

Chain multiple conditions together.

`driver.wait('name').chains(condition1, condition2, method='until')`

### Logical map

Run a set of conditions depending on wether the

`driver.wait('name').logical_map({'until': condition1, 'until_not': condition2, ...})`

### Types of conditions

#### Element visible

Waits until an element is visible on the page.

```
from zacoby.conditions import element_visible

driver.wait('name').until(element_visible)
```

# Support / Development

If you are interested in me participating in some other projects for you relate to the current work that I have done I am currently available for remote and on-site consulting for small, large and enterprise teams. Please contact me at pendenquejohn@gmail.com with your needs and let's work together! ❤️
