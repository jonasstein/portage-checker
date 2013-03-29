#!/usr/bin/python2.7

__author__="Jonas Stein (news@jonasstein.de)"

import portage
#import sys
#import urllib
import mechanize

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


def browsertest(url):
    br = mechanize.Browser()
    br.set_handle_redirect(True)
    try:
        br.open_novisit(url)
        return(htmlstring_OK)
    except:
        return(htmlstring_FAIL)
    
def pout(mystring):
    f = open("result.html", "a")
    f.write(mystring)
    f.close()

def main():
    # init
    porttree = portage.db[portage.root]['porttree']

    pout(htmlstring_HEAD)
    pout("""<body><table>""")

    all_cps = porttree.dbapi.cp_all()[1:30]

    for cp in all_cps:
        if (porttree.dep_bestmatch(cp)== "" ):
            bestcpv = porttree.dep_match(cp)

        else:
            bestcpv = porttree.dep_bestmatch(cp)
            package = {'name':cp,
                       'version':cp,
                       'homepage':porttree.dbapi.aux_get(bestcpv, ["HOMEPAGE"])[0],
                       'webstatus':browsertest(porttree.dbapi.aux_get(bestcpv, ["HOMEPAGE"])[0])}
            print(cp,bestcpv)
      
            pout("""<tr><td>%(name)s</td>
            <td><a href=%(homepage)s> %(homepage)s </a></td>
            <td>%(webstatus)s</td></tr> """ % package)


    pout(htmlstring_FOOTER)



if __name__ == '__main__':
    main()
