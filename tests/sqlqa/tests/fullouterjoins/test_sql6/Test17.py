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
    
def test001(desc="""Joins Set 17"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_r_l_l, a_l_r_l_r_l, a_r_r_r, b_l_r
from (
select e_r_l, a_l_r_l_r
from (
Select e_r_l, a_l_r_l_r
from (
Select e_l_l, e_r
from (
Select e_l, a_l, a_r
from (
Select e, a
from p3
where (77 = 8)
) T1(e_l, a_l)
full join (
Select a
from p3
where ((38 + d) = c)
) T2(a_r)
on ((a_r > e_l) AND (a_r = (((a_r - 36) * e_l) * 1)))
) T1(e_l_l, a_l_l, a_r_l)
full join (
Select e
from p2
where (95 = d)
) T2(e_r)
on ((56 + 69) < 87)
) T1(e_l_l_l, e_r_l)
left join (
Select a_l_r_l, e_l_l, a_r, d_r
from (
select e_l, a_l_r
from (
Select e_l, a_l_r
from (
Select e, b
from p4
where ((35 < c) OR ((68 * (b * b)) = 23))
) T1(e_l, b_l)
full join (
select c_l, a_l
from (
Select c_l, a_l, e_r
from (
select c, a
from (
Select c, a, b
from p1
where ((((c - 13) + e) - d) < (43 + d))
) T1
union all
select e, c
from (
select e, c
from (
Select e, c, b
from p2
where (58 > b)
) T1
union all
select c, a
from (
Select c, a
from p4
where ((23 = (82 * b)) OR (20 > b))
) T2
) T2
) T1(c_l, a_l)
left join (
Select e, b, d
from p5
where (51 < 66)
) T2(e_r, b_r, d_r)
on ((a_l = e_r) AND (e_r = 17))
) T1
union all
select e, b
from (
Select e, b
from p4
where (48 < 29)
) T2
) T2(c_l_r, a_l_r)
on ((e_l = 45) OR (((a_l_r * 74) * a_l_r) > (7 + a_l_r)))
) T1
union all
select e, a
from (
Select e, a
from p5
where ((23 = 9) OR ((e - e) = 78))
) T2
) T1(e_l_l, a_l_r_l)
left join (
Select a, d
from p3
where (89 < (d + 51))
) T2(a_r, d_r)
on (a_l_r_l = e_l_l)
) T2(a_l_r_l_r, e_l_l_r, a_r_r, d_r_r)
on ((e_r_l * 73) = 28)
) T1
union all
select c, a
from (
select c, a, d
from (
Select c, a, d
from p3
where (59 > (c - b))
) T1
union all
select b_l, c_r, d_r
from (
Select b_l, c_r, d_r
from (
Select c, b
from p4
where (((1 * a) > (d - (e + c))) AND (c > 66))
) T1(c_l, b_l)
inner join (
Select c, a, d
from p5
where (60 = c)
) T2(c_r, a_r, d_r)
on (52 = d_r)
) T2
) T2
) T1(e_r_l_l, a_l_r_l_r_l)
full join (
Select b_l, d_l, a_r_r, a_r_l_r
from (
Select a, b, d
from p5
where (a = ((45 * 42) + 2))
) T1(a_l, b_l, d_l)
inner join (
Select a_r_l, a_r
from (
Select e_l, c_l, c_r, a_r
from (
Select e, c, a, d
from p5
where (a = c)
) T1(e_l, c_l, a_l, d_l)
inner join (
select c, a
from (
Select c, a
from p5
where (60 < 89)
) T1
union all
select e, c
from (
Select e, c, b
from p5
where (((14 + b) = d) OR (e < b))
) T2
) T2(c_r, a_r)
on (c_l = ((c_r - c_r) * 60))
) T1(e_l_l, c_l_l, c_r_l, a_r_l)
inner join (
select a
from (
Select a, d
from p2
where ((c * c) < ((c - 12) - b))
) T1
union all
select a
from (
Select a
from p4
where (a = d)
) T2
) T2(a_r)
on (a_r_l > 61)
) T2(a_r_l_r, a_r_r)
on ((a_r_r < d_l) AND ((32 = 37) OR (a_r_l_r = 22)))
) T2(b_l_r, d_l_r, a_r_r_r, a_r_l_r_r)
on ((23 + 93) > 94)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_l, b_r_l_r, c_l_l_l_r
from (
Select a, d
from p1
where ((a * 18) = b)
) T1(a_l, d_l)
left join (
select c_l_l_l, b_r_l, e_l_l_l
from (
Select c_l_l_l, b_r_l, e_l_l_l, c_r
from (
Select c_l_l, e_l_l, d_r_l, b_r
from (
Select e_l, c_l, e_r, d_r
from (
Select e, c
from p5
where (92 = (b - (c + b)))
) T1(e_l, c_l)
inner join (
Select e, c, d
from p3
where (86 = c)
) T2(e_r, c_r, d_r)
on ((67 - 8) > d_r)
) T1(e_l_l, c_l_l, e_r_l, d_r_l)
left join (
Select b
from p3
where (((b - d) = e) OR ((c - 48) = d))
) T2(b_r)
on (6 > 3)
) T1(c_l_l_l, e_l_l_l, d_r_l_l, b_r_l)
inner join (
Select c, b
from p2
where (a > e)
) T2(c_r, b_r)
on (16 = e_l_l_l)
) T1
union all
select c, a, d
from (
Select c, a, d
from p2
where (11 > d)
) T2
) T2(c_l_l_l_r, b_r_l_r, e_l_l_l_r)
on ((c_l_l_l_r = c_l_l_l_r) OR (d_l = ((46 + a_l) - d_l)))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_r_l, d_r
from (
Select c_l, d_r
from (
Select e, c
from p4
where (60 = d)
) T1(e_l, c_l)
left join (
Select e, c, d
from p3
where (4 = d)
) T2(e_r, c_r, d_r)
on (72 = d_r)
) T1(c_l_l, d_r_l)
left join (
Select d
from p2
where (((12 * 54) = d) OR (e = 24))
) T2(d_r)
on ((65 = (d_r_l - 32)) OR (((d_r * d_r_l) + 54) < 90))
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
Select e_l, d_l, b_r_r, e_r_l_l_r, e_r_r
from (
Select e, d
from p5
where (66 = d)
) T1(e_l, d_l)
inner join (
Select e_r_l_l, e_r, b_r
from (
Select b_l_l, e_r_l, a_r
from (
Select b_l, e_r
from (
Select a, b
from p1
where (24 > (b + b))
) T1(a_l, b_l)
left join (
Select e
from p1
where ((e * d) < 76)
) T2(e_r)
on (((69 + ((e_r * b_l) - (15 * e_r))) < 74) AND (((b_l - e_r) + b_l) = (b_l - e_r)))
) T1(b_l_l, e_r_l)
inner join (
select a
from (
Select a, b
from p3
where (82 = 54)
) T1
union all
select c
from (
Select c
from p3
where ((89 * 8) = b)
) T2
) T2(a_r)
on (b_l_l = (36 - (5 + (35 + 23))))
) T1(b_l_l_l, e_r_l_l, a_r_l)
left join (
Select e, b
from p5
where (57 < 99)
) T2(e_r, b_r)
on ((e_r_l_l = e_r_l_l) OR (2 > (83 + 55)))
) T2(e_r_l_l_r, e_r_r, b_r_r)
on ((d_l > e_l) AND (93 = 42))
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
Select b_l, d_l, e_r, b_r
from (
Select b, d
from p4
where ((82 - (93 * e)) < 42)
) T1(b_l, d_l)
left join (
Select e, a, b
from p2
where (e < c)
) T2(e_r, a_r, b_r)
on (e_r > (24 - 93))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_l, c_r
from (
select a, b
from (
Select a, b
from p5
where ((19 > c) OR (b > 81))
) T1
union all
select a, b
from (
Select a, b
from p3
where (e > a)
) T2
) T1(a_l, b_l)
full join (
Select c
from p1
where ((d * (72 * (60 - (40 + 50)))) = 90)
) T2(c_r)
on ((81 - b_l) < (62 * 76))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, a_r, b_r
from (
Select e, d
from p3
where (36 > (48 - ((31 + 28) - 26)))
) T1(e_l, d_l)
inner join (
Select a, b
from p2
where (47 = 11)
) T2(a_r, b_r)
on (31 < a_r)
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
Select c_l, a_l, c_r
from (
Select e, c, a
from p5
where ((e = (b + 14)) OR ((b < (53 * e)) OR ((78 < 79) AND (a > d))))
) T1(e_l, c_l, a_l)
inner join (
Select e, c
from p3
where (b = 77)
) T2(e_r, c_r)
on ((a_l = c_l) OR (c_l = a_l))
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
Select d_l, a_r
from (
Select d
from p3
where (e < a)
) T1(d_l)
left join (
Select a
from p4
where (67 < 11)
) T2(a_r)
on (d_l > 30)
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
Select e_l, b_l, e_r, d_r
from (
Select e, b
from p1
where ((e > c) AND ((b * b) = 81))
) T1(e_l, b_l)
full join (
Select e, c, d
from p5
where (76 = 80)
) T2(e_r, c_r, d_r)
on (77 < d_r)
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
Select c_l, d_l_r, e_r_r_r
from (
Select e, c
from p5
where (b = a)
) T1(e_l, c_l)
full join (
Select e_l, d_l, e_r_r
from (
Select e, d
from p1
where (c = 93)
) T1(e_l, d_l)
full join (
Select e_l, e_r, c_r
from (
Select e
from p5
where ((85 > 85) OR ((b < c) OR (1 > (e + (77 + (a - d))))))
) T1(e_l)
left join (
Select e, c
from p2
where (((((4 * (b + a)) * 96) - (b + a)) < 78) AND (27 = 85))
) T2(e_r, c_r)
on (((26 + 34) > 68) OR (c_r = (c_r - 19)))
) T2(e_l_r, e_r_r, c_r_r)
on ((e_l > d_l) OR (e_r_r = 43))
) T2(e_l_r, d_l_r, e_r_r_r)
on (((3 + ((c_l - c_l) + (54 - 50))) < d_l_r) AND (22 < 86))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l_l, a_r_l, e_r, b_r
from (
Select e_l, a_r, b_r
from (
Select e, c, a
from p5
where ((63 > 43) OR (50 = 78))
) T1(e_l, c_l, a_l)
left join (
Select e, a, b
from p4
where ((c + (e + 63)) = d)
) T2(e_r, a_r, b_r)
on (b_r < (e_l - a_r))
) T1(e_l_l, a_r_l, b_r_l)
inner join (
Select e, b
from p2
where (((14 + a) > e) AND (67 < 33))
) T2(e_r, b_r)
on (23 < 15)
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
Select c_r_r_l, d_l_l, a_l_r, c_r_r
from (
Select e_l, c_l, d_l, a_l_r, c_r_r
from (
Select e, c, d
from p3
where ((82 = 47) AND ((86 < 38) AND (e < (22 + b))))
) T1(e_l, c_l, d_l)
inner join (
Select a_l, c_r, b_r
from (
Select e, a
from p1
where ((7 > c) AND (49 = 21))
) T1(e_l, a_l)
left join (
Select c, b, d
from p3
where ((89 * (8 + a)) > 80)
) T2(c_r, b_r, d_r)
on ((69 = 10) AND (b_r = (b_r - 71)))
) T2(a_l_r, c_r_r, b_r_r)
on (c_r_r = e_l)
) T1(e_l_l, c_l_l, d_l_l, a_l_r_l, c_r_r_l)
left join (
Select a_l, c_r
from (
Select a
from p1
where (((38 + 18) = 10) OR (b = (e + 77)))
) T1(a_l)
left join (
Select c
from p3
where ((55 < 8) AND ((67 - e) < (((d * 40) * 18) + b)))
) T2(c_r)
on (87 = (a_l * 72))
) T2(a_l_r, c_r_r)
on (c_r_r < 58)
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
Select d_l, c_r, d_r
from (
Select e, d
from p4
where ((a < a) OR (e = 31))
) T1(e_l, d_l)
left join (
Select c, d
from p2
where (a = 47)
) T2(c_r, d_r)
on (((58 * 49) < c_r) OR (c_r = (d_l * d_l)))
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
Select c_l, e_r, c_r
from (
Select c
from p1
where (((34 - c) = (c - 66)) OR ((91 > 46) OR (90 < 34)))
) T1(c_l)
left join (
Select e, c
from p5
where ((a + 20) = a)
) T2(e_r, c_r)
on ((e_r - 90) > c_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_l, b_r_r, c_r_l_r
from (
select a, b
from (
Select a, b
from p3
where (((52 + e) > (92 + a)) AND ((((c - 40) * 36) > 66) AND ((79 = ((80 * (e + 46)) * b)) OR (b > b))))
) T1
union all
select d_r_l, c_r_l
from (
Select d_r_l, c_r_l, e_r
from (
Select d_l, c_r, d_r
from (
select a, b, d
from (
Select a, b, d
from p5
where ((82 = c) AND (78 > (b - 98)))
) T1
union all
select e, c, b
from (
Select e, c, b, d
from p2
where (99 > 50)
) T2
) T1(a_l, b_l, d_l)
inner join (
Select c, d
from p4
where (((25 - c) = a) AND (26 < e))
) T2(c_r, d_r)
on (c_r < (95 * c_r))
) T1(d_l_l, c_r_l, d_r_l)
inner join (
Select e
from p3
where (8 = b)
) T2(e_r)
on ((c_r_l = 25) AND ((e_r > (c_r_l - 40)) AND ((((43 * d_r_l) * e_r) - c_r_l) > (e_r * c_r_l))))
) T2
) T1(a_l, b_l)
left join (
Select c_r_l, c_r, b_r
from (
Select c_l, a_l, b_l, c_r
from (
Select e, c, a, b
from p5
where (b = (32 - d))
) T1(e_l, c_l, a_l, b_l)
left join (
Select c
from p3
where ((84 + 52) > c)
) T2(c_r)
on ((a_l < 43) AND ((b_l < 52) AND (83 > c_r)))
) T1(c_l_l, a_l_l, b_l_l, c_r_l)
inner join (
Select c, b
from p3
where (59 > e)
) T2(c_r, b_r)
on (b_r = (66 * c_r_l))
) T2(c_r_l_r, c_r_r, b_r_r)
on (((b_r_r * (92 - a_l)) - (48 - 74)) > (b_l * c_r_l_r))
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
Select a_r_r_l, b_r_l_l, e_l_r, b_l_r
from (
Select b_r_l, a_r_r
from (
Select c_l, b_r
from (
Select e, c, a
from p3
where (67 > b)
) T1(e_l, c_l, a_l)
inner join (
Select b
from p1
where ((94 = 96) OR (e = 70))
) T2(b_r)
on ((20 < 40) OR (64 = 43))
) T1(c_l_l, b_r_l)
inner join (
Select a_l, a_r
from (
Select a
from p5
where ((63 + c) = c)
) T1(a_l)
inner join (
Select a
from p1
where (89 = (91 * a))
) T2(a_r)
on ((((6 - a_l) + (a_l - 89)) * 64) > 1)
) T2(a_l_r, a_r_r)
on ((13 - 37) < b_r_l)
) T1(b_r_l_l, a_r_r_l)
left join (
Select e_l, c_l, b_l, e_r_l_r, d_r_l_l_l_l_l_l_r_r
from (
Select e, c, a, b
from p1
where (9 > (99 * (c + ((12 - a) * e))))
) T1(e_l, c_l, a_l, b_l)
inner join (
Select a_r_l_l_l, e_r_l, d_r_r, d_r_l_l_l_l_l_l_r, c_l_r_r_l_r
from (
Select a_r_l_l, e_r
from (
Select b_l_l_l, a_r_l, a_l_l_r
from (
Select b_l_l, a_r
from (
select a_l, b_l
from (
Select a_l, b_l, a_r
from (
Select c, a, b
from p3
where ((e * b) < 81)
) T1(c_l, a_l, b_l)
full join (
Select a
from p4
where ((26 < d) AND (a > (43 - b)))
) T2(a_r)
on (a_l = 86)
) T1
union all
select c, a
from (
Select c, a
from p4
where (87 = 20)
) T2
) T1(a_l_l, b_l_l)
left join (
Select c, a, b
from p1
where (25 > 68)
) T2(c_r, a_r, b_r)
on (36 = 70)
) T1(b_l_l_l, a_r_l)
inner join (
select a_l_l
from (
select a_l_l, a_r_l
from (
Select a_l_l, a_r_l, a_l_r
from (
Select a_l, d_l, c_r, a_r
from (
Select c, a, d
from p4
where ((73 - c) > a)
) T1(c_l, a_l, d_l)
left join (
Select c, a
from p3
where ((d < ((e * b) * 32)) AND (12 < 52))
) T2(c_r, a_r)
on ((18 < (d_l * (d_l + (c_r + 61)))) OR (d_l > 82))
) T1(a_l_l, d_l_l, c_r_l, a_r_l)
left join (
Select a_l, d_l, a_r, b_r
from (
Select a, d
from p5
where (e = b)
) T1(a_l, d_l)
left join (
Select a, b
from p2
where (e = a)
) T2(a_r, b_r)
on (b_r = a_l)
) T2(a_l_r, d_l_r, a_r_r, b_r_r)
on (a_l_r > a_l_l)
) T1
union all
select b, d
from (
select b, d
from (
Select b, d
from p3
where (34 = 73)
) T1
union all
select c_l, d_l
from (
Select c_l, d_l, a_r_r
from (
Select c, a, d
from p5
where (e = c)
) T1(c_l, a_l, d_l)
left join (
Select c_l, a_r
from (
Select c
from p2
where (((e * e) = a) OR (c > d))
) T1(c_l)
full join (
Select c, a
from p3
where (0 > 20)
) T2(c_r, a_r)
on ((98 < (c_l - (32 + a_r))) AND (((a_r + 68) * c_l) > 67))
) T2(c_l_r, a_r_r)
on (d_l > 94)
) T2
) T2
) T1
union all
select c
from (
Select c
from p2
where (d < (e - a))
) T2
) T2(a_l_l_r)
on (a_l_l_r < a_r_l)
) T1(b_l_l_l_l, a_r_l_l, a_l_l_r_l)
left join (
Select e
from p4
where ((e > 54) AND (a = 85))
) T2(e_r)
on (a_r_l_l > 57)
) T1(a_r_l_l_l, e_r_l)
left join (
Select d_r_l_l_l_l_l_l, c_l_r_r_l, e_r, d_r
from (
Select d_r_l, d_r_l_l_l_l_l, c_l_r_r
from (
Select d_r_l_l_l_l, d_r
from (
select d_r_l_l_l, e_l_l_r_r
from (
Select d_r_l_l_l, e_l_l_r_r, b_l_r
from (
Select d_r_l_l, d_r
from (
Select d_r_l, b_l_l, e_r
from (
Select b_l, e_r, d_r
from (
Select c, b, d
from p2
where (89 = b)
) T1(c_l, b_l, d_l)
left join (
Select e, a, b, d
from p1
where (e > 97)
) T2(e_r, a_r, b_r, d_r)
on ((e_r * 44) < (b_l + 27))
) T1(b_l_l, e_r_l, d_r_l)
full join (
Select e, b
from p3
where ((49 = d) OR (d = 15))
) T2(e_r, b_r)
on (50 > d_r_l)
) T1(d_r_l_l, b_l_l_l, e_r_l)
left join (
Select d
from p2
where (98 < 70)
) T2(d_r)
on ((15 = (55 * 20)) AND (d_r > (27 * d_r_l_l)))
) T1(d_r_l_l_l, d_r_l)
full join (
Select b_l, c_r_r, e_l_l_r
from (
Select b, d
from p1
where ((10 - c) > b)
) T1(b_l, d_l)
full join (
Select e_l_l, e_r_l, c_r, d_r
from (
Select e_l, e_r
from (
Select e, b, d
from p2
where ((b > 28) AND ((64 > (89 - c)) AND (b < d)))
) T1(e_l, b_l, d_l)
full join (
select e
from (
Select e, b
from p2
where ((95 = (c + (13 * 91))) AND ((e = 15) OR (c = c)))
) T1
union all
select b
from (
Select b
from p4
where ((27 = ((e - 29) + 30)) AND ((b > ((32 - d) + 11)) OR (b < 1)))
) T2
) T2(e_r)
on (1 = 73)
) T1(e_l_l, e_r_l)
inner join (
Select c, d
from p1
where (11 = (77 * (80 + (26 * 83))))
) T2(c_r, d_r)
on (e_l_l > d_r)
) T2(e_l_l_r, e_r_l_r, c_r_r, d_r_r)
on (e_l_l_r > 90)
) T2(b_l_r, c_r_r_r, e_l_l_r_r)
on (53 < 88)
) T1
union all
select b_l, c_r
from (
Select b_l, c_r
from (
Select b
from p4
where ((49 = (c - b)) AND ((59 + e) > 97))
) T1(b_l)
inner join (
Select c
from p3
where (41 = d)
) T2(c_r)
on (c_r < b_l)
) T2
) T1(d_r_l_l_l_l, e_l_l_r_r_l)
full join (
Select d
from p3
where (c > 1)
) T2(d_r)
on ((d_r > d_r_l_l_l_l) AND (((61 - 36) < (2 - d_r)) AND ((d_r_l_l_l_l > 28) OR ((35 = ((d_r_l_l_l_l - ((58 * 63) + d_r_l_l_l_l)) * d_r_l_l_l_l)) AND (d_r_l_l_l_l = (d_r_l_l_l_l - d_r_l_l_l_l))))))
) T1(d_r_l_l_l_l_l, d_r_l)
left join (
select b_l, c_l_r
from (
select b_l, c_l_r
from (
Select b_l, c_l_r
from (
Select b, d
from p2
where ((b > 90) OR (((c + e) - b) = c))
) T1(b_l, d_l)
left join (
select c_l
from (
Select c_l, a_l, b_l, b_r_r
from (
Select c, a, b
from p3
where (c = 24)
) T1(c_l, a_l, b_l)
inner join (
Select d_l, b_r
from (
Select d
from p4
where (7 = c)
) T1(d_l)
full join (
Select b
from p5
where ((d = 8) OR (((35 * c) > 34) AND ((24 * 41) < c)))
) T2(b_r)
on ((11 = b_r) AND ((16 < d_l) AND ((b_r = (29 - b_r)) AND ((34 - b_r) < 75))))
) T2(d_l_r, b_r_r)
on (b_r_r < ((c_l + 38) * 30))
) T1
union all
select d
from (
Select d
from p2
where (91 = (27 * 20))
) T2
) T2(c_l_r)
on (b_l = 4)
) T1
union all
select a_l, a_r
from (
Select a_l, a_r
from (
Select a
from p1
where (((b - (a + a)) < (e * 37)) AND ((40 = a) AND (e = ((d + d) * 17))))
) T1(a_l)
left join (
Select a, d
from p1
where ((58 * c) > e)
) T2(a_r, d_r)
on (a_r < (a_l * 27))
) T2
) T1
union all
select e, d
from (
Select e, d
from p2
where (73 < b)
) T2
) T2(b_l_r, c_l_r_r)
on ((15 - d_r_l) < 39)
) T1(d_r_l_l, d_r_l_l_l_l_l_l, c_l_r_r_l)
full join (
Select e, a, d
from p3
where ((e + (99 * a)) = 41)
) T2(e_r, a_r, d_r)
on (c_l_r_r_l = ((5 - c_l_r_r_l) - e_r))
) T2(d_r_l_l_l_l_l_l_r, c_l_r_r_l_r, e_r_r, d_r_r)
on ((46 < e_r_l) OR ((78 = (98 + 11)) OR ((e_r_l > a_r_l_l_l) AND (44 = c_l_r_r_l_r))))
) T2(a_r_l_l_l_r, e_r_l_r, d_r_r_r, d_r_l_l_l_l_l_l_r_r, c_l_r_r_l_r_r)
on (97 > e_r_l_r)
) T2(e_l_r, c_l_r, b_l_r, e_r_l_r_r, d_r_l_l_l_l_l_l_r_r_r)
on ((b_r_l_l > (73 * b_r_l_l)) OR ((84 = e_l_r) OR ((b_r_l_l = (83 + 10)) AND (75 > (a_r_r_l + 32)))))
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
Select d_l_l, b_r_r, c_l_r
from (
Select b_l, d_l, d_r
from (
Select e, b, d
from p4
where (d = (b - ((79 * 46) + 83)))
) T1(e_l, b_l, d_l)
left join (
Select b, d
from p5
where (((a * a) > 30) AND (93 = (b - c)))
) T2(b_r, d_r)
on ((36 + (33 + 48)) > b_l)
) T1(b_l_l, d_l_l, d_r_l)
left join (
Select c_l, b_r, d_r
from (
Select c, a, d
from p5
where (d > (e * 65))
) T1(c_l, a_l, d_l)
left join (
Select c, b, d
from p2
where (a = 11)
) T2(c_r, b_r, d_r)
on ((24 + 1) > c_l)
) T2(c_l_r, b_r_r, d_r_r)
on (c_l_r = 73)
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
Select c_l, c_r
from (
Select c, d
from p5
where (((54 + (b - 78)) > 33) OR (b = 99))
) T1(c_l, d_l)
inner join (
Select c, a
from p5
where (21 > d)
) T2(c_r, a_r)
on ((53 < (43 - c_r)) OR (((72 + (c_l + 89)) < (96 + 34)) OR (c_l > 87)))
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
Select c_l, a_l, a_r_r
from (
select c, a
from (
Select c, a
from p2
where (((c - 9) * (d + 89)) = (a * a))
) T1
union all
select e_l, a_r
from (
Select e_l, a_r
from (
Select e, c
from p3
where (85 = c)
) T1(e_l, c_l)
left join (
Select a
from p2
where (91 > e)
) T2(a_r)
on ((79 * 42) = 66)
) T2
) T1(c_l, a_l)
full join (
Select e_l, a_r, b_r
from (
Select e
from p5
where (e = e)
) T1(e_l)
left join (
Select a, b, d
from p4
where ((97 * (e * 37)) = ((c * c) + (31 + b)))
) T2(a_r, b_r, d_r)
on (65 < 48)
) T2(e_l_r, a_r_r, b_r_r)
on (6 = 82)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #**********************************************
    _testmgr.testcase_end(desc)

