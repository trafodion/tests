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
    
def test001(desc="""Joins Set 11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l_l, d_l_l, e_l_r, e_r_r
from (
Select b_l, d_l, a_r
from (
Select b, d
from p2
where ((a = c) OR (13 = e))
) T1(b_l, d_l)
inner join (
Select c, a
from p4
where (a = 56)
) T2(c_r, a_r)
on ((91 - d_l) = 88)
) T1(b_l_l, d_l_l, a_r_l)
inner join (
select e_l, c_l, e_r
from (
Select e_l, c_l, e_r, d_r
from (
Select e, c
from p5
where (39 < d)
) T1(e_l, c_l)
inner join (
Select e, a, d
from p1
where (27 < a)
) T2(e_r, a_r, d_r)
on ((16 > 55) OR (d_r < c_l))
) T1
union all
select e, c, d
from (
select e, c, d
from (
Select e, c, d
from p5
where (a = 59)
) T1
union all
select e, b, d
from (
Select e, b, d
from p3
where ((21 < 63) OR (c = (c * d)))
) T2
) T2
) T2(e_l_r, c_l_r, e_r_r)
on (e_l_r = b_l_l)
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
Select c_l_l, e_l_l, b_r, d_r
from (
Select e_l, c_l, e_r
from (
Select e, c
from p5
where ((16 = d) OR (a > c))
) T1(e_l, c_l)
left join (
select e
from (
select e
from (
Select e, a, b
from p2
where (2 < (59 - d))
) T1
union all
select e
from (
Select e
from p4
where (a < a)
) T2
) T1
union all
select b_l
from (
Select b_l, d_l_r, e_r_r
from (
Select b
from p5
where (d = b)
) T1(b_l)
left join (
select d_l, e_r
from (
Select d_l, e_r
from (
Select d
from p4
where ((b - c) < 35)
) T1(d_l)
left join (
Select e, c
from p5
where ((b + 79) = b)
) T2(e_r, c_r)
on (63 = (e_r + (99 - ((e_r - 52) * e_r))))
) T1
union all
select e, c
from (
Select e, c
from p1
where ((e > (72 - a)) AND (((d * 55) < (a - d)) AND ((e = a) AND ((95 = 84) OR (d = (b * ((((44 * e) + 92) * 69) * (d * b))))))))
) T2
) T2(d_l_r, e_r_r)
on (e_r_r = (44 + d_l_r))
) T2
) T2(e_r)
on (e_l = (32 * e_l))
) T1(e_l_l, c_l_l, e_r_l)
inner join (
Select c, b, d
from p3
where (b > (d + a))
) T2(c_r, b_r, d_r)
on ((48 = 6) OR (c_l_l < 2))
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
Select b_l_r_l, b_l_l, b_r
from (
Select b_l, b_l_r
from (
select c, b, d
from (
Select c, b, d
from p2
where (d = ((d * e) + e))
) T1
union all
select c, a, d
from (
Select c, a, d
from p1
where ((a = b) OR (80 = (e * 68)))
) T2
) T1(c_l, b_l, d_l)
left join (
Select e_l, a_l, b_l, a_r
from (
Select e, a, b
from p1
where (c = 20)
) T1(e_l, a_l, b_l)
left join (
Select a, b
from p4
where (86 < c)
) T2(a_r, b_r)
on (91 = 74)
) T2(e_l_r, a_l_r, b_l_r, a_r_r)
on (b_l_r > 64)
) T1(b_l_l, b_l_r_l)
full join (
Select b
from p5
where (63 = (b + (23 * ((c - 24) + e))))
) T2(b_r)
on (b_l_l = 62)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_r
from (
Select a
from p4
where ((a + 91) = (84 * c))
) T1(a_l)
left join (
Select d
from p2
where ((((d - b) * d) = (d * 3)) OR ((a = c) OR (((b - 66) = d) AND (a = 39))))
) T2(d_r)
on (85 > (d_r + a_l))
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
Select c_l, e_r, b_r
from (
Select c
from p5
where ((99 < b) OR ((a = 95) AND (d = (b * 81))))
) T1(c_l)
inner join (
Select e, b
from p4
where (20 > 94)
) T2(e_r, b_r)
on (e_r = e_r)
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
Select d_l, a_r_r
from (
Select d
from p5
where (78 = c)
) T1(d_l)
inner join (
Select c_l, a_r
from (
select c
from (
Select c
from p5
where (80 < a)
) T1
union all
select c
from (
Select c, a, b
from p5
where (c = 87)
) T2
) T1(c_l)
full join (
select a
from (
select a
from (
Select a
from p1
where ((c = d) AND ((c > 98) OR (53 < a)))
) T1
union all
select c
from (
Select c, d
from p4
where (e = 18)
) T2
) T1
union all
select c_l
from (
Select c_l, a_l, d_l, d_r
from (
Select c, a, d
from p2
where ((b - 10) = b)
) T1(c_l, a_l, d_l)
full join (
Select d
from p1
where ((50 - e) > 58)
) T2(d_r)
on (83 = (d_r * ((d_l - d_l) - 71)))
) T2
) T2(a_r)
on (95 = 97)
) T2(c_l_r, a_r_r)
on ((d_l < a_r_r) AND (d_l = a_r_r))
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
Select e_l, e_r, d_r
from (
select e
from (
select e
from (
Select e
from p5
where ((33 * (c - ((33 * (a + 18)) * 38))) < 14)
) T1
union all
select d
from (
Select d
from p4
where (c = 96)
) T2
) T1
union all
select c
from (
select c, d
from (
Select c, d
from p2
where (66 = 8)
) T1
union all
select e, c
from (
Select e, c, a, b
from p1
where ((d = a) AND (((a + b) > c) AND (94 > b)))
) T2
) T2
) T1(e_l)
left join (
Select e, b, d
from p2
where ((d < 21) AND (73 = 38))
) T2(e_r, b_r, d_r)
on (e_r = e_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, e_r, c_r
from (
Select e, d
from p4
where ((a * a) < 4)
) T1(e_l, d_l)
left join (
Select e, c, b
from p3
where ((d < ((c - c) - (71 - (56 * e)))) OR (c = d))
) T2(e_r, c_r, b_r)
on (c_r < 45)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_l, a_l_r, c_l_r
from (
Select e, b
from p3
where ((d > c) AND (((7 * 92) > d) OR (59 < 44)))
) T1(e_l, b_l)
full join (
Select c_l, a_l, b_r
from (
Select c, a
from p1
where ((d < a) AND ((1 = c) OR (b > (a * c))))
) T1(c_l, a_l)
left join (
Select e, c, b
from p3
where ((c = b) OR (59 = 91))
) T2(e_r, c_r, b_r)
on ((43 > c_l) OR ((a_l = a_l) OR ((b_r - 98) > (77 - 68))))
) T2(c_l_r, a_l_r, b_r_r)
on ((e_l = ((c_l_r - (b_l * 22)) - 30)) AND (c_l_r = (c_l_r - 5)))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_r
from (
Select c
from p3
where (77 = 88)
) T1(c_l)
left join (
select b
from (
select b
from (
select b
from (
Select b
from p1
where ((14 * c) < c)
) T1
union all
select e
from (
Select e, a, d
from p3
where ((34 - 68) > c)
) T2
) T1
union all
select b
from (
Select b
from p5
where (c = 62)
) T2
) T1
union all
select e_l
from (
Select e_l, c_r
from (
Select e
from p1
where (73 < d)
) T1(e_l)
left join (
Select c, b, d
from p4
where ((c = (82 - a)) AND (((79 * (e + 73)) - 78) < b))
) T2(c_r, b_r, d_r)
on (16 = e_l)
) T2
) T2(b_r)
on (b_r > 2)
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
Select e_l_l, c_r_l, e_r, d_r
from (
Select e_l, b_l, d_l, c_r, b_r
from (
Select e, b, d
from p5
where (b > 65)
) T1(e_l, b_l, d_l)
full join (
Select c, b
from p2
where ((d = 49) AND (c = b))
) T2(c_r, b_r)
on (((7 + 21) > 54) OR (5 = 0))
) T1(e_l_l, b_l_l, d_l_l, c_r_l, b_r_l)
inner join (
Select e, d
from p5
where (a = e)
) T2(e_r, d_r)
on ((7 > e_r) OR (((79 * (c_r_l + 34)) < ((44 - e_l_l) * (e_l_l - (56 * (((d_r * e_l_l) - e_l_l) + e_l_l))))) AND ((23 * (c_r_l - e_l_l)) > e_l_l)))
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
Select c_l, e_r, c_r
from (
Select c
from p3
where ((81 - 41) < e)
) T1(c_l)
left join (
Select e, c, b
from p3
where ((36 < 12) AND ((e > c) AND (((53 + 89) < 27) OR (d < 80))))
) T2(e_r, c_r, b_r)
on (35 = (0 + (c_r * c_r)))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l_r_l, e_r, a_r
from (
Select d_l, e_l_r, e_r_r
from (
select d
from (
Select d
from p2
where ((2 = 22) AND (66 = e))
) T1
union all
select e
from (
Select e
from p2
where (((d - e) = ((b * 79) * (a + (c * d)))) OR (23 = e))
) T2
) T1(d_l)
inner join (
Select e_l, a_l, d_l, e_r
from (
Select e, a, d
from p2
where (14 < 33)
) T1(e_l, a_l, d_l)
full join (
select e
from (
Select e, c, b, d
from p3
where (c = (e - (96 + 39)))
) T1
union all
select b
from (
Select b
from p2
where (a = 5)
) T2
) T2(e_r)
on (((d_l + e_r) * (e_l + 91)) = 2)
) T2(e_l_r, a_l_r, d_l_r, e_r_r)
on (24 = (2 - (e_r_r + e_r_r)))
) T1(d_l_l, e_l_r_l, e_r_r_l)
left join (
Select e, c, a, d
from p3
where ((c > 31) AND (a < (1 + b)))
) T2(e_r, c_r, a_r, d_r)
on (64 = 61)
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
Select e_l, b_l, a_r
from (
Select e, b
from p3
where (80 > e)
) T1(e_l, b_l)
full join (
Select a
from p1
where (15 < 73)
) T2(a_r)
on (((59 - e_l) > 46) OR (97 = (12 - a_r)))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, c_r_r
from (
Select b
from p2
where (94 > e)
) T1(b_l)
left join (
Select e_l, b_l, c_r
from (
Select e, a, b
from p5
where ((55 - 67) > 79)
) T1(e_l, a_l, b_l)
inner join (
Select e, c, a
from p4
where (((55 * (a + (b - (d - a)))) = a) OR ((64 = 16) OR (e = 90)))
) T2(e_r, c_r, a_r)
on (6 = (e_l + b_l))
) T2(e_l_r, b_l_r, c_r_r)
on ((28 + c_r_r) = 2)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_r
from (
Select e, c, a
from p5
where (c = (e - c))
) T1(e_l, c_l, a_l)
left join (
Select a
from p3
where (57 = 51)
) T2(a_r)
on (87 = 7)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l_r_r, d_r_r_r_l_r
from (
Select c
from p3
where (93 < 50)
) T1(c_l)
left join (
Select e_l_l, e_l_r_r_l, d_r_r_r_l, b_l_r
from (
Select e_l, e_l_r_r, d_r_r_r
from (
Select e, d
from p2
where (5 < c)
) T1(e_l, d_l)
full join (
Select e_l, e_l_r, d_r_r
from (
select e
from (
Select e, a, d
from p5
where (e = e)
) T1
union all
select a
from (
Select a
from p1
where (83 > (b + e))
) T2
) T1(e_l)
full join (
Select e_l, d_r
from (
Select e
from p3
where ((e = 98) AND (15 = e))
) T1(e_l)
left join (
Select d
from p5
where (40 < e)
) T2(d_r)
on (e_l > (84 + (e_l + d_r)))
) T2(e_l_r, d_r_r)
on (39 > (84 * 62))
) T2(e_l_r, e_l_r_r, d_r_r_r)
on ((e_l < (10 * (96 + 71))) OR ((e_l_r_r < (24 * e_l)) AND ((95 = 92) AND (87 < 97))))
) T1(e_l_l, e_l_r_r_l, d_r_r_r_l)
left join (
Select c_l, b_l, b_r
from (
Select c, b
from p1
where (26 = 2)
) T1(c_l, b_l)
full join (
Select b
from p2
where (c = 38)
) T2(b_r)
on (((b_l + (22 - 70)) > c_l) OR (b_r = (c_l + c_l)))
) T2(c_l_r, b_l_r, b_r_r)
on (16 < d_r_r_r_l)
) T2(e_l_l_r, e_l_r_r_l_r, d_r_r_r_l_r, b_l_r_r)
on (d_r_r_r_l_r > 5)
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
Select a_l_l, c_r_r_l, c_r
from (
Select a_l, c_r_r
from (
select a
from (
Select a
from p2
where ((d = b) OR ((a = (a + b)) AND (c < 99)))
) T1
union all
select a_l
from (
Select a_l, c_r
from (
select a
from (
Select a, b, d
from p4
where ((b = 70) OR (a = b))
) T1
union all
select b
from (
Select b
from p5
where (75 = 7)
) T2
) T1(a_l)
left join (
Select c
from p4
where ((57 = (88 - (d + c))) OR (11 = a))
) T2(c_r)
on ((a_l = a_l) AND ((a_l < a_l) AND ((c_r = 57) AND (24 = a_l))))
) T2
) T1(a_l)
left join (
Select d_l, c_r
from (
Select e, d
from p5
where (b < e)
) T1(e_l, d_l)
full join (
Select c, b
from p3
where ((a * 74) = c)
) T2(c_r, b_r)
on (d_l = 89)
) T2(d_l_r, c_r_r)
on (a_l < a_l)
) T1(a_l_l, c_r_r_l)
left join (
Select c
from p4
where ((((b * a) * 68) = b) AND (((d * (b + (91 * 72))) = 62) OR (((35 + c) < d) AND (14 > 29))))
) T2(c_r)
on ((c_r * 34) > (76 - 21))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_r
from (
Select c
from p1
where ((77 - (((d + b) * c) + e)) < ((12 - d) - (2 * 32)))
) T1(c_l)
inner join (
select c, a, b
from (
Select c, a, b
from p5
where ((c > 48) OR (57 < d))
) T1
union all
select e, a, b
from (
Select e, a, b, d
from p3
where ((70 - (a + d)) < d)
) T2
) T2(c_r, a_r, b_r)
on (c_l = 25)
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
Select c_l_l, b_r
from (
Select c_l, d_r
from (
Select e, c, a
from p1
where ((53 < c) AND (52 < d))
) T1(e_l, c_l, a_l)
full join (
Select c, d
from p4
where ((b - c) = 65)
) T2(c_r, d_r)
on ((c_l > d_r) AND ((47 * ((44 * 53) * d_r)) < 54))
) T1(c_l_l, d_r_l)
left join (
Select e, c, b
from p1
where ((c = d) OR ((84 = (c - a)) AND (d = a)))
) T2(e_r, c_r, b_r)
on (c_l_l = 55)
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
    _testmgr.testcase_end(desc)

