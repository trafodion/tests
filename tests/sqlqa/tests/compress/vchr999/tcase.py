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

# vchr999: modify from arkt1101
#   testing varchar in adjacent and non-adjacent orders
#     with string functions and expressions
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""a01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1101:A01
    #
    #  Description:        This verifies the SQL CASE feature
    #                      This tests CASE with Row Value Constructor
    #
    # =================== End Test Case Header  ===================
    #
    
    stmt = """select * from tbl1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s0""")
    #
    #  Expect 2 rows (('crinar','jessica',59250.00),
    #                 ('howard','jerry',  65000.00),
    stmt = """select last_name, first_name
,( case marital_status
when '1' then salary
when '2' then salary * 1.50
when '3' then salary * 2
end) as salary_modified
from tbl1
where dept_num <> 9000
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s1""")
    #
    #  Expect 4 rows (('crinar jessica',59250.00),('dinah',37000.00)
    #                 ('green  roger',  87750.00),('howard',16250.00))
    stmt = """select (case marital_status
when '1' then last_name
when '2' then lasT_name || ' ' || first_name
when '3' then substring(first_name from 1 for 5)
else  'nameless string'
end) as name_for_marital
, (case
when salary<40000 then salary
when salary>39999 and salary<75000 then salary *.25
when salary>74999 then salary * .50
end) as salary_modified
from tbl1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s2""")
    #
    #  Expect (('double',1) ('single',1))
    stmt = """select (case
when marital_status > '1'
then 'double'
else 'single'
end) as marital
, (select max(marital_status) from tbl1
where dept_num = 1000
group by dept_num
) as max_marital_dept1000
from tbl1
where salary > 60000
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s3""")
    #
    #  ---------------------------
    #       Id: CA.101b      CASE as a predicate of a SELECT list element.
    #  ---------------------------
    #
    #  Expect (('dinah','clark') ('jerry','howard') ('roger','green') )
    stmt = """select first_name, last_name from tbl1 where
( case (marital_status)
when '1' then 'single'
else 'double'
end
, case (dept_num)
when 1000 then '1000'
when 9000 then '9000'
when 3500 then '3500'
else '0000'
end
) >=  ('double', '9000')
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s4""")
    #
    #  Expect 2 rows (('green') ('howard'))
    stmt = """select last_name from tbl1 where
( case dept_num
when 9000
then 'a'
else 'b'
end
)
=
( case marital_status
when '2'
then 'a'
else 'b'
end
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s5""")
    #
    #  Expect 2 rows (('clark') ('crinar'))
    stmt = """select last_name from tbl1 where
( case salary
when 65000.00
then 'a'
else 'b'
end
)
=
( case
when first_name like 'r%'
then 'a'
else 'b'
end
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s6""")
    #
    #  Expect (('clark') ('crinar'))
    stmt = """select last_name from tbl1 where
( case dept_num
when 1000
then 'a'
else 'b'
end
,case salary
when 65000.00
then 'a'
else 'b'
end
)
=
( case marital_status
when '1'
then 'a'
else 'b'
end
,case
when first_name like 'r%'
then 'a'
else 'b'
end
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s7""")
    #
    stmt = """set param ?p1 10000;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 70000;"""
    output = _dci.cmdexec(stmt)
    #
    #  Expect (('clark' 'dinah') ('crinar' 'jessica') ('green' 'roger'))
    stmt = """select last_name, first_name from tbl1
where (case
when salary  > ?p1 then ?p1
when salary <= ?p2 then ?p2
end
,case
when dept_num < 3000 then ?p1
when dept_num >= 3000 then ?p2
end
)
>= (10000, 70000)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s8""")
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1101:A02
    #
    #  Description:        This verifies the SQL CASE feature.
    #                      This has tests for CASE with Table Value
    #                      Constructor.
    #
    # =================== End Test Case Header  ===================
    #
    
    #  Check that table to insert into is empty; expect ((0)).
    stmt = """select count(*) as should_be_zero from tA02
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a02s0""")
    #
    #  Check contents of tables used.
    stmt = """select first_name, last_name, dept_num
from tbl1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a02s1""")
    #
    # ---------------------------
    #      Id: CA.102a      Insert into Table CASE values WHERE CASE.
    # ---------------------------
    #
    # Scaffolding: insert CASE values in value list.
    
    stmt = """insert into tA02 values (
case trim('A' from 'AA')
when '' then 'Albert'
else  'weill'
end
,  case char_length(substring('william' from 1 for 4))
when 4 then 'william'
else 'nobody'
end
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Check results; expect (('Albert','william'))
    stmt = """select * from tA02
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a02s2""")
    stmt = """delete from tA02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    # Scaffolding: insert CASE values in value list.
    stmt = """insert into tA02 values
( case trim('A' from 'AA')
when '' then 'Albert'
else  'weill'
end
, 'First Name'
)
,( 'Last Name'
, case char_length(substring('william' from 1 for 4))
when 4 then 'william'
else 'nobody'
end
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    #
    #  Check results; expect (('Albert' 'First Name') ('Last Name' 'william'))
    stmt = """select * from tA02
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a02s3""")
    stmt = """delete from tA02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #
    #  Scaffolding.
    #  Check case results to insert below.
    #  Expect (('roger'))
    stmt = """select case marital_status
when '1' then 'roger'
when '2' then 'weill'
when '3' then 'vincent'
else 'nobody'
end from tbl1
where dept_num = 1000
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a02s4""")
    
    # Insert using subquery only.
    stmt = """insert into tA02 (l_name)
(select case marital_status
when '1' then 'roger'
when '2' then 'weill'
when '3' then 'vincent'
else 'nobody'
end from tbl1
where dept_num = 1000)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    # Same insert, but uses VALUES keyword.
    stmt = """insert into tA02 (l_name) values
(  (select case marital_status
when '1' then 'roger'
when '2' then 'weill'
when '3' then 'vincent'
else 'nobody'
end from tbl1
where dept_num = 1000)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Check results; expect 2 * ('roger'  NULL)
    stmt = """select * from tA02
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a02s5""")
    stmt = """delete from tA02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #
    #  ---------------------------
    #  Insert CASE values in value list with CASE in WHERE clause.
    #  Scaffolding.
    #  ---------------------------
    #  (1) Expect 2 rows (('crinar', 'jessica', 3500, ...)
    #     ('howard', 'jerry', 1000, ...) )
    stmt = """select *
from tbl1
where dept_num < CASE
when dept_num between 4000 and 12000  then 0
when dept_num between 1000 and  3999  then dept_num+1
else dept_num
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a02s6""")
    # (2)
    stmt = """insert into tA02 (l_name, f_name)
( select last_name, first_name from tbl1
where dept_num < CASE
when dept_num between 4000 and 12000  then 0
when dept_num between 1000 and 3999 then dept_num+1
else dept_num
end
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    #
    #  Check results then clean up.
    #  Expect 2 rows (('crinar', 'jessica')
    #     ('howard', 'jerry') )
    stmt = """select * from tA02
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a02s7""")
    stmt = """delete from tA02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1101:A03
    #
    #  Description:        This verifies the SQL CASE feature
    #                      CASE with NATURAL JOIN.
    #
    # =================== End Test Case Header  ===================
    #
    #  Basic rows.
    
    #  Expect 4 rows.
    stmt = """select *
from tbl1
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", """a03s0""")
    #
    #  Expect 6 rows.
    stmt = """select *
from tbl5
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", """a03s1""")
    #
    #  ---------------------------
    #       Id: CA.061       CASE in SELECT list of NATURAL JOIN.
    #  ---------------------------
    #
    #  Natural join on table with same columns and rows.
    #  Expect 2 rows (('clark' ...) ('green' ...))
    stmt = """select *
from tbl1
natural join tbl5
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", """a03s2""")
    #
    #  Case and Natural Join.
    #  Expect 2 rows (('clark' 'dinah' 'divorced or widowed')
    #  ('green' 'roger' 'married'))
    stmt = """select last_name, first_name
, case marital_status
when '1' then 'single'
when '2' then 'married'
else 'divorced or widowed'
end as status
from tbl1
natural join tbl5
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", """a03s3""")
    #
    #  Expect 1 rows (('green' 'roger' '310310$' 175500 900))
    stmt = """select last_name,
case
when salary >= 40000 and salary < 60000 then last_name
when salary >= 60000 and salary < 90000 then last_name || first_name
else  first_name
end as name    

, case
when dept_num <= 3000 then '*****'
when dept_num >= 3000 and dept_num <= 7000 then '#####'
else '310310\$'
end as dept_symbol
, salary, dept_num
from tbl1 natural join tbl5
where last_name like '%een%'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", """a03s4""")
    #
    #  Expect 1 rows (('green' 'roger' 'Married' 'Admin depts' 175500))
    #  (Salary in WHERE clause out of range for (('clark' 'dinah' ...)) ).
    stmt = """select last_name, first_name
, (case marital_status
when '1' then 'Unmarried'
when '2' then 'Married'
when '3' then 'Divorced or widowed'
end)
, (case
when dept_num >= 5000 then 'Admin depts'
when dept_num < 5000 then 'Tech depts'
end) as dept_symbol    

, salary
from tbl1 natural join tbl5
where case
when salary  > 50000
then salary
else salary * .5
end
>= 150000.00
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", """a03s5""")
    #
    #  ---------------------------
    #       Id: CA.062       CASE in predicates of nested NATURAL JOIN.
    #  ---------------------------
    #
    #  Expect 4 rows (('clark' ...) ('crinar'...) ('howard' ...)
    #  ('green' ...))
    stmt = """select last_name, first_name, dept_num, salary from
tbl1 t1 natural join
(tbl1 t2 natural join
(tbl1 t3 natural join
(tbl1 t4 natural join
tbl1 t5)
)
)
where case
when marital_status = '1' then salary
when marital_status = '2' then salary *0.2
when marital_status = '3' then salary *0.5
end
< 89000
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", """a03s6""")
    #
    #  Scaffold
    #  Expect 2 rows (('clark' ...) ('green' ...))
    stmt = """select *
from tbl1 t1 natural join
(tbl5 t2 natural join
(tbl1 t3 natural join
tbl5 t4))
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", """a03s7""")
    #
    #  Scaffold.
    #  Expect 2 rows (('dinah') ('green'))
    stmt = """select (case marital_status
when '1' then last_name || first_name
when '2' then last_name
when '3' then first_name
end)
from tbl1 t1 natural join
(tbl5 t2 natural join
(tbl1 t3 natural join
tbl5 t4))
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", """a03s8""")
    #
    #  Scaffold.
    #  Expect 2 rows (('dinah') ('green'))
    stmt = """select (case marital_status
when '1' then last_name || first_name
when '2' then last_name
when '3' then first_name
end) as name
from tbl1 t1 natural join tbl5 t2
where
case
when dept_num >= 1000 and dept_num <= 5000
then salary
else salary/0.2 + 10000.00
end
>= 60000.00
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", """a03s9""")
    #
    #  Expect (('green'))
    stmt = """select (case marital_status
when '1' then last_name || first_name
when '2' then last_name
when '3' then first_name
end)
from tbl1 t1 natural join
(tbl5 t2 natural join
(tbl1 t3 natural join
tbl5 t4))
where
case
when dept_num >= 1000 and dept_num <= 5000 then salary
else salary / .2 + 10000.00
end
>= 60000.00
and marital_status between '1' and '2'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", """a03s10""")
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1101:A04
    #
    #  Description:        This verifies the SQL CASE feature
    #                      CASE with RIGHT OUTER JOIN
    #
    # =================== End Test Case Header  ===================
    #
    
    #  Check contents of tables used.
    #  Expect 4 rows.
    stmt = """select first_name, last_name from tbl1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", """a04s0""")
    #  Expect 3 rows.
    stmt = """select first_name, last_name from tbl2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", """a04s1""")
    #  Expect 3 rows.
    stmt = """select l_name, f_name, mar_status
from tbl3
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", """a04s2""")
    #
    #  ---------------------------
    #       Id: CA.051       CASE in SELECT list on left of RIGHT OUTER JOIN.
    #  ---------------------------
    #
    #  Expect 3 rows:
    #  (('jones' 'gail' 'divorced or widowed') ('velcro' 'judy' 'double')
    #   (('zann' 'kathy' 'single'))
    stmt = """select tbl2.last_name, tbl2.first_name
, case tbl2.marital_status
when '1' then 'single'
when '2' then 'double'
else 'divorced or widowed'
end as marital_status
from tbl1 right outer join tbl2
on tbl1.last_name = tbl2.last_name
and tbl1.dept_num = tbl2.dept_num
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", """a04s3""")
    #
    #  Scaffolding.
    #  No match so expect null row.
    stmt = """select tbl1.salary, tbl1.dept_num
from tbl1 right outer join tbl2
on tbl1.first_name = tbl2.first_name
where tbl1.last_name like '%een'
or tbl2.last_name like '%velcro%'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", """a04s4""")
    #
    #  No match so expect null row, with '%%%%%' in What_Else column.
    stmt = """select
case
when tbl1.salary >= 40000 and tbl1.salary < 60000
then tbl1.last_name
when tbl1.salary >= 60000 and tbl1.salary < 90000
then tbl1.last_name || tbl1.first_name
else  tbl1.first_name
end
, case
when tbl1.dept_num <= 3000 then '*****'
when tbl1.dept_num >= 3000 and tbl1.dept_num <= 7000 then '#####'
else '%%%%%'
end,
tbl1.salary, tbl1.dept_num
from tbl1 right outer join tbl2
on tbl1.first_name = tbl2.first_name
where tbl1.last_name like '%een'
or tbl2.last_name like '%velcro%'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", """a04s5""")
    #
    #  Expect data for Roger Green.
    stmt = """select tbl1.last_name, tbl1.first_name
, (case tbl1.marital_status
when '1' then 'Unmarried'
when '2' then 'Married'
when '3' then 'Married but Divorced'
else 'Unknown?'
end ) as State_Of_Marriage
, (case
when tbl1.dept_num >= 5000 then 'Admin depts'
when tbl1.dept_num < 5000 then 'Tech depts'
end ) as Department
, tbl1.salary
from tbl1 right outer join tbl2
on tbl1.marital_status = tbl2.marital_status
where case
when tbl1.salary  > 50000 then tbl1.salary
else tbl1.salary * .5
end
>= 150000.00
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", """a04s6""")
    #
    #  Scaffolding.
    #  Expect data for clark (3), crinar (2), howard (1) =>
    #  ((1 1) (2 2) (3 3))
    stmt = """select marital_status, mar_status from
tbl1 t1 right outer join tbl3 t2
on t1.last_name = t2.l_name
and  t1.first_name = t2.f_name
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", """a04s7""")
    #
    #  Expect (('crinar    jessica') ('crinar    jessica'))
    stmt = """select case marital_status
when '1' then last_name
when '2' then last_name||first_name
when '3' then first_name
end,
case mar_status
when '1' then l_name
when '2' then l_name || f_name
when '3' then f_name
end
from
tbl1 t1 right outer join tbl3 t2
on t1.last_name = t2.l_name
and  t1.first_name = t2.f_name
where marital_status = '2'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", """a04s8""")
    #
    #  ---------------------------
    #       Id: CA.052       CASE in predicate of nested RIGHT OUTER JOIN.
    #  ---------------------------
    #
    #  Expect all 4 rows.
    stmt = """select last_name, first_name, dept_num, salary from
tbl1 t1 natural right outer join
(tbl1 t2 natural right outer join
(tbl1 t3 natural right outer join
(tbl1 t4 natural right outer join
tbl1 t5
)
)
)
where case
when marital_status = '1' then salary
when marital_status = '2' then salary * .2
when marital_status = '3' then salary * .5
end
< 90000
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", """a04s9""")
    #
    #  Expect (('dinah') (NULL) (NULL) (NULL))
    stmt = """select (case t4.marital_status
when '3' then t3.first_name
end) as ROJ_name
from tbl1 t3
right outer join tbl2 t4
on t3.marital_status = t4.marital_status
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", """a04s10""")
    #
    #  Expect (('crinar...' 'crinar...') ('green...' 'crinar...'))
    stmt = """select case t3.marital_status
when '1' then t3.last_name
when '2' then t3.last_name||t3.first_name
when '3' then t3.first_name
end as tbl1_name,
case t4.mar_status
when '1' then t4.l_name
when '2' then t4.l_name || t4.f_name
when '3' then t4.f_name
end as tbl3_name
from tbl1 t3
right outer join tbl3 t4
on t3.marital_status = t4.mar_status
where t4.mar_status = '2'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", """a04s11""")
    #
    #  Expect (('crinar...' 'crinar...') ('green...' 'crinar...'))
    stmt = """select case t3.marital_status
when '1' then t3.last_name
when '2' then t3.last_name||t3.first_name
when '3' then t3.first_name
end as tbl1_name,
case t4.mar_status
when '1' then t4.l_name
when '2' then t4.l_name || t4.f_name
when '3' then t4.f_name
end as tbl3_name
from tbl1 t1
right outer join tbl3 t2
on t1.last_name = t2.l_name
right outer join tbl1 t3
on t2.f_name = t3.first_name
right outer join tbl3 t4
on t3.marital_status = t4.mar_status
where t4.mar_status = '2'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", """a04s12""")
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1101:A05
    #
    #  Description:        This verifies the SQL CASE feature
    #                      in modification of primary key;
    #                      OMIT primary key until supported -- then
    #                      restore in PREUNIT and should get same results.
    #                      Also test rollback.
    #
    # =================== End Test Case Header  ===================
    #
    
    #  Check initial values.
    #  Expect 4 rows as inserted in Preunit script.
    
    stmt = """select * from tbl1 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", """a05s0""")
    #  Expect 6 rows as inserted in Preunit script.
    stmt = """select * from tbl5 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", """a05s1""")
    #
    # Begin work so can roll back changes; must make turn off
    # autocommit.
    stmt = """set transaction autocommit off;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  ---------------------------
    #       Id: CA.091       CASE in modification of Primary Key.
    #  ---------------------------
    #
    #  Scaffolding.
    #  Expect 1 row (('zann' 1)).
    stmt = """select last_name, marital_status
from tbl5
where first_name like '_ath%'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", """a05s2""")
    #
    #  Expect 6 rows with the Case mapping.
    stmt = """select last_name, marital_status
, case marital_status
when '1' then 'xerxes'
when '2' then 'yacht'
when '3' then 'zann'
end
as word_code_for_marital
from tbl5
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", """a05s3""")
    #
    # Set up transaction to roll back.
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """update tbl5
set last_name =  case marital_status
when '1' then 'Xerxes'
when '2' then 'yacht'
when '3' then 'zann'
end
where first_name like '_ath%'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    #  Except as before but kathy zann's last_name becomes Xerxes.
    stmt = """select * from tbl5 order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", """a05s4""")
    #
    # Rollback then set up new transaction to roll back.
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # When 'update primary key' is supported, alter PREUNIT to
    # make dept_num into a primary key.
    stmt = """update tbl5
set dept_num = case
when salary < 50000 then 3000
when salary >= 50000 and salary < 90000 then 5999
when salary >= 90000 then 70000
end
where last_name in ('howard', 'green', 'crinar')
and marital_status = '1'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    #  Expect as before but Jerry's department number becomes 5999.
    stmt = """select * from tbl5 order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", """a05s5""")
    #
    # Rollback then set up new transaction to roll back.
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """update tbl5
set last_name
= case
when dept_num <= 3000  then upper(last_name)
when dept_num > 3000 and dept_num <= 5000 then last_name || 'hi there'
when dept_num > 5000 then substring(last_name from 1 for 3)
end
where case marital_status
when '1' then salary
when '2' then salary*.5
when '3' then salary*1.2
end
= 80000.00
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    #  Expect as before but Kathy's last_name becomes ZANN.
    stmt = """select * from tbl5 order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", """a05s6""")
    #
    # Roll back changes and check results are as we started.
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    #  Expect 6 rows with original data.
    stmt = """select * from tbl5 order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", """a05s7""")
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1101:A06
    #
    #  Description:        This verifies the SQL CASE feature
    #                      CASE with definition of View.
    #                      See also arkt1199.a09.
    #
    # =================== End Test Case Header  ===================
    #
    
    #  Check results in base table.
    stmt = """select * from tbl5 order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", """a06s0""")
    #
    #  Scaffolding.
    #  Expect all 6 rows.
    stmt = """select last_name, dept_num
, CASE dept_num WHEN 3000 THEN 'Value A'
WHEN 4000 THEN 'Value B'
WHEN 5000 THEN 'Value C'
ELSE 'Value D'
END as case1
, CASE when salary > 50000 then 'salary is > 500000'
when marital_status  = '3' then 'Uncertain state'
else 'unknown'
END as case2
from tbl5
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", """a06s1""")
    #
    #  Expect 2 rows with data for Velcro and Zann.
    stmt = """select last_name, dept_num
, CASE dept_num WHEN 3000 THEN 'Value A'
WHEN 4000 THEN 'Value B'
WHEN 5000 THEN 'Value C'
ELSE 'Value D'
END
, CASE when salary > 50000 then 'salary is > 500000'
when marital_status  = '3' then 'Uncertain state'
else 'unknown'
END as case1
from tbl5
where dept_num  < CASE
when dept_num between 1000 and 3000   then dept_num + 1000
when dept_num between 3000 and 6000   then dept_num - 1000
else dept_num
end
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", """a06s2""")
    #
    #BEGIN_DDL
    # create a view
    
    stmt = """create view tblview5 (csimple, csearched) as select
CASE dept_num WHEN 3000 THEN 'Value A'
WHEN 4000 THEN 'Value B'
WHEN 5000 THEN 'Value C'
ELSE 'Value D'
END
,   CASE when salary > 50000 then 'salary is > 500000'
when marital_status  = '3' then 'Uncertain state'
else 'unknown'
END
from tbl5
where dept_num  < CASE
when dept_num between 1000 and 3000   then dept_num + 1000
when dept_num between 3000 and 6000   then dept_num - 1000
else dept_num
end
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # END_DDL
    #
    #  Expect 2 rows with values of Cases as for Velcro and Zann above.
    stmt = """select *  from tblview5
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", """a06s3""")
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1101:A07
    #
    #  Description:        This verifies the SQL CASE feature
    #                      CASE with Grouped views
    #
    # =================== End Test Case Header  ===================
    #
    
    #
    #  Check initial values.
    #  Expect 2 rows.
    #   select * from grpview order by 1, 2;
    stmt = """select L_NAME,F_NAME,D_NUM,MIN_SAL,MAX_SAL,cast(AVG_SAL as numeric(9,2)) as AVG_SAL
from grpview order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", """a07s0""")
    
    #  Expect 6 rows.
    stmt = """select * from tbl5 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", """a07s1""")
    #
    #  This select should be the same as the grouped view.
    #  Expect Jerry Howard and Kathy Zann's data.
    stmt = """select last_name, first_name, dept_num,  min(salary)
, min(salary) as min_sal, max(salary) as max_sal
, cast(avg(salary) as numeric(9,2)) as avg_sal
from tbl5
where marital_status = '1'
group by last_name, first_name, dept_num
having dept_num = 4000 or dept_num = 3000
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", """a07s2""")
    #
    #  ---------------------------
    #       Id: CA.031       Columns from Grouped view within CASE in SELECT list.
    #       Id: CA.032       Columns from Grouped view within CASE in predicate.
    #  ---------------------------
    #
    #  Expect Jerry Howard and Kathy Zann's data.
    stmt = """select l_name, f_name, d_num
, case d_num
when 4000 then 'jerry'
else 'kathy'
end
as case_d_num
, case
when min_sal>65000 then 'great'
else 'oops'
end
as case_min_sal
from grpview
order by l_name
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", """a07s3""")
    #
    #  Expect Kathy Zann's data.
    stmt = """select l_name, f_name, d_num
, case
when min_sal >  60000 then 'great'
when min_sal <= 60000 then 'okay'
end
from grpview
where max_sal > 70000
order by l_name
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", """a07s4""")
    #  Should get data for Jerry Howard; spaces are needed in the string
    #  in the IN clause, because names are CHAR not VARCHAR.
    stmt = """select l_name, f_name, d_num
, case
when min_sal >  60000 then 'great'
when min_sal <= 60000 then 'okay'
end
from grpview
where case l_name
when 'zann' then  f_name || l_name
when 'howard' then l_name || f_name
else 'incorrect'
end
in ('howard    jerry', 'zann      kathy', 'judy      velcro')
and max_sal < 100000
order by l_name
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  Expect Jerry Howard and Kathy Zann's data:
    #  (('howjerry') ('zann   kathy'))
    stmt = """select case d_num
when 3000 then l_name || ' ' || f_name
when 4000 then substring(lower(l_name) from 1 for 3)
|| trim(both ' ' from f_name)
else 'incorrect'
end
from grpview
where case f_name
when 'kathy' then min_sal
when 'jerry' then avg_sal
else max_sal
end
>= 60000
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", """a07s6""")
    #
    #  Expect Kathy Zann's data:
    #   select l_name, min_sal, max_sal, avg_sal from grpview
    
    stmt = """SELECT L_NAME, MIN_SAL, MAX_SAL, cast(AVG_SAL as numeric(9,2)) as AVG_SAL
FROM grpview
where case
when f_name like '%th%' then max_sal - min_sal
when f_name like '_owa%' then max_sal - avg_sal
end
>= 0
order by l_name
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", """a07s7""")
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1101:A08
    #
    #  Description:        This verifies the SQL CASE feature.
    #                      CASE with distinct with expressions in the
    #                      set functions.
    #
    # =================== End Test Case Header  ===================
    #
    
    #  ---------------------------
    #  Id: CA.021 CASE in select list uses distinct with expressions in functions.
    #  ---------------------------
    #
    #  Scaffold.
    
    stmt = """select last_name, first_name
, cast( case
when dept_num >= 1000 and dept_num <= 3000
then count( dept_num + 1000)
when dept_num > 3000 and dept_num <= 6000
then count( dept_num - 1000)
when dept_num > 6000 and dept_num <= 9000
then count( dept_num + 1000 - 1000)
end
as int )
from tbl5
group by dept_num, last_name, first_name
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", """a08s0""")
    #
    stmt = """select last_name, first_name
, cast( ( case
when dept_num >= 1000 and dept_num <= 3000
then count( dept_num + 1000)
when dept_num > 3000 and dept_num <= 6000
then count( dept_num - 1000)
when dept_num > 6000 and dept_num <= 9000
then count( dept_num + 1000 - 1000)
end
) as int )
from tbl5
where case (marital_status)
when '1' then salary
when '2' then salary*.2
when '3' then salary*.3
end
> 70000
group by dept_num, last_name, first_name, marital_status, salary
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", """a08s1""")
    #
    #  Scaffolding.
    #  Multiple DISTINCTs are legal.
    stmt = """select
max(distinct salary + 10000)
, min(distinct salary + 50000)
from tbl5
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", """a08s2""")
    #
    stmt = """select
max(distinct salary + 10000)
, cast( avg(distinct salary + 20000) as int )
, min(distinct salary + 50000)
from tbl5
group by salary
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", """a08s3""")
    #
    #  Scaffolding.
    #  Multiple DISTINCTs are legal.
    stmt = """select last_name
, max(distinct salary + 10000)
, cast( avg(distinct salary + 20000) as int )
, min(distinct salary + 50000)
from tbl5
where dept_num between 3000 and 6000
group by last_name, salary, dept_num
order by last_name
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", """a08s4""")
    #
    #  Scaffolding.
    stmt = """select last_name
, cast( case marital_status
when '1' then max(distinct salary + 10000)
when '2' then avg(distinct salary + 20000)
when '3' then min(distinct salary + 50000)
end
as int )
from tbl5
where dept_num between 3000 and 6000
group by last_name, marital_status, salary, dept_num
order by last_name
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", """a08s5""")
    #
    stmt = """select last_name
, cast( case marital_status
when '1' then max(salary + 10000)
when '2' then avg(salary + 20000)
when '3' then min(salary + 50000)
end
as int )
from tbl5
where dept_num between 3000 and 6000
group by last_name, marital_status, salary, dept_num
order by last_name
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", """a08s6""")
    #
    #  Scaffold.
    stmt = """select (first_name || ' ' || last_name) as full_name
, cast( avg(distinct salary + 10000) as int )
from tbl5
group by dept_num , first_name , last_name , salary
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", """a08s7""")
    #
    stmt = """select (first_name || ' ' || last_name) as full_name
, dept_num
, cast( case dept_num
when 3000 then avg(distinct salary + 10000)
else (10000)
end
as int )
from tbl5
group by dept_num , first_name , last_name, salary
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", """a08s8""")
    #
    #  ---------------------------
    #       Id: CA.022       CASE in predicate uses distinct with expressions in functions.
    #  ---------------------------
    #
    #  Aggregate in CASE
    #  Expect ( ( "kathy" "zann" ) )
    stmt = """select (first_name || ' ' || last_name) as full_name
from tbl5
where
case dept_num
when 3000
then (select avg(distinct salary + 10000)
from tbl5
)
else (10000)
end
> 75000
group by first_name , last_name
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", """a08s9""")
    #
    #  Aggregate in subquery in CASE
    #  Expect ( ( "kathy" "zann" ) )
    stmt = """select (first_name || ' ' || last_name) as full_name
from tbl5
where
case dept_num
when 3000 then (select avg(distinct salary + 10000) from tbl5 tsub
where tsub.dept_num = tbl5.dept_num
)
else (10000)
end
> 75000
group by first_name , last_name
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", """a08s10""")
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1101:A09
    #
    #  Description:        This verifies the SQL CASE feature
    #                      This tests CASE with Row Value Constructor
    #
    # =================== End Test Case Header  ===================
    #
    
    #  ---------------------------------
    #  Separated out from testcase 1101.A01 (test area CA.101a)
    #  because of bug.
    #  ---------------------------------
    #
    stmt = """select * from tbl1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", """a09s0""")
    stmt = """select * from tbl3 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", """a09s1""")
    #
    #  Trouble with Right Join and Case.
    #
    #  Negative tests moved to Case arkt1101:N01.
    #
    stmt = """select distinct max(t.l_name), max(t.f_name)
, case t.mar_status
when '1' then 'single'
when '2' then 'double'
when '3' then 'divorced'
else 'unknown'
end
from tbl3 t
where t.l_name = 'crinar'
group by t.l_name, t.f_name, t.mar_status
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", """a09s2""")
    #
    stmt = """select ( select
case t.mar_status
when '1' then 'single'
when '2' then 'double'
when '3' then 'divorced'
else 'unknown'
end
from tbl3 t
where t.l_name = 'crinar'
group by t.l_name, t.mar_status
)
from tbl1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", """a09s3""")
    #
    stmt = """select (select distinct max(t.l_name)
from tbl3 t
where t.l_name = 'crinar'
group by t.l_name, t.mar_status
)
from tbl1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", """a09s4""")
    #
    stmt = """select (select distinct max(t.l_name)
from tbl3 t
where t.l_name = 'crinar'
group by t.l_name, t.mar_status
)
from tbl1 right join tbl3
on tbl1.last_name = tbl3.l_name
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", """a09s5""")
    #
    stmt = """select distinct max(t.l_name)
, case t.mar_status
when '1' then 'single'
when '2' then 'double'
else 'unknown'
end
from tbl3 t right join tbl3
on   tbl3.l_name = 'crinar'
where   t.l_name = 'crinar'
group by t.l_name, t.mar_status
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", """a09s6""")
    #
    #  Case and Right Join;
    #  ON clause forced TRUE (1=1).
    stmt = """select (select case t.mar_status
when '1' then 'single'
when '2' then 'double'
else 'unknown'
end
from tbl3 t
where t.l_name = 'crinar'
group by t.l_name, t.mar_status
)
from tbl1 right join tbl3
on (1=1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", """a09s7""")
    #
    
    #
    stmt = """select
case t.mar_status
when '1' then 'single'
when '2' then 'double'
when '3' then 'divorced'
else 'unknown'
end
from tbl3 t
where t.l_name = 'crinar'
group by t.l_name, t.f_name, t.mar_status
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", """a09s8""")
    stmt = """select tbl1.last_name, tbl1.first_name
, case tbl1.dept_num
when 9000 then 'admin dept'
when 3000 then 'sales dept'
else          'other dept'
end
, (select
case t.mar_status
when '1' then 'single'
when '2' then 'double'
when '3' then 'divorced'
else 'unknown'
end
from tbl3 t
where t.l_name = 'crinar'
group by t.l_name, t.f_name, t.mar_status
)
from tbl1 right join tbl3
on (1=1)      -- << --
and tbl1.first_name = tbl3.f_name
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", """a09s9""")
    
    _testmgr.testcase_end(desc)

