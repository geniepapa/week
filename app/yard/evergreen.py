import qindaoport


def grab(bl_num='TAO179960018'):
    return qindaoport.grab("crpcx.jsp", bl_num)


if __name__ == '__main__':
    grab()
