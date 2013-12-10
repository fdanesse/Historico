#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   setup.py por: Flavio Danesse fdanesse@gmail.com
#   Modificaciones menores por Daniel Francis <francis@sugarlabs.org>
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

try:
    from sugar.activity import bundlebuilder
    bundlebuilder.start()

except:
    import commands
    from distutils.core import setup

    setup(name="JAMedia",
          version="10",
          author="Flavio Danesse",
          author_email="fdanesse@gmail.com",
          url="https://sites.google.com/site/sugaractivities/",
          license="GPL3",

          scripts=["JAMedia", "JAMediaUninstall"],

          py_modules=['JAMediaGlobals', 'JAMediaLista', 'JAMediaMixer',
            'JAMediaWidgets',
            'Mplayer_Reproductor', 'Archivos_y_Directorios',
            'JAMedia', 'Mplayer_Grabador',
            'Olidata_install'],

          data_files=[('/usr/share/applications/', ['JAMedia.desktop']),
            ('', ['JAMediaUninstall.py']),
            ('Iconos', ['Iconos/pausa.png', 'Iconos/JAMedia.png',
            'Iconos/salir.png',
            'Iconos/play.png', 'Iconos/siguiente.png', 'Iconos/monitor.png',
            'Iconos/volumen.png', 'Iconos/fondo.png', 'Iconos/JAMedia.png',
            'Iconos/lista.png',
            'Iconos/stop.png', 'Iconos/camara.png', 'Iconos/iconplay.png',
            'Iconos/agregar.png'])])

    commands.getoutput(
        'chmod 755 /usr/local/share/JAMedia/Mplayer_Grabador.py')
