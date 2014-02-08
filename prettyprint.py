from xml.dom.minidom import parseString
import urllib.request
import pprint

class HTMLPrettyPrinter():
    def __init__(self):
        self.state = ""
        self.indentlevel = 0

    def feed(self, str):
        dom = parseString('<content>'+str+'</content>')
        
        #print(dom.firstChild.childNodes)
        self.descend(dom.firstChild)
            
    def descend(self, node):
        for node in node.childNodes:
            if node.nodeType == node.ELEMENT_NODE and node.tagName != 'i':
                self.handleTag(node, True)
                #print(node.tagName)
                self.descend(node)
                self.handleTag(node, False)
                
                #print("/"+node.tagName)
            elif node.nodeType == node.TEXT_NODE:
                self.handleText(node)
            else:
                print(node.firstChild.data, end="")
                
                
    def handleTag(self, node, enter=True):
        #guaranteed to have tagname
        if enter:
            mul = 1
        else:
            mul = -1
            
        if node.tagName == 'p':
            if not enter:
                print()
        elif node.tagName == 'ul':
            self.indentlevel += 4*mul
        elif node.tagName == 'li':
            if enter:
                offset = ' ' * self.indentlevel
                print(offset, "• ", end="")
            else:
                self.state = ""
        else:
            
            pass
        
    def handleText(self, node):
        offset = ' ' * self.indentlevel
        print( node.data, end="")