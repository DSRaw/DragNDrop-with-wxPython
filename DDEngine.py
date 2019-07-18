'''
Created on Jul 16, 2019

@author: Daphne
'''
import wx

class DD_Donkey(wx.Button):
    def __init__(self, parent, text):
        super().__init__(parent.get_top_panel(), label=text)
        self.parent = parent
        self.p_panel = parent.get_top_panel()
        self.text = text
        
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_mouseover)
        parent.drop_sizer.Add(self)
        
    def on_mouseover(self, event):
        print("Roger that")
        event.Skip()

class DD_Tail(wx.Button):
    def __init__(self, parent, text):
        super().__init__(parent.get_top_panel(), label=text)
        self.parent = parent
        self.p_panel = parent.get_top_panel()
        self.text = text
        
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_MOTION, self.on_drag)
        self.Bind(wx.EVT_LEFT_UP, self.on_release)
        
        parent.drag_sizer.Add(self)
    
    #We want our cursor to stay the same distance from the button's origin as it is when first clicked. First we get our absolute mouse position on the screen, then put it in terms of the parent.
    #We subtract to get the difference in position between mouse and button origin. Delta should stay the same for as long as this click is held down, to ensure smooth and intuitive movement.
    #These variables use self because they must be used in later functions, but aren't initialized until, and must be reassigned on every new L-click event.
    def on_click(self, event):
        self.btn_start_pos = event.GetEventObject().GetPosition()
        self.delta = self.parent.ScreenToClient(wx.GetMousePosition()) - self.btn_start_pos 
        event.Skip()
        
    def on_drag(self, event):
        if(event.Dragging() and event.LeftIsDown()):
            m_pos = self.parent.ScreenToClient(wx.GetMousePosition())   #This is repeated because we now need to get the mouse's changing position as long as the button is in a dragging state
            new_pos = m_pos - self.delta    #We subtract delta to ensure the button origin stays the same distance relative to the mouse's changing position as it was when 1st clicked.
            self.Move(new_pos)  #If we just set new_pos to where the mouse's current position is, the button origin would jump to the cursor's point. Such movement is jittery & unnatural.

        event.Skip()
        
    #Once finished dragging, either snap the button back to it's original position from this click event cycle, or check if it was dragged to a matching drop button:
    def on_release(self, event):
        self.SetPosition(self.btn_start_pos)
        
        event.Skip()

class DD_Frame(wx.Frame):
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

if __name__ == '__main__':
    DD_app = wx.App()
    DD_window = DD_Frame()
    donkeybtn = DD_Donkey(DD_window, "foobar")
    tailbtn = DD_Tail(DD_window, "fizzbuzz")
    DD_window.Show()
    DD_app.MainLoop()