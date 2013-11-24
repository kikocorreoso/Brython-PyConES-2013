import random

class BaseUI:
  def __init__(self, element, type, id=None, draggable=False):
      self._element=element

      if id is None:
         self._element.setAttribute('id','%s_%s' % (type, int(100000*random.random())))
      else:
         self._element.setAttribute('id',id)

      if draggable:
         self.draggable()

      self.attach=self.append

  def get_id(self):
      return self._element.id

  def append(self, element_id):
      """ append this DOM component to DOM element element_id"""
      doc.get(id=element_id)[0].appendChild(self._element)

  def draggable(self):
      def drag(e):
          self._element.style.top='%spx' % (e.clientY - self._deltaY)
          self._element.style.left='%spx' % (e.clientX - self._deltaX)

      def mouseDown(e):
          self._element.style.position='absolute'
          self._deltaX=e.clientX - self._element.offsetLeft
          self._deltaY=e.clientY - self._element.offsetTop
          win.addEventListener('mousemove', drag, true)

      def mouseUp(e):
          win.removeEventListener('mousemove', drag, true)

      self._element.addEventListener('mousedown', mouseDown, False)
      self._element.addEventListener('mouseup', mouseUp, False)

  def show(self):
      self._element.setAttribute('display', 'block')

  def hide(self):
      self._element.setAttribute('display', 'none')
