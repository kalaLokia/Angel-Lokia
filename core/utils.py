import datetime
import re


def calc24hr(hour, period):
    """Converts given hour to 24hr format"""
    if not hour:
        return None
    hour = int(hour)
    if period == "pm" and hour <= 12:
        hour = 0 if hour == 12 else hour + 12
    if hour > 23:
        hour = 8
    return hour


def calcWeekday(date, weekday):
    """Returns previous weekday datetime of the date."""

    dif = weekday - date.weekday()
    if dif > 0:
        return date - datetime.timedelta(days=7 - dif)
    if dif == 0:
        return date - datetime.timedelta(days=7)
    else:
        dif *= -1
        return date - datetime.timedelta(days=dif)


def chooseDay(day: str):
    """Returns datetime from given day string"""
    today = datetime.datetime.today().replace(hour=8, minute=0, second=0, microsecond=0)

    return {
        "today": today,
        "yesterday": (today - datetime.timedelta(days=1)),
        "tomorrow": (today + datetime.timedelta(days=1)),
        "monday": calcWeekday(today, 0),
        "tuesday": calcWeekday(today, 1),
        "wednesday": calcWeekday(today, 2),
        "thursday": calcWeekday(today, 3),
        "friday": calcWeekday(today, 4),
        "saturday": calcWeekday(today, 5),
        "sunday": calcWeekday(today, 6),
    }.get(day, today)


def chooseMonth(month: str):
    """Returns a date with given month (current or past)."""

    thismonth = datetime.datetime.today().replace(
        day=1, hour=8, minute=0, second=0, microsecond=0
    )
    date = None

    if month in ("thismonth", "curmonth", "currentmonth"):
        date = thismonth
    elif month in ("lastmonth", "previousmonth"):
        date = (thismonth - datetime.timedelta(days=1)).replace(day=1)
    else:
        try:
            date = datetime.datetime.strptime(
                f"{thismonth.year} {month[:3]} 1 8 0 0", "%Y %b %d %H %M %S"
            )
            if date > thismonth:
                date = date.replace(year=date.year - 1)
        except:
            date = thismonth

    return date


def changeDatesDay(date: datetime.datetime, day_num):
    try:
        date = date.replace(day=int(day_num))
    except ValueError:
        # day number out of range
        date = (date.replace(day=28) + datetime.timedelta(days=10)).replace(day=1)
        # ToDo: May be change to same month last day instead, check scope
    except TypeError:
        # day_num is None.
        date = date.replace(day=1, hour=8)
    return date


def datesFromRegex(regex_order, match):
    groups = match.groups()
    first_date, last_date = (None, None)

    if regex_order == 0:
        first_date = chooseDay(groups[0])
        hour = calc24hr(*groups[2:4])  # sh
        hour2 = calc24hr(*groups[6:8])  # eh

        if hour:
            first_date = first_date.replace(hour=hour)
        if hour2:
            last_date = first_date.replace(hour=hour2)

    elif regex_order == 1:
        first_date = chooseMonth(groups[0])  # month
        day = groups[2]  # sday
        hour = calc24hr(*groups[8:10])  # sh

        day2 = groups[6]  # eday
        hour2 = calc24hr(*groups[-2:])  # eh

        first_date = changeDatesDay(first_date, day)
        if not day:
            last_date = (
                first_date.replace(day=28) + datetime.timedelta(days=5)
            ).replace(day=1)
        else:
            if hour:
                first_date = first_date.replace(hour=hour)
            if day2:
                last_date = changeDatesDay(first_date, day2)
                if hour2:
                    last_date = last_date.replace(hour=hour2)
                else:
                    # Production timing 8 - 8 (next day)
                    last_date = (last_date + datetime.timedelta(days=1)).replace(hour=8)

    elif regex_order == 2:
        first_date = chooseMonth(groups[0])  # month
        day = groups[2]  # sday
        year = groups[3]  # year
        hour = calc24hr(*groups[10:12])  # sh

        day2 = groups[6]  # eday
        hour2 = calc24hr(*groups[-2:])  # eh

        first_date = changeDatesDay(first_date, day)
        if not day:
            last_date = (
                first_date.replace(day=28) + datetime.timedelta(days=5)
            ).replace(day=1)
        else:
            if year:
                first_date = first_date.replace(year=int(year))
            if hour:
                first_date = first_date.replace(hour=hour)

            if day2:
                last_date = changeDatesDay(first_date, day2)
                if hour2:
                    last_date = last_date.replace(hour=hour2)
                else:
                    # Production timing 8 - 8 (next day)
                    last_date = (last_date + datetime.timedelta(days=1)).replace(hour=8)

    elif regex_order == 3:
        # ('20', '12', '2021', ' 8pm', '8', 'pm')
        dd, mm, yy, _, hh, pp = match.groups()
        hh = calc24hr(hh, pp)
        if hh is None:
            hh = 8
        first_date = datetime.datetime(int(yy), int(mm), int(dd), hh, 0, 0)

    return first_date, last_date


def generateProductionDates(text: str):
    """Generate two production dates from given text and rest of text.

    Returns:
        start_date : A datetime object
        end_date   : A datetime object
        text       : Given text with production date params removed

    """
    date_junks = r"\b((on)|(from)|(and)|(between)|(bw)|(to))\b"
    regxes = (
        r"(today|yesterday|tomorrow)(\s(\d{1,2})\s?(am|pm)?(\s?(to|-)\s?(\d{1,2})\s?(am|pm)?$)?)?",
        r"(thismonth|lastmonth|previousmonth|curmonth|currentmonth)((\s\d{1,2})((\s?(to|-)\s?(\d{1,2})$)|(\s(\d{1,2})\s?(am|pm)(\s?(to|-)\s?(\d{1,2})\s?(am|pm)$)?))?)?",
        r"(january|jan|febuary|feb|march|mar|april|apr|may|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|nov|dec|december)((\s\d{1,2})(,?\s?(20\d{2}))?((\s?(to|-)\s?(\d{1,2})$)|(\s(\d{1,2})\s?(am|pm)(\s?(to|-)\s?(\d{1,2})\s?(am|pm)$)?))?)?",
        r"on (\d{1,2})[\.\-\s](\d[012])[\.\-\s](\d{4})([\s\-](\d{1,2})(am|pm))?",
    )

    text = text.replace("  ", " ").strip()  # Removing extra spaces from text
    text = re.sub("\smonth", "month", text)  # remove space before "month" for regex

    msg = ""  # For test purpose

    start_date, end_date = (None, None)

    match_order = {}

    loop = 0
    while loop < 2:  # Max two regex matches
        loop += 1
        for i, rgx in enumerate(regxes):
            match = re.search(rgx, text)
            if match:
                mstart, mend = match.span()
                match_order[mstart] = datesFromRegex(i, match)
                msg += "{0}.  {1}\n".format(loop, match.group())
                # remove the matched string from text
                text = (text[:mstart] + text[mend + 1 :]).strip()
                break

    if match_order:
        start_date, end_date = match_order[min(match_order)]

    if not start_date:
        start_date = datetime.datetime.today().replace(
            hour=8, minute=0, second=0, microsecond=0
        )
        end_date = start_date + datetime.timedelta(days=1)
    elif not end_date:
        if len(match_order) > 1:
            end_date, _ = match_order[max(match_order)]
        else:
            end_date = (start_date + datetime.timedelta(days=1)).replace(hour=8)

    if start_date > end_date:
        temp = start_date
        start_date = end_date
        end_date = temp

    msg += "```\nStart = {}\nEnd = {}\nText = {}\n```".format(
        start_date, end_date, text
    )
    text = re.sub(date_junks, "", text)
    text = re.sub("\W", " ", text)
    msg += f"\nClean Text: {text}"
    return msg
