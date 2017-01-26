# coding: utf-8

import qindaoport


def grab(bl_num='QD2E467045'):
    return qindaoport.grab("cargoDyaGlr.jsp", bl_num.strip())

if __name__ == '__main__':
    grab()
