#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Navegador_de_Archivos.py por:
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

import gtk, pygtk, os

from TreeView_Unidades import TreeView_Unidades
from TreeView_Directorios_y_archivos import TreeView_Directorios_y_archivos
from Preview import Preview

class Navegador_de_Archivos(gtk.HPaned):
    # Un panel horizontal con el navegador de archivos.
    # para agregar directamente a una ventana o al canvas de una ventana sugar.
    def __init__(self):
        gtk.HPaned.__init__(self)
        self.unidadesdealmacenamiento= None
        self.arboldedirectorios= None
        self.barra_info= Preview()

        #self.add1(self.area_izquierda_del_panel())
        #self.add2(self.area_derecha_del_panel())
        self.pack1(self.area_izquierda_del_panel(), resize=False, shrink=True)
        self.pack2(self.area_derecha_del_panel(), resize=True, shrink=True)

        # Vinculamos ambos treeview
        self.unidadesdealmacenamiento.asignar_arbol_de_directorios(self.arboldedirectorios)

        # Seleccionamos el primer punto de montaje en la lista para llenar el arbol de directorios
        self.unidadesdealmacenamiento.treeselection.select_path(0)

        # asignamos el preview
        self.arboldedirectorios.asignar_preview(self.barra_info)

        self.show_all()
    '''
    def asignar_barra_de_estado(self, barra_de_estado):
    # Una forma de conectar los treeview a la barra de estado
        self.unidadesdealmacenamiento.asignar_barra_de_estado(barra_de_estado)
        self.arboldedirectorios.asignar_barra_de_estado(barra_de_estado)'''

    def area_izquierda_del_panel(self):
        # El widget de la zona izquierda de gtk.HPaned
        self.unidadesdealmacenamiento= TreeView_Unidades()
        panel_izquierdo = gtk.VPaned()
        panel_izquierdo.pack1(self.unidadesdealmacenamiento, resize=False, shrink=True)
        panel_izquierdo.pack2(self.barra_info, resize=True, shrink=True)
        return panel_izquierdo


    def area_derecha_del_panel(self):
        # El widget de la zona derecha de gtk.HPaned
        scrolled_window2= gtk.ScrolledWindow()
        scrolled_window2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.arboldedirectorios= TreeView_Directorios_y_archivos()
        scrolled_window2.add_with_viewport (self.arboldedirectorios)
        return scrolled_window2
    