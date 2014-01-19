Description
===========
    An IMMENSELY FAST JPEG thumbnailer library API.

    Why write this? It's a convenience library API to using libjpeg to load
    JPEG images destined to be turned into thumbnails of the original, saving
    information with these thumbnails, retreiving it and managing to load the
    image ready for scaling with the minimum of fuss and CPU overhead.

    This means it's insanely fast at loading large JPEG images and scaling them
    down to tiny thumbnails. It's speedup will be proportional to the size
    difference between the source image and the output thumbnail size as a
    count of their pixels.

    It makes use of libjpeg features of being able to load an image by only
    decoding the DCT coefficients needed to reconstruct an image of the size
    desired. This gives a massive speedup. If you do not try and access the
    pixels in a format other than YUV (or GRAY8 if the source is grascale) then
    it also avoids colorspace conversions as well.

epeg source: https://github.com/mattes/epeg

This module provides Python bindings via CFFI.

Usage
=====
::

    In [1]: import epeg
    In [2]: thumbnail_data = epeg.scale_image(
        fname,   # Path to source JPEG image
        width,   # Desired thumbnail width
        height,  # Desired thumbnail height
        quality  # Desired quality, default: 75)


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

