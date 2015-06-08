import os
import unittest

class coastTest(unittest.TestCase):

	def setup(self):
		pass

	def teardown(self):
		pass

	def testCoastSQLAllocEnv(self):
		ret = os.system("./coast -d $ODBCTEST_DSN -u $ODBCTEST_USER -p $ODBCTEST_PASS -c $ODBCTEST_CHARSET -m $ODBCTEST_OS -f API SQLAllocEnv")
		assert ret == 0

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(coastTest)
    unittest.TextTestRunner(verbosity=2).run(suite)


