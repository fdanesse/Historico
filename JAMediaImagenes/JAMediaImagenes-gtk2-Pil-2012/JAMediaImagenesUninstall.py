#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, commands, platform

print "Desinstalando de:", platform.platform()
print commands.getoutput('rm -r /usr/local/share/JAMediaImagenes')
print commands.getoutput('rm /usr/share/applications/JAMediaImagenes.desktop')
print commands.getoutput('rm /usr/local/bin/JAMediaImagenes')
print commands.getoutput('rm /usr/local/bin/JAMediaImagenesUninstall')
print "JAMedia Imagenes se ha Desinstalado Correctamente del Sistema"

