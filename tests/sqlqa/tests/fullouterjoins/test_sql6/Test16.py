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
    
def test001(desc="""Joins Set 16"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, c_r, a_r
from (
Select a
from p1
where ((b = 31) OR ((86 = (67 + 17)) AND (92 = a)))
) T1(a_l)
full join (
Select c, a
from p3
where ((c - (1 - (57 * (78 * c)))) = b)
) T2(c_r, a_r)
on (a_l = 43)
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
Select d_r_l, e_r
from (
Select d_r_l, e_l_l, d_r
from (
Select e_l, d_r
from (
Select e, d
from p3
where (40 > d)
) T1(e_l, d_l)
left join (
Select b, d
from p5
where ((d = 5) AND (((d - 6) + c) < 67))
) T2(b_r, d_r)
on (40 > 6)
) T1(e_l_l, d_r_l)
full join (
Select d
from p1
where (c > 75)
) T2(d_r)
on (d_r_l = e_l_l)
) T1(d_r_l_l, e_l_l_l, d_r_l)
full join (
Select e
from p5
where ((55 = 52) OR (c > d))
) T2(e_r)
on (d_r_l < e_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, d_l_r, e_r_r
from (
Select d
from p3
where (((93 + 33) < 31) AND ((23 + 98) = b))
) T1(d_l)
full join (
Select d_l, e_r, c_r, d_r
from (
Select d
from p2
where (a > (7 * (7 * 83)))
) T1(d_l)
full join (
Select e, c, b, d
from p2
where ((47 = b) AND ((62 * 82) = b))
) T2(e_r, c_r, b_r, d_r)
on ((9 = 70) AND ((e_r - 45) = (63 * 73)))
) T2(d_l_r, e_r_r, c_r_r, d_r_r)
on ((82 - d_l_r) = (e_r_r - d_l))
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
Select d_l, c_r_r
from (
Select e, d
from p5
where (d > e)
) T1(e_l, d_l)
left join (
Select b_l, c_r
from (
Select b
from p5
where ((a * c) = e)
) T1(b_l)
inner join (
Select c, b, d
from p4
where (((a + 55) > d) OR (d > 99))
) T2(c_r, b_r, d_r)
on (49 = b_l)
) T2(b_l_r, c_r_r)
on (d_l < c_r_r)
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
Select b_l, d_l, c_r
from (
Select e, b, d
from p1
where ((8 + 7) > a)
) T1(e_l, b_l, d_l)
full join (
Select e, c, a, d
from p2
where (d > (c + (e * 95)))
) T2(e_r, c_r, a_r, d_r)
on (1 > 24)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_r
from (
Select e, c, a, b
from p4
where (b > a)
) T1(e_l, c_l, a_l, b_l)
full join (
Select d
from p4
where (a > a)
) T2(d_r)
on (e_l = d_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_l, b_r
from (
Select e, c, b, d
from p2
where ((6 < 69) AND (e < 68))
) T1(e_l, c_l, b_l, d_l)
left join (
Select a, b
from p4
where (((50 - c) < 87) OR ((((d * (b * b)) + d) < b) AND ((d > 32) OR (b = c))))
) T2(a_r, b_r)
on ((b_l > e_l) OR (48 < b_r))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, d_l, d_r_r
from (
Select c, d
from p3
where (54 < c)
) T1(c_l, d_l)
left join (
Select b_l_l_l_l, e_r_l, b_r, d_r
from (
Select b_l_l_l, e_r, a_r, d_r
from (
Select c_l_l, b_l_l, c_r
from (
Select c_l, b_l, c_r, b_r
from (
Select c, a, b
from p5
where (47 = a)
) T1(c_l, a_l, b_l)
inner join (
Select c, b
from p2
where (((c * 19) < a) AND ((a < ((b * 42) * c)) OR (((a * 30) = 65) OR (((99 + a) = e) OR (36 < 36)))))
) T2(c_r, b_r)
on (30 = (b_l * 48))
) T1(c_l_l, b_l_l, c_r_l, b_r_l)
inner join (
Select c, a
from p3
where (((3 + (c * b)) = a) AND (27 = (5 + 53)))
) T2(c_r, a_r)
on ((c_l_l < c_r) OR (c_l_l > c_l_l))
) T1(c_l_l_l, b_l_l_l, c_r_l)
left join (
Select e, a, d
from p2
where (c < 44)
) T2(e_r, a_r, d_r)
on (((18 + 11) > e_r) AND ((99 * (60 + 46)) = d_r))
) T1(b_l_l_l_l, e_r_l, a_r_l, d_r_l)
inner join (
Select c, b, d
from p2
where (((((d - 84) + c) + 54) < 13) OR (c > e))
) T2(c_r, b_r, d_r)
on ((((69 + 59) + 46) < 2) OR ((d_r = 21) AND ((25 = b_l_l_l_l) AND (e_r_l < 69))))
) T2(b_l_l_l_l_r, e_r_l_r, b_r_r, d_r_r)
on (c_l > d_r_r)
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
Select e_l, e_l_r
from (
select e
from (
Select e
from p1
where (c < e)
) T1
union all
select d
from (
Select d
from p4
where (59 = 23)
) T2
) T1(e_l)
left join (
Select e_l, c_l, e_l_l_r
from (
Select e, c, a
from p2
where (42 < ((b + e) * 39))
) T1(e_l, c_l, a_l)
left join (
Select e_l_l, c_r_l, a_r_r
from (
select e_l, c_r
from (
Select e_l, c_r
from (
Select e
from p5
where ((29 > 59) OR (e < a))
) T1(e_l)
left join (
Select c
from p2
where (27 < b)
) T2(c_r)
on (25 < (c_r + (95 - c_r)))
) T1
union all
select d_r_l, b_r
from (
Select d_r_l, b_r, d_r
from (
Select a_l, b_r, d_r
from (
Select a
from p3
where (d < (a - 11))
) T1(a_l)
inner join (
Select b, d
from p1
where ((e = e) OR (49 = e))
) T2(b_r, d_r)
on ((a_l > (27 * 50)) AND (a_l > 21))
) T1(a_l_l, b_r_l, d_r_l)
inner join (
Select b, d
from p4
where (73 > 85)
) T2(b_r, d_r)
on (53 = 9)
) T2
) T1(e_l_l, c_r_l)
inner join (
Select c_l, a_r
from (
Select c, d
from p1
where ((49 + 40) < 73)
) T1(c_l, d_l)
full join (
Select c, a
from p3
where (13 = 65)
) T2(c_r, a_r)
on ((c_l = (32 - 98)) OR (a_r < 18))
) T2(c_l_r, a_r_r)
on (a_r_r = 90)
) T2(e_l_l_r, c_r_l_r, a_r_r_r)
on (e_l_l_r < (e_l_l_r * e_l_l_r))
) T2(e_l_r, c_l_r, e_l_l_r_r)
on (e_l > e_l_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l_l, d_r_l, a_r
from (
Select e_l, c_l, e_r, d_r
from (
select e, c, d
from (
Select e, c, d
from p5
where ((e > ((86 * (b - a)) * (e - 59))) OR (c > 35))
) T1
union all
select a, b, d
from (
Select a, b, d
from p5
where ((62 + 91) = 97)
) T2
) T1(e_l, c_l, d_l)
left join (
Select e, a, d
from p2
where ((59 = b) AND ((97 < 34) AND (c < e)))
) T2(e_r, a_r, d_r)
on ((((e_r + (d_r * 2)) * (64 + e_l)) * e_r) < (d_r + e_r))
) T1(e_l_l, c_l_l, e_r_l, d_r_l)
full join (
Select e, a
from p3
where ((51 < (e - c)) OR ((d > b) AND (82 = (((c * e) + a) * 69))))
) T2(e_r, a_r)
on (25 = 26)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_r_r
from (
Select a, d
from p2
where (a = 1)
) T1(a_l, d_l)
left join (
Select c_r_l_l, b_r
from (
Select c_l_l, c_r_l, d_l_l, c_l_r, e_r_r
from (
Select c_l, d_l, c_r, b_r
from (
Select c, d
from p1
where (b < (a + 39))
) T1(c_l, d_l)
full join (
Select c, b
from p3
where ((36 > 61) OR (45 > (b + 47)))
) T2(c_r, b_r)
on ((((84 + (c_r + 26)) + b_r) + 90) > c_r)
) T1(c_l_l, d_l_l, c_r_l, b_r_l)
left join (
Select c_l, e_r, d_r
from (
Select c, b
from p1
where ((a = 17) OR (((18 + d) * 39) = 38))
) T1(c_l, b_l)
left join (
Select e, a, b, d
from p1
where (((38 * (a + 89)) - 85) = (c + a))
) T2(e_r, a_r, b_r, d_r)
on (((92 - d_r) > c_l) AND ((18 * 7) = d_r))
) T2(c_l_r, e_r_r, d_r_r)
on (20 > 74)
) T1(c_l_l_l, c_r_l_l, d_l_l_l, c_l_r_l, e_r_r_l)
left join (
Select b, d
from p3
where ((e = 84) AND (d = 73))
) T2(b_r, d_r)
on (87 = 55)
) T2(c_r_l_l_r, b_r_r)
on ((32 < b_r_r) AND ((b_r_r * 34) = 96))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_r_l, d_r_r, d_l_r
from (
Select b_l, c_r, d_r
from (
select a, b
from (
Select a, b
from p1
where (67 = 87)
) T1
union all
select e_r_l, b_r
from (
Select e_r_l, b_r, d_r
from (
Select d_l, e_r
from (
Select d
from p3
where ((d > d) AND ((e - e) < 21))
) T1(d_l)
inner join (
Select e, c
from p4
where (b = 66)
) T2(e_r, c_r)
on (d_l = 76)
) T1(d_l_l, e_r_l)
left join (
Select b, d
from p4
where (((12 * 15) - 11) < (a + c))
) T2(b_r, d_r)
on ((d_r < (76 + d_r)) OR ((57 - 1) > 58))
) T2
) T1(a_l, b_l)
left join (
Select c, d
from p5
where (c = a)
) T2(c_r, d_r)
on (((c_r - 7) > (d_r + 40)) OR (b_l = (b_l * 15)))
) T1(b_l_l, c_r_l, d_r_l)
left join (
select d_l, d_r
from (
Select d_l, d_r
from (
select a, d
from (
Select a, d
from p3
where ((98 = e) OR ((a = (a * c)) OR ((c = d) AND ((b * 90) = 96))))
) T1
union all
select c, a
from (
Select c, a, b
from p4
where ((a = (d + 27)) OR (60 = 92))
) T2
) T1(a_l, d_l)
left join (
select d
from (
Select d
from p5
where (d = 49)
) T1
union all
select c
from (
Select c, b, d
from p3
where (c = 45)
) T2
) T2(d_r)
on (10 = 9)
) T1
union all
select a, d
from (
Select a, d
from p1
where ((b > (b * a)) AND ((62 - (d + (e + 90))) < (e - 87)))
) T2
) T2(d_l_r, d_r_r)
on (d_r_l = 50)
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
Select a_l, a_r
from (
Select a
from p2
where ((b > (e + a)) OR ((11 - (59 + 41)) = 12))
) T1(a_l)
left join (
Select a
from p1
where (49 > c)
) T2(a_r)
on (((a_r * 75) - a_r) = 20)
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
Select e_l, a_l, c_r
from (
Select e, c, a
from p2
where (10 > 35)
) T1(e_l, c_l, a_l)
left join (
Select c
from p2
where ((((a * a) + a) < b) AND (36 = b))
) T2(c_r)
on (a_l = (a_l * c_r))
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
Select d_l_l, e_r, b_r
from (
Select d_l, c_r
from (
Select a, d
from p4
where (6 = 50)
) T1(a_l, d_l)
inner join (
Select e, c
from p1
where ((c < (a * d)) AND (39 = 37))
) T2(e_r, c_r)
on (18 > (c_r - c_r))
) T1(d_l_l, c_r_l)
left join (
Select e, b
from p5
where ((b = (d + (42 * b))) OR ((c = 59) OR (65 < 46)))
) T2(e_r, b_r)
on (52 = (b_r - 30))
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
Select a_l, d_l, a_r, b_r
from (
Select a, d
from p4
where (((17 * b) * c) = c)
) T1(a_l, d_l)
full join (
Select a, b, d
from p2
where (e = ((e * 58) - 23))
) T2(a_r, b_r, d_r)
on (((b_r + 97) = a_l) OR (a_r = b_r))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, e_r, a_r, d_r
from (
Select e, a, b
from p4
where ((57 > 81) OR (e > b))
) T1(e_l, a_l, b_l)
full join (
Select e, a, d
from p1
where ((82 * 30) > ((18 - (c - 22)) + 0))
) T2(e_r, a_r, d_r)
on (34 < 90)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, c_r
from (
Select a
from p3
where (97 = 7)
) T1(a_l)
full join (
Select c
from p1
where (((21 - b) = ((d * (0 - 81)) * 16)) AND (39 = (a + 23)))
) T2(c_r)
on ((70 + 51) = 73)
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
Select e_l_l, d_l_l_r, c_r_l_r
from (
Select e_l, b_r
from (
Select e, c, b
from p5
where (90 = c)
) T1(e_l, c_l, b_l)
left join (
select b
from (
Select b
from p2
where ((c < 36) OR (e > a))
) T1
union all
select c
from (
Select c
from p5
where ((a = 77) OR (((59 + c) * (c * d)) = (a - c)))
) T2
) T2(b_r)
on ((90 + e_l) < b_r)
) T1(e_l_l, b_r_l)
full join (
Select c_r_l, d_l_l, c_r_r, d_l_r
from (
Select d_l, e_r, c_r, d_r
from (
Select d
from p2
where (((a * ((65 - e) + a)) = (e - e)) OR (a > 87))
) T1(d_l)
left join (
Select e, c, d
from p4
where (57 = d)
) T2(e_r, c_r, d_r)
on (26 > c_r)
) T1(d_l_l, e_r_l, c_r_l, d_r_l)
inner join (
Select d_l, c_r, d_r
from (
Select b, d
from p4
where (b < e)
) T1(b_l, d_l)
left join (
Select c, d
from p3
where (13 = (c + b))
) T2(c_r, d_r)
on (d_r = 94)
) T2(d_l_r, c_r_r, d_r_r)
on ((79 = 29) OR (30 < d_l_l))
) T2(c_r_l_r, d_l_l_r, c_r_r_r, d_l_r_r)
on ((32 < e_l_l) OR ((91 > d_l_l_r) OR (c_r_l_r = 19)))
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
Select c_l_l_l, a_r_l_l, e_l_r, d_l_r
from (
Select c_l_l, a_r_l, d_r
from (
Select c_l, a_r, b_r, d_r
from (
Select c
from p1
where (21 > 13)
) T1(c_l)
full join (
Select e, a, b, d
from p3
where (22 = 49)
) T2(e_r, a_r, b_r, d_r)
on ((d_r < c_l) OR ((b_r = 17) AND (((d_r + b_r) - (a_r - 76)) = d_r)))
) T1(c_l_l, a_r_l, b_r_l, d_r_l)
full join (
select c, a, b, d
from (
Select c, a, b, d
from p2
where ((e + 75) = 55)
) T1
union all
select e_l, d_l, e_r, b_r
from (
Select e_l, d_l, e_r, b_r
from (
Select e, d
from p3
where (((b * 54) * b) = 40)
) T1(e_l, d_l)
inner join (
Select e, a, b
from p2
where (71 = 21)
) T2(e_r, a_r, b_r)
on ((34 = 71) OR (d_l = 31))
) T2
) T2(c_r, a_r, b_r, d_r)
on ((((59 + 17) - c_l_l) - c_l_l) = a_r_l)
) T1(c_l_l_l, a_r_l_l, d_r_l)
left join (
select e_l, d_l
from (
Select e_l, d_l, d_r
from (
Select e, d
from p1
where (d = 28)
) T1(e_l, d_l)
left join (
Select d
from p5
where (8 < a)
) T2(d_r)
on ((38 = 28) OR ((18 = (d_r * (96 - (d_r + e_l)))) AND (d_l = (80 * d_l))))
) T1
union all
select c, a
from (
Select c, a
from p1
where ((56 = 87) OR (d < c))
) T2
) T2(e_l_r, d_l_r)
on (d_l_r = ((85 - e_l_r) + d_l_r))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #***********************************************
    _testmgr.testcase_end(desc)

