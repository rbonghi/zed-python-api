########################################################################
#
# Copyright (c) 2020, STEREOLABS.
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

# Reference
# https://github.com/h5py/h5py/blob/master/setup.py
# https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html

try:
    from setuptools import Extension
except ImportError:
    from distutils.extension import Extension
import sys
from distutils.command.build_ext import build_ext

cython_directives = {"embedsignature": True}

GPUmodulesTable = [("pyzed.sl", ["pyzed/sl.pyx"])]

def create_extension(name, sources, libs):
    if sys.platform == "win32":
        ext = Extension(name,
                        sources=sources,
                        include_dirs=libs['incDirs'],
                        library_dirs=libs['libDirs'],
                        libraries=libs['libs'],
                        language="c++"
                        )

        return ext
    elif "linux" in sys.platform:
        ext = Extension(name,
                        sources=sources,
                        include_dirs=libs['incDirs'],
                        library_dirs=libs['libDirs'],
                        libraries=libs['libs'],
                        runtime_library_dirs=libs['libDirs'],
                        language="c++",
                        extra_compile_args=libs['cflags']
                        )
        return ext
    else:
        print ("Unknown system.platform: %s" % sys.platform)
        return None

class pyzed_build_ext(build_ext):

    @staticmethod
    def _make_extensions(config):
        """ Produce a list of Extension instances which can be passed to
        cythonize().
        This is the point at which custom directories, MPI options, etc.
        enter the build process.
        """

        from Cython.Build import cythonize

        extensions = []

        libs = {
            'incDirs': '',
            'libDirs': '',
            'libs': '',
            'cflags': '',
        }

        for mod in GPUmodulesTable:
            print ("Building module:", mod)
            extension = create_extension(mod[0], mod[1], libs)
            if extension == None:
                print ("WARNING: extension is None, see setup.py:", mod)
            extList = cythonize(extension, compiler_directives=cython_directives)#, language_level = "3")
            extensions.extend(extList)
        
        print(extensions)

    def run(self):
        """ Distutils calls this method to run the command """

        from Cython.Build import cythonize
        import numpy

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>")