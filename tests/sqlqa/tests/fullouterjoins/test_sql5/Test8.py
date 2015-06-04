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
    
def test001(desc="""Joins Set 8"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
Select e_l, a_l, d_l, c_r_l_l_l_r
from (
Select e, a, d
from p2
where (c < 34)
) T1(e_l, a_l, d_l)
left join (
Select c_r_l_l_l, b_r_r_l, d_l_r_l_l, e_r
from (
Select c_r_l_l, d_l_r_l, a_l_r, b_r_r
from (
Select c_r_l, d_l_r
from (
Select b_l_l, c_r
from (
Select b_l, b_r
from (
Select b
from p3
where ((23 > a) AND (b = 17))
) T1(b_l)
left join (
Select b
from p4
where ((9 < 50) OR (c = 32))
) T2(b_r)
on (b_l = b_l)
) T1(b_l_l, b_r_l)
left join (
Select c, d
from p1
where (37 = (94 - a))
) T2(c_r, d_r)
on (62 = b_l_l)
) T1(b_l_l_l, c_r_l)
full join (
Select c_l, d_l, d_r_r_r, d_l_r_r
from (
Select c, d
from p5
where ((d = c) OR (88 < ((6 + 82) + ((e * 91) - e))))
) T1(c_l, d_l)
inner join (
Select c_l, d_r_r, a_r_r, d_l_r
from (
Select c, b
from p2
where ((b > a) OR ((e - (e + ((66 + 98) + 96))) > a))
) T1(c_l, b_l)
full join (
Select a_l, d_l, a_r, d_r
from (
Select a, d
from p3
where (24 > 16)
) T1(a_l, d_l)
left join (
Select e, a, d
from p1
where (d = (95 * 47))
) T2(e_r, a_r, d_r)
on ((((a_r + d_l) + d_r) > 3) OR ((((a_r - 65) + 94) - 32) < d_r))
) T2(a_l_r, d_l_r, a_r_r, d_r_r)
on ((99 = (36 - 65)) OR (((45 + 16) < (d_r_r - c_l)) OR (a_r_r = d_r_r)))
) T2(c_l_r, d_r_r_r, a_r_r_r, d_l_r_r)
on (54 = (6 + 6))
) T2(c_l_r, d_l_r, d_r_r_r_r, d_l_r_r_r)
on (d_l_r < c_r_l)
) T1(c_r_l_l, d_l_r_l)
left join (
Select a_l, d_l, c_r, b_r
from (
Select a, d
from p2
where (13 = 87)
) T1(a_l, d_l)
inner join (
Select c, b
from p3
where ((68 = 23) AND ((85 * e) > 35))
) T2(c_r, b_r)
on ((8 + 6) = 96)
) T2(a_l_r, d_l_r, c_r_r, b_r_r)
on ((85 = a_l_r) OR ((84 = a_l_r) OR (((56 - a_l_r) - a_l_r) = 47)))
) T1(c_r_l_l_l, d_l_r_l_l, a_l_r_l, b_r_r_l)
inner join (
Select e, b
from p3
where ((e = d) OR (d = c))
) T2(e_r, b_r)
on (58 > d_l_r_l_l)
) T2(c_r_l_l_l_r, b_r_r_l_r, d_l_r_l_l_r, e_r_r)
on (98 = a_l)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_l, a_l_r, e_l_r
from (
Select a, d
from p5
where (1 = c)
) T1(a_l, d_l)
full join (
select e_l, a_l
from (
select e_l, a_l
from (
Select e_l, a_l, e_r, a_r
from (
select e, a, d
from (
Select e, a, d
from p5
where ((46 + (b + 59)) = (d - b))
) T1
union all
select e_r_l, b_l_l, d_r_l_r
from (
Select e_r_l, b_l_l, d_r_l_r, e_r_r
from (
Select b_l, e_r
from (
Select b
from p2
where (e = b)
) T1(b_l)
inner join (
Select e
from p4
where (b > a)
) T2(e_r)
on (72 > b_l)
) T1(b_l_l, e_r_l)
inner join (
select d_r_l, e_r
from (
Select d_r_l, e_r
from (
Select a_l_l, e_r, d_r
from (
Select a_l, e_r
from (
Select a
from p3
where (b = 51)
) T1(a_l)
inner join (
Select e
from p4
where (e = 83)
) T2(e_r)
on ((39 - 70) = (61 + (77 + 16)))
) T1(a_l_l, e_r_l)
left join (
Select e, d
from p5
where ((84 = b) OR (75 < (b * 85)))
) T2(e_r, d_r)
on ((10 = a_l_l) AND (d_r < (a_l_l - e_r)))
) T1(a_l_l_l, e_r_l, d_r_l)
left join (
select e
from (
Select e
from p2
where (((b - a) > b) AND (c > e))
) T1
union all
select a_l_l
from (
Select a_l_l, e_r_l_r_l, e_l_r, c_r_r
from (
Select e_l, a_l, b_r_r, e_r_l_r
from (
Select e, c, a
from p3
where ((e = c) AND (b < d))
) T1(e_l, c_l, a_l)
full join (
Select e_r_l, b_r
from (
Select d_r_l, b_r_l_l, e_r
from (
Select b_r_l, e_r_l, d_r
from (
Select a_l, e_r, b_r
from (
Select e, a, d
from p4
where (a = ((32 + (50 * 80)) * c))
) T1(e_l, a_l, d_l)
inner join (
Select e, b
from p2
where ((67 < 29) OR (a > d))
) T2(e_r, b_r)
on (88 = 27)
) T1(a_l_l, e_r_l, b_r_l)
inner join (
Select a, b, d
from p3
where (e < 4)
) T2(a_r, b_r, d_r)
on ((34 > 83) AND ((b_r_l > 91) OR ((e_r_l > 3) OR (e_r_l = 94))))
) T1(b_r_l_l, e_r_l_l, d_r_l)
full join (
Select e
from p2
where (d > 32)
) T2(e_r)
on (b_r_l_l < 20)
) T1(d_r_l_l, b_r_l_l_l, e_r_l)
left join (
Select a, b
from p1
where ((45 > c) AND (5 > b))
) T2(a_r, b_r)
on ((69 > 22) OR (b_r > e_r_l))
) T2(e_r_l_r, b_r_r)
on ((b_r_r > e_l) OR ((e_l + e_l) > a_l))
) T1(e_l_l, a_l_l, b_r_r_l, e_r_l_r_l)
left join (
Select e_l, c_r
from (
Select e, c, b, d
from p2
where ((58 * 98) > c)
) T1(e_l, c_l, b_l, d_l)
left join (
Select c
from p5
where ((46 = 44) AND (((c - 88) < 20) AND (d < (c + 94))))
) T2(c_r)
on (81 = (c_r - c_r))
) T2(e_l_r, c_r_r)
on (96 = 91)
) T2
) T2(e_r)
on (32 > d_r_l)
) T1
union all
select c, d
from (
Select c, d
from p3
where ((e - (67 * b)) > 16)
) T2
) T2(d_r_l_r, e_r_r)
on ((77 * 19) > 61)
) T2
) T1(e_l, a_l, d_l)
left join (
Select e, c, a, b
from p1
where ((((b + d) - (a - d)) = (d - (86 + 94))) AND ((65 = b) AND (d = ((17 * a) * 92))))
) T2(e_r, c_r, a_r, b_r)
on ((85 = 38) AND (31 < 51))
) T1
union all
select e, c
from (
Select e, c
from p4
where ((64 < 19) OR ((a = b) AND (((c + b) < c) OR (d = 13))))
) T2
) T1
union all
select c_l, b_r_l_r_r
from (
Select c_l, b_r_l_r_r, c_l_l_r_r
from (
select c, d
from (
Select c, d
from p4
where (43 = e)
) T1
union all
select e, c
from (
Select e, c
from p2
where (d > 7)
) T2
) T1(c_l, d_l)
full join (
Select d_l, c_l_l_r, b_r_l_r
from (
Select d
from p3
where (d > 65)
) T1(d_l)
full join (
Select c_l_l, b_r_l, b_r
from (
Select c_l, d_l, b_r
from (
Select c, a, d
from p1
where ((7 = (67 + (b * e))) OR ((b > ((31 - 97) + c)) AND ((88 + 55) > (a + c))))
) T1(c_l, a_l, d_l)
full join (
Select e, b
from p5
where ((90 + 46) = e)
) T2(e_r, b_r)
on ((((36 * 48) - d_l) + b_r) = 71)
) T1(c_l_l, d_l_l, b_r_l)
left join (
Select b
from p2
where (c = 87)
) T2(b_r)
on ((c_l_l = ((16 - 48) - c_l_l)) AND (66 > b_r_l))
) T2(c_l_l_r, b_r_l_r, b_r_r)
on ((d_l = 10) AND ((76 + b_r_l_r) = ((d_l - (c_l_l_r - 46)) + c_l_l_r)))
) T2(d_l_r, c_l_l_r_r, b_r_l_r_r)
on (c_l_l_r_r = b_r_l_r_r)
) T2
) T2(e_l_r, a_l_r)
on ((e_l_r + (d_l + (87 - 62))) < a_l_r)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_l, e_r, a_r, d_r
from (
Select c_l, c_r_r
from (
Select c
from p4
where (a > 10)
) T1(c_l)
inner join (
Select a_l, d_l, e_r, c_r, a_r
from (
Select a, d
from p3
where ((69 > (b * 38)) OR (a = a))
) T1(a_l, d_l)
left join (
Select e, c, a
from p2
where ((((18 - (47 - b)) * 40) = 86) AND (d = d))
) T2(e_r, c_r, a_r)
on ((2 = 29) OR ((d_l < 71) AND (a_r > c_r)))
) T2(a_l_r, d_l_r, e_r_r, c_r_r, a_r_r)
on (((c_l + c_l) * (c_r_r - 12)) < c_r_r)
) T1(c_l_l, c_r_r_l)
inner join (
Select e, a, d
from p3
where ((c > 40) OR (e > e))
) T2(e_r, a_r, d_r)
on (((a_r - c_l_l) = c_l_l) OR (c_l_l < (c_l_l - a_r)))
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
Select c_l_l_l_r_l, d_r
from (
Select e_l, a_l, c_l_l_r_r_l_r, b_l_r_l_r, e_l_l_r_r, c_l_l_l_r
from (
Select e, a
from p1
where (16 < b)
) T1(e_l, a_l)
inner join (
Select b_l_r_l, c_l_l_l, c_l_l_r_r_l, e_l_l_r
from (
Select a_l_l, c_l_l, d_r_l, c_l_l_r_r, b_l_r
from (
Select c_l, a_l, c_r, d_r
from (
Select c, a, b
from p4
where ((2 = c) AND ((b = 43) AND (19 = 58)))
) T1(c_l, a_l, b_l)
inner join (
Select c, d
from p4
where (e < b)
) T2(c_r, d_r)
on ((77 = a_l) OR (44 = c_l))
) T1(c_l_l, a_l_l, c_r_l, d_r_l)
left join (
Select b_l, d_l, c_l_l_r
from (
Select b, d
from p3
where (16 < 50)
) T1(b_l, d_l)
inner join (
Select c_l_l, e_r_l, e_l_r, a_r_r
from (
Select c_l, e_r
from (
Select c
from p1
where (b = c)
) T1(c_l)
left join (
Select e
from p2
where ((40 = e) AND (78 = 89))
) T2(e_r)
on ((e_r + (e_r - e_r)) < (3 * (e_r + e_r)))
) T1(c_l_l, e_r_l)
inner join (
Select e_l, a_r
from (
Select e, a
from p2
where (41 = d)
) T1(e_l, a_l)
full join (
select a
from (
Select a
from p1
where (e < d)
) T1
union all
select b
from (
Select b, d
from p2
where ((c * b) > ((e * 69) - 7))
) T2
) T2(a_r)
on ((a_r - a_r) = 99)
) T2(e_l_r, a_r_r)
on (c_l_l < 44)
) T2(c_l_l_r, e_r_l_r, e_l_r_r, a_r_r_r)
on ((31 < c_l_l_r) OR (c_l_l_r < 2))
) T2(b_l_r, d_l_r, c_l_l_r_r)
on (25 > a_l_l)
) T1(a_l_l_l, c_l_l_l, d_r_l_l, c_l_l_r_r_l, b_l_r_l)
left join (
Select e_l_l, e_r_l, c_l_r, d_l_r
from (
Select e_l, e_r
from (
Select e
from p4
where (c = b)
) T1(e_l)
inner join (
Select e, d
from p2
where ((9 = b) AND (47 = d))
) T2(e_r, d_r)
on (14 > e_l)
) T1(e_l_l, e_r_l)
left join (
select c_l, d_l
from (
Select c_l, d_l, d_l_r
from (
Select e, c, d
from p4
where ((52 < a) AND ((b = 19) AND (36 > (e * 82))))
) T1(e_l, c_l, d_l)
full join (
Select d_l, e_r
from (
select d
from (
Select d
from p3
where (16 = (53 * 37))
) T1
union all
select c
from (
Select c, a
from p4
where (74 = e)
) T2
) T1(d_l)
full join (
Select e
from p1
where ((67 < c) AND ((((8 * c) - a) = (41 + c)) AND (8 = e)))
) T2(e_r)
on (((35 - 5) = d_l) AND (e_r = 82))
) T2(d_l_r, e_r_r)
on ((14 = c_l) OR (52 > d_l))
) T1
union all
select a_l, e_r_r
from (
select a_l, e_r_r
from (
Select a_l, e_r_r
from (
Select a, b, d
from p3
where (b = 42)
) T1(a_l, b_l, d_l)
inner join (
Select b_l, e_r
from (
Select b
from p2
where ((b * ((d - (e + b)) + ((a * d) + 2))) < d)
) T1(b_l)
left join (
select e
from (
Select e, a, b
from p2
where ((d = e) OR (10 < b))
) T1
union all
select d
from (
Select d
from p4
where (c < 81)
) T2
) T2(e_r)
on (34 = 3)
) T2(b_l_r, e_r_r)
on (28 = a_l)
) T1
union all
select c, b
from (
Select c, b
from p3
where ((80 - ((31 - a) + a)) = d)
) T2
) T2
) T2(c_l_r, d_l_r)
on (82 = e_l_l)
) T2(e_l_l_r, e_r_l_r, c_l_r_r, d_l_r_r)
on ((b_l_r_l - 34) = b_l_r_l)
) T2(b_l_r_l_r, c_l_l_l_r, c_l_l_r_r_l_r, e_l_l_r_r)
on (((83 - 81) = 13) AND (((e_l_l_r_r - 86) - (c_l_l_r_r_l_r * (b_l_r_l_r + c_l_l_l_r))) > (25 * ((e_l_l_r_r - (c_l_l_l_r - (e_l_l_r_r - e_l_l_r_r))) * c_l_l_l_r))))
) T1(e_l_l, a_l_l, c_l_l_r_r_l_r_l, b_l_r_l_r_l, e_l_l_r_r_l, c_l_l_l_r_l)
inner join (
Select a, d
from p5
where (44 > d)
) T2(a_r, d_r)
on ((((62 * 43) + 36) = (4 * 70)) OR ((c_l_l_l_r_l = (c_l_l_l_r_l + 15)) AND (d_r = (c_l_l_l_r_l * (d_r + 86)))))
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
Select c_l, a_r
from (
Select e, c, d
from p4
where ((7 > b) OR ((c + c) = d))
) T1(e_l, c_l, d_l)
left join (
select a
from (
Select a
from p4
where (47 > 97)
) T1
union all
select d
from (
Select d
from p1
where ((d < (62 * 79)) AND (c = a))
) T2
) T2(a_r)
on (c_l > c_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_l, b_r_l, a_r_l, e_r
from (
Select a_l, a_r, b_r
from (
Select a
from p4
where (c < (c + 55))
) T1(a_l)
left join (
Select a, b
from p3
where ((b + ((d * e) - 90)) = 9)
) T2(a_r, b_r)
on (43 = 77)
) T1(a_l_l, a_r_l, b_r_l)
left join (
Select e, d
from p5
where (65 = (93 * 91))
) T2(e_r, d_r)
on (a_r_l > 28)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_l, b_r
from (
select a_l, d_l, a_r
from (
Select a_l, d_l, a_r
from (
Select a, d
from p4
where (c = d)
) T1(a_l, d_l)
full join (
Select c, a, b, d
from p4
where (26 < c)
) T2(c_r, a_r, b_r, d_r)
on (63 = 56)
) T1
union all
select a, b, d
from (
Select a, b, d
from p3
where (73 = (26 - 52))
) T2
) T1(a_l_l, d_l_l, a_r_l)
inner join (
Select b
from p2
where ((14 < ((a * 13) - 26)) AND ((34 + 17) = 19))
) T2(b_r)
on ((a_l_l > a_l_l) AND (94 > 81))
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
Select c_l, b_l, e_r
from (
Select c, b, d
from p1
where (74 > 25)
) T1(c_l, b_l, d_l)
left join (
Select e, d
from p5
where (46 = 34)
) T2(e_r, d_r)
on ((e_r > (23 + 35)) OR (48 > (b_l - 83)))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, c_r
from (
Select d
from p4
where (49 = 81)
) T1(d_l)
full join (
select c
from (
Select c
from p5
where (89 > d)
) T1
union all
select c
from (
Select c, a
from p2
where ((73 = ((c + a) - a)) AND ((b = 82) OR (1 = c)))
) T2
) T2(c_r)
on (35 < (36 * (d_l - 97)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_r_r
from (
Select a, d
from p3
where (c = a)
) T1(a_l, d_l)
left join (
Select a_l, c_r, a_r, d_r
from (
Select a, b
from p1
where (e = 93)
) T1(a_l, b_l)
full join (
Select c, a, b, d
from p1
where (d < d)
) T2(c_r, a_r, b_r, d_r)
on (39 = 73)
) T2(a_l_r, c_r_r, a_r_r, d_r_r)
on ((53 = (a_l - ((27 + d_r_r) + d_r_r))) OR ((11 - (6 + a_l)) = 56))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_r
from (
Select e
from p2
where ((61 - c) > 62)
) T1(e_l)
inner join (
Select a
from p3
where ((e = 42) AND ((42 < b) AND (1 < 98)))
) T2(a_r)
on ((4 + a_r) = e_l)
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
Select b_r_l, e_l_l_l, c_r
from (
Select e_l_l, c_r_l, b_r
from (
Select e_l, d_l, c_r
from (
Select e, c, d
from p1
where (c > 53)
) T1(e_l, c_l, d_l)
left join (
Select c, d
from p5
where (e > (63 + 5))
) T2(c_r, d_r)
on (((69 * 71) - d_l) = ((c_r - 60) * ((53 * 20) - (d_l + e_l))))
) T1(e_l_l, d_l_l, c_r_l)
full join (
Select e, c, b
from p5
where (b = c)
) T2(e_r, c_r, b_r)
on (39 = b_r)
) T1(e_l_l_l, c_r_l_l, b_r_l)
inner join (
select c
from (
select c
from (
Select c, a, d
from p3
where ((e * c) = c)
) T1
union all
select c
from (
select c
from (
Select c
from p3
where (((e + d) - 74) = 83)
) T1
union all
select e
from (
Select e, c
from p3
where (((54 * d) + 31) = 61)
) T2
) T2
) T1
union all
select b_r_l
from (
select b_r_l, e_r_l_l
from (
Select b_r_l, e_r_l_l, a_r
from (
Select e_r_l, b_r
from (
Select d_l, e_r, c_r
from (
Select d
from p2
where (64 = e)
) T1(d_l)
full join (
Select e, c, b
from p2
where ((((54 * e) - 26) * d) < (77 + 40))
) T2(e_r, c_r, b_r)
on (d_l = e_r)
) T1(d_l_l, e_r_l, c_r_l)
left join (
Select b
from p2
where ((e = b) OR (a = 5))
) T2(b_r)
on (86 > e_r_l)
) T1(e_r_l_l, b_r_l)
inner join (
Select a
from p5
where (6 = (51 + 88))
) T2(a_r)
on (((9 + a_r) = b_r_l) OR (29 > (48 - 23)))
) T1
union all
select b, d
from (
Select b, d
from p2
where (b > (84 + e))
) T2
) T2
) T2(c_r)
on (c_r = (1 * e_l_l_l))
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
Select c_l_l, a_r_l, a_l_r_r, e_l_r
from (
select c_l, a_r
from (
Select c_l, a_r
from (
Select e, c, b
from p1
where (((c - e) < 93) AND (a > 48))
) T1(e_l, c_l, b_l)
left join (
Select a, d
from p3
where ((e = b) OR ((51 = 4) OR ((53 > a) AND (a < e))))
) T2(a_r, d_r)
on ((50 * a_r) > 18)
) T1
union all
select b_l, c_r
from (
Select b_l, c_r
from (
Select b
from p1
where ((99 < 46) AND ((81 < b) OR (((b - b) = (77 * 51)) OR (b = ((83 * e) + 41)))))
) T1(b_l)
left join (
Select c, a, d
from p3
where (54 > 27)
) T2(c_r, a_r, d_r)
on ((b_l = c_r) AND (b_l > b_l))
) T2
) T1(c_l_l, a_r_l)
left join (
select e_l, a_l_r
from (
select e_l, a_l_r, b_r_r
from (
Select e_l, a_l_r, b_r_r
from (
Select e
from p3
where (35 = a)
) T1(e_l)
left join (
Select a_l, b_r
from (
Select a
from p5
where (e < (d + (e + 71)))
) T1(a_l)
left join (
Select b
from p2
where (58 < 15)
) T2(b_r)
on (a_l < (b_r + 99))
) T2(a_l_r, b_r_r)
on ((b_r_r < b_r_r) AND (a_l_r = 69))
) T1
union all
select e, c, a
from (
Select e, c, a, b
from p5
where ((13 = 6) AND (33 = a))
) T2
) T1
union all
select c_l, a_r_r
from (
Select c_l, a_r_r
from (
Select c
from p1
where ((e * 18) < 28)
) T1(c_l)
left join (
Select e_l, a_r
from (
Select e, a
from p1
where ((64 + 4) = (c - 53))
) T1(e_l, a_l)
full join (
Select a, b
from p5
where (e > (c * 57))
) T2(a_r, b_r)
on (83 = e_l)
) T2(e_l_r, a_r_r)
on (81 = 27)
) T2
) T2(e_l_r, a_l_r_r)
on ((74 - (65 * ((6 * a_r_l) * a_l_r_r))) > 63)
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
Select b_r_l, c_r_l, b_l_l, e_r
from (
Select b_l, c_r, b_r
from (
Select a, b
from p3
where (((c - 13) * 36) > 77)
) T1(a_l, b_l)
inner join (
Select e, c, b
from p3
where ((22 = c) AND (39 < a))
) T2(e_r, c_r, b_r)
on ((50 + b_l) > 22)
) T1(b_l_l, c_r_l, b_r_l)
full join (
Select e, c
from p5
where ((c > 43) OR (77 = b))
) T2(e_r, c_r)
on (24 = e_r)
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
Select c_l_l, c_r_l, b_l_r
from (
select c_l, c_r
from (
Select c_l, c_r
from (
Select c
from p3
where ((34 * b) = a)
) T1(c_l)
left join (
Select c
from p4
where (d = 1)
) T2(c_r)
on (c_l = 85)
) T1
union all
select c, a
from (
Select c, a, b
from p3
where (2 > b)
) T2
) T1(c_l_l, c_r_l)
left join (
select b_l
from (
Select b_l, e_l_r, a_r_r
from (
Select e, b
from p2
where ((25 < 78) OR (93 < 59))
) T1(e_l, b_l)
left join (
Select e_l, c_r, a_r
from (
select e
from (
Select e, b
from p2
where (b < 21)
) T1
union all
select d
from (
Select d
from p1
where ((33 < 84) AND (44 = ((c * 5) * (a * 83))))
) T2
) T1(e_l)
full join (
Select c, a
from p2
where ((b = (b * c)) OR ((e - d) > d))
) T2(c_r, a_r)
on (((c_r - (6 * a_r)) < a_r) OR ((a_r - a_r) > 65))
) T2(e_l_r, c_r_r, a_r_r)
on (b_l = 40)
) T1
union all
select a_l
from (
select a_l
from (
Select a_l, e_r
from (
Select e, a
from p1
where ((((d - d) + 1) + (d * 97)) = 6)
) T1(e_l, a_l)
inner join (
Select e
from p5
where (d = ((95 * a) * b))
) T2(e_r)
on ((76 = 6) AND (88 = (a_l * 60)))
) T1
union all
select a
from (
Select a
from p1
where (((c * d) = (21 * e)) OR (((b + 65) < b) OR (e = c)))
) T2
) T2
) T2(b_l_r)
on (11 = 10)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_r
from (
Select e, b
from p3
where (a > d)
) T1(e_l, b_l)
left join (
Select a, d
from p4
where ((((16 + a) * 2) = 5) AND (48 = a))
) T2(a_r, d_r)
on ((99 > a_r) AND (((a_r - 65) > 50) AND ((59 = 86) OR (e_l = e_l))))
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
Select c_l, a_l, c_l_r, c_r_r
from (
Select c, a, b
from p5
where ((b < 59) AND (d > (b + c)))
) T1(c_l, a_l, b_l)
full join (
Select c_l, c_r
from (
select e, c
from (
Select e, c, d
from p1
where ((6 + 29) = ((38 + 2) - a))
) T1
union all
select e, d
from (
Select e, d
from p1
where (88 = 60)
) T2
) T1(e_l, c_l)
full join (
Select c, b, d
from p5
where ((99 > d) AND (12 = d))
) T2(c_r, b_r, d_r)
on ((c_r > 96) OR (42 = ((0 * c_l) + c_r)))
) T2(c_l_r, c_r_r)
on (((17 + c_r_r) + 19) = c_l)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_l, e_r
from (
select c, a
from (
Select c, a, d
from p4
where (e = 55)
) T1
union all
select b_l, a_r
from (
select b_l, a_r
from (
Select b_l, a_r
from (
Select b
from p3
where ((a = 80) AND (b < ((e + c) - e)))
) T1(b_l)
left join (
Select e, a
from p4
where (7 = (87 + 64))
) T2(e_r, a_r)
on (b_l < (a_r - b_l))
) T1
union all
select e, a
from (
Select e, a, b, d
from p5
where (73 > a)
) T2
) T2
) T1(c_l, a_l)
inner join (
Select e
from p2
where (75 = 70)
) T2(e_r)
on (a_l < a_l)
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
Select e_l, d_l, e_l_r, c_r_r
from (
Select e, d
from p3
where (c = 45)
) T1(e_l, d_l)
full join (
Select e_l, c_r
from (
select e, d
from (
Select e, d
from p5
where (b > a)
) T1
union all
select b_l, e_r
from (
select b_l, e_r
from (
Select b_l, e_r
from (
Select c, b
from p2
where (97 = 15)
) T1(c_l, b_l)
left join (
Select e
from p1
where ((b < 9) AND (e = 76))
) T2(e_r)
on (68 = 64)
) T1
union all
select c, d
from (
Select c, d
from p1
where ((d = 73) OR (8 = b))
) T2
) T2
) T1(e_l, d_l)
left join (
Select c, b
from p5
where ((c = b) OR ((88 = 16) OR (88 = (74 * a))))
) T2(c_r, b_r)
on (74 = (e_l * e_l))
) T2(e_l_r, c_r_r)
on (d_l > (20 * e_l_r))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l_l, c_r_l, e_r_r
from (
Select e_l, d_l, c_r
from (
Select e, d
from p3
where (d = 50)
) T1(e_l, d_l)
inner join (
select c
from (
Select c
from p3
where (a = 19)
) T1
union all
select a
from (
Select a, d
from p5
where (a = ((d + c) - 54))
) T2
) T2(c_r)
on (c_r = (d_l + 27))
) T1(e_l_l, d_l_l, c_r_l)
inner join (
Select e_l, e_r
from (
Select e, a
from p5
where ((e < (e * 62)) AND (((e + e) = d) AND (13 < 46)))
) T1(e_l, a_l)
left join (
Select e
from p3
where ((48 = e) AND ((a > a) OR (58 < b)))
) T2(e_r)
on ((37 > 46) AND ((e_r < e_l) OR ((e_r - e_l) = 86)))
) T2(e_l_r, e_r_r)
on (0 > 43)
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
    #*************************************************
    _testmgr.testcase_end(desc)

