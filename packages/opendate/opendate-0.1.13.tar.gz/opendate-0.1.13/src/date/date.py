import calendar
import contextlib
import datetime as _datetime
import logging
import os
import re
import time
import warnings
import zoneinfo as _zoneinfo
from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from functools import lru_cache, partial, wraps
from typing import Self

import dateutil as _dateutil
import numpy as np
import pandas as pd
import pandas_market_calendars as mcal
import pendulum as _pendulum

warnings.simplefilter(action='ignore', category=DeprecationWarning)

logger = logging.getLogger(__name__)

__all__ = [
    'Date',
    'DateTime',
    'Interval',
    'IntervalError',
    'Time',
    'Timezone',
    'EST',
    'UTC',
    'GMT',
    'LCL',
    'expect_native_timezone',
    'expect_utc_timezone',
    'prefer_native_timezone',
    'prefer_utc_timezone',
    'expect_date',
    'expect_datetime',
    'Entity',
    'NYSE'
    'WEEKDAY_SHORTNAME',
    ]


def Timezone(name:str = 'US/Eastern') -> _zoneinfo.ZoneInfo:
    """Create a timezone object with the specified name.

    Simple wrapper around Pendulum's Timezone function that ensures
    consistent timezone handling across the library.

    Parameters
        name: Timezone name (e.g., 'US/Eastern', 'UTC')

    Returns
        A timezone object for the specified timezone

    Examples

    US/Eastern is equivalent to America/New_York:
    >>> winter1 = DateTime(2000, 1, 1, 12, tzinfo=Timezone('US/Eastern'))
    >>> winter2 = DateTime(2000, 1, 1, 12, tzinfo=Timezone('America/New_York'))
    >>> winter1 == winter2
    True

    This works in both summer and winter:
    >>> summer1 = DateTime(2000, 7, 1, 12, tzinfo=Timezone('US/Eastern'))
    >>> summer2 = DateTime(2000, 7, 1, 12, tzinfo=Timezone('America/New_York'))
    >>> summer1 == summer2
    True
    """
    return _pendulum.tz.Timezone(name)


UTC = Timezone('UTC')
GMT = Timezone('GMT')
EST = Timezone('US/Eastern')
LCL = _pendulum.tz.Timezone(_pendulum.tz.get_local_timezone().name)

WeekDay = _pendulum.day.WeekDay

WEEKDAY_SHORTNAME = {
    'MO': WeekDay.MONDAY,
    'TU': WeekDay.TUESDAY,
    'WE': WeekDay.WEDNESDAY,
    'TH': WeekDay.THURSDAY,
    'FR': WeekDay.FRIDAY,
    'SA': WeekDay.SATURDAY,
    'SU': WeekDay.SUNDAY
}


MONTH_SHORTNAME = {
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'oct': 10,
    'nov': 11,
    'dec': 12,
}

DATEMATCH = re.compile(r'^(?P<d>N|T|Y|P|M)(?P<n>[-+]?\d+)?(?P<b>b?)?$')


# def caller_entity(func):
    # """Helper to get current entity from function"""
    # # general frame args inspect
    # import inspect
    # frame = inspect.currentframe()
    # outer_frames = inspect.getouterframes(frame)
    # caller_frame = outer_frames[1][0]
    # args = inspect.getargvalues(caller_frame)
    # # find our entity
    # param = inspect.signature(func).parameters.get('entity')
    # default = param.default if param else NYSE
    # entity = args.locals['kwargs'].get('entity', default)
    # return entity


def isdateish(x):
    return isinstance(x, _datetime.date | _datetime.datetime | pd.Timestamp | np.datetime64)


def parse_arg(typ, arg):
    if isdateish(arg):
        if typ == _datetime.datetime:
            return DateTime.instance(arg)
        if typ == _datetime.date:
            return Date.instance(arg)
        if typ == _datetime.time:
            return Time.instance(arg)
    return arg


def parse_args(typ, *args):
    this = []
    for a in args:
        if isinstance(a, Sequence) and not isinstance(a, str):
            this.append(parse_args(typ, *a))
        else:
            this.append(parse_arg(typ, a))
    return this


def expect(func, typ: type[_datetime.date], exclkw: bool = False) -> Callable:
    """Decorator to force input type of date/datetime inputs
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        args = parse_args(typ, *args)
        if not exclkw:
            for k, v in kwargs.items():
                if isdateish(v):
                    if typ == _datetime.datetime:
                        kwargs[k] = DateTime.instance(v)
                        continue
                    if typ == _datetime.date:
                        kwargs[k] = Date.instance(v)
        return func(*args, **kwargs)
    return wrapper


expect_date = partial(expect, typ=_datetime.date)
expect_datetime = partial(expect, typ=_datetime.datetime)
expect_time = partial(expect, typ=_datetime.time)


def type_class(typ, obj):
    if isinstance(typ, str):
        if typ == 'Date':
            return Date
        if typ == 'DateTime':
            return DateTime
        if typ == 'Interval':
            return Interval
    if typ:
        return typ
    if obj.__class__ in {_pendulum.Interval, Interval}:
        return Interval
    if obj.__class__ in {_datetime.datetime, _pendulum.DateTime, DateTime}:
        return DateTime
    if obj.__class__ in {_datetime.date, _pendulum.Date, Date}:
        return Date
    raise ValueError(f'Unknown type {typ}')


def store_entity(func=None, *, typ=None):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        _entity = self._entity
        d = type_class(typ, self).instance(func(self, *args, **kwargs))
        d._entity = _entity
        return d
    if func is None:
        return partial(store_entity, typ=typ)
    return wrapper


def store_both(func=None, *, typ=None):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        _entity = self._entity
        _business = self._business
        d = type_class(typ, self).instance(func(self, *args, **kwargs))
        d._entity = _entity
        d._business = _business
        return d
    if func is None:
        return partial(store_both, typ=typ)
    return wrapper


def prefer_utc_timezone(func, force:bool = False):
    """Return datetime as UTC.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        d = func(*args, **kwargs)
        if not d:
            return
        if not force and d.tzinfo:
            return d
        return d.replace(tzinfo=UTC)
    return wrapper


def prefer_native_timezone(func, force:bool = False):
    """Return datetime as native.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        d = func(*args, **kwargs)
        if not d:
            return
        if not force and d.tzinfo:
            return d
        return d.replace(tzinfo=LCL)
    return wrapper


expect_native_timezone = partial(prefer_native_timezone, force=True)
expect_utc_timezone = partial(prefer_utc_timezone, force=True)


class Entity(ABC):
    """Abstract base class for calendar entities with business day definitions.

    This class defines the interface for calendar entities that provide
    business day information, such as market open/close times and holidays.
    Not available in pendulum.

    Concrete implementations (like NYSE) provide specific calendar rules
    for different business contexts.
    """

    tz = UTC

    @staticmethod
    @abstractmethod
    def business_days(begdate: _datetime.date, enddate: _datetime.date):
        """Returns all business days over a range"""

    @staticmethod
    @abstractmethod
    def business_hours(begdate: _datetime.date, enddate: _datetime.date):
        """Returns all business open and close times over a range"""

    @staticmethod
    @abstractmethod
    def business_holidays(begdate: _datetime.date, enddate: _datetime.date):
        """Returns only holidays over a range"""


class NYSE(Entity):
    """New York Stock Exchange calendar entity.

    Provides business day definitions, market hours, and holidays
    according to the NYSE trading calendar. Uses pandas_market_calendars
    for the underlying implementation.

    This entity is used as the default for business day calculations
    throughout the library.
    """

    BEGDATE = _datetime.date(1900, 1, 1)
    ENDDATE = _datetime.date(2200, 1, 1)
    calendar = mcal.get_calendar('NYSE')

    tz = EST

    @staticmethod
    @lru_cache
    def business_days(begdate=BEGDATE, enddate=ENDDATE) -> set:
        return {Date.instance(d.date())
                for d in NYSE.calendar.valid_days(begdate, enddate)}

    @staticmethod
    @lru_cache
    def business_hours(begdate=BEGDATE, enddate=ENDDATE) -> dict:
        df = NYSE.calendar.schedule(begdate, enddate, tz=EST)
        open_close = [(DateTime.instance(o.to_pydatetime()),
                       DateTime.instance(c.to_pydatetime()))
                      for o, c in zip(df.market_open, df.market_close)]
        return dict(zip(df.index.date, open_close))

    @staticmethod
    @lru_cache
    def business_holidays(begdate=BEGDATE, enddate=ENDDATE) -> set:
        return {Date.instance(d.date())
                for d in map(pd.to_datetime, NYSE.calendar.holidays().holidays)
                if begdate <= d <= enddate}


class DateBusinessMixin:
    """Mixin class providing business day functionality.

    This mixin adds business day awareness to Date and DateTime classes,
    allowing date operations to account for weekends and holidays according
    to a specified calendar entity.

    Features not available in pendulum:
    - Business day mode toggle
    - Entity-specific calendar rules
    - Business-aware date arithmetic
    """

    _entity: type[NYSE] = NYSE
    _business: bool = False

    def business(self) -> Self:
        """Switch to business day mode for date calculations.

        In business day mode, date arithmetic only counts business days
        as defined by the associated entity (default NYSE).

        Returns
            Self instance for method chaining
        """
        self._business = True
        return self

    @property
    def b(self) -> Self:
        """Shorthand property for business() method.

        Returns
            Self instance for method chaining
        """
        return self.business()

    def entity(self, entity: type[NYSE] = NYSE) -> Self:
        """Set the calendar entity for business day calculations.

        Parameters
            entity: Calendar entity class (defaults to NYSE)

        Returns
            Self instance for method chaining
        """
        self._entity = entity
        return self

    @store_entity
    def add(self, years: int = 0, months: int = 0, weeks: int = 0, days: int = 0, **kwargs) -> Self:
        """Add time periods to the current date or datetime.

        Extends pendulum's add method with business day awareness. When in business mode,
        only counts business days for the 'days' parameter.

        Parameters
            years: Number of years to add
            months: Number of months to add
            weeks: Number of weeks to add
            days: Number of days to add (business days if in business mode)
            **kwargs: Additional time units to add

        Returns
            New instance with added time
        """
        _business = self._business
        self._business = False
        if _business:
            if days == 0:
                return self._business_or_next()
            if days < 0:
                return self.business().subtract(days=abs(days))
            while days > 0:
                self = self._business_next(days=1)
                days -= 1
            return self
        return super().add(years, months, weeks, days, **kwargs)

    @store_entity
    def subtract(self, years: int = 0, months: int = 0, weeks: int = 0, days: int = 0, **kwargs) -> Self:
        """Subtract wrapper
        If not business use Pendulum
        If business assume only days (for now) and use local logic
        """
        _business = self._business
        self._business = False
        if _business:
            if days == 0:
                return self._business_or_previous()
            if days < 0:
                return self.business().add(days=abs(days))
            while days > 0:
                self = self._business_previous(days=1)
                days -= 1
            return self
        kwargs = {k: -1*v for k,v in kwargs.items()}
        return super().add(-years, -months, -weeks, -days, **kwargs)

    @store_entity
    def first_of(self, unit: str, day_of_week: WeekDay | None = None) -> Self:
        """Returns an instance set to the first occurrence
        of a given day of the week in the current unit.
        """
        _business = self._business
        self._business = False
        self = super().first_of(unit, day_of_week)
        if _business:
            self = self._business_or_next()
        return self

    @store_entity
    def last_of(self, unit: str, day_of_week: WeekDay | None = None) -> Self:
        """Returns an instance set to the last occurrence
        of a given day of the week in the current unit.
        """
        _business = self._business
        self._business = False
        self = super().last_of(unit, day_of_week)
        if _business:
            self = self._business_or_previous()
        return self

    @store_entity
    def start_of(self, unit: str) -> Self:
        """Returns a copy of the instance with the time reset
        """
        _business = self._business
        self._business = False
        self = super().start_of(unit)
        if _business:
            self = self._business_or_next()
        return self

    @store_entity
    def end_of(self, unit: str) -> Self:
        """Returns a copy of the instance with the time reset
        """
        _business = self._business
        self._business = False
        self = super().end_of(unit)
        if _business:
            self = self._business_or_previous()
        return self

    @store_entity
    def previous(self, day_of_week: WeekDay | None = None) -> Self:
        """Modify to the previous occurrence of a given day of the week.
        """
        _business = self._business
        self._business = False
        self = super().previous(day_of_week)
        if _business:
            self = self._business_or_next()
        return self

    @store_entity
    def next(self, day_of_week: WeekDay | None = None) -> Self:
        """Modify to the next occurrence of a given day of the week.
        """
        _business = self._business
        self._business = False
        self = super().next(day_of_week)
        if _business:
            self = self._business_or_previous()
        return self

    @expect_date
    def business_open(self) -> bool:
        """Business open

        >>> thedate = Date(2021, 4, 19) # Monday
        >>> thedate.business_open()
        True
        >>> thedate = Date(2021, 4, 17) # Saturday
        >>> thedate.business_open()
        False
        >>> thedate = Date(2021, 1, 18) # MLK Day
        >>> thedate.business_open()
        False
        """
        return self.is_business_day()

    @expect_date
    def is_business_day(self) -> bool:
        """Is business date.

        >>> thedate = Date(2021, 4, 19) # Monday
        >>> thedate.is_business_day()
        True
        >>> thedate = Date(2021, 4, 17) # Saturday
        >>> thedate.is_business_day()
        False
        >>> thedate = Date(2021, 1, 18) # MLK Day
        >>> thedate.is_business_day()
        False
        >>> thedate = Date(2021, 11, 25) # Thanksgiving
        >>> thedate.is_business_day()
        False
        >>> thedate = Date(2021, 11, 26) # Day after ^
        >>> thedate.is_business_day()
        True
        """
        return self in self._entity.business_days()

    @expect_date
    def business_hours(self) -> 'tuple[DateTime, DateTime]':
        """Business hours

        Returns (None, None) if not a business day

        >>> thedate = Date(2023, 1, 5)
        >>> thedate.business_hours()
        (... 9, 30, ... 16, 0, ...)

        >>> thedate = Date(2023, 7, 3)
        >>> thedate.business_hours()
        (... 9, 30, ... 13, 0, ...)

        >>> thedate = Date(2023, 11, 24)
        >>> thedate.business_hours()
        (... 9, 30, ... 13, 0, ...)

        >>> thedate = Date(2024, 5, 27) # memorial day
        >>> thedate.business_hours()
        (None, None)
        """
        return self._entity.business_hours(self, self)\
            .get(self, (None, None))

    @store_both
    def _business_next(self, days=0):
        """Helper for cycling through N business day"""
        days = abs(days)
        while days > 0:
            try:
                self = super().add(days=1)
            except OverflowError:
                break
            if self.is_business_day():
                days -= 1
        return self

    @store_both
    def _business_previous(self, days=0):
        """Helper for cycling through N business day"""
        days = abs(days)
        while days > 0:
            try:
                self = super().add(days=-1)
            except OverflowError:
                break
            if self.is_business_day():
                days -= 1
        return self

    @store_entity
    def _business_or_next(self):
        self._business = False
        self = super().subtract(days=1)
        self = self._business_next(days=1)
        return self

    @store_entity
    def _business_or_previous(self):
        self._business = False
        self = super().add(days=1)
        self = self._business_previous(days=1)
        return self


class DateExtrasMixin:
    """Extended date functionality not provided by Pendulum.

    This mixin provides additional date utilities primarily focused on:
    - Financial date calculations (nearest month start/end)
    - Weekday-oriented date navigation
    - Relative date lookups

    These methods extend Pendulum's functionality with features commonly
    needed in financial applications and reporting scenarios.
    """

    def nearest_start_of_month(self):
        """Get `nearest` start of month

        1/1/2015 -> Thursday (New Year's Day)
        2/1/2015 -> Sunday

        >>> from date import Date
        >>> Date(2015, 1, 1).nearest_start_of_month()
        Date(2015, 1, 1)
        >>> Date(2015, 1, 15).nearest_start_of_month()
        Date(2015, 1, 1)
        >>> Date(2015, 1, 15).b.nearest_start_of_month()
        Date(2015, 1, 2)
        >>> Date(2015, 1, 16).nearest_start_of_month()
        Date(2015, 2, 1)
        >>> Date(2015, 1, 31).nearest_start_of_month()
        Date(2015, 2, 1)
        >>> Date(2015, 1, 31).b.nearest_start_of_month()
        Date(2015, 2, 2)
        """
        _business = self._business
        self._business = False
        if self.day > 15:
            d = self.end_of('month')
            if _business:
                return d.business().add(days=1)
            return d.add(days=1)
        d = self.start_of('month')
        if _business:
            return d.business().add(days=1)
        return d

    def nearest_end_of_month(self):
        """Get `nearest` end of month

        12/31/2014 -> Wednesday
        1/31/2015 -> Saturday

        >>> from date import Date
        >>> Date(2015, 1, 1).nearest_end_of_month()
        Date(2014, 12, 31)
        >>> Date(2015, 1, 15).nearest_end_of_month()
        Date(2014, 12, 31)
        >>> Date(2015, 1, 15).b.nearest_end_of_month()
        Date(2014, 12, 31)
        >>> Date(2015, 1, 16).nearest_end_of_month()
        Date(2015, 1, 31)
        >>> Date(2015, 1, 31).nearest_end_of_month()
        Date(2015, 1, 31)
        >>> Date(2015, 1, 31).b.nearest_end_of_month()
        Date(2015, 1, 30)
        """
        _business = self._business
        self._business = False
        if self.day <= 15:
            d = self.start_of('month')
            if _business:
                return d.business().subtract(days=1)
            return d.subtract(days=1)
        d = self.end_of('month')
        if _business:
            return d.business().subtract(days=1)
        return d

    def next_relative_date_of_week_by_day(self, day='MO'):
        """Get next relative day of week by relativedelta code

        >>> from date import Date
        >>> Date(2020, 5, 18).next_relative_date_of_week_by_day('SU')
        Date(2020, 5, 24)
        >>> Date(2020, 5, 24).next_relative_date_of_week_by_day('SU')
        Date(2020, 5, 24)
        """
        if self.weekday() == WEEKDAY_SHORTNAME.get(day):
            return self
        return self.next(WEEKDAY_SHORTNAME.get(day))

    def weekday_or_previous_friday(self):
        """Return the date if it is a weekday, else previous Friday

        >>> from date import Date
        >>> Date(2019, 10, 6).weekday_or_previous_friday() # Sunday
        Date(2019, 10, 4)
        >>> Date(2019, 10, 5).weekday_or_previous_friday() # Saturday
        Date(2019, 10, 4)
        >>> Date(2019, 10, 4).weekday_or_previous_friday() # Friday
        Date(2019, 10, 4)
        >>> Date(2019, 10, 3).weekday_or_previous_friday() # Thursday
        Date(2019, 10, 3)
        """
        dnum = self.weekday()
        if dnum in {WeekDay.SATURDAY, WeekDay.SUNDAY}:
            return self.subtract(days=dnum - 4)
        return self

    """
    create a simple nth weekday function that accounts for
    [1,2,3,4] and weekday as options
    or weekday, [1,2,3,4]

    """

    @classmethod
    def third_wednesday(cls, year, month):
        """Calculate the date of the third Wednesday in a given month/year.

        Parameters
            year: The year to use
            month: The month to use (1-12)

        Returns
            A Date object representing the third Wednesday of the specified month
        """
        third = cls(year, month, 15)  # lowest 3rd day
        w = third.weekday()
        if w != WeekDay.WEDNESDAY:
            third = third.replace(day=(15 + (WeekDay.WEDNESDAY - w) % 7))
        return third


class Date(DateExtrasMixin, DateBusinessMixin, _pendulum.Date):
    """Date class extending pendulum.Date with business day and additional functionality.

    This class inherits all pendulum.Date functionality while adding:
    - Business day calculations with NYSE calendar integration
    - Additional date navigation methods
    - Enhanced parsing capabilities
    - Custom financial date utilities

    Unlike pendulum.Date, methods that create new instances return Date objects
    that preserve business status and entity association when chained.
    """

    def to_string(self, fmt: str) -> str:
        """Format cleaner https://stackoverflow.com/a/2073189.

        >>> Date(2022, 1, 5).to_string('%-m/%-d/%Y')
        '1/5/2022'
        """
        return self.strftime(fmt.replace('%-', '%#') if os.name == 'nt' else fmt)

    @store_entity(typ='Date')
    def replace(self, *args, **kwargs):
        """Replace method that preserves entity and business status.
        """
        return _pendulum.Date.replace(self, *args, **kwargs)

    @store_entity(typ='Date')
    def closest(self, *args, **kwargs):
        """Closest method that preserves entity and business status.
        """
        return _pendulum.Date.closest(self, *args, **kwargs)

    @store_entity(typ='Date')
    def farthest(self, *args, **kwargs):
        """Farthest method that preserves entity and business status.
        """
        return _pendulum.Date.farthest(self, *args, **kwargs)

    @store_entity(typ='Date')
    def average(self, dt=None):
        """Modify the current instance to the average
        of a given instance (default now) and the current instance.

        Parameters
            dt: The date to average with (defaults to today)

        Returns
            A new Date object representing the average date
        """
        return _pendulum.Date.average(self)

    @classmethod
    def fromordinal(cls, *args, **kwargs):
        """Create a Date from an ordinal.

        Parameters
            n: The ordinal value

        Returns
            Date instance
        """
        result = _pendulum.Date.fromordinal(*args, **kwargs)
        return cls.instance(result)

    @classmethod
    def fromtimestamp(cls, timestamp, tz=None):
        """Create a Date from a timestamp.

        Parameters
            timestamp: Unix timestamp
            tz: Optional timezone (defaults to UTC)

        Returns
            Date instance
        """
        # Ensure timezone is always applied to get consistent results
        tz = tz or UTC
        dt = _datetime.datetime.fromtimestamp(timestamp, tz=tz)
        return cls(dt.year, dt.month, dt.day)

    @store_entity(typ='Date')
    def nth_of(self, unit: str, nth: int, day_of_week: WeekDay) -> Self:
        """Returns a new instance set to the given occurrence
        of a given day of the week in the current unit.

        Parameters
            unit: The unit to use ("month", "quarter", or "year")
            nth: The position of the day in the unit (1 to 5)
            day_of_week: The day of the week (pendulum.MONDAY to pendulum.SUNDAY)

        Returns
            A new Date object for the nth occurrence

        Raises
            ValueError: If the occurrence can't be found
        """
        return _pendulum.Date.nth_of(self, unit, nth, day_of_week)

    @classmethod
    def parse(
        cls,
        s: str | None,
        fmt: str = None,
        entity: Entity = NYSE,
        raise_err: bool = False,
    ) -> Self | None:
        """Convert a string to a date handling many different formats.

        creating a new Date object
        >>> Date.parse('2022/1/1')
        Date(2022, 1, 1)

        previous business day accessed with 'P'
        >>> Date.parse('P')==Date.today().b.subtract(days=1)
        True
        >>> Date.parse('T-3b')==Date.today().b.subtract(days=3)
        True
        >>> Date.parse('T-3b')==Date.today().b.add(days=-3)
        True
        >>> Date.parse('T+3b')==Date.today().b.subtract(days=-3)
        True
        >>> Date.parse('T+3b')==Date.today().b.add(days=3)
        True
        >>> Date.parse('M')==Date.today().start_of('month').subtract(days=1)
        True

        m[/-]d[/-]yyyy  6-23-2006
        >>> Date.parse('6-23-2006')
        Date(2006, 6, 23)

        m[/-]d[/-]yy    6/23/06
        >>> Date.parse('6/23/06')
        Date(2006, 6, 23)

        m[/-]d          6/23
        >>> Date.parse('6/23') == Date(Date.today().year, 6, 23)
        True

        yyyy-mm-dd      2006-6-23
        >>> Date.parse('2006-6-23')
        Date(2006, 6, 23)

        yyyymmdd        20060623
        >>> Date.parse('20060623')
        Date(2006, 6, 23)

        dd-mon-yyyy     23-JUN-2006
        >>> Date.parse('23-JUN-2006')
        Date(2006, 6, 23)

        mon-dd-yyyy     JUN-23-2006
        >>> Date.parse('20 Jan 2009')
        Date(2009, 1, 20)

        month dd, yyyy  June 23, 2006
        >>> Date.parse('June 23, 2006')
        Date(2006, 6, 23)

        dd-mon-yy
        >>> Date.parse('23-May-12')
        Date(2012, 5, 23)

        ddmonyyyy
        >>> Date.parse('23May2012')
        Date(2012, 5, 23)

        >>> Date.parse('Oct. 24, 2007', fmt='%b. %d, %Y')
        Date(2007, 10, 24)

        >>> Date.parse('Yesterday') == DateTime.now().subtract(days=1).date()
        True
        >>> Date.parse('TODAY') == Date.today()
        True
        >>> Date.parse('Jan. 13, 2014')
        Date(2014, 1, 13)

        >>> Date.parse('March') == Date(Date.today().year, 3, Date.today().day)
        True

        only raise error when we explicitly say so
        >>> Date.parse('bad date') is None
        True
        >>> Date.parse('bad date', raise_err=True)
        Traceback (most recent call last):
        ...
        ValueError: Failed to parse date: bad date
        """

        def date_for_symbol(s):
            if s == 'N':
                return cls.today()
            if s == 'T':
                return cls.today()
            if s == 'Y':
                return cls.today().subtract(days=1)
            if s == 'P':
                return cls.today().entity(entity).business().subtract(days=1)
            if s == 'M':
                return cls.today().start_of('month').subtract(days=1)

        def year(m):
            try:
                yy = int(m.group('y'))
                if yy < 100:
                    yy += 2000
            except IndexError:
                logger.debug('Using default this year')
                yy = cls.today().year
            return yy

        if not s:
            if raise_err:
                raise ValueError('Empty value')
            return

        if not isinstance(s, str):
            raise TypeError(f'Invalid type for date parse: {s.__class__}')

        if fmt:
            try:
                return cls(*time.strptime(s, fmt)[:3])
            except:
                if raise_err:
                    raise ValueError(f'Unable to parse {s} using fmt {fmt}')
                return

        with contextlib.suppress(ValueError):
            if float(s) and len(s) != 8:  # 20000101
                if raise_err:
                    raise ValueError('Invalid date: %s', s)
                return

        # special shortcode symbolic values: T, Y-2, P-1b
        if m := DATEMATCH.match(s):
            d = date_for_symbol(m.groupdict().get('d'))
            n = m.groupdict().get('n')
            if not n:
                return d
            n = int(n)
            b = m.groupdict().get('b')
            if b:
                assert b == 'b'
                d = d.entity(entity).business().add(days=n)
            else:
                d = d.add(days=n)
            return d
        if 'today' in s.lower():
            return cls.today()
        if 'yester' in s.lower():
            return cls.today().subtract(days=1)

        with contextlib.suppress(TypeError, ValueError):
            return cls.instance(_dateutil.parser.parse(s))

        # Regex with Month Numbers
        exps = (
            r'^(?P<m>\d{1,2})[/-](?P<d>\d{1,2})[/-](?P<y>\d{4})$',
            r'^(?P<m>\d{1,2})[/-](?P<d>\d{1,2})[/-](?P<y>\d{1,2})$',
            r'^(?P<m>\d{1,2})[/-](?P<d>\d{1,2})$',
            r'^(?P<y>\d{4})-(?P<m>\d{1,2})-(?P<d>\d{1,2})$',
            r'^(?P<y>\d{4})(?P<m>\d{2})(?P<d>\d{2})$',
        )
        for exp in exps:
            if m := re.match(exp, s):
                mm = int(m.group('m'))
                dd = int(m.group('d'))
                yy = year(m)
                return cls(yy, mm, dd)

        # Regex with Month Name
        exps = (
            r'^(?P<d>\d{1,2})[- ](?P<m>[A-Za-z]{3,})[- ](?P<y>\d{4})$',
            r'^(?P<m>[A-Za-z]{3,})[- ](?P<d>\d{1,2})[- ](?P<y>\d{4})$',
            r'^(?P<m>[A-Za-z]{3,}) (?P<d>\d{1,2}), (?P<y>\d{4})$',
            r'^(?P<d>\d{2})(?P<m>[A-Z][a-z]{2})(?P<y>\d{4})$',
            r'^(?P<d>\d{1,2})-(?P<m>[A-Z][a-z][a-z])-(?P<y>\d{2})$',
            r'^(?P<d>\d{1,2})-(?P<m>[A-Z]{3})-(?P<y>\d{2})$',
        )
        for exp in exps:
            if m := re.match(exp, s):
                try:
                    mm = MONTH_SHORTNAME[m.group('m').lower()[:3]]
                except KeyError:
                    logger.debug('Month name did not match MONTH_SHORTNAME')
                    continue
                dd = int(m.group('d'))
                yy = year(m)
                return cls(yy, mm, dd)

        if raise_err:
            raise ValueError('Failed to parse date: %s', s)

    @classmethod
    def instance(
        cls,
        obj: _datetime.date
        | _datetime.datetime
        | _datetime.time
        | pd.Timestamp
        | np.datetime64
        | Self
        | None,
        raise_err: bool = False,
    ) -> Self | None:
        """From datetime.date like object

        >>> Date.instance(_datetime.date(2022, 1, 1))
        Date(2022, 1, 1)
        >>> Date.instance(Date(2022, 1, 1))
        Date(2022, 1, 1)
        >>> Date.instance(_pendulum.Date(2022, 1, 1))
        Date(2022, 1, 1)
        >>> Date.instance(Date(2022, 1, 1))
        Date(2022, 1, 1)
        >>> Date.instance(np.datetime64('2000-01', 'D'))
        Date(2000, 1, 1)
        >>> Date.instance(None)

        """
        if pd.isna(obj):
            if raise_err:
                raise ValueError('Empty value')
            return

        if obj.__class__ == cls:
            return obj

        if isinstance(obj, np.datetime64 | pd.Timestamp):
            obj = DateTime.instance(obj)

        return cls(obj.year, obj.month, obj.day)

    @classmethod
    def today(cls):
        d = _datetime.datetime.now(LCL)
        return cls(d.year, d.month, d.day)

    def isoweek(self):
        """Week number 1-52 following ISO week-numbering

        Standard weeks
        >>> Date(2023, 1, 2).isoweek()
        1
        >>> Date(2023, 4, 27).isoweek()
        17
        >>> Date(2023, 12, 31).isoweek()
        52

        Belongs to week of previous year
        >>> Date(2023, 1, 1).isoweek()
        52
        """
        with contextlib.suppress(Exception):
            return self.isocalendar()[1]

    def lookback(self, unit='last') -> Self:
        """Date back based on lookback string, ie last, week, month.

        >>> Date(2018, 12, 7).b.lookback('last')
        Date(2018, 12, 6)
        >>> Date(2018, 12, 7).b.lookback('day')
        Date(2018, 12, 6)
        >>> Date(2018, 12, 7).b.lookback('week')
        Date(2018, 11, 30)
        >>> Date(2018, 12, 7).b.lookback('month')
        Date(2018, 11, 7)
        """
        def _lookback(years=0, months=0, weeks=0, days=0):
            _business = self._business
            self._business = False
            d = self\
                .subtract(years=years, months=months, weeks=weeks, days=days)
            if _business:
                return d._business_or_previous()
            return d

        return {
            'day': _lookback(days=1),
            'last': _lookback(days=1),
            'week': _lookback(weeks=1),
            'month': _lookback(months=1),
            'quarter': _lookback(months=3),
            'year': _lookback(years=1),
            }.get(unit)


class Time(_pendulum.Time):
    """Time class extending pendulum.Time with additional functionality.

    This class inherits all pendulum.Time functionality while adding:
    - Enhanced parsing for various time formats
    - Default UTC timezone when created
    - Simple timezone conversion utilities

    Unlike pendulum.Time, this class has more lenient parsing capabilities
    and different timezone defaults.
    """

    @classmethod
    @prefer_utc_timezone
    def parse(cls, s: str | None, fmt: str | None = None, raise_err: bool = False) -> Self | None:
        """Convert a string to a time handling many formats::

            handle many time formats:
            hh[:.]mm
            hh[:.]mm am/pm
            hh[:.]mm[:.]ss
            hh[:.]mm[:.]ss[.,]uuu am/pm
            hhmmss[.,]uuu
            hhmmss[.,]uuu am/pm

        >>> Time.parse('9:30')
        Time(9, 30, 0, tzinfo=Timezone('UTC'))
        >>> Time.parse('9:30:15')
        Time(9, 30, 15, tzinfo=Timezone('UTC'))
        >>> Time.parse('9:30:15.751')
        Time(9, 30, 15, 751000, tzinfo=Timezone('UTC'))
        >>> Time.parse('9:30 AM')
        Time(9, 30, 0, tzinfo=Timezone('UTC'))
        >>> Time.parse('9:30 pm')
        Time(21, 30, 0, tzinfo=Timezone('UTC'))
        >>> Time.parse('9:30:15.751 PM')
        Time(21, 30, 15, 751000, tzinfo=Timezone('UTC'))
        >>> Time.parse('0930')  # Date treats this as a date, careful!!
        Time(9, 30, 0, tzinfo=Timezone('UTC'))
        >>> Time.parse('093015')
        Time(9, 30, 15, tzinfo=Timezone('UTC'))
        >>> Time.parse('093015,751')
        Time(9, 30, 15, 751000, tzinfo=Timezone('UTC'))
        >>> Time.parse('0930 pm')
        Time(21, 30, 0, tzinfo=Timezone('UTC'))
        >>> Time.parse('093015,751 PM')
        Time(21, 30, 15, 751000, tzinfo=Timezone('UTC'))
        """

        def seconds(m):
            try:
                return int(m.group('s'))
            except Exception:
                return 0

        def micros(m):
            try:
                return int(m.group('u'))
            except Exception:
                return 0

        def is_pm(m):
            try:
                return m.group('ap').lower() == 'pm'
            except Exception:
                return False

        if not s:
            if raise_err:
                raise ValueError('Empty value')
            return

        if not isinstance(s, str):
            raise TypeError(f'Invalid type for time parse: {s.__class__}')

        if fmt:
            try:
                return cls(*time.strptime(s, fmt)[3:6])
            except:
                if raise_err:
                    raise ValueError(f'Unable to parse {s} using fmt {fmt}')
                return

        exps = (
            r'^(?P<h>\d{1,2})[:.](?P<m>\d{2})([:.](?P<s>\d{2})([.,](?P<u>\d+))?)?( +(?P<ap>[aApP][mM]))?$',
            r'^(?P<h>\d{2})(?P<m>\d{2})((?P<s>\d{2})([.,](?P<u>\d+))?)?( +(?P<ap>[aApP][mM]))?$',
        )

        for exp in exps:
            if m := re.match(exp, s):
                hh = int(m.group('h'))
                mm = int(m.group('m'))
                ss = seconds(m)
                uu = micros(m)
                if is_pm(m) and hh < 12:
                    hh += 12
                return cls(hh, mm, ss, uu * 1000)

        with contextlib.suppress(TypeError, ValueError):
            return cls.instance(_dateutil.parser.parse(s))

        if raise_err:
            raise ValueError('Failed to parse time: %s', s)

    @classmethod
    def instance(
        cls,
        obj: _datetime.time
        | _datetime.datetime
        | pd.Timestamp
        | np.datetime64
        | Self
        | None,
        tz: str | _zoneinfo.ZoneInfo | _datetime.tzinfo | None = None,
        raise_err: bool = False,
    ) -> Self | None:
        """From datetime-like object

        >>> Time.instance(_datetime.time(12, 30, 1))
        Time(12, 30, 1, tzinfo=Timezone('UTC'))
        >>> Time.instance(_pendulum.Time(12, 30, 1))
        Time(12, 30, 1, tzinfo=Timezone('UTC'))
        >>> Time.instance(None)

        like Pendulum, do not add timzone if no timezone and Time object
        >>> Time.instance(Time(12, 30, 1))
        Time(12, 30, 1)

        """
        if pd.isna(obj):
            if raise_err:
                raise ValueError('Empty value')
            return

        if obj.__class__ == cls and not tz:
            return obj

        tz = tz or obj.tzinfo or UTC

        return cls(obj.hour, obj.minute, obj.second, obj.microsecond, tzinfo=tz)

    def in_timezone(self, tz: str | _zoneinfo.ZoneInfo | _datetime.tzinfo):
        """Convert timezone

        >>> Time(12, 0).in_timezone(Timezone('America/Sao_Paulo'))
        Time(9, 0, 0, tzinfo=Timezone('America/Sao_Paulo'))

        >>> Time(12, 0, tzinfo=Timezone('Europe/Moscow')).in_timezone(Timezone('America/Sao_Paulo'))
        Time(6, 0, 0, tzinfo=Timezone('America/Sao_Paulo'))

        """
        _dt = DateTime.combine(Date.today(), self, tzinfo=self.tzinfo or UTC)
        return _dt.in_timezone(tz).time()

    in_tz = in_timezone


class DateTime(DateBusinessMixin, _pendulum.DateTime):
    """DateTime class extending pendulum.DateTime with business day and additional functionality.

    This class inherits all pendulum.DateTime functionality while adding:
    - Business day calculations with NYSE calendar integration
    - Enhanced timezone handling
    - Extended parsing capabilities
    - Custom utility methods for financial applications

    Unlike pendulum.DateTime:
    - today() returns start of day rather than current time
    - Methods preserve business status and entity when chaining
    - Has timezone handling helpers not present in pendulum
    """

    def epoch(self):
        """Translate a datetime object into unix seconds since epoch
        """
        return self.timestamp()

    @store_entity(typ='DateTime')
    def astimezone(self, *args, **kwargs):
        """Convert to a timezone-aware datetime in a different timezone.
        """
        return _pendulum.DateTime.astimezone(self, *args, **kwargs)

    @store_entity(typ='DateTime')
    def in_timezone(self, *args, **kwargs):
        """Convert to a timezone-aware datetime in a different timezone.
        """
        return _pendulum.DateTime.in_timezone(self, *args, **kwargs)

    @store_entity(typ='DateTime')
    def in_tz(self, *args, **kwargs):
        """Convert to a timezone-aware datetime in a different timezone.
        """
        return _pendulum.DateTime.in_tz(self, *args, **kwargs)

    @store_entity(typ='DateTime')
    def replace(self, *args, **kwargs):
        """Replace method that preserves entity and business status.
        """
        return _pendulum.DateTime.replace(self, *args, **kwargs)

    @classmethod
    def fromordinal(cls, *args, **kwargs):
        """Create a DateTime from an ordinal.

        Parameters
            n: The ordinal value

        Returns
            DateTime instance
        """
        result = _pendulum.DateTime.fromordinal(*args, **kwargs)
        return cls.instance(result)

    @classmethod
    def fromtimestamp(cls, timestamp, tz=None):
        """Create a DateTime from a timestamp.

        Parameters
            timestamp: Unix timestamp
            tz: Optional timezone

        Returns
            DateTime instance
        """
        tz = tz or UTC
        result = _pendulum.DateTime.fromtimestamp(timestamp, tz)
        return cls.instance(result)

    @classmethod
    def strptime(cls, time_str, fmt):
        """Parse a string into a DateTime according to a format.

        Parameters
            time_str: String to parse
            fmt: Format string

        Returns
            DateTime instance
        """
        result = _pendulum.DateTime.strptime(time_str, fmt)
        return cls.instance(result)

    @classmethod
    def utcfromtimestamp(cls, timestamp):
        """Create a UTC DateTime from a timestamp.

        Parameters
            timestamp: Unix timestamp

        Returns
            DateTime instance
        """
        result = _pendulum.DateTime.utcfromtimestamp(timestamp)
        return cls.instance(result)

    @classmethod
    def utcnow(cls):
        """Create a DateTime representing current UTC time.

        Returns
            DateTime instance
        """
        result = _pendulum.DateTime.utcnow()
        return cls.instance(result)

    @classmethod
    def now(cls, tz: str | _zoneinfo.ZoneInfo | _datetime.tzinfo | None = None) -> Self:
        """Get a DateTime instance for the current date and time.
        """
        if tz is None or tz == 'local':
            d = _datetime.datetime.now(LCL)
        elif tz is UTC or tz == 'UTC':
            d = _datetime.datetime.now(UTC)
        else:
            d = _datetime.datetime.now(UTC)
            tz = _pendulum._safe_timezone(tz)
            d = d.astimezone(tz)
        return cls(d.year, d.month, d.day, d.hour, d.minute, d.second,
                   d.microsecond, tzinfo=d.tzinfo, fold=d.fold)

    @classmethod
    def today(cls, tz: str | _zoneinfo.ZoneInfo | None = None):
        """Create a DateTime object representing today at the start of day.

        Unlike pendulum.today() which returns current time, this method
        returns a DateTime object at 00:00:00 of the current day.

        Parameters
            tz: Optional timezone (defaults to local timezone)

        Returns
            DateTime instance representing start of current day
        """
        return DateTime.now(tz).start_of('day')

    def date(self):
        return Date(self.year, self.month, self.day)

    @classmethod
    def combine(
        cls,
        date: _datetime.date,
        time: _datetime.time,
        tzinfo: _zoneinfo.ZoneInfo | None = None,
    ) -> Self:
        """Combine date and time (*behaves differently from Pendulum `combine`*).
        """
        _tzinfo = tzinfo or time.tzinfo
        return DateTime.instance(_datetime.datetime.combine(date, time, tzinfo=_tzinfo))

    def rfc3339(self):
        """
        >>> DateTime.parse('Fri, 31 Oct 2014 10:55:00')
        DateTime(2014, 10, 31, 10, 55, 0, tzinfo=Timezone('UTC'))
        >>> DateTime.parse('Fri, 31 Oct 2014 10:55:00').rfc3339()
        '2014-10-31T10:55:00+00:00'
        """
        return self.isoformat()

    def time(self):
        """Extract time from self (preserve timezone)

        >>> d = DateTime(2022, 1, 1, 12, 30, 15, tzinfo=EST)
        >>> d.time()
        Time(12, 30, 15, tzinfo=Timezone('US/Eastern'))

        >>> d = DateTime(2022, 1, 1, 12, 30, 15, tzinfo=UTC)
        >>> d.time()
        Time(12, 30, 15, tzinfo=Timezone('UTC'))
        """
        return Time.instance(self)

    @classmethod
    def parse(
        cls, s: str | int | None,
        entity: Entity = NYSE,
        raise_err: bool = False
        ) -> Self | None:
        """Convert a string or timestamp to a DateTime with extended format support.

        Unlike pendulum's parse, this method supports:
        - Unix timestamps (int/float)
        - Special codes (T=today, Y=yesterday, P=previous business day)
        - Business day offsets (e.g., 'T-3b' for 3 business days before today)
        - Multiple date-time formats beyond ISO 8601

        Parameters
            s: String or timestamp to parse
            entity: Calendar entity for business day calculations
            raise_err: Whether to raise error on parse failure

        Returns
            DateTime instance or None if parsing fails and raise_err is False

        Examples

        Basic formats:
        >>> DateTime.parse('2022/1/1')
        DateTime(2022, 1, 1, 0, 0, 0, tzinfo=Timezone('...'))

        Timezone handling:
        >>> this_est1 = DateTime.parse('Fri, 31 Oct 2014 18:55:00').in_timezone(EST)
        >>> this_est1
        DateTime(2014, 10, 31, 14, 55, 0, tzinfo=Timezone('US/Eastern'))

        >>> this_est2 = DateTime.parse('Fri, 31 Oct 2014 14:55:00 -0400')
        >>> this_est2
        DateTime(2014, 10, 31, 14, 55, 0, tzinfo=...)

        >>> this_utc = DateTime.parse('Fri, 31 Oct 2014 18:55:00 GMT')
        >>> this_utc
        DateTime(2014, 10, 31, 18, 55, 0, tzinfo=tzutc())

        Timestamp parsing:
        >>> DateTime.parse(1707856982).replace(tzinfo=UTC).epoch()
        1707856982.0
        """
        if not s:
            if raise_err:
                raise ValueError('Empty value')
            return

        if not isinstance(s, str | int | float):
            raise TypeError(f'Invalid type for datetime parse: {s.__class__}')

        if isinstance(s, int | float):
            if len(str(int(s))) == 13:
                s /= 1000  # Convert from milliseconds to seconds
            iso = _datetime.datetime.fromtimestamp(s).isoformat()
            return cls.parse(iso).replace(tzinfo=LCL)

        with contextlib.suppress(ValueError, TypeError):
            return cls.instance(_dateutil.parser.parse(s))

        for delim in (' ', ':'):
            bits = s.split(delim, 1)
            if len(bits) == 2:
                d = Date.parse(bits[0])
                t = Time.parse(bits[1])
                if d is not None and t is not None:
                    return DateTime.combine(d, t, LCL)

        d = Date.parse(s, entity=entity)
        if d is not None:
            return cls(d.year, d.month, d.day, 0, 0, 0)

        current = Date.today()
        t = Time.parse(s)
        if t is not None:
            return cls.combine(current, t, LCL)

        if raise_err:
            raise ValueError('Invalid date-time format: %s', s)

    @classmethod
    def instance(
        cls,
        obj: _datetime.date
        | _datetime.time
        | pd.Timestamp
        | np.datetime64
        | Self
        | None,
        tz: str | _zoneinfo.ZoneInfo | _datetime.tzinfo | None = None,
        raise_err: bool = False,
    ) -> Self | None:
        """Create a DateTime instance from various datetime-like objects.

        This method provides a unified interface for converting different
        date/time types including pandas and numpy datetime objects into
        DateTime instances.

        Unlike pendulum, this method:
        - Handles pandas Timestamp and numpy datetime64 objects
        - Adds timezone (UTC by default) when none is specified
        - Has special handling for time objects

        Parameters
            obj: Date, datetime, time, or compatible object to convert
            tz: Optional timezone to apply (if None, uses obj's timezone or UTC)
            raise_err: Whether to raise error if obj is None/NA

        Returns
            DateTime instance or None if obj is None/NA and raise_err is False

        Examples

        From Python datetime types:
        >>> DateTime.instance(_datetime.date(2022, 1, 1))
        DateTime(2022, 1, 1, 0, 0, 0, tzinfo=Timezone('...'))
        >>> DateTime.instance(_datetime.datetime(2022, 1, 1, 0, 0, 0))
        DateTime(2022, 1, 1, 0, 0, 0, tzinfo=Timezone('...'))

        Preserves timezone behavior:
        >>> DateTime.instance(DateTime(2022, 1, 1, 0, 0, 0))
        DateTime(2022, 1, 1, 0, 0, 0)

        From Time objects:
        >>> DateTime.instance(Time(4, 4, 21))
        DateTime(..., 4, 4, 21, tzinfo=Timezone('UTC'))
        >>> DateTime.instance(Time(4, 4, 21, tzinfo=UTC))
        DateTime(..., 4, 4, 21, tzinfo=Timezone('UTC'))

        From numpy/pandas datetime:
        >>> DateTime.instance(np.datetime64('2000-01', 'D'))
        DateTime(2000, 1, 1, 0, 0, 0, tzinfo=Timezone('UTC'))
        """
        if pd.isna(obj):
            if raise_err:
                raise ValueError('Empty value')
            return

        if obj.__class__ == cls and not tz:
            return obj

        if isinstance(obj, pd.Timestamp):
            obj = obj.to_pydatetime()
            return cls.instance(obj, tz=tz or UTC)
        if isinstance(obj, np.datetime64):
            obj = np.datetime64(obj, 'us').astype(_datetime.datetime)
            return cls.instance(obj, tz=tz or UTC)

        if obj.__class__ == Date:
            return cls(obj.year, obj.month, obj.day, tzinfo=tz or UTC)
        if isinstance(obj, _datetime.date) and not isinstance(obj, _datetime.datetime):
            return cls(obj.year, obj.month, obj.day, tzinfo=tz or UTC)

        tz = tz or obj.tzinfo or UTC

        if obj.__class__ == Time:
            return cls.combine(Date.today(), obj, tzinfo=tz)
        if isinstance(obj, _datetime.time):
            return cls.combine(Date.today(), obj, tzinfo=tz)

        return cls(obj.year, obj.month, obj.day, obj.hour, obj.minute,
                   obj.second, obj.microsecond, tzinfo=tz)


class IntervalError(AttributeError):
    pass


class Interval:

    _business: bool = False
    _entity: type[NYSE] = NYSE

    def __init__(self, begdate: str | Date | None = None, enddate: str | Date | None = None):
        self.begdate = Date.parse(begdate) if isinstance(begdate, str) else Date.instance(begdate)
        self.enddate = Date.parse(enddate) if isinstance(enddate, str) else Date.instance(enddate)

    def business(self) -> Self:
        self._business = True
        if self.begdate:
            self.begdate.business()
        if self.enddate:
            self.enddate.business()
        return self

    @property
    def b(self) -> Self:
        return self.business()

    def entity(self, e: type[NYSE] = NYSE) -> Self:
        self._entity = e
        if self.begdate:
            self.enddate._entity = e
        if self.enddate:
            self.enddate._entity = e
        return self

    def range(self, window=0) -> tuple[_datetime.date, _datetime.date]:
        """Set date ranges based on begdate, enddate and window.

        The combinations are as follows:

          beg end num    action
          --- --- ---    ---------------------
           -   -   -     Error, underspecified
          set set set    Error, overspecified
          set set  -
          set  -   -     end=max date
           -  set  -     beg=min date
           -   -  set    end=max date, beg=end - num
          set  -  set    end=beg + num
           -  set set    beg=end - num

        Basic/legacy cases
        >>> Interval(Date(2014, 4, 3), None).b.range(3)
        (Date(2014, 4, 3), Date(2014, 4, 8))
        >>> Interval(None, Date(2014, 7, 27)).range(20)
        (Date(2014, 7, 7), Date(2014, 7, 27))
        >>> Interval(None, Date(2014, 7, 27)).b.range(20)
        (Date(2014, 6, 27), Date(2014, 7, 27))

        Do not modify dates if both are provided
        >>> Interval(Date(2024, 7, 25), Date(2024, 7, 25)).b.range(None)
        (Date(2024, 7, 25), Date(2024, 7, 25))
        >>> Interval(Date(2024, 7, 27), Date(2024, 7, 27)).b.range(None)
        (Date(2024, 7, 27), Date(2024, 7, 27))

        Edge cases (7/27/24 is weekend)
        >>> Interval(Date(2024, 7, 27), None).b.range(0)
        (Date(2024, 7, 27), Date(2024, 7, 27))
        >>> Interval(None, Date(2024, 7, 27)).b.range(0)
        (Date(2024, 7, 27), Date(2024, 7, 27))
        >>> Interval(Date(2024, 7, 27), None).b.range(1)
        (Date(2024, 7, 27), Date(2024, 7, 29))
        >>> Interval(None, Date(2024, 7, 27)).b.range(1)
        (Date(2024, 7, 26), Date(2024, 7, 27))
        """
        begdate, enddate = self.begdate, self.enddate

        window = abs(int(window or 0))

        if begdate and enddate and window:
            raise IntervalError('Window requested and begdate and enddate provided')
        if not begdate and not enddate and not window:
            raise IntervalError('Missing begdate, enddate, and window')
        if not begdate and not enddate and window:
            raise IntervalError('Missing begdate and enddate, window specified')

        if begdate and enddate:
            pass  # do nothing if both provided
        elif (not begdate and not enddate) or enddate:
            begdate = enddate.subtract(days=window) if window else enddate
        else:
            enddate = begdate.add(days=window) if window else begdate

        enddate._business = False
        begdate._business = False

        return begdate, enddate

    def is_business_day_series(self) -> list[bool]:
        """Is business date range.

        >>> list(Interval(Date(2018, 11, 19), Date(2018, 11, 25)).is_business_day_series())
        [True, True, True, False, True, False, False]
        >>> list(Interval(Date(2021, 11, 22),Date(2021, 11, 28)).is_business_day_series())
        [True, True, True, False, True, False, False]
        """
        for thedate in self.series():
            yield thedate.is_business_day()

    def series(self, window=0):
        """Get a series of datetime.date objects.

        give the function since and until wherever possible (more explicit)
        else pass in a window to back out since or until
        - Window gives window=N additional days. So `until`-`window`=1
        defaults to include ALL days (not just business days)

        >>> next(Interval(Date(2014,7,16), Date(2014,7,16)).series())
        Date(2014, 7, 16)
        >>> next(Interval(Date(2014,7,12), Date(2014,7,16)).series())
        Date(2014, 7, 12)
        >>> len(list(Interval(Date(2014,7,12), Date(2014,7,16)).series()))
        5
        >>> len(list(Interval(Date(2014,7,12), None).series(window=4)))
        5
        >>> len(list(Interval(Date(2014,7,16)).series(window=4)))
        5

        Weekend and a holiday
        >>> len(list(Interval(Date(2014,7,3), Date(2014,7,5)).b.series()))
        1
        >>> len(list(Interval(Date(2014,7,17), Date(2014,7,16)).series()))
        Traceback (most recent call last):
        ...
        AssertionError: Begdate must be earlier or equal to Enddate

        since != business day and want business days
        1/[3,10]/2015 is a Saturday, 1/7/2015 is a Wednesday
        >>> len(list(Interval(Date(2015,1,3), Date(2015,1,7)).b.series()))
        3
        >>> len(list(Interval(Date(2015,1,3), None).b.series(window=3)))
        3
        >>> len(list(Interval(Date(2015,1,3), Date(2015,1,10)).b.series()))
        5
        >>> len(list(Interval(Date(2015,1,3), None).b.series(window=5)))
        5
        """
        window = abs(int(window))
        since, until = self.begdate, self.enddate
        _business = self._business
        assert until or since, 'Since or until is required'
        if not since and until:
            since = (until.business() if _business else
                     until).subtract(days=window)
        elif since and not until:
            until = (since.business() if _business else
                     since).add(days=window)
        assert since <= until, 'Since date must be earlier or equal to Until date'
        thedate = since
        while thedate <= until:
            if _business:
                if thedate.is_business_day():
                    yield thedate
            else:
                yield thedate
            thedate = thedate.add(days=1)

    def start_of_series(self, unit='month') -> list[Date]:
        """Return a series between and inclusive of begdate and enddate.

        >>> Interval(Date(2018, 1, 5), Date(2018, 4, 5)).start_of_series('month')
        [Date(2018, 1, 1), Date(2018, 2, 1), Date(2018, 3, 1), Date(2018, 4, 1)]
        >>> Interval(Date(2018, 4, 30), Date(2018, 7, 30)).start_of_series('month')
        [Date(2018, 4, 1), Date(2018, 5, 1), Date(2018, 6, 1), Date(2018, 7, 1)]
        >>> Interval(Date(2018, 1, 5), Date(2018, 4, 5)).start_of_series('week')
        [Date(2018, 1, 1), Date(2018, 1, 8), ..., Date(2018, 4, 2)]
        """
        begdate = self.begdate.start_of(unit)
        enddate = self.enddate.start_of(unit)
        interval = _pendulum.interval(begdate, enddate)
        return [Date.instance(d).start_of(unit) for d in interval.range(f'{unit}s')]

    def end_of_series(self, unit='month') -> list[Date]:
        """Return a series between and inclusive of begdate and enddate.

        >>> Interval(Date(2018, 1, 5), Date(2018, 4, 5)).end_of_series('month')
        [Date(2018, 1, 31), Date(2018, 2, 28), Date(2018, 3, 31), Date(2018, 4, 30)]
        >>> Interval(Date(2018, 4, 30), Date(2018, 7, 30)).end_of_series('month')
        [Date(2018, 4, 30), Date(2018, 5, 31), Date(2018, 6, 30), Date(2018, 7, 31)]
        >>> Interval(Date(2018, 1, 5), Date(2018, 4, 5)).end_of_series('week')
        [Date(2018, 1, 7), Date(2018, 1, 14), ..., Date(2018, 4, 8)]
        """
        begdate = self.begdate.end_of(unit)
        enddate = self.enddate.end_of(unit)
        interval = _pendulum.interval(begdate, enddate)
        return [Date.instance(d).end_of(unit) for d in interval.range(f'{unit}s')]

    def days(self) -> int:
        """Return days between (begdate, enddate] or negative (enddate, begdate].

        >>> Interval(Date(2018, 9, 6), Date(2018, 9, 10)).days()
        4
        >>> Interval(Date(2018, 9, 10), Date(2018, 9, 6)).days()
        -4
        >>> Interval(Date(2018, 9, 6), Date(2018, 9, 10)).b.days()
        2
        >>> Interval(Date(2018, 9, 10), Date(2018, 9, 6)).b.days()
        -2
        """
        assert self.begdate
        assert self.enddate
        if self.begdate == self.enddate:
            return 0
        if not self._business:
            return (self.enddate - self.begdate).days
        if self.begdate < self.enddate:
            return len(list(self.series())) - 1
        _reverse = Interval(self.enddate, self.begdate)
        _reverse._entity = self._entity
        _reverse._business = self._business
        return -len(list(_reverse.series())) + 1

    def quarters(self):
        """Return the number of quarters between two dates
        TODO: good enough implementation; refine rules to be heuristically precise

        >>> round(Interval(Date(2020, 1, 1), Date(2020, 2, 16)).quarters(), 2)
        0.5
        >>> round(Interval(Date(2020, 1, 1), Date(2020, 4, 1)).quarters(), 2)
        1.0
        >>> round(Interval(Date(2020, 1, 1), Date(2020, 7, 1)).quarters(), 2)
        1.99
        >>> round(Interval(Date(2020, 1, 1), Date(2020, 8, 1)).quarters(), 2)
        2.33
        """
        return 4 * self.days() / 365.0

    def years(self, basis: int = 0):
        """Years with Fractions (matches Excel YEARFRAC)

        Adapted from https://web.archive.org/web/20200915094905/https://dwheeler.com/yearfrac/calc_yearfrac.py

        Basis:
        0 = US (NASD) 30/360
        1 = Actual/actual
        2 = Actual/360
        3 = Actual/365
        4 = European 30/360

        >>> begdate = Date(1978, 2, 28)
        >>> enddate = Date(2020, 5, 17)

        Tested Against Excel
        >>> "{:.4f}".format(Interval(begdate, enddate).years(0))
        '42.2139'
        >>> '{:.4f}'.format(Interval(begdate, enddate).years(1))
        '42.2142'
        >>> '{:.4f}'.format(Interval(begdate, enddate).years(2))
        '42.8306'
        >>> '{:.4f}'.format(Interval(begdate, enddate).years(3))
        '42.2438'
        >>> '{:.4f}'.format(Interval(begdate, enddate).years(4))
        '42.2194'
        >>> '{:.4f}'.format(Interval(enddate, begdate).years(4))
        '-42.2194'

        Excel has a known leap year bug when year == 1900 (=YEARFRAC("1900-1-1", "1900-12-1", 1) -> 0.9178)
        The bug originated from Lotus 1-2-3, and was purposely implemented in Excel for the purpose of backward compatibility.
        >>> begdate = Date(1900, 1, 1)
        >>> enddate = Date(1900, 12, 1)
        >>> '{:.4f}'.format(Interval(begdate, enddate).years(4))
        '0.9167'
        """

        def average_year_length(date1, date2):
            """Algorithm for average year length"""
            days = (Date(date2.year + 1, 1, 1) - Date(date1.year, 1, 1)).days
            years = (date2.year - date1.year) + 1
            return days / years

        def feb29_between(date1, date2):
            """Requires date2.year = (date1.year + 1) or date2.year = date1.year.

            Returns True if "Feb 29" is between the two dates (date1 may be Feb29).
            Two possibilities: date1.year is a leap year, and date1 <= Feb 29 y1,
            or date2.year is a leap year, and date2 > Feb 29 y2.
            """
            mar1_date1_year = Date(date1.year, 3, 1)
            if calendar.isleap(date1.year) and (date1 < mar1_date1_year) and (date2 >= mar1_date1_year):
                return True
            mar1_date2_year = Date(date2.year, 3, 1)
            return bool(calendar.isleap(date2.year) and date2 >= mar1_date2_year and date1 < mar1_date2_year)

        def appears_lte_one_year(date1, date2):
            """Returns True if date1 and date2 "appear" to be 1 year or less apart.

            This compares the values of year, month, and day directly to each other.
            Requires date1 <= date2; returns boolean. Used by basis 1.
            """
            if date1.year == date2.year:
                return True
            return bool(date1.year + 1 == date2.year and (date1.month > date2.month or date1.month == date2.month and date1.day >= date2.day))

        def basis0(date1, date2):
            # change day-of-month for purposes of calculation.
            date1day, date1month, date1year = date1.day, date1.month, date1.year
            date2day, date2month, date2year = date2.day, date2.month, date2.year
            if date1day == 31 and date2day == 31:
                date1day = 30
                date2day = 30
            elif date1day == 31:
                date1day = 30
            elif date1day == 30 and date2day == 31:
                date2day = 30
            # Note: If date2day==31, it STAYS 31 if date1day < 30.
            # Special fixes for February:
            elif date1month == 2 and date2month == 2 and date1 == date1.end_of('month') \
                and date2 == date2.end_of('month'):
                date1day = 30  # Set the day values to be equal
                date2day = 30
            elif date1month == 2 and date1 == date1.end_of('month'):
                date1day = 30  # "Illegal" Feb 30 date.
            daydiff360 = (date2day + date2month * 30 + date2year * 360) \
                - (date1day + date1month * 30 + date1year * 360)
            return daydiff360 / 360

        def basis1(date1, date2):
            if appears_lte_one_year(date1, date2):
                if date1.year == date2.year and calendar.isleap(date1.year):
                    year_length = 366.0
                elif feb29_between(date1, date2) or (date2.month == 2 and date2.day == 29):
                    year_length = 366.0
                else:
                    year_length = 365.0
                return (date2 - date1).days / year_length
            return (date2 - date1).days / average_year_length(date1, date2)

        def basis2(date1, date2):
            return (date2 - date1).days / 360.0

        def basis3(date1, date2):
            return (date2 - date1).days / 365.0

        def basis4(date1, date2):
            # change day-of-month for purposes of calculation.
            date1day, date1month, date1year = date1.day, date1.month, date1.year
            date2day, date2month, date2year = date2.day, date2.month, date2.year
            if date1day == 31:
                date1day = 30
            if date2day == 31:
                date2day = 30
            # Remarkably, do NOT change Feb. 28 or 29 at ALL.
            daydiff360 = (date2day + date2month * 30 + date2year * 360) - \
                (date1day + date1month * 30 + date1year * 360)
            return daydiff360 / 360

        begdate, enddate = self.begdate, self.enddate
        if enddate is None:
            return

        sign = 1
        if begdate > enddate:
            begdate, enddate = enddate, begdate
            sign = -1
        if begdate == enddate:
            return 0.0

        if basis == 0:
            return basis0(begdate, enddate) * sign
        if basis == 1:
            return basis1(begdate, enddate) * sign
        if basis == 2:
            return basis2(begdate, enddate) * sign
        if basis == 3:
            return basis3(begdate, enddate) * sign
        if basis == 4:
            return basis4(begdate, enddate) * sign

        raise ValueError('Basis range [0, 4]. Unknown basis {basis}.')


def create_ics(begdate, enddate, summary, location):
    """Create a simple .ics file per RFC 5545 guidelines."""

    return f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//hacksw/handcal//NONSGML v1.0//EN
BEGIN:VEVENT
DTSTART;TZID=America/New_York:{begdate:%Y%m%dT%H%M%S}
DTEND;TZID=America/New_York:{enddate:%Y%m%dT%H%M%S}
SUMMARY:{summary}
LOCATION:{location}
END:VEVENT
END:VCALENDAR
    """


if __name__ == '__main__':
    __import__('doctest').testmod(optionflags=4 | 8 | 32)
