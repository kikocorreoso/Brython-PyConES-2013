class NodeCollectionSelector(Selector):
  def __init__(self, selector, collection):
      Selector.__init__(self, selector)
      self._collection=collection

      if self._selector_type == 'id':
         self._match=self._match_id
      elif self._selector_type =='tag':
         self._match=self._match_tag
      elif self._selector_type == 'classname':
         self._match=self._match_classname

  def _match_id(self, node):
      if node.id is None: return False
      return node.id == self._selector

  def _match_tag(self, node):
      return node.tagName == self._selector

  def _match_classname(self, node):
      return self._selector in node.classname

  def get(self):
      _c1=NodeCollection()
      for _node in self._collection:
          if self._match(_node):
             _c1.append(_node)

      return _c1

class Selector:
  tags=['A','ABBR','ACRONYM','ADDRESS','APPLET','B','BDO','BIG','BLOCKQUOTE',
        'BUTTON','CAPTION','CENTER','CITE','CODE','DEL','DFN','DIR','DIV','DL',
        'EM','FIELDSET','FONT','FORM','FRAMESET','H1','H2','H3','H4','H5','H6',
        'I','IFRAME','INS','KBD','LABEL','LEGEND','MAP','MENU','NOFRAMES', 
        'NOSCRIPT','OBJECT','OL','OPTGROUP','PRE','Q','S','SAMP','SCRIPT', 
        'SELECT','SMALL','SPAN','STRIKE','STRONG','STYLE','SUB','SUP','TABLE',
        'TEXTAREA','TITLE','TT','U','UL','VAR','BODY','COLGROUP','DD','DT',
        'HEAD','HTML','LI','P','TBODY','OPTION','TD','TFOOT','TH','THEAD','TR',
        'AREA','BASE','BASEFONT','BR','COL','FRAME','HR','IMG','INPUT',
        'ISINDEX','LINK','META','PARAM',  #HTML 5 elements...
        'ARTICLE','ASIDE','AUDIO','BDI','CANVAS','COMMAND','DATALIST',
        'DETAILS','DIALOG','EMBED','FIGCAPTION','FIGURE','FOOTER','HEADER',
        'KEYGEN','MARK','METER','NAV','OUTPUT','PROGRESS','RP','RT',
        'RUBY','SECTION','SOURCE','SUMMARY','TIME','TRACK','VIDEO','WBR']

  def __init__(self, selector, start_node=doc):
      self._doc=start_node

      if (isinstance(selector, str)):
         if selector.startswith("."):   #class selector
            self._selector=selector[1:]
            self._selector_type="classname"
         elif selector.startswith("#"):  #id selector
            self._selector=selector[1:]
            self._selector_type="id"
         elif selector.upper() in tags:
            self._selector=selector.upper()
            self._selector_type="tag"
         else:  
            self._selector=selector
            self._selector_type="selector"
      else:  #this is a function
         self._selector_type="selector"
         self._function=selector
         self.get=self._function_get

  def _function_get(self):
      def recurse(node):
          _list=[]
          if self._function(node):
             _list.append(node)

          for _node in node.childNodes:
              _list+=recurse(_node)

          return _list

      _matched_nodes=recurse(self._doc)
      return NodeCollection(_matched_nodes)

  def get(self):
      if self._selector_type=="id":
         _matched_nodes=self._doc.get(id=self._selector)
      elif self._selector_type=="classname":
         _matched_nodes=self._doc.get(classname=self._selector)
      elif self._selector_type == "tag":
         _matched_nodes=self._doc.get(tag=self._selector)
      elif self._selector_type=="selector":
         _matched_nodes=self._doc.get(selector=self._selector)
      else:
         _matched_nodes=[]
      return NodeCollection(_matched_nodes)

class NodeCollection:
  def __init__(self, nodes=[]):
      self._nodes=nodes

  def __len__(self):
      return len(self._nodes)

  def __item__(self, i):
      return self._nodes[i]

  def __getitem__(self, i):
      return self._nodes[i]

  def __add__(self, nodes):
      self._nodes+=nodes

  def __str__(self):
      _str=[]
      for _node in self._nodes:
          _str.append(_node.__str__())

      return '<br>'.join(_str)

  def append(self, node):        
      self._nodes.append(node)

  def next(self):
      for _node in self._nodes:
          yield _node

  def add(self, selector, context):
      _ns=NodeCollectionSelector(selector, self)
      self._nodes+=_ns.get()

  def addBack(self):
      pass

  def addClass(self, classname):
      for _node in self._nodes:
          _node.addClass(classname)

  def after(self, content):
      for _node in self._nodes:
          _node.after(content)

  def append_content(self, content):
      for _node in self._nodes:
          _node.append(content)

  def appendTo(self, selector):
      _s=Selector(selector)

      for _node in _s.get():
          _node.append(self._node[0].clone())

  def attr(self, property, value=None):
      if value is None:
         return self._nodes[0][property]

      for _node in self._nodes:
          _node[property]=value

  def before(self, content):
      for _node in self._nodes:
          _node.before(content)

  def bind(self, event, handler):
      if ' ' in event:
         _events=' '.split(event)
         for _event in _events:
             for _node in self._nodes:
                 _node['on%s' % event]=handler
         return

      for _node in self._nodes:
          _node['on%s' % event]=handler

  def blur(self, handler=None):
      pass

  def change(self, handler=None):
      pass

  def children(self, selector=None):
      _c=NodeCollection()
      for _node in self._nodes:
          for _child in _node.get_children():
              _c.append(_child)

      if selector is None:
         return _c

      #selector is not None
      _ns=NodeCollectionSelector(selector, _c)
      return _ns.get()

  def click(self, handler=None):
      pass

  def clone(self):
      return NodeCollection([_node.clone() for _node in self._nodes])

  def closest(self, selector):
      if isinstance(selector, str):
         _ns=Selector(selector)
         selector=_ns.get()

      _c=NodeCollection()
      for _node in self._nodes:
          _c.append(_node.closest(selector))

      return _c

  def contains(self, text):
      pass

  def contents(self):
      pass

  def css(self, property, value=None):
      if value is None and not isinstance(property, dict):
         return self._nodes[0].css(property)

      if isinstance(property, dict):
         for _node in self._nodes:
             _node.css(property)
      else:
         for _node in self._nodes:
             _node.css(property, value)

  def data(self):
      pass

  def dblclick(self, handler=None):
      pass

  def detach(self):
      pass

  def each(self, func):
      for _node in self._nodes:
          func(_node)

  def empty(self):
      for _node in self._nodes:
          _node.empty()

  def eq(self, index):
      if index < len(self._nodes):
         return NodeCollections(self._nodes[index])

      return NodeCollections()

  def error(self, handler=None):
      pass

  def fadeIn(self):
      pass

  def fadeOut(self):
      pass

  def fadeTo(self):
      pass

  def fadeToggle(self):
      pass

  def filter(self, selector):
      _ns=NodeCollectionSelector(selector, self)
      return _ns.get()

  def find(self):
      pass

  def first(self):
      if len(self._nodes) == 0:
         return NodeCollection()

      return NodeCollection([self._nodes[0]])

  def focus(self, handler=None):
      pass

  def focusin(self, handler=None):
      pass

  def focusout(self, handler=None):
      pass

  def get(self, index=None):
      if index is None:
         return [_node for _node in self._nodes]

      return self._nodes[index]

  def gt(self, index):
      return NodeCollection([self._nodes[index:]])

  def has(self, selector):
      pass
  
  def hasClass(self, name):
      for _node in self._nodes:
          if _node.hasClass(name):
             return True

      return False

  def height(self, value=None):
      if value is None:
         return self._nodes[0].css('height')

      for _node in self._nodes:
          _node.set_style({'height': value})

  def hide(self):
      for _node in self._nodes:
          _node.set_style({'display': 'none'})

  def hover(self, handler=None):
      pass

  def html(self, content=None):
      if content is None:
         return self._nodes[0].get_html()

      for _node in self._nodes:
          _node.set_html(content)

  def innerHeight(self):
      pass

  def innerWidth(self):
      pass

  def insertAfter(self, target):
      pass

  def insertBefore(self, target):
      pass

  #def is(self, selector):
  #    pass

  def keydown(self, handler=None):
      pass

  def keypress(self, handler=None):
      pass

  def keyup(self, handler=None):
      pass

  def last(self):
      return self._nodes[-1]

  @property
  def length(self):
      return len(self._nodes)

  def mousedown(self, handler=None):
      pass

  def mouseenter(self, handler=None):
      pass

  def mouseleave(self, handler=None):
      pass

  def mousemove(self, handler=None):
      pass

  def mouseout(self, handler=None):
      pass

  def mouseover(self, handler=None):
      pass

  def mouseup(self, handler=None):
      pass

  def next(self):
      pass

  def nextAll(self):
      pass

  def nextUtil(self):
      pass

  def off(self, handler):
      pass

  def offset(self):
      pass

  def offsetParent(self):
      pass

  def on(self, handler):
      pass

  def outerHeight(self):
      pass

  def outerWidth(self):
      pass

  def parent(self):
      _p=NodeCollection()
      for _node in self._nodes:
          _p.append(_node.get_parent())

  def parents(self, selector=None):
      pass

  def parentsUntil(self, selector=None):
      pass

  def position(self):
      pass

  def prepend(self, content):
      for _node in self._nodes:
          _node.prepend(content)

  def prependTo(self, target):
      pass

  def prev(self):
      _p1=NodeCollection()
      for _node in self._nodes:
          _parent=_node.get_parent()
          for _i in range(len(_parent.childNodes)):
              if _parent.childNodes[_i] == _node:
                 if _i > 0:
                    _p1.append(_parent.childNodes[_i-1])
                 break

      return _p1

  def prevAll(self, selector=None):
      pass

  def prevUntil(self, selector=None):
      pass

  def prop(self, property, value=None):
      pass

  def ready(self, func):
      pass

  def remove(self):
      for _node in self._nodes:
          _node.get_parent().removeChild(_node) 

  def removeAttr(self, attr):
      pass

  def removeClass(self, name):
      for _node in self._nodes:
          _node.removeClass(name)

  def removeProp(self, property):
      pass

  def replaceAll(self):
      pass

  def replaceWith(self, content):
      for _node in self._nodes:
          _node.get_parent().replaceWith(content, _node)

  def resize(self, handler=None):
      pass

  def scroll(self, handler=None):
      pass

  def scrollLeft(self, value=None):
      pass

  def scrollTop(self, value=None):
      pass

  def select(self, handler=None):
      pass

  def show(self):
      for _node in self._nodes:
          _node.set_style({'display': 'block'})

  def siblings(self, selector=None):
      pass

  def size(self):
      pass

  def slice(self, index1=None, index2=None):
      if index1 is None and index2 is None:
         return NodeCollection()

      return NodeCollection(self._nodes[index1:index2])

  def slideDown(self):
      pass

  def slideToggle(self):
      pass

  def slideUp(self):
      pass

  def submit(self, handler=None):
      pass

  def text(self, content=None):
      if content is None:
         return self._nodes[0].get_text()

      for _node in self._nodes:
          _node.set_text(content) 

  def toggle(self, Function=None):
      if Function is None:
         _show=True
         if self._nodes[0].css('display') != 'none':
            _show=False
         for _node in self._nodes:
             if _show:
                _node.set_style({'display': 'block'})
             else:
                _node.set_style({'display': 'none'})
  
             _show=not _show

         return

      for _node in self._nodes:
          if Function(_node):
             _node.set_style({'display': 'block'})
          else:
             _node.set_style({'display': 'none'})

  def toggleClass(self):
      pass

  def toList(self):
      return self._nodes

  toArray=toList   #for jQuery compatibility

  def touchend(self, handler=None):
      pass

  def touchmove(self, handler=None):
      pass

  def touchstart(self, handler=None):
      pass

  def trigger(self, event_type):
      pass

  def triggerHandler(self, event_type):
      pass


  def unbind(self, event, handler):
      if ' ' in event:
         _events=' '.split(event)
         for _event in _events:
             for _node in self._nodes:
                 print("fix me!")
         return

      for _node in self._nodes:
          #look into how to detach an event
          print("fix me")


  def unload(self, handler):
      pass

  def unwrap(self):
      for _node in self._nodes:
          _parent=_node.get_parent()
          _grandparent=_parent.get_parent()
          _grandparent.replaceChild(_node, _parent)

          _parent.remove()

  def val(self, value=None):
      if value is None:
         return self._nodes[0]['text']   #is text the best here?

      for _node in self._nodes:
          _node['text']=value

  def width(self, width=None):
      if width is None:
         return self._nodes[0].css('width')

      for _node in self._nodes:
          _node.set_style({'width': width})

  def wrap(self):
      pass

  def wrapAll(self):
      pass

  def wrapInner(self):
      pass

def byId(id):
    _result=doc.get(id=id)
    return _result[0]

def createCSSClass(csstext):
    _style=doc.createElement('style')
    _style.type='text/css'
    _style.innerHTML = csstext
    doc.get(tag='head')[0].appendChild(_style)
