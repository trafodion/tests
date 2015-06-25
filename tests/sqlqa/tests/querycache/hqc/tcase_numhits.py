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


def test_numhits(desc="""HQCEntries num_hits differ; qry versus prep stmt"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: num_hits"""

    # The preparser stage of cache(which is part of SQC) captures an
    # exactly-identical query ahead of HQC, thus hit is not counted
    # in HQC. The preparser stage of cache skips prepare statement,
    # thus the same query with prepare could be matched and counted
    # by HQC.

    setup.resetHQC()

    # HQC entry added
    defs.qry = """select * from g00 where colint = abs(50 - 250);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM G00 WHERE COLINT = ABS ( #NP# - #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '35300A3235300A'
    setup.verifyHQCEntryExists()

    # issue query again and verify num_hits unchanged
    output = _dci.cmdexec(defs.qry)
    _dci.expect_selected_msg(output, '1')
    setup.getEntryNumHits()
    output = _dci.cmdexec("execute get_num_hits;")
    _dci.expect_str_token(output, '0')
    _dci.expect_selected_msg(output, '1')

    # prepare qry, skipped by preparser stage, hit counted
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("execute get_num_hits;")
    _dci.expect_str_token(output, '1')
    _dci.expect_selected_msg(output, '1')

    # prepare query again, hit counted
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("execute get_num_hits;")
    _dci.expect_str_token(output, '2')
    _dci.expect_selected_msg(output, '1')

    # query captured by preparser stage, hit not counted
    output = _dci.cmdexec(defs.qry)
    _dci.expect_selected_msg(output, '1')
    output = _dci.cmdexec("execute get_num_hits;")
    _dci.expect_str_token(output, '2')
    _dci.expect_selected_msg(output, '1')

    # prepare query again, hit counted
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("execute get_num_hits;")
    _dci.expect_str_token(output, '3')
    _dci.expect_selected_msg(output, '1')

    # query again, hit not counted
    output = _dci.cmdexec(defs.qry)
    _dci.expect_selected_msg(output, '1')
    output = _dci.cmdexec("execute get_num_hits;")
    _dci.expect_str_token(output, '3')
    _dci.expect_selected_msg(output, '1')

    # ========================================================
    setup.resetHQC()

    # HQC entry added
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.num_hits = 0
    setup.verifyHQCEntryExists()

    # prepare query again, hit counted
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("execute get_num_hits;")
    _dci.expect_str_token(output, '1')
    _dci.expect_selected_msg(output, '1')

    # query, hit counted
    output = _dci.cmdexec(defs.qry)
    _dci.expect_selected_msg(output, '1')
    output = _dci.cmdexec("execute get_num_hits;")
    _dci.expect_str_token(output, '2')
    _dci.expect_selected_msg(output, '1')

    # query again, hit not counted
    output = _dci.cmdexec(defs.qry)
    _dci.expect_selected_msg(output, '1')
    output = _dci.cmdexec("execute get_num_hits;")
    _dci.expect_str_token(output, '2')
    _dci.expect_selected_msg(output, '1')

    # prepare query again, hit counted
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("execute get_num_hits;")
    _dci.expect_str_token(output, '3')
    _dci.expect_selected_msg(output, '1')

    # issue query again, hit not counted
    output = _dci.cmdexec(defs.qry)
    _dci.expect_selected_msg(output, '1')
    output = _dci.cmdexec("execute get_num_hits;")
    _dci.expect_str_token(output, '3')
    _dci.expect_selected_msg(output, '1')

    _testmgr.testcase_end(desc)
