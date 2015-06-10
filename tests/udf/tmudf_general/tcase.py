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

_testmgr = None
_testlist = []
_dci = None

# This testcase verifies UDF invocation

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()

def test001(desc="""create and drop"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # create library with non-existing file
    stmt = """create library mytest file 'does not exist';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1382')

    # drop a library that does not exist
    stmt = """drop library doesnotexist cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1389')

    # create TMUDF with non-existing libary
    stmt = """create table_mapping function fake_func
(test_what char(100),
test_parm char(100))
external name 'FAKE_FUNC'
language cpp
library doesnotexist;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1389')

    # create TMUDF with a schema that does not exist
    stmt = """create table_mapping function doesnotexist.fake_func
(test_what char(100),
test_parm char(100))
external name 'DOESNOTEXIST.FAKE_FUNC'
language cpp
library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1003')

    # function name should be case insensitive.  This should work.
    stmt = """create table_mapping function MyTmUdF
(test_what char(100),
test_parm char(100))
external name 'QA_TMUDF'
language cpp
library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from
UDF(mYtMuDf(TABLE(select * from myShortTable),
'TEST_RUNTIME_EMIT_X_ROWS', '1')) 
t1, myShortTable t2 """ + defs.myShortTableEqualPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    stmt = """drop table_mapping function mYtmuDf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # External name should be case sensitive.  The actualy name is 'QA_TMUDF'.
    # specfy the lower case name should get an error.
    stmt = """create table_mapping function mytmudf
(test_what char(100),
test_parm char(100))
external name 'qa_tmudf'
language cpp
library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '11246')

    stmt = """drop table_mapping function mytmudf;"""
    output = _dci.cmdexec(stmt)

    # Missing 'language cpp' attribute is OK.  SQL will figure it out by 
    # the file suffix itself.
    stmt = """create table_mapping function mytmudf
(test_what char(100),
test_parm char(100))
external name 'QA_TMUDF'
library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from
UDF(mytmudf(TABLE(select * from myShortTable),
'TEST_RUNTIME_EMIT_X_ROWS', '1')) 
t1, myShortTable t2 """ + defs.myShortTableEqualPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    stmt = """drop table_mapping function mytmudf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # QA_TMUDF is a C++ UDF, there is no java UDF with this name.  
    # 'language java' should get an error saying that it is not found.
    stmt = """create table_mapping function mytmudf
(test_what char(100),
test_parm char(100))
external name 'QA_TMUDF'
language java
library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '11205')

    stmt = """drop table_mapping function mytmudf;"""
    output = _dci.cmdexec(stmt)

    # 'language c' for TMUDF should get an error.  It is not supported.
    stmt = """create table_mapping function mytmudf
(test_what char(100),
test_parm char(100))
external name 'QA_TMUDF'
language c
library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3286')

    stmt = """drop table_mapping function mytmudf;"""
    output = _dci.cmdexec(stmt)

    # Create a function with 2 paarmeter, but call it with:
    # 1 parameter -> this is not an error by dfault, but QA TMUDF does
    #                catch it internally.
    # 3 parameters -> this is not an error by default, but QA_TMUDF does
    #                 catch it internally.
    # 2 tables -> this is a syntax error
    # no table -> this is not an error by default, but QA_TMUDF does
    #             catch it internally.
    # passing int for char parameters -> this is not an error by default,
    #                 but QA_TMUDF implementation does catch it internally.
    stmt = """create table_mapping function mytmudf
(test_what char(100),
test_parm char(100))
external name 'QA_TMUDF'
language cpp
library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # passing only 1 parameter with 2 parameters defined
    stmt = """select * from
UDF(mytmudf(TABLE(select * from myShortTable), 'parm1'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # passing 3 parameters with 2 parameters defined.  
    stmt = """select * from
UDF(mytmudf(TABLE(select * from myShortTable), 'parm1', 'parm2', 'parm3'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # passing 2 tables.  This is a syntax error
    stmt = """select * from
UDF(mytmudf(
TABLE(select * from myShortTable), TABLE(select * from myShortTable),
'parm1', 'parm2'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # passing no table
    # QA_TMUDF is implemented to catch this.
    stmt = """select * from UDF(mytmudf('parm1', 'parm2'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # passing ints for characters. 
    # QA_TMUDF is implemented to catch this.
    stmt = """select * from UDF(mytmudf(TABLE(select * from myShortTable), 1, 2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    stmt = """drop table_mapping function mytmudf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # create TMUDF with an external name that does not exist
    stmt = """create table_mapping function doesnotexist.fake_func
(test_what char(100),
test_parm char(100))
external name 'FAKE_FUNC'
language cpp
library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1003')

    # create TMUDF with an external name that does not exist
    stmt = """create table_mapping function doesnotexist.fake_func
(test_what char(100),
test_parm char(100))
external name 'FAKE_FUNC'
language cpp
library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1003')

    # drop TMUDF with a name that does not exist
    stmt = """drop table_mapping function doesnotexist;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1389')

    # drop TMUDF with a schema that does not exist
    stmt = """drop table_mapping function doesnotexist.fake_func;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1389')

    # create TMUDF in a different schema
    stmt = """create table_mapping function """ + defs.my_schema1 + """.mytmudf
(test_what char(100),
test_parm char(100))
external name 'QA_TMUDF'
language cpp
library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # make sure that the TMUDF exists
    stmt = """get table_mapping functions for library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, defs.my_schema1_no_cat + '.MYTMUDF', True)

    # drop TUDF in a different schema. Should fail with the current schema
    stmt = """drop table_mapping function mytmudf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1389')

    # make sure that the TMUDF exists
    stmt = """get table_mapping functions for library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, defs.my_schema1_no_cat + '.MYTMUDF', True)

    # drop TMUDF in a different schema. Should work.
    stmt = """drop table_mapping function """ + defs.my_schema1 + """.mytmudf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # make sure that the TMUDF does not exist.
    stmt = """get table_mapping functions for library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, defs.my_schema1_no_cat + '.MYTMUDF', True)

    _testmgr.testcase_end(desc)

def test002(desc="""input parm/table column data and types"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Parameter data and types
    stmt = """select * from
UDF(qaTmudfInParms(TABLE(select * from myFullTable),
'TEST_RUNTIME_IN_PARM_DATA_AND_TYPES', '37',
'2', '3', '4', '5', '6', '7', '8', '9', '10',
_ucs2'11', _ucs2'12', _ucs2'13', _ucs2'14', _ucs2'15', _ucs2'16',
17.17, 18.18, 19.19, 20.20,
21, 22, 23, 24, 25, 26, 27, 28,
date '2029-01-01', time '01:01:30', time '01:01:31.12345',
timestamp '2032-01-01 01:01:32.123456', timestamp '2033-01-01 01:01:33.12345',
interval '34-01' year to month, '35', '36'
)) t1, myFullTable t2 """ + defs.myFullTableEqualPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    # Input table column data and types
    stmt = """select * from
UDF(qaTmudfGeneral(TABLE(select * from myFullPositionTable),
'TEST_RUNTIME_IN_TABLE_DATA_AND_TYPES', '35'
)) t1, myFullPositionTable t2 """ + defs.myFullPositionTableEqualPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    _testmgr.testcase_end(desc)

def test003(desc="""input parm/table column names and indexes"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Parameter names and indexes
    stmt = """select * from UDF(qaTmudfInParms(TABLE(select * from myFullTable),
'TEST_RUNTIME_IN_PARM_NAMES_AND_INDEXES', '37',
'2', '3', '4', '5', '6', '7', '8', '9', '10',
_ucs2'11', _ucs2'12', _ucs2'13', _ucs2'14', _ucs2'15', _ucs2'16',
17.17, 18.18, 19.19, 20.20,
21, 22, 23, 24, 25, 26, 27, 28,
date '2029-01-01', time '01:01:30', time '01:01:31.12345',
timestamp '2032-01-01 01:01:32.123456', timestamp '2033-01-01 01:01:33.12345',
interval '34-01' year to month, '35', '36'
)) t1, myFullTable t2 """ + defs.myFullTableEqualPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    # Input table column names and indexes
    stmt = """select * from
UDF(qaTmudfGeneral(TABLE(select * from myFullTable),
'TEST_RUNTIME_IN_TABLE_NAMES_AND_INDEXES', '35'
)) t1, myFullTable t2 """ + defs.myFullTableEqualPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    _testmgr.testcase_end(desc)

def test004(desc="""output table DDL and data"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Define the output table DDL from the compiler interface using
    # UDRInvocationInfo.addPassThruColumns() and copy the data using
    # UDRInvocationInfo.copyPassThruData()
    stmt = """select * from UDF(qaTmudfGeneral(TABLE(select * from myFullTable),
'TEST_CMPTIME_RUNTIME_OUT_TABLE_DEFINED_USING_PASSTHRU', '35'
)) t1, myFullTable t2 """ + defs.myFullTableEqualPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    # test null values as well
    stmt = """select * from UDF(qaTmudfGeneral(TABLE(select * from myFullTable),
'TEST_CMPTIME_RUNTIME_OUT_TABLE_DEFINED_USING_PASSTHRU', '35'
)) t1 """ + defs.myFullTableIsNullPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    # Define the output table DDL from the compiler interface using
    # UDRInvocationInfo.out().addColumn() and copy the data using
    # UDRInvocationInfo.out().setXXX()
    stmt = """select * from UDF(qaTmudfGeneral(TABLE(select * from myFullTable),
'TEST_CMPTIME_RUNTIME_OUT_TABLE_DEFINED_USING_SET', '35'
)) t1, myFullTable t2 """ + defs.myFullTableEqualPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    # test null values as well
    stmt = """select * from UDF(qaTmudfGeneral(TABLE(select * from myFullTable),
'TEST_CMPTIME_RUNTIME_OUT_TABLE_DEFINED_USING_SET', '35'
)) t1 """ + defs.myFullTableIsNullPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    # Define the output table DDL using the TMUDF output parms
    # and copy the data using UDRInvocationInfo.out().setXXX()
    stmt = """select * from 
UDF(qaTmudfOutParms(TABLE(select * from myFullTable),
'TEST_RUNTIME_OUT_TABLE_DEFINED_USING_PARMS', '35'
)) t1, myFullTable t2 """ + defs.myFullTableEqualPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    # test null values as well
    stmt = """select * from
UDF(qaTmudfOutParms(TABLE(select * from myFullTable),
'TEST_RUNTIME_OUT_TABLE_DEFINED_USING_PARMS', '35'
)) t1 """ + defs.myFullTableIsNullPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    _testmgr.testcase_end(desc)

def test005(desc="""delete output table columns"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # delete columns by index
    stmt = """select * from
UDF(qaTmudfOutParmsWithExtras(TABLE(select * from myFullTable),
'TEST_CMPTIME_RUNTIME_OUT_TABLE_DELETE_COLUMNS_BY_INDEX', '35'
)) t1, myFullTable t2 """ + defs.myFullTableEqualPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    # delete columns by name
    stmt = """select * from
UDF(qaTmudfOutParmsWithExtras(TABLE(select * from myFullTable),
'TEST_CMPTIME_RUNTIME_OUT_TABLE_DELETE_COLUMNS_BY_NAME', '35'
)) t1, myFullTable t2 """ + defs.myFullTableEqualPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    _testmgr.testcase_end(desc)

def test006(desc="""compile time exception"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # compile time exception
    stmt = """select * from
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_CMPTIME_EXCEPTION', '12345'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    _dci.expect_any_substr(output, '12345')

    # compile time exception
    stmt = """select * from 
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_CMPTIME_EXCEPTION', '54321'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    _dci.expect_any_substr(output, '54321')

    _testmgr.testcase_end(desc)

def test007(desc="""run time exception"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # runtime exception
    stmt = """select * from 
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_RUNTIME_EXCEPTION', '12345'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    _dci.expect_any_substr(output, '12345')

    # runtime exception
    stmt = """select * from 
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_RUNTIME_EXCEPTION', '54321'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    _dci.expect_any_substr(output, '54321')

    _testmgr.testcase_end(desc)

def test008(desc="""compile time interface invocation"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # This test go through the compiler interfaces to make sure that they
    # are invoked by SQL.

    # qaTmudfGeneral() raises an exception 99999 when the function is invoked, hence
    # we can expect the 'man-made' error here.
    stmt = """select * from
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_CMPTIME_INTERFACE_INVOKED', 'describeDataflow'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    _dci.expect_any_substr(output, '99999')
    _dci.expect_any_substr(output, 'Compiler time interface describeDataflow() is invoked')

    stmt = """select * from
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_CMPTIME_INTERFACE_INVOKED', 'describeConstraints'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    _dci.expect_any_substr(output, '99999')
    _dci.expect_any_substr(output, 'Compiler time interface describeConstraints() is invoked')

    stmt = """select * from
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_CMPTIME_INTERFACE_INVOKED', 'describeStatistics'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    _dci.expect_any_substr(output, '99999')
    _dci.expect_any_substr(output, 'Compiler time interface describeStatistics() is invoked')

    stmt = """select * from
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_CMPTIME_INTERFACE_INVOKED', 'describeDesiredDegreeOfParallelism'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    _dci.expect_any_substr(output, '99999')
    _dci.expect_any_substr(output, 'Compiler time interface describeDesiredDegreeOfParallelism() is invoked')

    stmt = """select * from
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_CMPTIME_INTERFACE_INVOKED', 'describePlanProperties'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    _dci.expect_any_substr(output, '99999')
    _dci.expect_any_substr(output, 'Compiler time interface describePlanProperties() is invoked')

    stmt = """select * from
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_CMPTIME_INTERFACE_INVOKED', 'completeDescription'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    _dci.expect_any_substr(output, '99999')
    _dci.expect_any_substr(output, 'Compiler time interface completeDescription() is invoked')

    _testmgr.testcase_end(desc)

def test009(desc="""explain"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare xx from select * from
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_RUNTIME_EMIT_X_ROWS', '1')) XO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, 'tmudf')
    _dci.expect_any_substr(output, 'XO')

    stmt = """explain xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # TMUDF_name ............. XO
    _dci.expect_any_substr(output, 'TMUDF_name')
    _dci.expect_any_substr(output, 'XO')
    # input_parameters ....... TEST_WHAT, TEST_PARM
    _dci.expect_any_substr(output, 'input_parameters')    
    _dci.expect_any_substr(output, 'TEST_WHAT')
    _dci.expect_any_substr(output, 'TEST_PARM')
    # external_name .......... QA_TMUDF
    _dci.expect_any_substr(output, 'external_name')
    _dci.expect_any_substr(output, 'QA_TMUDF')
    # external_file .......... qaTmudfTest.so
    _dci.expect_any_substr(output, 'external_file')
    _dci.expect_any_substr(output, 'qaTmudfTest.so')
    # actual_parameters ...... 'TEST_RUNTIME_EMIT_X_ROWS', '1'
    _dci.expect_any_substr(output, 'actual_parameters')
    _dci.expect_any_substr(output, 'TEST_RUNTIME_EMIT_X_ROWS')

    _testmgr.testcase_end(desc)

def test010(desc="""degree of parallelism"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # It's OK to see 11153 error.  Not all degrees of parallelsim can produce
    # a plan.  If an error is reurned at the prepare state, the test won't
    # continue
    stmt = """prepare xx from select * from
UDF(qaTmudfGeneral(TABLE(select * from myFullTable),
'TEST_CMPTIME_DEGREE_OF_PARALLELISM', 'ANY_DEGREE_OF_PARALLELISM'));"""
    output = _dci.cmdexec(stmt)
    if not """ERROR[11153] Unable to produce a query plan""" in output:
       _dci.expect_prepared_msg(output)

       stmt = """explain options 'f' xx;"""
       output = _dci.cmdexec(stmt)
       _dci.expect_complete_msg(output)

       stmt = """execute xx;"""
       output = _dci.cmdexec(stmt)
       _dci.expect_selected_msg(output, 5)

    stmt = """prepare xx from select * from
UDF(qaTmudfGeneral(TABLE(select * from myFullTable),
'TEST_CMPTIME_DEGREE_OF_PARALLELISM', 'DEFAULT_DEGREE_OF_PARALLELISM'));"""
    output = _dci.cmdexec(stmt)
    if not """ERROR[11153] Unable to produce a query plan""" in output:
        _dci.expect_prepared_msg(output)

        stmt = """explain options 'f' xx;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)

        stmt = """execute xx;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output, 5)

    stmt = """prepare xx from select * from
UDF(qaTmudfGeneral(TABLE(select * from myFullTable),
'TEST_CMPTIME_DEGREE_OF_PARALLELISM', 'MAX_DEGREE_OF_PARALLELISM'));"""
    output = _dci.cmdexec(stmt)
    if not """ERROR[11153] Unable to produce a query plan""" in output:
        _dci.expect_prepared_msg(output)

        stmt = """explain options 'f' xx;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)

        stmt = """execute xx;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output, 5)

    stmt = """prepare xx from select * from
UDF(qaTmudfGeneral(TABLE(select * from myFullTable),
'TEST_CMPTIME_DEGREE_OF_PARALLELISM', 'ONE_INSTANCE_PER_NODE'));"""
    output = _dci.cmdexec(stmt)
    if not """ERROR[11153] Unable to produce a query plan""" in output:
        _dci.expect_prepared_msg(output)

        stmt = """explain options 'f' xx;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)

        stmt = """execute xx;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output, 5)

    _testmgr.testcase_end(desc)

def test011(desc="""insert/delete/update"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """insert into
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_RUNTIME_EMIT_X_ROWS', '0')) (select * from myShortTable);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')   
 
    stmt = """delete from
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_RUNTIME_EMIT_X_ROWS', '0'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """update
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_RUNTIME_EMIT_X_ROWS', '0')) set c_integer=1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    _testmgr.testcase_end(desc)

def test012(desc="""select"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # TMUDF emits 0 rows, all columns
    stmt = """select * from 
UDF(qaTmudfGeneral(TABLE(select * from myFullTable),
'TEST_RUNTIME_EMIT_X_ROWS', '0'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    # TMUDF emits 1x4 rows, only 2 columns
    stmt = """select c_integer, c_char from
UDF(qaTmudfGeneral(TABLE(select * from myFullTable),
'TEST_RUNTIME_EMIT_X_ROWS', '1'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 5)

    # TMUDF emits 1x4 rows, with a where clause, 
    # only 2 columns, with predicates
    stmt = """select c_integer, c_char from
UDF(qaTmudfGeneral(TABLE(select * from myFullTable),
'TEST_RUNTIME_EMIT_X_ROWS', '1')) where c_integer = -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    # TMUDF emits 1x4 rows, only 2 columns, with predicates, with join
    stmt = """select t1.c_integer, t1.c_char, t2.c_integer, t2.c_char from
UDF(qaTmudfGeneral(TABLE(select * from myFullTable),
'TEST_RUNTIME_EMIT_X_ROWS', '1')) t1,
UDF(qaTmudfGeneral(TABLE(select * from myFullTable),
'TEST_RUNTIME_EMIT_X_ROWS', '1')) t2 """ + defs.myFullTableEqualPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    # TMUDF emits 10000000x4 rows. Use myShortTable in this test.
    # myFullTable has lob data in it.  With this large number of rows, the 
    # amount of data is too time consuming.
    stmt = """select count(*) from
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_RUNTIME_EMIT_X_ROWS', '10000000'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '40000000')
    _dci.expect_selected_msg(output, 1)

    _testmgr.testcase_end(desc)

def test013(desc="""partition by"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """select * from UDF(qaTmudfGeneral(TABLE(select * from myFullPositionTable
partition by
C00_CHAR, C01_CHAR, C02_CHAR, C03_VARCHAR, C04_VARCHAR, C05_VARCHAR,
C06_VARCHAR, C07_VARCHAR, C08_VARCHAR, C09_CHAR, C10_CHAR, C11_CHAR,
C12_VARCHAR, C13_VARCHAR, C14_VARCHAR, C15_NUMERIC, C16_NUMERIC_UNSIGNED,
C17_DECIMAL_LSE, C18_DECIMAL_UNSIGNED, C19_INT, C20_INT_UNSIGNED, C21_LARGEINT,
C22_SMALLINT, C23_SMALLINT_UNSIGNED, C24_DOUBLE_PRECISION, C25_REAL,
C26_DOUBLE_PRECISION, C27_DATE, C28_TIME, C29_TIME, C30_TIMESTAMP,
C31_TIMESTAMP, C32_INTERVAL, C33_VARCHAR, C34_VARCHAR
),
'TEST_CMPTIME_RUNTIME_IN_OUT_TABLE_PARTITIONING', '35'
)) t1, myFullPositionTable t2 """ + defs.myFullPositionTableEqualPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    _testmgr.testcase_end(desc)

def test014(desc="""order by"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """select * from UDF(qaTmudfGeneral(TABLE(select * from myFullPositionTable
order by
C00_CHAR, C01_CHAR, C02_CHAR, C03_VARCHAR, C04_VARCHAR, C05_VARCHAR,
C06_VARCHAR, C07_VARCHAR, C08_VARCHAR, C09_CHAR, C10_CHAR, C11_CHAR,
C12_VARCHAR, C13_VARCHAR, C14_VARCHAR, C15_NUMERIC, C16_NUMERIC_UNSIGNED,
C17_DECIMAL_LSE, C18_DECIMAL_UNSIGNED, C19_INT, C20_INT_UNSIGNED, C21_LARGEINT,
C22_SMALLINT, C23_SMALLINT_UNSIGNED, C24_DOUBLE_PRECISION, C25_REAL,
C26_DOUBLE_PRECISION, C27_DATE, C28_TIME, C29_TIME, C30_TIMESTAMP,
C31_TIMESTAMP, C32_INTERVAL, C33_VARCHAR, C34_VARCHAR
),
'TEST_CMPTIME_RUNTIME_IN_OUT_TABLE_ORDERING', '35' 
)) t1, myFullPositionTable t2 """ + defs.myFullPositionTableEqualPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    _testmgr.testcase_end(desc)

def test015(desc="""misc"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Verify UDRInvocationInfo::getUDRName()
    stmt = """select * from 
UDF(qaTmudfGeneral(TABLE(select * from myShortTable),
'TEST_CMPTIME_MISC_GETUDRNAME', 
'""" + defs.my_schema.upper() + """.""" + 'qaTmudfGeneral'.upper() + """'))
t1, myShortTable t2 """ + defs.myShortTableEqualPreds + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    _testmgr.testcase_end(desc)
