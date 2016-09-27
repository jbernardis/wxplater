import wx
import os
import sys, inspect

cmdFolder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmdFolder not in sys.path:
	sys.path.insert(0, cmdFolder)

from images import Images
from filelist import FileList	
from userdata import UserData
from stltool import stl, emitstl
from stlframe import StlFrame
from settings import Settings
from stlview import StlViewer, VIEW_MODE_LOAD, VIEW_MODE_LOOK_HERE
from mirrordlg import MirrorDlg, XAXIS, YAXIS, ZAXIS
from rotatedlg import RotateDlg
from translatedlg import TranslateDlg
from scaledlg import ScaleDlg
from gridparamsdlg import GridParamsDlg

BUTTONDIM = (48, 48)

class StlProxy:
	pass



class PlaterFrame(wx.Frame):

	def __init__(self):
		self.t = 0
		self.seq = 0
		self.modified = False
		self.settings = Settings(cmdFolder)
		wx.Frame.__init__(self, None, -1, "Plater", size=(300, 300))
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		self.images = Images(os.path.join(cmdFolder, "images"))
		
		self.stlCanvas = StlFrame(self, self.settings)
		
		self.bAdd = wx.BitmapButton(self, wx.ID_ANY, self.images.pngAdd, size=BUTTONDIM)
		self.bAdd.SetToolTipString("Add an STL file to the plate")
		self.Bind(wx.EVT_BUTTON, self.doAdd, self.bAdd)
		
		self.bClone = wx.BitmapButton(self, wx.ID_ANY, self.images.pngClone, size=BUTTONDIM)
		self.bClone.SetToolTipString("Add a copy of the selected object")
		self.Bind(wx.EVT_BUTTON, self.doClone, self.bClone)
		self.bClone.Enable(False)
		
		self.bDel = wx.BitmapButton(self, wx.ID_ANY, self.images.pngDel, size=BUTTONDIM)
		self.bDel.SetToolTipString("Delete the selected object from the plate")
		self.Bind(wx.EVT_BUTTON, self.doDel, self.bDel)
		self.bDel.Enable(False)
		
		self.bDelall = wx.BitmapButton(self, wx.ID_ANY, self.images.pngDelall, size=BUTTONDIM)
		self.bDelall.SetToolTipString("Delete ALL objects from the plate")
		self.Bind(wx.EVT_BUTTON, self.doDelall, self.bDelall)
		self.bDelall.Enable(False)
		
		self.bArrange = wx.BitmapButton(self, wx.ID_ANY, self.images.pngArrange, size=BUTTONDIM)
		self.bArrange.SetToolTipString("Arrange the objects on the plate")
		self.Bind(wx.EVT_BUTTON, self.doArrange, self.bArrange)
		self.bArrange.Enable(False)
		
		self.bCenter = wx.BitmapButton(self, wx.ID_ANY, self.images.pngCenter, size=BUTTONDIM)
		self.bCenter.SetToolTipString("Center the plate")
		self.Bind(wx.EVT_BUTTON, self.doCenter, self.bCenter)
		self.bCenter.Enable(False)
		
		self.bGrid = wx.BitmapButton(self, wx.ID_ANY, self.images.pngGrid, size=BUTTONDIM)
		self.bGrid.SetToolTipString("Create a grid of the selected object")
		self.Bind(wx.EVT_BUTTON, self.doGrid, self.bGrid)
		self.bGrid.Enable(False)
		
		self.bMirror = wx.BitmapButton(self, wx.ID_ANY, self.images.pngMirror, size=BUTTONDIM)
		self.bMirror.SetToolTipString("Mirror the selected object")
		self.Bind(wx.EVT_BUTTON, self.doMirror, self.bMirror)
		self.bMirror.Enable(False)
		
		self.bRotate = wx.BitmapButton(self, wx.ID_ANY, self.images.pngRotate, size=BUTTONDIM)
		self.bRotate.SetToolTipString("Rotate the selected object")
		self.Bind(wx.EVT_BUTTON, self.doRotate, self.bRotate)
		self.bRotate.Enable(False)
		
		self.bTranslate = wx.BitmapButton(self, wx.ID_ANY, self.images.pngTranslate, size=BUTTONDIM)
		self.bTranslate.SetToolTipString("Translate the selected object")
		self.Bind(wx.EVT_BUTTON, self.doTranslate, self.bTranslate)
		self.bTranslate.Enable(False)
		
		self.bScale = wx.BitmapButton(self, wx.ID_ANY, self.images.pngScale, size=BUTTONDIM)
		self.bScale.SetToolTipString("Scale the selected object")
		self.Bind(wx.EVT_BUTTON, self.doScale, self.bScale)
		self.bScale.Enable(False)
		
		self.bExport = wx.BitmapButton(self, wx.ID_ANY, self.images.pngExport, size=BUTTONDIM)
		self.bExport.SetToolTipString("Export the plate to an STL file")
		self.Bind(wx.EVT_BUTTON, self.doExport, self.bExport)
		self.bExport.Enable(False)
		
		self.bView = wx.BitmapButton(self, wx.ID_ANY, self.images.pngView, size=BUTTONDIM)
		self.bView.SetToolTipString("View the currently selected file")
		self.Bind(wx.EVT_BUTTON, self.doView, self.bView)
		self.bView.Enable(False)
		
		self.bViewPlate = wx.BitmapButton(self, wx.ID_ANY, self.images.pngViewplate, size=BUTTONDIM)
		self.bViewPlate.SetToolTipString("View the entire plate")
		self.Bind(wx.EVT_BUTTON, self.doViewPlate, self.bViewPlate)
		self.bViewPlate.Enable(False)
		
		self.cbPreview = wx.CheckBox(self, wx.ID_ANY, "3D Preview")
		self.cbPreview.SetValue(self.settings.preview)
		self.Bind(wx.EVT_CHECKBOX, self.onCbPreview, self.cbPreview)
		
		self.cbCenterOnArrange = wx.CheckBox(self, wx.ID_ANY, "Center Plate After Arrange")
		self.cbCenterOnArrange.SetValue(self.settings.centeronarrange)
		self.Bind(wx.EVT_CHECKBOX, self.onCbCenterOnArrange, self.cbCenterOnArrange)
		
		self.strategyList = ['column', 'row']
		self.rbStrategy = wx.RadioBox(
				self, -1, "Arrange Strategy", wx.DefaultPosition, wx.DefaultSize,
				self.strategyList, 1, wx.RA_SPECIFY_COLS
				)
		
		self.Bind(wx.EVT_RADIOBOX, self.onStrategy, self.rbStrategy)
		self.rbStrategy.SetToolTipString("Choose the strategy for auto-arrange")
		if not self.settings.arrangestrategy in self.strategyList:
			self.settings.arrangestrategy = self.strategyList[0]
		self.rbStrategy.SetStringSelection(self.settings.arrangestrategy)
		
		self.scMargin = wx.SpinCtrl(self, wx.ID_ANY, "Arrange Margin", size=(40, -1))
		self.scMargin.SetRange(1,5)
		self.scMargin.SetValue(self.settings.arrangemargin)
		self.scMargin.SetToolTipString("Choose the distance between objects")
		self.Bind(wx.EVT_SPINCTRL, self.onScMargin, self.scMargin)

		
		szFrame = wx.BoxSizer(wx.HORIZONTAL)
		szLeft = wx.BoxSizer(wx.VERTICAL)
		
		szCanvas = wx.BoxSizer(wx.VERTICAL)
		szCanvas.AddSpacer((10, 20))
		szCanvas.Add(self.stlCanvas)
		szCanvas.AddSpacer((10, 10))
		
		szLeft.Add(szCanvas)
		szRight = wx.BoxSizer(wx.VERTICAL)
		
		self.files = FileList(self)
		self.Bind(wx.EVT_LISTBOX, self.doFileSelect, self.files)
		szRight.AddSpacer((10, 20))
		szRight.Add(self.files)
		szRight.AddSpacer((10, 10))
		
		szBtn = wx.BoxSizer(wx.VERTICAL)
		szBtnLn1 = wx.BoxSizer(wx.HORIZONTAL)
		szBtnLn2 = wx.BoxSizer(wx.HORIZONTAL)
		szBtnLn3 = wx.BoxSizer(wx.HORIZONTAL)
		szOptions = wx.BoxSizer(wx.HORIZONTAL)
		szOptionsL = wx.BoxSizer(wx.VERTICAL)
		szOptionsR = wx.BoxSizer(wx.VERTICAL)
		
		szBtnLn1.Add(self.bAdd)
		szBtnLn1.Add(self.bDel)
		szBtnLn1.Add(self.bDelall)
		szBtnLn1.AddSpacer(BUTTONDIM)
		szBtnLn1.Add(self.bView)
		szBtnLn1.Add(self.bViewPlate)
		szBtnLn1.AddSpacer(BUTTONDIM)
		szBtnLn1.Add(self.bExport)
		
		szBtnLn2.Add(self.bArrange)
		szBtnLn2.Add(self.bCenter)
		szBtnLn2.AddSpacer(BUTTONDIM)
		szBtnLn2.Add(self.bClone)
		szBtnLn2.Add(self.bGrid)
		szBtnLn2.AddSpacer([BUTTONDIM[0]*3, BUTTONDIM[1]])
		
		szBtnLn3.Add(self.bMirror)
		szBtnLn3.Add(self.bRotate)
		szBtnLn3.Add(self.bTranslate)
		szBtnLn3.Add(self.bScale)
		szBtnLn3.AddSpacer([BUTTONDIM[0]*4, BUTTONDIM[1]])
		
		szBtn.Add(szBtnLn1)
		szBtn.Add(szBtnLn2)
		szBtn.Add(szBtnLn3)
		
		szRight.Add(szBtn, 1, wx.ALIGN_CENTER_HORIZONTAL)
		szRight.AddSpacer((5, 5))
		
		szOptionsL.Add(self.cbPreview)
		szOptionsL.AddSpacer((5, 5))
		szOptionsL.Add(self.cbCenterOnArrange)

		szOptionsR.Add(self.rbStrategy)
		szOptionsR.AddSpacer((5, 5))
		szMargin = wx.BoxSizer(wx.HORIZONTAL)
		szMargin.Add(wx.StaticText(self, wx.ID_ANY, "Arrange margin:"))
		szMargin.AddSpacer((5,5))
		szMargin.Add(self.scMargin)
		szOptionsR.Add(szMargin)
		
		szOptions.AddSpacer((10, 10))
		szOptions.Add(szOptionsL)
		szOptions.AddSpacer((30, 10))
		szOptions.Add(szOptionsR)
		szOptions.AddSpacer((10, 10))
		
		szRight.Add(szOptions, 1, wx.ALIGN_CENTER_HORIZONTAL)
		#szRight.AddSpacer((10, 10))

		szFrame.AddSpacer((20, 10))		
		szFrame.Add(szLeft)
		szFrame.AddSpacer((20, 10))		
		szFrame.Add(szRight)
		szFrame.AddSpacer((20, 10))		
		
		self.SetSizer(szFrame)
		self.Layout()
		self.Fit()
		
	def enableButtons(self):
		v = (self.files.countFiles() > 0)
		fn = self.files.getSelection()[0]
		
		self.bClone.Enable(v and not fn is None)
		self.bGrid.Enable(v and not fn is None)
		self.bDel.Enable(v and not fn is None)
		self.bView.Enable(v and not fn is None)
		self.bMirror.Enable(v and not fn is None)
		self.bRotate.Enable(v and not fn is None)
		self.bTranslate.Enable(v and not fn is None)
		self.bScale.Enable(v and not fn is None)
		self.bDelall.Enable(v)
		self.bArrange.Enable(v)
		self.bCenter.Enable(v)
		self.bExport.Enable(v)
		self.bViewPlate.Enable(v)
		
	def onScMargin(self, evt):
		self.settings.arrangemargin = self.scMargin.GetValue()

	def onCbPreview(self, evt):
		self.settings.preview = self.cbPreview.GetValue()
		
	def onStrategy(self, evt):
		self.settings.arrangestrategy = self.strategyList[evt.GetInt()]

	def onCbCenterOnArrange(self, evt):
		self.settings.centeronarrange = self.cbCenterOnArrange.GetValue()

	def doAdd(self, evt):
		wildcard = "STL (*.stl)|*.stl|"	 \
			"All files (*.*)|*.*"
			
		while True:
			dlg = wx.FileDialog(
				self, message="Choose an STL file",
				defaultDir=self.settings.lastdirectory, 
				defaultFile="",
				wildcard=wildcard,
				style=wx.OPEN)
	
			rc = dlg.ShowModal()
			if rc == wx.ID_OK:
				path = dlg.GetPath().encode('ascii','ignore')
			dlg.Destroy()
			if rc != wx.ID_OK:
				return
			
			self.settings.lastdirectory = os.path.dirname(path)
			
			if self.settings.preview:
				dlg = StlViewer(self, path, path, VIEW_MODE_LOAD, self.images, self.settings)
				rc = dlg.ShowModal()
				dlg.Destroy()
			
			if not self.settings.preview or rc == wx.ID_OK:
				stlFile = stl(filename = path)
				self.files.addFile(path, UserData(path, stlFile, self.seq))
				self.stlCanvas.addHull(stlFile, self.seq)
				self.seq += 1
				self.modified = True
				self.enableButtons()
				return
			
	def setFilesSelection(self, seq):
		self.files.setSelection(seq)
		self.enableButtons()
		
	def setHullSelection(self, seq):
		self.stlCanvas.setSelection(seq)
		self.enableButtons()
		
	def doClone(self, evt):
		self.clone()
		
	def clone(self):
		self.stlCanvas.commitDeltas(None)
		fn, ud = self.files.getSelection()
		if fn is None:
			return
		
		mySeq = self.seq
		self.seq += 1
		udNew = ud.clone(mySeq)
		
		self.files.addFile(fn, udNew)
		self.stlCanvas.addHull(udNew.getStlObj(), mySeq)
			
		self.modified = True
		self.enableButtons()
		return mySeq
		
	def doDel(self, evt):
		fx = self.files.getSelectionIndex()
		if fx == wx.NOT_FOUND:
			return
		
		ud = self.files.getUserDataByIndex(fx)
		if not ud is None:
			self.stlCanvas.delHull(ud.getSeqNbr())
			
		self.files.delFileByIndex(fx)
		if self.files.countFiles() > 0:
			self.modified = True
		else:
			self.modified = False
			self.seq = 0

		self.enableButtons()
		
	def doDelall(self, evt):
		dlg = wx.MessageDialog(self,
			"This will delete ALL items.\nAre you sure you want to do this?",
			"Confirm Delete All",
			wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		rc = dlg.ShowModal()
		dlg.Destroy()
		if rc == wx.ID_YES:
			self.modified = False
			self.files.delAll()
			self.stlCanvas.delAllHulls()
			self.seq = 0
			self.enableButtons()
		
	def doArrange(self, evt):
		self.stlCanvas.arrange()
		
	def doMirror(self, evt):
		dlg = MirrorDlg(self, self.images, wx.GetMousePosition())
		rc = dlg.ShowModal()
		dlg.Destroy()
		
		if rc == XAXIS:	
			self.stlCanvas.yzMirror()
		elif rc == YAXIS:	
			self.stlCanvas.xzMirror()
		elif rc == ZAXIS:	
			self.stlCanvas.xyMirror()
			
	def doRotate(self, evt):
		dlg = RotateDlg(self, self.stlCanvas, self.images, wx.GetMousePosition())
		dlg.ShowModal()
		dlg.Destroy()
			
	def doTranslate(self, evt):
		dlg = TranslateDlg(self, self.stlCanvas, self.images, wx.GetMousePosition())
		dlg.ShowModal()
		dlg.Destroy()
			
	def doScale(self, evt):
		dlg = ScaleDlg(self, self.stlCanvas, self.images, wx.GetMousePosition())
		dlg.ShowModal()
		dlg.Destroy()
		
	def doCenter(self, evt):
		self.stlCanvas.centerPlate()
		
	def doGrid(self, evt):
		fn, ud = self.files.getSelection()
		if fn is None:
			return
		
		masterSeq = ud.getSeqNbr()
		dlg = GridParamsDlg(self, self.images, wx.GetMousePosition())
		rc = dlg.ShowModal()
		if rc == wx.ID_OK:
			rows, cols = dlg.getValues()
			
		dlg.Destroy()
		if rc != wx.ID_OK:
			return
		
		copies = rows * cols - 1
		
		seqNbrs = [masterSeq]
		for i in range(copies):
			seqNbrs.append(self.clone())
			
		self.stlCanvas.gridArrange(seqNbrs, rows, cols)
		
	def doExport(self, evt):
		wildcard = "STL (*.stl)|*.stl"
		dlg = wx.FileDialog(
			self, message="Save file as ...", defaultDir=self.settings.lastdirectory, 
			defaultFile="", wildcard=wildcard, style=wx.SAVE | wx.FD_OVERWRITE_PROMPT
			)
		
		rc = dlg.ShowModal()
		if rc == wx.ID_OK:
			path = dlg.GetPath()
			
		dlg.Destroy()
		if rc != wx.ID_OK:
			return
		
		self.stlCanvas.commitDeltas(None)
		objs = self.files.getStlObjects()
		facets = []
		for o in objs:
			facets.extend(o.facets)
		
		emitstl(path, facets=facets, objname="PlaterObject", binary=False)
		self.modified = False
		
		dlg = wx.MessageDialog(self,
			"File '%s' written" % path,
			"Save",
			wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()

	def doView(self, evt):
		self.stlCanvas.commitDeltas(None)
		fn, ud = self.files.getSelection()
		title = "%s (Object %d)" % (fn, ud.getSeqNbr())
		dlg = StlViewer(self, ud.getStlObj(), title, VIEW_MODE_LOOK_HERE, self.images, self.settings)
		dlg.ShowModal()
		dlg.Destroy()
		
	def doViewPlate(self, evt):
		self.stlCanvas.commitDeltas(None)
		objs = self.files.getStlObjects()
		
		plateStl = StlProxy()
		plateStl.facets = []
		for o in objs:
			plateStl.facets.extend(o.facets)
		dlg = StlViewer(self, plateStl, "Plate", VIEW_MODE_LOOK_HERE, self.images, self.settings)
		dlg.ShowModal()
		dlg.Destroy()

		
	def doFileSelect(self, evt):
		self.enableButtons()
			
	def onClose(self, evt):
		self.settings.save()
		if self.modified:
			dlg = wx.MessageDialog(self,
				"You have unsaved changes.\nAre you sure you want to exit?",
				"Confirm Exit With Pending Changes",
				wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
			rc = dlg.ShowModal()
			dlg.Destroy()
			if rc == wx.ID_YES:
				self.Destroy()
		else:
			self.Destroy()
			
class App(wx.App):
	def OnInit(self):
		self.frame = PlaterFrame()
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True

app = App(False)
app.MainLoop()

