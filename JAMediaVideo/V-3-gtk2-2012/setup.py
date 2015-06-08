#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   setup.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import commands
from distutils.core import setup

setup(name="JAMediaVideo",  
      	version= "2",
      	author= "Flavio Danesse",
      	author_email= "fdanesse@gmail.com",
      	url= "https://sites.google.com/site/sugaractivities/jam/jamediavideoestudio",
      	license= "GPL3",

      	scripts= ['JAMediaVideo', 'JAMediaVideoUninstall'],

	py_modules= ['JAMediaGlobals', 'JAMediaReproductor', 'JAMediaWebCam', 'JAMediaMixer', 'JAMediaVideo',
	'JAMediaWidgets'],

	data_files= [('/usr/share/applications/', ['JAMediaVideo.desktop']), ('', ['JAMediaVideoUninstall.py']),
	('Iconos', ['Iconos/licencia.png', 'Iconos/pausa.png', 'Iconos/JAMediaVideo.png', 'Iconos/salir.png',
	'Iconos/iconplay.png', 'Iconos/play.png', 'Iconos/siguiente.png', 'Iconos/configurar.png',
	'Iconos/uruguay.png', 'Iconos/microfono.png', 'Iconos/camara.png', 'Iconos/monitor.png',
	'Iconos/volumen.png', 'Iconos/ceibaljam.png', 'Iconos/lista.png', 'Iconos/foto.png', 'Iconos/stop.png'])])

