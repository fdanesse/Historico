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

#   toolbar.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

import gtk
import gobject
import os

DIRECTORIO_BASE = os.path.dirname(__file__)
ICONOS = os.path.join(DIRECTORIO_BASE, "iconos/")


class ViewToolbar(gtk.Toolbar):

    __gtype_name__ = 'ViewToolbar'

    __gsignals__ = {
    'abrir_archivo': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'guardar_archivo': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'zoom_in': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'zoom_out': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'zoom_to_fit': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'rotate_clockwise': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'rotate_anticlockwise': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'undo': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'redo': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'cam_cb': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([]))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = True
        separator.set_size_request(0, -1)
        separator.set_expand(False)
        self.insert(separator, -1)

        open_button = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'iconplay.png'), 32, 32)
        pixbuf = pixbuf.rotate_simple(
            gtk.gdk.PIXBUF_ROTATE_COUNTERCLOCKWISE)
        imagen.set_from_pixbuf(pixbuf)
        open_button.set_icon_widget(imagen)
        imagen.show()
        open_button.connect('clicked', self.abrir_archivo)
        self.insert(open_button, -1)
        open_button.show()

        save_button = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'iconplay.png'), 32, 32)
        pixbuf = pixbuf.rotate_simple(
            gtk.gdk.PIXBUF_ROTATE_CLOCKWISE)
        imagen.set_from_pixbuf(pixbuf)
        save_button.set_icon_widget(imagen)
        imagen.show()
        save_button.connect('clicked', self.guardar_archivo)
        self.insert(save_button, -1)
        save_button.show()

        separator = gtk.SeparatorToolItem()
        separator.props.draw = True
        separator.set_size_request(0, -1)
        separator.set_expand(False)
        self.insert(separator, -1)

        zoom_out_button = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'alejar.png'), 32, 32)
        imagen.set_from_pixbuf(pixbuf)
        zoom_out_button.set_icon_widget(imagen)
        imagen.show()
        zoom_out_button.connect('clicked', self.zoom_out_cb)
        self.insert(zoom_out_button, -1)
        zoom_out_button.show()

        zoom_in_button = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'acercar.png'), 32, 32)
        imagen.set_from_pixbuf(pixbuf)
        zoom_in_button.set_icon_widget(imagen)
        imagen.show()
        zoom_in_button.connect('clicked', self.zoom_in_cb)
        self.insert(zoom_in_button, -1)
        zoom_in_button.show()

        zoom_tofit_button = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'escalaoriginal.png'), 32, 32)
        imagen.set_from_pixbuf(pixbuf)
        zoom_tofit_button.set_icon_widget(imagen)
        imagen.show()
        zoom_tofit_button.connect('clicked', self.zoom_to_fit_cb)
        self.insert(zoom_tofit_button, -1)
        zoom_tofit_button.show()

        separator = gtk.SeparatorToolItem()
        separator.props.draw = True
        separator.set_size_request(0, -1)
        separator.set_expand(False)
        self.insert(separator, -1)

        rotate_anticlockwise_button = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'rotar.png'), 32, 32)
        imagen.set_from_pixbuf(pixbuf)
        rotate_anticlockwise_button.set_icon_widget(imagen)
        imagen.show()
        rotate_anticlockwise_button.connect('clicked',
            self.rotate_anticlockwise_cb)
        self.insert(rotate_anticlockwise_button, -1)
        rotate_anticlockwise_button.show()

        rotate_clockwise_button = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'rotar.png'), 32, 32).flip(True)
        imagen.set_from_pixbuf(pixbuf)
        rotate_clockwise_button.set_icon_widget(imagen)
        imagen.show()
        rotate_clockwise_button.connect('clicked',
            self.rotate_clockwise_cb)
        self.insert(rotate_clockwise_button, -1)
        rotate_clockwise_button.show()

        separator = gtk.SeparatorToolItem()
        separator.props.draw = True
        separator.set_size_request(0, -1)
        separator.set_expand(False)
        self.insert(separator, -1)

        undo_button = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'deshacer.png'), 32, 32)
        imagen.set_from_pixbuf(pixbuf)
        undo_button.set_icon_widget(imagen)
        imagen.show()
        undo_button.connect('clicked', self.undo_cb)
        self.insert(undo_button, -1)
        undo_button.show()

        redo_button = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'deshacer.png'), 32, 32).flip(True)
        imagen.set_from_pixbuf(pixbuf)
        redo_button.set_icon_widget(imagen)
        imagen.show()
        redo_button.connect('clicked', self.redo_cb)
        self.insert(redo_button, -1)
        redo_button.show()

        separator = gtk.SeparatorToolItem()
        separator.props.draw = True
        separator.set_size_request(0, -1)
        separator.set_expand(False)
        self.insert(separator, -1)

        cam_button = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'foto.png'), 32, 32)
        imagen.set_from_pixbuf(pixbuf)
        cam_button.set_icon_widget(imagen)
        imagen.show()
        cam_button.connect('clicked', self.cam_cb)
        self.insert(cam_button, -1)
        cam_button.show()

        separator = gtk.SeparatorToolItem()
        separator.props.draw = True
        separator.set_size_request(0, -1)
        separator.set_expand(False)
        self.insert(separator, -1)

    def abrir_archivo(self, button):
        self.emit('abrir_archivo')

    def guardar_archivo(self, button):
        self.emit('guardar_archivo')

    def zoom_in_cb(self, button):
        self.emit('zoom_in')

    def zoom_out_cb(self, button):
        self.emit('zoom_out')

    def zoom_to_fit_cb(self, button):
        self.emit('zoom_to_fit')

    def rotate_clockwise_cb(self, button):
        self.emit('rotate_clockwise')

    def rotate_anticlockwise_cb(self, button):
        self.emit('rotate_anticlockwise')

    def undo_cb(self, button):
        self.emit('undo')

    def redo_cb(self, button):
        self.emit('redo')

    def cam_cb(self, button):
        self.emit('cam_cb')


class EditToolbar(gtk.Toolbar):

    __gtype_name__ = 'EditToolbar'

    __gsignals__ = {
    'grey': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'blur': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'transpose': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'contour': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'text': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'finedges': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'solarize': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'invert': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'ambross': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'left_top': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'right_top': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'left_bottom': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'right_bottom': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([])),
    'sharpen': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ([]))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = True
        separator.set_size_request(0, -1)
        separator.set_expand(False)
        self.insert(separator, -1)

        grey = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'grey.png'), 32, 32)
        imagen.set_from_pixbuf(pixbuf)
        grey.set_icon_widget(imagen)
        imagen.show()
        grey.connect('clicked', self.grey_cb)
        self.insert(grey, -1)
        grey.show()

        blur = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'blur.png'), 32, 32)
        imagen.set_from_pixbuf(pixbuf)
        blur.set_icon_widget(imagen)
        imagen.show()
        blur.connect('clicked', self.blur_cb)
        self.insert(blur, -1)
        blur.show()

        button_espejar = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'original.png'), 32, 32).flip(True)
        imagen.set_from_pixbuf(pixbuf)
        button_espejar.set_icon_widget(imagen)
        imagen.show()
        button_espejar.connect('clicked', self.transpose_cb)
        self.insert(button_espejar, -1)
        button_espejar.show()

        contour = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'contour.png'), 32, 32)
        imagen.set_from_pixbuf(pixbuf)
        contour.set_icon_widget(imagen)
        imagen.show()
        contour.connect('clicked', self.contour_cb)
        self.insert(contour, -1)
        contour.show()

        finedges = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'finedges.png'), 32, 32)
        imagen.set_from_pixbuf(pixbuf)
        finedges.set_icon_widget(imagen)
        imagen.show()
        finedges.connect('clicked', self.finedges_cb)
        self.insert(finedges, -1)
        finedges.show()

        solarize = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'solarize.png'), 32, 32)
        imagen.set_from_pixbuf(pixbuf)
        solarize.set_icon_widget(imagen)
        imagen.show()
        solarize.connect('clicked', self.solarize_cb)
        self.insert(solarize, -1)
        solarize.show()

        invert = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'invert.png'), 32, 32)
        imagen.set_from_pixbuf(pixbuf)
        invert.set_icon_widget(imagen)
        imagen.show()
        invert.connect('clicked', self.invert_cb)
        self.insert(invert, -1)
        invert.show()

        ambross = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'ambross.png'), 32, 32)
        imagen.set_from_pixbuf(pixbuf)
        ambross.set_icon_widget(imagen)
        imagen.show()
        ambross.connect('clicked', self.ambross_cb)
        self.insert(ambross, -1)
        ambross.show()

        sharpen = gtk.ToolButton()
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS, 'sharpen.png'), 32, 32)
        imagen.set_from_pixbuf(pixbuf)
        sharpen.set_icon_widget(imagen)
        imagen.show()
        sharpen.connect('clicked', self.sharpen_cb)
        self.insert(sharpen, -1)
        sharpen.show()

        separator = gtk.SeparatorToolItem()
        separator.props.draw = True
        separator.set_size_request(0, -1)
        separator.set_expand(False)
        self.insert(separator, -1)

    def grey_cb(self, button):
        self.emit('grey')

    def blur_cb(self, button):
        self.emit('blur')

    def transpose_cb(self, button):
        self.emit('transpose')

    def contour_cb(self, button):
        self.emit('contour')

    def finedges_cb(self, button):
        self.emit('finedges')

    def solarize_cb(self, button):
        self.emit('solarize')

    def invert_cb(self, button):
        self.emit('invert')

    def ambross_cb(self, button):
        self.emit('ambross')

    def sharpen_cb(self, button):
        self.emit('sharpen')

'''
class IPButton(gtk.ToolButton):
    def __init__(self, archivo):
        gtk.ToolButton.__init__(self)
        imagen = gtk.Image()
        pixbuf= gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONOS,archivo), 32, 32)
        imagen.set_from_pixbuf(pixbuf)
        self.set_icon_widget(imagen)
        imagen.show()
        self.show()

class IPButtonStock(gtk.ToolButton):
    def __init__(self, nombre):
        gtk.ToolButton.__init__(self)
        imagen = gtk.Image()
        imagen.set_from_stock(nombre, gtk.ICON_SIZE_BUTTON)
        self.set_icon_widget(imagen)
        imagen.show()
        self.show()'''
