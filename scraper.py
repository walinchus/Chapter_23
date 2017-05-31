###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree

url = "https://www.parliament.uk/documents/lords-committees/house/Minutes/2016-17/HCMinutes-1-290616.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]


# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

# print the first hundred text elements from the first page
page0 = pages[0]
for el in list(page0)[:100]:
    if el.tag == "text":
        print el.attrib, gettext_with_bi_tags(el).encode('ascii','ignore')


ID = 0
for el in list(page0)[:100]:
    print el.tag
    if el.tag == "text":
        print el.attrib, gettext_with_bi_tags(el).encode('ascii','ignore')
    record = {}
    record["text"] = gettext_with_bi_tags(el).encode('ascii','ignore')
    ID = ID+1
    record["ID"] = ID
    scraperwiki.sqlite.save(["ID"],record)
    print record
