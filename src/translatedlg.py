import wx

BUTTONDIM = (48, 48)

class TranslateDlg(wx.Dialog):
	def __init__(self, parent, stlframe, images, pos):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "", style=0, pos=pos)
		self.stlFrame = stlframe
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.scXDist = wx.SpinCtrl(self, wx.ID_ANY, "Millimeters", size=(60, -1))
		self.scXDist.SetRange(-200, 200)
		self.scXDist.SetValue(0)
		self.scXDist.SetToolTipString("Distance to move along the X axis")
		sizer.AddSpacer((20, 20))
		sizer.Add(self.scXDist, 1, wx.TOP, 12)
		sizer.AddSpacer((10, 10))
		
		self.scYDist = wx.SpinCtrl(self, wx.ID_ANY, "Millimeters", size=(60, -1))
		self.scYDist.SetRange(-200, 200)
		self.scYDist.SetValue(0)
		self.scYDist.SetToolTipString("Distance to move along the Y axis")
		sizer.AddSpacer((20, 20))
		sizer.Add(self.scYDist, 1, wx.TOP, 12)
		sizer.AddSpacer((10, 10))
		
		bMovexy = wx.BitmapButton(self, wx.ID_ANY, images.pngTranslate, size=BUTTONDIM)
		self.Bind(wx.EVT_BUTTON, self.onbMoveXY, bMovexy)
		bMovexy.SetToolTipString("move the specified number of millimeters along the X and Y axes")
		sizer.Add(bMovexy)
		
		bExit = wx.BitmapButton(self, wx.ID_ANY, images.pngExit, size=BUTTONDIM)
		self.Bind(wx.EVT_BUTTON, self.onbExit, bExit)
		bExit.SetToolTipString("Exit Dialog Box")
		sizer.AddSpacer((20, 20))
		sizer.Add(bExit)
		
		self.SetSizer(sizer)
		self.Fit()
		
	def onbMoveXY(self, evt):
		dx = self.scXDist.GetValue()
		dy = self.scYDist.GetValue()
		
		if dx != 0 or dy != 0:
			self.stlFrame.translatexy(dx, dy)
		
	def onbExit(self, evt):
		self.EndModal(wx.ID_OK)
