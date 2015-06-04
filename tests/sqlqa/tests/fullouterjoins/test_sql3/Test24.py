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
select e, d
from (
Select e, d
from t4
where (4 = 58)
) T1
union all
select e, c
from (
Select e, c
from t4
where (c > 59)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c
from t4
where (a = a)
) T1
union all
select e
from (
Select e
from t4
where (b = e)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l, d_l
from (
Select b_l, d_l, e_r, a_r, b_r
from (
Select b, d
from t4
where ((45 + d) = (d + c))
) T1(b_l, d_l)
left join (
Select e, a, b
from t3
where ((27 - (24 + (((c * 19) * 98) - (35 - a)))) < (b + (d * c)))
) T2(e_r, a_r, b_r)
on (66 = ((80 + 64) - (76 * 89)))
) T1
union all
select e, c
from (
Select e, c
from t4
where (c < 0)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, e_r
from (
Select e_l, e_r
from (
Select e
from t2
where (e > 13)
) T1(e_l)
full join (
Select e
from t1
where (a = a)
) T2(e_r)
on (27 = e_l)
) T1
union all
select e, c
from (
Select e, c
from t5
where (61 = a)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t5
where ((c * 4) < (c * 4))
) T1
union all
select c
from (
Select c
from t3
where ((b - b) < (a * (8 + c)))
) T2
order by 1
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
select b_l, c_r
from (
Select b_l, c_r
from (
Select c, b
from t4
where (9 > (42 - (e - (18 * 65))))
) T1(c_l, b_l)
left join (
Select c, b
from t5
where (b = 45)
) T2(c_r, b_r)
on ((38 * (b_l * 13)) = b_l)
) T1
union all
select c_l, d_r_l_r_l_r_r
from (
Select c_l, d_r_l_r_l_r_r, e_r_l_l_l_r
from (
Select c
from t3
where ((c + 26) < ((b * 25) * a))
) T1(c_l)
left join (
Select e_r_l_l_l, d_r_l_r_l_r
from (
Select e_r_l_l, d_r
from (
Select c_r_l, e_r_l, c_r
from (
Select a_l, e_r, c_r
from (
Select e, a, d
from t2
where (c = b)
) T1(e_l, a_l, d_l)
left join (
Select e, c, a
from t4
where (58 = 68)
) T2(e_r, c_r, a_r)
on (((77 * 3) * 95) = a_l)
) T1(a_l_l, e_r_l, c_r_l)
left join (
Select c
from t1
where ((78 + 51) = e)
) T2(c_r)
on (c_r < 61)
) T1(c_r_l_l, e_r_l_l, c_r_l)
full join (
Select d
from t2
where (c < (a - 44))
) T2(d_r)
on (d_r > (46 - 11))
) T1(e_r_l_l_l, d_r_l)
inner join (
Select e_l_l, d_r_l_r_l, e_l_r
from (
Select e_l, c_l, a_r_r, c_r_l_r, d_r_l_r
from (
Select e, c, a
from t3
where (d = 93)
) T1(e_l, c_l, a_l)
inner join (
Select d_r_l, c_r_l, a_r
from (
Select a_l, b_l, e_r, c_r, d_r
from (
Select a, b
from t3
where ((41 - 78) = 14)
) T1(a_l, b_l)
left join (
Select e, c, b, d
from t2
where (20 < (14 - b))
) T2(e_r, c_r, b_r, d_r)
on (b_l = (((a_l - (18 - 11)) * e_r) * a_l))
) T1(a_l_l, b_l_l, e_r_l, c_r_l, d_r_l)
left join (
Select e, c, a
from t1
where (10 = c)
) T2(e_r, c_r, a_r)
on (d_r_l > c_r_l)
) T2(d_r_l_r, c_r_l_r, a_r_r)
on (15 < ((1 - 24) + a_r_r))
) T1(e_l_l, c_l_l, a_r_r_l, c_r_l_r_l, d_r_l_r_l)
full join (
select e_l, c_l
from (
Select e_l, c_l, a_l_r
from (
Select e, c, d
from t3
where ((15 - 35) < 86)
) T1(e_l, c_l, d_l)
left join (
select a_l, b_l
from (
select a_l, b_l
from (
select a_l, b_l, c_r
from (
Select a_l, b_l, c_r
from (
Select e, a, b, d
from t3
where (b > (11 * 41))
) T1(e_l, a_l, b_l, d_l)
left join (
Select c
from t1
where (9 = 34)
) T2(c_r)
on ((c_r * 93) = c_r)
) T1
union all
select b_r_l_l, c_r, a_r
from (
Select b_r_l_l, c_r, a_r
from (
Select b_r_l, d_l_l_l, c_r_l_l, e_r, b_r
from (
select c_r_l, d_l_l, b_r
from (
Select c_r_l, d_l_l, b_r
from (
Select c_l, d_l, c_r
from (
Select c, a, d
from t3
where ((e * d) < (43 + (14 + 74)))
) T1(c_l, a_l, d_l)
full join (
Select c
from t3
where (a < (a + 4))
) T2(c_r)
on ((64 + d_l) = c_r)
) T1(c_l_l, d_l_l, c_r_l)
left join (
Select b
from t4
where (c < 63)
) T2(b_r)
on (d_l_l < b_r)
) T1
union all
select c, a, d
from (
Select c, a, d
from t3
where (7 > c)
) T2
) T1(c_r_l_l, d_l_l_l, b_r_l)
full join (
Select e, b
from t2
where (e > e)
) T2(e_r, b_r)
on (44 = d_l_l_l)
) T1(b_r_l_l, d_l_l_l_l, c_r_l_l_l, e_r_l, b_r_l)
inner join (
Select c, a
from t5
where (b = b)
) T2(c_r, a_r)
on (48 > c_r)
) T2
) T1
union all
select e, a
from (
Select e, a
from t3
where ((((20 * e) - d) - e) > e)
) T2
) T1
union all
select e, c
from (
Select e, c, a, d
from t4
where (77 > a)
) T2
) T2(a_l_r, b_l_r)
on ((c_l - a_l_r) > 97)
) T1
union all
select e, a
from (
Select e, a
from t3
where (48 < e)
) T2
) T2(e_l_r, c_l_r)
on (e_l_l < (d_r_l_r_l + 85))
) T2(e_l_l_r, d_r_l_r_l_r, e_l_r_r)
on (9 = d_r_l_r_l_r)
) T2(e_r_l_l_l_r, d_r_l_r_l_r_r)
on (22 = 24)
) T2
order by 1, 2
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
select a, b, d
from (
Select a, b, d
from t4
where ((68 - 2) = 37)
) T1
union all
select b_r_l_l, e_r_l, e_r
from (
Select b_r_l_l, e_r_l, e_r, b_r
from (
Select b_r_l, e_r
from (
Select c_l, c_r, b_r
from (
Select c
from t2
where (36 = 47)
) T1(c_l)
inner join (
Select c, b
from t5
where (d > e)
) T2(c_r, b_r)
on (c_l < (b_r * 85))
) T1(c_l_l, c_r_l, b_r_l)
left join (
Select e, c, a
from t1
where ((a - 73) = a)
) T2(e_r, c_r, a_r)
on (88 > 99)
) T1(b_r_l_l, e_r_l)
left join (
Select e, b
from t2
where ((d * 63) > 52)
) T2(e_r, b_r)
on (b_r_l_l > ((54 + 90) * 65))
) T2
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
select c
from (
select c
from (
Select c
from t4
where (((94 * d) - (53 * 63)) = (b * a))
) T1
union all
select e
from (
Select e, d
from t2
where (57 = 0)
) T2
) T1
union all
select c
from (
Select c
from t3
where (18 = (c + c))
) T2
order by 1
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
select c, a
from (
select c, a
from (
Select c, a, b
from t4
where (62 = 41)
) T1
union all
select c, a
from (
Select c, a
from t3
where (d = (e * b))
) T2
) T1
union all
select b_l, a_r
from (
Select b_l, a_r
from (
Select b, d
from t3
where (c < 24)
) T1(b_l, d_l)
left join (
Select a
from t1
where (64 = (a * 6))
) T2(a_r)
on (89 = 79)
) T2
order by 1, 2
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
select c, a
from (
Select c, a
from t1
where (43 < 48)
) T1
union all
select b_r_l, c_l_l_r
from (
Select b_r_l, c_l_l_r
from (
Select e_l_r_l_l, e_r_l, e_r, b_r
from (
Select e_l_r_l, e_r, b_r
from (
Select a_l, e_l_r, a_r_r
from (
Select c, a, b
from t5
where ((e * ((44 - (89 * (77 * (85 * d)))) - 54)) = 32)
) T1(c_l, a_l, b_l)
inner join (
Select e_l, a_r
from (
select e
from (
Select e, c
from t2
where (((70 * 0) + c) > d)
) T1
union all
select a_l_r_l
from (
select a_l_r_l
from (
Select a_l_r_l, a_r_r_l_l, b_l_r, d_l_r
from (
Select c_l_l, a_r_r_l, a_l_r, c_l_r, e_r_r
from (
Select c_l, a_r_r
from (
Select c, b
from t2
where (((b - a) - 82) = (c * 83))
) T1(c_l, b_l)
left join (
Select d_l, a_r
from (
Select d
from t5
where (72 < a)
) T1(d_l)
inner join (
Select a, d
from t5
where (27 = e)
) T2(a_r, d_r)
on (45 = a_r)
) T2(d_l_r, a_r_r)
on (c_l = 39)
) T1(c_l_l, a_r_r_l)
left join (
select c_l, a_l, e_r
from (
Select c_l, a_l, e_r, b_r
from (
Select e, c, a, d
from t1
where (b = 79)
) T1(e_l, c_l, a_l, d_l)
left join (
Select e, b, d
from t4
where (a = b)
) T2(e_r, b_r, d_r)
on (19 > a_l)
) T1
union all
select a_l, a_r, b_r
from (
Select a_l, a_r, b_r
from (
Select a
from t4
where (72 = a)
) T1(a_l)
left join (
Select a, b
from t1
where (e = c)
) T2(a_r, b_r)
on (30 = b_r)
) T2
) T2(c_l_r, a_l_r, e_r_r)
on (c_l_r > (a_r_r_l * c_l_l))
) T1(c_l_l_l, a_r_r_l_l, a_l_r_l, c_l_r_l, e_r_r_l)
inner join (
select b_l, d_l
from (
Select b_l, d_l, a_r_r, a_l_l_r, a_r_r_l_r
from (
Select b, d
from t5
where (((38 * 50) * 94) > 36)
) T1(b_l, d_l)
left join (
Select a_l_l, a_r_r_l, d_l_r_l, a_r
from (
Select a_l, a_r_r, d_l_r
from (
Select c, a
from t2
where (e < 19)
) T1(c_l, a_l)
left join (
Select d_l, a_r, b_r
from (
Select c, d
from t3
where ((a - 22) = 34)
) T1(c_l, d_l)
full join (
select a, b, d
from (
Select a, b, d
from t3
where (b = (22 + (e + 50)))
) T1
union all
select e, a, b
from (
Select e, a, b
from t1
where (14 = (31 - c))
) T2
) T2(a_r, b_r, d_r)
on (88 = a_r)
) T2(d_l_r, a_r_r, b_r_r)
on ((a_l + 4) > a_l)
) T1(a_l_l, a_r_r_l, d_l_r_l)
full join (
Select a
from t5
where (((40 * 9) - (63 - b)) = 34)
) T2(a_r)
on (d_l_r_l = a_l_l)
) T2(a_l_l_r, a_r_r_l_r, d_l_r_l_r, a_r_r)
on (9 < (a_l_l_r - 53))
) T1
union all
select d_l, c_l_r
from (
Select d_l, c_l_r
from (
Select d
from t4
where ((32 - d) < a)
) T1(d_l)
left join (
select c_l
from (
select c_l, c_l_r
from (
Select c_l, c_l_r
from (
Select c
from t5
where (e > a)
) T1(c_l)
inner join (
Select c_l, a_l, d_r
from (
Select c, a, b
from t1
where (c > (7 + 0))
) T1(c_l, a_l, b_l)
full join (
Select d
from t3
where (35 = ((42 - 13) + a))
) T2(d_r)
on (13 < c_l)
) T2(c_l_r, a_l_r, d_r_r)
on (42 > c_l_r)
) T1
union all
select a_l, e_l_r
from (
Select a_l, e_l_r
from (
select a
from (
Select a, d
from t2
where (0 = 57)
) T1
union all
select b
from (
select b
from (
Select b, d
from t3
where (8 > d)
) T1
union all
select e
from (
Select e
from t3
where ((12 + 69) > 20)
) T2
) T2
) T1(a_l)
full join (
Select e_l, c_l, c_r
from (
select e, c
from (
Select e, c
from t1
where (31 < d)
) T1
union all
select a_l, b_r
from (
Select a_l, b_r
from (
Select a
from t3
where (e < 35)
) T1(a_l)
full join (
Select b
from t2
where (25 < d)
) T2(b_r)
on ((53 - (b_r - (60 - a_l))) > 94)
) T2
) T1(e_l, c_l)
inner join (
select c, a
from (
Select c, a
from t3
where ((e + (98 - b)) = c)
) T1
union all
select c, a
from (
Select c, a, b
from t1
where (88 < ((a * 15) + 1))
) T2
) T2(c_r, a_r)
on ((89 * 89) = 52)
) T2(e_l_r, c_l_r, c_r_r)
on (a_l > 84)
) T2
) T1
union all
select c
from (
Select c
from t5
where (d < d)
) T2
) T2(c_l_r)
on (c_l_r > 22)
) T2
) T2(b_l_r, d_l_r)
on ((20 - (16 + d_l_r)) > b_l_r)
) T1
union all
select b
from (
Select b
from t3
where (23 > 10)
) T2
) T2
) T1(e_l)
left join (
Select a
from t3
where (59 > d)
) T2(a_r)
on (31 = 5)
) T2(e_l_r, a_r_r)
on (2 < 64)
) T1(a_l_l, e_l_r_l, a_r_r_l)
full join (
Select e, b
from t4
where ((a + b) = d)
) T2(e_r, b_r)
on ((79 - 53) < (74 * 96))
) T1(e_l_r_l_l, e_r_l, b_r_l)
left join (
Select e, a, b
from t5
where (9 > 60)
) T2(e_r, a_r, b_r)
on (e_r_l < b_r)
) T1(e_l_r_l_l_l, e_r_l_l, e_r_l, b_r_l)
left join (
select c_l_l, e_l_l
from (
Select c_l_l, e_l_l, c_r, a_r
from (
Select e_l, c_l, c_r
from (
Select e, c
from t3
where ((8 + 38) = d)
) T1(e_l, c_l)
inner join (
select c
from (
Select c
from t3
where (59 = e)
) T1
union all
select d
from (
Select d
from t4
where (e > d)
) T2
) T2(c_r)
on ((63 * e_l) < ((20 - (21 + 73)) - e_l))
) T1(e_l_l, c_l_l, c_r_l)
left join (
Select c, a, d
from t5
where (96 = 76)
) T2(c_r, a_r, d_r)
on (60 > ((4 + 67) * e_l_l))
) T1
union all
select b, d
from (
Select b, d
from t2
where (48 < (e - d))
) T2
) T2(c_l_l_r, e_l_l_r)
on (b_r_l = (b_r_l * b_r_l))
) T2
order by 1, 2
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
select b
from (
select b
from (
Select b
from t2
where (a = b)
) T1
union all
select e
from (
Select e, c, a
from t2
where (14 < a)
) T2
) T1
union all
select c
from (
Select c, a, b
from t1
where (87 < (44 * 35))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l_l, a_r_r, e_r_r
from (
Select d_l_l, a_r_r, e_r_r
from (
Select e_l, d_l, b_l_l_r, c_r_r
from (
Select e, d
from t1
where (62 = ((9 + 64) * 75))
) T1(e_l, d_l)
left join (
Select b_l_l, e_r, c_r
from (
Select b_l, e_r
from (
Select b
from t4
where (42 = (a - (d + d)))
) T1(b_l)
inner join (
Select e
from t1
where (19 = 6)
) T2(e_r)
on (b_l > b_l)
) T1(b_l_l, e_r_l)
inner join (
Select e, c
from t1
where ((a * 80) > b)
) T2(e_r, c_r)
on (e_r > (b_l_l - (22 - b_l_l)))
) T2(b_l_l_r, e_r_r, c_r_r)
on (84 = 22)
) T1(e_l_l, d_l_l, b_l_l_r_l, c_r_r_l)
left join (
Select e_l, d_l, e_r, a_r
from (
Select e, a, d
from t4
where ((d - (63 - b)) = d)
) T1(e_l, a_l, d_l)
full join (
Select e, a
from t5
where (72 = 23)
) T2(e_r, a_r)
on (d_l < 32)
) T2(e_l_r, d_l_r, e_r_r, a_r_r)
on (a_r_r = a_r_r)
) T1
union all
select c, a, b
from (
Select c, a, b
from t1
where (21 < (6 + 57))
) T2
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
select e
from (
Select e, a, b, d
from t2
where (a = b)
) T1
union all
select a
from (
Select a
from t3
where (26 = 59)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l
from (
Select c_l, e_r, a_r, b_r
from (
Select c
from t4
where ((e * 53) > 5)
) T1(c_l)
left join (
Select e, a, b
from t2
where (d < b)
) T2(e_r, a_r, b_r)
on (c_l > a_r)
) T1
union all
select a
from (
Select a
from t1
where (c = d)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_r_l
from (
Select d_r_l, a_r_l, b_r
from (
Select b_l, a_r, d_r
from (
Select b
from t1
where (46 > e)
) T1(b_l)
inner join (
Select a, d
from t4
where (c > (71 - d))
) T2(a_r, d_r)
on (40 = 17)
) T1(b_l_l, a_r_l, d_r_l)
inner join (
Select e, b
from t5
where ((d + (60 * d)) < e)
) T2(e_r, b_r)
on (53 < b_r)
) T1
union all
select a
from (
Select a
from t2
where (0 < 70)
) T2
order by 1
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
select d_r_l
from (
Select d_r_l, d_r_l_l, b_r, d_r
from (
Select d_r_l, d_r
from (
Select d_l, d_r
from (
Select d
from t4
where (86 > 75)
) T1(d_l)
left join (
Select d
from t4
where (15 = 44)
) T2(d_r)
on (d_l = 38)
) T1(d_l_l, d_r_l)
left join (
Select d
from t1
where (a = b)
) T2(d_r)
on (66 = d_r)
) T1(d_r_l_l, d_r_l)
inner join (
Select e, b, d
from t1
where (d = 63)
) T2(e_r, b_r, d_r)
on (8 = 46)
) T1
union all
select e
from (
Select e
from t5
where (7 = (b * 38))
) T2
order by 1
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
select c_r_l
from (
Select c_r_l, d_l_l, d_r
from (
Select c_l, d_l, c_r, b_r, d_r
from (
Select e, c, a, d
from t1
where ((c - b) = d)
) T1(e_l, c_l, a_l, d_l)
left join (
Select c, b, d
from t5
where (a = ((67 + 76) * c))
) T2(c_r, b_r, d_r)
on ((82 - b_r) > d_l)
) T1(c_l_l, d_l_l, c_r_l, b_r_l, d_r_l)
left join (
Select c, d
from t2
where (55 > 52)
) T2(c_r, d_r)
on (54 = c_r_l)
) T1
union all
select e
from (
Select e
from t2
where (c = 26)
) T2
order by 1
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
select e, c, d
from (
Select e, c, d
from t3
where (67 < b)
) T1
union all
select e, b, d
from (
Select e, b, d
from t2
where (d > 81)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test24exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, a_l, c_r
from (
Select e_l, a_l, c_r
from (
select e, a
from (
Select e, a, b, d
from t1
where ((e + a) > d)
) T1
union all
select e, d
from (
Select e, d
from t5
where (c = a)
) T2
) T1(e_l, a_l)
left join (
Select c
from t4
where (79 = 17)
) T2(c_r)
on (a_l < 0)
) T1
union all
select a_r_l_r_l, e_l_l, b_l_r
from (
Select a_r_l_r_l, e_l_l, b_l_r
from (
Select e_l, b_l, b_r_r, a_r_l_r
from (
Select e, b
from t1
where ((e - (c * e)) > (38 + (97 * (72 + (d - 20)))))
) T1(e_l, b_l)
left join (
Select a_r_l, b_r
from (
Select a_l, a_r
from (
Select c, a, b, d
from t4
where (d = 47)
) T1(c_l, a_l, b_l, d_l)
inner join (
Select a
from t2
where (6 = ((c + 42) * 74))
) T2(a_r)
on (53 = 12)
) T1(a_l_l, a_r_l)
full join (
Select b
from t4
where (83 < (a * 83))
) T2(b_r)
on (b_r = 75)
) T2(a_r_l_r, b_r_r)
on ((30 - 5) < (b_r_r + (15 + 29)))
) T1(e_l_l, b_l_l, b_r_r_l, a_r_l_r_l)
left join (
Select b_l, e_r
from (
Select b
from t5
where ((64 - 30) = 24)
) T1(b_l)
full join (
Select e
from t1
where (b = 48)
) T2(e_r)
on ((e_r * e_r) < b_l)
) T2(b_l_r, e_r_r)
on ((36 - 48) < 24)
) T2
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
select b_l, d_r
from (
Select b_l, d_r
from (
Select b
from t3
where (a > 98)
) T1(b_l)
full join (
Select b, d
from t3
where (6 > 99)
) T2(b_r, d_r)
on (d_r < 54)
) T1
union all
select e, b
from (
Select e, b, d
from t1
where ((6 + (22 - 0)) = b)
) T2
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
    #*******************************************
    _testmgr.testcase_end(desc)

