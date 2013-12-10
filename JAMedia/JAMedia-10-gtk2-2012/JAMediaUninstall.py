#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
import platform

print "Desinstalando de:", platform.platform()
print commands.getoutput('rm -r /usr/local/share/JAMedia')
print commands.getoutput('rm /usr/share/applications/JAMedia.desktop')
print commands.getoutput('rm /usr/local/bin/JAMedia')
print commands.getoutput('rm /usr/local/bin/JAMediaUninstall')
print "JAMedia se ha Desinstalado Correctamente del Sistema"
