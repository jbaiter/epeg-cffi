import os.path
import sys
from site import USER_SITE

from cffi import FFI
ffi = FFI()
try:
    lib = ffi.dlopen(next(os.path.join(x, '_epeg.so') for x in sys.path
                          if os.path.exists(os.path.join(x, '_epeg.so'))))
except StopIteration:
    raise Exception("Could not find _epeg.so!")

ffi.cdef("""
   typedef enum
     {
        EPEG_GRAY8,
        EPEG_YUV8,
        EPEG_RGB8,
        EPEG_BGR8,
        EPEG_RGBA8,
        EPEG_BGRA8,
        EPEG_ARGB32,
        EPEG_CMYK
     } Epeg_Colorspace;


   typedef struct
     {
        char                   *uri;
        unsigned long long int  mtime;
        int                     w, h;
        char                   *mimetype;
     } Epeg_Thumbnail_Info;

    typedef struct
    {
        struct _epeg_error_mgr          jerr;
        struct stat                     stat_info;
        unsigned char                  *pixels;
        unsigned char                 **lines;

        char                            scaled : 1;

        int                             error;

        Epeg_Colorspace                 color_space;

        struct {
            char                          *file;
            struct {
                unsigned char           **data;
                int                       size;
            } mem;
            int                            w, h;
            char                          *comment;
            FILE                          *f;
            struct jpeg_decompress_struct  jinfo;
            struct {
                char                       *uri;
                unsigned long long int      mtime;
                int                         w, h;
                char                       *mime;
            } thumb_info;
        } in;
        struct {
            char                        *file;
            struct {
                unsigned char           **data;
                int                      *size;
            } mem;
            int                          x, y;
            int                          w, h;
            char                        *comment;
            FILE                        *f;
            struct jpeg_compress_struct  jinfo;
            int                          quality;
            char                         thumbnail_info : 1;
        } out;
    } Epeg_Image;

   Epeg_Image   *epeg_file_open                 (const char *file);
   Epeg_Image   *epeg_memory_open               (unsigned char *data, int size);
   void          epeg_size_get                  (Epeg_Image *im, int *w, int *h);
   void          epeg_decode_size_set           (Epeg_Image *im, int w, int h);
   void          epeg_colorspace_get            (Epeg_Image *im, int *space);
   void          epeg_decode_colorspace_set     (Epeg_Image *im, Epeg_Colorspace colorspace);
   const void   *epeg_pixels_get                (Epeg_Image *im, int x, int y, int w, int h);
   void          epeg_pixels_free               (Epeg_Image *im, const void *data);
   const char   *epeg_comment_get               (Epeg_Image *im);
   void          epeg_thumbnail_comments_get    (Epeg_Image *im, Epeg_Thumbnail_Info *info);
   void          epeg_comment_set               (Epeg_Image *im, const char *comment);
   void          epeg_quality_set               (Epeg_Image *im, int quality);
   void          epeg_thumbnail_comments_enable (Epeg_Image *im, int onoff);
   void          epeg_file_output_set           (Epeg_Image *im, const char *file);
   void          epeg_memory_output_set         (Epeg_Image *im, unsigned char **data, int *size);
   int           epeg_encode                    (Epeg_Image *im);
   int           epeg_trim                      (Epeg_Image *im);
   void          epeg_close                     (Epeg_Image *im);
""")


def scale_image(fname, width, height, quality=75):
    try:
        img = lib.epeg_file_open(fname)
    except TypeError:
        # FIXME: The first call to epeg_file_open will always throw a
        #        TypeError, and I have no clue why...
        #        Subsequent calls always work fine, so we currently have
        #        this ugly workaround.
        img = lib.epeg_file_open(fname)
    lib.epeg_decode_size_set(img, width, height)
    lib.epeg_quality_set(img, quality)

    pdata = ffi.new("unsigned char **")
    psize = ffi.new("int*")
    lib.epeg_memory_output_set(img, pdata, psize)
    lib.epeg_encode(img)
    lib.epeg_close(img)
    return ffi.buffer(pdata[0], psize[0])[:]
