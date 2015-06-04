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
    
def test001(desc="""Joins Set 30"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, a_r
from (
Select b
from p5
where (22 = a)
) T1(b_l)
inner join (
Select a
from p5
where ((a = (e * a)) AND ((b < (a * e)) OR ((d = 91) AND (45 < 12))))
) T2(a_r)
on (a_r < (a_r - a_r))
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
Select e_l_l_r_r_r_l_l_l, e_r_l, e_r
from (
Select e_l_l_r_r_r_l_l, e_r
from (
Select e_l_l_r_r_r_l, e_r, c_r
from (
Select b_r_l, b_l_l, a_l_r_r, a_r_r_r_r, e_l_l_r_r_r
from (
Select b_l, b_r
from (
Select c, b, d
from p5
where (a > c)
) T1(c_l, b_l, d_l)
inner join (
Select e, c, a, b
from p3
where (d = 36)
) T2(e_r, c_r, a_r, b_r)
on ((78 < 96) OR ((b_r * (73 - (b_l + b_l))) = b_l))
) T1(b_l_l, b_r_l)
left join (
Select e_l, b_l, a_l_r, e_l_l_r_r, a_r_r_r
from (
Select e, b
from p2
where (e < 5)
) T1(e_l, b_l)
left join (
Select e_l, a_l, b_l, a_r_r, a_l_l_r, e_l_l_r
from (
Select e, a, b
from p5
where ((d < 13) OR (39 < b))
) T1(e_l, a_l, b_l)
left join (
Select a_l_l, e_l_l, a_r
from (
Select e_l, a_l, b_r
from (
Select e, a
from p4
where ((b * (29 - c)) = c)
) T1(e_l, a_l)
left join (
Select b
from p4
where (b = e)
) T2(b_r)
on ((5 > ((21 - e_l) + (e_l - a_l))) AND (a_l > 70))
) T1(e_l_l, a_l_l, b_r_l)
inner join (
Select e, a, b
from p3
where (81 = 21)
) T2(e_r, a_r, b_r)
on (e_l_l > a_r)
) T2(a_l_l_r, e_l_l_r, a_r_r)
on (30 < ((79 + a_l) + 90))
) T2(e_l_r, a_l_r, b_l_r, a_r_r_r, a_l_l_r_r, e_l_l_r_r)
on ((e_l_l_r_r - a_l_r) = b_l)
) T2(e_l_r, b_l_r, a_l_r_r, e_l_l_r_r_r, a_r_r_r_r)
on (((e_l_l_r_r_r + e_l_l_r_r_r) > e_l_l_r_r_r) OR (a_l_r_r < 31))
) T1(b_r_l_l, b_l_l_l, a_l_r_r_l, a_r_r_r_r_l, e_l_l_r_r_r_l)
left join (
Select e, c
from p3
where (e = 2)
) T2(e_r, c_r)
on ((((e_r - 92) + (c_r - e_l_l_r_r_r_l)) > e_l_l_r_r_r_l) AND (c_r = 47))
) T1(e_l_l_r_r_r_l_l, e_r_l, c_r_l)
full join (
Select e
from p2
where ((b - a) > d)
) T2(e_r)
on (69 = 73)
) T1(e_l_l_r_r_r_l_l_l, e_r_l)
left join (
Select e, a
from p5
where (60 < a)
) T2(e_r, a_r)
on (((90 + (95 + (1 + (((e_r + 6) * 41) * 53)))) = e_r) OR ((44 + e_r_l) > 96))
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
Select b_l, a_r, d_r
from (
select b
from (
Select b
from p3
where (70 < c)
) T1
union all
select e
from (
Select e
from p3
where (((34 * d) = 93) OR (e > (b + d)))
) T2
) T1(b_l)
inner join (
Select a, d
from p1
where (d = a)
) T2(a_r, d_r)
on ((b_l - d_r) > b_l)
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
Select e_l, c_l, c_r, d_r
from (
Select e, c, d
from p3
where ((55 = a) AND ((59 = e) AND ((94 > 68) AND (b > (76 + 22)))))
) T1(e_l, c_l, d_l)
left join (
Select c, a, d
from p1
where (((44 * e) + d) < (d + ((d + c) * 89)))
) T2(c_r, a_r, d_r)
on (d_r > 6)
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
Select c_l, a_l, d_l, c_r, a_r
from (
select c, a, d
from (
Select c, a, d
from p5
where (11 > ((62 * 47) * a))
) T1
union all
select a_l, c_l_r, c_r_r
from (
Select a_l, c_l_r, c_r_r
from (
Select e, a, b, d
from p2
where (c = 87)
) T1(e_l, a_l, b_l, d_l)
left join (
Select c_l, c_r, d_r
from (
Select c
from p3
where ((39 > d) OR ((77 = (e * (73 + b))) OR (b = e)))
) T1(c_l)
full join (
select c, d
from (
Select c, d
from p3
where ((((e + 30) + b) = a) OR (c = 22))
) T1
union all
select e, a
from (
Select e, a, d
from p2
where ((98 > c) OR (78 < c))
) T2
) T2(c_r, d_r)
on (c_r = c_l)
) T2(c_l_r, c_r_r, d_r_r)
on ((54 = 48) OR (54 > 23))
) T2
) T1(c_l, a_l, d_l)
full join (
Select c, a
from p3
where ((((d - 16) - 44) + b) < 30)
) T2(c_r, a_r)
on ((5 = (a_r * d_l)) AND (31 = ((c_l + c_l) + a_r)))
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test30exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_l, d_l, b_r_r, c_r_r
from (
Select c, a, d
from p1
where (a < 39)
) T1(c_l, a_l, d_l)
inner join (
Select d_l, c_r, b_r
from (
Select d
from p1
where ((e = b) OR ((83 = 66) AND ((c > b) OR (((52 + 38) > 26) AND ((94 - 38) > 2)))))
) T1(d_l)
full join (
Select c, a, b
from p1
where (((a * a) = 96) OR ((69 > b) AND ((d < b) AND (72 = c))))
) T2(c_r, a_r, b_r)
on ((82 = 65) AND (45 = b_r))
) T2(d_l_r, c_r_r, b_r_r)
on (b_r_r > c_l)
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
Select a_l, b_r
from (
Select a
from p2
where (a = 19)
) T1(a_l)
left join (
Select b, d
from p3
where (61 = 65)
) T2(b_r, d_r)
on (a_l = a_l)
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
Select e_l, d_r
from (
Select e
from p1
where ((15 > 62) AND (16 < b))
) T1(e_l)
inner join (
Select e, d
from p4
where (84 = 5)
) T2(e_r, d_r)
on ((38 = 53) OR ((12 = 72) OR (e_l = e_l)))
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
Select d_l, c_r, a_r
from (
Select e, a, b, d
from p2
where (c = c)
) T1(e_l, a_l, b_l, d_l)
inner join (
Select c, a, b, d
from p4
where (47 > (54 + a))
) T2(c_r, a_r, b_r, d_r)
on ((85 < c_r) AND (58 > (74 + 66)))
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
Select c_l, d_l, b_r, d_r
from (
Select c, d
from p1
where ((c = 69) OR (((81 + 23) - d) = d))
) T1(c_l, d_l)
left join (
Select c, b, d
from p2
where ((41 * d) = a)
) T2(c_r, b_r, d_r)
on (b_r > 72)
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
Select e_l_l, b_r_r
from (
Select e_l, c_r
from (
Select e, c
from p5
where ((e < (d + c)) AND (b < d))
) T1(e_l, c_l)
left join (
Select c
from p4
where (30 = ((2 + 77) - a))
) T2(c_r)
on (21 > e_l)
) T1(e_l_l, c_r_l)
left join (
Select c_l_r_l, c_l_l, b_r
from (
Select e_l, c_l, c_l_r
from (
Select e, c, d
from p1
where (84 > e)
) T1(e_l, c_l, d_l)
left join (
select c_l
from (
Select c_l, d_r_r, e_l_l_r
from (
Select c
from p2
where ((17 > (c - (94 + 39))) AND ((d * 38) > b))
) T1(c_l)
inner join (
Select e_l_l, d_r
from (
Select e_l, c_l, b_r
from (
select e, c
from (
Select e, c, d
from p3
where ((53 + c) > (25 - (40 - 91)))
) T1
union all
select c, a
from (
select c, a
from (
select c, a
from (
Select c, a, b
from p1
where ((15 - a) = a)
) T1
union all
select c, b
from (
Select c, b
from p5
where (84 = (e + c))
) T2
) T1
union all
select c, a
from (
Select c, a, b
from p1
where (46 > 95)
) T2
) T2
) T1(e_l, c_l)
left join (
Select b
from p1
where (e = e)
) T2(b_r)
on ((12 > (c_l - 84)) OR (75 = 22))
) T1(e_l_l, c_l_l, b_r_l)
inner join (
Select d
from p3
where (76 = a)
) T2(d_r)
on (25 = (d_r - 54))
) T2(e_l_l_r, d_r_r)
on (20 > 4)
) T1
union all
select a
from (
Select a
from p4
where ((92 < 87) AND ((c - 43) < a))
) T2
) T2(c_l_r)
on (c_l = 16)
) T1(e_l_l, c_l_l, c_l_r_l)
left join (
Select c, b
from p4
where (c = (c + 79))
) T2(c_r, b_r)
on ((c_l_l = 79) OR (((b_r + 72) < c_l_r_l) OR (5 = 77)))
) T2(c_l_r_l_r, c_l_l_r, b_r_r)
on (5 < 37)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test30exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_r
from (
Select e, a
from p4
where ((0 > (75 + 50)) OR (31 < 51))
) T1(e_l, a_l)
inner join (
Select b
from p5
where (85 = ((44 * a) + 3))
) T2(b_r)
on ((22 < 43) OR (19 = e_l))
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
from p2
where ((92 < a) AND (b = e))
) T1(b_l)
full join (
Select c_l, c_r, a_r
from (
Select e, c
from p3
where (55 = 29)
) T1(e_l, c_l)
full join (
Select e, c, a
from p2
where ((a + 7) = ((d * a) * 87))
) T2(e_r, c_r, a_r)
on (83 = 55)
) T2(c_l_r, c_r_r, a_r_r)
on ((a_r_r = 61) OR (a_r_r > (5 - 45)))
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
Select a_r_l_l_l, e_r_l, c_r, d_r
from (
Select a_r_l, a_r_l_l, e_r
from (
Select a_r_l, a_l_l_l, a_r
from (
select a_l_l, e_r, a_r
from (
Select a_l_l, e_r, a_r
from (
Select a_l, c_r
from (
Select c, a
from p1
where (b > 1)
) T1(c_l, a_l)
left join (
select c
from (
Select c
from p4
where (60 < ((b + 4) * 24))
) T1
union all
select e_l
from (
Select e_l, d_l, d_r
from (
Select e, b, d
from p5
where (83 = 78)
) T1(e_l, b_l, d_l)
full join (
Select d
from p1
where (b = (88 + e))
) T2(d_r)
on ((69 > e_l) AND (d_l = (22 * e_l)))
) T2
) T2(c_r)
on (((10 - (64 - 47)) = a_l) AND (a_l > c_r))
) T1(a_l_l, c_r_l)
full join (
Select e, a, d
from p1
where ((d > b) OR ((40 - b) > (c + (78 - 34))))
) T2(e_r, a_r, d_r)
on (74 = 55)
) T1
union all
select e, b, d
from (
Select e, b, d
from p4
where ((94 > 63) OR (b < 49))
) T2
) T1(a_l_l_l, e_r_l, a_r_l)
inner join (
select a
from (
select a
from (
Select a, b
from p4
where (((a * 75) < 45) AND (((15 - (a - 48)) > e) OR (((e + (b * ((d + 54) + 88))) - (c + 98)) > ((b - 97) + 67))))
) T1
union all
select a
from (
Select a
from p1
where (c < 16)
) T2
) T1
union all
select e_l
from (
Select e_l, e_l_r, d_r_r
from (
Select e, c, b
from p5
where (b < 88)
) T1(e_l, c_l, b_l)
left join (
Select e_l, e_r, d_r
from (
select e, a
from (
select e, a
from (
Select e, a, d
from p2
where ((b * 3) = 3)
) T1
union all
select e, a
from (
select e, a
from (
Select e, a
from p4
where (d > 96)
) T1
union all
select e, c
from (
Select e, c, b
from p1
where (c = 79)
) T2
) T2
) T1
union all
select e, c
from (
select e, c
from (
Select e, c
from p5
where (11 < b)
) T1
union all
select c, a
from (
Select c, a
from p2
where ((d < (e - 8)) OR (((e + a) = d) OR (22 = e)))
) T2
) T2
) T1(e_l, a_l)
full join (
Select e, d
from p5
where (20 = c)
) T2(e_r, d_r)
on (81 < e_l)
) T2(e_l_r, e_r_r, d_r_r)
on ((4 * e_l_r) = d_r_r)
) T2
) T2(a_r)
on (a_l_l_l > 40)
) T1(a_r_l_l, a_l_l_l_l, a_r_l)
left join (
select e
from (
Select e
from p4
where (90 = (a - 14))
) T1
union all
select e
from (
Select e, a, d
from p1
where (27 = 72)
) T2
) T2(e_r)
on ((e_r + a_r_l) < 19)
) T1(a_r_l_l, a_r_l_l_l, e_r_l)
full join (
Select c, d
from p2
where (b < e)
) T2(c_r, d_r)
on ((d_r = a_r_l_l_l) AND (e_r_l = 5))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test30exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, e_r
from (
Select d
from p1
where ((((a - 21) * e) > e) OR (62 > a))
) T1(d_l)
inner join (
Select e
from p2
where (76 > (54 * (b + 20)))
) T2(e_r)
on (36 > 93)
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
Select b_l, a_r
from (
Select b, d
from p2
where (83 = 61)
) T1(b_l, d_l)
left join (
Select c, a, b
from p2
where ((c < (((41 * 69) * d) - (26 + d))) AND (e = (d * 69)))
) T2(c_r, a_r, b_r)
on ((a_r > ((((b_l - 84) - b_l) - a_r) * 88)) AND (9 = a_r))
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
Select e_l, d_l, a_l_l_r_r
from (
Select e, b, d
from p3
where ((b < e) OR (81 > 65))
) T1(e_l, b_l, d_l)
full join (
Select b_l, d_r_r, a_l_l_r
from (
Select b
from p5
where ((a < 25) OR (((62 - 34) < (((38 + b) * a) + e)) AND ((35 < c) OR ((3 - 68) = 23))))
) T1(b_l)
inner join (
Select a_l_l, b_r_l, e_r, d_r
from (
Select a_l, a_r, b_r, d_r
from (
Select e, a
from p3
where (d = (d + (11 - (a * (83 + d)))))
) T1(e_l, a_l)
full join (
Select a, b, d
from p2
where ((55 - d) > 25)
) T2(a_r, b_r, d_r)
on (66 > 10)
) T1(a_l_l, a_r_l, b_r_l, d_r_l)
left join (
Select e, d
from p4
where (89 > (b + a))
) T2(e_r, d_r)
on ((37 = 56) OR (82 < 24))
) T2(a_l_l_r, b_r_l_r, e_r_r, d_r_r)
on ((b_l = (a_l_l_r * d_r_r)) AND (((38 * 37) = 80) AND (43 > (75 * (a_l_l_r + 13)))))
) T2(b_l_r, d_r_r_r, a_l_l_r_r)
on ((e_l = 96) OR (d_l > (a_l_l_r_r + d_l)))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test30exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, d_r
from (
Select d
from p2
where (a > 52)
) T1(d_l)
left join (
Select d
from p2
where (((49 + (e + 7)) + e) < a)
) T2(d_r)
on (d_r = d_l)
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
Select a_l_l, d_l_l, d_r
from (
Select c_l, a_l, d_l, e_r
from (
Select c, a, d
from p3
where ((c > (e * (a + (((b + a) * 6) + b)))) AND (e < e))
) T1(c_l, a_l, d_l)
left join (
Select e
from p2
where (((0 - 85) = a) AND (c < d))
) T2(e_r)
on ((a_l - c_l) = 8)
) T1(c_l_l, a_l_l, d_l_l, e_r_l)
full join (
Select d
from p1
where ((b < d) OR (87 = 60))
) T2(d_r)
on ((80 = 95) AND (d_r < d_r))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test30exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_l, b_r_r_l_l, b_l_l_l, e_r, b_r
from (
Select b_r_r_l, d_l_r_l, b_l_l, b_r
from (
Select b_l, b_r_r, d_l_r
from (
Select e, b
from p2
where (62 < 83)
) T1(e_l, b_l)
left join (
Select d_l, b_r
from (
Select b, d
from p3
where (75 > c)
) T1(b_l, d_l)
inner join (
Select c, b
from p4
where (((1 * b) = 3) OR (21 > (((69 + c) * c) * (78 - (e + ((b - b) - b))))))
) T2(c_r, b_r)
on (((d_l + b_r) * 28) < b_r)
) T2(d_l_r, b_r_r)
on ((38 < (d_l_r - (b_r_r * 89))) OR (b_l < d_l_r))
) T1(b_l_l, b_r_r_l, d_l_r_l)
inner join (
Select b
from p3
where ((39 + 87) = (d - e))
) T2(b_r)
on ((23 = ((88 * (86 * 96)) * d_l_r_l)) AND (47 = (((53 + (87 - 16)) + b_l_l) + d_l_r_l)))
) T1(b_r_r_l_l, d_l_r_l_l, b_l_l_l, b_r_l)
left join (
Select e, b, d
from p2
where (2 = 50)
) T2(e_r, b_r, d_r)
on ((90 + ((b_r_r_l_l - b_l_l_l) * ((21 - b_r_l) + 40))) < b_r_r_l_l)
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
    #*********************************************
    _testmgr.testcase_end(desc)

