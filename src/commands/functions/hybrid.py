from src.commands.functions import replacements
from src.commands.functions import schedule
from src.enums import Replacements


def get_hybrid(group="пр1-15", day="завтра"):
    zamen = replacements.get_change(group, day).replace(u'\xa0',
                                                        '').split('\n')
    if len(zamen) == 2:
        return zamen
    rsps = schedule.get_schedule(group, day).replace(u'\xa0', '').replace(
        u'\ufeff', '').replace(u'\r', '').split('\n')
    new_rsps = [rsps[0]]
    for i in range(1, len(rsps) - 1):
        if rsps[i].find('*') == -1:
            new_rsps.append(rsps[i])
            continue
        else:
            if rsps[i].find('**') != -1:
                if replacements.get_star(day) == 2:
                    new_rsps.append(rsps[i])
            else:
                if replacements.get_star(day) == 1:
                    new_rsps.append(rsps[i])
    rsps = new_rsps
    if zamen[0] == Replacements.not_ready.value or \
            zamen[0] == Replacements.something_wrong.value or \
            zamen[0] == Replacements.server_unavailable.value:
        return zamen[0]
    elif zamen[0] == Replacements.no_replacements.value:
        return '\n'.join(rsps)

    new_zamen = [zamen[0]]
    for i in range(1, len(zamen) - 1):
        zam_par = zamen[i][0:zamen[i].find("пара")].replace(' ', '').split(',')
        if len(zam_par) != 1:
            for j in range(0, len(zam_par)):
                new_zamen.append(zam_par[j] + ' ' +
                                 zamen[i][zamen[i].find("пара"):len(zamen[i])])
        else:
            new_zamen.append(zamen[i])
    zamen = new_zamen if len(new_zamen) > 1 else zamen
    del new_zamen
    for i in range(1, len(zamen)):
        for j in range(1, len(rsps)):
            if zamen[i][0:6] == rsps[j][0:6]:
                del rsps[j]
                break
    for i in range(1, len(zamen)):
        rsps.append(zamen[i])
    rsps = [line for line in rsps if line != '']
    temp_day = rsps[0]
    rsps = rsps[1:len(rsps)]
    rsps.sort(key=lambda x: int(x[0]))
    rsps.insert(0, temp_day)
    ans = '\n'.join(rsps[0:len(rsps)])
    return ans
