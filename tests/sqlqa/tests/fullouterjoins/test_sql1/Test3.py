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
    
def test001(desc='Joins Set 3'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select a_l_l, d_r_r_l, e_r
from (
Select a_l_l, d_r_r_l, e_r, b_r
from (
Select a_l, d_r_r
from (
Select e, a
from t2
where (c = c)
) T1(e_l, a_l)
inner join (
Select e_l, d_r
from (
Select e
from t5
where ((25 - 41) > 66)
) T1(e_l)
left join (
Select d
from t4
where ((30 + 16) > e)
) T2(d_r)
on (d_r = e_l)
) T2(e_l_r, d_r_r)
on (a_l < d_r_r)
) T1(a_l_l, d_r_r_l)
left join (
Select e, b, d
from t2
where (d = (28 * (e + 5)))
) T2(e_r, b_r, d_r)
on (((d_r_r_l * a_l_l) + 2) < 59)
) T1
union all
select c_l, e_r, a_r
from (
Select c_l, e_r, a_r
from (
select c
from (
Select c, a, b
from t1
where ((71 * 4) = (((d - 73) - d) + (93 - 86)))
) T1
union all
select b
from (
Select b
from t1
where (8 = (58 * e))
) T2
) T1(c_l)
left join (
select e, a
from (
Select e, a
from t3
where (b = 61)
) T1
union all
select c, a
from (
select c, a
from (
Select c, a
from t3
where (89 = a)
) T1
union all
select e_l, c_r
from (
Select e_l, c_r, a_r, d_r
from (
Select e
from t1
where (62 < b)
) T1(e_l)
inner join (
Select c, a, d
from t5
where (d < c)
) T2(c_r, a_r, d_r)
on ((27 + 44) > e_l)
) T2
) T2
) T2(e_r, a_r)
on (99 = (75 + 11))
) T2
order by 1, 2, 3
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
select e, c, a
from (
Select e, c, a, d
from t5
where (53 > (e * 63))
) T1
union all
select e, c, b
from (
Select e, c, b
from t4
where (b = b)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", 'a1s2')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a, d
from t2
where (33 < e)
) T1
union all
select e
from (
select e
from (
Select e, b
from t2
where (32 = (91 * 37))
) T1
union all
select a
from (
select a
from (
Select a, b, d
from t4
where ((a * a) = 19)
) T1
union all
select b
from (
Select b
from t5
where (78 = 83)
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
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", 'a1s3')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a, d
from (
Select c, a, d
from t5
where (57 = ((30 - 59) * b))
) T1
union all
select e, c, b
from (
Select e, c, b
from t1
where ((d * c) = e)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", 'a1s4')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a, d
from (
Select c, a, d
from t3
where (a = a)
) T1
union all
select e, c, b
from (
Select e, c, b, d
from t3
where ((b + d) = b)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", 'a1s5')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l_l, b_r_l
from (
Select a_l_l, b_r_l, e_l_l, e_r
from (
Select e_l, a_l, b_l, a_r, b_r
from (
Select e, a, b
from t4
where ((77 * e) = d)
) T1(e_l, a_l, b_l)
full join (
Select a, b
from t3
where (c = d)
) T2(a_r, b_r)
on (e_l < 80)
) T1(e_l_l, a_l_l, b_l_l, a_r_l, b_r_l)
full join (
Select e
from t2
where (d = 39)
) T2(e_r)
on ((37 * 94) > e_r)
) T1
union all
select e, d
from (
Select e, d
from t5
where (e < b)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", 'a1s6')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_r_l, b_l_l, c_r
from (
Select c_r_l, b_l_l, c_r, d_r
from (
Select c_l, b_l, c_r
from (
Select c, b
from t2
where (41 = b)
) T1(c_l, b_l)
left join (
Select c
from t2
where (d = e)
) T2(c_r)
on ((38 + b_l) = c_r)
) T1(c_l_l, b_l_l, c_r_l)
left join (
Select c, a, d
from t1
where (25 < 10)
) T2(c_r, a_r, d_r)
on (c_r = (66 * 7))
) T1
union all
select b_l, d_l, b_r
from (
Select b_l, d_l, b_r
from (
Select b, d
from t1
where (98 = 63)
) T1(b_l, d_l)
left join (
Select e, b, d
from t1
where (61 > c)
) T2(e_r, b_r, d_r)
on (b_l = d_l)
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
select e
from (
Select e
from t4
where (((((13 + 51) + ((6 + b) - e)) - 68) * 47) = a)
) T1
union all
select e
from (
Select e, d
from t2
where (92 = 4)
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
from t2
where (c = c)
) T1
union all
select c_l, d_l
from (
Select c_l, d_l, b_r
from (
Select c, d
from t3
where (b > b)
) T1(c_l, d_l)
left join (
Select b
from t3
where (44 = (42 * a))
) T2(b_r)
on (93 = 65)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", 'a1s9')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, a, b
from t5
where (38 = 10)
) T1
union all
select d
from (
Select d
from t3
where ((((c - 66) - 15) * 20) < a)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", 'a1s10')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
select c
from (
Select c
from t2
where (b = 12)
) T1
union all
select b
from (
Select b
from t2
where ((99 + d) > b)
) T2
) T1
union all
select c
from (
Select c, a, b, d
from t1
where (b < 39)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", 'a1s11')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, c_r
from (
Select a_l, c_r
from (
Select a
from t1
where (39 = d)
) T1(a_l)
inner join (
Select c
from t2
where (68 < (a - (55 + 32)))
) T2(c_r)
on (54 = a_l)
) T1
union all
select e, a
from (
Select e, a, d
from t1
where (38 = (4 - 71))
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
select c, a
from (
select c, a
from (
Select c, a, b
from t1
where (97 > (a * e))
) T1
union all
select c, a
from (
Select c, a
from t1
where (74 = d)
) T2
) T1
union all
select b, d
from (
Select b, d
from t2
where (a > b)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", 'a1s13')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, b_l
from (
Select a_l, b_l, e_r
from (
Select e, a, b, d
from t4
where (65 = (89 - (51 - c)))
) T1(e_l, a_l, b_l, d_l)
left join (
Select e
from t2
where (d = 16)
) T2(e_r)
on (e_r = 90)
) T1
union all
select d_l, c_l_l_r
from (
Select d_l, c_l_l_r
from (
Select a, d
from t2
where ((10 * c) = 57)
) T1(a_l, d_l)
full join (
Select c_l_l, e_l_r, b_l_r
from (
Select c_l, d_l, e_l_r
from (
select c, b, d
from (
Select c, b, d
from t2
where (71 = 19)
) T1
union all
select e, c, b
from (
Select e, c, b, d
from t4
where (72 < (38 - (34 * (a + 98))))
) T2
) T1(c_l, b_l, d_l)
inner join (
Select e_l, d_l, c_r
from (
Select e, d
from t2
where (b = 45)
) T1(e_l, d_l)
inner join (
Select c, d
from t4
where ((e - c) > d)
) T2(c_r, d_r)
on (25 = c_r)
) T2(e_l_r, d_l_r, c_r_r)
on ((c_l + 51) = 1)
) T1(c_l_l, d_l_l, e_l_r_l)
left join (
Select e_l, b_l, c_r
from (
Select e, b, d
from t5
where (c = a)
) T1(e_l, b_l, d_l)
left join (
Select c, b
from t1
where (38 = 32)
) T2(c_r, b_r)
on (c_r = (96 - c_r))
) T2(e_l_r, b_l_r, c_r_r)
on ((c_l_l + 12) < (b_l_r - e_l_r))
) T2(c_l_l_r, e_l_r_r, b_l_r_r)
on ((d_l * c_l_l_r) > (c_l_l_r + c_l_l_r))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", 'a1s14')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, e_r
from (
Select e_l, e_r
from (
select e
from (
Select e
from t3
where (b = d)
) T1
union all
select c
from (
Select c, b
from t3
where (((67 - d) - a) < 77)
) T2
) T1(e_l)
full join (
Select e
from t4
where (41 < 14)
) T2(e_r)
on (((40 - ((42 + e_r) + 15)) + e_l) = (86 - e_r))
) T1
union all
select d_l_l, c_r
from (
Select d_l_l, c_r, b_r, d_r
from (
Select e_l, d_l, d_l_r
from (
Select e, a, d
from t1
where (16 < (48 - 3))
) T1(e_l, a_l, d_l)
inner join (
select d_l, a_l_r
from (
Select d_l, a_l_r
from (
Select d
from t3
where (b < a)
) T1(d_l)
inner join (
Select a_l, b_r
from (
Select c, a, d
from t4
where (86 = 41)
) T1(c_l, a_l, d_l)
inner join (
select b
from (
Select b
from t5
where (((80 + (d - a)) - (81 * (5 - (e + (36 + 44))))) > 70)
) T1
union all
select b
from (
Select b
from t5
where (15 = c)
) T2
) T2(b_r)
on (b_r > a_l)
) T2(a_l_r, b_r_r)
on (84 < (a_l_r - (a_l_r + a_l_r)))
) T1
union all
select e_l_l, c_r_l
from (
Select e_l_l, c_r_l, e_r, c_r
from (
Select e_l, c_r
from (
Select e
from t5
where (77 > 37)
) T1(e_l)
left join (
select c, a, d
from (
select c, a, d
from (
Select c, a, d
from t2
where (b = 19)
) T1
union all
select e, a, b
from (
Select e, a, b
from t5
where (e = (41 + c))
) T2
) T1
union all
select e, b, d
from (
Select e, b, d
from t1
where (5 < 54)
) T2
) T2(c_r, a_r, d_r)
on ((e_l * e_l) > c_r)
) T1(e_l_l, c_r_l)
inner join (
select e, c
from (
Select e, c
from t5
where (((c + b) - (d * e)) = c)
) T1
union all
select e_l, d_l
from (
Select e_l, d_l, a_r
from (
Select e, b, d
from t5
where (74 > 74)
) T1(e_l, b_l, d_l)
full join (
Select a
from t3
where (36 > (e - a))
) T2(a_r)
on (57 = e_l)
) T2
) T2(e_r, c_r)
on (e_l_l = 95)
) T2
) T2(d_l_r, a_l_r_r)
on (4 = e_l)
) T1(e_l_l, d_l_l, d_l_r_l)
left join (
Select c, b, d
from t4
where ((c - a) = 28)
) T2(c_r, b_r, d_r)
on (95 > 68)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", 'a1s15')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, d
from (
Select e, d
from t4
where ((45 - d) > 12)
) T1
union all
select e, c
from (
select e, c
from (
select e, c
from (
Select e, c, a, b
from t1
where (b < ((80 - d) * 60))
) T1
union all
select e, c
from (
select e, c
from (
Select e, c, d
from t1
where (b > b)
) T1
union all
select c, d
from (
Select c, d
from t3
where (11 = ((56 + 24) * d))
) T2
) T2
) T1
union all
select a, d
from (
Select a, d
from t4
where (d < 2)
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
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", 'a1s16')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, c_l
from (
Select e_l, c_l, a_r
from (
Select e, c
from t1
where (d = (a + e))
) T1(e_l, c_l)
full join (
Select a
from t5
where ((d * (13 + ((b - d) - 75))) < 61)
) T2(a_r)
on (59 < ((a_r * (83 + e_l)) + c_l))
) T1
union all
select c, b
from (
Select c, b
from t4
where (((((e + b) - (b * e)) + c) + (63 + (((36 * c) * 68) * 99))) < (c - ((6 - 17) + ((c * 50) * d))))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", 'a1s17')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l, a_r_r, b_l_r
from (
Select c_l, a_r_r, b_l_r
from (
Select c, b, d
from t1
where ((a + c) < a)
) T1(c_l, b_l, d_l)
full join (
Select b_l, a_r
from (
Select a, b
from t3
where (81 = 47)
) T1(a_l, b_l)
left join (
select a
from (
Select a, d
from t1
where (d < (((e - a) + 41) + ((67 - 85) - d)))
) T1
union all
select d
from (
Select d
from t3
where ((a + d) = a)
) T2
) T2(a_r)
on (93 > 20)
) T2(b_l_r, a_r_r)
on (a_r_r = c_l)
) T1
union all
select e_l, e_r, a_r
from (
Select e_l, e_r, a_r
from (
Select e
from t4
where (65 > c)
) T1(e_l)
full join (
Select e, c, a, b
from t3
where (c < d)
) T2(e_r, c_r, a_r, b_r)
on (((((31 * 62) * e_l) - e_r) + a_r) = 11)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", 'a1s18')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, a, b, d
from t2
where (a < 47)
) T1
union all
select e
from (
Select e
from t5
where (36 > 21)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", 'a1s19')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l_l, a_r, d_r
from (
Select e_l_l, a_r, d_r
from (
select e_l
from (
select e_l, b_l, e_l_r
from (
Select e_l, b_l, e_l_r
from (
Select e, b, d
from t4
where (39 < d)
) T1(e_l, b_l, d_l)
inner join (
select e_l
from (
Select e_l, a_l, a_r
from (
Select e, a
from t2
where (92 = b)
) T1(e_l, a_l)
full join (
Select a, b
from t5
where ((a + 69) > 82)
) T2(a_r, b_r)
on (47 = (5 - (e_l * 15)))
) T1
union all
select b
from (
select b
from (
Select b
from t1
where (30 < 87)
) T1
union all
select e
from (
Select e, a, d
from t2
where ((29 - b) = (14 * d))
) T2
) T2
) T2(e_l_r)
on (e_l < e_l)
) T1
union all
select e_l, a_l_r, a_r_r
from (
Select e_l, a_l_r, a_r_r
from (
select e
from (
select e
from (
select e, c
from (
Select e, c, a, b
from t4
where (c = c)
) T1
union all
select a_l, c_r
from (
Select a_l, c_r
from (
Select a, d
from t2
where (e < (a + b))
) T1(a_l, d_l)
left join (
Select e, c, d
from t4
where (30 < 83)
) T2(e_r, c_r, d_r)
on (79 = c_r)
) T2
) T1
union all
select b
from (
Select b
from t1
where (d = d)
) T2
) T1
union all
select b_l
from (
Select b_l, a_r
from (
Select b
from t4
where (e > 55)
) T1(b_l)
inner join (
select a
from (
Select a
from t2
where (35 > 31)
) T1
union all
select d
from (
Select d
from t4
where (35 > c)
) T2
) T2(a_r)
on ((61 * 96) > 85)
) T2
) T1(e_l)
full join (
Select a_l, b_l, a_r
from (
Select a, b
from t3
where (83 = 97)
) T1(a_l, b_l)
full join (
Select a
from t5
where (b = 54)
) T2(a_r)
on (a_l > ((((a_r + 69) + 94) + 14) * 63))
) T2(a_l_r, b_l_r, a_r_r)
on (4 > a_r_r)
) T2
) T1
union all
select e
from (
Select e
from t2
where (c > ((79 * 21) - 62))
) T2
) T1(e_l_l)
inner join (
Select a, d
from t1
where (d > 34)
) T2(a_r, d_r)
on ((a_r + ((a_r * a_r) * e_l_l)) > e_l_l)
) T1
union all
select b_r_r_l, d_l_l, d_r
from (
Select b_r_r_l, d_l_l, d_r
from (
Select d_l, b_r_r
from (
Select e, a, b, d
from t3
where (d < 80)
) T1(e_l, a_l, b_l, d_l)
left join (
Select e_l, b_r
from (
Select e, a
from t5
where (b < 14)
) T1(e_l, a_l)
full join (
select b
from (
Select b
from t2
where ((d - (22 * b)) > b)
) T1
union all
select a
from (
Select a
from t5
where (a > 16)
) T2
) T2(b_r)
on (37 > 39)
) T2(e_l_r, b_r_r)
on (((d_l + 33) - b_r_r) = 22)
) T1(d_l_l, b_r_r_l)
left join (
Select a, d
from t4
where (a = 71)
) T2(a_r, d_r)
on (b_r_r_l = (((d_l_l * b_r_r_l) - 39) - (9 - d_r)))
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    ##expectfile $test_dir/Test03exp a1s20
    #execute s1;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #************************************************
    
    _testmgr.testcase_end(desc)

