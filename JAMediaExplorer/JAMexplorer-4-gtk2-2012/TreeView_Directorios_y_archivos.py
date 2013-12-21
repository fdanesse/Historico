#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   TreeView_Directorios_y_archivos.py por:
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

from Manejo_de_Directorios_y_archivos import Manejo_de_Directorios_y_archivos

class TreeView_Directorios_y_archivos(gtk.TreeView):
# Un arbol de directorios para agregar en un gtk.HPaned zona derecha
    def __init__(self):
        self.modelo= None
        #self.barra_de_estado= None
        self.preview= None

        gtk.TreeView.__init__(self)
        #self.set_property("enable-grid-lines", True)
        self.set_property("rules-hint", True)
        self.set_property("enable-tree-lines", True)

        # construir TreeStore
        self.modelo= self.construir_arbol()
        self.construir_columnas_de_arbol()

        # Conectamos el treeview a la señal "expandir fila" para que se llame a nuestra funcion callback_expand
        self.connect("row-expanded", self.callback_expand, None)
        self.connect("row-activated", self.callback_activated, None)
        self.connect("row-collapsed", self.callback_collapsed, None)

        # Detectar eventos del mouse, en particular click derecho para crear menu emergente
        self.add_events(gtk.gdk.BUTTON2_MASK)
        self.connect("button-press-event", self.handler_click)

        self.set_model(self.modelo)

        self.treeselection= self.get_selection() # treeview.get_selection()
        self.treeselection.set_mode(gtk.SELECTION_SINGLE)
        # conecta a una funcion que manejará las selecciones
        self.treeselection.set_select_function(self.func_selecciones, self.modelo, True)

        self.show_all()

        self.direccion_seleccionada= None
        self.direccion_seleccionada_para_cortar= None
        self.manejadordearchivos= Manejo_de_Directorios_y_archivos()

    def func_selecciones(self, selection, model, path, is_selected, user_data):
        # Control de selecciones sobre treestore
        iter= self.modelo.get_iter(path)
        direccion= self.modelo.get_value(iter, 2)
        self.preview.control_preview(direccion)
        return True # Debe devolver True

    def asignar_preview(self, barra_info):
        # preview de archivo seleccionado
        self.preview= barra_info

    '''
    def asignar_barra_de_estado(self, barra_de_estado):
    # Barra de estado
        self.barra_de_estado = barra_de_estado'''

    def handler_click(self, widget, event):
        # reacciona a los clicks sobre las filas de tresstore
        boton= event.button
        pos= (event.x, event.y)
        tiempo= event.time

        # widget es TreeView widget.get_name()
        # Obteniendo datos a partir de coordenadas de evento
        path, columna, xdefondo, ydefondo= widget.get_path_at_pos(int(pos[0]), int(pos[1]))
        # TreeView.get_path_at_pos(event.x, event.y) devuelve:
        # * La ruta de acceso en el punto especificado (x, y), en relación con las coordenadas widget
        # * El gtk.TreeViewColumn en ese punto
        # * La coordenada X en relación con el fondo de la celda
        # * La coordenada Y en relación con el fondo de la celda
        if boton == 1:
            return
        elif boton == 3:
            # Abrir menu - popup pasando el path de la fila seleccionada
            self.crear_menu_emergente(boton, pos, tiempo, path)
            return
        elif boton == 2:
            return

    def crear_menu_emergente(self, boton, pos, tiempo, path):
        # un menu para agregar o eliminar radios de la base de datos
        menu= gtk.Menu()
        iter= self.modelo.get_iter(path)
        direccion= self.modelo.get_value(iter, 2)
        # verificamos los permisos del archivo o directorio
        lectura, escritura, ejecucion= self.manejadordearchivos.verificar_permisos(direccion)

        # Items del menu
        if lectura: #and not os.path.ismount(os.path.join(direccion)):
            copiar = gtk.MenuItem("Copiar")
            menu.append(copiar)
            copiar.connect_object("activate", self.seleccionar_origen, path, "Copiar")

        if escritura and not os.path.ismount(os.path.join(direccion)):
            borrar = gtk.MenuItem("Borrar")
            menu.append(borrar)
            borrar.connect_object("activate", self.seleccionar_origen, path, "Borrar")

        if escritura and (os.path.isdir(os.path.join(direccion)) or os.path.ismount(os.path.join(direccion))) \
            and (self.direccion_seleccionada != None or self.direccion_seleccionada_para_cortar != None):
            pegar = gtk.MenuItem("Pegar")
            menu.append(pegar)
            pegar.connect_object("activate", self.seleccionar_origen, path, "Pegar")

        if escritura and (os.path.isdir(os.path.join(direccion)) or os.path.isfile(os.path.join(direccion))):
            cortar = gtk.MenuItem("Cortar")
            menu.append(cortar)
            cortar.connect_object("activate", self.seleccionar_origen, path, "Cortar")

        if escritura and (os.path.isdir(os.path.join(direccion)) or os.path.ismount(os.path.join(direccion))):
            nuevodirectorio = gtk.MenuItem("Crear Directorio")
            menu.append(nuevodirectorio)
            nuevodirectorio.connect_object("activate", self.seleccionar_origen, path, "Crear Directorio")

        menu.show_all()
        #popup(parent_menu_shell, parent_menu_item, func, button, activate_time, data=None)
        gtk.Menu.popup(menu, None, None, None, boton, tiempo)

    def seleccionar_origen(self, path, accion):
        # Recibe el path de la fila seleccionada en el modelo y una accion a realizar.
        iter= self.modelo.get_iter(path)
        direccion= self.modelo.get_value(iter, 2)
        lectura, escritura, ejecucion= self.manejadordearchivos.verificar_permisos(direccion)

        if accion == "Copiar":
            # Se selecciona un archivo o carpeta para copiarlo
            self.direccion_seleccionada= direccion
            #self.barra_de_estado.set_text("Vas a Copiar:  " + self.direccion_seleccionada + "  en . . .")
        elif accion == "Borrar":
            # Borramos un archivo o directorio
            self.direccion_seleccionada= direccion
            dialog= gtk.Dialog("Borrar Archivos o Carpeta . . .", None, gtk.DIALOG_MODAL, None)
            etiqueta= gtk.Label("¿Realmente deseas borrar: %s" % (direccion))
            dialog.vbox.pack_start(etiqueta, True, True, 5)
            dialog.add_button("Si, Borrar", 1)
            dialog.add_button("No, no borrar", 2)
            dialog.show_all()

            if dialog.run()== 1:
                # verificar y guardar
                if self.manejadordearchivos.borrar(self.direccion_seleccionada):
                    self.modelo.remove(iter)
            elif dialog.run()== 2:
                # sale automaticamente
                pass
                dialog.destroy()
            #self.barra_de_estado.set_text("Acabas de Borrar:  " + self.direccion_seleccionada)
            self.direccion_seleccionada = None

        elif accion == "Pegar":
            # Realizamos una copia de archivo o directorio
            if self.direccion_seleccionada_para_cortar:
                if self.manejadordearchivos.mover(self.direccion_seleccionada_para_cortar, direccion):
                    self.collapse_row(path)
                    self.expand_to_path(path)
                    self.direccion_seleccionada_para_cortar= None
            else:
                #self.barra_de_estado.set_text("Pegando:  " + self.direccion_seleccionada + "  en: " + direccion)
                if self.manejadordearchivos.copiar(self.direccion_seleccionada, direccion):
                    self.collapse_row(path)
                    self.expand_to_path(path)
                    self.direccion_seleccionada= None

        elif accion == "Cortar":
            # Realizamos una copia de archivo o directorio
            self.direccion_seleccionada_para_cortar= direccion
            self.modelo.remove(iter)
            self.direccion_seleccionada= None

        elif accion == "Crear Directorio":
            # Realizamos una copia de archivo o directorio
            dialog = gtk.Dialog("Crear Directorio . . .", None, gtk.DIALOG_MODAL, None)
            etiqueta = gtk.Label("Nombre del Directorio: ")
            entry = gtk.Entry(max=0)
            dialog.vbox.pack_start(etiqueta, True, True, 5)
            dialog.vbox.pack_start(entry, True, True, 5)
            dialog.add_button("Crear Directorio", 1)
            dialog.add_button("Cancelar", 2)
            dialog.show_all()

            if dialog.run() == 1:
                # verificar y guardar
                directorio_nuevo= entry.get_text()
                if directorio_nuevo != "" and directorio_nuevo != None:
                    if self.manejadordearchivos.crear_directorio(direccion, entry.get_text()):
                        self.collapse_row(path)
                        self.expand_to_path(path)
            elif dialog.run() == 2:
                # sale automaticamente
                pass
                dialog.destroy()

    def construir_arbol(self):
        # Arbol de directorios
        modelo = gtk.TreeStore (str, str, str, str)
        return modelo

    def construir_columnas_de_arbol(self):
        # Columnas para el TreeStore
        columna= gtk.TreeViewColumn('Directorios y Archivos')
        celda_de_imagen= gtk.CellRendererPixbuf() # para la imagen
        celda_de_texto= gtk.CellRendererText()
        celda_de_direccion= gtk.CellRendererText()

        columna.pack_start(celda_de_imagen, False)
        columna.pack_start(celda_de_texto, True)
        columna.pack_start(celda_de_direccion, True)

        celda_de_direccion.set_property('visible', False) # la hacemos invisible
        columna.set_property('resizable', True)
        self.append_column (columna)

        columna.set_attributes(celda_de_imagen, stock_id=1)
        columna.set_attributes(celda_de_texto, text=0)
        columna.set_attributes(celda_de_direccion, text=2)

        if gtk.gtk_version[1] < 2:
            columna.set_cell_data_func(celda_de_imagen, self.make_pb)
        else:
            columna.set_attributes(celda_de_imagen, stock_id=1)
            columna.set_attributes(celda_de_texto, text=0)

        render2= gtk.CellRendererText()
        columna2= gtk.TreeViewColumn('Tamaño', render2, text=3)
        self.append_column (columna2)

        self.set_expander_column(columna) # por defecto es la primer columna, este metodo permite cambiarla

    def make_pb(self, columna, celda_de_texto, model, iter):
        # Los iconos del ListStore
        stock= model.get_value(iter, 1)
        pb= self.render_icon(stock, gtk.ICON_SIZE_MENU, None)
        celda_de_texto.set_property('pixbuf', pb)
        return

    def leer_directorio(self, directorio):
        # Recibe el directorio base desde donde se armará el arbol del treestore.
        self.modelo.clear()
        path= 0
        carpeta= (directorio, path)
        self.leer(carpeta)

    def leer(self, carpeta):
        # Agrega directorios y archivos en un nodo del treestore
        try:
            directorio= carpeta[0] # direccion de la carpeta que vamos a leer
            path= carpeta[1] # nodo del treestore donde se insertará la carpeta
            if path == 0:
                iter= self.modelo.get_iter_first()
            else:
                iter= self.modelo.get_iter(path)

            archivos= []
            for archivo in os.listdir(os.path.join(directorio)): # lee el directorio
                direccion= os.path.join(directorio, archivo) # crea la direccion del archivo o directorio encontrado
                if os.path.isdir(direccion):
                    # si es un directorio
                    iteractual= self.modelo.append(iter,[archivo, gtk.STOCK_DIRECTORY, direccion, ""])
                    self.agregar_nada(iteractual) # para mostrar expansor de fila en los directorios
                    #print "Directorio agregado: ", direccion, self.modelo.get_path(iteractual)
                elif os.path.isfile(direccion):
                    #si es un archivo
                    archivos.append(direccion)
                
            for x in archivos:
                archivo= os.path.basename(x)
                self.modelo.append(iter,[archivo, gtk.STOCK_NEW, x, str(os.path.getsize(x))+" bytes"])
        except:
            print "**** Error de acceso a un archivo o carpeta ****"

    def agregar_nada(self, iterador):
        # para mostrar expansor de fila en los directorios
        self.modelo.append(iterador,["(Vacío)", None, None, None])

    def callback_expand (self, treeview, iter, path, user_param1):
        # Se ejecuta cuando el usuario expande la fila
        # Obtener los datos del primer hijo en este nodo
        iterdelprimerhijo= treeview.modelo.iter_children(iter) # El primer hijo de esta fila
        valordelprimerhijoenlafila= treeview.modelo.get_value(iterdelprimerhijo, 0)
        # tomar el valor de la direccion almacenada en el item
        valor= treeview.modelo.get_value(iter, 2)
        carpeta= (valor, path)
        #print "Valor de este item: ", valor
        # Ver si hay archivos o directorios bajo esta direccion
        if os.listdir(os.path.join(valor)) and valordelprimerhijoenlafila == "(Vacío)":
            #print ". . . Esta direccion contiene carpetas o archivos"
            #print ". . . El modelo contiene", treeview.modelo.iter_n_children(iter), "hijos"
            #print ". . . El valor del primer hijo es:",valordelprimerhijoenlafila
            self.leer(carpeta)
            treeview.modelo.remove(iterdelprimerhijo)
            #print "Borrando Item: ", valordelprimerhijoenlafila
        else:
            print ". . . Esta direccion está vacía o ya fue llenada"
        #print "row-expanded", path, directorio

    def callback_activated (self, treeview, path, view_column, user_param1):
        # Cuando se hace doble click sobre una fila
        # Obtengo el valor almacenado
        iter= treeview.modelo.get_iter(path)
        valor= treeview.modelo.get_value(iter, 2)

        if os.path.isdir(os.path.join(valor)):
            # Si representa a un directorio
            if treeview.row_expanded(path):
                # Si está expandida, colapsarla
                treeview.collapse_row(path)
            elif not treeview.row_expanded(path):
                # Si no está expandida, expandirla
                treeview.expand_to_path(path)
        elif os.path.isfile(os.path.join(valor)):
            # Si representa a un archivo
            pass

    def callback_collapsed(self, treeview, iter, path, user_param1):
        # Cuando se colapsa una fila, eliminar todos los hijos.
        while treeview.modelo.iter_n_children(iter):
            iterdelprimerhijo= treeview.modelo.iter_children(iter)
            treeview.modelo.remove(iterdelprimerhijo)
        # agregar un hijo vacío
        self.agregar_nada(iter)
        