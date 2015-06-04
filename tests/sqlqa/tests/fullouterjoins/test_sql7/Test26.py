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
    
def test001(desc="""Joins Set 26"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_r_l, c_r_l, b_l_l, d_l_r
from (
Select b_l, d_l, c_r, a_r
from (
Select b, d
from p2
where ((c < d) OR ((((a * a) + d) < a) AND ((b = 96) AND ((b * 16) > 10))))
) T1(b_l, d_l)
left join (
Select c, a
from p3
where ((7 < 55) OR (c > (a * b)))
) T2(c_r, a_r)
on (((c_r - 78) * 9) < 32)
) T1(b_l_l, d_l_l, c_r_l, a_r_l)
left join (
Select d_l, e_r
from (
Select b, d
from p1
where ((e - ((d + a) + 11)) = ((58 + (b - 47)) + b))
) T1(b_l, d_l)
inner join (
Select e
from p4
where (((85 - 7) + 45) = (((82 + ((b + 83) * 69)) - (53 * d)) - 35))
) T2(e_r)
on (d_l = e_r)
) T2(d_l_r, e_r_r)
on (22 < 16)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, e_r
from (
Select e
from p2
where (b < 13)
) T1(e_l)
full join (
Select e, b
from p5
where (a > a)
) T2(e_r, b_r)
on ((e_r = e_l) AND ((31 = e_r) OR (66 = 9)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l_l, a_r
from (
Select d_l, b_r
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
from p4
where (75 = 75)
) T1
union all
select c
from (
Select c
from p1
where (e = 92)
) T2
) T1
union all
select e
from (
Select e, a
from p2
where (62 = 13)
) T2
) T1
union all
select e_l
from (
Select e_l, b_l, d_r
from (
Select e, b
from p4
where (d = 85)
) T1(e_l, b_l)
left join (
Select b, d
from p1
where ((94 > (a - (d * 62))) AND (14 > 51))
) T2(b_r, d_r)
on ((d_r = b_l) AND (e_l > d_r))
) T2
) T1
union all
select e
from (
Select e, b, d
from p5
where (e = 5)
) T2
) T1(d_l)
full join (
Select b
from p3
where ((c - c) = a)
) T2(b_r)
on (d_l > d_l)
) T1(d_l_l, b_r_l)
left join (
select a
from (
Select a
from p4
where (a < c)
) T1
union all
select b
from (
Select b, d
from p3
where (96 = (5 * d))
) T2
) T2(a_r)
on (a_r < d_l_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, d_r
from (
Select c, b, d
from p1
where ((37 - 17) = a)
) T1(c_l, b_l, d_l)
left join (
Select d
from p5
where (10 > (d - a))
) T2(d_r)
on (d_r < 40)
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
Select c_r_l, b_l_l, d_l_l, c_l_r_r, a_l_l_r
from (
Select b_l, d_l, c_r
from (
Select a, b, d
from p3
where (a > b)
) T1(a_l, b_l, d_l)
left join (
Select c
from p4
where (a = a)
) T2(c_r)
on (d_l < 12)
) T1(b_l_l, d_l_l, c_r_l)
left join (
Select a_l_l, c_l_r, e_l_r
from (
Select a_l, b_r_r
from (
Select e, a, b
from p4
where ((b - (a + e)) < 35)
) T1(e_l, a_l, b_l)
full join (
Select b_l, b_r
from (
Select b
from p4
where (65 < (b - a))
) T1(b_l)
full join (
Select b
from p4
where (29 = d)
) T2(b_r)
on ((b_l - 67) > (81 - 49))
) T2(b_l_r, b_r_r)
on ((37 < b_r_r) AND (b_r_r = 87))
) T1(a_l_l, b_r_r_l)
left join (
select e_l, c_l
from (
Select e_l, c_l, d_l, c_r, d_r
from (
Select e, c, d
from p3
where (20 = 7)
) T1(e_l, c_l, d_l)
left join (
Select c, d
from p1
where (79 = 96)
) T2(c_r, d_r)
on (c_r > 18)
) T1
union all
select a, b
from (
Select a, b
from p5
where (8 = ((31 + d) + 14))
) T2
) T2(e_l_r, c_l_r)
on ((a_l_l + e_l_r) = e_l_r)
) T2(a_l_l_r, c_l_r_r, e_l_r_r)
on (85 < 34)
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
Select b_l, c_r, d_r
from (
Select b
from p4
where (e = d)
) T1(b_l)
left join (
Select c, d
from p1
where (((11 + c) = 90) OR (e > d))
) T2(c_r, d_r)
on (c_r > d_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_r_r, b_l_r
from (
select a
from (
select a
from (
Select a
from p3
where ((47 = 61) OR ((e < (10 * a)) AND (((10 - c) = (57 * a)) OR (56 = c))))
) T1
union all
select b
from (
Select b
from p5
where ((a * 90) < ((35 - (((86 - c) + ((b * b) + 62)) * (e + 48))) + 64))
) T2
) T1
union all
select d
from (
Select d
from p4
where (20 < 47)
) T2
) T1(a_l)
left join (
Select b_l, c_r, d_r
from (
Select b
from p1
where (e < 84)
) T1(b_l)
left join (
Select c, d
from p1
where ((15 = 92) AND ((b - (b + (b * 24))) < 93))
) T2(c_r, d_r)
on (49 = (9 - (d_r + 86)))
) T2(b_l_r, c_r_r, d_r_r)
on (b_l_r = (b_l_r + 99))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, d_l, b_r
from (
Select c, d
from p3
where ((45 + e) > (91 - e))
) T1(c_l, d_l)
inner join (
Select b
from p4
where (e > 94)
) T2(b_r)
on (94 = 68)
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
Select c_r_l, d_l_l, c_l_r
from (
Select d_l, c_r
from (
Select d
from p2
where ((a > 98) AND ((5 = b) AND (39 = 50)))
) T1(d_l)
left join (
Select c
from p5
where (b = 24)
) T2(c_r)
on (79 = ((d_l + d_l) + (25 * d_l)))
) T1(d_l_l, c_r_l)
full join (
select c_l
from (
Select c_l, d_l, a_r_r_r_r, e_r_r_l_r_l_l_r_r
from (
Select c, d
from p5
where (d < c)
) T1(c_l, d_l)
left join (
Select d_l_l, a_r_r_r, e_r_r_l_r_l_l_r
from (
Select d_l, a_r
from (
Select c, d
from p5
where ((d + b) = e)
) T1(c_l, d_l)
left join (
Select a
from p4
where (d > b)
) T2(a_r)
on ((a_r + 39) = (a_r - 8))
) T1(d_l_l, a_r_l)
inner join (
Select e_r_r_l_r_l_l, a_r_r
from (
Select e_r_r_l_r_l, a_r
from (
Select e_l, c_l, e_r_r_l_r
from (
Select e, c, b
from p5
where (b = 47)
) T1(e_l, c_l, b_l)
full join (
Select c_l_l_l, c_r_l_r_l, e_r_r_l, b_r
from (
Select c_l_l, c_l_l_r_l, c_r_l_r, e_r_r
from (
Select c_l, c_l_l_r, b_r_l_r
from (
Select c
from p4
where (a = c)
) T1(c_l)
full join (
Select c_l_l, b_r_l, b_l_l, b_r
from (
select c_l, b_l, b_r
from (
select c_l, b_l, b_r
from (
Select c_l, b_l, b_r
from (
Select c, b
from p1
where ((d = 71) OR ((51 - c) = 65))
) T1(c_l, b_l)
left join (
Select b
from p5
where ((a > e) AND (95 > 24))
) T2(b_r)
on (b_l > 35)
) T1
union all
select a_l_l, c_r_l, d_r
from (
Select a_l_l, c_r_l, d_r
from (
Select a_l, c_r
from (
select a
from (
Select a
from p1
where (20 = d)
) T1
union all
select b
from (
select b, d
from (
Select b, d
from p3
where (d > ((((43 + 56) - a) * 36) - b))
) T1
union all
select c, b
from (
Select c, b
from p2
where (a < 81)
) T2
) T2
) T1(a_l)
inner join (
Select c
from p5
where (a < a)
) T2(c_r)
on ((83 < a_l) OR (c_r > a_l))
) T1(a_l_l, c_r_l)
left join (
Select d
from p2
where ((d > (a + 44)) AND (((c + c) = d) AND (84 < 85)))
) T2(d_r)
on ((6 * d_r) = 63)
) T2
) T1
union all
select e, c, d
from (
Select e, c, d
from p5
where ((a = a) OR (e < 61))
) T2
) T1(c_l_l, b_l_l, b_r_l)
full join (
Select b
from p1
where (e < 6)
) T2(b_r)
on (b_r < 85)
) T2(c_l_l_r, b_r_l_r, b_l_l_r, b_r_r)
on ((c_l_l_r = 9) OR (45 > 22))
) T1(c_l_l, c_l_l_r_l, b_r_l_r_l)
left join (
Select c_r_l, e_r
from (
Select c_l, e_r, c_r
from (
select e, c
from (
Select e, c
from p4
where ((d < a) OR (d = (34 - a)))
) T1
union all
select d_r_l, c_r
from (
Select d_r_l, c_r
from (
Select e_r_l_l, e_l_r_l, d_r
from (
Select c_l_l, e_r_l, e_l_r
from (
select c_l, e_r
from (
Select c_l, e_r
from (
Select c
from p1
where (64 < b)
) T1(c_l)
full join (
select e
from (
Select e
from p2
where (68 < (50 - d))
) T1
union all
select a
from (
Select a, b
from p3
where ((91 + 37) < d)
) T2
) T2(e_r)
on (e_r = 96)
) T1
union all
select a_l, b_l
from (
Select a_l, b_l, a_r
from (
Select a, b
from p2
where ((42 = c) AND ((16 < b) AND (d > 89)))
) T1(a_l, b_l)
full join (
Select a
from p3
where (99 < 56)
) T2(a_r)
on (24 > 80)
) T2
) T1(c_l_l, e_r_l)
left join (
Select e_l, b_l, b_r_r
from (
Select e, b
from p5
where ((67 * a) < 41)
) T1(e_l, b_l)
left join (
select b_l, b_r
from (
Select b_l, b_r
from (
Select b
from p1
where ((c > c) OR (a = 11))
) T1(b_l)
left join (
Select b
from p1
where (a < d)
) T2(b_r)
on (8 = (28 - 36))
) T1
union all
select c, a
from (
Select c, a, b, d
from p1
where ((77 = a) AND ((e + 48) = c))
) T2
) T2(b_l_r, b_r_r)
on ((81 > e_l) AND ((b_r_r * 75) < (44 - (80 * (e_l * 50)))))
) T2(e_l_r, b_l_r, b_r_r_r)
on (e_r_l < (e_l_r - 81))
) T1(c_l_l_l, e_r_l_l, e_l_r_l)
full join (
Select e, c, d
from p5
where ((4 < (c * a)) OR (40 > c))
) T2(e_r, c_r, d_r)
on (d_r < (46 * (63 + e_r_l_l)))
) T1(e_r_l_l_l, e_l_r_l_l, d_r_l)
full join (
select c
from (
Select c
from p3
where (b > 39)
) T1
union all
select e
from (
Select e, c, b
from p3
where ((34 > 12) OR (67 > (c * c)))
) T2
) T2(c_r)
on (((d_r_l + d_r_l) = 26) AND (d_r_l > 75))
) T2
) T1(e_l, c_l)
inner join (
Select e, c
from p2
where (17 > 65)
) T2(e_r, c_r)
on ((90 = (((33 - c_l) + 46) - 75)) OR (45 = c_l))
) T1(c_l_l, e_r_l, c_r_l)
inner join (
Select e, c
from p3
where ((c > 86) OR (d > ((e - (82 - 11)) + c)))
) T2(e_r, c_r)
on (((c_r_l * e_r) * e_r) = (e_r - 93))
) T2(c_r_l_r, e_r_r)
on (c_l_l = 51)
) T1(c_l_l_l, c_l_l_r_l_l, c_r_l_r_l, e_r_r_l)
left join (
select b
from (
Select b
from p3
where (b < a)
) T1
union all
select c
from (
Select c, a
from p5
where (e > b)
) T2
) T2(b_r)
on (62 < 28)
) T2(c_l_l_l_r, c_r_l_r_l_r, e_r_r_l_r, b_r_r)
on (e_l = 1)
) T1(e_l_l, c_l_l, e_r_r_l_r_l)
left join (
Select a
from p4
where (2 = a)
) T2(a_r)
on (70 = ((a_r + (51 + e_r_r_l_r_l)) + 31))
) T1(e_r_r_l_r_l_l, a_r_l)
full join (
Select c_l_l, e_r, a_r
from (
Select c_l, c_r, a_r
from (
Select c
from p2
where ((a * (c + e)) = (20 + c))
) T1(c_l)
full join (
Select c, a, b, d
from p1
where (67 = b)
) T2(c_r, a_r, b_r, d_r)
on (c_r = 44)
) T1(c_l_l, c_r_l, a_r_l)
full join (
Select e, a
from p1
where ((a = c) AND ((c * c) = a))
) T2(e_r, a_r)
on (12 = 94)
) T2(c_l_l_r, e_r_r, a_r_r)
on ((a_r_r > 94) OR ((e_r_r_l_r_l_l = a_r_r) OR (e_r_r_l_r_l_l = a_r_r)))
) T2(e_r_r_l_r_l_l_r, a_r_r_r)
on ((55 < (d_l_l + (d_l_l + e_r_r_l_r_l_l_r))) OR (84 > 44))
) T2(d_l_l_r, a_r_r_r_r, e_r_r_l_r_l_l_r_r)
on ((44 - (71 - 70)) = d_l)
) T1
union all
select b
from (
Select b
from p5
where ((b = 97) OR (b = a))
) T2
) T2(c_l_r)
on (7 = 99)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, e_r
from (
Select e, b, d
from p4
where (e = 45)
) T1(e_l, b_l, d_l)
left join (
Select e
from p5
where (20 = e)
) T2(e_r)
on ((e_r < 49) OR ((64 * 96) > (b_l + e_r)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_r_r_l, d_r_l_l, e_r
from (
Select d_r_l, c_r_r
from (
Select c_l, a_r, d_r
from (
Select c, b
from p1
where (47 < d)
) T1(c_l, b_l)
left join (
Select e, a, d
from p1
where (e > ((1 + b) * d))
) T2(e_r, a_r, d_r)
on (46 > a_r)
) T1(c_l_l, a_r_l, d_r_l)
left join (
Select d_l_l, c_r
from (
Select d_l, b_r
from (
Select d
from p5
where (39 = (d + b))
) T1(d_l)
inner join (
Select e, b, d
from p1
where (52 < 33)
) T2(e_r, b_r, d_r)
on (4 < 29)
) T1(d_l_l, b_r_l)
inner join (
Select c, a
from p3
where (89 < e)
) T2(c_r, a_r)
on ((d_l_l - d_l_l) = 13)
) T2(d_l_l_r, c_r_r)
on (((c_r_r - d_r_l) * d_r_l) > d_r_l)
) T1(d_r_l_l, c_r_r_l)
full join (
Select e, c, d
from p3
where ((c = c) OR ((e + d) > (d - 51)))
) T2(e_r, c_r, d_r)
on ((c_r_r_l > 96) AND ((53 = d_r_l_l) AND ((d_r_l_l + 83) = e_r)))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, e_r
from (
Select e, b, d
from p4
where (c < 64)
) T1(e_l, b_l, d_l)
left join (
Select e
from p4
where (76 < 10)
) T2(e_r)
on ((91 - e_r) > (41 * 70))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, e_r
from (
Select e, a, b
from p2
where ((a = 78) OR (8 < 27))
) T1(e_l, a_l, b_l)
full join (
Select e, a
from p1
where (83 = (b - 65))
) T2(e_r, a_r)
on (b_l = 73)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_r_l, c_r_l, c_r
from (
Select a_l, c_r, a_r
from (
Select a
from p5
where (d = 99)
) T1(a_l)
full join (
Select c, a
from p1
where ((b = (b - ((63 - 18) + b))) AND ((5 + (b + (a + 29))) > a))
) T2(c_r, a_r)
on ((c_r = a_r) AND ((((16 + 46) * a_l) = c_r) AND (a_r = c_r)))
) T1(a_l_l, c_r_l, a_r_l)
inner join (
select c
from (
Select c, a
from p4
where ((7 = (e - a)) AND (69 < b))
) T1
union all
select d
from (
Select d
from p2
where (14 = c)
) T2
) T2(c_r)
on (a_r_l = 56)
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
Select c_l, a_l, e_r, c_r
from (
Select c, a, b
from p3
where ((c + a) > c)
) T1(c_l, a_l, b_l)
inner join (
select e, c
from (
Select e, c, b, d
from p4
where ((8 < e) AND ((e = 13) OR (d < ((d - c) - (e * d)))))
) T1
union all
select e, d
from (
Select e, d
from p4
where ((b < 5) AND ((7 = d) AND ((13 < b) OR (60 = 47))))
) T2
) T2(e_r, c_r)
on (c_r > 53)
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
Select b_l_l, e_r_l, a_r, b_r
from (
Select e_l, b_l, e_r
from (
Select e, a, b
from p5
where (29 = c)
) T1(e_l, a_l, b_l)
inner join (
Select e
from p1
where (((20 + d) = d) AND ((8 < 83) OR ((c = 32) OR ((c * 11) = 0))))
) T2(e_r)
on ((e_l = 79) OR ((e_r > b_l) AND (58 = 80)))
) T1(e_l_l, b_l_l, e_r_l)
inner join (
Select c, a, b
from p1
where (e = ((e * c) + d))
) T2(c_r, a_r, b_r)
on (a_r < 43)
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
Select d_l, b_r
from (
Select e, c, d
from p1
where (87 = 14)
) T1(e_l, c_l, d_l)
left join (
Select b
from p4
where ((c = 84) OR ((40 > 33) OR ((13 < ((58 - ((d * b) - e)) - c)) OR (b = d))))
) T2(b_r)
on (40 = 60)
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
Select e_l, e_r, a_r
from (
Select e, a, b, d
from p1
where ((d + d) > a)
) T1(e_l, a_l, b_l, d_l)
left join (
select e, a
from (
select e, a
from (
Select e, a
from p5
where ((31 > 42) OR (d = (a + a)))
) T1
union all
select e, c
from (
Select e, c, b, d
from p2
where (99 = ((74 + a) * d))
) T2
) T1
union all
select e, b
from (
Select e, b, d
from p2
where (71 < 73)
) T2
) T2(e_r, a_r)
on (a_r < (e_l * 32))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_l, e_r, b_r
from (
Select e, b, d
from p1
where (((a - e) < c) OR (25 > 45))
) T1(e_l, b_l, d_l)
left join (
select e, b
from (
select e, b
from (
Select e, b, d
from p3
where ((d = 75) OR (((a * 77) - 24) = e))
) T1
union all
select b, d
from (
Select b, d
from p1
where (((c - d) - 63) < 30)
) T2
) T1
union all
select e_l, b_l
from (
Select e_l, b_l, e_r
from (
Select e, b
from p4
where (81 > b)
) T1(e_l, b_l)
left join (
Select e
from p2
where (d < 33)
) T2(e_r)
on ((b_l = 83) OR ((b_l > b_l) OR ((((b_l - e_r) + b_l) * ((26 + 95) - e_r)) = e_l)))
) T2
) T2(e_r, b_r)
on (54 > 31)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, e_r, a_r
from (
Select e, b
from p1
where (e = (98 * 78))
) T1(e_l, b_l)
left join (
Select e, a, b
from p5
where (68 = d)
) T2(e_r, a_r, b_r)
on ((79 > e_l) AND (36 < a_r))
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
    #*****************************************
    _testmgr.testcase_end(desc)

