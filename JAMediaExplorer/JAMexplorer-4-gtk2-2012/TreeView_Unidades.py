#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   TreeView_Unidades.py por:
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

import gtk, pygtk, gobject, os

HOME= os.environ["HOME"]
DIARIO= os.path.join(HOME, ".sugar/default")

class TreeView_Unidades(gtk.TreeView):
# Una lista de puntos de montaje para agregar en un gtk.HPaned zona izquierda
    def __init__(self):
        self.modelo = None
        self.treeview_arbol = None
        self.barra_de_estado = None
        gtk.TreeView.__init__(self)

        # construir ListStore que muestra la lista de archivos en el directorio referido
        self.modelo = self.construir_lista()
        self.construir_columnas_de_listas()
        self.Llenar_ListStore()

        self.treeselection = self.get_selection() # treeview.get_selection()
        self.treeselection.set_mode(gtk.SELECTION_SINGLE)
        # conecta a una funcion que manejará las selecciones
        self.treeselection.set_select_function(self.func_selecciones, self.modelo, True)

        self.set_model(self.modelo)

        self.show_all()

    '''
    def asignar_barra_de_estado(self, barra_de_estado):
        self.barra_de_estado = barra_de_estado'''

    def asignar_arbol_de_directorios(self, treeview_arbol):
        # El treeview de tipo treestore que muestra el arbol de directorios
        self.treeview_arbol = treeview_arbol

    def func_selecciones(self, selection, model, path, is_selected, user_data):
        # Control de selecciones sobre ListTore
        # otener la carpeta almacenada en esta fila
        iter= model.get_iter(path)
        directorio =  model.get_value(iter, 2)
        # ahora, con estos datos hay que llenar el arbol de directorios

        if directorio == "sugar-xos":
            self.treeview_arbol.modelo.clear()
            expresion= os.system(directorio)
        else:
            self.treeview_arbol.leer_directorio(directorio)
        return True # Debe devolver True
        
    def construir_lista(self):
        # Construye Listore para carpetas y unidades
        modelo= gtk.ListStore (str, str, str)
        return modelo

    def construir_columnas_de_listas(self):
        # Columnas para ListStore
        # Nombre de la columna, tipo de cellrender, Numero de columna comenzando en 0
        columna= gtk.TreeViewColumn('Unidades y Directorios') # primera columna de datos

        # crear un CellRenderers para mostrar los datos
        celda_de_imagen = gtk.CellRendererPixbuf() # para la imagen
        celda_de_texto = gtk.CellRendererText() # para el texto
        celda_de_direccion = gtk.CellRendererText() # para la direccion en el sistema de archivos
        celda_de_direccion.set_property('visible', False) # la hacemos invisible

        # agregar las celdas a la columna
        columna.pack_start(celda_de_imagen, False)
        columna.pack_start(celda_de_texto, True)
        columna.pack_start(celda_de_direccion, True)
        self.append_column (columna)# treeview.append_column (columna)

        columna.set_attributes(celda_de_imagen, stock_id=1)
        columna.set_attributes(celda_de_texto, text=0)
        columna.set_attributes(celda_de_direccion, text=2)

        # configurar los atributos de las celdas
        # GTK+ 2.0 doesn't support the "stock_id" property
        if gtk.gtk_version[1] < 2:
            columna.set_cell_data_func(celda_de_imagen, self.make_pb)
        else:
            columna.set_attributes(celda_de_imagen, stock_id=1)
        columna.set_attributes(celda_de_texto, text=0)

    def make_pb(self, columna, celda_de_texto, model, iter):
        # Los iconos del ListStore
        stock= model.get_value(iter, 1)
        pb= self.render_icon(stock, gtk.ICON_SIZE_MENU, None)
        celda_de_texto.set_property('pixbuf', pb)
        return

    def Llenar_ListStore(self):
        # Carga la lista de archivos en el ListStore segun el directorio referido
        self.modelo.append([ 'Home', gtk.STOCK_HOME, HOME])
        self.modelo.append([ 'Diario', gtk.STOCK_DND_MULTIPLE, DIARIO])
        self.modelo.append([ 'Directorio Raiz', gtk.STOCK_DIRECTORY, "/"])
        self.modelo.append([ 'Pendrive', gtk.STOCK_SAVE_AS, "/media"])
        #self.modelo.append([ 'Red', gtk.STOCK_NETWORK, "sugar-xos"])
