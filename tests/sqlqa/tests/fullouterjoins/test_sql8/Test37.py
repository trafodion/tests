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
    
def test001(desc="""Joins Set 37"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_l, d_l, a_r
from (
Select e, a, d
from p5
where ((2 + b) < 47)
) T1(e_l, a_l, d_l)
left join (
Select a
from p2
where (d > 14)
) T2(a_r)
on (((15 + 18) > 30) AND (a_l = 77))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_r_r, a_r_r, b_l_r
from (
Select a, b, d
from p3
where ((c < (c + 69)) AND ((a = 11) AND ((e = 90) AND (46 < e))))
) T1(a_l, b_l, d_l)
left join (
Select b_l, d_l, a_r, d_r
from (
select b, d
from (
Select b, d
from p2
where ((54 + c) = a)
) T1
union all
select b_l, d_l
from (
select b_l, d_l, d_l_r_r_r, e_l_l_r
from (
Select b_l, d_l, d_l_r_r_r, e_l_l_r
from (
Select b, d
from p5
where (80 < (b - c))
) T1(b_l, d_l)
inner join (
Select c_l_l, e_l_l, a_l_r, d_l_r_r
from (
select e_l, c_l
from (
select e_l, c_l
from (
Select e_l, c_l, b_r
from (
Select e, c, b, d
from p2
where (b = 45)
) T1(e_l, c_l, b_l, d_l)
full join (
Select b
from p3
where ((13 - (32 + 77)) = 3)
) T2(b_r)
on (c_l = (12 + e_l))
) T1
union all
select e, b
from (
Select e, b
from p2
where ((75 < 70) AND (((48 - 23) * (e * (45 + (3 - d)))) = d))
) T2
) T1
union all
select c, d
from (
Select c, d
from p3
where ((a + (71 + (42 - 23))) = a)
) T2
) T1(e_l_l, c_l_l)
left join (
Select a_l, d_l_r
from (
Select a
from p4
where ((c - 62) > d)
) T1(a_l)
inner join (
select d_l, d_l_l_r
from (
Select d_l, d_l_l_r, e_r_r_l_r
from (
Select a, d
from p1
where (b = a)
) T1(a_l, d_l)
left join (
Select e_r_r_l, d_l_l, a_r
from (
Select d_l, b_r_r, e_r_r, a_l_r_l_l_r
from (
Select d
from p2
where (1 > (99 + (2 - 29)))
) T1(d_l)
inner join (
Select a_l_r_l_l, e_r, b_r
from (
Select a_l_r_l, c_r
from (
Select e_l, a_l_r
from (
select e
from (
Select e, c, b
from p5
where ((b = 62) OR (20 = b))
) T1
union all
select a
from (
select a
from (
Select a
from p5
where ((a > 71) OR (e = e))
) T1
union all
select c
from (
Select c
from p1
where ((e = (d * d)) OR ((39 = c) AND ((12 = 50) AND (85 = 41))))
) T2
) T2
) T1(e_l)
inner join (
Select a_l, d_l, a_r
from (
Select e, a, d
from p2
where (11 = (b * a))
) T1(e_l, a_l, d_l)
inner join (
Select a
from p3
where (69 > 5)
) T2(a_r)
on ((d_l > d_l) AND (94 > d_l))
) T2(a_l_r, d_l_r, a_r_r)
on ((56 < 32) AND ((e_l > a_l_r) OR ((e_l < 6) OR (67 = (a_l_r + 40)))))
) T1(e_l_l, a_l_r_l)
inner join (
Select e, c, b
from p5
where (35 = 13)
) T2(e_r, c_r, b_r)
on (a_l_r_l = 26)
) T1(a_l_r_l_l, c_r_l)
left join (
Select e, c, b
from p5
where ((c = b) AND (c < b))
) T2(e_r, c_r, b_r)
on ((b_r + 27) < b_r)
) T2(a_l_r_l_l_r, e_r_r, b_r_r)
on (d_l = (a_l_r_l_l_r + 30))
) T1(d_l_l, b_r_r_l, e_r_r_l, a_l_r_l_l_r_l)
inner join (
Select c, a, b
from p3
where (b = 87)
) T2(c_r, a_r, b_r)
on (d_l_l < 25)
) T2(e_r_r_l_r, d_l_l_r, a_r_r)
on (82 = 40)
) T1
union all
select e_l, d_r
from (
Select e_l, d_r
from (
Select e, b
from p4
where (b = 21)
) T1(e_l, b_l)
full join (
Select a, d
from p2
where (e = 3)
) T2(a_r, d_r)
on (51 = (77 - (25 * d_r)))
) T2
) T2(d_l_r, d_l_l_r_r)
on (((((a_l * 76) * a_l) * d_l_r) = (d_l_r - (91 + 1))) OR ((45 = d_l_r) OR ((a_l * 12) > 59)))
) T2(a_l_r, d_l_r_r)
on (c_l_l = 24)
) T2(c_l_l_r, e_l_l_r, a_l_r_r, d_l_r_r_r)
on ((d_l_r_r_r < d_l_r_r_r) AND (e_l_l_r < 12))
) T1
union all
select e_l, c_l, b_l, d_r
from (
Select e_l, c_l, b_l, d_r
from (
Select e, c, b
from p2
where (c = 13)
) T1(e_l, c_l, b_l)
left join (
Select a, d
from p3
where (52 = 0)
) T2(a_r, d_r)
on (b_l = c_l)
) T2
) T2
) T1(b_l, d_l)
left join (
Select e, a, d
from p1
where (d < 22)
) T2(e_r, a_r, d_r)
on (d_r > 43)
) T2(b_l_r, d_l_r, a_r_r, d_r_r)
on (38 < 54)
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
Select a_l, d_r
from (
select a
from (
select a
from (
Select a
from p4
where (d < 11)
) T1
union all
select b_l
from (
Select b_l, e_r, d_r
from (
Select b
from p3
where ((e * b) = d)
) T1(b_l)
left join (
Select e, d
from p4
where (55 < e)
) T2(e_r, d_r)
on (d_r > e_r)
) T2
) T1
union all
select c
from (
Select c, b, d
from p1
where (a < b)
) T2
) T1(a_l)
inner join (
Select d
from p5
where ((40 * 30) < d)
) T2(d_r)
on (63 > a_l)
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
Select a_l, b_l, b_r_r
from (
Select e, a, b
from p3
where (e < d)
) T1(e_l, a_l, b_l)
inner join (
Select a_l, d_l, b_r
from (
Select a, d
from p2
where (25 < a)
) T1(a_l, d_l)
left join (
Select b
from p3
where (29 = 84)
) T2(b_r)
on (40 = 44)
) T2(a_l_r, d_l_r, b_r_r)
on (86 = 2)
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
Select e_l, a_l_r, a_r_r
from (
Select e
from p2
where ((51 = (26 * 81)) OR (6 = 36))
) T1(e_l)
left join (
select a_l, a_r
from (
Select a_l, a_r
from (
Select a
from p3
where (49 < e)
) T1(a_l)
left join (
Select e, a, b
from p4
where (a < 13)
) T2(e_r, a_r, b_r)
on (45 = a_r)
) T1
union all
select a_l, b_r
from (
Select a_l, b_r, d_r
from (
Select a
from p3
where ((c = ((b * c) - 72)) AND (((d - d) = b) OR ((a = (d + 14)) OR (9 = (b + d)))))
) T1(a_l)
inner join (
select b, d
from (
Select b, d
from p3
where ((0 = d) AND (19 = a))
) T1
union all
select e, d
from (
Select e, d
from p1
where ((b < 86) OR (((c + e) = (a - d)) AND (52 < 30)))
) T2
) T2(b_r, d_r)
on ((a_l > (b_r * (((b_r * d_r) * d_r) - (d_r - 98)))) OR (29 = 54))
) T2
) T2(a_l_r, a_r_r)
on (((a_l_r - (63 + 85)) + a_r_r) < a_r_r)
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
Select c_l, c_r, a_r, b_r
from (
select c
from (
Select c, a, d
from p3
where (65 < c)
) T1
union all
select c
from (
select c
from (
Select c, d
from p4
where (d = 50)
) T1
union all
select a
from (
Select a
from p3
where (93 = 46)
) T2
) T2
) T1(c_l)
left join (
Select c, a, b
from p1
where (25 = a)
) T2(c_r, a_r, b_r)
on ((c_l - c_r) > (41 - c_r))
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
Select b_l, c_r, a_r
from (
select b
from (
Select b
from p4
where ((6 > 75) AND (65 < (b * (e + 86))))
) T1
union all
select c
from (
Select c, a, b
from p5
where ((a = (d * 43)) AND ((14 = 58) OR ((e = 62) OR (32 > 34))))
) T2
) T1(b_l)
inner join (
Select c, a
from p5
where (64 > 20)
) T2(c_r, a_r)
on ((3 = ((15 + 62) - (c_r - 30))) OR ((12 > 58) AND (c_r = 98)))
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
Select c_l, d_l, e_r
from (
Select c, a, d
from p5
where (34 = d)
) T1(c_l, a_l, d_l)
left join (
Select e, a
from p4
where ((c < 22) OR (b = d))
) T2(e_r, a_r)
on (90 = 46)
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
Select a_r_l, c_r, a_r
from (
Select e_l, a_l, d_l, a_r, d_r
from (
Select e, a, d
from p5
where (e > 61)
) T1(e_l, a_l, d_l)
left join (
Select a, b, d
from p1
where (a < 65)
) T2(a_r, b_r, d_r)
on (46 < a_l)
) T1(e_l_l, a_l_l, d_l_l, a_r_l, d_r_l)
left join (
Select c, a, d
from p5
where (((a + a) + 47) > a)
) T2(c_r, a_r, d_r)
on (43 < 96)
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
Select e_l, e_r_r
from (
Select e, c
from p1
where (((c + 49) + b) = ((86 - (b * 17)) + d))
) T1(e_l, c_l)
full join (
Select e_l, e_r, c_r, d_r
from (
Select e
from p3
where (18 < e)
) T1(e_l)
inner join (
Select e, c, d
from p5
where (22 > 18)
) T2(e_r, c_r, d_r)
on (20 = 13)
) T2(e_l_r, e_r_r, c_r_r, d_r_r)
on ((0 < e_r_r) OR ((e_l > 75) AND (54 > (((60 - 57) - e_r_r) - (35 + e_l)))))
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
Select e_l, c_r, a_r
from (
Select e
from p2
where ((d < d) OR ((a = c) AND (d = 67)))
) T1(e_l)
full join (
Select c, a, d
from p2
where ((c = 65) AND (b > 64))
) T2(c_r, a_r, d_r)
on ((6 - (((c_r - 27) * ((c_r + ((c_r * 13) * 40)) + e_l)) - 62)) = 68)
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
Select a_l, b_r
from (
Select a
from p5
where ((58 > 97) AND (56 = a))
) T1(a_l)
full join (
Select a, b
from p4
where (((71 * e) + 89) > 69)
) T2(a_r, b_r)
on ((b_r + (6 - a_l)) = 84)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_r_l, e_r_l, a_l_r, e_r_r
from (
Select b_l, d_l, e_r, c_r
from (
Select b, d
from p1
where (a = (6 - ((e * 2) + e)))
) T1(b_l, d_l)
inner join (
Select e, c, a, b
from p4
where ((d > 94) OR ((((10 - 53) * 93) = b) OR (c = (b * e))))
) T2(e_r, c_r, a_r, b_r)
on (((e_r * 23) = 81) OR (c_r = ((b_l + 84) - b_l)))
) T1(b_l_l, d_l_l, e_r_l, c_r_l)
full join (
Select a_l, e_r, d_r
from (
Select a
from p1
where ((6 = 76) OR ((e < (c - (71 * d))) OR (e = 58)))
) T1(a_l)
full join (
Select e, d
from p2
where (93 < (17 + e))
) T2(e_r, d_r)
on ((d_r > 2) AND ((58 = 56) AND (a_l = 18)))
) T2(a_l_r, e_r_r, d_r_r)
on ((0 = e_r_r) AND ((c_r_l > (79 + e_r_l)) OR (e_r_r < (11 * e_r_l))))
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
Select c_l, c_r
from (
select e, c, d
from (
Select e, c, d
from p3
where (b < 47)
) T1
union all
select e, c, d
from (
Select e, c, d
from p4
where ((e = 74) OR (((c * b) < 37) AND ((d > a) OR (e < d))))
) T2
) T1(e_l, c_l, d_l)
full join (
Select c, d
from p3
where ((d * a) = b)
) T2(c_r, d_r)
on ((c_r - (17 + (82 - 84))) = 46)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, e_r
from (
Select d
from p4
where ((47 + 19) < 27)
) T1(d_l)
inner join (
Select e
from p1
where ((24 = e) AND (81 < d))
) T2(e_r)
on (61 = 85)
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
Select e_l, c_r
from (
select e
from (
select e, c
from (
Select e, c
from p1
where ((41 = (b - ((78 * d) - a))) OR (22 > 3))
) T1
union all
select e, a
from (
Select e, a, b
from p1
where (a = 29)
) T2
) T1
union all
select b
from (
Select b
from p4
where (96 > (a + c))
) T2
) T1(e_l)
left join (
Select c
from p2
where ((((c * (e * c)) * c) - (b - d)) < 91)
) T2(c_r)
on (e_l = 18)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_l, c_r, b_r
from (
Select a, b
from p4
where ((c = c) OR (41 < e))
) T1(a_l, b_l)
inner join (
select c, b, d
from (
Select c, b, d
from p4
where (c < 80)
) T1
union all
select d_r_l, b_l_l, d_r
from (
Select d_r_l, b_l_l, d_r
from (
Select e_l, c_l, b_l, d_r
from (
Select e, c, b
from p2
where (a > 51)
) T1(e_l, c_l, b_l)
full join (
Select d
from p3
where ((48 * 62) < (95 * 55))
) T2(d_r)
on ((42 = e_l) OR (60 < 78))
) T1(e_l_l, c_l_l, b_l_l, d_r_l)
left join (
Select d
from p1
where ((c = 76) AND ((88 < a) AND (a > d)))
) T2(d_r)
on ((96 + b_l_l) > d_r)
) T2
) T2(c_r, b_r, d_r)
on (b_l = 96)
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
Select e_l, b_r
from (
Select e
from p1
where (67 < 78)
) T1(e_l)
left join (
Select e, b
from p4
where (42 < (63 * d))
) T2(e_r, b_r)
on (((b_r - 88) * ((e_l - e_l) + b_r)) = 88)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_r
from (
Select e, c, b
from p4
where (((a + a) < b) OR ((c > 75) AND (b < (d + ((35 - 94) + b)))))
) T1(e_l, c_l, b_l)
left join (
Select a, b
from p4
where (42 > 28)
) T2(a_r, b_r)
on ((a_r = e_l) AND ((e_l = e_l) OR ((a_r > 97) OR (29 = (21 + (e_l * e_l))))))
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
Select e_l, a_r_r_l_r
from (
select e
from (
select e, c
from (
Select e, c
from p4
where (69 > 61)
) T1
union all
select e, c
from (
select e, c, a
from (
Select e, c, a
from p4
where ((c = e) OR ((e + (a - 70)) < e))
) T1
union all
select e, c, b
from (
Select e, c, b
from p4
where ((79 * c) = e)
) T2
) T2
) T1
union all
select c
from (
select c
from (
Select c
from p1
where ((10 < b) OR (30 > a))
) T1
union all
select b_l
from (
Select b_l, d_l, c_l_r
from (
Select a, b, d
from p2
where (d = (41 + 84))
) T1(a_l, b_l, d_l)
left join (
Select e_l, c_l, d_l, b_l_r_r, c_l_r, e_l_r
from (
Select e, c, d
from p4
where ((((79 + a) * 38) < d) AND (a > c))
) T1(e_l, c_l, d_l)
inner join (
Select e_l, c_l, b_l_r
from (
select e, c
from (
Select e, c, d
from p3
where ((92 + 2) > e)
) T1
union all
select c_l, b_l_r
from (
select c_l, b_l_r
from (
Select c_l, b_l_r
from (
Select c, d
from p5
where (78 > c)
) T1(c_l, d_l)
inner join (
Select b_l, d_r
from (
Select b
from p1
where (d < c)
) T1(b_l)
left join (
Select e, b, d
from p2
where (((75 - (9 - a)) > (24 - ((e + 10) * a))) OR ((((e - (35 * d)) * 40) = c) AND (84 = 1)))
) T2(e_r, b_r, d_r)
on (19 > 27)
) T2(b_l_r, d_r_r)
on (((c_l - 16) > c_l) OR (b_l_r = 18))
) T1
union all
select b_l_l, c_l_r
from (
select b_l_l, c_l_r, e_r_r
from (
Select b_l_l, c_l_r, e_r_r
from (
select b_l
from (
Select b_l, e_r
from (
Select b
from p2
where ((72 > e) AND (b = e))
) T1(b_l)
inner join (
Select e, c
from p3
where (a = b)
) T2(e_r, c_r)
on ((e_r = 21) AND ((49 + b_l) < (e_r + 65)))
) T1
union all
select c
from (
Select c
from p4
where ((71 < 57) OR (d = a))
) T2
) T1(b_l_l)
full join (
Select c_l, e_r
from (
Select c
from p1
where (95 < c)
) T1(c_l)
inner join (
Select e, b
from p3
where ((e = a) AND ((76 < d) AND (a > 43)))
) T2(e_r, b_r)
on (((c_l * 96) * 61) > (8 + e_r))
) T2(c_l_r, e_r_r)
on (e_r_r = 13)
) T1
union all
select a_l, b_l, d_r
from (
Select a_l, b_l, d_r
from (
Select a, b
from p1
where ((79 + b) = d)
) T1(a_l, b_l)
left join (
Select d
from p3
where ((d = d) AND ((c = (47 - 80)) AND (b < a)))
) T2(d_r)
on ((d_r = 47) OR ((b_l = b_l) OR (d_r = b_l)))
) T2
) T2
) T2
) T1(e_l, c_l)
full join (
Select a_l, b_l, e_r
from (
Select a, b
from p2
where ((47 > (d + 7)) OR ((b > 51) AND (33 < 62)))
) T1(a_l, b_l)
full join (
Select e
from p1
where (89 = (b * c))
) T2(e_r)
on (b_l = b_l)
) T2(a_l_r, b_l_r, e_r_r)
on ((28 > b_l_r) AND (e_l > 45))
) T2(e_l_r, c_l_r, b_l_r_r)
on ((((46 * 12) - (e_l - 90)) = 57) OR ((((65 - c_l) + b_l_r_r) > (c_l_r + (14 * 14))) OR (9 < (32 - (c_l_r - 34)))))
) T2(e_l_r, c_l_r, d_l_r, b_l_r_r_r, c_l_r_r, e_l_r_r)
on (((4 - 1) + (b_l * 80)) = 59)
) T2
) T2
) T1(e_l)
full join (
Select c_l_l, a_r_r_l, e_r, b_r
from (
Select c_l, d_l, a_r_r, b_l_r
from (
Select c, d
from p5
where (((43 - (45 - c)) - a) > e)
) T1(c_l, d_l)
left join (
Select b_l, a_r
from (
select b, d
from (
Select b, d
from p2
where ((97 > (84 * 19)) OR ((d + (1 - (50 - a))) < (33 * 51)))
) T1
union all
select e, c
from (
Select e, c
from p3
where (65 = (((89 - 20) - (70 * c)) * e))
) T2
) T1(b_l, d_l)
inner join (
Select a
from p4
where ((90 > 58) AND ((e < b) AND ((b = 4) AND (3 < 24))))
) T2(a_r)
on (b_l = 49)
) T2(b_l_r, a_r_r)
on (30 > a_r_r)
) T1(c_l_l, d_l_l, a_r_r_l, b_l_r_l)
left join (
Select e, b
from p1
where (e > b)
) T2(e_r, b_r)
on (c_l_l > b_r)
) T2(c_l_l_r, a_r_r_l_r, e_r_r, b_r_r)
on (20 < 43)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #***********************
    _testmgr.testcase_end(desc)

