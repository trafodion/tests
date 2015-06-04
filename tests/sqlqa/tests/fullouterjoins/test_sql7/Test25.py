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
    
def test001(desc="""Joins Set 25"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_l, d_r
from (
select e, a
from (
Select e, a
from p3
where (a = 78)
) T1
union all
select e_l, a_l
from (
Select e_l, a_l, a_r, b_r
from (
Select e, a, d
from p2
where (c > d)
) T1(e_l, a_l, d_l)
full join (
Select a, b, d
from p3
where ((b = a) AND ((b = c) OR (c > (7 * d))))
) T2(a_r, b_r, d_r)
on (a_r = b_r)
) T2
) T1(e_l, a_l)
inner join (
Select c, d
from p2
where ((d < a) AND ((a = c) AND ((74 + d) > b)))
) T2(c_r, d_r)
on (d_r = 2)
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
Select a_l, d_l, c_r, a_r
from (
Select a, d
from p1
where ((37 < 37) OR ((d = d) AND (((75 - (13 + (92 - c))) = 11) OR ((67 + 10) < (91 * a)))))
) T1(a_l, d_l)
left join (
Select c, a, d
from p4
where (e = d)
) T2(c_r, a_r, d_r)
on (19 > d_l)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_l, b_r
from (
Select c, a, d
from p2
where (d > a)
) T1(c_l, a_l, d_l)
inner join (
Select b
from p1
where ((e + c) < 79)
) T2(b_r)
on (b_r < 14)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_r, d_r
from (
Select c
from p3
where (((a + 19) = a) AND ((67 = c) AND (((e + 23) - a) = c)))
) T1(c_l)
left join (
Select a, d
from p5
where (17 < 56)
) T2(a_r, d_r)
on (a_r = (d_r + a_r))
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
Select c_l, a_r
from (
select c
from (
Select c, b
from p4
where (40 = 73)
) T1
union all
select e
from (
select e
from (
Select e, c, b
from p1
where (45 > 87)
) T1
union all
select d
from (
Select d
from p1
where ((38 > 0) OR ((55 < ((95 + (78 - ((b - b) + 11))) * (d + b))) AND ((46 > (b + (60 * d))) AND (((62 + a) < ((e - 70) - c)) OR (c > 3)))))
) T2
) T2
) T1(c_l)
full join (
Select a
from p5
where ((d * (d * d)) = 72)
) T2(a_r)
on (26 = (69 * c_l))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, e_l_r, d_r_r, c_r_r, e_r_r
from (
Select e, a
from p3
where ((51 > (29 + ((c + b) + a))) OR (b > b))
) T1(e_l, a_l)
left join (
Select e_l, e_r, c_r, d_r
from (
Select e
from p4
where (b < b)
) T1(e_l)
inner join (
Select e, c, d
from p3
where (b > b)
) T2(e_r, c_r, d_r)
on ((e_l > 53) AND (26 = c_r))
) T2(e_l_r, e_r_r, c_r_r, d_r_r)
on (e_l > 72)
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, d_l_r
from (
Select c
from p1
where (((c + b) < 88) OR ((e - 14) = 41))
) T1(c_l)
full join (
select d_l
from (
Select d_l, b_r, d_r
from (
Select d
from p5
where (((a - e) - c) = b)
) T1(d_l)
full join (
Select b, d
from p4
where (63 > 30)
) T2(b_r, d_r)
on (b_r = (8 * d_r))
) T1
union all
select c
from (
Select c
from p4
where (d > ((b * (e - 72)) * d))
) T2
) T2(d_l_r)
on (c_l = c_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l, b_r
from (
Select c, b
from p3
where (15 < c)
) T1(c_l, b_l)
left join (
Select b
from p2
where (c > d)
) T2(b_r)
on ((c_l = c_l) AND ((81 * (c_l - 96)) = 64))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, c_r_r, e_r_r, d_l_r
from (
Select e, b, d
from p5
where (91 = c)
) T1(e_l, b_l, d_l)
left join (
Select d_l, e_r, c_r
from (
select d
from (
Select d
from p1
where (d < e)
) T1
union all
select c
from (
Select c, a
from p2
where (b < b)
) T2
) T1(d_l)
left join (
select e, c
from (
Select e, c
from p2
where (60 = c)
) T1
union all
select c_l, d_r
from (
Select c_l, d_r
from (
Select e, c, d
from p1
where (e = (10 * 28))
) T1(e_l, c_l, d_l)
left join (
select a, d
from (
Select a, d
from p4
where (b = 46)
) T1
union all
select c, a
from (
select c, a
from (
Select c, a
from p3
where ((e > a) AND (72 < 21))
) T1
union all
select a, b
from (
Select a, b
from p4
where (e = a)
) T2
) T2
) T2(a_r, d_r)
on (10 = d_r)
) T2
) T2(e_r, c_r)
on (63 = e_r)
) T2(d_l_r, e_r_r, c_r_r)
on (71 = d_l_r)
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
Select c_l_l, a_r_r_l, d_l_l, a_r
from (
Select c_l, d_l, a_r_r, e_r_r, b_l_r
from (
Select c, a, b, d
from p1
where ((c > (a * e)) OR (e = (85 + 26)))
) T1(c_l, a_l, b_l, d_l)
left join (
Select e_l, b_l, e_r, a_r
from (
Select e, a, b
from p2
where ((b * e) = 83)
) T1(e_l, a_l, b_l)
full join (
Select e, a
from p2
where ((c + 66) = 81)
) T2(e_r, a_r)
on (((5 + 86) = (e_l - 80)) OR (a_r = b_l))
) T2(e_l_r, b_l_r, e_r_r, a_r_r)
on (66 = 80)
) T1(c_l_l, d_l_l, a_r_r_l, e_r_r_l, b_l_r_l)
inner join (
select a
from (
Select a
from p3
where (26 = e)
) T1
union all
select d
from (
Select d
from p1
where (d = 24)
) T2
) T2(a_r)
on (28 = d_l_l)
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
Select e_l, b_l, e_r, c_r
from (
Select e, b
from p3
where (d > e)
) T1(e_l, b_l)
left join (
Select e, c, b
from p3
where ((c > d) AND (d < b))
) T2(e_r, c_r, b_r)
on (e_l > c_r)
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
Select a, b
from p1
where (41 = c)
) T1(a_l, b_l)
full join (
select c, b
from (
Select c, b
from p2
where (a = d)
) T1
union all
select c, a
from (
Select c, a, d
from p4
where (81 < 0)
) T2
) T2(c_r, b_r)
on ((39 > 60) AND ((c_r - (84 - ((b_l * b_l) - (c_r - 22)))) = 42))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_l, d_l, c_r, a_r
from (
Select c, a, d
from p4
where (c = (1 * (d * (74 + 41))))
) T1(c_l, a_l, d_l)
left join (
select c, a
from (
Select c, a
from p1
where (56 = 42)
) T1
union all
select e, d
from (
Select e, d
from p4
where (e > e)
) T2
) T2(c_r, a_r)
on (74 = (5 - d_l))
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, c_l_l_r, a_l_r_r
from (
Select a
from p5
where (d > e)
) T1(a_l)
left join (
Select c_l_l, a_l_r, a_l_r_r, e_l_r
from (
select c_l
from (
Select c_l, c_r, b_r
from (
Select e, c, d
from p5
where (c = d)
) T1(e_l, c_l, d_l)
inner join (
select c, b
from (
Select c, b
from p3
where ((45 = ((d * b) + 90)) AND ((e = 51) OR ((b = a) OR (e < e))))
) T1
union all
select e, b
from (
Select e, b
from p4
where (((96 - b) * e) > (3 - e))
) T2
) T2(c_r, b_r)
on (b_r = (68 - b_r))
) T1
union all
select d
from (
Select d
from p3
where ((d > 71) AND (17 = 69))
) T2
) T1(c_l_l)
left join (
Select e_l, a_l, a_l_r, d_r_r
from (
Select e, a
from p4
where (((d * d) > (61 + (c * 83))) OR (50 = a))
) T1(e_l, a_l)
left join (
Select a_l, d_r
from (
Select a
from p1
where ((65 = ((e - 39) - c)) AND (d = (82 + e)))
) T1(a_l)
left join (
Select d
from p1
where (25 > c)
) T2(d_r)
on (90 = d_r)
) T2(a_l_r, d_r_r)
on ((40 > (80 + a_l)) OR (((e_l * a_l) = a_l) OR ((a_l_r = d_r_r) OR (71 = 62))))
) T2(e_l_r, a_l_r, a_l_r_r, d_r_r_r)
on ((22 = 57) AND ((35 < 80) AND (30 > 38)))
) T2(c_l_l_r, a_l_r_r, a_l_r_r_r, e_l_r_r)
on (c_l_l_r > c_l_l_r)
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
Select c_l, d_l, e_r, b_r
from (
Select c, d
from p3
where ((27 > e) AND ((47 + b) > 21))
) T1(c_l, d_l)
inner join (
Select e, b, d
from p5
where (21 = d)
) T2(e_r, b_r, d_r)
on (b_r = 69)
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
Select c_l, e_l_r, d_l_r_r
from (
Select c, a, d
from p4
where (80 = 34)
) T1(c_l, a_l, d_l)
left join (
Select e_l, d_l_r
from (
Select e, c, d
from p2
where ((72 = 3) OR (c > (84 + c)))
) T1(e_l, c_l, d_l)
left join (
Select d_l, c_l_r, d_l_r
from (
Select e, a, d
from p1
where ((d < (a * 8)) OR (94 < 63))
) T1(e_l, a_l, d_l)
inner join (
select c_l, d_l
from (
Select c_l, d_l, e_r, d_r
from (
Select e, c, d
from p5
where ((b + 59) = 25)
) T1(e_l, c_l, d_l)
left join (
select e, d
from (
select e, d
from (
Select e, d
from p4
where (a < c)
) T1
union all
select e_l, b_l
from (
Select e_l, b_l, d_r
from (
Select e, c, b
from p5
where (((a * a) = d) OR ((e = b) AND (29 = e)))
) T1(e_l, c_l, b_l)
inner join (
Select d
from p4
where (((e - (6 + d)) = c) OR (d < b))
) T2(d_r)
on ((e_l = b_l) AND (e_l = (55 - d_r)))
) T2
) T1
union all
select e, b
from (
Select e, b
from p3
where ((b < e) AND ((((91 * a) + e) * 85) > a))
) T2
) T2(e_r, d_r)
on (d_l = 9)
) T1
union all
select e, c
from (
Select e, c
from p5
where ((8 * 22) > ((81 - b) + e))
) T2
) T2(c_l_r, d_l_r)
on ((12 = (55 - 81)) OR ((d_l * c_l_r) = 41))
) T2(d_l_r, c_l_r_r, d_l_r_r)
on (d_l_r = 62)
) T2(e_l_r, d_l_r_r)
on ((c_l = 99) AND (28 < d_l_r_r))
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
Select b_l, d_l, c_l_r, b_r_r
from (
Select e, c, b, d
from p2
where (d = 70)
) T1(e_l, c_l, b_l, d_l)
left join (
Select c_l, b_r
from (
Select c, a, b, d
from p1
where (c < 53)
) T1(c_l, a_l, b_l, d_l)
left join (
Select a, b
from p4
where (b = 60)
) T2(a_r, b_r)
on (0 = 68)
) T2(c_l_r, b_r_r)
on (d_l < 9)
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
Select a_l, d_l, c_r, b_r, d_r
from (
Select e, a, d
from p2
where ((40 > 91) OR ((35 = a) AND ((c - 81) = c)))
) T1(e_l, a_l, d_l)
full join (
Select c, b, d
from p2
where (80 > e)
) T2(c_r, b_r, d_r)
on (42 > (b_r + d_r))
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, c_r, a_r, b_r
from (
Select a
from p2
where ((c > 14) AND (51 > e))
) T1(a_l)
inner join (
Select c, a, b
from p4
where ((((b * d) * (33 - 27)) = d) OR (e > 66))
) T2(c_r, a_r, b_r)
on (31 < 66)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, d_r
from (
Select c
from p1
where (a = b)
) T1(c_l)
left join (
Select c, d
from p2
where ((b > ((26 + 20) - ((d * e) - (43 + 91)))) OR (((52 * c) = 24) AND ((c = e) OR ((c < 77) AND (90 = 31)))))
) T2(c_r, d_r)
on (90 > d_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #**********************************************
    _testmgr.testcase_end(desc)

