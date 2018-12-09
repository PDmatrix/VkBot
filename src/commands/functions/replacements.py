import requests
import sys
from bs4 import BeautifulSoup
from src import db_context
from src.enums import Replacements


# Функция получения недели(четная или нечётная)
def get_star(day="завтра"):
    if day == "завтра":
        day = "tomorrow"
    elif day == "сегодня":
        day = "today"
    try:
        site = requests.get(
            f"https://rsp.chemk.org/4korp/{day}.htm", verify=False)
    except Exception:
        return Replacements.server_unavailable.value
    cont = site.content
    soup = BeautifulSoup(cont, 'html.parser')
    lun = 0
    ne = False
    if len(soup.find_all("tr")) == 0:
        return Replacements.no_replacements.value

    if len(soup.find_all("tr")[0].p.text) != 49 or len(
            soup.find_all("tr")[0].p.text) != 46:
        for i in range(0, len(soup.find_all("tr"))):
            if len(soup.find_all("tr")[i].p.text) == 49 or len(
                    soup.find_all("tr")[i].p.text) == 46:
                lun = i
                ne = True
                break
        if ne is False:
            return Replacements.something_wrong.value
    mpa = dict.fromkeys(range(32))
    star = soup.find_all("tr")[2 + lun].text.translate(mpa).find("**")
    if star == -1:
        star = 1
    else:
        star = 2
    return star


def get_change(group="пр1-15", day="завтра"):
    if day == "завтра":
        day = "tomorrow"
    elif day == "сегодня":
        day = "today"
    try:
        site = requests.get(
            f"https://rsp.chemk.org/4korp/{day}.htm", verify=False)
    except Exception:
        return Replacements.server_unavailable.value
    cont = site.content
    soup = BeautifulSoup(cont, 'html.parser')
    lines = soup.find_all("tr")
    if len(lines) == 0:
        return Replacements.not_ready.value
    lun = 0
    ne = False
    mpa = dict.fromkeys(range(32))
    try:
        check = len(lines[0].p.text.translate(mpa).replace(' ', ''))
    except Exception:
        check = len(lines[0].h1.text.translate(mpa).replace(' ', ''))
    if check != 41:
        for i in range(0, len(lines)):
            check = len(lines[i].p.text.translate(mpa).replace(' ', ''))
            if check == 41:
                lun = i
                ne = True
                break
        if ne is False:
            return Replacements.something_wrong.value

    for i in range(5 + lun, len(lines)):
        strs = lines[i].find_all("p")
        if not strs:
            continue
        ans = ""
        rem = ""
        ans2 = ""
        try:
            if strs[0].text.lower() == group.lower():
                for k in range(i, len(lines)):
                    leave_loop = False
                    strs = lines[k].find_all("p")
                    if not strs:
                        break
                    for j in range(0, len(strs)):
                        if strs[j].text.lower() == group.lower():
                            continue
                        elif strs[j].text.lower().title(
                        ) in db_context.get_groups():
                            leave_loop = True
                            break
                        if strs[j].text == "1 п/г":
                            rem = strs[j + 1].text
                        ans += strs[j].text + ";"
                        if strs[j].text == "2 п/г":
                            if rem != "":
                                ans += rem + ";"
                            else:
                                ans + strs[j + 1].text
                    if leave_loop is True:
                        break
                    if ans[0] == u'\xa0' and ans[2] == u'\xa0' \
                            and ans[4] == u'\xa0':
                        break
                    if ans[0] == u'\xa0':
                        ans = ans[2:]
                    if ans[0] == u'\xa0':
                        ans = ans[2:]
                    mpa = dict.fromkeys(range(32))
                    fin = ans.translate(mpa).split(";")
                    ans = ""
                    if len(fin) == 2:
                        ans2 += fin[0]
                    elif len(fin) == 3:
                        if fin[0] == "1 п/г" or fin[0] == "2 п/г":
                            ans2 += fin[1] + " пара: " + fin[0] + " - \n"
                            continue
                        ans2 += fin[0] + " пара: " + fin[1] + "\n"
                        continue
                    elif len(fin) == 4:
                        ans2 += fin[1] + " пара: " + fin[0] + " " + fin[
                            2] + "\n"
                        continue
                    elif fin[0] == "1 п/г" or fin[0] == "2 п/г" \
                            or fin[0] == "(1/2)":
                        ans2 += fin[1] + " пара: " + fin[0] + " " + \
                                fin[2] + ". " + fin[3] + " " + fin[4] + "\n"
                    else:
                        ans2 += fin[0] + " пара: " + fin[1] + ". " + \
                                fin[2] + " " + fin[3] + "\n"
                if lines[1].p.text[0].isdigit() is False:
                    return lines[2].p.text.translate(mpa) + "\n" + ans2
                return lines[1].p.text.translate(mpa) + "\n" + ans2
        except Exception as e:
            print(e, file=sys.stderr)
            return Replacements.something_wrong.value
    if ans2 == "":
        return Replacements.no_replacements.value
