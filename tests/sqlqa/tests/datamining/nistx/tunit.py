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
import cr8allnist
import t001
import t002
import t003
import t004
import t005
import t006
import t007
import t008
import t009
import t010
import t011
import t012
import t013
import t014
import t015
import t016
import t017
import t018
import t019
import t020
import t021
import t022
import t023
import t024
import t025
import t026
import t027
import t028

def sq_testunit(hptestmgr, testlist=[]):

    cleanup._init(hptestmgr, testlist)
    setup._init(hptestmgr, testlist)

    # Auto execute your test modules, one line for each.
    hpdci.auto_execute_module_tests(cr8allnist, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t001, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t002, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t003, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t004, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t005, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t006, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t007, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t008, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t009, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t010, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t011, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t012, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t013, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t014, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t015, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t016, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t017, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t018, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t019, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t020, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t021, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t022, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t023, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t024, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t025, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t026, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t027, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t028, hptestmgr, testlist)

    cleanup._init(hptestmgr, testlist)
   
