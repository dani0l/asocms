# Introduction #

AsoCMS is currently organized in files. Here you can find a little summary of the files.

**This Page contains information for asocms 0.1. In later versions, something has changed.**


# Files #

## Projectfile (**.ini) ##
The Projectfile describes the names of the other files in the Windows-INI-Format.**

Example:
```
[Options]
descfile = descfile.txt
stencil = index.html
menu = menu.txt
output = html\
```

You see, a Projectfile has one section named 'Options'. The names of the keys describes the function of the entry.

## Descfile ##
The Descfile is a CSV (comma-seperated values) file which describes the pages and the menu links.

Example:
```
"Main Page","index","hp-index.txt"
"About us","about-us","hp-aboutus.txt"
```
The Values:
"_Page title and Menu Link Title_","_Name of the HTML-file (without extension)_","_Content-File_"

## Stencilfile ##
The Stencilfile is a HTML-file with placeholders for title, content and menu.

Example:
```
<html>
<head>
  <title><!--$title--></title>
</head>
<body>
<ul>
<!--$menu-->
</ul>
<br />
<p>
<!--$content-->
</p>
</body>
</html>
```

## Menufile ##
The Menufile is parsed for each menu item. It contains placeholders for the menu link.

Example:
```
<li><a href="<!--$link-->"<!--$extra-->><!--$text--></a></li>
```
Placeholders:

|<!--$link-->| Link to HTML-File, normally in the href=""-Tag|
|:-----------|:----------------------------------------------|
|<!--$extra-->| Extra informations like _target="_blank"_(not used in the current version)_|
|<!--$text-->| The Link Text, normally between the <a> and the </a> tag.|

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