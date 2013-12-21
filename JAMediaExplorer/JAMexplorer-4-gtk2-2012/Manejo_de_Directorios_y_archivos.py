#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Manejo_de_Directorios_y_archivos.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM - Uruguay
#
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

import gobject, os, string

class Manejo_de_Directorios_y_archivos():
    # Maneja las operaciones sobre el sistema de archivos
    def __init__(self):
        pass

    def verificar_permisos(self, path):
        # verificar:
        # 1- Si es un archivo o un directorio
        # 2- Si sus permisos permiten la copia, escritura y borrado

        # Comprobar existencia y permisos http://docs.python.org/library/os.html?highlight=os#module-os
        # os.access(path, mode)
        # os.F_OK # si existe la direccion
        # os.R_OK # Permisos de lectura
        # os.W_OK # Permisos de escritura
        # os.X_OK # Permisos de ejecucion
        if not os.path.exists(path): return False, False, False
        try:
            if  os.access(path, os.F_OK):
                return os.access(path, os.R_OK), os.access(path, os.W_OK), os.access(path, os.X_OK)
            else:
                return False, False, False
        except:
            return False, False, False

    def copiar(self, origen, destino):
        try:
            # copiar un directorio
            if os.path.isdir(origen):
                expresion = "cp -r \"" + origen + "\" \"" + destino + "\""
            # copiar un archivo
            if os.path.isfile(origen):
                expresion = "cp \"" + origen + "\" \"" + destino + "\""
            os.system(expresion)
            return True
        except:
            print "ERROR"
            return False

    def mover(self, origen, destino):
        try:
            expresion= "mv \"" + origen + "\" \"" + destino + "\""
            os.system(expresion)
            return True
        except:
            print "ERROR"
            return False

    def borrar (self, origen):
        try:
            # copiar un directorio
            if os.path.isdir(origen):
                expresion= "rm -r \"" + origen + "\""
            # copiar un archivo
            if os.path.isfile(origen):
                expresion= "rm \"" + origen  + "\""
            os.system(expresion)
            return True
        except:
            print "ERROR"
            return False

    def crear_directorio (self, origen, directorionuevo):
        try:
            if os.path.isdir(origen) or os.path.ismount(origen):
                expresion= "mkdir \"" + origen + "/\"" + directorionuevo
                os.system(expresion)
                return True
        except:
            print "ERROR"
            return False
        