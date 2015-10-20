import lxml.html
import json
import urllib2
from cookielib import CookieJar
import re
import os
import sys

cj=CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

base="http://www.europarl.europa.eu"
list="http://www.europarl.europa.eu/meps/en/full-list.html?filter=all&leg="
country_codes={'Malta':'mt','UnitedKingdom':'gb','Germany':'de','Italy':'it','France':'fr','Portugal':'pt','Sweden':'se','Spain':'es','Lithuania':'lt','Greece':'gr','Romania':'ro','Denmark':'dk','Ireland':'ie','Netherlands':'nl','Luxembourg':'lu','Hungary':'hu','Croatia':'hr','Slovakia':'sk','Austria':'at','Belgium':'be','Poland':'pl','Bulgaria':'bg','CzechRepublic':'cz','Finland':'fi','Slovenia':'si','Latvia':'lv','Cyprus':'cy','Estonia':'ee'}

pages=[list]

" Load Data "
if sys.argv[1]:
  with open(sys.argv[1]) as f:
    boiler = json.load(f)

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
  m['id']=re.match(r'.*\/meps\/en\/(\d+)\/', m['url']).group(1)
  m['image']="%s%s"%(base,r.xpath('//img[@class="photo_mep"]/@src')[0])
  if not os.path.isfile("images/%s.jpg"%m['id']):
    try:
        u = urllib2.urlopen(m['image'])
        with open("images/%s.jpg"%m['id'],"wb") as f:
            f.write(u.read())
    except:
        pass
  m['name']=" ".join(r.xpath('//li[@class="mep_name"]')[0].itertext()).strip()
  info=r.xpath('//div[@class="zone_info_mep_transparent_mep_details"]')[0]
  m['group']=info.xpath('./ul/li[2]')[0].text.strip()
  m['group_short']=info.xpath('./ul/li[2]/@class')[0].split(" ",1)[1]
  m['party']=info.xpath('.//span[@class="name_pol_group"]')[0].text
  m['country']=info.xpath('./ul/li[3]')[0].text.strip()
  m['country_short']=country_codes[m['country'].replace(' ', '')]
  try:
    m['email']="".join(reversed(r.xpath('//a[@id="email-0"]/@href')[0].replace("mailto:","").replace("[dot]",".").replace("[at]","@")))
  except IndexError:
    m['email']=None

  try:
    m['tel_bxl']=re.sub(r"[\s\n\r]", "", r.xpath('//span[@class="phone"]')[0].text.replace("(0)", ""))
  except IndexError:
    m['tel_bxl']=None
  try:
    m['tel_stg']=re.sub(r"[\s\n\r]", "", r.xpath('//span[@class="phone"]')[1].text.replace("(0)", ""))
  except IndexError:
    m['tel_stg']=None

  try:
    m['fax_bxl']=re.sub(r"[\s\n\r]", "", r.xpath('//span[@class="fax"]')[0].text.replace("(0)", ""))
  except IndexError:
    m['fax_bxl']=None
  try:
    m['fax_stg']=re.sub(r"[\s\n\r]", "", r.xpath('//span[@class="fax"]')[1].text.replace("(0)", ""))
  except IndexError:
    m['fax_stg']=None

  try:
    m['twitter']=re.sub(r".*twitter.com\/", "", r.xpath('//a[@class="link_twitt"]/@href')[0]).replace("@","").replace("/","")
  except IndexError:
    m['twitter']=None

  try:
    m['facebook']=r.xpath('//a[@class="link_fb"]/@href')[0]
  except IndexError:
    m['facebook']=None
  try:
    m['website']=r.xpath('//a[@class="link_website"]/@href')[0]
  except IndexError:
    m['website']=None

  try:
    i = 1;
    for position in r.xpath('//*[@id="content_left"]/div[1]/h4'):
      m[position.text] = []
      for x in r.xpath('//*[@id="content_left"]/div[1]/ul['+str(i)+']/descendant::*/a/acronym'):
        m[position.text].append(x.text)
      i = i + 1
  except IndexError:
    m['member']=None

  if boiler:
    m = merge_boiler(m)
  
  return m

def merge_boiler(m):
  b = get_mep_by_id(m['id'])
  if b is not None: 
    for x in b:
      m[x] = b[x]
  return m

def get_mep_by_id(id):
  for m in boiler:
    if m['id']==id:
      return m
  return None

def do():
  meps=reduce(lambda x,y: x+y, [extract_urls_from_page(i) for i in pages],
  [])
  meps=[expand_mep_info(m) for m in meps]
  with open("data-merged.json","wb") as f:
    json.dump(meps,f)

if __name__=='__main__':
    do()
