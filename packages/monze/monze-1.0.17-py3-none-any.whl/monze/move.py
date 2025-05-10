from flask import Blueprint, render_template, redirect, request
import sys
from singletons import UserSettings, Students, Sysls
from general import Mainroad, JINJAstuff, Casting
import os
import subprocess
from threading import Thread

from studenten import (
	StudentJinja,
	Student,
	Note,
)
# =============== endpoints =====================
ep_move = Blueprint(
	'ep_move', __name__,
	url_prefix="/move",
	template_folder='templates',
    static_folder='static',
	static_url_path='static',
)

menuitem = 'move'

@ep_move.get('/')
def move():
	jus = UserSettings()
	if not jus.magda(['beheer', 'admin']):
		Mainroad.loglog('Iets mis met login')
		sys.exit(1)



	'''
	try:
		dirpath = Casting.str_(request.form["dirpath"], default="").strip()
	except:
		dirpath = ""
	
	try:
		coursid = Casting.int_(request.form.get("coursid"), default=0)
	except:
		coursid = 0
	print("poep", coursid)

	dirs = list()
	courses = dict()
	studenten = list()

	
	home = pathlib.Path.home() / 'Downloads'
	homes = [home] + list(home.glob("**/*"))
	dirs = list()
	for i in range(len(homes)):
		if '$' in homes[i].name:
			continue
		if not os.path.isdir(homes[i]):
			continue
		dirs.append(str(homes[i]))
	

	sysls_o = Sysls()
	courses = sysls_o.get_sysl_active('s_course')
	if coursid > 0:
		students_o = Students()
		studenten = students_o.get_students_mongo(where={"s_status": {'$in': [20, 21, 22, 23]}, 's_course': {'$eq': coursid}})
		groepen = sysls_o.get_sysl('s_group')
		for i in range(len(studenten)):
			studenten[i] = StudentJinja(studenten[i], dict())
	'''
	return render_template(
		'move.html',
		menuitem='move',
		props=jus,
	)

@ep_move.post('/')
def move_post():
	jus = UserSettings()
	if not jus.magda(['beheer', 'admin']):
		Mainroad.loglog('Iets mis met login')
		sys.exit(1)

	thread = Thread(target=open_move_app)
	thread.start()
	return redirect('/move')

def open_move_app():
	pad = os.path.dirname(os.path.realpath(__file__))
	subprocess.Popen(['python3', os.path.join(pad, "dnd.py")])