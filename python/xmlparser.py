import xml


from xml.parsers import expat



class XMLParser(object):


    """docstring for XMLParser"""


    def __init__(self, contentKey='content', useAttrs=True, attrPrefix='@'):


        super(XMLParser, self).__init__()


        self.parser = expat.ParserCreate()


        self.parser.StartElementHandler = self.startElement


        self.parser.EndElementHandler = self.endElement


        self.parser.CharacterDataHandler = self.characterData


        self.contentKey = contentKey


        self.useAttrs = useAttrs


        self.attrPrefix = attrPrefix


        self.reset()



    def reset(self):


        self.path = []


        self.stack = []


        self.item = None



    def parse(self, xml):


        self.reset()


        self.parser.Parse(xml, True)


        return self.item



    def startElement(self, name, attrs):


        self.path.append((name, attrs or None))


        self.stack.append(self.item)


        if self.useAttrs and self.attrPrefix:


            attrs = dict((self.attrPrefix+key, value) for (key, value) in attrs.items())


        self.item = self.useAttrs and attrs or None


    
    def endElement(self, name):


        if len(self.stack):


            item = self.item


            self.item = self.stack.pop()


            self.push_item(name, item) #item becomes content of self.item


        else:


            self.item = None


        self.path.pop()



    def characterData(self, data):


        if data.strip():


            if not self.item:


                self.item = data


            elif isinstance(self.item, dict):


                if self.contentKey in self.item:


                    self.item[self.contentKey] += data


                else:


                    self.item[self.contentKey] = data


            else:


                self.item += data



    def push_item(self, key, subitem):


        if self.item is None:


            self.item = dict()


        try:


            value = self.item[key]


            if isinstance(value, list):


                value.append(subitem)


            else:


                self.item[key] = [value, subitem]


        except KeyError:


            self.item[key] = subitem



def parse(xml):


   parser = XMLParser(useAttrs=False)


   return parser.parse(xml)
