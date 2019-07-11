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

def gen_pdf(pid):
	# cwd = os.getcwd()
	# os.chdir(os.getcwd()+'/api/zip_container/')
	folder_name = datetime.datetime.now().strftime('%s')
	
	os.mkdir(folder_name)

	exit()
	
	pdf = Pdf.query.get(pid)
	pfile = pdf.pfile
	pname = pdf.pname
	
	f = open(folder_name+'/'+pname,'wb')
	f.write(pfile)

	DATA = pdf.zones

	print(DATA)

	ZONES = []
	for zone in DATA:
		while zone.page >= len(ZONES):
			ZONES.append([])
		ZONES[zone.page].append(zone)


	output = PdfFileWriter()
	#old_pdf = PdfFileReader(open("api/hr.pdf","rb"))
	old_pdf = PdfFileReader(pfile)
	for index,currPage in enumerate(ZONES):
		if len(currPage) == 0:
			continue

		packet = io.BytesIO()
		can = canvas.Canvas(packet)

		height = int(list(old_pdf.getPage(index).mediaBox)[3])
		width = int(list(old_pdf.getPage(index).mediaBox)[2])

		for zone in currPage:
			hr = height/zone.page_height
			wr = width/zone.page_width

			can.drawString(zone['lx'],height - zone['ly'],zone['zname'])
			can.drawString(0.5*wr+zone['lx']*wr,height - zone['ly']*hr-10*hr,zone['zname']+"zzzzzzzzz")

		can.save()

		packet.seek(0)
		new_pdf = PdfFileReader(packet)


		page = old_pdf.getPage(index)
		page.mergePage(new_pdf.getPage(0))
		output.addPage(page)

		outputStream = open("des.pdf","ab")
		output.write(outputStream)
		outputStream.close()

	# os.chdir(cwd)