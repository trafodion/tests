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
    
def test001(desc="""Joins Set 35"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_r_l, d_l_l, e_r
from (
Select b_l, d_l, e_r, d_r
from (
Select b, d
from p5
where (((c + (39 + 96)) - 0) > (69 + 31))
) T1(b_l, d_l)
left join (
Select e, d
from p4
where ((((21 + (e - 36)) * c) = b) AND ((28 < 12) AND ((27 < (a + e)) OR (e > 45))))
) T2(e_r, d_r)
on (93 = d_l)
) T1(b_l_l, d_l_l, e_r_l, d_r_l)
left join (
select e
from (
Select e, b
from p2
where (((a - 28) * (a - 89)) = 16)
) T1
union all
select b
from (
Select b
from p1
where (c = c)
) T2
) T2(e_r)
on ((56 + (63 + ((d_l_l - d_l_l) - d_l_l))) < 91)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, c_r, a_r, b_r
from (
Select a
from p2
where ((8 = a) OR ((((a + (c + b)) * 52) = c) AND ((43 - c) = d)))
) T1(a_l)
left join (
Select c, a, b
from p3
where ((31 * a) < 86)
) T2(c_r, a_r, b_r)
on (39 > c_r)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_l, b_r
from (
select c_l, a_l
from (
Select c_l, a_l, d_l, b_r_l_l_r
from (
Select c, a, d
from p1
where (40 < (28 + a))
) T1(c_l, a_l, d_l)
left join (
Select d_r_l, b_r_l_l, e_r_l, a_r, d_r
from (
Select b_r_l, e_r, d_r
from (
Select e_l, c_l, a_r, b_r
from (
Select e, c, a
from p1
where (b < a)
) T1(e_l, c_l, a_l)
inner join (
Select a, b
from p5
where ((d < a) AND ((52 > 17) OR ((b = 12) OR (((70 * a) < d) OR (b = e)))))
) T2(a_r, b_r)
on (((c_l - (42 - c_l)) + e_l) > (17 + ((b_r + 41) + (6 - e_l))))
) T1(e_l_l, c_l_l, a_r_l, b_r_l)
left join (
Select e, d
from p5
where (a < b)
) T2(e_r, d_r)
on ((23 = b_r_l) AND (89 < b_r_l))
) T1(b_r_l_l, e_r_l, d_r_l)
left join (
Select a, d
from p5
where (d < (b * 59))
) T2(a_r, d_r)
on (62 > a_r)
) T2(d_r_l_r, b_r_l_l_r, e_r_l_r, a_r_r, d_r_r)
on ((a_l < 72) AND (38 = a_l))
) T1
union all
select a, d
from (
Select a, d
from p1
where ((c - 3) = a)
) T2
) T1(c_l_l, a_l_l)
inner join (
Select b
from p3
where (b > 94)
) T2(b_r)
on ((85 - b_r) > b_r)
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
Select c_l, b_l, c_r
from (
Select c, b
from p5
where (85 = c)
) T1(c_l, b_l)
full join (
Select c
from p4
where (((37 + (e + 4)) > (c * ((56 - 66) * 36))) OR (19 < (((51 * e) - 73) * b)))
) T2(c_r)
on (((35 - 69) < (b_l - c_r)) OR ((b_l = 40) AND (c_r = 58)))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_r_l, b_l_l, e_r, a_r
from (
Select b_l, d_r
from (
Select e, a, b
from p4
where ((b = (49 - b)) OR (e = a))
) T1(e_l, a_l, b_l)
full join (
select d
from (
Select d
from p3
where ((b = 70) OR (a < e))
) T1
union all
select c
from (
Select c, a
from p5
where (d < 8)
) T2
) T2(d_r)
on ((24 < 42) AND (((b_l - (7 + 89)) < d_r) AND (36 < b_l)))
) T1(b_l_l, d_r_l)
left join (
select e, a
from (
Select e, a
from p5
where (b = d)
) T1
union all
select c, b
from (
Select c, b
from p1
where (d < 2)
) T2
) T2(e_r, a_r)
on (a_r = b_l_l)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, c_l, e_r, c_r, b_r
from (
Select e, c
from p1
where ((a < e) AND ((79 < d) AND ((81 > 28) AND (e < 33))))
) T1(e_l, c_l)
left join (
Select e, c, b
from p5
where (90 > (17 - (b - 77)))
) T2(e_r, c_r, b_r)
on ((e_l < 88) OR (91 = 35))
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
Select a_l, b_l, a_l_r_l_r, e_l_l_r, e_r_r
from (
Select e, a, b
from p4
where ((41 < 55) OR ((45 < 55) AND (c > b)))
) T1(e_l, a_l, b_l)
left join (
Select a_l_r_l, e_l_l, e_r
from (
Select e_l, a_l_r, c_l_r
from (
Select e, b, d
from p1
where (69 < c)
) T1(e_l, b_l, d_l)
full join (
Select c_l, a_l, e_r, b_r
from (
select c, a
from (
Select c, a
from p1
where (95 = (((77 * e) - 85) + b))
) T1
union all
select e, a
from (
Select e, a, d
from p1
where (c = (80 * 85))
) T2
) T1(c_l, a_l)
left join (
Select e, c, b
from p3
where ((83 > 69) OR (a < e))
) T2(e_r, c_r, b_r)
on (e_r = e_r)
) T2(c_l_r, a_l_r, e_r_r, b_r_r)
on (e_l = c_l_r)
) T1(e_l_l, a_l_r_l, c_l_r_l)
left join (
Select e
from p3
where (e < (b * d))
) T2(e_r)
on (42 = 43)
) T2(a_l_r_l_r, e_l_l_r, e_r_r)
on ((96 > (9 * 36)) OR (((e_r_r + 57) - (68 * a_l)) = b_l))
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, d_l, c_l_l_r, e_r_l_r, e_r_r
from (
Select a, b, d
from p5
where (c = c)
) T1(a_l, b_l, d_l)
left join (
Select c_l_l, e_r_l, e_r
from (
Select c_l, e_r
from (
Select c
from p2
where (b < e)
) T1(c_l)
left join (
select e
from (
Select e, d
from p5
where (84 = c)
) T1
union all
select a
from (
Select a
from p5
where (a = 80)
) T2
) T2(e_r)
on ((c_l > c_l) AND ((((((87 * 14) * e_r) - 89) - e_r) - e_r) = e_r))
) T1(c_l_l, e_r_l)
left join (
Select e, c, a
from p3
where ((4 = a) AND (24 = c))
) T2(e_r, c_r, a_r)
on ((32 = c_l_l) OR ((e_r = (16 + e_r)) AND (85 = c_l_l)))
) T2(c_l_l_r, e_r_l_r, e_r_r)
on ((e_r_l_r = 60) OR ((21 = e_r_r) OR ((84 > (c_l_l_r - 46)) AND (d_l = (13 * e_r_l_r)))))
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, b_r_r, e_l_r
from (
Select b
from p4
where (94 = d)
) T1(b_l)
left join (
Select e_l, b_r
from (
Select e
from p4
where (91 > 61)
) T1(e_l)
inner join (
Select b
from p1
where (22 < ((47 * d) + 24))
) T2(b_r)
on (b_r > (91 * (b_r * 26)))
) T2(e_l_r, b_r_r)
on (59 = b_r_r)
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
Select e_l, c_r, b_r
from (
Select e
from p4
where ((b > e) AND ((66 = 51) OR ((14 = d) AND ((d * 29) = 98))))
) T1(e_l)
inner join (
Select e, c, b
from p4
where ((d - 35) = d)
) T2(e_r, c_r, b_r)
on (80 > e_l)
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
Select e_l_l, e_r_r_l, d_r
from (
Select e_l, c_l_r, e_l_r, e_r_r
from (
Select e, d
from p3
where (a > (59 - 10))
) T1(e_l, d_l)
full join (
Select e_l, c_l, e_r, b_r
from (
Select e, c
from p3
where (b < 59)
) T1(e_l, c_l)
inner join (
Select e, a, b
from p4
where ((43 * 28) > 2)
) T2(e_r, a_r, b_r)
on (4 > b_r)
) T2(e_l_r, c_l_r, e_r_r, b_r_r)
on (((81 + c_l_r) = 33) AND ((18 > 4) AND ((c_l_r = (c_l_r - 92)) AND ((e_l * 28) > c_l_r))))
) T1(e_l_l, c_l_r_l, e_l_r_l, e_r_r_l)
inner join (
Select d
from p4
where ((32 = e) OR (c < 68))
) T2(d_r)
on (d_r = (d_r - 83))
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
Select a_l, e_r
from (
select a
from (
Select a
from p3
where (d > c)
) T1
union all
select e
from (
Select e, a, d
from p2
where ((62 < d) AND ((92 + (28 * e)) = b))
) T2
) T1(a_l)
full join (
select e
from (
Select e
from p1
where (((74 * 10) < (b - b)) AND (a = 79))
) T1
union all
select b
from (
Select b
from p5
where (50 = 70)
) T2
) T2(e_r)
on ((73 = 50) OR ((e_r > 45) OR (a_l = e_r)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_l, b_l, b_r
from (
Select e, a, b, d
from p4
where (((e - 21) - c) < e)
) T1(e_l, a_l, b_l, d_l)
left join (
Select b
from p1
where ((2 < b) OR (((45 - (c - a)) < b) AND (a > (33 - (35 - 10)))))
) T2(b_r)
on (13 = 44)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_r_r
from (
Select a
from p4
where ((a = c) AND ((d > ((a * (76 + c)) * 78)) OR ((e < 34) OR (b > c))))
) T1(a_l)
inner join (
Select c_l, b_l, a_r, d_r
from (
Select c, b
from p5
where (a = a)
) T1(c_l, b_l)
left join (
Select a, d
from p2
where (95 > (86 + 46))
) T2(a_r, d_r)
on (d_r > c_l)
) T2(c_l_r, b_l_r, a_r_r, d_r_r)
on ((34 = d_r_r) OR ((16 * a_l) = a_l))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, c_r
from (
Select e
from p4
where (a < 88)
) T1(e_l)
left join (
Select c
from p1
where (((17 + (e - d)) = 4) OR (52 = 25))
) T2(c_r)
on (16 = e_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, d_l, d_r
from (
Select e, b, d
from p3
where ((7 * e) < b)
) T1(e_l, b_l, d_l)
inner join (
Select a, d
from p5
where (a = 94)
) T2(a_r, d_r)
on (57 = b_l)
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
select c, b
from (
Select c, b
from p5
where ((c - a) = 55)
) T1
union all
select e, d
from (
Select e, d
from p3
where (((d * (73 - (17 + a))) = 4) OR (((c - (13 + 99)) > 35) AND (c < a)))
) T2
) T1(c_l, b_l)
inner join (
Select c, d
from p1
where ((28 = 61) AND (d = e))
) T2(c_r, d_r)
on ((d_r > 40) AND (c_r > d_r))
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
Select c_l, d_l, c_r, a_r
from (
Select c, b, d
from p4
where ((a + 40) > 85)
) T1(c_l, b_l, d_l)
inner join (
Select c, a
from p2
where ((a < c) AND ((17 + 31) > a))
) T2(c_r, a_r)
on (c_r < (66 - c_r))
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
Select a_l_r_r_l, a_l_r
from (
Select a_l, a_l_r_r
from (
Select e, a
from p2
where ((c = 52) AND ((35 = 30) OR ((b + 0) < (d + b))))
) T1(e_l, a_l)
left join (
Select b_l, a_l_r, b_r_r, c_l_r
from (
Select b, d
from p2
where (d > d)
) T1(b_l, d_l)
full join (
Select c_l, a_l, b_r
from (
Select c, a
from p5
where (36 > 60)
) T1(c_l, a_l)
full join (
Select e, b
from p1
where ((82 - 92) = b)
) T2(e_r, b_r)
on ((b_r < c_l) AND (86 < 57))
) T2(c_l_r, a_l_r, b_r_r)
on (59 = 7)
) T2(b_l_r, a_l_r_r, b_r_r_r, c_l_r_r)
on ((a_l_r_r = a_l) AND ((35 > a_l_r_r) OR ((71 - 88) > a_l)))
) T1(a_l_l, a_l_r_r_l)
left join (
Select a_l, e_r
from (
Select a
from p4
where ((76 + 41) = (d + c))
) T1(a_l)
full join (
Select e
from p2
where (a < e)
) T2(e_r)
on ((e_r = 3) OR ((a_l = (29 - e_r)) AND ((55 + ((e_r + 61) * a_l)) = e_r)))
) T2(a_l_r, e_r_r)
on ((a_l_r = a_l_r_r_l) OR ((a_l_r - (31 - 1)) < (a_l_r_r_l + (40 + 23))))
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
Select c_l_l, a_r
from (
Select c_l, d_r_r, c_r_r
from (
Select c, b
from p5
where (c = 82)
) T1(c_l, b_l)
left join (
Select c_l, c_r, d_r
from (
select c
from (
Select c, a, d
from p2
where ((a + b) > a)
) T1
union all
select b
from (
Select b
from p3
where (25 < c)
) T2
) T1(c_l)
inner join (
Select c, d
from p2
where (c = a)
) T2(c_r, d_r)
on (c_l = 8)
) T2(c_l_r, c_r_r, d_r_r)
on ((68 < 40) OR (((d_r_r + 52) = c_l) AND ((77 > 49) AND (c_l > c_r_r))))
) T1(c_l_l, d_r_r_l, c_r_r_l)
inner join (
Select a
from p3
where ((70 - (b - c)) < b)
) T2(a_r)
on ((29 < a_r) OR (67 = (93 - 20)))
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
    #*******************************************
    _testmgr.testcase_end(desc)

