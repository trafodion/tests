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
    
def test001(desc="""Joins Set 42"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_r_l, d_l_l, d_r
from (
Select d_l, e_r
from (
Select d
from p1
where ((c * 83) = c)
) T1(d_l)
full join (
Select e
from p5
where (c = e)
) T2(e_r)
on ((e_r - 13) < d_l)
) T1(d_l_l, e_r_l)
left join (
Select a, d
from p3
where ((a + e) > 28)
) T2(a_r, d_r)
on ((25 < ((98 - (e_r_l * 61)) * (d_l_l + 92))) AND (d_r > 60))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test42exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l, e_r, a_r, b_r
from (
Select c, b
from p4
where ((b * d) = b)
) T1(c_l, b_l)
full join (
Select e, c, a, b
from p1
where ((b * a) > d)
) T2(e_r, c_r, a_r, b_r)
on (b_r = b_l)
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test42exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, d_r
from (
select c
from (
Select c
from p3
where (e = (82 * c))
) T1
union all
select c
from (
Select c, a
from p4
where (62 = (52 * (68 * 44)))
) T2
) T1(c_l)
left join (
Select d
from p3
where (((75 - 47) * (68 * c)) < a)
) T2(d_r)
on (((c_l * (d_r + c_l)) = 82) AND (16 = d_r))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test42exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, e_r
from (
Select d
from p1
where ((45 > 25) OR (71 < a))
) T1(d_l)
full join (
Select e
from p2
where (((a + 60) + (78 * a)) < 58)
) T2(e_r)
on (85 < 48)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test42exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, d_l, e_r, d_r
from (
Select b, d
from p4
where ((0 > (e * c)) AND ((28 < 31) OR (((c + c) = (e + 35)) AND ((e - a) > e))))
) T1(b_l, d_l)
inner join (
select e, d
from (
Select e, d
from p4
where (95 = a)
) T1
union all
select e, a
from (
Select e, a
from p3
where (a = c)
) T2
) T2(e_r, d_r)
on (e_r < b_l)
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
Select b_l_l_l, e_r_l_l, b_r_r_l, c_r_l_r, a_r_l_r, e_r_r
from (
Select e_r_l, b_l_l, b_r_r, b_l_r
from (
select b_l, e_r
from (
Select b_l, e_r, a_r
from (
Select b
from p3
where ((41 = a) AND ((4 > (e * e)) OR (c = 90)))
) T1(b_l)
left join (
Select e, a
from p3
where (b = (b - 28))
) T2(e_r, a_r)
on (8 = e_r)
) T1
union all
select b, d
from (
Select b, d
from p4
where (d > d)
) T2
) T1(b_l_l, e_r_l)
left join (
Select b_l, b_r
from (
select b
from (
select b, d
from (
Select b, d
from p3
where (((45 - 39) - (b * 11)) > c)
) T1
union all
select c_l, e_r
from (
Select c_l, e_r
from (
Select c, b
from p1
where (a = a)
) T1(c_l, b_l)
full join (
Select e, c
from p3
where (b = a)
) T2(e_r, c_r)
on (c_l = 12)
) T2
) T1
union all
select d
from (
Select d
from p5
where (64 = 17)
) T2
) T1(b_l)
inner join (
select b
from (
Select b
from p5
where ((72 - 52) = e)
) T1
union all
select c
from (
Select c
from p5
where ((5 = 8) OR (d = d))
) T2
) T2(b_r)
on (b_l = b_l)
) T2(b_l_r, b_r_r)
on ((78 < b_l_r) AND (b_l_r = (0 * (22 - 5))))
) T1(e_r_l_l, b_l_l_l, b_r_r_l, b_l_r_l)
inner join (
Select a_r_l, c_r_l, e_r
from (
Select b_l, c_r, a_r
from (
Select b, d
from p4
where ((a = (26 - a)) OR (48 = e))
) T1(b_l, d_l)
left join (
Select c, a
from p4
where ((33 > e) AND ((84 * 95) > d))
) T2(c_r, a_r)
on ((61 - (a_r * (35 * a_r))) = 25)
) T1(b_l_l, c_r_l, a_r_l)
left join (
Select e, a
from p4
where (81 = e)
) T2(e_r, a_r)
on (((99 + 36) + (((e_r * (a_r_l - a_r_l)) + (e_r + 70)) + e_r)) > e_r)
) T2(a_r_l_r, c_r_l_r, e_r_r)
on (42 = e_r_l_l)
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
Select e_l, c_l, b_r
from (
select e, c
from (
Select e, c, b
from p4
where (a < c)
) T1
union all
select c, b
from (
Select c, b
from p3
where (18 > b)
) T2
) T1(e_l, c_l)
left join (
Select b
from p2
where (d < 83)
) T2(b_r)
on (13 = e_l)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test42exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_r_r
from (
Select e, b
from p3
where (d = (95 - 86))
) T1(e_l, b_l)
left join (
Select a_l, b_r
from (
Select a
from p5
where ((c = 2) OR (b > 73))
) T1(a_l)
full join (
Select b
from p3
where (e = 8)
) T2(b_r)
on (((17 + 7) < b_r) OR (b_r > a_l))
) T2(a_l_r, b_r_r)
on ((e_l = b_r_r) AND ((83 * 57) = b_r_r))
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
Select a_l, e_r
from (
Select a, d
from p1
where (c > a)
) T1(a_l, d_l)
left join (
select e, c
from (
Select e, c, a, b
from p4
where (e > b)
) T1
union all
select c, d
from (
Select c, d
from p1
where ((11 * a) = e)
) T2
) T2(e_r, c_r)
on (a_l < 22)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test42exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_l, b_r
from (
Select e, c, b
from p1
where ((a = (50 * 59)) AND ((c = (c - 19)) OR (94 = 21)))
) T1(e_l, c_l, b_l)
left join (
Select b
from p2
where ((a + 76) = e)
) T2(b_r)
on (73 < ((16 + (e_l + 98)) * 21))
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
Select b_l, e_r
from (
Select b
from p5
where (b < 57)
) T1(b_l)
full join (
Select e, c
from p2
where (((15 + b) * 12) > 3)
) T2(e_r, c_r)
on (((73 - 57) < 84) OR (e_r < (b_l * ((15 * (29 + (e_r - b_l))) * 57))))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test42exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, b_l_r_r, c_l_r, a_l_r_r_r
from (
Select d
from p5
where (e = 6)
) T1(d_l)
left join (
Select c_l, a_l_r_r, b_l_r
from (
Select c
from p1
where (b > e)
) T1(c_l)
left join (
Select b_l, a_l_r, c_l_r
from (
Select e, b
from p3
where (e = b)
) T1(e_l, b_l)
left join (
Select c_l, a_l, a_r
from (
Select c, a, b
from p1
where (a = 59)
) T1(c_l, a_l, b_l)
left join (
Select a
from p4
where (d > c)
) T2(a_r)
on (67 = 89)
) T2(c_l_r, a_l_r, a_r_r)
on (b_l = 54)
) T2(b_l_r, a_l_r_r, c_l_r_r)
on (67 = 1)
) T2(c_l_r, a_l_r_r_r, b_l_r_r)
on (60 > 97)
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
Select e_l, b_l, b_r_r, d_r_r
from (
Select e, b
from p2
where (e < b)
) T1(e_l, b_l)
left join (
Select c_l, b_r, d_r
from (
select c
from (
Select c
from p5
where ((a > c) OR ((d = a) AND ((d = (a * 99)) AND (36 = 78))))
) T1
union all
select e
from (
Select e
from p5
where ((13 > (79 + 16)) OR ((47 * e) < b))
) T2
) T1(c_l)
left join (
Select b, d
from p1
where (98 < 9)
) T2(b_r, d_r)
on (c_l = ((52 * d_r) - (41 - c_l)))
) T2(c_l_r, b_r_r, d_r_r)
on (((9 - 51) < 8) AND (31 = e_l))
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
Select c_l_l, c_r
from (
Select c_l, b_r
from (
Select c, a
from p1
where ((a = 5) AND (((c - 85) * b) = 84))
) T1(c_l, a_l)
inner join (
Select e, c, b
from p3
where ((((99 + b) + b) = 21) AND (d < 0))
) T2(e_r, c_r, b_r)
on (b_r = 60)
) T1(c_l_l, b_r_l)
inner join (
select c
from (
Select c
from p3
where ((b + c) = d)
) T1
union all
select e
from (
Select e, a, d
from p1
where ((19 - c) > 62)
) T2
) T2(c_r)
on (((c_r * c_l_l) + 40) < c_r)
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
Select c_l, e_r
from (
Select c, b, d
from p4
where (((e + b) = b) AND (((46 + 93) = (a - 71)) OR (a = e)))
) T1(c_l, b_l, d_l)
left join (
Select e, d
from p2
where (71 < 58)
) T2(e_r, d_r)
on (23 = 76)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test42exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_l_l_l_r, e_r_r
from (
Select a
from p2
where ((((39 + 33) * (c + d)) > d) OR (56 = a))
) T1(a_l)
left join (
select d_l_l_l, e_r
from (
Select d_l_l_l, e_r, c_r
from (
Select a_l_l, d_l_l, b_r
from (
Select a_l, d_l, c_r, d_r
from (
Select a, d
from p1
where (37 < 13)
) T1(a_l, d_l)
left join (
Select c, d
from p3
where (62 > 43)
) T2(c_r, d_r)
on (d_l > (d_l + 32))
) T1(a_l_l, d_l_l, c_r_l, d_r_l)
left join (
Select b
from p1
where (c = d)
) T2(b_r)
on (86 < d_l_l)
) T1(a_l_l_l, d_l_l_l, b_r_l)
left join (
Select e, c
from p2
where (19 > d)
) T2(e_r, c_r)
on (40 = c_r)
) T1
union all
select d_l, c_r
from (
Select d_l, c_r
from (
Select e, d
from p5
where ((98 = (70 - e)) OR ((2 = (50 * 8)) AND ((d = b) AND (((2 - (d - 54)) = 73) AND ((82 > (b - c)) AND ((82 < (0 * 82)) AND ((19 > 36) OR ((e > 45) AND (b = 94)))))))))
) T1(e_l, d_l)
left join (
Select c, a, b
from p2
where (2 = a)
) T2(c_r, a_r, b_r)
on (15 = d_l)
) T2
) T2(d_l_l_l_r, e_r_r)
on (a_l = 37)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test42exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, e_r, c_r
from (
Select e
from p5
where (a > 47)
) T1(e_l)
full join (
Select e, c
from p1
where ((c < 33) OR (((a * (51 - 99)) < 21) OR ((a < (e - 69)) AND ((10 = (31 * (b * 65))) AND (53 = 32)))))
) T2(e_r, c_r)
on (61 = e_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test42exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, a_l_r, c_l_r, d_l_r_r_r
from (
Select b
from p2
where ((e < ((33 - ((c + 5) + 7)) * 50)) OR (((d * e) + (62 - 77)) < 46))
) T1(b_l)
inner join (
Select c_l, a_l, d_l_r_r
from (
Select c, a, d
from p3
where (83 < 71)
) T1(c_l, a_l, d_l)
left join (
Select a_l, d_l_r, e_r_r_r
from (
Select a
from p1
where ((69 - a) = 24)
) T1(a_l)
left join (
Select b_l, d_l, e_r_r
from (
Select b, d
from p3
where ((61 = a) OR (47 < (66 - (e * b))))
) T1(b_l, d_l)
left join (
Select c_l, b_l, e_r, a_r
from (
Select c, b, d
from p3
where (((57 - b) = 42) AND (b = b))
) T1(c_l, b_l, d_l)
inner join (
Select e, a, b, d
from p2
where ((d = (c - c)) AND ((96 * ((d + d) + 36)) < (e + 20)))
) T2(e_r, a_r, b_r, d_r)
on ((17 < e_r) AND (25 = e_r))
) T2(c_l_r, b_l_r, e_r_r, a_r_r)
on ((b_l < e_r_r) AND ((80 > 87) AND (60 > b_l)))
) T2(b_l_r, d_l_r, e_r_r_r)
on ((e_r_r_r = (e_r_r_r * e_r_r_r)) OR (25 = 52))
) T2(a_l_r, d_l_r_r, e_r_r_r_r)
on ((36 - (a_l - (30 * 38))) < a_l)
) T2(c_l_r, a_l_r, d_l_r_r_r)
on ((((90 * d_l_r_r_r) + (c_l_r - b_l)) + (b_l + d_l_r_r_r)) = d_l_r_r_r)
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
Select c, d
from p3
where (13 = a)
) T1(c_l, d_l)
inner join (
Select c, a, b, d
from p2
where ((((e - (64 - 52)) * 99) = ((e - 13) * e)) OR ((d - d) = (22 * ((d - (b - d)) * 69))))
) T2(c_r, a_r, b_r, d_r)
on (d_l = d_l)
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
Select e_l, c_l, c_l_r
from (
Select e, c, b
from p1
where (71 = a)
) T1(e_l, c_l, b_l)
full join (
Select c_l, a_l_r, a_r_r
from (
Select e, c, a, d
from p1
where (d = 58)
) T1(e_l, c_l, a_l, d_l)
left join (
Select a_l, a_r
from (
Select a, b
from p3
where (e = a)
) T1(a_l, b_l)
left join (
Select a, b
from p5
where (((84 + c) > 99) AND (7 = 94))
) T2(a_r, b_r)
on ((((5 * 17) * a_r) - 71) = (a_r + a_r))
) T2(a_l_r, a_r_r)
on (a_l_r > (a_l_r - a_l_r))
) T2(c_l_r, a_l_r_r, a_r_r_r)
on ((c_l = 87) OR (c_l > e_l))
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
    #**********************
    _testmgr.testcase_end(desc)

