import wx

BUTTONDIM = (48, 48)
XAXIS = 1
YAXIS = 2
ZAXIS = 3


class MirrorDlg(wx.Dialog):
	def __init__(self, parent, images, pos):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "", style=0, pos=pos)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		
		bX = wx.BitmapButton(self, wx.ID_ANY, images.pngXaxis, size=BUTTONDIM)
		self.Bind(wx.EVT_BUTTON, self.onbX, bX)
		bX.SetToolTipString("Mirror on X Axis")
		sizer.Add(bX)
		
		bY = wx.BitmapButton(self, wx.ID_ANY, images.pngYaxis, size=BUTTONDIM)
		self.Bind(wx.EVT_BUTTON, self.onbY, bY)
		bY.SetToolTipString("Mirror on Y Axis")
		sizer.Add(bY)
		
		bZ = wx.BitmapButton(self, wx.ID_ANY, images.pngZaxis, size=BUTTONDIM)
		self.Bind(wx.EVT_BUTTON, self.onbZ, bZ)
		bZ.SetToolTipString("Mirror on Z Axis")
		sizer.Add(bZ)
		
		bCancel = wx.BitmapButton(self, wx.ID_ANY, images.pngCancel, size=BUTTONDIM)
		self.Bind(wx.EVT_BUTTON, self.onbCancel, bCancel)
		bCancel.SetToolTipString("Cancel Mirror Operation")
		sizer.AddSpacer((20, 20))
		sizer.Add(bCancel)
		
		self.SetSizer(sizer)
		self.Fit()
		
	def onbX(self, evt):
		self.EndModal(XAXIS)
		
	def onbY(self, evt):
		self.EndModal(YAXIS)
		
	def onbZ(self, evt):
		self.EndModal(ZAXIS)
		
	def onbCancel(self, evt):
		self.EndModal(wx.ID_CANCEL)

