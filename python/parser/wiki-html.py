import urllib, urllib2, re, time
import xmlparser
from datetime import date
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

def removeLinks(text):
   def linkLabel(link):
      m = re.search('\|(.*?)\]\]',link.group(0))
      if m:
         return m.group(1)
      return link.group(1)
   return re.sub('\[\[([^\]\[]*?)\]\]', linkLabel, text, flags=re.DOTALL) #rm wiki links

def extractLinks(text):
   print 'You mean:'
   for m in re.finditer('\[\[([^\]\[]*?)\]\]', text):
      print m.group(1).split('|')[-1]

def removeIPA(text):
   def ipaText(ipa):
      s = ipa.group(1).split('|')
      for i in range(len(s)):
         if s[i] == u'\u02c8':
            return ''.join(s[i:])
         elif s[i][0] == u'\u02c8':
            return s[i]
      return ''

   return re.sub('{{IPA(.*?)}}', ipaText, text)

def removeRefs(text):
   #text = re.sub('{{[^I](.*?)}}', '', text) #remove all {{}} except infobox
   #text = re.sub('^.*?\<nowiki\>\<\/nowiki\>', '', text, flags=re.DOTALL) #remove all {{}} 
   text = re.sub('\{\{.*?\}\}', '', text, flags=re.DOTALL) #remove all {{}} 
   #text = re.sub('\[\[Image:(.*?)\]\]', '', text, flags=re.DOTALL) #remove files
   #text = re.sub('\[\[File:(.*?)\]\]', '', text, flags=re.DOTALL) #remove files
   #text = re.sub('\[\[Category:(.*?)\]\]', '', text, flags=re.DOTALL) #remove files
   #text = re.sub('\[http(.*?)\]', '', text, flags=re.DOTALL) #remove files
   #text = re.sub('<.*?>', '', text, flags=re.DOTALL) #remove refs
   text = re.sub('\{\|\ class(.*?)\}', '', text, flags=re.DOTALL) #remove all {{}} 

   return text

def getBirthday(name):
   info = getInfoBox(name)
   if info:
      m = re.search('birth_date\s*?=\s*?{{(.*?)}}', info)
      if m:
         info = m.group(1).split('|')
         l = [num for num in info if num.isdigit()]
         bday = date(2000, int(l[1]), int(l[2]))
         return bday.strftime('%B %d, ' + l[0])
   return None

def getInfoBox(keywords):
   page = getPage(keywords)
   if not page:
      return None
   si = page.find('{{Infobox') + 10
   ei = page.rfind('}}')
   return page[si:ei]

def getSummary(keywords):
   page = getPage(keywords)
   if not page:
      return None
   try:
      page = removeIPA(page)
      page = removeRefs(page)
      page = removeLinks(page)
      print page
      ei = page.rfind('}}') #find start of summary
      if ei < 0:
         ei = -2
      summary = page[ei+2:]

      summary = re.sub("'''*", '', summary) #rm bolded/italic text
      return summary
   except Exception, e:
      return None

def getText(url_title):
   
   page = getPage(url_title)
   
   if not page:
      return None
   try:
      ps = BeautifulSoup(page).findAll('p')
      s = ''

      for p in ps:
         temp = str(p)
         temp = re.sub('\<.*?\>', '', temp);
         temp = re.sub('\[.*?\]', '', temp);
         s += temp 
         s += ' '

      s = BeautifulStoneSoup(s, convertEntities="html", 
                               smartQuotesTo="html").contents[0]
      return s
      
   except Exception, e:
      print e
      return None

def getPage(url_title, format='xml'):
   # Base Url:
   url = 'http://en.wikipedia.org/wiki/' + url_title
   try:
      
      print url
      
      req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
      page = urllib2.urlopen(req).read()
      
      
      return page
   except Exception, e:
      print e
      return None

if __name__ == '__main__':
   print getText('Kennet_and_Avon_Canal')

