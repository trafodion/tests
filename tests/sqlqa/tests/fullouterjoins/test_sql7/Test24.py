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
    
def test001(desc="""Joins Set 24"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l, b_r
from (
Select c, b
from p4
where (((58 + e) < (c - 81)) OR ((46 = d) OR ((a - c) = 35)))
) T1(c_l, b_l)
left join (
select b
from (
Select b
from p5
where (d = (c * 15))
) T1
union all
select c
from (
Select c, a
from p4
where (b < a)
) T2
) T2(b_r)
on (((c_l + (b_l * b_l)) - c_l) = 79)
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
Select c_l, a_r_r
from (
Select c, d
from p4
where ((23 * (6 * 10)) = b)
) T1(c_l, d_l)
left join (
select e_l, a_r
from (
Select e_l, a_r
from (
Select e, c, d
from p1
where ((80 + 64) = 98)
) T1(e_l, c_l, d_l)
full join (
Select a
from p3
where ((0 < c) OR ((b = 78) OR (e > a)))
) T2(a_r)
on ((e_l = e_l) OR ((40 = (a_r - 39)) OR (25 < 4)))
) T1
union all
select a, b
from (
Select a, b, d
from p1
where ((c > (c - b)) AND (b = b))
) T2
) T2(e_l_r, a_r_r)
on (94 = 14)
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
Select e_l, e_r
from (
Select e, c, b
from p4
where ((e - (18 * 65)) = b)
) T1(e_l, c_l, b_l)
full join (
Select e, d
from p5
where (33 < b)
) T2(e_r, d_r)
on (e_l = e_r)
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
Select b_l_l, e_r_l, e_r, d_r
from (
Select b_l, e_r
from (
Select a, b
from p4
where (11 > b)
) T1(a_l, b_l)
full join (
Select e
from p3
where ((77 > (c + c)) AND ((47 * 89) < (93 * e)))
) T2(e_r)
on ((b_l = b_l) AND (78 > b_l))
) T1(b_l_l, e_r_l)
inner join (
Select e, d
from p5
where (c = 50)
) T2(e_r, d_r)
on (e_r_l < e_r)
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
Select e_l, e_l_r
from (
Select e, c
from p3
where ((75 - e) > (46 - 11))
) T1(e_l, c_l)
left join (
Select e_l, d_r
from (
Select e, a, d
from p4
where ((c = 64) OR (a = 41))
) T1(e_l, a_l, d_l)
left join (
Select c, a, d
from p2
where (c = 20)
) T2(c_r, a_r, d_r)
on (d_r = d_r)
) T2(e_l_r, d_r_r)
on ((e_l_r + ((e_l + (((e_l_r - 16) * 88) + e_l_r)) * 88)) > e_l_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_l, b_r_l, e_r, c_r
from (
Select c_l, b_r
from (
select c
from (
Select c, d
from p5
where (d < b)
) T1
union all
select a
from (
Select a
from p4
where ((69 * c) < (15 + 16))
) T2
) T1(c_l)
full join (
Select c, a, b
from p5
where (24 = e)
) T2(c_r, a_r, b_r)
on (c_l > c_l)
) T1(c_l_l, b_r_l)
left join (
select e, c
from (
Select e, c
from p2
where ((a = c) AND ((28 = 70) OR (94 = (e * 93))))
) T1
union all
select d_r_l, c_r_l
from (
Select d_r_l, c_r_l, c_l_r, a_r_r
from (
Select d_r_l_l, c_r, d_r
from (
select d_r_l
from (
Select d_r_l, e_r_r
from (
Select e_l, a_l, d_r
from (
Select e, a
from p3
where (45 > d)
) T1(e_l, a_l)
left join (
Select d
from p1
where (14 < 93)
) T2(d_r)
on ((d_r = 18) AND ((50 = a_l) OR (50 < d_r)))
) T1(e_l_l, a_l_l, d_r_l)
left join (
Select c_l, e_r, c_r
from (
Select c, b, d
from p2
where (e < (b + b))
) T1(c_l, b_l, d_l)
left join (
Select e, c, d
from p3
where (11 < 7)
) T2(e_r, c_r, d_r)
on ((e_r > c_l) OR (e_r = e_r))
) T2(c_l_r, e_r_r, c_r_r)
on (d_r_l = 55)
) T1
union all
select c
from (
Select c
from p4
where ((b = d) OR (19 < e))
) T2
) T1(d_r_l_l)
left join (
Select c, d
from p3
where (a < (20 * e))
) T2(c_r, d_r)
on ((75 > c_r) OR (28 > d_r_l_l))
) T1(d_r_l_l_l, c_r_l, d_r_l)
full join (
Select c_l, a_r
from (
Select c, a
from p5
where (20 = b)
) T1(c_l, a_l)
left join (
Select c, a
from p3
where (43 < 59)
) T2(c_r, a_r)
on (9 = a_r)
) T2(c_l_r, a_r_r)
on ((a_r_r - d_r_l) = 77)
) T2
) T2(e_r, c_r)
on (b_r_l = c_r)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, a_r
from (
Select e, d
from p4
where (2 < a)
) T1(e_l, d_l)
left join (
Select a
from p4
where (b < (e * 85))
) T2(a_r)
on (54 > 63)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l_l, a_r
from (
Select b_l, d_r
from (
select c, b
from (
Select c, b
from p3
where (29 > c)
) T1
union all
select b, d
from (
select b, d
from (
Select b, d
from p1
where (7 < e)
) T1
union all
select e, a
from (
Select e, a
from p1
where (a = b)
) T2
) T2
) T1(c_l, b_l)
full join (
select a, d
from (
Select a, d
from p4
where ((65 > (((94 * d) - (53 * 63)) * (35 + b))) AND (c = 57))
) T1
union all
select c, d
from (
Select c, d
from p5
where (59 < ((c + c) - c))
) T2
) T2(a_r, d_r)
on ((d_r * b_l) < (((b_l - 97) * d_r) - d_r))
) T1(b_l_l, d_r_l)
left join (
Select a
from p3
where (64 = (a * 6))
) T2(a_r)
on ((8 > 96) OR ((46 > 26) AND ((a_r > b_l_l) AND (66 < 40))))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_l, e_r_l, e_r, c_r
from (
Select c_l, b_l, e_r, c_r
from (
Select e, c, b
from p5
where (1 < (44 - (89 * (77 * (85 * d)))))
) T1(e_l, c_l, b_l)
full join (
Select e, c
from p2
where ((6 * a) = (70 * 0))
) T2(e_r, c_r)
on (((32 + c_r) > b_l) AND (6 > 72))
) T1(c_l_l, b_l_l, e_r_l, c_r_l)
left join (
Select e, c, b
from p3
where (d < e)
) T2(e_r, c_r, b_r)
on ((6 < c_l_l) OR (((((c_r - c_l_l) * c_l_l) - c_l_l) < 3) OR ((e_r_l * 58) = e_r_l)))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, c_l, a_l, c_r
from (
Select e, c, a, d
from p4
where (74 = (a + 79))
) T1(e_l, c_l, a_l, d_l)
full join (
Select c, d
from p4
where ((b + 61) > b)
) T2(c_r, d_r)
on (70 < ((((5 - a_l) + c_l) + (c_r * 44)) - 74))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_l, a_r_r_l, a_r_r_r, d_l_r_r
from (
Select a_l, c_l_r, a_r_r
from (
Select a, b
from p4
where (d = e)
) T1(a_l, b_l)
inner join (
Select c_l, c_r, a_r
from (
Select e, c
from p3
where ((7 = 58) OR ((27 > b) OR (((b * a) > 61) OR (10 > 38))))
) T1(e_l, c_l)
full join (
select c, a
from (
select c, a
from (
Select c, a
from p5
where ((b = 68) AND (e < 19))
) T1
union all
select e_l, a_r
from (
Select e_l, a_r
from (
Select e
from p3
where (29 = 22)
) T1(e_l)
left join (
Select a, b
from p3
where (79 > c)
) T2(a_r, b_r)
on (60 = 14)
) T2
) T1
union all
select e, a
from (
Select e, a
from p1
where (31 = d)
) T2
) T2(c_r, a_r)
on (((76 - 51) > 35) AND (((77 * 15) - 74) = 10))
) T2(c_l_r, c_r_r, a_r_r)
on (63 = c_l_r)
) T1(a_l_l, c_l_r_l, a_r_r_l)
left join (
Select c_l, a_r_r, b_l_r, d_l_r
from (
Select c
from p1
where (13 = 59)
) T1(c_l)
inner join (
Select b_l, d_l, a_r
from (
Select c, b, d
from p4
where (20 > c)
) T1(c_l, b_l, d_l)
left join (
Select c, a
from p5
where (((e * c) = 42) OR (12 = 9))
) T2(c_r, a_r)
on ((99 + 80) = 50)
) T2(b_l_r, d_l_r, a_r_r)
on ((74 + c_l) = c_l)
) T2(c_l_r, a_r_r_r, b_l_r_r, d_l_r_r)
on (42 > a_r_r_r)
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
Select b_l_l, e_r, a_r
from (
Select b_l, d_l, b_l_l_r, c_r_r
from (
select b, d
from (
Select b, d
from p2
where (((57 - a) = 98) OR (8 > d))
) T1
union all
select e, c
from (
Select e, c, b, d
from p3
where (d = 69)
) T2
) T1(b_l, d_l)
left join (
Select c_r_l, b_l_l, e_r, c_r
from (
Select b_l, c_r
from (
select b
from (
Select b, d
from p1
where ((d = 57) AND ((72 = b) OR (35 = (b + 25))))
) T1
union all
select a
from (
Select a
from p3
where ((b > (57 * e)) AND (((53 - (d - (60 - c))) * 86) > 7))
) T2
) T1(b_l)
inner join (
Select c, b
from p5
where (e > b)
) T2(c_r, b_r)
on ((89 * 89) = 52)
) T1(b_l_l, c_r_l)
inner join (
Select e, c
from p2
where ((e - b) > b)
) T2(e_r, c_r)
on (((68 * e_r) > 22) OR (c_r_l < 68))
) T2(c_r_l_r, b_l_l_r, e_r_r, c_r_r)
on ((29 < (23 - 92)) AND (b_l < 59))
) T1(b_l_l, d_l_l, b_l_l_r_l, c_r_r_l)
left join (
select e, a
from (
Select e, a
from p4
where ((97 + a) > e)
) T1
union all
select a, b
from (
Select a, b
from p4
where (8 < ((c * c) - 87))
) T2
) T2(e_r, a_r)
on ((a_r + a_r) < a_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l_l_l, c_r_l_l, e_l_r_r
from (
select c_r_l, b_l_l
from (
Select c_r_l, b_l_l, e_r, c_r
from (
Select b_l, c_r
from (
Select b
from p4
where (82 < d)
) T1(b_l)
left join (
Select c, a, b
from p1
where (a = 48)
) T2(c_r, a_r, b_r)
on ((89 < b_l) OR ((94 > (9 * 68)) OR (((c_r * 12) < (81 - c_r)) AND (b_l > c_r))))
) T1(b_l_l, c_r_l)
full join (
Select e, c
from p2
where ((e > 86) OR ((8 + 38) = d))
) T2(e_r, c_r)
on (42 < 65)
) T1
union all
select e, c
from (
Select e, c
from p3
where (91 = 8)
) T2
) T1(c_r_l_l, b_l_l_l)
left join (
select a_l, e_l_r
from (
Select a_l, e_l_r, e_r_r
from (
Select a
from p1
where ((63 = (((20 - (21 + 73)) - a) - (96 * e))) OR (a < c))
) T1(a_l)
left join (
Select e_l, d_l, e_r, c_r
from (
Select e, d
from p3
where (d > c)
) T1(e_l, d_l)
inner join (
select e, c
from (
Select e, c, b
from p5
where (((55 * a) * e) = 19)
) T1
union all
select b_l, c_r
from (
Select b_l, c_r
from (
Select b
from p2
where (c > 67)
) T1(b_l)
left join (
Select c, a
from p2
where (d = b)
) T2(c_r, a_r)
on (((b_l - c_r) = ((69 * (44 * 35)) - 44)) AND ((36 - (43 * ((9 + 64) * 75))) > 79))
) T2
) T2(e_r, c_r)
on (e_l > (6 + c_r))
) T2(e_l_r, d_l_r, e_r_r, c_r_r)
on (52 < a_l)
) T1
union all
select c, a
from (
Select c, a
from p2
where ((d > 96) OR (c > (a - (22 - b))))
) T2
) T2(a_l_r, e_l_r_r)
on ((c_r_l_l = 3) OR (13 = 63))
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
Select c_l, c_l_l_r
from (
Select c
from p2
where (d < 65)
) T1(c_l)
inner join (
select c_l_l
from (
Select c_l_l, e_l_l, e_l_r
from (
Select e_l, c_l, b_l, c_r, b_r
from (
Select e, c, b
from p5
where (a > b)
) T1(e_l, c_l, b_l)
left join (
Select c, a, b
from p5
where (e = c)
) T2(c_r, a_r, b_r)
on (21 < (6 + 57))
) T1(e_l_l, c_l_l, b_l_l, c_r_l, b_r_l)
left join (
Select e_l, c_r, a_r
from (
Select e
from p3
where ((b + (b + 28)) > (c * 26))
) T1(e_l)
left join (
Select e, c, a
from p1
where (31 < (e * 53))
) T2(e_r, c_r, a_r)
on ((e_l = c_r) AND (c_r = 49))
) T2(e_l_r, c_r_r, a_r_r)
on (54 > e_l_r)
) T1
union all
select d
from (
Select d
from p1
where (a > 57)
) T2
) T2(c_l_l_r)
on (c_l_l_r = 87)
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
Select b_l, d_r
from (
Select e, b
from p2
where (34 > 28)
) T1(e_l, b_l)
full join (
Select c, a, d
from p4
where (65 < (6 + 53))
) T2(c_r, a_r, d_r)
on (29 < 15)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, a_r
from (
Select a, b, d
from p5
where ((6 * 89) < d)
) T1(a_l, b_l, d_l)
inner join (
Select a
from p3
where (a = 38)
) T2(a_r)
on ((66 + (25 - (20 - 63))) < a_r)
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
Select e_l_l, c_r_l, e_r, b_r
from (
Select e_l, c_r, d_r
from (
select e
from (
Select e
from p1
where ((c < 91) OR ((a - 8) = 46))
) T1
union all
select c
from (
Select c, a, d
from p1
where ((b * 38) = 66)
) T2
) T1(e_l)
left join (
Select c, a, d
from p3
where (b = 86)
) T2(c_r, a_r, d_r)
on ((e_l < c_r) OR (e_l < 82))
) T1(e_l_l, c_r_l, d_r_l)
left join (
Select e, b, d
from p4
where ((b = e) OR ((52 < 52) OR (b = 26)))
) T2(e_r, b_r, d_r)
on (e_r > 41)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, c_l_r, e_l_r, d_r_r
from (
Select e, b, d
from p2
where (84 > 91)
) T1(e_l, b_l, d_l)
left join (
Select e_l, c_l, b_r, d_r
from (
select e, c
from (
Select e, c, a, d
from p1
where (c > a)
) T1
union all
select b_l, b_r_r
from (
Select b_l, b_r_r
from (
select b
from (
Select b
from p2
where ((c = a) AND ((49 > 79) AND ((d + c) > b)))
) T1
union all
select d_l
from (
select d_l
from (
Select d_l, d_l_r
from (
Select d
from p2
where (b < 98)
) T1(d_l)
inner join (
Select a_l, d_l, c_r
from (
Select a, b, d
from p1
where (41 > (c * e))
) T1(a_l, b_l, d_l)
left join (
Select c
from p5
where (18 = 72)
) T2(c_r)
on (a_l < 42)
) T2(a_l_r, d_l_r, c_r_r)
on ((83 < (d_l * 83)) AND ((50 * d_l) < 32))
) T1
union all
select c
from (
Select c
from p4
where ((c = 75) OR (12 = 62))
) T2
) T2
) T1(b_l)
left join (
Select b_l, b_r, d_r
from (
Select b
from p3
where ((9 = 30) OR (17 = d))
) T1(b_l)
left join (
select b, d
from (
Select b, d
from p4
where (33 > (64 - 30))
) T1
union all
select c, d
from (
Select c, d
from p2
where ((b - 48) = 81)
) T2
) T2(b_r, d_r)
on ((23 = b_l) OR ((d_r * 22) = (36 - 48)))
) T2(b_l_r, b_r_r, d_r_r)
on (96 = 54)
) T2
) T1(e_l, c_l)
left join (
Select e, b, d
from p3
where ((62 < (b + 32)) OR (54 = (((e + d) * (b + b)) + 63)))
) T2(e_r, b_r, d_r)
on (72 > c_l)
) T2(e_l_r, c_l_r, b_r_r, d_r_r)
on (c_l_r < e_l)
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
Select b_r_l, a_l_r, a_r_r
from (
Select d_l_l, b_r
from (
Select b_l, d_l, b_l_r
from (
Select e, c, b, d
from p4
where (74 > a)
) T1(e_l, c_l, b_l, d_l)
full join (
select b_l
from (
select b_l
from (
Select b_l, a_r
from (
select b
from (
Select b
from p4
where (6 = ((41 - (76 - 60)) + 61))
) T1
union all
select d_l
from (
Select d_l, a_r
from (
Select c, d
from p2
where (a > (c - a))
) T1(c_l, d_l)
full join (
Select a, d
from p3
where ((e = 95) OR ((39 = (c + d)) AND ((b + 31) < (47 + (93 * e)))))
) T2(a_r, d_r)
on ((95 > 37) AND ((5 > (27 + a_r)) AND (64 > a_r)))
) T2
) T1(b_l)
left join (
Select a
from p1
where (c < 71)
) T2(a_r)
on (1 = a_r)
) T1
union all
select b_l
from (
select b_l
from (
Select b_l, d_r_l_l_l_r, e_r_r
from (
Select b
from p1
where (48 > d)
) T1(b_l)
left join (
Select d_r_l_l_l, e_r
from (
Select d_r_l_l, a_r, b_r
from (
Select d_r_l, b_l_l, d_r_l_r_l_l_r, d_r_r
from (
Select b_l, d_r
from (
select b
from (
Select b
from p4
where (b < c)
) T1
union all
select e_l
from (
Select e_l, b_r
from (
select e
from (
Select e
from p5
where (69 = a)
) T1
union all
select c_l
from (
Select c_l, a_r
from (
Select c
from p5
where (b < 68)
) T1(c_l)
left join (
Select e, a, b, d
from p2
where ((d = c) OR ((b = e) AND (a < (c + 61))))
) T2(e_r, a_r, b_r, d_r)
on ((49 * ((85 - a_r) + c_l)) < a_r)
) T2
) T1(e_l)
full join (
Select e, a, b
from p3
where ((92 + 21) > a)
) T2(e_r, a_r, b_r)
on ((e_l > 43) AND ((14 + (((e_l - b_r) * e_l) * e_l)) = 84))
) T2
) T1(b_l)
full join (
Select c, a, d
from p4
where (33 > (d + (((27 - (57 + (7 + ((12 - 26) - a)))) * b) * 64)))
) T2(c_r, a_r, d_r)
on (72 > d_r)
) T1(b_l_l, d_r_l)
inner join (
Select d_r_l_r_l_l, d_r
from (
Select d_r_l_r_l, d_l_l, a_l_r, e_r_r
from (
Select a_l, d_l, d_r_l_r, a_r_l_r
from (
Select c, a, d
from p3
where (a = a)
) T1(c_l, a_l, d_l)
inner join (
Select d_r_l, a_r_l, a_r
from (
Select b_l_l, a_r, d_r
from (
Select b_l, c_l_r, e_r_r
from (
Select c, b, d
from p1
where (e = 6)
) T1(c_l, b_l, d_l)
left join (
Select c_l, d_l, e_r
from (
Select c, b, d
from p3
where (b > e)
) T1(c_l, b_l, d_l)
left join (
Select e
from p4
where ((88 - 80) < (e + 61))
) T2(e_r)
on (67 = 3)
) T2(c_l_r, d_l_r, e_r_r)
on (((85 + b_l) * 36) = 71)
) T1(b_l_l, c_l_r_l, e_r_r_l)
left join (
Select a, d
from p3
where (d = 11)
) T2(a_r, d_r)
on ((97 < b_l_l) AND (a_r = (b_l_l + (60 - b_l_l))))
) T1(b_l_l_l, a_r_l, d_r_l)
left join (
Select e, a
from p1
where (((93 - 85) + 7) < 37)
) T2(e_r, a_r)
on ((75 = a_r) AND ((97 < 16) AND ((4 = (a_r_l - 9)) AND (a_r = (d_r_l + a_r)))))
) T2(d_r_l_r, a_r_l_r, a_r_r)
on ((23 < (a_l * 76)) OR (a_l = 49))
) T1(a_l_l, d_l_l, d_r_l_r_l, a_r_l_r_l)
left join (
Select a_l, e_r
from (
select a, b
from (
Select a, b, d
from p5
where (d > b)
) T1
union all
select e, c
from (
Select e, c
from p1
where (30 < 48)
) T2
) T1(a_l, b_l)
left join (
select e
from (
Select e
from p2
where (d < (a + (5 - 13)))
) T1
union all
select e_l
from (
select e_l, a_l
from (
Select e_l, a_l, d_l, e_r
from (
Select e, a, d
from p2
where ((c = e) OR (6 = c))
) T1(e_l, a_l, d_l)
full join (
Select e
from p3
where (14 = e)
) T2(e_r)
on ((5 = (82 - e_r)) OR ((a_l < a_l) AND ((61 - 42) > d_l)))
) T1
union all
select d_l, d_r
from (
Select d_l, d_r
from (
Select a, d
from p1
where (24 < 35)
) T1(a_l, d_l)
left join (
Select c, a, d
from p1
where ((b * 50) > ((31 - b) - b))
) T2(c_r, a_r, d_r)
on (d_l = 55)
) T2
) T2
) T2(e_r)
on ((34 > 38) AND (a_l < e_r))
) T2(a_l_r, e_r_r)
on (13 = 8)
) T1(d_r_l_r_l_l, d_l_l_l, a_l_r_l, e_r_r_l)
inner join (
Select d
from p1
where ((a = 23) AND (e = 71))
) T2(d_r)
on (84 = d_r)
) T2(d_r_l_r_l_l_r, d_r_r)
on (d_r_l_r_l_l_r = 44)
) T1(d_r_l_l, b_l_l_l, d_r_l_r_l_l_r_l, d_r_r_l)
left join (
Select a, b
from p2
where (c = a)
) T2(a_r, b_r)
on ((41 = 88) AND (b_r = (((d_r_l_l * a_r) - 70) + a_r)))
) T1(d_r_l_l_l, a_r_l, b_r_l)
full join (
Select e
from p5
where (66 > 96)
) T2(e_r)
on (29 < d_r_l_l_l)
) T2(d_r_l_l_l_r, e_r_r)
on ((91 = (e_r_r * ((b_l + 86) - 69))) AND ((e_r_r > d_r_l_l_l_r) AND ((b_l > 56) AND (23 < b_l))))
) T1
union all
select a
from (
Select a
from p3
where (62 < a)
) T2
) T2
) T1
union all
select c
from (
Select c, b
from p2
where ((14 + e) = 9)
) T2
) T2(b_l_r)
on (47 < b_l)
) T1(b_l_l, d_l_l, b_l_r_l)
left join (
Select b
from p2
where ((69 * d) = (11 + 66))
) T2(b_r)
on ((1 = d_l_l) OR (15 > (b_r * 15)))
) T1(d_l_l_l, b_r_l)
left join (
Select a_l, a_r
from (
Select c, a
from p1
where ((18 < 58) AND (e > 74))
) T1(c_l, a_l)
left join (
Select a, b
from p1
where ((a > d) AND ((c < (86 + 97)) OR ((c + c) < a)))
) T2(a_r, b_r)
on (a_l = 48)
) T2(a_l_r, a_r_r)
on (a_r_r = a_l_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, b_r
from (
Select d
from p2
where (24 > a)
) T1(d_l)
left join (
Select b
from p4
where (b = b)
) T2(b_r)
on (d_l = (14 + 1))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #********************************************
    _testmgr.testcase_end(desc)

