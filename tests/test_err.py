from trio_mysql import err


__all__ = ["TestRaiseException"]


class TestRaiseException:

    async def test_raise_mysql_exception(self, set_me_up):
        await set_me_up(self)
        data = b"\xff\x15\x04Access denied"
        with self.assertRaises(err.OperationalError) as cm:
            err.raise_mysql_exception(data)
        self.assertEqual(cm.exception.args, (1045, 'Access denied'))

    async def test_raise_mysql_exception_client_protocol_41(self, set_me_up):
        await set_me_up(self)
        data = b"\xff\x15\x04#28000Access denied"
        with self.assertRaises(err.OperationalError) as cm:
            err.raise_mysql_exception(data)
        self.assertEqual(cm.exception.args, (1045, 'Access denied'))
