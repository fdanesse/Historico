#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaGlobals.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gtk
import os
import commands

DIRECTORIO_BASE = os.path.dirname(__file__)
ICONOS = os.path.join(DIRECTORIO_BASE, "Iconos/")

if not os.path.exists(os.path.join(os.environ["HOME"], "JAMediaDatos")):
    os.mkdir(os.path.join(os.environ["HOME"], "JAMediaDatos"))
    os.chmod(os.path.join(os.environ["HOME"], "JAMediaDatos"), 0755)

# unificar directorios de JAMedia, JAMediaVideo, JAMediaTube y JAMediaImagenes
directorio_viejo = os.path.join(os.environ["HOME"], "DatosJAMediaVideoEstudio")
directorio_nuevo = os.path.join(os.environ["HOME"], "JAMediaDatos")
if os.path.exists(directorio_viejo):
    for elemento in os.listdir(directorio_viejo):
        commands.getoutput('mv %s %s' % (os.path.join(directorio_viejo,
            elemento), directorio_nuevo))
    commands.getoutput('rm -r %s' % (directorio_viejo))

DIRECTORIOVIDEOS = os.path.join(os.environ["HOME"], "JAMediaDatos", "Videos")
DIRECTORIOFOTOS = os.path.join(os.environ["HOME"], "JAMediaDatos", "Fotos")
DIRECTORIOAUDIO = os.path.join(os.environ["HOME"], "JAMediaDatos", "Audio")
DIRECTORIOJAMEDIA = os.path.join(os.environ["HOME"], "JAMediaDatos", "MisArchivos")
DIRECTORIOJAMEDIATUBE = os.path.join(os.environ["HOME"], "JAMediaDatos", "YoutubeVideos")

if not os.path.exists(DIRECTORIOVIDEOS):
    os.mkdir(DIRECTORIOVIDEOS)
    os.chmod(DIRECTORIOVIDEOS, 0755)

if not os.path.exists(DIRECTORIOFOTOS):
    os.mkdir(DIRECTORIOFOTOS)
    os.chmod(DIRECTORIOFOTOS, 0755)

if not os.path.exists(DIRECTORIOAUDIO):
    os.mkdir(DIRECTORIOAUDIO)
    os.chmod(DIRECTORIOAUDIO, 0755)

if not os.path.exists(DIRECTORIOJAMEDIA):
    os.mkdir(DIRECTORIOJAMEDIA)
    os.chmod(DIRECTORIOJAMEDIA, 0755)

if not os.path.exists(DIRECTORIOJAMEDIATUBE):
    os.mkdir(DIRECTORIOJAMEDIATUBE)
    os.chmod(DIRECTORIOJAMEDIATUBE, 0755)

# Versiones viejas de gtk no funcionan si no se usa 0 a 65000. Ejem: 122*65000/255= 26000
GRIS = gtk.gdk.Color(60156, 60156, 60156, 1)
AMARILLO = gtk.gdk.Color(65000,65000,40275,1)
NARANJA = gtk.gdk.Color(65000,26000,0,1)
BLANCO = gtk.gdk.Color(65535, 65535, 65535,1)
NEGRO = gtk.gdk.Color(0, 0, 0, 1)

WIDTH = 640
HEIGHT = 480
BUTTONS = 60

def borrar_archivo(direccion):
    if os.path.exists(direccion):
        commands.getoutput('rm %s' % (direccion))

def describe_archivo(archivo):
    """ Devuelve el tipo de un archivo (imagen, video, texto).
    -z, --uncompress para ver dentro de los zip."""
    
    datos = commands.getoutput('file -ik %s%s%s' % ("\"", archivo, "\""))
    retorno = ""
    for dat in datos.split(":")[1:]:
        retorno += " %s" % (dat)
    return retorno
