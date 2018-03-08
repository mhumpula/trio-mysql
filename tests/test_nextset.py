import pytest

from trio_mysql.tests import base
from trio_mysql import util


class TestNextset(base.TrioMySQLTestCase):

    def setUp(self):
        super(TestNextset, self).setUp()
        self.con = self.connections[0]

    def test_nextset(self):
        cur = self.con.cursor()
        await cur.execute("SELECT 1; SELECT 2;")
        self.assertEqual([(1,)], list(cur))

        r = await cur.nextset()
        self.assertTrue(r)

        self.assertEqual([(2,)], list(cur))
        assert await cur.nextset() is None

    def test_skip_nextset(self):
        cur = self.con.cursor()
        await cur.execute("SELECT 1; SELECT 2;")
        self.assertEqual([(1,)], list(cur))

        await cur.execute("SELECT 42")
        self.assertEqual([(42,)], list(cur))

    def test_ok_and_next(self):
        cur = self.con.cursor()
        await cur.execute("SELECT 1; commit; SELECT 2;")
        self.assertEqual([(1,)], list(cur))
        assert await cur.nextset()
        assert await cur.nextset()
        self.assertEqual([(2,)], list(cur))
        assert not await cur.nextset()

    @pytest.mark.xfail
    def test_multi_cursor(self):
        cur1 = self.con.cursor()
        cur2 = self.con.cursor()

        await cur1.execute("SELECT 1; SELECT 2;")
        await cur2.execute("SELECT 42")

        self.assertEqual([(1,)], list(cur1))
        self.assertEqual([(42,)], list(cur2))

        r = await cur1.nextset()
        self.assertTrue(r)

        self.assertEqual([(2,)], list(cur1))
        assert await cur1.nextset() is None

    def test_multi_statement_warnings(self):
        cursor = self.con.cursor()

        try:
            await cursor.execute('DROP TABLE IF EXISTS a; '
                           'DROP TABLE IF EXISTS b;')
        except TypeError:
            self.fail()

    #TODO: How about SSCursor and nextset?
    # It's very hard to implement correctly...
