#!/usr/bin/python
#coding=utf-8

import  urllib
import xml.sax
import  urllib2
from xml.dom.minidom import parse
import xml.dom.minidom
import  re
str = '<h2 class="title">Science Bulletin(《科学通报》英文版)2015年第17期中文概要</h2>'
searcheObj = re.search(r'>.*?</',str)
print searcheObj.group()
newStr = searcheObj.group()[1:len(searcheObj.group())-2]
print newStr