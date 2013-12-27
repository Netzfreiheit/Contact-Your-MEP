import web
import json
from jinja2 import Template
import random

urls= (
  '/(.*)' , 'main' )

with open("widget.tmpl") as f:
  template = Template(f.read().decode("utf-8"))

app= web.application(urls,globals())
with open("data.json") as f:
  meps=json.load(f)

class main:
  def GET(self,foo):
    web.header("Content-Type", "text/html;charset=utf-8")
    with open("widget.tmpl") as f:
      template = Template(f.read().decode("utf-8"))
    m=random.choice(meps)
    return template.render(m)

if __name__=="__main__":
  app.run()
