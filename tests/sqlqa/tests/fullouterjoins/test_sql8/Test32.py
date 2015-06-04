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
    
def test001(desc="""Joins Set 32"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_l, e_l_r, d_r_r
from (
Select e, c, a, d
from p2
where ((19 < b) OR (b < 20))
) T1(e_l, c_l, a_l, d_l)
inner join (
Select e_l, c_l, b_r, d_r
from (
Select e, c, b
from p2
where (a < 3)
) T1(e_l, c_l, b_l)
left join (
Select b, d
from p1
where (24 < 24)
) T2(b_r, d_r)
on (((e_l * 92) = e_l) AND (81 = e_l))
) T2(e_l_r, c_l_r, b_r_r, d_r_r)
on (d_r_r = (13 - 34))
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
Select c_l, e_r
from (
Select c, b, d
from p5
where (a > a)
) T1(c_l, b_l, d_l)
left join (
Select e, c, d
from p2
where (32 = ((a * a) - 47))
) T2(e_r, c_r, d_r)
on ((e_r = 2) OR ((3 < e_r) OR (((c_l + 91) = c_l) AND ((((e_r + 72) + c_l) = 23) AND (c_l = c_l)))))
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
Select a_l, b_l, e_r
from (
select a, b
from (
Select a, b
from p2
where ((e = 10) OR (a < c))
) T1
union all
select a, b
from (
select a, b
from (
Select a, b
from p4
where (b < a)
) T1
union all
select e_l, a_l
from (
Select e_l, a_l, a_r
from (
Select e, a, b, d
from p5
where (44 > (54 - c))
) T1(e_l, a_l, b_l, d_l)
left join (
Select c, a, b
from p1
where (d > a)
) T2(c_r, a_r, b_r)
on (e_l = 25)
) T2
) T2
) T1(a_l, b_l)
full join (
Select e
from p1
where ((61 = 79) AND ((a - 93) > a))
) T2(e_r)
on (21 = (2 + a_l))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_r_l, e_r
from (
Select a_l, b_r_r
from (
Select a
from p3
where ((68 = e) OR (a > 33))
) T1(a_l)
left join (
Select a_l_l, b_r
from (
Select a_l, d_l, b_r
from (
Select c, a, d
from p1
where (e = b)
) T1(c_l, a_l, d_l)
inner join (
Select b
from p4
where (52 < 98)
) T2(b_r)
on ((d_l + d_l) = 31)
) T1(a_l_l, d_l_l, b_r_l)
full join (
Select b
from p2
where (e > d)
) T2(b_r)
on ((40 < 19) AND ((a_l_l - 36) = b_r))
) T2(a_l_l_r, b_r_r)
on (87 = 28)
) T1(a_l_l, b_r_r_l)
left join (
Select e
from p5
where (a > a)
) T2(e_r)
on ((e_r = (11 * b_r_r_l)) OR (((46 * 35) - e_r) = e_r))
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
Select a_l, d_l, b_l_l_r, c_r_r
from (
Select e, a, d
from p4
where ((a = (b * d)) OR ((97 + (b - 1)) > 85))
) T1(e_l, a_l, d_l)
left join (
Select b_l_l, c_r, d_r
from (
Select e_l, b_l, b_r, d_r
from (
select e, a, b
from (
select e, a, b
from (
Select e, a, b
from p1
where ((85 = a) AND ((7 < 43) OR ((d = d) AND (e < d))))
) T1
union all
select a_l_l_l, c_r, b_r
from (
Select a_l_l_l, c_r, b_r
from (
select a_l_l
from (
Select a_l_l, b_r_l, e_l_l, b_r_r
from (
Select e_l, a_l, b_r
from (
Select e, a
from p5
where ((a = c) OR (e = e))
) T1(e_l, a_l)
left join (
Select a, b, d
from p5
where (b = 71)
) T2(a_r, b_r, d_r)
on ((21 = 69) AND ((64 < 26) OR ((b_r > e_l) OR ((41 > 36) OR ((24 < e_l) OR (25 = a_l))))))
) T1(e_l_l, a_l_l, b_r_l)
inner join (
Select c_l, b_l, c_r, b_r
from (
Select c, b
from p2
where ((48 * (e * e)) > (92 + 71))
) T1(c_l, b_l)
inner join (
Select c, b
from p3
where ((11 = (77 + (60 * e))) AND ((22 < b) OR ((72 = c) OR (85 < (83 + 70)))))
) T2(c_r, b_r)
on ((((c_r + b_r) + 75) * 14) > c_l)
) T2(c_l_r, b_l_r, c_r_r, b_r_r)
on (46 < b_r_r)
) T1
union all
select e
from (
Select e
from p2
where ((62 + (d - (e * a))) = 10)
) T2
) T1(a_l_l_l)
full join (
Select e, c, b
from p5
where ((c < a) OR (((44 - (a + 33)) = 67) OR (d = e)))
) T2(e_r, c_r, b_r)
on (((19 - 92) < a_l_l_l) OR ((c_r = (93 * 73)) OR ((b_r = c_r) AND (15 > 85))))
) T2
) T1
union all
select e, a, b
from (
Select e, a, b
from p1
where (e < b)
) T2
) T1(e_l, a_l, b_l)
left join (
Select b, d
from p2
where (20 = ((57 - 94) - 60))
) T2(b_r, d_r)
on ((53 > (b_r + b_r)) AND (83 = 19))
) T1(e_l_l, b_l_l, b_r_l, d_r_l)
inner join (
Select c, b, d
from p4
where (b < d)
) T2(c_r, b_r, d_r)
on (66 > c_r)
) T2(b_l_l_r, c_r_r, d_r_r)
on (a_l > 10)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_r_l, a_l_r, d_r_r
from (
Select e_l, d_l, e_r
from (
Select e, d
from p3
where (e < 86)
) T1(e_l, d_l)
left join (
select e, c
from (
Select e, c
from p4
where (67 = (d * c))
) T1
union all
select c, a
from (
Select c, a
from p3
where (c < 13)
) T2
) T2(e_r, c_r)
on ((19 < e_l) OR (5 < e_r))
) T1(e_l_l, d_l_l, e_r_l)
full join (
Select a_l, d_r
from (
Select a
from p4
where (56 = ((c + (a - 23)) + (e * 80)))
) T1(a_l)
inner join (
Select b, d
from p2
where (52 = b)
) T2(b_r, d_r)
on ((39 < d_r) AND ((14 + a_l) < 1))
) T2(a_l_r, d_r_r)
on (88 > 77)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_l, e_l_r
from (
Select e, a
from p4
where ((80 * e) > 57)
) T1(e_l, a_l)
inner join (
Select e_l, c_l, b_r
from (
Select e, c
from p5
where (e = b)
) T1(e_l, c_l)
left join (
Select b
from p1
where (a = e)
) T2(b_r)
on (((c_l - 32) < (e_l - 40)) OR (47 > 32))
) T2(e_l_r, c_l_r, b_r_r)
on (91 = a_l)
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
Select c
from p3
where (94 < e)
) T1(c_l)
inner join (
Select c
from p5
where (b > 52)
) T2(c_r)
on (c_r > 18)
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
Select c_l, a_l, d_l, a_r_r, d_l_r
from (
Select c, a, d
from p2
where (a = a)
) T1(c_l, a_l, d_l)
inner join (
Select d_l, a_r
from (
Select d
from p1
where ((a = d) AND ((26 < (94 + b)) OR (46 > (e - c))))
) T1(d_l)
inner join (
Select e, c, a
from p4
where (a = (c * d))
) T2(e_r, c_r, a_r)
on (56 < d_l)
) T2(d_l_r, a_r_r)
on (d_l_r = a_r_r)
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
Select e_l, b_l, e_r
from (
Select e, b
from p1
where ((97 = b) AND ((e = c) OR (d < c)))
) T1(e_l, b_l)
full join (
select e
from (
Select e, c
from p1
where (52 > 14)
) T1
union all
select a
from (
Select a
from p2
where (((98 * (34 * 10)) = (93 + d)) OR (c = 6))
) T2
) T2(e_r)
on (e_l = (49 + b_l))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_r, d_r
from (
Select c, a
from p4
where ((e > 73) OR ((d < (36 - 90)) OR ((8 < c) OR (((b + e) = 57) AND (a < c)))))
) T1(c_l, a_l)
inner join (
Select b, d
from p4
where (61 = 96)
) T2(b_r, d_r)
on (27 > 87)
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
Select e_l, a_r
from (
select e
from (
Select e
from p2
where (49 = (e + 3))
) T1
union all
select d
from (
Select d
from p5
where (97 < c)
) T2
) T1(e_l)
left join (
Select c, a, b
from p2
where ((37 > 20) OR ((52 > d) OR ((e * d) = e)))
) T2(c_r, a_r, b_r)
on ((22 > (47 + a_r)) OR (e_l < (55 * 0)))
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
Select a_r_l, c_l_l_r, a_r_r
from (
Select a_l, c_r, a_r
from (
Select a
from p4
where (((35 + 18) - 67) = 36)
) T1(a_l)
left join (
select c, a, d
from (
Select c, a, d
from p3
where (30 = e)
) T1
union all
select e, b, d
from (
Select e, b, d
from p1
where (((a * d) + (40 + 82)) = e)
) T2
) T2(c_r, a_r, d_r)
on (c_r = 6)
) T1(a_l_l, c_r_l, a_r_l)
left join (
select c_l_l, b_l_l_r_l, a_r, d_r
from (
Select c_l_l, b_l_l_r_l, a_r, d_r
from (
Select c_l, b_l_l_r, c_r_r
from (
Select c
from p4
where ((a + 75) < 38)
) T1(c_l)
inner join (
Select b_l_l, e_r_l, c_r
from (
Select a_l, b_l, e_r
from (
Select a, b
from p2
where (c > 75)
) T1(a_l, b_l)
inner join (
Select e
from p3
where (25 = (d + 6))
) T2(e_r)
on (32 = 83)
) T1(a_l_l, b_l_l, e_r_l)
inner join (
Select c
from p3
where (d = c)
) T2(c_r)
on (e_r_l = 43)
) T2(b_l_l_r, e_r_l_r, c_r_r)
on ((4 > 14) AND (b_l_l_r = 48))
) T1(c_l_l, b_l_l_r_l, c_r_r_l)
left join (
Select a, d
from p2
where (13 > 97)
) T2(a_r, d_r)
on (80 = b_l_l_r_l)
) T1
union all
select a_l_l, c_l_l, c_r_l, e_l_r
from (
Select a_l_l, c_l_l, c_r_l, e_l_r, e_r_r, b_l_r
from (
Select c_l, a_l, e_r, c_r, a_r
from (
Select c, a
from p4
where ((50 + 60) > 7)
) T1(c_l, a_l)
inner join (
select e, c, a
from (
Select e, c, a
from p5
where ((12 < 65) AND ((97 < (1 * e)) AND ((25 = 47) OR (36 = 68))))
) T1
union all
select c_l, e_r, a_r
from (
Select c_l, e_r, a_r, d_r
from (
Select c
from p4
where (d < 30)
) T1(c_l)
inner join (
Select e, a, d
from p4
where (d = c)
) T2(e_r, a_r, d_r)
on (c_l > d_r)
) T2
) T2(e_r, c_r, a_r)
on ((38 = (68 * (a_l * c_r))) OR (46 = 98))
) T1(c_l_l, a_l_l, e_r_l, c_r_l, a_r_l)
left join (
Select e_l, b_l, e_r, a_r
from (
Select e, c, b
from p2
where (47 = b)
) T1(e_l, c_l, b_l)
left join (
Select e, a
from p2
where ((94 > b) AND ((27 + d) = b))
) T2(e_r, a_r)
on ((((e_r - 80) + (70 * b_l)) - 56) = 72)
) T2(e_l_r, b_l_r, e_r_r, a_r_r)
on (e_r_r > e_r_r)
) T2
) T2(c_l_l_r, b_l_l_r_l_r, a_r_r, d_r_r)
on ((a_r_r + 40) > (c_l_l_r + 84))
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
Select c_l, d_r
from (
Select c
from p3
where (7 < a)
) T1(c_l)
left join (
Select d
from p1
where ((d = 42) OR (78 = 27))
) T2(d_r)
on (d_r < c_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_l, c_r_r_l, d_l_l, e_r
from (
Select c_l, b_l, d_l, a_r_l_r, c_r_r
from (
Select c, b, d
from p4
where (56 > c)
) T1(c_l, b_l, d_l)
full join (
Select a_r_l, c_r
from (
Select b_l, d_l, a_r
from (
Select c, b, d
from p1
where (48 < 63)
) T1(c_l, b_l, d_l)
left join (
Select a
from p3
where (58 > e)
) T2(a_r)
on ((53 > (18 * 98)) OR ((a_r = d_l) OR ((a_r = 82) AND ((43 > 94) AND (7 < (7 - b_l))))))
) T1(b_l_l, d_l_l, a_r_l)
inner join (
Select c
from p3
where (91 = a)
) T2(c_r)
on ((8 * c_r) > 44)
) T2(a_r_l_r, c_r_r)
on (b_l < (d_l + 12))
) T1(c_l_l, b_l_l, d_l_l, a_r_l_r_l, c_r_r_l)
full join (
select e, a
from (
Select e, a
from p2
where ((6 + e) > c)
) T1
union all
select d_l, d_r
from (
Select d_l, d_r
from (
Select d
from p5
where ((28 = 21) OR ((27 > ((46 - d) + c)) AND (e = 52)))
) T1(d_l)
left join (
Select d
from p2
where (8 > 17)
) T2(d_r)
on ((8 = d_r) AND (89 < d_r))
) T2
) T2(e_r, a_r)
on (c_r_r_l = c_r_r_l)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_l, d_l, d_r
from (
Select e, a, b, d
from p2
where (28 = 29)
) T1(e_l, a_l, b_l, d_l)
inner join (
select d
from (
select d
from (
Select d
from p2
where (38 = d)
) T1
union all
select a
from (
select a
from (
Select a
from p4
where (b = b)
) T1
union all
select a_r_l_l_r_l_l_l
from (
Select a_r_l_l_r_l_l_l, d_r
from (
Select a_r_l_l_r_l_l, c_r_l, e_r, d_r
from (
Select a_r_l_l_r_l, b_l_l, c_r
from (
Select b_l, e_l_l_l_r, a_r_l_l_r
from (
select b
from (
Select b
from p3
where ((53 * 72) = 89)
) T1
union all
select e
from (
Select e, c
from p2
where (c = c)
) T2
) T1(b_l)
left join (
Select a_r_l_l, e_l_l_l, e_r
from (
Select e_l_l, a_r_l, d_r
from (
Select e_l, b_l, a_r
from (
Select e, b
from p4
where ((d = 42) AND (93 > 73))
) T1(e_l, b_l)
left join (
Select a
from p4
where (((e + (76 + a)) = (b * d)) AND (b = 51))
) T2(a_r)
on (((31 + (e_l - a_r)) > b_l) AND ((e_l * (39 - 12)) = ((e_l - a_r) * (93 + (72 - e_l)))))
) T1(e_l_l, b_l_l, a_r_l)
inner join (
Select e, b, d
from p2
where (c > 82)
) T2(e_r, b_r, d_r)
on ((e_l_l = 13) AND ((97 = 36) AND ((d_r > 68) OR (e_l_l > a_r_l))))
) T1(e_l_l_l, a_r_l_l, d_r_l)
inner join (
Select e, d
from p5
where ((39 = d) AND (28 = (a * (c + (a * 82)))))
) T2(e_r, d_r)
on (53 > (78 + (e_l_l_l * 59)))
) T2(a_r_l_l_r, e_l_l_l_r, e_r_r)
on (((88 * 32) * (a_r_l_l_r - 93)) = (44 - (e_l_l_l_r * 11)))
) T1(b_l_l, e_l_l_l_r_l, a_r_l_l_r_l)
left join (
select c
from (
Select c, b
from p1
where ((d = a) AND ((b > (90 * ((15 * ((c - d) + 24)) - 23))) AND (((49 + 15) < 60) AND ((86 > 50) AND ((((89 + a) * a) > a) OR (b < c))))))
) T1
union all
select d
from (
Select d
from p4
where ((95 = (14 - d)) AND (e = (22 * 44)))
) T2
) T2(c_r)
on (b_l_l > 15)
) T1(a_r_l_l_r_l_l, b_l_l_l, c_r_l)
inner join (
Select e, c, d
from p5
where (56 = (0 * e))
) T2(e_r, c_r, d_r)
on (5 > e_r)
) T1(a_r_l_l_r_l_l_l, c_r_l_l, e_r_l, d_r_l)
full join (
Select a, d
from p4
where (d < e)
) T2(a_r, d_r)
on ((43 - (d_r * 78)) > d_r)
) T2
) T2
) T1
union all
select e
from (
Select e
from p3
where (c > 97)
) T2
) T2(d_r)
on ((b_l > d_r) OR (29 > 86))
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
Select a_l_r_r_l, b_l_l, c_r
from (
Select a_l, b_l, a_l_r_r, d_r_l_r_r_r
from (
Select a, b
from p4
where ((5 > 18) AND (a = b))
) T1(a_l, b_l)
inner join (
select e_l, a_l_r, d_r_l_r_r
from (
Select e_l, a_l_r, d_r_l_r_r
from (
Select e, a
from p1
where (38 = a)
) T1(e_l, a_l)
left join (
Select c_l, a_l, b_l, d_r_r, a_l_l_r, d_r_l_r
from (
Select c, a, b
from p2
where ((51 = d) OR (((65 * 26) < d) OR (d = (12 + 43))))
) T1(c_l, a_l, b_l)
inner join (
Select a_l_l, d_r_l, d_r
from (
Select a_l, d_r
from (
Select c, a, b
from p2
where ((a * 42) < 97)
) T1(c_l, a_l, b_l)
full join (
Select d
from p1
where (74 = 63)
) T2(d_r)
on (((a_l * (d_r + 25)) > a_l) AND ((d_r < 49) OR ((72 = 85) AND (22 < d_r))))
) T1(a_l_l, d_r_l)
left join (
Select b, d
from p4
where ((d < b) OR ((((a + d) + e) < 66) OR ((c * d) > (68 - 15))))
) T2(b_r, d_r)
on (d_r_l < 56)
) T2(a_l_l_r, d_r_l_r, d_r_r)
on (((37 * 94) = a_l_l_r) AND (a_l = 7))
) T2(c_l_r, a_l_r, b_l_r, d_r_r_r, a_l_l_r_r, d_r_l_r_r)
on ((e_l = d_r_l_r_r) OR ((d_r_l_r_r - a_l_r) = ((71 * 28) * (92 + e_l))))
) T1
union all
select c_l, d_l, c_l_r
from (
Select c_l, d_l, c_l_r, e_l_r
from (
Select c, d
from p5
where (7 = b)
) T1(c_l, d_l)
left join (
Select e_l, c_l, d_r_r
from (
Select e, c
from p4
where ((((63 * 50) + ((a + 3) * e)) < d) AND ((8 + a) > 70))
) T1(e_l, c_l)
left join (
Select c_l_l, d_r
from (
Select c_l, c_r, a_r
from (
Select c, a, b
from p2
where (((a - b) > c) OR (31 < ((b - c) * 89)))
) T1(c_l, a_l, b_l)
inner join (
Select c, a
from p5
where (((22 - b) = c) AND ((a = a) OR ((d > (47 + 41)) OR (d = b))))
) T2(c_r, a_r)
on ((7 > 9) AND ((a_r < a_r) OR ((13 = 65) AND ((c_r > 21) AND (59 > 94)))))
) T1(c_l_l, c_r_l, a_r_l)
left join (
select c, d
from (
Select c, d
from p4
where (((18 * 57) = d) AND ((e = d) OR ((60 - d) = 88)))
) T1
union all
select e, c
from (
Select e, c, d
from p4
where ((31 > d) AND ((c > 84) AND (60 = (e + 73))))
) T2
) T2(c_r, d_r)
on (67 > 77)
) T2(c_l_l_r, d_r_r)
on (d_r_r > 21)
) T2(e_l_r, c_l_r, d_r_r_r)
on (47 = 99)
) T2
) T2(e_l_r, a_l_r_r, d_r_l_r_r_r)
on ((57 * (a_l - ((b_l - 15) - d_r_l_r_r_r))) = 79)
) T1(a_l_l, b_l_l, a_l_r_r_l, d_r_l_r_r_r_l)
full join (
select c
from (
Select c, b, d
from p2
where (((e + a) * b) = d)
) T1
union all
select b
from (
Select b
from p2
where (27 = 40)
) T2
) T2(c_r)
on (37 = 39)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_l, d_l, a_l_r, c_r_r_r
from (
Select c, a, d
from p1
where (e = e)
) T1(c_l, a_l, d_l)
left join (
Select a_l, d_r_r_l_r, c_r_r
from (
Select a
from p1
where ((((22 + 71) + ((98 + (69 - a)) + e)) = 36) OR (a = 55))
) T1(a_l)
inner join (
Select d_r_r_l, e_r, c_r
from (
Select c_l_l, e_l_r, d_r_r
from (
select c_l, b_l, c_l_r
from (
Select c_l, b_l, c_l_r
from (
Select c, a, b
from p4
where (d = 78)
) T1(c_l, a_l, b_l)
left join (
Select c_l, b_r
from (
Select c
from p1
where ((20 < 38) OR ((63 + 57) = c))
) T1(c_l)
left join (
Select b
from p2
where ((e - c) > 99)
) T2(b_r)
on (90 = ((c_l * b_r) + 27))
) T2(c_l_r, b_r_r)
on (((c_l_r + c_l) < 42) OR (((78 * b_l) = b_l) AND (c_l = (62 + (29 - 45)))))
) T1
union all
select b_r_l, d_r_l_l, e_r
from (
Select b_r_l, d_r_l_l, e_r, c_r
from (
Select d_r_l, a_r_l_l, b_r
from (
Select e_l_l, a_r_l, b_l_l, a_r, d_r
from (
Select e_l, b_l, d_l, a_r
from (
Select e, a, b, d
from p3
where (((55 - 57) * b) > c)
) T1(e_l, a_l, b_l, d_l)
left join (
Select a
from p4
where (25 = 82)
) T2(a_r)
on (d_l = 21)
) T1(e_l_l, b_l_l, d_l_l, a_r_l)
inner join (
Select e, a, d
from p5
where (d < ((e - c) * b))
) T2(e_r, a_r, d_r)
on ((22 = 90) AND (25 = (b_l_l * 70)))
) T1(e_l_l_l, a_r_l_l, b_l_l_l, a_r_l, d_r_l)
left join (
select b
from (
Select b
from p1
where (((66 - c) = d) OR ((10 - 89) = (((d - a) - d) - 24)))
) T1
union all
select c
from (
Select c
from p2
where (c = 61)
) T2
) T2(b_r)
on (d_r_l = (14 - 17))
) T1(d_r_l_l, a_r_l_l_l, b_r_l)
inner join (
Select e, c, d
from p3
where ((89 = c) OR ((e < a) OR ((b - (e - b)) = 2)))
) T2(e_r, c_r, d_r)
on (3 > 67)
) T2
) T1(c_l_l, b_l_l, c_l_r_l)
full join (
Select e_l, d_r
from (
Select e, c, a
from p5
where (c > e)
) T1(e_l, c_l, a_l)
left join (
Select c, d
from p5
where (c = 2)
) T2(c_r, d_r)
on (d_r > e_l)
) T2(e_l_r, d_r_r)
on (32 = 13)
) T1(c_l_l_l, e_l_r_l, d_r_r_l)
left join (
Select e, c, d
from p3
where ((72 = d) AND (93 = 19))
) T2(e_r, c_r, d_r)
on (((6 - (d_r_r_l * e_r)) - 76) < c_r)
) T2(d_r_r_l_r, e_r_r, c_r_r)
on (d_r_r_l_r = 47)
) T2(a_l_r, d_r_r_l_r_r, c_r_r_r)
on ((d_l = (a_l - ((74 + d_l) + a_l))) OR (a_l = 78))
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_r_l_l, a_r, d_r
from (
Select c_r_l, b_r_r_r_r, b_l_r
from (
Select e_l, c_r
from (
Select e, c, a
from p2
where (b > b)
) T1(e_l, c_l, a_l)
left join (
Select c, a
from p2
where (d < 26)
) T2(c_r, a_r)
on (c_r < e_l)
) T1(e_l_l, c_r_l)
left join (
Select c_l, b_l, a_l_r_r, e_r_l_r, b_r_r_r
from (
Select c, b
from p5
where (d = 66)
) T1(c_l, b_l)
inner join (
Select e_r_l, a_l_r, b_r_r
from (
Select e_l, d_l, e_r
from (
select e, d
from (
Select e, d
from p5
where ((e = c) AND (63 = 79))
) T1
union all
select c, a
from (
Select c, a
from p2
where ((d + e) = b)
) T2
) T1(e_l, d_l)
left join (
select e
from (
Select e
from p2
where ((c < d) OR (47 = 46))
) T1
union all
select e
from (
Select e, c, a, d
from p3
where (18 = (22 * 31))
) T2
) T2(e_r)
on ((d_l < (13 * 91)) OR ((e_r - e_r) = d_l))
) T1(e_l_l, d_l_l, e_r_l)
inner join (
Select a_l, b_r
from (
Select a
from p1
where (96 > d)
) T1(a_l)
left join (
Select a, b
from p4
where (54 > b)
) T2(a_r, b_r)
on ((b_r * 11) < 59)
) T2(a_l_r, b_r_r)
on (11 > 7)
) T2(e_r_l_r, a_l_r_r, b_r_r_r)
on (31 = 42)
) T2(c_l_r, b_l_r, a_l_r_r_r, e_r_l_r_r, b_r_r_r_r)
on (78 < c_r_l)
) T1(c_r_l_l, b_r_r_r_r_l, b_l_r_l)
inner join (
Select e, a, b, d
from p4
where (((c * 72) = (c * 70)) OR (((b * d) = a) AND (12 < 34)))
) T2(e_r, a_r, b_r, d_r)
on (c_r_l_l > ((a_r * (67 - ((c_r_l_l - d_r) + a_r))) + (c_r_l_l + a_r)))
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
Select a_l_l, c_r_l, e_r
from (
Select a_l, c_r
from (
Select e, a, d
from p1
where ((a + b) = b)
) T1(e_l, a_l, d_l)
left join (
Select c
from p1
where (52 = 76)
) T2(c_r)
on ((a_l > 41) OR (67 = 91))
) T1(a_l_l, c_r_l)
inner join (
Select e, d
from p5
where ((38 < (8 * 75)) AND ((33 = ((a * a) + 99)) OR (a = 51)))
) T2(e_r, d_r)
on ((c_r_l - 99) > e_r)
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
    #*********************************
    _testmgr.testcase_end(desc)

