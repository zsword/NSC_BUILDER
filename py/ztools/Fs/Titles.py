#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import re
import time
import json
import operator
import Print

global titles
titles = None

class Title:
	def __init__(self):
		self.key = None
		self.id = None
		
	def setId(self, id):
		self.id = id.upper()

global nsuIdMap
nsuIdMap = {}

global regionTitles
regionTitles = {}

def data(region = None, language = None):
	global regionTitles
	global titles

	if region:
		if not region in regionTitles:
			regionTitles[region] = {}

		if not language in regionTitles[region]:
			regionTitles[region][language] = {}

		return regionTitles[region][language]

	if titles is None:
		titles = {}
	return titles

def items(region = None, language = None):
	if region:
		return regionTitles[region][language].items()

	global titles
	if titles is None:
		titles = {}
	return titles.items()

def get(key, region = None, language = None):
	key = key.upper()

	if not key in data(region, language):
		t = Title()
		t.setId(key)
		data(region, language)[key] = t
	return data(region, language)[key]
	
def contains(key, region = None):
	global titles
	if titles is None:
		titles = {}
	return key in titles

def erase(id):
	id = id.upper()
	del titles[id]
	
def set(key, value):
	titles[key] = value
	
	
def keys(region = None, language = None):
	global titles
	if region:
		return regionTitles[region][language].keys()
	if titles is None:
		titles = {}
	return titles.keys()


