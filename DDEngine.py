'''
Created on Jul 16, 2019

@author: Daphne
'''
import wx
import MatchPair

class Top_Frame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Sup')
        self.top_panel = wx.Panel(self)
        
        self.top_sizer = wx.BoxSizer(wx.VERTICAL)
        self.drop_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self.top_panel, label = "Drop Here")
        self.drag_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self.top_panel, label = "Drag This")
        
        self.top_sizer.Add(self.drop_sizer, 1, wx.ALL | wx.EXPAND)
        self.top_sizer.Add(self.drag_sizer, 1, wx.ALL | wx.EXPAND)
        self.top_panel.SetSizer(self.top_sizer)
        
    def get_top_panel(self):
        return self.top_panel
    
    def populate_frame(self):
        print("")
        self.match_obj1 = MatchPair.Match_Pair(self)
        self.match_obj2 = MatchPair.Match_Pair(self)

if __name__ == '__main__':
    DD_app = wx.App()
    DD_window = Top_Frame()
    DD_window.populate_frame()
    
    DD_window.Show()
    DD_app.MainLoop()