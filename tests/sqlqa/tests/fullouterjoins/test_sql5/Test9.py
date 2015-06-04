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
    
def test001(desc="""Joins Set 9"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
Select e_l, a_l, c_r
from (
Select e, a, d
from p1
where (((15 - 76) = b) AND (a < c))
) T1(e_l, a_l, d_l)
inner join (
Select c, b, d
from p5
where ((a + 57) = (e - d))
) T2(c_r, b_r, d_r)
on (((22 * 72) > 65) OR ((c_r = e_l) AND (29 < 78)))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_l, b_l, a_r, b_r
from (
Select e, c, a, b
from p5
where ((25 * b) = 43)
) T1(e_l, c_l, a_l, b_l)
full join (
Select a, b
from p2
where (32 = 4)
) T2(a_r, b_r)
on (55 = 34)
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
Select e_r_l, b_r, d_r
from (
Select c_l_l_l, d_r_r_l, e_r, c_r
from (
Select c_l_l, d_r_r
from (
select c_l
from (
Select c_l, b_l, e_r
from (
Select c, b, d
from p1
where ((d = d) AND (a = (54 - (12 + 56))))
) T1(c_l, b_l, d_l)
inner join (
select e
from (
Select e
from p3
where ((a > (c - (96 - (((96 + (67 * (b * c))) + d) + e)))) AND (c = b))
) T1
union all
select e
from (
select e, a
from (
Select e, a, d
from p1
where ((20 = (c + a)) OR (d < ((b * (a + 1)) - e)))
) T1
union all
select b_l, a_r
from (
select b_l, a_r
from (
Select b_l, a_r
from (
Select c, b, d
from p1
where ((e = 49) AND (95 < d))
) T1(c_l, b_l, d_l)
full join (
Select a
from p4
where (e = 66)
) T2(a_r)
on (16 < 49)
) T1
union all
select a_l, d_r
from (
select a_l, d_r
from (
Select a_l, d_r
from (
Select a
from p2
where (8 < (82 * 40))
) T1(a_l)
inner join (
Select d
from p1
where ((99 - 96) = 29)
) T2(d_r)
on (2 = ((a_l + a_l) - d_r))
) T1
union all
select a, b
from (
Select a, b
from p4
where ((d = 28) OR (53 < 66))
) T2
) T2
) T2
) T2
) T2(e_r)
on (e_r = 43)
) T1
union all
select a
from (
select a
from (
Select a, b
from p3
where (b = b)
) T1
union all
select a
from (
Select a
from p1
where ((83 + e) = a)
) T2
) T2
) T1(c_l_l)
left join (
Select a_l, d_r
from (
select a, b
from (
Select a, b
from p3
where ((a > 58) OR (41 = a))
) T1
union all
select e_l, b_r_r
from (
Select e_l, b_r_r
from (
Select e, d
from p3
where (d = 48)
) T1(e_l, d_l)
left join (
Select c_r_l, d_l_l, e_r, b_r
from (
Select c_l, a_l, d_l, c_r, d_r
from (
Select c, a, d
from p3
where ((a * 14) > e)
) T1(c_l, a_l, d_l)
left join (
Select c, d
from p1
where (((b * 96) + b) < ((77 + d) - 58))
) T2(c_r, d_r)
on (d_r = a_l)
) T1(c_l_l, a_l_l, d_l_l, c_r_l, d_r_l)
left join (
Select e, b
from p5
where (c < (e * 14))
) T2(e_r, b_r)
on (12 < (d_l_l * b_r))
) T2(c_r_l_r, d_l_l_r, e_r_r, b_r_r)
on (2 = b_r_r)
) T2
) T1(a_l, b_l)
inner join (
Select c, d
from p5
where (7 = 85)
) T2(c_r, d_r)
on ((31 * a_l) = 51)
) T2(a_l_r, d_r_r)
on ((6 < d_r_r) OR (d_r_r > d_r_r))
) T1(c_l_l_l, d_r_r_l)
left join (
Select e, c, a
from p4
where (e > d)
) T2(e_r, c_r, a_r)
on (((68 * ((8 + (41 + 98)) - 78)) - e_r) > ((61 - d_r_r_l) - c_r))
) T1(c_l_l_l_l, d_r_r_l_l, e_r_l, c_r_l)
full join (
Select b, d
from p1
where ((b = 90) AND (((86 - 76) + (b - a)) < e))
) T2(b_r, d_r)
on (75 > e_r_l)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, b_r, d_r
from (
Select d
from p2
where (70 > c)
) T1(d_l)
left join (
Select b, d
from p3
where (e = 72)
) T2(b_r, d_r)
on (81 < d_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_l, c_r, b_r
from (
Select c, a
from p4
where ((c < 65) OR (15 < 9))
) T1(c_l, a_l)
inner join (
select c, b
from (
Select c, b
from p5
where (((((e * (c + c)) - 75) - 35) * 35) = (e * 8))
) T1
union all
select b, d
from (
Select b, d
from p3
where ((b = d) AND (c < a))
) T2
) T2(c_r, b_r)
on (49 < (32 + 71))
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
Select e_l, c_r
from (
Select e
from p4
where (((51 * d) < (13 - d)) AND (53 < c))
) T1(e_l)
left join (
Select c, a
from p3
where ((19 > (77 * (39 * d))) OR ((71 = c) AND ((e - 19) < d)))
) T2(c_r, a_r)
on ((c_r = e_l) AND ((c_r * 78) = e_l))
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
Select b_l, c_r, a_r
from (
Select c, b
from p2
where (78 < b)
) T1(c_l, b_l)
left join (
select c, a
from (
Select c, a
from p5
where (93 > d)
) T1
union all
select c, a
from (
Select c, a, b
from p2
where (52 > (37 - 33))
) T2
) T2(c_r, a_r)
on (b_l = 29)
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
Select e_l, e_r
from (
Select e, c, d
from p4
where (((d + b) = 10) AND ((26 = 82) OR (d = (46 - e))))
) T1(e_l, c_l, d_l)
full join (
Select e
from p5
where ((a = (d * 79)) AND (75 = d))
) T2(e_r)
on ((37 < 28) AND ((71 > (e_r - 51)) OR ((e_r > (e_r + 89)) OR (5 < (37 + e_r)))))
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
Select e_l, c_l, d_r_r, d_l_r
from (
Select e, c, d
from p1
where (c > e)
) T1(e_l, c_l, d_l)
inner join (
Select d_l, a_r, d_r
from (
Select c, d
from p5
where (c > (e + 17))
) T1(c_l, d_l)
inner join (
Select e, a, b, d
from p5
where ((21 > 97) AND (d = 2))
) T2(e_r, a_r, b_r, d_r)
on ((45 - 67) > 24)
) T2(d_l_r, a_r_r, d_r_r)
on ((d_r_r = e_l) OR (((e_l + c_l) < d_r_r) AND (e_l > d_r_r)))
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
Select e_l, a_l, d_l, a_r
from (
Select e, a, d
from p4
where (93 = (b * 54))
) T1(e_l, a_l, d_l)
left join (
Select c, a
from p4
where ((e < (46 * 65)) AND (e > c))
) T2(c_r, a_r)
on ((52 = d_l) OR (23 < ((a_l + (e_l + 7)) + a_l)))
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
Select a_l_l_l, e_r, b_r
from (
select a_l_l
from (
Select a_l_l, d_r_l, b_l_l_r, a_r_r, a_l_l_r
from (
Select a_l, d_r
from (
Select a
from p2
where (d = a)
) T1(a_l)
full join (
Select d
from p2
where (b = 54)
) T2(d_r)
on (30 = a_l)
) T1(a_l_l, d_r_l)
left join (
Select a_l_l, d_r_l, b_l_l, a_r
from (
Select a_l, b_l, e_r, d_r
from (
Select e, a, b
from p3
where ((72 = 94) AND (c > 24))
) T1(e_l, a_l, b_l)
left join (
Select e, d
from p3
where ((d - 68) = 46)
) T2(e_r, d_r)
on (55 = (96 - 1))
) T1(a_l_l, b_l_l, e_r_l, d_r_l)
left join (
select a
from (
Select a
from p3
where (25 > d)
) T1
union all
select b
from (
Select b
from p2
where (7 < a)
) T2
) T2(a_r)
on (a_l_l = 41)
) T2(a_l_l_r, d_r_l_r, b_l_l_r, a_r_r)
on (b_l_l_r = 50)
) T1
union all
select b
from (
select b
from (
Select b
from p2
where (c > 29)
) T1
union all
select e
from (
select e, c
from (
Select e, c, a, d
from p2
where (e = 38)
) T1
union all
select a_l, c_r
from (
Select a_l, c_r
from (
select c, a
from (
Select c, a
from p1
where ((((a * 42) + 23) = b) OR (b < 39))
) T1
union all
select a, b
from (
Select a, b
from p2
where ((d > d) OR (54 = 33))
) T2
) T1(c_l, a_l)
left join (
select c
from (
Select c
from p4
where (d > (22 + (46 * (b * ((37 * d) * d)))))
) T1
union all
select c
from (
Select c
from p4
where (c > 86)
) T2
) T2(c_r)
on ((a_l > a_l) AND (66 = 56))
) T2
) T2
) T2
) T1(a_l_l_l)
left join (
select e, b
from (
Select e, b
from p1
where ((d = a) OR ((a = 83) OR ((12 > (a + 58)) AND ((11 > a) OR ((d - 28) = 45)))))
) T1
union all
select e, a
from (
Select e, a, d
from p3
where (80 = (e + ((a - a) * d)))
) T2
) T2(e_r, b_r)
on (69 > e_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, e_r
from (
Select b
from p3
where (52 < 91)
) T1(b_l)
inner join (
select e, a
from (
Select e, a
from p4
where ((86 = 40) AND (27 < 49))
) T1
union all
select e_l, d_r_r
from (
Select e_l, d_r_r, b_l_r
from (
Select e, a, b
from p2
where (e < 58)
) T1(e_l, a_l, b_l)
left join (
Select b_l, d_r
from (
Select e, b, d
from p4
where (((62 * 29) > 36) OR (93 = a))
) T1(e_l, b_l, d_l)
left join (
Select b, d
from p2
where (e < b)
) T2(b_r, d_r)
on (d_r < b_l)
) T2(b_l_r, d_r_r)
on (b_l_r = d_r_r)
) T2
) T2(e_r, a_r)
on ((((72 + 28) * 72) > e_r) AND ((16 * 62) = b_l))
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
Select e_l, d_l, e_r, c_r, d_r
from (
Select e, d
from p1
where (e = c)
) T1(e_l, d_l)
inner join (
Select e, c, d
from p4
where (e = 80)
) T2(e_r, c_r, d_r)
on (c_r = c_r)
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
Select d_l, a_r
from (
Select d
from p2
where (d = (b + 13))
) T1(d_l)
full join (
Select c, a, d
from p3
where (d > e)
) T2(c_r, a_r, d_r)
on (4 = (75 - 5))
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
Select d_l_l, c_r_r
from (
Select d_l, e_l_r, c_l_l_r_r
from (
Select d
from p1
where (d < ((9 + e) * c))
) T1(d_l)
left join (
Select e_l, c_l_l_r, b_l_l_r
from (
Select e, a, b
from p2
where (((35 + d) = 37) OR (c = d))
) T1(e_l, a_l, b_l)
left join (
select c_l_l, b_l_l
from (
Select c_l_l, b_l_l, e_r_r_l, a_r_l_l_r, d_r_r, d_l_r_l_r
from (
Select c_l, b_l, e_r_r
from (
Select c, a, b
from p3
where ((38 + d) = c)
) T1(c_l, a_l, b_l)
inner join (
Select e_l, e_r, c_r, a_r
from (
Select e
from p3
where ((b > 39) AND (83 < e))
) T1(e_l)
left join (
Select e, c, a
from p2
where (a > a)
) T2(e_r, c_r, a_r)
on ((76 - 61) > e_r)
) T2(e_l_r, e_r_r, c_r_r, a_r_r)
on ((b_l + 11) = c_l)
) T1(c_l_l, b_l_l, e_r_r_l)
left join (
Select c_r_r_l, a_r_l_l, d_l_r_l, d_r
from (
Select a_r_l, e_r_l, c_r_r, d_l_r
from (
Select d_l_l, e_r, a_r
from (
Select d_l, e_r
from (
Select d
from p2
where ((54 < d) AND ((d > a) OR (((84 + 27) + 2) > d)))
) T1(d_l)
left join (
Select e, a
from p5
where (e > 74)
) T2(e_r, a_r)
on (e_r > 12)
) T1(d_l_l, e_r_l)
inner join (
Select e, a
from p1
where ((67 * 96) < 90)
) T2(e_r, a_r)
on ((e_r > d_l_l) AND ((a_r > 14) AND ((e_r = a_r) AND (e_r = a_r))))
) T1(d_l_l_l, e_r_l, a_r_l)
left join (
Select c_l, b_l, d_l, c_r
from (
Select c, b, d
from p3
where (e = 62)
) T1(c_l, b_l, d_l)
left join (
select c
from (
Select c
from p1
where (((e * 0) * 82) > c)
) T1
union all
select a
from (
Select a, b, d
from p1
where (c = (89 + 99))
) T2
) T2(c_r)
on ((55 = 90) AND ((67 < 51) AND ((b_l > 23) AND (((d_l + (b_l + 22)) > d_l) OR ((1 = 90) OR (c_r = d_l))))))
) T2(c_l_r, b_l_r, d_l_r, c_r_r)
on (11 > c_r_r)
) T1(a_r_l_l, e_r_l_l, c_r_r_l, d_l_r_l)
inner join (
Select d
from p5
where ((e = b) AND (69 > 49))
) T2(d_r)
on ((8 = 14) OR ((43 > c_r_r_l) AND (c_r_r_l = c_r_r_l)))
) T2(c_r_r_l_r, a_r_l_l_r, d_l_r_l_r, d_r_r)
on ((2 = 65) AND ((b_l_l + 17) = (b_l_l - a_r_l_l_r)))
) T1
union all
select a, b
from (
Select a, b
from p3
where (38 = 69)
) T2
) T2(c_l_l_r, b_l_l_r)
on (16 = b_l_l_r)
) T2(e_l_r, c_l_l_r_r, b_l_l_r_r)
on (4 > e_l_r)
) T1(d_l_l, e_l_r_l, c_l_l_r_r_l)
left join (
Select c_l, a_l, d_l, c_r
from (
Select e, c, a, d
from p4
where (4 < c)
) T1(e_l, c_l, a_l, d_l)
full join (
Select c
from p5
where ((b = 54) OR ((79 - 10) = a))
) T2(c_r)
on ((d_l + 88) < (d_l * (d_l + 3)))
) T2(c_l_r, a_l_r, d_l_r, c_r_r)
on (97 = 63)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_l, d_l, b_r
from (
Select e, b, d
from p5
where (d < c)
) T1(e_l, b_l, d_l)
left join (
Select b
from p3
where (((91 + e) * b) = ((11 - d) * 56))
) T2(b_r)
on ((b_r + e_l) = 71)
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
Select d_l_l, a_r_r
from (
Select c_l, d_l, c_r, d_r
from (
select c, b, d
from (
Select c, b, d
from p1
where ((58 + d) = 19)
) T1
union all
select e, c, a
from (
Select e, c, a, b
from p2
where ((a < 59) AND (11 = e))
) T2
) T1(c_l, b_l, d_l)
left join (
Select c, d
from p2
where ((c = b) AND (40 = (c * 23)))
) T2(c_r, d_r)
on ((16 < 41) OR (d_r < 9))
) T1(c_l_l, d_l_l, c_r_l, d_r_l)
full join (
Select b_l, d_l, c_r, a_r
from (
Select b, d
from p5
where (((34 - c) + a) < (85 * (93 - 88)))
) T1(b_l, d_l)
left join (
select c, a, b
from (
Select c, a, b
from p3
where (33 = 39)
) T1
union all
select e, c, a
from (
Select e, c, a
from p2
where ((25 = d) AND ((b > 13) OR (e > d)))
) T2
) T2(c_r, a_r, b_r)
on (81 < (35 + a_r))
) T2(b_l_r, d_l_r, c_r_r, a_r_r)
on ((d_l_l > 38) OR (a_r_r < a_r_r))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_r
from (
Select e
from p2
where ((((c + 78) + e) > c) AND (94 < 19))
) T1(e_l)
left join (
Select b
from p2
where ((16 = e) AND (61 < a))
) T2(b_r)
on (b_r = b_r)
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
Select d_l, c_r
from (
Select d
from p3
where ((52 > 46) AND (a > 84))
) T1(d_l)
left join (
Select c, b
from p2
where (((d - b) > d) OR ((70 - c) < 26))
) T2(c_r, b_r)
on (d_l > 91)
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
Select d_l, a_l_r, c_l_r, a_r_r
from (
Select e, c, d
from p4
where ((d - (92 * 85)) < 77)
) T1(e_l, c_l, d_l)
left join (
Select c_l, a_l, d_l, a_r
from (
Select c, a, d
from p5
where ((12 = 39) AND ((b > 90) OR (63 = (34 - c))))
) T1(c_l, a_l, d_l)
left join (
Select a
from p4
where (d = (51 - (30 + b)))
) T2(a_r)
on (6 = c_l)
) T2(c_l_r, a_l_r, d_l_r, a_r_r)
on (((29 - 24) + 60) > 76)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #****************************************
    _testmgr.testcase_end(desc)

