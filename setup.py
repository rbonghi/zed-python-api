########################################################################
#
# Copyright (c) 2018, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################

"""
    Setup file to build, install, clean the pyzed package.
"""
try:
    from setuptools import Extension, setup
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension

from os import path
import re

import setup_build

here = path.abspath(path.dirname(__file__))
project_homepage = "https://github.com/rbonghi/zed-python-api"

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Load version package
with open(path.join(here, "pyzed", "__init__.py")) as fp:
    VERSION = (
        re.compile(r""".*__version__ = ["'](.*?)['"]""", re.S).match(fp.read()).group(1)
    )
# Store version package
version = VERSION

setup(name="pyzed",
      version=version,
      author_email="developers@stereolabs.com",
      description="Use the ZED SDK with Python",
      license='MIT',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url=project_homepage,
      packages=["pyzed"],
      project_urls={
           "How To": (project_homepage + "/tree/master/docs"),
           "Examples": (project_homepage + "/tree/master/examples"),
           "Bug Reports": (project_homepage + "/issues"),
           "Source": (project_homepage + "/tree/master")
      },
      setup_requires=[
          'cython >= 0.28',
          'numpy >= 1.13',
          'wheel'],
      python_requires='>=3.6',
      cmdclass = {
          'build_ext': setup_build.pyzed_build_ext,
      },
      install_requires=requirements,
      #ext_modules=extensions
)
# EOF
