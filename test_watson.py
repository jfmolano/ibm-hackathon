# -*- coding: utf-8 -*-
import json
from os.path import join, dirname
from watson_developer_cloud import AlchemyLanguageV1

with open('conf.json', 'r') as f:
    try:
        conf = json.load(f)
    except ValueError:
        conf = {}

alchemy_key = conf["alchemy_key"]

alchemy_language = AlchemyLanguageV1(api_key=alchemy_key)

url = 'https://developer.ibm.com/watson/blog/2015/11/03/price-reduction-for-watson-personality-insights/'

print(json.dumps(alchemy_language.targeted_sentiment(text='Mi salud es hermosa.',
targets=['salud'], language='spanish'), indent=2))