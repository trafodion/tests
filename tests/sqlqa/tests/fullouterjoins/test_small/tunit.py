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
import create_tables_vt
import tcase
import tcase_vt
import tcase_joins
import tcase_nulltbls
import tcase_unequal

def sq_testunit(hptestmgr, testlist=[]):

    cleanup._init(hptestmgr, testlist)
    setup._init(hptestmgr, testlist)

    # Auto execute your test modules, one line for each.
    hpdci.auto_execute_module_tests(create_tables, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(create_tables_vt, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_vt, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_joins, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_nulltbls, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_unequal, hptestmgr, testlist)

    cleanup._init(hptestmgr, testlist)
   
