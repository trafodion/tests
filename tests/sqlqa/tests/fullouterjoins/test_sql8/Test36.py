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
    
def test001(desc="""Joins Set 36"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, d_r
from (
Select d
from p1
where ((15 < d) AND (((b + d) + 15) = 15))
) T1(d_l)
full join (
Select e, d
from p2
where ((1 > (d * e)) OR (c > a))
) T2(e_r, d_r)
on (((d_l * 88) = 70) OR ((48 * 66) > d_l))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l_l, c_l_r
from (
select e_l
from (
Select e_l, d_l, c_l_r
from (
Select e, d
from p3
where ((55 * c) = 49)
) T1(e_l, d_l)
left join (
Select c_l, b_l, a_r
from (
Select e, c, b, d
from p4
where (d < 59)
) T1(e_l, c_l, b_l, d_l)
inner join (
Select a, d
from p3
where (c > d)
) T2(a_r, d_r)
on (a_r > 88)
) T2(c_l_r, b_l_r, a_r_r)
on ((49 = e_l) AND (1 = (d_l * 14)))
) T1
union all
select a
from (
Select a
from p3
where (a < c)
) T2
) T1(e_l_l)
inner join (
select c_l
from (
Select c_l, a_l, b_l, e_r, c_r, d_r
from (
Select c, a, b
from p5
where ((59 = 19) OR (81 = b))
) T1(c_l, a_l, b_l)
inner join (
Select e, c, d
from p2
where (90 < a)
) T2(e_r, c_r, d_r)
on ((95 = d_r) AND (32 = d_r))
) T1
union all
select a
from (
Select a
from p2
where (64 < (a * 83))
) T2
) T2(c_l_r)
on ((c_l_r < 75) AND (85 = 34))
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
Select e_r_l, e_r
from (
Select b_l, e_r
from (
Select c, a, b
from p5
where (e < (b * c))
) T1(c_l, a_l, b_l)
full join (
Select e, a
from p2
where ((d + 17) = 21)
) T2(e_r, a_r)
on (e_r > (b_l * 21))
) T1(b_l_l, e_r_l)
left join (
Select e, a
from p3
where (37 = e)
) T2(e_r, a_r)
on (e_r = 65)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_r_r_l, e_r, d_r
from (
Select e_l, e_r_r
from (
Select e, a
from p3
where (d > a)
) T1(e_l, a_l)
left join (
Select a_r_r_l_l, e_r, b_r
from (
Select a_r_r_l, b_r_l_l, a_r_l_l_r, d_r_r
from (
select b_r_l, a_r_r
from (
select b_r_l, a_r_r
from (
select b_r_l, a_r_r
from (
Select b_r_l, a_r_r, d_r_r_l_r, e_r_r
from (
Select a_l_l, e_r, b_r
from (
Select a_l, d_l, a_r, b_r
from (
Select a, d
from p2
where (41 = b)
) T1(a_l, d_l)
left join (
Select a, b
from p2
where (8 = a)
) T2(a_r, b_r)
on (65 < b_r)
) T1(a_l_l, d_l_l, a_r_l, b_r_l)
inner join (
Select e, b
from p1
where (62 = (66 + b))
) T2(e_r, b_r)
on ((83 = 32) AND (((b_r + 24) > a_l_l) OR (89 = a_l_l)))
) T1(a_l_l_l, e_r_l, b_r_l)
left join (
Select d_r_r_l, e_r, a_r
from (
Select c_l, b_l, d_r_r, b_l_r
from (
Select c, a, b
from p4
where (b = 82)
) T1(c_l, a_l, b_l)
inner join (
Select a_l, b_l, e_r, d_r
from (
Select c, a, b
from p2
where (a > 59)
) T1(c_l, a_l, b_l)
full join (
Select e, a, d
from p1
where (42 = (d + (e - d)))
) T2(e_r, a_r, d_r)
on ((a_l > 31) AND ((e_r = 17) OR ((b_l < (d_r + 96)) OR ((5 < 56) AND ((d_r + d_r) < 26)))))
) T2(a_l_r, b_l_r, e_r_r, d_r_r)
on ((b_l * 32) = 90)
) T1(c_l_l, b_l_l, d_r_r_l, b_l_r_l)
left join (
Select e, c, a
from p5
where ((d = 7) OR ((22 < a) OR (64 > (d + e))))
) T2(e_r, c_r, a_r)
on (89 > d_r_r_l)
) T2(d_r_r_l_r, e_r_r, a_r_r)
on ((b_r_l = a_r_r) AND (d_r_r_l_r = 48))
) T1
union all
select e, c
from (
Select e, c
from p2
where (b > b)
) T2
) T1
union all
select c_l, a_l
from (
Select c_l, a_l, e_r
from (
Select c, a
from p5
where (c > 73)
) T1(c_l, a_l)
inner join (
select e
from (
select e
from (
Select e
from p5
where (e = 68)
) T1
union all
select e_l
from (
Select e_l, d_l, b_r_r, d_l_r
from (
Select e, d
from p1
where (35 < ((40 * 79) + e))
) T1(e_l, d_l)
left join (
Select d_l, b_r
from (
Select c, a, d
from p1
where ((a = e) AND (97 = a))
) T1(c_l, a_l, d_l)
left join (
select b
from (
Select b
from p3
where (e < 24)
) T1
union all
select e
from (
Select e
from p5
where (b < b)
) T2
) T2(b_r)
on ((b_r + b_r) > 25)
) T2(d_l_r, b_r_r)
on (d_l_r > d_l_r)
) T2
) T1
union all
select e
from (
Select e, c
from p2
where (16 = b)
) T2
) T2(e_r)
on ((4 = 47) AND ((a_l * c_l) > (81 + a_l)))
) T2
) T1
union all
select b, d
from (
Select b, d
from p4
where ((54 > 88) OR ((86 * 81) > 71))
) T2
) T1(b_r_l_l, a_r_r_l)
left join (
Select a_r_l_l, c_r, d_r
from (
select a_r_l
from (
select a_r_l
from (
Select a_r_l, c_r
from (
Select c_l, b_l, a_r
from (
Select c, b
from p4
where (25 > 75)
) T1(c_l, b_l)
inner join (
Select c, a
from p4
where (e = e)
) T2(c_r, a_r)
on ((c_l > (a_r + 1)) AND (c_l > b_l))
) T1(c_l_l, b_l_l, a_r_l)
left join (
Select c
from p1
where ((52 > b) OR (35 < (e + c)))
) T2(c_r)
on ((87 + c_r) > 59)
) T1
union all
select d
from (
Select d
from p5
where (a > 30)
) T2
) T1
union all
select e_l_l
from (
Select e_l_l, a_r
from (
Select e_l, a_l, e_r, c_r, a_r
from (
Select e, c, a
from p2
where (e < (29 - d))
) T1(e_l, c_l, a_l)
full join (
Select e, c, a
from p1
where ((c = 93) OR (60 < 73))
) T2(e_r, c_r, a_r)
on ((e_r > a_r) OR (e_r = 8))
) T1(e_l_l, a_l_l, e_r_l, c_r_l, a_r_l)
inner join (
Select a
from p2
where ((96 * c) = 8)
) T2(a_r)
on ((53 + 24) = a_r)
) T2
) T1(a_r_l_l)
left join (
Select c, d
from p4
where (c = (61 - 10))
) T2(c_r, d_r)
on (12 = c_r)
) T2(a_r_l_l_r, c_r_r, d_r_r)
on (91 = (a_r_l_l_r + b_r_l_l))
) T1(a_r_r_l_l, b_r_l_l_l, a_r_l_l_r_l, d_r_r_l)
full join (
Select e, b
from p1
where (d = c)
) T2(e_r, b_r)
on (40 = 91)
) T2(a_r_r_l_l_r, e_r_r, b_r_r)
on (e_r_r = e_l)
) T1(e_l_l, e_r_r_l)
full join (
Select e, b, d
from p3
where (37 = (48 * b))
) T2(e_r, b_r, d_r)
on (d_r > d_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_l, c_r, b_r
from (
Select a_l, e_r, b_r
from (
Select a
from p1
where ((91 + (b * d)) = d)
) T1(a_l)
inner join (
select e, b
from (
Select e, b, d
from p4
where ((b = 81) OR ((51 < (b - (c + b))) OR (b = 31)))
) T1
union all
select c_l, c_r
from (
Select c_l, c_r
from (
Select e, c
from p1
where (((a * 93) + 28) > e)
) T1(e_l, c_l)
left join (
Select c
from p1
where (20 = 48)
) T2(c_r)
on ((c_l * c_l) = (15 + c_r))
) T2
) T2(e_r, b_r)
on (e_r > b_r)
) T1(a_l_l, e_r_l, b_r_l)
left join (
Select c, b
from p2
where ((a > 42) OR ((a > a) AND ((b * 90) = 90)))
) T2(c_r, b_r)
on (a_l_l < ((52 + c_r) * 21))
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
Select a_l, c_r, a_r, b_r
from (
Select e, a
from p4
where (((c + (30 + 30)) = 87) OR (((74 * 96) < 86) AND ((b * (60 * 73)) > e)))
) T1(e_l, a_l)
inner join (
Select c, a, b
from p2
where ((2 = d) AND (((d - b) * (94 + (d * (70 - (12 + (24 * b)))))) < b))
) T2(c_r, a_r, b_r)
on ((50 = 83) AND ((58 > 59) AND ((24 = 99) AND ((b_r = c_r) OR ((22 < b_r) OR ((33 > a_l) AND (((60 + b_r) = 47) OR (a_r > (c_r * 43)))))))))
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
Select a_l, b_r_r
from (
Select a
from p4
where (35 > 70)
) T1(a_l)
inner join (
Select a_l, b_l, b_r
from (
Select e, a, b, d
from p5
where ((d * e) < 62)
) T1(e_l, a_l, b_l, d_l)
full join (
Select b
from p4
where (c > a)
) T2(b_r)
on ((72 - 73) < 10)
) T2(a_l_r, b_l_r, b_r_r)
on ((a_l - b_r_r) < a_l)
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
Select e_l, d_l, a_r
from (
Select e, d
from p3
where ((d * 78) > b)
) T1(e_l, d_l)
full join (
Select a
from p3
where (e < a)
) T2(a_r)
on (45 = a_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, e_r, a_r
from (
Select b
from p4
where (d = 1)
) T1(b_l)
full join (
Select e, a
from p2
where (b = 26)
) T2(e_r, a_r)
on ((60 < 9) OR (34 = a_r))
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
Select a_l, b_l, a_r_r, c_r_r
from (
Select a, b
from p1
where ((62 > 12) OR ((c = 46) AND (((10 - 31) = 17) AND (b > b))))
) T1(a_l, b_l)
inner join (
Select d_l, c_r, a_r
from (
select d
from (
Select d
from p1
where (c = 40)
) T1
union all
select e
from (
Select e, d
from p4
where ((22 * (b + 56)) = ((88 * 71) - a))
) T2
) T1(d_l)
full join (
Select c, a
from p2
where ((a * e) < d)
) T2(c_r, a_r)
on ((c_r - c_r) > 51)
) T2(d_l_r, c_r_r, a_r_r)
on ((84 = b_l) AND ((47 = a_r_r) AND (59 < (b_l * 9))))
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
Select e_l, e_r, b_r
from (
select e
from (
Select e, d
from p3
where (b = c)
) T1
union all
select b
from (
Select b
from p1
where ((c > 80) OR (e = 35))
) T2
) T1(e_l)
left join (
select e, b
from (
Select e, b, d
from p3
where ((89 < (a - 9)) AND ((b = c) AND (91 > e)))
) T1
union all
select c, b
from (
Select c, b
from p2
where (e = 53)
) T2
) T2(e_r, b_r)
on ((51 < 98) OR (((b_r + e_l) + (21 - ((e_l - e_l) * e_l))) > b_r))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_l, d_r_l, c_r_l, c_r
from (
Select d_l, c_r, b_r, d_r
from (
select d
from (
Select d
from p3
where (((((29 * e) + e) + c) > 38) OR (16 < d))
) T1
union all
select a
from (
Select a, d
from p2
where ((98 + a) = 41)
) T2
) T1(d_l)
inner join (
Select c, b, d
from p1
where ((42 * 52) > 86)
) T2(c_r, b_r, d_r)
on ((38 = 8) AND ((45 < 3) OR ((48 > d_l) OR ((0 = 51) AND (43 = ((7 - c_r) - d_l))))))
) T1(d_l_l, c_r_l, b_r_l, d_r_l)
full join (
select c
from (
Select c, d
from p1
where (a > e)
) T1
union all
select a
from (
Select a
from p1
where (44 > (c + (c + 67)))
) T2
) T2(c_r)
on ((b_r_l = b_r_l) OR ((79 = d_r_l) OR (20 > 24)))
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
Select c, d
from p5
where (c < 92)
) T1(c_l, d_l)
full join (
select a
from (
Select a
from p4
where ((d = e) AND ((98 + d) = e))
) T1
union all
select b_l_l
from (
Select b_l_l, e_l_r
from (
Select b_l, d_r_r, d_l_r
from (
select e, b
from (
Select e, b
from p3
where (76 = (a - c))
) T1
union all
select c_l_l, a_r
from (
select c_l_l, a_r
from (
Select c_l_l, a_r, d_r
from (
Select c_l, b_r
from (
Select e, c, b, d
from p4
where (22 = d)
) T1(e_l, c_l, b_l, d_l)
inner join (
select b
from (
Select b
from p4
where (((e * 82) * 35) = 27)
) T1
union all
select a_l_l
from (
Select a_l_l, c_l_l, e_r, b_r
from (
Select c_l, a_l, e_r, b_r
from (
select c, a
from (
Select c, a
from p4
where (e < a)
) T1
union all
select c_l, d_l
from (
Select c_l, d_l, c_l_r
from (
Select c, d
from p5
where (b < d)
) T1(c_l, d_l)
left join (
Select c_l, e_r, b_r
from (
Select c, b
from p2
where ((((82 + 27) * b) + e) = 21)
) T1(c_l, b_l)
inner join (
Select e, a, b
from p4
where ((98 = (((b + e) + 25) + ((e + 30) * 86))) OR (20 = c))
) T2(e_r, a_r, b_r)
on (c_l = e_r)
) T2(c_l_r, e_r_r, b_r_r)
on (((d_l * (c_l - d_l)) = 0) OR ((59 = 68) OR (((46 + (44 - d_l)) = 84) OR (78 < c_l))))
) T2
) T1(c_l, a_l)
full join (
Select e, b
from p5
where (31 > 17)
) T2(e_r, b_r)
on (78 = c_l)
) T1(c_l_l, a_l_l, e_r_l, b_r_l)
inner join (
Select e, a, b
from p2
where (31 = e)
) T2(e_r, a_r, b_r)
on (c_l_l < 70)
) T2
) T2(b_r)
on (95 < 82)
) T1(c_l_l, b_r_l)
left join (
Select c, a, d
from p3
where ((6 = a) AND (d = (0 - (9 * 34))))
) T2(c_r, a_r, d_r)
on (5 < d_r)
) T1
union all
select b, d
from (
Select b, d
from p2
where (52 = 36)
) T2
) T2
) T1(e_l, b_l)
left join (
Select d_l, d_r
from (
Select e, c, d
from p1
where (20 > d)
) T1(e_l, c_l, d_l)
inner join (
Select a, d
from p4
where (e > 35)
) T2(a_r, d_r)
on ((d_r = d_l) OR (7 < d_l))
) T2(d_l_r, d_r_r)
on ((90 > 2) AND ((d_l_r + 56) < 43))
) T1(b_l_l, d_r_r_l, d_l_r_l)
full join (
Select e_l, e_r
from (
Select e
from p5
where ((b + c) = e)
) T1(e_l)
left join (
select e
from (
Select e
from p5
where (97 = a)
) T1
union all
select e
from (
Select e, c
from p1
where ((a < d) AND (((93 + d) * ((c + e) - a)) = 84))
) T2
) T2(e_r)
on ((11 < e_r) OR (e_l = (72 - e_r)))
) T2(e_l_r, e_r_r)
on ((b_l_l < ((97 + 82) + b_l_l)) AND (b_l_l = (25 * 61)))
) T2
) T2(a_r)
on (79 = a_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_r
from (
Select a
from p1
where (a < (((a * b) - c) - 23))
) T1(a_l)
inner join (
Select d
from p1
where (28 < 53)
) T2(d_r)
on (8 = d_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, d_r
from (
Select b
from p4
where (40 < 53)
) T1(b_l)
inner join (
Select d
from p2
where (99 = c)
) T2(d_r)
on (d_r = 24)
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
Select e_l, e_r, c_r
from (
select e
from (
Select e
from p4
where (b = d)
) T1
union all
select e_l
from (
Select e_l, a_l, c_r, b_r
from (
Select e, a
from p5
where ((a = (b * d)) OR (74 < (22 - a)))
) T1(e_l, a_l)
full join (
Select e, c, b
from p4
where (c = (23 + b))
) T2(e_r, c_r, b_r)
on (a_l = 67)
) T2
) T1(e_l)
inner join (
Select e, c
from p3
where (26 = (a - (e * 13)))
) T2(e_r, c_r)
on (33 = ((c_r + e_r) * (89 * (e_r * e_r))))
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
Select e_l, c_l_r_r, a_r_r_r
from (
Select e, c, d
from p4
where (d > 92)
) T1(e_l, c_l, d_l)
left join (
Select e_l, c_l_r, a_r_r, c_r_r
from (
Select e
from p5
where (((a * 12) < a) OR ((a = 79) AND ((61 * 58) = a)))
) T1(e_l)
left join (
Select c_l, d_l, c_r, a_r, d_r
from (
Select e, c, b, d
from p5
where ((a = 72) AND (34 < 66))
) T1(e_l, c_l, b_l, d_l)
inner join (
select c, a, d
from (
select c, a, d
from (
Select c, a, d
from p1
where (5 = 97)
) T1
union all
select c, b, d
from (
Select c, b, d
from p2
where ((b = 18) OR (55 < (d + a)))
) T2
) T1
union all
select c, a, b
from (
Select c, a, b
from p4
where ((69 = d) AND ((b * 9) = 81))
) T2
) T2(c_r, a_r, d_r)
on ((14 + 66) = d_r)
) T2(c_l_r, d_l_r, c_r_r, a_r_r, d_r_r)
on ((4 = (36 * e_l)) OR (c_r_r = 14))
) T2(e_l_r, c_l_r_r, a_r_r_r, c_r_r_r)
on (98 = c_l_r_r)
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
Select c_l, b_l, b_r
from (
select c, b
from (
Select c, b, d
from p5
where ((e = 40) AND (82 < a))
) T1
union all
select a_l, e_r
from (
Select a_l, e_r
from (
Select e, c, a
from p2
where (82 > 81)
) T1(e_l, c_l, a_l)
inner join (
Select e
from p5
where (a > b)
) T2(e_r)
on (11 > 62)
) T2
) T1(c_l, b_l)
left join (
Select b
from p4
where ((4 * 77) < 64)
) T2(b_r)
on (b_l = c_l)
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
Select e_l, c_l, b_r
from (
Select e, c, a
from p1
where (8 < 84)
) T1(e_l, c_l, a_l)
inner join (
Select b
from p3
where (99 > d)
) T2(b_r)
on (30 > 70)
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
Select e_r_l, c_r
from (
Select d_l, e_r
from (
Select a, d
from p3
where (0 = (57 + (c - 72)))
) T1(a_l, d_l)
full join (
Select e
from p2
where (a = 18)
) T2(e_r)
on (93 = 8)
) T1(d_l_l, e_r_l)
left join (
select c
from (
Select c, d
from p2
where ((c = ((b - 15) * e)) AND (36 > a))
) T1
union all
select b
from (
Select b
from p4
where (85 < 44)
) T2
) T2(c_r)
on (52 = e_r_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #******************************
    _testmgr.testcase_end(desc)

