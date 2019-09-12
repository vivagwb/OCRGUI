
#V1.4 创建一个单独线程用于调用百度OCR接口，避免调用时间过长导致界面程序卡顿


import wx
from aip import AipOcr
from PIL import ImageGrab
from PIL import Image
import io
from threading import Thread
from wx.lib.pubsub import pub
import filetype





# """ 你的 APPID AK SK """
APP_ID = '11389544'
API_KEY = '8mkOOPxRRXbhaPDChh7jeKPM'
SECRET_KEY = '8pGmWq2o3loYlNLHNkSxRbBiek3h5Vdd'

# """ OCR可选参数 """
options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "true"
options["detect_language"] = "true"
options["probability"] = "true"


#以二进制方式读取本地图片文件
def get_file_content(filePath):
     with open(filePath, 'rb') as fp:
           return fp.read()

#创建一个单独线程用于调用百度OCG，避免调用时间过长导致界面卡顿
class threadocg(Thread):

    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.start()    # start the thread

    def run(self):
    # """ 带参数调用通用文字识别, 图片参数为本地图片 """
             AipOcr.setConnectionTimeoutInMillis(self,ms=5000) #设置连接超时时间，一般没必要设置
             AipOcr.setSocketTimeoutInMillis(self,ms=6000)   #设置传送文件超时时间，一般么没必要设置
             client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
             result={}
             try:
                 result=client.basicGeneral(image, options)
                 if result.get("error_msg"):
                     print(result['error_msg'])
                     contents.SetValue(result['error_msg'])
                 else:
                     resultword=result['words_result']
                     num=result['words_result_num']
                     OCRtext=[]
                 for i in range(0,num):
                     print(resultword[i]['words'])#由于返回的信息
                     OCRtext.append(resultword[i]['words'])
                     OutPutOCRtext='\n'.join(OCRtext)
                 wx.CallAfter(pub.sendMessage,'update',re_msg="以下为识别内容")
                 wx.CallAfter(pub.sendMessage,'update',re_msg=OutPutOCRtext)

             except:
                 print('发生错误')
                 wx.CallAfter(pub.sendMessage,'update',re_msg="发生错误\n请重试")





class MyForm(wx.Frame):

    #-------------------------------------------------------------------
    #set the window layout
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "OCR程序", size =(410,335))
        global filename,contents,get_file_content,imgmark
        imgmark=""
#app=wx.App()
#win=wx.Frame(None,title='OCR程序',size=(410,335))
        bkg=wx.Panel(self,wx.ID_ANY)

        loadButton=wx.Button(bkg,label='选择文件')
        loadButton.Bind(wx.EVT_BUTTON,self.choose)

        ocrButton=wx.Button(bkg,label='识别文字')
        ocrButton.Bind(wx.EVT_BUTTON,self.OCR)

        clipButton=wx.Button(bkg,label="获取剪贴板")
        clipButton.Bind(wx.EVT_BUTTON,self.clipOCR)

        filename=wx.TextCtrl(bkg)
        contents=wx.TextCtrl(bkg,style=wx.TE_MULTILINE | wx.HSCROLL)
        #contents.SetStyle(410,335,wx.TextAttr("RED","YELLOW"))

        hbox=wx.BoxSizer()
        hbox.Add(filename,1,wx.EXPAND)
        hbox.Add(loadButton,0,wx.LEFT,5)
        hbox.Add(clipButton,0,wx.LEFT,5)
        hbox.Add(ocrButton,0,wx.LEFT,5)

        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox,0,wx.EXPAND | wx.ALL,5)
        vbox.Add(contents,1,wx.EXPAND | wx.LEFT |wx.BOTTOM | wx.RIGHT,5)

        bkg.SetSizer(vbox)

        #创建一个接收器
        pub.subscribe(self.updatedispaly,'update')


# 创建一个文件对话框，用于选择需要识别的图片并
    def choose(self,event):
        global imgmark
        wildcard1 = "All files (*.*)|*.*|" \
                    "Python source (*.py; *.pyc)|*.py;*.pyc"  #文件过滤器

        dlg = wx.FileDialog(self,message="Choose a file",defaultFile="",wildcard=wildcard1,style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
        tmp=""
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths() #返回的是一个包含路径字符串的列表
            tmp=paths[0]  #只取第一个文的路径，不做多选
            #filename.SetValue(tmp)

            gusstype=filetype.guess_extension(tmp)
            print(gusstype)
            if gusstype in ['jpg','png','bmp']:

                print('已选取图片')
                contents.SetValue("已选取图片\n\n")
                filename.SetValue(tmp)
                imgmark="已选取图片"
            else:
                print('请选取格式为jpg、png或bmp格式的图片')
                contents.SetValue("请选取格式为jpg、png或bmp格式的图片\n\n")
        else:
            print('还未选择图片')
            contents.SetValue('还未选择图片\n\n')

        dlg.Destroy()

#创建获取剪贴板函数，通过PIL模块实现
    def clipOCR(self,event):
         global imagefile,imgmark
         im = ImageGrab.grabclipboard()
         imagefile=io.BytesIO()
        #photo=Image.new('RGB',(1000,1000))
         if isinstance(im, Image.Image):
           print(im.format, im.size, im.mode)
           contents.SetValue("已获取剪贴板图片\n\n")
           im.save(imagefile,'JPEG')
           imagefile.seek(0)
           imgmark='已获取剪贴板图片'
         else:
            contents.SetValue("剪贴板无图片\n\n")
    #@timeout_decorator.timeout(10,use_signals=False,timeout_exception=TimeoutError)

#
    def OCR(self,event):
        global image,imgmark
        #AipOcr.setConnectionTimeoutInMillis(self,2000)
        #AipOcr.setSocketTimeoutInMillis(self,3000)
        #print(imgmark)
        if imgmark == "已获取剪贴板图片":
            image=imagefile.read()
            #@timeout_decorator.timeout(10,use_signals=False)
            contents.AppendText("请稍等\n\n")
            threadocg()

        elif imgmark== "已选取图片":
            image = get_file_content(filename.GetValue())
            contents.AppendText("请稍等\n\n")
            threadocg()

        else:
            contents.SetValue("请选择图片或粘贴图片\n\n")

         #return image

    def updatedispaly(self,re_msg):
        displaymessage=re_msg
        contents.AppendText(displaymessage+'\n\n')


#主函数
if __name__ == "__main__":

    app = wx.App(False)

    frame = MyForm()

    frame.Show()
    app.MainLoop()





