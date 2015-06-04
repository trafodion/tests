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

from datetime import datetime
from ...lib import hpdci
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None
_tables = []
_qid = None
_state = None
_errorCode = None
_queryType = None
_sourceString = None
_rowsReturn = None
_compileStartTime = None
_compileEndTime = None
_executeStartTime = None
_executeEndTime = None
_statsCollectType = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
#*********************************************************************
#test0001
#  SQL_INSERT_UNIQUE 
#*********************************************************************
def test0001(desc="test0001"):
    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create table tstat (a char(5) not null ,
        b smallint not null ,
        c char(4),
        d integer,
        primary key (a,b) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into tstat values ('AAAA ',11,'AAAA',11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into tstat values ('BBBB ',12,'BBBB',12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into tstat values ('MMMM ',21,'MMMM',21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into tstat values ('XXXXX',22,'XXXX',22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """Prepare xx  from insert into tstat values ('SSSS', ?, 'SSSS', 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx using 10;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_INSERT_UNIQUE"
    _sourceString = "insert into tstat values ('SSSS', ?, 'SSSS', 10)"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".tstat").upper()
    _tables = [table1]
    verifyGetstats()
    verifyInfostats()

    stmt = """drop table tstat;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0002
#  SQL_INSERT_NON_UNIQUE
#*********************************************************************
def test0002(desc="test0002"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = "create table nation2 like " + gvars.g_schema_tpch2x + ".nation;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "Prepare xx from insert into nation2 select * from " + gvars.g_schema_tpch2x+ ".nation;"
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*row(s) inserted.*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_INSERT_NON_UNIQUE"
    _sourceString = "insert into nation2 select * from " + gvars.g_schema_tpch2x+ ".nation"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (gvars.g_schema_tpch2x + ".nation").upper()
    table2 = (defs.my_schema + ".nation2").upper()
    _tables = [table1, table2]
    verifyGetstats()
    verifyInfostats()

    stmt = """drop table nation2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0003
#  SQL_DELETE_NON_UNIQUE
#*********************************************************************
def test0003(desc="test0003"):
    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create table nation2 like """ + gvars.g_schema_tpch2x + ".nation;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into nation2 select * from """ + gvars.g_schema_tpch2x + ".nation;"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """Prepare xx from delete from nation2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_DELETE_NON_UNIQUE"
    _sourceString = "delete from nation2"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".nation2").upper()
    _tables = [table1]
    verifyGetstats()
    verifyInfostats()

    stmt = """drop table nation2;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0004
#  SQL_DELETE_UNIQUE
#*********************************************************************
def test0004(desc="test0004"):
    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create table nation2 like """ + gvars.g_schema_tpch2x + ".nation;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into nation2 select * from """ + gvars.g_schema_tpch2x + ".nation;"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """Prepare xx  from delete from nation2 where n_name = 'CANADA';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_DELETE_NON_UNIQUE"
    _sourceString = "delete from nation2 where n_name = 'CANADA'"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".nation2").upper()
    _tables = [table1]
    verifyGetstats()
    verifyInfostats()

    stmt = """drop table nation2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0005
#  SQL_UPDATE_NON_UNIQUE
#*********************************************************************
def test0005(desc="test0005"):
    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create table t304
        (a1 int not null,
        a2 char(20),
        primary key (a1)
        );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into t304 values(1, 'aaaaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into t304 values(2, 'aaaaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into t304 values(3, 'aaaaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into t304 values(4, 'aaaaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into t304 values(5, 'aaaaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """Prepare xx  from UPDATE t304 SET a2 = 'sr_update' WHERE a2 in (select a2 from t304 where a2 = 'aaaaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_UPDATE_NON_UNIQUE"
    _sourceString = "UPDATE t304 SET a2 = 'sr_update' WHERE a2 in (select a2 from t304 where a2 = 'aaaaa')"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".t304").upper()
    _tables = [table1]
    verifyGetstats()
    verifyInfostats()

    stmt = """drop table t304 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0006
#  SQL_UPDATE_UNIQUE
#*********************************************************************
def test0006(desc="test0006"):
    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create table nation2 like """ + gvars.g_schema_tpch2x + ".nation;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into nation2 select * from """ + gvars.g_schema_tpch2x + ".nation;"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """Prepare xx from update nation2 set N_REGIONKEY = 2 where N_NATIONKEY = 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_UPDATE_UNIQUE"
    _sourceString = "update nation2 set N_REGIONKEY = 2 where N_NATIONKEY = 3"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".nation2").upper()
    _tables = [table1]
    verifyGetstats()
    verifyInfostats()

    stmt = """drop table nation2;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0007
#  SQL_UPSERT_NON_UNIQUE
#*********************************************************************
def test0007(desc="test0007"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = "create table customer2 like " + gvars.g_schema_tpch2x + ".customer;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "Prepare xx from upsert using load into customer2 select * from " + gvars.g_schema_tpch2x+ ".customer;"
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_INSERT_NON_UNIQUE"
    _sourceString = "upsert using load into customer2 select * from " + gvars.g_schema_tpch2x+ ".customer"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (gvars.g_schema_tpch2x + ".customer").upper()
    table2 = (defs.my_schema + ".customer2").upper()
    _tables = [table1, table2]
    verifyGetstats()
    verifyInfostats()

    stmt = """drop table customer2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


#*********************************************************************
#test0010
#  SQL_SELECT_UNIQUE
#*********************************************************************
def test0010(desc="test0010"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """prepare xx from SELECT p_name, p_type, p_brand, p_container from """ + gvars.g_schema_tpch2x + ".part where p_partkey = 7;"
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_SELECT_UNIQUE"
    _sourceString = "SELECT p_name, p_type, p_brand, p_container from """ + gvars.g_schema_tpch2x + ".part where p_partkey = 7"
    _rowsReturn = "1"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (gvars.g_schema_tpch2x + ".part").upper()
    _tables = [table1]
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0011
#  SQL_SELECT_NON_UNIQUE
#  EQUALS int, skewed value
#*********************************************************************
def test0011(desc="test0011"):
    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx from select [first 1] * from f00 where colint = 543210 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "select [first 1] * from f00 where colint = 543210 order by colkey"
    _rowsReturn = "1"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".f00").upper()
    _tables = [table1]
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0012
#  SQL_SELECT_NON_UNIQUE
#  EQUALS iso, skewed
#*********************************************************************
def test0012(desc="test0012"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx from select [last 1] * from f00 where colchariso = 'stuvwx' order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "select [last 1] * from f00 where colchariso = 'stuvwx' order by colkey"
    _rowsReturn = "1"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".f00").upper()
    _tables = [table1]
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0013
#  SQL_SELECT_NON_UNIQUE
#  LIKE
#*********************************************************************
def test0013(desc="test0013"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx from select [first 1] * from f00 where colcharucs2 LIKE 'abcdefghij_' order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "select [first 1] * from f00 where colcharucs2 LIKE 'abcdefghij_' order by colkey"
    _rowsReturn = "1"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".f00").upper()
    _tables = [table1]
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0014
#  SQL_SELECT_NON_UNIQUE
#  GTE
#*********************************************************************
def test0014(desc="test0014"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx from select [last 1] * from f00 where colint >= 99975 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "select [last 1] * from f00 where colint >= 99975 order by colkey"
    _rowsReturn = "1"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".f00").upper()
    _tables = [table1]
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0015
#  SQL_SELECT_NON_UNIQUE
#  LT
#*********************************************************************
def test0015(desc="test0015"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx from select [first 1] * from f00 where colcharucs2 < _ucs2'abcdefghijk' order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "select [first 1] * from f00 where colcharucs2 < _ucs2'abcdefghijk' order by colkey"
    _rowsReturn = "1"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".f00").upper()
    _tables = [table1]
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0016
#  SQL_SELECT_NON_UNIQUE
#  IN
#*********************************************************************
def test0016(desc="test0016"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx from select [last 1] * from f00 where colchariso NOT in ('10000', '30000', 'abcdefghijk', 'stuvwx', '900000') order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "select [last 1] * from f00 where colchariso NOT in ('10000', '30000', 'abcdefghijk', 'stuvwx', '900000') order by colkey"
    _rowsReturn = "1"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".f00").upper()
    _tables = [table1]
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0017
#  SQL_SELECT_NON_UNIQUE
#  BETWEEN
#*********************************************************************
def test0017(desc="test0017"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx from select [first 1] * from f00 where colchariso BETWEEN '900000' and 'azzzzz' order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "select [first 1] * from f00 where colchariso BETWEEN '900000' and 'azzzzz' order by colkey"
    _rowsReturn = "1"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".f00").upper()
    _tables = [table1]
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0018
#  SQL_SELECT_NON_UNIQUE
#  IN NULL
#*********************************************************************
def test0018(desc="test0018"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx from select [last 1] * from f00 where colcharison IS NULL order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "select [last 1] * from f00 where colcharison IS NULL order by colkey"
    _rowsReturn = "1"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".f00").upper()
    _tables = [table1]
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0019
#  SQL_SELECT_NON_UNIQUE
#  JOIN, EQUALS
#*********************************************************************
def test0019(desc="test0019"):

    global _testmgr
    global _testlist
    global _tables
    global _dci
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx from select [first 1] * from f00, d00 where colkey = d00colkey and colint = 10000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "select [first 1] * from f00, d00 where colkey = d00colkey and colint = 10000"
    _rowsReturn = "1"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".f00").upper()
    table2 = (defs.my_schema + ".d00").upper()
    _tables = [table1, table2]
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0020
#  SQL_SELECT_NON_UNIQUE
#  JOIN, LIKE
#*********************************************************************
def test0020(desc="test0020"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx from select [last 1] * from f00, d00 where colkey = d00colkey and f00.colchariso LIKE '%defgh%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "select [last 1] * from f00, d00 where colkey = d00colkey and f00.colchariso LIKE '%defgh%'"
    _rowsReturn = "1"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".f00").upper()
    table2 = (defs.my_schema + ".d00").upper()
    _tables = [table1, table2]
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0021
#  SQL_SELECT_NON_UNIQUE
#  JOIN, GTE
#*********************************************************************
def test0021(desc="test0021"):

    global _testmgr
    global _testlist
    global _tables
    global _dci
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx from select [first 1] * from f00, d00 where colkey = d00colkey and d00colcharucs2 >= _ucs2'zyxwvuts';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "select [first 1] * from f00, d00 where colkey = d00colkey and d00colcharucs2 >= _ucs2'zyxwvuts'"
    _rowsReturn = "1"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".f00").upper()
    table2 = (defs.my_schema + ".d00").upper()
    _tables = [table1, table2]
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0022
#  SQL_SELECT_NON_UNIQUE
#  JOIN, LT
#*********************************************************************
def test0022(desc="test0022"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx from select [last 1] * from f00, d00 where colkey = d00colkey and f00.colchariso < '1500';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "select [last 1] * from f00, d00 where colkey = d00colkey and f00.colchariso < '1500'"
    _rowsReturn = "1"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".f00").upper()
    table2 = (defs.my_schema + ".d00").upper()
    _tables = [table1, table2]
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0023
#  SQL_SELECT_NON_UNIQUE
#  JOIN, IN
#*********************************************************************
def test0023(desc="test0023"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx from select [first 1] * from f00, d00 where colkey = d00colkey and d00colint in (10000, 30000, 543210, 876543, 900000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "select [first 1] * from f00, d00 where colkey = d00colkey and d00colint in (10000, 30000, 543210, 876543, 900000)"
    _rowsReturn = "1"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (defs.my_schema + ".f00").upper()
    table2 = (defs.my_schema + ".d00").upper()
    _tables = [table1, table2]
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0024
#  SQL_SELECT_NON_UNIQUE
#  JOIN, IN
#*********************************************************************
def test0024(desc="test0024"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = "Prepare xx from select * from " + gvars.g_schema_tpch2x + ".nation;"
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "select * from " + gvars.g_schema_tpch2x+ ".nation"
    _rowsReturn = "25"
    _statsCollectType = "OPERATOR_STATS"
    table1 = (gvars.g_schema_tpch2x + ".nation").upper()
    _tables = [table1]
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)


#*********************************************************************
#test0030
#  SQL_OTHER - CREATE TABLE
#*********************************************************************
def test0030(desc="test0030"):
    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop table F0101;"""
    output = _dci.cmdexec(stmt)

    stmt = """Prepare xx  from Create table F0101
        (
        pk int not null not droppable primary key
        , fk_d01 int not null -- foreign key references D01(pk)
        , fk_d02 int not null -- foreign key references D02(pk)
        , fk_d03 int not null -- foreign key references D03(pk)
        , fk_d04 int not null -- foreign key references D04(pk)
        , fk_d05 int not null -- foreign key references D05(pk)
        , fk_d06 int not null -- foreign key references D06(pk)
        , fk_d07 int not null -- foreign key references D07(pk)
        , fk_d08 int not null -- foreign key references D08(pk)
        , fk_d09 int not null -- foreign key references D09(pk)
        , fk_d10 int not null -- foreign key references D10(pk)
        , val01 int
        , val02 int
        , val01_d01 int
        , val02_d01 int
        , val01_d02 int
        , val02_d02 int
        , val01_d03 int
        , val02_d03 int
        );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_OTHER"
    _sourceString = "Create table F0101"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    _tables = []
    verifyGetstats()
    verifyInfostats()

    stmt = """drop table F0101 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0031
#  SQL_OTHER - DROP TABLE
#*********************************************************************
def test0031(desc="test0031"):
    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create table F0101
        (
        pk int not null not droppable primary key
        , fk_d01 int not null -- foreign key references D01(pk)
        , fk_d02 int not null -- foreign key references D02(pk)
        , fk_d03 int not null -- foreign key references D03(pk)
        , fk_d04 int not null -- foreign key references D04(pk)
        , fk_d05 int not null -- foreign key references D05(pk)
        , fk_d06 int not null -- foreign key references D06(pk)
        , fk_d07 int not null -- foreign key references D07(pk)
        , fk_d08 int not null -- foreign key references D08(pk)
        , fk_d09 int not null -- foreign key references D09(pk)
        , fk_d10 int not null -- foreign key references D10(pk)
        , val01 int
        , val02 int
        , val01_d01 int
        , val02_d01 int
        , val01_d02 int
        , val02_d02 int
        , val01_d03 int
        , val02_d03 int
        );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table f0202 like f0101;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Prepare xx from drop table f0202;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_OTHER"
    _sourceString = "drop table f0202"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    _tables = []
    verifyGetstats()
    verifyInfostats()

    stmt = """drop table f0101 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0032
#  SQL_OTHER - ALTER TABLE
#*********************************************************************
def test0032(desc="test0032"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop table F0101;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create table F0101
        (
        pk int not null not droppable primary key
        , fk_d01 int not null -- foreign key references D01(pk)
        , fk_d02 int not null -- foreign key references D02(pk)
        , fk_d03 int not null -- foreign key references D03(pk)
        , fk_d04 int not null -- foreign key references D04(pk)
        , fk_d05 int not null -- foreign key references D05(pk)
        , fk_d06 int not null -- foreign key references D06(pk)
        , fk_d07 int not null -- foreign key references D07(pk)
        , fk_d08 int not null -- foreign key references D08(pk)
        , fk_d09 int not null -- foreign key references D09(pk)
        , fk_d10 int not null -- foreign key references D10(pk)
        , val01 int
        , val02 int
        , val01_d01 int
        , val02_d01 int
        , val01_d02 int
        , val02_d02 int
        , val01_d03 int
        , val02_d03 int
        );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Prepare xx  from alter table F0101 rename to F0102;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_OTHER"
    _sourceString = "alter table F0101 rename to F0102"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    _tables = []
    verifyGetstats()
    verifyInfostats()

    stmt = """drop table F0102 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0033
#  SQL_OTHER - CREATE INDEX
#*********************************************************************
def test0033(desc="test0033"):
    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create table t303 (
        char3_4             Varchar(8)                  no default not null not droppable,
        sdec4_n20           Decimal(4)                  no default,
        int4_yTOm_uniq      Interval year(5) to month   no default not null droppable,
        sbin4_n1000         Smallint                    not null not droppable,
        time4_1000          Time                        no default not null not droppable,
        primary key (time4_1000)  not droppable
        ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Prepare xx  from create unique index idx303 on t303 (char3_4, sdec4_n20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_OTHER"
    _sourceString = "create unique index idx303 on t303 (char3_4, sdec4_n20)"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    _tables = []
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0034
#  SQL_OTHER - DROP INDEX
#*********************************************************************
def test0034(desc="test0034"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx  from drop index idx303 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_OTHER"
    _sourceString = "drop index idx303 cascade"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    _tables = []
    verifyGetstats()
    verifyInfostats()

    stmt = """drop table t303 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0035
#  SQL_OTHER - CREATE VIEW
#*********************************************************************
def test0035(desc="test0035"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop table F0101 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create table F0101
        (
        pk int not null not droppable primary key
        , fk_d01 int not null -- foreign key references D01(pk)
        , fk_d02 int not null -- foreign key references D02(pk)
        , fk_d03 int not null -- foreign key references D03(pk)
        , fk_d04 int not null -- foreign key references D04(pk)
        , fk_d05 int not null -- foreign key references D05(pk)
        , fk_d06 int not null -- foreign key references D06(pk)
        , fk_d07 int not null -- foreign key references D07(pk)
        , fk_d08 int not null -- foreign key references D08(pk)
        , fk_d09 int not null -- foreign key references D09(pk)
        , fk_d10 int not null -- foreign key references D10(pk)
        , val01 int
        , val02 int
        , val01_d01 int
        , val02_d01 int
        , val01_d02 int
        , val02_d02 int
        , val01_d03 int
        , val02_d03 int
        );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Prepare xx  from create view V0101 (c1, c2, c3, c4, c5, c6, c7, c8)
        as select pk, fk_d01, fk_d02, val01, val02, val01_d01, val02_d01, val01_d02 from F0101;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_OTHER"
    _sourceString = "create view V0101 (c1, c2, c3, c4, c5, c6, c7, c8)"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    _tables = []
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0037
#  SQL_OTHER - DROP VIEW
#*********************************************************************
def test0037(desc="test0037"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx  from drop view V0101 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_OTHER"
    _sourceString = "drop view V0101 cascade"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    _tables = []
    verifyGetstats()
    verifyInfostats()

    stmt = """drop table F0101 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#*********************************************************************
# test0038
#  SQL_OTHER - create schema
#*********************************************************************
def test0038(desc="test0038"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx  from create schema sch320;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_OTHER"
    _sourceString = "create schema sch320"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    _tables = []
    verifyGetstats()
    verifyInfostats()

    stmt = """drop schema sch320 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#*********************************************************************
# test0039
#  SQL_OTHER - drop schema
#*********************************************************************
def test0039(desc="test0039"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create schema sch320;"""
    output = _dci.cmdexec(stmt)

    stmt = """Prepare xx  from drop schema sch320 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_OTHER"
    _sourceString = "drop schema sch320 cascade"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    _tables = []
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
#test0040
#  SQL_CAT_UTIL
#*********************************************************************
def test0040(desc="test0040"):
    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create table nation2 like """ + gvars.g_schema_tpch2x + ".nation;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into nation2 select * from """ + gvars.g_schema_tpch2x + ".nation;"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """Prepare xx  from update statistics for table nation2 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_CAT_UTIL"
    _sourceString = "update statistics for table nation2 on every column"
    _rowsReturn = "0"
    _statsCollectType = "OPERATOR_STATS"
    _tables = []
    verifyGetstats()
    verifyInfostats()

    stmt = """drop table nation2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#*********************************************************************
# test0043
#  SQL_OTHER - set schema
#*********************************************************************
def test0043(desc="test0043"):

    global _testmgr
    global _testlist
    global _dci
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx  from set schema """ + gvars.g_schema_tpch2x + ";"
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_SET_SCHEMA"
    _sourceString = "set schema """ + gvars.g_schema_tpch2x
    _rowsReturn = "0"
    _statsCollectType = "NO_STATS"
    verifyGetstats2()

    # reset schema
    stmt = "set schema " + defs.my_schema + ";"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#*********************************************************************
# test0044
#  SQL_OTHER - control query default
#*********************************************************************
def test0044(desc="test0044"):

    global _testmgr
    global _testlist
    global _dci
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx  from cqd catalog reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_CONTROL"
    _sourceString = "cqd catalog reset"
    _rowsReturn = "0"
    _statsCollectType = "NO_STATS"
    verifyGetstats2()

    _testmgr.testcase_end(desc)

#*********************************************************************
# test0045
#  SQL_OTHER - showcontrol default
#*********************************************************************
def test0045(desc="test0045"):

    global _testmgr
    global _testlist
    global _dci
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx  from showcontrol default catalog;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "showcontrol default catalog"
    _rowsReturn = "8"
    _statsCollectType = "NO_STATS"
    verifyGetstats2()

    _testmgr.testcase_end(desc)

#*********************************************************************
# test0046
#  SQL_OTHER - begin work
#*********************************************************************
def test0046(desc="test0046"):

    global _testmgr
    global _testlist
    global _dci
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx  from begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_OTHER"
    _sourceString = "begin work"
    _rowsReturn = "0"
    _statsCollectType = "NO_STATS"
    verifyGetstats2()

    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#*********************************************************************
# test0047
#  SQL_OTHER - commit work
#*********************************************************************
def test0047(desc="test0047"):

    global _testmgr
    global _testlist
    global _dci
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    stmt = """Prepare xx  from commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "0"
    _queryType = "SQL_OTHER"
    _sourceString = "commit work"
    _rowsReturn = "0"
    _statsCollectType = "NO_STATS"
    verifyGetstats2()

    _testmgr.testcase_end(desc)

#*********************************************************************
# test0048
#  SQL_OTHER - showddl
#*********************************************************************
def test0048(desc="test0048"):

    global _testmgr
    global _testlist
    global _dci
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create table a02
        ( c1 int CONSTRAINT t2pri PRIMARY KEY
        CONSTRAINT t2ntnul1 NOT NULL
        NOT DROPPABLE
        , c2 char(3) CONSTRAINT t2uniq UNIQUE
        CONSTRAINT t2ntnul2 NOT NULL
        , c3 char(2) CONSTRAINT t2ck CHECK (c3 > 'aa')
        , c4 int CONSTRAINT t2nul4 NOT NULL
        );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Prepare xx  from showddl a02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "showddl a02"
    # showddl returns different numbers of rows depending on a lot of things.
    # For example, security on and off will affect the output. Specify "-1" to 
    # let verifyRowsReturned() know that this comparision should be skipped.
    _rowsReturn = "-1"
    _statsCollectType = "NO_STATS"
    verifyGetstats2()

    stmt = """drop table a02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#*********************************************************************
# test0049
#  SQL_OTHER - get tables
#*********************************************************************
def test0049(desc="test0049"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Prepare xx  from get tables;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_EXE_UTIL"
    _sourceString = "get tables"
    _rowsReturn = "-1"
    _statsCollectType = "OPERATOR_STATS"
    _tables = []
    verifyGetstats()
    verifyInfostats()

    _testmgr.testcase_end(desc)

#*********************************************************************
# test0050
#  SQL_OTHER - values
#*********************************************************************
def test0050(desc="test0050"):

    global _testmgr
    global _testlist
    global _dci
    global _tables
    global _state
    global _errorCode
    global _queryType
    global _sourceString
    global _rowsReturn
    global _statsCollectType
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create table a02
        ( c1 int CONSTRAINT t2pri PRIMARY KEY
        CONSTRAINT t2ntnul1 NOT NULL
        NOT DROPPABLE
        , c2 char(3) CONSTRAINT t2uniq UNIQUE
        CONSTRAINT t2ntnul2 NOT NULL
        , c3 char(2) CONSTRAINT t2ck CHECK (c3 > 'aa')
        , c4 int CONSTRAINT t2nul4 NOT NULL
        );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Prepare xx  from values (1, (select count(*) from a02));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """*ERROR*""")

    _state = "CLOSE"
    _errorCode = "100"
    _queryType = "SQL_SELECT_NON_UNIQUE"
    _sourceString = "values (1, (select count(*) from a02))"
    _rowsReturn = "1"
    _statsCollectType = "OPERATOR_STATS"
    _tables = []
    verifyGetstats()
    verifyInfostats()

    stmt = """drop table a02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#*********************************************************************
# The following are functions to verify stats
#*********************************************************************
def verifyGetstats():
    global _testmgr
    global _dci
    global _qid
    global _tables

    stmt = """infostats xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    for line in output.splitlines():
        if line.startswith('MXID'):
            token = line.split()
            _qid = token[0]

    stmt = "get statistics for qid " + _qid + ";"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    verifyQid(output)
    verifyCompileStartTime(output)
    verifyCompileEndTime(output)
    verifyCompileElapsedTime(output)
    verifyExecuteStartTime(output)
    verifyExecuteEndTime(output)
    verifyExecuteElapsedTime(output)
    verifyState(output)
    verifyRowsAffected(output)
    verifySQLErroeCode(output)
    verifyStatsErrorCode(output)
    verifyQueryType(output)
    verifySubQueryType(output)
    verifyEstimatedAccessedRows(output)
    verifyEstimatedUsedRows(output)
    verifyParentQid(output)
    verifyParentQuerySystem(output)
    verifyChildQid(output)
    verifyNumberofSQLProcesses(output)
    verifyNumberofCpus(output)
    verifyTransactionId(output)
    verifySourceString(output)
    verifySQLSourceLength(output)
    verifyRowsReturned(output)
    verifyFirstRowReturnedTime(output)
    verifyLastErrorbeforeAQR(output)
    verifyNumberofAQRretries(output)
    verifyDelaybeforeAQR(output)
    verifyNooftimesreclaimed(output)
    verifyCancelTime(output)
    verifyLastSuspendTime(output)
    verifyStatsCollectionType(output)
    verifySQLProcessBusyTime(output)
    verifyUDRProcessBusyTime(output)
    verifySQLSpaceAllocated(output)
    verifySQLSpaceUsed(output)
    verifySQLHeapAllocated(output)
    verifySQLHeapUsed(output)
    verifyEIDSpaceAllocated(output)
    verifyEIDSpaceUsed(output)
    verifyEIDHeapAllocated(output)
    verifyEIDHeapUsed(output)
    verifyProcessesCreated(output)
    verifyProcessCreateTime(output)
    verifyRequestMessageCount(output)
    verifyRequestMessageBytes(output)
    verifyReplyMessageCount(output)
    verifyReplyMessageBytes(output)
    verifyScrOverflowMode(output)
    verifyScrFileCount(output)
    verifyScrBufferBlkSize(output)
    verifyScrBufferBlksRead(output)
    verifyScrBufferBlksWritten(output)
    verifyScrReadCount(output)
    verifyScrWriteCount(output)

    # verify table stats
    if len(_tables) != 0:
        verifyTableStats(output)

def verifyGetstats2():
    global _testmgr
    global _dci
    global _qid

    stmt = """infostats xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    for line in output.splitlines():
        if line.startswith('MXID'):
            token = line.split()
            _qid = token[0]

    stmt = "get statistics for qid " + _qid + ";"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    verifyQid(output)
    verifyCompileStartTime(output)
    verifyCompileEndTime(output)
    verifyCompileElapsedTime(output)
    verifyExecuteStartTime(output)
    verifyExecuteEndTime(output)
    verifyExecuteElapsedTime(output)
    verifyState(output)
    verifyRowsAffected(output)
    verifySQLErroeCode(output)
    verifyStatsErrorCode(output)
    verifyQueryType(output)
    verifySubQueryType(output)
    verifyEstimatedAccessedRows(output)
    verifyEstimatedUsedRows(output)
    verifyParentQid(output)
    verifyParentQuerySystem(output)
    verifyChildQid(output)
    verifyNumberofSQLProcesses(output)
    verifyNumberofCpus(output)
    verifyTransactionId(output)
    verifySourceString(output)
    verifySQLSourceLength(output)
    verifyRowsReturned(output)
    verifyFirstRowReturnedTime(output)
    verifyLastErrorbeforeAQR(output)
    verifyNumberofAQRretries(output)
    verifyDelaybeforeAQR(output)
    verifyNooftimesreclaimed(output)
    verifyCancelTime(output)
    verifyLastSuspendTime(output)
    verifyStatsCollectionType(output)

def verifyInfostats():
    global _testmgr
    global _dci

    stmt = """infostats xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    found = False
    for line in output.splitlines():
        if line.startswith('MXID'):
            found = True
            token = line.split()
            try:
                v = float(token[1])
                if v < 0:
                    _testmgr.mismatch_record("infostats CPUTime has negative value")
            except:
                _testmgr.mismatch_record("infostats CPUTime has invalid value")
            try:
                v = float(token[2])
                if v < 0:
                    _testmgr.mismatch_record("infostats IOTime has negative value")
            except:
                _testmgr.mismatch_record("infostats IOTime has invalid value")
            try:
                v = float(token[3])
                if v < 0:
                    _testmgr.mismatch_record("infostats MsgTime has negative value")
            except:
                _testmgr.mismatch_record("infostats MsgTime has invalid value")
            try:
                v = float(token[4])
                if v < 0:
                    _testmgr.mismatch_record("infostats IdleTime has negative value")
            except:
                _testmgr.mismatch_record("infostats MsgTime has invalid value")
            try:
                v = float(token[5])
                if v < 0:
                    _testmgr.mismatch_record("infostats TotalTime has negative value")
            except:
                _testmgr.mismatch_record("infostats TotalTime has invalid value")
            try:
                v = float(token[6])
                if v < 0:
                    _testmgr.mismatch_record("infostats Cardinality has negative value")
            except:
                _testmgr.mismatch_record("infostats Cardinality has invalid value")
            try:
                v = float(token[7])
                if v < 0:
                    _testmgr.mismatch_record("infostats ResourceUsage has negative value")
            except:
                _testmgr.mismatch_record("infostats ResourceUsage has invalid value")
            try:
                v = float(token[8])
                if v < 0:
                    _testmgr.mismatch_record("infostats AffinityNumber has negative value")
            except:
                _testmgr.mismatch_record("infostats AffinityNumber has invalid value")
            try:
                v = float(token[9])
                if v < 0:
                    _testmgr.mismatch_record("infostats Dop has negative value")
            except:
                _testmgr.mismatch_record("infostats Dop has invalid value")
            try:
                v = float(token[10])
                if v < 0:
                    _testmgr.mismatch_record("infostats XnNeeded has negative value")
            except:
                _testmgr.mismatch_record("infostats XnNeeded has invalid value")
            try:
                v = float(token[11])
                if v < 0:
                    _testmgr.mismatch_record("infostats MandatoryCrossProduct has negative value")
            except:
                _testmgr.mismatch_record("infostats MandatoryCrossProduct has invalid value")
            try:
                v = float(token[12])
                if v < 0:
                    _testmgr.mismatch_record("infostats MissingStats has negative value")
            except:
                _testmgr.mismatch_record("infostats MissingStats has invalid value")
            try:
                v = float(token[13])
                if v < 0:
                    _testmgr.mismatch_record("infostats NumOfJoins has negative value")
            except:
                _testmgr.mismatch_record("infostats NumOfJoins has invalid value")
            try:
                v = float(token[14])
                if v < 0:
                    _testmgr.mismatch_record("infostats FullScanOnTable has negative value")
            except:
                _testmgr.mismatch_record("infostats FullScanOnTable has invalid value")
            try:
                v = float(token[15])
                if v < 0:
                    _testmgr.mismatch_record("infostats HighDp2MxBufferUsage has negative value")
            except:
                _testmgr.mismatch_record("infostats HighDp2MxBufferUsage has invalid value")
            try:
                v = float(token[16])
                if v < -1:
                    _testmgr.mismatch_record("infostats RowsAccessedForFullScan has negative value")
            except:
                _testmgr.mismatch_record("infostats RowsAccessedForFullScan has invalid value")
            try:
                v = float(token[17])
                if v < 0:
                    _testmgr.mismatch_record("infostats Dp2RowsAccessed has negative value")
            except:
                _testmgr.mismatch_record("infostats Dp2RowsAccessed has invalid value")
            try:
                v = float(token[18])
                if v < 0:
                    _testmgr.mismatch_record("infostats Dp2RowsUsed has negative value")
            except:
                _testmgr.mismatch_record("infostats Dp2RowsUse has invalid value")

    if not found:
            _testmgr.mismatch_record("infostats Qid not found")


def verifyTableStats(data):
    global _testmgr
    global _tables

    lines = data.splitlines()
    for table in _tables:
        tableline = 0
        for i in range(len(lines)):
            if lines[i].startswith(table):
                tableline = i

        if tableline == 0:
                _testmgr.mismatch_record("Table stats for " + table + " not found")
        else:
            token = lines[tableline+1].split()
            if int(token[0].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Records Accessed Estimated has negative value")
            if int(token[1].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Records Used Estimated has negative value")
        
            token = lines[tableline+2].split()
            if int(token[0].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Records Accessed Actual has negative value")
            if int(token[1].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Records Used Actual has negative value")
            if int(token[2].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Hbase IOs has negative value")
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Hbase IO Bytes has negative value")
            if int(token[4].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Hbase IO Sum Time has negative value")
            if int(token[5].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Hbase IO Max Time has negative value")

def verifyQid(data):
    global _testmgr

    found = False
    for line in data.splitlines():
        if line.startswith('Qid'):
            found = True
            token = line.split()
            if token[1] != _qid:
                _testmgr.mismatch_record("Qid is not correct")

    if not found:
            _testmgr.mismatch_record("Qid not found")

def verifyCompileStartTime(data):
    global _testmgr
    global _compileStartTime

    found = False
    for line in data.splitlines():
        if line.startswith('Compile Start Time'):
            found = True
            token = line.split()
            try:
                dt = token[3] + " " + token[4]
                _compileStartTime = datetime.strptime(dt, "%Y/%m/%d %H:%M:%S.%f")
            except:
                _testmgr.mismatch_record("Compile Start Time has invalid value")
            
    if not found:
            _testmgr.mismatch_record("Compile Start Time not found")

def verifyCompileEndTime(data):
    global _testmgr
    global _compileStartTime
    global _compileEndTime

    found = False
    for line in data.splitlines():
        if line.startswith('Compile End Time'):
            found = True
            token = line.split()
            try:
                dt = token[3] + " " + token[4]
                _compileEndTime = datetime.strptime(dt, "%Y/%m/%d %H:%M:%S.%f")
            except:
                _testmgr.mismatch_record("Compile End Time has invalid value")

            if _compileStartTime > _compileEndTime:
                _testmgr.mismatch_record("Compile Start Time is later then Compile End Time")

    if not found:
            _testmgr.mismatch_record("Compile End Time not found")

def verifyCompileElapsedTime(data):
    global _testmgr
    global _compileStartTime
    global _compileEndTime

    found = False
    for line in data.splitlines():
        if line.startswith('Compile Elapsed Time'):
            found = True
            token = line.split()
            elapseTime = str(_compileEndTime - _compileStartTime)
            if token[3] != elapseTime:
                _testmgr.mismatch_record("Compile Elapse Time is not correct")

    if not found:
            _testmgr.mismatch_record("Compile Elapsed Time not found")

def verifyExecuteStartTime(data):
    global _testmgr
    global _executeStartTime

    found = False
    for line in data.splitlines():
        if line.startswith('Execute Start Time'):
            found = True
            token = line.split()
            try:
                dt = token[3] + " " + token[4]
                _executeStartTime= datetime.strptime(dt, "%Y/%m/%d %H:%M:%S.%f")
            except:
                _testmgr.mismatch_record("Execute Start Time has invalid data")

    if not found:
            _testmgr.mismatch_record("Execute Start Time not found")

def verifyExecuteEndTime(data):
    global _testmgr
    global _executeStartTime
    global _executeEndTime

    found = False
    for line in data.splitlines():
        if line.startswith('Execute End Time'):
            found = True
            token = line.split()
            try:
                dt = token[3] + " " + token[4]
                _executeEndTime= datetime.strptime(dt, "%Y/%m/%d %H:%M:%S.%f")
            except:
                _testmgr.mismatch_record("Execute End Time has invalid data")

            if _executeStartTime > _executeEndTime:
                _testmgr.mismatch_record("Execute Start Time is later then Execute End Time")

    if not found:
            _testmgr.mismatch_record("Execute End Time not found")

def verifyExecuteElapsedTime(data):
    global _testmgr
    global _executeStartTime
    global _executeEndTime

    found = False
    for line in data.splitlines():
        if line.startswith('Execute Elapsed Time'):
            found = True
            token = line.split()
            elapseTime = str(_executeEndTime- _executeStartTime)
            if token[3] != elapseTime:
                _testmgr.mismatch_record("Execute Elapse Time is not correct")

    if not found:
            _testmgr.mismatch_record("Execute Elapsed Time not found")

def verifyState(data):
    global _testmgr
    global _state

    found = False
    for line in data.splitlines():
        if line.startswith('State'):
            found = True
            token = line.split()
            if _state != token[1]:
                _testmgr.mismatch_record("State is not correct")

    if not found:
            _testmgr.mismatch_record("State not found")

def verifyRowsAffected(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Rows Affected'):
            found = True
            token = line.split()
            if int(token[2].translate(None, ',')) < -1:
                _testmgr.mismatch_record("Rows Affected has negative value")

    if not found:
            _testmgr.mismatch_record("Rows Affected not found")

def verifySQLErroeCode(data):
    global _testmgr
    global _errorCode

    found = False
    for line in data.splitlines():
        if line.startswith('SQL Error Code'):
            found = True
            token = line.split()
            if _errorCode != token[3]:
                _testmgr.mismatch_record("SQL Error Code is not correct")

    if not found:
            _testmgr.mismatch_record("SQL Error Code not found")

def verifyStatsErrorCode(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Stats Error Code'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Stats Error Code has incorrect value")
    if not found:
            _testmgr.mismatch_record("Stats Error Code not found")

def verifyQueryType(data):
    global _testmgr
    global _queryType

    found = False
    for line in data.splitlines():
        if line.startswith('Query Type'):
            found = True
            token = line.split()
            if _queryType != token[2]:
                _testmgr.mismatch_record("Query Type is not correct")

    if not found:
            _testmgr.mismatch_record("Query Type not found")

def verifySubQueryType (data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Sub Query Type '):
            found = True
    if not found:
            _testmgr.mismatch_record("Sub Query Type not found")

def verifyEstimatedAccessedRows(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Estimated Accessed Rows'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Estimated Accessed Rows has incorrect value")

    if not found:
            _testmgr.mismatch_record("Estimated Accessed Rows not found")

def verifyEstimatedUsedRows(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Estimated Used Rows'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Estimated Used Rows has incorrect value")

    if not found:
            _testmgr.mismatch_record("Estimated Used Rows not found")

def verifyParentQid(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Parent Qid'):
            found = True
    if not found:
            _testmgr.mismatch_record("Parent Qid not found")

def verifyParentQuerySystem(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Parent Query System'):
            found = True
    if not found:
            _testmgr.mismatch_record("Parent Query System not found")

def verifyChildQid(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Child Qid'):
            found = True
    if not found:
            _testmgr.mismatch_record("Child Qid not found")

def verifyNumberofSQLProcesses(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Number of SQL Processes'):
            found = True
            token = line.split()
            if int(token[4].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Number of SQL Processes has incorrect value")

    if not found:
            _testmgr.mismatch_record("Number of SQL Processes not found")

def verifyNumberofCpus(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Number of Cpus'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Number of Cpus has incorrect value")

    if not found:
            _testmgr.mismatch_record("Number of Cpus not found")

def verifyTransactionId(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Transaction Id'):
            found = True
            token = line.split()
            if int(token[2].translate(None, ',')) < -1:
                _testmgr.mismatch_record("Transaction Id has incorrect value")

    if not found:
            _testmgr.mismatch_record("Transaction Id not found")

def verifySourceString(data):
    global _testmgr
    global _sourceString

    found = False
    for line in data.splitlines():
        if line.startswith('Source String'):
            found = True
            line = line.replace('Source String', '', 1).strip();
            if _sourceString != line:
                _testmgr.mismatch_record("Source String is not correct")

    if not found:
            _testmgr.mismatch_record("Source String not found")

def verifySQLSourceLength(data):
    global _testmgr
    global _sourceString

    found = False
    for line in data.splitlines():
        if line.startswith('SQL Source Length'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("SQL Source Length is not correct")

    if not found:
            _testmgr.mismatch_record("SQL Source Length not found")

def verifyRowsReturned(data):
    global _testmgr
    global _rowsReturn

    found = False
    # "-1" means that the test does not want to verify _rowsReturn
    if _rowsReturn != "-1":
        for line in data.splitlines():
            if line.startswith('Rows Returned'):
                found = True
                token = line.split()
                if _rowsReturn != token[2]:
                    _testmgr.mismatch_record("Rows Returned is not correct")

        if not found:
            _testmgr.mismatch_record("Rows Returned not found")

def verifyFirstRowReturnedTime(data):
    global _testmgr
    global _executeStartTime
    global _executeEndTime

    found = False
    for line in data.splitlines():
        if line.startswith('First Row Returned Time'):
            found = True
            token = line.split()
            if token[4] == "-1":
                break;
            try:
                dt = token[4] + " " + token[5]
                firstRowTime= datetime.strptime(dt, "%Y/%m/%d %H:%M:%S.%f")
                if  _executeStartTime > firstRowTime or firstRowTime  > _executeEndTime:
                    _testmgr.mismatch_record("First Row Returned Time is not correct")
            except:
                _testmgr.mismatch_record("First Row Returned Time has invalid data")

    if not found:
            _testmgr.mismatch_record("First Row Returned Time not found")

def verifyLastErrorbeforeAQR(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Last Error before AQR'):
            found = True
    if not found:
            _testmgr.mismatch_record("Last Error before AQR not found")

def verifyNumberofAQRretries(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Number of AQR retries'):
            found = True
            token = line.split()
            if int(token[4].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Transaction Id has incorrect value")

    if not found:
            _testmgr.mismatch_record("Number of AQR retries not found")

def verifyDelaybeforeAQR(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Delay before AQR'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Transaction Id has incorrect value")

    if not found:
            _testmgr.mismatch_record("Delay before AQR not found")

def verifyNooftimesreclaimed(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('No. of times reclaimed'):
            found = True
            token = line.split()
            if int(token[4].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Transaction Id has incorrect value")

    if not found:
            _testmgr.mismatch_record("No. of times reclaimed not found")

def verifyCancelTime(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Cancel Time'):
            found = True
            token = line.split()

    if not found:
            _testmgr.mismatch_record("Cancel Time not found")

def verifyLastSuspendTime(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Last Suspend Time'):
            found = True

    if not found:
            _testmgr.mismatch_record("Last Suspend Time not found")

def verifyStatsCollectionType(data):
    global _testmgr
    global _statsCollectType

    found = False
    for line in data.splitlines():
        if line.startswith('Stats Collection Type'):
            found = True
            token = line.split()
            if token[3] != _statsCollectType:
                _testmgr.mismatch_record("Stats Collection Type has incorrect value")

    if not found:
            _testmgr.mismatch_record("Stats Collection Type not found")

def verifySQLProcessBusyTime(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('SQL Process Busy Time'):
            found = True
            token = line.split()
            if int(token[4].translate(None, ',')) < 0:
                _testmgr.mismatch_record("SQL Process Busy Time has incorrect value")

    if not found:
            _testmgr.mismatch_record("SQL Process Busy Time not found")

def verifyUDRProcessBusyTime(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('UDR Process Busy Time'):
            found = True
            token = line.split()
            if int(token[4].translate(None, ',')) < 0:
                _testmgr.mismatch_record("UDR Process Busy Time has incorrect value")

    if not found:
            _testmgr.mismatch_record("UDR Process Busy Time not found")

def verifySQLSpaceAllocated(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('SQL Space Allocated'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("SQL Space Allocated has incorrect value")

    if not found:
            _testmgr.mismatch_record("SQL Space Allocated not found")

def verifySQLSpaceUsed(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('SQL Space Used'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("SQL Space Used has incorrect value")

    if not found:
            _testmgr.mismatch_record("SQL Space Used not found")

def verifySQLHeapAllocated(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('SQL Heap Allocated'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("SQL Heap Allocated has incorrect value")

    if not found:
            _testmgr.mismatch_record("SQL Heap Allocated not found")

def verifySQLHeapUsed(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('SQL Heap Used'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("SQL Heap Used has incorrect value")

    if not found:
            _testmgr.mismatch_record("SQL Heap Used not found")

def verifyEIDSpaceAllocated(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('EID Space Allocated'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("EID Space Allocated has incorrect value")

    if not found:
            _testmgr.mismatch_record("EID Space Allocated not found")

def verifyEIDSpaceUsed(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('EID Space Used'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("EID Space Used has incorrect value")

    if not found:
            _testmgr.mismatch_record("EID Space Used not found")

def verifyEIDHeapAllocated(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('EID Heap Allocated'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("EID Heap Allocated has incorrect value")

    if not found:
            _testmgr.mismatch_record("EID Heap Allocated not found")

def verifyEIDHeapUsed(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('EID Heap Used'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("EID Heap Used has incorrect value")

    if not found:
            _testmgr.mismatch_record("EID Heap Used not found")

def verifyProcessesCreated(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Processes Created'):
            found = True
            token = line.split()
            if int(token[2].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Processes Created has incorrect value")

    if not found:
            _testmgr.mismatch_record("Processes Created not found")

def verifyProcessCreateTime(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Process Create Time'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Process Create Time has incorrect value")

    if not found:
            _testmgr.mismatch_record("Process Create Time not found")

def verifyRequestMessageCount(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Request Message Count'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Request Message Count has incorrect value")

    if not found:
            _testmgr.mismatch_record("Request Message Count not found")

def verifyRequestMessageBytes(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Request Message Bytes'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Request Message Bytes has incorrect value")

    if not found:
            _testmgr.mismatch_record("Request Message Bytes not found")

def verifyReplyMessageCount(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Reply Message Count'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Reply Message Count has incorrect value")

    if not found:
            _testmgr.mismatch_record("Reply Message Count not found")

def verifyReplyMessageBytes(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Reply Message Bytes'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Reply Message Bytes has incorrect value")

    if not found:
            _testmgr.mismatch_record("Reply Message Bytes not found")

def verifyScrOverflowMode(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Scr. Overflow Mode'):
            found = True
    if not found:
            _testmgr.mismatch_record("Scr. Overflow Mode not found")

def verifyScrFileCount(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Scr File Count'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Scr File Count has incorrect value")

    if not found:
            _testmgr.mismatch_record("Scr File Count not found")

def verifyScrBufferBlkSize(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Scr. Buffer Blk Size'):
            found = True
            token = line.split()
            if int(token[4].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Scr. Buffer Blk Size has incorrect value")

    if not found:
            _testmgr.mismatch_record("Scr. Buffer Blk Size not found")

def verifyScrBufferBlksRead(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Scr. Buffer Blks Read'):
            found = True
            token = line.split()
            if int(token[4].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Scr. Buffer Blks Read has incorrect value")

    if not found:
            _testmgr.mismatch_record("Scr. Buffer Blks Read not found")

def verifyScrBufferBlksWritten(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Scr. Buffer Blks Written'):
            found = True
            token = line.split()
            if int(token[4].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Scr. Buffer Blks Written has incorrect value")

    if not found:
            _testmgr.mismatch_record("Scr. Buffer Blks Written not found")

def verifyScrReadCount(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Scr. Read Count'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Scr. Read Count has incorrect value")

    if not found:
            _testmgr.mismatch_record("Scr. Read Count not found")

def verifyScrWriteCount(data):
    global _testmgr
    found = False
    for line in data.splitlines():
        if line.startswith('Scr. Write Count'):
            found = True
            token = line.split()
            if int(token[3].translate(None, ',')) < 0:
                _testmgr.mismatch_record("Scr. Write Count has incorrect value")

    if not found:
            _testmgr.mismatch_record("Scr. Write Count not found")

