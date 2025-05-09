# from setuptools import setup,find_packages

# setup (
# name = "peuent",
# version = "1.1.1.1",
# author = "Adnan"
# )

# packages = find_packages(),
# install_requirements = [
#     'selenium',
#     'webdriber_manager'


# ]

from setuptools import setup

setup(
    name="peuent",
    version="1.1.1.3",
    author="Adnan",
    py_modules=["peuent"],
    install_requires=[
        "selenium",
        "webdriver_manager"
    ]
)
