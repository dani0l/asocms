# Introduction #

AsoCMS is currently organized in files. Here you can find a little summary of the files.

**This Page contains information for asocms 0.2.**


# Files #

## Projectfile (**.ini) ##
The Projectfile describes the names of the other files in the Windows-INI-Format.**

Example:
```
[Options]
descfile = descfile.txt
stencil = index.html
output = html\
also-copy = 
```

You see, a Projectfile has one section named 'Options'. The names of the keys describes the function of the entry.

_also-copy_: If you have a css-file, images or something like this in the directory with the descfile, you can copy these files with the command _also-copy_.
The filenames (relative to the descfile) are seperated by commas.

## Descfile ##
The Descfile is a CSV (comma-seperated values) file which describes the pages and the menu links.

Example:
```
"Main Page","index","hp-index.txt"
"About us","about-us","hp-aboutus.txt","index"
```
The Values:
"_Page title and Menu Link Title_","_Name of the HTML-file (without extension)_","_Content-File_","_Parent (not required)_"
For submenus, just type the shortname of the parent item as 4th value.

## Stencilfile ##
The stencilfile is the stencil for generating the HTML-pages. In new versions, you can use python code in <!--$ and $-->.
Example:
```
<html>
<head>
  <title><!--$write(title)$--></title>
</head>
<body>
<!--$
pattern = '<li><a href="$link"$extra>$text</a>'
def writeItems(tree, pattern, write, writeItems):
    write('<ul>')
    for item in tree:
        write(StrTemplate(pattern).safe_substitute(item['template']))
        if item.has_key('children') and len(item['children']) > 0:
           writeItems(item['children'], pattern, write, writeItems)
        write('</li>')
    write('</ul>')
writeItems(menu.maintree, pattern, write, writeItems)
$-->
<br />
<p>
<!--$
write(content)
$-->
</p>
</body>
</html>
```

In the stencilfile you can use Python code. Use the function write() to write in the html output.
The following names are defined:
|menu|Menu Information (there: menu.maintree, a list of dictionaries). It is recommended that you use the existing function _writeItems_|
|:---|:---------------------------------------------------------------------------------------------------------------------------------|
|content|HTML-Content of the current page                                                                                                  |
|title|Title of the current page                                                                                                         |
In the name _pattern_ you can define a individual pattern for one link.

## Menufile ##
In versions >0.2, there are no menu files longer.

## Content-Files ##
The most important files are the content-files. Their names are defined in the descfile, they contain the HTML-Content.

Example:

_hp-index.txt_
```
<b>This text is bold</b>, <i>this text is italic</i>, <u>This one is underlined</u>.<br/>
Lorem ipsum.
```
This text will be displayed in the file index.html.

_hp-aboutus.txt_
```
<i>We are a team of</i> ... <b>blah blah blah</b>
```
This text will be displayed in the file about-us.html.

If you run asocms with these files, the HTML-Files _index.html_ and _about-us.html_ will be created in the directory html\. Have fun.