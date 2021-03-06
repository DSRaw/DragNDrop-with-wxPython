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
        #self.drag_temp = Drag_Frame(self.p_panel, pos = self.parent.ClientToScreen(self.btn_start_pos)) #btn pos is in terms of panel, but DragFrame is in terms of screen. Conversion necessary
        
        event.Skip()
        
    def on_drag(self, event):
        if(event.Dragging() and event.LeftIsDown()):
            m_pos = self.parent.ScreenToClient(wx.GetMousePosition())   #This is repeated because we now need to get the mouse's changing position as long as the button is in a dragging state
            new_pos = m_pos - self.delta    #We subtract delta to ensure the button origin stays the same distance relative to the mouse's changing position as it was when 1st clicked.
            btn_scrn_pos = self.parent.ClientToScreen(self.btn_start_pos)
            #self.Move(new_pos)  #If we just set new_pos to where the mouse's current position is, the button origin would jump to the cursor's point. Such movement is jittery & unnatural.
            self.drag_temp = Drag_Frame(self.p_panel, btn_scrn_pos, self.delta) #btn pos is in terms of panel, but DragFrame is in terms of screen. Conversion necessary
        
            '''Try shoving Drag_Frame inside of this class by bringing all our varaibles and attributes together'''
        event.Skip()
        
    #Once finished dragging, either snap the button back to it's original position from this click event cycle, or check if it was dragged to a matching drop button:
    def on_release(self, event):
        self.SetPosition(self.btn_start_pos)
        
        event.Skip()

class Drag_Frame(wx.Frame):
    def __init__(self, parent, pos, delta):
        super().__init__(parent, title='borderless', pos=pos, style=wx.BORDER_NONE | wx.FRAME_FLOAT_ON_PARENT)
        self.btn = wx.Button(self, label="dragging")
        
        self.og_pos = pos
        self.delta = delta
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.btn, 1, wx.ALL | wx.EXPAND)
        self.SetSizerAndFit(self.sizer)
        
        self.btn.Bind(wx.EVT_MOTION, self.on_drag)
        self.btn.Bind(wx.EVT_LEFT_UP, self.on_release)
        
        self.Show()
        
    def on_drag(self, event):
        print("entered ondrag")
        if(event.Dragging() and event.LeftIsDown()):
            print("entered if")
            m_pos = wx.GetMousePosition()
            new_pos = m_pos - self.delta
            self.Move(new_pos)
        event.Skip()
        
    def on_release(self, event):
        self.Destroy()
        
        event.Skip()
    
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
        
        #self.dd_frame = Drag_Frame(self)
        
    def get_top_panel(self):
        return self.top_panel

if __name__ == '__main__':
    DD_app = wx.App()
    DD_window = Top_Frame()
    donkeybtn = DD_Donkey(DD_window, "foobar")
    tailbtn = DD_Tail(DD_window, "fizzbuzz")
    DD_window.Show()
    DD_app.MainLoop()