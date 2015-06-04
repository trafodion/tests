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
    
def test001(desc="""Joins Set 18"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l_l, e_r_l, a_r
from (
Select e_l, d_l, e_r, c_r
from (
Select e, b, d
from p2
where (d < d)
) T1(e_l, b_l, d_l)
left join (
Select e, c, a, d
from p3
where (((84 - 12) - 28) > d)
) T2(e_r, c_r, a_r, d_r)
on ((73 = e_l) OR (84 > 83))
) T1(e_l_l, d_l_l, e_r_l, c_r_l)
inner join (
Select a
from p1
where (c = c)
) T2(a_r)
on (e_r_l > 6)
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
Select a_l_l, b_r_r
from (
select a_l, b_r_l_r
from (
Select a_l, b_r_l_r
from (
Select a, b, d
from p5
where ((35 = b) AND (12 < (34 + b)))
) T1(a_l, b_l, d_l)
full join (
select b_r_l
from (
Select b_r_l, e_r
from (
Select b_r_l, e_r_l_l, c_r, b_r, d_r
from (
Select c_l_l, e_r_l, c_r, b_r
from (
Select c_l, e_r
from (
Select c
from p4
where (48 < d)
) T1(c_l)
full join (
select e
from (
Select e, a
from p5
where (d = 22)
) T1
union all
select a
from (
Select a
from p1
where (((77 - e) > c) AND (c > (47 - a)))
) T2
) T2(e_r)
on (76 = c_l)
) T1(c_l_l, e_r_l)
left join (
Select c, b
from p5
where (71 > 21)
) T2(c_r, b_r)
on (e_r_l = c_r)
) T1(c_l_l_l, e_r_l_l, c_r_l, b_r_l)
left join (
Select c, b, d
from p3
where (67 > d)
) T2(c_r, b_r, d_r)
on (52 < b_r)
) T1(b_r_l_l, e_r_l_l_l, c_r_l, b_r_l, d_r_l)
left join (
Select e
from p1
where (((b * 60) < (30 - 86)) AND (75 = d))
) T2(e_r)
on ((b_r_l = e_r) AND (56 > (e_r * e_r)))
) T1
union all
select d
from (
select d
from (
Select d
from p3
where ((93 - d) = 99)
) T1
union all
select d_r_l_l
from (
Select d_r_l_l, e_r
from (
Select d_r_l, b_l_l, c_r, b_r
from (
Select b_l, d_r
from (
select b
from (
Select b
from p5
where (c < (94 * ((b - e) * 38)))
) T1
union all
select b
from (
Select b
from p5
where ((45 = 32) AND ((19 < b) AND (a < (81 - (b - 29)))))
) T2
) T1(b_l)
left join (
Select e, d
from p4
where (b = (d - 54))
) T2(e_r, d_r)
on ((b_l = 1) OR ((((b_l * (d_r - b_l)) - 63) = d_r) AND ((((2 - 1) - 17) = d_r) OR ((51 = 21) OR ((93 = b_l) AND ((14 + 5) = (d_r + (20 * b_l))))))))
) T1(b_l_l, d_r_l)
left join (
Select e, c, b
from p4
where (((45 + (a + 86)) > (42 - 83)) AND ((76 = 16) OR (64 = 13)))
) T2(e_r, c_r, b_r)
on (78 < (60 - 25))
) T1(d_r_l_l, b_l_l_l, c_r_l, b_r_l)
left join (
Select e, c, a, b
from p5
where (78 > 52)
) T2(e_r, c_r, a_r, b_r)
on (e_r = d_r_l_l)
) T2
) T2
) T2(b_r_l_r)
on (a_l = 29)
) T1
union all
select e_l, c_r
from (
Select e_l, c_r
from (
Select e, b, d
from p1
where (89 < e)
) T1(e_l, b_l, d_l)
left join (
Select c, a
from p4
where (((c - 20) * b) > 87)
) T2(c_r, a_r)
on (95 > 86)
) T2
) T1(a_l_l, b_r_l_r_l)
left join (
Select e_l, b_r
from (
Select e, c
from p5
where (54 = (e - b))
) T1(e_l, c_l)
left join (
Select b
from p2
where ((97 = e) AND ((72 + ((c - c) - 16)) > e))
) T2(b_r)
on (b_r > 24)
) T2(e_l_r, b_r_r)
on ((89 > 21) AND ((12 - a_l_l) < 13))
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
Select a_l, a_r_r, e_r_r
from (
Select a, d
from p2
where (d = 2)
) T1(a_l, d_l)
full join (
Select a_l, e_r, c_r, a_r
from (
Select c, a, b
from p4
where (a = a)
) T1(c_l, a_l, b_l)
left join (
Select e, c, a
from p1
where (((e * d) = c) AND (d < 72))
) T2(e_r, c_r, a_r)
on ((44 = 91) OR ((e_r > a_r) OR (36 > a_r)))
) T2(a_l_r, e_r_r, c_r_r, a_r_r)
on ((a_l > 66) AND ((7 + e_r_r) > 53))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l_l, a_r
from (
Select e_l, b_l, a_r, d_r
from (
Select e, c, b, d
from p4
where (44 = (89 - c))
) T1(e_l, c_l, b_l, d_l)
inner join (
Select a, d
from p3
where ((a = 27) OR (47 > (91 + e)))
) T2(a_r, d_r)
on (44 > b_l)
) T1(e_l_l, b_l_l, a_r_l, d_r_l)
full join (
Select a
from p2
where (b = c)
) T2(a_r)
on (a_r = a_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_r
from (
Select e
from p2
where (53 > 82)
) T1(e_l)
inner join (
Select a
from p1
where ((a - d) = c)
) T2(a_r)
on ((a_r = e_l) AND (3 = e_l))
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
Select c_l, c_r, a_r, b_r
from (
Select c, b
from p1
where (14 = 9)
) T1(c_l, b_l)
left join (
Select c, a, b
from p4
where (77 < d)
) T2(c_r, a_r, b_r)
on (a_r > a_r)
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
Select e_l_l, b_r, d_r
from (
Select e_l, c_r
from (
Select e
from p5
where (b = c)
) T1(e_l)
left join (
Select c
from p5
where ((74 = c) OR ((a = a) OR (((e - d) = c) OR ((34 = 3) OR (14 = 82)))))
) T2(c_r)
on (c_r > 2)
) T1(e_l_l, c_r_l)
inner join (
Select b, d
from p2
where (d = 7)
) T2(b_r, d_r)
on ((68 > d_r) OR (e_l_l = (b_r * b_r)))
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
Select d_r_l_r_l, d_r_r_l, b_r
from (
Select c_l, d_r_r, d_r_l_r, e_r_r
from (
Select c
from p4
where ((43 = e) OR (d > 91))
) T1(c_l)
full join (
Select d_r_l, e_r, b_r, d_r
from (
Select c_l, e_r, a_r, d_r
from (
Select c, a, d
from p2
where ((d = (44 + (63 * a))) OR (d < 30))
) T1(c_l, a_l, d_l)
left join (
Select e, a, d
from p2
where ((e < b) AND (53 = e))
) T2(e_r, a_r, d_r)
on (((d_r + 13) > 27) AND (c_l < 3))
) T1(c_l_l, e_r_l, a_r_l, d_r_l)
full join (
Select e, b, d
from p1
where ((71 = (d + e)) OR (16 > d))
) T2(e_r, b_r, d_r)
on (d_r > 40)
) T2(d_r_l_r, e_r_r, b_r_r, d_r_r)
on (((e_r_r * 67) - d_r_l_r) = e_r_r)
) T1(c_l_l, d_r_r_l, d_r_l_r_l, e_r_r_l)
left join (
Select b
from p1
where (82 < a)
) T2(b_r)
on (66 < 87)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, a_r
from (
Select a
from p4
where (7 = (67 - e))
) T1(a_l)
left join (
select a
from (
select a, d
from (
select a, d
from (
Select a, d
from p3
where (d > e)
) T1
union all
select c_l, d_l
from (
Select c_l, d_l, e_r_l_r, e_r_r_r
from (
Select e, c, d
from p5
where (37 = 4)
) T1(e_l, c_l, d_l)
full join (
Select e_r_l, c_l_r, e_r_r
from (
Select e_l_l, c_r_l, e_r
from (
Select e_l, c_r, d_r
from (
Select e, a
from p1
where (d > ((b + (65 * (e * c))) + 21))
) T1(e_l, a_l)
full join (
Select c, d
from p1
where ((83 > b) AND (78 > b))
) T2(c_r, d_r)
on (((e_l * 32) = 2) OR ((c_r < e_l) OR (61 > e_l)))
) T1(e_l_l, c_r_l, d_r_l)
left join (
Select e, b
from p5
where ((d = 25) AND ((a = (c * ((a * (30 * 56)) + (72 + 59)))) OR ((33 = (a - a)) AND (((c + a) = d) AND (c > 89)))))
) T2(e_r, b_r)
on (27 = 12)
) T1(e_l_l_l, c_r_l_l, e_r_l)
left join (
Select c_l, e_r
from (
select c
from (
Select c
from p5
where ((e * a) > (97 - a))
) T1
union all
select b
from (
Select b, d
from p2
where (60 = ((a - d) * d))
) T2
) T1(c_l)
inner join (
Select e
from p3
where (12 < e)
) T2(e_r)
on (31 = 82)
) T2(c_l_r, e_r_r)
on (55 < (19 + 14))
) T2(e_r_l_r, c_l_r_r, e_r_r_r)
on (e_r_r_r < e_r_l_r)
) T2
) T1
union all
select c_r_l_l, d_l_r_l
from (
Select c_r_l_l, d_l_r_l, e_r
from (
Select a_l_l, a_r_l, c_r_l, d_r_r, d_l_r
from (
Select a_l, c_r, a_r
from (
Select a, d
from p1
where ((e < 85) OR (13 = 37))
) T1(a_l, d_l)
inner join (
select c, a
from (
Select c, a, b, d
from p4
where (18 = a)
) T1
union all
select e, c
from (
Select e, c
from p4
where ((22 > d) AND ((93 = (99 - 87)) OR ((91 * (5 * c)) > 52)))
) T2
) T2(c_r, a_r)
on ((a_l > 43) AND (12 = c_r))
) T1(a_l_l, c_r_l, a_r_l)
inner join (
Select d_l, d_r
from (
Select c, b, d
from p1
where ((a > 13) AND (22 = 49))
) T1(c_l, b_l, d_l)
left join (
Select b, d
from p5
where ((97 < ((66 * (d + 40)) + 92)) AND ((b > 43) OR ((86 = 57) OR (77 = (d - 48)))))
) T2(b_r, d_r)
on (d_l = 78)
) T2(d_l_r, d_r_r)
on ((c_r_l < d_r_r) OR (((43 * (d_l_r + (12 * 31))) - ((d_r_r + 61) * d_r_r)) = a_l_l))
) T1(a_l_l_l, a_r_l_l, c_r_l_l, d_r_r_l, d_l_r_l)
left join (
Select e
from p2
where (99 = 74)
) T2(e_r)
on (((13 + c_r_l_l) + d_l_r_l) < (6 * c_r_l_l))
) T2
) T1
union all
select d
from (
Select d
from p3
where ((32 - d) = 71)
) T2
) T2(a_r)
on (89 > 92)
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
Select a_l_r_l, c_r_l_r_r_r_l, c_l_r, b_l_r
from (
Select d_l, a_l_r, c_r_l_r_r_r
from (
Select c, a, b, d
from p2
where (e < 49)
) T1(c_l, a_l, b_l, d_l)
left join (
Select a_l, c_r_l_r_r, d_r_l_l_r_r, d_l_r
from (
select a
from (
select a
from (
Select a
from p4
where (89 = 81)
) T1
union all
select c
from (
Select c, b
from p3
where (a > e)
) T2
) T1
union all
select a_l_l
from (
select a_l_l, d_l_l, c_r
from (
Select a_l_l, d_l_l, c_r, b_r
from (
Select a_l, d_l, d_l_r
from (
Select c, a, d
from p1
where (5 > b)
) T1(c_l, a_l, d_l)
inner join (
Select d_l, d_r
from (
select e, d
from (
Select e, d
from p2
where ((d * 1) = e)
) T1
union all
select c_l_l, b_r_l
from (
Select c_l_l, b_r_l, e_l_l, b_r
from (
Select e_l, c_l, a_l, b_r
from (
Select e, c, a
from p2
where ((b = (22 + e)) AND (b > (d * 80)))
) T1(e_l, c_l, a_l)
left join (
Select a, b
from p5
where ((83 = 86) OR ((c = b) AND (d = b)))
) T2(a_r, b_r)
on ((e_l * 79) > e_l)
) T1(e_l_l, c_l_l, a_l_l, b_r_l)
left join (
Select b, d
from p3
where ((a = a) AND ((d > 89) OR ((78 = b) OR (((b - d) * d) < e))))
) T2(b_r, d_r)
on ((57 + (35 * 8)) = 29)
) T2
) T1(e_l, d_l)
inner join (
Select b, d
from p5
where ((13 - e) = c)
) T2(b_r, d_r)
on ((d_l < d_l) AND ((d_r * d_r) < 94))
) T2(d_l_r, d_r_r)
on (94 < ((22 + 43) + a_l))
) T1(a_l_l, d_l_l, d_l_r_l)
full join (
Select e, c, b, d
from p3
where (a > (c - d))
) T2(e_r, c_r, b_r, d_r)
on ((d_l_l < 16) OR (42 = 31))
) T1
union all
select e, b, d
from (
Select e, b, d
from p2
where ((87 = 66) AND (73 = a))
) T2
) T2
) T1(a_l)
inner join (
Select d_l, d_r_l_l_r, c_r_l_r
from (
Select c, b, d
from p1
where (b > 41)
) T1(c_l, b_l, d_l)
left join (
select c_r_l, d_r_l_l
from (
Select c_r_l, d_r_l_l, a_r_l_l, c_r
from (
Select d_r_l, a_r_l, c_r
from (
Select e_l_l, a_r_l, a_r, d_r
from (
Select e_l, b_l, e_r, a_r
from (
Select e, c, b
from p3
where (85 < 93)
) T1(e_l, c_l, b_l)
left join (
Select e, a
from p1
where (a = 46)
) T2(e_r, a_r)
on ((19 - e_r) = e_r)
) T1(e_l_l, b_l_l, e_r_l, a_r_l)
inner join (
Select a, d
from p5
where ((d < c) OR (a < 77))
) T2(a_r, d_r)
on (e_l_l < e_l_l)
) T1(e_l_l_l, a_r_l_l, a_r_l, d_r_l)
full join (
Select c, b, d
from p3
where ((64 = 76) AND ((85 > 45) OR ((21 < ((90 + (b + 39)) * (d + a))) AND ((25 < ((c * 72) * 49)) OR (((3 * a) = a) AND ((16 + d) > (10 - ((c * 28) * (c - c)))))))))
) T2(c_r, b_r, d_r)
on (a_r_l = (26 * a_r_l))
) T1(d_r_l_l, a_r_l_l, c_r_l)
full join (
Select e, c
from p1
where (80 > 8)
) T2(e_r, c_r)
on ((18 = 13) OR (a_r_l_l < 33))
) T1
union all
select e_l, e_r
from (
Select e_l, e_r
from (
Select e, b
from p3
where (c = 2)
) T1(e_l, b_l)
left join (
Select e
from p4
where (35 = 9)
) T2(e_r)
on (((50 * e_r) < 5) OR ((e_r + 52) = 35))
) T2
) T2(c_r_l_r, d_r_l_l_r)
on ((d_r_l_l_r = d_l) AND (38 < 24))
) T2(d_l_r, d_r_l_l_r_r, c_r_l_r_r)
on (((32 + 90) < 41) OR ((d_l_r = (45 * 77)) OR (d_r_l_l_r_r = 63)))
) T2(a_l_r, c_r_l_r_r_r, d_r_l_l_r_r_r, d_l_r_r)
on ((70 > (c_r_l_r_r_r + 9)) OR (c_r_l_r_r_r = c_r_l_r_r_r))
) T1(d_l_l, a_l_r_l, c_r_l_r_r_r_l)
full join (
Select c_l, b_l, a_r
from (
Select c, a, b
from p3
where (35 > 78)
) T1(c_l, a_l, b_l)
left join (
Select a, b
from p4
where ((b = b) OR ((76 * (b * d)) = c))
) T2(a_r, b_r)
on (b_l = a_r)
) T2(c_l_r, b_l_r, a_r_r)
on ((12 = c_l_r) AND (c_r_l_r_r_r_l = a_l_r_l))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_r_l, c_r_l, a_r_r_r
from (
Select d_l, c_r, d_r
from (
Select d
from p2
where ((15 + ((55 + 94) * c)) = a)
) T1(d_l)
inner join (
Select c, d
from p1
where ((a = a) OR (((a - (e * c)) + a) = 40))
) T2(c_r, d_r)
on ((40 < 1) OR ((13 - 17) < (91 * c_r)))
) T1(d_l_l, c_r_l, d_r_l)
full join (
Select a_l, a_r_r
from (
Select a
from p2
where (a > b)
) T1(a_l)
left join (
Select d_l, a_r, b_r, d_r
from (
Select d
from p2
where (76 = 30)
) T1(d_l)
inner join (
Select a, b, d
from p5
where (7 = e)
) T2(a_r, b_r, d_r)
on (((a_r + ((18 + d_l) - b_r)) > (a_r - 53)) OR ((d_r > b_r) AND (b_r = a_r)))
) T2(d_l_r, a_r_r, b_r_r, d_r_r)
on ((a_r_r = 83) OR ((a_r_r + 5) = 7))
) T2(a_l_r, a_r_r_r)
on ((c_r_l > 75) AND (c_r_l > 4))
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
Select e_l_r_l, c_r, b_r
from (
Select a_r_l, e_l_r
from (
Select e_l, a_l, a_r
from (
Select e, a
from p2
where (21 = (55 - b))
) T1(e_l, a_l)
inner join (
Select a
from p4
where (d < (14 + 45))
) T2(a_r)
on (a_l = a_r)
) T1(e_l_l, a_l_l, a_r_l)
inner join (
Select e_l, d_r
from (
Select e, b
from p4
where (78 = b)
) T1(e_l, b_l)
full join (
select a, d
from (
Select a, d
from p3
where (d = a)
) T1
union all
select a, b
from (
Select a, b
from p4
where ((60 = 27) OR (91 < 81))
) T2
) T2(a_r, d_r)
on (34 > d_r)
) T2(e_l_r, d_r_r)
on (a_r_l < e_l_r)
) T1(a_r_l_l, e_l_r_l)
left join (
Select c, a, b
from p4
where ((41 < (24 * (97 * a))) AND (d = (23 - d)))
) T2(c_r, a_r, b_r)
on ((38 * c_r) > 85)
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
Select d_l, a_l_r, a_r_r
from (
Select e, b, d
from p4
where (c > d)
) T1(e_l, b_l, d_l)
left join (
Select a_l, b_l, d_l, a_r
from (
Select a, b, d
from p1
where (b = b)
) T1(a_l, b_l, d_l)
left join (
Select e, a
from p2
where ((c = 24) AND ((b + 18) = 47))
) T2(e_r, a_r)
on (d_l > 3)
) T2(a_l_r, b_l_r, d_l_r, a_r_r)
on ((a_l_r > 85) AND ((a_r_r = 42) OR ((55 > a_r_r) AND ((11 = (63 - d_l)) OR ((d_l = (a_l_r - d_l)) AND (d_l = (a_r_r - (20 - a_l_r))))))))
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
Select a_l, c_r, b_r
from (
select c, a
from (
Select c, a, b
from p3
where (c < 41)
) T1
union all
select c_l, b_r_r
from (
Select c_l, b_r_r
from (
Select e, c
from p2
where (90 < 91)
) T1(e_l, c_l)
left join (
Select c_l, a_r, b_r
from (
Select c
from p3
where (21 = d)
) T1(c_l)
full join (
select a, b
from (
Select a, b
from p2
where (35 < a)
) T1
union all
select c, a
from (
Select c, a, b
from p3
where ((3 < 16) OR (41 < 74))
) T2
) T2(a_r, b_r)
on (82 = 12)
) T2(c_l_r, a_r_r, b_r_r)
on (56 = 26)
) T2
) T1(c_l, a_l)
left join (
Select c, b
from p1
where ((39 = (54 * 5)) AND ((22 = c) OR (6 > 2)))
) T2(c_r, b_r)
on ((a_l = a_l) OR (45 > b_r))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_l, d_l_l, e_r
from (
Select d_l, b_r
from (
Select d
from p2
where (((d - (58 + 62)) > 82) AND (81 = 57))
) T1(d_l)
left join (
select b
from (
Select b
from p2
where (d < d)
) T1
union all
select c_l
from (
Select c_l, a_l, e_r
from (
select c, a
from (
select c, a, d
from (
Select c, a, d
from p2
where ((14 + 45) = 89)
) T1
union all
select e, a, b
from (
Select e, a, b, d
from p4
where (75 = a)
) T2
) T1
union all
select b, d
from (
Select b, d
from p3
where (5 < (48 + 93))
) T2
) T1(c_l, a_l)
left join (
Select e, c
from p1
where ((c > (c * c)) AND (d = 26))
) T2(e_r, c_r)
on (e_r > c_l)
) T2
) T2(b_r)
on (b_r < 38)
) T1(d_l_l, b_r_l)
left join (
Select e
from p4
where (c > b)
) T2(e_r)
on (67 = b_r_l)
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
Select e
from p4
where (46 < d)
) T1(e_l)
left join (
Select e
from p1
where ((60 < 70) AND (2 < b))
) T2(e_r)
on ((68 * (91 + 16)) > e_l)
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
Select b_r_l, e_r, c_r, a_r, d_r
from (
Select e_l, a_l, b_r
from (
Select e, a, b
from p1
where (31 < 67)
) T1(e_l, a_l, b_l)
inner join (
Select b, d
from p5
where (29 = d)
) T2(b_r, d_r)
on (27 = (36 * 3))
) T1(e_l_l, a_l_l, b_r_l)
left join (
Select e, c, a, d
from p4
where ((a = 93) AND ((13 = 61) AND (25 > 70)))
) T2(e_r, c_r, a_r, d_r)
on (68 < 7)
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
Select c_l, b_l, a_l_r
from (
Select c, b
from p1
where (((((40 + b) + (47 - (81 + e))) * 5) - 36) < 47)
) T1(c_l, b_l)
full join (
select e_l, a_l, e_r
from (
Select e_l, a_l, e_r, c_r
from (
Select e, a
from p2
where ((e = (a - 63)) AND (b = a))
) T1(e_l, a_l)
left join (
Select e, c
from p1
where ((85 = 84) OR (((d + 20) = 90) OR ((84 > ((a * 91) + a)) AND (b = 33))))
) T2(e_r, c_r)
on (59 = (93 + 96))
) T1
union all
select e, c, d
from (
Select e, c, d
from p4
where (a < 1)
) T2
) T2(e_l_r, a_l_r, e_r_r)
on (c_l = 10)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_l_l, e_r, a_r
from (
Select b_r_l, e_r_l, e_r
from (
Select a_r_l, b_l_l, e_r, b_r
from (
Select a_l, b_l, a_r
from (
Select a, b
from p1
where ((88 - 33) < b)
) T1(a_l, b_l)
left join (
Select c, a, b
from p5
where ((86 = 51) AND (d = d))
) T2(c_r, a_r, b_r)
on (a_l < a_l)
) T1(a_l_l, b_l_l, a_r_l)
full join (
Select e, b
from p1
where (78 = c)
) T2(e_r, b_r)
on ((b_l_l = 1) AND (a_r_l < 52))
) T1(a_r_l_l, b_l_l_l, e_r_l, b_r_l)
left join (
select e, d
from (
Select e, d
from p2
where (d > 45)
) T1
union all
select e_l, b_l
from (
Select e_l, b_l, e_r
from (
select e, c, b
from (
Select e, c, b
from p5
where ((b = a) OR ((53 = b) AND ((13 - 96) = 85)))
) T1
union all
select a_l, b_l, b_r_l_r
from (
Select a_l, b_l, b_r_l_r, e_l_l_r
from (
Select a, b
from p3
where (e = b)
) T1(a_l, b_l)
left join (
Select b_r_l, e_l_l, d_r_r, c_r_r, d_l_r
from (
Select e_l, b_r
from (
Select e
from p4
where (b > ((2 + c) + b))
) T1(e_l)
full join (
Select e, b, d
from p2
where (10 < (e * (e + 49)))
) T2(e_r, b_r, d_r)
on ((((95 + e_l) - 69) = 91) AND (29 > 12))
) T1(e_l_l, b_r_l)
inner join (
Select e_l, d_l, e_r, c_r, d_r
from (
Select e, d
from p3
where (a = (69 + c))
) T1(e_l, d_l)
left join (
select e, c, d
from (
select e, c, d
from (
Select e, c, d
from p3
where (66 > c)
) T1
union all
select a_l_l, e_l_l, a_r
from (
Select a_l_l, e_l_l, a_r, d_r
from (
select e_l, a_l
from (
Select e_l, a_l, e_r, c_r
from (
Select e, a
from p1
where (c = (51 * (37 * c)))
) T1(e_l, a_l)
left join (
Select e, c, a
from p3
where (70 = 10)
) T2(e_r, c_r, a_r)
on (c_r < e_r)
) T1
union all
select b, d
from (
select b, d
from (
Select b, d
from p2
where ((c < e) OR (c = a))
) T1
union all
select d_l_r_l, e_r
from (
Select d_l_r_l, e_r
from (
Select c_l, d_l, d_r_r, a_r_r, d_l_r
from (
Select c, a, d
from p4
where ((0 = 59) AND (((83 - 43) - d) < e))
) T1(c_l, a_l, d_l)
full join (
Select d_l, a_r, d_r
from (
Select c, a, d
from p3
where (3 = d)
) T1(c_l, a_l, d_l)
left join (
Select c, a, d
from p4
where ((e < (c - (16 - c))) AND (((e + d) = (d * 85)) AND (26 > b)))
) T2(c_r, a_r, d_r)
on (d_r < a_r)
) T2(d_l_r, a_r_r, d_r_r)
on (27 = 95)
) T1(c_l_l, d_l_l, d_r_r_l, a_r_r_l, d_l_r_l)
left join (
Select e, c, d
from p2
where (20 < 79)
) T2(e_r, c_r, d_r)
on ((d_l_r_l = e_r) AND (36 = e_r))
) T2
) T2
) T1(e_l_l, a_l_l)
full join (
Select a, d
from p4
where ((61 - 32) = b)
) T2(a_r, d_r)
on (a_r = 25)
) T2
) T1
union all
select c, a, b
from (
Select c, a, b
from p4
where ((a > (26 - b)) OR (c < (b * 67)))
) T2
) T2(e_r, c_r, d_r)
on (15 = d_l)
) T2(e_l_r, d_l_r, e_r_r, c_r_r, d_r_r)
on ((48 + (65 + 34)) = (b_r_l * c_r_r))
) T2(b_r_l_r, e_l_l_r, d_r_r_r, c_r_r_r, d_l_r_r)
on (b_r_l_r < 73)
) T2
) T1(e_l, c_l, b_l)
full join (
Select e, d
from p5
where ((74 + 88) = c)
) T2(e_r, d_r)
on ((e_l = (65 * e_r)) AND (71 = ((14 * 47) * ((34 + 96) + e_l))))
) T2
) T2(e_r, d_r)
on (e_r_l > (e_r * 81))
) T1(b_r_l_l, e_r_l_l, e_r_l)
left join (
Select e, a, d
from p4
where (24 = (40 - d))
) T2(e_r, a_r, d_r)
on (81 < 2)
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
Select e_l, a_l, e_r, c_r, a_r
from (
Select e, a
from p1
where ((80 + (5 - c)) > 33)
) T1(e_l, a_l)
inner join (
Select e, c, a
from p5
where ((c = a) AND (b > (84 * 91)))
) T2(e_r, c_r, a_r)
on ((a_r + e_r) < 53)
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
    #**********************************************
    _testmgr.testcase_end(desc)

