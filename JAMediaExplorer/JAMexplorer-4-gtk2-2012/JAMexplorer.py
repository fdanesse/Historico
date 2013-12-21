#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMexplorer.py por:
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
from sugar.activity import activity

from Navegador_de_Archivos import Navegador_de_Archivos

class JAMexplorer(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle, False)
        self.set_title("JAMexplorer")
        self.set_resizable(True)
        self.connect("delete_event", self.delete_event)
        self.set_border_width(3)
        self.set_toolbox(activity.ActivityToolbox(self))
        self.set_canvas(Navegador_de_Archivos())
        self.show_all()

    def delete_event(self, widget, event, data=None):
        sys.exit(0)
        return False

class Ventana(gtk.Window):
    def __init__(self):
        super(Ventana, self).__init__()
        self.set_title("JAMexplorer")
        self.set_icon_from_file(os.path.join(os.path.dirname(__file__), "Iconos", "jamplorer.png"))
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(3)
        self.connect("delete_event", self.delete_event)
        self.connect("destroy", self.destroy)
        self.add(Navegador_de_Archivos())
        self.show_all()

    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

if __name__ == "__main__":
    Ventana()
    gtk.main()
    