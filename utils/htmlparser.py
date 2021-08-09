from urllib.request import urlopen
from lxml import etree
from io import BytesIO


__tag_xpath    = "XPath="
__tag_selector = "__select__:"


def convert_to_value(tree, s):
    if has_xpath_tag(s):
        s = s[len(__tag_xpath):]
        return get_xpath_value(tree, s)
    elif has_selector_tag(s):
        s = s[len(__tag_selector):]
        return get_selector_value(tree, s)
    else:
        return s

def get_xpath_value(html_tree, xpath_string):
    try:
        elem = html_tree.xpath(xpath_string)
        text = []
        for child in elem:
            if type(child) is etree._Element:
                text.append(''.join(elem[0].itertext()))
            elif type(child) is etree._ElementUnicodeResult:
                text.append(str(child))
        text = ''.join(text).strip()
        print(text)
        return text
    except etree.XPathError:
        return ''

def get_selector_value(html_tree, selector_string):
    # not implemented
    return ""

def has_xpath_tag(s):
    return len(s) > len(__tag_xpath) and s[0:len(__tag_xpath)] == __tag_xpath

def has_selector_tag(s):
    return len(s) > len(__tag_selector) and s[0:len(__tag_selector)] == __tag_selector
    
def get_html_tree(url):
    with urlopen(url) as page:
        parser = etree.HTMLParser()
        tree   = etree.parse(BytesIO(page.read()), parser)
        return tree
 