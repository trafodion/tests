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

#****************************************
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc='Joins Set 2'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select e
from (
select e
from (
Select e, b, d
from t3
where (55 = 61)
) T1
union all
select d
from (
Select d
from t5
where (c = 89)
) T2
) T1
union all
select c
from (
Select c, a
from t3
where (29 < 2)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, d
from t5
where ((b * a) = (0 + 44))
) T1
union all
select a, d
from (
Select a, d
from t3
where (c < 30)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", 'a1s2')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a, d
from (
Select c, a, d
from t4
where (c = 11)
) T1
union all
select e, c, b
from (
Select e, c, b
from t3
where ((a + 3) = b)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", 'a1s3')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, a, d
from t1
where (e = ((61 * c) * e))
) T1
union all
select d
from (
Select d
from t5
where (78 > c)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", 'a1s4')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, c_l_r, a_r_r
from (
Select e_l, c_l_r, a_r_r
from (
Select e
from t5
where (66 > e)
) T1(e_l)
full join (
Select c_l, a_r
from (
Select c
from t2
where ((4 * 51) < a)
) T1(c_l)
full join (
Select c, a
from t2
where ((79 + 50) < 82)
) T2(c_r, a_r)
on ((52 - (62 + a_r)) < a_r)
) T2(c_l_r, a_r_r)
on (13 = c_l_r)
) T1
union all
select c, a, b
from (
Select c, a, b, d
from t4
where (32 > (77 * b))
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", 'a1s5')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l, b_r
from (
Select d_l, b_r
from (
Select d
from t4
where (d > e)
) T1(d_l)
left join (
Select b
from t4
where (62 < 27)
) T2(b_r)
on (d_l = b_r)
) T1
union all
select e, c
from (
Select e, c, d
from t5
where (e > a)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", 'a1s6')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, a
from (
Select e, c, a
from t3
where (b > 59)
) T1
union all
select b_r_l, a_r_l, e_r
from (
Select b_r_l, a_r_l, e_r, d_r
from (
Select a_l, a_r, b_r
from (
Select a
from t4
where (31 = e)
) T1(a_l)
left join (
Select c, a, b
from t1
where (d < a)
) T2(c_r, a_r, b_r)
on (11 > (73 + 54))
) T1(a_l_l, a_r_l, b_r_l)
left join (
Select e, c, d
from t5
where ((12 * 94) = 27)
) T2(e_r, c_r, d_r)
on (79 > b_r_l)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", 'a1s7')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l
from (
Select e_l, a_r
from (
select e
from (
Select e, c, b
from t2
where (32 < 45)
) T1
union all
select a
from (
Select a
from t2
where (b = e)
) T2
) T1(e_l)
left join (
Select e, a
from t3
where ((c * d) = (19 - 10))
) T2(e_r, a_r)
on ((e_l - 18) = 0)
) T1
union all
select e
from (
Select e
from t3
where (a = d)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", 'a1s8')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, d
from (
Select a, d
from t2
where ((d - a) = 39)
) T1
union all
select e, c
from (
Select e, c, d
from t1
where (79 < (d - ((35 * (88 - 38)) - d)))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", 'a1s9')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_r_l
from (
Select a_r_l, c_r
from (
Select d_l, a_r
from (
Select d
from t3
where (38 < (c * c))
) T1(d_l)
full join (
Select a
from t5
where (75 = a)
) T2(a_r)
on (94 = 7)
) T1(d_l_l, a_r_l)
inner join (
Select c
from t4
where (44 = b)
) T2(c_r)
on (24 > a_r_l)
) T1
union all
select e
from (
Select e
from t5
where (d = 74)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, c_r_l_r
from (
Select e_l, c_r_l_r
from (
select e
from (
Select e, c, b, d
from t4
where (61 > (d * (b - 60)))
) T1
union all
select a
from (
Select a
from t1
where (59 = e)
) T2
) T1(e_l)
inner join (
Select a_r_l, c_r_l, b_r
from (
Select d_l, c_r, a_r
from (
Select d
from t3
where (12 = (65 + e))
) T1(d_l)
full join (
Select c, a
from t3
where (94 > e)
) T2(c_r, a_r)
on (79 < 2)
) T1(d_l_l, c_r_l, a_r_l)
full join (
Select c, b
from t2
where (b = 2)
) T2(c_r, b_r)
on (16 = (56 - (a_r_l + c_r_l)))
) T2(a_r_l_r, c_r_l_r, b_r_r)
on (e_l > e_l)
) T1
union all
select e, c
from (
Select e, c, d
from t2
where (e = 6)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b
from t1
where ((17 + 22) = 34)
) T1
union all
select e, a
from (
Select e, a
from t5
where ((55 * 39) = ((39 * 90) + (d + e)))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t3
where (d = 8)
) T1
union all
select e
from (
Select e, a, d
from t4
where (73 = e)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", 'a1s13')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, b
from t5
where (a = a)
) T1
union all
select e
from (
Select e
from t4
where (79 < 7)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", 'a1s14')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, d
from t3
where (e > a)
) T1
union all
select a
from (
Select a
from t2
where (99 = 97)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", 'a1s15')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, d
from t4
where (30 < 42)
) T1
union all
select c
from (
Select c
from t2
where ((93 * ((c - 49) - 47)) = 35)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", 'a1s16')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l, b_l_r
from (
Select c_l, b_l_r
from (
Select c
from t4
where ((55 - 52) = a)
) T1(c_l)
left join (
Select b_l, e_l_r
from (
Select b
from t1
where (c > 50)
) T1(b_l)
left join (
Select e_l, b_l, e_l_r, c_r_r
from (
Select e, c, b
from t5
where (19 = 33)
) T1(e_l, c_l, b_l)
left join (
Select e_l, c_r
from (
Select e
from t2
where ((((a + 18) - 13) * b) = 72)
) T1(e_l)
left join (
Select c, a, b
from t5
where (35 > 33)
) T2(c_r, a_r, b_r)
on (4 = e_l)
) T2(e_l_r, c_r_r)
on (26 = 69)
) T2(e_l_r, b_l_r, e_l_r_r, c_r_r_r)
on (e_l_r = 61)
) T2(b_l_r, e_l_r_r)
on (((14 * (29 * c_l)) * 26) = 47)
) T1
union all
select e, a
from (
Select e, a, b
from t1
where (77 < 43)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", 'a1s17')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
select e
from (
Select e, a, b
from t2
where (20 = d)
) T1
union all
select c
from (
Select c
from t4
where (35 > b)
) T2
) T1
union all
select c
from (
select c
from (
Select c
from t1
where (e < b)
) T1
union all
select c_l
from (
select c_l, c_r, b_r
from (
Select c_l, c_r, b_r
from (
Select c, b
from t5
where (83 = (c * d))
) T1(c_l, b_l)
left join (
Select c, b
from t1
where (a < 2)
) T2(c_r, b_r)
on (20 = c_l)
) T1
union all
select e, a, d
from (
Select e, a, d
from t1
where (93 < 66)
) T2
) T2
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", 'a1s18')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, d
from (
Select e, d
from t3
where (54 = 13)
) T1
union all
select b_l, a_r
from (
Select b_l, a_r
from (
Select b
from t1
where (15 = b)
) T1(b_l)
left join (
select a
from (
Select a
from t2
where (e < (b + a))
) T1
union all
select e
from (
Select e, a, d
from t4
where (e > 27)
) T2
) T2(a_r)
on (((43 - 90) + a_r) = a_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t3
where (b < 21)
) T1
union all
select d
from (
Select d
from t5
where (((47 - b) + 24) = 47)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", 'a1s20')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #*******************************************
    
    _testmgr.testcase_end(desc)

