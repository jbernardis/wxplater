import wx

BUTTONDIM = (48, 48)

class RotateDlg(wx.Dialog):
	def __init__(self, parent, stlframe, images, pos):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "", style=0, pos=pos)
		self.stlFrame = stlframe
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		
		bRot45CCW = wx.BitmapButton(self, wx.ID_ANY, images.pngRot45ccw, size=BUTTONDIM)
		self.Bind(wx.EVT_BUTTON, self.onbRot45CCW, bRot45CCW)
		bRot45CCW.SetToolTipString("Rotate 45 degrees CCW")
		sizer.Add(bRot45CCW)
		
		bRot45CW = wx.BitmapButton(self, wx.ID_ANY, images.pngRot45cw, size=BUTTONDIM)
		self.Bind(wx.EVT_BUTTON, self.onbRot45CW, bRot45CW)
		bRot45CW.SetToolTipString("Rotate 45 degrees CW")
		sizer.Add(bRot45CW)
		
		self.scDeg = wx.SpinCtrl(self, wx.ID_ANY, "Degrees", size=(60, -1))
		self.scDeg.SetRange(-359, 359)
		self.scDeg.SetValue(0)
		self.scDeg.SetToolTipString("Angle of rotation (<0 => CW rotation)")
		sizer.AddSpacer((20, 20))
		sizer.Add(self.scDeg, 1, wx.TOP, 12)
		sizer.AddSpacer((10, 10))
		
		bRot = wx.BitmapButton(self, wx.ID_ANY, images.pngRotate, size=BUTTONDIM)
		self.Bind(wx.EVT_BUTTON, self.onbRotate, bRot)
		bRot.SetToolTipString("Rotate the specified number of degrees")
		sizer.Add(bRot)
		
		bExit = wx.BitmapButton(self, wx.ID_ANY, images.pngExit, size=BUTTONDIM)
		self.Bind(wx.EVT_BUTTON, self.onbExit, bExit)
		bExit.SetToolTipString("Exit Dialog Box")
		sizer.AddSpacer((20, 20))
		sizer.Add(bExit)
		
		self.SetSizer(sizer)
		self.Fit()
		
	def onbRot45CCW(self, evt):
		self.stlFrame.rotate(45)
		
	def onbRot45CW(self, evt):
		self.stlFrame.rotate(-45)
		
	def onbRotate(self, evt):
		degrees = self.scDeg.GetValue()
		if degrees != 0:
			self.stlFrame.rotate(degrees)
		
	def onbExit(self, evt):
		self.EndModal(wx.ID_OK)
