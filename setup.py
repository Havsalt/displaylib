from setuptools import setup
from displaylib import __version__, __author__


setup(
   name="displaylib",
   version=__version__,
   description="A collection of frameworks used to display ASCII or Pygame graphics",
   author=__author__,
   packages=[
      "displaylib",
      "displaylib.template",
      "displaylib.ascii",
      "displaylib.ascii.prefab",
      "displaylib.pygame"
   ]
)
