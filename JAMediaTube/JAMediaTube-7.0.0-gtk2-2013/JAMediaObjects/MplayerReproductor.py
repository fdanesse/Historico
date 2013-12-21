#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   MplayerReproductor.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       CeibalJAM! - Uruguay

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

import time
import os
import subprocess

import gobject
import platform

from JAMFileSystem import get_programa

STDOUT = "/tmp/mplayerout%d" % time.time()
MPLAYER = "mplayer"

if not get_programa("mplayer"):
    if "xo1.5" in platform.platform():
        MPLAYER = "./mplayer"


class MplayerReproductor(gobject.GObject):
    """
    Reproductor de Audio, Video y Streaming de
    Radio y Television. Implementado sobre:

        python 2.7.3
        Gtk 3
        mplayer (a traves de python.subprocess)
    """

    __gsignals__ = {
    "endfile": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    "estado": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_STRING,)),
    "newposicion": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_INT,)),
    "volumen": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_FLOAT,)),
    "video": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_BOOLEAN,))}

    # Estados: playing, paused, None

    def __init__(self, ventana_id):
        """
        Recibe el id de un DrawingArea
        para mostrar el video.
        """

        gobject.GObject.__init__(self)

        self.name = "MplayerReproductor"
        self.ventana_id = ventana_id
        self.mplayer = False
        self.salida = False
        self.entrada = False
        self.estado = False
        self.duracion = 0
        self.posicion = 0
        self.volumen = 0
        self.actualizador = False
        self.uri = False
        self.video_in_stream = False

        self.config = {
            'saturacion': 0,
            'contraste': 0,
            'brillo': 0,
            'hue': 0,
            'gamma': 0,
            }

        self.efectos = []
        self.config_efectos = {}

    def stop(self):
        """
        Detiene todo.
        """

        try:
            if self.entrada:
                self.entrada.write('%s 0\n' % "quit")
                self.entrada.flush()
                self.__new_handle(False)

        except Exception, e:
            #print "HA OCURRIDO UN ERROR EN QUIT DEL REPRODUCTOR", e
            pass

        self.posicion = 0

        if os.path.exists(STDOUT):
            os.unlink(STDOUT)

        self.estado = False
        self.emit("estado", "None")

    def load(self, uri):
        """
        Carga y Reproduce un archivo o streaming.
        """

        self.stop()
        self.uri = uri

        if os.path.exists(self.uri):
            uri = "%s%s%s" % ("\"", self.uri, "\"")

        cache_pantalla = "%s -cache %i -wid %i" % (
            MPLAYER, 1024, self.ventana_id)

        estructura = "%s -slave -idle -nolirc" % (cache_pantalla)
        estructura = "%s -rtc -nomouseinput" % estructura
        estructura = "%s -noconsolecontrols -nojoystick" % estructura

        self.mplayer = subprocess.Popen(
            estructura, shell=True, stdin=subprocess.PIPE,
            stdout=open(STDOUT, "w+b"), stderr=open(STDOUT, "r+b"),
            universal_newlines=True)

        self.entrada = self.mplayer.stdin
        self.salida = open(STDOUT, "r")
        self.entrada.write("loadfile %s 0\n" % uri)
        self.entrada.flush()
        self.video_in_stream = False
        self.__new_handle(True)

    def __handle(self):
        """
        Consulta el estado y progreso del
        la reproduccion actual.
        """

        if not self.entrada.closed:
            self.entrada.write("%s 0\n" % ("get_property percent_pos"))
            self.entrada.flush()
            linea = self.salida.readline()

            if linea:
                if "ANS_percent_pos" in linea:
                    self.__get_progress_in_mplayer(linea)
                    self.get_volumen()

                elif "Video: no video" in linea or \
                    "Audio only file format detected" in linea:

                    if self.video_in_stream:
                        self.video_in_stream = False
                        self.emit("video", False)

                elif "Movie-Aspect" in linea:
                    if not self.video_in_stream:
                        self.video_in_stream = True
                        self.emit("video", True)

                elif "Cache" in linea:
                    pass

                elif "Starting playback" in linea:
                    self.estado = "playing"
                    self.emit("estado", "playing")

                elif "AO:" in linea:
                    pass

                elif "VO:" in linea:
                    pass

                elif "Resolving" in linea:
                    pass

                elif "Connecting" in linea:
                    pass

                elif "Name" in linea:
                    pass

                elif "Playing" in linea:
                    pass

                elif "Genre" in linea or \
                    "Website" in linea or "Bitrate" in linea:
                    pass

                elif "Opening" in linea or \
                    "AUDIO" in linea or "Selected" in linea:
                    pass

                else:
                    pass

        return True

    def __get_progress_in_mplayer(self, linea):
        """
        Obtiene el progreso de la reproduccion y lo
        envia en una señal para actualizar la barra de
        progreso.
        """

        pos = 0
        try:
            if "Cache size" in linea:
                return

            pos = int(linea.split('=')[1])

            if pos != self.posicion:
                self.posicion = pos
                self.emit("newposicion", self.posicion)

                if self.posicion >= 100:
                    self.emit("endfile")

        except Exception, e:
            print "Error en Progreso de Reproducción: %s" % (e)

    def pause_play(self):
        """
        Llama a play() o pause()
        segun el estado actual del reproductor.
        """

        try:
            if self.entrada:
                if self.estado == "playing":
                    self.__pause()

                elif self.estado == "paused":
                    self.__pause(True)
                    self.estado = "playing"
                    self.emit("estado", "playing")

                else:
                    #if self.uri: self.load(self.uri)
                    pass

        except Exception, e:
            print "HA OCURRIDO UN ERROR EN PAUSE_PLAY DEL REPRODUCTOR", e

    def __pause(self, reset=False):
        """
        Pone en pause o unpause a mplayer
        """

        self.entrada.write('pause 0\n')
        self.entrada.flush()
        self.__new_handle(reset)
        self.estado = "paused"
        self.emit("estado", "paused")

    def __play(self):
        """
        No hace nada. mplayer utiliza:
        pause, unpause y load en lugar de play.
        """

        pass

    def __new_handle(self, reset):
        """
        Elimina o reinicia la funcion que
        envia los datos de actualizacion para
        la barra de progreso del reproductor.
        """

        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False

        if reset:
            self.actualizador = gobject.timeout_add(500, self.__handle)

    def set_position(self, posicion):
        """
        Permite desplazarse por
        la pista que se esta reproduciendo.
        """

        # FIXME: Actualmente no funciona bien
        posicion = int(posicion)
        if posicion != self.posicion:
            self.posicion = posicion
            self.entrada.write('seek %s %i 0\n' % (posicion, 1))
            self.entrada.flush()

    def get_volumen(self):
        """
        Obtiene el volumen de reproducción.
        Lo hace solo al reproducir el primer archivo
        o streaming y envía el dato para actualizar
        el control de volúmen.
        """

        if self.volumen != 0:
            return

        if self.entrada:
            self.entrada.write("%s 0\n" % ("get_property volume"))
            self.entrada.flush()
            linea = self.salida.readline()

            if "ANS_volume" in linea:
                valor = float(linea.split("=")[1])

                if self.volumen == 0:
                    self.volumen = valor
                    self.emit('volumen', valor)

    def set_volumen(self, valor):
        """
        Cambia el volúmen de Reproducción.
        """

        if self.entrada:
            if valor != self.volumen:
                self.volumen = valor
                self.entrada.write("%s %s 0\n" % (
                    "set_property volume", valor))
                self.entrada.flush()

    def set_balance(self, brillo=None, contraste=None,
        saturacion=None, hue=None, gamma=None):
        """
        Seteos de balance en la fuente de video.
        Recibe % en float y convierte a los valores del filtro.
        """

        # FIXME: Actualmente no funciona.
        if saturacion != None:
            # int. Range: -100 - 100 Default: 0
            self.config['saturacion'] = int(200 * saturacion / 100 - 100)

            if self.entrada:
                self.entrada.write("%s %i 0\n" % ("set_property saturation",
                    self.config['saturacion']))
                self.entrada.flush()

        if contraste != None:
            # int. Range: -100 - 100 Default: 0
            self.config['contraste'] = int(200 * contraste / 100 - 100)

            if self.entrada:
                self.entrada.write("%s %i 0\n" % ("set_property contrast",
                    self.config['contraste']))
                self.entrada.flush()

        if brillo != None:
            # int. Range: -100 - 100 Default: 0
            self.config['brillo'] = int(200 * brillo / 100 - 100)

            if self.entrada:
                self.entrada.write("%s %i 0\n" % ("set_property brightness",
                    self.config['brillo']))
                self.entrada.flush()

        if hue != None:
            # int. Range: -100 - 100 Default: 0
            self.config['hue'] = int(200 * hue / 100 - 100)

            if self.entrada:
                self.entrada.write("%s %i 0\n" % ("set_property hue",
                    self.config['hue']))
                self.entrada.flush()

        if gamma != None:
            # int. Range: -100 - 100 Default: 0
            self.config['gamma'] = int(200 * gamma / 100 - 100)

            if self.entrada:
                self.entrada.write("%s %i 0\n" % ("set_property gamma",
                    self.config['gamma']))
                self.entrada.flush()

    def get_balance(self):
        """
        Retorna los valores actuales de balance en %.
        """

        return {
        'saturacion': (self.config['saturacion'] + 100) * 100.0 / 200.0,
        'contraste': (self.config['contraste'] + 100) * 100.0 / 200.0,
        'brillo': (self.config['brillo'] + 100) * 100.0 / 200.0,
        'hue': (self.config['hue'] + 100) * 100.0 / 200.0,
        'gamma': (self.config['gamma'] + 100) * 100.0 / 200.0,
        }

    def agregar_efecto(self, nombre_efecto):
        pass

    def quitar_efecto(self, indice_efecto):
        pass

    def configurar_efecto(self, nombre_efecto, propiedad, valor):
        pass

    def rotar(self, valor):
        pass

REC = "/tmp/mplayerrec%d" % time.time()


class MplayerGrabador(gobject.GObject):
    """
    Graba desde un streaming de radio o tv.
    """

    __gsignals__ = {
    "update": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self, uri, archivo):

        gobject.GObject.__init__(self)

        self.actualizador = False
        self.archivo = False
        self.uri = uri
        self.info = ""

        estructura = "%s -slave -idle -nolirc" % MPLAYER
        estructura = "%s -nomouseinput -noconsolecontrols" % estructura
        estructura = "%s -nojoystick -dumpstream -dumpfile %s" % (
            estructura, archivo)

        self.mplayer = subprocess.Popen(
            estructura, shell=True,
            stdin=subprocess.PIPE,
            stdout=open(REC, "w+b"),
            stderr=open(REC, "r+b"),
            universal_newlines=True)

        self.entrada = self.mplayer.stdin
        self.salida = open(REC, "r")

        self.entrada.write("loadfile %s 0\n" % uri)
        self.entrada.flush()

        self.__new_handle(True)

    def __new_handle(self, reset):
        """
        Elimina o reinicia la funcion que
        envia los datos de actualizacion.
        """

        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False

        if reset:
            self.actualizador = gobject.timeout_add(500, self.__handle)

    def __handle(self):
        """
        Consulta el estado y progreso de
        la grabacion.
        """

        if not self.entrada.closed:
            linea = self.salida.readline()
            tamanio = None

            if linea:
                #if 'Playing' in linea:
                #    self.uri = linea.split()[-1]

                if 'dump:' in linea:
                    tamanio = int(int(linea.split()[1]) / 1024)

                if self.uri and tamanio:
                    uri = self.uri
                    if len(self.uri) > 20:
                        uri = str(self.uri[0:20]) + " . . . "

                    info = "Grabando: %s - %s Kb Almacenados." % (
                        uri, str(tamanio))

                    if self.info != info:
                        self.info = info
                        self.emit('update', self.info)

        return True

    def stop(self):
        """
        Detiene la Grabación actual.
        """

        try:
            if self.entrada:
                self.entrada.write('%s 0\n' % "quit")
                self.entrada.flush()
                self.__new_handle(False)

        except Exception, e:
            print "HA OCURRIDO UN ERROR EN QUIT DEL GRABADOR", e

        self.mplayer.kill()

        try:
            if os.path.exists(self.archivo):
                os.chmod(self.archivo, 0755)

        except:
            pass

        if os.path.exists(REC):
            os.unlink(REC)
