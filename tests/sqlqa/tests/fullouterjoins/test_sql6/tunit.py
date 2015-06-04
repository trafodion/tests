# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
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

from ...lib import hpdci
import setup
import cleanup
# Import you own test modules, one line for each.
import create_tables
import Test11
import Test12
import Test13
import Test14
import Test15
import Test16
import Test17
import Test18
import Test19
import Test20

def sq_testunit(hptestmgr, testlist=[]):

    cleanup._init(hptestmgr, testlist)
    setup._init(hptestmgr, testlist)

    # Auto execute your test modules, one line for each.
    hpdci.auto_execute_module_tests(create_tables, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test11, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test12, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test13, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test14, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test15, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test16, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test17, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test18, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test19, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test20, hptestmgr, testlist)

    cleanup._init(hptestmgr, testlist)
   
