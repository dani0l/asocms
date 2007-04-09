# coding: iso-8859-1
# Kjaste / AsoCMS

import ConfigParser
import csv
import os
import sys

def append_sep(p):
    if not p.endswith(os.sep):
       p += os.sep 
    return p

def make_path(filename):
    # hole Pfad aus filename, mache ggf. \\ dran
    p = os.path.dirname(filename)
    p = append_sep(p)
    return p

def output(str):
    # schreibe
    print str

class Dummy:
    def __init__(self):
        pass

class TContent: # Klasse zum Einlesen des Contents aus Dateiname
    def __init__(self):
        output('Creating Contentmanager...')

    def get_content(self, filepath, filename):
        # hole Content
        f = file(filepath+filename, 'r')
        content = f.read()
        f.close()
        return content

class TMenu:
    def __init__(self, filename):
        # lies Menü-Schablone ein
        self.filename = filename
        output('Opening menu...')
        self.menufile = file(filename, 'r')
        self.menudata = self.menufile.read()

    def parse_one(self, linkinfo, last=0):
        # parse ein Menü mit Linkinformationen,
        # gib Menü-HTML zurück
        # linkinfo: [link], [extra], [text]
        # Wenn last == 1, bei <!--stophereiflast--> stoppen
        html = (' ' + self.menudata)[1:]
        html = html.replace('<!--$link-->', linkinfo['link'])
        html = html.replace('<!--$extra-->', linkinfo['extra'])
        html = html.replace('<!--$text-->', linkinfo['text'])
        if last:
            stophereiflast = html.find('<!--$stophereiflast-->')
            if stophereiflast != -1:
               html = html[:stophereiflast]
        else:
            html = html.replace('<!--$stophereiflast-->', '')
        return html
    
    def parse_all(self, linkinfo):
        # parse alle Menülinks
        # linkinfo: Sequenz aus [[link], [extra], [text]]
        output('Parsing menu...')
        html = ''
        for li in linkinfo:
            last = linkinfo[-1] == li # ist letztes?
            html += self.parse_one(li, last)
        return html
    
class TStencil:
    def __init__(self, filename):
        # lies Schablone ein
        self.filename = filename
        output('Opening stencil...')
        self.stencilfile = file(filename, 'r')
        self.stencildata = self.stencilfile.read()
        
    def parse(self, content, menu, title):
        # parse Schablone mit Content-HTML, Menü-HTML und Titel,
        # gib HTML-Seite zurück
        html = (' ' + self.stencildata)[1:]
        html = html.replace('<!--$menu-->', menu)
        html = html.replace('<!--$content-->', content)
        html = html.replace('<!--$title-->', title)
        return html
        
class TProjectFile:
    def __init__(self, filename):
        # lies INI ein
        self.filename = filename
        self._config = ConfigParser.ConfigParser()
        self._config.read(filename)
        # setze Variablen aus INI
        output('Parsing Projectfile...')
        path = make_path(self.filename)
        self.descfile = path+self._config.get('Options', 'descfile', '')
        self.stencilfile = path+self._config.get('Options', 'stencil', '')
        self.menufile = path+self._config.get('Options', 'menu', '')
        self.output = path+self._config.get('Options', 'output', '')
        #self.encoding = self._config.get('Options','encoding','utf-8')
        if not self.output.endswith(os.sep):
           self.output += os.sep
        
class TDescFile:
    def __init__(self, filename):
        # lies Descfile ein
        self.filename = filename
        self.csv = csv.reader(open(filename, "r"))
        # Variablen
        self.pages = list()
        # parse Descfile
        self.parse_descfile()
        
    def parse_descfile(self):
        # parse Descfile
        # Inhaltsüberschrift, Inhaltskurzname, Dateiname relativ zur Descfile
        # title, shortname, file
        output('Parsing Descfile...')
        for page in self.csv:
            if len(page) == 3:
                p = Dummy()   #page[1]
                p.title = page[0]
                p.shortname = page[1]
                p.file = page[2]
                self.pages.append(p)
                
    def get_page_as_linkinfo(self, p):
        # hole Page als Linkinfo-Dictionary
        return {'link':p.shortname+'.html','text':p.title,'extra':''}
    
    def get_all_pages_as_linkinfo(self):
        # hole alle Pages als Linkinfo-Dictionaries in einer Sequenz
        linkinfo = list()
        for p in self.pages:
            linkinfo.append(self.get_page_as_linkinfo(p))
        return linkinfo
            
class TTemplate:
    def __init__(self, projectfile):
        self.projectfile = TProjectFile(projectfile)
        self.descfile = TDescFile(self.projectfile.descfile)
        self.stencil = TStencil(self.projectfile.stencilfile)
        self.menu = TMenu(self.projectfile.menufile)
        self.content_manager = TContent()
        self.html_menu = self.menu.parse_all(self.descfile.get_all_pages_as_linkinfo())
        self.make_contents()
        
    def make_contents(self):
        output('Parsing Contents...')
        filepath = make_path(self.projectfile.descfile)
        output('Saving all files in %s' % (filepath))
        for page in self.descfile.pages:
            # hole Content
            content = self.content_manager.get_content(filepath, page.file)
            # hole HTML
            html = self.stencil.parse(content, self.html_menu, page.title)
            # speichere ab
            output('Creating file %s...' % (page.shortname+'.html'))
            f = file(self.projectfile.output + page.shortname+'.html', 'w')
            f.write(html)
            f.close()
        output('Done!')



print "AsoCMS: A simple Offline Content Management System"
print "by Friedrich 'fred.reichbier' Weber 06.04.2007 / April 2007"
print "type : asocms [ProjectFile]"
print "---------------------------"
if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
    projectfile = sys.argv[1]
    if os.path.dirname(projectfile) == '':
        projectfile = append_sep(os.getcwd()) + projectfile
    t = TTemplate(projectfile)
else:
    print "Error: File does not exist"

raw_input()