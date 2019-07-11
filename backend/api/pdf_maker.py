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
	folder_name = datetime.datetime.now().strftime('%s')
	if not os.path.exists(folder_name):
		os.mkdir(folder_name)
	
	pdf = Pdf.query.get(pid)
	pfile = pdf.pfile
	pname = pdf.pname
	
	f = open(folder_name+'/'+pname,'wb')
	f.write(pfile)

	DATA = pdf.zones
	ZONES = []
	for zone in DATA:
		while zone.pageno-1 >= len(ZONES):
			ZONES.append([])
		ZONES[zone.pageno-1].append(zone)


	output = PdfFileWriter()
	
	old_pdf = PdfFileReader(folder_name+'/'+pname)
	for index,currPage in enumerate(ZONES):
		if len(currPage) == 0:
			continue
		packet = io.BytesIO()
		can = canvas.Canvas(packet)

		height = int(list(old_pdf.getPage(index).mediaBox)[3])
		width = int(list(old_pdf.getPage(index).mediaBox)[2])

		for zone in currPage:
			hr = height/zone.canvas_height
			wr = width/zone.canvas_width
			can.drawString(0.5*wr+zone.lx*wr,height - zone.ly*hr-10*hr,zone.zname)

		can.save()

		packet.seek(0)
		new_pdf = PdfFileReader(packet)

		page = old_pdf.getPage(index)
		page.mergePage(new_pdf.getPage(0))
		output.addPage(page)

		outputStream = open(folder_name + "/des.pdf","ab")
		output.write(outputStream)
		outputStream.close()