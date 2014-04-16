#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: larryhu
# Website: http://www.larryhu.com
# Date: Monday, May. 10 2013
# Version: 1.0

import os, gtk, pynotify, webkit, webbrowser, time

#import gtkmozembed
#from selenium import webdriver

URL = "https://wx.qq.com/"
#URL = "http://www.baidu.com"
INIIAL_TITLE = "miniWEB \t\tauthor:larryhu larryhu.com"

ICON = os.path.join(os.getcwd(), 'wechat.jpg')
WEB_NAME = "wechat"
	

class MiniWEB():
	
	def __init__(self):

		tray = gtk.StatusIcon()
		tray.set_from_file(ICON)
		tray.set_tooltip(' miniWEB 1.0 ')
		tray.connect('popup-menu', self.popupMenu)
		tray.connect('activate', self.clickTray)

		page = webkit.WebView()#gtkmozembed.MozEmbed()
		page.connect('title-changed', self.titleChange)
		setttings = page.get_settings()
#		setttings.set_property("enable-universal-access-from-file-uris", True)
		setttings.set_property('user-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1496.0 Safari/537.36 larryhu')
#		setttings.set_property('enable-offline-web-application-cache', True)
#		setttings.set_property('enable-page-cache', True)
		setttings.set_property('enable-xss-auditor', False)

		window = gtk.Window()
		window.add(page)
#		window.show_all()
		window.connect("delete_event", self.minimize)
		window.set_size_request(1000, 600)
		window.set_title(INIIAL_TITLE)
		window.set_icon_from_file(ICON)
		self.lastMessage = None

		window.show_all()
		self.window = window
		self.page = page
		self.tray = tray

#		print dir(self.page)
		self.page.open(URL)
#		self.page.reload()

		gtk.main()

	def minimize(self, widget, event, data=None):
		self.window.hide()
		return True

	def titleChange(self, *data):
		title = self.page.get_title()
		self.tray = gtk.StatusIcon()
#		print '\nnotify %s \n' % (self.lastMessage)
		if title.endswith('...') and title!=self.lastMessage:
			self.lastMessage = title
			self.tray.set_blinking(True)
			self.notification()
		else:
			if self.tray.get_blinking():
				self.tray.set_blinking(False)

	def notification(self):
		pynotify.init("image")
#		print 'notify load icon ', ICON
		notify = pynotify.Notification(WEB_NAME, self.page.get_title(), ICON)
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
#	gtk.main()

