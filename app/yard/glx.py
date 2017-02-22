# coding: utf-8

import requests
from lxml import etree


def grab(bl_num='HDMUQIAS4311777'):

    session = requests.session()

    session.get("http://www.cmlog.com.cn/WebApp/loginnew.aspx")
    session.get("http://www.cmlog.com.cn/zcxt/Frame/Home.aspx")
    session.get("http://www.cmlog.com.cn/zcxt/GLX/ExportUsual.aspx")

    data = {
        '__VIEWSTATE': '/wEPDwUKLTY4NjM1MzA1MQ9kFgJmD2QWAgIDD2QWBAIDDw8WAh4EVGV4dAVCPGZvbnQgc3R5bGU9J2NvbG9yOiM1YjViNWI7Jz7muK/ogZTmrKPmn6Xor6IgLSDpgJrnlKjmn6Xor6I8L2ZvbnQ+ZGQCCQ9kFgQCAw8PZBYCHgdvbmNsaWNrBQ5TaG93V2FpdGluZygpO2QCBw8WAh4HVmlzaWJsZWgWEAIBD2QWAmYPZBYCAgEPPCsAEQIBEBYAFgAWAAwUKwAAZAIDD2QWAmYPZBYCAgEPPCsAEQIBEBYAFgAWAAwUKwAAZAIFD2QWAmYPZBYCAgEPPCsAEQIBEBYAFgAWAAwUKwAAZAIHD2QWAmYPZBYCAgEPPCsAEQIBEBYAFgAWAAwUKwAAZAIJD2QWAmYPZBYCAgEPPCsAEQIBEBYAFgAWAAwUKwAAZAILD2QWAmYPZBYCAgEPPCsAEQIBEBYAFgAWAAwUKwAAZAIND2QWAmYPZBYCAgEPPCsAEQIBEBYAFgAWAAwUKwAAZAIQD2QWAmYPZBYCAgEPPCsAEQIBEBYAFgAWAAwUKwAAZBgIBSVfY3RsMDpDb250ZW50UGxhY2VIb2xkZXIxOmd2U2hpWmh1YW5nDzwrAAwCBhUBBmN0bnJlZggC/////w9kBSJfY3RsMDpDb250ZW50UGxhY2VIb2xkZXIxOmd2VmVzdm95DzwrAAwCBhUBBVpDWVdZCAL/////D2QFJF9jdGwwOkNvbnRlbnRQbGFjZUhvbGRlcjE6Z3ZFeHByZXN0dQ88KwAMAgYVBQhjdG5hcHBsYgV0eGVkdAVlaXJubwdlbWZ1ZWR0BWN0bm5vCAL/////D2QFIl9jdGwwOkNvbnRlbnRQbGFjZUhvbGRlcjE6Z3ZDdXN0b20PZ2QFIF9jdGwwOkNvbnRlbnRQbGFjZUhvbGRlcjE6Z3ZCaWxsDzwrAAwCBhUDBmJpbGxubwdtYmlsbG5vCGV4YmlscmVmCAL/////D2QFIl9jdGwwOkNvbnRlbnRQbGFjZUhvbGRlcjE6Z3JkVHJrdGIPZ2QFIV9jdGwwOkNvbnRlbnRQbGFjZUhvbGRlcjE6Z3ZFb3lwbA9nZAUjX2N0bDA6Q29udGVudFBsYWNlSG9sZGVyMTpndkRpbmdoYW8PZ2S6SUPdeOExdY9hF6JGoPS318LLBvUJZWp4gyR+696KjA==',
        '_ctl0:ContentPlaceHolder1:TextBox1': bl_num.strip(),
        '_ctl0:ContentPlaceHolder1:btnQuery': u'查询'
    }
    response = session.post("http://www.cmlog.com.cn/zcxt/GLX/ExportUsual.aspx", data=data)

    html = etree.HTML(response.text)

    info_html = html.xpath("//table[@id='_ctl0_ContentPlaceHolder1_tbl']")

    if len(info_html) > 0:

        elem_links = info_html[0].xpath("//a")
        for elem_link in elem_links:
            elem_link.set("href", "#")

        info = etree.tostring(info_html[0], pretty_print=True)
    else:
        info = None
    session.close()

    return info


if __name__ == '__main__':
    grab()
