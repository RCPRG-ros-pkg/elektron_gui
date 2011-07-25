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


class MemFrame(wx.Window):
  def __init__(self, parent, id):
    wx.Window.__init__(self, parent, id, wx.DefaultPosition, wx.Size(82, 32))

    self._total = 1.0
    self._used = 0.0
    self._shared = 0.0
    self._cached = 0.0
    self._buffers = 0.0
    
    self._buf_size = 40
    
    #self._buffer = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self._buffer = [0.0] * self._buf_size
    self._cnt = 0

    self.Bind(wx.EVT_PAINT, self.on_paint)

  def on_paint(self, evt):
    dc = wx.BufferedPaintDC(self)

    dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
    dc.Clear()

    w = self.GetSize().GetWidth()

    br_black = wx.Brush(wx.Colour(0, 0, 0, 255))
    br_white = wx.Brush(wx.Colour(255, 255, 255, 255))
    
    pen_black = wx.Pen(wx.Colour(0, 0, 0, 255))
    pen_white = wx.Pen(wx.Colour(255, 255, 255, 255))
    
    dc.SetBrush(br_black)
    
    dc.DrawRectangle(0, 0, w, 32)
    
    dc.SetBrush(br_white)
    dc.SetPen(pen_white)

    w_step = (w - 2) / self._buf_size
    for i in range(self._buf_size):
        id = (self._cnt + i) % self._buf_size
        us = int(self._buffer[id])
        r = 0
        g = 0
        if (us <= 50):
            g = 255
            r = int(us*5.1)
        else:
            r = 255
            g = 255 - int((us-50)*5.1)
        dc.SetPen(wx.Pen(wx.Colour(r, g, 0, 255)))
        dc.SetBrush(wx.Brush(wx.Colour(r, g, 0, 255)))
        dc.DrawRectangle(1 + i*w_step, 31, w_step, -us * 0.3)

    fnt = dc.GetFont()
    fnt.SetFamily(wx.FONTFAMILY_MODERN)
    fnt.SetFaceName("FreeMono")
    fnt.SetWeight(wx.FONTWEIGHT_BOLD)
    fnt.SetPointSize(7)
    
    dc.SetFont(fnt)
    dc.SetTextForeground(wx.Colour(0, 0, 0, 255))
    dc.DrawText('%3.0f%%   %4.0fMB' % (100 * self._used / self._total, self._total), 2, 2)
    dc.SetTextForeground(wx.Colour(255, 255, 255, 255))
    dc.DrawText('%3.0f%%   %4.0fMB' % (100 * self._used / self._total, self._total), 1, 1)


  def set_state(self, msg):
    self._total = float(msg['total'])
    self._used = float(msg['used'])
    
    self._buffer[self._cnt] = 100 * self._used / self._total
    self._cnt = (self._cnt + 1) % self._buf_size
    
    self.Refresh()

  def set_stale(self):
    self._cur_freq = 0.0
    self._max_freq = 0.0
    self._usage = 0.0
    self.Refresh()
