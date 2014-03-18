import lxml.html
import json
import urllib2
from cookielib import CookieJar

cj=CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

base="http://www.europarl.europa.eu"
list="http://www.europarl.europa.eu/meps/en/full-list.html?filter=all&leg="

pages=[list]

def root_from_url(u):
  u=opener.open(u)
  return lxml.html.fromstring(u.read())

def extract_urls_from_page(u):  
  r=root_from_url(u)

  urls=["%s%s"%(base,i) for i in r.xpath('//li[@class="mep_name"]/a/@href')]
  return [{'url': x} for x in urls]

def expand_mep_info(m):
  print m['url']
  r=root_from_url(m['url'].replace(" ","%20"))
  m['image']="%s%s"%(base,r.xpath('//img[@class="photo_mep"]/@src')[0])
  m['name']=" ".join(r.xpath('//li[@class="mep_name"]')[0].itertext())
  info=r.xpath('//div[@class="zone_info_mep_transparent_mep_details"]')[0]
  m['group']=info.xpath('./ul/li[2]')[0].text.strip()
  m['group_short']=info.xpath('./ul/li[2]/@class')[0].split(" ",1)[1]
  m['party']=info.xpath('.//span[@class="name_pol_group"]')[0].text
  m['country']=info.xpath('./ul/li[3]')[0].text.strip()
  m['country_short']=info.xpath('./ul/li[3]/@class')[0].split(" ",1)[1]
  try:
    m['email']="".join(reversed(r.xpath('//a[@id="email-0"]/@href')[0].replace("mailto:","").replace("[dot]",".").replace("[at]","@")))
  except IndexError:
    m['email']=None
  return m

def do():
  meps=reduce(lambda x,y: x+y, [extract_urls_from_page(i) for i in pages],
  [])
  meps=[expand_mep_info(m) for m in meps]
  with open("data.json","wb") as f:
    json.dump(meps,f)

if __name__=='__main__':
    do()
