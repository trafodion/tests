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
    
def test001(desc="""Joins Set 31"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_l, b_r
from (
Select e, a
from p3
where ((b = ((a + (45 + 44)) - e)) OR (5 > 59))
) T1(e_l, a_l)
left join (
Select b
from p1
where (18 > 73)
) T2(b_r)
on (85 < (95 + 0))
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
Select d_l, b_r_r
from (
Select c, d
from p5
where ((71 < (e - c)) AND ((97 = 92) OR ((c + e) = 47)))
) T1(c_l, d_l)
full join (
select a_l, b_r
from (
Select a_l, b_r, d_r
from (
select e, a
from (
Select e, a, b
from p3
where (c = 67)
) T1
union all
select e, c
from (
Select e, c
from p1
where (a = a)
) T2
) T1(e_l, a_l)
left join (
Select b, d
from p1
where ((91 = 81) OR (12 = 34))
) T2(b_r, d_r)
on ((24 = 70) AND (b_r = a_l))
) T1
union all
select a_l, d_r
from (
Select a_l, d_r
from (
Select a
from p5
where (91 = (54 - (20 - (71 + 74))))
) T1(a_l)
left join (
Select d
from p2
where (92 = 94)
) T2(d_r)
on ((23 > (d_r + 6)) OR ((d_r = d_r) OR (93 = a_l)))
) T2
) T2(a_l_r, b_r_r)
on (d_l < 84)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, e_r, c_r
from (
Select e, c
from p2
where (24 > 18)
) T1(e_l, c_l)
full join (
Select e, c
from p5
where ((66 * a) = a)
) T2(e_r, c_r)
on (e_r = 14)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l, c_l_r
from (
Select c, b, d
from p1
where (27 = 52)
) T1(c_l, b_l, d_l)
left join (
select c_l
from (
Select c_l, e_r
from (
select c
from (
Select c
from p1
where ((63 = a) OR (12 > c))
) T1
union all
select e_l
from (
Select e_l, d_l, b_l_r_r
from (
select e, d
from (
Select e, d
from p4
where ((86 > (94 * (82 - b))) OR ((d > e) OR ((a - 33) = 43)))
) T1
union all
select e, c
from (
Select e, c, b, d
from p3
where ((e > b) OR (42 = 82))
) T2
) T1(e_l, d_l)
inner join (
Select d_l, b_r_r, b_l_r
from (
select d
from (
Select d
from p1
where (8 = 58)
) T1
union all
select c
from (
Select c
from p4
where (c = 82)
) T2
) T1(d_l)
inner join (
Select b_l, d_l, b_r
from (
Select a, b, d
from p4
where ((49 > e) OR ((c = 79) AND ((81 + 92) > a)))
) T1(a_l, b_l, d_l)
inner join (
Select c, b
from p4
where (4 = d)
) T2(c_r, b_r)
on ((42 > b_r) AND ((b_l + (39 + b_l)) > 26))
) T2(b_l_r, d_l_r, b_r_r)
on (((b_r_r * 79) = b_l_r) OR (58 < 88))
) T2(d_l_r, b_r_r_r, b_l_r_r)
on (26 = 98)
) T2
) T1(c_l)
left join (
Select e
from p5
where ((((79 + d) - 92) = 56) OR (a < 51))
) T2(e_r)
on (c_l < 14)
) T1
union all
select b
from (
Select b
from p2
where ((e = c) AND (((15 - d) = (e * 4)) OR ((25 > a) OR (d < 36))))
) T2
) T2(c_l_r)
on (((b_l + (52 - (b_l - c_l))) < c_l_r) OR (((62 * (74 - (3 * c_l))) = 44) OR (83 < (((b_l + c_l) - (c_l - b_l)) + c_l_r))))
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
Select c_l, b_r
from (
Select c
from p1
where ((8 - c) = b)
) T1(c_l)
left join (
Select c, b
from p5
where (((a + e) * (c + a)) = 25)
) T2(c_r, b_r)
on (b_r = (((b_r + b_r) * b_r) + b_r))
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
Select c, a, b
from p1
where ((c < b) OR ((a = 34) OR (27 > d)))
) T1(c_l, a_l, b_l)
left join (
Select b
from p4
where (82 > a)
) T2(b_r)
on ((b_r + 70) > 9)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l, e_r
from (
Select c, b, d
from p5
where (e > 98)
) T1(c_l, b_l, d_l)
left join (
Select e
from p2
where (((89 * a) > (((94 * 6) - 9) + d)) AND (d = 59))
) T2(e_r)
on (13 > b_l)
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
Select b_l, c_r, d_r
from (
Select a, b
from p1
where ((b = c) AND (c < e))
) T1(a_l, b_l)
left join (
Select c, d
from p1
where ((c = d) OR (c > b))
) T2(c_r, d_r)
on (d_r = c_r)
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
Select b_l, c_r, a_r
from (
select c, b
from (
select c, b
from (
Select c, b
from p5
where (67 < (d + e))
) T1
union all
select e, a
from (
Select e, a, b
from p2
where ((b = 12) OR (42 = 16))
) T2
) T1
union all
select c, b
from (
Select c, b
from p1
where ((10 > e) AND (69 > 80))
) T2
) T1(c_l, b_l)
full join (
Select c, a
from p4
where (18 < c)
) T2(c_r, a_r)
on ((40 > c_r) OR ((a_r * b_l) = 34))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l_l, e_r_l, b_r
from (
Select d_l, e_r
from (
Select d
from p3
where ((d = 3) AND ((b - (76 - (e * 33))) = 35))
) T1(d_l)
left join (
select e
from (
Select e, c
from p3
where (e < 2)
) T1
union all
select c
from (
Select c
from p5
where ((15 < c) AND (((c + a) = (73 * d)) AND ((b = e) OR ((83 = 85) OR (c = (16 - a))))))
) T2
) T2(e_r)
on (((76 - (d_l - 0)) * d_l) < (e_r - e_r))
) T1(d_l_l, e_r_l)
left join (
Select b
from p2
where ((30 = 49) AND (d < (e - ((2 * 44) - b))))
) T2(b_r)
on (21 < (1 * 48))
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
Select b_l, d_l, d_r_r_r
from (
select a, b, d
from (
Select a, b, d
from p4
where (b > 74)
) T1
union all
select e_l, a_r_r, d_l_r
from (
Select e_l, a_r_r, d_l_r, e_r_r
from (
Select e, c
from p3
where ((a > (78 * b)) OR (50 < 78))
) T1(e_l, c_l)
full join (
Select d_l, e_r, a_r
from (
Select d
from p3
where (e = c)
) T1(d_l)
left join (
Select e, a, d
from p5
where ((86 + (60 - 55)) < b)
) T2(e_r, a_r, d_r)
on (e_r > e_r)
) T2(d_l_r, e_r_r, a_r_r)
on ((18 < a_r_r) AND ((81 * 2) < 10))
) T2
) T1(a_l, b_l, d_l)
left join (
select a_r_l, c_l_r, d_r_r
from (
Select a_r_l, c_l_r, d_r_r, d_l_r
from (
select a_r_l, e_r_l_l, a_r, d_r
from (
Select a_r_l, e_r_l_l, a_r, d_r
from (
Select e_r_l, b_l_l, a_r
from (
Select c_l, b_l, e_r, a_r
from (
select c, b, d
from (
Select c, b, d
from p2
where (60 > e)
) T1
union all
select c_l_l_l, e_r_l, c_r
from (
Select c_l_l_l, e_r_l, c_r, b_r
from (
Select c_l_l, d_r_r_l, e_r, d_r
from (
Select e_l, c_l, d_r_r
from (
Select e, c
from p2
where (((b - 72) - b) = (a * (((e - 72) * c) - 52)))
) T1(e_l, c_l)
inner join (
Select b_l, d_r
from (
Select b
from p4
where ((c < 10) AND (45 = (a - (a - (b - b)))))
) T1(b_l)
left join (
Select e, c, d
from p4
where ((54 + 38) = b)
) T2(e_r, c_r, d_r)
on ((b_l + (22 + b_l)) = (d_r * (67 - 83)))
) T2(b_l_r, d_r_r)
on ((47 = c_l) OR (c_l > 94))
) T1(e_l_l, c_l_l, d_r_r_l)
left join (
Select e, a, d
from p2
where (d > 33)
) T2(e_r, a_r, d_r)
on ((4 = 98) OR (10 = 79))
) T1(c_l_l_l, d_r_r_l_l, e_r_l, d_r_l)
left join (
select e, c, b
from (
Select e, c, b
from p3
where (12 > 65)
) T1
union all
select e, a, d
from (
select e, a, d
from (
Select e, a, d
from p2
where (((d + a) = d) OR (28 = b))
) T1
union all
select c, b, d
from (
Select c, b, d
from p4
where (e < 96)
) T2
) T2
) T2(e_r, c_r, b_r)
on ((67 * 40) = 34)
) T2
) T1(c_l, b_l, d_l)
inner join (
Select e, a
from p5
where (36 < 71)
) T2(e_r, a_r)
on ((9 > a_r) OR (99 < 5))
) T1(c_l_l, b_l_l, e_r_l, a_r_l)
left join (
Select e, a, d
from p3
where ((17 > d) AND ((0 = 51) AND (((23 * 83) = 1) OR ((76 = (e * 68)) OR ((72 = 20) OR (66 = 17))))))
) T2(e_r, a_r, d_r)
on (24 = ((b_l_l + 58) + (b_l_l + e_r_l)))
) T1(e_r_l_l, b_l_l_l, a_r_l)
full join (
Select a, b, d
from p1
where (8 > (26 - (c - (c + b))))
) T2(a_r, b_r, d_r)
on (e_r_l_l = d_r)
) T1
union all
select c_l, b_l, a_r_r_r, e_l_l_r
from (
Select c_l, b_l, a_r_r_r, e_l_l_r
from (
Select c, b
from p4
where (15 > 22)
) T1(c_l, b_l)
full join (
Select e_l_l, a_r_r, c_r_r
from (
Select e_l, c_r
from (
Select e, c, a
from p5
where ((d - e) < 28)
) T1(e_l, c_l, a_l)
inner join (
Select c, a
from p2
where (7 < 4)
) T2(c_r, a_r)
on ((e_l > 12) AND (e_l = e_l))
) T1(e_l_l, c_r_l)
inner join (
Select e_l, a_l, c_r, a_r
from (
Select e, c, a
from p2
where ((a = d) OR ((66 > 88) AND ((82 = ((e - 32) * (c + c))) OR (b = 13))))
) T1(e_l, c_l, a_l)
left join (
Select c, a
from p2
where ((c - 63) > d)
) T2(c_r, a_r)
on (e_l > e_l)
) T2(e_l_r, a_l_r, c_r_r, a_r_r)
on ((3 = 15) OR ((e_l_l * ((((53 + 77) * e_l_l) * (99 + 80)) * 72)) < (a_r_r - 28)))
) T2(e_l_l_r, a_r_r_r, c_r_r_r)
on (c_l > a_r_r_r)
) T2
) T1(a_r_l_l, e_r_l_l_l, a_r_l, d_r_l)
full join (
Select c_l, d_l, d_r
from (
Select c, d
from p5
where (28 < e)
) T1(c_l, d_l)
left join (
Select a, b, d
from p2
where (e < e)
) T2(a_r, b_r, d_r)
on (32 = 42)
) T2(c_l_r, d_l_r, d_r_r)
on (12 < a_r_l)
) T1
union all
select c_l, b_l, e_r
from (
Select c_l, b_l, e_r
from (
Select e, c, b
from p2
where (c = 99)
) T1(e_l, c_l, b_l)
full join (
Select e, b
from p1
where ((d > e) AND ((13 = e) AND ((44 < d) OR ((a + 68) > (((d * 72) * 98) * 64)))))
) T2(e_r, b_r)
on (22 > e_r)
) T2
) T2(a_r_l_r, c_l_r_r, d_r_r_r)
on ((24 = d_r_r_r) AND (d_r_r_r > b_l))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_l, e_r, c_r
from (
Select e_l, b_r
from (
Select e
from p1
where ((a = 43) OR ((((b - e) * e) = (98 - 98)) OR (c > d)))
) T1(e_l)
full join (
Select a, b
from p3
where (77 = 27)
) T2(a_r, b_r)
on (3 < 96)
) T1(e_l_l, b_r_l)
inner join (
Select e, c
from p3
where (3 = 21)
) T2(e_r, c_r)
on (c_r = 58)
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
Select c_l, c_l_r_r, e_l_r, b_l_r
from (
Select c, b
from p2
where ((6 > 21) OR (23 < e))
) T1(c_l, b_l)
inner join (
select e_l, b_l, c_l_r
from (
select e_l, b_l, c_l_r
from (
Select e_l, b_l, c_l_r, a_r_r, d_l_r
from (
Select e, b
from p2
where (d = 61)
) T1(e_l, b_l)
left join (
Select c_l, d_l, a_r
from (
Select c, a, d
from p5
where (e = (e + ((52 - 27) * a)))
) T1(c_l, a_l, d_l)
left join (
Select a, d
from p5
where ((19 = d) AND ((89 > a) OR ((59 = b) OR ((a > 55) OR ((c = d) OR (d < (53 * d)))))))
) T2(a_r, d_r)
on (d_l = a_r)
) T2(c_l_r, d_l_r, a_r_r)
on ((88 = 34) OR ((((c_l_r + 36) + 24) - d_l_r) = d_l_r))
) T1
union all
select e, c, b
from (
Select e, c, b
from p5
where ((a < d) OR ((e = 80) AND (47 = (c + 71))))
) T2
) T1
union all
select e, c, b
from (
Select e, c, b, d
from p1
where (d = 86)
) T2
) T2(e_l_r, b_l_r, c_l_r_r)
on ((b_l_r > 56) AND (e_l_r = b_l_r))
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
Select e_l, d_r
from (
Select e, a, b
from p1
where ((87 > 45) AND (80 > 98))
) T1(e_l, a_l, b_l)
left join (
Select e, d
from p1
where ((((93 + 46) * 94) > 40) AND (61 < (c - 73)))
) T2(e_r, d_r)
on (59 > ((d_r + d_r) + (45 + 1)))
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
Select a_l_l_l, c_l_r, a_l_r_r
from (
Select a_l_l, d_r
from (
select a_l
from (
Select a_l, d_l, e_r, c_r, a_r
from (
Select c, a, d
from p4
where ((11 * (84 * 56)) < (64 - c))
) T1(c_l, a_l, d_l)
inner join (
Select e, c, a
from p2
where (e > (79 + a))
) T2(e_r, c_r, a_r)
on ((a_r - 53) = (48 - c_r))
) T1
union all
select a
from (
Select a
from p1
where (((42 + e) = a) AND (d = 87))
) T2
) T1(a_l_l)
left join (
Select d
from p4
where (98 > c)
) T2(d_r)
on (a_l_l < (58 - a_l_l))
) T1(a_l_l_l, d_r_l)
left join (
Select c_l, a_l_r
from (
Select c
from p1
where (((99 + c) + ((e * d) - (41 * d))) = 59)
) T1(c_l)
left join (
Select a_l, d_l, b_r
from (
select a, d
from (
Select a, d
from p5
where ((b > 76) OR (((d + 22) = a) AND ((a + 22) = 22)))
) T1
union all
select c, a
from (
Select c, a
from p3
where (a < b)
) T2
) T1(a_l, d_l)
left join (
Select b
from p1
where (32 > e)
) T2(b_r)
on (17 = 41)
) T2(a_l_r, d_l_r, b_r_r)
on (40 > ((77 - 27) + c_l))
) T2(c_l_r, a_l_r_r)
on ((7 = a_l_l_l) AND (((c_l_r + 15) > c_l_r) AND (((c_l_r - 96) + a_l_l_l) = c_l_r)))
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
Select a_l, b_l, d_r_r
from (
Select a, b
from p1
where ((((87 + c) * (43 * (34 - (a - 52)))) - 88) = 25)
) T1(a_l, b_l)
left join (
Select a_r_l, e_l_l_l, d_r
from (
Select e_l_l, c_r_r_l, a_r
from (
Select e_l, e_l_r, d_r_r, c_r_r
from (
Select e, c, d
from p5
where (89 = (73 - e))
) T1(e_l, c_l, d_l)
inner join (
Select e_l, b_l, c_r, d_r
from (
select e, b
from (
Select e, b
from p5
where (39 > a)
) T1
union all
select e, a
from (
Select e, a, b, d
from p4
where (e > 8)
) T2
) T1(e_l, b_l)
left join (
Select e, c, d
from p1
where ((c > e) AND (((b * 95) = 49) AND (((53 - (37 - b)) * 9) = 58)))
) T2(e_r, c_r, d_r)
on ((20 > e_l) AND ((c_r > (91 - 21)) AND (e_l = c_r)))
) T2(e_l_r, b_l_r, c_r_r, d_r_r)
on ((c_r_r = 37) AND ((d_r_r < 77) OR (d_r_r = 75)))
) T1(e_l_l, e_l_r_l, d_r_r_l, c_r_r_l)
inner join (
Select a
from p3
where (c > 7)
) T2(a_r)
on (84 = 18)
) T1(e_l_l_l, c_r_r_l_l, a_r_l)
inner join (
Select d
from p5
where ((90 > 83) AND ((a = a) OR ((c * 77) = d)))
) T2(d_r)
on (a_r_l < e_l_l_l)
) T2(a_r_l_r, e_l_l_l_r, d_r_r)
on (d_r_r = 98)
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
Select a_l_r_l, e_r
from (
Select a_l, a_l_r
from (
Select a
from p2
where (70 = (31 - 36))
) T1(a_l)
left join (
Select a_l, b_l, d_l, a_r, d_r
from (
Select a, b, d
from p4
where ((12 < a) OR (37 < e))
) T1(a_l, b_l, d_l)
left join (
Select a, d
from p4
where ((d > b) OR ((63 < 24) AND (e < 64)))
) T2(a_r, d_r)
on ((((87 + (38 * 20)) + d_l) < d_l) OR (d_r > b_l))
) T2(a_l_r, b_l_r, d_l_r, a_r_r, d_r_r)
on (a_l = a_l)
) T1(a_l_l, a_l_r_l)
left join (
Select e
from p1
where ((a = e) OR ((a - b) < (b - 56)))
) T2(e_r)
on (a_l_r_l > 51)
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
Select a_r_r_r_l, e_l_r_l, e_r
from (
Select d_l, e_l_r, a_r_r_r
from (
Select d
from p2
where (40 = 3)
) T1(d_l)
left join (
Select e_l, a_r_r
from (
Select e, c, a, d
from p5
where (e = 13)
) T1(e_l, c_l, a_l, d_l)
full join (
Select d_l, c_r, a_r
from (
Select d
from p4
where ((e = 69) OR (c = 14))
) T1(d_l)
full join (
Select c, a, b
from p2
where ((b + b) > 26)
) T2(c_r, a_r, b_r)
on (((82 - a_r) < a_r) OR ((71 > a_r) AND (76 = 72)))
) T2(d_l_r, c_r_r, a_r_r)
on (88 < 68)
) T2(e_l_r, a_r_r_r)
on (a_r_r_r = e_l_r)
) T1(d_l_l, e_l_r_l, a_r_r_r_l)
full join (
Select e
from p4
where (d < a)
) T2(e_r)
on (((56 * a_r_r_r_l) + 40) = e_l_r_l)
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
Select b_l, d_l, c_r_r, e_r_r
from (
Select b, d
from p5
where (((27 + 73) - 25) = 40)
) T1(b_l, d_l)
left join (
Select e_l, a_l, e_r, c_r
from (
Select e, a
from p4
where (e > ((6 * 2) * c))
) T1(e_l, a_l)
left join (
Select e, c
from p3
where (c > e)
) T2(e_r, c_r)
on (c_r = a_l)
) T2(e_l_r, a_l_r, e_r_r, c_r_r)
on (73 > b_l)
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
Select c_l, a_r
from (
Select c
from p2
where (e > e)
) T1(c_l)
full join (
select a
from (
Select a, d
from p1
where (83 = a)
) T1
union all
select e
from (
Select e
from p1
where ((62 > b) OR (26 < 16))
) T2
) T2(a_r)
on (((c_l - a_r) = 52) OR (63 = 85))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #**************
    _testmgr.testcase_end(desc)

