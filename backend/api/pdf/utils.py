import pandas as pd
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,A4
from api.pdf.models import Pdf
import datetime
import os
from flask import jsonify, send_file
import zipfile

def create_zip(folder_path, exceptions = []):
	cwd = os.getcwd()
	os.chdir(folder_path)
	with zipfile.ZipFile('pdf.zip', 'w') as myzip:
		for r,d,f in os.walk(folder_path):
			for f_ in f:
				if f_[:4] == 'dest':
					myzip.write(f_)
	os.chdir(cwd)

def create_dir():
	#unique folder name
	folder_name = datetime.datetime.now().strftime('%s')
	#folder doesn't exists
	if not os.path.exists(os.path.join(os.getcwd(),'zip',folder_name)):
		os.mkdir(os.path.join(os.getcwd(),'zip',folder_name))
		return os.path.join(os.getcwd(),'zip',folder_name)
	return None

def fill_pdf(folder_path, pdf_path, data, i):
	zones = []
	#group zones to pages
	for zone in data:
		while zone.pageno-1 >= len(zones):
			zones.append([])
		zones[zone.pageno-1].append(zone)
	#initialise pdffilewriter and pdffilereader
	output = PdfFileWriter()
	old_pdf = PdfFileReader(pdf_path)
	#for all page
	for pageno,curr_page in enumerate(zones):
		if len(curr_page) == 0:
			continue
		#initialise the bytes
		packet = io.BytesIO()
		can = canvas.Canvas(packet)
		#get the actual page size of the pdf
		height = int(list(old_pdf.getPage(pageno).mediaBox)[3])
		width = int(list(old_pdf.getPage(pageno).mediaBox)[2])
		#for all zones in current page
		for zone in curr_page:
			#get the actual coordinates
			hr = height/zone.canvas_height
			wr = width/zone.canvas_width
			#write the data on the packet at the specified location
			#0.5*wr and 10*hr are the buffers
			can.drawString(0.5*wr+zone.left*wr,height - zone.top*hr-10*hr,zone.zdata)
		#save the canvas and bring the cursor to the very first
		can.save()
		packet.seek(0)
		#open the packet io as new_pdf
		new_pdf = PdfFileReader(packet)
		#merge corresponding pdf page and packet
		page = old_pdf.getPage(pageno)
		page.mergePage(new_pdf.getPage(0))
		output.addPage(page)
		#write it to the output stream
		destination = os.path.join(folder_path,'dest'+str(i)+'.pdf')
		outputStream = open(destination,"ab")
		output.write(outputStream)
		outputStream.close()

def process_excel(pdf, folder_path, pdf_path):
	excel_path = os.path.join(folder_path, pdf.ename)
	#save excel to the folder
	f = open(excel_path,'wb')
	f.write(pdf.efile)
	f.close()
	#read excel
	excel = pd.read_excel(excel_path)
	keys = excel.keys()
	length = len(excel[keys[0]])
	#create a copy of zones
	zones = pdf.zones.copy()
	arr = []
	for i in range(length):
		arr.append(zones.copy())

	for i in range(length):
		for zone in arr[i]:
			zone.zdata = str(excel[zone.zname][i])
		#generate pdf for each record
		fill_pdf(folder_path,pdf_path,arr[i],i)
		
def gen_pdf(pid):
	folder_path = create_dir()
	#if exists send 500 error
	if folder_path == None:
		return jsonify({
			'status': 500
		})
	#get pdf from db
	pdf = Pdf.query.get(pid)
	pfile = pdf.pfile
	pname = pdf.pname
	#set path to pdf and save pdf
	pdf_path = os.path.join(folder_path,pname)
	f = open(pdf_path,'wb')
	f.write(pfile)
	#read excel and fill pdf
	process_excel(pdf, folder_path, pdf_path)
	create_zip(folder_path, [pname, pdf.ename])
	return send_file(os.path.join(folder_path,'pdf.zip'))