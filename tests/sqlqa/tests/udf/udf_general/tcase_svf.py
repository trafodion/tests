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

def test001(desc="""UDF (SVF) input/output data types"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # These UDFs return the same values, so the output with or without
    # UDF should be the same if the data types are handled properly.
    stmt = """select * from myFullTable where
qa_udf_char(c_char) = c_char and 
qa_udf_char_upshift(c_char_upshift) = c_char_upshift and 
qa_udf_char_not_casespecific(c_char_not_casespecific) = c_char_not_casespecific and 
qa_udf_char_varying(c_char_varying) = c_char_varying and
qa_udf_char_varying_upshift(c_char_varying_upshift) = c_char_varying_upshift and
qa_udf_char_varying_not_casespecific(c_char_varying_not_casespecific) = c_char_varying_not_casespecific and
qa_udf_varchar(c_varchar) = c_varchar and 
qa_udf_varchar_upshift(c_varchar_upshift) = c_varchar_upshift and
qa_udf_varchar_not_casespecific(c_varchar_not_casespecific) = c_varchar_not_casespecific and
qa_udf_nchar(c_nchar) = c_nchar and
qa_udf_nchar_upshift(c_nchar_upshift) = c_nchar_upshift and
qa_udf_nchar_not_casespecific(c_nchar_not_casespecific) = c_nchar_not_casespecific and
qa_udf_nchar_varying(c_nchar_varying) = c_nchar_varying and
qa_udf_nchar_varying_upshift(c_nchar_varying_upshift) = c_nchar_varying_upshift and
qa_udf_nchar_varying_not_casespecific(c_nchar_varying_not_casespecific) = c_nchar_varying_not_casespecific and
qa_udf_numeric(c_numeric) = c_numeric and
qa_udf_numeric_unsigned(c_numeric_unsigned) = c_numeric_unsigned and
qa_udf_decimal(c_decimal) = c_decimal and
qa_udf_decimal_unsigned(c_decimal_unsigned) = c_decimal_unsigned and
qa_udf_integer(c_integer) = c_integer and
qa_udf_integer_unsigned(c_integer_unsigned) = c_integer_unsigned and
qa_udf_largeint(c_largeint) = c_largeint and
qa_udf_smallint(c_smallint) = c_smallint and
qa_udf_smallint_unsigned(c_smallint_unsigned) = c_smallint_unsigned and
qa_udf_float(c_float) = c_float and
qa_udf_real(c_real) = c_real and
qa_udf_double_precision(c_double_precision) = c_double_precision and
qa_udf_date(c_date) = c_date and
qa_udf_time(c_time) = c_time and
qa_udf_time5(c_time5) = c_time5 and
qa_udf_timestamp(c_timestamp) = c_timestamp and 
qa_udf_timestamp5(c_timestamp5) = c_timestamp5 and
qa_udf_clob(c_clob) = c_clob and
qa_udf_blob(c_blob) = c_blob;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    stmt = """select * from myFullTable where
qa_udf_char(c_char) is null and
qa_udf_char_upshift(c_char_upshift) is null and
qa_udf_char_not_casespecific(c_char_not_casespecific) is null and
qa_udf_char_varying(c_char_varying) is null and
qa_udf_char_varying_upshift(c_char_varying_upshift) is null and
qa_udf_char_varying_not_casespecific(c_char_varying_not_casespecific) is null and
qa_udf_varchar(c_varchar) is null and
qa_udf_varchar_upshift(c_varchar_upshift) is null and
qa_udf_varchar_not_casespecific(c_varchar_not_casespecific) is null and
qa_udf_nchar(c_nchar) is null and
qa_udf_nchar_upshift(c_nchar_upshift) is null and
qa_udf_nchar_not_casespecific(c_nchar_not_casespecific) is null and
qa_udf_nchar_varying(c_nchar_varying) is null and
qa_udf_nchar_varying_upshift(c_nchar_varying_upshift) is null and
qa_udf_nchar_varying_not_casespecific(c_nchar_varying_not_casespecific) is null and
qa_udf_numeric(c_numeric) is null and
qa_udf_numeric_unsigned(c_numeric_unsigned) is null and
qa_udf_decimal(c_decimal) is null and
qa_udf_decimal_unsigned(c_decimal_unsigned) is null and
qa_udf_integer(c_integer) is null and
qa_udf_integer_unsigned(c_integer_unsigned) is null and
qa_udf_largeint(c_largeint) is null and
qa_udf_smallint(c_smallint) is null and
qa_udf_smallint_unsigned(c_smallint_unsigned) is null and
qa_udf_float(c_float) is null and
qa_udf_real(c_real) is null and
qa_udf_double_precision(c_double_precision) is null and
qa_udf_date(c_date) is null and
qa_udf_time(c_time) is null and
qa_udf_time5(c_time5) is null and
qa_udf_timestamp(c_timestamp) is null and
qa_udf_timestamp5(c_timestamp5) is null and
qa_udf_clob(c_clob) is null and
qa_udf_blob(c_blob) is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    _testmgr.testcase_end(desc)

def test002(desc="""UDF (SVF) names"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # UDF name case insensitive
    stmt = """select qa_udf_integer(b) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(B) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select Qa_UdF_InTeGer(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(b) from myview;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(B) from myview;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qA_uDf_iNtEgEr(a) from myview;"""
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
    stmt = """select """ + gvars.definition_schema + """.qa_udf_integer(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""UDF (SVF) arguments"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """values(qa_udf_integer(-1234));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The datatype is iso88591, forcing _ucs2 should see error.
    stmt = """values(qa_udf_char(_ucs2'abcd'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4455')
    
    stmt = """values(qa_udf_char(_iso88591'abcd'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """values(qa_udf_char(qa_udf_char('abcd')));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(1234) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char('abcd') from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(a+b) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(d) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(e) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(aa) from mytable as t (aa,bb,cc,dd,ee);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # UDF wrong number of arguments
    stmt = """select qa_udf_integer(a,b) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4457')
    
    # UDF wrong argument type
    stmt = """select qa_udf_integer('ABCD') from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4455')
    
    # UDF wrong argument type
    stmt = """select qa_udf_integer(d) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4455')
    
    # UDF wrong argument type
    stmt = """select qa_udf_integer(e) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4455')
    
    # UDF wrong argument type
    stmt = """select qa_udf_char(1234) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4455')
    
    # UDF wrong argument type
    stmt = """select qa_udf_char(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4455')
    
    # syntax error
    stmt = """select qa_udf_integer(*) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # SELECT as the argument
    stmt = """select qa_udf_integer(select a from mytable) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # INSERT as the argument
    # The UDF ES explicitly says that an embedded IUD statement in the
    # argument list is not allowed.  Although the ES seems to indicate
    # that the error number should be ERROR[4469]???
    stmt = """select qa_udf_integer(insert into mytable values (6,6,6)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # UPDATE as the argument
    # The UDF ES explicitly says that an embedded IUD statement in the
    # argument list is not allowed.  Although the ES seems to indicate
    # that the error number should be ERROR[4469]???
    stmt = """select qa_udf_integer(update mytable set b=1234 where a=b) from mytable;"""
    output = _dci.cmdexec(stmt)
    
    # DELETE as the argument
    # The UDF ES explicitly says that an embedded IUD statement in the
    # argument list is not allowed.  Although the ES seems to indicate
    # that the error number should be ERROR[4469]???
    stmt = """select qa_udf_char(delete from mytable where a=1234) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # Derived names in the output header
    # The derived name should show up in the header.
    stmt = """select qa_udf_integer(a) as ABCDEFGHIJK from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """ABCDEFGHIJK""")
    
    # No derived name, so the registered name should show up in the header.
    stmt = """select qa_udf_integer(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """C_INTEGER""")
    
    _testmgr.testcase_end(desc)

def test004(desc="""SELECT: UDF (SVF) in the select-list"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select qa_udf_integer(a), qa_udf_integer(b), qa_udf_char(d), qa_udf_char(e) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(a), qa_udf_integer(b) from myview;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select [first 2] qa_udf_integer(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select [any 2] qa_udf_integer(a), qa_udf_char(d) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(a)+qa_udf_integer(b) as name_a, qa_udf_char(d) as name_d from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select all qa_udf_integer(a)-qa_udf_integer(b) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select distinct qa_udf_integer(a)-qa_udf_integer(b), qa_udf_char(d) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(v.a) as name_a, qa_udf_integer(t.b) as name_b, c as name_c,
d as name_d, qa_udf_char(e) as name_e
from myview v, mytable t
where qa_udf_integer(v.a)=qa_udf_integer(t.b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # syntax error
    stmt = """select t.qa_udf_integer(a) from mytable as t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""SELECT: UDF (SVF) in the WHERE clause"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select * from mytable where qa_udf_integer(a) between qa_udf_integer(b) and qa_udf_integer(c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable
where (qa_udf_integer(a), qa_udf_integer(b))
between (qa_udf_integer(a-1), qa_udf_integer(b-1)) and (qa_udf_integer(a+1),qa_udf_integer(b+1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # Running this query from MXCI used to cause a saveabend file.  The
    # sympton on DFM/NCI was that it hanged for a while and nothing comes back.
    # DFM then continued.  Now this problem seems to go away, but instead of
    # unexpecting any error, we will expect row(s) selected to make sure that
    # the problem does not show up again.
    # Note: The subquery here needs to return only one row.  A good example,
    # is the next query that uses max().  Here, even we know that there is only
    # row, but the actual code might not.  However, it should exit gracefully,
    # instead of abending.
    stmt = """select * from mytable
where (qa_udf_integer(a), qa_udf_integer(b))
not between (qa_udf_integer(a-1), qa_udf_integer(b-1))
and (select qa_udf_integer(a), qa_udf_integer(b) from myonerowtable
where qa_udf_integer(a)=qa_udf_integer(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable
where (qa_udf_integer(a), qa_udf_integer(b))
not between (qa_udf_integer(a-1), qa_udf_integer(b-1))
and (select max(a), max(b) from mytable2
where qa_udf_integer(a)=qa_udf_integer(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable where qa_udf_integer(a)=qa_udf_integer(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable where qa_udf_char(d)=qa_udf_char(e);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from myview where qa_udf_integer(a)=qa_udf_integer(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from myview v, mytable t
where qa_udf_integer(v.a)<qa_udf_integer(t.b) and qa_udf_char(t.d)=qa_udf_char(t.e);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from myview v, mytable t
where (qa_udf_integer(v.a), qa_udf_integer(t.a)) >= (qa_udf_integer(v.b), qa_udf_integer(t.b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from myview v, mytable t
where (qa_udf_integer(v.a), qa_udf_integer(t.b)) !=
(select qa_udf_integer(a), qa_udf_integer(b) from myonerowtable);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from myview v, mytable t
where (qa_udf_integer(v.a), qa_udf_integer(t.b)) >
all (select qa_udf_integer(a), qa_udf_integer(b) from mytable2
where qa_udf_integer(a) = qa_udf_integer(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from myview v, mytable t
where (qa_udf_integer(v.a), qa_udf_integer(t.b)) >
any (select qa_udf_integer(a), qa_udf_integer(b) from mytable2
where qa_udf_integer(a) = qa_udf_integer(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from myview v, mytable t
where (qa_udf_integer(v.a), qa_udf_integer(t.b)) >
some (select qa_udf_integer(a), qa_udf_integer(b) from mytable2
where qa_udf_integer(a) = qa_udf_integer(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select c from mytable where exists
(select qa_udf_integer(b) from myview where qa_udf_integer(a)=qa_udf_integer(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable where
qa_udf_integer(a) in (1, 2, 3) or
qa_udf_char(d) in ('AAA', 'BBB', 'CCC');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable where (qa_udf_integer(a), qa_udf_integer(b)) not in
(values (qa_udf_integer(1), qa_udf_integer(1)), (qa_udf_integer(2), qa_udf_integer(2)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable where qa_udf_integer(a) in (qa_udf_integer(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select c from mytable where qa_udf_integer(a) in
(select qa_udf_integer(b) from myview where qa_udf_integer(a) = qa_udf_integer(b));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable as t (name_a,name_b,name_c,name_d,name_e)
where qa_udf_integer(name_a)=qa_udf_integer(name_c) and
qa_udf_char(name_d)=qa_udf_char(name_e);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable where qa_udf_integer(a) is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable where qa_udf_char(d) like '%A%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""SELECT: UDF (SVF) in a subquery as the table reference"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # SELECT subquery as table reference
    stmt = """select * from
(select qa_udf_integer(a) as a, qa_udf_char(d) as d
from mytable where qa_udf_char(d)=qa_udf_char(e)) as t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # DELETE subquery as table reference
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the WHERE clause
    # of the DELETE [FIRST N] statement.  This subquery does not have [FIRST N],
    # so it should work.
    stmt = """select * from
(delete from mytable where qa_udf_integer(a)=qa_udf_integer(b)) as t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select qa_udf_integer(t.aa), qa_udf_char(t.ee) from
(delete from mytable where d=e
return qa_udf_integer(a), qa_udf_char(e)) as t (aa, ee);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # syntax error
    stmt = """select qa_udf_integer(t.aa), qa_udf_char(t.ee) from
(delete from mytable where d=e
return qa_udf_integer(a), qa_udf_char(e)) as t (qa_udf_integer(aa), qa_udf_char(ee));"""
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
(update mytable set b=qa_udf_integer(c) where qa_udf_integer(a)=qa_udf_integer(b)) as t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select qa_udf_integer(t.bb), qa_udf_char(t.ee) from
(update mytable set b=qa_udf_integer(c) where d=e
return qa_udf_integer(new.b), qa_udf_char(new.e)) as t (bb, ee);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select qa_udf_integer(t.bb), qa_udf_char(t.ee) from
(update mytable set b=qa_udf_integer(c) where d=e
return qa_udf_integer(old.b), qa_udf_char(new.e)) as t (bb, ee);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # syntax error
    stmt = """select qa_udf_integer(t.aa), qa_udf_char(t.ee) from
(update mytable set b=qa_udf_integer(c) where d=e
return qa_udf_integer(a), qa_udf_char(e)) as t (qa_udf_integer(aa), qa_udf_char(ee));"""
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
(insert into myemptytable
(select qa_udf_integer(a), b, c, qa_udf_char(d), e from mytable)) as t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # syntax error
    stmt = """select qa_udf_integer(t.aa), qa_udf_char(t.ee) from
(insert into mytable values (7, 7, qa_udf_integer(7), 'ggg', qa_udf_char('ggg')))
as t (qa_udf_integer(aa), bb, cc, dd, qa_udf_char(ee));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""SELECT: UDF (SVF) Misc"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # SAMPLE clause
    stmt = """select * from mytable sample first
balance when qa_udf_integer(a)=1 then 10 rows
when qa_udf_integer(a)=2 then 15 rows
else 20 rows
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable sample random
balance when qa_udf_char(d)='AAA' then 10 percent
when qa_udf_char(e)='BBB' then 15 percent
else 20 percent
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # TRANSPOSE clause
    stmt = """select a, val from mytable
transpose qa_udf_integer(b)+qa_udf_integer(c) as val;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable
transpose qa_udf_integer(a), qa_udf_integer(b), qa_udf_integer(a)+qa_udf_integer(b) as valcol;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable
transpose qa_udf_integer(a) as valcol1
transpose qa_udf_integer(b) as valcol2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from mytable
transpose (d,e),(qa_udf_char(d),qa_udf_char(e)) as (valcol1,valcol2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # SEQUENCE BY clause
    # The UDF ES explicitly says that UDF is not allowed in the SEQUENE BY
    # clause of a SELECT statement.
    stmt = """select diff1(a,b) from mytable sequence by qa_udf_integer(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # GROUP BY clause
    # expression not allowed in group by
    stmt = """select * from mytable group by qa_udf_integer(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4012')
    
    # HAVING clause
    stmt = """select qa_udf_integer(a),qa_udf_integer(b) from mytable
having qa_udf_integer(a)=qa_udf_integer(b) group by a, b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # ORDER BY clause
    # syntax error
    stmt = """select * from
mytable order by qa_udf_integer(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # syntax error
    stmt = """select * from
mytable order by qa_udf_char(e);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # ON clause in FULL OUTER JOIN
    # The UDF ES explicitly says that UDF is not allowed in the ON clause
    # of a FULL OUTER JOIN.
    stmt = """select * from mytable full outer join mytable2
on qa_udf_integer(mytable.a) = qa_udf_integer(mytable2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4463')
    
    # ON clause in LEFT OUTER JOIN
    stmt = """select * from mytable left outer join mytable2
on qa_udf_integer(mytable.a) = qa_udf_integer(mytable2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # ON clause in RIGHT OUTER JOIN
    stmt = """select * from mytable right outer join mytable2
on qa_udf_integer(mytable.a) = qa_udf_integer(mytable2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # ON clause in INNER JOIN
    stmt = """select * from mytable inner join mytable2
on qa_udf_char(mytable.d) = qa_udf_char(mytable2.d);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # UNION
    stmt = """select * from mytable inner join mytable2
on qa_udf_integer(mytable.a) = qa_udf_integer(mytable2.a)
union
select * from mytable right outer join mytable2
on qa_udf_integer(mytable.a) = qa_udf_integer(mytable2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # Other places that UDF should not show up
    # syntax error
    stmt = """select t1.a, t2.b, t1.c from
mytable2 as t1 (a, qa_udf_integer(b), c)
cross join
mytable2 as t2
group by t1.a, t2.b, t1.c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

def test008(desc="""UDF (SVF) and SQL function (aggregate function)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select qa_udf_integer(CAST(AVG(a) as INT)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select AVG(qa_udf_integer(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(COUNT(a)) from mytable group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select COUNT(qa_udf_integer(a)) from mytable group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(MAX(a)), qa_udf_integer(MAXIMUM(b)) from mytable group by c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select MAX(qa_udf_integer(a)), MAXIMUM(qa_udf_integer(b)) from mytable group by c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(MIN(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select MIN(qa_udf_integer(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(STDDEV(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select STDDEV(qa_udf_integer(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select distinct qa_udf_integer(SUM(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select SUM(qa_udf_integer(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(VARIANCE(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select VARIANCE(qa_udf_integer(a)) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""UDF (SVF) and SQL function (character string function)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select ASCII(qa_udf_char(e)), CHAR(ASCII(qa_udf_char(e))) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(ASCII(e)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select CHAR_LENGTH(qa_udf_char(d)), OCTET_LENGTH(qa_udf_char(e)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select CHAR_LENGTH(qa_udf_char(d) || qa_udf_char(e)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select COALESCE(qa_udf_char(d), qa_udf_char(e), 'mmm') from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(COALESCE(d, e, 'mmm')) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select CODE_VALUE(qa_udf_char(d)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select CONCAT(qa_udf_char(d), qa_udf_char(e)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(CONCAT(CAST(d as CHAR(25)), CAST(e as CHAR(25)))) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select INSERT(qa_udf_char(d), 1, 2, 'mmm') from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(INSERT(d, 1, 2, 'mmm')) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select UCASE(qa_udf_char(d)), LCASE(qa_udf_char(e)),
UPPER(qa_udf_char(d)), LOWER(qa_udf_char(e)),
UPSHIFT(qa_udf_char(d)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(UCASE(d)), qa_udf_char(LCASE(e)),
qa_udf_char(UPPER(d)), qa_udf_char(LOWER(e)),
qa_udf_char(UPSHIFT(d)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select LEFT(qa_udf_char(d), 2), RIGHT(qa_udf_char(e), 2) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(LEFT(d, 2)), qa_udf_char(RIGHT(e, 2)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select LOCATE(qa_udf_char(d), 'BB'), POSITION(qa_udf_char(d) in qa_udf_char(e))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(LOCATE(d, 'BB')), qa_udf_integer(POSITION(d in e))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select LPAD(qa_udf_char(d), 2), RPAD(qa_udf_char(e), 2) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(LPAD(d, 2)), qa_udf_char(RPAD(e, 2)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select LPAD(qa_udf_char(d), 2, qa_udf_char(e)),
RPAD(qa_udf_char(e), 2, qa_udf_char(d)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select TRIM(qa_udf_char(e)), LTRIM(qa_udf_char(e)), RTRIM(qa_udf_char(d))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(TRIM(e)), qa_udf_char(LTRIM(e)), qa_udf_char(RTRIM(d))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select REPEAT(qa_udf_char(e), 2) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(REPEAT(e, 2)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select REPLACE(qa_udf_char(d), qa_udf_char(e), 'mmm') from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(REPLACE(d, e, 'mmm')) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select SUBSTRING(qa_udf_char(d) from 0 for 2),
SUBSTR(qa_udf_char(e), 0, 2) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(SUBSTRING(d from 0 for 2)),
qa_udf_char(SUBSTR(e, 0, 2)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select TRANSLATE(qa_udf_char(d) using ISO88591TOUCS2) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(TRANSLATE(TRANSLATE(d using ISO88591TOUCS2) using UCS2TOISO88591)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""UDF (SVF) and SQL function (datetime function)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # The first set of tests for ADD_MONTHS() are more thorough, with negative
    # tests for mismatching datetime datatype.  The rest of them are simplier
    # positive tests so that we don't end up with too many duplicate tests.

    stmt = """select ADD_MONTHS(qa_udf_date(c_date),
qa_udf_integer(c_integer)/qa_udf_integer(c_integer), 0) from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    # TIME data type should not be allowed.
    stmt = """select ADD_MONTHS(qa_udf_time(c_time),
qa_udf_integer(c_integer)/qa_udf_integer(c_integer), 0) from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')

    # TIME(6) data type should not be allowed.
    stmt = """select ADD_MONTHS(qa_udf_time5(c_time5),
qa_udf_integer(c_integer)/qa_udf_integer(c_integer), 0) from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')

    stmt = """select ADD_MONTHS(qa_udf_timestamp(c_timestamp),
qa_udf_integer(c_integer)/qa_udf_integer(c_integer), 0) from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select ADD_MONTHS(qa_udf_timestamp(c_timestamp),
qa_udf_integer(c_integer)/qa_udf_integer(c_integer), 0) from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_date(ADD_MONTHS(c_date, qa_udf_integer(c_integer)/qa_udf_integer(c_integer), 0))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_date(ADD_MONTHS(c_date, 1, 0)) from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    # DATE type is not right for the UDF, which expects a TIME parameter.
    stmt = """select qa_udf_time(ADD_MONTHS(c_date, 1, 0)) from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4455')

    # DATE type is not right for the UDF, which expects a TIME(6) parameter.
    stmt = """select qa_udf_time5(ADD_MONTHS(c_date, 1, 0))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4455')

    stmt = """select qa_udf_timestamp(ADD_MONTHS(c_timestamp, 1, 0))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_timestamp(ADD_MONTHS(c_timestamp, 1, 0))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select CONVERTTIMESTAMP(148731163200000000+qa_udf_integer(c_integer)-qa_udf_integer(c_integer))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_timestamp(CONVERTTIMESTAMP(148731163200000000))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_timestamp(CURRENT(3)), qa_udf_timestamp(CURRENT_TIMESTAMP)
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_date(CURRENT_DATE), qa_udf_time5(CURRENT_TIME(6))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select DATE_ADD(qa_udf_date(c_date), INTERVAL '1' DAY),
DATE_ADD(qa_udf_timestamp(c_timestamp), INTERVAL '1' DAY),
DATE_SUB(qa_udf_date(c_date), INTERVAL '1' DAY),
DATE_SUB(qa_udf_timestamp(c_timestamp), INTERVAL '1' DAY)
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_date(DATE_ADD(c_date, INTERVAL '1' DAY)),
qa_udf_timestamp(DATE_ADD(c_timestamp, INTERVAL '1' DAY)),
qa_udf_date(DATE_SUB(c_date, INTERVAL '1' DAY)),
qa_udf_timestamp(DATE_SUB(c_timestamp, INTERVAL '1' DAY))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select DATE_PART('year', qa_udf_date(c_date)),
DATE_PART('month', qa_udf_timestamp(c_timestamp)),
EXTRACT(day from qa_udf_date(c_date)),
EXTRACT(second from qa_udf_timestamp(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)


    stmt = """select DATE_TRUNC('year', qa_udf_date(c_date)),
DATE_TRUNC('month', qa_udf_timestamp(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_timestamp(DATE_TRUNC('year', c_date)),
qa_udf_timestamp(DATE_TRUNC('month', c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select DATEADD(DAY, 7, qa_udf_date(c_date)),
DATEADD(WEEK, 1, qa_udf_timestamp(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_date(DATEADD(DAY, 7, c_date)),
qa_udf_timestamp(DATEADD(WEEK, 1, c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select DATEDIFF(DAY, qa_udf_date(c_date), qa_udf_timestamp(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_integer(DATEDIFF(DAY, c_timestamp, c_date))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select DATEFORMAT(qa_udf_date(c_date), USA),
DATEFORMAT(qa_udf_timestamp(c_timestamp), EUROPEAN)
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_char(DATEFORMAT(c_date, USA)),
qa_udf_char(DATEFORMAT(c_timestamp, EUROPEAN))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select DAY(qa_udf_date(c_date)), DAY(qa_udf_timestamp(c_timestamp)),
MONTH(qa_udf_date(c_date)), MONTH(qa_udf_timestamp(c_timestamp)),
YEAR(qa_udf_date(c_date)), YEAR(qa_udf_timestamp(c_timestamp)),
QUARTER(qa_udf_date(c_date)), QUARTER(qa_udf_timestamp(c_timestamp)),
WEEK(qa_udf_date(c_date)), WEEK(qa_udf_timestamp(c_timestamp)),
DAYOFWEEK(qa_udf_date(c_date)),
DAYOFWEEK(qa_udf_timestamp(c_timestamp)),
DAYOFMONTH(qa_udf_date(c_date)),
DAYOFMONTH(qa_udf_timestamp(c_timestamp)),
DAYOFYEAR(qa_udf_date(c_date)),
DAYOFYEAR(qa_udf_timestamp(c_timestamp)),
HOUR(qa_udf_time(c_time)), HOUR(qa_udf_timestamp(c_timestamp)),
MINUTE(qa_udf_time(c_time)), MINUTE(qa_udf_timestamp(c_timestamp)),
SECOND(qa_udf_time(c_time)), SECOND(qa_udf_timestamp(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_integer(DAY(c_date)), qa_udf_integer(DAY(c_timestamp)),
qa_udf_integer(MONTH(c_date)), qa_udf_integer(MONTH(c_timestamp)),
qa_udf_integer(YEAR(c_date)), qa_udf_integer(YEAR(c_timestamp)),
qa_udf_integer(QUARTER(c_date)), qa_udf_integer(QUARTER(c_timestamp)),
qa_udf_integer(WEEK(c_date)), qa_udf_integer(WEEK(c_timestamp)),
qa_udf_integer(DAYOFWEEK(c_date)), qa_udf_integer(DAYOFWEEK(c_timestamp)),
qa_udf_integer(DAYOFMONTH(c_date)), qa_udf_integer(DAYOFMONTH(c_timestamp)),
qa_udf_integer(DAYOFYEAR(c_date)), qa_udf_integer(DAYOFYEAR(c_timestamp)),
qa_udf_integer(HOUR(c_time)), qa_udf_integer(HOUR(c_timestamp)),
qa_udf_integer(MINUTE(c_time)), qa_udf_integer(MINUTE(c_timestamp)),
qa_udf_integer(SECOND(c_time)), qa_udf_integer(SECOND(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select DAYNAME(qa_udf_date(c_date)), DAYNAME(qa_udf_timestamp(c_timestamp)),
MONTHNAME(qa_udf_date(c_date)),
MONTHNAME(qa_udf_timestamp(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_char(DAYNAME(c_date)), qa_udf_char(DAYNAME(c_timestamp)),
qa_udf_char(MONTHNAME(c_date)), qa_udf_char(MONTHNAME(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select JULIANTIMESTAMP(qa_udf_date(c_date)),
JULIANTIMESTAMP(qa_udf_time(c_time)),
JULIANTIMESTAMP(qa_udf_timestamp(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select TIMESTAMPADD(SQL_TSI_DAY, 7, qa_udf_date(c_date)),
TIMESTAMPADD(SQL_TSI_YEAR, 1, qa_udf_timestamp(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_date(TIMESTAMPADD(SQL_TSI_DAY, 7, c_date)),
qa_udf_timestamp(TIMESTAMPADD(SQL_TSI_YEAR, 1, c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select TIMESTAMPDIFF(SQL_TSI_DAY, qa_udf_date(c_date),
qa_udf_timestamp(c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """select qa_udf_integer(TIMESTAMPDIFF(SQL_TSI_DAY, c_date, c_timestamp))
from myFullTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    _testmgr.testcase_end(desc)

def test011(desc="""UDF (SVF) and SQL function (mathematical function)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select ABS(qa_udf_integer(a)), CEILING(qa_udf_integer(b)),
DEGREES(qa_udf_integer(c)), EXP(qa_udf_integer(a)/qa_udf_integer(a)),
FLOOR(qa_udf_integer(b)), LOG(qa_udf_integer(c)),
LOG10(qa_udf_integer(a)), MOD(qa_udf_integer(b), qa_udf_integer(c)),
PI(), POWER(qa_udf_integer(a), qa_udf_integer(b)/qa_udf_integer(b)),
RADIANS(qa_udf_integer(b)), ROUND(qa_udf_integer(c)),
SIGN(qa_udf_integer(a)), SQRT(qa_udf_integer(b))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(ABS(a)), qa_udf_integer(CEILING(b)),
qa_udf_integer(DEGREES(c)), qa_udf_integer(EXP(a)),
qa_udf_integer(FLOOR(b)), qa_udf_integer(LOG(c)),
qa_udf_integer(LOG10(a)), qa_udf_integer(MOD(b, c)),
qa_udf_integer(PI()), qa_udf_integer(POWER(a, b)),
qa_udf_integer(RADIANS(b)), qa_udf_integer(ROUND(c)),
qa_udf_integer(SIGN(a)), qa_udf_integer(SQRT(b))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select ACOS(qa_udf_integer(a)/qa_udf_integer(a)), ASIN(qa_udf_integer(b)/qa_udf_integer(b)),
ATAN(qa_udf_integer(c)/qa_udf_integer(c)),
ATAN2(qa_udf_integer(a)/qa_udf_integer(a),qa_udf_integer(b)/qa_udf_integer(b)),
COS(qa_udf_integer(b)), COSH(qa_udf_integer(c)/qa_udf_integer(c)),
SIN(qa_udf_integer(a)), SINH(qa_udf_integer(b)/qa_udf_integer(b)),
TAN(qa_udf_integer(c)), TANH(qa_udf_integer(a)/qa_udf_integer(a))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(ACOS(a/a)), qa_udf_integer(ASIN(b/b)),
qa_udf_integer(ATAN(c)), qa_udf_integer(ATAN2(a,b)),
qa_udf_integer(COS(b)), qa_udf_integer(COSH(c)),
qa_udf_integer(SIN(a)), qa_udf_integer(SINH(b)),
qa_udf_integer(TAN(c)), qa_udf_integer(TANH(a))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select NULLIFZERO(qa_udf_integer(a)), ZEROIFNULL(qa_udf_integer(b))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(NULLIFZERO(a)), qa_udf_integer(ZEROIFNULL(b))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test012(desc="""UDF (SVF) and SQL function (sequence function)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Sequence function is not supported yet
    if hpdci.tgtTR():
        _testmgr.testcase_end(desc)
        return

    stmt = """select qa_udf_integer(DIFF1(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(DIFF1(a, b)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select DIFF1(qa_udf_integer(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select DIFF1(qa_udf_integer(a), qa_udf_integer(b)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(DIFF2(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(DIFF2(a, b)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select DIFF2(qa_udf_integer(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select DIFF2(qa_udf_integer(a), qa_udf_integer(b)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # MOVINGAVG as a squbquery but no sequence by in the subquery is an error.
    stmt = """select qa_udf_integer(MOVINGAVG(a, 2, 4)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGAVG(qa_udf_integer(a), 2, 4) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(MOVINGCOUNT(a, 2, 4)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGCOUNT(qa_udf_integer(a), 2, 4) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(MOVINGMAX(a, 3)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGMAX(qa_udf_integer(a),3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGMAX(a, qa_udf_integer(3)-qa_udf_integer(3)+3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(MOVINGMIN(a, 3)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGMIN(qa_udf_integer(a),3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGMIN(a, qa_udf_integer(3)-qa_udf_integer(3)+3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # expect any *row(s) selected*
    # select qa_udf_integer(MOVINGSTDEV(a, 3)) from mytable sequence by a;
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    # expect any *ERROR[4461]*
    # select MOVINGSTDEV(qa_udf_integer(a),3) from mytable sequence by b;
    
    stmt = """select qa_udf_integer(MOVINGSUM(a, 3)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGSUM(qa_udf_integer(a),3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(MOVINGVARIANCE(a, 3)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select MOVINGVARIANCE(qa_udf_integer(a),3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(OFFSET(a, 3)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select OFFSET(qa_udf_integer(a),3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select OFFSET(qa_udf_integer(a), qa_udf_integer(3)*0+3) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(RUNNINGRANK(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGRANK(qa_udf_integer(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(RUNNINGAVG(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGAVG(qa_udf_integer(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(RUNNINGCOUNT(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGCOUNT(qa_udf_integer(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(RUNNINGMAX(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGMAX(qa_udf_integer(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(RUNNINGMIN(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGMIN(qa_udf_integer(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(RUNNINGSTDDEV(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGSTDDEV(qa_udf_integer(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(RUNNINGSUM(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGSUM(qa_udf_integer(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(RUNNINGVARIANCE(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select RUNNINGVARIANCE(qa_udf_integer(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(LASTNOTNULL(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select LASTNOTNULL(qa_udf_integer(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    stmt = """select qa_udf_integer(ROWS SINCE CHANGED(a)) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select ROWS SINCE CHANGED (qa_udf_integer(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # THIS not in ROWS SINCE is an error.
    stmt = """select ROWS SINCE (qa_udf_integer(THIS(a)) < a) from mytable sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    # The UDF ES explicitly says that UDF is not allowed in the argument list of
    # a sequence function.
    stmt = """select ROWS SINCE (THIS(qa_udf_integer(a)) < qa_udf_integer(a)) from mytable sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4461')
    
    _testmgr.testcase_end(desc)

def test013(desc="""UDF (SVF) and SQL function (other SQL function/expression)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select BITAND(qa_udf_integer(a), qa_udf_integer(b)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(BITAND(a, b)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select *, CASE qa_udf_integer(a)
WHEN 1 THEN 'TYPE A'
ELSE 'TYPE B'
END
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select *, CASE a
WHEN qa_udf_integer(1234) THEN 'TYPE A'
ELSE 'TYPE B'
END
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select *, CASE a
WHEN qa_udf_integer(a) THEN qa_udf_integer(a)
ELSE qa_udf_integer(b)
END
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select CAST(qa_udf_integer(a)-qa_udf_integer(a)+1 as CHAR) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(CAST(a as CHAR)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(CAST(qa_udf_char('1234') as INTEGER)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select COALESCE(a, b, qa_udf_integer(a), qa_udf_integer(b)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(COALESCE(a,b)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select CONVERTTOHEX(qa_udf_integer(c)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select CONVERTTOHEX(qa_udf_char(e)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(CONVERTTOHEX(e)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(CONVERTTOHEX(a)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # TRAF stmt = """select qa_udf_char(CURRENT_ROLE) from myonerowtable;"""
    # TRAF output = _dci.cmdexec(stmt)
    # TRAF _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(CURRENT_USER) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(USER) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select DECODE(qa_udf_char(d), 'AAA', '1st',
'BBB', '2nd',
'3rd') from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select DECODE(qa_udf_char(d), qa_udf_char(e), qa_udf_char(e),
qa_udf_char(e), qa_udf_char(e),
qa_udf_char('3rd')) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(DECODE(d, 'AAA', '1st',
'BBB', '2nd',
'3rd')) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(DECODE(qa_udf_char(d), qa_udf_char(e), qa_udf_char(e),
qa_udf_char(e), qa_udf_char(e),
qa_udf_char('3rd')))
from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select ISNULL(qa_udf_integer(a),qa_udf_integer(b)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(ISNULL(a,0)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select ISNULL(qa_udf_char(d),qa_udf_char(e)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(ISNULL(d,'')) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select NULLIF(qa_udf_char(d),qa_udf_char(d)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(NULLIF(d,'fff')) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select NVL(qa_udf_integer(b), 9999) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(NVL(b, 9999)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test014(desc="""UDF (SVF) in UDF"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select qa_udf_integer(qa_udf_integer(a)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(qa_udf_integer(a)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_integer(qa_udf_integer(qa_udf_integer(qa_udf_integer(a)))) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(qa_udf_char(d)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(qa_udf_char(d)) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select qa_udf_char(qa_udf_char(qa_udf_char(qa_udf_char(e)))) from myonerowtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test015(desc="""UDF (SVF) in INSERT (and TRANSACTION CONTROL)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # VALUES clause
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into myemptytable values
(qa_udf_integer(1), qa_udf_integer(2)+qa_udf_integer(3), qa_udf_integer(4),
qa_udf_char('mmm'), qa_udf_char('nnn'));"""
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
(select a*10, qa_udf_integer(b), 1, d, qa_udf_char(e) from mytable2);"""
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
(select a*10, qa_udf_integer(b), 1, d, qa_udf_char(e) from mytable2
where qa_udf_integer(a)=qa_udf_integer(b));"""
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
(select [first 5] a*10, qa_udf_integer(b), 1, d, qa_udf_char(e) from mytable2
where qa_udf_integer(a)=qa_udf_integer(b));"""
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
on qa_udf_integer(t1.a)=qa_udf_integer(t2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """delete from mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """insert into mytmptable
select * from mytable as t1 left outer join mytable2 as t2
on qa_udf_integer(t1.a)=qa_udf_integer(t2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """delete from mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """insert into mytmptable
select * from mytable as t1 right outer join mytable2 as t2
on qa_udf_integer(t1.a)=qa_udf_integer(t2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """delete from mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """insert into mytmptable
select * from mytable as t1 inner join mytable2 as t2
on qa_udf_integer(t1.a)=qa_udf_integer(t2.a)
union
select * from mytable as t1 left outer join mytable2 as t2
on qa_udf_integer(t1.a)=qa_udf_integer(t2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """delete from mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """drop table mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test016(desc="""UDF (SVF) in DELETE (and TRANSACTION CONTROL)"""):
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
    stmt = """delete from mytable where qa_udf_integer(a)=qa_udf_integer(b);"""
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
    stmt = """delete [first 1] from mytable where NVL(qa_udf_integer(b), 9999)=9999;"""
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
    stmt = """delete from mytable where qa_udf_integer(a) in (select qa_udf_integer(a) from mytable2);"""
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
    stmt = """delete with multi commit from mytmptable  where qa_udf_integer(a)=qa_udf_integer(b);"""
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
    stmt = """delete from mytmptable where qa_udf_integer(a)=qa_udf_integer(b);"""
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
    stmt = """delete from mytmptable where NVL(qa_udf_integer(b), 9999)=9999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4474')
    
    stmt = """set transaction multi commit off;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test017(desc="""UDF (SVF) in UPDATE (and TRANSACTION CONTROL)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # SET clause
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytable set b=qa_udf_integer(b) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytable set (b,c)=(qa_udf_integer(1),qa_udf_integer(1)) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytable set (b,c)=
    (select qa_udf_integer(b),qa_udf_integer(c) from mytable2 where a=1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytable set (b,c)=
(select avg(b), avg(c) from mytable2 where qa_udf_integer(a)=qa_udf_integer(b));"""
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
    stmt = """update mytable set b=qa_udf_integer(b) where qa_udf_integer(a)=qa_udf_integer(b);"""
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
    stmt = """update [first 2] mytable set b=qa_udf_integer(b) where qa_udf_integer(a)=qa_udf_integer(b);"""
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
    stmt = """update mytable set b=1 where a in (qa_udf_integer(5),6,7);"""
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
    stmt = """update [first 2] mytable set b=1 where a in (qa_udf_integer(5),6,7);"""
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
    stmt = """update mytable set b=1 where a in (select qa_udf_integer(a) from mytable2);"""
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
    stmt = """update [first 2] mytable set b=1 where a in
(select qa_udf_integer(qa_udf_integer(a)) from mytable2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test018(desc="""UDF (SVF) in MERGE INTO (and TRANSACTION CONTROL)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # USING clause
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """merge into mytable
using (select a,b from mytable2 where qa_udf_integer(a)=qa_udf_integer(b)) x
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
    stmt = """merge into mytable on a=qa_udf_integer(10)
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
when matched then update set b=qa_udf_integer(a)
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
when not matched then insert values (qa_udf_integer(10),6,6, qa_udf_char('fff'), 'fff');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4471')
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test019(desc="""UDF (SVF) in CREATE TRIGGER (and TRANSACTION CONTROL)"""):
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
when (qa_udf_integer(sample.b) = qa_udf_integer(sample.b))
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
when (qa_udf_integer(sample.b) = qa_udf_integer(sample.b))
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
(qa_udf_integer(qa_udf_integer(sample.a)), sample.b, qa_udf_integer(qa_udf_integer(sample.c)),
qa_udf_char(sample.d), qa_udf_char(qa_udf_char(sample.e)));"""
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
(qa_udf_integer(sample.a), sample.b, qa_udf_integer(sample.c),
qa_udf_char(sample.d), qa_udf_char(sample.e));"""
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

def test020(desc="""UDF (SVF) in CREATE TABLE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
   
    # AS SELECT
    # Should see a string ovrflow error 8402, as d and e are only declared as
    # two bytes, which are too short.
    stmt = """create table mytmptable0
(a int not null primary key, b int, c int, d char(2), e varchar(2))
as select qa_udf_integer(a), b, qa_udf_integer(c), qa_udf_char(d), qa_udf_char(e)
from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    stmt = """create table mytmptable1
(a int not null primary key, b int, c int, d char(10), e varchar(10))
as select qa_udf_integer(a), b, qa_udf_integer(c), qa_udf_char(d), qa_udf_char(e)
from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """drop table mytmptable1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table mytmptable2
(a int not null primary key, b int, c int, d char(10), e varchar(10))
as select * from mytable where qa_udf_integer(a)=qa_udf_integer(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """drop table mytmptable2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    # create set table is not supported in TRAFODION yet
    if not hpdci.tgtTR():
        stmt = """create set table mytmptable3
(a int not null primary key, b int, c int, d char(10), e varchar(10))
TRAF as select * from mytable where qa_udf_integer(a)=qa_udf_integer(b);"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
        stmt = """drop table mytmptable3;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
    # LIKE ... AS SELECT
    stmt = """create table mytmptable4 like mytable
as select qa_udf_integer(a), b, qa_udf_integer(c), qa_udf_char(d), e from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """drop table mytmptable4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table mytmptable5 like mytable
as select * from mytable where qa_udf_integer(a)=qa_udf_integer(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """drop table mytmptable5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    # create set table is not supported in TRAFODION yet
    if not hpdci.tgtTR():
        stmt = """create set table mytmptable6 like mytable
as select * from mytable where qa_udf_char(d)=qa_udf_char(e);"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
        stmt = """drop table mytmptable6;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
    # DEFAULT clause
    stmt = """create table mytmptable7
(a int not null not droppable primary key,
b int,
c int default qa_udf_integer(1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # CHECK constraint (column constraint)
    # The UDF ES explicitly says that UDF is not allowed in a CHECK constraint.
    stmt = """create table mytmptable8
(a int not null not droppable primary key,
b int,
c int check(qa_udf_integer(c)<1234));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4470')
    
    # CHECK constraint (table constraint)
    # The UDF ES explicitly says that UDF is not allowed in a CHECK constraint.
    stmt = """create table mytmptable9
(a int not null not droppable primary key,
b int,
c int,
check(qa_udf_integer(c)<1234));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4470')
    
    _testmgr.testcase_end(desc)

def test021(desc="""UDF (SVF) in ALTER TABLE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # DEFAULT attribute
    stmt = """alter table mytable
add column zz int default qa_udf_integer(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # CHECK constraint (column constraint)
    # The UDF ES explicitly says that UDF is not allowed in a CHECK constraint.
    stmt = """alter table mytable
add column zz int check (qa_udf_integer(c)>10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4470')
    
    # CHECK constraint (table constraint)
    # The UDF ES explicitly says that UDF is not allowed in a CHECK constraint.
    stmt = """alter table mytable
add constraint myconstraint check (qa_udf_integer(b)<1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4470')
    
    _testmgr.testcase_end(desc)

def test022(desc="""UDF (SVF) in CREATE MV"""):
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
as select a, qa_udf_integer(b) as b from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '12001')
    
    # This should work.  Recompute every time should work with a UDF.
    stmt = """create mv mytmpmv2
recompute
initialize on create
as select a, qa_udf_integer(b) as b from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
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
as select * from mytable where qa_udf_integer(a)=qa_udf_integer(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '12001')
    
    # This should work.  Recompute every time should work with a UDF.
    stmt = """create mv mytmpmv4
recompute
initialize on refresh
as select * from mytable where qa_udf_integer(a)=qa_udf_integer(b);"""
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
on qa_udf_integer(t1.a)=qa_udf_integer(t2.a);"""
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
hash partition by (qa_udf_integer(a))
as select * from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # UDF in STORE BY
    # The UDF ES explicitily says that UDF is not allowed in the STORE BY
    # clause of the CREATE MV statement.
    stmt = """create mv mytmpmv7
refresh on request
initialize on create
store by (qa_udf_integer(a))
as select * from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

def test023(desc="""UDF (SVF) in CREATE VIEW"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # UDF in SELECT
    stmt = """create view myview1
as select qa_udf_integer(a) as a from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from myview1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """drop view myview1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view myview2
as select qa_udf_integer(a) as a, qa_udf_integer(qa_udf_integer(b)) as b from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from myview2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """drop view myview2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view myview3
as select * from mytable where qa_udf_integer(a)=qa_udf_integer(b);"""
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
    
    # This is allowed.  They are all deterministic UDFs
    stmt = """create view myview3_1
as select qa_udf_integer(a) as a, qa_udf_integer(b) as b from mytable
with check option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from myview3_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """drop view myview3_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # This is allowed.  They are all deterministic UDFs
    stmt = """create view myview3_2
as select qa_udf_integer(a) as a, qa_udf_integer(b) as b from mytable
with cascaded check option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from myview3_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """drop view myview3_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # This is NOT allowed, one of them is a nondeterministic UDFs
    stmt = """create view myview3_3
as select qa_udf_integer_nondeterministic(a) as a, qa_udf_integer(b) as b from mytable
with check option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4467')
    
    # This is NOT allowed, one of them is a nondeterministic UDFs
    stmt = """create view myview3_4
as select qa_udf_integer_nondeterministic(a) as a, qa_udf_integer(b) as b from mytable
with cascaded check option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4467')
    
    # UDF in the ON clause of INNER/LEFT OUTER/RIGHT OUTER JOIN
    stmt = """create view myview4 (c1,c2,c3,c4,c5,c6,c7,c8,c9,c10)
as select * from mytable as t1 inner join mytable2 as t2
on qa_udf_integer(t1.a)=qa_udf_integer(t2.a);"""
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
on qa_udf_integer(t1.a)=qa_udf_integer(t2.a);"""
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
on qa_udf_integer(t1.a)=qa_udf_integer(t2.a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from myview6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """drop view myview6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test024(desc="""UDF (SVF) in CALL/GRANT EXECUTE/REVOKE EXECUTE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # CALL/GRANT EXECUTE should only work on SPJ, not UDF.
    
    stmt = """call qa_udf_integer(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
  
    if not hpdci.tgtTR():
        stmt = """grant execute on procedure qa_udf_integer to "role.support";"""
        output = _dci.cmdexec(stmt)
        _dci.expect_error_msg(output)
    
        stmt = """revoke execute on procedure qa_udf_integer from "role.support";"""
        output = _dci.cmdexec(stmt)
        _dci.expect_error_msg(output)
    
    _testmgr.testcase_end(desc)

def test025(desc="""UDF (SVF) in SET PARAM/PREPARE/EXECUTE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # a NCI command, only numeric or character literal is allowed as the value.
    stmt = """set param ?myval 100;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select qa_udf_integer(?myval) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare xx from
select qa_udf_integer(?myval) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare yy from
select qa_udf_integer(?) from mytable where qa_udf_integer(a) = qa_udf_integer(?);"""
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
    
    stmt = """select qa_udf_char(?myval) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare xx from
select qa_udf_char(?myval) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare yy from
select qa_udf_char(?) from mytable where qa_udf_char(d) = qa_udf_char(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute yy using ?myval, 'AAA       ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """reset param ?myval;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test026(desc="""UDF (SVF) in SET TRANSACTION/LOCK TABLE"""):
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
    
    stmt = """select *, qa_udf_integer(a)+qa_udf_integer(b)
from mytmptable
where qa_udf_integer(a)=qa_udf_integer(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """set transaction isolation level serializable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set b=qa_udf_integer(b) where a=b;"""
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
    
    stmt = """update mytmptable set b=qa_udf_integer(b) where a=b;"""
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
    
    stmt = """update mytmptable set b=qa_udf_integer(b) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # access mode
    stmt = """set transaction read only;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select *, qa_udf_integer(a)+qa_udf_integer(b)
from mytmptable
where qa_udf_integer(a)=qa_udf_integer(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # This is also the default, so the attribute is restored as well.
    stmt = """set transaction read write;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set b=qa_udf_integer(b) where a=b;"""
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
    
    stmt = """update mytmptable set b=qa_udf_integer(b) where a=b;"""
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
    
    stmt = """update mytmptable set b=qa_udf_integer(b) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # norollback option
    # TRAF stmt = """set transaction no rollback on;"""
    # TRAF output = _dci.cmdexec(stmt)
    # TRAF _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set b=qa_udf_integer(b) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # This is also the default, so the attribute is restored as well.
    # TRAF stmt = """set transaction no rollback off;"""
    # TRAF output = _dci.cmdexec(stmt)
    # TRAF _dci.expect_complete_msg(output)
    
    # restore the table
    stmt = """update mytmptable set b=a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set b=qa_udf_integer(b) where a=b;"""
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
    
    stmt = """update mytmptable set b=qa_udf_integer(b) where a=b;"""
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
    
    stmt = """update mytmptable set b=qa_udf_integer(b) where a=b;"""
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
    
    stmt = """update mytmptable set b=qa_udf_integer(b) where a=b;"""
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
    
    stmt = """update mytmptable set b=qa_udf_integer(b) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # This is also the default, so the attribute is restored as well.
    stmt = """set transaction autobegin on;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update mytmptable set b=qa_udf_integer(b) where a=b;"""
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
    
    stmt = """update mytmptable set b=qa_udf_integer(b) where a=b;"""
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
    
    stmt = """update mytmptable set b=qa_udf_integer(b) where a=b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table mytmptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test027(desc="""UDF (SVF) in STREAM (CURSOR)"""):
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
    stmt = """select qa_udf_integer(a), qa_udf_integer(b), qa_udf_char(d), qa_udf_char(e)
from stream(mytable)
where qa_udf_integer(a)=qa_udf_integer(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8006')
    
    stmt = """set table * stream timeout reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

