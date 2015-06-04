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
    
def test001(desc="""Joins Set 44"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, e_r, c_r, d_r
from (
Select a, b
from p4
where (a = d)
) T1(a_l, b_l)
left join (
Select e, c, d
from p2
where (35 = 71)
) T2(e_r, c_r, d_r)
on (0 = d_r)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test44exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, a_r
from (
Select b
from p4
where (74 > (66 * ((a * 31) + (68 + a))))
) T1(b_l)
full join (
Select c, a, b
from p3
where (d > a)
) T2(c_r, a_r, b_r)
on (33 = a_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test44exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_l, c_r
from (
Select c, a, b
from p4
where ((28 = 27) OR ((d = ((a * 48) * 25)) AND (a > (43 - d))))
) T1(c_l, a_l, b_l)
left join (
Select c
from p3
where ((28 * 53) = 43)
) T2(c_r)
on (c_r = 53)
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
Select e_l, c_l, b_l, e_r, b_r
from (
Select e, c, b
from p4
where (((a - 62) > (63 * 69)) OR ((94 = 40) OR (78 < (d * 69))))
) T1(e_l, c_l, b_l)
left join (
Select e, c, b
from p5
where ((e * (54 - e)) > 34)
) T2(e_r, c_r, b_r)
on (e_r > (31 + (e_l + (55 + c_l))))
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test44exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, a_r
from (
select c, a
from (
select c, a, b
from (
Select c, a, b
from p4
where (34 = 88)
) T1
union all
select c, a, d
from (
Select c, a, d
from p2
where (c = a)
) T2
) T1
union all
select e_l, c_r_l_r
from (
Select e_l, c_r_l_r
from (
Select e, c, b
from p5
where (e > 10)
) T1(e_l, c_l, b_l)
inner join (
select e_l_l, c_r_l
from (
Select e_l_l, c_r_l, b_l_l, b_r
from (
Select e_l, b_l, c_r
from (
Select e, b
from p3
where (((18 - 89) < 46) OR ((15 > a) AND (21 = (d * 93))))
) T1(e_l, b_l)
left join (
Select c, a
from p1
where (10 < 67)
) T2(c_r, a_r)
on ((31 > e_l) AND ((b_l > (33 - e_l)) OR (b_l < (62 + 48))))
) T1(e_l_l, b_l_l, c_r_l)
inner join (
Select e, c, a, b
from p3
where (96 > e)
) T2(e_r, c_r, a_r, b_r)
on (55 < 57)
) T1
union all
select e, b
from (
Select e, b
from p2
where ((74 - c) > c)
) T2
) T2(e_l_l_r, c_r_l_r)
on (59 < 5)
) T2
) T1(c_l, a_l)
inner join (
Select e, a, d
from p3
where (1 = 90)
) T2(e_r, a_r, d_r)
on ((0 < 26) AND (a_r > a_l))
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
Select c_l_l_l, b_r_r_l, e_r, b_r
from (
Select c_l_l, b_r_r, b_l_r
from (
Select c_l, b_l, c_r, a_r
from (
Select c, b
from p1
where (c > (72 * 1))
) T1(c_l, b_l)
left join (
select c, a
from (
select c, a
from (
Select c, a
from p1
where (73 = e)
) T1
union all
select c, a
from (
select c, a, b, d
from (
Select c, a, b, d
from p4
where (a > 46)
) T1
union all
select e, c, b, d
from (
Select e, c, b, d
from p5
where (56 = 10)
) T2
) T2
) T1
union all
select e, a
from (
Select e, a, b
from p2
where ((17 + 94) > 1)
) T2
) T2(c_r, a_r)
on ((c_l = 64) OR (83 = 40))
) T1(c_l_l, b_l_l, c_r_l, a_r_l)
full join (
Select b_l, e_r, b_r
from (
Select b
from p3
where (63 > 86)
) T1(b_l)
inner join (
select e, b, d
from (
Select e, b, d
from p3
where ((c < c) AND (e = 24))
) T1
union all
select e, c, d
from (
Select e, c, d
from p5
where ((35 < b) AND ((7 + e) > 66))
) T2
) T2(e_r, b_r, d_r)
on (31 = b_r)
) T2(b_l_r, e_r_r, b_r_r)
on ((b_l_r < 52) AND (b_r_r < 72))
) T1(c_l_l_l, b_r_r_l, b_l_r_l)
left join (
Select e, b
from p3
where (b = (16 + (13 - b)))
) T2(e_r, b_r)
on (e_r > 30)
order by 1, 2, 3, 4
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
Select a_l, b_r
from (
Select a, b
from p4
where (b = 9)
) T1(a_l, b_l)
inner join (
Select b
from p2
where (20 < 7)
) T2(b_r)
on ((a_l = b_r) AND (b_r = 48))
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
Select a_l, e_r
from (
Select a
from p2
where ((b + 0) = c)
) T1(a_l)
inner join (
Select e
from p1
where (d > 59)
) T2(e_r)
on ((85 < a_l) AND ((e_r < 21) AND ((a_l = 78) AND ((a_l = 30) AND (e_r > 67)))))
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
Select c_l, b_l, e_r
from (
select c, b
from (
Select c, b, d
from p3
where (75 < d)
) T1
union all
select b, d
from (
Select b, d
from p1
where (99 > d)
) T2
) T1(c_l, b_l)
full join (
Select e, b, d
from p2
where (d < (b * e))
) T2(e_r, b_r, d_r)
on ((((b_l - e_r) + 81) = 10) OR ((c_l = e_r) OR ((c_l = (b_l + 22)) AND (b_l > b_l))))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test44exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_l, e_l_l, b_l_l, e_r, d_r
from (
Select e_l, c_l, b_l, d_r
from (
Select e, c, b, d
from p3
where (d > b)
) T1(e_l, c_l, b_l, d_l)
inner join (
Select b, d
from p4
where ((4 - 90) = 31)
) T2(b_r, d_r)
on ((36 > 3) OR (34 = d_r))
) T1(e_l_l, c_l_l, b_l_l, d_r_l)
full join (
Select e, c, d
from p1
where (b = a)
) T2(e_r, c_r, d_r)
on ((b_l_l < b_l_l) OR (72 < c_l_l))
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test44exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_r_l, b_l_l, e_r, a_r, b_r
from (
Select b_l, e_r, a_r
from (
Select b
from p3
where (a < a)
) T1(b_l)
inner join (
Select e, c, a
from p4
where (20 > 42)
) T2(e_r, c_r, a_r)
on ((21 - a_r) = e_r)
) T1(b_l_l, e_r_l, a_r_l)
full join (
Select e, a, b
from p5
where ((e > (98 - (a * (c + 15)))) AND ((b * a) = b))
) T2(e_r, a_r, b_r)
on ((68 - a_r) < e_r)
order by 1, 2, 3, 4, 5
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
Select e_l, a_l, e_r
from (
Select e, a
from p3
where (15 < d)
) T1(e_l, a_l)
full join (
Select e
from p5
where (b = (50 + 65))
) T2(e_r)
on ((a_l = 96) OR ((a_l = e_r) AND (((58 * 31) - 74) = (65 * 71))))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test44exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_l_l, d_l_l_l, e_r
from (
Select c_l_l, d_r_l, d_l_l, a_l_r, d_l_l_r_r
from (
Select c_l, d_l, d_r
from (
Select c, d
from p2
where (d = 16)
) T1(c_l, d_l)
left join (
Select e, c, a, d
from p5
where ((d + 69) = 39)
) T2(e_r, c_r, a_r, d_r)
on (68 < 37)
) T1(c_l_l, d_l_l, d_r_l)
left join (
Select a_l, d_l, d_l_l_r, d_l_r_l_r
from (
Select a, d
from p4
where ((((65 - (a - e)) + 53) < 55) AND ((16 < e) AND (((c - (c - 64)) * 92) = b)))
) T1(a_l, d_l)
inner join (
select d_l_r_l, d_l_l, e_r
from (
Select d_l_r_l, d_l_l, e_r, b_r
from (
Select d_l, d_l_r
from (
Select e, a, d
from p5
where ((59 * e) = b)
) T1(e_l, a_l, d_l)
left join (
Select b_l, d_l, c_r
from (
Select e, c, b, d
from p3
where ((98 > a) OR (42 = b))
) T1(e_l, c_l, b_l, d_l)
inner join (
Select c
from p5
where (((17 + a) < 97) OR (78 = a))
) T2(c_r)
on (d_l < d_l)
) T2(b_l_r, d_l_r, c_r_r)
on ((d_l_r * 42) > 29)
) T1(d_l_l, d_l_r_l)
full join (
Select e, c, b
from p5
where ((e - b) > d)
) T2(e_r, c_r, b_r)
on ((9 * 53) > e_r)
) T1
union all
select e, c, a
from (
Select e, c, a
from p5
where (a = d)
) T2
) T2(d_l_r_l_r, d_l_l_r, e_r_r)
on (a_l = 63)
) T2(a_l_r, d_l_r, d_l_l_r_r, d_l_r_l_r_r)
on ((d_l_l < a_l_r) AND (d_l_l_r_r = 77))
) T1(c_l_l_l, d_r_l_l, d_l_l_l, a_l_r_l, d_l_l_r_r_l)
inner join (
Select e
from p2
where ((a > a) OR (((63 - 63) + 33) < c))
) T2(e_r)
on (97 < 36)
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
Select a_l_l, a_r_r_l, e_l_l_l_r
from (
Select a_l, a_r_r
from (
Select a
from p3
where (((30 + 63) = (c * c)) OR (62 < c))
) T1(a_l)
left join (
Select a_l, c_r, a_r
from (
Select e, a
from p3
where (a < d)
) T1(e_l, a_l)
left join (
Select c, a, b, d
from p3
where (c > a)
) T2(c_r, a_r, b_r, d_r)
on (81 = (6 - 66))
) T2(a_l_r, c_r_r, a_r_r)
on ((96 = 56) AND ((a_r_r - a_l) > a_l))
) T1(a_l_l, a_r_r_l)
left join (
Select e_l_l_l, c_r
from (
Select e_l_l, c_r_l, b_l_l, c_l_r_r, b_l_l_r
from (
select e_l, b_l, c_r
from (
Select e_l, b_l, c_r
from (
Select e, c, b
from p5
where (c = 14)
) T1(e_l, c_l, b_l)
inner join (
Select c
from p4
where ((21 = a) AND (((b * a) = 28) OR (17 > d)))
) T2(c_r)
on ((0 < 85) AND (b_l < b_l))
) T1
union all
select b_l, c_r, d_r
from (
Select b_l, c_r, d_r
from (
Select c, b
from p5
where (68 = (((51 * 39) + a) * d))
) T1(c_l, b_l)
inner join (
Select e, c, d
from p3
where ((a > b) OR (c = 65))
) T2(e_r, c_r, d_r)
on ((b_l > d_r) OR ((93 - (d_r * 1)) = 47))
) T2
) T1(e_l_l, b_l_l, c_r_l)
inner join (
Select b_l_l, d_l_l, c_l_r, c_r_r
from (
select b_l, d_l, a_r
from (
Select b_l, d_l, a_r, b_r, d_r
from (
Select a, b, d
from p2
where (11 < e)
) T1(a_l, b_l, d_l)
left join (
Select a, b, d
from p2
where (a > (64 - 30))
) T2(a_r, b_r, d_r)
on (b_r = d_l)
) T1
union all
select c, a, d
from (
Select c, a, d
from p2
where ((d * 34) = (e + 23))
) T2
) T1(b_l_l, d_l_l, a_r_l)
left join (
Select c_l, d_l, c_r
from (
Select c, a, d
from p4
where (70 > (e * c))
) T1(c_l, a_l, d_l)
left join (
Select c
from p4
where (80 > c)
) T2(c_r)
on ((d_l - d_l) = 85)
) T2(c_l_r, d_l_r, c_r_r)
on ((11 > d_l_l) AND (9 = 81))
) T2(b_l_l_r, d_l_l_r, c_l_r_r, c_r_r_r)
on ((e_l_l + 14) = ((33 * c_l_r_r) - (e_l_l - (b_l_l_r * 18))))
) T1(e_l_l_l, c_r_l_l, b_l_l_l, c_l_r_r_l, b_l_l_r_l)
inner join (
Select c
from p2
where ((d = (b + e)) OR (15 < 22))
) T2(c_r)
on (e_l_l_l = 99)
) T2(e_l_l_l_r, c_r_r)
on ((63 + 53) = a_l_l)
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
Select a_l, c_r
from (
select c, a
from (
Select c, a
from p3
where (59 = a)
) T1
union all
select e_l, b_l
from (
Select e_l, b_l, b_r_r, a_r_r, d_l_r
from (
Select e, a, b
from p5
where ((a = (13 + 75)) OR (34 = 92))
) T1(e_l, a_l, b_l)
full join (
Select d_l, a_r, b_r
from (
Select b, d
from p3
where (d = (d * 65))
) T1(b_l, d_l)
left join (
Select a, b
from p4
where ((58 - a) > 2)
) T2(a_r, b_r)
on (12 < b_r)
) T2(d_l_r, a_r_r, b_r_r)
on (8 > d_l_r)
) T2
) T1(c_l, a_l)
inner join (
Select c, d
from p2
where (58 = 64)
) T2(c_r, d_r)
on ((80 * a_l) < a_l)
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
Select a_r_l, c_l_l_r_l_l, b_r_r, e_r_r_l_r
from (
Select c_l_l_r_l, a_r
from (
Select d_l, c_l_l_r
from (
Select d
from p3
where ((44 = 30) OR (b = d))
) T1(d_l)
left join (
select c_l_l, c_l_r_l
from (
Select c_l_l, c_l_r_l, b_r, d_r
from (
Select c_l, c_l_r
from (
Select c
from p5
where ((d = (d - 45)) OR (a < 9))
) T1(c_l)
inner join (
select e_l, c_l
from (
Select e_l, c_l, d_l, e_r, a_r
from (
Select e, c, d
from p1
where ((c = c) OR (((e * 74) * b) = e))
) T1(e_l, c_l, d_l)
inner join (
Select e, a
from p5
where (b = ((e + 70) - 58))
) T2(e_r, a_r)
on (c_l = e_r)
) T1
union all
select e, b
from (
select e, b
from (
Select e, b
from p4
where ((61 = a) OR ((e < 17) AND ((77 + 85) > b)))
) T1
union all
select b_l, d_r_r
from (
Select b_l, d_r_r, a_r_r, d_l_r
from (
Select e, c, b, d
from p4
where ((c > e) OR (49 > (d * 62)))
) T1(e_l, c_l, b_l, d_l)
inner join (
select d_l, a_r, d_r
from (
Select d_l, a_r, d_r
from (
Select d
from p3
where ((d = (a - 42)) OR (86 = (a - 54)))
) T1(d_l)
full join (
Select a, d
from p2
where ((a < 45) OR (b = (c + 88)))
) T2(a_r, d_r)
on (65 = d_l)
) T1
union all
select e_l, d_l, e_r_r
from (
Select e_l, d_l, e_r_r
from (
select e, d
from (
Select e, d
from p2
where (c < e)
) T1
union all
select e_l, c_r
from (
Select e_l, c_r, d_r
from (
Select e, b, d
from p5
where ((b = d) AND (14 < (78 - 59)))
) T1(e_l, b_l, d_l)
inner join (
select c, a, d
from (
Select c, a, d
from p2
where (70 = (1 - 36))
) T1
union all
select e, c, a
from (
Select e, c, a, b
from p5
where ((a - 66) > e)
) T2
) T2(c_r, a_r, d_r)
on (55 = c_r)
) T2
) T1(e_l, d_l)
full join (
Select a_l_r_r_r_l, e_r
from (
Select a_l_l, e_l_r, a_l_r_r_r
from (
select a_l
from (
select a_l
from (
Select a_l, d_l, b_r
from (
Select a, d
from p2
where (((d * d) * d) = 39)
) T1(a_l, d_l)
left join (
Select b
from p4
where ((46 - a) > (48 - a))
) T2(b_r)
on ((d_l < a_l) OR ((86 = 90) OR (((a_l + 29) * b_r) < (b_r * (b_r - 54)))))
) T1
union all
select d
from (
Select d
from p4
where (e = (66 * 77))
) T2
) T1
union all
select c
from (
Select c
from p2
where (60 = 26)
) T2
) T1(a_l_l)
left join (
select e_l, c_l, a_l_r_r
from (
Select e_l, c_l, a_l_r_r, c_l_r
from (
Select e, c
from p5
where ((c < b) AND (12 = (c - d)))
) T1(e_l, c_l)
full join (
Select c_l, a_l_r
from (
Select e, c
from p1
where (21 = 5)
) T1(e_l, c_l)
inner join (
select a_l
from (
Select a_l, c_r, d_r
from (
Select a
from p4
where ((c = e) AND ((68 = (45 * b)) OR ((29 = (a * a)) AND (e < 54))))
) T1(a_l)
full join (
Select e, c, d
from p2
where (32 < 94)
) T2(e_r, c_r, d_r)
on (21 < 74)
) T1
union all
select d
from (
select d
from (
Select d
from p3
where ((26 > 74) AND (((93 - a) < 98) OR (c = b)))
) T1
union all
select e_l
from (
Select e_l, d_l, e_r
from (
Select e, d
from p1
where (c < 10)
) T1(e_l, d_l)
full join (
Select e
from p1
where ((a > c) AND (c = e))
) T2(e_r)
on ((62 = (e_l - e_r)) OR (((e_r - 33) = 85) OR ((92 + 80) < (d_l + (82 * 4)))))
) T2
) T2
) T2(a_l_r)
on (c_l = a_l_r)
) T2(c_l_r, a_l_r_r)
on (38 < c_l)
) T1
union all
select b_l, d_r_r, d_l_r
from (
Select b_l, d_r_r, d_l_r
from (
Select e, b
from p4
where ((c * 33) = 48)
) T1(e_l, b_l)
full join (
Select b_l, d_l, d_r
from (
Select b, d
from p3
where ((14 = a) OR (b = d))
) T1(b_l, d_l)
left join (
select c, d
from (
Select c, d
from p3
where ((55 < d) AND (d < c))
) T1
union all
select c, a
from (
Select c, a, d
from p4
where (79 = 86)
) T2
) T2(c_r, d_r)
on ((d_r - 63) = 81)
) T2(b_l_r, d_l_r, d_r_r)
on (94 < d_r_r)
) T2
) T2(e_l_r, c_l_r, a_l_r_r_r)
on (((33 - 93) = a_l_r_r_r) AND (e_l_r = e_l_r))
) T1(a_l_l_l, e_l_r_l, a_l_r_r_r_l)
inner join (
Select e
from p4
where (37 = (c * (e - (68 * 88))))
) T2(e_r)
on (e_r = e_r)
) T2(a_l_r_r_r_l_r, e_r_r)
on (d_l < e_l)
) T2
) T2(d_l_r, a_r_r, d_r_r)
on (63 > 28)
) T2
) T2
) T2(e_l_r, c_l_r)
on (c_l_r = 50)
) T1(c_l_l, c_l_r_l)
inner join (
Select e, b, d
from p3
where (b = 7)
) T2(e_r, b_r, d_r)
on ((13 + c_l_l) > c_l_l)
) T1
union all
select a_r_l, a_r
from (
Select a_r_l, a_r
from (
Select a_r_l, d_l_l, a_r
from (
Select a_l, d_l, c_r, a_r
from (
Select c, a, d
from p2
where (39 = 78)
) T1(c_l, a_l, d_l)
full join (
Select e, c, a
from p5
where (((b + b) < 86) OR (94 > c))
) T2(e_r, c_r, a_r)
on (86 < d_l)
) T1(a_l_l, d_l_l, c_r_l, a_r_l)
inner join (
Select c, a, b
from p2
where ((((70 + 38) * a) = 68) OR ((d = b) AND (b = d)))
) T2(c_r, a_r, b_r)
on (a_r < 42)
) T1(a_r_l_l, d_l_l_l, a_r_l)
full join (
Select c, a, b
from p5
where ((19 = a) AND (((c + d) < a) OR ((66 < 22) OR (38 = c))))
) T2(c_r, a_r, b_r)
on (59 > a_r_l)
) T2
) T2(c_l_l_r, c_l_r_l_r)
on ((d_l < 17) AND (c_l_l_r = 82))
) T1(d_l_l, c_l_l_r_l)
left join (
Select a
from p4
where (51 > (a + e))
) T2(a_r)
on ((24 - a_r) = 99)
) T1(c_l_l_r_l_l, a_r_l)
full join (
Select e_l_l, e_r_r_l, b_r
from (
select e_l, b_l, e_r_r
from (
Select e_l, b_l, e_r_r
from (
Select e, b, d
from p5
where ((c = 7) OR (46 = 57))
) T1(e_l, b_l, d_l)
left join (
Select a_l, b_l, e_r, d_r
from (
Select a, b
from p4
where (33 > 28)
) T1(a_l, b_l)
left join (
Select e, d
from p3
where (a = 10)
) T2(e_r, d_r)
on ((97 + a_l) = 74)
) T2(a_l_r, b_l_r, e_r_r, d_r_r)
on (e_r_r = 76)
) T1
union all
select e_l_l, e_r_l, a_r_r
from (
select e_l_l, e_r_l, a_r_r
from (
select e_l_l, e_r_l, a_r_r
from (
Select e_l_l, e_r_l, a_r_r, b_l_r
from (
Select e_l, e_r, b_r
from (
Select e
from p1
where (20 = 1)
) T1(e_l)
inner join (
Select e, b
from p5
where (d > b)
) T2(e_r, b_r)
on (e_l > 85)
) T1(e_l_l, e_r_l, b_r_l)
inner join (
Select b_l, a_r
from (
Select b
from p1
where (65 > 37)
) T1(b_l)
left join (
Select a, b
from p5
where ((99 = (c - 69)) OR ((20 * a) = a))
) T2(a_r, b_r)
on (a_r > 52)
) T2(b_l_r, a_r_r)
on (25 > e_r_l)
) T1
union all
select e, b, d
from (
Select e, b, d
from p5
where ((59 < 72) AND (((58 - 50) > c) AND (27 = 63)))
) T2
) T1
union all
select a, b, d
from (
Select a, b, d
from p2
where (d < 77)
) T2
) T2
) T1(e_l_l, b_l_l, e_r_r_l)
left join (
Select b
from p1
where (((((45 * c) + e) * 6) * 67) = b)
) T2(b_r)
on (60 < 9)
) T2(e_l_l_r, e_r_r_l_r, b_r_r)
on ((72 < ((a_r_l * (3 - 7)) + c_l_l_r_l_l)) OR ((e_r_r_l_r = 5) OR ((b_r_r = c_l_l_r_l_l) AND ((((15 - 13) - 26) + b_r_r) = a_r_l))))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test44exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_l, e_r
from (
Select e, a, b
from p5
where (78 = a)
) T1(e_l, a_l, b_l)
full join (
Select e, d
from p4
where ((84 > ((b + 96) - 16)) OR ((25 > a) OR (2 > 47)))
) T2(e_r, d_r)
on (e_l = b_l)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test44exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, e_r
from (
Select e, c, d
from p5
where ((65 = c) OR (63 > 40))
) T1(e_l, c_l, d_l)
inner join (
Select e, d
from p3
where ((d = c) AND ((b = b) AND (e = c)))
) T2(e_r, d_r)
on (((e_r + e_l) = 75) AND (e_l < e_r))
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
Select c_l, d_l, b_r_r, e_l_r, b_l_r
from (
Select c, b, d
from p2
where ((51 = a) AND ((79 = c) AND ((76 > (5 * 71)) OR (5 = d))))
) T1(c_l, b_l, d_l)
left join (
Select e_l, b_l, e_r, b_r
from (
Select e, c, b
from p3
where (70 = 37)
) T1(e_l, c_l, b_l)
left join (
Select e, a, b
from p3
where ((e = e) OR (d = 69))
) T2(e_r, a_r, b_r)
on (19 = (98 - e_l))
) T2(e_l_r, b_l_r, e_r_r, b_r_r)
on (71 > 0)
order by 1, 2, 3, 4, 5
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
Select e_l_l, c_r_l, e_r
from (
select e_l, c_r
from (
Select e_l, c_r
from (
Select e
from p2
where ((d + b) = 41)
) T1(e_l)
left join (
Select c
from p4
where (62 = b)
) T2(c_r)
on (c_r > c_r)
) T1
union all
select b, d
from (
Select b, d
from p3
where ((b * 33) = e)
) T2
) T1(e_l_l, c_r_l)
inner join (
select e
from (
Select e, a, b
from p1
where ((33 * (73 + 16)) = b)
) T1
union all
select b
from (
Select b
from p5
where (94 = a)
) T2
) T2(e_r)
on (37 < e_l_l)
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
    #**********************
    _testmgr.testcase_end(desc)

