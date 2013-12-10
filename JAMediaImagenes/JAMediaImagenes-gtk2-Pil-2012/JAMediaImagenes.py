#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

#   JAMediaImagenes.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

import os
import gtk
import gobject
import sys
import commands

from toolbar import ViewToolbar, EditToolbar
from ImageProcess import ImageProcessor

DIRECTORIO_BASE = os.path.dirname(__file__)
ICONOS = os.path.join(DIRECTORIO_BASE, "iconos/")


class JAMediaImagenes(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self)

        self.set_title("JAMedia Imágenes")
        self.set_icon_from_file(os.path.join(ICONOS, "JAMediaImagenes.png"))
        self.set_resizable(True)
        self.set_size_request(800, 600)
        self.set_position(gtk.WIN_POS_CENTER)
        #self.modify_bg(gtk.STATE_NORMAL, MG.BACKGROUND)

        self.view = None

        self.layout()

        self.connect("delete_event", self.delete_event)

    def layout(self):

        caja = gtk.VBox()
        self.view = ImageProcessor()
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add_with_viewport(self.view)

        view_toolbar = ViewToolbar()
        view_toolbar.connect('abrir_archivo', self.abrir_archivo)
        view_toolbar.connect('guardar_archivo', self.guardar_archivo)
        view_toolbar.connect('zoom_in', self.zoom_in)
        view_toolbar.connect('zoom_out', self.zoom_out)
        view_toolbar.connect('zoom_to_fit', self.zoom_tofit)
        view_toolbar.connect('rotate_clockwise', self.rotate_anticlockwise)
        view_toolbar.connect('rotate_anticlockwise', self.rotate_clockwise)
        view_toolbar.connect('undo', self.undo)
        view_toolbar.connect('redo', self.redo)
        view_toolbar.connect('cam_cb', self.fotografiar)
        view_toolbar.show()
        edit_toolbar = EditToolbar()
        edit_toolbar.connect('grey', self.view.grey)
        edit_toolbar.connect('blur', self.view.image_Blur)
        edit_toolbar.connect('transpose', self.view.image_Transpose)
        edit_toolbar.connect('contour', self.view.image_Contour)
        edit_toolbar.connect('finedges', self.view.image_Finedges)
        edit_toolbar.connect('solarize', self.view.image_Solarize)
        edit_toolbar.connect('invert', self.view.image_Invert)
        edit_toolbar.connect('ambross', self.view.image_Ambross)
        edit_toolbar.connect('sharpen', self.view.image_Sharpen)
        edit_toolbar.show()

        for toolbar in [view_toolbar, edit_toolbar]:
            caja.pack_start(toolbar, False, False, 0)

        caja.pack_start(sw, True, True, 0)

        self.add(caja)
        self.show_all()

    def delete_event(self, widget, event, data=None):

        sys.exit(0)
        return False

    def fotografiar(self, button):

        archivo = "/tmp/photo.jpg"
        #photocmd = "v4l2src ! ffmpegcolorspace !
        # jpegenc ! filesink location=%s" % (archivo)
        #pipeline = gst.parse_launch (photocmd)
        #pipeline.set_state(gst.STATE_PLAYING)
        #time.sleep(3)
        #pipeline.set_state(gst.STATE_NULL)
        comando = 'gst-launch-0.10 v4l2src ! ffmpegcolorspace ! pngenc ! filesink location=%s' % (archivo)
        commands.getoutput(comando)
        self.view.set_pixbuf(gtk.gdk.pixbuf_new_from_file(archivo))

    def undo(self, button):
        self.view.image_undo()

    def redo(self, button):
        self.view.image_redo()

    def zoom_in(self, button):
        self.view.zoom_in()

    def zoom_out(self, button):
        self.view.zoom_out()

    def zoom_tofit(self, button):
        self.view.set_zoom(1)

    def rotate_anticlockwise(self, button):
        self.view.set_angulo(-1)

    def rotate_clockwise(self, button):
        self.view.set_angulo(1)

    def abrir_archivo(self, button):
        selector = Selector_de_Archivos(self)
        selector.connect('abrir_archivo', self.load)

    def guardar_archivo(self, button):

        if not self.view.pixbufs_stack:
            return

        selector = Selector_de_Directorio(self)
        selector.connect('guardar_archivo', self.save)

    def load(self, widget=None, senial=None):
        self.view.set_pixbuf(gtk.gdk.pixbuf_new_from_file(senial))

    def save(self, widget=None, senial=None):
        self.view.guardar_archivo(senial)


class Selector_de_Archivos (gtk.FileChooserDialog):

    __gsignals__ = {
    'abrir_archivo': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([gobject.TYPE_STRING, ]))}

    def __init__(self, ventana):

        gtk.FileChooserDialog.__init__(self,
            title="Abrir Archivos de Imágenes", parent=ventana,
            action=gtk.FILE_CHOOSER_ACTION_OPEN)

        self.set_default_size(640, 480)
        self.resize(640, 480)
        self.set_select_multiple(False)

        # extras
        hbox = gtk.HBox()
        boton_abrir = gtk.Button("Abrir")
        boton_salir = gtk.Button("Salir")
        hbox.pack_end(boton_salir, True, True, 5)
        hbox.pack_end(boton_abrir, True, True, 5)
        self.set_extra_widget(hbox)

        filter = gtk.FileFilter()
        filter.set_name("Imagenes")
        filter.add_mime_type("image/*")
        self.add_filter(filter)

        # Callbacks
        boton_salir.connect("clicked", self.salir)
        boton_abrir.connect("clicked", self.abrir)

        self.show_all()
        self.resize(640, 480)

    def abrir(self, widget):

        archivo = self.get_filename()

        if not archivo:
            return self.salir(None)

        if os.path.exists(archivo):
            if os.path.isfile(archivo):
                    self.emit('abrir_archivo', archivo)

        self.salir(None)

    def salir(self, widget):
        self.destroy()


class Selector_de_Directorio (gtk.FileChooserDialog):

    __gsignals__ = {
    'guardar_archivo': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([gobject.TYPE_STRING, ]))}

    def __init__(self, ventana):

        gtk.FileChooserDialog.__init__(self,
            title="Guardar Imagen", parent=ventana,
            action=gtk.FILE_CHOOSER_ACTION_SAVE)

        self.set_default_size(640, 480)
        self.resize(640, 480)

        # extras
        hbox = gtk.HBox()
        boton_abrir = gtk.Button("Guardar")
        boton_salir = gtk.Button("Salir")
        hbox.pack_end(boton_salir, True, True, 5)
        hbox.pack_end(boton_abrir, True, True, 5)
        self.set_extra_widget(hbox)

        filter = gtk.FileFilter()
        filter.set_name("Imagenes")
        filter.add_mime_type("image/*")
        self.add_filter(filter)

        # Callbacks
        boton_salir.connect("clicked", self.salir)
        boton_abrir.connect("clicked", self.guardar)

        self.show_all()
        self.resize(640, 480)

    def guardar(self, widget):

        archivo = self.get_filename()

        if not archivo:
            return self.salir(None)

        self.emit('guardar_archivo', archivo)
        self.salir(None)

    def salir(self, widget):
        self.destroy()


if __name__ == "__main__":
    JAMediaImagenes()
    gtk.main()
