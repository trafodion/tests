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
    
def test001(desc="""Joins Set 38"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, e_r_r
from (
Select b
from p3
where (a > e)
) T1(b_l)
full join (
Select c_l_l_l, e_r, d_r
from (
Select c_l_l, c_r
from (
select c_l
from (
Select c_l, b_l, e_l_r, a_r_r
from (
Select c, b
from p1
where ((17 = 94) AND (c > d))
) T1(c_l, b_l)
full join (
Select e_l, a_r
from (
Select e
from p4
where (14 > 59)
) T1(e_l)
left join (
Select a, d
from p2
where (a = 50)
) T2(a_r, d_r)
on ((a_r = 98) AND ((a_r = e_l) OR (a_r = e_l)))
) T2(e_l_r, a_r_r)
on ((e_l_r = c_l) AND ((79 < (b_l - 38)) OR ((16 < (65 + 22)) OR (a_r_r < c_l))))
) T1
union all
select b
from (
Select b
from p3
where ((43 * 48) = (47 * 27))
) T2
) T1(c_l_l)
left join (
Select c
from p2
where ((75 > 33) AND (27 < e))
) T2(c_r)
on ((c_l_l + 97) < c_r)
) T1(c_l_l_l, c_r_l)
left join (
Select e, d
from p3
where (b < c)
) T2(e_r, d_r)
on (((69 + 77) - 52) < 49)
) T2(c_l_l_l_r, e_r_r, d_r_r)
on (b_l = 72)
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
Select d_l, b_r
from (
select c, d
from (
select c, d
from (
Select c, d
from p2
where (c > (c * 37))
) T1
union all
select a, b
from (
Select a, b
from p5
where ((60 > 19) OR (5 = (b * ((d - 48) - c))))
) T2
) T1
union all
select e, c
from (
Select e, c, b
from p2
where (c < 83)
) T2
) T1(c_l, d_l)
inner join (
Select b
from p5
where ((b < c) OR (39 > ((c * d) + 66)))
) T2(b_r)
on (44 > (b_r + 67))
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
Select e_l, b_l, d_r
from (
Select e, b
from p2
where ((54 = 65) AND ((17 * b) = d))
) T1(e_l, b_l)
inner join (
Select d
from p5
where (31 > ((19 + 90) + 87))
) T2(d_r)
on (92 > 73)
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
Select a, b
from p4
where ((a = 21) AND ((32 = b) AND (e = 28)))
) T1(a_l, b_l)
full join (
select e
from (
select e, b
from (
Select e, b, d
from p3
where ((40 < 71) AND ((59 < (e - (((96 + 4) + 93) - 98))) OR (d = a)))
) T1
union all
select a_l, c_r
from (
Select a_l, c_r
from (
Select a
from p2
where (((b - 43) < e) AND ((((10 + e) * 0) = (e - 52)) AND (((a * 17) < (d - 65)) AND ((c * e) = e))))
) T1(a_l)
full join (
Select c
from p4
where (((c * c) = (e - (d - 35))) AND (71 = a))
) T2(c_r)
on (c_r = 10)
) T2
) T1
union all
select c
from (
Select c
from p3
where ((a > d) OR (38 < 56))
) T2
) T2(e_r)
on ((95 = 69) AND (a_l = (a_l * 19)))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, e_r, d_r
from (
Select e, c, d
from p2
where (c = (c + 24))
) T1(e_l, c_l, d_l)
full join (
Select e, d
from p2
where (d = 88)
) T2(e_r, d_r)
on (((d_r * 95) < e_l) OR (d_r > e_l))
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
Select e_l, b_l, a_r
from (
Select e, a, b
from p1
where ((d = 65) AND (89 = e))
) T1(e_l, a_l, b_l)
left join (
Select c, a, b, d
from p5
where ((c > 79) AND (e > 37))
) T2(c_r, a_r, b_r, d_r)
on (31 = (94 + e_l))
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
Select b_l, e_r, a_r
from (
Select b
from p2
where (68 > (95 * d))
) T1(b_l)
inner join (
Select e, a
from p4
where (d = a)
) T2(e_r, a_r)
on ((a_r = (25 - 44)) OR ((8 - e_r) = b_l))
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
Select b_l, e_l_r_r, e_l_l_r
from (
Select b
from p4
where (e = 37)
) T1(b_l)
left join (
Select d_r_l, e_l_l, e_l_r, e_l_r_r
from (
Select e_l, d_r
from (
Select e, a
from p4
where ((74 * ((a + c) - (a - (28 * c)))) < e)
) T1(e_l, a_l)
inner join (
Select e, a, d
from p3
where ((46 + 61) = e)
) T2(e_r, a_r, d_r)
on ((61 - 7) > 18)
) T1(e_l_l, d_r_l)
inner join (
Select e_l, e_l_r, e_r_r
from (
Select e
from p3
where ((d + 88) < e)
) T1(e_l)
left join (
Select e_l, e_r
from (
Select e
from p3
where (83 > 65)
) T1(e_l)
full join (
Select e
from p4
where (c = 87)
) T2(e_r)
on ((e_l > 11) OR (e_r = 61))
) T2(e_l_r, e_r_r)
on ((95 = 40) AND ((e_l_r - ((e_l * 10) + (e_l - 12))) = 66))
) T2(e_l_r, e_l_r_r, e_r_r_r)
on ((e_l_r_r > 20) AND (e_l_r = e_l_r))
) T2(d_r_l_r, e_l_l_r, e_l_r_r, e_l_r_r_r)
on (((e_l_l_r + 62) < 4) OR (28 = 85))
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
Select e_l, b_l, c_r, b_r
from (
Select e, b, d
from p1
where (((24 * e) * e) > 27)
) T1(e_l, b_l, d_l)
inner join (
Select c, b, d
from p2
where (98 < 50)
) T2(c_r, b_r, d_r)
on ((88 + 96) = 19)
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
Select b_l, e_r
from (
Select e, b
from p4
where (59 > 22)
) T1(e_l, b_l)
left join (
select e
from (
Select e
from p1
where (31 < c)
) T1
union all
select e
from (
Select e
from p2
where ((a - c) < 72)
) T2
) T2(e_r)
on (94 > b_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, c_r
from (
Select b, d
from p3
where (((47 + 56) + d) = (73 * (e + e)))
) T1(b_l, d_l)
left join (
Select c
from p3
where ((e > (39 * c)) AND (36 > 17))
) T2(c_r)
on ((c_r = c_r) OR ((c_r = (c_r * 73)) AND (b_l = b_l)))
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
Select a_l, b_l, c_r, d_r
from (
Select a, b
from p1
where (8 = 69)
) T1(a_l, b_l)
inner join (
Select e, c, d
from p5
where (c < e)
) T2(e_r, c_r, d_r)
on ((81 + (a_l + 40)) < b_l)
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
Select c_l, a_r
from (
select c, a
from (
Select c, a, b
from p5
where (38 < 64)
) T1
union all
select b_l, e_r
from (
Select b_l, e_r
from (
Select b
from p3
where ((11 > c) AND (a > c))
) T1(b_l)
inner join (
Select e, c, d
from p4
where ((22 < e) AND (b = a))
) T2(e_r, c_r, d_r)
on ((e_r = b_l) OR (96 < e_r))
) T2
) T1(c_l, a_l)
full join (
Select c, a
from p1
where (((23 + b) = 27) OR (15 < 61))
) T2(c_r, a_r)
on ((a_r = a_r) OR (22 > 3))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, c_r, b_r
from (
Select b
from p2
where ((d < a) AND (62 = (e + 38)))
) T1(b_l)
inner join (
Select e, c, b
from p5
where (25 = c)
) T2(e_r, c_r, b_r)
on (b_l = 92)
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
Select d_l, a_r_r
from (
Select d
from p5
where ((c > 60) AND ((c < 75) AND (e = 3)))
) T1(d_l)
left join (
Select e_l, c_l, a_r
from (
select e, c
from (
Select e, c
from p2
where ((e > 48) OR ((13 * 51) > (94 * c)))
) T1
union all
select b_l, d_r
from (
Select b_l, d_r
from (
Select a, b, d
from p2
where ((47 + e) > (58 + 59))
) T1(a_l, b_l, d_l)
left join (
Select d
from p4
where (b > b)
) T2(d_r)
on (38 > (27 * 13))
) T2
) T1(e_l, c_l)
left join (
Select a
from p2
where (((d + 89) = a) OR (d > 77))
) T2(a_r)
on ((c_l = 53) OR (a_r = 19))
) T2(e_l_r, c_l_r, a_r_r)
on ((65 - (d_l - d_l)) = 94)
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
Select e_l, b_l, d_r
from (
Select e, c, b
from p4
where (85 = ((b + 24) - 24))
) T1(e_l, c_l, b_l)
inner join (
Select e, d
from p2
where ((a = e) OR (90 < 45))
) T2(e_r, d_r)
on ((d_r < d_r) OR (d_r > 14))
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
Select e_l, d_l, e_r, a_r, d_r
from (
select e, d
from (
Select e, d
from p2
where (39 = 95)
) T1
union all
select c, d
from (
Select c, d
from p5
where (d = d)
) T2
) T1(e_l, d_l)
left join (
Select e, a, d
from p5
where ((b > 89) AND ((e = c) AND ((a < 75) OR ((a = e) AND (48 = 45)))))
) T2(e_r, a_r, d_r)
on ((67 < e_r) AND (e_l > d_r))
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_r
from (
Select e, a
from p1
where (81 < (((e * 42) + (12 - ((a + d) + (b - 88)))) + (8 * c)))
) T1(e_l, a_l)
full join (
Select d
from p4
where ((a = 74) OR ((14 > 56) OR ((55 = (52 * 94)) AND (42 > 25))))
) T2(d_r)
on (((d_r * 68) < (14 - ((d_r - 60) + d_r))) AND (d_r = e_l))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, d_l, d_r
from (
Select b, d
from p5
where (62 = d)
) T1(b_l, d_l)
left join (
Select d
from p3
where ((b = a) OR ((14 > ((e + 3) - 23)) AND (48 = 77)))
) T2(d_r)
on (60 = d_l)
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
Select d_r_l, a_r_l, e_l_r, a_r_r
from (
Select a_l, a_r, d_r
from (
Select e, a
from p1
where ((c - e) > a)
) T1(e_l, a_l)
inner join (
Select a, d
from p1
where (32 = c)
) T2(a_r, d_r)
on (a_l < a_l)
) T1(a_l_l, a_r_l, d_r_l)
left join (
Select e_l, a_r
from (
select e
from (
Select e, b, d
from p4
where (62 < 75)
) T1
union all
select e
from (
Select e
from p5
where (42 > e)
) T2
) T1(e_l)
left join (
Select a
from p4
where ((74 = (d * (d * b))) AND (b < ((44 - d) - b)))
) T2(a_r)
on ((e_l < e_l) OR (39 = 42))
) T2(e_l_r, a_r_r)
on (d_r_l = 32)
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
    #****************************
    _testmgr.testcase_end(desc)

