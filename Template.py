#coding:utf-8
import util
import Rule
from cStringIO import StringIO

class Position():
	#位置类

	def __init__(self,row,column):
		self.row = row	#行
		self.column = column	#每行位置

class Template():

	def __init__(self,path):
		self.path = path
		self.lines = [] #字符串数据列表
		self.rules = []

		i=0;
		f = None
		try:
			#读取文件存入列表
			f = file(path)
			while True:
				self.lines.append(unicode(f.readline()))
				if len(self.lines[i]) == 0: # Zero length indicates EOF
					break
				i+=1
			#删除最后一行空行
			del self.lines[i]
		except IOError:
			raise IOError("%s%s%s" % ("this file is not exists(",path,")"))
		finally:
			if f!=None:
				f.close()

		self.__formatTemplate()
		#self.currentPosition = Position(0,0)	#start find position

	
	def __duplicatePart(self,sp,ep):

		result = []
		index = sp.row
		b = e = 0
		while index<=ep.row:
			
			if index == sp.row: b=sp.column
			else: b=0

			if index == ep.row: e=ep.column+1
			else: e=len(self.lines[index])

			line = self.lines[index][b:e]
			
			if line!=None and line!="":
				result.append(line)

			index+=1

		return result

	def __formatTemplate(self):

		i = Position(0,0)								#扫描时行数
		eIndex = bIndex = -1                #临时变量 记录rule在y坐标 起始位置和截止位置
		length = len(self.lines)            #行数
		startPosition = endPosition = None  #临时变量 记录rule起始位置和截止位置
		dpStartPos = dpEndPos = None        #临时变量 记录rule对应模版截取的 起始位置和截止位置
		targetName = None                   #临时变量 记录rule的targetName
		dataString = None                   #临时变量 记录rule的dataString
		tmpIndex = None                     #y坐标的临时变量
		lines = None                        #临时变量 记录复制的rule的lines(从dpStartPos和dpEndPos复制出来的内容)

		while i.row<length:

			bIndex = self.lines[i.row].find("[",i.column)
			if bIndex == -1:
				i.row+=1
				i.column = 0
				continue
			eIndex = self.lines[i.row].find("]",bIndex+1)
			#获得targetName
			targetName = self.lines[i.row][bIndex+1:eIndex]
			#获得rule 起始位置
			startPosition = Position(i.row,bIndex)
			tmpIndex = self.lines[i.row].find("]",eIndex+1)
			#获得dataString
			dataString = self.lines[i.row][(eIndex+1):tmpIndex]
			#截取内容的起始位置
			dpStartPos = Position(i.row,tmpIndex+1)

			tmpIndex = self.lines[i.row].find(Rule.getRules()[targetName].endName,tmpIndex+1)
			while tmpIndex==-1 and i.row<length:
				i.row+=1
				tmpIndex = self.lines[i.row].find(Rule.getRules()[targetName].endName)

			if tmpIndex == -1:
				raise Exception()

			#获得rule截止位置
			endPosition = Position(i.row,tmpIndex+len(Rule.getRules()[targetName].endName)-1)
			i.column = tmpIndex+1
			#截取内容的截止位置
			if tmpIndex:
				dpEndPos = Position(i.row,tmpIndex-1)
			else:
				dpEndPos = Position(i.row-1,len(self.lines[i.row-1]))

			#截取模版内容
			lines = self.__duplicatePart(dpStartPos,dpEndPos)
			#创建rule
			self.rules.append(Rule.getRules()[targetName](startPosition,endPosition,dataString,lines))


	def Generate(self):

		i = Position(0,0)				#当前写入位置
		j = 0                           #当前rule的index
		length = len(self.lines)        #模版行数
		rules_count = len(self.rules)   #rule总数
		data = None                     #保存rule执行后返回的string list，然后写入文本
		line = None                     #临时变量-单行文本

		file_str = StringIO()

		while i.row<length:
			
			if  j<rules_count and self.rules[j].startPosition.row == i.row:
				file_str.write(self.lines[i.row][i.column:self.rules[j].startPosition.column])
				data = self.rules[j].execute()

				if data:
					h = 0
					while h<(len(data)-1):
						file_str.write(data[h])
						#file_str.write("\n")
						h+=1
					file_str.write(data[h])

				i.row = self.rules[j].endPosition.row
				i.column = self.rules[j].endPosition.column+1
				j+=1
			else:
				line = self.lines[i.row][i.column:]
				if line!=None and line!="":
					file_str.write(line)
				#file_str.write("\n")
				i.row +=1
				i.column = 0

		return file_str.getvalue()

	def GenerateFile(self,path):
		s = self.Generate()
		f = None
		try:
			f = open(path,"w")
			f.write(s)
		except:
			print "%s%s%s" % ("can not write file on path(",path,")")
		finally:
			if f:
				f.close()



if __name__ == "__main__":

	util.setSysCoding()

	template = Template("test_data/d.txt")
#	lines = ["string1",
#			 "string2",
#			 "[r]1,1]",
#			 "aaaaa",
#			 "bbb",
#			 "[/r]",
#			 "stri[r]1,1]cccc[/r]ng3"]
#	template = Template(lines)
	print template.rules
	for r in template.rules:
		print r.lines
	
	print template.Generate()
	template.GenerateFile("test_data/file.txt")









