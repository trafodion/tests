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
    
def test001(desc="""Joins Set 20"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_l, a_r, b_r
from (
Select a, b, d
from p5
where ((((40 - (73 - c)) - d) = b) OR (4 > b))
) T1(a_l, b_l, d_l)
left join (
Select a, b
from p5
where (84 = 99)
) T2(a_r, b_r)
on (39 > b_l)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_l, c_r
from (
Select e, b
from p1
where ((63 = b) OR (a = e))
) T1(e_l, b_l)
full join (
Select c
from p3
where (a = d)
) T2(c_r)
on ((56 < e_l) OR (b_l = c_r))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, a_r, b_r
from (
Select e, a, b
from p2
where (e = 65)
) T1(e_l, a_l, b_l)
full join (
select a, b
from (
Select a, b
from p1
where (a = c)
) T1
union all
select e, c
from (
Select e, c, a, b
from p4
where (58 < a)
) T2
) T2(a_r, b_r)
on (3 = (a_r * a_r))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_l, d_r_r_l, a_r_r, b_l_r
from (
Select a_l, b_l, b_l_l_r, d_r_r, e_r_l_r
from (
Select c, a, b
from p4
where ((13 * 19) < a)
) T1(c_l, a_l, b_l)
left join (
Select d_r_l, e_r_l, b_l_l, d_r
from (
Select a_l, b_l, e_r, d_r
from (
select a, b
from (
Select a, b
from p4
where (((a + c) + 38) = b)
) T1
union all
select e_l, a_l
from (
Select e_l, a_l, b_r
from (
select e, a
from (
Select e, a, d
from p1
where (48 = 7)
) T1
union all
select a, d
from (
Select a, d
from p3
where (96 = a)
) T2
) T1(e_l, a_l)
full join (
Select a, b
from p2
where (e > 12)
) T2(a_r, b_r)
on (83 = b_r)
) T2
) T1(a_l, b_l)
inner join (
Select e, d
from p5
where (d < a)
) T2(e_r, d_r)
on (13 = 27)
) T1(a_l_l, b_l_l, e_r_l, d_r_l)
left join (
Select b, d
from p3
where (c > 65)
) T2(b_r, d_r)
on (45 > 28)
) T2(d_r_l_r, e_r_l_r, b_l_l_r, d_r_r)
on ((45 > d_r_r) AND (74 = 49))
) T1(a_l_l, b_l_l, b_l_l_r_l, d_r_r_l, e_r_l_r_l)
left join (
Select b_l, a_r, b_r
from (
Select a, b, d
from p4
where ((d = 1) OR ((d - (85 * d)) = 47))
) T1(a_l, b_l, d_l)
full join (
Select a, b
from p1
where ((45 > 97) AND (a = (39 * (b - 73))))
) T2(a_r, b_r)
on ((a_r = 50) AND (b_r = 28))
) T2(b_l_r, a_r_r, b_r_r)
on ((a_r_r - b_l_r) < 22)
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
Select a_l_l, d_r_l, d_r
from (
Select a_l, c_r, d_r
from (
Select a
from p2
where (c < b)
) T1(a_l)
inner join (
Select c, a, d
from p3
where (a = c)
) T2(c_r, a_r, d_r)
on (12 = 53)
) T1(a_l_l, c_r_l, d_r_l)
full join (
Select e, d
from p1
where (3 < b)
) T2(e_r, d_r)
on (71 < a_l_l)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_r_l, b_l_l, d_r_r, e_r_l_r
from (
Select b_l, a_l_r
from (
Select b
from p2
where (e > 54)
) T1(b_l)
left join (
Select c_l, a_l, e_r
from (
Select c, a
from p3
where (b = c)
) T1(c_l, a_l)
left join (
Select e, d
from p2
where (67 = 13)
) T2(e_r, d_r)
on (c_l > a_l)
) T2(c_l_r, a_l_r, e_r_r)
on (94 = a_l_r)
) T1(b_l_l, a_l_r_l)
left join (
Select e_r_l, d_r
from (
Select a_l, e_r, b_r
from (
Select e, a
from p5
where (d = 16)
) T1(e_l, a_l)
full join (
select e, b
from (
select e, b
from (
Select e, b, d
from p2
where (92 < e)
) T1
union all
select c_l, d_r
from (
Select c_l, d_r
from (
Select c, b
from p5
where (c = 70)
) T1(c_l, b_l)
left join (
Select d
from p1
where ((75 > (e * 64)) OR (c > (d + 44)))
) T2(d_r)
on (((81 + (45 + d_r)) + (c_l - d_r)) = d_r)
) T2
) T1
union all
select c, b
from (
Select c, b, d
from p5
where ((a - 53) > 5)
) T2
) T2(e_r, b_r)
on (e_r > a_l)
) T1(a_l_l, e_r_l, b_r_l)
left join (
select d
from (
select d
from (
Select d
from p1
where ((a + a) > 78)
) T1
union all
select a
from (
select a
from (
Select a
from p1
where ((e > a) OR (98 > 11))
) T1
union all
select e
from (
select e, c
from (
Select e, c
from p2
where ((27 = (2 - 9)) OR (81 = a))
) T1
union all
select e, c
from (
Select e, c, d
from p5
where ((((((a + 83) + (e * 25)) - e) + (90 * ((9 - 67) - b))) - (28 * e)) = (51 - (19 - a)))
) T2
) T2
) T2
) T1
union all
select e
from (
Select e, a
from p2
where (c = a)
) T2
) T2(d_r)
on ((98 < 51) OR ((16 = d_r) AND (e_r_l < 55)))
) T2(e_r_l_r, d_r_r)
on (a_l_r_l = 36)
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
Select e_l, d_l, a_l_l_r, a_l_r_r_r
from (
select e, d
from (
select e, d
from (
Select e, d
from p5
where (94 = e)
) T1
union all
select a, b
from (
Select a, b, d
from p1
where (b < 82)
) T2
) T1
union all
select d_r_l, a_r_l
from (
Select d_r_l, a_r_l, c_r_l_r, c_r_r
from (
Select b_r_r_l, a_r, d_r
from (
Select e_l, d_l, b_r_r
from (
Select e, d
from p2
where ((68 > a) OR ((d > 56) AND (79 = 94)))
) T1(e_l, d_l)
inner join (
Select e_l_l, a_r_l, e_r, b_r
from (
Select e_l, a_r, d_r
from (
select e, b
from (
Select e, b
from p1
where (57 = (e - 24))
) T1
union all
select a, b
from (
Select a, b, d
from p2
where ((d > e) OR ((e * e) = d))
) T2
) T1(e_l, b_l)
full join (
Select e, a, d
from p3
where (67 < c)
) T2(e_r, a_r, d_r)
on (52 = (5 + d_r))
) T1(e_l_l, a_r_l, d_r_l)
left join (
Select e, a, b
from p5
where (a < 48)
) T2(e_r, a_r, b_r)
on (e_r = e_r)
) T2(e_l_l_r, a_r_l_r, e_r_r, b_r_r)
on ((98 - e_l) = ((d_l - 48) + b_r_r))
) T1(e_l_l, d_l_l, b_r_r_l)
left join (
Select e, a, d
from p3
where (27 = 91)
) T2(e_r, a_r, d_r)
on ((d_r + (b_r_r_l * b_r_r_l)) < 59)
) T1(b_r_r_l_l, a_r_l, d_r_l)
left join (
Select c_r_l, c_r
from (
Select e_l, c_r
from (
Select e, a, d
from p5
where (c > c)
) T1(e_l, a_l, d_l)
left join (
select c
from (
Select c, b
from p5
where ((35 = 69) OR (((46 - (b - 44)) < a) AND ((b = b) AND ((32 = c) AND ((87 + (33 + 74)) < 31)))))
) T1
union all
select e
from (
Select e
from p1
where (d = 47)
) T2
) T2(c_r)
on ((c_r + e_l) > 2)
) T1(e_l_l, c_r_l)
inner join (
Select c, a, b
from p2
where (d = a)
) T2(c_r, a_r, b_r)
on ((37 = c_r) OR (c_r_l = (c_r_l + 88)))
) T2(c_r_l_r, c_r_r)
on (d_r_l > c_r_r)
) T2
) T1(e_l, d_l)
left join (
Select a_l_l, a_l_r_r, e_l_r
from (
Select a_l, a_r
from (
select a
from (
Select a, b
from p2
where (c = e)
) T1
union all
select e
from (
Select e
from p5
where (c = e)
) T2
) T1(a_l)
inner join (
Select a
from p2
where (42 = e)
) T2(a_r)
on ((a_r > 55) AND (((86 - a_l) = a_r) AND (a_l = 88)))
) T1(a_l_l, a_r_l)
full join (
Select e_l, a_l_r, b_r_r
from (
Select e, a, d
from p5
where ((c = ((c - (86 - a)) * 99)) OR ((b > a) AND ((d * e) < 92)))
) T1(e_l, a_l, d_l)
full join (
Select a_l, d_l, a_r, b_r
from (
Select a, d
from p5
where (d = 76)
) T1(a_l, d_l)
inner join (
Select e, a, b
from p2
where (((85 + 25) = 47) AND (91 = (99 - d)))
) T2(e_r, a_r, b_r)
on (17 = 23)
) T2(a_l_r, d_l_r, a_r_r, b_r_r)
on (50 = 89)
) T2(e_l_r, a_l_r_r, b_r_r_r)
on ((12 = e_l_r) OR (a_l_l = (47 * e_l_r)))
) T2(a_l_l_r, a_l_r_r_r, e_l_r_r)
on (a_l_r_r_r < (36 * 82))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_l, e_l_l_l, a_l_r, a_r_r, d_l_r
from (
select e_l_l, e_r_l, e_r, b_r
from (
Select e_l_l, e_r_l, e_r, b_r
from (
select e_l, e_r
from (
Select e_l, e_r
from (
Select e
from p3
where ((b = d) OR (61 = b))
) T1(e_l)
left join (
Select e, c
from p2
where ((b + 93) = d)
) T2(e_r, c_r)
on ((e_l > (e_l * e_l)) AND ((((((53 + e_l) + e_l) * (8 + e_r)) + 65) = 98) AND (81 = e_r)))
) T1
union all
select a_l, d_r
from (
Select a_l, d_r
from (
Select c, a
from p5
where (23 < 45)
) T1(c_l, a_l)
inner join (
select c, d
from (
Select c, d
from p1
where ((a = b) OR (c < 29))
) T1
union all
select e, a
from (
Select e, a
from p1
where (29 = a)
) T2
) T2(c_r, d_r)
on (d_r > (a_l + (a_l * (d_r + 87))))
) T2
) T1(e_l_l, e_r_l)
full join (
select e, b
from (
Select e, b
from p2
where ((d < (e + (e * 7))) AND (e > 24))
) T1
union all
select e, d
from (
Select e, d
from p2
where (92 > d)
) T2
) T2(e_r, b_r)
on ((e_r = e_l_l) OR (21 = 75))
) T1
union all
select e_l, d_l, e_r, d_r
from (
Select e_l, d_l, e_r, d_r
from (
Select e, b, d
from p3
where ((6 * 43) > 99)
) T1(e_l, b_l, d_l)
left join (
select e, d
from (
Select e, d
from p2
where (a < 89)
) T1
union all
select c, a
from (
Select c, a
from p3
where ((a - d) = (84 * b))
) T2
) T2(e_r, d_r)
on (d_r > 34)
) T2
) T1(e_l_l_l, e_r_l_l, e_r_l, b_r_l)
inner join (
Select a_l, d_l, a_r, d_r
from (
select a, b, d
from (
Select a, b, d
from p4
where (d < (a - e))
) T1
union all
select a, b, d
from (
Select a, b, d
from p1
where (90 > b)
) T2
) T1(a_l, b_l, d_l)
left join (
Select c, a, d
from p3
where (e < ((22 + 85) - a))
) T2(c_r, a_r, d_r)
on ((85 - d_r) < a_l)
) T2(a_l_r, d_l_r, a_r_r, d_r_r)
on ((40 < (a_l_r + (18 - 62))) OR ((7 = d_l_r) OR (49 < d_l_r)))
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
Select b_l, a_l_r, a_r_r
from (
Select c, b
from p1
where (((d - b) * 22) = (66 * e))
) T1(c_l, b_l)
left join (
Select a_l, c_r, a_r
from (
Select e, a, b
from p2
where ((b = (d - d)) OR (c = e))
) T1(e_l, a_l, b_l)
full join (
Select c, a
from p3
where (0 = 71)
) T2(c_r, a_r)
on (37 > a_l)
) T2(a_l_r, c_r_r, a_r_r)
on (b_l = 24)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_r_l_l, a_r
from (
select b_r_r_l
from (
Select b_r_r_l, e_r, b_r
from (
Select b_l, b_r_r, c_l_r
from (
Select a, b
from p2
where ((99 + 70) < 32)
) T1(a_l, b_l)
full join (
Select c_l, c_r, b_r
from (
select c
from (
Select c, b, d
from p1
where (((e + a) - 48) < 79)
) T1
union all
select a
from (
Select a
from p4
where (((a + d) = 14) OR ((56 = 11) AND ((((32 * 53) + 99) - c) > c)))
) T2
) T1(c_l)
left join (
Select c, b
from p1
where (c = (d - c))
) T2(c_r, b_r)
on ((c_r = (26 + c_l)) AND ((b_r - 81) = 43))
) T2(c_l_r, c_r_r, b_r_r)
on (c_l_r = 76)
) T1(b_l_l, b_r_r_l, c_l_r_l)
full join (
Select e, b
from p2
where (97 < 75)
) T2(e_r, b_r)
on ((53 = b_r_r_l) OR (b_r_r_l < 99))
) T1
union all
select b
from (
Select b
from p3
where (d < a)
) T2
) T1(b_r_r_l_l)
left join (
Select a, b
from p4
where ((33 = a) OR ((d = (c + c)) AND ((86 * (72 + 83)) < 75)))
) T2(a_r, b_r)
on (a_r > 37)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, b_r, d_r
from (
Select b, d
from p1
where ((2 = (e + b)) AND (((c * e) * e) > (58 + 74)))
) T1(b_l, d_l)
left join (
Select b, d
from p4
where ((c > 59) OR ((b < 71) OR (c < 88)))
) T2(b_r, d_r)
on (b_r > b_r)
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
Select c_l, c_r, b_r
from (
Select c, a
from p4
where (62 = b)
) T1(c_l, a_l)
left join (
Select c, b
from p5
where (c = (15 + 27))
) T2(c_r, b_r)
on ((b_r < 99) AND ((c_l > b_r) OR (c_l = 13)))
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
Select a_l, c_r, a_r, d_r
from (
Select e, c, a
from p3
where (50 > c)
) T1(e_l, c_l, a_l)
left join (
Select c, a, d
from p3
where ((72 = c) AND (35 = 24))
) T2(c_r, a_r, d_r)
on ((d_r < 41) OR (a_l = (91 - 56)))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l_r_l, c_l_l, c_l_r_l, a_r
from (
Select c_l, c_l_r, b_l_r
from (
select c
from (
Select c, d
from p2
where (d = (80 * ((a * 58) * (((19 + 73) - (e + d)) - 60))))
) T1
union all
select a
from (
Select a
from p3
where ((48 * 67) = b)
) T2
) T1(c_l)
left join (
Select c_l, b_l, e_r
from (
Select c, b
from p1
where (55 < 20)
) T1(c_l, b_l)
full join (
select e
from (
Select e
from p4
where ((97 > 92) OR ((b > 21) AND ((a > b) OR (88 > d))))
) T1
union all
select e
from (
select e
from (
Select e, d
from p4
where (((e - 53) - e) > c)
) T1
union all
select e
from (
Select e
from p5
where ((e = a) OR ((c * (58 * (75 * 53))) > e))
) T2
) T2
) T2(e_r)
on ((44 = 95) OR ((c_l > 36) AND (c_l = c_l)))
) T2(c_l_r, b_l_r, e_r_r)
on ((3 = c_l) OR ((69 > (44 + ((29 - c_l) + 82))) AND (27 > b_l_r)))
) T1(c_l_l, c_l_r_l, b_l_r_l)
left join (
Select c, a
from p3
where (7 = (12 * 75))
) T2(c_r, a_r)
on (c_l_r_l > (b_l_r_l * 79))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, e_r
from (
Select e, b, d
from p2
where (d > (81 + 91))
) T1(e_l, b_l, d_l)
inner join (
Select e, a, b, d
from p2
where (e < a)
) T2(e_r, a_r, b_r, d_r)
on (e_r > 25)
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
Select e_l, a_r
from (
Select e, b, d
from p2
where (6 < 89)
) T1(e_l, b_l, d_l)
inner join (
Select c, a
from p4
where (((74 - (87 * e)) < a) OR (96 > e))
) T2(c_r, a_r)
on ((e_l = 12) AND (a_r > e_l))
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
Select b_l, d_l, e_r, c_r
from (
select b, d
from (
Select b, d
from p4
where (69 > 42)
) T1
union all
select e, b
from (
Select e, b, d
from p1
where (c = (((c + e) + 69) * (40 + 25)))
) T2
) T1(b_l, d_l)
full join (
select e, c
from (
Select e, c
from p1
where (c < c)
) T1
union all
select e, c
from (
Select e, c, b
from p3
where (a = b)
) T2
) T2(e_r, c_r)
on (90 > 48)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, c_r, d_r
from (
select a
from (
Select a
from p1
where (c = d)
) T1
union all
select a
from (
select a, b
from (
Select a, b
from p4
where ((57 + 16) > e)
) T1
union all
select e_l, d_r
from (
Select e_l, d_r
from (
Select e, a
from p2
where (41 = 11)
) T1(e_l, a_l)
left join (
Select d
from p4
where ((d > e) OR (94 > d))
) T2(d_r)
on (6 > e_l)
) T2
) T2
) T1(a_l)
left join (
Select c, a, d
from p5
where ((a + a) = 8)
) T2(c_r, a_r, d_r)
on (c_r = 1)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_r_l_l, e_r
from (
select c_l_r_l, e_l_l, e_r
from (
Select c_l_r_l, e_l_l, e_r
from (
Select e_l, c_l_r
from (
Select e
from p2
where ((92 > 22) AND ((e = a) OR (47 = ((a + d) * e))))
) T1(e_l)
left join (
select c_l, b_l
from (
Select c_l, b_l, d_l, a_r, d_r
from (
Select c, b, d
from p4
where (b < c)
) T1(c_l, b_l, d_l)
inner join (
Select c, a, d
from p4
where ((((a + 1) + e) > 27) AND (e < b))
) T2(c_r, a_r, d_r)
on (b_l < d_l)
) T1
union all
select c, d
from (
Select c, d
from p2
where ((c > e) OR (b = ((d * (b - e)) * e)))
) T2
) T2(c_l_r, b_l_r)
on (((e_l - c_l_r) > 97) AND (97 < 87))
) T1(e_l_l, c_l_r_l)
full join (
Select e
from p1
where (7 = (a - c))
) T2(e_r)
on (((e_r - 41) - 93) = 64)
) T1
union all
select e, c, a
from (
Select e, c, a, d
from p4
where (d = b)
) T2
) T1(c_l_r_l_l, e_l_l_l, e_r_l)
full join (
select e
from (
Select e, c
from p4
where (a > 9)
) T1
union all
select a
from (
Select a
from p4
where ((c = 12) OR ((b = 27) AND (e = 54)))
) T2
) T2(e_r)
on (25 = (e_r - e_r))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, d_r
from (
select c
from (
Select c, a, d
from p2
where (e = e)
) T1
union all
select e
from (
Select e
from p3
where (d = a)
) T2
) T1(c_l)
full join (
Select d
from p3
where (40 = 0)
) T2(d_r)
on (50 < 93)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

