import cv2
import numpy as np
import time
import datetime
import fitz
import sys
import os

def output_foldername():
	now = datetime.datetime.now()
	return 'output_'+now.strftime("%Y%m%d%H%M%S")

def print_usage():	
	print('\nUsage:\t python '+sys.argv[0]+ ' -p | -f | -s target -t threshold -i iterations\n')
	print('Options:')
	print('\t-p\t\tProcess images in pdf file named `target`')
	print('\t-f\t\tProcess images in folder named `target`')
	print('\t-s\t\tProcess single image file named `target`')
	print('\t-t threshold\tThershold level [0-255] to apply binarization on at the watermark area')
	print('\t-i iterations\tNumber of iterations in the watermark detection using Opening/Closing  Morphological process')
	print('')
	exit(1)


def import_pdf(filename, iterations, threshold):
	input = fitz.open(filename)	#input file	
	print('Starting task for pdf file `' + filename + '`')
	output_folder = output_foldername()
	os.mkdir(output_folder)
	n = 1
	for i in range(len(input)):#Each page
		for img in input.getPageImageList(i):
			xref = img[0]
			pix = fitz.Pixmap(input, xref)
			if pix.n >= 5:       # CMYK: convert to RGB first
				pix = fitz.Pixmap(fitz.csRGB, pix)              

			data = np.fromstring(pix.getPNGData(), np.uint8) #convert to raw bytes
			I = cv2.imdecode(data, cv2.IMREAD_UNCHANGED) #decode
			I = remove_watermark(I, iterations, threshold)
			cv2.imwrite(os.path.join(output_folder, 'pdf_'+str(n)+'.jpg'), I)
			print('Image #'+str(n)+'/'+str(len(input)))
			n = n + 1


def import_folder(foldername, iterations, threshold):
	files = os.listdir(foldername)
	print('Starting task for folder `' + foldername + '`')
	output_folder = os.path.join(foldername, output_foldername())
	os.mkdir(output_folder)
	n = 1
	for file in files:
		if file.endswith('.jpg') or file.endswith('.png'):
			print(str(n)+'/'+str(len(files))+': '+file)
			I = cv2.imread(os.path.join(foldername,file))
			I = remove_watermark(I, iterations, threshold)
			cv2.imwrite(os.path.join(output_folder, file), I)
			n = n + 1


def import_file(filename, iterations, threshold):
	print('Starting task for image `' + filename + '`')
	I = cv2.imread(filename)
	I = remove_watermark(I, iterations, threshold)
	output_folder = output_foldername()
	os.mkdir(output_folder)
	cv2.imwrite(os.path.join(output_folder, filename), I)


def remove_watermark(I, iterations, threshold):
	if np.max(I)<=1:
		I = np.array(255*I,dtype = np.uint8)

	gray = cv2.cvtColor(I,cv2.COLOR_BGR2GRAY)

	bg = np.copy(gray,np.uint8)

	#Extract background from the image
	for i in range(iterations):
		#repeat for n iterations
		elipse = cv2.getStructuringElement(cv2.MORPH_RECT,(2*i+1,2*i+1))
		#Dilation followed by Erosion to remove all word
		#since ink is always darker even than the watermark
		bg = cv2.morphologyEx(bg, cv2.MORPH_CLOSE, elipse)
		#Erosion followed by Dilation to remove traces 
		bg = cv2.morphologyEx(bg, cv2.MORPH_OPEN, elipse)

		
	
	#threshold the extracted background
	_,bg = cv2.threshold(bg,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	output = 255*np.ones(np.shape(gray),dtype=np.uint8)


	#copy from the original gray image where there is no watermark
	output[bg!=0] = gray[bg!=0]

	#apply the threshold specific where there is a watermark
	mask = np.logical_and(bg==0,gray<threshold)
	output[mask] = gray[mask]

	#apply another threshold to binarize the final image for consistent and clear output
	th,_ = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	output[output>th] = 255
	output[output<th] = 0
	return output


if __name__ == "__main__":
	
	print('\nElmalzmaDechiper v0.0.2\n')
	if len(sys.argv)!=7:
		print_usage()
	
	i=1
	
	while i < len(sys.argv) -1:
		if sys.argv[i]=='-p':
			mode='pdf'
			filename = sys.argv[i+1]
			i = i + 2
		elif sys.argv[i]=='-f':
			mode='folder'
			filename = sys.argv[i+1]
			i = i + 2
		elif sys.argv[i]=='-s':
			mode='file'
			filename = sys.argv[i+1]
			i = i + 2	
		elif sys.argv[i]=='-t':
			try:
				th = int(float(sys.argv[i+1]))
			except ValueError:
				print_usage()
			i = i + 2
		elif sys.argv[i]=='-i':
			try:
				it = int(sys.argv[i+1])
			except ValueError:
				print_usage()
			i = i + 2

	start = time.time()
	if mode=='pdf':
		import_pdf(filename, iterations = it, threshold = th)
	elif mode=='folder':
		import_folder(filename, iterations = it, threshold = th)
	elif mode=='file':
		import_file(filename, iterations = it, threshold = th)

		
	end = time.time()
	print('Task Finished in '+str(round(end-start,2))+'s')
	