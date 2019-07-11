import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
from PIL import Image
from PIL import ImageFilter
import matplotlib as mpl
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,A4
from api.models import Pdf
import datetime
import os


def create_dir():
	#unique folder name
	folder_name = datetime.datetime.now().strftime('%s')
	#folder doesn't exists
	if not os.path.exists(folder_name):
		os.mkdir(folder_name)
		return folder_name
	return None

def fill_pdf(folder_path, pdf_path, data):
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
		height = int(list(old_pdf.getPage(index).mediaBox)[3])
		width = int(list(old_pdf.getPage(index).mediaBox)[2])
		#for all zones in current page
		for zone in curr_page:
			#get the actual coordinates
			hr = height/zone.canvas_height
			wr = width/zone.canvas_width
			#write the data on the packet at the specified location
			#0.5*wr and 10*hr are the buffers
			can.drawString(0.5*wr+zone.left*wr,height - zone.top*hr-10*hr,zone.zname)
		#save the canvas and bring the cursor to the very first
		can.save()
		packet.seek(0)
		#open the packet io as new_pdf
		new_pdf = PdfFileReader(packet)
		#merge the corresponding pdf page and packet
		page = old_pdf.getPage(pageno)
		page.mergePage(new_pdf.getPage(0))
		output.addPage(page)
		#write it to the output stream
		destination = os.path.join(folder_path,'destination.pdf')
		outputStream = open(destination,"ab")
		output.write(outputStream)
		outputStream.close()

def gen_pdf(pid):
	folder_name = create_dir()
	#if exists send 500 error
	if folder_name == None:
		return jsonify({
			'status': 500
		})
	#get pdf from db
	pdf = Pdf.query.get(pid)
	pfile = pdf.pfile
	pname = pdf.pname
	#set path to pdf
	folder_path = os.path.join(os.getcwd(),'zip',folder_name)
	pdf_path = os.path.join(folder_path,pname)
	#save pdf to the folder
	f = open(pdf_path,'wb')
	f.write(pfile)
	#fill pdf
	fill_pdf(folder_path,pdf_path,pdf.zones)
	