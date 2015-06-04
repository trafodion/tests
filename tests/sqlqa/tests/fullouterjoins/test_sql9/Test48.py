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
    
def test001(desc="""Joins Set 48"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_r
from (
select e, a
from (
Select e, a, b
from p3
where ((b + 56) > 93)
) T1
union all
select c, a
from (
Select c, a
from p5
where (69 = (83 + 93))
) T2
) T1(e_l, a_l)
inner join (
Select b
from p3
where ((d < 86) OR ((a > e) OR ((d = 30) AND ((14 = 30) OR (a < b)))))
) T2(b_r)
on (28 = b_r)
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
Select e_l, c_l_r, e_r_r
from (
Select e, c, a, b
from p4
where ((23 > b) AND ((90 > d) OR (e > a)))
) T1(e_l, c_l, a_l, b_l)
full join (
Select e_l, c_l, e_r, b_r
from (
Select e, c, a, b
from p4
where (c = (c + d))
) T1(e_l, c_l, a_l, b_l)
full join (
select e, b
from (
Select e, b
from p2
where (1 > a)
) T1
union all
select a, d
from (
Select a, d
from p5
where ((68 = (d - (35 * 65))) AND (e = (71 + 62)))
) T2
) T2(e_r, b_r)
on ((75 > e_r) AND ((0 + e_r) = c_l))
) T2(e_l_r, c_l_r, e_r_r, b_r_r)
on ((41 > 4) OR (55 < e_l))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test48exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_r
from (
Select a
from p3
where (54 = 95)
) T1(a_l)
inner join (
Select b
from p4
where ((46 > 0) OR (25 > b))
) T2(b_r)
on (a_l = a_l)
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
Select e_l_l, c_r
from (
Select e_l, e_r
from (
Select e, b
from p4
where (d > d)
) T1(e_l, b_l)
inner join (
Select e
from p2
where (d > 22)
) T2(e_r)
on ((10 < e_r) AND ((44 = 8) OR (e_l > 43)))
) T1(e_l_l, e_r_l)
left join (
Select e, c
from p2
where (b < c)
) T2(e_r, c_r)
on (c_r > c_r)
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
Select b_l, e_r, d_r
from (
Select c, b
from p2
where (b = d)
) T1(c_l, b_l)
left join (
Select e, d
from p5
where (d = a)
) T2(e_r, d_r)
on ((d_r - 71) < 35)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test48exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_r_l_l_r
from (
Select a
from p4
where (e = a)
) T1(a_l)
left join (
Select a_r_l, b_r_l_l, e_r
from (
Select a_l_l, b_r_l, a_r
from (
Select a_l, b_r
from (
Select a
from p3
where ((85 = e) OR (((27 - 65) < a) AND (d = e)))
) T1(a_l)
left join (
Select b, d
from p1
where (a > 17)
) T2(b_r, d_r)
on (a_l < 75)
) T1(a_l_l, b_r_l)
full join (
Select a
from p3
where (12 > 19)
) T2(a_r)
on ((b_r_l * b_r_l) = a_l_l)
) T1(a_l_l_l, b_r_l_l, a_r_l)
full join (
Select e
from p1
where ((94 < 48) OR ((b > 84) OR (41 = e)))
) T2(e_r)
on (71 < e_r)
) T2(a_r_l_r, b_r_l_l_r, e_r_r)
on (b_r_l_l_r = 95)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test48exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, b_r
from (
Select a, b, d
from p1
where (42 = a)
) T1(a_l, b_l, d_l)
left join (
Select b
from p4
where ((19 = 70) AND (((91 + e) = ((44 * (81 - 25)) - (36 * (((b - a) + 88) + 49)))) OR (((42 + 93) = b) AND ((61 = d) OR ((28 = a) OR ((a - ((c - (a - (99 * b))) - (61 * 83))) > d))))))
) T2(b_r)
on (b_l = b_l)
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
Select d_l, e_r, c_r
from (
Select d
from p5
where (44 = (c - 26))
) T1(d_l)
inner join (
Select e, c
from p2
where (a < c)
) T2(e_r, c_r)
on (((4 * e_r) = c_r) AND (14 = 22))
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
Select c_r_l, c_r
from (
select b_l, c_r
from (
Select b_l, c_r
from (
Select c, b, d
from p4
where (e = 24)
) T1(c_l, b_l, d_l)
full join (
Select c
from p4
where (a = 33)
) T2(c_r)
on (23 < 82)
) T1
union all
select e_l, c_l
from (
Select e_l, c_l, c_l_l_r
from (
Select e, c, b
from p2
where (c = 17)
) T1(e_l, c_l, b_l)
full join (
select b_r_l, c_l_l
from (
select b_r_l, c_l_l
from (
Select b_r_l, c_l_l, c_r, d_r
from (
Select c_l, d_l, b_r
from (
Select c, d
from p2
where (((53 - (c * 2)) > 59) AND (44 = (b - c)))
) T1(c_l, d_l)
left join (
Select b
from p4
where (32 < ((36 + 19) * 93))
) T2(b_r)
on (82 < d_l)
) T1(c_l_l, d_l_l, b_r_l)
full join (
select c, d
from (
Select c, d
from p1
where ((89 - b) > 48)
) T1
union all
select b_l, a_r
from (
Select b_l, a_r
from (
Select b
from p2
where (33 < 5)
) T1(b_l)
left join (
Select a, d
from p1
where ((((((d - 64) * e) * c) + (10 + 99)) < (61 - d)) OR (21 > 10))
) T2(a_r, d_r)
on ((10 * (a_r + a_r)) < 64)
) T2
) T2(c_r, d_r)
on ((67 > (c_r * 51)) AND (15 < 8))
) T1
union all
select e, b
from (
Select e, b
from p5
where ((c < c) OR (85 > 55))
) T2
) T1
union all
select e, c
from (
select e, c
from (
Select e, c, a, d
from p5
where (a < 62)
) T1
union all
select c, a
from (
Select c, a
from p5
where (47 = (c * e))
) T2
) T2
) T2(b_r_l_r, c_l_l_r)
on (62 > 47)
) T2
) T1(b_l_l, c_r_l)
left join (
Select c
from p5
where ((4 = 47) AND ((9 > 79) AND (94 < e)))
) T2(c_r)
on ((c_r + 36) > 12)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test48exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_r
from (
Select e, b
from p1
where (((a + b) = (b - b)) AND (a > ((a * 76) * c)))
) T1(e_l, b_l)
inner join (
Select c, b, d
from p3
where ((16 * 95) = 35)
) T2(c_r, b_r, d_r)
on (27 < 75)
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
Select e_l, d_r
from (
select e, a
from (
Select e, a
from p2
where (64 = c)
) T1
union all
select e, b
from (
select e, b
from (
Select e, b
from p3
where (22 = (24 + 72))
) T1
union all
select c, b
from (
Select c, b
from p4
where (((c - d) > 33) OR (b > 34))
) T2
) T2
) T1(e_l, a_l)
full join (
Select e, d
from p1
where (e = 34)
) T2(e_r, d_r)
on ((((75 * (57 - e_l)) * d_r) < 42) AND ((d_r > (97 - e_l)) OR (((d_r * 31) + 47) = e_l)))
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
Select a_l, d_l, c_r, b_r
from (
Select a, d
from p3
where (24 = 56)
) T1(a_l, d_l)
left join (
Select c, a, b
from p3
where (c > (96 * a))
) T2(c_r, a_r, b_r)
on (a_l < 82)
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
Select a_r_l_l, e_r_r
from (
Select d_l_l_l, a_r_l, b_r_l_l, e_r_l, c_r, a_r, d_r
from (
Select b_r_l, d_l_l, e_r, a_r
from (
Select d_l, b_r
from (
Select d
from p3
where (c = 99)
) T1(d_l)
inner join (
Select b
from p1
where (((a * (85 * (d - d))) = 57) OR ((c + a) > a))
) T2(b_r)
on ((b_r * b_r) > d_l)
) T1(d_l_l, b_r_l)
left join (
Select e, a, b
from p2
where (c > d)
) T2(e_r, a_r, b_r)
on (b_r_l = (b_r_l * 76))
) T1(b_r_l_l, d_l_l_l, e_r_l, a_r_l)
inner join (
Select c, a, b, d
from p4
where ((7 = b) OR ((e > (63 * e)) OR ((b = e) OR (20 = e))))
) T2(c_r, a_r, b_r, d_r)
on ((d_l_l_l = d_r) AND ((a_r - 22) < 15))
) T1(d_l_l_l_l, a_r_l_l, b_r_l_l_l, e_r_l_l, c_r_l, a_r_l, d_r_l)
left join (
Select e_l_l, e_r
from (
Select e_l, b_l, a_r
from (
select e, b
from (
Select e, b, d
from p3
where (62 = d)
) T1
union all
select c, b
from (
select c, b
from (
Select c, b
from p3
where (c = (e - 30))
) T1
union all
select e, c
from (
Select e, c, d
from p3
where ((32 = d) OR ((5 = e) OR (e = 12)))
) T2
) T2
) T1(e_l, b_l)
inner join (
Select a
from p3
where ((b > 73) OR ((((2 * 49) - (58 - 93)) + ((54 * b) - (d - 43))) = 77))
) T2(a_r)
on (a_r = (69 + 82))
) T1(e_l_l, b_l_l, a_r_l)
inner join (
select e
from (
Select e, a
from p4
where (b = a)
) T1
union all
select b
from (
Select b
from p1
where (((60 * b) * b) = d)
) T2
) T2(e_r)
on (59 = e_r)
) T2(e_l_l_r, e_r_r)
on ((18 = (a_r_l_l - (73 + (15 - 66)))) OR (e_r_r = (91 - 3)))
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
Select b_r_l, e_r_l, c_r, d_r
from (
Select e_l, e_r, b_r
from (
Select e, b
from p1
where (60 < (13 - (51 * (89 * 29))))
) T1(e_l, b_l)
full join (
Select e, c, b
from p5
where ((e * 12) > e)
) T2(e_r, c_r, b_r)
on (e_r > 39)
) T1(e_l_l, e_r_l, b_r_l)
full join (
Select c, d
from p2
where ((60 + ((((9 + 39) * d) + 88) + e)) < e)
) T2(c_r, d_r)
on (e_r_l < d_r)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test48exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_l, d_r
from (
Select c_l, d_l, e_r
from (
Select c, d
from p4
where (e = 99)
) T1(c_l, d_l)
inner join (
Select e, a
from p2
where ((67 = 87) OR (((c * (83 + b)) + (d + 42)) < 82))
) T2(e_r, a_r)
on ((c_l > 41) AND (83 < 69))
) T1(c_l_l, d_l_l, e_r_l)
left join (
select e, d
from (
Select e, d
from p5
where (e = b)
) T1
union all
select c, b
from (
Select c, b, d
from p3
where ((17 + d) = c)
) T2
) T2(e_r, d_r)
on ((87 = 65) OR (d_r > 30))
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
Select c_l, b_l, e_r, a_r
from (
Select c, b
from p3
where (c = (e - 77))
) T1(c_l, b_l)
left join (
Select e, a
from p3
where ((c * ((e * 88) + c)) = ((79 * 39) + 2))
) T2(e_r, a_r)
on ((41 * c_l) < b_l)
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
Select d_l, b_l_r_r, e_l_r, d_l_r_r_r
from (
Select d
from p3
where (c = b)
) T1(d_l)
left join (
Select e_l, d_l, b_l_r, d_l_r_r
from (
Select e, d
from p2
where ((b = b) OR (a < c))
) T1(e_l, d_l)
full join (
Select e_l, b_l, d_l_r
from (
Select e, b, d
from p5
where ((c - 16) = 29)
) T1(e_l, b_l, d_l)
full join (
Select b_l, d_l, e_r, c_r
from (
Select a, b, d
from p2
where (95 = ((95 * c) - 37))
) T1(a_l, b_l, d_l)
left join (
Select e, c
from p2
where (94 < a)
) T2(e_r, c_r)
on ((16 = 89) AND ((c_r = e_r) OR ((b_l = d_l) AND (92 > d_l))))
) T2(b_l_r, d_l_r, e_r_r, c_r_r)
on (((b_l * 0) < (22 * 10)) AND (b_l > 35))
) T2(e_l_r, b_l_r, d_l_r_r)
on (45 = 11)
) T2(e_l_r, d_l_r, b_l_r_r, d_l_r_r_r)
on (e_l_r > d_l)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test48exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l, b_r
from (
Select c, b
from p4
where (a > ((80 * 55) + (a * 37)))
) T1(c_l, b_l)
left join (
Select b
from p2
where ((58 + 89) < 93)
) T2(b_r)
on (73 > 69)
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
Select d_l, b_l_r
from (
Select d
from p3
where (14 = e)
) T1(d_l)
left join (
Select e_l, b_l, c_r, b_r
from (
Select e, b
from p5
where (27 = 73)
) T1(e_l, b_l)
left join (
Select e, c, b
from p2
where (31 = 36)
) T2(e_r, c_r, b_r)
on (((b_l - 94) < (29 + 27)) OR (((((c_r * b_l) - (32 * b_r)) - e_l) - (b_r + 67)) = 94))
) T2(e_l_r, b_l_r, c_r_r, b_r_r)
on ((b_l_r = 95) OR ((3 = d_l) AND (b_l_r = (0 + (d_l + 12)))))
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
Select e_l, d_l, a_r
from (
Select e, b, d
from p3
where (b = 82)
) T1(e_l, b_l, d_l)
left join (
Select a
from p3
where ((d > c) OR (((4 - 42) < 60) OR (e > (60 * (e - c)))))
) T2(a_r)
on (((66 * 76) < e_l) AND (((e_l - 41) > 41) AND (e_l < 0)))
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
    #**************
    _testmgr.testcase_end(desc)

