from setuptools import setup, Extension

setup(name='epeg-cffi',
    version="0.01",
    description=(
        "Insanely fast JPEG/ JPG thumbnail scaling with the minimum fuss and "
        "CPU overhead. It makes use of libjpeg features of being able to load "
        "an image by only decoding the DCT coefficients needed to reconstruct "
        "an image of the size desired."),
    long_description=open('README.rst').read(),
    author="Johannes Baiter",
    url="http://github.com/jbaiter/epeg-cffi.git",
    author_email="johannes.baiter@gmail.com",
    license='MIT',
    py_modules=['epeg'],
    ext_modules=[
        Extension('_epeg',
            include_dirs = ['./src'],
            libraries = ['jpeg'],
            sources = ['src/epeg.c']),
    ],
    install_requires=['cffi >= 0.8.1'],
)
