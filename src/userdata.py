class UserData:
	def __init__(self, fn, stlObj, seq):
		self.fn = fn
		self.stlObj = stlObj
		self.seq = seq
		self.part = None
		self.formObjectName()
		
	def formObjectName(self):
		self.name = "%s (Object %d" % (self.fn, self.seq)
		if self.part is None:
			self.name += ")"
		else:
			self.name += " - Part %s)" % self.part
			
	def setPart(self, part):
		self.part = part
		self.formObjectName()
	
	def getName(self):
		return self.name
		
	def clone(self, seq):
		s = self.stlObj.clone()
		return UserData(self.fn, s, seq)
	
	def getStlObj(self):
		return self.stlObj
		
	def getSeqNbr(self):
		return self.seq
