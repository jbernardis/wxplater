		
class UserData:
	def __init__(self, fn, stlObj, seq):
		self.fn = fn
		self.stlObj = stlObj
		self.seq = seq
		
	def clone(self, seq):
		s = self.stlObj.clone()
		return UserData(self.fn, s, seq)
	
	def getStlObj(self):
		return self.stlObj
		
	def getSeqNbr(self):
		return self.seq
