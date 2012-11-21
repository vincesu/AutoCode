#coding:utf-8
class DataSource():
	
	def __init__(self):
		self.__data = []
		self.__data.append(("1","2","3","4"))
		self.__data.append(("1","2","3","4"))
		self.__data.append(("1","2","3","4"))
		self.__data.append(("1","2","3","4"))
		self.__data.append(("1","2","3","4"))

	def get(self,x,y):
		return self.__data[x][y]

if __name__ == "__main__":
	print DataSource().get(1,1)
