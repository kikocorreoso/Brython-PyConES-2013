class CookieError(Exception):
    pass
    
class BaseCookie:

    def __init__(self,data=None):
        self.morsels = {}
        if data is not None:
            self.load(data)
    
    def load(self,data):
        elts = data.split(';')
        for elt in elts:
            elt = elt.strip().split('=',1)
            if len(elt)!=2:
                raise ValueError('invalid cookie %s' %data)
            morsel,value = elt
            if morsel in self.morsels:
                self.morsels[morsel].append(value)
            else:
                self.morsels[morsel] = [value]
    
