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
    
def test001(desc='Joins Set 4'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l
from (
Select b_l, b_r
from (
Select a, b
from t1
where (53 < 85)
) T1(a_l, b_l)
inner join (
Select b
from t2
where (d = 13)
) T2(b_r)
on (48 < (b_r * ((95 - 49) + 93)))
) T1
union all
select c
from (
Select c
from t2
where (b < 0)
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
select e, b
from (
Select e, b
from t1
where ((86 * ((96 + a) - 9)) = ((((c - c) - (d + 65)) - c) + (a + 23)))
) T1
union all
select a, b
from (
Select a, b, d
from t5
where (c = 13)
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
from t2
where (c > c)
) T1
union all
select a
from (
Select a, b
from t3
where ((35 - b) > 19)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s3')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, b, d
from t3
where (44 = 94)
) T1
union all
select b
from (
select b
from (
Select b
from t1
where (b = e)
) T1
union all
select c_r_l
from (
select c_r_l, e_r
from (
Select c_r_l, e_r, b_r
from (
Select c_l, c_r
from (
Select c
from t4
where (e > ((((((b - (a + 0)) + e) + 82) - 95) * 32) * 25))
) T1(c_l)
full join (
select c
from (
Select c
from t3
where ((a - (50 - b)) > 7)
) T1
union all
select e
from (
Select e
from t4
where (((d - d) - 87) > 33)
) T2
) T2(c_r)
on ((c_l * (c_r - (79 * c_r))) > 29)
) T1(c_l_l, c_r_l)
left join (
Select e, b
from t2
where (2 = 82)
) T2(e_r, b_r)
on (72 < b_r)
) T1
union all
select e, b
from (
Select e, b
from t1
where (c > 20)
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
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s4')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
select e
from (
Select e, a, b
from t5
where (81 > 28)
) T1
union all
select e
from (
select e
from (
Select e
from t4
where (4 = d)
) T1
union all
select a
from (
Select a, d
from t1
where ((e + (d * 98)) > 90)
) T2
) T2
) T1
union all
select c
from (
Select c, d
from t4
where ((23 - ((e + 56) - d)) = (11 + 42))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s5')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, a, d
from t4
where (c = (5 + d))
) T1
union all
select e
from (
Select e
from t4
where (a > b)
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
select e
from (
Select e, c, d
from t5
where (c = 81)
) T1
union all
select e
from (
select e
from (
Select e, a, d
from t1
where ((c + 60) < 48)
) T1
union all
select c
from (
Select c
from t4
where (33 < d)
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
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s7')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, d_l, a_r
from (
Select e_l, d_l, a_r
from (
Select e, d
from t5
where (44 < 23)
) T1(e_l, d_l)
left join (
Select a
from t2
where (d < c)
) T2(a_r)
on ((12 * d_l) = d_l)
) T1
union all
select e, c, b
from (
Select e, c, b
from t4
where (e < c)
) T2
order by 1, 2, 3
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
select e, c
from (
Select e, c
from t1
where ((70 * 89) = 18)
) T1
union all
select c, a
from (
Select c, a, d
from t4
where (96 > b)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s9')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, e_l_r
from (
Select a_l, e_l_r
from (
Select a
from t4
where ((b + 69) < (c * a))
) T1(a_l)
left join (
Select e_l, e_l_r, c_r_r
from (
Select e, a, d
from t2
where (4 < 7)
) T1(e_l, a_l, d_l)
inner join (
Select e_l, c_r
from (
Select e, b
from t4
where (58 = 63)
) T1(e_l, b_l)
left join (
Select c
from t5
where (c = 12)
) T2(c_r)
on (69 < 97)
) T2(e_l_r, c_r_r)
on (c_r_r < e_l_r)
) T2(e_l_r, e_l_r_r, c_r_r_r)
on (69 < (e_l_r * 70))
) T1
union all
select c, b
from (
select c, b
from (
Select c, b, d
from t1
where (62 = b)
) T1
union all
select a, d
from (
Select a, d
from t1
where (d = a)
) T2
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s10')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t4
where (1 < (d * e))
) T1
union all
select e
from (
Select e, c, a
from t2
where ((d * 93) = e)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s11')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t1
where (39 = a)
) T1
union all
select d_l
from (
Select d_l, a_r, b_r, d_r
from (
Select e, d
from t2
where (27 = e)
) T1(e_l, d_l)
inner join (
Select a, b, d
from t5
where (a = 91)
) T2(a_r, b_r, d_r)
on (d_l = 33)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s12')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, b
from (
Select e, c, b, d
from t1
where ((95 - c) = 44)
) T1
union all
select c, a, d
from (
Select c, a, d
from t4
where (14 < 46)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s13')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t5
where (68 < e)
) T1
union all
select b
from (
Select b, d
from t5
where (57 = 37)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s14')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l
from (
select c_l
from (
Select c_l, b_r
from (
Select c
from t2
where (73 = (99 + 15))
) T1(c_l)
inner join (
select b
from (
select b
from (
select b
from (
Select b
from t1
where ((1 - (42 + 6)) = ((b * 22) * c))
) T1
union all
select e
from (
select e, a
from (
Select e, a, b
from t5
where (96 = b)
) T1
union all
select c, a
from (
Select c, a
from t1
where (c = 69)
) T2
) T2
) T1
union all
select e
from (
Select e, c, a
from t4
where ((e + b) > 86)
) T2
) T1
union all
select a
from (
Select a, b
from t5
where (89 > 16)
) T2
) T2(b_r)
on (c_l = b_r)
) T1
union all
select d
from (
Select d
from t3
where (13 > 8)
) T2
) T1
union all
select d
from (
select d
from (
select d
from (
select d
from (
select d
from (
Select d
from t1
where ((a - e) < 53)
) T1
union all
select e
from (
Select e, a
from t3
where (65 < c)
) T2
) T1
union all
select c_l
from (
Select c_l, e_r
from (
Select e, c, b, d
from t2
where ((c - 4) > e)
) T1(e_l, c_l, b_l, d_l)
left join (
Select e, b, d
from t2
where (a = (90 + b))
) T2(e_r, b_r, d_r)
on (76 > (c_l + e_r))
) T2
) T1
union all
select c_l
from (
Select c_l, a_r, b_r
from (
Select e, c
from t3
where (c > 29)
) T1(e_l, c_l)
full join (
Select c, a, b
from t4
where (19 = 84)
) T2(c_r, a_r, b_r)
on (b_r > 83)
) T2
) T1
union all
select c_l
from (
Select c_l, b_r
from (
Select c
from t1
where (61 > a)
) T1(c_l)
inner join (
Select b
from t2
where (c = a)
) T2(b_r)
on (b_r > c_l)
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
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s15')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c, d
from t1
where (86 < d)
) T1
union all
select b
from (
Select b
from t4
where ((a + c) > ((14 + e) - e))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s16')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t4
where (a = e)
) T1
union all
select a
from (
Select a, d
from t3
where (23 > 43)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s17')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t5
where (90 > 79)
) T1
union all
select e
from (
select e
from (
select e, b
from (
Select e, b
from t2
where (15 > b)
) T1
union all
select b_r_l_l, c_r
from (
Select b_r_l_l, c_r, b_r
from (
Select b_r_l, d_r_l, b_r
from (
Select c_l, b_r, d_r
from (
Select c
from t3
where (26 > 98)
) T1(c_l)
inner join (
Select a, b, d
from t5
where (b = 14)
) T2(a_r, b_r, d_r)
on (25 = d_r)
) T1(c_l_l, b_r_l, d_r_l)
full join (
Select c, a, b
from t4
where (56 > (d + (d - c)))
) T2(c_r, a_r, b_r)
on (b_r_l > 69)
) T1(b_r_l_l, d_r_l_l, b_r_l)
left join (
Select e, c, a, b
from t5
where ((a - (b * a)) < e)
) T2(e_r, c_r, a_r, b_r)
on (90 = b_r)
) T2
) T1
union all
select c
from (
Select c
from t1
where ((96 - b) = 37)
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
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s18')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l, a_r_r
from (
Select d_l, a_r_r
from (
Select c, b, d
from t5
where ((99 - 22) < d)
) T1(c_l, b_l, d_l)
left join (
Select d_r_l, c_r, a_r
from (
Select b_l_l, e_r, d_r
from (
Select b_l, b_r
from (
Select b
from t2
where (39 = 9)
) T1(b_l)
left join (
Select b
from t2
where (74 > 20)
) T2(b_r)
on (b_r = b_r)
) T1(b_l_l, b_r_l)
inner join (
Select e, a, d
from t1
where (77 = d)
) T2(e_r, a_r, d_r)
on (62 < b_l_l)
) T1(b_l_l_l, e_r_l, d_r_l)
inner join (
select c, a
from (
Select c, a, d
from t1
where (a = 77)
) T1
union all
select a, d
from (
Select a, d
from t3
where (13 > (59 + 84))
) T2
) T2(c_r, a_r)
on ((a_r - ((a_r * c_r) + a_r)) > 10)
) T2(d_r_l_r, c_r_r, a_r_r)
on (((d_l + 51) * (20 + 39)) > 33)
) T1
union all
select d_l, a_r
from (
Select d_l, a_r, d_r
from (
Select a, d
from t4
where (69 = d)
) T1(a_l, d_l)
inner join (
select a, d
from (
Select a, d
from t4
where (30 = (a + d))
) T1
union all
select a_l, b_l
from (
select a_l, b_l
from (
Select a_l, b_l, e_l_r, a_r_r, c_r_r
from (
Select a, b
from t5
where (37 > b)
) T1(a_l, b_l)
left join (
select e_l, c_r, a_r
from (
Select e_l, c_r, a_r
from (
Select e
from t4
where (a = 59)
) T1(e_l)
left join (
Select c, a
from t2
where ((95 + 85) = b)
) T2(c_r, a_r)
on (a_r > 65)
) T1
union all
select c, a, d
from (
Select c, a, d
from t2
where ((48 - d) > 3)
) T2
) T2(e_l_r, c_r_r, a_r_r)
on (70 = e_l_r)
) T1
union all
select c, a
from (
Select c, a
from t4
where (c = 8)
) T2
) T2
) T2(a_r, d_r)
on (a_r = a_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s19')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b, d
from t2
where (e > 33)
) T1
union all
select b
from (
Select b
from t4
where (c < b)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", 'a1s20')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    #*********************************************
    
    _testmgr.testcase_end(desc)

