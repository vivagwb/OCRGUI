from paddleocr import  PaddleOCR,draw_ocr
from tkinter import  *
from tkinter.filedialog import askopenfilename
#from threading import Thread





class GUI(Frame):
    def __init__(self,parent=None, **kwargs):
        Frame.__init__(self,parent,**kwargs)
        self.config(height=500,width=300,bg="whitesmoke")
        self.pack()
        self.var=StringVar()
        #openfile=lambda buttonReturn=askopenfilename:self.fileOCR(buttonReturn)
        FileAcquireButton=Button(self,text="本地图片识别",command=self.fileOCR)
        FileAcquireButton.pack(side=TOP,expand=YES)
        contentMessage=Message(self,textvariable=self.var,font="times")
        contentMessage.pack(side=BOTTOM,expand=YES,fill=X)


    def fileOCR(self):
        contentR=[]
        filepath=askopenfilename()
        print(filepath)
        ocr=PaddleOCR(use_angle_cls=True)
        result=ocr.ocr(filepath,cls=True)
        for line in result:
            contentR.append(line[1][0])
        print(contentR)
        self.var.set('\n'.join(contentR))
        print(self.var)


if __name__=="__main__":
    GUI().mainloop()





