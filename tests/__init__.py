# Sorted by alphabetical order
from trio_mysql.tests.test_DictCursor import *
from trio_mysql.tests.test_SSCursor import *
from trio_mysql.tests.test_basic import *
from trio_mysql.tests.test_connection import *
from trio_mysql.tests.test_converters import *
from trio_mysql.tests.test_cursor import *
from trio_mysql.tests.test_err import *
from trio_mysql.tests.test_issues import *
from trio_mysql.tests.test_load_local import *
from trio_mysql.tests.test_nextset import *
from trio_mysql.tests.test_optionfile import *

from trio_mysql.tests.thirdparty import *

if __name__ == "__main__":
    import unittest2
    unittest2.main()
