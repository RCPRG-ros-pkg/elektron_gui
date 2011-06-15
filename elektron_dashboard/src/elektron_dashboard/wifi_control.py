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


class WifiControl(wx.Window):
  def __init__(self, parent, id, icons_path):
    wx.Window.__init__(self, parent, id, wx.DefaultPosition, wx.Size(60, 50))

    self._base_bitmap = wx.Bitmap(path.join(icons_path, "wifi_bars.png"), wx.BITMAP_TYPE_PNG)
    self._bar_bitmap = wx.Bitmap(path.join(icons_path, "bar_on.png"), wx.BITMAP_TYPE_PNG)

    self._signal_power = 3
    self._max_signal_power = 5

    self.SetSize(wx.Size(self._base_bitmap.GetWidth(), 50))

    self.Bind(wx.EVT_PAINT, self.on_paint)

  def on_paint(self, evt):
    dc = wx.BufferedPaintDC(self)

    dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
    dc.Clear()

    w = self.GetSize().GetWidth()
    h = self._base_bitmap.GetHeight()

    dc.DrawBitmap(self._base_bitmap, 0, 0, True)

    bars = 5 * self._signal_power / self._max_signal_power
    
    for i in range(bars):
        dc.DrawBitmap(self._bar_bitmap, 36 + i * self._bar_bitmap.GetWidth(), 1, True)

    fnt = dc.GetFont()
    fnt.SetPointSize(7)
    dc.SetFont(fnt)
   # dc.DrawText("PWR Cons.", 0, 32)
   # dc.DrawText('%1.3f W' % self._power_consumption, 60, 32)


  def set_wifi_state(self, msg):
    self._signal_power = float(msg["Quality"])

    self.SetToolTip(wx.ToolTip("Quality: %.2f%%"%(self._signal_power)))
    self.Refresh()

  def set_stale(self):
    self._signal_power = 0
    self.SetToolTip(wx.ToolTip("WiFi: Stale"))

    self.Refresh()
