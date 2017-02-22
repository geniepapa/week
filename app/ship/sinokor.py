import requests
from lxml import etree

session_url = "http://www.sinokor.co.kr/contents/main/main.asp?language=ZH"
content_url = "http://eservice.sinokor.co.kr/ASPNETService/COM/CP_TrackingInquiry.aspx"


def grab(bl_num='SNKO020170202406'):

    session = requests.session()
    session.get(session_url)

    data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': '/wEPDwUIMzE1MTIzNzcPFgIeD1RyYWNraW5nSW5xdWlyeTLHEwABAAAA/////wEAAAAAAAAADAIAAABOU3lzdGVtLkRhdGEsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5BQEAAAAVU3lzdGVtLkRhdGEuRGF0YVRhYmxlAwAAABlEYXRhVGFibGUuUmVtb3RpbmdWZXJzaW9uCVhtbFNjaGVtYQtYbWxEaWZmR3JhbQMBAQ5TeXN0ZW0uVmVyc2lvbgIAAAAJAwAAAAYEAAAAngw8P3htbCB2ZXJzaW9uPSIxLjAiIGVuY29kaW5nPSJ1dGYtMTYiPz4NCjx4czpzY2hlbWEgeG1sbnM9IiIgeG1sbnM6eHM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvWE1MU2NoZW1hIiB4bWxuczptc2RhdGE9InVybjpzY2hlbWFzLW1pY3Jvc29mdC1jb206eG1sLW1zZGF0YSI+DQogIDx4czplbGVtZW50IG5hbWU9IlRhYmxlMSI+DQogICAgPHhzOmNvbXBsZXhUeXBlPg0KICAgICAgPHhzOnNlcXVlbmNlPg0KICAgICAgICA8eHM6ZWxlbWVudCBuYW1lPSJCS0NOVE5PIiB0eXBlPSJ4czpzdHJpbmciIG1zZGF0YTp0YXJnZXROYW1lc3BhY2U9IiIgbWluT2NjdXJzPSIwIiAvPg0KICAgICAgICA8eHM6ZWxlbWVudCBuYW1lPSJCS05PIiB0eXBlPSJ4czpzdHJpbmciIG1zZGF0YTp0YXJnZXROYW1lc3BhY2U9IiIgbWluT2NjdXJzPSIwIiAvPg0KICAgICAgICA8eHM6ZWxlbWVudCBuYW1lPSJDTlRSIiB0eXBlPSJ4czpzdHJpbmciIG1zZGF0YTp0YXJnZXROYW1lc3BhY2U9IiIgbWluT2NjdXJzPSIwIiAvPg0KICAgICAgICA8eHM6ZWxlbWVudCBuYW1lPSJUUFNaIiB0eXBlPSJ4czpzdHJpbmciIG1zZGF0YTp0YXJnZXROYW1lc3BhY2U9IiIgbWluT2NjdXJzPSIwIiAvPg0KICAgICAgICA8eHM6ZWxlbWVudCBuYW1lPSJDT0NTT0MiIHR5cGU9InhzOnN0cmluZyIgbXNkYXRhOnRhcmdldE5hbWVzcGFjZT0iIiBtaW5PY2N1cnM9IjAiIC8+DQogICAgICAgIDx4czplbGVtZW50IG5hbWU9IlBPTCIgdHlwZT0ieHM6c3RyaW5nIiBtc2RhdGE6dGFyZ2V0TmFtZXNwYWNlPSIiIG1pbk9jY3Vycz0iMCIgLz4NCiAgICAgICAgPHhzOmVsZW1lbnQgbmFtZT0iRVREIiB0eXBlPSJ4czpzdHJpbmciIG1zZGF0YTp0YXJnZXROYW1lc3BhY2U9IiIgbWluT2NjdXJzPSIwIiAvPg0KICAgICAgICA8eHM6ZWxlbWVudCBuYW1lPSJQT0QiIHR5cGU9InhzOnN0cmluZyIgbXNkYXRhOnRhcmdldE5hbWVzcGFjZT0iIiBtaW5PY2N1cnM9IjAiIC8+DQogICAgICAgIDx4czplbGVtZW50IG5hbWU9IkVUQSIgdHlwZT0ieHM6c3RyaW5nIiBtc2RhdGE6dGFyZ2V0TmFtZXNwYWNlPSIiIG1pbk9jY3Vycz0iMCIgLz4NCiAgICAgICAgPHhzOmVsZW1lbnQgbmFtZT0iVlNMIiB0eXBlPSJ4czpzdHJpbmciIG1zZGF0YTp0YXJnZXROYW1lc3BhY2U9IiIgbWluT2NjdXJzPSIwIiAvPg0KICAgICAgICA8eHM6ZWxlbWVudCBuYW1lPSJWWUciIHR5cGU9InhzOnN0cmluZyIgbXNkYXRhOnRhcmdldE5hbWVzcGFjZT0iIiBtaW5PY2N1cnM9IjAiIC8+DQogICAgICA8L3hzOnNlcXVlbmNlPg0KICAgIDwveHM6Y29tcGxleFR5cGU+DQogIDwveHM6ZWxlbWVudD4NCiAgPHhzOmVsZW1lbnQgbmFtZT0idG1wRGF0YVNldCIgbXNkYXRhOklzRGF0YVNldD0idHJ1ZSIgbXNkYXRhOk1haW5EYXRhVGFibGU9IlRhYmxlMSIgbXNkYXRhOlVzZUN1cnJlbnRMb2NhbGU9InRydWUiPg0KICAgIDx4czpjb21wbGV4VHlwZT4NCiAgICAgIDx4czpjaG9pY2UgbWluT2NjdXJzPSIwIiBtYXhPY2N1cnM9InVuYm91bmRlZCIgLz4NCiAgICA8L3hzOmNvbXBsZXhUeXBlPg0KICA8L3hzOmVsZW1lbnQ+DQo8L3hzOnNjaGVtYT4GBQAAAPwEPGRpZmZncjpkaWZmZ3JhbSB4bWxuczptc2RhdGE9InVybjpzY2hlbWFzLW1pY3Jvc29mdC1jb206eG1sLW1zZGF0YSIgeG1sbnM6ZGlmZmdyPSJ1cm46c2NoZW1hcy1taWNyb3NvZnQtY29tOnhtbC1kaWZmZ3JhbS12MSI+DQogIDx0bXBEYXRhU2V0Pg0KICAgIDxUYWJsZTEgZGlmZmdyOmlkPSJUYWJsZTExIiBtc2RhdGE6cm93T3JkZXI9IjAiIGRpZmZncjpoYXNDaGFuZ2VzPSJpbnNlcnRlZCI+DQogICAgICA8QktDTlROTz5TTktPMDIwMTcwMjAyNDA2VEdIVTMxMjA2NjY8L0JLQ05UTk8+DQogICAgICA8QktOTz5TTktPMDIwMTcwMjAyNDA2PC9CS05PPg0KICAgICAgPENOVFI+VEdIVTMxMjA2NjY8L0NOVFI+DQogICAgICA8VFBTWj4yMCcgRFJZPC9UUFNaPg0KICAgICAgPENPQ1NPQz5DT0M8L0NPQ1NPQz4NCiAgICAgIDxQT0w+U0hBTkdIQUksIENISU5BPC9QT0w+DQogICAgICA8RVREPjIwMTctMDItMjE8L0VURD4NCiAgICAgIDxQT0Q+Vk9TVE9DSE5ZLCBSVVNTSUE8L1BPRD4NCiAgICAgIDxFVEE+MjAxNy0wMi0yODwvRVRBPg0KICAgICAgPFZTTD5DQVJQQVRISUE8L1ZTTD4NCiAgICAgIDxWWUc+MDAzMU48L1ZZRz4NCiAgICA8L1RhYmxlMT4NCiAgPC90bXBEYXRhU2V0Pg0KPC9kaWZmZ3I6ZGlmZmdyYW0+BAMAAAAOU3lzdGVtLlZlcnNpb24EAAAABl9NYWpvcgZfTWlub3IGX0J1aWxkCV9SZXZpc2lvbgAAAAAICAgIAgAAAAAAAAD//////////wsWAgIDD2QWEAIFDw8WAh4EVGV4dAUWQ2FyZ28gVHJhY2tpbmcgSW5xdWlyeWRkAgkPDxYCHwEFByBPcHRpb25kZAIPDw8WAh8BBQUgWWVhcmRkAhEPEGQPFghmAgECAgIDAgQCBQIGAgcWCBAFBDIwMTcFBDIwMTdnEAUEMjAxNgUEMjAxNmcQBQQyMDE1BQQyMDE1ZxAFBDIwMTQFBDIwMTRnEAUEMjAxMwUEMjAxM2cQBQQyMDEyBQQyMDEyZxAFBDIwMTEFBDIwMTFnEAUEMjAxMAUEMjAxMGdkZAITDw9kFgIeBXN0eWxlBQ1kaXNwbGF5Om5vbmU7ZAIVDw9kFgIfAgUOZGlzcGxheTpibG9jaztkAhcPPCsABgEADxYCHwEFCCBJbnF1aXJ5ZGQCGw9kFgJmD2QWAgIBDw9kFgIfAgUOZGlzcGxheTpibG9jazsWAgIBDzwrABwCAA8WAh4PRGF0YVNvdXJjZUJvdW5kZ2QYPCsABgEFFCsAAmRkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBQUEcmRiMQUEcmRiMgUKYnRuSW5xdWlyeQUER3JpZAUIYnRuRXhjZWyJgEOC+WIJLeExrnlAhDN1gbdrMnMa8K3TWRSk8WUwCw==',
        '__VIEWSTATEGENERATOR': '4F4F22BD',
        'txtViewNacd': 'CN',
        'rdbInquiry': '1',
        'ddlYear': '2017',
        'txtCntrNo': '',
        'txtBlNo': bl_num,
        'Grid$DXSelInput': '',
        'Grid$DXKVInput': '[\'SNKO020170202406TGHU3120666\']',
        'Grid$CallbackState': 'BwMHAgIERGF0YQZjAQAAAAABAAAAAQAAAAAAAAABAAAAAAsAAAAHQktDTlROTwdCS0NOVE5PBwAAAQRCS05PBEJLTk8HAAABBENOVFIEQ05UUgcAAAEEVFBTWgRUUFNaBwAAAQZDT0NTT0MGQ09DU09DBwAAAQNQT0wDUE9MBwAAAQNFVEQDRVREBwAAAQNQT0QDUE9EBwAAAQNFVEEDRVRBBwAAAQNWU0wDVlNMBwAAAQNWWUcDVllHBwAAAQAAAAAHAAcABwAHAAb//wcCG1NOS08wMjAxNzAyMDI0MDZUR0hVMzEyMDY2NgcCEFNOS08wMjAxNzAyMDI0MDYHAgtUR0hVMzEyMDY2NgcCBzIwJyBEUlkHAgNDT0MHAg9TSEFOR0hBSSwgQ0hJTkEHAgoyMDE3LTAyLTIxBwIRVk9TVE9DSE5ZLCBSVVNTSUEHAgoyMDE3LTAyLTI4BwIJQ0FSUEFUSElBBwIFMDAzMU4CBVN0YXRlB4oHCwb//wIABwECAQcCAgEHAwIBBwQCAQcFAgEHBgIBBwcCAQcIAgEHCQIBBwoCAQcABwAHAAcAAgAHAAcCG1NOS08wMjAxNzAyMDI0MDZUR0hVMzEyMDY2NgIHQktDTlROTwcBAgdCS0NOVE5PBwkCAAIAAwcEAgAHAAIBBwEHAAIAAgEHAAcABwACCFBhZ2VTaXplAwcF',
        'Grid$DXFocusedRowInput': '0',
        'XScript': '1_187,1_101,1_180,1_121,1_162,1_120,1_154,1_130,1_137,1_169,1_98,1_172,1_100',
        'DXCss': '0_103,1_16,1_8,0_105,0_277,0_110,0_273,0_112,1_14,../DynamicStyles.ashx?file=main.css,../Include/Site.css',
        '__CALLBACKID': 'callbackPanel',
        '__CALLBACKPARAM': 'c0:SNKO020170202406TGHU3120666',
        '__EVENTVALIDATION': '/wEdABHmf3KAI+/vXNfD0LLlXl5ui1mkKITlHUhei7t72dHRI3Kp2B5oQ3U/J4D3VbpuEpkSylk9zDCM+b/Yd3OAoisI+UjHaziFq4A2Apshbtkkaqh+ll8bPCT3wuR0TgExGp9vS79CQa5ggWUtrK6PFC5GijsW4PLs1cHXhq+r9va/t3aFOlnZ8BT9A1zy9XasZBgHGaMsr8bAr7t9J86+pu1fJYCUlgaG+w5vBo1YFua/SeKZ19D/tmy2bwXzh/7eH1iHU8HDoDJVT1J2K/eQI4+AZoJ728kr5pbEJVspi8yBvUu+NP098XiccL4mJPmakBswCu/VKNCmPgJV51T6HJtqn45UI7MT1acbfZgSyJ+k4bl+ZMkloZ0b7OurKSNZRH6TsnuS+T6rUqJ2VxUnB0DW'
    }


    response = session.post(content_url, data=data)

    print(response.text)


    return html_parse(response)


routes_xpath = "//body/table[3]/tr/td/table[1]/tr"
routes_extend_xpath = "///body/table[3]/tr/td/table[2]/tr"
container_xpath = "//body/table[3]/tr/td/table[3]/tr"


def html_parse(response):

    routes_doc, containers_doc = get_docs(response.text)
    return {'routing': get_routes(routes_doc), 'containers': get_containers(containers_doc)}


def get_docs(content):

    doc = etree.HTML(unicode.encode(content, encoding='utf-8'))
    containers_doc = doc.xpath(container_xpath)
    routes_doc = doc.xpath(routes_xpath)

    routes_extend_doc = doc.xpath(routes_extend_xpath)
    routes_doc[0].extend([
        routes_extend_doc[2].find("td[2]"),
        routes_extend_doc[3].find("td[2]"),
        routes_extend_doc[5].find("td[4]")])

    return routes_doc, containers_doc


def get_routes(routes_doc):

    routes = []
    for index, route in enumerate(routes_doc):
        if index > -1:
            route_td = route.getchildren()
            vessel_part1, vessel_part2, voyage = route_td[4].text.strip().split(" ")[:3]
            routes.append({
                'route_name': 'Load Port',
                'location': route_td[5].text.strip(),
                'vessel': "{0} {1}".format(vessel_part1, vessel_part2),
                'voyage': voyage.strip(),
                'call_sign': '',
                'estimate_arrival_date': route_td[7].text.strip(),
                'actual_arrival_date': '',
                'container_load_date': route_td[7].text.strip(),
                'container_discharge_date': '',
                'estimate_departure_date': '',
                'actual_departure_date': ''
            })
            routes.append({
                'route_name': 'Discharge Port',
                'location': route_td[6].text.strip(),
                'vessel': "{0} {1}".format(vessel_part1, vessel_part2),
                'voyage': voyage.strip(),
                'call_sign': '',
                'estimate_arrival_date': '',
                'actual_arrival_date': '',
                'container_load_date': '',
                'container_discharge_date': '',
                'estimate_departure_date': 'unknown',
                'actual_departure_date': ''
            })
    return routes


def get_containers(containers_doc):
    containers = []
    for index, container in enumerate(containers_doc):
        if index > 1:
            container_td = container.getchildren()
            containers.append({
                'number': container_td[0].find("a").text.strip(),
                'seal_no': container_td[2].text.strip(),
                'status': container_td[7].text.strip(),
                'type': container_td[1].find("span").text[4:6],
                'size': container_td[1].find("span").text[:2],
                'height': '',
                'location': '',
                'container_load_date': '',
                'container_discharge_date': container_td[8].text
            })
    return containers


if __name__ == '__main__':
    grab()

