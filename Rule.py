#coding:utf-8
from DataSource import DataSource

class AbstractRule():

	rules = None

	targetName = None
	startName = None
	endName = None

	def __init__(self,sp,ep,d,lines):
		self.startPosition = sp
		self.endPosition = ep
		self.lines = lines
		self.setData(d)
	
	def setData(self,string):
		return None
	
	def execute(self):
		return ""

class ReplaceRule(AbstractRule):

	targetName = "r"
	startName = "[r]"
	endName = "[/r]"

	def __init__(self,sp,ep,dataString,lines=None):
		AbstractRule.__init__(self,sp,ep,dataString,lines)
	
	def setData(self,string):
		strings = string.split(",")
		if len(strings) == 2:
			self.x = int(strings[0])
			self.y = int(strings[1])
		
	def execute(self):
		return DataSource().get(self.x,self.y)

def getRules():
	if not AbstractRule.rules:
		AbstractRule.rules = {}
		for k in globals().keys():
			if str(k).endswith("Rule") and str(k) != "AbstractRule":
				AbstractRule.rules[globals()[k].targetName] = globals()[k]
	return AbstractRule.rules

if __name__ == "__main__":
	print getRules()
	r = ReplaceRule(1,1,"1,1")
	print r.execute()
