#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Preview.py por:
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

import gtk, pygtk, pango, os, mimetypes, commands, re

class Preview(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)
        self.directoriodeiconos= os.path.join(os.path.dirname(__file__), "Iconos")
        self.barra_info= self.crear_barra_info()
        self.pack_start(self.barra_info, True, True, 5)
        self.show_all()

    def control_preview(self, archivo):
        # controla lo que se muestra en el preview
        for child in self:
                self.remove(child)

        if not os.path.exists(archivo):
            self.pack_start(self.barra_info, True, True, 5)
            return

        formatos_de_imagen= ["TGA", "TIF", "PCX", "PNG", "GIF", "JPG", "jpg", "SVG", "Targa"]

        tipo_ = commands.getoutput("file %s" % (archivo))
        for formato in formatos_de_imagen:
            if re.search(formato, tipo_) and re.search("image", tipo_):
                self.crear_preview_imagen(archivo)
                return

        if re.search("text", tipo_) and not re.search("image", tipo_) and not re.search("XCF", tipo_):
            self.crear_preview_texto(archivo)
            return
        else:
            self.pack_start(self.barra_info, True, True, 5)

    def crear_preview_texto(self, archivo):
        # Muestra el texto en el preview
        scroll= gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        archivo_leido= open(archivo,"r")
        textbuffer= gtk.TextBuffer(table= None)

        contarlineas = 0
        for linea in archivo_leido.readlines():
            textbuffer.insert_at_cursor(linea) # Acá metemos el texto en el buffer
            contarlineas += 1
            if contarlineas > 20:
                textbuffer.insert_at_cursor("\n . . .")
                break
        archivo_leido.close()
        visordetexto = gtk.TextView(textbuffer)
        visordetexto.set_editable(False)
        scroll.add(visordetexto)
        self.pack_start(scroll, True, True)
        self.show_all()

    def crear_preview_imagen(self, archivo):
        # Muestra la imagen en el preview
        imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(archivo, 220, 220)
        imagen.set_from_pixbuf(pixbuf)
        self.pack_start(imagen, True, True)
        self.show_all()

    def crear_barra_info(self):
        caja = gtk.VBox()
        imagen1 = gtk.Image()
        imagen1.set_from_file(os.path.join(self.directoriodeiconos, "bandera_uruguay.png"))
        etiq_info1 = gtk.Label("JAMexplorer\nfdanesse@gmail.com\nhttp://sites.google.com/\nsite/sugaractivities/home")
        etiq_info1.modify_font(pango.FontDescription("purisa 10"))
        etiq_info1.set_justify(gtk.JUSTIFY_CENTER)
        etiq_info2 = gtk.Label("http://drupal.ceibaljam.org/\nwebmaster@ceibaljam.org")
        etiq_info2.modify_font(pango.FontDescription("purisa 10"))
        etiq_info2.set_justify(gtk.JUSTIFY_CENTER)
        imagen2 = gtk.Image()
        imagen2.set_from_file(os.path.join(self.directoriodeiconos, "ceibaljam.png"))
        caja.pack_start(imagen2, True, True, 5)
        caja.pack_start(etiq_info2, True, True, 5)
        caja.pack_start(imagen1, True, True, 5)
        caja.pack_start(etiq_info1, True, True, 5)
        caja.show_all()
        return caja
    