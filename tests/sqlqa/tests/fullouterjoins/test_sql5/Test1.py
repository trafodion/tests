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
    
def test001(desc="""Joins Set 1"""):
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
from p3
where ((c = (36 * c)) AND (15 < e))
) T1(d_l)
left join (
Select e, a, b, d
from p1
where (34 > b)
) T2(e_r, a_r, b_r, d_r)
on ((81 = 67) AND ((37 < d_l) OR (d_r < d_l)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, c_l, a_l_r, c_r_r
from (
Select e, c
from p2
where ((67 < c) OR (19 < (e - e)))
) T1(e_l, c_l)
left join (
Select e_l, a_l, b_l, c_r
from (
select e, a, b
from (
Select e, a, b
from p2
where (32 > e)
) T1
union all
select a, b, d
from (
Select a, b, d
from p5
where (e = 64)
) T2
) T1(e_l, a_l, b_l)
inner join (
Select c, b
from p5
where ((6 > d) AND (((71 + 43) = c) OR ((76 = c) AND (e = 22))))
) T2(c_r, b_r)
on (b_l = c_r)
) T2(e_l_r, a_l_r, b_l_r, c_r_r)
on (c_r_r < a_l_r)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, c_r
from (
Select e, c
from p3
where (a < 55)
) T1(e_l, c_l)
left join (
select c
from (
Select c
from p4
where (e > d)
) T1
union all
select a
from (
Select a, d
from p3
where (9 > c)
) T2
) T2(c_r)
on (c_r = 91)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, c_r
from (
Select e
from p3
where ((88 > a) OR (95 = c))
) T1(e_l)
full join (
Select c
from p1
where (b < 42)
) T2(c_r)
on ((26 = (e_l - c_r)) AND ((c_r * e_l) = c_r))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, e_r
from (
Select d
from p2
where (89 = e)
) T1(d_l)
inner join (
Select e, d
from p1
where (((30 - 52) = c) AND ((12 = 82) AND ((d * (36 * 72)) > c)))
) T2(e_r, d_r)
on (d_l > (62 + d_l))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, c_r
from (
Select c, a, d
from p5
where ((52 < 30) OR (((((((97 - d) - 43) - (((86 - b) + c) - e)) + d) * 71) = 55) AND ((c < ((45 - c) + 50)) AND ((42 = (e + (d + b))) AND (((32 * (44 - (64 - (78 + 11)))) < 87) OR ((d = a) AND ((56 < b) OR (22 > 28))))))))
) T1(c_l, a_l, d_l)
left join (
Select c, a
from p2
where (((4 - (b + ((e * 48) - d))) = d) OR ((d - 72) > ((72 - (23 - c)) * d)))
) T2(c_r, a_r)
on ((67 + c_l) > c_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l, d_l, d_r
from (
Select c, b, d
from p4
where (((39 + (85 + a)) > ((69 + d) + (c * e))) OR (((c * 51) > d) AND (a < 72)))
) T1(c_l, b_l, d_l)
left join (
Select d
from p3
where (((2 + ((43 + 65) - 9)) > 83) OR (46 < (d + b)))
) T2(d_r)
on (30 = c_l)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, e_r
from (
Select e, a, d
from p5
where (35 = a)
) T1(e_l, a_l, d_l)
full join (
Select e
from p4
where (((38 + ((10 - (90 * 77)) + 64)) + a) = (a + 60))
) T2(e_r)
on ((d_l = e_l) OR ((e_r = e_r) AND ((39 = e_r) AND ((e_l = d_l) OR ((d_l + 90) = 78)))))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_r_l_r_l_l, e_r_l, e_r, a_r
from (
Select a_r_l_r_l, d_l_l, e_r, b_r
from (
Select d_l, a_r_l_r
from (
Select d
from p4
where ((67 > 10) AND (25 > 56))
) T1(d_l)
full join (
Select a_r_l, c_r_l, d_r_r
from (
Select b_l, c_r, a_r
from (
Select e, c, a, b
from p1
where ((c > a) OR (b = (e * (e + b))))
) T1(e_l, c_l, a_l, b_l)
inner join (
Select e, c, a, b
from p4
where ((79 > (a - 62)) OR (a = a))
) T2(e_r, c_r, a_r, b_r)
on (28 > 98)
) T1(b_l_l, c_r_l, a_r_l)
left join (
Select e_l_l, d_r
from (
Select e_l, e_r
from (
Select e
from p2
where ((43 - 16) < 17)
) T1(e_l)
full join (
Select e, d
from p4
where ((37 + (89 - (a + 44))) < (12 + 73))
) T2(e_r, d_r)
on (e_l < 29)
) T1(e_l_l, e_r_l)
full join (
Select d
from p2
where ((12 = 45) OR ((8 = 89) AND (e = 79)))
) T2(d_r)
on (e_l_l = 14)
) T2(e_l_l_r, d_r_r)
on (a_r_l = 93)
) T2(a_r_l_r, c_r_l_r, d_r_r_r)
on (53 < a_r_l_r)
) T1(d_l_l, a_r_l_r_l)
inner join (
Select e, b
from p4
where (10 = ((47 + 39) + 67))
) T2(e_r, b_r)
on ((((e_r * 53) * e_r) = (b_r * 72)) AND (28 = d_l_l))
) T1(a_r_l_r_l_l, d_l_l_l, e_r_l, b_r_l)
full join (
Select e, c, a
from p1
where (e = (c + d))
) T2(e_r, c_r, a_r)
on ((87 + 14) = 28)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l_r_l, a_l_l, d_l_l, a_r
from (
Select a_l, d_l, b_l_r
from (
Select a, d
from p2
where ((c = (e - 67)) OR (33 = c))
) T1(a_l, d_l)
left join (
Select b_l, b_r
from (
Select b, d
from p1
where (c = 35)
) T1(b_l, d_l)
left join (
Select e, b
from p1
where (b < (b + 26))
) T2(e_r, b_r)
on ((b_l - 66) < b_r)
) T2(b_l_r, b_r_r)
on (99 = a_l)
) T1(a_l_l, d_l_l, b_l_r_l)
left join (
select a
from (
select a
from (
Select a
from p4
where (16 < 61)
) T1
union all
select d_r_r_l_l
from (
Select d_r_r_l_l, c_r_l, b_l_r
from (
Select c_r_r_l_r_r_l_r_l, d_r_r_l, c_r
from (
Select e_l, c_r_r_l_r_r_l_r, d_r_r
from (
Select e, a
from p1
where (20 > 85)
) T1(e_l, a_l)
left join (
Select c_r_r_l_r_r_l, d_r
from (
Select b_l_l, c_r_r_l_r_r
from (
Select b_l, a_r_r, b_l_r
from (
Select b
from p4
where ((25 > 65) AND ((a - a) > 0))
) T1(b_l)
left join (
Select b_l, a_r
from (
Select b
from p1
where (17 < ((24 * 89) - d))
) T1(b_l)
full join (
Select a
from p4
where (32 = 55)
) T2(a_r)
on (74 < b_l)
) T2(b_l_r, a_r_r)
on ((b_l = b_l_r) OR (49 < 44))
) T1(b_l_l, a_r_r_l, b_l_r_l)
left join (
Select e_l, d_l, a_r_r, c_r_r_l_r
from (
Select e, d
from p4
where (b = 2)
) T1(e_l, d_l)
left join (
Select c_r_r_l, a_r, d_r
from (
Select b_l, d_l, a_r_r, c_r_r
from (
Select a, b, d
from p3
where (e < (c - 43))
) T1(a_l, b_l, d_l)
inner join (
Select e_l, c_r, a_r
from (
Select e
from p5
where ((c = 87) AND (a = (a + c)))
) T1(e_l)
left join (
Select e, c, a
from p1
where ((28 = c) AND (79 < e))
) T2(e_r, c_r, a_r)
on (e_l > 96)
) T2(e_l_r, c_r_r, a_r_r)
on ((d_l = b_l) OR (52 < d_l))
) T1(b_l_l, d_l_l, a_r_r_l, c_r_r_l)
inner join (
Select c, a, d
from p1
where (62 < e)
) T2(c_r, a_r, d_r)
on ((74 = d_r) OR ((d_r > d_r) AND (d_r = (a_r * c_r_r_l))))
) T2(c_r_r_l_r, a_r_r, d_r_r)
on ((d_l = e_l) OR (c_r_r_l_r < d_l))
) T2(e_l_r, d_l_r, a_r_r_r, c_r_r_l_r_r)
on ((b_l_l = 78) OR ((c_r_r_l_r_r = 83) OR (b_l_l = 24)))
) T1(b_l_l_l, c_r_r_l_r_r_l)
full join (
Select e, c, b, d
from p3
where (a < a)
) T2(e_r, c_r, b_r, d_r)
on (93 > c_r_r_l_r_r_l)
) T2(c_r_r_l_r_r_l_r, d_r_r)
on (d_r_r = d_r_r)
) T1(e_l_l, c_r_r_l_r_r_l_r_l, d_r_r_l)
full join (
Select c
from p2
where (1 = 36)
) T2(c_r)
on ((((50 - 96) + c_r) * c_r) > c_r_r_l_r_r_l_r_l)
) T1(c_r_r_l_r_r_l_r_l_l, d_r_r_l_l, c_r_l)
left join (
Select e_l, b_l, a_r
from (
Select e, c, b
from p5
where ((27 = e) AND ((d * (d + 78)) < (e - (4 * 50))))
) T1(e_l, c_l, b_l)
left join (
Select e, c, a
from p3
where (61 > 28)
) T2(e_r, c_r, a_r)
on ((1 < 50) AND (a_r < 44))
) T2(e_l_r, b_l_r, a_r_r)
on (b_l_r > b_l_r)
) T2
) T1
union all
select e
from (
Select e, d
from p5
where (a = e)
) T2
) T2(a_r)
on (87 = 80)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, e_r, c_r
from (
Select c, b
from p3
where (((e - 78) = c) OR ((e < 68) AND (15 = (71 * (e - 18)))))
) T1(c_l, b_l)
full join (
Select e, c
from p2
where (e > (d * d))
) T2(e_r, c_r)
on (59 = 46)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_l, d_r
from (
Select e, b
from p3
where (79 = 41)
) T1(e_l, b_l)
left join (
Select d
from p4
where (c < 2)
) T2(d_r)
on ((34 = e_l) AND (52 = e_l))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_r_l, a_r
from (
Select c_l, b_r_r, e_l_r
from (
select c, a
from (
Select c, a
from p2
where (54 = c)
) T1
union all
select b_l, d_r
from (
Select b_l, d_r
from (
Select c, a, b
from p5
where ((31 > 15) AND (26 < (d - e)))
) T1(c_l, a_l, b_l)
inner join (
Select e, d
from p2
where (((32 - e) = a) OR ((c = 35) AND (0 = 26)))
) T2(e_r, d_r)
on ((d_r + b_l) < (23 + b_l))
) T2
) T1(c_l, a_l)
left join (
Select e_l, b_r
from (
Select e, a, d
from p5
where (59 = c)
) T1(e_l, a_l, d_l)
inner join (
Select b
from p3
where ((10 + a) > c)
) T2(b_r)
on (((b_r + b_r) < 16) OR (e_l = 96))
) T2(e_l_r, b_r_r)
on (20 = b_r_r)
) T1(c_l_l, b_r_r_l, e_l_r_l)
full join (
Select a
from p3
where ((57 = c) OR (a < a))
) T2(a_r)
on (b_r_r_l < 62)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l_l, a_r, d_r
from (
select b_l, d_l, d_r_r, a_l_l_r
from (
Select b_l, d_l, d_r_r, a_l_l_r
from (
Select b, d
from p4
where ((a = a) AND (d = 3))
) T1(b_l, d_l)
inner join (
Select a_l_l, d_r
from (
Select a_l, b_l, c_r
from (
Select a, b
from p1
where ((61 + (b - 19)) = b)
) T1(a_l, b_l)
inner join (
Select c
from p1
where ((75 > 54) AND (47 > d))
) T2(c_r)
on (92 < a_l)
) T1(a_l_l, b_l_l, c_r_l)
full join (
Select d
from p4
where ((71 < 35) AND (90 < (c + d)))
) T2(d_r)
on (32 > d_r)
) T2(a_l_l_r, d_r_r)
on ((70 * d_l) > d_r_r)
) T1
union all
select e_l, a_l, d_l, a_l_r
from (
Select e_l, a_l, d_l, a_l_r, b_r_r_r
from (
Select e, a, b, d
from p4
where (b = (94 + 94))
) T1(e_l, a_l, b_l, d_l)
left join (
Select a_l, d_l, b_r_r
from (
Select e, a, d
from p3
where (b = b)
) T1(e_l, a_l, d_l)
full join (
Select e_l_l, b_l_l, c_r, b_r
from (
Select e_l, b_l, c_r_r
from (
Select e, c, a, b
from p3
where ((b = 19) OR (73 < 43))
) T1(e_l, c_l, a_l, b_l)
left join (
Select e_l, d_l, c_r
from (
Select e, c, d
from p5
where (b = 91)
) T1(e_l, c_l, d_l)
left join (
Select c
from p2
where (98 = 17)
) T2(c_r)
on ((22 - 32) = 30)
) T2(e_l_r, d_l_r, c_r_r)
on (b_l = b_l)
) T1(e_l_l, b_l_l, c_r_r_l)
inner join (
select c, b
from (
Select c, b
from p4
where ((d + ((50 * 4) + 3)) > (65 + 86))
) T1
union all
select e, b
from (
Select e, b, d
from p3
where ((41 = 97) AND (c = 12))
) T2
) T2(c_r, b_r)
on (((b_r - 58) = 4) AND ((c_r < 90) AND ((b_r < (c_r * 72)) AND ((e_l_l < ((85 - c_r) + c_r)) OR (c_r = c_r)))))
) T2(e_l_l_r, b_l_l_r, c_r_r, b_r_r)
on ((99 < 46) AND ((a_l < 10) AND ((a_l < (d_l * (44 * a_l))) AND (d_l < a_l))))
) T2(a_l_r, d_l_r, b_r_r_r)
on (((98 * (e_l - 56)) = d_l) AND ((d_l * (92 + a_l_r)) = e_l))
) T2
) T1(b_l_l, d_l_l, d_r_r_l, a_l_l_r_l)
left join (
Select c, a, d
from p2
where (d > a)
) T2(c_r, a_r, d_r)
on ((b_l_l > b_l_l) OR (a_r > 87))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, c_r, b_r
from (
Select e
from p5
where (b = 60)
) T1(e_l)
left join (
Select c, b, d
from p2
where (38 = b)
) T2(c_r, b_r, d_r)
on (96 > 11)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, d_l, b_r, d_r
from (
select c, d
from (
select c, d
from (
Select c, d
from p1
where ((81 = (b + d)) AND ((98 = 23) OR ((((((a - b) + 23) - 86) - 69) = 93) OR ((95 + b) < 72))))
) T1
union all
select e, c
from (
Select e, c, d
from p1
where (((29 - c) = 52) AND ((33 < 50) AND (c < 7)))
) T2
) T1
union all
select e, a
from (
select e, a, b
from (
Select e, a, b
from p2
where (e = a)
) T1
union all
select e, c, b
from (
Select e, c, b
from p1
where ((96 = 45) OR ((83 = ((a - d) + e)) OR (((48 * 6) = 68) OR ((e - 34) = 82))))
) T2
) T2
) T1(c_l, d_l)
full join (
Select a, b, d
from p2
where (c > (90 - b))
) T2(a_r, b_r, d_r)
on (11 < 66)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_r
from (
Select c
from p5
where (((15 - (62 * (a * 39))) * 45) = (e * (7 * 34)))
) T1(c_l)
left join (
Select e, b
from p3
where ((d = (c - e)) OR (a = 84))
) T2(e_r, b_r)
on (((86 * 0) = c_l) AND (c_l > 9))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_r, d_r
from (
Select c
from p5
where (((c - 41) - b) > b)
) T1(c_l)
inner join (
Select b, d
from p5
where (14 < (22 - 67))
) T2(b_r, d_r)
on (44 = 7)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_r
from (
Select e, a
from p3
where (c > (1 - 37))
) T1(e_l, a_l)
left join (
Select a
from p2
where (b > 83)
) T2(a_r)
on (19 > 28)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_r_l, d_r
from (
Select a_l, b_l, c_r, a_r
from (
select a, b
from (
Select a, b
from p1
where (14 = a)
) T1
union all
select a_l, b_l
from (
select a_l, b_l, d_l, c_r
from (
Select a_l, b_l, d_l, c_r
from (
Select c, a, b, d
from p3
where (c = 18)
) T1(c_l, a_l, b_l, d_l)
inner join (
Select e, c
from p1
where (d = d)
) T2(e_r, c_r)
on ((96 > 75) AND (((b_l + b_l) * d_l) > 21))
) T1
union all
select e, c, a, d
from (
Select e, c, a, d
from p4
where ((11 = c) AND (((9 + a) < b) AND (50 = (c - b))))
) T2
) T2
) T1(a_l, b_l)
full join (
Select c, a, d
from p5
where ((e > 24) AND ((a < 62) AND ((60 * a) = 15)))
) T2(c_r, a_r, d_r)
on (((86 + a_r) + 57) = 40)
) T1(a_l_l, b_l_l, c_r_l, a_r_l)
left join (
Select a, d
from p5
where (24 = 68)
) T2(a_r, d_r)
on ((50 < c_r_l) AND ((c_r_l < 1) OR ((d_r < 37) AND (d_r = (c_r_l - ((56 * d_r) + 69))))))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

