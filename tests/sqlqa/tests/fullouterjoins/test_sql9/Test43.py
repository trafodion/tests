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
    
def test001(desc="""Joins Set 43"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, d_r
from (
Select c, a, d
from p1
where ((6 = 10) OR (d > 32))
) T1(c_l, a_l, d_l)
inner join (
Select a, d
from p3
where (b = 68)
) T2(a_r, d_r)
on ((12 - c_l) = (30 - 55))
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
Select b_r_l, b_r_r
from (
Select a_l, b_l, b_r
from (
Select a, b
from p3
where (11 > (e * ((e * 4) + d)))
) T1(a_l, b_l)
inner join (
Select b
from p2
where ((33 < d) OR ((c * 50) > d))
) T2(b_r)
on ((((((79 - b_l) * (b_l * (71 * 35))) * 80) - 9) * 44) = a_l)
) T1(a_l_l, b_l_l, b_r_l)
left join (
select d_l, c_r, b_r
from (
Select d_l, c_r, b_r
from (
Select c, d
from p4
where (((51 + b) = 69) AND (91 < 62))
) T1(c_l, d_l)
full join (
Select e, c, b
from p1
where (86 > 2)
) T2(e_r, c_r, b_r)
on ((44 + c_r) < d_l)
) T1
union all
select a_l, e_r_r, d_l_r
from (
Select a_l, e_r_r, d_l_r
from (
Select a
from p1
where ((a + 51) < (11 - 13))
) T1(a_l)
full join (
Select d_l, e_r
from (
Select c, b, d
from p3
where (c > b)
) T1(c_l, b_l, d_l)
left join (
Select e, b
from p3
where (37 < 7)
) T2(e_r, b_r)
on ((36 > 51) OR ((95 * e_r) > e_r))
) T2(d_l_r, e_r_r)
on (67 > 6)
) T2
) T2(d_l_r, c_r_r, b_r_r)
on (b_r_l = b_r_r)
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
Select e_l, c_l, c_r
from (
Select e, c, d
from p1
where (e > (d - (12 + (b - 51))))
) T1(e_l, c_l, d_l)
left join (
Select c
from p4
where (51 > (e + 20))
) T2(c_r)
on ((c_l + (15 * 53)) = c_l)
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
Select e_l, b_l, d_l_r_r_r, d_r_l_l_r_r, b_l_r
from (
Select e, a, b
from p2
where (d = a)
) T1(e_l, a_l, b_l)
left join (
Select b_l, d_r_l_l_r, d_l_r_r
from (
Select a, b, d
from p5
where (b < a)
) T1(a_l, b_l, d_l)
full join (
Select d_r_l_l, d_l_r
from (
select d_r_l
from (
Select d_r_l, d_l_l, a_l_l_r
from (
Select d_l, d_r
from (
Select d
from p2
where ((96 = 11) AND ((c = 76) OR (16 > 93)))
) T1(d_l)
full join (
Select b, d
from p3
where ((32 * (b * d)) = (c * 7))
) T2(b_r, d_r)
on (72 = 52)
) T1(d_l_l, d_r_l)
inner join (
Select a_l_l, e_r_r, b_l_r
from (
Select e_l, a_l, d_l, a_r
from (
Select e, c, a, d
from p2
where ((89 > ((d - 38) * d)) AND ((c = a) AND (b < (30 - e))))
) T1(e_l, c_l, a_l, d_l)
left join (
Select a
from p2
where (a > c)
) T2(a_r)
on (26 = 56)
) T1(e_l_l, a_l_l, d_l_l, a_r_l)
left join (
Select b_l, e_r
from (
Select c, a, b
from p1
where (d = (28 * (20 - 8)))
) T1(c_l, a_l, b_l)
full join (
select e
from (
Select e
from p1
where (a > 80)
) T1
union all
select a_l
from (
Select a_l, d_l, b_r_r, b_l_r
from (
Select a, d
from p5
where ((((e - a) + (d * (63 + e))) + c) = d)
) T1(a_l, d_l)
left join (
Select b_l, b_r
from (
Select b
from p1
where ((a > 68) OR (55 > e))
) T1(b_l)
inner join (
select a, b
from (
Select a, b
from p3
where (62 < (a - b))
) T1
union all
select a, b
from (
Select a, b
from p3
where (3 > c)
) T2
) T2(a_r, b_r)
on (((75 - (b_r * b_l)) = b_l) AND (b_l = b_l))
) T2(b_l_r, b_r_r)
on ((74 = b_l_r) AND (a_l = 19))
) T2
) T2(e_r)
on (e_r < b_l)
) T2(b_l_r, e_r_r)
on ((17 = e_r_r) OR ((10 = b_l_r) AND ((46 < ((58 * b_l_r) + b_l_r)) OR ((33 > b_l_r) OR (97 = a_l_l)))))
) T2(a_l_l_r, e_r_r_r, b_l_r_r)
on ((0 < 5) AND (1 = (17 * 70)))
) T1
union all
select a
from (
select a
from (
Select a, d
from p1
where ((b > 96) OR (d < b))
) T1
union all
select e
from (
Select e
from p5
where ((71 - 18) = a)
) T2
) T2
) T1(d_r_l_l)
inner join (
Select d_l, e_r, b_r, d_r
from (
Select d
from p3
where (d = b)
) T1(d_l)
inner join (
Select e, b, d
from p5
where (((52 - (e + 72)) = e) AND (39 = 82))
) T2(e_r, b_r, d_r)
on (b_r = (5 - 69))
) T2(d_l_r, e_r_r, b_r_r, d_r_r)
on ((78 * 40) = 52)
) T2(d_r_l_l_r, d_l_r_r)
on (((b_l * (b_l + d_r_l_l_r)) * b_l) > 90)
) T2(b_l_r, d_r_l_l_r_r, d_l_r_r_r)
on (73 > 36)
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test43exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, e_l_r
from (
select e, c
from (
select e, c
from (
Select e, c
from p1
where (b = 1)
) T1
union all
select c, d
from (
Select c, d
from p4
where (66 < (15 - (4 * ((d - 32) * c))))
) T2
) T1
union all
select a_l, c_r
from (
Select a_l, c_r, b_r
from (
Select a, b
from p5
where ((a = e) OR ((b = 56) OR ((b + 44) = 49)))
) T1(a_l, b_l)
left join (
Select e, c, b, d
from p2
where ((e < 76) OR (d > 94))
) T2(e_r, c_r, b_r, d_r)
on ((50 > 90) AND (96 = a_l))
) T2
) T1(e_l, c_l)
full join (
select e_l, e_r, c_r
from (
Select e_l, e_r, c_r, b_r, d_r
from (
Select e
from p1
where (((82 + c) = 46) AND ((b > 62) AND ((d > (e + 20)) OR ((e > a) AND (46 > 18)))))
) T1(e_l)
left join (
Select e, c, b, d
from p1
where (c > (16 * c))
) T2(e_r, c_r, b_r, d_r)
on ((26 < b_r) AND ((e_l = 82) AND (b_r = b_r)))
) T1
union all
select a_l_l, e_r, a_r
from (
Select a_l_l, e_r, a_r
from (
Select a_l, b_r
from (
select e, a
from (
Select e, a, b
from p2
where (79 < b)
) T1
union all
select a_l, d_r
from (
Select a_l, d_r
from (
select c, a
from (
Select c, a, d
from p1
where (20 = 16)
) T1
union all
select a, d
from (
Select a, d
from p5
where (56 = b)
) T2
) T1(c_l, a_l)
inner join (
Select a, d
from p3
where (88 > 13)
) T2(a_r, d_r)
on (d_r > a_l)
) T2
) T1(e_l, a_l)
left join (
Select c, b
from p3
where ((b * e) < 68)
) T2(c_r, b_r)
on ((b_r < b_r) AND (((a_l + b_r) = a_l) AND ((a_l + 3) < 53)))
) T1(a_l_l, b_r_l)
inner join (
Select e, a
from p3
where ((4 < 80) AND (90 = 37))
) T2(e_r, a_r)
on (56 < (51 - (a_r + 72)))
) T2
) T2(e_l_r, e_r_r, c_r_r)
on (((((18 - 85) + 95) * 93) = 53) OR ((8 = 17) OR ((51 > (e_l * 34)) OR (e_l = 25))))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test43exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l_r_l, b_l_l, e_r, b_r
from (
select b_l, e_l_r
from (
Select b_l, e_l_r, d_l_r_r
from (
Select b
from p3
where ((a = b) AND ((38 + b) < d))
) T1(b_l)
full join (
Select e_l, d_l_r
from (
Select e, b
from p1
where (c = (24 * (e - 17)))
) T1(e_l, b_l)
full join (
Select d_l, a_l_r, a_r_r
from (
Select d
from p3
where (15 > (e - 53))
) T1(d_l)
full join (
select a_l, a_r
from (
Select a_l, a_r
from (
Select a
from p5
where ((b > 3) OR (51 < (a - 46)))
) T1(a_l)
full join (
Select a, d
from p1
where ((a - a) > d)
) T2(a_r, d_r)
on (((28 * a_r) < a_r) AND (10 = a_l))
) T1
union all
select c_l_r_l, b_l_r
from (
Select c_l_r_l, b_l_r
from (
Select a_l, a_l_r, c_l_r
from (
Select a
from p4
where (d < b)
) T1(a_l)
full join (
Select c_l, a_l, a_r
from (
Select c, a
from p2
where (((b - 63) = e) OR ((79 = 70) OR ((20 + ((e - 94) - (37 + 22))) = 8)))
) T1(c_l, a_l)
left join (
Select c, a
from p2
where ((c > 42) OR ((a > d) OR ((22 * 31) > (87 * c))))
) T2(c_r, a_r)
on ((((a_r + (a_l * 66)) + c_l) = 43) AND (23 > 65))
) T2(c_l_r, a_l_r, a_r_r)
on ((41 < c_l_r) AND (a_l_r < a_l_r))
) T1(a_l_l, a_l_r_l, c_l_r_l)
left join (
select b_l
from (
Select b_l, a_r
from (
Select b
from p1
where (((47 + c) - 93) = (d - (49 * 77)))
) T1(b_l)
inner join (
Select a
from p2
where ((a = 11) AND (c = (c - 72)))
) T2(a_r)
on (1 < a_r)
) T1
union all
select c_l
from (
select c_l
from (
Select c_l, d_r
from (
Select e, c, b
from p5
where ((20 = 54) OR (46 = a))
) T1(e_l, c_l, b_l)
left join (
Select e, d
from p2
where (b > 54)
) T2(e_r, d_r)
on ((d_r = c_l) OR (d_r > (70 - c_l)))
) T1
union all
select a
from (
Select a
from p1
where ((b = 23) AND ((b < 0) AND (76 = c)))
) T2
) T2
) T2(b_l_r)
on (91 = 14)
) T2
) T2(a_l_r, a_r_r)
on ((8 * d_l) = 32)
) T2(d_l_r, a_l_r_r, a_r_r_r)
on (e_l < 18)
) T2(e_l_r, d_l_r_r)
on ((87 - 26) = e_l_r)
) T1
union all
select e_l_l, e_r
from (
Select e_l_l, e_r
from (
select e_l, e_r
from (
Select e_l, e_r
from (
Select e, a
from p5
where (a = a)
) T1(e_l, a_l)
left join (
Select e
from p1
where ((c = d) AND (a = 15))
) T2(e_r)
on (95 = 16)
) T1
union all
select c, b
from (
Select c, b
from p5
where (c < 41)
) T2
) T1(e_l_l, e_r_l)
full join (
Select e
from p5
where (6 = c)
) T2(e_r)
on ((e_r < e_l_l) OR ((20 < e_r) AND ((e_r < e_r) AND (85 > 21))))
) T2
) T1(b_l_l, e_l_r_l)
inner join (
Select e, c, b
from p4
where (((c + a) * (32 - c)) = e)
) T2(e_r, c_r, b_r)
on (99 = (b_l_l - b_l_l))
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
Select a_l_l, e_r
from (
Select a_l, b_l, a_r
from (
Select e, a, b
from p3
where (a = a)
) T1(e_l, a_l, b_l)
left join (
Select a
from p1
where (a = e)
) T2(a_r)
on ((a_l > 5) OR ((a_r = b_l) AND ((25 + 0) = a_l)))
) T1(a_l_l, b_l_l, a_r_l)
full join (
Select e
from p3
where ((c < (86 * a)) AND ((61 = d) OR (68 = (b * a))))
) T2(e_r)
on ((6 = 42) OR ((36 > e_r) AND ((76 + 33) > a_l_l)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test43exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_l, c_r_r
from (
Select e, a, d
from p3
where (c = 54)
) T1(e_l, a_l, d_l)
left join (
Select a_r_l, d_l_l, c_r, d_r
from (
Select c_l, d_l, a_r, d_r
from (
Select c, d
from p2
where (93 > 32)
) T1(c_l, d_l)
left join (
select a, d
from (
select a, d
from (
Select a, d
from p2
where (d > 81)
) T1
union all
select e, b
from (
Select e, b
from p4
where (b = 41)
) T2
) T1
union all
select b_r_l, d_r
from (
Select b_r_l, d_r
from (
select a_l, d_l, b_r
from (
Select a_l, d_l, b_r
from (
Select a, b, d
from p1
where (77 = a)
) T1(a_l, b_l, d_l)
full join (
Select e, b
from p2
where (89 > (37 + b))
) T2(e_r, b_r)
on (d_l = a_l)
) T1
union all
select e, c, a
from (
Select e, c, a
from p3
where ((c < ((55 * d) + 37)) OR ((75 = a) OR (((b * 54) < ((d + 53) * (a + 4))) AND ((30 = 78) OR ((a = e) OR ((e = c) OR ((c = b) AND (72 > 87))))))))
) T2
) T1(a_l_l, d_l_l, b_r_l)
left join (
Select d
from p3
where ((7 = c) OR ((a = 51) AND ((44 < e) AND ((((e - 20) * e) = ((74 + 35) - 34)) AND (c > (60 - (93 + ((64 - c) + b))))))))
) T2(d_r)
on (39 = 8)
) T2
) T2(a_r, d_r)
on ((d_r < 75) OR (a_r < 75))
) T1(c_l_l, d_l_l, a_r_l, d_r_l)
left join (
Select c, d
from p5
where (29 > e)
) T2(c_r, d_r)
on ((76 = c_r) OR (((36 + 41) < 87) AND (42 < (35 * d_l_l))))
) T2(a_r_l_r, d_l_l_r, c_r_r, d_r_r)
on (52 < (18 * 25))
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
Select c_l, e_r, a_r
from (
Select c
from p4
where (((b - d) < (a * 96)) AND (53 < 18))
) T1(c_l)
left join (
Select e, a
from p3
where (29 < ((b - (67 + 80)) * 6))
) T2(e_r, a_r)
on ((a_r * a_r) > 11)
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
Select e_l, a_l, b_l, b_r_r, d_l_r
from (
Select e, a, b
from p2
where ((a = 81) OR (90 = b))
) T1(e_l, a_l, b_l)
inner join (
Select b_l, d_l, b_r
from (
Select b, d
from p4
where (e > (56 - (70 * (44 + b))))
) T1(b_l, d_l)
full join (
Select e, b
from p4
where (e = (d * 77))
) T2(e_r, b_r)
on (88 > b_l)
) T2(b_l_r, d_l_r, b_r_r)
on ((42 - 63) = b_r_r)
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
Select e_l, e_r, c_r
from (
Select e, c, a
from p4
where (c > 37)
) T1(e_l, c_l, a_l)
left join (
Select e, c, a
from p1
where ((56 * 7) = (0 * a))
) T2(e_r, c_r, a_r)
on (45 > 36)
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
Select a_l, d_l, a_r
from (
Select a, d
from p3
where ((e = ((37 - 62) + a)) OR (a < a))
) T1(a_l, d_l)
inner join (
Select a
from p4
where (((a * e) > 15) AND ((75 < d) AND ((74 = 67) OR (19 = e))))
) T2(a_r)
on ((((95 * (d_l - a_r)) + a_l) < d_l) AND (a_l < ((30 + d_l) - 92)))
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
Select c_l, b_l, c_r
from (
Select c, b
from p2
where (b < b)
) T1(c_l, b_l)
inner join (
Select c
from p2
where (a > 22)
) T2(c_r)
on ((3 + c_r) < b_l)
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
Select d_l, e_r
from (
Select d
from p3
where (a > 49)
) T1(d_l)
inner join (
Select e, d
from p4
where (96 > a)
) T2(e_r, d_r)
on ((e_r < 18) AND ((63 < 78) OR ((e_r > d_l) OR (74 < 56))))
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
Select a_r_r_r_l, c_l_r_l_l, d_r
from (
Select c_l_r_l, a_r_r_r
from (
Select d_l, c_l_r, b_r_r
from (
Select a, b, d
from p1
where ((c > e) AND (90 > b))
) T1(a_l, b_l, d_l)
inner join (
Select c_l, b_r
from (
select c
from (
Select c, b
from p3
where (85 > 27)
) T1
union all
select e
from (
select e
from (
Select e
from p5
where ((b + b) = a)
) T1
union all
select e
from (
Select e, a
from p3
where (21 < e)
) T2
) T2
) T1(c_l)
left join (
Select c, b
from p5
where (29 > c)
) T2(c_r, b_r)
on (36 = b_r)
) T2(c_l_r, b_r_r)
on (d_l < 27)
) T1(d_l_l, c_l_r_l, b_r_r_l)
left join (
Select b_l, a_r_r
from (
Select c, b, d
from p1
where ((76 = 71) OR ((a = (64 + 64)) AND ((14 < b) OR ((28 = a) OR (6 < e)))))
) T1(c_l, b_l, d_l)
full join (
Select c_l_l, c_r_l, a_r, b_r
from (
Select e_l, c_l, c_r
from (
Select e, c, a, d
from p2
where (78 = a)
) T1(e_l, c_l, a_l, d_l)
left join (
Select c
from p2
where ((34 < (45 - 65)) AND (((66 - 36) + 35) = 97))
) T2(c_r)
on (38 > (c_l * 13))
) T1(e_l_l, c_l_l, c_r_l)
left join (
Select a, b
from p5
where (((a - e) < 80) OR (e < a))
) T2(a_r, b_r)
on ((55 < 60) OR (((c_r_l * 15) < a_r) OR (a_r > b_r)))
) T2(c_l_l_r, c_r_l_r, a_r_r, b_r_r)
on ((a_r_r - 51) < 90)
) T2(b_l_r, a_r_r_r)
on (a_r_r_r > 93)
) T1(c_l_r_l_l, a_r_r_r_l)
inner join (
Select d
from p1
where (36 > c)
) T2(d_r)
on ((62 = d_r) OR (48 = (d_r * (41 - ((d_r * a_r_r_r_l) - (c_l_r_l_l * (9 * a_r_r_r_l)))))))
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
Select a_l, b_l, e_r, a_r
from (
Select c, a, b
from p2
where (a = 82)
) T1(c_l, a_l, b_l)
inner join (
Select e, c, a
from p4
where ((b = 23) AND ((98 = d) OR (11 < (86 - e))))
) T2(e_r, c_r, a_r)
on (50 = a_l)
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
Select e_l, e_l_r_r
from (
Select e
from p1
where ((e - c) < 5)
) T1(e_l)
full join (
Select b_l, e_l_r
from (
Select b
from p4
where (c = ((e + 67) * b))
) T1(b_l)
full join (
Select e_l, a_r
from (
Select e
from p1
where (41 < b)
) T1(e_l)
left join (
Select a
from p2
where ((14 = c) AND (a = 47))
) T2(a_r)
on (79 = e_l)
) T2(e_l_r, a_r_r)
on (b_l = (6 * b_l))
) T2(b_l_r, e_l_r_r)
on ((e_l_r_r < e_l) OR (16 > (19 - e_l)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test43exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_l, d_l, b_r
from (
Select e, a, b, d
from p2
where ((e < ((39 + (((c + c) + 49) + c)) * c)) AND (e = 39))
) T1(e_l, a_l, b_l, d_l)
full join (
Select b
from p3
where ((83 - a) = 2)
) T2(b_r)
on (36 > 19)
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
Select c_l, d_r
from (
select c, a, b
from (
Select c, a, b, d
from p4
where (80 = c)
) T1
union all
select e, c, d
from (
select e, c, d
from (
Select e, c, d
from p4
where (((c * a) = 33) AND (73 > 11))
) T1
union all
select e, b, d
from (
Select e, b, d
from p1
where ((30 < 83) AND ((a = 10) AND (a > c)))
) T2
) T2
) T1(c_l, a_l, b_l)
full join (
Select e, d
from p4
where (13 = 34)
) T2(e_r, d_r)
on (c_l < d_r)
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
Select b_l, c_r
from (
Select b
from p5
where (26 = d)
) T1(b_l)
left join (
Select c
from p2
where (((86 * (d * d)) > 93) AND (62 = b))
) T2(c_r)
on (91 = 36)
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
    #****************************
    _testmgr.testcase_end(desc)

