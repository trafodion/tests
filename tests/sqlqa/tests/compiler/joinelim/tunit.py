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
import create_tables
import do_prepare
import tcase_je01
import tcase_je02
import tcase_je03
import create_tables04
import tcase_je04
import restore_tables04
import create_tables05
import tcase_je05
import restore_tables05
import tcase_je06
import tcase_je07
import tcase_je08
import tcase_je09
import create_tables10
import tcase_je10
import create_tables11
import tcase_je11
import create_tables12
import tcase_je12
import create_tables13
import tcase_je13
import create_tables14
import tcase_je14
import create_tables15
import tcase_je15
import create_tables16
import tcase_je16
import create_tables17
import tcase_je17


def sq_testunit(hptestmgr, testlist=[]):

    cleanup._init(hptestmgr, testlist)
    setup._init(hptestmgr, testlist)

    # Auto execute your test modules, one line for each.
    hpdci.auto_execute_module_tests(create_tables, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(do_prepare, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je01, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je02, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je03, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(create_tables04, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je04, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(restore_tables04, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(create_tables05, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je05, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(restore_tables05, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je06, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je07, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je08, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je09, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(create_tables10, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je10, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(create_tables11, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je11, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(create_tables12, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je12, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(create_tables13, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je13, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(create_tables14, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je14, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(create_tables15, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je15, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(create_tables16, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je16, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(create_tables17, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_je17, hptestmgr, testlist)

    cleanup._init(hptestmgr, testlist)
   
