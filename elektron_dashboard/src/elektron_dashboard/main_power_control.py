# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of the Willow Garage nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import roslib
roslib.load_manifest('elektron_dashboard')

import wx

from os import path

def non_zero(value):
  if value < 0.00001 and value > -0.00001:
    return 0.00001
  return value


class MainPowerControl(wx.Window):
  def __init__(self, parent, id, icons_path):
    wx.Window.__init__(self, parent, id, wx.DefaultPosition, wx.Size(82, 32))

    self._voltage = 0.0

    self.Bind(wx.EVT_PAINT, self.on_paint)

  def on_paint(self, evt):
    dc = wx.BufferedPaintDC(self)

    dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
    dc.Clear()

    w = self.GetSize().GetWidth()
    h = self.GetSize().GetHeight()
    
    br_black = wx.Brush(wx.Colour(0, 0, 0, 255))
    br_white = wx.Brush(wx.Colour(255, 255, 255, 255))
    
    pen_black = wx.Pen(wx.Colour(0, 0, 0, 255))
    pen_white = wx.Pen(wx.Colour(255, 255, 255, 255))
    
    dc.SetBrush(br_black)
    
    dc.DrawRectangle(0, 0, w, h)
    
    cols = [wx.Colour(255, 0, 0), 
            wx.Colour(255, 128, 0), 
            wx.Colour(255, 255, 0), 
            wx.Colour(128, 255, 0), 
            wx.Colour(0, 255, 0), 
            wx.Colour(0, 255, 0), 
            wx.Colour(0, 255, 0) ]
    
    fnt = dc.GetFont()
    fnt.SetFamily(wx.FONTFAMILY_MODERN)
    fnt.SetFaceName("FreeMono")
    fnt.SetWeight(wx.FONTWEIGHT_BOLD)
    fnt.SetPointSize(7)
    dc.SetFont(fnt)
    
    # plugged in
    if (self._voltage > 26):
        dc.SetTextForeground(wx.Colour(255, 255, 255, 255))
        dc.DrawText(' Plugged in. ', 1, 1)
    else:
        dc.SetTextForeground(wx.Colour(255, 255, 255, 255))
        dc.DrawText('      %6.2fV' % self._voltage, 1, 1)
        dc.SetPen(pen_white)
        for i in range(7):
            dc.SetPen(wx.Pen(cols[i]))
            dc.DrawLine(11 + i * 10, h-3, 11 + i * 10, h-15)
            
        dc.SetPen(pen_white)
        dc.SetBrush(br_white)
        xx = 11 + (self._voltage-20) * 10
        yy = h-10
        dc.DrawPolygon([wx.Point(xx, yy), wx.Point(xx+3, yy-3), wx.Point(xx+3, yy-9), wx.Point(xx-3, yy-9), wx.Point(xx-3, yy-3)])


  def set_power_state(self, msg):
    self._voltage = float(msg['Voltage'])
    
    self.Refresh()

  def set_stale(self):
    self._voltage = 0.0

    self.Refresh()
