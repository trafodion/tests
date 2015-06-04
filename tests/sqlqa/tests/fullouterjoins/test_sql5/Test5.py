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
    
def test001(desc="""Joins Set 5"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
Select e_l, c_l, c_r_r
from (
Select e, c
from p2
where (((16 - b) > 45) OR ((d - (d - 30)) = 98))
) T1(e_l, c_l)
full join (
Select a_l, c_r
from (
Select a
from p4
where (d = (1 * 85))
) T1(a_l)
full join (
Select e, c, a
from p3
where ((3 = (87 * (39 - 84))) OR (43 < (d * 5)))
) T2(e_r, c_r, a_r)
on ((72 > (c_r + (21 - 42))) OR (93 > ((c_r * a_l) - 70)))
) T2(a_l_r, c_r_r)
on (89 > 12)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, d_r
from (
Select a, d
from p3
where (c = 0)
) T1(a_l, d_l)
full join (
select c, d
from (
Select c, d
from p2
where (31 = 9)
) T1
union all
select c, a
from (
Select c, a, b
from p1
where ((25 + a) = d)
) T2
) T2(c_r, d_r)
on (d_r < (17 + 58))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_l, a_l_r, a_r_l_r_r
from (
Select d_l, b_r
from (
Select d
from p3
where ((d < (c + (e - e))) OR (((c * c) > 26) OR (e = 0)))
) T1(d_l)
left join (
Select b
from p4
where ((e - a) > (b * a))
) T2(b_r)
on (22 = (d_l - b_r))
) T1(d_l_l, b_r_l)
full join (
Select c_l, a_l, a_r_l_r
from (
select c, a
from (
Select c, a
from p4
where (e > 26)
) T1
union all
select e, c
from (
select e, c
from (
Select e, c, a
from p2
where ((a * e) = 67)
) T1
union all
select e_r_l, a_r
from (
Select e_r_l, a_r
from (
Select b_l, e_r, c_r
from (
Select b
from p1
where (85 > 43)
) T1(b_l)
full join (
Select e, c
from p3
where (((e - 50) - 2) > d)
) T2(e_r, c_r)
on ((37 = 80) AND ((31 > 45) OR (6 < 80)))
) T1(b_l_l, e_r_l, c_r_l)
inner join (
Select a
from p4
where ((49 + e) > 63)
) T2(a_r)
on ((e_r_l = e_r_l) AND ((73 - e_r_l) < e_r_l))
) T2
) T2
) T1(c_l, a_l)
left join (
select a_r_l
from (
Select a_r_l, a_r_l_l, e_r_l_r
from (
Select a_r_l, a_r, b_r
from (
Select c_r_l, b_l_l, a_r
from (
Select b_l, c_r
from (
Select e, b
from p5
where (a = e)
) T1(e_l, b_l)
inner join (
Select c
from p4
where (b > c)
) T2(c_r)
on (87 < c_r)
) T1(b_l_l, c_r_l)
inner join (
select e, a
from (
Select e, a
from p2
where (e < b)
) T1
union all
select e, c
from (
select e, c, d
from (
Select e, c, d
from p3
where ((71 = b) OR (d < (a - (35 * b))))
) T1
union all
select c, a, d
from (
Select c, a, d
from p3
where ((b < a) AND ((46 = 59) OR ((1 - 88) > 42)))
) T2
) T2
) T2(e_r, a_r)
on ((b_l_l * 39) = b_l_l)
) T1(c_r_l_l, b_l_l_l, a_r_l)
full join (
Select a, b
from p4
where (90 = (89 * b))
) T2(a_r, b_r)
on ((b_r = 55) AND (25 > 92))
) T1(a_r_l_l, a_r_l, b_r_l)
full join (
Select d_r_r_l_l, e_l_r_l_l, e_r_l, d_r_r, c_r_r
from (
Select c_l_l, e_l_r_l, d_r_r_l, e_r
from (
Select c_l, d_l, c_l_r, e_l_r, d_r_r
from (
select c, d
from (
Select c, d
from p4
where (e = 85)
) T1
union all
select b, d
from (
Select b, d
from p1
where (c < 19)
) T2
) T1(c_l, d_l)
left join (
Select e_l, c_l, d_l, d_r
from (
Select e, c, d
from p5
where (d = (e + 94))
) T1(e_l, c_l, d_l)
full join (
Select d
from p5
where ((80 - 66) < b)
) T2(d_r)
on (12 = e_l)
) T2(e_l_r, c_l_r, d_l_r, d_r_r)
on ((c_l + d_r_r) > e_l_r)
) T1(c_l_l, d_l_l, c_l_r_l, e_l_r_l, d_r_r_l)
left join (
select e, d
from (
Select e, d
from p2
where (35 < 40)
) T1
union all
select a, d
from (
Select a, d
from p2
where (b = b)
) T2
) T2(e_r, d_r)
on ((d_r_r_l * 91) = e_l_r_l)
) T1(c_l_l_l, e_l_r_l_l, d_r_r_l_l, e_r_l)
inner join (
Select a_r_l, d_l_l, c_r, d_r
from (
Select d_l, a_r
from (
Select d
from p2
where (a < (b * 70))
) T1(d_l)
full join (
Select a
from p4
where (b < 5)
) T2(a_r)
on (((d_l + 37) * (a_r + 66)) < (a_r - 39))
) T1(d_l_l, a_r_l)
left join (
Select c, d
from p4
where (e = e)
) T2(c_r, d_r)
on ((a_r_l - (a_r_l * d_l_l)) = c_r)
) T2(a_r_l_r, d_l_l_r, c_r_r, d_r_r)
on (((e_l_r_l_l + (0 + 1)) < d_r_r_l_l) OR ((41 = d_r_r) AND ((e_r_l - 5) = c_r_r)))
) T2(d_r_r_l_l_r, e_l_r_l_l_r, e_r_l_r, d_r_r_r, c_r_r_r)
on ((a_r_l_l = a_r_l_l) AND (79 > (((((a_r_l - ((a_r_l - a_r_l) * a_r_l_l)) * e_r_l_r) + a_r_l_l) * a_r_l) * 80)))
) T1
union all
select e
from (
Select e
from p2
where ((c = 49) OR ((e > (22 * (e * d))) OR (22 = 71)))
) T2
) T2(a_r_l_r)
on ((a_l = 42) AND (13 > c_l))
) T2(c_l_r, a_l_r, a_r_l_r_r)
on ((4 = 98) AND (a_l_r = 10))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_l, c_r
from (
Select e, c, a
from p5
where (13 > b)
) T1(e_l, c_l, a_l)
full join (
Select c, a
from p5
where (89 = 27)
) T2(c_r, a_r)
on (e_l > ((36 - c_r) - (96 + e_l)))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_r_r
from (
Select e, a, b
from p2
where (73 = (b + a))
) T1(e_l, a_l, b_l)
left join (
Select b_l, a_r
from (
Select b
from p2
where (44 > (e * d))
) T1(b_l)
inner join (
Select a, b, d
from p1
where (d > ((c * 56) * 35))
) T2(a_r, b_r, d_r)
on (5 = b_l)
) T2(b_l_r, a_r_r)
on (65 > 19)
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
Select c_l, b_r
from (
select c
from (
select c
from (
Select c
from p2
where (b > 59)
) T1
union all
select d
from (
Select d
from p1
where ((50 * d) = 60)
) T2
) T1
union all
select b_l_l
from (
Select b_l_l, e_r, b_r
from (
Select b_l, e_r, a_r
from (
Select b, d
from p5
where (((c - b) < 47) OR ((((32 + c) * d) - 74) = 90))
) T1(b_l, d_l)
inner join (
Select e, a
from p4
where ((((b + 70) * a) - 66) > (((87 * 5) - 16) * (66 - ((b + 46) * d))))
) T2(e_r, a_r)
on (b_l = (a_r + a_r))
) T1(b_l_l, e_r_l, a_r_l)
inner join (
Select e, c, b
from p5
where ((d = (d - 76)) AND (((e + c) * 61) > 78))
) T2(e_r, c_r, b_r)
on ((((b_r + 6) * b_r) * 51) < 70)
) T2
) T1(c_l)
left join (
Select b
from p1
where (13 = (86 * b))
) T2(b_r)
on (36 = (94 + 20))
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
Select a_l, d_r_r
from (
Select a
from p2
where (42 = 20)
) T1(a_l)
inner join (
Select a_l, d_r
from (
Select a, d
from p3
where (c > c)
) T1(a_l, d_l)
left join (
Select d
from p3
where (41 = c)
) T2(d_r)
on (64 > (d_r - a_l))
) T2(a_l_r, d_r_r)
on ((90 = a_l) AND (13 > 61))
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
Select a_l, c_r
from (
Select a
from p3
where ((a = 17) OR (b = 38))
) T1(a_l)
full join (
Select c
from p1
where (92 < d)
) T2(c_r)
on ((a_l > 70) OR (86 > 60))
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
Select c_l, a_l, a_l_r, d_r_r
from (
select c, a
from (
Select c, a
from p1
where (c = c)
) T1
union all
select c, d
from (
Select c, d
from p4
where (a > 39)
) T2
) T1(c_l, a_l)
inner join (
Select a_l, d_l, d_r
from (
Select a, d
from p5
where ((d = (b + 99)) AND ((22 * c) < 75))
) T1(a_l, d_l)
inner join (
Select d
from p1
where (11 = 49)
) T2(d_r)
on ((a_l = (d_r + 0)) AND (d_r > (a_l * 87)))
) T2(a_l_r, d_l_r, d_r_r)
on ((d_r_r < a_l_r) AND (a_l_r = a_l_r))
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
Select e_l, e_r
from (
Select e
from p2
where (((d - e) = 51) OR (((a * d) > 35) AND ((e = d) AND ((57 = c) AND (d < b)))))
) T1(e_l)
full join (
Select e, a
from p1
where (((1 + d) * a) = e)
) T2(e_r, a_r)
on ((e_r = (27 - (e_l - (e_r + 2)))) AND (e_r = 29))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l_l, d_r
from (
Select e_l, e_r
from (
select e
from (
Select e, b
from p4
where (((33 - 0) > c) OR (d = 1))
) T1
union all
select d
from (
Select d
from p1
where (87 > 33)
) T2
) T1(e_l)
left join (
Select e
from p2
where (83 < 76)
) T2(e_r)
on (((81 + 71) > 11) OR (((e_r + e_l) = 68) AND ((((25 * 22) - ((e_r - e_l) * 89)) < (89 + e_l)) AND ((19 = e_l) AND (e_l = e_r)))))
) T1(e_l_l, e_r_l)
left join (
Select c, a, d
from p5
where (b < (22 * a))
) T2(c_r, a_r, d_r)
on ((e_l_l = d_r) OR (((58 + (d_r - e_l_l)) < 77) AND (((d_r + 97) < 8) AND ((d_r + 14) = e_l_l))))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_l, c_r, d_r
from (
Select c, a, b, d
from p5
where ((c < 7) OR (a < 24))
) T1(c_l, a_l, b_l, d_l)
inner join (
Select e, c, d
from p1
where (74 = 64)
) T2(e_r, c_r, d_r)
on (28 > d_r)
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
Select b_l, c_r
from (
Select b
from p4
where (48 > 18)
) T1(b_l)
left join (
Select c, d
from p3
where ((e = (53 + b)) AND (e > 89))
) T2(c_r, d_r)
on (b_l < b_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, b_r
from (
Select a, d
from p2
where (18 = (8 + 20))
) T1(a_l, d_l)
left join (
Select b
from p1
where (((2 * a) < a) AND ((e > 55) OR (65 = 70)))
) T2(b_r)
on (46 = 45)
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
Select b_l, d_r
from (
Select b
from p1
where ((c = 47) AND (a < 57))
) T1(b_l)
left join (
Select d
from p2
where (15 > b)
) T2(d_r)
on (((d_r - 31) - 77) < 27)
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
Select e_l, c_l, b_l, e_r, a_r, d_r
from (
Select e, c, b
from p5
where (((a * (35 + e)) < 74) AND (a < (c * (((32 - 86) * 67) - 41))))
) T1(e_l, c_l, b_l)
left join (
select e, a, d
from (
Select e, a, d
from p5
where ((33 - 31) = 87)
) T1
union all
select c, a, b
from (
Select c, a, b
from p1
where (e > 61)
) T2
) T2(e_r, a_r, d_r)
on ((43 > 93) OR ((d_r = 64) OR (73 > 6)))
order by 1, 2, 3, 4, 5, 6
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
Select d_l, e_r
from (
Select d
from p4
where ((86 + (31 + 3)) = (64 + (b - a)))
) T1(d_l)
left join (
select e
from (
Select e
from p2
where ((((d * b) + e) * 69) < 90)
) T1
union all
select c
from (
Select c
from p2
where ((72 = a) AND ((24 = 56) AND ((c + 34) = 27)))
) T2
) T2(e_r)
on ((d_l + 66) < (e_r + 51))
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
Select a_l, e_r, d_r
from (
select a
from (
Select a
from p2
where ((0 = e) AND (a < 75))
) T1
union all
select e
from (
Select e, c, a
from p5
where (((84 - b) > 68) AND (c = 13))
) T2
) T1(a_l)
left join (
Select e, d
from p2
where (((c + (19 + b)) = b) OR (22 = 38))
) T2(e_r, d_r)
on (((32 + 61) > 52) AND (e_r = 61))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, b_r
from (
Select e, c, a, b
from p1
where (a = c)
) T1(e_l, c_l, a_l, b_l)
inner join (
Select a, b
from p5
where ((53 + 92) = 85)
) T2(a_r, b_r)
on ((39 > b_r) OR (b_l = b_r))
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
Select e_l_l, a_l_r_l_r_l_r_r_l, d_l_r
from (
Select e_l, b_l, a_l_r_l_r_l_r_r, b_l_r
from (
select e, b
from (
Select e, b
from p5
where ((c > (41 + 82)) OR (e = (c - 34)))
) T1
union all
select e, a
from (
Select e, a, d
from p5
where (75 = ((5 * 90) + e))
) T2
) T1(e_l, b_l)
full join (
Select e_l, b_l, a_l_r_l_r_l_r, c_r_r
from (
Select e, c, b
from p4
where ((d = ((40 + e) + (13 * b))) AND (63 = 99))
) T1(e_l, c_l, b_l)
full join (
Select c_l_l, c_r_r_l, a_l_r_l_r_l, c_r
from (
Select c_l, d_l, a_r_r, a_l_r_l_r, c_r_r
from (
Select c, a, d
from p1
where (70 = c)
) T1(c_l, a_l, d_l)
full join (
Select e_l_l_l_l, a_l_r_l, c_r, a_r, b_r
from (
Select e_l_l_l, a_l_r, c_r_r
from (
Select e_l_l, b_r_r
from (
select e_l
from (
Select e_l, b_r, d_r
from (
Select e, a, b
from p4
where (18 = e)
) T1(e_l, a_l, b_l)
inner join (
Select e, b, d
from p5
where ((85 = 87) OR (((83 + a) > 90) AND (e > 39)))
) T2(e_r, b_r, d_r)
on (e_l < 93)
) T1
union all
select c
from (
Select c
from p4
where (b = c)
) T2
) T1(e_l_l)
left join (
Select c_l, e_r, c_r, b_r
from (
Select e, c
from p1
where (77 > b)
) T1(e_l, c_l)
inner join (
Select e, c, b
from p1
where ((a = (66 * (e - 99))) AND ((26 * 40) < 94))
) T2(e_r, c_r, b_r)
on (c_r > ((b_r + (((86 + (54 * 63)) + b_r) - 62)) - c_l))
) T2(c_l_r, e_r_r, c_r_r, b_r_r)
on (b_r_r = b_r_r)
) T1(e_l_l_l, b_r_r_l)
full join (
Select a_l, c_r
from (
Select a
from p4
where ((e = (40 - c)) AND ((d - 80) > b))
) T1(a_l)
left join (
select c, a
from (
select c, a
from (
Select c, a, d
from p3
where (98 < d)
) T1
union all
select a, b
from (
Select a, b
from p2
where ((((74 + b) * 99) > 26) AND (d < (c - (33 + 67))))
) T2
) T1
union all
select e, d
from (
Select e, d
from p3
where (a > c)
) T2
) T2(c_r, a_r)
on (c_r = 15)
) T2(a_l_r, c_r_r)
on (49 = (e_l_l_l + e_l_l_l))
) T1(e_l_l_l_l, a_l_r_l, c_r_r_l)
left join (
Select c, a, b
from p3
where (82 < (84 + a))
) T2(c_r, a_r, b_r)
on (77 = 61)
) T2(e_l_l_l_l_r, a_l_r_l_r, c_r_r, a_r_r, b_r_r)
on ((a_r_r + a_r_r) = c_r_r)
) T1(c_l_l, d_l_l, a_r_r_l, a_l_r_l_r_l, c_r_r_l)
full join (
Select e, c, d
from p1
where ((34 > 29) AND (4 = e))
) T2(e_r, c_r, d_r)
on (80 > c_l_l)
) T2(c_l_l_r, c_r_r_l_r, a_l_r_l_r_l_r, c_r_r)
on ((89 < e_l) OR (15 > 8))
) T2(e_l_r, b_l_r, a_l_r_l_r_l_r_r, c_r_r_r)
on (b_l < 8)
) T1(e_l_l, b_l_l, a_l_r_l_r_l_r_r_l, b_l_r_l)
full join (
Select b_l, d_l, c_r
from (
Select b, d
from p3
where (55 = ((b * (c + b)) - (d + (45 + b))))
) T1(b_l, d_l)
left join (
Select c
from p4
where (c = b)
) T2(c_r)
on (69 = (d_l * c_r))
) T2(b_l_r, d_l_r, c_r_r)
on (68 = 84)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #*********************************************
    _testmgr.testcase_end(desc)

