#encoding:utf8
import os, os.path
import cherrypy
import simplejson
import csv
import StringIO
import sys
import sqlite3 as sql
import json, io

class Root(object):
	#http://localhost:8080/createSong?name=The%20Simpsons&notes=c.6,e6,f%236,8a6,g.6,e6,c6,8a,8f%23,8f%23,8f%23,2g,8p,8p,8f%23,8f%23,8f%23,8g,a%23.,8c6,8c6,8c6,c6
	@cherrypy.expose
	def createSong(self, **kw):
		x = repr(dict(kw=kw))
		x = x.split("'")
		xdourl = ""
		ydourl = ""
		xdox = x[7]
		ydoy = x[3]
		if(xdox == "name" and ydoy == "notes"):
			xdourl = x[9]
			ydourl = x[5]

			db = sql.connect("database.db")
			db.execute("INSERT INTO song (name,sheet) VALUES (?,?)", (xdourl,ydourl,))
			db.commit()
			db.close()

		return "Música enviada com sucesso!"

	@cherrypy.expose
	def getNotes(self, **kw):
		x = repr(dict(kw=kw))
		x = x.split("'")
		ydourl = ""
		row = ""
		ydoy = x[3]
		if(ydoy == "id"):
			ydourl = x[5]
			print ydourl
			db = sql.connect("database.db")
			result = db.execute("SELECT sheet FROM song WHERE id=?",(ydourl,))
			rows = result.fetchone()
			row = rows
			db.commit()
			db.close()

		return row

	@cherrypy.expose
	def listSongs(self):
		db = sql.connect("database.db")
		result = db.execute("SELECT * FROM song")
		rows = result.fetchall()
		d = []
		for row in rows:
			print row
			name = {"id":row[0],"name":row[1],"notes":row[2]}
			d.append(name)
		print d
		'''for x in row:
			name = {"name":x}
			d.append(name)
		print d'''

		f = open('alllist.js','w')
		f.write(unicode("alllist("))
		f.write(unicode(json.dumps(d, ensure_ascii=False)))
		f.write(unicode(")"))
		f.close()
		db.commit()
		db.close()
		return open("allmusic.html","r")

	def update(self):
		cl = cherrypy.request.headers['Content-Length']
		rawbody = cherrypy.request.body.read(int(cl))
		#body = simplejson.loads(rawbody)
		# do_something_with(body)

		rawbody = rawbody.replace('"', '').split(":",1)
		print rawbody
		db = sql.connect("database.db")
		db.execute("INSERT INTO song (name,sheet) VALUES (?,?)", (rawbody[0],rawbody[1],))
		db.commit()
		db.close()

	@cherrypy.expose
	def upload(self):
		return open("upload.html")

	@cherrypy.expose
	def alllist(self):
		return open("alllist.js","r")
cherrypy.config.update({'server.socket_host': '127.0.0.1',
	'server.socket_port': 8083,
	})
cherrypy.quickstart(Root())