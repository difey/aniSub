from bs4 import BeautifulSoup
import requests

def magnetExtract(banGuMiNum, targetSub, filter_=''):
    baseUrl = "https://mikanani.me/Home/Bangumi"
    r = requests.get(baseUrl+"/"+banGuMiNum)
    html = r.text
    soup = BeautifulSoup(html,features="html.parser")
    central_container = soup.find_all("div", class_="central-container")[0]
    subs = central_container.find_all("div", class_="subgroup-text")
    tables = central_container.find_all("table")
    targetTable = None
    for (sub,table) in zip(subs,tables):
        print(sub.a.text)
        if sub.a.text == targetSub:
            targetTable = table
            break
    if not targetTable:
        return
    mags = []
    for tr in targetTable.tbody.find_all('tr'):
        title = tr.find_all('a',class_='magnet-link-wrap')[0].text
        if filter_ != '' and filter_ not in title:
            continue
        mag = tr.find_all('a',class_="js-magnet magnet-link")[0]['data-clipboard-text']
        mags.append(mag)
    return mags

mags = magnetExtract('2320','Lilith-Raws')
for l in mags:
    print(l)
