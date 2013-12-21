#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaWidgets.py por:
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

import os

import gtk
import gobject

from JAMediaGlobales import get_pixels
from JAMediaGlobales import get_separador
from JAMediaGlobales import get_boton
from JAMediaGlobales import get_color

JAMediaWidgetsBASE = os.path.dirname(__file__)


class JAMediaToolButton(gtk.ToolButton):
    """
    Toolbutton con drawingarea donde se
    dibuja una imagen con cairo.
    """

    def __init__(self, pixels=0):

        gtk.ToolButton.__init__(self)

        if not pixels:
            pixels = get_pixels(1)

        self.imagen = gtk.Image()
        self.set_icon_widget(self.imagen)
        self.imagen.show()

        self.set_size_request(pixels + 10, pixels + 10)
        self.pixels = pixels
        #self.pixels
        #self.imagen.set_size_request(pixels, pixels)

        self.show_all()

    def set_imagen(self, archivo=None, flip=False, rotacion=False):

        if archivo == None:
            pixbuf = None

        else:
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                os.path.join(archivo), self.pixels, self.pixels)

            if flip:
                pixbuf = pixbuf.flip(True)

            if rotacion:
                pixbuf = pixbuf.rotate_simple(rotacion)

        self.imagen.set_from_pixbuf(pixbuf)


class Imagen_Button(gtk.DrawingArea):
    """
    DrawingArea de JAMediaToolButton.
    """

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.pixbuf = None

        self.show_all()

    def do_expose_event(self, context):
        if not self.pixbuf:
            return

        import cairo

        rect = self.get_allocation()
        x, y, w, h = (rect.x, rect.y, rect.width, rect.height)
        ww, hh = self.pixbuf.get_width(), self.pixbuf.get_height()

        scaledPixbuf = self.pixbuf.scale_simple(
                w, h, gtk.gdk.INTERP_BILINEAR)

        surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            scaledPixbuf.get_width(),
            scaledPixbuf.get_height())

        gc = gtk.gdk.Drawable.new_gc(self.window)
        gc.set_rgb_fg_color(get_color("AMARILLO"))
        self.window.draw_pixbuf(scaledPixbuf)

        gc.set_source_surface(surface)
        gc.paint()

        return True

    def set_imagen(self, pixbuf):

        self.pixbuf = pixbuf
        self.queue_draw()


class JAMediaButton(gtk.EventBox):
    """
    Un Boton a medida.
    """

    __gsignals__ = {
    "clicked": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "click_derecho": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.cn = get_color("BLANCO")
        self.cs = get_color("AMARILLO")
        self.cc = get_color("NARANJA")
        self.text_color = get_color("NEGRO")
        self.colornormal = self.cn
        self.colorselect = self.cs
        self.colorclicked = self.cc

        self.set_visible_window(True)
        self.modify_bg(0, self.colornormal)
        self.modify_fg(0, self.text_color)
        self.set_border_width(1)

        self.estado_select = False

        self.add_events(
            gtk.gdk.BUTTON_PRESS_MASK |
            gtk.gdk.BUTTON_RELEASE_MASK |
            gtk.gdk.POINTER_MOTION_MASK |
            gtk.gdk.ENTER_NOTIFY_MASK |
            gtk.gdk.LEAVE_NOTIFY_MASK)

        self.connect("button_press_event", self.button_press)
        self.connect("button_release_event", self.__button_release)
        self.connect("enter-notify-event", self.__enter_notify_event)
        self.connect("leave-notify-event", self.__leave_notify_event)

        self.imagen = gtk.Image()
        self.add(self.imagen)

        self.show_all()

    def set_colores(self, colornormal=False,
        colorselect=False, colorclicked=False):

        if colornormal:
            self.cn = colornormal

        if colorselect:
            self.cs = colorselect

        if colorclicked:
            self.cc = colorclicked

        self.colornormal = self.cn
        self.colorselect = self.cs
        self.colorclicked = self.cc

        if self.estado_select:
            self.seleccionar()

        else:
            self.des_seleccionar()

    def seleccionar(self):
        """
        Marca como seleccionado
        """

        self.estado_select = True
        self.colornormal = self.cc
        self.colorselect = self.cc
        self.colorclicked = self.cc

        self.modify_bg(0, self.colornormal)

    def des_seleccionar(self):
        """
        Desmarca como seleccionado
        """

        self.estado_select = False

        self.colornormal = self.cn
        self.colorselect = self.cs
        self.colorclicked = self.cc

        self.modify_bg(0, self.colornormal)

    def __button_release(self, widget, event):

        self.modify_bg(0, self.colorselect)

    def __leave_notify_event(self, widget, event):

        self.modify_bg(0, self.colornormal)

    def __enter_notify_event(self, widget, event):

        self.modify_bg(0, self.colorselect)

    def button_press(self, widget, event):

        self.seleccionar()

        if event.button == 1:
            self.emit("clicked", event)

        elif event.button == 3:
            self.emit("click_derecho", event)

    def set_tooltip(self, texto):

        self.set_tooltip_text(texto)

    def set_label(self, texto):

        for child in self.get_children():
            child.destroy()

        label = gtk.Label(texto)
        label.show()
        self.add(label)

    def set_imagen(self, archivo):

        self.imagen.set_from_file(archivo)

    def set_tamanio(self, w, h):

        self.set_size_request(w, h)


class Visor(gtk.DrawingArea):
    """
    Visor generico para utilizar como area de
    reproduccion de videos o dibujar.
    """

    __gtype_name__ = 'Visor'

    __gsignals__ = {
    "ocultar_controles": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,))}

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.add_events(
            gtk.gdk.KEY_PRESS_MASK |
            gtk.gdk.KEY_RELEASE_MASK |
            gtk.gdk.POINTER_MOTION_MASK |
            gtk.gdk.POINTER_MOTION_HINT_MASK |
            gtk.gdk.BUTTON_MOTION_MASK |
            gtk.gdk.BUTTON_PRESS_MASK |
            gtk.gdk.BUTTON_RELEASE_MASK
        )

        self.modify_bg(0, get_color("NEGRO"))

        self.show_all()

        #self.connect("touch-event", self.__touch)

    def do_motion_notify_event(self, event):
        """
        Cuando se mueve el mouse sobre el visor.
        """

        # FIXME: Ocultar Controles interfiere con la
        # reproducción de videos en las xo
        #x, y = (int(event.x), int(event.y))
        #rect = self.get_allocation()
        #xx, yy, ww, hh = (rect.x, rect.y, rect.width, rect.height)

        #if x in range(ww - 60, ww) or y in range(yy, yy + 60) \
        #    or y in range(hh - 60, hh):
        #    self.emit("ocultar_controles", False)
        #    return

        #else:
        #    self.emit("ocultar_controles", True)
        #    return

        pass

class Lista(gtk.TreeView):
    """
    Lista generica.
    """

    __gsignals__ = {
    "nueva-seleccion": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self):

        gtk.TreeView.__init__(self)

        self.set_property("rules-hint", True)
        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.permitir_select = True
        self.valor_select = None

        self.modelo = gtk.ListStore(
            gtk.gdk.Pixbuf,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING)

        self.__setear_columnas()

        self.treeselection = self.get_selection()
        self.treeselection.set_select_function(self.__selecciones, self.modelo)

        self.set_model(self.modelo)
        self.show_all()

    '''
    def keypress(self, widget, event):
        # derecha 114 izquierda 113 suprimir 119
        # backspace 22 (en xo no existe suprimir)
        tecla = event.get_keycode()[1]
        model, iter = self.treeselection.get_selected()
        valor = self.modelo.get_value(iter, 2)
        path = self.modelo.get_path(iter)
        if tecla == 22:
            if self.row_expanded(path):
                self.collapse_row(path)
        elif tecla == 113:
            if self.row_expanded(path):
                self.collapse_row(path)
        elif tecla == 114:
            if not self.row_expanded(path):
                self.expand_to_path(path)
        elif tecla == 119:
            # suprimir
            print valor, path
        else:
            pass
        return False'''

    def __selecciones(self, path, column):
        """
        Cuando se selecciona un item en la lista.
        """

        if not self.permitir_select:
            return True

        # model y listore son ==
        iter = self.get_model().get_iter(path)
        valor = self.get_model().get_value(iter, 2)

        if self.valor_select != valor:
            #self.scroll_to_cell(self.get_model().get_path(iter))
            self.valor_select = valor
            self.emit('nueva-seleccion', self.valor_select)

        return True

    def __setear_columnas(self):

        self.append_column(self.__construir_columa_icono('', 0, True))
        self.append_column(self.__construir_columa('Nombre', 1, True))
        self.append_column(self.__construir_columa('', 2, False))

    def __construir_columa(self, text, index, visible):

        render = gtk.CellRendererText()

        columna = gtk.TreeViewColumn(text, render, text=index)
        columna.set_sort_column_id(index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', False)
        columna.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

        return columna

    def __construir_columa_icono(self, text, index, visible):

        render = gtk.CellRendererPixbuf()

        columna = gtk.TreeViewColumn(text, render, pixbuf=index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', False)
        columna.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

        return columna

    def limpiar(self):

        self.permitir_select = False
        self.modelo.clear()
        self.permitir_select = True

    def agregar_items(self, elementos):
        """
        Recibe lista de: [texto para mostrar, path oculto] y
        Comienza secuencia de agregado a la lista.
        """

        self.get_toplevel().set_sensitive(False)
        self.permitir_select = False

        gobject.idle_add(self.__ejecutar_agregar_elemento, elementos)

    def __ejecutar_agregar_elemento(self, elementos):
        """
        Agrega los items a la lista, uno a uno, actualizando.
        """

        if not elementos:
            self.permitir_select = True
            self.seleccionar_primero()
            self.get_toplevel().set_sensitive(True)
            return False

        texto, path = elementos[0]

        from JAMFileSystem import describe_uri
        from JAMFileSystem import describe_archivo

        descripcion = describe_uri(path)

        icono = None
        if descripcion:
            if descripcion[2]:
                # Es un Archivo
                tipo = describe_archivo(path)

                if 'video' in tipo:
                    icono = os.path.join(JAMediaWidgetsBASE,
                        "Iconos", "video.png")

                elif 'audio' in tipo:
                    icono = os.path.join(JAMediaWidgetsBASE,
                        "Iconos", "sonido.png")

                elif 'image' in tipo and not 'iso' in tipo:
                    icono = os.path.join(path)  # exige rendimiento
                    #icono = os.path.join(JAMediaWidgetsBASE,
                    #    "Iconos", "imagen.png")

                elif 'pdf' in tipo:
                    icono = os.path.join(JAMediaWidgetsBASE,
                        "Iconos", "pdf.png")

                elif 'zip' in tipo or 'rar' in tipo:
                    icono = os.path.join(JAMediaWidgetsBASE,
                        "Iconos", "zip.png")

                else:
                    icono = os.path.join(JAMediaWidgetsBASE,
                        "Iconos", "archivo.png")
        else:
            icono = os.path.join(JAMediaWidgetsBASE,
                "Iconos", "archivo.png")

        try:
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono,
                get_pixels(0.8), -1)
            self.modelo.append([pixbuf, texto, path])

        except:
            pass

        elementos.remove(elementos[0])

        gobject.idle_add(self.__ejecutar_agregar_elemento, elementos)

        return False

    def seleccionar_siguiente(self, widget=None):

        modelo, iter = self.treeselection.get_selected()

        try:
            self.treeselection.select_iter(modelo.iter_next(iter))

        except:
            self.seleccionar_primero()

        return False

    def seleccionar_anterior(self, widget=None):

        # FIXME: iter_previous no existe
        #modelo, iter = self.treeselection.get_selected()

        #try:
        #    self.treeselection.select_iter(modelo.iter_previous(iter))

        #except:
        #    self.seleccionar_ultimo()

        return False

    def seleccionar_primero(self, widget=None):

        self.treeselection.select_path(0)

    def seleccionar_ultimo(self, widget=None):

        model = self.get_model()
        item = model.get_iter_first()

        iter = None

        while item:
            iter = item
            item = model.iter_next(item)

        if iter:
            self.treeselection.select_iter(iter)
            #path = model.get_path(iter)


class ToolbarReproduccion(gtk.HBox):
    """
    Controles de reproduccion: play/pausa, stop, siguiente, atras.
    """

    __gsignals__ = {
    "activar": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.HBox.__init__(self)

        self.botonatras = JAMediaToolButton(pixels=get_pixels(0.8))
        archivo = os.path.join(JAMediaWidgetsBASE, "Iconos", "siguiente.png")
        self.botonatras.set_imagen(
            archivo=archivo,
            flip=True,
            rotacion=False)
        self.botonatras.set_tooltip_text("Anterior")
        self.botonatras.connect("clicked", self.__clickenatras)
        self.pack_start(self.botonatras, False, True, 0)

        self.botonplay = JAMediaToolButton(pixels=get_pixels(0.8))
        archivo = os.path.join(JAMediaWidgetsBASE, "Iconos", "play.png")
        self.botonplay.set_imagen(
            archivo=archivo,
            flip=False,
            rotacion=False)
        self.botonplay.set_tooltip_text("Reproducir")
        self.botonplay.connect("clicked", self.__clickenplay_pausa)
        self.pack_start(self.botonplay, False, True, 0)

        self.botonsiguiente = JAMediaToolButton(pixels=get_pixels(0.8))
        archivo = os.path.join(JAMediaWidgetsBASE, "Iconos", "siguiente.png")
        self.botonsiguiente.set_imagen(
            archivo=archivo,
            flip=False,
            rotacion=False)
        self.botonsiguiente.set_tooltip_text("Siguiente")
        self.botonsiguiente.connect("clicked", self.__clickensiguiente)
        self.pack_start(self.botonsiguiente, False, True, 0)

        self.botonstop = JAMediaToolButton(pixels=get_pixels(0.8))
        archivo = os.path.join(JAMediaWidgetsBASE, "Iconos", "stop.png")
        self.botonstop.set_imagen(
            archivo=archivo,
            flip=False,
            rotacion=False)
        self.botonstop.set_tooltip_text("Detener Reproducción")
        self.botonstop.connect("clicked", self.__clickenstop)
        self.pack_start(self.botonstop, False, True, 0)

        self.show_all()

    def set_paused(self):

        archivo = os.path.join(JAMediaWidgetsBASE, "Iconos", "play.png")

        self.botonplay.set_imagen(
            archivo=archivo,
            flip=False,
            rotacion=False)

    def set_playing(self):

        archivo = os.path.join(JAMediaWidgetsBASE, "Iconos", "pausa.png")

        self.botonplay.set_imagen(
            archivo=archivo,
            flip=False,
            rotacion=False)

    def __clickenstop(self, widget=None, event=None):

        self.emit("activar", "stop")

    def __clickenplay_pausa(self, widget=None, event=None):

        self.emit("activar", "pausa-play")

    def __clickenatras(self, widget=None, event=None):

        self.emit("activar", "atras")

    def __clickensiguiente(self, widget=None, event=None):

        self.emit("activar", "siguiente")


class BarraProgreso(gtk.EventBox):
    """
    Barra de progreso para mostrar estado de reproduccion.
    """

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, get_color("BLANCO"))
        self.escala = ProgressBar(
            gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0))

        self.valor = 0
        self.presion = False

        self.add(self.escala)
        self.show_all()

        self.escala.connect("button-press-event", self.buttonpressevent)
        self.escala.connect("button-release-event", self.buttonreleaseevent)
        self.escala.connect('user-set-value', self.__emit_valor)
        self.set_size_request(-1, get_pixels(1.2))

    def buttonpressevent(self, widget, event):

        self.presion = True

    def buttonreleaseevent(self, widget, event):

        self.presion = False

    def set_progress(self, valor=0):
        """
        El reproductor modifica la escala.
        """

        if not self.presion:
            if self.valor != valor:
                self.valor = valor
                self.escala.get_adjustment().set_value(valor)
                self.escala.queue_draw()

    def __emit_valor(self, widget, valor):
        """
        El usuario modifica la escala.
        """

        if self.valor != valor:
            self.valor = valor
            self.emit("user-set-value", valor)


class ProgressBar(gtk.HScale):

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self, ajuste):

        gtk.HScale.__init__(self, ajuste)

        self.ajuste = ajuste
        self.set_digits(0)
        #self.modify_bg(gtk.STATE_NORMAL, G.BLANCO)
        self.set_draw_value(False)

        self.x, self.y, self.w, self.h = (0, 0, 200, 40)
        self.borde, self.ancho = (15, 10)

        icono = os.path.join(JAMediaWidgetsBASE,
            "Iconos", "iconplay.png")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            icono, get_pixels(0.8), get_pixels(0.8))
        self.pixbuf = pixbuf.rotate_simple(
            gtk.gdk.PIXBUF_ROTATE_COUNTERCLOCKWISE)

        self.connect("expose_event", self.expose)
        self.connect("size-allocate", self.size_allocate)

    def do_motion_notify_event(self, event):
        """
        Cuando el usuario se desplaza por la barra de progreso.
        Se emite el valor en % (float).
        """

        if event.state == gtk.gdk.MOD2_MASK | gtk.gdk.BUTTON1_MASK:

            rect = self.get_allocation()
            valor = float(event.x * 100 / rect.width)

            if valor >= 0.0 and valor <= 100.0:
                self.ajuste.set_value(valor)
                self.queue_draw()
                self.emit("user-set-value", valor)

    def expose(self, widget, event):

        x, y, w, h = (self.x, self.y, self.w, self.h)
        ancho, borde = (self.ancho, self.borde)

        gc = gtk.gdk.Drawable.new_gc(self.window)

        gc.set_rgb_fg_color(get_color("BLANCO"))
        self.window.draw_rectangle(gc, True, x, y, w, h)

        gc.set_rgb_fg_color(get_color("AMARILLO"))
        ww = w - borde * 2
        xx = x + w / 2 - ww / 2
        hh = ancho
        yy = y + h / 2 - ancho / 2
        self.window.draw_rectangle(gc, True, xx, yy, ww, hh)

        anchoimagen, altoimagen = (self.pixbuf.get_width(),
            self.pixbuf.get_height())
        ximagen = int((xx - anchoimagen / 2) + self.get_value() * (
            ww / (self.ajuste.upper - self.ajuste.lower)))
        yimagen = yy + hh / 2 - altoimagen / 2

        gc.set_rgb_fg_color(get_color("NARANJA"))
        self.window.draw_rectangle(gc, True, xx, yy, ximagen, hh)

        gc.set_rgb_fg_color(get_color("NEGRO"))
        self.window.draw_rectangle(gc, False, xx, yy, ww, hh)

        self.window.draw_pixbuf(gc, self.pixbuf, 0, 0, ximagen, yimagen,
            anchoimagen, altoimagen, gtk.gdk.RGB_DITHER_NORMAL, 0, 0)

        return True

    def size_allocate(self, widget, allocation):

        self.x, self.y, self.w, self.h = allocation
        return False


class ControlVolumen(gtk.VolumeButton):
    """
    Botón con escala para controlar el volúmen
    de reproducción en los reproductores.
    """

    __gsignals__ = {
    "volumen": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    def __init__(self):

        gtk.VolumeButton.__init__(self)

        self.connect("value-changed", self.value_changed)
        self.show_all()

    def value_changed(self, widget, valor):
        """
        Cuando el usuario desplaza la escala
        emite el valor en float de 0.0 a 1.0.
        """

        self.emit('volumen', valor)


class ToolbarAccion(gtk.Toolbar):
    """
    Toolbar para que el usuario confirme las
    acciones que se realizan sobre items que se
    seleccionan en la lista de reproduccion.
    (Borrar, mover, copiar, quitar).
    """

    __gsignals__ = {
    "Grabar": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "accion-stream": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_STRING))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_color("NEGRO"))
        self.modify_fg(0, get_color("BLANCO"))

        self.lista = None
        self.accion = None
        self.iter = None

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(JAMediaWidgetsBASE,
            "Iconos", "alejar.png")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        self.insert(boton, -1)

        item = gtk.ToolItem()
        item.set_expand(True)
        self.label = gtk.Label("")
        self.label.modify_fg(0, get_color("BLANCO"))
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        archivo = os.path.join(JAMediaWidgetsBASE,
            "Iconos", "acercar.png")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.__realizar_accion)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        self.show_all()

    def __realizar_accion(self, widget):
        """
        Ejecuta una accion sobre un archivo o streaming
        en la lista de reprucción cuando el usuario confirma.
        """

        from JAMediaGlobales import get_my_files_directory

        from JAMFileSystem import describe_acceso_uri
        from JAMFileSystem import copiar
        from JAMFileSystem import borrar
        from JAMFileSystem import mover

        uri = self.lista.modelo.get_value(self.iter, 2)

        if describe_acceso_uri(uri):
            if self.accion == "Quitar":
                self.lista.modelo.remove(self.iter)

            elif self.accion == "Copiar":
                if os.path.isfile(uri):
                    copiar(uri, get_my_files_directory())

            elif self.accion == "Borrar":
                if os.path.isfile(uri):
                    if borrar(uri):
                        self.lista.modelo.remove(self.iter)

            elif self.accion == "Mover":
                if os.path.isfile(uri):
                    if mover(uri, get_my_files_directory()):
                        self.lista.modelo.remove(self.iter)
        else:
            if self.accion == "Quitar":
                self.lista.modelo.remove(self.iter)

            elif self.accion == "Borrar":
                self.emit("accion-stream", "Borrar", uri)
                self.lista.modelo.remove(self.iter)

            elif self.accion == "Copiar":
                self.emit("accion-stream", "Copiar", uri)

            elif self.accion == "Mover":
                self.emit("accion-stream", "Mover", uri)
                self.lista.modelo.remove(self.iter)

            elif self.accion == "Grabar":
                self.emit("Grabar", uri)

        self.label.set_text("")
        self.lista = None
        self.accion = None
        self.iter = None
        self.hide()

    def set_accion(self, lista, accion, iter):
        """
        Configura una accion sobre un archivo o
        streaming y muestra toolbaraccion para que
        el usuario confirme o cancele dicha accion.
        """

        self.lista = lista
        self.accion = accion
        self.iter = iter

        if self.lista and self.accion and self.iter:
            uri = self.lista.modelo.get_value(self.iter, 2)
            texto = uri

            if os.path.exists(uri):
                texto = os.path.basename(uri)

            if len(texto) > 30:
                texto = str(texto[0:30]) + " . . . "

            self.label.set_text("¿%s?: %s" % (accion, texto))
            self.show_all()

    def cancelar(self, widget=None):
        """
        Cancela la accion configurada sobre
        un archivo o streaming en la lista de
        reproduccion.
        """

        self.label.set_text("")
        self.lista = None
        self.accion = None
        self.iter = None
        self.hide()


class ToolbarBalanceConfig(gtk.Table):
    """
    Toolbar de Configuración de Balance
    en Video. (Utilizado por JAMediaVideo).
    """

    __gsignals__ = {
    'valor': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_FLOAT, gobject.TYPE_STRING))}

    def __init__(self):

        gtk.Table.__init__(self, rows=5, columns=1, homogeneous=True)

        self.brillo = ToolbarcontrolValores("Brillo")
        self.contraste = ToolbarcontrolValores("Contraste")
        self.saturacion = ToolbarcontrolValores("Saturación")
        self.hue = ToolbarcontrolValores("Matíz")
        self.gamma = ToolbarcontrolValores("Gamma")

        self.attach(self.brillo, 0, 1, 0, 1)
        self.attach(self.contraste, 0, 1, 1, 2)
        self.attach(self.saturacion, 0, 1, 2, 3)
        self.attach(self.hue, 0, 1, 3, 4)
        self.attach(self.gamma, 0, 1, 4, 5)

        self.show_all()

        self.brillo.connect('valor', self.__emit_senial, 'brillo')
        self.contraste.connect('valor', self.__emit_senial, 'contraste')
        self.saturacion.connect('valor', self.__emit_senial, 'saturacion')
        self.hue.connect('valor', self.__emit_senial, 'hue')
        self.gamma.connect('valor', self.__emit_senial, 'gamma')

    def __emit_senial(self, widget, valor, tipo):
        """
        Emite valor, que representa un valor
        en % float y un valor tipo para:
            brillo - contraste - saturacion - hue - gamma
        """

        self.emit('valor', valor, tipo)

    def set_balance(self, brillo=None, contraste=None,
        saturacion=None, hue=None, gamma=None):
        """
        Setea las barras segun valores.
        """

        if saturacion != None:
            self.saturacion.set_progress(saturacion)

        if contraste != None:
            self.contraste.set_progress(contraste)

        if brillo != None:
            self.brillo.set_progress(brillo)

        if hue != None:
            self.hue.set_progress(hue)

        if gamma != None:
            self.gamma.set_progress(gamma)


class ToolbarcontrolValores(gtk.Toolbar):
    """
    Toolbar con escala para modificar
    valores de balance en video, utilizada
    por ToolbarBalanceConfig.
    """

    __gsignals__ = {
    'valor': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    def __init__(self, label):

        self.modify_bg(0, get_color("NEGRO"))
        self.modify_fg(0, get_color("BLANCO"))

        gtk.Toolbar.__init__(self)

        self.titulo = label

        self.escala = SlicerBalance()

        item = gtk.ToolItem()
        item.set_expand(True)

        self.frame = gtk.Frame()
        self.frame.set_label(self.titulo)
        self.frame.set_label_align(0.5, 1.0)
        self.frame.add(self.escala)
        self.frame.show()
        item.add(self.frame)
        self.insert(item, -1)

        self.show_all()

        self.escala.connect("user-set-value", self.__user_set_value)

    def __user_set_value(self, widget=None, valor=None):
        """
        Recibe la posicion en la barra de
        progreso (en % float), y re emite los valores.
        """

        self.emit('valor', valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))

    def set_progress(self, valor):
        """
        Establece valores en la escala.
        """

        self.escala.set_progress(valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))


class SlicerBalance(gtk.EventBox):
    """
    Barra deslizable para cambiar valores de Balance en Video.
    """

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.escala = BalanceBar(gtk.Adjustment(0.0, 0.0,
            101.0, 0.1, 1.0, 1.0))
        self.escala.set_size_request(-1, 30)
        self.add(self.escala)
        self.show_all()

        self.escala.connect('user-set-value', self.__emit_valor)

    def set_progress(self, valor=0.0):
        """
        El reproductor modifica la escala.
        """

        self.escala.ajuste.set_value(valor)
        self.escala.queue_draw()

    def __emit_valor(self, widget, valor):
        """
        El usuario modifica la escala.
        Y se emite la señal con el valor (% float).
        """

        self.emit("user-set-value", valor)


class BalanceBar(gtk.HScale):
    """
    Escala de SlicerBalance.
    """

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self, ajuste):

        gtk.HScale.__init__(self, ajuste)
        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)

        self.x, self.y, self.w, self.h = (0, 0, 200, 40)
        self.borde, self.ancho = (15, 10)

        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(JAMediaWidgetsBASE,
            "Iconos", "iconplay.png"), 25, 25)
        self.pixbuf = pixbuf.rotate_simple(
            gtk.gdk.PIXBUF_ROTATE_COUNTERCLOCKWISE)

        self.connect("expose_event", self.expose)
        self.connect("size-allocate", self.size_allocate)

    def do_motion_notify_event(self, event):
        """
        Cuando el usuario se desplaza por la barra de progreso.
        Se emite el valor en % (float).
        """

        if event.state == gtk.gdk.MOD2_MASK | gtk.gdk.BUTTON1_MASK:

            rect = self.get_allocation()
            valor = float(event.x * 100 / rect.width)

            if valor >= 0.0 and valor <= 100.0:
                self.ajuste.set_value(valor)
                self.queue_draw()
                self.emit("user-set-value", valor)

    def expose(self, widget, event):

        x, y, w, h = (self.x, self.y, self.w, self.h)
        ancho, borde = (self.ancho, self.borde)

        gc = gtk.gdk.Drawable.new_gc(self.window)
        gc.set_rgb_fg_color(get_color("AMARILLO"))

        ww = w - borde * 2
        xx = x + w / 2 - ww / 2
        hh = ancho
        yy = y + h / 2 - ancho / 2
        self.window.draw_rectangle(gc, True, xx, yy, ww, hh)

        anchoimagen, altoimagen = (
            self.pixbuf.get_width(), self.pixbuf.get_height())
        ximagen = int((xx - anchoimagen / 2) + self.get_value() * (
            ww / (self.ajuste.upper - self.ajuste.lower)))
        yimagen = yy + hh / 2 - altoimagen / 2

        gc.set_rgb_fg_color(get_color("NARANJA"))
        self.window.draw_rectangle(gc, True, xx, yy, ximagen, hh)

        gc.set_rgb_fg_color(get_color("NEGRO"))
        self.window.draw_rectangle(gc, False, xx, yy, ww, hh)

        self.window.draw_pixbuf(gc, self.pixbuf, 0, 0,
            ximagen, yimagen, anchoimagen,
            altoimagen, gtk.gdk.RGB_DITHER_NORMAL, 0, 0)

        return True

    def size_allocate(self, widget, allocation):
        self.x, self.y, self.w, self.h = allocation
        return False


class ItemSwitch(gtk.Frame):

    __gsignals__ = {
    "switch": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,))}

    def __init__(self, text):

        gtk.Frame.__init__(self)

        self.set_label(text)
        self.set_label_align(0.5, 1.0)

        self.switch = gtk.CheckButton()
        self.switch.connect('button-press-event', self.__emit_switch)

        self.add(self.switch)
        self.show_all()

    def __emit_switch(self, widget, senial):
        """
        Emite la señal switch con el valor correspondiente.
        """

        self.emit("switch", not widget.get_active())


class ToolbarSalir(gtk.Toolbar):
    """
    Toolbar para confirmar salir de la aplicación.
    """

    __gsignals__ = {
    "salir": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_color("NEGRO"))
        self.modify_fg(0, get_color("BLANCO"))

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(JAMediaWidgetsBASE,
            "Iconos", "alejar.png")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.label = gtk.Label("")
        self.label.modify_fg(0, get_color("BLANCO"))
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(JAMediaWidgetsBASE,
            "Iconos", "acercar.png")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.__emit_salir)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        self.show_all()

    def run(self, nombre_aplicacion):
        """
        La toolbar se muestra y espera confirmación
        del usuario.
        """

        self.label.set_text("Salir de %s ?" % (nombre_aplicacion))
        self.show()

    def __emit_salir(self, widget):
        """
        Confirma Salir de la aplicación.
        """

        self.cancelar()
        self.emit('salir')

    def cancelar(self, widget=None):
        """
        Cancela salir de la aplicación.
        """

        self.label.set_text("")
        self.hide()


class WidgetsGstreamerEfectos(gtk.Frame):
    """
    Frame exterior de Contenedor de widgets que
    representan efectos de video para gstreamer.
    """

    __gsignals__ = {
    "click_efecto": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    'configurar_efecto': (
        gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_STRING, gobject.TYPE_STRING,
        gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.Frame.__init__(self)

        self.modify_bg(0, get_color("BLANCO"))

        self.set_label(" Efectos: ")
        self.set_label_align(0.0, 0.5)
        self.gstreamer_efectos = GstreamerVideoEfectos()
        self.gstreamer_efectos.connect('agregar_efecto',
            self.__emit_click_efecto)
        self.gstreamer_efectos.connect('configurar_efecto',
            self.__configurar_efecto)
        self.add(self.gstreamer_efectos)

        self.show_all()

    def __configurar_efecto(self, widget, efecto, propiedad, valor):

        self.emit('configurar_efecto', efecto, propiedad, valor)

    def __emit_click_efecto(self, widget, nombre_efecto):

        self.emit('click_efecto', nombre_efecto)

    def cargar_efectos(self, elementos):
        """
        Agrega los widgets de efectos.
        """

        self.gstreamer_efectos.cargar_efectos(elementos)

    def des_seleccionar_efecto(self, nombre):

        self.gstreamer_efectos.des_seleccionar_efecto(nombre)

    def seleccionar_efecto(self, nombre):

        self.gstreamer_efectos.seleccionar_efecto(nombre)


class GstreamerVideoEfectos(gtk.VBox):
    """
    Contenedor de widgets que representan
    efectos de video para gstreamer.
    """

    __gsignals__ = {
    'agregar_efecto': (
        gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_STRING,)),
    'configurar_efecto': (
        gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_STRING, gobject.TYPE_STRING,
        gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.VBox.__init__(self)

        self.show_all()

    def cargar_efectos(self, elementos):
        """
        Agrega los items a la lista, uno a uno, actualizando.
        """

        if not elementos:
            return False

        nombre = elementos[0]
        # Los efectos se definen en globales
        # pero hay que ver si están instalados.
        import commands
        datos = commands.getoutput('gst-inspect-0.10 %s' % (nombre))

        # if 'gst-plugins-good' in datos and \
        #    ('Filter/Effect/Video' in datos or \
        # 'Transform/Effect/Video' in datos):
        if 'Filter/Effect/Video' in datos or 'Transform/Effect/Video' in datos:
            botonefecto = Efecto_widget_Config(nombre)
            botonefecto.connect('agregar_efecto', self.agregar_efecto)
            botonefecto.connect('configurar_efecto', self.__configurar_efecto)
            self.pack_start(botonefecto, False, False, 10)

        self.show_all()
        elementos.remove(elementos[0])
        gobject.idle_add(self.cargar_efectos, elementos)

    def __configurar_efecto(self, widget, efecto, propiedad, valor):

        self.emit('configurar_efecto', efecto, propiedad, valor)

    def agregar_efecto(self, widget, nombre_efecto):
        """
        Cuando se hace click en el botón del efecto
        se envía la señal 'agregar-efecto'.
        """

        self.emit('agregar_efecto', nombre_efecto)

    '''
    def efecto_click_derecho(self, widget, void):

        #print "Click", widget.get_tooltip_text(),
        #"Select", widget.estado_select
        pass'''

    def des_seleccionar_efecto(self, nombre):

        efectos = self.get_children()

        for efecto in efectos:

            if efecto.botonefecto.get_tooltip_text() == nombre:
                efecto.des_seleccionar()
                return

    def seleccionar_efecto(self, nombre):

        efectos = self.get_children()

        for efecto in efectos:

            if efecto.botonefecto.get_tooltip_text() == nombre:
                efecto.seleccionar()
                return

'''
class WidgetsGstreamerAudioVisualizador(gtk.Frame):
    """
    Frame exterior de Contenedor de widgets que
    representan visualizadores de audio para gstreamer.
    """

    __gsignals__ = {
    "click_efecto":(gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    'configurar_efecto':(
        gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.Frame.__init__(self)

        self.set_label(" Visualizadores: ")
        self.set_label_align(0.0, 0.5)
        self.gstreamer_efectos = GstreamerAudioVisualizador()
        self.gstreamer_efectos.connect('agregar_efecto',
            self.__emit_click_efecto)
        self.gstreamer_efectos.connect('configurar_efecto',
            self.__configurar_efecto)
        self.add(self.gstreamer_efectos)

        self.show_all()

    def __configurar_efecto(self, widget, efecto, propiedad, valor):

        self.emit('configurar_efecto', efecto, propiedad, valor)

    def __emit_click_efecto(self, widget, nombre_efecto):

        # HACK: Deselecciona todos los demás visualizadores
        # ya que solo se puede aplicar uno a la vez a diferencia
        # de los efectos de video que pueden encolarse.
        efectos = self.gstreamer_efectos.get_children()
        for efecto in efectos:
            if not efecto.botonefecto.get_tooltip_text() == nombre_efecto:
                efecto.des_seleccionar()

        self.emit('click_efecto', nombre_efecto)

    def cargar_efectos(self, elementos):
        """
        Agrega los widgets de efectos.
        """

        self.gstreamer_efectos.cargar_efectos(elementos)

        return False

    def des_seleccionar_efecto(self, nombre):

        self.gstreamer_efectos.des_seleccionar_efecto(nombre)

    def seleccionar_efecto(self, nombre):

        self.gstreamer_efectos.seleccionar_efecto(nombre)


class GstreamerAudioVisualizador(GstreamerVideoEfectos):
    """
    Contenedor de widgets que representan
    visualizadores de audio para gstreamer.
    """

    def __init__(self):

        GstreamerVideoEfectos.__init__(self)

        self.set_property('orientation', gtk.ORIENTATION_HORIZONTAL)
        self.show_all()

    def cargar_efectos(self, elementos):
        """
        Agrega los items a la lista, uno a uno, actualizando.
        """

        if not elementos:
            return False

        nombre = elementos[0]
        # Los efectos se definen en globales pero
        # hay que ver si están instalados.
        import commands
        datos = commands.getoutput('gst-inspect-1.0 %s' % (nombre))

        #if 'gst-plugins-good' in datos and 'Visualization' in datos:
        if 'Visualization' in datos:
            botonefecto = Efecto_widget_Config(nombre)
            botonefecto.connect('agregar_efecto', self.agregar_efecto)
            # FIXME: Agregar configuracion para visualizador
            #botonefecto.connect('configurar_efecto', self.configurar_efecto)
            self.pack_start(botonefecto, False, False, 1)

        self.show_all()
        elementos.remove(elementos[0])
        gobject.idle_add(self.cargar_efectos, elementos)
'''


class Efecto_widget_Config(gtk.VBox):
    """
    Contiene el botón para el efecto y los
    controles de configuración del mismo.
    """

    __gsignals__ = {
    'agregar_efecto': (
        gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_STRING,)),
    'configurar_efecto': (
        gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    def __init__(self, nombre):

        gtk.VBox.__init__(self)

        self.botonefecto = JAMediaButton()
        self.botonefecto.connect('clicked', self.__efecto_click)
        #self.botonefecto.connect('click_derecho', self.__efecto_click_derecho)
        self.botonefecto.set_tooltip(nombre)
        lado = get_pixels(1.0)
        self.botonefecto.set_tamanio(lado, lado)

        archivo = os.path.join(JAMediaWidgetsBASE,
            "Iconos", '%s.png' % (nombre))

        if not os.path.exists(archivo):
            archivo = os.path.join(JAMediaWidgetsBASE,
                "Iconos", '%s.png' % ('configurar'))

        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(archivo, lado, lado)
        self.botonefecto.imagen.set_from_pixbuf(pixbuf)

        frame = gtk.Frame()
        frame.set_label(nombre)
        frame.set_label_align(0.5, 1.0)
        frame.add(self.botonefecto)

        self.pack_start(frame, False, False, 1)

        from JAMediaGlobales import get_widget_config_efecto

        self.widget_config = get_widget_config_efecto(nombre)

        if self.widget_config:
            self.widget_config.connect('propiedad', self.__set_efecto)
            frame = gtk.Frame()
            frame.set_label("Configuración")
            frame.set_label_align(0.5, 1.0)
            frame.add(self.widget_config)

            box = gtk.EventBox()
            box.modify_bg(0, get_color("NEGRO"))
            box.modify_fg(0, get_color("BLANCO"))
            box.add(frame)

            self.pack_start(box, False, False, 1)

        self.show_all()
        # y ocultar configuraciones.

    def __set_efecto(self, widget, propiedad, valor):

        self.emit('configurar_efecto',
            self.botonefecto.get_tooltip_text(), propiedad, valor)

    def __efecto_click(self, widget, void):
        """
        Cuando se hace click en el botón del efecto
        se envía la señal 'agregar-efecto'.
        """

        self.emit('agregar_efecto', widget.get_tooltip_text())

    '''
    def efecto_click_derecho(self, widget, void):

        #print "Click", widget.get_tooltip_text(),
        #"Select", widget.estado_select
        pass'''

    def seleccionar(self):
        """
        Marca como seleccionado
        """

        self.botonefecto.seleccionar()
        # y mostrar configuracion

    def des_seleccionar(self):
        """
        Desmarca como seleccionado
        """

        self.botonefecto.des_seleccionar()
        #y ocultar configuracion


class MouseSpeedDetector(gobject.GObject):
    """
    Verifica posición y moviemiento del mouse.
    estado puede ser:
        fuera       (está fuera de la ventana según self.parent)
        moviendose
        detenido
    """

    __gsignals__ = {
        'estado': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self, parent):

        gobject.GObject.__init__(self)

        self.parent = parent

        self.actualizador = False
        self.mouse_pos = (0, 0)

    def __handler(self):
        """
        Emite la señal de estado cada 60 segundos.
        """

        posx, posy, ww, hh = self.parent.get_allocation()

        if posx > 0 and posy > 0:
            if posx != self.mouse_pos[0] or posy != self.mouse_pos[1]:
                self.mouse_pos = (posx, posy)
                self.emit("estado", "moviendose")

            else:
                self.emit("estado", "detenido")

        else:
            self.emit("estado", "fuera")

        return True

    def new_handler(self, reset):
        """
        Resetea el controlador o lo termina según reset.
        """

        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False

        if reset:
            self.actualizador = gobject.timeout_add(1000, self.__handler)
