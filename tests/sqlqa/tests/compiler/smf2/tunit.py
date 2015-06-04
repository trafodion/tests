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

from ...lib import hpdci
import setup
import cleanup
# Import you own test modules, one line for each.
import create_temp_tables
import comp_queries
import cqdT1
import tcase1
import resetcqdT1
import cqdT2
import tcase2
import resetcqdT2
import summary

def sq_testunit(hptestmgr, testlist=[]):

    cleanup._init(hptestmgr, testlist)
    setup._init(hptestmgr, testlist)

    # Auto execute your test modules, one line for each.
    hpdci.auto_execute_module_tests(create_temp_tables, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(comp_queries, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(cqdT1, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase1, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(resetcqdT1, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(cqdT2, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase2, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(resetcqdT2, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(summary, hptestmgr, testlist)

    cleanup._init(hptestmgr, testlist)
   
