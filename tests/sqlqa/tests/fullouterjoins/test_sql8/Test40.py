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
    
def test001(desc="""Joins Set 40"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_l, c_r, a_r
from (
Select c, a, d
from p5
where (a = b)
) T1(c_l, a_l, d_l)
inner join (
Select c, a
from p4
where ((b = a) AND ((13 = 39) OR ((14 < b) OR (((41 * 78) = (46 + d)) AND ((60 < 99) AND (53 = e))))))
) T2(c_r, a_r)
on ((c_r < a_l) AND (c_l = a_l))
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
Select e_l, a_r
from (
Select e, c, d
from p1
where ((60 * e) = 68)
) T1(e_l, c_l, d_l)
full join (
Select a
from p4
where (48 = a)
) T2(a_r)
on ((e_l = a_r) AND (20 > 88))
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
Select a_l, b_r, d_r
from (
Select c, a, d
from p1
where (70 = (44 - c))
) T1(c_l, a_l, d_l)
left join (
Select b, d
from p1
where (37 = c)
) T2(b_r, d_r)
on (d_r > ((a_l * 43) - 58))
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
Select b_l, d_r_r, b_l_r
from (
select b
from (
Select b, d
from p2
where (19 = b)
) T1
union all
select a
from (
select a
from (
Select a
from p2
where ((16 = 85) AND ((45 > 8) OR (88 = 89)))
) T1
union all
select a
from (
select a
from (
Select a
from p3
where ((98 - (3 + c)) = (b * d))
) T1
union all
select e
from (
Select e, b, d
from p2
where ((97 < d) AND (a < 76))
) T2
) T2
) T2
) T1(b_l)
full join (
Select b_l, d_r
from (
Select c, b
from p1
where ((c > 99) OR ((e - 38) = 33))
) T1(c_l, b_l)
left join (
Select d
from p5
where (b > 24)
) T2(d_r)
on ((((38 * (b_l + 83)) - 67) < b_l) OR ((12 * (73 - 0)) < b_l))
) T2(b_l_r, d_r_r)
on (31 = 47)
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
Select e_l, a_l, d_l_l_r, c_r_r_r
from (
select e, a
from (
Select e, a, b
from p4
where ((((b + a) * c) < ((a - 51) + (95 * e))) AND (82 < a))
) T1
union all
select e, a
from (
Select e, a
from p5
where ((a = 49) OR (d = c))
) T2
) T1(e_l, a_l)
left join (
Select e_l_r_l, d_l_l, c_r_r
from (
Select d_l, e_l_r
from (
Select e, d
from p1
where (86 = b)
) T1(e_l, d_l)
inner join (
select e_l
from (
select e_l, c_l
from (
Select e_l, c_l, d_r
from (
Select e, c
from p5
where ((61 = 35) AND (b > (64 * 20)))
) T1(e_l, c_l)
full join (
Select c, d
from p3
where (24 = (((b + 79) * 6) + (b - e)))
) T2(c_r, d_r)
on ((e_l * 24) = c_l)
) T1
union all
select e, c
from (
select e, c
from (
Select e, c, a, d
from p5
where (c > 3)
) T1
union all
select c, a
from (
Select c, a
from p1
where ((b > b) AND (e = a))
) T2
) T2
) T1
union all
select c
from (
Select c
from p2
where (b = 77)
) T2
) T2(e_l_r)
on ((d_l * 80) > (15 * d_l))
) T1(d_l_l, e_l_r_l)
inner join (
Select e_l_l, c_r
from (
Select e_l, d_r
from (
Select e, b
from p2
where (d > 96)
) T1(e_l, b_l)
full join (
Select d
from p2
where (c > ((63 - 23) * e))
) T2(d_r)
on ((e_l = 6) AND (29 < d_r))
) T1(e_l_l, d_r_l)
left join (
Select c
from p1
where (83 = ((8 - 34) * c))
) T2(c_r)
on (c_r = c_r)
) T2(e_l_l_r, c_r_r)
on (54 < 52)
) T2(e_l_r_l_r, d_l_l_r, c_r_r_r)
on ((12 > 39) AND (((a_l + 16) + a_l) = 44))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test40exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_r
from (
Select a, b, d
from p5
where (b < c)
) T1(a_l, b_l, d_l)
full join (
Select b
from p5
where (((e + e) + a) = (23 + 31))
) T2(b_r)
on (a_l < b_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test40exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_r_l, e_r, d_r
from (
Select a_l, b_l, c_r
from (
select e, a, b
from (
Select e, a, b
from p4
where (b > (e * (b - 19)))
) T1
union all
select b_l, a_r, d_r
from (
Select b_l, a_r, d_r
from (
Select b
from p4
where (50 = (0 - c))
) T1(b_l)
inner join (
Select a, d
from p1
where ((52 > a) AND (29 = b))
) T2(a_r, d_r)
on (d_r > 26)
) T2
) T1(e_l, a_l, b_l)
inner join (
select c
from (
Select c, d
from p2
where (52 = 75)
) T1
union all
select c
from (
Select c
from p3
where ((((e * c) - b) + 29) < (a + 64))
) T2
) T2(c_r)
on ((((a_l * 85) * b_l) < 24) OR (c_r = c_r))
) T1(a_l_l, b_l_l, c_r_l)
full join (
Select e, a, b, d
from p1
where (41 < e)
) T2(e_r, a_r, b_r, d_r)
on (91 > (c_r_l + 57))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test40exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_r_l_l_l, c_r_l, c_l_r, e_r_r_r, b_l_r
from (
Select c_l_r_l_l, c_r
from (
select c_l_r_l, a_l_r_r_l_l
from (
Select c_l_r_l, a_l_r_r_l_l, a_l_r, e_r_r
from (
Select a_l_r_r_l, d_l_l, c_l_r, e_r_r_r
from (
Select d_l, a_l_r_r
from (
Select d
from p1
where (b = 15)
) T1(d_l)
full join (
Select b_l, d_l, a_l_r, b_r_r
from (
Select b, d
from p3
where (49 < e)
) T1(b_l, d_l)
left join (
select a_l, b_r
from (
Select a_l, b_r
from (
Select a
from p5
where (17 < 9)
) T1(a_l)
left join (
Select b
from p2
where ((c < 59) OR (52 = 3))
) T2(b_r)
on ((55 = b_r) AND (a_l = (48 + 28)))
) T1
union all
select b_l, d_l
from (
select b_l, d_l, a_r
from (
select b_l, d_l, a_r, d_r
from (
Select b_l, d_l, a_r, d_r
from (
select c, b, d
from (
Select c, b, d
from p1
where ((48 < 96) OR ((74 = a) OR ((e * 27) > c)))
) T1
union all
select e_l_l, d_l_r_l, a_r
from (
Select e_l_l, d_l_r_l, a_r
from (
Select e_l, d_l_r
from (
Select e
from p2
where (c < b)
) T1(e_l)
left join (
Select e_l, d_l, c_l_r, a_r_r
from (
Select e, a, d
from p2
where (51 < b)
) T1(e_l, a_l, d_l)
inner join (
Select c_l, a_r
from (
select e, c, a
from (
Select e, c, a
from p5
where (((c * 54) > 52) AND (((a + b) > 40) AND ((d = c) OR ((99 = a) AND ((d = (c + a)) AND (b = b))))))
) T1
union all
select e, a, d
from (
Select e, a, d
from p5
where (e = 71)
) T2
) T1(e_l, c_l, a_l)
left join (
Select c, a
from p1
where (d = c)
) T2(c_r, a_r)
on (59 = c_l)
) T2(c_l_r, a_r_r)
on ((a_r_r > 11) AND (65 > c_l_r))
) T2(e_l_r, d_l_r, c_l_r_r, a_r_r_r)
on (d_l_r > e_l)
) T1(e_l_l, d_l_r_l)
full join (
Select e, a
from p3
where (b = (83 + e))
) T2(e_r, a_r)
on (85 = e_l_l)
) T2
) T1(c_l, b_l, d_l)
left join (
select a, d
from (
select a, d
from (
select a, d
from (
Select a, d
from p1
where (33 = 29)
) T1
union all
select c, a
from (
Select c, a
from p5
where ((c > 87) OR (((64 - 34) = (b * b)) OR ((((23 - e) + 21) * a) < (69 * d))))
) T2
) T1
union all
select a, d
from (
select a, d
from (
Select a, d
from p2
where ((84 + b) < 36)
) T1
union all
select c, a
from (
Select c, a
from p3
where ((a < 68) AND (((c + e) = (d + b)) OR (a > e)))
) T2
) T2
) T1
union all
select e, a
from (
Select e, a, b
from p2
where (((d + 73) = 2) OR ((94 < (92 + d)) AND ((b > e) AND ((17 > 8) OR (((b - 86) < e) OR ((52 = b) AND (c = c)))))))
) T2
) T2(a_r, d_r)
on (a_r = b_l)
) T1
union all
select e, c, b, d
from (
Select e, c, b, d
from p3
where ((e = d) OR (7 < a))
) T2
) T1
union all
select e, c, a
from (
Select e, c, a
from p4
where ((b - e) = 72)
) T2
) T2
) T2(a_l_r, b_r_r)
on ((b_l + 68) < 94)
) T2(b_l_r, d_l_r, a_l_r_r, b_r_r_r)
on (d_l = a_l_r_r)
) T1(d_l_l, a_l_r_r_l)
full join (
Select c_l, e_r_r
from (
Select c
from p2
where (e < 52)
) T1(c_l)
left join (
Select c_l, e_r, c_r
from (
Select c
from p4
where ((a = 50) AND (e > 87))
) T1(c_l)
left join (
Select e, c, a
from p2
where (6 = d)
) T2(e_r, c_r, a_r)
on (((c_l * c_l) < c_r) AND (((c_l - c_r) = c_l) AND (c_r = (c_r - 89))))
) T2(c_l_r, e_r_r, c_r_r)
on ((c_l > c_l) AND (e_r_r = e_r_r))
) T2(c_l_r, e_r_r_r)
on (48 < d_l_l)
) T1(a_l_r_r_l_l, d_l_l_l, c_l_r_l, e_r_r_r_l)
left join (
Select a_l, e_r
from (
Select c, a, b
from p4
where (a = 77)
) T1(c_l, a_l, b_l)
left join (
select e
from (
select e, b
from (
Select e, b, d
from p5
where (e = a)
) T1
union all
select d_l, d_r
from (
Select d_l, d_r
from (
select c, d
from (
Select c, d
from p2
where (97 = e)
) T1
union all
select a, d
from (
Select a, d
from p2
where ((23 + d) < b)
) T2
) T1(c_l, d_l)
left join (
Select d
from p5
where (((b + 7) = (98 * 82)) OR (d < (83 * (34 * (c + e)))))
) T2(d_r)
on ((d_r - 87) > (d_l - d_l))
) T2
) T1
union all
select d
from (
Select d
from p1
where (98 < 70)
) T2
) T2(e_r)
on ((4 + (21 - 51)) < 63)
) T2(a_l_r, e_r_r)
on (a_l_r < 60)
) T1
union all
select c, b
from (
Select c, b
from p2
where (d < 34)
) T2
) T1(c_l_r_l_l, a_l_r_r_l_l_l)
left join (
select e, c
from (
Select e, c, d
from p3
where (((e * c) > 0) AND ((b > 98) AND (c = 77)))
) T1
union all
select a_l_l_r_l, c_r
from (
select a_l_l_r_l, c_r
from (
Select a_l_l_r_l, c_r
from (
Select c_r_l, a_l_l_r
from (
Select e_l, d_l, c_r
from (
Select e, d
from p5
where (a > (13 - 3))
) T1(e_l, d_l)
left join (
select c
from (
Select c, b, d
from p3
where (a < 42)
) T1
union all
select c
from (
Select c
from p5
where (e = 55)
) T2
) T2(c_r)
on (61 > 29)
) T1(e_l_l, d_l_l, c_r_l)
left join (
Select a_l_l, b_r_l, c_r
from (
Select a_l, d_l, e_r, b_r
from (
Select c, a, d
from p3
where ((d > a) AND (16 < 23))
) T1(c_l, a_l, d_l)
left join (
Select e, b
from p3
where ((61 < 10) OR (((b + 39) = e) OR (35 = 33)))
) T2(e_r, b_r)
on (b_r = e_r)
) T1(a_l_l, d_l_l, e_r_l, b_r_l)
inner join (
select c
from (
Select c
from p4
where ((92 = 64) AND (97 = (e - d)))
) T1
union all
select e
from (
Select e, c, b
from p2
where ((b * 32) = 0)
) T2
) T2(c_r)
on (89 < 57)
) T2(a_l_l_r, b_r_l_r, c_r_r)
on (24 < 94)
) T1(c_r_l_l, a_l_l_r_l)
inner join (
Select e, c
from p5
where ((d < 40) AND (d = (99 - d)))
) T2(e_r, c_r)
on (a_l_l_r_l = 55)
) T1
union all
select a_r_l, b_l_r_r
from (
Select a_r_l, b_l_r_r
from (
Select b_r_l, d_r_l, a_r, b_r
from (
Select a_l, b_r, d_r
from (
Select a, d
from p4
where (13 < 66)
) T1(a_l, d_l)
left join (
Select c, a, b, d
from p1
where ((73 > 78) OR (b > e))
) T2(c_r, a_r, b_r, d_r)
on ((55 < 32) AND (3 > ((28 + b_r) * a_l)))
) T1(a_l_l, b_r_l, d_r_l)
left join (
Select c, a, b
from p4
where (b = 93)
) T2(c_r, a_r, b_r)
on (b_r_l < (d_r_l * 44))
) T1(b_r_l_l, d_r_l_l, a_r_l, b_r_l)
full join (
Select d_l, b_l_r, e_r_r
from (
Select c, d
from p1
where (((44 + 51) > 98) OR ((e - b) = (92 * c)))
) T1(c_l, d_l)
full join (
Select a_l, b_l, e_r
from (
Select e, a, b
from p2
where ((97 + 20) = (63 * 70))
) T1(e_l, a_l, b_l)
left join (
Select e, c, a, b
from p5
where (40 = (89 - e))
) T2(e_r, c_r, a_r, b_r)
on (24 = e_r)
) T2(a_l_r, b_l_r, e_r_r)
on (b_l_r = b_l_r)
) T2(d_l_r, b_l_r_r, e_r_r_r)
on (a_r_l = a_r_l)
) T2
) T2
) T2(e_r, c_r)
on ((c_l_r_l_l < 6) OR ((65 = c_r) AND (c_l_r_l_l = c_l_r_l_l)))
) T1(c_l_r_l_l_l, c_r_l)
inner join (
Select c_l, b_l, e_r_r
from (
Select c, b
from p2
where (c > d)
) T1(c_l, b_l)
inner join (
Select a_l, b_l, e_r, d_r
from (
Select e, a, b
from p1
where ((24 - e) = c)
) T1(e_l, a_l, b_l)
left join (
select e, d
from (
Select e, d
from p1
where ((71 * 16) > 79)
) T1
union all
select b, d
from (
Select b, d
from p3
where ((1 < 68) AND (e = (((b * 76) + (a - (a - (96 * (41 - 97))))) * 37)))
) T2
) T2(e_r, d_r)
on (a_l > b_l)
) T2(a_l_r, b_l_r, e_r_r, d_r_r)
on (7 = 80)
) T2(c_l_r, b_l_r, e_r_r_r)
on ((e_r_r_r > 36) OR (c_r_l > ((97 * (((((34 * 3) * e_r_r_r) + (13 * e_r_r_r)) + c_l_r) * b_l_r)) * 22)))
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
Select a_l, a_l_r, b_r_r
from (
Select a
from p2
where (b > ((b + d) - (a - (b + c))))
) T1(a_l)
left join (
Select a_l, b_r
from (
Select e, a
from p2
where ((a > a) AND (((57 + 30) = c) OR (d = a)))
) T1(e_l, a_l)
left join (
Select b, d
from p1
where (a = (b + 36))
) T2(b_r, d_r)
on ((b_r + 33) > ((a_l - b_r) + a_l))
) T2(a_l_r, b_r_r)
on (64 > (b_r_r + 15))
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
Select d_r_l, c_r
from (
Select e_l_l, c_r_l, e_r, d_r
from (
Select e_l, c_l, c_r
from (
Select e, c
from p2
where (13 = c)
) T1(e_l, c_l)
inner join (
Select c
from p3
where ((20 = 34) OR (c < (((b - 17) - e) + 75)))
) T2(c_r)
on (39 < 64)
) T1(e_l_l, c_l_l, c_r_l)
left join (
Select e, c, d
from p5
where (e > (94 * 69))
) T2(e_r, c_r, d_r)
on ((16 = 94) OR ((e_l_l < e_l_l) AND ((e_l_l > 52) OR (e_r = (c_r_l + (79 - 48))))))
) T1(e_l_l_l, c_r_l_l, e_r_l, d_r_l)
left join (
select c, a
from (
select c, a, b
from (
Select c, a, b
from p1
where (63 = 31)
) T1
union all
select e, c, a
from (
Select e, c, a, d
from p5
where ((((d - 45) + 49) = a) OR (c < b))
) T2
) T1
union all
select b, d
from (
Select b, d
from p3
where (((86 + a) + 31) > 19)
) T2
) T2(c_r, a_r)
on ((76 > c_r) OR ((85 + 22) < 37))
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
Select a_l, b_l, d_l, a_r_r_r_r, c_l_r_r, d_l_r
from (
Select a, b, d
from p1
where (c > 44)
) T1(a_l, b_l, d_l)
left join (
Select d_l, c_l_r, a_r_r_r
from (
Select d
from p5
where ((11 = (14 - (b - d))) AND (19 < 33))
) T1(d_l)
left join (
Select c_l, a_r_r
from (
Select c, a
from p2
where ((e + (46 - 42)) = b)
) T1(c_l, a_l)
left join (
Select b_r_l, e_r, a_r
from (
Select a_l, d_l, b_r, d_r
from (
Select a, b, d
from p2
where ((a * 6) > c)
) T1(a_l, b_l, d_l)
left join (
select b, d
from (
Select b, d
from p5
where (d = c)
) T1
union all
select c, a
from (
Select c, a
from p1
where (e > e)
) T2
) T2(b_r, d_r)
on ((((b_r + b_r) + a_l) + d_r) = 88)
) T1(a_l_l, d_l_l, b_r_l, d_r_l)
left join (
select e, a
from (
Select e, a, b, d
from p1
where (((53 - (89 * d)) < ((b - (c - c)) + a)) OR ((c = 34) OR (4 = b)))
) T1
union all
select e_l, d_r
from (
Select e_l, d_r
from (
Select e
from p1
where ((b > 3) OR (8 = d))
) T1(e_l)
inner join (
Select d
from p2
where ((a + d) > 11)
) T2(d_r)
on (64 = 5)
) T2
) T2(e_r, a_r)
on ((e_r = (b_r_l - 90)) AND ((55 = 49) AND (65 < 22)))
) T2(b_r_l_r, e_r_r, a_r_r)
on ((((a_r_r + 23) * 4) - 15) < c_l)
) T2(c_l_r, a_r_r_r)
on (((61 * a_r_r_r) = a_r_r_r) AND (30 < (c_l_r + 56)))
) T2(d_l_r, c_l_r_r, a_r_r_r_r)
on (61 = c_l_r_r)
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
Select d_l_l_r_l, e_r_l_l, a_r
from (
select a_l_l, e_r_l, d_l_l_r
from (
Select a_l_l, e_r_l, d_l_l_r, a_r_l_l_r_l_r
from (
Select a_l, e_r
from (
Select c, a
from p4
where ((d < 75) OR (76 < ((49 * a) * a)))
) T1(c_l, a_l)
full join (
select e
from (
Select e
from p5
where (48 = c)
) T1
union all
select e
from (
Select e
from p5
where (44 < ((70 * e) + a))
) T2
) T2(e_r)
on (63 = e_r)
) T1(a_l_l, e_r_l)
full join (
Select a_r_l_l_r_l, d_l_l, c_r
from (
Select e_l, b_l, d_l, a_r_l_l_r, e_r_r
from (
Select e, b, d
from p1
where ((a + (a + 15)) < (e - 69))
) T1(e_l, b_l, d_l)
inner join (
Select a_r_l_l, d_l_r_l, e_r, a_r
from (
Select b_l_l_l, a_r_l, d_l_r
from (
Select b_l_l, a_r
from (
Select b_l, d_r
from (
Select b
from p4
where (86 = b)
) T1(b_l)
left join (
select d
from (
Select d
from p5
where (d < 9)
) T1
union all
select e
from (
Select e, c
from p3
where (66 = 2)
) T2
) T2(d_r)
on (((b_l + d_r) * (9 - 4)) > 28)
) T1(b_l_l, d_r_l)
full join (
Select a
from p4
where (e = (74 * c))
) T2(a_r)
on (a_r = 8)
) T1(b_l_l_l, a_r_l)
full join (
Select e_l, d_l, b_r
from (
Select e, c, b, d
from p3
where ((84 * d) = 83)
) T1(e_l, c_l, b_l, d_l)
inner join (
Select e, a, b
from p1
where (14 = b)
) T2(e_r, a_r, b_r)
on (((b_r * b_r) < d_l) OR (e_l > (b_r * 27)))
) T2(e_l_r, d_l_r, b_r_r)
on (70 < b_l_l_l)
) T1(b_l_l_l_l, a_r_l_l, d_l_r_l)
left join (
Select e, a
from p2
where ((a < c) AND (((e - 82) = d) OR (16 = 65)))
) T2(e_r, a_r)
on (d_l_r_l < 31)
) T2(a_r_l_l_r, d_l_r_l_r, e_r_r, a_r_r)
on (b_l > b_l)
) T1(e_l_l, b_l_l, d_l_l, a_r_l_l_r_l, e_r_r_l)
full join (
Select c
from p4
where ((c = 99) OR (((b - 9) = (36 * b)) OR (a = 75)))
) T2(c_r)
on ((38 + 40) = a_r_l_l_r_l)
) T2(a_r_l_l_r_l_r, d_l_l_r, c_r_r)
on (10 > 88)
) T1
union all
select e, a, b
from (
Select e, a, b
from p2
where ((25 * (57 - a)) = (69 * b))
) T2
) T1(a_l_l_l, e_r_l_l, d_l_l_r_l)
inner join (
Select c, a, d
from p4
where (((a - 44) > a) AND ((57 = (d - (e + b))) AND ((b = d) OR (c < 85))))
) T2(c_r, a_r, d_r)
on (95 > (e_r_l_l - 2))
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
Select b_r_l, a_r_l, d_l_r
from (
Select a_l, a_r, b_r
from (
Select a
from p5
where ((1 < a) AND ((62 = 70) OR (e = 4)))
) T1(a_l)
left join (
Select a, b
from p1
where (e > b)
) T2(a_r, b_r)
on (b_r < b_r)
) T1(a_l_l, a_r_l, b_r_l)
left join (
Select d_l, a_r
from (
Select d
from p1
where (d = 6)
) T1(d_l)
inner join (
Select a
from p4
where (((b - d) > 14) OR ((e + (a * b)) > 17))
) T2(a_r)
on (73 = ((a_r + a_r) * 53))
) T2(d_l_r, a_r_r)
on ((24 * d_l_r) > b_r_l)
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
Select e_l, d_r
from (
select e
from (
Select e, c
from p2
where ((83 = 23) OR (1 = b))
) T1
union all
select b
from (
Select b
from p1
where (49 < b)
) T2
) T1(e_l)
left join (
Select d
from p4
where ((53 * b) = 2)
) T2(d_r)
on ((39 = d_r) OR (e_l = e_l))
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
Select d_l, d_r
from (
Select b, d
from p1
where (e > 35)
) T1(b_l, d_l)
left join (
Select d
from p5
where ((a < b) AND (b < b))
) T2(d_r)
on (d_l = d_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test40exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l_l, e_r
from (
Select e_l, a_r
from (
Select e
from p1
where ((34 > a) OR (68 = 99))
) T1(e_l)
full join (
Select e, a, d
from p4
where ((d - 82) > 2)
) T2(e_r, a_r, d_r)
on (78 < 87)
) T1(e_l_l, a_r_l)
left join (
Select e
from p2
where (50 = e)
) T2(e_r)
on ((10 * 14) = e_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test40exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_l, b_r_r_l, b_r, d_r
from (
Select a_l, b_r_r
from (
select a
from (
Select a
from p5
where ((d = b) OR (c > 78))
) T1
union all
select c
from (
Select c
from p3
where ((e - a) = c)
) T2
) T1(a_l)
inner join (
Select c_l, d_l, c_r, b_r
from (
Select c, d
from p3
where (28 = e)
) T1(c_l, d_l)
inner join (
Select e, c, b
from p1
where (c = 32)
) T2(e_r, c_r, b_r)
on (90 > (58 * c_l))
) T2(c_l_r, d_l_r, c_r_r, b_r_r)
on (b_r_r < 11)
) T1(a_l_l, b_r_r_l)
left join (
Select e, b, d
from p3
where ((26 > (c * b)) OR ((45 > 76) OR ((58 - 4) < 13)))
) T2(e_r, b_r, d_r)
on ((b_r = (20 + 45)) OR (a_l_l > 77))
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
Select a_l, b_l, b_r
from (
Select e, a, b
from p4
where (70 = d)
) T1(e_l, a_l, b_l)
left join (
select a, b
from (
Select a, b
from p3
where (47 > (33 - 4))
) T1
union all
select c_l, b_r
from (
Select c_l, b_r, d_r
from (
Select c
from p4
where ((19 = e) AND (92 = b))
) T1(c_l)
left join (
Select e, b, d
from p2
where (e > (e + 83))
) T2(e_r, b_r, d_r)
on (b_r > 97)
) T2
) T2(a_r, b_r)
on ((b_l < 79) AND (3 = b_l))
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
Select e_l_l, d_l_l, c_r, a_r
from (
Select e_l, d_l, a_r
from (
Select e, c, d
from p4
where (55 < a)
) T1(e_l, c_l, d_l)
full join (
Select a
from p4
where (21 = (e + e))
) T2(a_r)
on (60 < 57)
) T1(e_l_l, d_l_l, a_r_l)
left join (
select c, a
from (
Select c, a, b
from p3
where (d > b)
) T1
union all
select e, a
from (
Select e, a
from p2
where ((c = 96) OR (67 = d))
) T2
) T2(c_r, a_r)
on (e_l_l = 67)
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
Select b_l, e_r, b_r
from (
Select b
from p5
where ((14 = (46 - e)) OR (48 = 31))
) T1(b_l)
inner join (
Select e, b
from p1
where (a = 7)
) T2(e_r, b_r)
on ((b_r = (42 + (b_l - b_r))) OR ((75 > 5) OR (68 < b_r)))
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
    #************************
    _testmgr.testcase_end(desc)

