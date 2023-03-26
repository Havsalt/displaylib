from setuptools import setup
from displaylib import __doc__, __version__, __author__


setup(
   name="displaylib",
   version=__version__,
   author=__author__,
   description="A collection of frameworks used to display ASCII or Pygame graphics",
   long_description=__doc__,
   url="https://github.com/Floating-Int/displaylib",
   download_url="https://pypi.org/project/displaylib/",
   packages=[
      "displaylib",
      "displaylib.template",
      "displaylib.ascii",
      "displaylib.ascii.prefab",
      "displaylib.pygame"
   ]
)
