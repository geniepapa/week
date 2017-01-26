# coding: utf-8

import requests
from lxml import etree


def grab(bl_num='177TCACAQ11817FB'):

    session = requests.session()

    login_data = {
        '__VIEWSTATE': '/wEPDwUKLTE2NjU3ODMwOQ9kFgJmD2QWAgIDD2QWAgIFDxYCHgtfIUl0ZW1Db3VudAIKFhRmD2QWAgIBDxYCHgRUZXh0BVA8YSAgaHJlZj0iaHR0cDovL3d3dy5tZWRsb2cuY29tLmNuOjg4NjYvSW5kZXguYXNweCIgdGl0bGU9IummlumhtSI+6aaW6aG1PC9hPiB8IGQCAQ9kFgICAQ8WAh8BBX08YSAgaHJlZj0iaHR0cDovL3d3dy5tZWRsb2cuY29tLmNuOjg4NjYvbmV3cy9tYWluaXRlbS5hc3B4P3NpZD0yMDEzMTExODA4MDYwNTk2ODI1MyIgdGl0bGU9IuWFrOWPuOamguWGtSI+5YWs5Y+45qaC5Ya1PC9hPiB8IGQCAg9kFgICAQ8WAh8BBX08YSAgaHJlZj0iaHR0cDovL3d3dy5tZWRsb2cuY29tLmNuOjg4NjYvbmV3cy9JdGVtTGlzdC5hc3B4P3NpZD0yMDEzMTExODA4MzI1ODkwNjg5NCIgdGl0bGU9IuWSqOivouS4reW/gyI+5ZKo6K+i5Lit5b+DPC9hPiB8IGQCAw9kFgICAQ8WAh8BBX08YSAgaHJlZj0iaHR0cDovL3d3dy5tZWRsb2cuY29tLmNuOjg4NjYvbmV3cy9tYWluaXRlbS5hc3B4P3NpZD0yMDEzMTExODA4MzM1MjA0NjU3NiIgdGl0bGU9IuWFrOWPuOS4muWKoSI+5YWs5Y+45Lia5YqhPC9hPiB8IGQCBA9kFgICAQ8WAh8BBXs8YSAgaHJlZj0iaHR0cDovL3d3dy5tZWRsb2cuY29tLmNuOjg4NjYvbmV3cy9JdGVtTGlzdC5hc3B4P3NpZD0yMDEzMTExODA4MzkyMDg5MDYiIHRpdGxlPSLph4fotK3mi5vmoIciPumHh+i0reaLm+aghzwvYT4gfCBkAgUPZBYCAgEPFgIfAQV9PGEgIGhyZWY9Imh0dHA6Ly93d3cubWVkbG9nLmNvbS5jbjo4ODY2L25ld3MvbWFpbml0ZW0uYXNweD9zaWQ9MjAxMzExMTgwODQwNTYzMTI4NzQiIHRpdGxlPSLkv6Hmga/mioDmnK8iPuS/oeaBr+aKgOacrzwvYT4gfCBkAgYPZBYCAgEPFgIfAQVwPGEgIGhyZWY9Imh0dHA6Ly93d3cubWVkbG9nLmNvbS5jbjo4ODY2L3F1ZXJ5ZGF0YS9iaWxscXVlcnlzZWFyY2guYXNweCIgdGl0bGU9IuWcqOe6v+afpeivoiI+5Zyo57q/5p+l6K+iPC9hPiB8IGQCBw9kFgICAQ8WAh8BBWI8YSAgaHJlZj0iaHR0cDovL3d3dy5tZWRsb2cuY29tLmNuOjg4NjYvbmV3cy9IUmxpc3QuYXNweCIgdGl0bGU9IuS6uuaJjeaLm+iBmCI+5Lq65omN5oub6IGYPC9hPiB8IGQCCA9kFgICAQ8WAh8BBWY8YSAgaHJlZj0iaHR0cDovL3d3dy5tZWRsb2cuY29tLmNuOjg4NjYvbmV3cy90YWxrT25saW5lLmFzcHgiIHRpdGxlPSLlnKjnur/nlZnoqIAiPuWcqOe6v+eVmeiogDwvYT4gfCBkAgkPZBYCAgEPFgIfAQV9PGEgIGhyZWY9Imh0dHA6Ly93d3cubWVkbG9nLmNvbS5jbjo4ODY2L25ld3MvbWFpbml0ZW0uYXNweD9zaWQ9MjAxMzExMTgwODUwMDI0MzczOTkiIHRpdGxlPSLogZTns7vmiJHku6wiPuiBlOezu+aIkeS7rDwvYT4gfCBkZLBE76CIkRf/r9DInwx6jV+Bwa+vORC5NsXUVxMuLlTl',
        'ctl00$Maincontent$txtBillNo': bl_num.strip(),
        'ctl00$Maincontent$btnSearch': u'查询'
    }
    response = session.post("http://www.medlog.com.cn/querydata/billquerysearch.aspx", data=login_data)

    html = etree.HTML(response.text.encode(response.encoding))

    info_html = html.xpath("//div[@id='Maincontent_divform']")

    if len(info_html) > 0:

        elem_links = info_html[0].xpath("//a")
        for elem_link in elem_links:
            elem_link.set("href", "#")

        elem_tables = info_html[0].xpath("//table")
        for elem_table in elem_tables:
            elem_table.set("style", "")

        info = etree.tostring(info_html[0], pretty_print=True)
    else:
        info = None
    session.close()

    return info


if __name__ == '__main__':
    grab()
