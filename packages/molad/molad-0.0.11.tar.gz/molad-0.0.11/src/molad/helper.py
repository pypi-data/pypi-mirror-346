import datetime
import math
import hdate
from hdate import Location
import hdate.htables
import hdate.converters

class Molad:
    def __init__(self, day, hours, minutes, am_or_pm, chalakim, friendly):
        self.day = day
        self.hours = hours
        self.minutes = minutes
        self.am_or_pm = am_or_pm
        self.chalakim = chalakim
        self.friendly = friendly

class RoshChodesh:
    def __init__(self, month, text, days, gdays=None):
        self.month = month
        self.text = text
        self.days = days
        self.gdays = gdays

class MoladDetails:
    def __init__(self, molad: Molad, is_shabbos_mevorchim : bool, is_upcoming_shabbos_mevorchim : bool, rosh_chodesh: RoshChodesh):
        self.molad = molad
        self.is_shabbos_mevorchim = is_shabbos_mevorchim
        self.is_upcoming_shabbos_mevorchim = is_upcoming_shabbos_mevorchim
        self.rosh_chodesh = rosh_chodesh

class MoladHelper:

    config = None

    def __init__(self, config):
        self.config = config

    def sumup(self, multipliers) -> Molad:
        shifts = [
            [2, 5, 204],  # starting point
            [2, 16, 595],  # 19-year cycle
            [4, 8, 876],  # regular year
            [5, 21, 589],  # leap year
            [1, 12, 793],  # month
        ]
        mults = []
        mults.append(multipliers)
        out00 = self.multiply_matrix(mults, shifts)  # --> 1x3 triplet
        out0 = out00[0]
        out1 = self.carry_and_reduce(out0)  # now need to reduce by carrying
        out2 = self.convert_to_english(out1)  # convert to English date/time
        return out2

    def multiply_matrix(self, matrix1, matrix2):
        res = [[0 for x in range(5)] for y in range(5)]

        for i in range(len(matrix1)):
            for j in range(len(matrix2[0])):
                for k in range(len(matrix2)):

                    # resulted matrix
                    res[i][j] += matrix1[i][k] * matrix2[k][j]

        return res

    def carry_and_reduce(
        self, out0
    ):  # carry properly triple for the molad calculations
        # 7 days/week, 24 hours/day, 1080 chalakim/hours/day
        # we don't have to worry about the weeks.
        xx = out0[2]
        yy = xx % 1080
        zz = math.floor(xx / 1080)
        # chalakim
        if yy < 0:
            yy = yy + 1080
            z = zz - 1
            # carry up

        out1 = [0, 0, 0]
        out1[2] = yy
        xx = out0[1] + zz
        yy = xx % 24
        zz = math.floor(xx / 24)
        # hours
        if yy < 0:
            yy = yy + 24
            zz = zz - 1

        out1[1] = yy
        xx = out0[0] + zz
        yy = (xx + 6) % 7 + 1
        zz = math.floor(xx / 7)
        # days removing weeks - keep Shabbos=7
        if yy < 0:
            yy = yy + 7
        out1[0] = yy
        return out1

    def convert_to_english(self, out1) -> Molad:  # convert triple to English time
        days = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Shabbos",
        ]
        day = out1[0]
        hours = out1[1]
        # hours are measured from 6 pm of the day before
        chalakim = out1[2]
        # 1080/hour, 18/minute, 3+1/3 seconds
        hours = hours - 6
        if hours < 0:
            day = day - 1
            hours = hours + 24
            # evening of previous day

        daynm = days[day - 1]
        pm = "am"

        if hours >= 12:
            pm = "pm"
            hours = hours - 12

        minutes = math.floor(chalakim / 18)
        chalakim = chalakim % 18
        # left over
        leng = len(str(minutes))
        filler = "0" if (leng == 1) else ""
        # like the 0 in 3:01
        hours = 12 if (hours == 0) else hours

        friendly = (
            str(daynm)
            + ", "
            + str(hours)
            + ":"
            + str(filler)
            + str(minutes)
            + " "
            + str(pm)
            + " and "
            + str(chalakim)
            + " chalakim"
        )

        return Molad(
            day = daynm,
            hours = hours,
            minutes = minutes,
            am_or_pm = pm,
            chalakim =  chalakim,
            friendly = friendly,
        )

    def get_actual_molad(self, date) -> Molad:  # load this year into multipliers
        d = self.get_next_numeric_month_year(date)
        year = d["year"]
        month = d["month"]

        guachadazat = [3, 6, 8, 11, 14, 17, 19]
        cycles = math.floor(year / 19)  # 19-year cycles
        yrs = year % 19  # leftover years
        isleap = yrs in guachadazat  # is this year a leap year?

        # Move Adar back into middle of year for leap years
        if isleap:
            if month == 13:
                month = 6
            elif month == 14:
                month = 7
            elif month > 6:
                month = month + 1

        regular = 0
        leap = 0

        for ii in range(yrs - 1):  # for years _prior_ to this one
            if (ii + 1) in guachadazat:
                leap = leap + 1
            else:
                regular = regular + 1

        # okay, set various multiplies
        multipliers = []
        multipliers.append(1)
        multipliers.append(cycles)
        multipliers.append(regular)
        multipliers.append(leap)
        multipliers.append(
            month - 1
        )  # for the beginning of the month, so Tishrei is 0, etc.

        return self.sumup(multipliers)

    def get_numeric_month_year(self, date):
        j = hdate.converters.gdate_to_jdn(date)
        h = hdate.converters.jdn_to_hdate(j)
        m = hdate.htables.Months(h.month).value

        return {
            "year": h.year,
            "month": m,
        }

    def get_next_numeric_month_year(self, date):
        d = self.get_numeric_month_year(date)
        year = d["year"]
        month = d["month"] 

        # Tishrei = 12 
        if month == 12:
            month = 1
            year = year + 1
        # Adar II = 14, Next Month is Nissan = 7
        if month == 14:
            month = 7
        else:
            month = month + 1

        return {"year": year, "month": month}

    def get_gdate(self, numeric_date, day):
        hebrew_date = hdate.HebrewDate(numeric_date["year"], numeric_date["month"], day)
        jdn_date = hdate.converters.hdate_to_jdn(hebrew_date)
        gdate = hdate.converters.jdn_to_gdate(jdn_date)

        return gdate;

    def get_day_of_week(self, gdate):
        weekday = gdate.strftime("%A")

        if weekday == "Saturday":
            weekday = "Shabbos"

        return weekday

    def get_rosh_chodesh_days(self, date) -> RoshChodesh:
        this_month = self.get_numeric_month_year(date)
        next_month = self.get_next_numeric_month_year(date)

        next_month_name = hdate.htables.MONTHS[next_month["month"] - 1][False]

        # no Rosh Chodesh Tishrei
        if next_month["month"] == 1:
            return RoshChodesh(
                month = next_month_name,
                text = "",
                days = [],
                gdays = [],
            )

        gdate_first = self.get_gdate(this_month, 30)
        gdate_gsecond = self.get_gdate(next_month, 1)

        first = self.get_day_of_week(gdate_first)
        second = self.get_day_of_week(gdate_gsecond)


        if first == second:
            return RoshChodesh(
                month = next_month_name,
                text = first,
                days = [first],
                gdays = [gdate_first],
            )
        else:
            return RoshChodesh(
                month = next_month_name,
                text = first + " & " + second,
                days = [first, second],
                gdays = [gdate_first, gdate_gsecond],
            )

    def get_shabbos_mevorchim_english_date(self, date):
        this_month = self.get_numeric_month_year(date)
        gdate = self.get_gdate(this_month, 30)

        idx = (gdate.weekday() + 1) % 7
        sat_date = gdate - datetime.timedelta(7+idx-6)

        return sat_date
    
    def get_shabbos_mevorchim_hebrew_day_of_month(self, date):
        gdate = self.get_shabbos_mevorchim_english_date(date)
        j = hdate.converters.gdate_to_jdn(gdate)
        h = hdate.converters.jdn_to_hdate(j)
        return h.day
    
    def is_shabbos_mevorchim(self, date) -> bool:
        loc = self.get_current_location()
        j = hdate.converters.gdate_to_jdn(date)
        h = hdate.converters.jdn_to_hdate(j)
        hd = h.day
        z = hdate.Zmanim(date=date, location=loc, hebrew=False)

        if (z.time > z.zmanim["sunset"]):
            hd += 1

        sm = self.get_shabbos_mevorchim_hebrew_day_of_month(date)
        
        return (
            self.is_actual_shabbat(z)
            and hd == sm
            and h.month != hdate.htables.Months.ELUL
        )
    
    def is_upcoming_shabbos_mevorchim(self, date) -> bool:
        weekday_sunday_as_zero = (date.weekday() + 1) % 7
        upcoming_saturday =  date - datetime.timedelta(days=weekday_sunday_as_zero) + datetime.timedelta(days=6)
        upcoming_saturday_at_midnight = datetime.datetime.combine(upcoming_saturday, datetime.datetime.min.time())

        return self.is_shabbos_mevorchim(upcoming_saturday_at_midnight)

    def is_actual_shabbat(self, z) -> bool:
        today = hdate.HDate(gdate=z.date, diaspora=z.location.diaspora)
        tomorrow = hdate.HDate(
            gdate=z.date + datetime.timedelta(days=1), diaspora=z.location.diaspora
        )

        if (today.is_shabbat) and (z.havdalah != None) and (z.time < z.havdalah):
            return True
        if (tomorrow.is_shabbat) and (z.candle_lighting != None) and (z.time >= z.candle_lighting):
            return True

        return False

    def get_current_location(self) -> Location:
        return Location(
            latitude=self.config.latitude,
            longitude=self.config.longitude,
            timezone=self.config.time_zone,
            diaspora=True,
        )

    def get_molad(self, date) -> MoladDetails:
        molad = self.get_actual_molad(date)
        is_shabbos_mevorchim = self.is_shabbos_mevorchim(date)
        is_upcoming_shabbos_mevorchim = self.is_upcoming_shabbos_mevorchim(date)
        rosh_chodesh = self.get_rosh_chodesh_days(date)

        return MoladDetails(molad, is_shabbos_mevorchim, is_upcoming_shabbos_mevorchim, rosh_chodesh)