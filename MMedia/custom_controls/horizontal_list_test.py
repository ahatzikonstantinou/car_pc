import wx
import wx.lib.scrolledpanel as scrolled

class TestPanel(scrolled.ScrolledPanel):
	def __init__(self, parent):
		scrolled.ScrolledPanel.__init__(self, parent, -1)
		#vbox = wx.BoxSizer(wx.VERTICAL)
		#desc = wx.StaticText(self, -1,
			#"ScrolledPanel extends wx.ScrolledWindow, adding all "
			#"the necessary bits to set up scroll handling for you.\n\n"
			#"Here are three fixed size examples of its use. The "
			#"demo panel for this sample is also using it -- the \nwxStaticLine "
			#"below is intentionally made too long so a scrollbar will be "
			#"activated."
			#)
		#desc.SetForegroundColour("Blue")
		#vbox.Add(desc, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		#self.SetSizer(vbox)
		
		hbox = wx.BoxSizer( wx.HORIZONTAL )
		for i in range( 0, 10 ):
			b = wx.Button( self, label='Button'+str( i ) )
			hbox.Add( b )
		self.SetSizer( hbox )
		self.SetAutoLayout(1)
		self.SetupScrolling()
		
app = wx.App(0)
frame = wx.Frame(None, wx.ID_ANY)
fa = TestPanel(frame)
frame.Show()
app.MainLoop()
