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
    
def test001(desc="""Joins Set 3"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
Select d_r_r_l_l, a_r_l, a_r
from (
Select a_l_l, d_r_r_l, a_r, b_r
from (
Select a_l, d_r_r, d_l_r
from (
Select a
from p2
where (a = d)
) T1(a_l)
full join (
select d_l, d_r
from (
Select d_l, d_r
from (
Select e, a, d
from p5
where (e = 41)
) T1(e_l, a_l, d_l)
left join (
Select e, a, b, d
from p4
where (e = 16)
) T2(e_r, a_r, b_r, d_r)
on (d_l = d_r)
) T1
union all
select a, b
from (
Select a, b
from p4
where (67 = 32)
) T2
) T2(d_l_r, d_r_r)
on (30 < 61)
) T1(a_l_l, d_r_r_l, d_l_r_l)
left join (
Select a, b
from p2
where (32 = d)
) T2(a_r, b_r)
on (((93 - 86) < a_r) AND ((((58 * b_r) - (43 - d_r_r_l)) * d_r_r_l) > 25))
) T1(a_l_l_l, d_r_r_l_l, a_r_l, b_r_l)
left join (
Select a
from p5
where ((c < 23) AND (3 = d))
) T2(a_r)
on ((d_r_r_l_l < 19) AND ((13 < 49) AND (54 = (27 + 44))))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l_l, e_r, c_r
from (
Select e_l, d_l, b_r
from (
Select e, d
from p1
where (c < 57)
) T1(e_l, d_l)
full join (
Select b
from p5
where (d > 23)
) T2(b_r)
on (4 < 81)
) T1(e_l_l, d_l_l, b_r_l)
inner join (
Select e, c
from p4
where (c < d)
) T2(e_r, c_r)
on (c_r > e_r)
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
Select b, d
from p5
where (e = 59)
) T1(b_l, d_l)
left join (
Select e, c
from p4
where (((d * c) + c) > 54)
) T2(e_r, c_r)
on (e_r = 35)
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
Select b_r_l_l, c_r_l, d_l_r
from (
Select b_r_l, c_r
from (
Select c_l_l, d_l_l, b_r
from (
Select c_l, d_l, d_r
from (
Select c, d
from p4
where (74 > e)
) T1(c_l, d_l)
full join (
Select b, d
from p2
where (((b + c) = 52) AND ((17 * d) < 51))
) T2(b_r, d_r)
on ((d_r > 28) OR (43 > d_l))
) T1(c_l_l, d_l_l, d_r_l)
inner join (
Select b
from p2
where (74 > (41 + c))
) T2(b_r)
on ((92 - 0) > (d_l_l - 50))
) T1(c_l_l_l, d_l_l_l, b_r_l)
full join (
Select e, c
from p1
where (38 = b)
) T2(e_r, c_r)
on (c_r > c_r)
) T1(b_r_l_l, c_r_l)
left join (
Select d_l, d_r
from (
Select d
from p1
where (48 > 80)
) T1(d_l)
full join (
Select d
from p4
where ((66 * 7) < (98 + d))
) T2(d_r)
on (5 = d_l)
) T2(d_l_r, d_r_r)
on ((14 + d_l_r) > d_l_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_r, d_r
from (
Select c
from p3
where (9 = c)
) T1(c_l)
inner join (
Select b, d
from p3
where (e > c)
) T2(b_r, d_r)
on (24 = 35)
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
Select a_r_l, b_l_l, d_r
from (
Select b_l, a_r
from (
select b
from (
Select b
from p4
where (26 = 5)
) T1
union all
select e
from (
select e, c
from (
Select e, c, a, d
from p2
where (c > d)
) T1
union all
select e, a
from (
select e, a
from (
select e, a
from (
Select e, a, b, d
from p1
where ((30 * (a - 6)) = (c - 66))
) T1
union all
select e, c
from (
Select e, c
from p1
where (92 = b)
) T2
) T1
union all
select a, b
from (
Select a, b
from p2
where (b = (33 * 96))
) T2
) T2
) T2
) T1(b_l)
left join (
Select c, a, b, d
from p1
where (b < 39)
) T2(c_r, a_r, b_r, d_r)
on ((b_l - a_r) = 54)
) T1(b_l_l, a_r_l)
left join (
Select a, d
from p2
where ((38 + (e + (82 * 74))) = 89)
) T2(a_r, d_r)
on (a_r_l = a_r_l)
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
Select e_r_l, d_r_r
from (
Select e_l, e_r, a_r
from (
Select e
from p2
where (22 < (65 - a))
) T1(e_l)
full join (
Select e, a
from p3
where ((b < 65) AND (34 = d))
) T2(e_r, a_r)
on (a_r = 90)
) T1(e_l_l, e_r_l, a_r_l)
left join (
Select d_l, d_r
from (
Select d
from p2
where (80 = c)
) T1(d_l)
full join (
Select d
from p3
where (((91 - b) > 49) OR (d < a))
) T2(d_r)
on (42 = d_l)
) T2(d_l_r, d_r_r)
on (30 < 66)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_l, c_r
from (
Select c_l, d_r
from (
Select c, a
from p2
where (11 = (e - 65))
) T1(c_l, a_l)
inner join (
Select d
from p4
where (b < d)
) T2(d_r)
on (18 < d_r)
) T1(c_l_l, d_r_l)
inner join (
Select e, c
from p3
where ((a + 51) = 1)
) T2(e_r, c_r)
on ((44 = (((32 + c_l_l) - ((c_l_l - 30) + c_r)) - 2)) AND (96 < 92))
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
Select c_l, b_l, c_r, a_r
from (
Select c, a, b
from p2
where (b < (18 * (57 + (d + c))))
) T1(c_l, a_l, b_l)
left join (
Select c, a
from p4
where (13 < d)
) T2(c_r, a_r)
on (c_l < 46)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_r_l, a_l_r, c_l_r_r, e_l_r, e_l_r_r
from (
Select a_l, e_r, a_r
from (
select c, a
from (
Select c, a, d
from p3
where (0 < 67)
) T1
union all
select c, a
from (
Select c, a
from p5
where ((c = (41 * 67)) AND (68 > d))
) T2
) T1(c_l, a_l)
inner join (
Select e, a, b
from p5
where (76 = d)
) T2(e_r, a_r, b_r)
on (a_l = a_r)
) T1(a_l_l, e_r_l, a_r_l)
left join (
Select e_l, a_l, c_l_r, e_l_r
from (
Select e, a, d
from p5
where ((62 = 16) OR (99 = 3))
) T1(e_l, a_l, d_l)
left join (
select e_l, c_l, a_r
from (
Select e_l, c_l, a_r
from (
Select e, c
from p3
where (c = (68 + d))
) T1(e_l, c_l)
inner join (
select a
from (
Select a
from p1
where (93 = 0)
) T1
union all
select c_l
from (
select c_l, c_r, b_r
from (
Select c_l, c_r, b_r
from (
Select e, c, b, d
from p4
where (42 = (81 * (5 - (e + (36 + 44)))))
) T1(e_l, c_l, b_l, d_l)
inner join (
Select c, b
from p3
where ((15 = c) AND (c = d))
) T2(c_r, b_r)
on ((c_r = (84 + 0)) OR (c_l = c_r))
) T1
union all
select c, a, d
from (
Select c, a, d
from p5
where ((53 > 77) OR ((a > 97) OR (b = 19)))
) T2
) T2
) T2(a_r)
on ((e_l < (54 * 68)) OR (98 = 85))
) T1
union all
select e, c, a
from (
Select e, c, a
from p2
where (((b - 6) * 45) = b)
) T2
) T2(e_l_r, c_l_r, a_r_r)
on (72 < 88)
) T2(e_l_r, a_l_r, c_l_r_r, e_l_r_r)
on (57 = (24 + (22 + 51)))
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
Select e_l, e_r, a_r
from (
Select e, c, d
from p5
where ((57 * c) = b)
) T1(e_l, c_l, d_l)
left join (
Select e, a
from p1
where (88 = 83)
) T2(e_r, a_r)
on (51 = a_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, e_r, a_r
from (
Select e, b, d
from p1
where ((68 = d) OR ((95 > 68) OR (((45 - d) > 12) AND ((98 > a) AND (a > (80 - d))))))
) T1(e_l, b_l, d_l)
full join (
Select e, a
from p3
where (((b + 47) = 69) OR (45 < 11))
) T2(e_r, a_r)
on (58 < (64 * (25 * (27 - (e_l + a_r)))))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_l, b_r_l, b_r
from (
Select a_l, c_r, b_r
from (
select a
from (
Select a
from p5
where (1 > d)
) T1
union all
select e_l
from (
Select e_l, a_l, d_r
from (
Select e, a, d
from p1
where ((b - d) < 70)
) T1(e_l, a_l, d_l)
left join (
Select d
from p3
where ((2 - ((c * 68) * d)) = (33 + 19))
) T2(d_r)
on ((e_l * d_r) = e_l)
) T2
) T1(a_l)
left join (
Select c, b
from p4
where ((((36 * c) * 68) * 99) < (c - ((6 - 17) + ((c * 50) * d))))
) T2(c_r, b_r)
on (13 = 81)
) T1(a_l_l, c_r_l, b_r_l)
full join (
Select b
from p5
where (a = 49)
) T2(b_r)
on (((67 - 85) - b_r_l) < 67)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, b_l_r_r, d_l_l_r
from (
Select d
from p2
where ((a + d) = a)
) T1(d_l)
full join (
Select d_l_l, b_l_r, e_r_r
from (
Select d_l, d_r
from (
Select d
from p5
where (86 = 1)
) T1(d_l)
left join (
Select b, d
from p4
where ((89 > b) AND ((7 > 7) AND ((b > 13) OR (d > c))))
) T2(b_r, d_r)
on (17 = d_r)
) T1(d_l_l, d_r_l)
left join (
Select b_l, d_l, e_r, d_r
from (
Select e, a, b, d
from p4
where ((29 = e) OR ((95 = ((23 * 92) - 44)) OR ((((((31 * 62) * a) - b) + e) = 11) AND (a < 47))))
) T1(e_l, a_l, b_l, d_l)
left join (
Select e, d
from p5
where (d > a)
) T2(e_r, d_r)
on ((d_r * (b_l + 69)) > 82)
) T2(b_l_r, d_l_r, e_r_r, d_r_r)
on ((47 = (5 - (d_l_l * 15))) OR ((b_l_r * 87) = b_l_r))
) T2(d_l_l_r, b_l_r_r, e_r_r_r)
on ((41 = (d_l + (b_l_r_r * d_l))) OR ((d_l + b_l_r_r) = 90))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l_r
from (
select c
from (
select c
from (
Select c
from p4
where (c = e)
) T1
union all
select e
from (
Select e, c, d
from p5
where (((e + 8) = a) AND (a < (30 - 72)))
) T2
) T1
union all
select a
from (
select a, d
from (
Select a, d
from p2
where (a < e)
) T1
union all
select c_l, b_r
from (
Select c_l, b_r, d_r
from (
Select e, c
from p3
where ((a = 44) AND ((b = 7) OR (86 < a)))
) T1(e_l, c_l)
left join (
Select c, b, d
from p4
where (98 = (d + 35))
) T2(c_r, b_r, d_r)
on ((20 * (61 * 96)) > 85)
) T2
) T2
) T1(c_l)
left join (
Select a_l, b_l, a_r, d_r
from (
Select c, a, b
from p3
where ((2 < 46) AND (e = b))
) T1(c_l, a_l, b_l)
left join (
Select a, d
from p1
where ((69 > 63) OR ((d > a) OR (13 = ((e + 69) + 94))))
) T2(a_r, d_r)
on ((4 * 25) > b_l)
) T2(a_l_r, b_l_r, a_r_r, d_r_r)
on (b_l_r = (86 - 34))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, b_r, d_r
from (
Select b
from p1
where ((c < b) OR (61 < e))
) T1(b_l)
full join (
Select a, b, d
from p1
where (a > (d * d))
) T2(a_r, b_r, d_r)
on ((7 > b_l) OR (((97 * (((d_r - (22 * b_l)) - 32) * b_l)) = b_r) OR ((16 * (((62 - b_l) + d_r) + 37)) > 39)))
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
Select b_l, d_l, c_r_r, b_l_r
from (
Select b, d
from p5
where ((81 < e) OR ((c < a) OR (c = 33)))
) T1(b_l, d_l)
left join (
Select b_l, d_l, c_r
from (
Select b, d
from p2
where ((a = 71) AND (62 > (68 - 68)))
) T1(b_l, d_l)
left join (
Select c
from p2
where (a = ((d * a) - 39))
) T2(c_r)
on (58 < 83)
) T2(b_l_r, d_l_r, c_r_r)
on (((b_l * ((81 * b_l) + 9)) < d_l) OR ((53 < (80 * d_l)) AND ((8 = 64) OR (28 > 67))))
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
Select a_r_r_l, e_l_r_l, c_r
from (
Select c_l, d_l, b_r_r, e_l_r, a_r_r
from (
Select c, b, d
from p2
where (32 < e)
) T1(c_l, b_l, d_l)
left join (
Select e_l, d_l, a_r, b_r
from (
Select e, d
from p5
where (24 = 13)
) T1(e_l, d_l)
left join (
Select a, b
from p4
where (13 = 66)
) T2(a_r, b_r)
on ((a_r - 52) < b_r)
) T2(e_l_r, d_l_r, a_r_r, b_r_r)
on (((56 - e_l_r) = (84 + 23)) OR (a_r_r > a_r_r))
) T1(c_l_l, d_l_l, b_r_r_l, e_l_r_l, a_r_r_l)
full join (
Select c
from p4
where (88 > (c * 22))
) T2(c_r)
on (((a_r_r_l - 1) = a_r_r_l) AND ((41 = c_r) OR ((e_l_r_l = 43) OR ((a_r_r_l = a_r_r_l) OR ((e_l_r_l < a_r_r_l) OR (((21 - (e_l_r_l - 56)) = (33 + (e_l_r_l + 14))) OR (c_r = e_l_r_l)))))))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test03exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, b_r_r, b_l_r
from (
Select b, d
from p5
where (b < a)
) T1(b_l, d_l)
full join (
Select b_l, b_r
from (
Select b, d
from p3
where (((30 - c) = e) OR (d = (((15 * 2) + a) - 34)))
) T1(b_l, d_l)
left join (
select c, b, d
from (
Select c, b, d
from p4
where (((81 * (34 + (31 - 64))) = 52) AND ((15 = 93) OR ((66 = ((70 - 84) - d)) OR (20 < a))))
) T1
union all
select e, a, b
from (
Select e, a, b
from p1
where (58 < d)
) T2
) T2(c_r, b_r, d_r)
on (b_r > b_r)
) T2(b_l_r, b_r_r)
on ((b_r_r * b_r_r) = (b_r_r * 28))
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
Select e_l, e_r, a_r
from (
Select e
from p4
where ((((a - 83) + 44) > ((31 + 30) + c)) OR ((c = (d * (e + 37))) OR (d > b)))
) T1(e_l)
inner join (
Select e, a, d
from p2
where ((5 - (b * 67)) = c)
) T2(e_r, a_r, d_r)
on (40 = 64)
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
    #*****************************************
    _testmgr.testcase_end(desc)

