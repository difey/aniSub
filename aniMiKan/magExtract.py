#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import argparse

def magnetExtract(banGuMiNum, targetSub, filter_=''):
    baseUrl = "https://mikanani.me/Home/Bangumi"
    r = requests.get(baseUrl+"/"+banGuMiNum)
    html = r.text
    soup = BeautifulSoup(html,features="html.parser")
    central_container = soup.find_all("div", class_="central-container")[0]
    subs = central_container.find_all("div", class_="subgroup-text")
    tables = central_container.find_all("table")
    targetTable = None
    subs_ = []
    for (sub,table) in zip(subs,tables):
        subs_.append(sub.a.text)
        if sub.a.text == targetSub:
            targetTable = table
            break
    if not targetTable:
        print('没有找到指定字幕组')
        print('找到了如下字幕组：')
        for i in subs_:
            print(i)
        return []
    mags = []
    for tr in targetTable.tbody.find_all('tr'):
        title = tr.find_all('a',class_='magnet-link-wrap')[0].text
        if filter_ and filter_ != '' and (not (filter_ in title)):
            continue
        mag = tr.find_all('a',class_="js-magnet magnet-link")[0]['data-clipboard-text']
        mags.append(mag)
    return mags

parser = argparse.ArgumentParser(description="get magnets from bugumi number")
parser.add_argument('-b','--bnum',help='bangumi number')
parser.add_argument('-s','--sub',help='sub name')
parser.add_argument('-f','--filter',help='filter in title')
args = parser.parse_args()
mags = magnetExtract(args.bnum,args.sub,args.filter)
for l in mags:
    print(l)
