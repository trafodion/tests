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
    
def test001(desc="""Joins Set 46"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, a_r, d_r
from (
Select b
from p1
where (a < e)
) T1(b_l)
inner join (
Select a, d
from p3
where (e = 5)
) T2(a_r, d_r)
on ((31 < 92) AND (a_r = b_l))
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
Select e_l, b_r
from (
select e
from (
select e, b, d
from (
Select e, b, d
from p5
where (a > c)
) T1
union all
select e, c, a
from (
Select e, c, a
from p3
where ((b = (c + c)) AND ((a > e) OR (65 = 94)))
) T2
) T1
union all
select d
from (
Select d
from p2
where (33 > b)
) T2
) T1(e_l)
left join (
Select b
from p1
where (b > 46)
) T2(b_r)
on (27 = 24)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test46exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l, e_r
from (
Select e, c, b
from p2
where (92 = (43 * a))
) T1(e_l, c_l, b_l)
inner join (
Select e, c
from p2
where ((75 = 16) OR (b < 93))
) T2(e_r, c_r)
on (81 < b_l)
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
Select c_l, c_r
from (
Select c, a, b
from p3
where (b = (7 + 78))
) T1(c_l, a_l, b_l)
left join (
Select c
from p4
where (6 < 21)
) T2(c_r)
on (c_r = 87)
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
Select e_l, c_r_r_r
from (
Select e, c, a
from p5
where (10 > 73)
) T1(e_l, c_l, a_l)
left join (
Select e_l, c_r_r, b_l_r
from (
Select e
from p2
where (((e * d) + b) = (1 + 24))
) T1(e_l)
inner join (
Select b_l, c_r
from (
select c, b
from (
Select c, b, d
from p1
where (b = b)
) T1
union all
select a, d
from (
Select a, d
from p2
where (14 < (e - 35))
) T2
) T1(c_l, b_l)
left join (
Select e, c, b, d
from p4
where (e = (42 - a))
) T2(e_r, c_r, b_r, d_r)
on ((c_r * ((c_r + 24) - 34)) = c_r)
) T2(b_l_r, c_r_r)
on (e_l = 86)
) T2(e_l_r, c_r_r_r, b_l_r_r)
on ((3 > e_l) AND (98 < 59))
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
Select c_r_l_l_l, e_r, b_r
from (
Select c_r_l_l, d_r_l_l, e_r, d_r
from (
Select d_r_l, c_r_l, c_l_r
from (
Select c_l, d_l, c_r, d_r
from (
Select c, a, d
from p5
where (d > 24)
) T1(c_l, a_l, d_l)
inner join (
Select c, d
from p3
where (((54 * ((20 + (c + 28)) * e)) = 97) AND (c > c))
) T2(c_r, d_r)
on ((c_l + 79) < 81)
) T1(c_l_l, d_l_l, c_r_l, d_r_l)
full join (
Select c_l, b_l, c_r
from (
Select c, b
from p3
where (e > e)
) T1(c_l, b_l)
left join (
Select c
from p4
where ((9 * (9 + c)) = c)
) T2(c_r)
on (27 = c_r)
) T2(c_l_r, b_l_r, c_r_r)
on (72 = 78)
) T1(d_r_l_l, c_r_l_l, c_l_r_l)
full join (
Select e, b, d
from p4
where (c = 4)
) T2(e_r, b_r, d_r)
on (55 = 54)
) T1(c_r_l_l_l, d_r_l_l_l, e_r_l, d_r_l)
inner join (
select e, b
from (
Select e, b, d
from p2
where (71 > d)
) T1
union all
select c, a
from (
select c, a
from (
Select c, a
from p5
where (11 = 75)
) T1
union all
select e, c
from (
Select e, c
from p5
where ((35 > b) AND (((56 - c) + (87 + (81 + e))) = 12))
) T2
) T2
) T2(e_r, b_r)
on (57 = ((33 - e_r) - c_r_l_l_l))
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
select b
from (
Select b
from p4
where ((66 - e) = d)
) T1
union all
select e
from (
Select e, c, a, b
from p1
where (((46 * 57) < 12) AND (((66 - c) = a) OR (e = e)))
) T2
) T1(b_l)
left join (
Select c, a, b
from p3
where ((71 = ((e * 96) + b)) OR ((a = c) AND ((56 < c) OR (((57 - (43 - b)) > a) AND (b < a)))))
) T2(c_r, a_r, b_r)
on ((51 < 27) AND (43 > 60))
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
Select e_l, c_l, b_r
from (
Select e, c, a, b
from p1
where (a = 78)
) T1(e_l, c_l, a_l, b_l)
inner join (
Select b
from p1
where (b < d)
) T2(b_r)
on ((c_l = 25) AND (e_l > (b_r - 14)))
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
Select b_l, d_l, a_r
from (
Select b, d
from p3
where (d = e)
) T1(b_l, d_l)
full join (
select a
from (
Select a
from p5
where ((7 < 4) AND (69 < 98))
) T1
union all
select a
from (
Select a, d
from p3
where ((81 = a) AND ((7 * c) = a))
) T2
) T2(a_r)
on (a_r = a_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test46exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, e_r
from (
Select c, b
from p3
where ((a = 7) AND ((e > e) AND (24 > a)))
) T1(c_l, b_l)
full join (
Select e, a
from p5
where ((94 < (c * (d - 79))) AND (98 > 41))
) T2(e_r, a_r)
on (72 < e_r)
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
Select c_l, a_r_r, d_r_l_r, e_r_r
from (
Select c
from p1
where (c = 56)
) T1(c_l)
inner join (
Select d_r_l, e_r, a_r
from (
Select c_l, b_l, d_r
from (
Select c, b
from p4
where ((98 = a) OR ((65 > 63) AND (15 > 50)))
) T1(c_l, b_l)
full join (
Select a, d
from p4
where ((21 > c) OR (28 = d))
) T2(a_r, d_r)
on ((2 > 21) AND (c_l = 15))
) T1(c_l_l, b_l_l, d_r_l)
left join (
Select e, a
from p2
where (d = 30)
) T2(e_r, a_r)
on (e_r = a_r)
) T2(d_r_l_r, e_r_r, a_r_r)
on (69 = d_r_l_r)
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
Select d
from p1
where (80 > 10)
) T1(d_l)
full join (
Select b
from p5
where (c = ((((a + c) - ((a - 64) - 58)) - 84) * 59))
) T2(b_r)
on (87 = 52)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test46exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_l, e_r, d_r
from (
Select e, a
from p4
where ((e < e) AND ((d = (39 * 21)) AND (b = (d + (51 + 86)))))
) T1(e_l, a_l)
inner join (
Select e, d
from p2
where ((50 < 88) AND (e < 57))
) T2(e_r, d_r)
on ((78 + e_r) = 17)
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
Select b_l_l_l, b_r
from (
Select b_l_l, e_r_l_l_r
from (
Select b_l, e_l_l_l_l_r
from (
select b
from (
Select b
from p4
where (c < (48 * 84))
) T1
union all
select c
from (
Select c, a, b
from p2
where (94 = d)
) T2
) T1(b_l)
inner join (
Select e_l_l_l_l, c_r, d_r
from (
select e_l_l_l
from (
Select e_l_l_l, a_r, d_r
from (
Select e_l_l, c_r_l, a_r, d_r
from (
Select e_l, c_r
from (
select e
from (
Select e, c, d
from p2
where ((89 = (67 - (32 - d))) OR ((((a - 33) + e) = d) AND ((d > a) AND (82 > d))))
) T1
union all
select a
from (
Select a
from p5
where (d < d)
) T2
) T1(e_l)
inner join (
Select c, a
from p4
where (99 = (54 * 17))
) T2(c_r, a_r)
on ((17 = 59) OR (((c_r - (44 * 28)) * 34) < c_r))
) T1(e_l_l, c_r_l)
inner join (
Select a, d
from p5
where (87 = 18)
) T2(a_r, d_r)
on (19 = (a_r - 1))
) T1(e_l_l_l, c_r_l_l, a_r_l, d_r_l)
full join (
select a, b, d
from (
Select a, b, d
from p2
where (e = (a - 68))
) T1
union all
select d_l, b_l_r_r, c_r_r_r
from (
select d_l, b_l_r_r, c_r_r_r, b_l_r
from (
Select d_l, b_l_r_r, c_r_r_r, b_l_r
from (
Select b, d
from p2
where (15 < 17)
) T1(b_l, d_l)
left join (
Select b_l, c_r_r, b_l_r
from (
Select b
from p2
where ((a < b) OR (b = a))
) T1(b_l)
inner join (
Select b_l, c_r
from (
select b
from (
Select b
from p1
where (11 < c)
) T1
union all
select c
from (
select c, d
from (
select c, d
from (
Select c, d
from p4
where (50 = 83)
) T1
union all
select e, c
from (
Select e, c, b
from p4
where (((b * 31) > 4) AND (c = c))
) T2
) T1
union all
select c_l, a_l_r
from (
select c_l, a_l_r, e_r_r
from (
select c_l, a_l_r, e_r_r
from (
Select c_l, a_l_r, e_r_r
from (
Select c, d
from p5
where ((a * c) > e)
) T1(c_l, d_l)
left join (
Select a_l, e_r
from (
Select a
from p1
where (84 > c)
) T1(a_l)
left join (
Select e, c, a, d
from p2
where ((b < a) OR (63 = 87))
) T2(e_r, c_r, a_r, d_r)
on (1 < 89)
) T2(a_l_r, e_r_r)
on (8 = ((94 - (a_l_r + (75 + 20))) - a_l_r))
) T1
union all
select e, a, d
from (
Select e, a, d
from p5
where (e = 7)
) T2
) T1
union all
select c, a, b
from (
Select c, a, b
from p5
where (c = b)
) T2
) T2
) T2
) T1(b_l)
left join (
Select c, b
from p5
where ((99 * b) < a)
) T2(c_r, b_r)
on (b_l < (c_r - 61))
) T2(b_l_r, c_r_r)
on (65 = 14)
) T2(b_l_r, c_r_r_r, b_l_r_r)
on (((c_r_r_r - 27) > 63) OR (d_l < 43))
) T1
union all
select c, a, b, d
from (
Select c, a, b, d
from p2
where (18 = 46)
) T2
) T2
) T2(a_r, b_r, d_r)
on (71 > 90)
) T1
union all
select b
from (
Select b
from p5
where (29 = 79)
) T2
) T1(e_l_l_l_l)
left join (
Select c, d
from p5
where (80 > (17 + e))
) T2(c_r, d_r)
on (c_r < 87)
) T2(e_l_l_l_l_r, c_r_r, d_r_r)
on (b_l < e_l_l_l_l_r)
) T1(b_l_l, e_l_l_l_l_r_l)
inner join (
select c_l_l_l, e_r_l_l
from (
Select c_l_l_l, e_r_l_l, d_r
from (
Select c_l_l, e_r_l, a_r
from (
select c_l, e_r
from (
Select c_l, e_r, c_r
from (
Select c
from p3
where (d > (73 - d))
) T1(c_l)
inner join (
Select e, c
from p5
where (87 = 61)
) T2(e_r, c_r)
on ((c_l < e_r) OR (32 > 94))
) T1
union all
select c, a
from (
Select c, a
from p5
where (85 > b)
) T2
) T1(c_l_l, e_r_l)
left join (
Select a
from p4
where ((94 * 9) < 44)
) T2(a_r)
on (c_l_l = ((37 - e_r_l) + c_l_l))
) T1(c_l_l_l, e_r_l_l, a_r_l)
left join (
Select c, a, d
from p1
where (24 < 58)
) T2(c_r, a_r, d_r)
on ((94 = c_l_l_l) OR (67 = d_r))
) T1
union all
select c, d
from (
Select c, d
from p3
where (49 = b)
) T2
) T2(c_l_l_l_r, e_r_l_l_r)
on ((3 = 7) OR ((19 * e_r_l_l_r) = e_r_l_l_r))
) T1(b_l_l_l, e_r_l_l_r_l)
inner join (
Select b
from p2
where (b > b)
) T2(b_r)
on ((72 = b_r) AND ((b_l_l_l < ((b_l_l_l + b_l_l_l) + (b_r * b_l_l_l))) OR (b_l_l_l < 9)))
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
Select a_l, b_l, d_l, c_r, d_r
from (
Select a, b, d
from p1
where (79 < e)
) T1(a_l, b_l, d_l)
inner join (
Select e, c, d
from p3
where (78 < (b * 63))
) T2(e_r, c_r, d_r)
on ((25 = (d_r * (d_l - (81 + c_r)))) OR (((c_r - d_r) > 2) AND (b_l > 30)))
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
Select c_l, a_l, d_l, e_r, c_r
from (
Select c, a, b, d
from p3
where (((73 - c) = 74) AND ((66 * (a - d)) < b))
) T1(c_l, a_l, b_l, d_l)
inner join (
Select e, c, d
from p4
where (77 = 80)
) T2(e_r, c_r, d_r)
on ((((((a_l - a_l) + 41) + 39) - c_l) = (12 - 11)) AND ((c_l * 32) = e_r))
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
Select c_l, b_l, d_l, b_r
from (
Select e, c, b, d
from p4
where (93 = c)
) T1(e_l, c_l, b_l, d_l)
full join (
Select b
from p2
where ((((((8 * 24) - 15) * b) + a) < a) AND (a = e))
) T2(b_r)
on ((18 > 96) AND ((92 * 77) > 97))
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
Select a_r_l, d_r_r
from (
Select d_l, c_r, a_r
from (
Select e, d
from p3
where ((85 - 17) = 22)
) T1(e_l, d_l)
left join (
select c, a
from (
Select c, a, d
from p1
where ((43 = ((52 - d) + 57)) AND (23 = c))
) T1
union all
select e_l, c_l
from (
select e_l, c_l
from (
Select e_l, c_l, d_r
from (
Select e, c, a, d
from p2
where (7 < (65 * b))
) T1(e_l, c_l, a_l, d_l)
full join (
select d
from (
Select d
from p1
where ((78 = 45) OR ((73 * 52) = (c + 28)))
) T1
union all
select a
from (
select a
from (
Select a
from p1
where (46 = b)
) T1
union all
select d
from (
Select d
from p1
where (89 = c)
) T2
) T2
) T2(d_r)
on ((d_r = d_r) OR ((((9 * c_l) + 68) = c_l) OR ((d_r = 19) AND (e_l = 42))))
) T1
union all
select e, b
from (
Select e, b
from p2
where (e = d)
) T2
) T2
) T2(c_r, a_r)
on ((((a_r * 51) - d_l) + (d_l - 72)) = c_r)
) T1(d_l_l, c_r_l, a_r_l)
inner join (
Select d_l, d_r
from (
Select a, d
from p2
where ((b = (e - 36)) OR (b > ((71 * a) - (81 * d))))
) T1(a_l, d_l)
full join (
select d
from (
select d
from (
Select d
from p5
where (a < 90)
) T1
union all
select b
from (
Select b, d
from p1
where (d = 8)
) T2
) T1
union all
select c
from (
Select c
from p1
where ((c = 52) OR ((e * 5) = 31))
) T2
) T2(d_r)
on ((38 + 17) < 28)
) T2(d_l_r, d_r_r)
on (d_r_r = d_r_r)
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
Select b_r_l, c_l_l_l, a_r_l_l, c_r_r_r
from (
Select c_l_l, a_r_l, b_r
from (
Select c_l, d_l, a_r, b_r
from (
Select c, d
from p4
where (85 = 55)
) T1(c_l, d_l)
inner join (
Select a, b
from p3
where (c < e)
) T2(a_r, b_r)
on (c_l > (25 * c_l))
) T1(c_l_l, d_l_l, a_r_l, b_r_l)
full join (
select e, c, b
from (
Select e, c, b
from p4
where ((60 < 19) AND (9 < 48))
) T1
union all
select b_l, b_l_r, e_r_r
from (
Select b_l, b_l_r, e_r_r
from (
Select b
from p2
where ((51 = (a * 8)) AND ((c * 15) < c))
) T1(b_l)
full join (
Select b_l, e_r
from (
Select e, b, d
from p5
where (b = 37)
) T1(e_l, b_l, d_l)
full join (
Select e
from p4
where (c = 9)
) T2(e_r)
on (b_l < 84)
) T2(b_l_r, e_r_r)
on (9 > e_r_r)
) T2
) T2(e_r, c_r, b_r)
on ((86 - 51) > 16)
) T1(c_l_l_l, a_r_l_l, b_r_l)
left join (
select c_l, a_l, c_r_r
from (
Select c_l, a_l, c_r_r, e_r_r
from (
Select e, c, a
from p4
where ((e < (31 - b)) OR (a < c))
) T1(e_l, c_l, a_l)
full join (
Select a_l, e_r, c_r, a_r
from (
Select a
from p3
where (d > 50)
) T1(a_l)
full join (
Select e, c, a
from p3
where (b = a)
) T2(e_r, c_r, a_r)
on (44 = 88)
) T2(a_l_r, e_r_r, c_r_r, a_r_r)
on ((9 - c_r_r) = 11)
) T1
union all
select e, b, d
from (
Select e, b, d
from p5
where (((d * b) = 16) OR ((d = d) AND ((d = 70) OR ((d = 28) OR (86 = (b - d))))))
) T2
) T2(c_l_r, a_l_r, c_r_r_r)
on (c_l_l_l = (c_l_l_l - c_l_l_l))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test46exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_l, e_l_r
from (
Select c, a, b, d
from p3
where (e > (c - 51))
) T1(c_l, a_l, b_l, d_l)
left join (
select e_l, b_l
from (
Select e_l, b_l, e_r
from (
Select e, c, a, b
from p3
where ((16 = b) OR (((((e * 61) * (e + d)) * b) > a) OR (64 = 30)))
) T1(e_l, c_l, a_l, b_l)
inner join (
Select e, b
from p4
where (d > (34 * c))
) T2(e_r, b_r)
on (b_l < 87)
) T1
union all
select e, c
from (
Select e, c
from p1
where (a > e)
) T2
) T2(e_l_r, b_l_r)
on (e_l_r = 85)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test46exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #************
    _testmgr.testcase_end(desc)

