import requests
from bs4 import BeautifulSoup
import discord


async def default_embed(ctx, description, color=0x110011):
    await ctx.send (embed=discord.Embed (description=description, color=color))


async def bday_embed(ctx, head, description):
    def hsv_to_rgb(h, s, v):
        def boo(r0,r1,r2):
          return (r0<<16) + (r1<<8) + r2
        if s == 0.0: v*=255; return (v, v, v)
        i = int(h*6.)
        f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
        if i == 0: return boo(v, t, p)
        if i == 1: return boo(q, v, p)
        if i == 2: return boo(p, v, t)
        if i == 3: return boo(p, q, v)
        if i == 4: return boo(t, p, v)
        if i == 5: return boo(v, p, q)
    import random
    color=hsv_to_rgb(random.random(),1,1)
    await ctx.send (embed=discord.Embed (color=color).add_field (name=head, value=description))


def searchAbi(abi):
    abi = (abi.replace (" ", "+")) + " pokemon"
    url = f"https://www.google.com/search?sxsrf=ALeKk01JKoHk2Qbzeg9XeIFY2MNDkheecg%3A1604463145764&ei=KSqiX5ufLpbAz7sPnsu4mAw&q={abi}&oq={abi}&gs_lcp=CgZwc3ktYWIQAzIECCMQJzIHCCMQyQMQJzICCAAyAggAMgIIADICCAAyAggAMgIIADIECAAQCjICCAA6BAgAEEc6CAgAEMkDEJECOgcIABAUEIcCUL6HHVj8mB1ghZwdaAJwAngAgAF6iAGaA5IBAzIuMpgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwjb1-7-gujsAhUW4HMBHZ4lDsMQ4dUDCA0&uact=5"
    page = requests.get (url)
    soup = BeautifulSoup (page.content, 'html.parser')

    query = soup.find ("span", class_="BNeawe tAd8D AP7Wnd")
    return query.text


def print_stats(lis):
    return f"HP: {lis[0]}, Atk: {lis[1]}, Def: {lis[2]}, SpAtk: {lis[3]}, SpDef: {lis[4]}, Spe: {lis[5]}"


def bubble_sort(lis, lis1, avg):
    arr = []
    for i in lis:
        arr.append (int (i))
        avg += int (i)
    avg /= 6
    n = len (arr)
    for i in range (n - 1):
        for j in range (0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                lis1[j], lis1[j + 1] = lis1[j + 1], lis1[j]
    return arr


async def get_format(bestStats):
    if "Atk" in bestStats and "Spe" in bestStats:
        return ("Fast Physical Sweeper")
    elif "SpAtk" in bestStats and "Spe" in bestStats:
        return ("Fast Special Sweeper")
    elif "SpAtk" in bestStats and "Atk" in bestStats:
        return ("Mixed Sweeper")
    elif "Atk" in bestStats and "Def" in bestStats:
        return ("Physical Tank")
    elif "SpAtk" in bestStats and "SpDef" in bestStats:
        return ("Special Tank")
    elif "SpAtk" in bestStats and "Def" in bestStats:
        return ("Special Tank Physically Defensive")
    elif "Atk" in bestStats and "SpDef" in bestStats:
        return ("Physical Tank Specially Defensive")
    elif "SpAtk" in bestStats and "HP" in bestStats:
        return ("Bulky Special Sweeper")
    elif "Atk" in bestStats and "HP" in bestStats:
        return ("Bulky Physical Sweeper")
    elif "Def" in bestStats and "SpDef" in bestStats:
        return ("Mixed Wall")
    elif "HP" in bestStats and "Def" in bestStats:
        return ("Physically Defensive Wall")
    elif "HP" in bestStats and "SpDef" in bestStats:
        return ("Specially Defensive Wall")
    elif "Spe" in bestStats and "SpDef" in bestStats:
        return ("Fast SpDef Tank")
    elif "Spe" in bestStats and "Def" in bestStats:
        return ("Fast Def Tank")
    elif "Spe" in bestStats and "HP" in bestStats:
        return ("Fast Tank")
    elif "Spe" in bestStats:
        return ("Fast Boi")
    elif "HP" in bestStats:
        return ("Bulky Boi")
    elif "Atk" in bestStats:
        return ("Physical Hit Boi")
    elif "SpAtk" in bestStats:
        return ("Special Hit Boi")
    elif "SpDef" in bestStats:
        return ("Specially Bulky Boi")
    elif "Def" in bestStats:
        return ("Physically Bulky Boi")


def search(abi):
    abi = (abi.replace (" ", "+"))
    url = f"https://www.google.com/search?sxsrf=ALeKk01JKoHk2Qbzeg9XeIFY2MNDkheecg%3A1604463145764&ei=KSqiX5ufLpbAz7sPnsu4mAw&q={abi}&oq={abi}&gs_lcp=CgZwc3ktYWIQAzIECCMQJzIHCCMQyQMQJzICCAAyAggAMgIIADICCAAyAggAMgIIADIECAAQCjICCAA6BAgAEEc6CAgAEMkDEJECOgcIABAUEIcCUL6HHVj8mB1ghZwdaAJwAngAgAF6iAGaA5IBAzIuMpgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwjb1-7-gujsAhUW4HMBHZ4lDsMQ4dUDCA0&uact=5"
    page = requests.get (url)
    soup = BeautifulSoup (page.content, 'html.parser')
    query = soup.find ("div", class_="BNeawe s3v9rd AP7Wnd")
    return query.text


def psearch(name):
    url = f"https://www.pokemon.com/us/pokedex/{name}"
    page = requests.get (url)
    soup = BeautifulSoup (page.content, 'html.parser')
    query = [
        soup.find ("p", class_="version-x active").text,
        soup.find ("p", class_="version-y").text
    ]
    return query


def song_search():
    url = "https://www.billboard.com/charts/hot-100"
    page = requests.get (url)
    soup = BeautifulSoup (page.content, 'html.parser')
    query = []
    td = soup.find_all (
        "span",
        class_="chart-element__information__song text--truncate color--primary"
    )[:10]
    ts = soup.find_all (
        "span",
        class_=
        "chart-element__information__artist text--truncate color--secondary"
    )[:10]
    for i in range (10):
        query.append (f"{i + 1}. {td[i].text} - {ts[i].text}")
    return query


def csearch():
    url = "https://www.google.com/search?q=cricket&oq=cr&aqs=chrome.0.69i59l3j69i60l5.1602j0j7&sourceid=chrome&ie=UTF-8"
    page = requests.get (url)
    soup = BeautifulSoup (page.content, 'html.parser')
    query = []
    for d in soup.find_all ("div", class_="BNeawe s3v9rd AP7Wnd lRVwie")[:3]:
        query.append (d.text)
    query.append (soup.find_all ("div", class_="BNeawe deIvCb AP7Wnd")[1].text)
    query.append (soup.find_all ("div", class_="BNeawe tAd8D AP7Wnd")[1].text)
    return query


def imgsearch(cx: str):
    cx = cx.replace (" ", "+")
    url = f"https://www.google.com/search?q={cx}&sxsrf=ALeKk00Op--bGnt2uIMs0LTmh5KVDLP3KQ:1604926865894&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjxpe29wvXsAhV3IbcAHYh8BGcQ_AUoAXoECB8QAw&biw=1366&bih=625"
    page = requests.get (url)
    soup = BeautifulSoup (page.content, 'html.parser')
    query = []
    for i in soup.find_all ("img", class_="t0fcAb"):
        query.append (i['src'])
    return query


def pun():
    url = "https://www.boredpanda.com/funny-pun-jokes/?utm_source=google&utm_medium=organic&utm_campaign=organic"
    page = requests.get (url)
    soup = BeautifulSoup (page.content, 'html.parser')
    query = []
    for i in soup.find_all ("span", class_="bordered-description"):
        query.append (i.text)
    return query


def listComp(lis1, lis2):
    for i in lis1:
        if i in lis2:
            return True
    return False


class Help:
    def __init__(self, name, help, format):
        self.name = name
        self.help = help
        self.format = format

    def brr(self):
        e = discord.Embed ()
        e.title = self.name
        e.add_field (name="Use", value=self.help)
        e.add_field (name="Format", value=f"`{self.format}`", inline=False)
        return e
