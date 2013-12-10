#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   setup.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

from distutils.core import setup

setup(name="JAMediaImagenes",
    version="1",
    author="Flavio Danesse",
    author_email="fdanesse@gmail.com",
    url="https://sites.google.com/site/sugaractivities/",
    license="GPL3",

    scripts=["JAMediaImagenes", "JAMediaImagenesUninstall"],

    py_modules=['ImageProcess', 'toolbar', 'JAMediaImagenes'],

    data_files=[('/usr/share/applications/', ['JAMediaImagenes.desktop']),
        ('', ['JAMediaImagenesUninstall.py']),
        ('PIL', ['PIL/XVThumbImagePlugin.py', 'PIL/PSDraw.py',
        'PIL/_imagingft.so',
        'PIL/SpiderImagePlugin.py', 'PIL/IcoImagePlugin.py',
        'PIL/ImImagePlugin.py',
        'PIL/PalmImagePlugin.py', 'PIL/ExifTags.py', 'PIL/_imaging.so',
        'PIL/WmfImagePlugin.py',
        'PIL/PixarImagePlugin.py', 'PIL/ImageFilter.py', 'PIL/TarIO.py',
        'PIL/ImageEnhance.py',
        'PIL/PcdImagePlugin.py', 'PIL/JpegImagePlugin.py',
        'PIL/GimpPaletteFile.py', 'PIL/PaletteFile.py',
        'PIL/ImageGL.py', 'PIL/TiffImagePlugin.py', 'PIL/ImageDraw.py',
        'PIL/Image.py', 'PIL/SunImagePlugin.py',
        'PIL/EpsImagePlugin.py', 'PIL/ImageWin.py', 'PIL/ImageStat.py',
        'PIL/McIdasImagePlugin.py',
        'PIL/FontFile.py', 'PIL/XbmImagePlugin.py', 'PIL/TgaImagePlugin.py',
        'PIL/WalImageFile.py',
        'PIL/ImageTransform.py', 'PIL/PdfImagePlugin.py',
        'PIL/BdfFontFile.py', 'PIL/ContainerIO.py',
        'PIL/CurImagePlugin.py', 'PIL/IptcImagePlugin.py',
        'PIL/ImageFileIO.py', 'PIL/PsdImagePlugin.py',
        'PIL/BmpImagePlugin.py', 'PIL/PngImagePlugin.py',
        'PIL/_imagingmath.so', 'PIL/OleFileIO.py',
        'PIL/XpmImagePlugin.py', 'PIL/GbrImagePlugin.py',
        'PIL/ImageFont.py', 'PIL/FitsStubImagePlugin.py',
        'PIL/ImageDraw2.py', 'PIL/ImtImagePlugin.py',
        'PIL/ImageGrab.py', 'PIL/GimpGradientFile.py',
        'PIL/TiffTags.py', 'PIL/__init__.py', 'PIL/DcxImagePlugin.py',
        'PIL/ImageMath.py',
        'PIL/Hdf5StubImagePlugin.py', 'PIL/MicImagePlugin.py',
        'PIL/PIL-1.1.6.egg-info',
        'PIL/ImagePalette.py', 'PIL/MpegImagePlugin.py',
        'PIL/ImageColor.py', 'PIL/ImageChops.py',
        'PIL/PpmImagePlugin.py', 'PIL/BufrStubImagePlugin.py',
        'PIL/FpxImagePlugin.py',
        'PIL/GdImageFile.py', 'PIL/ImageQt.py', 'PIL/ImagePath.py',
        'PIL/_imagingtk.so',
        'PIL/GifImagePlugin.py', 'PIL/ImageTk.py', 'PIL/ImageSequence.py',
        'PIL/GribStubImagePlugin.py',
        'PIL/PcxImagePlugin.py', 'PIL/ImageOps.py', 'PIL/MspImagePlugin.py',
        'PIL/SgiImagePlugin.py',
        'PIL/FliImagePlugin.py', 'PIL/PcfFontFile.py',
        'PIL/ArgImagePlugin.py', 'PIL/ImageFile.py',
        'PIL/ImageMode.py', 'PIL/IcnsImagePlugin.py']),
        ('iconos', ['iconos/invert.png', 'iconos/grey.png',
        'iconos/JAMediaImagenes.png', 'iconos/finedges.png',
        'iconos/iconplay.png', 'iconos/ambross.png',
        'iconos/original.png', 'iconos/contour.png', 'iconos/solarize.png',
        'iconos/alejar.png',
        'iconos/deshacer.png', 'iconos/escalaoriginal.png',
        'iconos/acercar.png', 'iconos/sharpen.png',
        'iconos/blur.png', 'iconos/foto.png', 'iconos/rotar.png'])])
