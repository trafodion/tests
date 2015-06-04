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

import time
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
    
def test001(desc="""a01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1116:A01
    #  Description:        This test verifies the SQL STRING
    #                      features on grouped views.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------------
    # Populate table.
    # ---------------------------------
    
    stmt = """delete from empA01 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into empA01 
values ('mitchell', 'andrea', 'programmer', 'female', 20000, 12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA01 
values ('WALTERS', 'MARVIN', 'systemanalyst', 'male', 20000, 15);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA01 
values ('richards', 'martha', 'SECRETARY', 'FEMALE', 30000, 12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA01 
values ('OSLO', 'DOUG', 'ENGINEER', 'MALE', 40000, 17);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA01 
values ('Young', 'Gail', 'SALESREP', 'female', 40000, 15);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA01 
values ('Weill', 'Kathy',  'Manager', 'Female', 50000, 17);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from empA01 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    # Create grouped views for using the string functions
    
    #BEGIN_DDL
    #
    # Underlying table empA01 differs from empA02; some columns in empA01
    # are char while they are varchar in test A02's empA02.
    #
    # Create a grouped view with group by in the select statement.
    
    stmt = """create view empview1 (last_name, first_name, dept_num
, AVG_SAL, MIN_SAL, MAX_SAL )
as
select last_name, first_name, dept_num,
cast(avg(salary) as int) ,
cast(min(salary) as int) ,
cast(max(salary) as int)
from empA01 
group by dept_num, last_name, first_name
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Create a grouped view with having clause in the select statement.
    stmt = """create view empview2 (last_name, first_name, job, gender)
as
select last_name, first_name, job, gender
from empA01 
group by last_name, first_name, job, gender, salary
having salary in (10000, 20000, 30000, 40000, 50000)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Create a grouped view with group by and having clauses in
    # the select statement.
    stmt = """create view empview3 (last_name, first_name)
as
select last_name, first_name from empA01 
group by last_name, first_name, gender
having LOWER(gender) = 'female'
or   LOWER(gender) = 'male'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view empview4 (last_first, job_gender )
as
select cast(last_name||first_name as char(14)),
'job = '||upper(job)||' and gender = ' || lower (job)
from empA01 
group by job, gender, last_name, first_name
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Look at values in grouped views.
    #
    stmt = """select * from empview1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    stmt = """select * from empview2 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    stmt = """select * from empview3 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    stmt = """select * from empview4 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    #  Expect 6 for each.
    
    stmt = """select cast(count(*) as int) from empview1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    stmt = """select cast(count(*) as int) from empview2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    stmt = """select cast(count(*) as int) from empview3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    stmt = """select cast(count(*) as int) from empview4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    #
    #  ANSI String functions on Columns from Group views
    #
    # -------------------------
    #  AS.021
    #  UPPER and LOWER on char and varchar columns
    # -------------------------
    stmt = """select UPPER(last_name), LOWER(first_name)
from empview1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    #
    stmt = """select UPPER( LOWER(last_name) || LOWER(first_name) )
from empview1 
where LOWER(last_name) = 'young'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    #
    stmt = """select UPPER(gender), LOWER(job) from empview2 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    #
    stmt = """select UPPER(substring(first_name from 1 for 3)) ||
LOWER(substring(first_name from 4 for 5))
from empview2 
where LOWER(gender) = 'male'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    #
    stmt = """select UPPER(trim(LEADING 'm' FROM LOWER(first_name)) ),
LOWER(trim(LEADING 'W' FROM UPPER(last_name)) )
from empview3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    #
    stmt = """select LOWER(trim(LEADING 'W' FROM UPPER(last_name )) ),
UPPER(trim(LEADING 'm' FROM LOWER(first_name)) )
from empview3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    #
    # -------------------------
    #  AS.022
    #  Arithmetic upon CHAR_LENGTH of Concatenated char and varchar
    #  columns
    # -------------------------
    #
    #  Note throughout these tests that views are based upon table
    #  empA01, where fixed-length fields are:
    #     first_name  char(13)
    #     gender      char(8)
    #  and variable-length fields are:
    #     last_name   varchar(15) not null
    #     job         varchar(15)
    #
    #  Expect length of 13 for each.
    stmt = """select first_name
, char_length(first_name) as cLen
from empview1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    #
    #  Expect length equal to number of characters for each.
    stmt = """select last_name
, char_length(last_name) as cLen
from empview1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    #
    stmt = """select last_name || first_name
, char_length(last_name || first_name) as cLen
, char_length(last_name || first_name) +1 as cLen_plus_1
, char_length(last_name || first_name) *1 as cLen_times_1
from empview1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    #
    stmt = """select last_name || first_name
, char_length(last_name || first_name) -1 as cLen_minus_1
, char_length(last_name || first_name) /1 as cLen_div_1
-- No exponentiation -- moved to 1116.N02 for Beta (1998) because unsupported.
from empview1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    #
    stmt = """select first_name || ' ' || last_name
, char_length(last_name || ' ' ||
trim(TRAILING ' ' FROM first_name ) )
from empview1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    #
    stmt = """select first_name, job, character_length(first_name || job)
from empview2 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    #
    stmt = """select last_name || first_name, job || gender,
char_length(last_name || first_name),
character_length(job || gender)
from empview2 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s21')
    #
    stmt = """select upper(first_name)||lower(last_name)||upper(job)||lower(gender),
character_length( trim(BOTH 'A' FROM upper(first_name)) ||
last_name || job ||
substring(gender from 1 for 8)
)
from empview2 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s22')
    #
    stmt = """select first_name, last_name,
character_length(substring(first_name from 1 for 4) ||
substring(last_name from 1 for 4) )
from empview3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s23')
    #
    stmt = """select first_name, last_name,
character_length(trim(TRAILING 'A' FROM first_name)
|| trim(BOTH 'R'     FROM last_name) )
from empview3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s24')
    #
    # -------------------------
    #  AS.023
    #  Arithmetic upon OCTET_LENGTH of concatenated char and varchar
    #  columns
    # -------------------------
    #
    stmt = """select last_name || first_name
, octet_length(last_name || first_name)
from empview1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s25')
    #
    stmt = """select last_name, first_name, dept_num,
octet_length(last_name || ' ' || trim(TRAILING ' ' FROM first_name )
) as octLen
from empview1 
where dept_num > 14 and dept_num < 17
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s26')
    #
    stmt = """select last_name, octet_length(last_name || gender) from empview2 
where UPPER(gender) = 'MALE'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s27')
    #
    stmt = """select last_name, first_name, job, gender,
octet_length(last_name || first_name),
octet_length(job || gender)
from empview2 
where job = 'programmer'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s28')
    #
    stmt = """select last_name,octet_length(first_name || last_name)
from empview3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s29')
    #
    #  Expect (('Kathy Weill.' 8)).
    stmt = """select first_name || ' ' || last_name || '.',
octet_length(substring(first_name FROM 1 for 4) ||
substring(last_name  FROM 1 for 4)
)
from empview3 
where char_length(last_name) =
character_length(trim(BOTH ' ' FROM first_name) )
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s30')
    #
    # -------------------------
    #  AS.024
    #  POSITION of literal in varchar
    # -------------------------
    #
    #  Expect (('mitchell andrea' 0) ('richards martha' 10))
    stmt = """select last_name || ' ' || first_name,
POSITION ('MAR' IN UPPER(last_name || ' ' || first_name) )
from empview1 
where dept_num = 12
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s31')
    #
    #  Expect (('Gail' 6))
    stmt = """select last_name, first_name,
POSITION ('Gail' IN (last_name || first_name) )
from empview2 
where gender = 'female'
and LOWER(job) = 'salesrep'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s32')
    #
    #  Expect (('OSLO' 'DOUG' 0))
    stmt = """select last_name, first_name,
POSITION ('DOG' IN (first_name || last_name))
from empview2 
where LOWER(gender) = 'male'
and UPPER(LOWER(job)) = 'ENGINEER'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s33')
    #
    #  Expect (('WALTERS MARVIN' 0 0 8))
    stmt = """select last_name || ' ' first_name
, POSITION('' IN last_name)
, POSITION('Not there' IN last_name)
, POSITION(' ' IN last_name || ' ' || first_name)
from empview3 
where last_name = 'WALTERS'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s34')
    #
    #  Expect (('andrea' 4))
    stmt = """select first_name, POSITION('chel' IN last_name)
from empview3 
where last_name LIKE '%itch%'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s35')
    #
    # -------------------------
    #  AS.025
    #  Substring in Varchar
    # -------------------------
    #
    stmt = """select last_name,
substring(last_name from -8 for 7) as blank_substr,
substring(last_name from -8 for 9) as initial_substr
from empview1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s36')
    #
    stmt = """select last_name, first_name,
substring(first_name from 1 for 15),
substring(last_name from -2 for 6 )
from empview1 
where dept_num = 12
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s37')
    #
    #  Expect (('OSLO' 'ENGINEER' 'ENGI' '')
    #          ('WALTERS' 'systemanalyst' 'syst' 'S')
    #          ('richards' 'SECRETARY' 'secr' 'ds'))
    stmt = """select last_name, job,
substring(job from 0 for 5),
substring(last_name from 7 for 2)
from empview2 
where LOWER(gender) = 'male'
or LOWER(job) = 'secretary'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s38')
    #
    stmt = """select last_name, job, substring(last_name from 1 for 7),
substring(job from 1 for 7)
from empview2 
where lower(gender) = 'female'
and   char_length(first_name) = 6
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    stmt = """select last_name, first_name ,
substring(last_name from -1) as whole_last,
substring(first_name from 1 for 4) as four_last
from empview3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s39')
    #
    #  Expect (('Weill' 'Kathy' 'ill' 'Kathy')
    #          ('Young' 'Gail'  'ung' 'Gail' ))
    stmt = """select last_name, first_name
, substring(last_name from 3 for 5) as last_3_4_5
, substring(first_name from 1) as all_first
from empview3 
where LOWER(last_name) in ('young', 'turnip', 'weill')
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s40')
    #
    # -------------------------
    #  AS.026
    #  TRIM of Concatenated literal and varchar
    # -------------------------
    #
    stmt = """select first_name
, trim(leading 'x' from
('x' || last_name || 'x' || first_name || 'x' )
)
, trim(trailing 'Q' from
('Q' || last_name || 'Q' || first_name || 'Q' )
)
from empview1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s41')
    #
    #  2 Temporary for debugging the above.
    stmt = """select trim(leading 'x' from
('x' || last_name || 'x' || first_name || 'x' ) )
from empview1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s42')
    stmt = """select trim(trailing 'Q' from
('Q' || last_name || 'Q' || first_name || 'Q' ) )
from empview1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s43')
    #
    stmt = """select first_name,
trim(BOTH 'J' from
('JAZ' || last_name || first_name || 'ZAJ') )
from empview1 
where dept_num >=12 and dept_num <=14
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s44')
    #
    #  Double trim.
    stmt = """select first_name,
trim(LEADING 'y' from trim(LEADING 'x' from
('xyz ' || last_name || ' ' || job || ' ' || gender )
))
from empview2 
where LOWER(gender) = 'female'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s45')
    #
    #  Time without explicit trim-character trims spaces.
    stmt = """select 'A' || trim(BOTH from (' ' || gender || job || ' ' ) ) ||'Z'
from empview2 
where LOWER(last_name) like '%alt%'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s46')
    #
    #  Trim character argument of TRIM function can be only
    #  1 character long. e.g. cannot put:
    #     trim(TRAILING 'test' from ( first_name||LOWER('TEST') ))
    #
    stmt = """select trim(TRAILING 't' from (
trim(TRAILING 'e' from (
trim(TRAILING 's' from (
trim(TRAILING 't' from (
first_name || last_name || LOWER('TEST')
) )
) )
) )
) )
from empview3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s47')
    #
    #  Time without explicit trim-character trims spaces.
    #  Expect '  .'  (3 spaces cut to 2 spaces after first name.
    stmt = """select trim(trailing from
('my name is ' || last_name || '_' || first_name || '   ') || '.'
) as c
from empview3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s48')
    #
    # -------------------------
    #  AS.027
    #  Concatenated string literals and chars and varchars
    # -------------------------
    #
    stmt = """select (last_name || ' **** ' || first_name || ' '
||  ':-) hello folks !' )
from empview1 
where dept_num = 17
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s49')
    #
    stmt = """select (last_name || ' ' || first_name || gender || ' ' || job)
from empview2 
where LOWER(job) = 'manager'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s50')
    #
    stmt = """select ('my name is ' || first_name || 'and I am ' || gender)
from empview2 
where UPPER(LOWER(gender)) = 'MALE'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s51')
    #
    stmt = """select ('*****' || last_name || '#####' || first_name || '.')
from empview3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s52')
    #
    stmt = """select (last_name || ' of ' || first_name || 'changed to ' ||
LOWER('ABRAKADABRA') )
from empview3 
where LOWER(last_name) = 'mitchell'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s53')
    #
    #                      Insert the results of the queries against
    #                      grouped views into private tables
    
    #-------------------------
    # AS.028
    #-------------------------
    #
    #BEGIN_DDL
    stmt = """create table tempA01 
(
t1 varchar(30) ,
t2 char(15)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #END_DDL
    #
    stmt = """insert into tempA01 
select UPPER(last_name), LOWER(first_name) from empview1 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    stmt = """select * from tempA01 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s54')
    stmt = """delete from tempA01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    #
    stmt = """insert into tempA01 
select LOWER(UPPER(last_name)), UPPER(LOWER(first_name))
from empview3 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    stmt = """select * from tempA01 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s55')
    stmt = """delete from tempA01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    #
    stmt = """select 'matched parens'
, lower(first_name) from empview1 where
lower(last_name) = 'young'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s56')
    stmt = """insert into tempA01 values
( 'matched parens'
, ( select lower(first_name) from empview1 where
lower(last_name) = 'young'
)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tempA01 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s57')
    #
    #BEGIN_DDL
    stmt = """drop table tempA01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tempA01 
(
c1 char(15) ,
c2 int
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #END_DDL
    #
    stmt = """insert into tempA01 
select first_name, char_length(last_name || first_name)
from empview1 
where lower(last_name) = 'young'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tempA01 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s58')
    stmt = """delete from tempA01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    stmt = """insert into tempA01 
select first_name,
octet_length( trim(BOTH ' ' FROM first_name) ||
last_name || job ||
substring(gender from 1 for 8)
)
from empview2 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    stmt = """select * from tempA01 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s59')
    stmt = """delete from tempA01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    #
    #BEGIN_DDL
    stmt = """drop table tempA01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tempA01 
(
p1 char(15),
p2 int
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #END_DDL
    #
    stmt = """insert into tempA01 
select first_name, POSITION('' IN last_name)
from empview3 
where last_name = 'WALTERS'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tempA01 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s60')
    stmt = """delete from tempA01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    stmt = """insert into tempA01 
( select 'gupta', position('t' in last_name)  from
 empview3 where lower(last_name)
like '%alt%'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tempA01 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s61')
    stmt = """delete from tempA01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    #BEGIN_DDL
    stmt = """drop table tempA01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tempA01 
(
t1 char(15),
t2 varchar(50)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #END_DDL
    #
    stmt = """insert into tempA01 
select first_name,
trim(BOTH 'A' from
('ABC ' || last_name || first_name || 'ABC') )
from empview1 
where dept_num >=12 and dept_num <=17
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    stmt = """select * from tempA01 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s62')
    stmt = """delete from tempA01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    #
    #BEGIN_DDL
    stmt = """drop table tempA01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tempA01 
(
c1 varchar(50)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #END_DDL
    #
    stmt = """insert into tempA01 
select ('my name is ' || first_name || 'and I am a ' || gender)
from empview2 
where UPPER(LOWER(gender)) = 'MALE'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """select * from tempA01 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s63')
    stmt = """delete from tempA01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #
    # ---------------------------------
    # Drop tables local to this testcase.
    # ---------------------------------
    #
    stmt = """drop view empview1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view empview2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view empview3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view empview4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tempA01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------------
    # Empty all rows from table(s) to avoid conflict with other testcases.
    # ---------------------------------
    #
    stmt = """delete from empA01 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1116:A02
    #  Description:        This test verifies the SQL STRING features.
    #                      Predicates involving ANSI string functions
    #                      on query whose select list includes grouped
    #                      views.
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------------
    # Populate table.
    # ---------------------------------
    
    stmt = """delete from empA02 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into empA02 
values ('mitchell', 'andrea', 'programmer', 'female', 20000, 12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA02 
values ('WALTERS', 'MARVIN', 'systemanalyst', 'male', 20000, 15);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA02 
values ('richards', 'martha', 'SECRETARY', 'FEMALE', 30000, 12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA02 
values ('OSLO', 'DOUG', 'ENGINEER', 'MALE', 40000, 17);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA02 
values ('Young', 'Gail', 'SALESREP', 'female', 40000, 15);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA02 
values ('Weill', 'Kathy',  'Manager', 'Female', 50000, 17);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """select * from empA02 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #
    # Create grouped views for using the string functions
    #
    # Underlying table empA02 differs from empA01; some columns in empA01
    # are char while they are varchar in test A02's empA02.
    #
    # Create a grouped view with group by in the select statement
    
    stmt = """create view empview1 (last_name, first_name, dept_num
, AVG_SAL, MIN_SAL, MAX_SAL )
as
select cast(last_name as varchar(9)) ,
cast(first_name as varchar(9)) ,
dept_num ,
cast(avg(salary) as int) ,
cast(min(salary) as int) ,
cast(max(salary) as int)
from empA02 
group by dept_num, last_name, first_name
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Create a grouped view with having clause in the select statement
    stmt = """create view empview2 (last_name, first_name, job, gender)
as
select last_name, first_name,
job, gender
from empA02 
group by last_name, first_name, job, gender, salary
having salary in (10000, 20000, 30000, 40000, 50000)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create a grouped view with group by and having clauses in
    # the select statement
    stmt = """create view empview3 (last_name, first_name)
as
select last_name, first_name from empA02 
group by last_name, first_name, gender
having LOWER(gender) = 'female'
or   LOWER(gender) = 'male'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Look at values in grouped views.
    #
    stmt = """select * from empview1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    stmt = """select * from empview2 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    stmt = """select * from empview3 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #
    #  Expect 6 for each.
    stmt = """select cast(count(*) as int) from empview1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    stmt = """select cast(count(*) as int) from empview2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    stmt = """select cast(count(*) as int) from empview3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    #
    # -------------------------
    #  AS.031 to AS.038
    #  Predicates involving ANSI string functions on query whose
    #  select list includes group views
    # -------------------------
    #
    #  Expect (('richards' 'martha'))
    stmt = """select last_name, first_name from empview1 
where LOWER(last_name) like '%cha%'
or UPPER(first_name) like '%COT_'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    #
    #  Left join on grouped view.
    #  Expect 11 rows, including 2 null-extended rows (WALTERS and mitchell).
    stmt = """select va.last_name, va.avg_sal, vb.last_name, vb.min_sal
from empview1 va
left join empview1 vb
on va.avg_sal > vb.min_sal
and ( lower(va.last_name) >= lower(vb.last_name) )
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    #
    #  Inner join on grouped view.
    #  Expect 9 rows (excludes null-extended rows).
    stmt = """select va.last_name as vaLast
, vb.last_name as vbLast
, va.avg_sal, vb.min_sal
from empview1 va
inner join empview1 vb
on va.avg_sal > vb.min_sal
and ( lower(va.last_name) >= lower(vb.last_name) )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    #
    #  Expect 5 rows, all but for OSLO.
    stmt = """select last_name, first_name, job, gender from empview2 
where character_length(last_name) in (5,6,7,8)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    #
    #  Expect (('OSLO') ('Young'))
    stmt = """select last_name from empview2 
where octet_length(first_name||last_name) not between 10 and 20
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    #
    #  Expect (('WALTERS' 'MARVIN') ('richards' 'martha'))
    stmt = """select last_name, first_name from empview3 
where position('MAR' IN UPPER(first_name || last_name))
between 1 and 5
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    #
    # Expect 0 rows.
    stmt = """select last_name from empview3 
where substring(first_name from 1 for 5) is null
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  Expect 6 rows (DOUG ... martha)
    stmt = """select first_name from empview3 
where trim(BOTH ' ' from (last_name || first_name)) is not null
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    #
    #  Expect (('OSLO') ('WALTERS'))
    stmt = """select last_name from empview2 t1
where substring(last_name from 1)
between
'OSLO'
and
'WALTERS'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    #
    #  Expect (('OSLO') ('WALTERS'))
    stmt = """select last_name from empview2 t1
where substring(last_name from 1)
between
(select t2.last_name from empview2 t2
where LOWER(UPPER(t2.job)) = 'engineer'
)
and
(select t3.last_name from empview2 t3
where LOWER(t3.gender) = 'male'
and LOWER(substring(t3.first_name from 1 for 6)) = 'marvin'
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    #
    #-------------------------
    # AS.038
    #-------------------------
    #
    stmt = """create table tempA02 (c1 varchar(25) ) no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Expect (('oslo'))
    stmt = """select LOWER(last_name) from empview2 
where trim(BOTH from LOWER(last_name)) in
(select lower(last_name) from empview1 
where empview1.first_name = empview2.first_name
and (dept_num = 17)
and lower(empview1.first_name) = 'doug'
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    stmt = """insert into tempA02 
select LOWER(last_name) from empview2 
where trim(BOTH from LOWER(last_name)) in
(select lower(last_name) from empview1 
where empview1.first_name = empview2.first_name
and (dept_num = 17)
and lower(empview1.first_name) = 'doug'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect (('oslo'))
    stmt = """select * from tempA02 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    stmt = """delete from tempA02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    #  Expect (('Weill Kathy') ('mitchell andrea'))
    stmt = """select trim (BOTH ' ' from (last_name || ' ' || first_name))
from empview2 t2
where lower(last_name) like '%ll%'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    stmt = """insert into tempA02 
select LOWER(last_name) from empview2 tempA02 
where last_name || trim(trailing ' ' from first_name)
in
(select trim (BOTH ' ' from (last_name || first_name))
from empview2 t2
where lower(last_name) like '%ll%'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    #  Expect (('mitchell') ('weill'))
    stmt = """select * from tempA02 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    stmt = """delete from tempA02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #
    # ---------------------------------
    # Drop tables local to this testcase.
    # ---------------------------------
    #
    stmt = """drop table tempA02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view empview1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view empview2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view empview3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------------
    # Empty all rows from table(s) to avoid conflict with other testcases.
    # ---------------------------------
    #
    stmt = """delete from empA02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1116:A03
    #  Description:        This test verifies the SQL STRING features.
    #                      ANSI string functions with table value
    #                      constructors.
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------------
    # Empty table in preparation for Inserts.
    # ---------------------------------
    
    stmt = """delete from tab1;"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------------
    # Test plan test id AS.101 ANSI string functions with Table value
    # constructors insert into 5 columns using 3 sets of values using
    # table value constructor.
    # ---------------------------------
    #
    # First insert the rows one-by-one within a transaction;
    # check them, then rollback.
    #
    stmt = """set transaction autocommit off;"""
    output = _dci.cmdexec(stmt)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into tab1 (v1, v2, c1, c2, i1) values
(  lower(upper('madonna')),
null,
('whitney' || 'houston'),
null
, character_length('abcdefg')
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect (('madonna'  NULL  'whitneyhouston'  NULL  7))
    stmt = """select * from tab1 order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    #
    stmt = """insert into tab1 (v1, v2, c1, c2, i1) values
( substring('geena' from 1 for 5) || 'davis' ,
substring( ('steve' || ' ' || 'wonder') from 1 for 5 ),
lower(upper(lower(upper('TeStEr')))) ,
trim( BOTH ' ' from (substring(LOWER('SHANTI') from 1 for 4) )),
octet_length('abcdefgh')
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect the above row plus (('geenadavis' 'steve' 'tester' 'shan' 8  ))
    stmt = """select * from tab1 order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    #
    stmt = """insert into tab1 (v1, v2, c1, c2, i1) values
( substring('margaret' from 2 for 5) || 'et',
trim(both 't' from 'target'),
lower('TIMOTHY'),
upper('johnson'),
position('amy' in 'ramaswamy')
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Expect the above row plus (('argaret' 'arge' 'timothy' 'JOHNSON' 7))
    stmt = """select * from tab1 order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """insert into tab1 (v1, v2, c1, c2, i1) values
(  lower(upper('madonna')),
null,
('whitney' || 'houston'),
null
, character_length('abcdefg')
) ,    

( substring('geena' from 1 for 5) || 'davis' ,
substring( ('steve' || ' ' || 'wonder') from 1 for 5),
lower(upper(lower(upper('TeStEr')))),
trim( BOTH ' ' from (substring(LOWER('SHANTI') from 1 for 4))),
octet_length('abcdefgh')
),    

( (substring('margaret' from 2 for 5) || 'et'),
(trim(both 't' from 'target') ),
(lower('TIMOTHY')),
(upper('johnson')),
(position('amy' in 'ramaswamy'))
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    #
    #  Expect 3 rows as above.
    stmt = """select * from tab1 order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    # ---------------------------------
    # Empty all rows from table(s) to avoid conflict with other testcases.
    # Expect there are 0 rows because of rollback.
    # ---------------------------------
    #
    stmt = """delete from tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1116:A04
    #  Description:        This test verifies the SQL STRING features.
    #                      ANSI string functions with Row Value Constructor.
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Check contents of emp; Populate table emp in PREUNIT.
    #  ---------------------------------
    
    stmt = """select FIRST_NAME, LAST_NAME, JOB, GENDER
from emp order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    stmt = """select FIRST_NAME, LAST_NAME, SALARY, DEPT_NUM, STR
from emp order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    #
    # ---------------------------------
    # Populate table emptabl.
    # ---------------------------------
    #
    
    stmt = """delete from emptabl ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into emptabl values
('andrea', 'mitchell', 'programmer', 'female', 'pathway', 123);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into emptabl values
('sulu', 'kapoor', 'manager', 'female', 'arkqa' , 2345);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into emptabl values
('martha', 'vincent', 'SECRETARY', 'FEMALE', 'networkmanagement', 345);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into emptabl values
('MARIA', 'JOYCE',  'HAIRDRESSER', 'FEMALE', 'Boutique', 23232);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into emptabl values
('ANANDHI', 'RAMASWAMY',  'PROGRAMMER', 'female', 'arkqa' , 4254);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """select FIRST_NAME, LAST_NAME, JOB, GENDER
from emptabl 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    stmt = """select FIRST_NAME, LAST_NAME, DEPT_NAME, EMP_NUM
from emptabl 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    #
    # -------------------------
    #  AS.091
    #  ANSI string functions with Row value constructor in WHERE predicate
    #  And string functions with RVC in ON clause
    # -------------------------
    #
    #  Scaffolding for subsequent query.
    #  Expect Kathy Baxter's data.
    stmt = """select last_name, first_name, salary, dept_num from emp 
where  lower(last_name|| ' ' || first_name )
=   ('baxter kathy')
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    #
    #  Expect Kathy Baxter's data.
    stmt = """select last_name, first_name, salary, dept_num from emp 
where ( substring( trim(leading 's' from job) from 5 for 4)
)
=   ('tary')
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    #
    #  Expect Kathy Baxter's data.
    stmt = """select last_name, first_name, salary, dept_num from emp 
where ( lower(last_name|| ' ' || first_name),
substring( trim(leading 's' from job) from 5 for 4)
)
=   ('baxter kathy', 'tary')
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    #
    #  Expect Kathy Baxter's data.
    stmt = """select last_name, first_name, salary, dept_num from emp 
where (
character_length(gender),
position('ax' in last_name)
)
=   (6, 2)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    #
    #  Expect Kathy Baxter's data.
    stmt = """select last_name, first_name, salary, dept_num from emp 
where ( lower(last_name|| ' ' || first_name),
substring( trim(leading 's' from job) from 5 for 4),
character_length(gender),
position('ax' in last_name)
)
=   ('baxter kathy', 'tary', 6, 2)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    #
    #  Expect data for Kapoor and Martin.
    stmt = """select lower(last_name) as lower_last,
substring(trim (both ' ' from job) from 1 for 6)
as substring_both,
salary, dept_num
from emp where
(    substring(last_name from 1 for 5) )
>= ('farra')
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    #
    #  Expect data for Kapoor and Martin.
    stmt = """select lower(last_name) as lower_last,
substring(trim (both ' ' from job) from 1 for 6)
as substring_both,
salary, dept_num
from emp where
(    substring(last_name from 1 for 5),
position('t' in job),
character_length(gender),
octet_length(gender),
trim(both ' ' from lower( ' ' || first_name || ' ')),
upper(lower(str) )
)
--  NOTE: kapoor is truncated to match the substring!
>= ('kapoo', 0, 6, 6, 'sulu', 'B')
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    #
    #  Expect 3 rows for (joyce, kapoor, ramaswamy).
    stmt = """select lower(t1.last_name) as left_last
, lower(t1.first_name) as left_first
, lower(t2.last_name)  as right_last
, lower(t2.first_name) as right_first
from emp as t1 JOIN emptabl as t2
ON
( substring(t1.last_name from 1 for 5),
trim(leading 's'  from lower(t1.first_name)),
position ('pro' in t1.job),
character_length(t1.gender)
)
=
( substring(t2.last_name from 1 for 5),
trim(leading 's'  from lower(t2.first_name)),
position ('pro' in t2.job),
character_length(t2.gender)
)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    #
    #  Expect 5 rows; includes mitchell and vincent with null in dept_num.
    stmt = """select lower(emptabl.last_name) as right_last
, lower(emptabl.dept_name) as right_dept
, emp.dept_num as left_Dnum
, emptabl.emp_num as right_Enum
from emp right outer join emptabl 
ON
( substring(emp.first_name from 1),
trim (both ' ' from (' ' || emp.last_name || ' ') ),
octet_length(emp.gender)
)
=
( substring(emptabl.first_name from 1),
trim (both ' ' from (' ' || emptabl.last_name || ' ') ),
octet_length(emptabl.gender)
)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    
    #  Expect 9 rows; Anandhi's data is non-null on the right.
    stmt = """select cast(t1.first_name as varchar(9)) as left_first
, cast(t1.last_name  as varchar(9)) as left_last
, cast(t2.first_name as varchar(9)) as right_first
, cast(t2.last_name  as varchar(9)) as right_last
from emp t1 left outer join emp t2
ON
( character_length(t1.first_name)
, (t2.first_name || ' ' || t2.last_name)
, position('P' in upper(t1.job))
)
=
(7, 'ANANDHI RAMASWAMY', 1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    #
    # ---------------------------------
    # Empty all rows inserted into table(s) in this testcase,
    # to avoid conflict with other testcases.
    # ---------------------------------
    #
    # DO NOT DELETE FROM EMP!
    stmt = """delete from emptabl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1116:A05
    #  Description:        This test verifies the SQL STRING features.
    #                      ANSI String functions with Right Outer Join.
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Check contents of emp; Populate table emp in PREUNIT.
    #  ---------------------------------
    
    stmt = """select FIRST_NAME, LAST_NAME, JOB, GENDER
from emp order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    stmt = """select FIRST_NAME, LAST_NAME, SALARY, DEPT_NUM, STR
from emp order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    # ---------------------------------
    # Populate tables.
    # ---------------------------------
    
    stmt = """delete from emptabl ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into emptabl values
('andrea', 'mitchell', 'programmer', 'female', 'pathway', 123);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into emptabl values
('sulu', 'kapoor', 'manager', 'female', 'arkqa' , 2345);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into emptabl values
('martha', 'vincent', 'SECRETARY', 'FEMALE', 'networkmanagement', 345);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into emptabl values
('MARIA', 'JOYCE',  'HAIRDRESSER', 'FEMALE', 'Boutique', 23232);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into emptabl values
('ANANDHI', 'RAMASWAMY',  'PROGRAMMER', 'female', 'arkqa' , 4254);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """select FIRST_NAME, LAST_NAME, JOB, GENDER
from emptabl order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    stmt = """select FIRST_NAME, LAST_NAME, DEPT_NAME, EMP_NUM
from emptabl order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    #
    # -------------------------
    #  AS.051: Right outer join with string functions in select list.
    #  AS.052: Right outer join with string functions in predicates.
    #  AS.053: Right outer join with string functions in queries.
    #  AS.054: Right outer join with string functions in correlated subqueries.
    #  AS.055: Right outer join with string functions in uncorrelated subqueries.
    # -------------------------
    #
    #  Expect 3 rows matching for JOYCE, RAMASWAMY, kapoor.
    stmt = """select emp.last_name||' emp.LAST'
, emptabl.last_name|| ' EMPTAB1.LAST'
from emp Inner Join emptabl 
on lower(emp.last_name) = lower(emptabl.last_name)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    #  Expect 5 rows matching for JOYCE, RAMASWAMY, kapoor,
    #  with other 2 rows of emptabl null-extended.
    stmt = """select emp.first_name, emp.last_name
, emptabl.first_name, emptabl.last_name
from emp Right outer join emptabl 
on lower(emp.last_name) = lower(emptabl.last_name)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    #
    #  ---------------------------------
    #  Right outer join.
    #  ---------------------------------
    #
    #  Expect 5 rows matching for joyce, kapoor, ramaswamy.
    #  with other 2 rows of emptabl (mitchell, vincent) null-extended.
    stmt = """select cast(lower(emptabl.last_name||emptabl.first_name) as char(18))
as R_names,
cast(lower(upper(emp.last_name)) as char(9))
as L_last,
cast( char_length(emp.last_name) as smallint)
as L_cLen,
cast( octet_length(emp.last_name) as smallint)
as L_oct,
cast( position('A' in upper(lower(emp.last_name)) ) as smallint)
as L_pos,
trim(both ' ' from emp.last_name)
as L_trim
from emp right outer join  emptabl 
on substring(emp.last_name from 1 for 5) =
substring(emptabl.last_name from 1 for 5)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    #
    #  As above with more complex ON clause.
    stmt = """select cast(lower(emptabl.last_name||emptabl.first_name) as char(18))
as R_names,
cast(lower(upper(emp.last_name)) as char(9))
as L_lower_last,
cast( char_length(emp.last_name) as smallint)
as L_cLen_last,
cast( octet_length(emp.last_name) as smallint)
as L_oct,
cast( position('A' in upper(lower(emp.last_name)) ) as smallint)
as L_pos,
trim(both ' ' from emp.last_name)
as L_trim
from emp right outer join  emptabl 
on (substring(emp.last_name from 1 for 5) =
substring(emptabl.last_name from 1 for 5)
)
and (character_length(substring(emp.gender from 1 for 3)) =
char_length(substring(emptabl.gender from 1 for 3))
)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    #
    #  ---------------------------------
    #  Right outer join.
    #  ---------------------------------
    #  Expect 45 rows from this query that shows items to be
    #  used in next query including its ON clause below.
    stmt = """select lower(upper(t1.last_name)) as L_last
, substring(t1.gender from 3 for 6) as t1Gender36
, t1.job
, substring(t2.gender from 3 for 6) as t2Gender36
, t2.job
from emp as t1 right outer join emptabl as t2
on (1 = 1)
order by t2.gender , t2.job
, t1.gender , t1.job
, t1.last_name
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    #  Expect 13 rows (omit the values that mismatch on case)
    stmt = """select lower(upper(t1.last_name)) as L_last,
character_length(t1.last_name) as L_charLen,
trim(leading 'H' from t1.job) as L_job,
substring(t1.gender from 3 for 6) as L_gender,
substring(t2.gender from 3 for 6) as "R_gender"
from emp as t1 right outer join emptabl as t2
on substring(t1.gender from 3 for 6)
= substring(t2.gender from 3 for 6)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    #
    #  ---------------------------------
    #  Expect 5 rows: 3 rows matching for JOYCE, RAMASWAMY, kapoor;
    #  and 2 rows entirely null.
    stmt = """select trim(both 'p' from lower(substring(emp.job from 1))) as L_job,
lower(emp.first_name||emp.last_name) as L_name,
octet_length(lower(emp.first_name||emp.last_name))
as L_oct_name
from emp right join emptabl 
on emp.last_name = emptabl.last_name
and emp.first_name = emptabl.first_name
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    #
    #  Expect 5 rows, each ('JOYCE').
    stmt = """select ca
from (select t1.last_name
from emp t1 right outer join
 emptabl t2 -- Removed USING (not supported 1997).
on 1=1
) dt1(ca)
where lower(dt1.ca) = 'joyce'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')

    stmt = """select t1.last_name , t2.last_name
from emp t1 right outer join  emptabl t2
on t1.job = t2.job
where t1.last_name
in ('JOYCE', 'kapoor')
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    #
    #  Expect data for 'JOYCE' and 'kapoor'
    stmt = """select cast(t1.first_name || ' ' || t1.last_name as char(12)) as L_name
, cast(t2.first_name || ' ' || t2.last_name as char(12)) as R_name
, t1.job as L_job
, t2.job as R_job
from emp t1 right outer join emptabl t2
on lower(t1.job) = lower(upper(lower(t2.job)))
and upper(t1.first_name) = upper(t2.first_name)
where lower(t1.last_name)
in ('joyce', 'kapoor', 'farrar', 'cheng', 'wu')
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    #
    #  Expect 45 rows.
    stmt = """select cast(emp.last_name as char(9)) as emp_L
, emp.job
, cast(emptabl.last_name as char(9)) as emptabl_L
, cast(substring(
trim(leading 'r' from lower(emp.last_name || emp.first_name))
from 3 for 5) as char(7)) as trim_N
from emp right outer join emptabl 
on (1=1)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    stmt = """select emp.last_name, emp.first_name, emp.job
, emp.gender, emp.salary, emp.dept_num, emptabl.dept_name
from emp right outer join emptabl 
on octet_length(emp.last_name) = octet_length(emptabl.last_name)
and char_length(emp.first_name) = character_length(emptabl.first_name)
and trim(both 's' from emp.job) = trim (both 's' from emptabl.job)
and substring (emp.gender from 2 for 2) =
substring(emptabl.gender from 2 for 2)
where substring(
trim(leading 'r' from lower(emp.last_name || emp.first_name))
from 3 for 5) like 'h%h%'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  There is only one match ('sulu') in where clause's subquery.
    #  Therefore expect 5 rows.
    stmt = """select emptabl.last_name
, emp.last_name, emptabl.dept_name, emp.job
from emp right outer join emptabl 
on lower(emp.job) = lower(emptabl.job)
where substring(lower(emp.first_name) from 1 for 4)
<=
(select lower(first_name) from emptabl where
dept_name = 'arkqa'
and emp_num < 3000)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    #
    # Expect 0 rows.
    stmt = """select emptabl.last_name
, emp.last_name, emptabl.dept_name, emp.job
from emp right outer join emptabl 
on octet_length(emp.gender) = octet_length(emptabl.gender)
and emp.first_name || ' ' || emp.last_name
= emptabl.first_name || ' ' || emptabl.last_name
where lower(emp.gender)
>= (select lower(gender) from emptabl 
where dept_name = 'tuxedo')
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  Expect 5 rows with 2 null-extended.
    stmt = """select emp.first_name || ' ' || emp.last_name
, emptabl.first_name || ' ' || emptabl.last_name
from emp right outer join emptabl 
on emp.first_name || emp.last_name =
 emptabl.first_name || emptabl.last_name
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    #
    #  Expect 1 row for Maria Joyce.
    stmt = """select emp.first_name || ' ' || emp.last_name
, emptabl.first_name || ' ' || emptabl.last_name
from emp right outer join emptabl 
on emp.first_name || emp.last_name =
 emptabl.first_name || emptabl.last_name
where character_length(emp.last_name) in
(select character_length(substring (emptabl.last_name from 1 ))
from emptabl 
where emp.last_name = emptabl.last_name
and (substring(lower(emptabl.dept_name) from 4 for 3)
= 'tiq')
)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    #
    #  Scaffolding for next query; expect 5 rows.
    stmt = """select lower(upper(lower(first_name))) from emp 
where lower(gender) = 'female'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s18')
    #  Expect 25 (like a self-join).
    stmt = """select ca from
(select emp.first_name, emptabl.first_name
from emp right outer join emptabl 
on position ('' in emp.first_name) =
position ('' in emptabl.first_name)
) dt(ca,cb)
where substring (
trim(both ' ' from (' '||lower(ca)||' ') )
from 1 )
= some
(select lower(upper(lower(first_name))) from emp 
where lower(gender) = 'female'
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s19')
    #
    #  Expect 45 rows.
    stmt = """select emp.first_name, emptabl.first_name
, substring(emp.first_name from 3 for 1)
, substring(emptabl.first_name from 3 for 1)
from emp right join emptabl 
on 1=1
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s20')
    #
    #  Expect 5 rows plus 2 extra matching on 3rd letter in "anandhi"
    stmt = """select emp.first_name as emp_first
, emptabl.first_name as emptabl_first
from emp right join emptabl 
on substring(lower(emp.first_name) from 3 for 1) =
substring(lower(emptabl.first_name) from 3 for 1)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s21')

    #  Expect 3 rows.
    stmt = """select emp.first_name, emptabl.first_name
from emp right join emptabl 
on substring(emp.first_name from 1) =
substring(emptabl.first_name from 1)
where  emp.first_name is not null
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s22')
    #  Expect 5 rows.
    stmt = """select emp.first_name, emptabl.first_name
from emp right join emptabl 
on substring(lower(emp.first_name) from 1) =
substring(lower(emptabl.first_name) from 1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s23')
    #
    # ---------------------------------
    # Empty all rows inserted into table(s) in this testcase,
    # to avoid conflict with other testcases.
    # ---------------------------------
    #
    # DO NOT DELETE FROM EMP!
    stmt = """delete from emptabl ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1116:A06
    #  Description:        This test verifies the SQL STRING features.
    #                      ANSI String functions with Natural Join.
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Check contents of emp; Populate table emp in PREUNIT.
    #  ---------------------------------
    
    stmt = """select FIRST_NAME, LAST_NAME, JOB, GENDER
from emp order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    stmt = """select FIRST_NAME, LAST_NAME, SALARY, DEPT_NUM, STR
from emp order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    # ---------------------------------
    # Populate table.
    # ---------------------------------
    
    stmt = """delete from emptabl ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into emptabl values
('andrea', 'mitchell', 'programmer', 'female', 'pathway', 123);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into emptabl values
('sulu', 'kapoor', 'manager', 'female', 'arkqa' , 2345);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into emptabl values
('martha', 'vincent', 'SECRETARY', 'FEMALE', 'networkmanagement', 345);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into emptabl values
('MARIA', 'JOYCE',  'HAIRDRESSER', 'FEMALE', 'Boutique', 23232);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into emptabl values
('ANANDHI', 'RAMASWAMY',  'PROGRAMMER', 'female', 'arkqa' , 4254);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """select FIRST_NAME, LAST_NAME, JOB, GENDER
from emptabl order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    stmt = """select FIRST_NAME, LAST_NAME, DEPT_NAME, EMP_NUM
from emptabl order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    #
    stmt = """create view vA6A as select
first_name , last_name , job , gender
from emp 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select * from vA6A order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    #
    stmt = """create view vA6B as select
first_name , last_name , job , gender
from emptabl 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select * from vA6B order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    #
    # -------------------------
    #  AS.061 - AS.065
    # -------------------------
    #
    #  Expect matching data for Sulu Kapoor and Maria Joyce.
    stmt = """select * from
 vA6A NATURAL JOIN vA6B 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    #
    # Set warnings off to avoid warnings introduced late in Beta, e.g.
    #   -- >>select cast(lower(last_name || first_name) as varchar(6)) as b
    #   -- +>     , cast(char_length(last_name) as smallint) as c
    #   -- +>;
    #   -- *** WARNING[8402] A string overflow occurred during the evaluation of a character expression.
    #   -- B       C       D       E       F       G
    #   -- ------  ------  ------  ------  ------  ------
    #   -- joycem       5       5       0  JOYCE   JOYCE
    #   -- *** WARNING[8402] A string overflow occurred during the evaluation of a character expression.
    #   -- kapoor       6       6       2  kapoor  kapoor
    #   -- --- 2 row(s) selected.
    stmt = """SET WARNINGS OFF;"""
    output = _dci.cmdexec(stmt)
    #  Expect matching data for Sulu Kapoor and Maria Joyce.
    stmt = """select cast(lower(last_name || first_name) as varchar(6)) as b
, cast(char_length(last_name) as smallint) as c
, cast(octet_length(last_name) as smallint) as d
, cast(position('A' in upper(lower(last_name))) as smallint)
as e
, cast(trim(both ' ' from last_name) as varchar(6)) as f
, cast(substring(last_name from 1) as varchar(6)) as g
from vA6A 
NATURAL JOIN vA6B 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    #
    #  Expect matching data for Sulu Kapoor and Maria Joyce.
    stmt = """select lower(upper(last_name)) as a,
position('m' in lower(first_name)) as b,
trim(leading 'm' from job) as c,
substring(gender from 3 for 6) as d,
character_length(last_name || first_name) as e
from vA6A 
NATURAL JOIN vA6B 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    #
    #  Expect matching data for Sulu Kapoor and Maria Joyce.
    stmt = """select * from vA6A NATURAL JOIN vA6B 
where lower(last_name) in ('joyce', 'kapoor', 'farr', 'cheng','wu')
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    #
    #  Expect matching data for Maria Joyce.
    stmt = """select last_name , first_name, job, gender
from vA6A 
NATURAL JOIN vA6B 
where substring(
trim(leading 'j'
from lower(last_name || first_name))
from 2 for 3)
like 'y%e'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    #
    #  Expect 3 rows
    stmt = """select lower(first_name) as first_name
, lower(last_name) as last_name
, emp_num
from emptabl 
where emp_num < 3000
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s11')
    #
    #  Scaffolding.
    stmt = """select lower(first_name) from emptabl where
first_name = 'martha' and
emp_num < 3000
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s12')
    #  Expect (('JOYCE' 'kathy' 'HAIRDRESSER'))
    stmt = """select last_name, lower(first_name), job
from vA6A 
NATURAL JOIN vA6B 
where substring(lower(first_name) from 1 for 4)
<=
(select lower(first_name) from emptabl where
first_name = 'martha' and
emp_num < 3000
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s13')
    #
    #  Expect matching columns for kapoor and JOYCE.
    stmt = """select *
from vA6A 
NATURAL JOIN vA6B 
where lower(gender)
>=
(select min(lower(gender)) from emptabl 
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s14')
    #
    stmt = """select emptabl.dept_name from emptabl 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s15')
    #
    #  Scaffolding for the next query.
    stmt = """select lower(first_name) from emp 
where lower(gender) = 'female'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s16')
    #  Expect matching data for MARIA and Sulu.
    stmt = """select ca from
(select first_name from vA6A NATURAL JOIN vA6B) dt(ca)
where substring (trim(both ' ' from (' ' || lower(ca) || ' '))
from 1)
= some
(select lower(first_name) from emp 
where lower(gender) = 'female'
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s17')
    #
    #  Expect data for kapoor.
    stmt = """select last_name, job
, character_length(first_name) as length_first
, octet_length(last_name) as octet_first
, position('p' in lower(job) ) as position_job
, char_length(gender) as length_gender
from vA6A 
NATURAL JOIN vA6B 
where character_length(gender) between
char_length(first_name) and char_length(last_name)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s18')
    #
    # ---------------------------------
    # Empty all rows inserted into table(s) in this testcase,
    # to avoid conflict with other testcases.
    # ---------------------------------
    #
    # DO NOT DELETE FROM EMP!
    stmt = """delete from emptabl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    #
    # ---------------------------------
    # Drop views created in this test case.
    # ---------------------------------
    stmt = """drop view vA6A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vA6B;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1116:A07
    #  Description:        This test verifies the SQL STRING features.
    #                      Predicates involving ANSI string functions
    #                      on update; when update primary key is supported
    #                      we can change some columns to primary keys.
    #
    # =================== End Test Case Header  ===================
    #
    stmt = """set transaction autocommit off;"""
    output = _dci.cmdexec(stmt)
    #
    # ---------------------------------
    # Populate table.
    # ---------------------------------
    #
    
    stmt = """delete from depart;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into depart values
('Srinivas Morton' , 16, 'ALGORITHMS', 10, 'CS600',  'CS300', 'fall', 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into depart values
('George Memory' , 15,  'Computer ARCHITECTURE',21, 'CS555',  'CS200', 'spring', 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into depart values
('David Crane', 15, 'Computer Graphics', 16, 'CS500', 'CS150', 'summer',3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into depart values
('Srinivas Morton' , 16, 'Software Engineering', 20, 'CS700', 'CS300', 'fall',3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into depart values
('Simon Chu', 11, 'Computer Networks', 17, 'CS777', ' ' , 'fall', 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into depart values
('Simon Chu', 11,  'Data Base', 9, 'CS666', 'CS100', 'summer', 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Check the inserted rows.
    stmt = """select PROF, CNUM, CNAME, NAMELEN, CLEN
from depart 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    stmt = """select PROF, CNUM, PREREQ, SEMESTER, CREDITS
from depart 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    #
    #  Expect 3 rows, (('srinivas morton' 'ALGORITHMS CS600' 5)
    #  ('srinivas morton' 'SOFTWARE ENGINEERING CS700' 5)
    #  ('simon chu' 'COMPUTER NETWORKS CS777' 5))
    stmt = """select lower(prof), upper(cname || ' ' || cnum), char_length(cnum)
from depart 
where upper(lower(semester)) = 'FALL'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    #
    stmt = """commit work ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #-------------------------
    # AS.081
    # ANSI string functions providing values for updating a group of
    # primary keys. Update primary key is not supported in 1998, so
    # leave primary key out of definition in preunit.
    #-------------------------
    #
    stmt = """begin work ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Check which row might change.
    #
    #  Expect 6 rows with basic data.
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
--       ,      clen                    as clen
, cast(lower(cnum) as char(7)) as cnum
, cast(credits as smallint)    as credits
--     ,      credits                 as credits
from depart 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    #
    #  Expect 1 row (('simon chu' ... cs666 3))
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(7)) as cnum
, cast(credits as smallint)    as credits
from depart 
where trim(leading 's' from
(substring(lower(prof) from 1 for 5))
) = 'imon'
and lower(semester) = 'summer'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    #
    stmt = """update depart 
set prof    = (upper('angela' || ' ' || lower('davis') ) ),
namelen = (octet_length('angela' || ' ' || 'davis')),
cname   = (substring('Programming Languages' from 13 for 9)),
clen    = (position('s' in 'Languages')),
cnum    = (trim(both 'S' from ('SCS' || '111S') )),
credits = (char_length(substring('phoenix' from 4 for 3)))
where trim(leading 's' from
(substring(lower(prof) from 1 for 5))
) = 'imon'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    #
    #  Check result of Update.
    #  Expect 6 rows with 'angela davis' replacing 'simon chu'.
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(5)) as cnum
, cast(credits as smallint)    as credits
from depart 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    #
    #  Check subcomponents of update:
    #  Expect david crane's data.
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(5)) as cnum
, cast(credits as smallint)    as credits
from depart 
where lower(prof) = 'david crane' and credits = 3
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    #
    stmt = """rollback work ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(5)
    stmt = """begin work ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Check after rollback
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(7)) as cnum
, cast(credits as smallint)    as credits
from depart 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    #
    # Populating table empA07
    #
    stmt = """delete from empA07 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """insert into empA07 values
('sulu', 'kapoor', 'manager', 'female', 90000, 13, 'B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA07 values
('BHAVESH', 'MEHTA', 'ENGINEER', 'MALE', 50000, 14 , 'C');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA07 values
('YUGAL', 'AGGARWAL', 'SYSADMIN', 'MALE', 80000, 14, 'D');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA07 values
('ANANDHI', 'RAMASWAMY', 'PROGRAMMER', 'FEMALE', 50000, 13, 'E');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """commit work ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Expect (('sulu'))
    stmt = """select first_name from empA07 
where lower(job) = 'manager'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    #  Expect (('male'))
    stmt = """select lower(gender) from empA07 
where lower(last_name) = 'mehta'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    #  Expect (('sysadmin'))
    stmt = """select lower(job) from empA07 
where lower(last_name) = 'aggarwal'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    #  Expect (('programmer'))
    stmt = """select lower(job) from empA07 
where first_name = 'ANANDHI'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s11')
    #  Expect (('kapoor' 'female'))
    stmt = """select last_name, gender from empA07 
where upper(first_name)='SULU'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    #  Expect (('aggarwal'))
    stmt = """select last_name from empA07 
where lower(first_name) = 'yugal'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s13')
    #
    # Attempt update in small, rolled-back transactions.
    stmt = """commit work ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """update depart 
set prof = ( select first_name from empA07 
where lower(job) = 'manager')
|| ' ' || lower('KAPOOR')
where lower(prof) = 'david crane'
and credits = 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #  Expect 6 lines, with 'sulu kapoor' for CNUM of 'cs500'.
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(5)) as cnum
, cast(credits as smallint)    as credits
from depart 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s14')
    #
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Check use of scalar subquery to return character expression
    #  for argument of upper function.
    #  Expect (('SULU')).
    stmt = """select DISTINCT upper (
(select first_name from empA07 
where lower(job) = 'manager')
)
from depart 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s15')
    #  Expect (('SULU')).
    stmt = """select DISTINCT upper (( select max(first_name) from empA07 ))
from depart 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s16')
    #
    stmt = """update depart 
set prof = ( upper
( ( select first_name from empA07 
where lower(job) = 'manager') )
|| ' ' || lower('KAPOOR')
)
where
lower(prof) = 'david crane'
and credits = 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    stmt = """select cast(lower(prof) as char(15)) as prof
,      namelen                 as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(5)) as cnum
, cast(credits as smallint)    as credits
from depart 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s17')
    #
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Now do 4 updates, look at results, then roll back.
    stmt = """select prof
from depart 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s18')
    #
    stmt = """update depart set
namelen = ( select octet_length(gender)
from empA07 
where lower(last_name) = 'mehta'
)
where
lower(prof) = 'david crane'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    stmt = """update depart set
cname   = ( select substring(lower(job) from 1 for 7)
from empA07 
where first_name = 'ANANDHI'
)
where
lower(prof) = 'david crane'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    stmt = """update depart set
clen    = ( position ( 's' in lower
(( select last_name from empA07 
where upper(first_name)='SULU' ))
) )
where
lower(prof) = 'david crane'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    stmt = """update depart set
cnum    = trim ( trailing 'x' from 'CSxxx' ) ||
(( select substring( last_name from 1 for 1 )
from empA07 
where lower( first_name ) = 'yugal' ))
where
lower(prof) = 'david crane'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(5)) as cnum
, cast(credits as smallint)    as credits
from depart 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s19')
    #
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Finally the last update/rollback before the big update.
    stmt = """update depart set
credits = ( select (char_length (
substring (gender from 1)))
from empA07 
where first_name = 'sulu'
)
where
lower(prof) = 'david crane'
and credits = 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # If the above is incorrect, then ....
    stmt = """update depart set
credits =
(select char_length (substring (gender from 1) )
from empA07 
where first_name = 'sulu'
)
where
lower(prof) = 'david crane'
and credits = 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    #
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(5)) as cnum
, cast(credits as smallint)    as credits
from depart 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s20')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """select cast(clen as smallint)       as clen
from depart 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s21')
    #
    stmt = """select cast(credits as smallint)    as credits
from depart 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s22')
    #
    # ---------------------------------
    # Empty all rows inserted into table(s) in this testcase,
    # to avoid conflict with other testcases.
    # ---------------------------------
    #
    stmt = """delete from empA07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    stmt = """delete from depart;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1116:A08
    #  Description:        This test verifies the SQL STRING features.
    #                      Basic Tests for Comparison predicates, for predicates
    #                      containing string literals, parameters.
    #
    # =================== End Test Case Header  ===================
    #
    
    #  ---------------------------------
    #  Check contents of emp; Populate table emp in PREUNIT.
    #  ---------------------------------
    stmt = """select FIRST_NAME, LAST_NAME, JOB, GENDER
from emp 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    stmt = """select FIRST_NAME, LAST_NAME, SALARY, DEPT_NUM, STR
from emp 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    #
    # -------------------------
    #  AS.111
    #  LOWER basic and LOWER of empty string
    # -------------------------
    
    #  Expect (('hausmann'  NULL))
    stmt = """select LOWER(last_name), LOWER(first_name) from emp 
where LOWER(gender) = 'male'
and LOWER(job) = 'programmer'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    #
    #  Expect data for hausmann, kapoor, martin, ramaswamy.
    stmt = """select LOWER(last_name), LOWER(job), LOWER('') from emp 
where dept_num = 13
or lower(job) = 'programmer'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    #
    #  Expect data for aradhyula, kapoor, martin.
    stmt = """select LOWER(last_name), LOWER(first_name), LOWER(job), LOWER(gender)
from emp 
where dept_num in (12,13,14)
and (salary > 54000)
and lower(last_name) > 'aggarwal'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    #
    # -------------------------
    #  AS.112
    #  String Literal
    # -------------------------
    #
    #  Expect data for aggarwal, kapoor, martin.
    stmt = """select LOWER('abcDeFgHijKlMNOpqrS') , LOWER(last_name)
from emp 
where salary > 70000
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    #
    #  Expect 1 row.
    stmt = """select LOWER('abc')||LOWER('DEF')||LOWER('')||LOWER('gHi')||LOWER('JkL')from emp 
where salary >= 90000 and LOWER(gender) = 'male'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    #
    #-------------------------
    # AS.113
    # Parameter
    #-------------------------
    #
    stmt = """set param ?parm1 'AbCdEfG';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?parm2 'hIjKlMn';"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """select LOWER(last_name)||LOWER(UPPER(LOWER(?parm1)))
, upper(?parm2)||gender
from emp 
where LOWER(gender) = 'female'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    #
    stmt = """select  LOWER(last_name),
cast(LOWER(?parm1)||LOWER(?parm2) as char(20) )
from emp 
where LOWER(gender) = 'female'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    #
    stmt = """select  LOWER(last_name),
cast(LOWER(?parm2) as char(20) )
from emp 
where LOWER(gender) = 'female'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s9')
    #
    stmt = """select  LOWER(last_name),
cast(LOWER(?parm1)||LOWER(?parm2)
||LOWER(UPPER(LOWER(?parm1)))
as char(21) )
from emp 
where LOWER(gender) = 'female'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s10')
    #
    stmt = """select LOWER(first_name)
, cast(LOWER(?parm1||?parm2) as varchar(20) )
from emp 
where dept_num = 15
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s11')
    #
    # -------------------------
    #  AS.114
    #  Comparision  Predicate : =
    # -------------------------
    #
    stmt = """select last_name, first_name from emp 
where gender = LOWER('FEMALE')
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s12')
    #
    stmt = """select last_name, job from emp 
where LOWER(first_name) = 'maria'
or last_name = LOWER(UPPER('kapoor'))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s13')
    #
    stmt = """select first_name, last_name from emp 
where job = LOWER(UPPER(LOWER('secretary')))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s14')
    #
    # -------------------------
    #  AS.115
    #  Comparision Predicate : <>
    # -------------------------
    #
    stmt = """select last_name, first_name from emp 
where gender <> LOWER(UPPER('female')) and gender <> 'FEMALE'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s15')
    #
    stmt = """select last_name from emp 
where LOWER(first_name) <> 'kathy' and LOWER(job) <> 'sysadmin'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s16')
    #
    # -------------------------
    #  AS.116
    #  Comparision Predicate :  <
    # -------------------------
    #
    stmt = """select last_name, first_name from emp 
where LOWER(last_name) < LOWER(first_name)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s17')
    #
    # 0 rows
    stmt = """select last_name, job, gender from emp 
where LOWER(job) < LOWER(UPPER(gender))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s18')
    #
    # -------------------------
    #  AS.117
    #  Comparision Predicate : >
    # -------------------------
    #
    stmt = """select last_name, first_name from emp 
where LOWER(last_name) > LOWER(first_name)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s19')
    #
    #  Expect all rows.
    stmt = """select last_name, job, gender from emp 
where LOWER(job) > UPPER(job)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s20')
    #
    # -------------------------
    #  AS.118
    #  Comparision Predicate : >=
    # -------------------------
    #
    stmt = """select last_name , first_name , job from emp 
where job >= LOWER('ENGINEER')
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s21')
    #
    stmt = """select LOWER(last_name) as lower_last
,  LOWER(UPPER(first_name)) as upper_last
, LOWER(job) as lower_job
from emp 
where gender >= LOWER('FEMALE')
and gender >= LOWER('female')
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s22')
    #
    stmt = """select last_name, first_name from emp 
where LOWER(job) >= 'manager'
and salary > 80000
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s23')
    #
    # -------------------------
    #  AS.119
    #  Comparision Predicate : <=
    # -------------------------
    #
    stmt = """select last_name , first_name , job
from emp 
where job <= LOWER('ENGINEER')
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s24')
    #
    stmt = """select LOWER(last_name),  LOWER(UPPER(first_name)), LOWER(job)
from emp 
where gender <= LOWER('FEMALE')
and gender >=  LOWER('female')
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s25')
    #
    stmt = """select last_name, first_name from emp 
where LOWER(job) <= 'manager'
and salary > 80000
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s26')
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1116:A09
    #  Description:        This test verifies the SQL STRING features in
    #                      predicates (IN, NOT IN).
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Check contents of emp; Populate table emp in PREUNIT.
    #  ---------------------------------
    
    stmt = """select FIRST_NAME, LAST_NAME, JOB, GENDER
from emp order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    stmt = """select FIRST_NAME, LAST_NAME, SALARY, DEPT_NUM, STR
from emp order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    
    # Creation of a temporary table for use in subqueries for testing
    # the IN and NOT IN predicates.
    
    stmt = """create table temp 
(person varchar(15), age int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Populating table temp
    stmt = """insert into temp values ('batlin' , 25);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into temp values ('KAtHy' , 35);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into temp values ('JoHn', 45);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into temp values ('steVE' , 55);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into temp values ('Maria', 30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """select * from temp order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    #
    # -------------------------
    #  AS.121
    #  IN predicate
    # -------------------------
    #
    #  Expect all 9 rows.
    stmt = """select LOWER(last_name), LOWER(first_name)
, LOWER(job), LOWER(gender)
from emp 
where ('john') IN
( select lower(person) from temp where age >= 25)
OR ('kathy' IN
( select lower(person) from temp where age >= 25))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    #
    #  Expect 1 row, for Kathy.
    stmt = """select * from emp where ('kathy',35) IN
( select lower(person),age from temp 
where lower(temp.person) = lower(emp.first_name)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    #
    #  Expect data for Kathy.
    stmt = """select * from emp where (lower('katHy'),35) IN
( select lower(person),age from temp 
where lower(temp.person) = lower(emp.first_name)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    #
    #-------------------------
    # AS.122
    # NOT IN
    #-------------------------
    #
    # Expect 0 rows.
    stmt = """select LOWER(last_name), LOWER(first_name)
, LOWER(job), LOWER(gender)
from emp 
where LOWER('MaRiA')
NOT IN
(select LOWER(person) from temp 
where age >= 20
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # Expect 0 rows.
    stmt = """select LOWER(last_name), LOWER(job), LOWER(gender)
, salary  from emp 
where UPPER('MeHtA')
NOT IN
(select UPPER(last_name) from emp 
where salary >= 35000
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #-------------------------
    # DO NOT DELETE FROM EMP!
    stmt = """delete from temp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1116:A10
    #  Description:        This test verifies the SQL STRING features in
    #                      predicates (LIKE, NULL).
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Check contents of emp; Populate table emp in PREUNIT.
    #  ---------------------------------
    
    stmt = """select FIRST_NAME, LAST_NAME, JOB, GENDER
from emp order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    stmt = """select FIRST_NAME, LAST_NAME, SALARY, DEPT_NUM, STR
from emp order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    #
    # -------------------------
    #  AS.120
    #  Between Predicate
    # -------------------------
    #
    #  Expect all 9 rows.
    stmt = """select last_name, first_name, job, str
from emp 
where   (LOWER('C'), LOWER('F'), LOWER('I'))
between (LOWER('A'), LOWER('E'), LOWER('H'))
and     (LOWER('D'), LOWER('G'), LOWER('J'))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    #
    #  Expect 5 rows.
    stmt = """select last_name, first_name, upper(job) as job
from emp 
where   (LOWER(str), LOWER(first_name), LOWER(job) )
between (LOWER('c'), LOWER('BHAVESH'), LOWER('ENGINEER'))
and     (LOWER('H'), LOWER('steve'), LOWER('director'))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
    #
    # -------------------------
    #  AS.123
    #  Like predicate
    # -------------------------
    #
    #  Expect data for hausmann, martin, ramaswamy.
    stmt = """select LOWER(last_name) as lastName, LOWER(job) as job
from emp 
where LOWER(last_name) LIKE LOWER('%MA%')
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s4')
    #
    # Expect 0 rows.
    
    stmt = """select LOWER(last_name) as lastName, LOWER(job) as job from emp 
where LOWER(last_name) LIKE upper('__ma%')
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  Expect data for aggarwal.
    stmt = """select LOWER(last_name) as lastName
, LOWER(gender) as gender, job
from emp 
where LOWER(job) LIKE LOWER('__SAD%')
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s5')
    #
    #  Expect data for baxter, ramaswamy.
    stmt = """select LOWER(last_name) as lastName, LOWER(first_name) as firstName
from emp 
where LOWER(first_name) like LOWER('%H_') and
LOWER(gender) like LOWER('__mal%')
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s6')
    #
    # -------------------------
    #  AS.124
    #  Null Predicate
    # -------------------------
    #
    #  Expect Hausmann's data.
    stmt = """select last_name, job, gender, salary
from emp 
where LOWER(first_name) IS NULL
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s7')
    #
    #  Expect all 9 rows.
    stmt = """select last_name, first_name
from emp 
where (LOWER(last_name), LOWER(job)
, LOWER(gender)) IS NOT NULL
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s8')
    #
    #  Expect 8 rows (i.e. for all except for 'hausmann').
    stmt = """select (LOWER(last_name)||LOWER(first_name))
from emp 
where ( LOWER(last_name), LOWER(first_name)
, LOWER(gender), LOWER(str) )
IS NOT NULL
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s9')
    #
    #  Expect data for 'hausmann'.
    stmt = """select LOWER(last_name), LOWER(gender) from emp 
where (LOWER(last_name)||LOWER(first_name)||LOWER(gender))
IS NULL
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s10')
    
    _testmgr.testcase_end(desc)

def test011(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1116:A11
    #  Description:        This test verifies the SQL STRING features
    #                      in predicates (quantified, EXISTS).
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Check contents of emp; Populated table emp in PREUNIT.
    #  ---------------------------------
    
    #  Expect 9 rows.
    stmt = """select FIRST_NAME, LAST_NAME, JOB, GENDER
from emp order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s0')
    
    #  Expect 9 rows.
    stmt = """select FIRST_NAME, LAST_NAME, SALARY, DEPT_NUM, STR
from emp order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    #
    # Creation of a temporary table for use in subqueries.
    #
    
    stmt = """create table tempA11 (person varchar(15), age int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Populating table tempA11
    stmt = """insert into tempA11 values ('batlin' , 25);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tempA11 values ('KAtHy' , 35);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tempA11 values ('JoHn', 45);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tempA11 values ('steVE' , 55);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tempA11 values ('Maria', 30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect 5 rows.
    stmt = """select * from tempA11 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
    
    # -------------------------
    #  AS.125. Quantified comparison predicates : ALL
    #  AS.126. Quantified comparison predicates : SOME
    #  AS.127. Quantified comparison predicates : ANY
    # -------------------------
    #
    #  Expect data for 'kathy' only.
    stmt = """select LOWER(last_name), LOWER(first_name), LOWER(job), LOWER(gender)
from emp X
where (LOWER('KATHY')) = SOME
( select LOWER(first_name) from emp Y
where  Y.last_name = X.last_name
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')
    #
    #  Expect data for 'kathy' only.
    stmt = """select LOWER(last_name), LOWER(first_name), LOWER(job), LOWER(gender)
from emp X
where LOWER('JOHN') = SOME
( select LOWER(first_name) from emp Y
where  Y.last_name = X.last_name
)
OR LOWER('KATHY') = SOME
( select LOWER(first_name) from emp Y
where  Y.last_name = X.last_name
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    #
    # Expect 0 rows.
    stmt = """select LOWER(last_name) from emp X
where LOWER('BaTlIn')
= ALL
(select LOWER(last_name) from emp Y
where LOWER(X.last_name) = LOWER(Y.last_name)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  Expect all 9 rows.
    stmt = """select LOWER(last_name) from emp X
where LOWER('BaTlIn')
<> ALL
(select LOWER(last_name) from emp Y
where LOWER(X.last_name) = LOWER(Y.last_name)
and   LOWER(Y.last_name) not like 'bat%'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    #
    #  Expect all 5 rows.
    stmt = """select person, age from tempA11 X
where lower(person)
>= SOME (select Y.person from tempA11 Y where Y.age > 30)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    #
    #  Expect 3 rows -- correlated query.
    stmt = """select person, age from tempA11 X
where lower(X.person)
>= SOME (select Y.person from tempA11 Y where X.age > 30)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    #
    #  Expect 4 rows (all except Steve)
    stmt = """select LOWER(PERSON) from tempA11 
where lower(person)
<= ANY (select person from tempA11 where age >= 20)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
    #
    #  Expect all 5 rows.
    stmt = """select LOWER(person) from tempA11 X
where lower('batline')
<> ANY (select Y.person from tempA11 Y where age >= 20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s9')
    #
    # -------------------------
    #  AS.129
    #  EXISTS
    # -------------------------
    
    #  Expect all 9 rows.
    stmt = """select LOWER(last_name), LOWER(first_name), LOWER(job), LOWER(gender)
from emp 
where  exists
( select LOWER(person) from tempA11 
where age >= 25);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s10')
    
    #  Expect data for 'steve martin'.
    stmt = """select LOWER(last_name), LOWER(first_name), LOWER(job)
from emp 
where exists
(select LOWER(UPPER(first_name)) from tempA11 
where salary >= 100000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s11')
    
    #  Expect ( ('baxter')  ('joyce') )
    stmt = """select LOWER(last_name) from emp 
where exists
(select LOWER(UPPER(last_name)) from tempA11 
where dept_num >=15);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s12')
    
    stmt = """select FIRST_NAME, LAST_NAME, SALARY, DEPT_NUM, STR
from emp order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s13')
    
    #  Expect data for 'mehta' and 'aggarwal'
    stmt = """select LOWER(last_name), LOWER(job), LOWER(gender), salary
from emp 
where exists
(select LOWER(UPPER(job)) from tempA11 
where dept_num <= 14 and
str between 'A' and 'F' and
LOWER(gender) = 'male'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s14')
    #
    # ---------------------------------
    # Empty all rows inserted into table(s) in this testcase,
    # to avoid conflict with other testcases.
    # ---------------------------------
    #
    # DO NOT DELETE FROM EMP!
    stmt = """delete from tempA11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    
    _testmgr.testcase_end(desc)

def test012(desc="""a12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1116:A12
    #  Description:        This test verifies the SQL STRING
    #                      features -- error handling with exponent,
    #                      which is not supported 1998 Beta release.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------------
    #  No table to populate -- use table from PREUNIT.
    #  ---------------------------------
    #
    
    stmt = """select last_name, first_name
from emp 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s0')
    #
    #  Exponents.
    #
    #  Simplifying to locate above Executor internal error, I find that minus and
    #  division are ok but exponent is not.
    stmt = """select last_name || first_name
, cast(char_length(last_name || first_name) **1 as int)
as cLen_exponent_1
from emp 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s1')
    stmt = """select cast(char_length(last_name || first_name) **2 as int)
as cLen_exponent_1
from emp 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s2')
    stmt = """select 3 **2
as three_squared
from emp 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s3')
    
    _testmgr.testcase_end(desc)

def test013(desc="""n01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1116:N01
    #  Description:        Negative test verifies the SQL STRING features in
    #                      predicates (IN, NOT IN): error handling
    #
    # =================== End Test Case Header  ===================
    #
    #
    
    #  ---------------------------------
    #  Check contents of emp; Populate table emp in PREUNIT.
    #  ---------------------------------
    
    stmt = """select FIRST_NAME, LAST_NAME, JOB, GENDER
from emp order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s0')
    stmt = """select FIRST_NAME, LAST_NAME, SALARY, DEPT_NUM, STR
from emp order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s1')
    #
    # Creation of a temporary table for use in subqueries for testing
    # the IN and NOT IN predicates.
    #
    
    stmt = """drop table temp;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table temp 
(person varchar(15), age int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Populating table temp
    stmt = """insert into temp values ('batlin' , 25);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into temp values ('KAtHy' , 35);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into temp values ('JoHn', 45);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into temp values ('steVE' , 55);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into temp values ('Maria', 30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """select * from temp order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s2')
    #
    # -------------------------
    #  AS.121 (see A09 for positive tests)
    #  IN predicate
    # -------------------------
    #
    stmt = """select LOWER(last_name), LOWER(first_name)
, LOWER(job), LOWER(gender)
from emp 
where (LOWER('JOHN'), LOWER('KATHY')) IN
( select LOWER(person) from temp where age >= 25)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4042')
    #
    stmt = """select LOWER(last_name), LOWER(first_name), LOWER(job)
from emp 
where (LOWER('bAtLin'), LOWER('KATHY'), LOWER('Maria') )
IN (select LOWER(UPPER(person)) from temp)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4042')
    #
    stmt = """select LOWER(last_name) from emp 
where (LOWER('aradhyula'), LOWER('MeHtA')
, LOWER('AGGARWAL'), LOWER('kApOoR')) IN
(select LOWER(last_name) from emp 
where salary > 40000
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4042')
    #
    # -------------------------
    #  AS.122 (see A09 for positive tests)
    #  NOT IN
    # -------------------------
    #
    stmt = """select LOWER(last_name), LOWER(first_name)
, LOWER(job), LOWER(gender)
from emp 
where (LOWER('MaRiA'), LOWER('steve'), LOWER('JOHN'),LOWER('kaThY'))
NOT IN
(select LOWER(UPPER(LOWER(person))) from temp 
where age >= 20
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4042')
    #
    stmt = """select LOWER(UPPER(LOWER(last_name))), LOWER(UPPER(LOWER(first_name)))
from emp 
where (LOWER('shanti'), LOWER('MARGARET'), LOWER('Maria'), LOWER('Steve'), LOWER(''))
NOT IN
(select LOWER(person) from temp 
where age >= 20
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4042')
    #
    stmt = """select LOWER(last_name), LOWER(job), LOWER(gender)
, salary  from emp 
where
(LOWER('aradhyula'), LOWER('MeHtA'), LOWER('AGGARWAL'), LOWER('kApOoR'))
NOT IN
(select LOWER(last_name) from emp 
where salary >= 35000
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4042')
    #
    #  Should get error that:
    #     The operands are mismatched data types.
    stmt = """select * from emp where ('kathy','john') IN
( select lower(person),age from temp 
where lower(temp.person) = lower(emp.first_name)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    #
    #  Should get error that:
    #     The operands of a comparison predicate must be of equal degree
    #  and should not get:
    #  (2) Arkcmp memory read error with more expressions in expression list than IN-value list:
    stmt = """select * from emp where ('john','kathy') IN
( select LOWER(person) from temp where age >= 25);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4042')
    #
    #  Should get error that:
    #     The operands of a comparison predicate must be of equal degree
    #  and should not get:
    #  (3) Internal error with more expressions in IN-value list than expression list:
    stmt = """select * from emp where ('kathy') IN
( select lower(person),age from temp 
where lower(temp.person) = lower(emp.first_name)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4042')
    #
    #-------------------------
    # Cleanup.
    # DO NOT DELETE FROM EMP!
    #-------------------------
    stmt = """delete from temp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    
    _testmgr.testcase_end(desc)

