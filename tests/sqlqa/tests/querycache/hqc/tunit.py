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
import defs
import setup
import cleanup
# Import you own test modules, one line for each.
import tcase_numhits
import tcase_math
import tcase_agg
import tcase_cstr
import tcase_datetime
import tcase_other
import tcase_pred
import tcase_eqchar
import tcase_eqdate
import tcase_eqts
import tcase_eqint
import tcase_eqflt
import tcase_eqvchr
import tcase_eqnum
import tcase_eqsint
import tcase_eqintvl
import tcase_eqreal


def sq_testunit(hptestmgr, testlist=[]):

    cleanup._init(hptestmgr, testlist)
    setup._init(hptestmgr, testlist)

    # Auto execute your test modules, one line for each.
    if defs.genexp == 0:
        hpdci.auto_execute_module_tests(tcase_numhits, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_math, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_agg, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_cstr, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_datetime, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_other, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_pred, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_eqchar, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_eqdate, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_eqts, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_eqint, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_eqflt, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_eqvchr, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_eqnum, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_eqsint, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(tcase_eqreal, hptestmgr, testlist)
    #LP bug 1450853: query with equals predicate on INTERVAL datatype
    #    should not have a non-parameterized literal. Also hkey value
    #    appears inconsistent with parameterized literal. Commented
    #    out testcase for now.
    #hpdci.auto_execute_module_tests(tcase_eqintvl, hptestmgr, testlist)

    cleanup._init(hptestmgr, testlist)
