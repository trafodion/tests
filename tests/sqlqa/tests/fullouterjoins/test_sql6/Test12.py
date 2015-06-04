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
    
def test001(desc="""Joins Set 12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, d_l, b_r_l_r
from (
Select b, d
from p2
where ((c = 82) AND (e < 7))
) T1(b_l, d_l)
inner join (
Select b_r_l, b_l_l, a_l_r
from (
Select b_l, b_r
from (
Select b
from p2
where (e < (92 + (74 * b)))
) T1(b_l)
inner join (
Select b
from p1
where (a = e)
) T2(b_r)
on ((17 < (b_l + b_r)) AND ((b_l < 89) AND ((b_r > 26) OR ((b_r - 36) = (b_l - 24)))))
) T1(b_l_l, b_r_l)
inner join (
Select e_l, a_l, d_r
from (
Select e, a
from p5
where ((68 * 57) < c)
) T1(e_l, a_l)
left join (
Select d
from p4
where ((d < b) AND ((81 = 77) AND (73 = (39 + e))))
) T2(d_r)
on (d_r = d_r)
) T2(e_l_r, a_l_r, d_r_r)
on (((b_l_l - 32) = 61) OR (a_l_r > b_r_l))
) T2(b_r_l_r, b_l_l_r, a_l_r_r)
on (12 > 2)
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
Select a_l, b_l, e_r
from (
Select a, b, d
from p1
where (d = 42)
) T1(a_l, b_l, d_l)
left join (
Select e, a
from p5
where ((33 + 89) = a)
) T2(e_r, a_r)
on ((89 < 1) OR (36 > a_l))
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
Select b_l_l_r_l, a_r, b_r
from (
Select e_l, b_l_l_r, e_r_r_r_r, b_r_l_r
from (
select e, c
from (
Select e, c, b, d
from p3
where (b = 7)
) T1
union all
select b_l, c_r
from (
Select b_l, c_r
from (
Select c, a, b
from p4
where (75 < a)
) T1(c_l, a_l, b_l)
left join (
Select c, b
from p3
where ((d = (((c + 97) + a) + 50)) AND ((56 > 73) OR ((c * a) > b)))
) T2(c_r, b_r)
on ((64 < 43) OR (b_l = (54 - b_l)))
) T2
) T1(e_l, c_l)
left join (
select b_r_l, b_l_l, e_r_r_r
from (
Select b_r_l, b_l_l, e_r_r_r
from (
Select b_l, d_l, b_r
from (
Select b, d
from p3
where (b = e)
) T1(b_l, d_l)
inner join (
Select b
from p4
where ((c > b) OR (14 = ((b * d) - b)))
) T2(b_r)
on ((b_l = 94) AND ((b_r = b_r) OR ((d_l = 58) OR (d_l = (22 + d_l)))))
) T1(b_l_l, d_l_l, b_r_l)
left join (
Select c_l, e_l_r, e_r_r
from (
Select c
from p4
where (59 = 75)
) T1(c_l)
full join (
select e_l, b_l, e_r
from (
Select e_l, b_l, e_r
from (
Select e, a, b
from p5
where ((c = (a + (c - 65))) AND (e = ((a - 27) + (22 * a))))
) T1(e_l, a_l, b_l)
inner join (
Select e, c, a
from p4
where (27 = 24)
) T2(e_r, c_r, a_r)
on (b_l < e_l)
) T1
union all
select c_l, a_l, c_r
from (
Select c_l, a_l, c_r, b_r
from (
Select e, c, a
from p3
where ((46 > ((65 + (e * 45)) - 29)) AND ((36 = a) AND ((7 - 52) = c)))
) T1(e_l, c_l, a_l)
inner join (
Select e, c, a, b
from p5
where ((66 = 13) AND (33 = e))
) T2(e_r, c_r, a_r, b_r)
on (((70 + c_l) < b_r) OR ((68 * a_l) = 16))
) T2
) T2(e_l_r, b_l_r, e_r_r)
on ((e_r_r - e_r_r) = (e_l_r * 23))
) T2(c_l_r, e_l_r_r, e_r_r_r)
on (b_r_l > e_r_r_r)
) T1
union all
select e, c, a
from (
Select e, c, a
from p1
where (37 = 37)
) T2
) T2(b_r_l_r, b_l_l_r, e_r_r_r_r)
on (20 = 87)
) T1(e_l_l, b_l_l_r_l, e_r_r_r_r_l, b_r_l_r_l)
left join (
Select a, b, d
from p2
where (d < e)
) T2(a_r, b_r, d_r)
on ((b_l_l_r_l = (b_r + 99)) OR ((b_l_l_r_l * 16) > a_r))
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
Select a_l, c_r, a_r
from (
Select a
from p3
where (b = 74)
) T1(a_l)
left join (
Select c, a, d
from p5
where ((c - d) = (((39 + 91) * 40) + 82))
) T2(c_r, a_r, d_r)
on ((18 - c_r) = ((75 - c_r) + (((67 - a_r) - a_r) - (a_l * 90))))
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
select e
from (
Select e, b
from p5
where (a = b)
) T1
union all
select c
from (
Select c
from p4
where (15 = 63)
) T2
) T1(e_l)
inner join (
Select e
from p5
where (79 = (20 + 41))
) T2(e_r)
on ((13 < 20) AND (39 = e_l))
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
Select b_l_l_l, c_r_l_l, e_r_r
from (
Select c_r_l, b_l_l, b_l_l_r
from (
Select b_l, c_r
from (
Select c, a, b, d
from p4
where (76 > a)
) T1(c_l, a_l, b_l, d_l)
left join (
Select c
from p1
where (c = a)
) T2(c_r)
on ((c_r < c_r) OR ((11 - (c_r - (68 - c_r))) = c_r))
) T1(b_l_l, c_r_l)
left join (
Select e_r_l, b_l_l, b_r
from (
select b_l, e_r, a_r
from (
Select b_l, e_r, a_r
from (
select a, b
from (
Select a, b
from p2
where ((e < (b - e)) OR (94 > c))
) T1
union all
select b_l, c_r
from (
Select b_l, c_r
from (
Select a, b
from p3
where (d = (c - (e + 65)))
) T1(a_l, b_l)
left join (
select c
from (
Select c, b, d
from p1
where (48 = c)
) T1
union all
select b
from (
Select b
from p2
where (88 > 72)
) T2
) T2(c_r)
on (c_r = (84 * c_r))
) T2
) T1(a_l, b_l)
inner join (
Select e, a
from p1
where (a > d)
) T2(e_r, a_r)
on ((51 * (b_l + e_r)) = 44)
) T1
union all
select a_r_l, b_l_l, b_r
from (
Select a_r_l, b_l_l, b_r
from (
Select b_l, a_r
from (
Select a, b
from p2
where (4 = 57)
) T1(a_l, b_l)
full join (
Select a
from p2
where (c = 69)
) T2(a_r)
on ((15 < ((17 - b_l) * (6 - a_r))) AND (72 = 82))
) T1(b_l_l, a_r_l)
inner join (
Select b
from p2
where (((a * b) < 44) OR (c = a))
) T2(b_r)
on ((27 > (b_r + 42)) AND (a_r_l = 13))
) T2
) T1(b_l_l, e_r_l, a_r_l)
inner join (
Select b, d
from p4
where (b > 24)
) T2(b_r, d_r)
on ((86 - (b_r - e_r_l)) > e_r_l)
) T2(e_r_l_r, b_l_l_r, b_r_r)
on ((45 < (b_l_l * 8)) OR (b_l_l_r > b_l_l_r))
) T1(c_r_l_l, b_l_l_l, b_l_l_r_l)
inner join (
Select c_l, d_l, e_r, b_r
from (
Select c, d
from p2
where (e < 2)
) T1(c_l, d_l)
left join (
select e, b
from (
Select e, b
from p4
where (61 < 5)
) T1
union all
select c, d
from (
Select c, d
from p1
where ((75 > (80 * e)) AND (45 = 31))
) T2
) T2(e_r, b_r)
on (c_l > 90)
) T2(c_l_r, d_l_r, e_r_r, b_r_r)
on (b_l_l_l > b_l_l_l)
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
Select e_l_l, e_r_l, c_r, d_r
from (
Select e_l, e_r
from (
Select e, a
from p5
where (e < 64)
) T1(e_l, a_l)
full join (
Select e
from p2
where (((b - 30) < e) AND (e < 59))
) T2(e_r)
on (96 < e_l)
) T1(e_l_l, e_r_l)
left join (
Select c, d
from p2
where (d = 46)
) T2(c_r, d_r)
on (((c_r - d_r) < e_r_l) AND (e_r_l < 75))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_r_l, b_l_l, e_r, b_r, d_r
from (
Select b_l, a_r
from (
Select e, b
from p2
where (c > b)
) T1(e_l, b_l)
full join (
Select a
from p4
where (6 = 83)
) T2(a_r)
on ((5 = 52) OR ((78 * a_r) < b_l))
) T1(b_l_l, a_r_l)
left join (
Select e, b, d
from p4
where ((92 = a) AND ((e - b) = ((35 - 42) + (31 - c))))
) T2(e_r, b_r, d_r)
on ((e_r > (b_l_l * 90)) AND ((b_l_l * 47) = 55))
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, d_r
from (
Select a, b
from p3
where ((c = ((31 * (47 - 79)) + 47)) AND (17 > 90))
) T1(a_l, b_l)
full join (
Select a, d
from p5
where (81 = d)
) T2(a_r, d_r)
on (18 = 61)
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
Select e_l, a_l, c_r_r
from (
Select e, a
from p4
where ((d < ((27 + (c * (12 * 33))) * e)) AND ((d = 2) AND ((47 = (((69 - e) + e) * 88)) OR ((d = a) OR (92 = 44)))))
) T1(e_l, a_l)
left join (
Select b_l, c_r, b_r
from (
Select b
from p5
where (0 = 43)
) T1(b_l)
inner join (
Select c, b
from p2
where ((e < 93) AND (c < (63 * a)))
) T2(c_r, b_r)
on ((((c_r + 74) * b_r) * c_r) = (b_l * (23 * 38)))
) T2(b_l_r, c_r_r, b_r_r)
on ((14 * 66) = c_r_r)
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
Select c_r_l, d_r
from (
Select e_l, c_l, c_r, a_r, b_r
from (
select e, c, d
from (
Select e, c, d
from p1
where (14 < b)
) T1
union all
select c, a, d
from (
Select c, a, d
from p5
where (((c - c) = 95) AND ((77 = 47) AND (20 = b)))
) T2
) T1(e_l, c_l, d_l)
left join (
Select c, a, b
from p3
where (7 = 73)
) T2(c_r, a_r, b_r)
on ((c_l = b_r) AND (36 < 32))
) T1(e_l_l, c_l_l, c_r_l, a_r_l, b_r_l)
full join (
select d
from (
Select d
from p2
where ((c > 59) AND ((36 = e) AND ((d = 54) AND (a < (d * b)))))
) T1
union all
select d
from (
Select d
from p1
where (d > e)
) T2
) T2(d_r)
on ((c_r_l * 8) > d_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, e_r
from (
Select b
from p5
where (86 > (16 + 67))
) T1(b_l)
inner join (
Select e
from p4
where (c > 79)
) T2(e_r)
on (61 < (e_r - 33))
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
Select a_l, b_r
from (
select a
from (
select a
from (
Select a, b, d
from p1
where (a = (a - 59))
) T1
union all
select e
from (
select e
from (
Select e
from p2
where ((e > c) AND ((a > (d - c)) AND ((19 < b) OR ((98 + 20) = 16))))
) T1
union all
select b
from (
Select b, d
from p1
where (62 > 2)
) T2
) T2
) T1
union all
select b_l_r_l
from (
Select b_l_r_l, c_l_r_l, b_r
from (
Select d_l, c_l_r, b_l_r
from (
Select a, d
from p1
where (((a - e) < d) AND (11 > 17))
) T1(a_l, d_l)
left join (
Select c_l, b_l, c_l_r, b_r_r
from (
Select c, a, b
from p1
where ((b = b) OR (((46 - c) > 27) AND ((b > 74) OR (((b - 7) > c) AND ((54 + d) = 88)))))
) T1(c_l, a_l, b_l)
full join (
Select c_l, b_r
from (
Select c, a
from p4
where ((e = a) OR (49 < b))
) T1(c_l, a_l)
left join (
Select b
from p4
where (((17 + d) > e) AND (((e - 77) * (c - d)) = a))
) T2(b_r)
on ((5 * (b_r - (41 - c_l))) = c_l)
) T2(c_l_r, b_r_r)
on (22 > c_l)
) T2(c_l_r, b_l_r, c_l_r_r, b_r_r_r)
on ((d_l = 51) OR ((((27 + 68) + 18) < 10) AND (44 < (90 + 86))))
) T1(d_l_l, c_l_r_l, b_l_r_l)
left join (
Select b
from p3
where ((a > 10) AND ((e - c) = (a * e)))
) T2(b_r)
on ((23 - c_l_r_l) > 74)
) T2
) T1(a_l)
full join (
Select b
from p5
where (27 = 3)
) T2(b_r)
on (b_r < 0)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, d_l_r
from (
Select e, b, d
from p2
where (51 = a)
) T1(e_l, b_l, d_l)
inner join (
Select e_l, d_l, d_r_r
from (
Select e, c, a, d
from p4
where ((78 < b) AND (e = (68 * c)))
) T1(e_l, c_l, a_l, d_l)
full join (
Select c_l_l_l, e_r_l, d_r
from (
Select c_l_l, b_r_r_l, e_r
from (
select c_l, b_r_r
from (
Select c_l, b_r_r, e_l_r
from (
select c
from (
Select c
from p2
where ((b + 27) > 33)
) T1
union all
select e
from (
Select e, b
from p4
where (d = (21 * 83))
) T2
) T1(c_l)
full join (
Select e_l, b_r
from (
Select e
from p3
where ((((c - b) * a) = a) OR ((37 * e) < 34))
) T1(e_l)
left join (
Select b
from p2
where (d = (e * e))
) T2(b_r)
on ((e_l < (e_l * 64)) AND (57 = (91 * 66)))
) T2(e_l_r, b_r_r)
on (61 > e_l_r)
) T1
union all
select e, c
from (
Select e, c
from p3
where (a < ((a - d) + (99 - e)))
) T2
) T1(c_l_l, b_r_r_l)
inner join (
Select e, c, a, d
from p5
where ((b = (a * e)) OR ((d < 46) OR (15 > c)))
) T2(e_r, c_r, a_r, d_r)
on (((e_r + c_l_l) = 61) OR ((13 = 3) AND (b_r_r_l = 43)))
) T1(c_l_l_l, b_r_r_l_l, e_r_l)
inner join (
Select d
from p3
where (84 = c)
) T2(d_r)
on (53 < c_l_l_l)
) T2(c_l_l_l_r, e_r_l_r, d_r_r)
on ((e_l + (17 * d_r_r)) = d_l)
) T2(e_l_r, d_l_r, d_r_r_r)
on (b_l = d_l_r)
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
Select b_l, a_l_r
from (
Select c, a, b
from p2
where (14 = 76)
) T1(c_l, a_l, b_l)
left join (
Select a_l, c_r
from (
Select a
from p3
where (c < (((98 * c) * (d * a)) - 6))
) T1(a_l)
left join (
Select c
from p4
where (38 = 88)
) T2(c_r)
on (87 = c_r)
) T2(a_l_r, c_r_r)
on (28 = 5)
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
Select a_l_l, c_r_r_l, b_l_l, b_r
from (
Select a_l, b_l, d_r_r, c_r_r, b_l_r
from (
Select a, b
from p4
where (9 > 23)
) T1(a_l, b_l)
inner join (
Select b_l, c_r, b_r, d_r
from (
Select b
from p2
where ((b * d) < 17)
) T1(b_l)
inner join (
Select c, b, d
from p1
where (d > b)
) T2(c_r, b_r, d_r)
on (b_l = 91)
) T2(b_l_r, c_r_r, b_r_r, d_r_r)
on ((b_l_r < 76) OR (66 < (a_l - a_l)))
) T1(a_l_l, b_l_l, d_r_r_l, c_r_r_l, b_l_r_l)
inner join (
Select b
from p3
where (29 = d)
) T2(b_r)
on (82 > 84)
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
Select a_l_l_l, d_r_l_l, c_r_l, b_r_r, c_r_r_r_l_r
from (
Select a_l_l, b_r_l, d_r_l, c_r
from (
Select a_l, e_r, b_r, d_r
from (
Select a, d
from p2
where (86 < e)
) T1(a_l, d_l)
left join (
Select e, b, d
from p4
where (38 < 26)
) T2(e_r, b_r, d_r)
on ((3 > 55) AND ((3 < a_l) AND (65 < a_l)))
) T1(a_l_l, e_r_l, b_r_l, d_r_l)
full join (
Select e, c, a
from p2
where ((b - c) = a)
) T2(e_r, c_r, a_r)
on ((d_r_l + c_r) < (45 - 96))
) T1(a_l_l_l, b_r_l_l, d_r_l_l, c_r_l)
inner join (
Select e_r_l_l, c_r_r_r_l, b_r
from (
Select a_l_l, e_r_l, a_l_r, c_r_r_r
from (
select a_l, e_r
from (
Select a_l, e_r
from (
Select a
from p2
where (e > a)
) T1(a_l)
inner join (
Select e
from p2
where ((b > (83 - 6)) AND (15 < 93))
) T2(e_r)
on (24 < (25 * e_r))
) T1
union all
select a, d
from (
Select a, d
from p5
where ((74 - 80) < (d - a))
) T2
) T1(a_l_l, e_r_l)
inner join (
Select a_l, e_l_r, c_r_r
from (
Select e, a
from p2
where (34 = (c - 44))
) T1(e_l, a_l)
left join (
Select e_l, a_l, d_l, c_r
from (
Select e, a, d
from p3
where (81 = a)
) T1(e_l, a_l, d_l)
inner join (
Select e, c, d
from p1
where (48 = e)
) T2(e_r, c_r, d_r)
on (a_l < 9)
) T2(e_l_r, a_l_r, d_l_r, c_r_r)
on (99 = e_l_r)
) T2(a_l_r, e_l_r_r, c_r_r_r)
on ((a_l_r + (76 + 20)) > 82)
) T1(a_l_l_l, e_r_l_l, a_l_r_l, c_r_r_r_l)
left join (
Select b
from p2
where ((16 < (d * c)) OR (a = (b + e)))
) T2(b_r)
on ((13 > 67) OR (c_r_r_r_l > 90))
) T2(e_r_l_l_r, c_r_r_r_l_r, b_r_r)
on (a_l_l_l > 5)
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
Select b_l_l, e_r, c_r
from (
Select b_l, e_r
from (
Select b
from p1
where ((b = e) AND (c = a))
) T1(b_l)
inner join (
Select e, c, b
from p2
where (98 = a)
) T2(e_r, c_r, b_r)
on (e_r < ((e_r - 44) - b_l))
) T1(b_l_l, e_r_l)
left join (
Select e, c, a
from p5
where ((60 * 8) > d)
) T2(e_r, c_r, a_r)
on ((b_l_l = 24) OR (c_r > (23 - (e_r + c_r))))
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
Select c_l_l, a_r_l, c_r, d_r
from (
Select c_l, a_r, b_r
from (
Select c
from p4
where ((28 = (a * c)) AND ((46 * b) = (d + a)))
) T1(c_l)
full join (
Select a, b
from p1
where ((90 < 46) OR (99 < b))
) T2(a_r, b_r)
on ((21 = 82) OR (((c_l - c_l) = 48) OR (((a_r * 27) * 36) < b_r)))
) T1(c_l_l, a_r_l, b_r_l)
full join (
Select c, d
from p3
where ((e > b) OR ((a < 87) AND ((a = e) AND (63 < (d + 37)))))
) T2(c_r, d_r)
on ((d_r = 97) AND (70 < 64))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_l, e_l_l, c_r_r_l, b_r
from (
Select e_l, a_l, c_r_r
from (
Select e, a, b
from p2
where ((23 = a) OR (99 = e))
) T1(e_l, a_l, b_l)
inner join (
Select a_l, c_r
from (
Select a
from p1
where (a = 62)
) T1(a_l)
left join (
Select e, c
from p2
where (((b + 76) * e) > (23 + c))
) T2(e_r, c_r)
on (a_l < a_l)
) T2(a_l_r, c_r_r)
on (a_l > c_r_r)
) T1(e_l_l, a_l_l, c_r_r_l)
inner join (
Select c, a, b
from p1
where ((14 - 99) = 50)
) T2(c_r, a_r, b_r)
on ((a_l_l > a_l_l) AND (97 > 72))
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
    #**********************************************
    _testmgr.testcase_end(desc)

