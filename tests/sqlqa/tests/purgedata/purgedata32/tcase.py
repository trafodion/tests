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
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None

#
#                       Purgedata 32
#
#    A1: SQL utility Purgedata -- Functional test.
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""Purgedata from multi-partitioned SQL tables, and then do some"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  DDL and DML on it.
    
    stmt = """purgedata """ + defs.my_schema + """.pd32004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """purgedata """ + defs.my_schema + """.pd32004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from """ + defs.my_schema + """.pd32004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    ##sh import ${my_schema}.pd32004 -I ${qagdata1}/dat10500 -C 200
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd32004 select * from """ + gvars.g_schema_cmureg + """.dat200;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.pd32004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '200')
    
    stmt = """update """ + defs.my_schema + """.pd32004 set two = 2 where UNIQUE2 < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 20)
    
    stmt = """select * from """ + defs.my_schema + """.pd32004 where unique2 < 50;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 50)
    
    stmt = """select max(UNIQUE1), min(UNIQUE2), sum(TWO), sum(FOUR),
sum(TEN), sum(TWENTY), sum(ONEPERCENT), sum(TENPERCENT),
sum(TWENTYPERCENT), sum(FIFTYPERCENT), max(UNIQUE3),
sum(EVENONEPERCENT), sum(ODDONEPERCENT), max(STRINGU1),
max(STRINGU2), min(STRING4)
from """ + defs.my_schema + """.pd32004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select * from """ + defs.my_schema + """.pd32004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 200)
    
    stmt = """delete from """ + defs.my_schema + """.pd32004
where unique2 between 50 and 99;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 50)
    
    stmt = """select * from """ + defs.my_schema + """.pd32004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 150)
    
    stmt = """purgedata """ + defs.my_schema + """.pd32004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from """ + defs.my_schema + """.pd32004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    stmt = """drop table """ + defs.my_schema + """.pd32004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

