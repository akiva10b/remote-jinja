[![PyPI version](https://badge.fury.io/py/remote-jinja.svg)](https://badge.fury.io/py/remote-jinja) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/remote-jinja.svg)
![GitHub stars](https://img.shields.io/github/stars/akiva10b/remote-jinja.svg) ![PyPI - Downloads](https://img.shields.io/pypi/dm/remote-jinja.svg) ![GitHub issues](https://img.shields.io/github/issues/akiva10b/remote-jinja.svg)

## Description

Remote Jinja template renderer - this library pulls the html from a remote location and renders it as a jinja template.

Frameworks such as [Fast-API](https://fastapi.tiangolo.com/), [Flask](https://flask.palletsprojects.com/en/2.1.x/) or [Django](https://www.djangoproject.com/) are great for serving your backend needs and providing functionality for data management. Jinja is a great add-on to manage HTML template and render data dynamically. However, when a user wants to use a tool such as [Webflow](http://webflow.io/) to manage the look and feel of their site, they must export the HTML and insert the template logic. This creates sustainability issues when changes are introduced to the template, and requires more boilerplate work.
That is what Remote Jinja solves. Using Remote Jinja you can easily pull the live version of your template and make changes on the fly even while your site is live.


**NOTE:** If you are managing your site on another templating service like Webflow, it is best to stick to that service. Importing templates from multiple sources can be problematic.

## Usage

Install: `pip install remote-jinja`

Import the `render_remote` function which takes a url and renders it as a jinja template
```python
from remote_jinja import render_remote
def some_view():
    return render_remote("https://akivas-initial-project-7c4990.webflow.io/")
```

Now your view will return all the HTML from the url like a local jinja template.

## Dynamic Content

While Jinja uses the deliminators `{{ }}` and `{% %}` by default, remote-jinja uses `{[ ]}` and `{[% %]}` instead. This is because many websites already use the default deliminators for other uses, causing template parsing errors.

In your HTML, put in a variable.
```html
<p>{[name]}</p>
```
Or just put in `{[name]}` somewhere in the content builder. 
Now, add the parameter to your template:
```python
from remote_jinja import render_remote
def some_view():
    return render_remote("https://akivas-initial-project-7c4990.webflow.io/", name="Cool new site")
```
Thats pretty much it, but now lets talk about caching and refreshing.

## Caching

By default, all remote templates are not cached, and if they are- it will be for 5 minutes. This is a useful default for development but not something we want in production. To activate caching, and change the caching timeout, do the following at the base for your project (`config.py`, `app.py` or `init.py` in most frameworks):
```python
from remote_jinja import rt
...
rt.default_refresh = True # set to False in production
rt.default_timeout = 300 # set to longer period of time
```
The caching is handeled in memory. This isn't very reliable so it is recommended to use a seperate caching server like redis or memcached so that the templates are saved there. You can do so by setting the `cache` parameter. For example, in Flask with memcached you can do as follows:
```python
from werkzeug.contrib.cache import MemcachedCache
from remote_jinja import rt
mc = pylibmc.Client(mc_servers...)
cache = MemcachedCache(mc)
...
rt.cache = cache
rt.default_refresh = False
rt.default_timeout = 60 * 60 * 72
```
## Settings
Other settings you can change are the deliminators, and per render function attributes. To change the deliminators globally, do the following:
```python
from remote_jinja import rt
...
rt.block_start_string='{[%'
rt.block_end_string='%]}'
rt.variable_start_string='{['
rt.variable_end_string=']}'
```

To change settings for just one view, place the params on the view level:
```python
from remote_jinja import render_remote
...
render_remote("https://yourwebsite.com/template",
block_start_string='{[%',
block_end_string='%]}',
variable_start_string='{[',
variable_end_string=']}',
refresh_template=request.args.get("refresh") # Refresh if URL contains param "refresh"
)
```
And that is all!

