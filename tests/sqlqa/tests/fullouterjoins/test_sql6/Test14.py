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
    
def test001(desc="""Joins Set 14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, e_r
from (
Select c
from p4
where (c > 7)
) T1(c_l)
inner join (
Select e
from p3
where (a = (88 - 52))
) T2(e_r)
on (80 < (c_l * e_r))
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
Select d_l, a_r
from (
Select c, d
from p4
where ((75 > 90) OR (e = 96))
) T1(c_l, d_l)
inner join (
select a
from (
Select a, b
from p1
where ((b > (31 * a)) AND ((6 < 33) OR ((e * (c + (4 - a))) = 43)))
) T1
union all
select d
from (
Select d
from p5
where ((c * 29) < 96)
) T2
) T2(a_r)
on (((49 - a_r) > 73) OR ((57 = d_l) AND (d_l < 72)))
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
Select e_l_l, a_l_l_r
from (
Select e_l, c_l, e_r
from (
select e, c
from (
Select e, c, a, b
from p3
where (87 > c)
) T1
union all
select c_l, d_r
from (
Select c_l, d_r
from (
Select e, c
from p5
where (e > d)
) T1(e_l, c_l)
left join (
Select e, a, d
from p4
where (55 = ((c + 65) * b))
) T2(e_r, a_r, d_r)
on ((61 - 36) = c_l)
) T2
) T1(e_l, c_l)
inner join (
Select e
from p1
where (99 = 12)
) T2(e_r)
on ((c_l + e_r) > e_l)
) T1(e_l_l, c_l_l, e_r_l)
full join (
select a_l_l
from (
select a_l_l
from (
Select a_l_l, a_r_l, c_r, a_r
from (
Select a_l, a_r
from (
Select e, a
from p4
where ((34 < 44) OR ((e - b) = b))
) T1(e_l, a_l)
left join (
Select a
from p4
where ((a = d) AND ((95 = 99) AND ((45 < b) OR (a = d))))
) T2(a_r)
on (a_r = a_r)
) T1(a_l_l, a_r_l)
inner join (
Select c, a
from p1
where ((b * e) > b)
) T2(c_r, a_r)
on ((97 < 82) AND ((29 = 31) OR (a_r = 59)))
) T1
union all
select e
from (
select e
from (
Select e, d
from p2
where ((43 * 42) = e)
) T1
union all
select c
from (
Select c
from p2
where (c = (93 + a))
) T2
) T2
) T1
union all
select a
from (
select a
from (
Select a
from p5
where (92 = c)
) T1
union all
select a
from (
Select a, b, d
from p2
where (c > (b * 67))
) T2
) T2
) T2(a_l_l_r)
on (((37 + a_l_l_r) > 85) AND (22 = 71))
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
Select a_l, d_r
from (
Select a
from p3
where ((96 + 2) > a)
) T1(a_l)
left join (
Select d
from p4
where (e > c)
) T2(d_r)
on ((66 = a_l) OR (d_r < 41))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_r_l, e_r_r_l_l, a_r, b_r, d_r
from (
Select e_r_r_l, a_l_r
from (
Select c_l_l, e_l_r, d_r_r, e_r_r
from (
Select c_l, a_l_r
from (
Select c, b
from p5
where (23 = 78)
) T1(c_l, b_l)
left join (
Select a_l, e_r
from (
Select e, a
from p3
where ((87 * (c * (a - d))) < ((79 * a) * b))
) T1(e_l, a_l)
left join (
Select e, c, a
from p1
where (c = 52)
) T2(e_r, c_r, a_r)
on (a_l > (e_r - 18))
) T2(a_l_r, e_r_r)
on (70 < 93)
) T1(c_l_l, a_l_r_l)
left join (
Select e_l, e_r, d_r
from (
Select e
from p4
where (((a + (((0 + 53) + 33) - 63)) < e) OR ((26 = 80) OR (3 < (e - e))))
) T1(e_l)
inner join (
Select e, c, d
from p3
where ((e < 59) OR (c > b))
) T2(e_r, c_r, d_r)
on (e_l < 75)
) T2(e_l_r, e_r_r, d_r_r)
on (60 = e_r_r)
) T1(c_l_l_l, e_l_r_l, d_r_r_l, e_r_r_l)
left join (
Select a_l, b_r_l_r
from (
Select c, a, d
from p3
where (a = 35)
) T1(c_l, a_l, d_l)
left join (
Select b_r_l, c_r
from (
Select b_r_l, d_r_l, b_r
from (
Select a_l, c_r, b_r, d_r
from (
Select c, a, b
from p3
where (10 = (73 * b))
) T1(c_l, a_l, b_l)
inner join (
Select c, b, d
from p5
where ((a = e) AND (a > 47))
) T2(c_r, b_r, d_r)
on (d_r < c_r)
) T1(a_l_l, c_r_l, b_r_l, d_r_l)
left join (
Select b
from p3
where ((16 - (b + b)) < a)
) T2(b_r)
on (95 = 59)
) T1(b_r_l_l, d_r_l_l, b_r_l)
full join (
Select e, c, a
from p1
where (e < (a + 2))
) T2(e_r, c_r, a_r)
on (97 < c_r)
) T2(b_r_l_r, c_r_r)
on (a_l > (b_r_l_r * ((a_l + 53) + a_l)))
) T2(a_l_r, b_r_l_r_r)
on ((60 + 2) > (a_l_r + e_r_r_l))
) T1(e_r_r_l_l, a_l_r_l)
full join (
Select a, b, d
from p3
where ((b + c) > e)
) T2(a_r, b_r, d_r)
on (((b_r * ((((e_r_r_l_l + (a_l_r_l - e_r_r_l_l)) + 40) + (d_r * ((a_r * 94) + d_r))) - e_r_r_l_l)) < ((47 + (24 * 77)) * (46 - 70))) AND ((b_r > e_r_r_l_l) AND (88 < 95)))
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
Select c_l_l, b_l_l, e_r
from (
select c_l, b_l
from (
Select c_l, b_l, c_r_r, d_l_r
from (
Select e, c, b
from p1
where (52 = (69 * 45))
) T1(e_l, c_l, b_l)
left join (
Select d_l, c_r
from (
Select d
from p5
where (c = 65)
) T1(d_l)
left join (
select c
from (
Select c, d
from p3
where (37 = 35)
) T1
union all
select b
from (
Select b
from p4
where (49 > b)
) T2
) T2(c_r)
on ((22 = d_l) AND (21 = d_l))
) T2(d_l_r, c_r_r)
on (((21 - 83) - c_r_r) < 28)
) T1
union all
select e, b
from (
Select e, b
from p4
where ((26 > 64) OR ((c - c) = d))
) T2
) T1(c_l_l, b_l_l)
left join (
select e
from (
Select e
from p2
where ((e > (c * e)) OR ((d = c) AND (34 = a)))
) T1
union all
select b
from (
Select b
from p2
where ((72 * (a * 56)) < ((3 - 1) + 91))
) T2
) T2(e_r)
on (12 = e_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, a_r
from (
select c, a
from (
Select c, a, b
from p5
where (((3 + (c + e)) = d) AND ((54 + b) = (91 + e)))
) T1
union all
select e, b
from (
Select e, b
from p5
where (d > e)
) T2
) T1(c_l, a_l)
inner join (
Select e, a, d
from p1
where (((a - 21) < d) AND ((e * 75) = 74))
) T2(e_r, a_r, d_r)
on (25 = 66)
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
Select e_l, d_l, e_r
from (
select e, d
from (
Select e, d
from p5
where (e < 13)
) T1
union all
select c, b
from (
Select c, b
from p1
where (31 = e)
) T2
) T1(e_l, d_l)
left join (
Select e, c
from p5
where (29 = 60)
) T2(e_r, c_r)
on ((34 - e_r) < d_l)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, c_r
from (
Select d
from p5
where (((c + (69 * (50 + 15))) > 89) AND ((e - d) = c))
) T1(d_l)
left join (
Select c, a, b
from p5
where ((65 < e) AND ((c < 75) AND ((((88 + c) * 54) - 55) = 79)))
) T2(c_r, a_r, b_r)
on (((c_r + d_l) - 6) > 23)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, c_r, d_r
from (
Select e, a
from p3
where (d > (d * 57))
) T1(e_l, a_l)
left join (
Select c, a, d
from p3
where ((13 < 40) AND ((a = 80) AND (c = 34)))
) T2(c_r, a_r, d_r)
on (((99 + (62 * (c_r * (69 - 66)))) = 55) AND ((d_r = c_r) AND (77 > c_r)))
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
Select c_l, d_l, e_r
from (
Select c, d
from p1
where ((2 - 96) < 10)
) T1(c_l, d_l)
full join (
Select e
from p3
where (c = c)
) T2(e_r)
on (15 = 19)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_r_l, b_l_l, a_r
from (
Select b_l, a_l_r
from (
Select b
from p5
where ((d < 81) OR (c < e))
) T1(b_l)
left join (
Select a_l, b_r
from (
Select a
from p5
where (17 > (b * c))
) T1(a_l)
left join (
Select b
from p5
where (a > 73)
) T2(b_r)
on (a_l > a_l)
) T2(a_l_r, b_r_r)
on (b_l > b_l)
) T1(b_l_l, a_l_r_l)
inner join (
Select a
from p4
where (((68 + d) < ((b + d) + 47)) OR (a = 26))
) T2(a_r)
on (57 < 72)
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
Select c_l, e_l_l_l_r
from (
Select e, c
from p2
where (e = c)
) T1(e_l, c_l)
left join (
Select e_l_l_l, b_r
from (
Select e_l_l, e_l_r
from (
Select e_l, b_r_r, a_r_r, b_l_r
from (
Select e
from p2
where (d > 27)
) T1(e_l)
left join (
Select b_l, a_r, b_r
from (
Select b, d
from p4
where (((50 - (d - 29)) - ((a - 93) * 87)) = 12)
) T1(b_l, d_l)
left join (
Select a, b
from p2
where (81 = e)
) T2(a_r, b_r)
on (32 = (13 + (a_r + b_r)))
) T2(b_l_r, a_r_r, b_r_r)
on (64 > 36)
) T1(e_l_l, b_r_r_l, a_r_r_l, b_l_r_l)
full join (
Select e_l, b_r
from (
Select e, c
from p5
where (b = 5)
) T1(e_l, c_l)
inner join (
Select b
from p1
where (b = 55)
) T2(b_r)
on (74 < e_l)
) T2(e_l_r, b_r_r)
on (31 = e_l_l)
) T1(e_l_l_l, e_l_r_l)
inner join (
select b
from (
Select b
from p5
where ((68 = 48) OR (d > b))
) T1
union all
select c
from (
Select c, b
from p5
where (d = (b * c))
) T2
) T2(b_r)
on (e_l_l_l = e_l_l_l)
) T2(e_l_l_l_r, b_r_r)
on ((9 - 26) < e_l_l_l_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_l, c_r_r_l, b_l_l, c_r, a_r, d_r
from (
Select a_l, b_l, c_r_r
from (
Select a, b
from p1
where ((62 = ((14 - 86) * a)) AND (e = c))
) T1(a_l, b_l)
inner join (
Select e_l, c_r
from (
Select e
from p2
where (53 < a)
) T1(e_l)
left join (
Select c
from p1
where (34 = 82)
) T2(c_r)
on ((((52 - 41) * e_l) = 48) AND ((c_r + (c_r + e_l)) < e_l))
) T2(e_l_r, c_r_r)
on (43 > 49)
) T1(a_l_l, b_l_l, c_r_r_l)
left join (
Select c, a, d
from p5
where (((83 - d) > (c * 34)) OR (c > c))
) T2(c_r, a_r, d_r)
on ((c_r < b_l_l) AND ((66 - 65) = b_l_l))
order by 1, 2, 3, 4, 5, 6
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
Select e_l, b_r_r, a_r_r
from (
Select e, a
from p4
where ((a < c) OR ((e = 77) AND (8 > d)))
) T1(e_l, a_l)
inner join (
Select a_l, a_r, b_r
from (
Select a, d
from p4
where (39 = (b * b))
) T1(a_l, d_l)
full join (
Select c, a, b
from p5
where ((b < (18 + 19)) AND (a > (36 + 63)))
) T2(c_r, a_r, b_r)
on ((a_r < b_r) AND ((96 > 84) AND (87 = 61)))
) T2(a_l_r, a_r_r, b_r_r)
on (99 = b_r_r)
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
Select c_l, d_l, e_r, b_r
from (
Select c, d
from p3
where (d = 64)
) T1(c_l, d_l)
full join (
Select e, b
from p4
where (61 > 78)
) T2(e_r, b_r)
on (b_r > 28)
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
Select b_l, a_r_r
from (
Select e, c, b
from p1
where ((33 - 47) = c)
) T1(e_l, c_l, b_l)
inner join (
Select e_l, c_r, a_r
from (
Select e
from p4
where (40 < 77)
) T1(e_l)
left join (
Select c, a
from p4
where (79 < (20 - c))
) T2(c_r, a_r)
on (c_r = 66)
) T2(e_l_r, c_r_r, a_r_r)
on (a_r_r < 47)
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
Select b_l, e_r, b_r
from (
Select c, b, d
from p2
where ((c = ((d * (21 + 29)) + (89 * c))) OR ((b < b) AND (67 < 68)))
) T1(c_l, b_l, d_l)
inner join (
Select e, a, b
from p1
where (89 = 9)
) T2(e_r, a_r, b_r)
on (34 < 27)
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
Select e_l_r_l, b_l_r
from (
Select a_l, b_l_r_r, e_l_r
from (
Select e, c, a
from p3
where ((e * 50) > e)
) T1(e_l, c_l, a_l)
left join (
Select e_l, b_r_r, b_l_r
from (
Select e, b
from p1
where ((d = (23 * (((61 * (86 * c)) * 58) + 80))) AND ((d + (5 - 89)) > ((e + c) * 12)))
) T1(e_l, b_l)
inner join (
Select b_l, b_r
from (
Select b
from p2
where (a = 14)
) T1(b_l)
full join (
Select e, b
from p1
where (b = (e * 56))
) T2(e_r, b_r)
on ((50 > 97) AND (b_r > ((b_r - 67) - b_l)))
) T2(b_l_r, b_r_r)
on (((b_l_r - 82) < b_l_r) OR (b_l_r = e_l))
) T2(e_l_r, b_r_r_r, b_l_r_r)
on (88 = a_l)
) T1(a_l_l, b_l_r_r_l, e_l_r_l)
inner join (
Select b_l, e_r
from (
Select b
from p5
where ((b < b) AND (d > (c + 76)))
) T1(b_l)
left join (
select e
from (
Select e, c
from p1
where (c > 18)
) T1
union all
select a
from (
select a
from (
Select a
from p2
where ((33 > 13) OR (42 < b))
) T1
union all
select c
from (
Select c
from p5
where (b > b)
) T2
) T2
) T2(e_r)
on ((e_r - 5) = 30)
) T2(b_l_r, e_r_r)
on (92 = 72)
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
Select c_l, d_r
from (
Select c, a
from p3
where (55 = 28)
) T1(c_l, a_l)
inner join (
Select d
from p3
where ((d = c) OR (47 < c))
) T2(d_r)
on (56 > c_l)
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
    #*************************************************
    _testmgr.testcase_end(desc)

