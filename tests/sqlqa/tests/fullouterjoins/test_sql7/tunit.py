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
import Test21
import Test22
import Test23
import Test24
import Test25
import Test26
import Test27
import Test28
import Test29
import Test30

def sq_testunit(hptestmgr, testlist=[]):

    cleanup._init(hptestmgr, testlist)
    setup._init(hptestmgr, testlist)

    # Auto execute your test modules, one line for each.
    hpdci.auto_execute_module_tests(create_tables, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test21, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test22, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test23, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test24, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test25, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test26, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test27, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test28, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test29, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test30, hptestmgr, testlist)

    cleanup._init(hptestmgr, testlist)
   
