#!/usr/bin/env python
# coding: iso-8859-1
"""
   AsoCMS
   
   is released under the terms of the GNU GPL v2 License.

"""

# not sure whether asocms runs on linux...
import sys
import os
import shutil
import csv
import re
import ExtendedConfigParser as ECP
from string import Template as StrTemplate


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
    def __init__(self):
        # read menu-stencil
        #self.filename = filename
        output('Creating Menumanager')
        #self.menufile = file(filename, 'r')
        #self.menudata = self.menufile.read()
        #self.main_html = ''
    
    def create_menuitem_list(self, linkinfo):
        # create a tree-like list of menu items
        # [{'html':'<a href...', 'shortname':'', 'children':[{...}, {...}, ...]]
        # shortname = html-file without html
        tree = list() # tree-like
        blank = list()  # simple list without nodes
        for li in linkinfo:  # main menu items
            last = linkinfo[-1] == li # ist letztes?
            menuitem = {'template':dict(link=li['link'], extra=li['extra'], text=li['text']), 'shortname': li['shortname']}
            if li['child_of']:
                # set as child of parent
                # find parent
                parent = [lix for lix in blank if (lix['shortname'] == li['child_of'])][0]
                if not parent.has_key('children'):
                   parent['children'] = list()
                blank.append(menuitem)
                parent['children'].append(menuitem)
            else:
                # set as main
                tree.append(menuitem)
                blank.append(menuitem)
        self.maintree = tree
        return tree
    

class TStencil:
    def __init__(self, filename):
        # read main-stencil
        self.filename = filename
        output('Opening Stencil...')
        self.stencilfile = file(filename, 'r')
        self.stencildata = self.stencilfile.read()
        self.menu = None
        self.content = None

    def re_callback(self, match):
        # callback for self.parse()
        global st_new
        st_new = ''
        def write(s):
            # write something
            global st_new
            st_new += s
        # match.group() = the python snippet with <!--$ and $-->
        # strip whitespaces
        snip = match.group().strip()
        # fetch variables
        menu = self.menu
        content = self.content
        title =  self.title
        # delete <!--$ and $-->
        snip = snip.replace('<!--$', '')
        snip = snip.replace('$-->', '')
        # parse it
        exec(snip)
        return st_new

    def parse(self, menu, content, title):
        # parse the stencil. parse commands like <!--$ for ... $-->
        # menu = TMenu, content = current Content-String
        # use RE
        self.menu = menu
        self.content = content
        self.title = title
        old = (' ' + self.stencildata)[1:]
        re_comp = re.compile('<!--\$(.+?)\$-->', re.DOTALL)
        new = re_comp.sub(self.re_callback, old)
        return new


class TProjectFile:
    def __init__(self, filename):
        # read INI
        self.filename = filename
        self._config = ECP.ExtendedConfigParser()
        self._config.read(filename)
        # set vars of the ini
        output('Parsing Projectfile...')
        path = make_path(self.filename)
        self.descfile = path+self._config.get('Options', 'descfile', '')
        self.stencilfile = path+self._config.get('Options', 'stencil', '')
        self.output = path+self._config.get('Options', 'output', '')
        self.also_copy = self._config.get('Options', 'also-copy', '')
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
        # content title,  shortname, filename (relative to descfile)[, child_of (shortname of parent)]
        # title, shortname, file
        output('Parsing Descfile...')
        for page in self.csv:
            if len(page) >= 3:
                p = Dummy()   #page[1]
                p.title = page[0]
                p.shortname = page[1]
                p.file = page[2]
                if len(page) == 4:
                   p.child_of = page[3]
                else:
                   p.child_of = ''
                self.pages.append(p)
                
    def get_page_as_linkinfo(self, p):
        # fetch page as linkinfo-dictionary
        return {'link':p.shortname+'.html','text':p.title,'extra':'','child_of':p.child_of,'shortname':p.shortname}
    
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
        self.menu = TMenu()
        self.content_manager = TContent()
        self.menu.create_menuitem_list(self.descfile.get_all_pages_as_linkinfo())
        self.make_contents()

    def make_contents(self):
        output('Parsing Contents...')
        filepath = make_path(self.projectfile.descfile)
        output('Saving all files in %s' % (self.projectfile.output))
        for page in self.descfile.pages:
            # fetch content
            content = self.content_manager.get_content(filepath, page.file)
            # fetch ready html
            html = self.stencil.parse(self.menu, content, page.title)
            # save
            output('Creating file %s...' % (page.shortname+'.html'))
            f = file(self.projectfile.output + page.shortname+'.html', 'w')
            f.write(html)
            f.close()
        # Also copy the files specified in the ProjectINI, Option 'also-copy'
        for copyfile in self.projectfile.also_copy.split(','):
            if copyfile.strip() == '':
               continue
            output('Copying file %s...' % (copyfile))
            if os.path.isfile(filepath + copyfile):
               shutil.copy(filepath + copyfile, self.projectfile.output)
            else:
               output('File not found: %s!' % (filepath + copyfile))
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