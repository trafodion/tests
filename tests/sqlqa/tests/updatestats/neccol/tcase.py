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
from ...lib import gvars
import defs
import setup

_testmgr = None
_testlist = []
_dci = None


def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()


def test_auto4(desc="""auto missing stats level 4(def)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    # USTAT_AUTO_MISSING_STATS_LEVEL = 4
    # optimizer will request single column and multi-column stats
    # for scans, joins and groupbys
    setup.run_each_test()

    _testmgr.testcase_end(desc)


def test_auto3(desc="""auto missing stats level 3"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    # USTAT_AUTO_MISSING_STATS_LEVEL = 3
    # optimizer will request single column and multi-column stats
    # for scans and joins
    setup.run_each_test('3')

    _testmgr.testcase_end(desc)


def test_auto2(desc="""auto missing stats level 2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    # USTAT_AUTO_MISSING_STATS_LEVEL = 2
    # optimizer will request single column and multi-column stats for scans
    setup.run_each_test('2')

    _testmgr.testcase_end(desc)


def test_auto1(desc="""auto missing stats level 1"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    # USTAT_AUTO_MISSING_STATS_LEVEL = 1
    # optimizer will request single column stats
    setup.run_each_test('1')

    _testmgr.testcase_end(desc)


def test_auto0(desc="""auto missing stats level 0"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    # USTAT_AUTO_MISSING_STATS_LEVEL = 0
    # optimizer will request no stats
    setup.run_each_test('0')

    _testmgr.testcase_end(desc)
