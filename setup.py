import os

from setuptools import setup

root_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root_dir, "VERSION")) as f:
    VERSION = f.read().rstrip()

setup(
    name="mkpipU",

    version=VERSION,

    py_modules=['mkpipU'],

    entry_points={
        'console_scripts': [
            'pip-upgrade-all=mkpipU:main',
        ],
    },

    url="https://github.com/MichaelKim0407/mk-pip-upgrade-all",

    license="MIT",

    author="Michael Kim",

    author_email="mkim0407@gmail.com",

    description="pip upgrade all packages",

    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",

        "Topic :: Software Development :: Libraries",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ]
)
