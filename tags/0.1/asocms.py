#!/usr/bin/env python
# coding: iso-8859-1
"""
   AsoCMS
   
   is released under the terms of the GNU GPL v2 License.

"""

# not sure whether asocms runs on linux...

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

def output(s):
    # schreibe
    print s

class Dummy:
    def __init__(self):
        pass

class TContent: # class for reading content-files
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
        # read menu-stencil
        self.filename = filename
        output('Opening menu...')
        self.menufile = file(filename, 'r')
        self.menudata = self.menufile.read()

    def parse_one(self, linkinfo, last=0):
        # parse ONE menu-link with information,
        # return HTML
        # linkinfo: {link, extra, text}
        # if last == 1, stop at <!--stophereiflast-->
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
        # parse all menu links
        # linkinfo: list [{link, extra, text}]
        output('Parsing menu...')
        html = ''
        for li in linkinfo:
            last = linkinfo[-1] == li # ist letztes?
            html += self.parse_one(li, last)
        return html
    
class TStencil:
    def __init__(self, filename):
        # read main-stencil
        self.filename = filename
        output('Opening stencil...')
        self.stencilfile = file(filename, 'r')
        self.stencildata = self.stencilfile.read()
        
    def parse(self, content, menu, title):
        # parse stencil with Content-HTML, Menu-HTML and title,
        # return pretty HTML-Page
        html = (' ' + self.stencildata)[1:]
        html = html.replace('<!--$menu-->', menu)
        html = html.replace('<!--$content-->', content)
        html = html.replace('<!--$title-->', title)
        return html
        
class TProjectFile:
    def __init__(self, filename):
        # read INI
        self.filename = filename
        self._config = ConfigParser.ConfigParser()
        self._config.read(filename)
        # set vars of the ini
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
        # read descfile
        self.filename = filename
        self.csv = csv.reader(open(filename, "r"))
        # Vars
        self.pages = list()
        # parse descfile
        self.parse_descfile()
        
    def parse_descfile(self):
        # parse Descfile
        # content title,  shortname, filename (relative to descfile)
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
        # fetch page as linkinfo-dictionary
        return {'link':p.shortname+'.html','text':p.title,'extra':''}
    
    def get_all_pages_as_linkinfo(self):
        # fetch all pages as linkinfo-dictionary in a list
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
        self.html_menu = self.menu.parse_all(self.descfile.get_all_pages_as_linkinfo())  # fetch ready menu
        self.make_contents()
        
    def make_contents(self):
        output('Parsing Contents...')
        filepath = make_path(self.projectfile.descfile)
        output('Saving all files in %s' % (filepath))
        for page in self.descfile.pages:
            # fetch content
            content = self.content_manager.get_content(filepath, page.file)
            # fetch ready html
            html = self.stencil.parse(content, self.html_menu, page.title)
            # save
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