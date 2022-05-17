from paddleocr import  PaddleOCR
from tkinter import  *
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
from threading import Thread
import queue
import time
import filetype
import pyperclip
from PIL import ImageGrab
from PIL import Image
import numpy as np
import os



class GUI(Frame):
    def __init__(self,parent=None, **kwargs):
        Frame.__init__(self,parent,**kwargs)
        self.config(height=500,width=300,bg="white")
        self.pack()
        self.dataqueue=queue.Queue()
        #self.var=StringVar()
        #openfile=lambda buttonReturn=askopenfilename:self.fileOCR(buttonReturn)
        self.FileOCRButton=Button(self,text="本地图片识别",command=self.filemakethread)
        self.FileOCRButton.grid(row=0,sticky=E,padx=15,pady=3)
        self.ClipOCRButton=Button(self,text="剪贴板图片识别",command=self.clipmakethread)
        self.ClipOCRButton.grid(row=0,sticky=W,padx=15,pady=3)
        self.content=ScrolledText(self)
        self.content.grid(row=1,sticky=W+E+N+S)
        #self.content.pack(side=BOTTOM,expand=YES,fill=BOTH)
        self.contentDisplay()



    def contentDisplay(self):
        try:
            data=self.dataqueue.get(block=True)
        except queue.Empty:
            pass
        else:
            self.content.insert('end',"%s\n" % str(data))
            self.content.see('end')
        self.content.after(50,self.contentDisplay)


    def fileOCR(self):
        self.content.delete(1.0,"end")
        filepath = askopenfilename()
        filekind=filetype.guess_extension(filepath)
        if filekind in ['jpg','png','bmp']:
            filename=os.path.split(filepath)[1]
            self.dataqueue.put("已获取本地图片文件:%s \n" % filename )
            contentR = []
            ocr = PaddleOCR(use_angle_cls=True)
            result = ocr.ocr(filepath, cls=True)
            for line in result:
                contentR.append(line[1][0])
            self.ocrcontent = '\n'.join(contentR)
            print(contentR)
            self.dataqueue.put("%s" % self.ocrcontent)
            #把内容写入剪贴板
            try:
                pyperclip.copy(self.ocrcontent)
                self.dataqueue.put("\n识别内容写入剪贴板")
            except:
                self.dataqueue.put("\n 识别内容写入剪贴板失败")
        else:
            self.dataqueue.put("文件不是图片，无法识别!")


    def clipOCR(self):
        self.content.delete(1.0, "end")
        im=ImageGrab.grabclipboard()
        if isinstance(im,Image.Image):
            imdata=np.array(im)
            print(im.format, im.size, im.mode)
            self.dataqueue.put("已读取剪贴板图片,图片格式%s,图片大小%s，图片模式%s \n" % (im.format,im.size,im.mode))
            contentR = []
            ocr = PaddleOCR(use_angle_cls=True)
            result = ocr.ocr(imdata, cls=True)
            for line in result:
                contentR.append(line[1][0])
            self.ocrcontent = '\n'.join(contentR)
            print(contentR)
            self.dataqueue.put("%s" % self.ocrcontent)
            # 把内容写入剪贴板
            try:
                pyperclip.copy(self.ocrcontent)
                self.dataqueue.put("\n识别内容写入剪贴板")
            except:
                self.dataqueue.put("\n 识别内容写入剪贴板失败")
        else:
            self.dataqueue.put("剪贴板无图片！")

    def filemakethread(self):
        Thread(target=self.fileOCR,args=()).start()

    def clipmakethread(self):
        Thread(target=self.clipOCR,args=()).start()





if __name__=="__main__":
    root=Tk()
    root.title("OCRPaddle")
    OCRGUI=GUI(root)

    OCRGUI.mainloop()





