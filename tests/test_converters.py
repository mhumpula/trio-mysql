import datetime

from trio_mysql import converters


__all__ = ["TestConverter"]


class TestConverter:

    async def test_escape_string(self, set_me_up):
        await set_me_up(self)
        self.assertEqual(
            converters.escape_string(u"foo\nbar"),
            u"foo\\nbar"
        )

    async def test_convert_datetime(self, set_me_up):
        await set_me_up(self)
        expected = datetime.datetime(2007, 2, 24, 23, 6, 20)
        dt = converters.convert_datetime('2007-02-24 23:06:20')
        self.assertEqual(dt, expected)

    async def test_convert_datetime_with_fsp(self, set_me_up):
        await set_me_up(self)
        expected = datetime.datetime(2007, 2, 24, 23, 6, 20, 511581)
        dt = converters.convert_datetime('2007-02-24 23:06:20.511581')
        self.assertEqual(dt, expected)

    def _test_convert_timedelta(self, with_negate=False, with_fsp=False):
        d = {'hours': 789, 'minutes': 12, 'seconds': 34}
        s = '%(hours)s:%(minutes)s:%(seconds)s' % d
        if with_fsp:
            d['microseconds'] = 511581
            s += '.%(microseconds)s' % d

        expected = datetime.timedelta(**d)
        if with_negate:
            expected = -expected
            s = '-' + s

        tdelta = converters.convert_timedelta(s)
        self.assertEqual(tdelta, expected)

    async def test_convert_timedelta(self, set_me_up):
        await set_me_up(self)
        self._test_convert_timedelta(with_negate=False, with_fsp=False)
        self._test_convert_timedelta(with_negate=True, with_fsp=False)

    async def test_convert_timedelta_with_fsp(self, set_me_up):
        await set_me_up(self)
        self._test_convert_timedelta(with_negate=False, with_fsp=True)
        self._test_convert_timedelta(with_negate=False, with_fsp=True)

    async def test_convert_time(self, set_me_up):
        await set_me_up(self)
        expected = datetime.time(23, 6, 20)
        time_obj = converters.convert_time('23:06:20')
        self.assertEqual(time_obj, expected)

    async def test_convert_time_with_fsp(self, set_me_up):
        await set_me_up(self)
        expected = datetime.time(23, 6, 20, 511581)
        time_obj = converters.convert_time('23:06:20.511581')
        self.assertEqual(time_obj, expected)
