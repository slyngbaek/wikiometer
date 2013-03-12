import urllib, urllib2, re, time
import xmlparser
from datetime import date

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
   #url_title = re.sub('http://en.wikipedia.org/wiki/', '', url)
   #re.sub('en.wikipedia.org/wiki/', '', url_title)
   page = getPage(url_title)
   if not page:
      return None
   try:
      print page + '\n\n\n\n\n\n\n\n\n'
      page = removeRefs(page)
      #page = removeIPA(page)
      #page = removeLinks(page)
      print page
   except Exception, e:
      return None

def getPage(url_title, format='xml'):
   # Base Url:
   base_url = 'http://en.wikipedia.org/w/api.php?'
   values = {
      # Specify Format
      'format'     : format,
      # Specify action type.
      'action'     : 'query',
      # Tell it to get the latest revision
      'prop'       : 'revisions',
      # Define page titles separated by pipes
      'titles'     : url_title,
      'rvprop'     : 'content',
      #automatically resolves redirects
      'redirects'  : ''
   }

   values = urllib.urlencode(values)
   req = urllib2.Request(base_url, values, {"User-Agent":"Magic Browser"})

   try:
      # Get request from web
      xml = urllib2.urlopen(req).read()
      # Parse XML
      doc =  xmlparser.parse(xml)
      # Get page from response
      page = doc['api']['query']['pages']['page']
      if page:
         page = page['revisions']['rev']

         # Handle Redirect
         if page[:10] == '{{Redirect' or page[:12] == '{{Wiktionary':
            extractLinks(page)
            #print page
            return None

      return page
   except Exception, e:
      print e
      return None

if __name__ == '__main__':
   getText('Michael_jordan')

