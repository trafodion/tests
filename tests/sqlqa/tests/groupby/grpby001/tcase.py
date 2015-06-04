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

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA01
    #  Description:        Tests for SQL, use of Case (with
    #			values) with other string functions.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    ##1 different kind of datatypes in case stmt - numeric
    stmt = """SELECT
case
when salary < 40000 then salary *2
when salary <70000 then salary *1.5
else salary
end
from emp
group by
case
when salary < 40000 then salary *2
when salary <70000 then salary *1.5
else salary
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s1""")
    
    stmt = """SELECT
case
marital_status
when 1 then last_name || first_name
when 2 then substring(trim(' '  from first_name) ||
trim(' ' from last_name ) from 4 for 8)
end
from emp
group by
case
marital_status
when 1 then last_name || first_name
when 2 then substring(trim(' '  from first_name) ||
trim(' ' from last_name ) from 4 for 8)
end ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s2""")
    
    stmt = """SELECT
case
--select ubin1_n2,char0_n10,date1_n4,
substring(char0_n10 from 1 for 1)
when 'A'  then 'its A'
when 'B'   then 'its B'
else ' is Null'
end
from b2uns01
where sbin0_uniq < 5
group by
case
substring(char0_n10 from 1 for 1)
when 'A'  then 'its A'
when 'B'   then 'its B'
else ' is Null'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s3""")
    
    stmt = """SELECT
case
--select ubin1_n2,char0_n10,date1_n4,
trim('A' from char0_n10 )
when ''  then 'its A'
when 'B'   then 'its B'
else ' is Null'
end
from b2uns01
where sbin0_uniq < 5
group by
case
trim('A' from char0_n10 )
when ''  then 'its A'
when 'B'   then 'its B'
else ' is Null'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s4""")
    
    stmt = """SELECT
case
--select ubin1_n2,char0_n10,date1_n4,
trim('A' from char0_n10 )
when ''  then 'its zero String'
when 'B' then 'its B'
else 'its Null'
end
from b2uns01
where sbin0_uniq < 5
group by
case
trim('A' from char0_n10 )
when ''  then 'its zero String'
when 'B' then 'its B'
else 'its Null'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s5""")
    
    stmt = """SELECT
case
trim('0' from char0_09_uniq)
when '1423' then substring(char0_09_uniq from 7 for 2)
when '1035' then
trim(leading '0' from char0_09_uniq)
else char0_az_uniq
end   ,
case substring(char0_az_uniq from 1 for 3)
when 'diaaae' then 'Wrong'
when 'dia' then 'right'
when 'eaa' then 'Right'
when 'fda' then 'Fad'
else 'Other Values'
end
,    case substring(varchar0_money_100 from 1 for 1 )
when '$' then 'Money'
else 'Junk'
end
from b3uns01
where udec1_uniq <10
group by
case
trim('0' from char0_09_uniq)
when '1423' then substring(char0_09_uniq from 7 for 2)
when '1035' then
trim(leading '0' from char0_09_uniq)
else char0_az_uniq
end   ,
case substring(char0_az_uniq from 1 for 3)
when 'diaaae' then 'Wrong'
when 'dia' then 'right'
when 'eaa' then 'Right'
when 'fda' then 'Fad'
else 'Other Values'
end
,    case substring(varchar0_money_100 from 1 for 1 )
when '$' then 'Money'
else 'Junk'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s6""")
    
    _testmgr.testcase_end(desc)

def test002(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA02
    #  Description:        Test SQL for use of Case (with values)
    #			on the predicates of non key columns in
    #			combo with other string function and
    #			params.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT
case
marital_status
when 1 then last_name || first_name
when 2 then substring(trim(' '  from first_name) || trim(' ' from
last_name ) from 4 for 8)
end
from emp
where last_name = case marital_status
when 1 then last_name
when 2 then first_name
end
group by
case
marital_status
when 1 then last_name || first_name
when 2 then substring(trim(' '  from first_name) || trim(' ' from
last_name ) from 4 for 8)
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", """a02s1""")
    
    # simple case function mixed with searched case function
    stmt = """set param ?p1 'HOWARD';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 'KING';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 'MARTIN';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
marital_status
when 1 then last_name || first_name
when 2 then substring(trim(' '  from first_name) ||
trim(' ' from last_name ) from 4 for 8)
end
from emp
where last_name = case marital_status
when 1 then case last_name
when upper('howard') then  'HOWARD'
when upper('king') then 'KING'
when 'MARTIN' then case
when salary = 65000.00 then
cast(?p1 as char(10))
when salary = 69000.00 then
cast(?p2 as char(10))
when salary = 64000.00 then
cast(?p3 as char(10))
end
end
when 2 then case
when salary = 175500.00 then 'GREEN'
when salary = 39500.00 then 'CRINAR'
end
end
group by
case
marital_status
when 1 then last_name || first_name
when 2 then substring(trim(' '  from first_name) ||
trim(' ' from last_name ) from 4 for 8)
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", """a02s2""")
    
    #  searched case function mixed with simple case function
    stmt = """SELECT
case
marital_status
when 1 then last_name || first_name
when 2 then substring(trim(' '  from first_name) ||
trim(' ' from last_name ) from 4 for 8)
end
from emp
where last_name = case
when marital_status = 1 then case
when last_name = upper('howard') then  'HOWARD'
when last_name = upper('king') then 'KING'
when last_name = 'MARTIN' then case salary
when 65000.00 then
cast(?p1 as char(10))
when 69000.00 then
cast(?p2 as char(10))
when 64000.00 then
cast(?p3 as char(10))
end
end
when marital_status = 2 then case salary
when 175500.00 then 'GREEN'
when 39500.00 then 'CRINAR'
end
end
group by
case
marital_status
when 1 then last_name || first_name
when 2 then substring(trim(' '  from first_name) ||
trim(' ' from last_name ) from 4 for 8)
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", """a02s3""")
    
    stmt = """SELECT
case
ubin1_n2
when 0 then ubin1_n2
else ubin1_n2
end
from b2uns01
group by
case
ubin1_n2
when 0 then ubin1_n2
else ubin1_n2
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", """a02s4""")
    
    stmt = """set param ?p1 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 0;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
ubin1_n2
when ?p1 then ?p2
else ?p3
end
from b2uns01
group by
case
ubin1_n2
when ?p1 then ?p2
else ?p3
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", """a02s5""")
    
    stmt = """set param ?p1 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 0;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
ubin1_n2
when ?p1 then ?p2
else ?p3
end
from b2uns01
where sbin0_uniq < 5
group by
case
ubin1_n2
when ?p1 then ?p2
else ?p3
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", """a02s6""")
    
    stmt = """SELECT
case
ubin1_n2
when 0 then 0
else null
end
from b2uns01
group by
case
ubin1_n2
when 0 then 0
else null
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", """a02s7""")
    
    stmt = """set param ?p 'param';"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT
case
varchar1_ascii_uniq
when 'Z,' then ?p
when 'k,' then 'lower ascii'
else 'special'
end
from b3uns01
where udec1_uniq < 10
group by
case
varchar1_ascii_uniq
when 'Z,' then ?p
when 'k,' then 'lower ascii'
else 'special'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", """a02s8""")
    
    stmt = """set param ?p 'param';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 'exception value';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
when varchar1_ascii_uniq = 'Z,' then cast(?p as char(15))
when varchar1_ascii_uniq = 'k,' then 'lower ascii'
else cast(?p1 as varchar(15))
end
from b3uns01
where udec1_uniq < 10
group by
case
when varchar1_ascii_uniq = 'Z,' then cast(?p as char(15))
when varchar1_ascii_uniq = 'k,' then 'lower ascii'
else cast(?p1 as varchar(15))
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", """a02s9""")
    
    _testmgr.testcase_end(desc)

def test003(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA03
    #  Description:        Tests for SQL, use of Case (with
    #                      search conditions) with aggregates in
    #			the predicates.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT
case
sbin0_uniq
when 4 then sbin0_uniq/2
when 3 then sbin0_uniq -1
end
from b2uns01
group by
case
sbin0_uniq
when 4 then sbin0_uniq/2
when 3 then sbin0_uniq -1
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", """a03s1""")
    
    stmt = """SELECT
case
when sbin0_uniq > 100 then sbin0_uniq
else sbin0_uniq/2
end
from b2uns01
group by
case
when sbin0_uniq > 100 then sbin0_uniq
else sbin0_uniq/2
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", """a03s2""")
    
    stmt = """SELECT
case
when sbin0_uniq < 100 then sbin0_uniq
else sbin0_uniq/2
end
from b2uns01
group by
case
when sbin0_uniq < 100 then sbin0_uniq
else sbin0_uniq/2
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", """a03s3""")
    
    stmt = """SELECT
case
when first_name like 'JE%' then trim(first_name)
when trim(first_name) like 'DI%'
then substring(first_name from 1 for 5)
end
from emp
group by
case
when first_name like 'JE%' then trim(first_name)
when trim(first_name) like 'DI%'
then substring(first_name from 1 for 5)
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", """a03s4""")
    
    stmt = """SELECT
case
when salary < 40000 then first_name
when salary < 80000 then trim(first_name)
else substring(first_name from 1 for 3)
end
from emp
group by
case
when salary < 40000 then first_name
when salary < 80000 then trim(first_name)
else substring(first_name from 1 for 3)
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", """a03s5""")
    
    stmt = """SELECT
case
when trim(first_name) like 'JE%' then salary
when substring(first_name from 1 for 5)
like 'DI%' then salary * 2
end
from emp
group by
case
when trim(first_name) like 'JE%' then salary
when substring(first_name from 1 for 5)
like 'DI%' then salary * 2
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", """a03s6""")
    
    _testmgr.testcase_end(desc)

def test004(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA04
    #  Description:        Tests for SQL, use of Case (with
    #                      values) with aggregates.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT
case
marital_status
when 1 then salary
when 2 then salary * 1.5
when 3 then salary * 2
end
from emp
group by
case
marital_status
when 1 then salary
when 2 then salary * 1.5
when 3 then salary * 2
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", """a04s1""")
    
    stmt = """SELECT
case
marital_status
when 1 then salary
when 2 then salary * 1.5
when 3 then salary * 2
end
from emp
group by
case
marital_status
when 1 then salary
when 2 then salary * 1.5
when 3 then salary * 2
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", """a04s2""")
    
    stmt = """SELECT
case
when  sum(sbin0_uniq) < 10600 then sum(sbin0_uniq)
end
from b2pns01
where udec1_100 < 10
group by
case
when  sum(sbin0_uniq) < 10600 then sum(sbin0_uniq)
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """SELECT
case
when  sum(sbin0_uniq) < 10600 then sum(sbin0_uniq)
else avg(sbin0_uniq)
end
from b2pns01
where udec1_100 < 10
group by
case
when  sum(sbin0_uniq) < 10600 then sum(sbin0_uniq)
else avg(sbin0_uniq)
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """SELECT
case
max( char0_aazy_20 )
when 'C' then 'Double'
else 'Single'
end
from b3uns05
where sbin0_uniq < 10
group by
case
max( char0_aazy_20 )
when 'C' then 'Double'
else 'Single'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4185')
    
    stmt = """SELECT
case  char0_aazy_20
when 'C' then 'Double'
else 'Single'
end
from b3uns05
where sbin0_uniq < 10
group by
case  char0_aazy_20
when 'C' then 'Double'
else 'Single'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", """a04s6""")
    
    _testmgr.testcase_end(desc)

def test005(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA05
    #  Description:        Tests for SQL, use of Case (both
    #                      values) in the select list.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    stmt = """SELECT
case
varchar1_ascii_uniq
when 'c0' then 123.56
when 'r;' then 1408285.1734
else 99999999
end
from b3uns01
where udec1_uniq < 10
group by
case
varchar1_ascii_uniq
when 'c0' then 123.56
when 'r;' then 1408285.1734
else 99999999
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", """a05s1""")
    
    stmt = """SELECT
case
when sbin0_uniq = ubin1_n2  then 'Value is zero'
when sbin0_uniq = sdec0_n500  then 'value is one'
else 'value is neither zero nor one'
end
from b2uns01
where sbin0_uniq < 5
group by
case
when sbin0_uniq = ubin1_n2  then 'Value is zero'
when sbin0_uniq = sdec0_n500  then 'value is one'
else 'value is neither zero nor one'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", """a05s2""")
    
    _testmgr.testcase_end(desc)

def test006(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA06
    #  Description:        Tests for SQL, use of Case (with
    #                      search conditions) with other string
    #			functions.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT
case
when salary < 40000 then last_name
when salary > 40000 and salary < 70000 then
position('R' in  last_name || first_name   )
when salary > 70000 and salary <100000 then
substring(first_name from 2 for 5)
else trim (last_name) || trim(first_name)
end
from emp
group by
case
when salary < 40000 then last_name
when salary > 40000 and salary < 70000 then
position('R' in  last_name || first_name   )
when salary > 70000 and salary <100000 then
substring(first_name from 2 for 5)
else trim (last_name) || trim(first_name)
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4049')
    
    stmt = """SELECT
case
when salary < 40000 then last_name
when salary > 40000 and salary < 70000 then
last_name || first_name
when salary > 70000 and salary <100000 then
substring(first_name from 2 for 5)
else trim (last_name) || trim(first_name)
end
from emp
group by
case
when salary < 40000 then last_name
when salary > 40000 and salary < 70000 then
last_name || first_name
when salary > 70000 and salary <100000 then
substring(first_name from 2 for 5)
else trim (last_name) || trim(first_name)
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", """a06s2""")
    
    _testmgr.testcase_end(desc)

def test007(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA07
    #  Description:        Tests for SQL, use of Case with
    #                      IN clause.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT
case
when last_name in ('CRINAR','GREEN') then 'Valid'
when first_name in ('DINAH','ROGER','JESSICA') THEN 'NOT VALID'
when dept_num <5000 then 'Junkk'
end
from emp
group by
case
when last_name in ('CRINAR','GREEN') then 'Valid'
when first_name in ('DINAH','ROGER','JESSICA') THEN 'NOT VALID'
when dept_num <5000 then 'Junkk'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", """a07s1""")
    
    stmt = """SELECT
case
when last_name in ('CRINAR','GREEN') then 'Valid'
when first_name in ('DINAH','ROGER','JESSICA') THEN 'NOT VALID'
when dept_num <5000 then dept_num
end
from emp
group by
case
when last_name in ('CRINAR','GREEN') then 'Valid'
when first_name in ('DINAH','ROGER','JESSICA') THEN 'NOT VALID'
when dept_num <5000 then dept_num
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4049')
    
    _testmgr.testcase_end(desc)

def test008(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA08
    #  Description:        Tests for SQL, use of Case with
    #                      aggregates and string functions.
    #			(char length and trim).
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT
case
char_length(trim('0' from char0_09_uniq))
when 1 then upshift ('length is 1')
when 2 then upshift('length is 2')
when 3 then upshift('length is 3')
else ('Length is >= 4')
end
from b3uns01
group by
case
char_length(trim('0' from char0_09_uniq))
when 1 then upshift ('length is 1')
when 2 then upshift('length is 2')
when 3 then upshift('length is 3')
else ('Length is >= 4')
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", """a08s1""")
    
    stmt = """SELECT
case
char_length(trim('0' from char0_09_uniq))
when 1 then upshift ('length is 1')
when 2 then upshift('length is 2')
when 3 then upshift('length is 3')
else ('Length is >= 4')
end
from b3uns01
where udec1_uniq  <10
group by
case
char_length(trim('0' from char0_09_uniq))
when 1 then upshift ('length is 1')
when 2 then upshift('length is 2')
when 3 then upshift('length is 3')
else ('Length is >= 4')
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", """a08s2""")
    
    stmt = """SELECT
max(case char0_aazy_20
when 'C' then 'Double'
else 'Single'
end)
from b3uns05
where sbin0_uniq < 20
group by
max(case char0_aazy_20
when 'C' then 'Double'
else 'Single'
end)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """SELECT
case
min(char0_aazy_20 )
when 'C' then 'Double'
else 'Single'
end
from b3uns05
where sbin0_uniq < 10
group by
case
min(char0_aazy_20 )
when 'C' then 'Double'
else 'Single'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4185')
    
    stmt = """SELECT
case
count(*)
when 1 then 'Fine'
else 'error'
end
from b2uwl02
where char10_nuniq = 'AAAAAAAA'
group by
case
count(*)
when 1 then 'Fine'
else 'error'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4185')
    
    stmt = """SELECT
case
max(trim('0' from char0_09_uniq))
when '905' then 'the number is 905'
else    'it is Wrong'
end
from b3uns01
group by
case
max(trim('0' from char0_09_uniq))
when '905' then 'the number is 905'
else    'it is Wrong'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4185')
    
    stmt = """SELECT
case
when max(sbin0_uniq) > 1498 then sbin0_uniq
when min(sbin0_uniq) < 1 then sbin0_uniq
end
from b2uns01
group by
case
when max(sbin0_uniq) > 1498 then sbin0_uniq
when min(sbin0_uniq) < 1 then sbin0_uniq
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """SELECT
case
max(salary)
when 175500 then salary
else salary *2    end
from emp
where emp.dept_num = 9000
group by
case
max(salary)
when 175500 then salary
else salary *2    end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4185')
    
    stmt = """SELECT
max( case
when salary <40000 then salary * 2
when salary < 70000 then salary * 1.5
else salary
end )
from emp
group by
max( case
when salary <40000 then salary * 2
when salary < 70000 then salary * 1.5
else salary
end )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    _testmgr.testcase_end(desc)

def test009(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA09
    #  Description:        Tests for SQL, use of Case (search
    #                      conditions) with BETWEEN.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT
case
when salary <40000 then salary
when salary between 41000 and 65000   then salary *.25
when salary >66000 then salary *.50
end
from emp
group by
case
when salary <40000 then salary
when salary between 41000 and 65000   then salary *.25
when salary >66000 then salary *.50
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", """a09s1""")
    
    stmt = """SELECT
case
when salary between 0 and 40000 then salary *2
when salary between 0 and 75000 then salary *1.5
else salary
end
from emp
group by
case
when salary between 0 and 40000 then salary *2
when salary between 0 and 75000 then salary *1.5
else salary
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", """a09s2""")
    
    stmt = """prepare q3 from
SELECT
case
when salary between 10000 and 40000 then salary * 2
when salary between 40000 and 80000 then salary * 1.5
else salary
end
from emp
where salary between case
when dept_num = 9000 then 10000
when dept_num = 1000 then 40000
else 80000
end
and case
when dept_num = 9000 then 40000
when dept_num = 1000 then 80000
else 100000
end
group by
case
when salary between 10000 and 40000 then salary * 2
when salary between 40000 and 80000 then salary * 1.5
else salary
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute q3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", """a09s3""")
    
    _testmgr.testcase_end(desc)

def test010(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA10
    #  Description:        Tests for SQL, use of Case (with
    #                      values) with params, literals, boundary
    #			conditions.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """set param ?p1 21;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 22;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 23;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
udec1_uniq
when ?p1 then 'Twenty'
when ?p2 then 'One'
when ?p3 then 'Two'
else 'Greater'
end
from b3uns01
where udec1_uniq < 21
group by
case
udec1_uniq
when ?p1 then 'Twenty'
when ?p2 then 'One'
when ?p3 then 'Two'
else 'Greater'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", """a10s1""")
    
    stmt = """set param ?p1 21;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 22;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 23;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
udec1_uniq
when 21 then ?p1
when 22 then ?p2
when 23 then ?p3
else 'Greater'
end
from b3uns01
where udec1_uniq between 20 and 25
group by
case
udec1_uniq
when 21 then ?p1
when 22 then ?p2
when 23 then ?p3
else 'Greater'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", """a10s2""")
    
    stmt = """set param ?p 'a';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
trim(?p from ch1)
when 'asd' then 'ERRR'
end
from xlong
group by
case
trim(?p from ch1)
when 'asd' then 'ERRR'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """set param ?p 'a';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
when ?p is null then date '1995-07-01'
else date '1995-06-01'
end
from xlong
group by
case
when ?p is null then date '1995-07-01'
else date '1995-06-01'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """set param ?p1 'abc';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 '';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 'abc';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
(?p1 || ?p2)
when ?p1 then 'Hi'
when ?p3 then Null
end
from emp
group by
case
(?p1 || ?p2)
when ?p1 then 'Hi'
when ?p3 then Null
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4049')
    
    stmt = """set param ?p1 10000;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 37000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
salary
when ?p1 then ?p1
when ?p2 then ?p2
else salary
end
from emp
group by
case
salary
when ?p1 then ?p1
when ?p2 then ?p2
else salary
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", """a10s6""")
    
    ##expectfile ${test_dir}/a010exp a10s7
    stmt = """SELECT
case
salary
when ?p1 then ?p1 || ?p3
when ?p2 then ?p2
else salary
end
from emp
group by
case
salary
when ?p1 then ?p1 || ?p3
when ?p2 then ?p2
else salary
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """SELECT
case
salary
when ?p1 then ?p1
when ?p2 then ?p2
else salary
end
from emp
group by
case
salary
when ?p1 then ?p1
when ?p2 then ?p2
else salary
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", """a10s8""")
    
    stmt = """set  param ?p1 10000;"""
    output = _dci.cmdexec(stmt)
    stmt = """set  param ?p2 37000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
when ?p1 is null   then ?p1
when ?p2 > ?p1 then ?p2
else salary
end
from emp
group by
case
when ?p1 is null   then ?p1
when ?p2 > ?p1 then ?p2
else salary
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4049')
    
    stmt = """set  param ?p1 10000;"""
    output = _dci.cmdexec(stmt)
    stmt = """set  param ?p2 37000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
when ?p1 is null   then salary
when ?p2 > salary then ?p2
else salary
end
from emp
group by
case
when ?p1 is null   then salary
when ?p2 > salary then ?p2
else salary
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", """a10s10""")
    
    stmt = """set  param ?p1 10000;"""
    output = _dci.cmdexec(stmt)
    stmt = """set  param ?p2 37000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
when ?p1 is not null   then salary
when ?p2 < salary then ?p2
else salary
end
from emp
group by
case
when ?p1 is not null   then salary
when ?p2 < salary then ?p2
else salary
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", """a10s11""")
    
    stmt = """set  param ?p1 10000;"""
    output = _dci.cmdexec(stmt)
    stmt = """set  param ?p2 37000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
when ?p1 <> ?p1        then salary
when ?p2 < salary then ?p2
else salary
end
from emp
group by
case
when ?p1 <> ?p1        then salary
when ?p2 < salary then ?p2
else salary
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", """a10s12""")
    
    stmt = """set param ?p1 'abc';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
when ?p1 <> ?p2        then salary *2
when ?p2 < salary then ?p2
else salary
end
from emp
group by
case
when ?p1 <> ?p2        then salary *2
when ?p2 < salary then ?p2
else salary
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    stmt = """set param ?p1 '1';"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile ${test_dir}/a010exp a10s14
    stmt = """SELECT
case ''
when ?p1 then 'Fine'
else ''
end
from emp
group by
case ''
when ?p1 then 'Fine'
else ''
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """SELECT
case
?p1
when ?p1 then 'Fine'
else 'ERROR'     end
from emp
group by
case
?p1
when ?p1 then 'Fine'
else 'ERROR'     end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", """a10s15""")
    
    stmt = """SELECT
case
xs
when 4294967393 then 'Value is max'
when x then 'Wrong Value' end
from tmp5
group by
case
xs
when 4294967393 then 'Value is max'
when x then 'Wrong Value' end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """SELECT
case
x
when 4294967293 then xs
when x+2  then x end
from tmp5
group by
case
x
when 4294967293 then xs
when x+2  then x end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """SELECT
case
x
when 9223372036854775807 then x
when x  then x+1  end
from tmp5
group by
case
x
when 9223372036854775807 then x
when x  then x+1  end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """set param ?p1 32767;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
xvc
when ?p1 then 'Valid'
else 'Null'
end
from tmp5
group by
case
xvc
when ?p1 then 'Valid'
else 'Null'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """set param ?p1 '';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
xvc
when ?p1 then 'Valid'
else 'Null'
end
from tmp5
group by
case
xvc
when ?p1 then 'Valid'
else 'Null'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test011(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA11
    #  Description:        Tests for SQL, use of Case (search
    #                      condition) in use with nulls.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT
case
when  varchar1_ascii_uniq is not null then null
when varchar1_ascii_uniq is null then null
end
from b3uns01
where udec1_uniq < 10
group by
case
when  varchar1_ascii_uniq is not null then null
when varchar1_ascii_uniq is null then null
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a011exp""", """a11s1""")
    
    stmt = """SELECT
case
when char0_n10 is null  then 'Char0_n10 is null'
when date1_n4 is null   then 'date1_n4 is null'
when ubin1_n2 is null then 'ubin1_n2  is Null'
end
from b2uns01
where sbin0_uniq < 5
group by
case
when char0_n10 is null  then 'Char0_n10 is null'
when date1_n4 is null   then 'date1_n4 is null'
when ubin1_n2 is null then 'ubin1_n2  is Null'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a011exp""", """a11s2""")
    
    stmt = """SELECT
case
trim('A' from char0_n10 )
when 'A'  then 'its A'
when 'B'   then 'its B'
else ' is Null'
end
from b2uns01
where sbin0_uniq < 5
group by
case
trim('A' from char0_n10 )
when 'A'  then 'its A'
when 'B'   then 'its B'
else ' is Null'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a011exp""", """a11s3""")
    
    stmt = """SELECT
case
trim('A' from char0_n10 )
when ''  then 'its A'
when 'B'   then 'its B'
else ' is Null'
end
from b2uns01
where sbin0_uniq < 5
group by
case
trim('A' from char0_n10 )
when ''  then 'its A'
when 'B'   then 'its B'
else ' is Null'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a011exp""", """a11s4""")
    
    _testmgr.testcase_end(desc)

def test012(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA12
    #  Description:        Tests for SQL, -ve tests for combination
    #			of different data types (int, char, Null,
    #			datetime, real) in CASE.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT
case
sbin0_uniq
when 0  then 'Value is zero'
when '1'  then 'value is one'
else 'value is neither zero nor one'
end
from b2uns01
where sbin0_uniq < 5
group by
case
sbin0_uniq
when 0  then 'Value is zero'
when '1'  then 'value is one'
else 'value is neither zero nor one'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    stmt = """SELECT
case
char0_n10
when null  then 'Value is Null'
when 'AD'  then 'value is one'
else 'value is neither zero nor one'
end
from b2uns01
where sbin0_uniq < 5
group by
case
char0_n10
when null  then 'Value is Null'
when 'AD'  then 'value is one'
else 'value is neither zero nor one'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4099')
    
    stmt = """SELECT
case
char0_n10
when 10  then 'Value is Null'
when 'AD'  then 'value is one'
else 'value is neither zero nor one'
end
from b2uns01
where sbin0_uniq < 5
group by
case
char0_n10
when 10  then 'Value is Null'
when 'AD'  then 'value is one'
else 'value is neither zero nor one'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    stmt = """SELECT
case
date1_n4
when '2100-01-03'  then 'Value is 3rd Jan'
when '2100-01-02'  then 'value is 2nd Jan'
else 'value is neither zero nor one'
end
from b2uns01
where sbin0_uniq < 5
group by
case
date1_n4
when '2100-01-03'  then 'Value is 3rd Jan'
when '2100-01-02'  then 'value is 2nd Jan'
else 'value is neither zero nor one'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    stmt = """SELECT
case
date1_n4
when 2100-01-03  then 'Value is 3rd Jan'
when 2100-01-02  then 'value is 2nd Jan'
else 'value is neither zero nor one'
end
from b2uns01
where sbin0_uniq < 5
group by
case
date1_n4
when 2100-01-03  then 'Value is 3rd Jan'
when 2100-01-02  then 'value is 2nd Jan'
else 'value is neither zero nor one'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    stmt = """SElECT
case
real1_uniq
when 2100-01-03  then 'Value is 3rd Jan'
when 2100-01-02  then 'value is 2nd Jan'
else 'value is neither zero nor one'
end
from b2uns01
where sbin0_uniq < 5
group by
case
real1_uniq
when 2100-01-03  then 'Value is 3rd Jan'
when 2100-01-02  then 'value is 2nd Jan'
else 'value is neither zero nor one'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a012exp""", """a12s6""")
    
    stmt = """SELECT
case
real1_uniq
when '2100-01-03'  then 'Value is 3rd Jan'
when '2100-01-02' then 'value is 2nd Jan'
else 'value is neither zero nor one'
end
from b2uns01
where sbin0_uniq < 5
group by
case
real1_uniq
when '2100-01-03'  then 'Value is 3rd Jan'
when '2100-01-02' then 'value is 2nd Jan'
else 'value is neither zero nor one'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    stmt = """SELECT
case
sdec0_n500
when 1 then timestamp  '1995-05-01:12:59:59.9999'
when 2 then 'value is 2'
end
from b2uns01
where sbin0_uniq < 5
group by
case
sdec0_n500
when 1 then timestamp  '1995-05-01:12:59:59.9999'
when 2 then 'value is 2'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4049')
    
    stmt = """SELECT
case
sdec0_n500
when 1 then timestamp '1995-05-01 12:59:54.0000'
when 2          then 'value is 2'
end
from b2uns01
where sbin0_uniq < 5
group by
case
sdec0_n500
when 1 then timestamp '1995-05-01 12:59:54.0000'
when 2          then 'value is 2'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4049')
    
    stmt = """SELECT
case
real1_uniq
when  2100-01-03 then   2100-01-03
when .1023600E+03 then .1023600E+03
else timestamp '1000-10-20 12:30:45.9999'
end
from b2uns01
where sbin0_uniq < 5
group by
case
real1_uniq
when  2100-01-03 then   2100-01-03
when .1023600E+03 then .1023600E+03
else timestamp '1000-10-20 12:30:45.9999'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4049')
    
    stmt = """SELECT
case
int0_ytom_nuniq
when interval '05-09' year(5)  to month
then timestamp '2005-09-06 12:30:45.9999'
else interval '05-09' year(5) to month
end
from b2pns01
where sbin0_uniq < 5
group by
case
int0_ytom_nuniq
when interval '05-09' year(5)  to month
then timestamp '2005-09-06 12:30:45.9999'
else interval '05-09' year(5) to month
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4049')
    
    stmt = """SELECT
case
date1_n4
when Null then 'Value is Null'
when '2100-01-01' then 'it is jan 1st 2100'
end
from b2uns01
group by
case
date1_n4
when Null then 'Value is Null'
when '2100-01-01' then 'it is jan 1st 2100'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4099')
    
    _testmgr.testcase_end(desc)

def test013(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA13
    #  Description:        Tests for SQL, use of Case with
    #			different datatypes (datetime).
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT
case
marital_status
when 1 then current_date
when 2 then timestamp '1995-07-10 03:35:59.999999'
when 3 then timestamp '1995-07-10 15:40:25.999999'
end
from emp
group by
case
marital_status
when 1 then current_date
when 2 then timestamp '1995-07-10 03:35:59.999999'
when 3 then timestamp '1995-07-10 15:40:25.999999'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4049')
    
    stmt = """SELECT
case
date0_nuniq
when current_date then  current_date
else timestamp '1995-07-11 15:40:25.999999'
end
from b2unl15
where sbin0_uniq < 5
group by
case
date0_nuniq
when current_date then  current_date
else timestamp '1995-07-11 15:40:25.999999'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4049')
    
    stmt = """SELECT
case
sbin0_uniq
when 1 then current_date
when 2 then timestamp '1995-07-10 03:35:59.999999'
when 3 then timestamp '1995-07-10 03:35:59.999999'
end
from b2uns01
where sbin0_uniq < 5
group by
case
sbin0_uniq
when 1 then current_date
when 2 then timestamp '1995-07-10 03:35:59.999999'
when 3 then timestamp '1995-07-10 03:35:59.999999'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4049')
    
    stmt = """SELECT
case
real1_uniq
when  2100-01-03 then   2100-01-03
when .1023600E+03 then .1023600E+03
else 1000*10-20
end
from b2uns01
where sbin0_uniq < 5
group by
case
real1_uniq
when  2100-01-03 then   2100-01-03
when .1023600E+03 then .1023600E+03
else 1000*10-20
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a013exp""", """a13s4""")
    
    stmt = """SELECT
case
real1_uniq
when  2100-01-03 then   1
when .1023600E+03 then .1023600E+03
else 100
end
from b2uns01
where sbin0_uniq < 5
group by
case
real1_uniq
when  2100-01-03 then   1
when .1023600E+03 then .1023600E+03
else 100
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a013exp""", """a13s5""")
    
    _testmgr.testcase_end(desc)

def test014(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA14
    #  Description:        Tests for SQL, use of Case with
    #                      empty strings (zero length).
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT
case
trim('A' from char0_n10 )
when ''  then 'its A'
when 'B'   then 'its B'
else ' is Null'
end
from b2uns01
where sbin0_uniq < 5
group by
case
trim('A' from char0_n10 )
when ''  then 'its A'
when 'B'   then 'its B'
else ' is Null'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a014exp""", """a14s1""")
    
    stmt = """SELECT
case
trim('A' from char0_n10 )
when ''  then 'its zero String'
when 'B'   then 'its B'
else 'its Null'
end
from b2uns01
where sbin0_uniq < 5
group by
case
trim('A' from char0_n10 )
when ''  then 'its zero String'
when 'B'   then 'its B'
else 'its Null'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a014exp""", """a14s2""")
    
    stmt = """set param ?p1 '';"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT
case ''
when ?p1 then 'Fine'
else 'Error'
end
from emp
group by
case ''
when ?p1 then 'Fine'
else 'Error'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a014exp""", """a14s3""")
    
    _testmgr.testcase_end(desc)

def test015(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA17
    #  Description:        Tests for SQL, use of Case in
    #                      subqueries.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT
case
when udec1_nuniq < 25 then 1
when udec1_nuniq < 50 then 2
when udec1_nuniq < 75 then 3
end
from b2pns03
group by
case
when udec1_nuniq < 25 then 1
when udec1_nuniq < 50 then 2
when udec1_nuniq < 75 then 3
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a015exp""", """a15s1""")
    
    stmt = """SELECT
case
when sbin0_uniq = (select sdec1_uniq
from btuns01
where sdec1_uniq = 0)
then 'value is zero'
else 'value is not zero'
end
from btuns01
group by
case
when sbin0_uniq = (select sdec1_uniq
from btuns01
where sdec1_uniq = 0)
then 'value is zero'
else 'value is not zero'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """SELECT
case
when salary >0 and salary < 40000 or salary = 39500
then salary *1.5
when salary in (select salary
from emp
where emp.salary
= employ.salary)
then salary
else salary
end
from employ
group by
case
when salary >0 and salary < 40000 or salary = 39500
then salary *1.5
when salary in (select salary
from emp
where emp.salary
= employ.salary)
then salary
else salary
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    _testmgr.testcase_end(desc)

def test016(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA18
    #  Description:        Tests for SQL, use of Nested Case,
    #                      also nested Case in Predicates (where
    #			and having).
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT
case
sum(select case when dept_no = 9000 then salary *1.2
else salary
end
from emp )
when 100000 then 'salary'
else 'Error'
end
from emp
group by
case
sum(select case when dept_no = 9000 then salary *1.2
else salary
end
from emp )
when 100000 then 'salary'
else 'Error'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select
case when (select salary from emp where dept_no = 9000)
then salary * 1.12
else salary
end
from emp
group by
case
when (select salary from emp where dept_no = 9000)
then salary * 1.12
else salary
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT
case
sbin0_uniq
when 100 then real1_uniq
else null
end
from b2pns01
where real1_uniq = (select  sum(case sbin0_uniq
when 100 then real1_uniq
else null
end
)
from b2pns01)
group by
case
sbin0_uniq
when 100 then real1_uniq
else null
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a016exp""", """a16s3""")
    
    stmt = """SELECT
case
sbin0_uniq
when 100 then sbin0_uniq
else null
end
from b2pns01
group by
case
sbin0_uniq
when 100 then sbin0_uniq
else null
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a016exp""", """a16s4""")
    
    stmt = """set param ?p1 1000;"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT
case
when real1_uniq in (select real1_uniq
from b2uns09)  then
real1_uniq
else null end
from b2uns01
where case
when real1_uniq in (select real1_uniq
from b2uns09)  then
real1_uniq
else null end
= (select real1_uniq
from b2uns09
where real1_uniq = ?p1)
group by
case
when real1_uniq in (select real1_uniq
from b2uns09)  then
real1_uniq
else null end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    ##expectfile ${test_dir}/a016exp a16s6
    stmt = """select
case
when substring(char0_09_uniq from 1 for 2)
= any (select case when substring(char0_09_uniq from 1 for 2)
= '00'
then '00'
else '01'
end
from b3uns01)
then 'Exists'
else 'Not Exists'
end
where case when substring(char0_09_uniq from 1 for 2)
= any (select case when substring(char0_09_uniq from 1 for 2)
= '00'
then '00'
else '01'
end
from b3uns01)
then 'Exists'
else 'Not Exists'
end
= 'Exists'
group by
case
when substring(char0_09_uniq from 1 for 2)
= any (select case when substring(char0_09_uniq from 1 for 2)
= '00'
then '00'
else '01'
end
from b3uns01)
then 'Exists'
else 'Not Exists'
end
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select
case when first_name in
(select first_name
from emp
where first_name = 'DINAH')
then 10000
else 20000
end
from emp
where sum(case when first_name in
(select first_name
from emp
where first_name = 'DINAH')
then 10000
else 20000
end) < 100000
group by
case when first_name in
(select first_name
from emp
where first_name = 'DINAH')
then 10000
else 20000
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select
case when first_name in
(select first_name
from emp
where first_name = 'DINAH')
then 10000
else 20000
end
from emp
group by
case when first_name in
(select first_name
from emp
where first_name = 'DINAH')
then 10000
else 20000
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """SELECT
case
char0_n10
when 'AD' then case sbin0_uniq
when 1401 then 'value = 1401'
when 1407 then 'value = 1407'
else 'don''t care for this value'
end
when 'BB' then case sbin0_uniq
when 1419 then 'value = 1419'
else 'passed'
end
end
from b2uns01
where sbin0_uniq >= 1400 and
sbin0_uniq < 1450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a016exp""", """a16s9""")
    stmt = """group by
case
char0_n10
when 'AD' then case sbin0_uniq
when 1401 then 'value = 1401'
when 1407 then 'value = 1407'
else 'don''t care for this value'
end
when 'BB' then case sbin0_uniq
when 1419 then 'value = 1419'
else 'passed'
end
end
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
case
char0_n10
when 'AD' then case
when sbin0_uniq = 1401 then 'value = 1401'
when sbin0_uniq = 1407 then 'value = 1407'
when sbin0_uniq > 1430 then 'a large value'
else 'don''t care for this value'
end
when 'BB' then case sbin0_uniq
when 1419 then 'value = 1419BB'
else 'value passed'
end
end
from b2uns01
where sbin0_uniq >= 1400 and
sbin0_uniq < 1450
group by
case
char0_n10
when 'AD' then case
when sbin0_uniq = 1401 then 'value = 1401'
when sbin0_uniq = 1407 then 'value = 1407'
when sbin0_uniq > 1430 then 'a large value'
else 'don''t care for this value'
end
when 'BB' then case sbin0_uniq
when 1419 then 'value = 1419BB'
else 'value passed'
end
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a016exp""", """a16s10""")
    
    stmt = """SELECT
case
when char0_n10 = 'AD' then case sbin0_uniq
when 1401 then 'value = 1401'
when 1407 then 'value = 1407'
else 'don''t care for this value'
end
when char0_n10 = 'BB' then case sbin0_uniq
when 1419 then 'value = 1419'
else 'passed'
end
end
from b2uns01
where sbin0_uniq >= 1400 and
sbin0_uniq < 1450
group by
case
when char0_n10 = 'AD' then case sbin0_uniq
when 1401 then 'value = 1401'
when 1407 then 'value = 1407'
else 'don''t care for this value'
end
when char0_n10 = 'BB' then case sbin0_uniq
when 1419 then 'value = 1419'
else 'passed'
end
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a016exp""", """a16s11""")
    
    stmt = """SELECT
case
when char0_n10 = 'AD' then case
when sbin0_uniq = 1401 then 'value = 1401'
when sbin0_uniq = 1407 then 'value = 1407'
when sbin0_uniq > 1430 then 'a large value'
else 'don''t care for this value'
end
when char0_n10 = 'BB' then case sbin0_uniq
when 1419 then 'value = 1419BB'
else 'value passed'
end
end
from b2uns01
where sbin0_uniq >= 1400 and
sbin0_uniq < 1450
group by
case
when char0_n10 = 'AD' then case
when sbin0_uniq = 1401 then 'value = 1401'
when sbin0_uniq = 1407 then 'value = 1407'
when sbin0_uniq > 1430 then 'a large value'
else 'don''t care for this value'
end
when char0_n10 = 'BB' then case sbin0_uniq
when 1419 then 'value = 1419BB'
else 'value passed'
end
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a016exp""", """a16s12""")
    
    #  Three level nested cases function
    stmt = """SELECT
case
char0_n10
when 'AD' then case
when sbin0_uniq = 1401 then case udec1_100
when 1 then '1 found'
else 'not found'
end
when sbin0_uniq = 1407 then case udec1_100
when 7 then '7 found'
end
when sbin0_uniq > 1430 then 'a large value'
else 'do not care for this value'
end
when 'BB' then case sbin0_uniq
when 1419 then case
when udec1_100 = 19 then '19BB'
end
else 'value passed'
end
end
from b2uns01
where sbin0_uniq >= 1400 and
sbin0_uniq < 1450
group by
case
char0_n10
when 'AD' then case
when sbin0_uniq = 1401 then case udec1_100
when 1 then '1 found'
else 'not found'
end
when sbin0_uniq = 1407 then case udec1_100
when 7 then '7 found'
end
when sbin0_uniq > 1430 then 'a large value'
else 'do not care for this value'
end
when 'BB' then case sbin0_uniq
when 1419 then case
when udec1_100 = 19 then '19BB'
end
else 'value passed'
end
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a016exp""", """a16s13""")
    
    stmt = """SELECT
case
when char0_n10 = 'AD' then case
when sbin0_uniq = 1401 then case udec1_100
when 1 then '1 found'
else 'not found'
end
when sbin0_uniq = 1407 then case udec1_100
when 7 then '7 found'
end
when sbin0_uniq > 1430 then 'a large value'
else 'don''t care for this value'
end
when char0_n10 = 'BB' then case sbin0_uniq
when 1419 then '1419BB'
when 1420 then '1420BB'
end
end
from b2uns01
where sbin0_uniq >= 1400 and
sbin0_uniq < 1450
group by
case
when char0_n10 = 'AD' then case
when sbin0_uniq = 1401 then case udec1_100
when 1 then '1 found'
else 'not found'
end
when sbin0_uniq = 1407 then case udec1_100
when 7 then '7 found'
end
when sbin0_uniq > 1430 then 'a large value'
else 'don''t care for this value'
end
when char0_n10 = 'BB' then case sbin0_uniq
when 1419 then '1419BB'
when 1420 then '1420BB'
end
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a016exp""", """a16s14""")
    
    _testmgr.testcase_end(desc)

def test017(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN01
    #  Description:        Tests for SQL, use of Case (both
    #                      values) in the select list.  This is
    #			a negative test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #searched case with case expression
    stmt = """SELECT
case
salary
when salary < 40000 then salary
when salary >40000 and salary  < 70000
then salary  * 1.5
when salary >60000 then salary * 2
end
from emp
group by
case
salary
when salary < 40000 then salary
when salary >40000 and salary  < 70000
then salary  * 1.5
when salary >60000 then salary * 2
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  case typed in twice
    stmt = """SELECT
case
when salary < 40000 then salary
when salary >40000 and salary  < 70000
then salary  * 1.5
when salary >60000 then salary * 2
end
from emp
group by
case
when salary < 40000 then salary
when salary >40000 and salary  < 70000
then salary  * 1.5
when salary >60000 then salary * 2
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n001exp""", """n01s2""")
    
    #expression in the when clause omitted
    stmt = """SELECT
case
when  then salary
when salary >30000 and salary  <75000  then salary *.25
when salary >60000 then salary *.50
end
from emp
group by
case
when  then salary
when salary >30000 and salary  <75000  then salary *.25
when salary >60000 then salary *.50
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #case-expression omitted
    stmt = """SELECT
case
when 'INA' then first_name
when 'ESS' then first_name || substring(last_name from 1)
else last_name
end
from emp
group by
case
when 'INA' then first_name
when 'ESS' then first_name || substring(last_name from 1)
else last_name
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  result-expression-n omitted
    stmt = """SELECT
case
varchar1_ascii_uniq
when 'Z,' then ''
when 'k,' then 'lower ascii'
else 'special'
end
from b3uns01
where udec1_uniq < 10
group by
case
varchar1_ascii_uniq
when 'Z,' then ''
when 'k,' then 'lower ascii'
else 'special'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n001exp""", """n01s5""")
    
    #  result-expression-n in the THEN clause are special characters
    ##expectfile ${test_dir}/n001exp n01s6
    stmt = """SELECT
case
varchar1_ascii_uniq
when 'c0' then  '%'
when 'r;' then  '#'
else '&'
end
from b3uns01
where udec1_uniq < 10
group by
case
varchar1_ascii_uniq
when 'c0' then  '%'
when 'r;' then  '#'
else '&'
end
;"""
    output = _dci.cmdexec(stmt)
    
    #  then clause omitted
    stmt = """SELECT
case
varchar1_ascii_uniq
when 'Z,'
when 'k,' then 'lower ascii'
else 'special'
end
from b3uns01
where udec1_uniq < 10
group by
case
varchar1_ascii_uniq
when 'Z,'
when 'k,' then 'lower ascii'
else 'special'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  when clause omitted
    ##expectfile ${test_dir}/n001exp n01s8
    stmt = """SELECT
case
then 'upper ascii'
when 'k,' then 'lower ascii'
else 'special'
end
from b3uns01
where udec1_uniq < 10
group by
case
then 'upper ascii'
when 'k,' then 'lower ascii'
else 'special'
end
;"""
    output = _dci.cmdexec(stmt)
    
    #  when omitted
    stmt = """SELECT
case
varchar1_ascii_uniq
'Z,'	then 'upper ascii'
when 'k,' then 'lower ascii'
else 'special'
end
from b3uns01
where udec1_uniq < 10
group by
case
varchar1_ascii_uniq
'Z,'	then 'upper ascii'
when 'k,' then 'lower ascii'
else 'special'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  result-expression in the ELSE clause omitted
    stmt = """SELECT
case
varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
else
end
from b3uns01
where udec1_uniq < 10
group by
case
varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
else
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    
    #  else omitted
    stmt = """SELECT
case
varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
'special'
end
from b3uns01
where udec1_uniq < 10
group by
case
varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
'special'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n001exp""", """n01s11""")
    
    #  ELSE result-expression has a different value than
    #  result-expression in the THEN clause
    stmt = """SELECT
case
varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
else 99999999
end
from b3uns01
where udec1_uniq < 10
group by
case
varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
else 99999999
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4049')
    
    #  ELSE result-expression has a special characters
    ##expectfile ${test_dir}/n001exp n01s13
    stmt = """SELECT
case
varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
else '&%'
end
from b3uns01
where udec1_uniq < 10
group by
case
varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
else '&%'
end
;"""
    output = _dci.cmdexec(stmt)
    
    #  THEN result-expressions have different data types
    stmt = """SELECT
case
varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 123.454
else 99999999
end
from b3uns01
where udec1_uniq < 10
group by
case
varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 123.454
else 99999999
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4049')
    
    #  two case-expressions used
    ##expectfile ${test_dir}/n001exp n01s15
    stmt = """SELECT
case
varchar1_ascii_uniq, char0_09_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
else 'special'
end
from b3uns01
where udec1_uniq < 10
group by
case
varchar1_ascii_uniq, char0_09_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
else 'special'
end
;"""
    output = _dci.cmdexec(stmt)
    
    #  case-expression differs from expression-n
    stmt = """SELECT
case
udec1_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
else 'special'
end
from b3uns01
where udec1_uniq < 10
group by
case
udec1_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
else 'special'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    #  unmatched result-expressions
    stmt = """SELECT
case
varchar1_ascii_uniq
when 'Z,' then DATE '04/22/1998'
when 'k,' then 'lower ascii'
else 'special'
end
from b3uns01
where udec1_uniq < 10
group by
case
varchar1_ascii_uniq
when 'Z,' then DATE '04/22/1998'
when 'k,' then 'lower ascii'
else 'special'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4049')
    
    #  two result-expression in simple case function
    stmt = """SELECT
case
varchar1_ascii_uniq
when 'Z,' then 'upper ascii' 'upper ascii'
when 'k,' then 'lower ascii'
else 'special'
end
from b3uns01
where udec1_uniq < 10
group by
case
varchar1_ascii_uniq
when 'Z,' then 'upper ascii' 'upper ascii'
when 'k,' then 'lower ascii'
else 'special'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n001exp""", """n01s18""")
    
    #  two then clause in the simple case funtion
    ##expectfile ${test_dir}/n001exp n01s19
    stmt = """SELECT
case
varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
else 'special'
end
from b3uns01
where udec1_uniq < 10
group by
case
varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
else 'special'
end
;"""
    output = _dci.cmdexec(stmt)
    
    #  two then clause in the seached case function
    stmt = """SELECT
case
when varchar1_ascii_uniq = 'Z,' then then 'upper ascii'
when varchar1_ascii_uniq = 'k,' then 'lower ascii'
else 'special'
end
from b3uns01
where udec1_uniq < 10
group by
case
when varchar1_ascii_uniq = 'Z,' then then 'upper ascii'
when varchar1_ascii_uniq = 'k,' then 'lower ascii'
else 'special'
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  two when clause in the simple case function
    stmt = """SELECT
case
select (case varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when when 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when when 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  two when clause in the searched case function
    stmt = """SELECT
case
select (case
when when varchar1_ascii_uniq = 'Z,' then 'upper ascii'
when varchar1_ascii_uniq = 'k,' then 'lower ascii'
else 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case
when when varchar1_ascii_uniq = 'Z,' then 'upper ascii'
when varchar1_ascii_uniq = 'k,' then 'lower ascii'
else 'special'
end),char0_09_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  two else in the simple case function
    stmt = """SELECT
case
select (case varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then'lower ascii'
else else 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then'lower ascii'
else else 'special'
end),char0_09_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  two else in the searched case function
    stmt = """SELECT
case
select (case
when varchar1_ascii_uniq = 'Z,' then 'upper ascii'
when varchar1_ascii_uniq = 'k,' then 'lower ascii'
else else 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case
when varchar1_ascii_uniq = 'Z,' then 'upper ascii'
when varchar1_ascii_uniq = 'k,' then 'lower ascii'
else else 'special'
end),char0_09_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  misspelled else in simple case function
    stmt = """SELECT
case
select (case varchar1_ascii_uniq
when 'Z,' them 'upper ascii'
when 'k,' then'lower ascii'
elsse 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case varchar1_ascii_uniq
when 'Z,' them 'upper ascii'
when 'k,' then'lower ascii'
elsse 'special'
end),char0_09_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  misspelled else in searched case function
    stmt = """SELECT
case
select (case
when varchar1_ascii_uniq = 'Z,' then 'upper ascii'
when varchar1_ascii_uniq = 'k,' then'lower ascii'
els 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case
when varchar1_ascii_uniq = 'Z,' then 'upper ascii'
when varchar1_ascii_uniq = 'k,' then'lower ascii'
els 'special'
end),char0_09_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  misspelled when in simple case function
    stmt = """SELECT
case
select (case varchar1_ascii_uniq
whe 'Z,' then 'upper ascii'
when 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case varchar1_ascii_uniq
whe 'Z,' then 'upper ascii'
when 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  misspelled when in searched case function
    stmt = """SELECT
case
select (case
when varchar1_ascii_uniq = 'Z,' then 'upper ascii'
whem varchar1_ascii_uniq = 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case
when varchar1_ascii_uniq = 'Z,' then 'upper ascii'
whem varchar1_ascii_uniq = 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  misspelled then in simple case function
    stmt = """SELECT
case
select (case varchar1_ascii_uniq
when 'Z,' ther 'upper ascii'
when 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case varchar1_ascii_uniq
when 'Z,' ther 'upper ascii'
when 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  misspelled then in searched case function
    stmt = """SELECT
case
select (case
when varchar1_ascii_uniq = 'Z,' whan 'upper ascii'
whem varchar1_ascii_uniq = 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case
when varchar1_ascii_uniq = 'Z,' whan 'upper ascii'
whem varchar1_ascii_uniq = 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  misspelled then in simple case function
    stmt = """SELECT
case
select (zawd varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (zawd varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  misspelled case in searched case function
    stmt = """SELECT
case
select (case
when varchar1_ascii_uniq = 'Z,' than 'upper ascii'
when varchar1_ascii_uniq = 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case
when varchar1_ascii_uniq = 'Z,' than 'upper ascii'
when varchar1_ascii_uniq = 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  non-exist colume name in simple case function
    stmt = """SELECT
case
select (case har1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case har1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  non-exist colume name in simple case function
    stmt = """SELECT
case
select (case
when varchar1_ascii_uniq = 'Z,' then 'upper ascii'
when har1_ascii_uniq = 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case
when varchar1_ascii_uniq = 'Z,' then 'upper ascii'
when har1_ascii_uniq = 'k,' then'lower ascii'
else 'special'
end),char0_09_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  two end in the simple case function
    stmt = """SELECT
case
select (case varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then'lower ascii'
else 'special'
end end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then'lower ascii'
else 'special'
end end),char0_09_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  two end in the searched case function
    stmt = """SELECT
case
select (case
when when varchar1_ascii_uniq = 'Z,' then 'upper ascii'
when varchar1_ascii_uniq = 'k,' then 'lower ascii'
else 'special'
end end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case
when when varchar1_ascii_uniq = 'Z,' then 'upper ascii'
when varchar1_ascii_uniq = 'k,' then 'lower ascii'
else 'special'
end end),char0_09_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  two result-expression in searched case function
    stmt = """SELECT
case
select (case
when varchar1_ascii_uniq = 'Z,' then 'upper ascii', 'upper ascii'
when varchar1_ascii_uniq = 'k,' then 'lower ascii'
else 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case
when varchar1_ascii_uniq = 'Z,' then 'upper ascii', 'upper ascii'
when varchar1_ascii_uniq = 'k,' then 'lower ascii'
else 'special'
end),char0_09_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  invalid search condition
    stmt = """SELECT
case
select (case
when varchar1_ascii_uniq > 100   then 'upper ascii'
when varchar1_ascii_uniq = 'aab' then 'lower ascii'
else 'special'
end),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case
when varchar1_ascii_uniq > 100   then 'upper ascii'
when varchar1_ascii_uniq = 'aab' then 'lower ascii'
else 'special'
end),char0_09_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  unmatched result-expressions
    stmt = """SELECT
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then DATE '04/22/1998'
when sbin0_uniq = sdec0_n500  then 'value is one'
else 'value is neither zero nor one'
end
from b2uns01
where sbin0_uniq < 5
group by
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then DATE '04/22/1998'
when sbin0_uniq = sdec0_n500  then 'value is one'
else 'value is neither zero nor one'
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  unmatched result-expressions
    stmt = """SELECT
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then TIME '15:44:00'
when sbin0_uniq = sdec0_n500  then 'value is one'
else 'value is neither zero nor one'
end
from b2uns01
where sbin0_uniq < 5
group by
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then TIME '15:44:00'
when sbin0_uniq = sdec0_n500  then 'value is one'
else 'value is neither zero nor one'
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  unmatched result-expressions
    stmt = """SELECT
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then 'Value is zero'
when sbin0_uniq = sdec0_n500  then INTERVAL '9' YEAR
else 'value is neither zero nor one'
end
from b2uns01
where sbin0_uniq < 5
group by
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then 'Value is zero'
when sbin0_uniq = sdec0_n500  then INTERVAL '9' YEAR
else 'value is neither zero nor one';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  unmatched result-expression-n with result-expression
    #  in the ELSE clause.
    stmt = """SELECT
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then 'Value is zero'
when sbin0_uniq = sdec0_n500  then 'value is one'
else 9999999999
end
from b2uns01
where sbin0_uniq < 5
group by
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then 'Value is zero'
when sbin0_uniq = sdec0_n500  then 'value is one'
else 9999999999
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  ELSE result-expression has a special character
    stmt = """SELECT
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then $
when sbin0_uniq = sdec0_n500  then \
else &
end
from b2uns01
where sbin0_uniq < 5
group by
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then $
when sbin0_uniq = sdec0_n500  then \
else &
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  THEN result-expressions have different data types
    stmt = """SELECT
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then 'Value is zero'
when sbin0_uniq = sdec0_n500  then 23.99
else 9999999999
end
from b2uns01
where sbin0_uniq < 5
group by
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then 'Value is zero'
when sbin0_uniq = sdec0_n500  then 23.99
else 9999999999
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  else omitted
    stmt = """SELECT
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then 'Value is zero'
when sbin0_uniq = sdec0_n500  then 'value is one'
'special'
end
from b2uns01
where sbin0_uniq < 5
group by
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then 'Value is zero'
when sbin0_uniq = sdec0_n500  then 'value is one'
'special'
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  missing END clause in the searched case function
    stmt = """SELECT
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then 'Value is zero'
when sbin0_uniq = sdec0_n500  then 'value is one'
else 'special'
from b2uns01
where sbin0_uniq < 5
group by
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then 'Value is zero'
when sbin0_uniq = sdec0_n500  then 'value is one'
else 'special';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  misspelled END clause in the searched case function
    stmt = """SELECT
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then 'Value is zero'
when sbin0_uniq = sdec0_n500  then 'value is one'
else 'special'
emd
from b2uns01
where sbin0_uniq < 5
group by
case
select sbin0_uniq,ubin1_n2,sdec0_n500,
case
when sbin0_uniq = ubin1_n2  then 'Value is zero'
when sbin0_uniq = sdec0_n500  then 'value is one'
else 'special';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  misspelled END clause in the simple case function
    stmt = """SELECT
case
select (case varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
else 'special'
enf ),char0_09_uniq
from b3uns01
where udec1_uniq < 10
group by
case
select (case varchar1_ascii_uniq
when 'Z,' then 'upper ascii'
when 'k,' then 'lower ascii'
else 'special'
enf ),char0_09_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

def test018(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN02
    #  Description:        Tests for SQL, use of nested Case
    #                      (both values) in the select list. This
    #                      is a negative test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  nested CASE word omitted in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested CASE word omitted in searched case
    stmt = """SELECT
case
select (case
when sbin0_uniq = 100 then udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq = 100 then udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case missing END in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case missing END in searched case
    stmt = """SELECT
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case misspelled END in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
ens
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
ens
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case misspelled END in searched case
    stmt = """SELECT
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
efm
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
efm
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case misspelled case in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then cass udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then cass udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case misspelled case in searched case
    stmt = """SELECT
case
select (case
when sbin0_uniq = 100 then cas udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq = 100 then cas udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case misspelled then in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then 'value is 0'
when 68 the 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then 'value is 0'
when 68 the 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case misspelled when in searched case
    stmt = """SELECT
case
select (case
when sbin0_uniq = 100 then case udec1_100
whem 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq = 100 then case udec1_100
whem 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case misspelled when in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 the case udec1_100
whem 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 the case udec1_100
whem 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case misspelled then in searched case
    stmt = """SELECT
case
select (case
when sbin0_uniq = 100 them case udec1_100
whe 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq = 100 them case udec1_100
whe 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case missing then in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0  'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0  'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case missing then in searched case
    stmt = """SELECT
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0  'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0  'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case missing else in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0  'value is 0'
when 68 then 'value is 68'
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0  'value is 0'
when 68 then 'value is 68'
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case misspelled else in searched case
    stmt = """SELECT
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0  'value is 0'
when 68 then 'value is 68'
wles null
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0  'value is 0'
when 68 then 'value is 68'
wles null
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case missing result-expression in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then 'value is 0'
when 68 then
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then 'value is 0'
when 68 then
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case missing result-expression in searched case
    stmt = """SELECT
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0 then 'value is 0'
when 68 then
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0 then 'value is 0'
when 68 then
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case missing expression in when clause in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then 'value is 0'
when then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then 'value is 0'
when then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case missing expression in when clause in searched case
    stmt = """SELECT
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0 then 'value is 0'
when then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0 then 'value is 0'
when then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case missing reserved word when in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case udec1_100
0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case udec1_100
0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case missing reserved word when in searched case
    stmt = """SELECT
case
select (case
when sbin0_uniq = 100 then case udec1_100
0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq = 100 then case udec1_100
0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  non-exist column name in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case sc1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case sc1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  non-exist column name in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case
when udec1_100 = 0 then 'value is 0'
when yedf1_234 = 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case
when udec1_100 = 0 then 'value is 0'
when yedf1_234 = 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case case in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case case udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case case udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case case in searched case
    stmt = """SELECT
case
select (case
when sbin0_uniq 100 then case case udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq 100 then case case udec1_100
when 0 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case with two expressions in the when clause in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0, 77 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0, 77 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case with two expressions in when clause in searched case
    stmt = """SELECT
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0, 77 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0, 77 then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case with two result-expressions in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then 'value is 0', 'done'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then 'value is 0', 'done'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case with two result-expressions in searched case
    stmt = """SELECT
case
select (case
when sinb0_uniq = 100 then case udec1_100
when 0 then 'value is 0', 'done'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sinb0_uniq = 100 then case udec1_100
when 0 then 'value is 0', 'done'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case with two then in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case with two then in search case
    stmt = """SELECT
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0 then then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0 then then 'value is 0'
when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case with two when clause in simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then 'value is 0'
when when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0 then 'value is 0'
when when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case with two when clause in searched case
    stmt = """SELECT
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0 then 'value is 0'
when when 68 then 'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0 then 'value is 0'
when when 68 then 'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case missing then clause in the simple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0  'value is 0'
when 68  'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0  'value is 0'
when 68  'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case missing then clause in the search case
    stmt = """SELECT
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0  'value is 0'
when 68  'value is 68'
end
else 'value not = 100'
end)
from b2pns01
group by
case
select (case
when sbin0_uniq = 100 then case udec1_100
when 0  'value is 0'
when 68  'value is 68'
end
else 'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  missing result-expression in the else caluse in smple case
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0  then 'value is 0'
when 68 then 'value is 68'
end
else
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0  then 'value is 0'
when 68 then 'value is 68'
end
else
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  missing result-expression in the else clause in searched case
    stmt = """SELECT
case
select (case sbin0_uniq
when sbin0_uniq = 100 then case udec1_100
when 0  then 'value is 0'
when 68 then 'value is 68'
end
else
end)
from b2pns01
group by
case
select (case sbin0_uniq
when sbin0_uniq = 100 then case udec1_100
when 0  then 'value is 0'
when 68 then 'value is 68'
end
else
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  missing reserved word else in simple case function
    stmt = """SELECT
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0  then 'value is 0'
when 68 then 'value is 68'
end
'value not = 100'
end)
from b2pns01
group by
case
select (case sbin0_uniq
when 100 then case udec1_100
when 0  then 'value is 0'
when 68 then 'value is 68'
end
'value not = 100'
end);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  inner and outer case functions have different result-expressions.
    stmt = """SELECT
case
select char0_n10, case
when char0_n10 = 'AD' then case
when sbin0_uniq = 1401 then case udec1_100
when 1 then '1 found'
else 'not found'
end
when sbin0_uniq = 1407 then case udec1_100
when 7 then '7 found'
end
when sbin0_uniq > 1430 then 'a large value'
else 'don''t care for this value'
end
when char0_n10 = 'BB' then case sbin0_uniq
when 1419 then 19
when 1420 then 20
end
end
from b2uns01
where sbin0_uniq >= 1400 and
sbin0_uniq < 1450
group by
case
select char0_n10, case
when char0_n10 = 'AD' then case
when sbin0_uniq = 1401 then case udec1_100
when 1 then '1 found'
else 'not found'
end
when sbin0_uniq = 1407 then case udec1_100
when 7 then '7 found'
end
when sbin0_uniq > 1430 then 'a large value'
else 'don''t care for this value'
end
when char0_n10 = 'BB' then case sbin0_uniq
when 1419 then 19
when 1420 then 20
end
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case has two end
    stmt = """SELECT
case
select char0_n10, case
when char0_n10 = 'AD' then case
when sbin0_uniq = 1401 then case udec1_100
when 1 then '1 found'
else 'not found'
end
when sbin0_uniq = 1407 then case udec1_100
when 7 then '7 found'
end
when sbin0_uniq > 1430 then 'a large value'
else 'don''t care for this value'
end
when char0_n10 = 'BB' then case sbin0_uniq
when 1419 then '19'
when 1420 then '20'
end end
end
from b2uns01
where sbin0_uniq >= 1400 and
sbin0_uniq < 1450
group by
case
select char0_n10, case
when char0_n10 = 'AD' then case
when sbin0_uniq = 1401 then case udec1_100
when 1 then '1 found'
else 'not found'
end
when sbin0_uniq = 1407 then case udec1_100
when 7 then '7 found'
end
when sbin0_uniq > 1430 then 'a large value'
else 'don''t care for this value'
end
when char0_n10 = 'BB' then case sbin0_uniq
when 1419 then '19'
when 1420 then '20'
end end
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  nested case missing resule-expression in the else clause
    stmt = """SELECT
case
select char0_n10, case
when char0_n10 = 'AD' then case
when sbin0_uniq = 1401 then case udec1_100
when 1 then '1 found'
else 'not found'
end
when sbin0_uniq = 1407 then case udec1_100
when 7 then '7 found'
end
when sbin0_uniq > 1430 then 'a large value'
else
end
when char0_n10 = 'BB' then case sbin0_uniq
when 1419 then '19'
when 1420 then '20'
end
end
from b2uns01
where sbin0_uniq >= 1400 and
sbin0_uniq < 1450
group by
case
select char0_n10, case
when char0_n10 = 'AD' then case
when sbin0_uniq = 1401 then case udec1_100
when 1 then '1 found'
else 'not found'
end
when sbin0_uniq = 1407 then case udec1_100
when 7 then '7 found'
end
when sbin0_uniq > 1430 then 'a large value'
else
end
when char0_n10 = 'BB' then case sbin0_uniq
when 1419 then '19'
when 1420 then '20'
end
end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

