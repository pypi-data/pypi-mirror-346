#!/usr/bin/env python3

#Do not run this file directly!
# This `setup.py` is to be called by pip,
# reading the pyproject.toml file!
# It's purpose is to build the C++ components.

#Inspired by https://setuptools.pypa.io/en/latest/userguide/ext_modules.html

from setuptools import Extension, setup

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

#From https://stackoverflow.com/a/68349405
from setuptools.command.build_ext import build_ext
class build_ext_ex(build_ext):

    extra_compile_args = {
        'CLICopti._CLICopti': {
            'msvc' : ['/permissive-'],
            'unix' : ['-std=c++11']
        }
    }

    def build_extension(self, ext):
        extra_args = self.extra_compile_args.get(ext.name)
        if extra_args is not None:
            ctype = self.compiler.compiler_type
            ext.extra_compile_args = extra_args.get(ctype, [])
        build_ext.build_extension(self, ext)

#TODO: It might be possible to run SWIG straight from here
#      However this would require the user to have SWIG installed.
#      See main readme.md for how to regenerate swig wrapper code after changing API.

setup(
    cmdclass = {'build_ext': build_ext_ex},
    ext_modules=[
        Extension(
            name="CLICopti._CLICopti",
            include_dirs=['h'],
            language='c++',
            sources=["swig/CLICopti_python_wrap.cc",
                     "swig/splash.cc",
                     "src/cellBase.cpp",
                     "src/cellParams.cpp",
                     "src/structure.cpp"
                     ],
            depends=["h/cellBase.h",
                     "h/cellParams.h",
                     "h/constants.h",
                     "h/structure.h"]
            )
    ]
)
