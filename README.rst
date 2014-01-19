Description
===========
    Insanely fast JPEG/ JPG thumbnail scaling with the minimum fuss and CPU overhead. It makes use of libjpeg features of being able to load an image by only decoding the DCT coefficients needed to reconstruct an image of the size desired.

This module provides Python bindings via CFFI.


Benchmarks
==========

Wand
----
::

    In [1]: from wand.image import Image
    In [2]: %timeit Image(filename='/tmp/007.jpg'); img.sample(800, 600); _ = img.make_blob('jpeg')
    1 loops, best of 3: 264 ms per loop

PIL/Pillow
----------
::

    In [1]: from PIL import Image
    In [2]: %timeit Image.open('/tmp/007.jpg').resize((800, 600)).save('/tmp/foo_thumb.jpg')
    1 loops, best of 3: 234 ms per loop

epeg
----
::

    In [1]: import epeg
    In [2]: %timeit epeg.scale_image('/tmp/007.jpg', 800, 600)
    10 loops, best of 3: 101 ms per loop

