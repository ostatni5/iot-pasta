#!/usr/bin/python
# -*- coding: utf-8 -*-

# inspired by IO-Link master with EtherNet/IP interface AL1322 made by ifm electronic gmbh
# https://www.ifm.com/de/en/product/AL1322




class Master:
    def __init__(self, name):
        self.name = name
        self.sensors = []
        # TODO

