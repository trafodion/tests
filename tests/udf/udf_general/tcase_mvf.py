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
   
def test001(desc="""UDF (MVF) input/output data types"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # These UDFs return the same values, so the output with or without
    # UDF should be the same if the data types are handled properly.
    stmt = """create table myFullDoubleWideTableNew like myFullDoubleWideTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into myFullDoubleWideTableNew (select
qa_udf_char_mvf(c_char),
qa_udf_char_upshift_mvf(c_char_upshift),
qa_udf_char_not_casespecific_mvf(c_char_not_casespecific),
qa_udf_char_varying_mvf(c_char_varying),
qa_udf_char_varying_upshift_mvf(c_char_varying_upshift),
qa_udf_char_varying_not_casespecific_mvf(c_char_varying_not_casespecific),
qa_udf_varchar_mvf(c_varchar),
qa_udf_varchar_upshift_mvf(c_varchar_upshift),
qa_udf_varchar_not_casespecific_mvf(c_varchar_not_casespecific),
qa_udf_nchar_mvf(c_nchar),
qa_udf_nchar_upshift_mvf(c_nchar_upshift),
qa_udf_nchar_not_casespecific_mvf(c_nchar_not_casespecific),
qa_udf_nchar_varying_mvf(c_nchar_varying),
qa_udf_nchar_varying_upshift_mvf(c_nchar_varying_upshift),
qa_udf_nchar_varying_not_casespecific_mvf(c_nchar_varying_not_casespecific),
qa_udf_numeric_mvf(c_numeric),
qa_udf_numeric_unsigned_mvf(c_numeric_unsigned),
qa_udf_decimal_mvf(c_decimal),
qa_udf_decimal_unsigned_mvf(c_decimal_unsigned),
qa_udf_integer_mvf(c_integer),
qa_udf_integer_unsigned_mvf(c_integer_unsigned),
qa_udf_largeint_mvf(c_largeint),
qa_udf_smallint_mvf(c_smallint),
qa_udf_smallint_unsigned_mvf(c_smallint_unsigned),
qa_udf_float_mvf(c_float),
qa_udf_real_mvf(c_real),
qa_udf_double_precision_mvf(c_double_precision),
qa_udf_date_mvf(c_date),
qa_udf_time_mvf(c_time),
qa_udf_time5_mvf(c_time5),
qa_udf_timestamp_mvf(c_timestamp),
qa_udf_timestamp5_mvf(c_timestamp5)
-- BUG this crashes mxosrvr right now LP#1441378: qa_udf_clob_mvf(c_clob),
-- BUG this crashes mxosrvr right now LP#1441378: qa_udf_blob_mvf(c_blob)
from myFullTable);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """select * from myFullDoubleWideTableNew t1, myFullDoubleWideTable t2 where
t1.c_char1 = t2.c_char1 and
t1.c_char2 =  t2.c_char2 and
t1.c_char_upshift1 = t2.c_char_upshift1 and
t1.c_char_upshift2 = t2.c_char_upshift2 and
t1.c_char_not_casespecific1 = t2.c_char_not_casespecific1 and
t1.c_char_not_casespecific2 = t2.c_char_not_casespecific2 and
t1.c_char_varying1 = t2.c_char_varying1 and
t1.c_char_varying2 = t2.c_char_varying2 and
t1.c_char_varying_upshift1 = t2.c_char_varying_upshift1 and
t1.c_char_varying_upshift2 = t2.c_char_varying_upshift2 and
t1.c_char_varying_not_casespecific1 = t2.c_char_varying_not_casespecific1 and
t1.c_char_varying_not_casespecific2 = t2.c_char_varying_not_casespecific2 and
t1.c_varchar1 = t2.c_varchar1 and
t1.c_varchar2 = t2.c_varchar2 and
t1.c_varchar_upshift1 = t2.c_varchar_upshift1 and
t1.c_varchar_upshift2 = t2.c_varchar_upshift2  and
t1.c_varchar_not_casespecific1 = t2.c_varchar_not_casespecific1 and
t1.c_varchar_not_casespecific2 = t2.c_varchar_not_casespecific2 and
t1.c_nchar1 = t2.c_nchar1 and
t1.c_nchar2 = t2.c_nchar2 and
t1.c_nchar_upshift1 = t2.c_nchar_upshift1 and
t1.c_nchar_upshift2 = t2.c_nchar_upshift2 and
t1.c_nchar_not_casespecific1 = t2.c_nchar_not_casespecific1 and
t1.c_nchar_not_casespecific2 = t2.c_nchar_not_casespecific2 and
t1.c_nchar_varying1 = t2.c_nchar_varying1 and
t1.c_nchar_varying2 = t2.c_nchar_varying2 and
t1.c_nchar_varying_upshift1 = t2.c_nchar_varying_upshift1 and
t1.c_nchar_varying_upshift2 = t2.c_nchar_varying_upshift2 and
t1.c_nchar_varying_not_casespecific1 = t2.c_nchar_varying_not_casespecific1 and
t1.c_nchar_varying_not_casespecific2 = t2.c_nchar_varying_not_casespecific2 and
t1.c_numeric1 = t2.c_numeric1 and
t1.c_numeric2 = t2.c_numeric2 and
t1.c_numeric_unsigned1 = t2.c_numeric_unsigned1 and
t1.c_numeric_unsigned2 = t2.c_numeric_unsigned2 and
t1.c_decimal1 = t2.c_decimal1 and
t1.c_decimal2 = t2.c_decimal2 and
t1.c_decimal_unsigned1 = t2.c_decimal_unsigned1 and
t1.c_decimal_unsigned2 = t2.c_decimal_unsigned2 and
t1.c_integer1 = t2.c_integer1 and
t1.c_integer2 = t2.c_integer2 and
t1.c_integer_unsigned1 = t2.c_integer_unsigned1 and
t1.c_integer_unsigned2 = t2.c_integer_unsigned2 and
t1.c_largeint1 = t2.c_largeint1 and
t1.c_largeint2 = t2.c_largeint2 and
t1.c_smallint1 = t2.c_smallint1 and
t1.c_smallint2 = t2.c_smallint2 and
t1.c_smallint_unsigned1 = t2.c_smallint_unsigned1 and
t1.c_smallint_unsigned2 = t2.c_smallint_unsigned2 and
t1.c_float1 = t2.c_float1 and
t1.c_float2 = t2.c_float2 and
t1.c_real1 = t2.c_real1 and
t1.c_real2 = t2.c_real2 and
t1.c_double_precision1 = t2.c_double_precision1 and
t1.c_double_precision2 = t2.c_double_precision2 and
t1.c_date1 = t2.c_date1 and
t1.c_date2 = t2.c_date2 and
t1.c_time1 = t2.c_time1 and
t1.c_time2 = t2.c_time2 and
t1.c_time51 = t2.c_time51 and
t1.c_time52 = t2.c_time52 and
t1.c_timestamp1 = t2.c_timestamp1 and
t1.c_timestamp2 = t2.c_timestamp2 and
t1.c_timestamp51 = t2.c_timestamp51 and
t1.c_timestamp52 = t2.c_timestamp52
-- BUG this crashes mxosrvr right now LP#1441378: t1.c_clob1 = t2.c_clob1 and
-- BUG this crashes mxosrvr right now LP#1441378: t1.c_clob2 = t2.c_clob2 and
-- BUG this crashes mxosrvr right now LP#1441378: t1.c_blob1 = t2.c_blob1 and
-- BUG this crashes mxosrvr right now LP#1441378: t1.c_blob2 = t2.c_blob2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    stmt = """select * from myFullDoubleWideTableNew t1 where
t1.c_char1 is null and
t1.c_char2 is null and
t1.c_char_upshift1 is null and
t1.c_char_upshift2 is null and
t1.c_char_not_casespecific1 is null and
t1.c_char_not_casespecific2 is null and
t1.c_char_varying1 is null and
t1.c_char_varying2 is null and
t1.c_char_varying_upshift1 is null and
t1.c_char_varying_upshift2 is null and
t1.c_char_varying_not_casespecific1 is null and
t1.c_char_varying_not_casespecific2 is null and
t1.c_varchar1 is null and
t1.c_varchar2 is null and
t1.c_varchar_upshift1 is null and
t1.c_varchar_upshift2 is null  and
t1.c_varchar_not_casespecific1 is null and
t1.c_varchar_not_casespecific2 is null and
t1.c_nchar1 is null and
t1.c_nchar2 is null and
t1.c_nchar_upshift1 is null and
t1.c_nchar_upshift2 is null and
t1.c_nchar_not_casespecific1 is null and
t1.c_nchar_not_casespecific2 is null and
t1.c_nchar_varying1 is null and
t1.c_nchar_varying2 is null and
t1.c_nchar_varying_upshift1 is null and
t1.c_nchar_varying_upshift2 is null and
t1.c_nchar_varying_not_casespecific1 is null and
t1.c_nchar_varying_not_casespecific2 is null and
t1.c_numeric1 is null and
t1.c_numeric2 is null and
t1.c_numeric_unsigned1 is null and
t1.c_numeric_unsigned2 is null and
t1.c_decimal1 is null and
t1.c_decimal2 is null and
t1.c_decimal_unsigned1 is null and
t1.c_decimal_unsigned2 is null and
t1.c_integer1 is null and
t1.c_integer2 is null and
t1.c_integer_unsigned1 is null and
t1.c_integer_unsigned2 is null and
t1.c_largeint1 is null and
t1.c_largeint2 is null and
t1.c_smallint1 is null and
t1.c_smallint2 is null and
t1.c_smallint_unsigned1 is null and
t1.c_smallint_unsigned2 is null and
t1.c_float1 is null and
t1.c_float2 is null and
t1.c_real1 is null and
t1.c_real2 is null and
t1.c_double_precision1 is null and
t1.c_double_precision2 is null and
t1.c_date1 is null and
t1.c_date2 is null and
t1.c_time1 is null and
t1.c_time2 is null and
t1.c_time51 is null and
t1.c_time52 is null and
t1.c_timestamp1 is null and
t1.c_timestamp2 is null and
t1.c_timestamp51 is null and
t1.c_timestamp52 is null
-- BUG this crashes mxosrvr right now LP#1441378: t1.c_clob1 is null and
-- BUG this crashes mxosrvr right now LP#1441378: t1.c_clob2 is null and
-- BUG this crashes mxosrvr right now LP#1441378: t1.c_blob1 is null and
-- BUG this crashes mxosrvr right now LP#1441378: t1.c_blob2 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """drop table myFullDoubleWideTableNew cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test002(desc="""UDF (MVF) names"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # UDF name case insensitive
    stmt = """select qa_udf_integer_mvf(b) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer_mvf(B) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select Qa_UdF_InTeGeR_MvF(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer_mvf(b) from myview;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer_mvf(B) from myview;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qA_uDf_iNtEgEr_mVf(a) from myview;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # UDF name syntax
    # UDF does not exist
    stmt = """select abcd(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4450')
    
    # UDF does not exist
    stmt = """select abcd1(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4450')
    
    # syntax error
    # expect any *ERROR[15001]*
    # select abcd$(a) from mytable;
    
    # syntax error
    stmt = """select 1abcd(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # syntax error
    stmt = """select 12345(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # UDF name & cat/sch
    stmt = """select """ + gvars.definition_schema + """.qa_udf_integer_mvf(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""UDF (MVF) arguments"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """values(qa_udf_integer_mvf(-1234));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The datatype is iso88591, forcing _ucs2 should see error.
    stmt = """values(qa_udf_char_mvf(_ucs2'abcd'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4455')
    
    stmt = """values(qa_udf_char_mvf(_iso88591'abcd'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # This should return an error, only expecting one input.
    stmt = """values(qa_udf_char_mvf(qa_udf_char_mvf('abcd')));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4457')
    
    stmt = """select qa_udf_integer_mvf(1234) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char_mvf('abcd') from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer_mvf(a+b) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char_mvf(d) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char_mvf(e) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer_mvf(aa) from mytable as t (aa,bb,cc,dd,ee);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # UDF wrong number of arguments
    stmt = """select qa_udf_integer_mvf(a,b) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4457')
    
    # UDF wrong argument type
    stmt = """select qa_udf_integer_mvf('ABCD') from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4455')
    
    # UDF wrong argument type
    stmt = """select qa_udf_integer_mvf(d) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4455')
    
    # UDF wrong argument type
    stmt = """select qa_udf_integer_mvf(e) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4455')
    
    # UDF wrong argument type
    stmt = """select qa_udf_char_mvf(1234) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4455')
    
    # UDF wrong argument type
    stmt = """select qa_udf_char_mvf(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4455')
    
    # syntax error
    stmt = """select qa_udf_integer_mvf(*) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # SELECT as the argument
    stmt = """select qa_udf_integer_mvf(select a from mytable) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # INSERT as the argument
    # The UDF ES explicitly says that an embedded IUD statement in the
    # argument list is not allowed.  Although the ES seems to indicate
    # that the error number should be ERROR[4469]???
    stmt = """select qa_udf_integer_mvf(insert into mytable values (6,6,6)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # UPDATE as the argument
    # The UDF ES explicitly says that an embedded IUD statement in the
    # argument list is not allowed.  Although the ES seems to indicate
    # that the error number should be ERROR[4469]???
    stmt = """select qa_udf_integer_mvf(update mytable set b=1234 where a=b) from mytable;"""
    output = _dci.cmdexec(stmt)
    
    # DELETE as the argument
    # The UDF ES explicitly says that an embedded IUD statement in the
    # argument list is not allowed.  Although the ES seems to indicate
    # that the error number should be ERROR[4469]???
    stmt = """select qa_udf_char_mvf(delete from mytable where a=1234) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # Derived names in the output header
    # Using derived name on MVF should be an error.
    stmt = """select qa_udf_integer_mvf(a) as ABCDEFGHIJK from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4478')
    
    # No derived name, so the registered name should show up in the header.
    stmt = """select qa_udf_integer_mvf(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """C_INTEGER1*C_INTEGER2""")
    
    _testmgr.testcase_end(desc)

def test004(desc="""SELECT: UDF (MVF) in the select-list"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select qa_udf_integer_mvf(a), qa_udf_integer_mvf(b), qa_udf_char_mvf(d), qa_udf_char_mvf(e)
from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer_mvf(a), qa_udf_integer_mvf(b) from myview;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select [first 2] qa_udf_integer_mvf(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select [any 2] qa_udf_integer_mvf(a), qa_udf_char_mvf(d) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer_mvf(b) as name_a,
qa_udf_char_mvf(d) as name_d from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4478')
    
    stmt = """select all qa_udf_integer_mvf(b) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select distinct qa_udf_integer_mvf(a), qa_udf_integer_mvf(b), qa_udf_char_mvf(d)
from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer_mvf(v.a), qa_udf_integer_mvf(t.b), c, d, qa_udf_char_mvf(e)
from myview v, mytable t
where qa_udf_integer_mvf(v.a)=qa_udf_integer_mvf(t.b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # error
    stmt = """select t.qa_udf_integer_mvf(a) from mytable as t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""SELECT: UDF (MVF) in the WHERE clause"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select * from mytable where qa_udf_integer_mvf(a) between
qa_udf_integer_mvf(b) and qa_udf_integer_mvf(c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable
where (qa_udf_integer_mvf(a), qa_udf_integer_mvf(b))
between (qa_udf_integer_mvf(a-1), qa_udf_integer_mvf(b-1)) and
(qa_udf_integer_mvf(a+1),qa_udf_integer_mvf(b+1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # Note: The subquery here needs to return only one row.  A good example,
    # is the next query that uses max().  Here, even we know that there is only
    # row, but the actual code might not.  However, it should exit gracefully,
    # instead of abending.
    stmt = """select * from mytable
where (qa_udf_integer_mvf(a), qa_udf_integer_mvf(b))
not between (qa_udf_integer_mvf(a-1), qa_udf_integer_mvf(b-1))
and (select qa_udf_integer_mvf(a), qa_udf_integer_mvf(b) from myonerowtable
where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable
where (qa_udf_integer_mvf(a), qa_udf_integer_mvf(b))
not between (qa_udf_integer_mvf(a-1), qa_udf_integer_mvf(b-1))
and (select max(a), max(a), max(b), max(b) from mytable2
where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable where qa_udf_char_mvf(d)=qa_udf_char_mvf(e);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from myview where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from myview v, mytable t
where qa_udf_integer_mvf(v.a)<qa_udf_integer_mvf(t.b) and
qa_udf_char_mvf(t.d)=qa_udf_char_mvf(t.e);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from myview v, mytable t
where (qa_udf_integer_mvf(v.a), qa_udf_integer_mvf(t.a)) >=
(qa_udf_integer_mvf(v.b), qa_udf_integer_mvf(t.b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from myview v, mytable t
where (qa_udf_integer_mvf(v.a), qa_udf_integer_mvf(t.b)) !=
(select qa_udf_integer_mvf(a), qa_udf_integer_mvf(b) from myonerowtable);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from myview v, mytable t
where (qa_udf_integer_mvf(v.a), qa_udf_integer_mvf(t.b)) >
all (select qa_udf_integer_mvf(a), qa_udf_integer_mvf(b) from mytable2
where qa_udf_integer_mvf(a) = qa_udf_integer_mvf(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from myview v, mytable t
where (qa_udf_integer_mvf(v.a), qa_udf_integer_mvf(t.b)) >
any (select qa_udf_integer_mvf(a), qa_udf_integer_mvf(b) from mytable2
where qa_udf_integer_mvf(a) = qa_udf_integer_mvf(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from myview v, mytable t
where (qa_udf_integer_mvf(v.a), qa_udf_integer_mvf(t.b)) >
some (select qa_udf_integer_mvf(a), qa_udf_integer_mvf(b) from mytable2
where qa_udf_integer_mvf(a) = qa_udf_integer_mvf(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select c from mytable where exists
(select qa_udf_integer_mvf(b) from myview where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable where
qa_udf_integer_mvf(a) in (values (1,1),(2,2),(3,3)) or
qa_udf_char_mvf(d) in (values ('AAA','AAA'),('BBB','BBB'),('CCC','CCC'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable where (qa_udf_integer_mvf(a), qa_udf_integer_mvf(b)) not in
(values (qa_udf_integer_mvf(1), qa_udf_integer_mvf(1)),
(qa_udf_integer_mvf(2), qa_udf_integer_mvf(2)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable where qa_udf_integer_mvf(a) in (qa_udf_integer_mvf(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select c from mytable where qa_udf_integer_mvf(a) in
(select qa_udf_integer_mvf(b) from myview where qa_udf_integer_mvf(a) = qa_udf_integer_mvf(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable as t (name_a,name_b,name_c,name_d,name_e)
where qa_udf_integer_mvf(name_a)=qa_udf_integer_mvf(name_c) and
qa_udf_char_mvf(name_d)=qa_udf_char_mvf(name_e);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable where qa_udf_integer_mvf(a) is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from mytable where qa_udf_char_mvf(d) like '%A%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""SELECT: UDF (MVF) in a subquery as the table reference"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # SELECT subquery as table reference
    # multile columns can't be renamed into a single column.
    stmt = """select * from
(select qa_udf_integer_mvf(a) as a, qa_udf_char_mvf(d) as d
from mytable where qa_udf_char_mvf(d)=qa_udf_char_mvf(e)) as t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4478')
    
    # DELETE subquery as table reference
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of the DELETE [FIRST N] statement.  This subquery does not have [FIRST N],
    # so it should work.
    stmt = """select * from
(delete from mytable where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b)) as t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select qa_udf_integer_mvf(t.aa), qa_udf_integer_mvf(t.ee) from
(delete from mytable where d=e
return qa_udf_integer_mvf(a)) as t (aa, ee);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # syntax error
    stmt = """select qa_udf_integer_mvf(t.aa), qa_udf_char_mvf(t.ee) from
(delete from mytable where d=e
return qa_udf_integer_mvf(a)) as t (qa_udf_integer_mvf(aa), qa_udf_char_mvf(ee));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # UPDATE subquery as table reference
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of the UPDATE [FIRST N] statement. This subquery does not have [FIRST N],
    # so it should work.
    stmt = """select * from
(update mytable set (b,c)=(qa_udf_integer_mvf(a))
where (qa_udf_integer_mvf(a))=(qa_udf_integer_mvf(b))) as t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select qa_udf_integer_mvf(t.bb), qa_udf_integer_mvf(t.ee) from
(update mytable set (b,c)=(qa_udf_integer_mvf(a)) where d=e
return qa_udf_integer_mvf(new.b)) as t (bb, ee);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select qa_udf_integer_mvf(t.bb), qa_udf_integer_mvf(t.ee) from
(update mytable set (b,c)=(qa_udf_integer_mvf(a)) where d=e
return qa_udf_integer_mvf(old.b)) as t (bb, ee);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # syntax error
    stmt = """select qa_udf_integer_mvf(t.aa), qa_udf_char_mvf(t.ee) from
(update mytable set (b,c)=(qa_udf_integer_mvf(a)) where d=e
return qa_udf_integer_mvf(a)) as t (qa_udf_integer_mvf(aa), qa_udf_char_mvf(ee));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # INSERT subquery as table reference
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from
(insert into mytable
(select a, qa_udf_integer_mvf(a), qa_udf_char_mvf(d) from myonerowtable)) as t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # syntax error
    stmt = """select qa_udf_integer_mvf(t.aa), qa_udf_char_mvf(t.ee) from
(insert into mytable values (7, qa_udf_integer_mvf(7), qa_udf_char_mvf('ggg')))
as t (qa_udf_integer_mvf(aa), bb, cc, dd, qa_udf_char_mvf(ee));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""SELECT: UDF (MVF) Misc"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # SAMPLE clause
    stmt = """select * from mytable sample first
balance when qa_udf_integer_mvf(a)=(values(1,1)) then 10 rows
when qa_udf_integer_mvf(a)=(values(2,2)) then 15 rows
else 20 rows
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable sample random
balance when qa_udf_char_mvf(d)=(values('AAA','AAA')) then 10 percent
when qa_udf_char_mvf(e)=(values('BBB','BBB')) then 15 percent
else 20 percent
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # TRANSPOSE clause
    # The ES explicitly says that a MVF is not allowed in the transpose clause
    # of a select statement.
    
    stmt = """select a, val from mytable
transpose qa_udf_integer_mvf(b) as val;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4468')
    
    stmt = """select * from mytable
transpose qa_udf_integer_mvf(a), qa_udf_integer_mvf(b), qa_udf_char_mvf(d) as valcol;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4468')
    
    stmt = """select * from mytable
transpose qa_udf_integer_mvf(a) as valcol1
transpose qa_udf_integer_mvf(b) as valcol2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4468')
    
    stmt = """select * from mytable
transpose (d,e),(qa_udf_char_mvf(d),qa_udf_char_mvf(e)) as (valcol1,valcol2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4468')
    
    # SEQUENCE BY clause
    # The UDF ES explicitly says that UDF is not allowed in the SEQUENE BY
    # clause of a SELECT statement.
    stmt = """select diff1(a,b) from mytable sequence by qa_udf_integer_mvf(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # GROUP BY clause
    # expression not allowed in group by
    stmt = """select * from mytable group by qa_udf_integer_mvf(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4012')
    
    # HAVING clause
    stmt = """select qa_udf_integer_mvf(a),qa_udf_integer_mvf(b) from mytable
having qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b) group by a, b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # ORDER BY clause
    # syntax error
    stmt = """select * from
mytable order by qa_udf_integer_mvf(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # syntax error
    stmt = """select * from
mytable order by qa_udf_char_mvf(e);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # ON clause in FULL OUTER JOIN
    # The UDF ES explicitly says that UDF is not allowed in the ON clause
    # of a FULL OUTER JOIN.
    stmt = """select * from mytable full outer join mytable2
on qa_udf_integer_mvf(mytable.a) = qa_udf_integer_mvf(mytable2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4463')
    
    # ON clause in LEFT OUTER JOIN
    stmt = """select * from mytable left outer join mytable2
on qa_udf_integer_mvf(mytable.a) = qa_udf_integer_mvf(mytable2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # ON clause in RIGHT OUTER JOIN
    stmt = """select * from mytable right outer join mytable2
on qa_udf_integer_mvf(mytable.a) = qa_udf_integer_mvf(mytable2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # ON clause in INNER JOIN
    stmt = """select * from mytable inner join mytable2
on qa_udf_char_mvf(mytable.d) = qa_udf_char_mvf(mytable2.d);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # UNION
    stmt = """select * from mytable inner join mytable2
on qa_udf_integer_mvf(mytable.a) = qa_udf_integer_mvf(mytable2.a)
union
select * from mytable right outer join mytable2
on qa_udf_integer_mvf(mytable.a) = qa_udf_integer_mvf(mytable2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # Other places that UDF should not show up
    # syntax error
    stmt = """select t1.a, t2.b, t1.c from
mytable2 as t1 (a, qa_udf_integer_mvf(b), c)
cross join
mytable2 as t2
group by t1.a, t2.b, t1.c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

def test008(desc="""UDF (MVF) and SQL function (aggregate function)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select qa_udf_integer_mvf(CAST(AVG(a) as INT)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select AVG(qa_udf_integer_mvf(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4476')
    
    stmt = """select qa_udf_integer_mvf(COUNT(a)) from mytable group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select COUNT(qa_udf_integer_mvf(a)) from mytable group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4476')
    
    stmt = """select qa_udf_integer_mvf(MAX(a)), qa_udf_integer_mvf(MAXIMUM(b)) from mytable group by c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select MAX(qa_udf_integer_mvf(a)), MAXIMUM(qa_udf_integer_mvf(b)) from mytable group by c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4476')
    
    stmt = """select qa_udf_integer_mvf(MIN(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select MIN(qa_udf_integer_mvf(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4476')
    
    stmt = """select qa_udf_integer_mvf(STDDEV(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # This should work.  select stddev(1,1) from mytables works too.
    stmt = """select STDDEV(qa_udf_integer_mvf(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select distinct qa_udf_integer_mvf(SUM(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select SUM(qa_udf_integer_mvf(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4476')
    
    stmt = """select qa_udf_integer_mvf(VARIANCE(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select VARIANCE(qa_udf_integer_mvf(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    _testmgr.testcase_end(desc)

def test009(desc="""UDF (MVF) and SQL function (character string function)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select ASCII(qa_udf_char_mvf(e)), CHAR(ASCII(qa_udf_char_mvf(e)))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_integer_mvf(ASCII(e)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select CHAR_LENGTH(qa_udf_char_mvf(d)), OCTET_LENGTH(qa_udf_char_mvf(e))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select CHAR_LENGTH(qa_udf_char_mvf(d) || qa_udf_char_mvf(e)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select COALESCE(qa_udf_char_mvf(d), 'mmm') from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_char_mvf(COALESCE(d, e, 'mmm')) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select CODE_VALUE(qa_udf_char_mvf(d)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select CONCAT(qa_udf_char_mvf(d)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select qa_udf_char_mvf(CONCAT(CAST(d as char(25)), CAST(e as char(25)))) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select INSERT(qa_udf_char_mvf(d), 1, 2, 'mmm') from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_char_mvf(INSERT(d, 1, 2, 'mmm')) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select UCASE(qa_udf_char_mvf(d)), LCASE(qa_udf_char_mvf(e)),
UPPER(qa_udf_char_mvf(d)), LOWER(qa_udf_char_mvf(e)),
UPSHIFT(qa_udf_char_mvf(d)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_char_mvf(UCASE(d)), qa_udf_char_mvf(LCASE(e)),
qa_udf_char_mvf(UPPER(d)), qa_udf_char_mvf(LOWER(e)),
qa_udf_char_mvf(UPSHIFT(d)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select LEFT(qa_udf_char_mvf(d), 2), RIGHT(qa_udf_char_mvf(e), 2) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_char_mvf(LEFT(d, 2)), qa_udf_char_mvf(RIGHT(e, 2)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select LOCATE(qa_udf_char_mvf(d), 'BB'),
POSITION(qa_udf_char_mvf(d) in qa_udf_char_mvf(e))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_integer_mvf(LOCATE(d, 'BB')), qa_udf_integer_mvf(POSITION(d in e))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select LPAD(qa_udf_char_mvf(d), 2), RPAD(qa_udf_char_mvf(e), 2) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select qa_udf_char_mvf(LPAD(d, 2)), qa_udf_char_mvf(RPAD(e, 2)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select LPAD(qa_udf_char_mvf(d), 2, qa_udf_char_mvf(e)),
RPAD(qa_udf_char_mvf(e), 2, qa_udf_char_mvf(d)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select TRIM(qa_udf_char_mvf(e)), LTRIM(qa_udf_char_mvf(e)), RTRIM(qa_udf_char_mvf(d))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_char_mvf(TRIM(e)), qa_udf_char_mvf(LTRIM(e)), qa_udf_char_mvf(RTRIM(d))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select REPEAT(qa_udf_char_mvf(e), 2) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_char_mvf(REPEAT(e, 2)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select REPLACE(qa_udf_char_mvf(d), 'mmm') from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select qa_udf_char_mvf(REPLACE(d, e, 'mmm')) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select SUBSTRING(qa_udf_char_mvf(d) from 0 for 2),
SUBSTR(qa_udf_char_mvf(e), 0, 2) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_char_mvf(SUBSTRING(d from 0 for 2)),
qa_udf_char_mvf(SUBSTR(e, 0, 2)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select TRANSLATE(qa_udf_char_mvf(d) using ISO88591TOUCS2) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_char_mvf(TRANSLATE(TRANSLATE(d using ISO88591TOUCS2) using UCS2TOISO88591)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""UDF (MVF) and SQL function (datetime function)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # MVF is not allowed in most of the cases.
    stmt = """select ADD_MONTHS(qa_udf_date_mvf(c_date),
1, 0) from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select ADD_MONTHS(qa_udf_time_mvf(c_time),
1, 0) from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select ADD_MONTHS(qa_udf_time5_mvf(c_time5),
1, 0) from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select ADD_MONTHS(qa_udf_timestamp_mvf(c_timestamp),
1, 0) from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select ADD_MONTHS(qa_udf_timestamp_mvf(c_timestamp),
1, 0) from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select qa_udf_date_mvf(ADD_MONTHS(c_date, 1, 0))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_date_mvf(ADD_MONTHS(c_date, 1, 0)) from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    # DATE type is not right for the UDF, which expects a TIME parameter.
    stmt = """select qa_udf_time_mvf(ADD_MONTHS(c_date, 1, 0)) from myFullTable;"""
    output = _dci.cmdexec(stmt)

    _dci.expect_error_msg(output, '4455')

    # DATE type is not right for the UDF, which expects a TIME(6) parameter.
    stmt = """select qa_udf_time5_mvf(ADD_MONTHS(c_date, 1, 0))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4455')

    stmt = """select qa_udf_timestamp_mvf(ADD_MONTHS(c_timestamp, 1, 0))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_timestamp_mvf(ADD_MONTHS(c_timestamp, 1, 0))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select CONVERTTIMESTAMP(148731163200000000+qa_udf_integer_mvf(c_integer))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select qa_udf_timestamp_mvf(CONVERTTIMESTAMP(148731163200000000))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_timestamp_mvf(CURRENT(3)), qa_udf_timestamp_mvf(CURRENT_TIMESTAMP)
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_date_mvf(CURRENT_DATE), qa_udf_time5_mvf(CURRENT_TIME(6))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select DATE_ADD(qa_udf_date_mvf(c_date), INTERVAL '1' DAY),
DATE_ADD(qa_udf_timestamp_mvf(c_timestamp), INTERVAL '1' DAY),
DATE_SUB(qa_udf_date_mvf(c_date), INTERVAL '1' DAY),
DATE_SUB(qa_udf_timestamp_mvf(c_timestamp), INTERVAL '1' DAY)
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select qa_udf_date_mvf(DATE_ADD(c_date, INTERVAL '1' DAY)),
qa_udf_timestamp_mvf(DATE_ADD(c_timestamp, INTERVAL '1' DAY)),
qa_udf_date_mvf(DATE_SUB(c_date, INTERVAL '1' DAY)),
qa_udf_timestamp_mvf(DATE_SUB(c_timestamp, INTERVAL '1' DAY))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select DATE_PART('year', qa_udf_date_mvf(c_date)),
DATE_PART('month', qa_udf_timestamp_mvf(c_timestamp)),
EXTRACT(day from qa_udf_date_mvf(c_date)),
EXTRACT(second from qa_udf_timestamp_mvf(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select DATE_TRUNC('year', qa_udf_date_mvf(c_date)),
DATE_TRUNC('month', qa_udf_timestamp_mvf(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select qa_udf_timestamp_mvf(DATE_TRUNC('year', c_date)),
qa_udf_timestamp_mvf(DATE_TRUNC('month', c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select DATEADD(DAY, 7, qa_udf_date_mvf(c_date)),
DATEADD(WEEK, 1, qa_udf_timestamp_mvf(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select qa_udf_date_mvf(DATEADD(DAY, 7, c_date)),
qa_udf_timestamp_mvf(DATEADD(WEEK, 1, c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select DATEDIFF(DAY, qa_udf_date_mvf(c_date),
qa_udf_timestamp_mvf(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select qa_udf_integer_mvf(DATEDIFF(DAY, c_timestamp, c_date))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select DATEFORMAT(qa_udf_date_mvf(c_date), USA),
DATEFORMAT(qa_udf_timestamp_mvf(c_timestamp), EUROPEAN)
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select qa_udf_char_mvf(DATEFORMAT(c_date, USA)),
qa_udf_char_mvf(DATEFORMAT(c_timestamp, EUROPEAN))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select DAY(qa_udf_date_mvf(c_date)), DAY(qa_udf_timestamp_mvf(c_timestamp)),
MONTH(qa_udf_date_mvf(c_date)), MONTH(qa_udf_timestamp_mvf(c_timestamp)),
YEAR(qa_udf_date_mvf(c_date)), YEAR(qa_udf_timestamp_mvf(c_timestamp)),
QUARTER(qa_udf_date_mvf(c_date)), QUARTER(qa_udf_timestamp_mvf(c_timestamp)),
WEEK(qa_udf_date_mvf(c_date)), WEEK(qa_udf_timestamp_mvf(c_timestamp)),
DAYOFWEEK(qa_udf_date_mvf(c_date)),
DAYOFWEEK(qa_udf_timestamp_mvf(c_timestamp)),
DAYOFMONTH(qa_udf_date_mvf(c_date)),
DAYOFMONTH(qa_udf_timestamp_mvf(c_timestamp)),
DAYOFYEAR(qa_udf_date_mvf(c_date)),
DAYOFYEAR(qa_udf_timestamp_mvf(c_timestamp)),
HOUR(qa_udf_time_mvf(c_time)), HOUR(qa_udf_timestamp_mvf(c_timestamp)),
MINUTE(qa_udf_time_mvf(c_time)), MINUTE(qa_udf_timestamp_mvf(c_timestamp)),
SECOND(qa_udf_time_mvf(c_time)), SECOND(qa_udf_timestamp_mvf(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select qa_udf_integer_mvf(DAY(c_date)), qa_udf_integer_mvf(DAY(c_timestamp)),
qa_udf_integer_mvf(MONTH(c_date)), qa_udf_integer_mvf(MONTH(c_timestamp)),
qa_udf_integer_mvf(YEAR(c_date)), qa_udf_integer_mvf(YEAR(c_timestamp)),
qa_udf_integer_mvf(QUARTER(c_date)), qa_udf_integer_mvf(QUARTER(c_timestamp)),
qa_udf_integer_mvf(WEEK(c_date)), qa_udf_integer_mvf(WEEK(c_timestamp)),
qa_udf_integer_mvf(DAYOFWEEK(c_date)), qa_udf_integer_mvf(DAYOFWEEK(c_timestamp)),
qa_udf_integer_mvf(DAYOFMONTH(c_date)), qa_udf_integer_mvf(DAYOFMONTH(c_timestamp)),
qa_udf_integer_mvf(DAYOFYEAR(c_date)), qa_udf_integer_mvf(DAYOFYEAR(c_timestamp)),
qa_udf_integer_mvf(HOUR(c_time)), qa_udf_integer_mvf(HOUR(c_timestamp)),
qa_udf_integer_mvf(MINUTE(c_time)), qa_udf_integer_mvf(MINUTE(c_timestamp)),
qa_udf_integer_mvf(SECOND(c_time)), qa_udf_integer_mvf(SECOND(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select DAYNAME(qa_udf_date_mvf(c_date)), DAYNAME(qa_udf_timestamp_mvf(c_timestamp)),
MONTHNAME(qa_udf_date_mvf(c_date)),
MONTHNAME(qa_udf_timestamp_mvf(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select qa_udf_char_mvf(DAYNAME(c_date)), qa_udf_char_mvf(DAYNAME(c_timestamp)),
qa_udf_char_mvf(MONTHNAME(c_date)), qa_udf_char_mvf(MONTHNAME(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select JULIANTIMESTAMP(qa_udf_date_mvf(c_date)),
JULIANTIMESTAMP(qa_udf_time_mvf(c_time)),
JULIANTIMESTAMP(qa_udf_timestamp_mvf(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select TIMESTAMPADD(SQL_TSI_DAY, 7, qa_udf_date_mvf(c_date)),
TIMESTAMPADD(SQL_TSI_YEAR, 1, qa_udf_timestamp_mvf(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select qa_udf_date_mvf(TIMESTAMPADD(SQL_TSI_DAY, 7, c_date)),
qa_udf_timestamp_mvf(TIMESTAMPADD(SQL_TSI_YEAR, 1, c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select TIMESTAMPDIFF(SQL_TSI_DAY, qa_udf_date_mvf(c_date),
qa_udf_timestamp_mvf(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')

    stmt = """select qa_udf_integer_mvf(TIMESTAMPDIFF(SQL_TSI_DAY, c_date, c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    _testmgr.testcase_end(desc)

def test011(desc="""UDF (MVF) and SQL function (mathematical function)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select ABS(qa_udf_integer_mvf(a)), CEILING(qa_udf_integer_mvf(b)),
DEGREES(qa_udf_integer_mvf(c)), EXP(qa_udf_integer_mvf(a)/qa_udf_integer_mvf(a)),
FLOOR(qa_udf_integer_mvf(b)), LOG(qa_udf_integer_mvf(c)),
LOG10(qa_udf_integer_mvf(a)), MOD(qa_udf_integer_mvf(b), qa_udf_integer_mvf(c)),
PI(), POWER(qa_udf_integer_mvf(a), qa_udf_integer_mvf(b)/qa_udf_integer_mvf(b)),
RADIANS(qa_udf_integer_mvf(b)), ROUND(qa_udf_integer_mvf(c)),
SIGN(qa_udf_integer_mvf(a)), SQRT(qa_udf_integer_mvf(b))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_integer_mvf(ABS(a)), qa_udf_integer_mvf(CEILING(b)),
qa_udf_integer_mvf(DEGREES(c)), qa_udf_integer_mvf(EXP(a)),
qa_udf_integer_mvf(FLOOR(b)), qa_udf_integer_mvf(LOG(c)),
qa_udf_integer_mvf(LOG10(a)), qa_udf_integer_mvf(MOD(b, c)),
qa_udf_integer_mvf(PI()), qa_udf_integer_mvf(POWER(a, b)),
qa_udf_integer_mvf(RADIANS(b)), qa_udf_integer_mvf(ROUND(c)),
qa_udf_integer_mvf(SIGN(a)), qa_udf_integer_mvf(SQRT(b))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select ACOS(qa_udf_integer_mvf(a)/qa_udf_integer_mvf(a)), ASIN(qa_udf_integer_mvf(b)/qa_udf_integer_mvf(b)),
ATAN(qa_udf_integer_mvf(c)/qa_udf_integer_mvf(c)),
ATAN2(qa_udf_integer_mvf(a)/qa_udf_integer_mvf(a),qa_udf_integer_mvf(b)/qa_udf_integer_mvf(b)),
COS(qa_udf_integer_mvf(b)), COSH(qa_udf_integer_mvf(c)/qa_udf_integer_mvf(c)),
SIN(qa_udf_integer_mvf(a)), SINH(qa_udf_integer_mvf(b)/qa_udf_integer_mvf(b)),
TAN(qa_udf_integer_mvf(c)), TANH(qa_udf_integer_mvf(a)/qa_udf_integer_mvf(a))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_integer_mvf(ACOS(a/a)), qa_udf_integer_mvf(ASIN(b/b)),
qa_udf_integer_mvf(ATAN(c)), qa_udf_integer_mvf(ATAN2(a,b)),
qa_udf_integer_mvf(COS(b)), qa_udf_integer_mvf(COSH(c)),
qa_udf_integer_mvf(SIN(a)), qa_udf_integer_mvf(SINH(b)),
qa_udf_integer_mvf(TAN(c)), qa_udf_integer_mvf(TANH(a))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select NULLIFZERO(qa_udf_integer_mvf(a)), ZEROIFNULL(qa_udf_integer_mvf(b))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_integer_mvf(NULLIFZERO(a)), qa_udf_integer_mvf(ZEROIFNULL(b))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test012(desc="""UDF (MVF) and SQL function (sequence function)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
  
    # Sequence function is not supported yet
    if hpdci.tgtTR():
        _testmgr.testcase_end(desc)
        return
 
    stmt = """select qa_udf_integer_mvf(DIFF1(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer_mvf(DIFF1(a, b)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select DIFF1(qa_udf_integer_mvf(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select DIFF1(qa_udf_integer_mvf(a), qa_udf_integer_mvf(b)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(DIFF2(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer_mvf(DIFF2(a, b)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select DIFF2(qa_udf_integer_mvf(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select DIFF2(qa_udf_integer_mvf(a), qa_udf_integer_mvf(b)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # MOVINGAVG as a squbquery but no sequence by in the subquery is an error.
    stmt = """select qa_udf_integer_mvf(MOVINGAVG(a, 2, 4)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGAVG(qa_udf_integer_mvf(a), 2, 4) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(MOVINGCOUNT(a, 2, 4)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGCOUNT(qa_udf_integer_mvf(a), 2, 4) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(MOVINGMAX(a, 3)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGMAX(qa_udf_integer_mvf(a),3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGMAX(a, qa_udf_integer_mvf(3)-qa_udf_integer_mvf(3)+3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(MOVINGMIN(a, 3)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGMIN(qa_udf_integer_mvf(a),3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGMIN(a, qa_udf_integer_mvf(3)-qa_udf_integer_mvf(3)+3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # expect any *row(s) selected*
    # select qa_udf_integer_mvf(MOVINGSTDEV(a, 3)) from mytable sequence by a;
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    # expect any *ERROR[4461]*
    # select MOVINGSTDEV(qa_udf_integer_mvf(a),3) from mytable sequence by b;
    
    stmt = """select qa_udf_integer_mvf(MOVINGSUM(a, 3)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGSUM(qa_udf_integer_mvf(a),3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(MOVINGVARIANCE(a, 3)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGVARIANCE(qa_udf_integer_mvf(a),3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(OFFSET(a, 3)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select OFFSET(qa_udf_integer_mvf(a),3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select OFFSET(qa_udf_integer_mvf(a), qa_udf_integer_mvf(3)*0+3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(RUNNINGRANK(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGRANK(qa_udf_integer_mvf(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(RUNNINGAVG(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGAVG(qa_udf_integer_mvf(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(RUNNINGCOUNT(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGCOUNT(qa_udf_integer_mvf(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(RUNNINGMAX(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGMAX(qa_udf_integer_mvf(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(RUNNINGMIN(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGMIN(qa_udf_integer_mvf(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(RUNNINGSTDDEV(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGSTDDEV(qa_udf_integer_mvf(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(RUNNINGSUM(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGSUM(qa_udf_integer_mvf(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(RUNNINGVARIANCE(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGVARIANCE(qa_udf_integer_mvf(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(LASTNOTNULL(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select LASTNOTNULL(qa_udf_integer_mvf(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer_mvf(ROWS SINCE CHANGED(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select ROWS SINCE CHANGED (qa_udf_integer_mvf(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # THIS not in ROWS SINCE is an error.
    stmt = """select ROWS SINCE (qa_udf_integer_mvf(THIS(a)) < a) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select ROWS SINCE (THIS(qa_udf_integer_mvf(a)) < qa_udf_integer_mvf(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    _testmgr.testcase_end(desc)

def test013(desc="""UDF (MVF) and SQL function (other SQL function/expression)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select BITAND(qa_udf_integer_mvf(a), qa_udf_integer_mvf(b)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_integer_mvf(BITAND(a, b)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # Syntax error. The following example sees syntax error, so a MVF should
    # see the same error.
    # select *, CASE (c1,c2)
    # WHEN (1,2) THEN 'TYPE A' ELSE 'TYPE B' END from udftable;
    stmt = """select *, CASE qa_udf_integer_mvf(a)
WHEN (1,1) THEN 'TYPE A'
ELSE 'TYPE B'
END
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # Should see the comparison predicate must be of equal degree error.
    stmt = """select *, CASE a
WHEN qa_udf_integer_mvf(1234) THEN 'TYPE A'
ELSE 'TYPE B'
END
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4042')
    
    stmt = """select *, CASE a
WHEN 1 THEN qa_udf_integer_mvf(a)
ELSE qa_udf_integer_mvf(b)
END
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select CAST(qa_udf_integer_mvf(a)-qa_udf_integer_mvf(a)+1 as CHAR) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_char_mvf(CAST(a as CHAR)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer_mvf(CAST(qa_udf_char_mvf('1234') as INTEGER)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select COALESCE(a, b, qa_udf_integer_mvf(a), qa_udf_integer_mvf(b)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_integer_mvf(COALESCE(a,b)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select CONVERTTOHEX(qa_udf_integer_mvf(c)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select CONVERTTOHEX(qa_udf_char_mvf(e)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_char_mvf(CONVERTTOHEX(e)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char_mvf(CONVERTTOHEX(a)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
   
    if hpdci.tgtSQ(): 
        stmt = """select qa_udf_char_mvf(CURRENT_ROLE) from myonerowtable;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char_mvf(CURRENT_USER) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char_mvf(USER) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # Should see the comparison predicate must be of equal degree error.
    stmt = """select DECODE(qa_udf_char_mvf(d), 'AAA', '1st',
'BBB', '2nd',
'3rd') from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4042')
    
    stmt = """select DECODE(qa_udf_char_mvf(d), qa_udf_char_mvf(e), qa_udf_char_mvf(e),
qa_udf_char_mvf(e), qa_udf_char_mvf(e),
qa_udf_char_mvf('3rd')) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_char_mvf(DECODE(d, 'AAA', '1st',
'BBB', '2nd',
'3rd')) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char_mvf(DECODE(qa_udf_char_mvf(d), qa_udf_char_mvf(e), qa_udf_char_mvf(e),
qa_udf_char_mvf(e), qa_udf_char_mvf(e),
qa_udf_char_mvf('3rd')))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select ISNULL(qa_udf_integer_mvf(a),qa_udf_integer_mvf(b)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_integer_mvf(ISNULL(a,0)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select ISNULL(qa_udf_char_mvf(d),qa_udf_char_mvf(e)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_char_mvf(ISNULL(d,'')) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select NULLIF(qa_udf_char_mvf(d),qa_udf_char_mvf(d)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_char_mvf(NULLIF(d,'fff')) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select NVL(qa_udf_integer_mvf(b), 9999) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4479')
    
    stmt = """select qa_udf_integer_mvf(NVL(b, 9999)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test014(desc="""UDF (MVF) in UDF"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select qa_udf_integer_mvf(qa_udf_integer_mvf(a)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4457')
    
    stmt = """select qa_udf_integer_mvf(qa_udf_integer(a)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer_mvf(qa_udf_integer(qa_udf_integer(qa_udf_integer(a)))) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char_mvf(qa_udf_char(d)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char_mvf(qa_udf_char(d)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char_mvf(qa_udf_char(qa_udf_char(qa_udf_char(e)))) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test015(desc="""UDF (MVF) in INSERT (and TRANSACTION CONTROL)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # VALUES clause
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mytable values
(101, qa_udf_integer_mvf(1), qa_udf_char_mvf('mmm'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # in a subquery
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mytable
(select a*10, qa_udf_integer_mvf(b), qa_udf_char_mvf(e) from mytable2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of the INSERT...SELECT [FIRST N] statement.  This one does not have
    # [FIRST N], so it should work.
    stmt = """insert into mytable
(select a*10, qa_udf_integer_mvf(b), qa_udf_char_mvf(e) from mytable2
where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of the INSERT...SELECT [first N] statement.
    # To use [first N] in a subquery at all, you need to turn on the CQD
    # ALLOW_FIRSTN_IN_SUBQUERIES. Otherwise, you will see error 4102.
    stmt = """control query default ALLOW_FIRSTN_IN_SUBQUERIES 'TRUE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mytable
(select [first 5] a*10, qa_udf_integer_mvf(b), qa_udf_char_mvf(e) from mytable2
where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4473')
    
    stmt = """control query default ALLOW_FIRSTN_IN_SUBQUERIES reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # UDF in the ON clause of INNER/LEFT OUTER/RIGHT OUTER JOIN/UNION
    stmt = """create table mytmptable
(c1 int not null not droppable primary key,
c2 int,
c3 int,
c4 char(10),
c5 varchar(10),
c6 int,
c7 int,
c8 int,
c9 char(10),
c10 varchar(10));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mytmptable
select * from mytable as t1 inner join mytable2 as t2
on qa_udf_integer_mvf(t1.a)=qa_udf_integer_mvf(t2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """delete from mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """insert into mytmptable
select * from mytable as t1 left outer join mytable2 as t2
on qa_udf_integer_mvf(t1.a)=qa_udf_integer_mvf(t2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """delete from mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """insert into mytmptable
select * from mytable as t1 right outer join mytable2 as t2
on qa_udf_integer_mvf(t1.a)=qa_udf_integer_mvf(t2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """delete from mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """insert into mytmptable
select * from mytable as t1 inner join mytable2 as t2
on qa_udf_integer_mvf(t1.a)=qa_udf_integer_mvf(t2.a)
union
select * from mytable as t1 left outer join mytable2 as t2
on qa_udf_integer_mvf(t1.a)=qa_udf_integer_mvf(t2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """delete from mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """drop table mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test016(desc="""UDF (MVF) in DELETE (and TRANSACTION CONTROL)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # WHERE clause
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of the DELETE [FIRST N] statement.  This one does not have [FIRST N], it
    # should work.
    stmt = """delete from mytable where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of the DELETE [FIRST N] statement.
    stmt = """delete [first 1] from mytable where qa_udf_integer_mvf(b)=(values(1,1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4465')
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of the DELETE [FIRST N] statement.  This one does not have [FIRST N], it
    # should work.
    stmt = """delete from mytable where qa_udf_integer_mvf(a) in
(select qa_udf_integer_mvf(a) from mytable2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Long Running Delete (LRD, a.k.a. DELETE with MULTI COMMIT)
    stmt = """create table mytmptable like mytable
as select * from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of a statement using MULTI COMMIT.
    stmt = """delete with multi commit from mytmptable
where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4474')
    
    stmt = """drop table mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table mytmptable like mytable
as select * from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """set transaction multi commit on;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of a statement using MULTI COMMIT.
    stmt = """delete from mytmptable where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4474')
    
    stmt = """set transaction multi commit off;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table mytmptable like mytable
as select * from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """set transaction multi commit on;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of a statement using MULTI COMMIT.
    stmt = """delete from mytmptable where qa_udf_integer_mvf(b)=(values(1,1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4139')
    
    stmt = """set transaction multi commit off;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test017(desc="""UDF (MVF) in UPDATE (and TRANSACTION CONTROL)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # SET clause
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytable set (b,c)=(qa_udf_integer_mvf(1)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytable set (b,c)=
(select qa_udf_integer_mvf(b) from mytable2 where a=1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytable set (b,c)=
(select avg(b), avg(c) from mytable2 where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # WHERE clause
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of the UPDATE [FIRST N] statement.  It should work without [FIRST N].
    stmt = """update mytable set b=2 where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of the UPDATE [FIRST N] statement.
    stmt = """update [first 2] mytable set b=2 where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4466')
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of the UPDATE [FIRST N] statement.  It should work without [FIRST N].
    # where only takes a scalar value.  where (a,c) should not be allowed.
    stmt = """update mytable set b=1 where (a,c) in (qa_udf_integer_mvf(5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of the UPDATE [FIRST N] statement.
    stmt = """update [first 2] mytable set b=1 where (a,c) in (qa_udf_integer_mvf(5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of the UPDATE [FIRST N] statement.  It should work without [FIRST N].
    # where only takes a scalar value.  where (a,c) should not be allowed.
    stmt = """update mytable set b=1 where (a,c) in (select qa_udf_integer_mvf(a) from mytable2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of the UPDATE [FIRST N] statement.  But this one is in a subquery, so
    # it should work.
    stmt = """update [first 2] mytable set b=1 where (a,c) in
(select qa_udf_integer_mvf(qa_udf_integer(a)) from mytable2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test018(desc="""UDF (MVF) in MERGE INTO (and TRANSACTION CONTROL)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # USING clause
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """merge into mytable
using (select a,b from mytable2 where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b)) x
on mytable.a = x.a
when matched then update set b=x.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ON clause
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the ON clause
    # of a MERGE INTO statement.
    stmt = """merge into mytable on qa_udf_integer_mvf(a)=qa_udf_integer_mvf(10)
when matched then update set b=a
when not matched then insert values (6,6,6,'fff','fff');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4471')
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # UPDATE SET clause
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the UPDATE SET
    # clause of a MERGE INTO statement.
    stmt = """merge into mytable on a=10
when matched then update set (b,c)=(qa_udf_integer_mvf(a))
when not matched then insert values (10,6,6,'fff','fff');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4471')
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # INSERT VALUES clause
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the INSERT VALUES
    # clause of a MERGE INTO statement.
    stmt = """merge into mytable on a=10
when matched then update set b=a
when not matched then insert values (6, qa_udf_integer_mvf(10),qa_udf_char_mvf('fff'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4471')
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test019(desc="""UDF (MVF) in CREATE TRIGGER (and TRANSACTION CONTROL)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # WHEN clause (for a BEFORE trigger)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create trigger mytrigger1 before insert on mytable
referencing new as sample
for each row
when (qa_udf_integer_mvf(sample.b) = qa_udf_integer_mvf(sample.b))
set sample.b=sample.b+1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (6,6,6,'fff','fff');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from mytable where b=7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # WHEN clause (for an AFTER trigger)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHEN clause
    # of an AFTER TRIGGER
    stmt = """create trigger mytrigger2 after insert on mytable
referencing new as sample
for each row
when (qa_udf_integer_mvf(sample.b) = qa_udf_integer_mvf(sample.b))
insert into mytable2 values
(6,6,6,'fff','fff');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4464')
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # trigger SQL statement
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create trigger mytrigger3 after insert on mytable
referencing new as sample
for each row
when (sample.a = sample.b)
insert into mytable2 values
(qa_udf_integer_mvf(sample.a), sample.b,
qa_udf_char_mvf(sample.d));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from mytable2 where b=6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """insert into mytable values (6,6,6,'fff','fff');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from mytable2 where b=6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # trigger SQL statement
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create trigger mytrigger4 after insert on mytable
referencing new as sample
for each row
when (sample.a = sample.b)
insert into mytable2 values
(qa_udf_integer_mvf(sample.a), sample.c,
qa_udf_char_mvf(sample.d));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from mytable2 where b=6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """insert into mytable values (6,6,6,'fff','fff');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from mytable2 where b=6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test020(desc="""UDF (MVF) in CREATE TABLE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # AS SELECT
    # Should see a string ovrflow error 8402, as d and e are only declared as
    # two bytes, which are too short.
    stmt = """create table mytmptable0
(a int not null primary key, b int, c int, d char(2), e varchar(2))
as select qa_udf_integer_mvf(a), c, qa_udf_char_mvf(d) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    stmt = """create table mytmptable1
(a int not null primary key, b int, c int, d char(10), e varchar(10))
as select qa_udf_integer_mvf(a), c, qa_udf_char_mvf(d) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """drop table mytmptable1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table mytmptable2
(a int not null primary key, b int, c int, d char(10), e varchar(10))
as select * from mytable where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """drop table mytmptable2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    # create set table is not supported in TRAFODION yet
    if not hpdci.tgtTR():
        stmt = """create set table mytmptable3
(a int not null primary key, b int, c int, d char(10), e varchar(10))
as select * from mytable where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
        stmt = """drop table mytmptable3;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
    # LIKE ... AS SELECT
    stmt = """create table mytmptable4 like mytable
as select qa_udf_integer_mvf(a), c, qa_udf_char_mvf(d) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """drop table mytmptable4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table mytmptable5 like mytable
as select * from mytable where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """drop table mytmptable5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    # create set table is not supported in TRAFODION yet
    if not hpdci.tgtTR():
        stmt = """create set table mytmptable6 like mytable
as select * from mytable where qa_udf_char_mvf(d)=qa_udf_char_mvf(e);"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
        stmt = """drop table mytmptable6;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
    # DEFAULT clause
    stmt = """create table mytmptable7
(a int not null not droppable primary key,
b int,
c int default qa_udf_integer_mvf(1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # CHECK constraint (column constraint)
    # The UDF ES explicitly says that UDF is not allowed in a CHECK constraint.
    stmt = """create table mytmptable8
(a int not null not droppable primary key,
b int,
c int check(qa_udf_integer_mvf(c)=qa_udf_integer_mvf(a)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4470')
    
    # CHECK constraint (table constraint)
    # The UDF ES explicitly says that UDF is not allowed in a CHECK constraint.
    stmt = """create table mytmptable9
(a int not null not droppable primary key,
b int,
c int,
check(qa_udf_integer_mvf(c)=qa_udf_integer_mvf(a)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4470')
    
    _testmgr.testcase_end(desc)

def test021(desc="""UDF (MVF) in ALTER TABLE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # DEFAULT attribute
    stmt = """alter table mytable
add column zz int default qa_udf_integer_mvf(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # CHECK constraint (column constraint)
    # The UDF ES explicitly says that UDF is not allowed in a CHECK constraint.
    stmt = """alter table mytable
add column zz int check (qa_udf_integer_mvf(c)=qa_udf_integer_mvf(a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4470')
    
    # CHECK constraint (table constraint)
    # The UDF ES explicitly says that UDF is not allowed in a CHECK constraint.
    stmt = """alter table mytable
add constraint myconstraint check (qa_udf_integer_mvf(b)=qa_udf_integer_mvf(a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4470')
    
    _testmgr.testcase_end(desc)

def test022(desc="""UDF (MVF) in CREATE MV"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
   
    # MV is not supported in TRAFODION yet
    if hpdci.tgtTR():
        _testmgr.testcase_end(desc)
        return
 
    # UDF in SELECT
    # This should fail.  Incremental refresh shouldn't work with a UDF.
    stmt = """create mv mytmpmv1
refresh on request
initialize on create
as select a, qa_udf_integer_mvf(b) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '12001')
    
    # This should work.  Recompute every time should work with a UDF.
    stmt = """create mv mytmpmv2
recompute
initialize on create
as select a, qa_udf_integer_mvf(b) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """12345""")
    
    stmt = """select * from mytmpmv2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """drop mv mytmpmv2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # This should fail.  Incremental refresh shouldn't work with a UDF.
    stmt = """create mv mytmpmv3
refresh on request
initialize on refresh
as select * from mytable where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '12001')
    
    # This should work.  Recompute every time should work with a UDF.
    stmt = """create mv mytmpmv4
recompute
initialize on refresh
as select * from mytable where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """maintain mv mytmpmv4, refresh;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from mytmpmv4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """drop mv mytmpmv4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # UDF in the ON clause of INNER JOIN
    stmt = """create mv mytmpmv5 (c1,c2,c3,c4,c5,c6,c7,c8,c9,c10)
recompute initialize on create
as select * from mytable as t1 inner join mytable2 as t2
on qa_udf_integer_mvf(t1.a)=qa_udf_integer_mvf(t2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from mytmpmv5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """drop mv mytmpmv5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # UDF in HASH PARTITION BY
    # The UDF ES explicitily says that UDF is not allowed in the PARTITION BY
    # clause of the CREATE MV statement.
    stmt = """create mv mytmpmv6
refresh on request
initialize on create
hash partition by (qa_udf_integer_mvf(a))
as select * from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # UDF in STORE BY
    # The UDF ES explicitily says that UDF is not allowed in the STORE BY
    # clause of the CREATE MV statement.
    stmt = """create mv mytmpmv7
refresh on request
initialize on create
store by (qa_udf_integer_mvf(a))
as select * from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

def test023(desc="""UDF (MVF) in CREATE VIEW"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # UDF in SELECT
    stmt = """create view myview1
as select qa_udf_integer_mvf(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from myview1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """drop view myview1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Should see an error.  The same function used twice causes duplicated out
    # parameter names in the select list.
    stmt = """create view myview2
as select qa_udf_integer_mvf(a), qa_udf_integer_mvf(qa_udf_integer(b)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1080')
   
    stmt = """create view myview3
as select * from mytable where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from myview3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """drop view myview3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Non-deterministic UDF in not allowed with [with [cascaded] check option]
    # with check option and with cascaded check option are the same, but we
    # will run them twice just to be sure.
    
    # This is allowed.  it's a deterministic UDF
    stmt = """create view myview3_1
as select qa_udf_integer_mvf(a) from mytable
with check option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from myview3_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """drop view myview3_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # This is allowed.  it's a deterministic UDF
    stmt = """create view myview3_2
as select qa_udf_integer_mvf(a) from mytable
with cascaded check option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from myview3_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """drop view myview3_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # This is NOT allowed, it's a nondeterministic UDFs
    stmt = """create view myview3_3
as select qa_udf_integer_nondeterministic_mvf(a) from mytable
with check option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4467')
    
    # This is NOT allowed, it's a nondeterministic UDFs
    stmt = """create view myview3_4
as select qa_udf_integer_nondeterministic_mvf(a) from mytable
with cascaded check option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4467')
    
    # UDF in the ON clause of INNER/LEFT OUTER/RIGHT OUTER JOIN
    stmt = """create view myview4 (c1,c2,c3,c4,c5,c6,c7,c8,c9,c10)
as select * from mytable as t1 inner join mytable2 as t2
on qa_udf_integer_mvf(t1.a)=qa_udf_integer_mvf(t2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from myview4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """drop view myview4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view myview5 (c1,c2,c3,c4,c5,c6,c7,c8,c9,c10)
as select * from mytable as t1 left outer join mytable2 as t2
on qa_udf_integer_mvf(t1.a)=qa_udf_integer_mvf(t2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from myview5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """drop view myview5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view myview6 (c1,c2,c3,c4,c5,c6,c7,c8,c9,c10)
as select * from mytable as t1 right outer join mytable2 as t2
on qa_udf_integer_mvf(t1.a)=qa_udf_integer_mvf(t2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from myview6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """drop view myview6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test024(desc="""UDF (MVF) in CALL/GRANT EXECUTE/REVOKE EXECUTE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # CALL/GRANT EXECUTE should only work on SPJ, not UDF.
    
    stmt = """call qa_udf_integer_mvf(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
   
    if not hpdci.tgtTR(): 
        stmt = """grant execute on procedure qa_udf_integer_mvf to "role.support";"""
        output = _dci.cmdexec(stmt)
        _dci.expect_error_msg(output, '1004')
    
        stmt = """revoke execute on procedure qa_udf_integer_mvf from "role.support";"""
        output = _dci.cmdexec(stmt)
        _dci.expect_error_msg(output, '1004')
    
    _testmgr.testcase_end(desc)

def test025(desc="""UDF (MVF) in SET PARAM/PREPARE/EXECUTE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # a NCI command, only numeric or character literal is allowed as the value.
    stmt = """set param ?myval 100;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select qa_udf_integer_mvf(?myval) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare xx from
select qa_udf_integer_mvf(?myval) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare yy from
select qa_udf_integer_mvf(?) from mytable where qa_udf_integer_mvf(a) = qa_udf_integer_mvf(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute yy using ?myval, 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """reset param ?myval;"""
    output = _dci.cmdexec(stmt)
    
    # a NCI command, only numeric or character literal is allowed as the value.
    stmt = """set param ?myval 'AAA';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select qa_udf_char_mvf(?myval) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare xx from
select qa_udf_char_mvf(?myval) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare yy from
select qa_udf_char_mvf(?) from mytable where qa_udf_char_mvf(d) = qa_udf_char_mvf(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute yy using ?myval, 'AAA       ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """reset param ?myval;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test026(desc="""UDF (MVF) in SET TRANSACTION/LOCK TABLE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # Try to use UDF in various transaction mode just to make sure...
    
    stmt = """create table mytmptable like mytable
as select * from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # isolation level
    stmt = """set transaction isolation level read uncommitted;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select *, qa_udf_integer_mvf(a)
from mytmptable
where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """set transaction isolation level serializable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set transaction isolation level repeatable read;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # This is also the default, so the attribute is restored as well.
    stmt = """set transaction isolation level read committed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # access mode
    stmt = """set transaction read only;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select *, qa_udf_integer_mvf(a)
from mytmptable
where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # This is also the default, so the attribute is restored as well.
    stmt = """set transaction read write;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # autocommit option
    stmt = """set transaction autocommit off;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # This is also the default, so the attribute is restored as well.
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # norollback option
    stmt = """set transaction no rollback on;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # This is also the default, so the attribute is restored as well.
    stmt = """set transaction no rollback off;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # restore the table
    stmt = """update mytmptable set b=a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # auto abort option
    stmt = """set transaction autoabort 60 seconds;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set transaction autoabort 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # This is also the default, so the attribute is restored as well.
    stmt = """set transaction autoabort reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # autobegin option
    stmt = """set transaction autobegin off;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # This is also the default, so the attribute is restored as well.
    stmt = """set transaction autobegin on;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # restore the table
    stmt = """update mytmptable set b=a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # multicommit option
    # MULTI COMMIT ON/OFF is being tested separately in the testcase where
    # the DELETE statement is tested.
    
    # LOCK TABLE
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if not hpdci.tgtTR(): 
        stmt = """lock table mytmptable in exclusive mode;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    if not hpdci.tgtTR(): 
        stmt = """lock table mytmptable in share mode;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set (b,c)=(qa_udf_integer_mvf(a)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test027(desc="""UDF (MVF) in STREAM (CURSOR)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
   
    # Stream is not supported in TRAFODION yet
    if hpdci.tgtTR():
        _testmgr.testcase_end(desc)
        return
 
    # timeout after 5 seconds
    stmt = """set table * stream timeout 500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Should see the timeout error, but shouldn't see any other errors.
    stmt = """select qa_udf_integer_mvf(a), qa_udf_integer_mvf(b), qa_udf_char_mvf(d), qa_udf_char_mvf(e)
from stream(mytable)
where qa_udf_integer_mvf(a)=qa_udf_integer_mvf(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8006')
    
    stmt = """set table * stream timeout reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

