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
    
def test001(desc="""Joins Set 10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
Select c_l_l, e_r, c_r
from (
select c_l, a_r
from (
Select c_l, a_r
from (
Select c, d
from p3
where (64 < 95)
) T1(c_l, d_l)
full join (
Select a
from p5
where (e < 11)
) T2(a_r)
on (c_l < (77 + ((94 * 92) * c_l)))
) T1
union all
select e, d
from (
Select e, d
from p5
where (e = 45)
) T2
) T1(c_l_l, a_r_l)
inner join (
select e, c
from (
Select e, c, b, d
from p2
where ((b + 2) > ((a * 83) + (d + a)))
) T1
union all
select e, c
from (
Select e, c
from p2
where (62 = 83)
) T2
) T2(e_r, c_r)
on ((91 - 39) = (c_l_l + e_r))
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
Select a_l_l, d_r_l, b_l_l, d_r_r, d_l_r
from (
Select a_l, b_l, d_r
from (
Select e, a, b
from p4
where (d = (a + 79))
) T1(e_l, a_l, b_l)
inner join (
Select d
from p1
where (4 = 98)
) T2(d_r)
on ((d_r = 96) AND (66 > (a_l * 7)))
) T1(a_l_l, b_l_l, d_r_l)
left join (
Select d_l, e_r, d_r
from (
Select a, d
from p2
where (e = 50)
) T1(a_l, d_l)
full join (
Select e, d
from p3
where (28 < 39)
) T2(e_r, d_r)
on ((11 > 8) OR ((d_l < e_r) AND (d_l < 65)))
) T2(d_l_r, e_r_r, d_r_r)
on ((75 > 78) AND (d_r_r = (42 + 79)))
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
Select e_l, b_l, a_r
from (
Select e, b
from p3
where (d = 8)
) T1(e_l, b_l)
inner join (
Select a, d
from p5
where (9 = e)
) T2(a_r, d_r)
on ((51 = b_l) AND (a_r > ((9 - 40) + e_l)))
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
Select c_l, d_l, d_r
from (
select c, d
from (
Select c, d
from p1
where (((d * 80) < a) OR (99 = 41))
) T1
union all
select e, d
from (
Select e, d
from p3
where (((a + e) > d) OR ((65 < a) AND ((0 = (((c * b) * c) - e)) AND (((88 * 72) = 60) AND (((d - 19) + a) < 83)))))
) T2
) T1(c_l, d_l)
left join (
select d
from (
Select d
from p2
where ((42 > 87) AND (((c - a) * (40 * a)) = 84))
) T1
union all
select e
from (
Select e, d
from p4
where ((e - e) > d)
) T2
) T2(d_r)
on (32 < (93 - 56))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, d_l, c_r
from (
Select b, d
from p1
where ((83 < (27 + b)) OR ((95 = e) OR ((24 - (0 * d)) = ((e * b) * d))))
) T1(b_l, d_l)
inner join (
Select c
from p4
where (b = (98 * 79))
) T2(c_r)
on (61 < b_l)
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
Select e_l, a_l, e_r, b_r
from (
Select e, a
from p3
where (37 > a)
) T1(e_l, a_l)
inner join (
select e, c, b
from (
Select e, c, b, d
from p5
where (d = (96 - (c - (27 + 57))))
) T1
union all
select b_l, d_l, d_r_r_r
from (
Select b_l, d_l, d_r_r_r
from (
Select a, b, d
from p2
where (21 > 67)
) T1(a_l, b_l, d_l)
left join (
Select c_r_l, b_l_l, d_r_r, a_r_r
from (
Select b_l, c_r, b_r
from (
Select b
from p2
where (b > (b + b))
) T1(b_l)
full join (
Select c, b
from p4
where (b < a)
) T2(c_r, b_r)
on (b_r = 84)
) T1(b_l_l, c_r_l, b_r_l)
inner join (
Select d_l, a_r, d_r
from (
Select b, d
from p1
where (41 > e)
) T1(b_l, d_l)
left join (
Select a, b, d
from p3
where (e = 38)
) T2(a_r, b_r, d_r)
on (((a_r * a_r) = 58) AND (((53 - d_l) - d_l) < 93))
) T2(d_l_r, a_r_r, d_r_r)
on (a_r_r > 86)
) T2(c_r_l_r, b_l_l_r, d_r_r_r, a_r_r_r)
on (d_l < 31)
) T2
) T2(e_r, c_r, b_r)
on (e_r = 42)
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
Select d_l, e_r
from (
Select c, b, d
from p3
where (c = c)
) T1(c_l, b_l, d_l)
inner join (
Select e
from p1
where ((70 < d) AND (57 = a))
) T2(e_r)
on (81 < 3)
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
Select e, b, d
from p2
where (12 = 29)
) T1(e_l, b_l, d_l)
inner join (
select c
from (
Select c
from p4
where (12 = 85)
) T1
union all
select a_l
from (
Select a_l, a_r
from (
Select e, a, b, d
from p3
where (0 < 2)
) T1(e_l, a_l, b_l, d_l)
left join (
Select c, a
from p4
where (e < c)
) T2(c_r, a_r)
on ((a_l = a_r) OR (a_r = a_l))
) T2
) T2(c_r)
on (((65 * 58) = c_r) OR (c_r = c_r))
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
Select a_l, d_r_r
from (
Select a
from p4
where (d = b)
) T1(a_l)
full join (
Select e_l, d_l, d_r
from (
Select e, d
from p3
where (c = 98)
) T1(e_l, d_l)
full join (
Select e, c, a, d
from p4
where (((93 + (d + e)) < 84) OR ((18 < 30) AND (b < 59)))
) T2(e_r, c_r, a_r, d_r)
on (0 > 62)
) T2(e_l_r, d_l_r, d_r_r)
on ((a_l = d_r_r) AND (((d_r_r + d_r_r) > a_l) OR ((54 + a_l) = a_l)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, e_r
from (
Select e, a
from p1
where ((78 > b) OR (74 = c))
) T1(e_l, a_l)
inner join (
Select e, a, b
from p5
where ((81 = d) OR (63 = e))
) T2(e_r, a_r, b_r)
on ((e_r + (10 - a_l)) > 65)
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
Select c_l, a_l, a_l_r, c_r_r, b_l_r
from (
select c, a, b, d
from (
Select c, a, b, d
from p3
where (97 = a)
) T1
union all
select e, c, b, d
from (
Select e, c, b, d
from p5
where ((c > (((c * 15) * e) * b)) AND (a = 23))
) T2
) T1(c_l, a_l, b_l, d_l)
full join (
select a_l, b_l, c_r
from (
Select a_l, b_l, c_r, b_r
from (
Select a, b, d
from p4
where (80 = (96 * (78 * (47 + d))))
) T1(a_l, b_l, d_l)
inner join (
Select c, b
from p1
where ((d > 47) OR (95 = (d * c)))
) T2(c_r, b_r)
on ((84 = (((b_l + 78) - 2) - 27)) OR ((b_r - 23) = c_r))
) T1
union all
select e, c, a
from (
Select e, c, a
from p1
where ((d = d) AND (4 = 0))
) T2
) T2(a_l_r, b_l_r, c_r_r)
on ((c_l = 89) AND ((66 = 41) OR ((a_l_r = b_l_r) OR (21 = 6))))
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
Select e_l, b_l, a_r, b_r
from (
Select e, b
from p5
where (b = 90)
) T1(e_l, b_l)
left join (
Select a, b
from p3
where (e = c)
) T2(a_r, b_r)
on (51 < 68)
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
Select d_l, e_r_l_r
from (
Select d
from p2
where ((92 < b) AND ((d = e) AND (d > c)))
) T1(d_l)
full join (
Select d_l_l, e_r_l, d_r
from (
Select d_l, e_r
from (
Select b, d
from p2
where (95 < 73)
) T1(b_l, d_l)
left join (
Select e, a
from p5
where (e = (e + ((a * 15) * ((b * 22) - b))))
) T2(e_r, a_r)
on ((67 = 44) AND ((24 + 11) < (d_l * d_l)))
) T1(d_l_l, e_r_l)
full join (
Select d
from p2
where (d = c)
) T2(d_r)
on (d_l_l < d_l_l)
) T2(d_l_l_r, e_r_l_r, d_r_r)
on (31 < d_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, e_r, c_r
from (
select d
from (
Select d
from p5
where (21 > (8 * 88))
) T1
union all
select d
from (
select d
from (
Select d
from p5
where ((1 * 99) < b)
) T1
union all
select a
from (
Select a
from p5
where ((d * (40 + (85 + 32))) = 24)
) T2
) T2
) T1(d_l)
left join (
Select e, c
from p5
where ((a = (93 - a)) OR (c = a))
) T2(e_r, c_r)
on (89 = 59)
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
Select a_l_r_l, a_l_l_l, c_r
from (
Select a_l_l, b_r_l, a_l_r, a_r_r
from (
Select e_l, a_l, b_r
from (
Select e, a, d
from p1
where (23 = 30)
) T1(e_l, a_l, d_l)
left join (
Select b
from p4
where ((b > 35) AND (51 < e))
) T2(b_r)
on (29 < b_r)
) T1(e_l_l, a_l_l, b_r_l)
left join (
select a_l, a_r
from (
select a_l, a_r
from (
Select a_l, a_r
from (
Select e, a
from p3
where ((30 = (a * a)) AND ((a - 40) = d))
) T1(e_l, a_l)
left join (
Select a
from p5
where (d < 54)
) T2(a_r)
on (3 = 4)
) T1
union all
select e, c
from (
Select e, c, d
from p4
where ((((28 - (e - (57 * c))) + (a * c)) = d) AND (d = e))
) T2
) T1
union all
select e, b
from (
Select e, b
from p5
where (c = e)
) T2
) T2(a_l_r, a_r_r)
on (56 = 67)
) T1(a_l_l_l, b_r_l_l, a_l_r_l, a_r_r_l)
left join (
Select c, d
from p4
where ((76 < b) AND ((a = d) AND (d > 3)))
) T2(c_r, d_r)
on ((((35 - (88 * ((96 + a_l_l_l) * ((c_r * c_r) + 80)))) - a_l_l_l) * 31) < 8)
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
Select a_l, c_l_l_r
from (
Select a
from p2
where (a > 87)
) T1(a_l)
inner join (
Select c_l_l, d_r
from (
Select c_l, d_l, d_r_l_r_r, a_r_l_r
from (
Select c, a, d
from p2
where (((((35 - ((a + (((5 - 6) * 43) - a)) + (66 - 15))) + 65) * (74 - (b + d))) = b) AND ((d = (69 + c)) AND (84 < a)))
) T1(c_l, a_l, d_l)
left join (
select a_r_l, d_r_l_r
from (
Select a_r_l, d_r_l_r
from (
Select b_r_l, a_r
from (
Select b_l, b_r
from (
Select b
from p4
where (a > a)
) T1(b_l)
left join (
Select a, b
from p3
where (e = ((e + (c - c)) - 77))
) T2(a_r, b_r)
on ((33 = b_r) OR ((b_l > 19) AND (76 = 14)))
) T1(b_l_l, b_r_l)
left join (
Select a
from p5
where ((47 = 90) AND (4 = c))
) T2(a_r)
on ((a_r = a_r) OR ((15 = 28) OR ((b_r_l + 94) = 63)))
) T1(b_r_l_l, a_r_l)
full join (
Select d_r_l, c_r, b_r
from (
Select e_l_r_l, d_r_r_l, b_r, d_r
from (
Select a_l, e_l_r, d_r_r
from (
Select a
from p2
where (c = 13)
) T1(a_l)
inner join (
Select e_l, d_r
from (
Select e, d
from p2
where (((b * 22) > (66 - b)) OR ((92 = e) AND (77 > 10)))
) T1(e_l, d_l)
full join (
Select d
from p4
where ((55 * b) = (75 - b))
) T2(d_r)
on ((d_r > 98) OR (59 > d_r))
) T2(e_l_r, d_r_r)
on (a_l < 7)
) T1(a_l_l, e_l_r_l, d_r_r_l)
left join (
Select c, a, b, d
from p3
where ((e = a) AND (e > (a + (c + e))))
) T2(c_r, a_r, b_r, d_r)
on ((((b_r + 95) + 62) = (6 * 81)) AND (48 < 4))
) T1(e_l_r_l_l, d_r_r_l_l, b_r_l, d_r_l)
left join (
Select c, b
from p1
where (c > 99)
) T2(c_r, b_r)
on (c_r < 82)
) T2(d_r_l_r, c_r_r, b_r_r)
on (46 > 1)
) T1
union all
select a, d
from (
Select a, d
from p5
where ((e < 29) AND (85 = 43))
) T2
) T2(a_r_l_r, d_r_l_r_r)
on ((24 + d_r_l_r_r) = (97 + a_r_l_r))
) T1(c_l_l, d_l_l, d_r_l_r_r_l, a_r_l_r_l)
left join (
Select d
from p2
where (8 > ((((d * (0 - 67)) - 16) + c) - 61))
) T2(d_r)
on (65 < d_r)
) T2(c_l_l_r, d_r_r)
on (((c_l_l_r - a_l) < ((c_l_l_r - 10) + 34)) AND ((37 = a_l) OR (49 > (c_l_l_r + 41))))
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
Select b_l, d_l, e_r, a_r
from (
Select b, d
from p3
where (((e + e) = 74) AND (a = (a + (((b * e) * 22) - 49))))
) T1(b_l, d_l)
left join (
Select e, a
from p1
where (10 = a)
) T2(e_r, a_r)
on (d_l < 32)
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
Select a_l, d_l, c_r
from (
select a, d
from (
Select a, d
from p5
where (73 < e)
) T1
union all
select b, d
from (
Select b, d
from p5
where (b < c)
) T2
) T1(a_l, d_l)
inner join (
Select c
from p5
where (((c - 28) = d) OR ((82 - e) < 14))
) T2(c_r)
on (a_l = a_l)
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
Select e, c, d
from p3
where (e = 84)
) T1(e_l, c_l, d_l)
inner join (
Select e_l, c_l, a_r
from (
Select e, c, a
from p5
where (a = d)
) T1(e_l, c_l, a_l)
left join (
Select a
from p3
where (20 < c)
) T2(a_r)
on (46 = e_l)
) T2(e_l_r, c_l_r, a_r_r)
on (d_l < d_l)
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
Select b_l, a_r_r
from (
Select b
from p5
where (7 < 24)
) T1(b_l)
left join (
Select c_r_r_l_l, a_r
from (
Select c_r_r_l, c_r, a_r
from (
Select c_l_l, c_r_r
from (
select c_l
from (
Select c_l, b_l, a_r
from (
Select c, a, b
from p5
where (((43 * (c * 56)) > e) AND (((c * 8) * d) > (54 + 63)))
) T1(c_l, a_l, b_l)
full join (
Select e, a
from p4
where ((a = b) OR (e = (17 + ((22 * (95 - d)) + b))))
) T2(e_r, a_r)
on (((c_l * 27) * c_l) = 16)
) T1
union all
select a
from (
Select a
from p4
where ((d - 41) = 81)
) T2
) T1(c_l_l)
inner join (
Select e_l, c_r
from (
Select e, c
from p2
where ((50 = c) AND ((22 > (12 + 36)) OR (c = d)))
) T1(e_l, c_l)
full join (
select e, c, a
from (
Select e, c, a, b
from p5
where (b = ((36 - a) + 2))
) T1
union all
select a_l, b_l, b_r
from (
Select a_l, b_l, b_r
from (
Select e, a, b
from p4
where (a = d)
) T1(e_l, a_l, b_l)
left join (
select b
from (
Select b
from p4
where ((86 * ((32 * (58 * 51)) + 74)) > 85)
) T1
union all
select c
from (
Select c, b
from p1
where (d > 6)
) T2
) T2(b_r)
on (((77 - a_l) - 87) < b_l)
) T2
) T2(e_r, c_r, a_r)
on ((((c_r - (92 - (52 * c_r))) + (5 * e_l)) = (e_l + 86)) AND (16 < 9))
) T2(e_l_r, c_r_r)
on ((17 = c_r_r) AND (c_l_l > 14))
) T1(c_l_l_l, c_r_r_l)
left join (
Select c, a
from p1
where ((98 - e) < 39)
) T2(c_r, a_r)
on (89 = (31 * c_r))
) T1(c_r_r_l_l, c_r_l, a_r_l)
inner join (
Select c, a, b
from p3
where (43 = b)
) T2(c_r, a_r, b_r)
on ((74 = 18) AND ((a_r < 79) AND ((2 < c_r_r_l_l) OR ((c_r_r_l_l = (2 + 91)) OR ((c_r_r_l_l = a_r) OR ((20 > a_r) OR ((77 - c_r_r_l_l) = 65)))))))
) T2(c_r_r_l_l_r, a_r_r)
on ((4 < a_r_r) AND ((a_r_r > 66) OR (a_r_r > b_l)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #*******************************************
    _testmgr.testcase_end(desc)

