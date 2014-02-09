from xml.dom.minidom import parseString
import urllib.request
import pprint

class HTMLPrettyPrinter():
    def __init__(self):
        self.state = ""
        self.indentlevel = 0
        self.retval = ""

    def feed(self, str):
        dom = parseString('<content>'+str+'</content>')
        
        #print(dom.firstChild.childNodes)
        self.descend(dom.firstChild)
        return self.retval
            
    def descend(self, node):
        for node in node.childNodes:
            if node.nodeType == node.ELEMENT_NODE and node.tagName != 'i':
                self.handleTag(node, True)
                self.descend(node)
                self.handleTag(node, False)
                
            elif node.nodeType == node.TEXT_NODE:
                self.handleText(node)
            else:
                self.retval += node.firstChild.data
                #print(node.firstChild.data, end="")
                
                
    def handleTag(self, node, enter=True):
        #guaranteed to have tagname
        if enter:
            mul = 1
        else:
            mul = -1
            
        if node.tagName == 'p':
            if not enter:
                #print()
                self.retval += '\n'
        elif node.tagName == 'ul':
            self.indentlevel += 4*mul
        elif node.tagName == 'li':
            if enter:
                offset = ' ' * self.indentlevel
                self.retval += offset + "• "
                #print(offset, "• ", end="")
            else:
                self.state = ""
        else:
            
            pass
        
    def handleText(self, node):
        offset = ' ' * self.indentlevel
        self.retval+=node.data
        #print( node.data, end="")