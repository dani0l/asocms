# -*- coding: iso-8859-1 -*-
## Extended Config Parser v1.0 ##
## released under the terms of the GNU GPL v2 ##
## von Friedrich Weber / Akaz, reichbier.de ##
## besserer Configparser mit Funktionen zum Speichern und Laden ##
## Grund von http://python.net/pipermail/python-de/2005q1/006498.html ##

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
    # hole nur oben angegebenes und gib es zurück, dann
    # gib den Parser wieder frei
    p = ExtendedConfigParser()
    p.read(filename)
    res = p.get(section, option, default)
    del p
    return res
