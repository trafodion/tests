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
    
def test001(desc="""Joins Set 33"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, c_r
from (
select e, d
from (
Select e, d
from p3
where (((24 * d) * 79) > b)
) T1
union all
select c, b
from (
Select c, b
from p4
where (c < a)
) T2
) T1(e_l, d_l)
inner join (
Select c, a
from p2
where ((56 + a) = 96)
) T2(c_r, a_r)
on ((88 + 61) = 83)
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
Select c_l, b_r_r, e_l_r
from (
Select c
from p4
where ((65 - e) = 17)
) T1(c_l)
full join (
Select e_l, a_l, b_r, d_r
from (
Select e, a
from p4
where (((79 * 37) - 5) > ((24 * 49) + 7))
) T1(e_l, a_l)
left join (
Select b, d
from p4
where (45 > c)
) T2(b_r, d_r)
on (14 > a_l)
) T2(e_l_r, a_l_r, b_r_r, d_r_r)
on (39 < e_l_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_l, d_l_l_r, e_r_l_r
from (
Select e, a, b
from p1
where (b = ((30 + (b + 2)) + 65))
) T1(e_l, a_l, b_l)
left join (
Select d_l_l, e_r_l, b_r
from (
Select d_l, e_r
from (
Select a, d
from p3
where (5 > 0)
) T1(a_l, d_l)
full join (
Select e, d
from p4
where ((91 + 50) = a)
) T2(e_r, d_r)
on (d_l < d_l)
) T1(d_l_l, e_r_l)
inner join (
select b
from (
Select b
from p1
where ((48 < 65) OR ((d < 35) AND ((56 = e) AND ((c + 40) = 58))))
) T1
union all
select d
from (
Select d
from p3
where ((1 + (26 - (a + (a - (d * e))))) = 21)
) T2
) T2(b_r)
on ((65 > e_r_l) OR (e_r_l > b_r))
) T2(d_l_l_r, e_r_l_r, b_r_r)
on ((45 = e_r_l_r) OR (b_l > 15))
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
Select e_l_l, a_r
from (
Select e_l, c_l, b_r
from (
Select e, c
from p2
where ((28 = c) AND (((((79 - 63) * (47 + 3)) + b) = a) AND (6 > d)))
) T1(e_l, c_l)
inner join (
Select a, b
from p2
where (80 > d)
) T2(a_r, b_r)
on (85 > e_l)
) T1(e_l_l, c_l_l, b_r_l)
full join (
Select c, a, d
from p4
where (d < (e * 1))
) T2(c_r, a_r, d_r)
on (a_r = (((33 + (7 - e_l_l)) * (51 - 50)) - e_l_l))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, b_r_r
from (
Select e, d
from p2
where ((16 < (0 + c)) AND ((c - 40) = 79))
) T1(e_l, d_l)
left join (
Select c_l, e_r, b_r
from (
Select c
from p2
where ((a > 10) OR (a = (d - e)))
) T1(c_l)
left join (
Select e, b
from p3
where ((c = 48) OR (77 > c))
) T2(e_r, b_r)
on ((((c_l + 3) * e_r) = b_r) AND (10 = b_r))
) T2(c_l_r, e_r_r, b_r_r)
on ((32 * 81) = 68)
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
Select c_l, c_r, b_r
from (
select c
from (
Select c
from p3
where ((b = 76) OR ((a < a) AND ((a < e) AND (19 = 38))))
) T1
union all
select e
from (
Select e
from p4
where (b = (45 - b))
) T2
) T1(c_l)
inner join (
Select c, b
from p4
where ((b + (13 * (77 + (d * (((e - ((62 + 18) - 62)) * (88 - 30)) + d))))) > 2)
) T2(c_r, b_r)
on (2 < (c_l + (61 * b_r)))
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
Select c_l, a_l, d_l, d_r
from (
Select c, a, d
from p4
where ((d + e) < d)
) T1(c_l, a_l, d_l)
left join (
Select d
from p5
where (b = e)
) T2(d_r)
on ((41 > a_l) AND ((a_l = (5 - 67)) AND ((((67 + (91 - 95)) * ((a_l * (d_r + c_l)) - 33)) + d_l) = (3 - d_l))))
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
Select a_l, a_r_r, e_r_r
from (
select a
from (
select a, b
from (
Select a, b
from p1
where (6 < 75)
) T1
union all
select d_l_l, b_l_r_r
from (
Select d_l_l, b_l_r_r, e_l_r
from (
select d_l
from (
select d_l, e_r
from (
Select d_l, e_r
from (
Select d
from p4
where (13 = d)
) T1(d_l)
left join (
Select e
from p1
where (4 > (d + c))
) T2(e_r)
on (e_r = d_l)
) T1
union all
select c, a
from (
Select c, a, d
from p2
where ((b = (47 - 8)) OR ((c > (c - b)) AND (((43 + e) = (70 + 42)) AND (5 > e))))
) T2
) T1
union all
select c
from (
Select c
from p1
where (95 > a)
) T2
) T1(d_l_l)
left join (
Select e_l, b_l_r
from (
Select e
from p4
where ((c + (e + a)) > b)
) T1(e_l)
left join (
Select c_l, a_l, b_l, b_r
from (
Select c, a, b
from p1
where (e < e)
) T1(c_l, a_l, b_l)
left join (
Select b
from p4
where (b = b)
) T2(b_r)
on (c_l < (((21 * 78) + (c_l * (49 - (86 + 79)))) - b_l))
) T2(c_l_r, a_l_r, b_l_r, b_r_r)
on (b_l_r = 64)
) T2(e_l_r, b_l_r_r)
on ((b_l_r_r > d_l_l) OR (e_l_r = b_l_r_r))
) T2
) T1
union all
select d
from (
Select d
from p5
where (c > e)
) T2
) T1(a_l)
full join (
Select a_l, d_l, e_r, a_r
from (
Select c, a, d
from p5
where ((9 = d) OR ((c > ((19 + a) * ((e * 66) + c))) AND ((d > 31) OR (((c * 55) > e) AND ((a = b) AND (c > (e - 32)))))))
) T1(c_l, a_l, d_l)
full join (
select e, c, a
from (
Select e, c, a
from p4
where (74 = 2)
) T1
union all
select e, a, d
from (
Select e, a, d
from p3
where (68 < 64)
) T2
) T2(e_r, c_r, a_r)
on (3 = (e_r * 99))
) T2(a_l_r, d_l_r, e_r_r, a_r_r)
on (42 = a_r_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_l_r
from (
Select e
from p2
where (33 = ((d - ((c * (d * e)) - c)) - 36))
) T1(e_l)
inner join (
Select c_l, b_l, b_r, d_r
from (
Select c, b
from p2
where (d = (c + ((e - 37) - ((a + (c + b)) * ((9 - (d + (e * e))) + a)))))
) T1(c_l, b_l)
left join (
Select c, b, d
from p2
where (e = d)
) T2(c_r, b_r, d_r)
on (22 = 2)
) T2(c_l_r, b_l_r, b_r_r, d_r_r)
on (55 > 22)
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
Select c_l, d_l, a_r
from (
Select c, a, d
from p2
where ((a = 46) AND (d = (29 + e)))
) T1(c_l, a_l, d_l)
left join (
Select a
from p3
where (d = (((d - b) + 43) + 75))
) T2(a_r)
on (d_l > ((90 - c_l) - a_r))
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
Select e_r_l, a_r
from (
Select c_l, b_l, e_r, d_r
from (
Select c, b
from p1
where ((58 * e) > c)
) T1(c_l, b_l)
left join (
select e, d
from (
Select e, d
from p4
where (a < 38)
) T1
union all
select c_l, b_r
from (
select c_l, b_r
from (
select c_l, b_r, d_r
from (
Select c_l, b_r, d_r
from (
Select c
from p2
where ((e * 85) > 91)
) T1(c_l)
left join (
Select b, d
from p3
where (e = d)
) T2(b_r, d_r)
on (c_l = 92)
) T1
union all
select e, a, b
from (
Select e, a, b
from p2
where (27 = a)
) T2
) T1
union all
select e, b
from (
select e, b
from (
Select e, b, d
from p4
where ((61 < 58) AND ((e = 69) AND ((99 > 7) AND (d < c))))
) T1
union all
select b_l, b_r
from (
Select b_l, b_r
from (
Select b
from p4
where (75 = 86)
) T1(b_l)
full join (
Select b
from p3
where (e = 36)
) T2(b_r)
on ((((b_r + 90) * b_r) = b_r) OR (16 < 25))
) T2
) T2
) T2
) T2(e_r, d_r)
on (91 = 24)
) T1(c_l_l, b_l_l, e_r_l, d_r_l)
left join (
Select c, a
from p2
where (((5 * 35) < b) OR (21 = 21))
) T2(c_r, a_r)
on ((e_r_l = 53) AND (59 > 38))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l_r_l_r_l, a_r
from (
Select b_l, d_l, b_r_r, d_l_r_l_r
from (
Select c, b, d
from p3
where (94 > 79)
) T1(c_l, b_l, d_l)
inner join (
Select e_l_l, d_l_r_l, e_r, b_r, d_r
from (
Select e_l, d_l_r
from (
Select e
from p2
where (b < 82)
) T1(e_l)
left join (
select d_l
from (
Select d_l, d_l_r
from (
Select b, d
from p3
where (1 > 79)
) T1(b_l, d_l)
full join (
Select a_l, d_l, c_l_r, d_l_r, e_r_r
from (
Select e, c, a, d
from p1
where (86 = b)
) T1(e_l, c_l, a_l, d_l)
left join (
Select c_l, d_l, e_r
from (
select c, d
from (
Select c, d
from p5
where ((a = c) OR (94 = (81 * 80)))
) T1
union all
select c, a
from (
Select c, a, b, d
from p2
where ((1 * e) < d)
) T2
) T1(c_l, d_l)
left join (
Select e, a, d
from p2
where (((80 + (a * (6 - 14))) = a) OR (e > b))
) T2(e_r, a_r, d_r)
on (c_l < d_l)
) T2(c_l_r, d_l_r, e_r_r)
on (a_l < 18)
) T2(a_l_r, d_l_r, c_l_r_r, d_l_r_r, e_r_r_r)
on (((d_l_r - (90 - 76)) > 87) AND (((d_l_r - d_l_r) > 11) OR ((d_l_r > d_l) OR (d_l > d_l_r))))
) T1
union all
select e_l
from (
select e_l
from (
select e_l
from (
Select e_l, b_r, d_r
from (
Select e
from p5
where (14 > e)
) T1(e_l)
left join (
Select b, d
from p2
where ((5 = (6 - (34 - d))) OR ((b < 79) OR (31 = a)))
) T2(b_r, d_r)
on (e_l = d_r)
) T1
union all
select a
from (
Select a
from p4
where (16 < e)
) T2
) T1
union all
select e_r_l
from (
select e_r_l
from (
Select e_r_l, e_r, d_r
from (
Select b_l, d_l, e_r
from (
Select b, d
from p2
where (a > (47 * c))
) T1(b_l, d_l)
inner join (
Select e, b
from p4
where ((e > c) OR ((d < 30) OR ((d < a) OR (83 > 95))))
) T2(e_r, b_r)
on (((47 * 12) < d_l) AND ((((39 * e_r) + 6) - 37) > 68))
) T1(b_l_l, d_l_l, e_r_l)
left join (
Select e, c, d
from p3
where (e = 36)
) T2(e_r, c_r, d_r)
on (89 > 70)
) T1
union all
select d
from (
Select d
from p5
where (c = 52)
) T2
) T2
) T2
) T2(d_l_r)
on ((91 - 22) = 2)
) T1(e_l_l, d_l_r_l)
left join (
Select e, b, d
from p2
where ((23 > 71) AND (78 < e))
) T2(e_r, b_r, d_r)
on (37 > d_r)
) T2(e_l_l_r, d_l_r_l_r, e_r_r, b_r_r, d_r_r)
on ((17 = 68) AND ((b_r_r < b_l) OR ((41 = d_l_r_l_r) AND (b_l > 4))))
) T1(b_l_l, d_l_l, b_r_r_l, d_l_r_l_r_l)
left join (
Select e, c, a, d
from p3
where ((a = a) OR (b = 24))
) T2(e_r, c_r, a_r, d_r)
on (a_r < d_l_r_l_r_l)
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
Select e_l, b_l, a_r
from (
Select e, b
from p2
where (a = b)
) T1(e_l, b_l)
left join (
Select a
from p1
where ((30 = ((d - 52) + 36)) AND (e = d))
) T2(a_r)
on ((75 - a_r) > 64)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l_l_l, d_r_r
from (
Select d_l_l, e_l_r_r
from (
Select e_l, d_l, c_r
from (
Select e, a, d
from p4
where ((56 - 32) < (a * e))
) T1(e_l, a_l, d_l)
left join (
select c
from (
Select c
from p3
where ((e = c) OR (d = c))
) T1
union all
select b_l
from (
Select b_l, c_l_r_r, d_l_r
from (
Select e, b
from p5
where ((0 > (d * d)) OR (((d * 50) = 23) OR ((b > 73) OR (b = ((35 - a) * 98)))))
) T1(e_l, b_l)
inner join (
Select d_l, c_l_r
from (
Select d
from p3
where (a = c)
) T1(d_l)
left join (
select c_l
from (
Select c_l, b_l, e_r
from (
Select c, b
from p3
where (56 = 34)
) T1(c_l, b_l)
left join (
Select e, d
from p5
where (85 < 6)
) T2(e_r, d_r)
on (98 > 56)
) T1
union all
select e
from (
Select e
from p3
where ((59 - 31) = d)
) T2
) T2(c_l_r)
on (71 = 54)
) T2(d_l_r, c_l_r_r)
on (c_l_r_r = (11 - 54))
) T2
) T2(c_r)
on ((c_r + e_l) > d_l)
) T1(e_l_l, d_l_l, c_r_l)
left join (
Select e_l, d_l, e_l_r, a_r_r, c_r_r
from (
Select e, c, b, d
from p5
where (97 = d)
) T1(e_l, c_l, b_l, d_l)
left join (
select e_l, c_r, a_r
from (
Select e_l, c_r, a_r
from (
Select e, b
from p3
where (b > 82)
) T1(e_l, b_l)
left join (
Select c, a
from p1
where (c < b)
) T2(c_r, a_r)
on ((e_l = a_r) AND (87 < 9))
) T1
union all
select a, b, d
from (
Select a, b, d
from p5
where (50 = 4)
) T2
) T2(e_l_r, c_r_r, a_r_r)
on (c_r_r > 51)
) T2(e_l_r, d_l_r, e_l_r_r, a_r_r_r, c_r_r_r)
on ((48 - e_l_r_r) = e_l_r_r)
) T1(d_l_l_l, e_l_r_r_l)
left join (
Select d_r_r_l_r_l, d_l_l, e_r, d_r
from (
Select d_l, d_r_r_l_r
from (
Select d
from p3
where (e < 60)
) T1(d_l)
inner join (
Select e_l_l_l_l, d_r_r_l, c_l_r, e_l_r
from (
select e_l_l_l, d_r_r
from (
Select e_l_l_l, d_r_r
from (
Select e_l_l, c_r
from (
Select e_l, b_r
from (
Select e, c
from p1
where ((7 < 6) OR (30 > 1))
) T1(e_l, c_l)
inner join (
Select b
from p5
where ((c > (76 - 16)) OR (14 < c))
) T2(b_r)
on (45 > b_r)
) T1(e_l_l, b_r_l)
inner join (
select c, d
from (
Select c, d
from p5
where (e > 28)
) T1
union all
select c, a
from (
select c, a
from (
Select c, a
from p4
where ((c = 63) OR (75 = 55))
) T1
union all
select c, a
from (
Select c, a
from p1
where (b = (41 + b))
) T2
) T2
) T2(c_r, d_r)
on (c_r = c_r)
) T1(e_l_l_l, c_r_l)
full join (
Select b_l, d_r
from (
Select b
from p1
where (c > 80)
) T1(b_l)
full join (
Select d
from p2
where ((99 - 11) < (98 + d))
) T2(d_r)
on (33 < d_r)
) T2(b_l_r, d_r_r)
on ((50 = 79) OR (1 < (31 - e_l_l_l)))
) T1
union all
select c, a
from (
Select c, a
from p4
where (92 = 0)
) T2
) T1(e_l_l_l_l, d_r_r_l)
full join (
Select e_l, c_l, a_l, a_r
from (
Select e, c, a
from p1
where ((40 = ((c - 24) + c)) OR (d < d))
) T1(e_l, c_l, a_l)
inner join (
Select a
from p5
where ((c < (99 * b)) AND (d = c))
) T2(a_r)
on (45 > (e_l + e_l))
) T2(e_l_r, c_l_r, a_l_r, a_r_r)
on (10 < (42 + 45))
) T2(e_l_l_l_l_r, d_r_r_l_r, c_l_r_r, e_l_r_r)
on (d_r_r_l_r = d_r_r_l_r)
) T1(d_l_l, d_r_r_l_r_l)
full join (
select e, b, d
from (
Select e, b, d
from p2
where (b > 63)
) T1
union all
select c, a, d
from (
Select c, a, d
from p1
where (c > a)
) T2
) T2(e_r, b_r, d_r)
on (5 > 37)
) T2(d_r_r_l_r_l_r, d_l_l_r, e_r_r, d_r_r)
on ((35 > (2 + 74)) OR (d_r_r > d_r_r))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l, d_l, b_r
from (
Select c, b, d
from p3
where ((56 < a) OR ((78 < a) OR (19 = 43)))
) T1(c_l, b_l, d_l)
left join (
Select b
from p1
where ((e = a) OR (((85 * 59) = 91) OR ((97 = 12) AND ((94 = c) OR ((66 < a) AND (d = b))))))
) T2(b_r)
on ((b_l = 43) AND ((b_r < 33) AND ((74 < 52) OR (b_r = 33))))
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
Select e_l, c_r, a_r
from (
Select e
from p1
where ((23 < 87) AND ((58 - 30) = e))
) T1(e_l)
inner join (
Select c, a, b
from p4
where (a = (85 + 22))
) T2(c_r, a_r, b_r)
on (82 > 7)
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
Select c, a
from p3
where (d = a)
) T1(c_l, a_l)
left join (
Select e, a, b
from p3
where ((90 + b) < ((c * b) * d))
) T2(e_r, a_r, b_r)
on ((c_l + a_r) = 50)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, e_r
from (
Select d
from p5
where (e = d)
) T1(d_l)
full join (
Select e, c, a
from p4
where ((0 > a) AND (((a * (a - d)) = 51) OR ((21 - a) < 36)))
) T2(e_r, c_r, a_r)
on (20 > (d_l - (d_l - 23)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, a_l_l_l_r
from (
select d
from (
Select d
from p4
where ((d < 34) AND (19 < b))
) T1
union all
select c_l
from (
Select c_l, a_r
from (
Select c, b, d
from p2
where ((10 < 99) OR ((25 > b) OR ((d = 57) OR (e < 95))))
) T1(c_l, b_l, d_l)
inner join (
Select a, b
from p5
where (66 = e)
) T2(a_r, b_r)
on (c_l = (9 * a_r))
) T2
) T1(d_l)
full join (
select b_r_l_r_l, a_l_l_l, e_r
from (
Select b_r_l_r_l, a_l_l_l, e_r, a_r
from (
Select a_l_l, e_r_l, b_r_l_r
from (
Select a_l, e_r
from (
Select a
from p2
where (6 < b)
) T1(a_l)
left join (
Select e, a, d
from p4
where ((d = ((e * (30 - 62)) - 33)) AND ((e = 36) AND ((c = 75) OR ((d = 37) OR (61 < e)))))
) T2(e_r, a_r, d_r)
on ((78 < (32 - 59)) AND (66 > a_l))
) T1(a_l_l, e_r_l)
inner join (
Select b_r_l, a_r_l, a_r
from (
Select e_l, d_l, e_r, a_r, b_r
from (
Select e, b, d
from p5
where (d = c)
) T1(e_l, b_l, d_l)
full join (
Select e, a, b
from p1
where (16 = (b + 0))
) T2(e_r, a_r, b_r)
on (62 < a_r)
) T1(e_l_l, d_l_l, e_r_l, a_r_l, b_r_l)
inner join (
Select a
from p4
where ((65 = e) OR (((((25 - 45) * 62) - (55 - d)) = d) AND (e > (16 * a))))
) T2(a_r)
on ((62 < 29) AND (b_r_l > 90))
) T2(b_r_l_r, a_r_l_r, a_r_r)
on (83 = e_r_l)
) T1(a_l_l_l, e_r_l_l, b_r_l_r_l)
left join (
Select e, a
from p3
where ((77 > 58) OR ((46 - 9) = d))
) T2(e_r, a_r)
on ((a_l_l_l + 75) < 85)
) T1
union all
select a, b, d
from (
Select a, b, d
from p3
where (d = b)
) T2
) T2(b_r_l_r_l_r, a_l_l_l_r, e_r_r)
on (12 < (38 - 18))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, b_r
from (
Select e, b, d
from p2
where (25 = 88)
) T1(e_l, b_l, d_l)
left join (
Select b
from p2
where (d > 73)
) T2(b_r)
on ((99 + b_l) = 52)
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
    #******************
    _testmgr.testcase_end(desc)

