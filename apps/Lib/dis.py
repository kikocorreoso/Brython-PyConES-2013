def dis(src):
    return JSObject(__BRYTHON__.py2js(src)).to_js()
