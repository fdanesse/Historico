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

#   ImageProcessor.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay
#   Basado en código de: Keshav Sharma <keshav7890@gmail.com> & Vaibhav Sharma

import gtk
import StringIO
import platform

if 'olpc' in platform.platform():
    from PIL import Image
    #from PIL import ImageEnhance
    #from PIL import ImageFont
    from PIL import ImageFilter
    from PIL import ImageOps
    #from PIL import ImageDraw

else:
    #import Image
    #import ImageEnhance
    #import ImageFont
    #import ImageFilter
    #import ImageOps
    #import ImageDraw
    pass


def pixbuftoImage(pb):

    width, height = pb.get_width(), pb.get_height()
    return Image.fromstring("RGB", (width, height), pb.get_pixels())


def imagetopixbuf(im):

    file1 = StringIO.StringIO()
    im.save(file1, "ppm")
    contents = file1.getvalue()
    file1.close()
    loader = gtk.gdk.PixbufLoader("pnm")
    loader.write(contents, len(contents))
    pixbuf = loader.get_pixbuf()
    loader.close()

    return pixbuf


class ImageProcessor(gtk.DrawingArea):

    __gsignals__ = {
    'expose-event': ('override')}

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.pixbuf = None
        self.pixbufs_stack = []
        self.temp_pixbuf_index = 0
        self.zoom = 1
        self.temp_pixbuf = None
        self.tamanio = (0, 0)

    def reset(self):

        self.pixbuf = None
        self.pixbufs_stack = []
        self.temp_pixbuf_index = 0
        self.zoom = 1
        self.temp_pixbuf = None
        self.tamanio = (0, 0)

    def set_pixbuf(self, pixbuf):

        self.reset()
        self.pixbuf = pixbuf
        self.tamanio = (self.pixbuf.get_width(), self.pixbuf.get_height())
        pixbuf = self.pixbuf.copy()
        self.add_pixbuf_stack(pixbuf)
        self.window.invalidate_rect(self.get_allocation(), True)
        self.window.process_updates(True)

    def add_pixbuf_stack(self, pixbuf):

        if self.pixbufs_stack:
            if self.temp_pixbuf_index != self.pixbufs_stack.index(
                self.pixbufs_stack[-1]):

                self.pixbufs_stack = self.pixbufs_stack[
                    0: self.temp_pixbuf_index + 1]
                self.pixbufs_stack.append(pixbuf)
                self.temp_pixbuf_index = self.pixbufs_stack.index(pixbuf)

            else:
                self.pixbufs_stack.append(pixbuf)

                while len(self.pixbufs_stack) > 10:
                    self.pixbufs_stack.remove(self.pixbufs_stack[0])

                self.temp_pixbuf_index = self.pixbufs_stack.index(pixbuf)

        else:
            self.pixbufs_stack.append(pixbuf)

            while len(self.pixbufs_stack) > 10:
                self.pixbufs_stack.remove(self.pixbufs_stack[0])

            self.temp_pixbuf_index = self.pixbufs_stack.index(pixbuf)

    def do_expose_event(self, event):

        ctx = self.window.cairo_create()
        ctx.rectangle(event.area.x, event.area.y,
            event.area.width, event.area.height)
        ctx.clip()
        self.draw(ctx)

    def draw(self, ctx):

        if not self.pixbufs_stack:
            return

        x, y, w, h = self.get_allocation()
        # Actualizar según zoom
        width, height = self.tamanio
        self.set_size_request(width, height)
        self.temp_pixbuf = self.pixbufs_stack[self.temp_pixbuf_index]

        pixbuf = self.temp_pixbuf.scale_simple(width,
            height, gtk.gdk.INTERP_TILES)

        rect = self.parent.get_allocation()

        if rect.width > width:
            x = int(((rect.width - x) - width) / 2)

        if rect.height > height:
            y = int(((rect.height - y) - height) / 2)

        ctx.set_source_pixbuf(pixbuf, x, y)
        ctx.paint()

    def set_zoom(self, zoom):

        if not self.pixbufs_stack:
            return

        self.zoom = zoom

        if self.zoom <= 0.2:
            self.zoom = 0.2

        self.tamanio = (int(self.temp_pixbuf.get_width() * self.zoom),
            int(self.temp_pixbuf.get_height() * self.zoom))

        self.window.invalidate_rect(self.get_allocation(), True)
        self.window.process_updates(True)

    def set_angulo(self, angulo):

        if not self.pixbufs_stack:
            return

        if angulo > 0:
            rotacion = gtk.gdk.PIXBUF_ROTATE_COUNTERCLOCKWISE

        else:
            rotacion = gtk.gdk.PIXBUF_ROTATE_CLOCKWISE

        pixbuf = self.temp_pixbuf.copy().rotate_simple(rotacion)
        self.tamanio = (int(pixbuf.get_width() * self.zoom),
            int(pixbuf.get_height() * self.zoom))
        self.add_pixbuf_stack(pixbuf)
        self.window.invalidate_rect(self.get_allocation(), True)
        self.window.process_updates(True)

    def zoom_in(self):

        if not self.pixbufs_stack:
            return

        self.set_zoom(self.zoom + 0.2)

    def zoom_out(self):

        if not self.pixbufs_stack:
            return

        self.set_zoom(self.zoom - 0.2)

    def grey(self, value):

        if not self.pixbufs_stack:
            return

        im = pixbuftoImage(self.temp_pixbuf.copy())
        im.convert("RGB")
        r, g, b = im.split()
        im = Image.merge("RGB", (g, g, g))
        pixbuf = imagetopixbuf(im)
        self.add_pixbuf_stack(pixbuf)
        self.window.invalidate_rect(self.get_allocation(), True)
        self.window.process_updates(True)

    def image_undo(self):

        if self.pixbufs_stack and self.temp_pixbuf_index > 0:
            self.temp_pixbuf_index -= 1
            pixbuf = self.pixbufs_stack[self.temp_pixbuf_index]
            self.tamanio = (int(pixbuf.get_width() * self.zoom),
                int(pixbuf.get_height() * self.zoom))
            self.window.invalidate_rect(self.get_allocation(), True)
            self.window.process_updates(True)

    def image_redo(self):
        if self.pixbufs_stack and \
            self.temp_pixbuf_index < len(self.pixbufs_stack) - 1:

            self.temp_pixbuf_index += 1
            pixbuf = self.pixbufs_stack[self.temp_pixbuf_index]
            self.tamanio = (int(pixbuf.get_width() * self.zoom),
                int(pixbuf.get_height() * self.zoom))
            self.window.invalidate_rect(self.get_allocation(), True)
            self.window.process_updates(True)

    def image_Blur(self, value):

        if not self.pixbufs_stack:
            return

        im = pixbuftoImage(self.temp_pixbuf.copy())
        im = im.filter(ImageFilter.BLUR)
        pixbuf = imagetopixbuf(im)
        self.add_pixbuf_stack(pixbuf)
        self.window.invalidate_rect(self.get_allocation(), True)
        self.window.process_updates(True)

    def image_Transpose(self, value):

        if not self.pixbufs_stack:
            return

        im = pixbuftoImage(self.temp_pixbuf.copy())
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        pixbuf = imagetopixbuf(im)
        self.add_pixbuf_stack(pixbuf)
        self.window.invalidate_rect(self.get_allocation(), True)
        self.window.process_updates(True)

    def image_Contour(self, value):

        if not self.pixbufs_stack:
            return

        im = pixbuftoImage(self.temp_pixbuf.copy())
        im = im.filter(ImageFilter.CONTOUR)
        pixbuf = imagetopixbuf(im)
        self.add_pixbuf_stack(pixbuf)
        self.window.invalidate_rect(self.get_allocation(), True)
        self.window.process_updates(True)

    def image_Finedges(self, value):

        if not self.pixbufs_stack:
            return

        im = pixbuftoImage(self.temp_pixbuf.copy())
        im = im.filter(ImageFilter.FIND_EDGES)
        pixbuf = imagetopixbuf(im)
        self.add_pixbuf_stack(pixbuf)
        self.window.invalidate_rect(self.get_allocation(), True)
        self.window.process_updates(True)

    def image_Solarize(self, value):

        if not self.pixbufs_stack:
            return

        im = pixbuftoImage(self.temp_pixbuf.copy())
        im = ImageOps.solarize(im, threshold=128)
        pixbuf = imagetopixbuf(im)
        self.add_pixbuf_stack(pixbuf)
        self.window.invalidate_rect(self.get_allocation(), True)
        self.window.process_updates(True)

    def image_Sharpen(self, value):

        if not self.pixbufs_stack:
            return

        im = pixbuftoImage(self.temp_pixbuf.copy())
        im = im.filter(ImageFilter.SHARPEN)
        pixbuf = imagetopixbuf(im)
        self.add_pixbuf_stack(pixbuf)
        self.window.invalidate_rect(self.get_allocation(), True)
        self.window.process_updates(True)

    def image_Ambross(self, value):

        if not self.pixbufs_stack:
            return

        im = pixbuftoImage(self.temp_pixbuf.copy())
        im = im.filter(ImageFilter.EMBOSS)
        pixbuf = imagetopixbuf(im)
        self.add_pixbuf_stack(pixbuf)
        self.window.invalidate_rect(self.get_allocation(), True)
        self.window.process_updates(True)

    def image_Invert(self, value):

        if not self.pixbufs_stack:
            return

        im = pixbuftoImage(self.temp_pixbuf.copy())
        im = ImageOps.invert(im)
        pixbuf = imagetopixbuf(im)
        self.add_pixbuf_stack(pixbuf)
        self.window.invalidate_rect(self.get_allocation(), True)
        self.window.process_updates(True)

    def guardar_archivo(self, path):

        if not self.pixbufs_stack or not path:
            return

        path = "%s%s" % (path, ".png")
        self.pixbufs_stack[self.temp_pixbuf_index].save(path, "png")
