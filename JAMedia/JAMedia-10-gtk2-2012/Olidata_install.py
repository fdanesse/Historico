#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands
import platform

jamedia = os.environ["PWD"]


def install():

    if "Strawberry" in platform.platform():

        print commands.getoutput('yum -y install mplayer')

        plugins = [
            'gstreamer-plugins-base',
            'gstreamer-plugins-good', 'gstreamer-plugins-ugly',
            'gstreamer-plugins-bad', 'gstreamer-ffmpeg']

        for plugin in plugins:
            print commands.getoutput('yum -y install %s' % (plugin))

        print commands.getoutput('yum -y install alsa-lib alsa-utils')
        print commands.getoutput('yum erase pulseaudio')

        print "Instalando JAMedia en:", platform.platform()

        print commands.getoutput(
            'cp -r %s /usr/local/share/JAMedia' % (jamedia))
        print commands.getoutput(
            'cp JAMedia.desktop /usr/share/applications/')
        print commands.getoutput('cp JAMedia /usr/local/bin/')
        print commands.getoutput('cp JAMediaUninstall /usr/local/bin/')
        print commands.getoutput('chmod 755 /usr/local/bin/JAMedia')
        print commands.getoutput('chmod 755 /usr/local/bin/JAMediaUninstall')
        print commands.getoutput(
            'chmod 755 /usr/local/share/JAMedia/Mplayer_Grabador.py')

        print "JAMedia instalado Correctamente !!!"
        print "Puedes acceder desde el menú Aplicaciones - Sonido y Video.\n"
        print "Para Desinstalar JAMedia, Ejecuta con Permisos de Administrador: JAMediaUninstall"

    else:
        print "No se puede instalar en:", platform.platform()

if __name__ == "__main__":
    install()
