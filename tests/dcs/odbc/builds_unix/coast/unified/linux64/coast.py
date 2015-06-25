# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @@@ END COPYRIGHT @@@


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


