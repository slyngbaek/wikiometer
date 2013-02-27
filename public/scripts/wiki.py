import urllib, urllib2, re, time
import xmlparser
from datetime import date

def removeLinks(text):
   def linkLabel(link):
      m = re.search('\|(.*?)\]\]',link.group(0))
      if m:
         return m.group(1)
      return link.group(1)
   return re.sub('\[\[([^\]\[]*?)\]\]', linkLabel, text) #rm wiki links

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
      page = removeLinks(page)
      page = removeIPA(page)
      page = re.sub('{{[^I](.*?)}}', '', page) #remove all {{}} except infobox
      page = re.sub('\[\[Image:(.*?)\]\]', '', page) #remove files
      page = re.sub('\[\[File:(.*?)\]\]', '', page) #remove files
      page = re.sub('<ref(.*?)/(ref)?>', '', page) #remove refs
      page = re.sub('<!--(.*?)-->', '', page) #remove refs
      #print page
      ei = page.rfind('}}') #find start of summary
      if ei < 0:
         ei = -2
      summary = page[ei+2:]

      summary = re.sub("'''*", '', summary) #rm bolded/italic text
      return summary
   except Exception, e:
      return None

def getPage(keywords, format='xml'):
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
      'titles'     : keywords.replace(' ', '_'),
      # Specify that we want the page content
      'rvprop'     : 'content',
      # Lets you choose which section you want. 0 is the first one.
      'rvsection'  : '0',
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
