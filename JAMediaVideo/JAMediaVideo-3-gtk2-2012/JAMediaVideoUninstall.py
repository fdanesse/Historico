#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, commands, platform

print "Desinstalando de:", platform.platform()
print commands.getoutput('rm -r /usr/local/share/JAMediaVideo')
print commands.getoutput('rm /usr/share/applications/JAMediaVideo.desktop')
print commands.getoutput('rm /usr/local/bin/JAMediaVideo')
print commands.getoutput('rm /usr/local/bin/JAMediaVideoUninstall')
print "JAMedia Video se ha Desinstalado Correctamente del Sistema"

