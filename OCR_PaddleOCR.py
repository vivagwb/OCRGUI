from paddleocr import  PaddleOCR,draw_ocr
from tkinter import  *
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
from threading import Thread
import queue
import time
import filetype
import pyperclip





class GUI(Frame):
    def __init__(self,parent=None, **kwargs):
        Frame.__init__(self,parent,**kwargs)
        self.config(height=500,width=300,bg="white")
        self.pack()
        self.dataqueue=queue.Queue()
        #self.var=StringVar()
        #openfile=lambda buttonReturn=askopenfilename:self.fileOCR(buttonReturn)
        self.FileOCRButton=Button(self,text="本地图片识别",command=self.makethread)
        self.FileOCRButton.pack(side=TOP,expand=YES,fill=X)
        self.content=ScrolledText(self)
        self.content.pack(side=BOTTOM,expand=YES,fill=BOTH)
        self.contentDisplay()



    def contentDisplay(self):
        try:
            data=self.dataqueue.get(block=False)
        except queue.Empty:
            pass
        else:
            self.content.insert('end',"%s\n" % str(data))
        self.content.see('end')
        self.content.after(100,self.contentDisplay)


    def fileOCR(self):
        self.content.delete(1.0,"end")
        filepath = askopenfilename()
        filekind=filetype.guess_extension(filepath)
        if filekind in ['jpg','png','bmp']:
            self.Avaialfilepath=filepath
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



    def makethread(self):
        Thread(target=self.fileOCR,args=()).start()



if __name__=="__main__":
    root=Tk()
    root.title("OCRPaddle")
    OCRGUI=GUI(root)

    OCRGUI.mainloop()





