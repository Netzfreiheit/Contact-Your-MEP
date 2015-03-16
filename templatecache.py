from jinja2 import Template

class TemplateCache():
    def __init__(self):
        self.cache = {}

    def get(self,fn):
        return self.cache.get(fn,self.load(fn))

    def load(self,fn):
        with open(fn) as f:
            self.cache[fn] = Template(f.read().decode("utf-8"))
        return self.cache[fn]
        
