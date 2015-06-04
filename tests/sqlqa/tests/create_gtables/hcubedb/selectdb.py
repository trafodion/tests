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
import defs

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


def test001(desc='select tables'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """select count(*) from t0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '10')
    stmt = """select count(*) from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '10')
    stmt = """select count(*) from t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '10')
    stmt = """select count(*) from t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '10')
    stmt = """select count(*) from t4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '10')
    stmt = """select count(*) from t5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '10')
    stmt = """select count(*) from t6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '100')
    stmt = """select count(*) from t66;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '100')
    stmt = """select count(*) from t7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '100')
    stmt = """select count(*) from t8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1000')
    stmt = """select count(*) from t9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '10000')
    stmt = """select count(*) from t10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '100000')
    stmt = """select count(*) from t11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '10')
    stmt = """select count(*) from t12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '10')
    stmt = """select count(*) from cube1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '100000')
    stmt = """select count(*) from cube2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1000000')
    stmt = """select count(*) from cube3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '10000000')
    stmt = """select count(*) from cube4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '100000000')
    # below table not automatically created
    ##expectfile $test_dir/count.exp cube5
    #select count(*) from cube5;

    _testmgr.testcase_end(desc)    
