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
import Test41
import Test42
import Test43
import Test44
import Test45
import Test46
import Test47
import Test48
import Test49
import Test50

def sq_testunit(hptestmgr, testlist=[]):

    cleanup._init(hptestmgr, testlist)
    setup._init(hptestmgr, testlist)

    # Auto execute your test modules, one line for each.
    hpdci.auto_execute_module_tests(create_tables, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test41, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test42, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test43, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test44, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test45, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test46, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test47, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test48, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test49, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(Test50, hptestmgr, testlist)

    cleanup._init(hptestmgr, testlist)
   
