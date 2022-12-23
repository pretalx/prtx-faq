import os
from distutils.command.build import build

from django.core import management
from setuptools import find_packages, setup

try:
    with open(
        os.path.join(os.path.dirname(__file__), "README.rst"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""


class CustomBuild(build):
    def run(self):
        management.call_command("compilemessages", verbosity=1)
        build.run(self)


cmdclass = {"build": CustomBuild}


setup(
    name="prtx-faq",
    version="1.0.2",
    description="An FAQ plugin for pretalx and pretix",
    long_description=long_description,
    url="https://github.com/pretalx/prtx-faq",
    author="Tobias Kunze",
    author_email="r@rixx.de",
    license="Apache Software License",
    install_requires=[],
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretix.plugin]
prtx_faq=prtx_faq:PretixPluginMeta

[pretalx.plugin]
prtx_faq=prtx_faq:PretalxPluginMeta
""",
)
