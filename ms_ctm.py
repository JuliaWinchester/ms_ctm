# Script for exporting audubon core CSV file representing UF specimens.
#
# Author: Julie Winchester <julia.m.winchester@gmail.com>
# February 14, 2018

import credentials
import ms_media_file
import pandas
import phpserialize
import pymysql
import zlib
import os.path

from subprocess import call

def db_conn():
	return pymysql.connect(host = credentials.db['server'],
						   user = credentials.db['username'],
						   password = credentials.db['password'],
						   db = credentials.db['db'],
						   charset = 'utf8mb4',
						   cursorclass=pymysql.cursors.DictCursor)

def db_query(cursor, sql, args):
	cursor.execute(sql, [args])
	return cursor.fetchall()

def db_query_no_args(cursor, sql):
	cursor.execute(sql)
	return cursor.fetchall()

def save_ctm(file_path, ctm_path):
	if 'ply' in file_path or 'obj' in file_path:
		# Just re-run ctmconv
		call('/usr/local/bin/ctmconv ' + file_path + ' ' + ctm_path + ' --method MG2 --level 9', shell=True)
		return True
	elif 'stl' in file_path:
		call("xvfb-run -a -s '-screen 0 800x600x24' meshlabserver -i " + file_path + " -o /tmp/temp.stl")
		call('/usr/local/bin/ctmconv /tmp/temp.stl ' + ctm_path + ' --method MG2 --level 9', shell=True)
		return True
	else:
		return False

def mf_ctm_url(mf_info_dict):
	return os.path.join('/opt/rh/httpd24/root/var/www/html/media/morphosource/images/', mf_info_dict['ctm']['HASH'], str(mf_info_dict['ctm']['MAGIC'])+'_'+mf_info_dict['ctm']['FILENAME'])

conn = db_conn()
c = conn.cursor()

sql = """ SELECT * FROM `ms_media_files`"""

#sql = """ SELECT * FROM `ms_media_files` WHERE media_file_id = %s """
#sql = """ SELECT * FROM `ms_media_files` WHERE media_file_id = 29 """

r = db_query_no_args(c, sql)

mf_array = list()
broken_ctm = list()
original_file = list()

for mf_dict in r:
	print mf_dict['media_file_id']
	mf = ms_media_file.MsMediaFile(mf_dict)
	mf_array.append(mf)
	if 'ctm' in mf.mf_info_dict:
		if mf.mf_info_dict['ctm'] is not None:
			file_path = os.path.join('/opt/rh/httpd24/root/var/www/html/media/morphosource/images/', mf_info_dict['original']['HASH'], str(mf_info_dict['original']['MAGIC'])+'_'+mf_info_dict['original']['FILENAME'])
			ctm_path = os.path.join('/opt/rh/httpd24/root/var/www/html/media/morphosource/images/', mf_info_dict['ctm']['HASH'], str(mf_info_dict['ctm']['MAGIC'])+'_'+mf_info_dict['ctm']['FILENAME'])
			if not os.path.isfile(ctm_path):
				broken_ctm.append(ctm_path)
				original_file.append(file_path)
				save_ctm(file_path, ctm_path)









