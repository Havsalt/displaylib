from setuptools import setup
from displaylib import __doc__, __version__, __author__


with open("README.md", "r") as markdown_file:
   markdown_content = markdown_file.read()

setup(
   name="displaylib",
   version=__version__,
   author=__author__,
   description="An object-oriented framework for displaying ASCII graphics and creating an infinite world, aimed at simplifying the process",
   long_description=markdown_content,
   long_description_content_type="text/markdown",
   url="https://github.com/Floating-Int/displaylib",
   download_url="https://pypi.org/project/displaylib/",
   python_requires=">=3.10",
   packages=[
      "displaylib",
      "displaylib.template",
      "displaylib.template.networking",
      "displaylib.ascii",
      "displaylib.ascii.prefab",
      "displaylib.ascii.networking",
      "displaylib.pygame",
      "displaylib.pygame.networking"
   ]
)
