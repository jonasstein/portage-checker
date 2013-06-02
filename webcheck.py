#!/usr/bin/python2.7

__author__="Jonas Stein (news@jonasstein.de)"

import os 
import fnmatch
import requests


htmlstring_FAIL = """<basefont color="#FF2020">FAIL</font>"""
htmlstring_OK = """<basefont color="#20FF20">OK</font>"""

htmlstring_HEAD = """ <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="de">
<head>
<title>gentoo ebuild checker</title>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
</head>
"""

htmlstring_FOOTER = """</table> </body> </html>"""


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def dropQuotes(quotedString):
    nostartquote = (quotedString.split('"')[1])
    noendquote = (nostartquote.split('"')[0])
    return(noendquote)
    
def getValue(key, filename):
    key += "="
    value = ""
    for line in open(filename):
        if key in line:
            value = dropQuotes(line.split("=")[1])
    return(value)


def browsertest(url):
    print(url)# "checking url: %s")%url


    try:
        r = requests.get(url) 
    except requests.exceptions.Timeout:
        msg = "EE: Maybe set up for a retry, or continue in a retry loop"
    except requests.exceptions.TooManyRedirects:
        msg = "EE: Tell the user their URL was bad and try a different one"
    except requests.exceptions.RequestException as e:
        msg = "EE: catastrophic error. bail."
        return(msg)    
    return(r.status_code)    
    
def pout(mystring):
    f = open("result.html", "a")
    f.write(mystring)
    f.close()


def main():
    # init

    pout(htmlstring_HEAD)
    pout("""<body><table>""")
    
    ebuilds = find('*.ebuild', '/usr/portage')

    for thisEbuild in ebuilds:
        package = {"name" : thisEbuild.split("/usr/portage/")[1],
                   "description" : getValue("DESCRIPTION",thisEbuild),
                   "homepage" : getValue("HOMEPAGE",thisEbuild),
                   "webstatus" : browsertest(getValue("HOMEPAGE",thisEbuild)),
                   "license" : getValue("LICENSE",thisEbuild)}

    
        pout("""<tr><td>%s</td>""" % (package["name"]))

        pout("""<td><a href=%(homepage)s> %(homepage)s </a></td>
        <td>%(webstatus)s</td>
        <td><a href="https://bugs.gentoo.org/enter_bug.cgi?product=Gentoo Linux&format=guided">report bug</a></td></tr> """ % package)

    pout(htmlstring_FOOTER)


if __name__ == '__main__':
    main()
