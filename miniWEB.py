#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: larryhu
# Website: http://www.larryhu.com
# Date: Monday, May. 10 2013
# Version: 1.0

import os, gtk, pynotify, webkit, webbrowser
import sys, ConfigParser, time


# URL = "http://www.baidu.com"

# global schedudler
# schedudler = Scheduler(daemonic = False)

class MiniWEB:
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read('miniweb.conf')
        if len(sys.argv) > 1:
            section = sys.argv[1]
            try:
                conf.options(section)
            except Exception as e:
                print '启动失败.退出', e
                print '可启动项:', conf.sections()
                return
        else:
            section = 'wechat'
            conf.options(section)

        url = conf.get(section, 'url')
        high = conf.getint(section, 'high')
        width = conf.getint(section, 'width')
        self.WEB_NAME = section
        self.icon = os.path.abspath(conf.get(section, 'icon'))

        tray = gtk.StatusIcon()
        tray.set_from_file(self.icon)
        tray.set_tooltip('miniWEB ' + section)
        tray.connect('popup-menu', self.popupMenu)
        tray.connect('activate', self.clickTray)

        page = webkit.WebView()
        page.connect('title-changed', self.titleChange)
        settings = page.get_settings()
        settings.set_property("enable-universal-access-from-file-uris", True)
        settings.set_property('user-agent',
                              'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1496.0 Safari/537.36 larryhu')
        # settings.set_property('enable-offline-web-application-cache', True)
        # settings.set_property('enable-page-cache', True)
        settings.set_property('enable-xss-auditor', False)
        page.set_settings(settings)

        window = gtk.Window()
        window.add(page)
        # window.show_all()
        window.connect("delete_event", self.minimize)

        window.set_size_request(width, high)
        window.set_title("miniWEB " + section)
        window.set_icon_from_file(self.icon)

        window.show_all()
        self.window = window
        self.page = page
        self.tray = tray
        self.page.open(url)

        self.last_notify_time = time.time()
        self.msgs = set()
        pynotify.init("image")

        gtk.main()

    def minimize(self, widget, event, data=None):
        self.window.hide()
        return True

    def titleChange(self, *data):
        title = self.page.get_title()
        self.msgs.add(title)
        self.tray = gtk.StatusIcon()
        if len(self.msgs) > 1:
            self.notification()
            self.tray.set_blinking(True)
        else:
            self.tray.set_blinking(False)

    def notification(self):
        size = len(self.msgs)
        if size > 1 and (time.time() - self.last_notify_time) > 10:
            self.last_notify_time = time.time()
            notify = pynotify.Notification(self.WEB_NAME, list(self.msgs)[size - 1], self.icon)
            self.msgs.clear()
            notify.set_timeout(1)
            notify.show()

    def popupMenu(self, statusicon, button, activate_time):
        self.Author_Blog = 'http://www.larryhu.com'
        menu = gtk.Menu()
        btn_show = gtk.MenuItem('Show/Hide')
        btn_show.connect("activate", self.clickTray)
        menu.append(btn_show)

        btn_author = gtk.MenuItem('Author: %s' % self.Author_Blog)
        btn_author.connect("activate", self.openLink)
        menu.append(btn_author)

        btn_quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        btn_quit.connect("activate", self.quit)
        menu.append(btn_quit)

        menu.show_all()
        menu.popup(None, None, None, 0, gtk.get_current_event_time())

    def quit(self, widget):
        gtk.main_quit()

    def openLink(self, widget):
        webbrowser.open_new_tab(self.Author_Blog)

    def clickTray(self, widget):
        if self.window.get_property('is-active'):
            self.window.hide()
        else:
            if self.tray.get_blinking():
                self.tray.set_blinking(False)
            self.window.present()


if __name__ == '__main__':
    MiniWEB()
# gtk.main()
