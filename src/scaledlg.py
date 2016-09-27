import wx

BUTTONDIM = (48, 48)

class ScaleDlg(wx.Dialog):
	def __init__(self, parent, stlframe, images, pos):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "", style=0, pos=pos)
		self.stlFrame = stlframe
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.uniform = False
		
		self.scXFactor = wx.SpinCtrl(self, wx.ID_ANY, "ScaleX", size=(60, -1))
		self.scXFactor.SetRange(1, 200)
		self.scXFactor.SetValue(100)
		self.scXFactor.SetToolTipString("Scaling factor (%) for the X axis")
		sizer.AddSpacer((20, 20))
		self.Bind(wx.EVT_SPINCTRL, self.onscXFactor, self.scXFactor)
		sizer.Add(self.scXFactor, 1, wx.TOP, 12)
		sizer.AddSpacer((10, 10))
		
		self.scYFactor = wx.SpinCtrl(self, wx.ID_ANY, "ScaleY", size=(60, -1))
		self.scYFactor.SetRange(1, 200)
		self.scYFactor.SetValue(100)
		self.scYFactor.SetToolTipString("Scaling factor (%) for the Y axis")
		sizer.AddSpacer((20, 20))
		sizer.Add(self.scYFactor, 1, wx.TOP, 12)
		sizer.AddSpacer((10, 10))
		
		self.scZFactor = wx.SpinCtrl(self, wx.ID_ANY, "ScaleZ", size=(60, -1))
		self.scZFactor.SetRange(1, 200)
		self.scZFactor.SetValue(100)
		self.scZFactor.SetToolTipString("Scaling factor (%) for the Z axis")
		sizer.AddSpacer((20, 20))
		sizer.Add(self.scZFactor, 1, wx.TOP, 12)
		sizer.AddSpacer((20, 10))
		
		self.cbUniform = wx.CheckBox(self, wx.ID_ANY, "Uniform Scaling")
		self.cbUniform.SetValue(False)
		self.cbUniform.SetToolTipString("Scale uniformly along all 3 axes")
		sizer.Add(self.cbUniform, 2, wx.TOP, 16)
		self.Bind(wx.EVT_CHECKBOX, self.oncbUniform, self.cbUniform)
		sizer.AddSpacer((10, 10))
		
		bScale = wx.BitmapButton(self, wx.ID_ANY, images.pngScale, size=BUTTONDIM)
		self.Bind(wx.EVT_BUTTON, self.onbScale, bScale)
		bScale.SetToolTipString("Scale the selected object by the specified scaling factors")
		sizer.Add(bScale)
		sizer.AddSpacer((10, 10))
		
		bExit = wx.BitmapButton(self, wx.ID_ANY, images.pngExit, size=BUTTONDIM)
		self.Bind(wx.EVT_BUTTON, self.onbExit, bExit)
		bExit.SetToolTipString("Exit Dialog Box")
		sizer.AddSpacer((20, 20))
		sizer.Add(bExit)
		
		self.SetSizer(sizer)
		self.Fit()
		
	def oncbUniform(self, evt):
		self.uniform = self.cbUniform.GetValue()
		if self.uniform:
			v = self.scXFactor.GetValue()
			self.scYFactor.SetValue(v)
			self.scZFactor.SetValue(v)
			self.scYFactor.Enable(False)
			self.scZFactor.Enable(False)
			self.scXFactor.SetToolTipString("Scaling factor (%) for the X, Y, and Z axes")
		else:
			self.scYFactor.Enable(True)
			self.scZFactor.Enable(True)
			self.scXFactor.SetToolTipString("Scaling factor (%) for the X axis")
			
	def onscXFactor(self, evt):
		if self.uniform:
			v = self.scXFactor.GetValue()
			self.scYFactor.SetValue(v)
			self.scZFactor.SetValue(v)
		
	def onbScale(self, evt):
		sx = self.scXFactor.GetValue() / 100.0
		sy = self.scYFactor.GetValue() / 100.0
		sz = self.scZFactor.GetValue() / 100.0
		
		if sx != 1 or sy != 1 or sz != 1:
			self.stlFrame.scalexyz(sx, sy, sz)
		
	def onbExit(self, evt):
		self.EndModal(wx.ID_OK)
