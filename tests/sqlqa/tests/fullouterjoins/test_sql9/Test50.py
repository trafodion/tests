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
    
def test001(desc="""Joins Set 50"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l_l, b_r_l_r_r
from (
Select e_l, a_r, b_r
from (
select e
from (
Select e, b, d
from p1
where ((c = 80) OR (45 = 82))
) T1
union all
select c
from (
Select c
from p4
where (2 = 14)
) T2
) T1(e_l)
left join (
Select e, a, b, d
from p3
where (a < 11)
) T2(e_r, a_r, b_r, d_r)
on ((e_l < (e_l - b_r)) AND (a_r = 96))
) T1(e_l_l, a_r_l, b_r_l)
left join (
Select a_l, b_r_r, b_r_l_r
from (
Select a, b
from p1
where (((76 * (26 * c)) + a) = 50)
) T1(a_l, b_l)
inner join (
Select b_r_l, c_r, b_r
from (
Select c_l, b_l, b_r
from (
Select c, b
from p5
where (82 = 52)
) T1(c_l, b_l)
full join (
Select e, b
from p3
where (e = (c - b))
) T2(e_r, b_r)
on ((c_l = b_r) AND (((53 * 28) = 69) AND (c_l = (30 * (b_r * 54)))))
) T1(c_l_l, b_l_l, b_r_l)
left join (
Select c, b
from p5
where (96 = 71)
) T2(c_r, b_r)
on (99 < b_r)
) T2(b_r_l_r, c_r_r, b_r_r)
on (((b_r_l_r * 97) = b_r_r) AND (b_r_r > a_l))
) T2(a_l_r, b_r_r_r, b_r_l_r_r)
on (64 = 27)
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
Select b_r_l, e_l_l, e_l_l_l_r, d_r_l_r
from (
Select e_l, b_l, b_r
from (
Select e, b
from p5
where (((((b * a) + (82 - c)) * ((((94 * (e + 19)) + a) * 73) * d)) < 80) OR (a > (a - (22 * (e + 15)))))
) T1(e_l, b_l)
inner join (
Select a, b
from p1
where ((55 = c) AND (d = 81))
) T2(a_r, b_r)
on (65 = 68)
) T1(e_l_l, b_l_l, b_r_l)
left join (
Select d_r_l, e_l_l_l, a_l_r
from (
Select e_l_l, e_r_l, d_r
from (
Select e_l, a_l, d_l, e_r
from (
Select e, a, d
from p1
where ((89 = 57) OR ((a = 69) AND ((((c + 85) + 45) = 96) AND (a = 20))))
) T1(e_l, a_l, d_l)
inner join (
Select e
from p5
where (((c + 58) = 38) OR (22 < 44))
) T2(e_r)
on ((78 = a_l) AND (e_r > a_l))
) T1(e_l_l, a_l_l, d_l_l, e_r_l)
left join (
Select d
from p3
where ((20 - (b + 42)) = 28)
) T2(d_r)
on ((e_r_l = e_l_l) OR (((d_r * e_l_l) > 2) OR (85 < 7)))
) T1(e_l_l_l, e_r_l_l, d_r_l)
inner join (
Select a_l, d_l, c_r, b_r
from (
Select e, a, d
from p1
where (6 > a)
) T1(e_l, a_l, d_l)
full join (
Select c, a, b
from p1
where (62 < a)
) T2(c_r, a_r, b_r)
on ((a_l = d_l) OR ((c_r * c_r) = (c_r * d_l)))
) T2(a_l_r, d_l_r, c_r_r, b_r_r)
on ((d_r_l * a_l_r) < 10)
) T2(d_r_l_r, e_l_l_l_r, a_l_r_r)
on (d_r_l_r = 65)
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
Select d_l, a_r
from (
Select d
from p3
where (41 < e)
) T1(d_l)
inner join (
Select a, b, d
from p3
where (30 < 19)
) T2(a_r, b_r, d_r)
on (a_r = a_r)
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
Select d_r_l, c_r
from (
Select b_l, d_r
from (
Select b
from p4
where (((c - 80) = 78) OR (86 = (b * 90)))
) T1(b_l)
inner join (
Select d
from p3
where ((48 = ((63 - 39) + e)) OR ((77 = b) AND (23 = b)))
) T2(d_r)
on (b_l = 95)
) T1(b_l_l, d_r_l)
left join (
Select e, c, b, d
from p5
where (80 = a)
) T2(e_r, c_r, b_r, d_r)
on (c_r < c_r)
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
Select a_l_l, d_l_l_r_l, b_l_l, a_r
from (
Select a_l, b_l, b_r_r, d_l_l_r
from (
Select c, a, b
from p2
where (33 = 54)
) T1(c_l, a_l, b_l)
left join (
Select d_l_l, b_r
from (
Select d_l, e_l_r
from (
Select e, c, d
from p2
where ((b = c) AND (36 = e))
) T1(e_l, c_l, d_l)
left join (
Select e_l, a_l, a_l_r
from (
Select e, a
from p2
where (68 = e)
) T1(e_l, a_l)
left join (
Select a_l, d_r
from (
Select a
from p1
where (78 = 88)
) T1(a_l)
left join (
Select e, b, d
from p4
where (44 = 70)
) T2(e_r, b_r, d_r)
on ((a_l > 95) AND (((44 + (d_r + a_l)) = (a_l * d_r)) AND (((d_r - 43) = 43) AND ((64 < d_r) OR (d_r = a_l)))))
) T2(a_l_r, d_r_r)
on (38 = ((21 - 74) * a_l_r))
) T2(e_l_r, a_l_r, a_l_r_r)
on (e_l_r < e_l_r)
) T1(d_l_l, e_l_r_l)
left join (
Select b
from p4
where ((b = a) OR (95 < (95 - 69)))
) T2(b_r)
on (d_l_l > (82 + (64 * d_l_l)))
) T2(d_l_l_r, b_r_r)
on ((11 > 88) AND (83 = 7))
) T1(a_l_l, b_l_l, b_r_r_l, d_l_l_r_l)
full join (
Select a
from p3
where (99 < b)
) T2(a_r)
on ((82 = b_l_l) OR (a_l_l = 68))
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
Select e_l_l, c_r_l, e_r, a_r, b_r
from (
Select e_l, c_r
from (
Select e, b
from p5
where (b = (90 + 29))
) T1(e_l, b_l)
left join (
Select c, d
from p5
where (b = 77)
) T2(c_r, d_r)
on ((32 + 51) = (5 + (e_l - 13)))
) T1(e_l_l, c_r_l)
left join (
Select e, a, b, d
from p2
where ((e * 53) < c)
) T2(e_r, a_r, b_r, d_r)
on (6 < 77)
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
Select e_r_l_r_r_r_r_l, e_l_r_l, b_r
from (
Select c_r_l, e_l_r, e_r_l_r_r_r_r
from (
Select c_l, a_l, c_r
from (
select e, c, a
from (
Select e, c, a, d
from p1
where (27 = 46)
) T1
union all
select c, b, d
from (
Select c, b, d
from p1
where ((63 = 13) OR ((99 > 52) AND (c < a)))
) T2
) T1(e_l, c_l, a_l)
full join (
select c, d
from (
Select c, d
from p2
where ((47 < a) OR ((28 = c) OR (c = 38)))
) T1
union all
select c_l, e_r
from (
Select c_l, e_r, a_r, b_r
from (
Select c, a
from p2
where ((e = (b * 46)) OR ((b = ((17 * 84) * 50)) AND (e = 51)))
) T1(c_l, a_l)
left join (
Select e, a, b
from p4
where ((c = ((45 + d) + b)) OR (((c * 95) = (57 * d)) OR (81 = (d + 27))))
) T2(e_r, a_r, b_r)
on ((a_r = e_r) AND (53 > 64))
) T2
) T2(c_r, d_r)
on (a_l = 42)
) T1(c_l_l, a_l_l, c_r_l)
inner join (
Select e_l, c_l, a_l_r, e_r_l_r_r_r
from (
Select e, c
from p3
where ((8 < (e + 31)) OR ((83 > 93) AND (((b + 85) < c) OR (88 > e))))
) T1(e_l, c_l)
left join (
Select c_l, a_l, e_r_l_r_r
from (
Select c, a
from p4
where ((b < b) OR ((e - 1) = 49))
) T1(c_l, a_l)
full join (
Select c_l_l_l, c_r_l_r_l_l, e_r_l_r
from (
Select c_l_l, c_r_l_r_l, a_r
from (
Select c_l, b_l, c_r_l_r
from (
Select c, b
from p5
where (62 = 93)
) T1(c_l, b_l)
full join (
Select c_r_l, e_r
from (
Select d_l, c_r
from (
Select d
from p3
where ((b > 69) AND (16 = b))
) T1(d_l)
inner join (
Select e, c, a, d
from p1
where ((b > c) OR (c > b))
) T2(e_r, c_r, a_r, d_r)
on (c_r > 43)
) T1(d_l_l, c_r_l)
left join (
Select e
from p3
where ((c + 67) > a)
) T2(e_r)
on (e_r = 82)
) T2(c_r_l_r, e_r_r)
on (c_l = c_r_l_r)
) T1(c_l_l, b_l_l, c_r_l_r_l)
left join (
Select a
from p3
where ((d = c) AND (10 < c))
) T2(a_r)
on ((71 > a_r) OR ((a_r + (27 - (74 * c_l_l))) > c_l_l))
) T1(c_l_l_l, c_r_l_r_l_l, a_r_l)
inner join (
Select e_l_l, e_r_l, e_r_r
from (
Select e_l, e_r
from (
Select e
from p1
where (c = c)
) T1(e_l)
left join (
Select e
from p5
where (b < 58)
) T2(e_r)
on (e_l < 36)
) T1(e_l_l, e_r_l)
full join (
Select e_l, e_r
from (
Select e
from p1
where ((e = 43) OR ((d = (68 + (74 * b))) AND ((b < 10) AND ((c * 14) > (e * e)))))
) T1(e_l)
inner join (
Select e
from p4
where (e = (b - b))
) T2(e_r)
on ((e_r < ((e_r - e_l) + 71)) AND ((e_l < 75) AND (55 = 97)))
) T2(e_l_r, e_r_r)
on ((e_l_l < 26) OR (82 = (e_l_l * (e_l_l - 97))))
) T2(e_l_l_r, e_r_l_r, e_r_r_r)
on (14 = (e_r_l_r - 79))
) T2(c_l_l_l_r, c_r_l_r_l_l_r, e_r_l_r_r)
on (1 > 54)
) T2(c_l_r, a_l_r, e_r_l_r_r_r)
on ((e_r_l_r_r_r - e_l) = 64)
) T2(e_l_r, c_l_r, a_l_r_r, e_r_l_r_r_r_r)
on ((e_l_r > c_r_l) AND ((e_l_r > 78) AND ((c_r_l = 47) AND (((90 - (60 + (c_r_l * 95))) = c_r_l) AND (c_r_l < e_l_r)))))
) T1(c_r_l_l, e_l_r_l, e_r_l_r_r_r_r_l)
full join (
Select b
from p4
where ((c + (3 - (c + c))) > 99)
) T2(b_r)
on (22 > 67)
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
Select e_r_l_l, d_r_l_r_l, a_l_l_l, a_l_r, e_r_r
from (
select a_l_l, e_r_l, d_r_l_r
from (
select a_l_l, e_r_l, d_r_l_r
from (
Select a_l_l, e_r_l, d_r_l_r
from (
Select a_l, b_l, e_r, d_r
from (
Select a, b
from p1
where ((e * c) = 11)
) T1(a_l, b_l)
left join (
Select e, d
from p1
where (d = 89)
) T2(e_r, d_r)
on (b_l < (41 - 38))
) T1(a_l_l, b_l_l, e_r_l, d_r_l)
full join (
Select d_r_l, a_l_l_l, d_r
from (
select a_l_l, d_r
from (
Select a_l_l, d_r
from (
select a_l, a_r_l_l_r
from (
select a_l, a_r_l_l_r
from (
Select a_l, a_r_l_l_r, a_r_r, c_r_r
from (
Select c, a
from p5
where ((54 > d) AND (e = 67))
) T1(c_l, a_l)
inner join (
Select a_r_l_l, c_r, a_r
from (
Select b_r_l, a_r_l, c_r
from (
Select d_l, e_r, a_r, b_r
from (
Select d
from p1
where (11 < 35)
) T1(d_l)
left join (
Select e, a, b, d
from p2
where (((d * 35) < 26) OR ((10 = d) OR (c = 58)))
) T2(e_r, a_r, b_r, d_r)
on (((b_r + d_l) < 66) OR ((e_r - b_r) = b_r))
) T1(d_l_l, e_r_l, a_r_l, b_r_l)
left join (
Select c
from p5
where (9 = 98)
) T2(c_r)
on ((84 * a_r_l) > a_r_l)
) T1(b_r_l_l, a_r_l_l, c_r_l)
full join (
Select c, a
from p3
where (90 = 72)
) T2(c_r, a_r)
on ((a_r_l_l = 67) OR (38 = c_r))
) T2(a_r_l_l_r, c_r_r, a_r_r)
on (a_r_r = 67)
) T1
union all
select a, b
from (
Select a, b
from p2
where (58 = a)
) T2
) T1
union all
select e_l, b_l
from (
Select e_l, b_l, b_r_r
from (
Select e, b
from p2
where (a > 98)
) T1(e_l, b_l)
left join (
Select e_l_l, d_l_l, b_r, d_r
from (
Select e_l, d_l, a_r_r
from (
Select e, b, d
from p4
where (29 = 75)
) T1(e_l, b_l, d_l)
inner join (
Select e_l, d_l, a_r
from (
Select e, a, d
from p1
where ((((d * b) + (((64 + 48) * 77) - 9)) > b) AND (46 = c))
) T1(e_l, a_l, d_l)
full join (
Select a, d
from p2
where (46 > e)
) T2(a_r, d_r)
on ((a_r = 99) AND (e_l = a_r))
) T2(e_l_r, d_l_r, a_r_r)
on ((a_r_r - (87 - d_l)) = ((31 + d_l) - a_r_r))
) T1(e_l_l, d_l_l, a_r_r_l)
left join (
Select e, b, d
from p5
where ((d = ((57 * 38) * 43)) AND ((8 + 39) < a))
) T2(e_r, b_r, d_r)
on (b_r > b_r)
) T2(e_l_l_r, d_l_l_r, b_r_r, d_r_r)
on (22 = b_r_r)
) T2
) T1(a_l_l, a_r_l_l_r_l)
left join (
Select e, c, d
from p2
where (83 = d)
) T2(e_r, c_r, d_r)
on ((67 * (d_r + d_r)) = 13)
) T1
union all
select e, b
from (
Select e, b
from p2
where (e > c)
) T2
) T1(a_l_l_l, d_r_l)
inner join (
Select a, b, d
from p4
where ((31 < 61) AND (d > (96 - d)))
) T2(a_r, b_r, d_r)
on (a_l_l_l < d_r)
) T2(d_r_l_r, a_l_l_l_r, d_r_r)
on (8 > 28)
) T1
union all
select a_l_l, a_r_r_l, e_r
from (
Select a_l_l, a_r_r_l, e_r
from (
select a_l, a_r_r
from (
Select a_l, a_r_r
from (
Select c, a, b
from p1
where ((b = (41 * d)) OR ((b * d) < ((25 + b) + 16)))
) T1(c_l, a_l, b_l)
left join (
Select e_l, a_r
from (
Select e, d
from p3
where ((43 = ((58 + c) - 1)) AND (c = e))
) T1(e_l, d_l)
left join (
Select a
from p3
where (0 > 47)
) T2(a_r)
on (70 = e_l)
) T2(e_l_r, a_r_r)
on (a_l > a_l)
) T1
union all
select b_r_l_l, c_r_l
from (
Select b_r_l_l, c_r_l, e_r_l, c_r, a_r
from (
Select b_r_l, e_r, c_r
from (
Select a_l, b_r
from (
Select a, d
from p3
where ((a * 63) > (c + 7))
) T1(a_l, d_l)
full join (
Select b
from p4
where (b < 90)
) T2(b_r)
on ((96 + a_l) < a_l)
) T1(a_l_l, b_r_l)
inner join (
Select e, c
from p4
where ((77 < (1 * 37)) AND ((50 < 84) OR ((a < 8) OR (9 > d))))
) T2(e_r, c_r)
on ((53 + e_r) = 10)
) T1(b_r_l_l, e_r_l, c_r_l)
full join (
Select c, a
from p3
where (77 = c)
) T2(c_r, a_r)
on ((5 * 79) > 34)
) T2
) T1(a_l_l, a_r_r_l)
inner join (
Select e
from p3
where (a < d)
) T2(e_r)
on (11 < a_r_r_l)
) T2
) T1
union all
select e_l, a_l, d_l
from (
Select e_l, a_l, d_l, c_r, b_r
from (
Select e, a, d
from p2
where (c = (b * b))
) T1(e_l, a_l, d_l)
full join (
Select c, a, b, d
from p5
where (18 < b)
) T2(c_r, a_r, b_r, d_r)
on (a_l = c_r)
) T2
) T1(a_l_l_l, e_r_l_l, d_r_l_r_l)
left join (
Select a_l, e_r
from (
select a
from (
select a, d
from (
Select a, d
from p1
where (((d * (77 - c)) = b) AND (5 > 17))
) T1
union all
select e, b
from (
Select e, b, d
from p4
where ((a = (a + e)) OR (d = 96))
) T2
) T1
union all
select e
from (
Select e
from p1
where (a = c)
) T2
) T1(a_l)
left join (
Select e
from p5
where (c = a)
) T2(e_r)
on ((a_l - 1) < 42)
) T2(a_l_r, e_r_r)
on (e_r_l_l = d_r_l_r_l)
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test50exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, b_r_r, e_l_r, c_r_r
from (
Select b, d
from p3
where (((81 - ((75 + c) + (e * 37))) = b) OR (29 = e))
) T1(b_l, d_l)
inner join (
Select e_l, c_r, b_r, d_r
from (
Select e, c, d
from p1
where ((e = 35) AND ((74 * b) = 44))
) T1(e_l, c_l, d_l)
left join (
Select c, b, d
from p5
where (a = b)
) T2(c_r, b_r, d_r)
on (((((((c_r + 52) + d_r) - (60 - c_r)) - (51 - 48)) + b_r) - 91) < ((63 + 7) + (10 + 72)))
) T2(e_l_r, c_r_r, b_r_r, d_r_r)
on (67 = (b_l - (70 * (12 * 74))))
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
Select c_r_l, e_l_l_l, a_r, b_r
from (
Select e_l_l, c_r
from (
Select e_l, c_r
from (
Select e
from p4
where ((46 = 9) AND ((e - a) > (d + c)))
) T1(e_l)
full join (
Select c
from p1
where (c = e)
) T2(c_r)
on ((99 - (e_l + e_l)) = (25 + 30))
) T1(e_l_l, c_r_l)
inner join (
Select c, d
from p1
where (a < 94)
) T2(c_r, d_r)
on (30 = 36)
) T1(e_l_l_l, c_r_l)
inner join (
Select a, b
from p1
where (52 = a)
) T2(a_r, b_r)
on (b_r > a_r)
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
Select a_l, d_l, b_r
from (
Select a, d
from p5
where (a = 67)
) T1(a_l, d_l)
left join (
Select e, c, b
from p2
where ((b < e) OR ((22 < 30) AND ((65 - e) > (((b + 58) + (e * 10)) + c))))
) T2(e_r, c_r, b_r)
on (a_l = 98)
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
Select e_l, b_r_r, b_l_r
from (
Select e, a
from p1
where ((36 = 11) AND (b < (c + 51)))
) T1(e_l, a_l)
left join (
Select b_l, b_r
from (
Select b
from p3
where (a = d)
) T1(b_l)
left join (
Select e, b
from p2
where (((d - ((12 * 64) * c)) > (57 * (a - ((38 - a) + a)))) OR (d = 42))
) T2(e_r, b_r)
on ((b_r - (b_r * b_r)) = 69)
) T2(b_l_r, b_r_r)
on ((b_l_r > (77 + (0 - (b_l_r + e_l)))) AND (b_r_r > 83))
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
select e, c
from (
Select e, c
from p4
where ((86 > 16) AND (46 = e))
) T1
union all
select e, c
from (
Select e, c, a
from p1
where (d = 63)
) T2
) T1(e_l, c_l)
left join (
Select e
from p2
where (((70 + d) > 24) OR (c = e))
) T2(e_r)
on (e_l < (10 - e_l))
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
select b
from (
Select b
from p1
where ((59 < 54) AND ((c * 10) = c))
) T1
union all
select e
from (
Select e, b
from p4
where ((a = c) OR ((d - (a * 6)) < b))
) T2
) T1(b_l)
left join (
Select d
from p3
where (a = (d - d))
) T2(d_r)
on ((16 > (24 - d_r)) AND ((d_r * (d_r * (d_r * d_r))) < d_r))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test50exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l_l, e_r
from (
Select c_l, d_l, e_r
from (
Select c, d
from p1
where (a = (b * 10))
) T1(c_l, d_l)
left join (
select e
from (
Select e
from p3
where (((60 * 75) > 80) OR (e = d))
) T1
union all
select b
from (
Select b, d
from p5
where (91 = (72 + (b + 96)))
) T2
) T2(e_r)
on ((65 = 86) OR ((88 - (44 * c_l)) = c_l))
) T1(c_l_l, d_l_l, e_r_l)
left join (
select e
from (
Select e
from p3
where (72 > 93)
) T1
union all
select a
from (
Select a, b, d
from p2
where (((a - (c + b)) = (b + 78)) OR (46 = 88))
) T2
) T2(e_r)
on ((3 < e_r) AND (((e_r - 52) - e_r) > 82))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test50exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_r_l, e_r_r_l_l_l_l, a_r
from (
Select b_r_l, e_r_r_l_l_l, c_r
from (
Select e_r_r_l_l, b_r
from (
Select d_l_l, e_r_r_l, b_r_r, e_l_r
from (
Select c_l, b_l, d_l, d_l_l_r, e_r_l_r, e_r_r
from (
Select e, c, b, d
from p5
where ((20 = (e + e)) AND ((b = 58) OR (b < b)))
) T1(e_l, c_l, b_l, d_l)
inner join (
Select d_l_l, e_r_l, e_r
from (
Select d_l, e_r
from (
Select c, d
from p5
where ((47 * a) > c)
) T1(c_l, d_l)
inner join (
Select e, c, a, d
from p4
where ((31 > e) AND (44 > c))
) T2(e_r, c_r, a_r, d_r)
on (e_r < 11)
) T1(d_l_l, e_r_l)
left join (
Select e, b
from p4
where (e = c)
) T2(e_r, b_r)
on (4 = (13 - e_r))
) T2(d_l_l_r, e_r_l_r, e_r_r)
on ((24 = 15) AND (c_l = 12))
) T1(c_l_l, b_l_l, d_l_l, d_l_l_r_l, e_r_l_r_l, e_r_r_l)
left join (
Select e_l, b_r
from (
Select e
from p2
where ((5 - 90) = a)
) T1(e_l)
inner join (
Select e, c, a, b
from p4
where (64 < a)
) T2(e_r, c_r, a_r, b_r)
on ((83 + b_r) = 68)
) T2(e_l_r, b_r_r)
on (47 = b_r_r)
) T1(d_l_l_l, e_r_r_l_l, b_r_r_l, e_l_r_l)
left join (
Select b
from p2
where (d = a)
) T2(b_r)
on (93 = e_r_r_l_l)
) T1(e_r_r_l_l_l, b_r_l)
full join (
Select c, d
from p3
where (d > 16)
) T2(c_r, d_r)
on ((b_r_l = b_r_l) OR ((76 = b_r_l) OR ((78 > c_r) AND (b_r_l < 18))))
) T1(b_r_l_l, e_r_r_l_l_l_l, c_r_l)
left join (
Select a
from p2
where (a > 86)
) T2(a_r)
on (27 = e_r_r_l_l_l_l)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test50exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, e_l_r
from (
Select c
from p1
where (60 < (54 + 70))
) T1(c_l)
inner join (
Select e_l, a_l, b_l, d_r_r
from (
Select e, a, b
from p1
where ((59 < 86) AND (59 < 69))
) T1(e_l, a_l, b_l)
left join (
Select c_l, b_l, c_r, b_r, d_r
from (
Select c, b
from p3
where (c < b)
) T1(c_l, b_l)
left join (
select c, b, d
from (
Select c, b, d
from p1
where (d < 9)
) T1
union all
select e_l, c_l, d_l
from (
Select e_l, c_l, d_l, e_r, a_r, d_r
from (
Select e, c, d
from p2
where ((21 = (d * 41)) OR (c < b))
) T1(e_l, c_l, d_l)
inner join (
Select e, a, d
from p2
where ((87 * (45 * 25)) = 72)
) T2(e_r, a_r, d_r)
on ((e_r = a_r) AND ((c_l = 9) AND ((a_r < 26) OR (85 > (e_l * 96)))))
) T2
) T2(c_r, b_r, d_r)
on (b_l = d_r)
) T2(c_l_r, b_l_r, c_r_r, b_r_r, d_r_r)
on ((50 > (86 + 53)) AND ((e_l > 35) OR ((d_r_r = (d_r_r - 19)) OR (e_l = d_r_r))))
) T2(e_l_r, a_l_r, b_l_r, d_r_r_r)
on (74 = e_l_r)
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
Select d_l, d_l_r_l_l_l_r, c_r_l_r_r_r
from (
Select d
from p5
where (30 = b)
) T1(d_l)
left join (
Select d_l_r_l_l_l, a_r_r_l_l_l_l, b_l_r_l_l_l_l, c_l_r, c_r_l_r_r
from (
Select a_r_r_l_l_l, b_l_r_l_l_l, d_l_r_l_l, c_r
from (
Select b_l_r_l_l, a_r_r_l_l, d_l_r_l, e_l_l_l_l_r
from (
Select b_l_r_l, a_l_l, a_r_r_l, c_l_r, b_r_r, d_l_r
from (
Select c_l, a_l, a_r_r, b_l_r
from (
Select c, a, b
from p3
where ((81 + 48) = 90)
) T1(c_l, a_l, b_l)
left join (
Select e_l, b_l, a_r
from (
Select e, b
from p4
where ((b > 36) AND (((16 + a) * 3) = (78 + a)))
) T1(e_l, b_l)
left join (
select a
from (
Select a
from p4
where (93 = d)
) T1
union all
select e
from (
Select e, b, d
from p5
where (a < c)
) T2
) T2(a_r)
on ((a_r > (b_l * 24)) OR ((e_l + 25) < b_l))
) T2(e_l_r, b_l_r, a_r_r)
on (b_l_r < a_r_r)
) T1(c_l_l, a_l_l, a_r_r_l, b_l_r_l)
left join (
Select c_l, d_l, b_r
from (
Select c, d
from p1
where ((d = b) OR ((89 < c) AND (48 < c)))
) T1(c_l, d_l)
left join (
Select b, d
from p4
where (18 > e)
) T2(b_r, d_r)
on (b_r = 24)
) T2(c_l_r, d_l_r, b_r_r)
on ((69 = 62) AND (19 > b_l_r_l))
) T1(b_l_r_l_l, a_l_l_l, a_r_r_l_l, c_l_r_l, b_r_r_l, d_l_r_l)
inner join (
select e_l_l_l_l, a_r_l
from (
Select e_l_l_l_l, a_r_l, c_r_l_l, e_r
from (
Select c_r_l, e_l_l_l, a_r
from (
select e_l_l, c_r
from (
Select e_l_l, c_r
from (
Select e_l, b_l, c_r
from (
Select e, c, b
from p3
where ((c - 68) = ((12 + (((11 * ((27 - e) + 2)) - (46 * a)) + 27)) * (9 + 82)))
) T1(e_l, c_l, b_l)
left join (
Select c, a
from p3
where (d > c)
) T2(c_r, a_r)
on (c_r = (b_l * e_l))
) T1(e_l_l, b_l_l, c_r_l)
inner join (
Select c
from p2
where (36 = c)
) T2(c_r)
on ((e_l_l < ((92 * (27 + ((7 + 67) + 38))) - e_l_l)) OR (3 = c_r))
) T1
union all
select b_l, b_r
from (
Select b_l, b_r
from (
select b
from (
select b
from (
Select b
from p1
where ((99 - 70) < b)
) T1
union all
select c
from (
Select c
from p3
where (a > 17)
) T2
) T1
union all
select c
from (
Select c, b
from p5
where (((33 - d) = 26) OR (69 = 10))
) T2
) T1(b_l)
left join (
Select e, b
from p2
where (b = 39)
) T2(e_r, b_r)
on (49 < b_r)
) T2
) T1(e_l_l_l, c_r_l)
left join (
Select a
from p1
where ((c < 65) AND (5 > e))
) T2(a_r)
on ((67 > 60) OR (22 = e_l_l_l))
) T1(c_r_l_l, e_l_l_l_l, a_r_l)
left join (
select e
from (
Select e, c
from p1
where (91 = 90)
) T1
union all
select a
from (
Select a
from p4
where ((c = c) AND ((94 = 89) AND (e < 19)))
) T2
) T2(e_r)
on (((c_r_l_l - e_l_l_l_l) > 81) AND (92 = 19))
) T1
union all
select d_r_l_l, c_r
from (
Select d_r_l_l, c_r
from (
Select b_r_l, d_r_l, a_r
from (
Select c_r_l, e_r_l, a_r, b_r, d_r
from (
Select b_l, e_r, c_r
from (
Select b
from p3
where (19 < b)
) T1(b_l)
left join (
Select e, c
from p1
where ((81 = b) AND (((46 + 63) > 33) OR ((84 = 71) AND ((a - 37) = 38))))
) T2(e_r, c_r)
on (((74 + (b_l * b_l)) = c_r) OR ((e_r = 32) OR ((e_r > 9) AND (e_r = e_r))))
) T1(b_l_l, e_r_l, c_r_l)
left join (
Select a, b, d
from p5
where ((d = c) OR ((94 = c) OR (c = c)))
) T2(a_r, b_r, d_r)
on ((b_r = 11) AND ((56 * e_r_l) < a_r))
) T1(c_r_l_l, e_r_l_l, a_r_l, b_r_l, d_r_l)
inner join (
Select e, a
from p1
where (a = d)
) T2(e_r, a_r)
on ((a_r + d_r_l) > a_r)
) T1(b_r_l_l, d_r_l_l, a_r_l)
left join (
Select e, c
from p5
where (a > a)
) T2(e_r, c_r)
on (c_r < d_r_l_l)
) T2
) T2(e_l_l_l_l_r, a_r_l_r)
on ((62 - 43) > d_l_r_l)
) T1(b_l_r_l_l_l, a_r_r_l_l_l, d_l_r_l_l, e_l_l_l_l_r_l)
inner join (
select e, c
from (
Select e, c
from p2
where (74 > (d * 82))
) T1
union all
select e_l, a_l
from (
Select e_l, a_l, e_r, b_r
from (
Select e, a
from p2
where (b = ((a * (14 - a)) * ((44 - c) - a)))
) T1(e_l, a_l)
left join (
Select e, c, b
from p5
where (26 = (32 - 88))
) T2(e_r, c_r, b_r)
on (20 = (((e_r + e_r) + e_l) + e_r))
) T2
) T2(e_r, c_r)
on (92 < 12)
) T1(a_r_r_l_l_l_l, b_l_r_l_l_l_l, d_l_r_l_l_l, c_r_l)
inner join (
Select c_l, c_r_l_r
from (
Select c
from p2
where ((66 = (a - c)) AND (78 > a))
) T1(c_l)
left join (
select c_r_l
from (
Select c_r_l, e_r
from (
Select c_r_r_l, e_r, c_r
from (
Select c_l, b_l, a_l_l_l_r, c_r_r
from (
Select e, c, b
from p4
where ((79 > 27) AND (a = 75))
) T1(e_l, c_l, b_l)
inner join (
Select d_l_r_r_l, a_l_l_l, c_r
from (
Select a_l_l, e_r_l_r_l, e_r_r_r_l, d_l_r_r
from (
Select e_l, a_l, e_r_l_r, e_r_r_r
from (
Select e, a
from p2
where ((53 < e) OR (67 = 78))
) T1(e_l, a_l)
full join (
Select a_r_l_l, e_r_l, d_r_r, e_r_r
from (
Select a_r_l, e_r
from (
Select c_l, a_r
from (
Select e, c, a
from p3
where ((50 < c) OR (((((60 - d) * e) * ((e + (c * (d - d))) + 37)) = 7) OR ((b < (c - e)) OR (d = 29))))
) T1(e_l, c_l, a_l)
full join (
Select a
from p2
where (82 > (18 * (d * (79 * (((b - (a - 34)) - e) + 25)))))
) T2(a_r)
on (90 > (a_r * 50))
) T1(c_l_l, a_r_l)
left join (
Select e
from p3
where (37 > d)
) T2(e_r)
on (94 = a_r_l)
) T1(a_r_l_l, e_r_l)
full join (
Select b_l, e_r, d_r
from (
Select b
from p3
where (46 > 97)
) T1(b_l)
left join (
Select e, d
from p2
where (c > 10)
) T2(e_r, d_r)
on ((((13 + e_r) - e_r) = d_r) OR (13 > 57))
) T2(b_l_r, e_r_r, d_r_r)
on ((e_r_r - (a_r_l_l + 96)) = d_r_r)
) T2(a_r_l_l_r, e_r_l_r, d_r_r_r, e_r_r_r)
on (a_l = e_r_l_r)
) T1(e_l_l, a_l_l, e_r_l_r_l, e_r_r_r_l)
full join (
Select a_l_r_r_r_l, a_l_r_r_l, b_l_l, d_l_r
from (
Select b_l, a_l_r_r, a_l_r_r_r
from (
Select b
from p5
where ((86 > b) OR ((e < 91) AND (a = c)))
) T1(b_l)
left join (
Select b_l_l, a_l_r, a_l_r_r, a_r_r_r
from (
Select b_l, b_r
from (
Select b, d
from p3
where ((e = (b * (e - 79))) AND (((d * 29) = b) OR (e < b)))
) T1(b_l, d_l)
full join (
Select b
from p5
where (89 = d)
) T2(b_r)
on ((60 + b_l) > 19)
) T1(b_l_l, b_r_l)
left join (
Select a_l, a_l_r, a_r_r, e_r_r
from (
select e, a, d
from (
Select e, a, d
from p5
where (13 > d)
) T1
union all
select e, c, b
from (
Select e, c, b
from p4
where (c = (50 * 22))
) T2
) T1(e_l, a_l, d_l)
left join (
Select a_l, e_r, a_r
from (
Select a
from p5
where ((d > 52) AND ((b > 35) AND (88 > a)))
) T1(a_l)
left join (
Select e, a
from p2
where ((82 = 86) AND (22 = d))
) T2(e_r, a_r)
on ((e_r = (41 + (13 * 84))) OR ((14 = (83 - (52 - (35 * a_l)))) OR (e_r > e_r)))
) T2(a_l_r, e_r_r, a_r_r)
on (49 = 87)
) T2(a_l_r, a_l_r_r, a_r_r_r, e_r_r_r)
on (83 < a_l_r)
) T2(b_l_l_r, a_l_r_r, a_l_r_r_r, a_r_r_r_r)
on (a_l_r_r_r = a_l_r_r_r)
) T1(b_l_l, a_l_r_r_l, a_l_r_r_r_l)
left join (
Select e_l, d_l, e_r_l_r, e_r_r_l_l_r
from (
Select e, d
from p4
where (e < 54)
) T1(e_l, d_l)
inner join (
Select e_r_r_l_l, e_r_l, a_r
from (
Select e_r_r_l, e_r, c_r
from (
Select a_l, e_l_r, e_r_r
from (
Select c, a
from p3
where ((b = 75) AND (59 > 74))
) T1(c_l, a_l)
left join (
Select e_l, e_r, c_r
from (
Select e
from p4
where (56 = 69)
) T1(e_l)
left join (
Select e, c
from p4
where (28 < (40 - ((37 * c) - 61)))
) T2(e_r, c_r)
on (94 = e_l)
) T2(e_l_r, e_r_r, c_r_r)
on (23 > 53)
) T1(a_l_l, e_l_r_l, e_r_r_l)
left join (
Select e, c, b
from p2
where ((d < (d * c)) OR ((c = 26) AND (50 = b)))
) T2(e_r, c_r, b_r)
on (e_r_r_l = e_r)
) T1(e_r_r_l_l, e_r_l, c_r_l)
left join (
Select a
from p3
where ((b = ((((79 + d) + 45) + d) - a)) OR (((d + a) = 25) AND (e = a)))
) T2(a_r)
on (a_r = 6)
) T2(e_r_r_l_l_r, e_r_l_r, a_r_r)
on (e_r_r_l_l_r > (((82 + (99 + e_r_r_l_l_r)) + ((d_l - 4) + 29)) - 21))
) T2(e_l_r, d_l_r, e_r_l_r_r, e_r_r_l_l_r_r)
on (a_l_r_r_r_l = a_l_r_r_l)
) T2(a_l_r_r_r_l_r, a_l_r_r_l_r, b_l_l_r, d_l_r_r)
on (d_l_r_r < e_r_l_r_l)
) T1(a_l_l_l, e_r_l_r_l_l, e_r_r_r_l_l, d_l_r_r_l)
inner join (
Select c, b
from p4
where (c < e)
) T2(c_r, b_r)
on ((a_l_l_l = 25) AND ((c_r = 12) AND (d_l_r_r_l < a_l_l_l)))
) T2(d_l_r_r_l_r, a_l_l_l_r, c_r_r)
on ((((12 * a_l_l_l_r) * 9) + c_l) > (44 + c_l))
) T1(c_l_l, b_l_l, a_l_l_l_r_l, c_r_r_l)
inner join (
Select e, c, b
from p5
where (70 = c)
) T2(e_r, c_r, b_r)
on ((c_r < c_r) AND ((c_r > c_r_r_l) OR (e_r = (c_r_r_l + 27))))
) T1(c_r_r_l_l, e_r_l, c_r_l)
left join (
select e
from (
Select e
from p2
where ((c > 97) OR (a > 48))
) T1
union all
select e
from (
select e, a
from (
Select e, a
from p3
where (d = 62)
) T1
union all
select e, a
from (
Select e, a, b, d
from p5
where ((42 * 2) = 75)
) T2
) T2
) T2(e_r)
on ((13 < ((72 + c_r_l) + 56)) AND (71 = c_r_l))
) T1
union all
select e
from (
Select e
from p3
where (29 = 49)
) T2
) T2(c_r_l_r)
on (c_r_l_r = c_l)
) T2(c_l_r, c_r_l_r_r)
on ((50 < 22) AND ((b_l_r_l_l_l_l = 88) AND ((1 < b_l_r_l_l_l_l) OR (a_r_r_l_l_l_l = (a_r_r_l_l_l_l + (c_l_r + d_l_r_l_l_l))))))
) T2(d_l_r_l_l_l_r, a_r_r_l_l_l_l_r, b_l_r_l_l_l_l_r, c_l_r_r, c_r_l_r_r_r)
on (((19 * 33) > (d_l - 59)) OR (57 > d_l_r_l_l_l_r))
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
Select c_r_l, d_l_l, b_r_r, b_l_l_r, c_r_r
from (
Select a_l, d_l, c_r
from (
Select a, d
from p3
where (c < 31)
) T1(a_l, d_l)
full join (
select e, c
from (
Select e, c, b
from p3
where (e = e)
) T1
union all
select e, a
from (
Select e, a
from p2
where ((50 < 52) AND (((a - (a + 27)) < 39) AND ((b = 84) OR (54 = b))))
) T2
) T2(e_r, c_r)
on (((16 * c_r) < (a_l + 73)) AND ((c_r = 1) OR (66 = 8)))
) T1(a_l_l, d_l_l, c_r_l)
full join (
Select b_l_l, c_r, b_r
from (
Select c_l, a_l, b_l, c_r_r
from (
Select c, a, b
from p1
where ((b * (91 * d)) > 8)
) T1(c_l, a_l, b_l)
left join (
Select e_l_l, a_r_l, c_r, b_r
from (
Select e_l, a_r
from (
Select e, c
from p1
where (d > 59)
) T1(e_l, c_l)
inner join (
Select a
from p5
where ((37 = 12) OR (11 = 83))
) T2(a_r)
on ((87 > a_r) OR ((a_r < (26 + e_l)) OR (((e_l - e_l) + a_r) > a_r)))
) T1(e_l_l, a_r_l)
full join (
Select c, b
from p4
where ((b = 69) OR (55 > b))
) T2(c_r, b_r)
on (a_r_l > a_r_l)
) T2(e_l_l_r, a_r_l_r, c_r_r, b_r_r)
on (28 = (a_l - 53))
) T1(c_l_l, a_l_l, b_l_l, c_r_r_l)
full join (
Select c, b
from p3
where (c < b)
) T2(c_r, b_r)
on ((46 > b_r) AND ((17 - (34 * b_l_l)) = 48))
) T2(b_l_l_r, c_r_r, b_r_r)
on (b_l_l_r = d_l_l)
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test50exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, a_r, b_r
from (
Select b
from p2
where (24 < 3)
) T1(b_l)
left join (
Select e, a, b
from p2
where ((26 > (((81 + (26 - 62)) * (a * 85)) * (d * 91))) OR (e > (a - a)))
) T2(e_r, a_r, b_r)
on (b_r = ((99 * b_r) - b_r))
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
    #******************
    _testmgr.testcase_end(desc)

