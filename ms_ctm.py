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

conn = db_conn()
c = conn.cursor()

sql = """ SELECT * FROM `ms_media_files`"""

#sql = """ SELECT * FROM `ms_media_files` WHERE media_file_id = %s """

r = db_query(c, sql)

ac = pandas.DataFrame(columns=
	['dcterms:identifier', 
	'ac:associatedSpecimenReference',
	'ac:providerManagedID',
	'ac:derivedFrom',
	'ac:providerLiteral',
	'ac:provider',
	'dc:type',
	'dcterms:type',
	'ac:subtypeLiteral',
	'ac:subtype',
	'ac:accessURI',
	'dc:format',
	'ac:subjectPart',
	'ac:subjectOrientation',
	'ac:caption',
	'Iptc4xmpExt:LocationCreated',
	'ac:captureDevice',
	'dc:creator',
	'ms:scanningTechnician',
	'ac:fundingAttribution',
	'exif:Xresolution',
	'exif:Yresolution',
	'dicom:SpacingBetweenSlices',
	'dc:rights',
	'dcterms:rights',
	'xmpRights:Owner',
	'xmpRights:UsageTerms',
	'xmpRights:WebStatement',
	'ac:licenseLogoURL',
	'photoshop:Credit',
	'coreid'])

for mf_dict in r:
	mf = ms_media_file.MsMediaFile(mf_dict)

	if mf.is_published():	
		ac = ac.append(mf.ac_mf_dict, ignore_index=True)
		ac = ac.append(mf.ac_mfp_dict, ignore_index=True)

ac.to_csv('output.csv', index=False, index_label=False)










