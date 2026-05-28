import pyttsx3
import PyPDF2
from tkinter.filedialog import *

PDF = askopenfilename()
PdfReader = PyPDF2.PdfReader(PDF)
pages = PdfReader.numPages  

for num in range(0, pages):
    page = PdfReader.getPage(num)
    text = page.extractText()

    speaker = pyttsx3.init()
    speaker.say(text)
    speaker.runAndWait()    