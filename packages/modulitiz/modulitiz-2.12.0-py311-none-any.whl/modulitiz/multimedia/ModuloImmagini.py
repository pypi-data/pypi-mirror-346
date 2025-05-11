from PIL import Image
from PIL import ImageGrab
from PIL import ImageOps


class ModuloImmagini(object):
	@staticmethod
	def getAllPixels(img):
		return list(img.getdata())
	
	@staticmethod
	def imgToList(img):
		pixels = list(img.getdata())
		width, height = img.size
		pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
		return pixels
	
	@staticmethod
	def convertToJpg(inputFile:str,outputFile:str):
		immagine=Image.open(inputFile).convert("RGB")
		try:
			immagine=ImageOps.exif_transpose(immagine)
		except TypeError:
			pass
		immagine.save(outputFile,"jpeg")
	
	@staticmethod
	def screenshot(nomefile:str)->Image:
		screenshot=ImageGrab.grab()
		screenshot.save(nomefile,'PNG')
		return screenshot
