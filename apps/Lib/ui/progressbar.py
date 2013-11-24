import Widget
from browser import html

class ProgressBar(Widget.Widget):
  def __init__(self, id=None, label=False):
      self._div_shell=html.DIV(Class="ui-progressbar ui-widget ui-widget-content ui-corner-all")
      Widget.Widget.__init__(self, self._div_shell, 'progressbar', id)

      self._show_label=label
      if label:
         self._label=html.DIV(Class='progress-label')
         self._div_shell <= self._label

      self._bar=html.DIV(Class="ui-progressbar-value ui-widget-header ui-corner-left",
                         style={'width': '0px'})
      self._div_shell <= self._bar

  def set_progress(self, percent):
      self._bar.style.width='%s%%' % percent
      if self._show_label:
         self._label.text='%s%%' % percent
