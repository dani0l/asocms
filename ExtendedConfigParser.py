# -*- coding: iso-8859-1 -*-
"""
	ExtendedConfigParser, released under the zlib/libpng license
	
	Copyright (c) 2006-2007 Friedrich Weber

	This software is provided 'as-is', without any express or implied
	warranty. In no event will the authors be held liable for any damages
	arising from the use of this software.
	
	Permission is granted to anyone to use this software for any purpose,
	including commercial applications, and to alter it and redistribute it
	freely, subject to the following restrictions:

	    1. The origin of this software must not be misrepresented; you must not
	    claim that you wrote the original software. If you use this software
	    in a product, an acknowledgment in the product documentation would be
	    appreciated but is not required.
	
	    2. Altered source versions must be plainly marked as such, and must not be
	    misrepresented as being the original software.
	
	    3. This notice may not be removed or altered from any source
	    distribution.
	    
	(gpl before)
"""

from ConfigParser import ConfigParser

class ExtendedConfigParser(ConfigParser):
    ### config file reader class ###
    def __init__(self):
        ConfigParser.__init__(self)
        self.loadedfile = '' ## file loaded, set in read() ##

    def read(self, filename):
        ## read ONE file ##
        ConfigParser.read(self, [filename])
        self.loadedfile = filename

    def savetofile(self, filename):
        ### save to filename ###
        f = file(filename, 'w')
        self.write(f)
        f.close

    def save(self):
        ### save to the loaded file ###
        if self.loadedfile != '':
            self.savetofile(self.loadedfile)
        else:
            import warnings
            warnings.warn("Call savetofile()!", None, 2)
            
    def set(self, section, option, value):
        # lege Section an, falls sie nicht existiert
        if not self.has_section(section):
           self.add_section(section)
        ConfigParser.set(self, section, option, value)
        
    def get(self, section, option, default=None):
        res = default
        if ConfigParser.has_option(self, section, option):
            res = ConfigParser.get(self, section, option)
        return res

    def getbool(self, section, option, default=None):
        ### short version of getboolean ###
        res = default
        if ConfigParser.has_option(self, section, option):
            res = ConfigParser.getboolean(self, section, option)
        return res

    def getint(self, section, option, default=None):
        res = default
        if ConfigParser.has_option(self, section, option):
            res = ConfigParser.getint(self, section, option)
        return res

    def getlist(self, section, option, default=None):
        ### convert a space separated option value to a list ###
        res = default
        if ConfigParser.has_option(self, section, option):
            res = ConfigParser.get(self, section, option).strip()
            res = res.replace('\n', ' ')
            if ' ' in res:
                res = res.split(' ')
            else:
                res = [res]
            while '' in res:
                res.remove('')
        return res
        
def get_and_free(filename, section, option, default=''):
    # hole nur oben angegebenes und gib es zurck, dann
    # gib den Parser wieder frei
    p = ExtendedConfigParser()
    p.read(filename)
    res = p.get(section, option, default)
    del p
    return res

