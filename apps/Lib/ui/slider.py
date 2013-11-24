import Widget
from browser import html

class Slider(Widget.Widget):
  def __init__(self, id=None, document=doc, label=False):
      self._div_shell=html.DIV(Class="ui-slider ui-slider-horizontal ui-widget ui-widget-content ui-corner-all")

      Widget.Widget.__init__(self, self._div_shell, 'slider', id)

      self._handle=html.A(Class="ui-slider-handle ui-state-default ui-corner-all",
                          Href='#', style={'left': '0px'})
      self._value=0
      self._isMouseDown=False

      def startSlide(e):
          self._isMouseDown=True
          self._upperBound = self._div_shell.offsetWidth - self._handle.offsetWidth

          pos = Widget.getMousePosition(e)
          self._startMouseX=pos['x']

          self._lastElementLeft = parseInt(self._handle.elt.style.left) #- parseInt(self._div_shell.elt.style.left)
          #print(self._upperBound)
          updatePosition(e)

      def updatePosition(e):
          pos = Widget.getMousePosition(e)
          _newPos = self._lastElementLeft + pos['x'] - self._startMouseX
          
          _newPos = max(0, _newPos)
          _newPos = min(_newPos, self._upperBound)

          #print(_newPos)
          self._handle.elt.style.left = '%spx' % _newPos
          self._lastElementLeft = _newPos

      def moving(e):
          if self._isMouseDown:
             updatePosition(e)

      def dropCallback(e):
          self._isMouseDown=False
          self._handle.unbind('mousemove', moving)


      self._handle.bind('mousemove', moving)
      self._handle.bind('mouseup', dropCallback)
      #self._handle.bind('mouseout', dropCallback)
      self._handle.bind('mousedown', startSlide)

      def mouseover(e):
          _class=self._handle.getAttribute('class')
          self._handle.setAttribute('class', '%s %s' % (_class, 'ui-state-hover'))

      def mouseout(e):
          self._isMouseDown=False
          _class=self._handle.getAttribute('class')
          self._handle.setAttribute('class', _class.replace('ui-state-hover', ''))

      self._handle.bind('mouseover', mouseover)
      self._handle.bind('mouseout', mouseout)

      self._div_shell <= self._handle

  def get_value(self):
      return self._value

  #def set_value(self, value):
  #    self._value=value
  #   self._handle.style.left='%spx' % value
