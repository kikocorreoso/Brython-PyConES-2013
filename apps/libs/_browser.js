$module = {
    __getattr__ : function(attr){return this[attr]},
    alert: function(message){window.alert(message)},
    confirm: function(message){return JSObject(window.confirm(message))},
    doc: $DOMNode(document),   //want to use document instead of doc
    mouseCoords: function(ev){return JSObject($mouseCoords(ev))},
    prompt: function(message, default_value){return JSObject(window.prompt(message, default_value))},
    win: JSObject(window)     //want to use window instead of win
}
$module.__class__ = $module // defined in $py_utils
$module.__str__ = function(){return "<module 'browser'>"}
