'''
Created on Jul 19, 2019

@author: Daphne
'''

import wx

class Match_Pair():
    '''
    @Description: This class facilitates both a "drag cycle", and a method for checking for matches between dragged objects. A drag cycle via this class begins with the creation of a Donkey and a Tail button as a pair. ***FINISH WRITING***
    @NOTABLE ATTRIBUTES:
    @parent: Receives top-level frame when this object is created 
    @self.Donkey: The button that REPRESENTS a target to which an object should be dragged
    @self.Tail: The button that REPRESENTS the information that is to be dragged to Donkey
    @self.drag_frame: Created within on_drag_start(). This is the ACTUAL object (wx.Frame with a child wx.Button) that will be draggable around the screen
    '''
    def __init__(self, parent):
        self.parent = parent
        self.p_panel = parent.get_top_panel()
        
        self.IsDragging = False
        self.OnTarget = False
        self.IsMatch = False

        #Creation of widgets involved in visual representation of dragging process:
        self.Donkey = wx.Button(self.p_panel, label="Foobar")
        self.Tail = wx.Button(self.p_panel, label="Fizzbuzz")
        
        #Event Bindings:
        self.Tail.Bind(wx.EVT_MOTION, self.on_drag_start)
        
        #Insertion into parent frame's geometry:
        self.parent.drop_sizer.Add(self.Donkey)
        self.parent.drag_sizer.Add(self.Tail)
    
    def _check_match(self):
        if(self.IsDragging == True and self.OnTarget == True):
            print(str(self.IsDragging) + " " + str(self.OnTarget))
            self.IsMatch = True
        self.OnTarget = False     #OnTarget must be set back to False here. 
        self.IsDragging = False     #IsDragging must be set to false at end of on_release and on_leave events, but is also set False here just to be sure. This func is only called from on_release
        print(str(self.IsDragging) + " " + str(self.OnTarget))
            
    def _check_OnTarget(self):  #Will check if the mouse is within the Donkey button's area on_release of the dragging event
        #Sets and Returns bool value of OnTarget based on whether or not the mouse is within the area of the Donkey btn on_release() of Tail's drag cycle
        #Does this by calculating the difference in distance (delta) between the mouse on release of dragging event and the origin point og Donkey btn
        #If statements delta is less than the width and height of Donkey btn. If yes, mouse is OnTarget (return True), otherwise mouse is not OnTarget (return False)
        Donkey_size = self.Donkey.GetSize()
        Donkey_pos = self.Donkey.GetPosition()
        m_pos = self.parent.ScreenToClient(wx.GetMousePosition())
        Donkey_delta = m_pos - Donkey_pos
        
        if(Donkey_delta.x >= 0 and Donkey_delta.x <= Donkey_size.width):
            if(Donkey_delta.y >= 0 and Donkey_delta.y <= Donkey_size.height):
                self.OnTarget = True
        else:
            self.OnTarget = False
            
        return (self.OnTarget)
    
    #Events for Tail and drag_frame:    
    def on_drag_start(self, event):
        if(event.Dragging() and event.LeftIsDown()):
            #Gets the origin of the Tail button in the parents geometry, and calculates the difference between Tails' starting position and where the mouse was first clicked, allowing the mouse position to stay constant relative to the button origin throughout the drag.
            #The calculations in the Calculation block can only be done here because the Tail button (the calling object) immediately loses focus and exits it's event cycle once drag_frame is created and shown over top of it. At that point, the events bound to drag_frame from within this function take over.
            #If significantly changing the placement of drag_frame's creation, consider moving these calculations from here to a separate left-click event bound to Tail.'''
            
            # Begin Calculation block #
            self.btn_start_pos = event.GetEventObject().GetPosition()
            self.btn_scrn_pos = self.parent.ClientToScreen(self.btn_start_pos)
            self.delta = self.parent.ScreenToClient(wx.GetMousePosition()) - self.btn_start_pos
            # End Calculation block #
            
            #Creation of frame and its child button used to visually represent the drag operation
            self.drag_frame = wx.Frame(self.p_panel, pos=self.btn_scrn_pos, style=wx.BORDER_NONE | wx.FRAME_FLOAT_ON_PARENT | wx.FRAME_NO_TASKBAR)
            self.drag_btn = wx.Button(self.drag_frame, label="Fizzbuzzing")
            
            #Add button to drag_frame's geometry. SetSizerAndFit will ensure the frame is only large enough to hold the button
            self.sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer.Add(self.drag_btn, 1, wx.ALL | wx.EXPAND)
            self.drag_frame.SetSizerAndFit(self.sizer)
            
            #Once the frame is shown, the dragging operation is now handles by the following events.
            #EVT_LEAVE_WINDOW will help prevent cases where Destroy() is not called because the frame's focus get's unexpectedly pulled away by the client's OS before the mouse button is actually released.
            self.drag_btn.Bind(wx.EVT_MOTION, self.on_dragging)
            self.drag_btn.Bind(wx.EVT_LEFT_UP, self.on_release)     #Separate LEFT_UP and LEAVE_WINDOW events are needed otherwise check_on_Donkey will be called unnecessarily
            #self.drag_btn.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
            #self.drag_btn.Bind(wx.EVT_KILL_FOCUS, self.on_release)    #Likely unnecessary
            
            self.drag_frame.Show()
            self.Tail.Hide()
            
            #Since on_dragging event should immediately begin as long as button remains depressed, IsDragging will remain true until on_release.
            #Putting this here prevents the IsDragging state from being updated a million times with the same state upon each new mouse position in on_dragging
            self.IsDragging = True
            #print(self.IsDragging)

        event.Skip()
        
    def on_dragging(self, event):
        '''Moves drag_frame along with the mouse's movement. Subtracts delta from the current mouse position, in order to keep the cursor constant relative to the drag_frame.'''
        if(event.Dragging() and event.LeftIsDown()):
            m_pos = wx.GetMousePosition()
            new_pos = m_pos - self.delta
            self.drag_frame.Move(new_pos)
        event.Skip()
        
    def on_release(self, event):
        '''Once dragging is finished, or the drag_frame has lost focus, either check if Tail was dragged to it's matching Donkey, or destroy the drag_frame and re-Show() the Tail button to allow another drag cycle. '''
        if(self._check_OnTarget()):  #if Tail is within area of Donkey when drag is released
            self._check_match()      #check is this Tail matches this Donkey
        
        self.IsDragging = False
        if (self.drag_frame): #if drag_frame still exists in any form
            self.drag_frame.Destroy()
            print("release")
        self.Tail.Show()
        
        event.Skip()
        
    def on_leave(self, event):
        self.IsDragging = False
        if (self.drag_frame): #if drag_frame still exists in any form
            self.drag_frame.Destroy()
            print("left")
        self.Tail.Show()
        
        event.Skip()
        
        
        
        
        
        