# pyColdStream
<p align="center">
  <img src="images/logo.png" alt="pyColdStream Logo" width="500">
</p>

The pyColdStream library provides a simple and convenient way to interact with Diabatix's ColdStream using Python. It is based on the official REST API of ColdStream. This library can be used to automate tasks, integrate with other tools and systems, and build custom applications that interact with ColdStream. Overall, it is a convenient way to access the full range of functionality offered by the ColdStream REST API.

## How to install?
From Pypi
`pip install pycoldstream`

From Source
- Git clone repository
- Use `pip install -r requirements.txt` to install the required packages
- or `pipenv install && pipenv install --dev`

## Examples
More examples in `examples/` directory

Here's a short example of how to create a new project in ColdStream and load the project data afterwards:
```
from coldstream import ColdstreamSession
from pprint import pprint

session = ColdstreamSession.create_from_login(user="admin@admin.com", password="admin")
new_project = session.projects.create_project("Project Name", "This is the project description.")

pprint(new_project.data)
```

## Additional resources
<a href="https://coldstream.readme.io/reference">API documentation</a><br>
<a href="https://www.diabatix.com">Visit our website</a>
