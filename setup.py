from setuptools import setup, Extension

setup(name='epeg-cffi',
    version="0.01",
    author="Johannes Baiter",
    url="http://github.com/jbaiter/epeg-cffi.git",
    author_email="johannes.baiter@gmail.com",
    py_modules=['epeg'],
    ext_modules=[
        Extension('_epeg',
            include_dirs = ['./src'],
            libraries = ['jpeg'],
            sources = ['src/epeg.c']),
    ],
    install_requires=['cffi >= 0.8.1'],
)
