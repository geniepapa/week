import qindaoport


def grab(bl_num='CQDJNCV6501203'):
    return qindaoport.grab("cargoDyaJzcz.jsp", bl_num)


if __name__ == '__main__':
    grab()
