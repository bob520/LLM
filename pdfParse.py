# -*- coding: utf-8 -*-
import os
import re
import sys
import io
from pdfminer.pdfpage import PDFPage
# from pdfminer.converter import TextConverter
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
# from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

# 解析文本用到的类：
# PDFParser（文档分析器）：从文件中获取数据
# PDFDocument（文档对象）：保存文件数据
# PDFPageInterpreter（解释器）：处理页面内容
# PDFResourceManager（资源管理器）：存储共享资源
# PDFDevice:将解释器处理好的内容转换为我们所需要的
# PDFPageAggregator（聚合器）:读取文档对象
# LAParams（参数分析器）

# convert one PDF file to TXT file
def onePdfToTxt(base_path,filename,outpath):
    try:
        filepath=os.path.join(base_path, filename)
        #rb以二进制读模式打开本地pdf文件
        fp = open(filepath, 'rb')
        outfp = open(outpath, 'w', encoding='utf-8')
        #创建一个pdf文档分析器
        parser = PDFParser(fp)
        #创建一个PDF文档
        doc= PDFDocument(parser)
        #创建PDf资源管理器
        resource = PDFResourceManager()
        #创建一个PDF参数分析器
        laparams = LAParams()
        #创建聚合器,用于读取文档的对象
        device = PDFPageAggregator(resource,laparams=laparams)
        #创建解释器，对文档编码，解释成Python能够识别的格式
        interpreter = PDFPageInterpreter(resource,device)
        start_saving = False
        # 循环遍历列表，每次处理一页的内容 doc.get_pages() 获取page列表
        for page in enumerate(PDFPage.create_pages(doc)):
            # 固定忽略前2页
            if page[0]<2:
                continue
            print("当前的页面是", page[0])
            # 每一页的初始段落块都是空
            text_blocks = []
            #利用解释器的process_page()方法解析读取单独页数
            interpreter.process_page(page[1])
            #使用聚合器get_result()方法获取内容
            layout = device.get_result()
            #这里layout是一个LTPage对象,里面存放着这个page解析出的各种对象
            for out in layout:
                #判断是否含有get_text()方法，获取我们想要的文字
                if hasattr(out,"get_text"):
                    # text是一段文字，而不是一行
                    text=out.get_text()
                    # if page[0]==8:
                    #     print(text)
                    #保留text中最后一个换行，把文本中间的所有换行去掉。
                    if not (text.startswith("GB") or text.startswith("DB") or text.startswith("NY")):
                        text = text.replace('\n', '')
                        text=text+"\n"
                    # 把这一页的所有段落存储起来
                    text_blocks.append(text)
            if len(text_blocks)>2:
                # 去掉每一页的开头和最后一个文本块
                for text in text_blocks[1:-1]:
                    # 检测是否包含“引言”的开头
                    if text.startswith("引 言") or text.startswith("引\n"):
                        start_saving = True
                    else:
                        if text.startswith("1 范围") or text.startswith("1  范围"):
                            title=filename.replace(".pdf","\n")
                            outfp.write(title)
                            start_saving = True
                    if text.startswith("附录") or text.startswith("附 录"):
                        start_saving = False
                    if start_saving:
                        outfp.write(text)
        fp.close()
        outfp.close()
    except Exception as e:
         print (e)

# convert all PDF files in a folder to TXT files
def manyPdfToTxt (fileDir):
    fileDir_long="../dbba_pdf"+'/'+fileDir
    files = os.listdir(fileDir_long)
    tarDir = "../dbba_txt"+'/'+fileDir
    if not os.path.exists(tarDir):
        os.mkdir(tarDir)
    replace = re.compile(r'\.pdf',re.I)
    for file in files:
        outPath = tarDir+'/'+re.sub(replace, '', file)+'.txt'
        onePdfToTxt(fileDir_long,file, outPath)
        print("saved in "+outPath)

def fix_zero_txt(fileDir):
    fileDir_long="../dbba_pdf"+'/'+fileDir
    empty_files=[]
    tarDir = "../dbba_txt"+'/'+fileDir
    files = os.listdir(tarDir)
    for i in files:
        full_path=tarDir+'/'+i
        if os.path.getsize(full_path) == 0:  # 检查文件大小
            empty_files.append(i)
    replace = re.compile(r'\.txt',re.I)
    for zero_txt_name in empty_files:
        outPath = tarDir+'/'+ zero_txt_name
        pdf_name=re.sub(replace, '', zero_txt_name)+'.pdf'
        onePdfToTxt(fileDir_long,pdf_name, outPath)
        print("saved in "+outPath)

def del_zero_txt(fileDir):
    tarDir = "../dbba_txt"+'/'+fileDir
    files = os.listdir(tarDir)
    count=0
    for i in files:
        full_path=tarDir+'/'+i
        if os.path.getsize(full_path) == 0:  # 检查文件大小
            os.remove(full_path)
            count+=1
    print(fileDir+"删除个数是"+str(count))

def sum_file_num(fileDir):
    tarDir = "../dbba_txt" + '/' + fileDir
    files = os.listdir(tarDir)
    print("当前的种类的文本个数是",fileDir,len(files))
    return len(files)

import os
folder_path = "../dbba_pdf"
subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
num=0
sum=0
for subf in subfolders:
    # manyPdfToTxt(subf)
    # fix_zero_txt(subf)
    # del_zero_txt(subf)
    num=sum_file_num(subf)
    sum+=num
print("总文档个数是:",sum)