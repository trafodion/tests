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
select e, d
from (
Select e, d
from t3
where (((e * (69 - 81)) - a) > 17)
) T1
union all
select c, b
from (
Select c, b
from t2
where (c > d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, a_r
from (
Select a_l, a_r
from (
Select e, c, a
from t4
where (e = 62)
) T1(e_l, c_l, a_l)
left join (
Select a, d
from t3
where (a = 50)
) T2(a_r, d_r)
on (74 = 3)
) T1
union all
select b_l, b_r
from (
Select b_l, b_r
from (
select c, b
from (
Select c, b, d
from t4
where (d = a)
) T1
union all
select e, a
from (
Select e, a
from t3
where (13 = 64)
) T2
) T1(c_l, b_l)
left join (
Select e, b, d
from t1
where (b = 11)
) T2(e_r, b_r, d_r)
on ((b_l - 38) > 96)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, a, b, d
from t4
where ((65 + 22) < b)
) T1
union all
select b
from (
Select b
from t3
where ((43 * 48) = (47 * 27))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a, b
from t2
where (85 > 64)
) T1
union all
select e
from (
select e
from (
Select e, c, d
from t3
where (e = c)
) T1
union all
select b
from (
Select b
from t5
where ((69 * b) = 18)
) T2
) T2
order by 1
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
select a, b
from (
Select a, b
from t5
where (a = b)
) T1
union all
select c, b
from (
Select c, b
from t2
where (97 < e)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t4
where (c = 88)
) T1
union all
select c_r_l
from (
Select c_r_l, d_l_l, c_r
from (
Select d_l, c_r
from (
Select d
from t3
where (d = e)
) T1(d_l)
left join (
Select c, d
from t1
where (a = 69)
) T2(c_r, d_r)
on (c_r = 38)
) T1(d_l_l, c_r_l)
left join (
Select c, a
from t1
where (51 = 53)
) T2(c_r, a_r)
on (37 = 47)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t5
where (98 < 85)
) T1
union all
select c
from (
Select c, b
from t4
where (((b * ((d - 48) - c)) + b) = b)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_r_l_l, d_r
from (
Select c_r_l_l, d_r
from (
select c_r_l
from (
Select c_r_l, b_l_l, d_r_r
from (
Select b_l, d_l, c_r
from (
select b, d
from (
Select b, d
from t2
where (a > 59)
) T1
union all
select c, a
from (
Select c, a, b
from t3
where ((e * ((c * d) + 66)) = a)
) T2
) T1(b_l, d_l)
left join (
Select c, a, b
from t4
where (68 < 48)
) T2(c_r, a_r, b_r)
on (c_r < b_l)
) T1(b_l_l, d_l_l, c_r_l)
full join (
Select e_l_l, b_l_l, d_r
from (
Select e_l, b_l, a_r
from (
Select e, b
from t3
where ((17 * b) = d)
) T1(e_l, b_l)
left join (
Select a
from t5
where (e = 12)
) T2(a_r)
on (73 > b_l)
) T1(e_l_l, b_l_l, a_r_l)
inner join (
select e, d
from (
Select e, d
from t2
where (86 = a)
) T1
union all
select a_l_l, e_l_r_r_l
from (
Select a_l_l, e_l_r_r_l, b_l_l_r_l, a_r
from (
Select a_l, b_l_l_r, e_l_r_r
from (
Select a
from t4
where (32 = e)
) T1(a_l)
full join (
Select c_r_l, b_l_l, e_l_r, b_l_r
from (
Select a_l, b_l, e_r, c_r
from (
Select e, a, b
from t1
where (b = c)
) T1(e_l, a_l, b_l)
inner join (
Select e, c
from t1
where (96 = e)
) T2(e_r, c_r)
on ((96 + 4) > 90)
) T1(a_l_l, b_l_l, e_r_l, c_r_l)
left join (
select e_l, b_l
from (
Select e_l, b_l, e_r, a_r
from (
Select e, c, b
from t3
where (42 = (25 * 67))
) T1(e_l, c_l, b_l)
inner join (
Select e, a
from t2
where (b > c)
) T2(e_r, a_r)
on (27 = 17)
) T1
union all
select a_l, a_r_r
from (
Select a_l, a_r_r
from (
Select a
from t2
where (d < 2)
) T1(a_l)
left join (
Select a_l, c_r, a_r
from (
Select a
from t3
where (e = e)
) T1(a_l)
left join (
Select c, a
from t4
where (8 > c)
) T2(c_r, a_r)
on (71 = a_l)
) T2(a_l_r, c_r_r, a_r_r)
on (28 = a_l)
) T2
) T2(e_l_r, b_l_r)
on (b_l_r = 90)
) T2(c_r_l_r, b_l_l_r, e_l_r_r, b_l_r_r)
on ((54 + e_l_r_r) > 84)
) T1(a_l_l, b_l_l_r_l, e_l_r_r_l)
full join (
select a
from (
Select a
from t5
where (44 = a)
) T1
union all
select c_l
from (
Select c_l, c_r, d_r
from (
Select c, a
from t1
where (19 < c)
) T1(c_l, a_l)
full join (
Select c, d
from t1
where (c < e)
) T2(c_r, d_r)
on (c_l > 70)
) T2
) T2(a_r)
on (50 < (b_l_l_r_l * 96))
) T2
) T2(e_r, d_r)
on ((12 * d_r) < e_l_l)
) T2(e_l_l_r, b_l_l_r, d_r_r)
on (37 > d_r_r)
) T1
union all
select c
from (
Select c
from t3
where (78 = 24)
) T2
) T1(c_r_l_l)
left join (
Select b, d
from t3
where (46 < c)
) T2(b_r, d_r)
on (68 > (95 * d_r))
) T1
union all
select e_l, a_l
from (
Select e_l, a_l, e_l_r, a_r_r, d_l_r
from (
Select e, a
from t2
where (a < (0 + a))
) T1(e_l, a_l)
left join (
Select e_l, d_l, a_r, b_r
from (
Select e, c, d
from t4
where (d = 62)
) T1(e_l, c_l, d_l)
left join (
Select a, b
from t5
where (71 > b)
) T2(a_r, b_r)
on (25 > b_r)
) T2(e_l_r, d_l_r, a_r_r, b_r_r)
on (78 = 1)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t5
where (74 = 10)
) T1
union all
select d
from (
Select d
from t3
where (a < a)
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
select e
from (
select e
from (
Select e
from t2
where (d = 31)
) T1
union all
select a
from (
Select a, b, d
from t3
where (a = 46)
) T2
) T1
union all
select a_l
from (
select a_l
from (
Select a_l, d_r
from (
Select a
from t1
where (95 > b)
) T1(a_l)
left join (
Select d
from t5
where ((a - 96) = a)
) T2(d_r)
on (80 > 1)
) T1
union all
select e
from (
Select e
from t1
where (83 > 65)
) T2
) T2
order by 1
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
select b
from (
Select b
from t4
where ((c + 87) = 46)
) T1
union all
select e
from (
Select e
from t2
where (13 > b)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, c_r_r
from (
Select a_l, c_r_r
from (
Select e, a
from t1
where (88 = 8)
) T1(e_l, a_l)
inner join (
Select b_l, c_r
from (
Select b
from t3
where ((55 * a) < a)
) T1(b_l)
left join (
Select e, c, a, d
from t3
where ((b + 80) = 79)
) T2(e_r, c_r, a_r, d_r)
on (b_l > c_r)
) T2(b_l_r, c_r_r)
on (c_r_r > 58)
) T1
union all
select a_l, d_l
from (
Select a_l, d_l, b_r_r, e_l_r
from (
Select c, a, d
from t4
where (d = e)
) T1(c_l, a_l, d_l)
full join (
Select e_l, b_r
from (
select e, c
from (
Select e, c, a
from t2
where (e < 51)
) T1
union all
select e, b
from (
select e, b
from (
Select e, b
from t3
where (85 < (((24 * e) * e) + 73))
) T1
union all
select c_r_l, b_l_l
from (
Select c_r_l, b_l_l, b_r_r, e_l_r
from (
Select b_l, c_r
from (
Select e, c, b
from t3
where (c < 53)
) T1(e_l, c_l, b_l)
inner join (
Select c
from t4
where (59 < (((e - (62 * a)) + (88 + 96)) * ((28 + 59) * 89)))
) T2(c_r)
on (27 = b_l)
) T1(b_l_l, c_r_l)
left join (
Select e_l, b_r, d_r
from (
Select e
from t1
where (c < 72)
) T1(e_l)
inner join (
Select b, d
from t5
where (d > b)
) T2(b_r, d_r)
on (47 < b_r)
) T2(e_l_r, b_r_r, d_r_r)
on (b_r_r > e_l_r)
) T2
) T2
) T1(e_l, c_l)
inner join (
select e, b
from (
Select e, b
from t5
where (39 = a)
) T1
union all
select d_r_l, c_r_l
from (
Select d_r_l, c_r_l, a_r_r, d_l_r
from (
Select e_l, c_r, d_r
from (
Select e, b
from t1
where (d = a)
) T1(e_l, b_l)
left join (
Select c, d
from t1
where ((e + e) > 0)
) T2(c_r, d_r)
on (13 = (6 + c_r))
) T1(e_l_l, c_r_l, d_r_l)
inner join (
Select d_l, a_r
from (
Select a, d
from t5
where (65 > 57)
) T1(a_l, d_l)
full join (
Select a
from t2
where (91 < d)
) T2(a_r)
on (((a_r + 66) - 64) = ((14 * ((a_r * d_l) - 56)) + 57))
) T2(d_l_r, a_r_r)
on (29 = (d_r_l - 29))
) T2
) T2(e_r, b_r)
on (e_l = e_l)
) T2(e_l_r, b_r_r)
on (a_l > b_r_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t2
where (81 = 28)
) T1
union all
select e
from (
Select e, b, d
from t5
where (c = 11)
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
select a
from (
Select a, d
from t1
where (((23 + b) * (e * e)) = 69)
) T1
union all
select d
from (
Select d
from t2
where ((e - e) = e)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, d_r
from (
Select a_l, d_r
from (
Select a
from t4
where ((97 - e) = 71)
) T1(a_l)
full join (
Select a, d
from t4
where (d < a)
) T2(a_r, d_r)
on ((a_l * a_l) > a_l)
) T1
union all
select e, c
from (
select e, c, b, d
from (
Select e, c, b, d
from t2
where (64 > 82)
) T1
union all
select b_l, d_l, c_l_l_r, d_l_r_r
from (
Select b_l, d_l, c_l_l_r, d_l_r_r
from (
Select e, b, d
from t2
where (d = a)
) T1(e_l, b_l, d_l)
left join (
Select b_r_l, c_l_l, b_l_l, d_l_r
from (
Select c_l, b_l, b_r
from (
Select e, c, b
from t4
where (96 = a)
) T1(e_l, c_l, b_l)
inner join (
Select a, b, d
from t2
where ((13 * 89) < d)
) T2(a_r, b_r, d_r)
on (84 > c_l)
) T1(c_l_l, b_l_l, b_r_l)
full join (
Select d_l, c_l_r
from (
Select d
from t5
where (74 = 65)
) T1(d_l)
left join (
Select c_l, e_r, a_r
from (
Select e, c
from t4
where (e = 76)
) T1(e_l, c_l)
full join (
select e, c, a
from (
Select e, c, a
from t4
where (b < (47 + e))
) T1
union all
select a_l, b_l, a_l_r
from (
Select a_l, b_l, a_l_r, b_l_r
from (
Select a, b
from t3
where ((34 - 62) = e)
) T1(a_l, b_l)
full join (
Select a_l, b_l, d_r
from (
Select a, b
from t2
where (e = 67)
) T1(a_l, b_l)
inner join (
Select d
from t2
where (e = (5 * e))
) T2(d_r)
on ((64 + 38) = (43 * 90))
) T2(a_l_r, b_l_r, d_r_r)
on (0 < (34 - a_l))
) T2
) T2(e_r, c_r, a_r)
on (e_r = c_l)
) T2(c_l_r, e_r_r, a_r_r)
on (((d_l + 24) - 24) < 39)
) T2(d_l_r, c_l_r_r)
on (54 > d_l_r)
) T2(b_r_l_r, c_l_l_r, b_l_l_r, d_l_r_r)
on (97 > ((77 - b_l) * 95))
) T2
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, d
from (
Select c, d
from t5
where (24 > (3 - d))
) T1
union all
select e, c
from (
Select e, c
from t5
where (31 = 70)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t2
where (c > a)
) T1
union all
select a_l
from (
Select a_l, c_r_r, c_l_l_l_r
from (
Select a
from t1
where (b > (48 + (e * 77)))
) T1(a_l)
left join (
Select c_l_l_l, c_r
from (
select c_l_l
from (
Select c_l_l, e_r_l, d_r
from (
Select e_l, c_l, e_r
from (
Select e, c, b
from t5
where (c > (83 * a))
) T1(e_l, c_l, b_l)
left join (
Select e, d
from t1
where (b > 71)
) T2(e_r, d_r)
on ((((e_r * 42) + (12 - ((e_l + c_l) + (e_l - 88)))) + (8 * c_l)) = 13)
) T1(e_l_l, c_l_l, e_r_l)
inner join (
Select d
from t4
where (48 = (96 * 78))
) T2(d_r)
on (42 > 25)
) T1
union all
select d
from (
Select d
from t4
where (a = 14)
) T2
) T1(c_l_l_l)
left join (
Select e, c, a, d
from t3
where (a < (16 * 58))
) T2(e_r, c_r, a_r, d_r)
on (c_r = c_l_l_l)
) T2(c_l_l_l_r, c_r_r)
on (24 = c_r_r)
) T2
order by 1
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
select a
from (
Select a, b
from t4
where (76 = 14)
) T1
union all
select e
from (
Select e
from t5
where (3 > a)
) T2
order by 1
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
select c, d
from (
Select c, d
from t3
where (77 = 49)
) T1
union all
select c_l_l, d_l_l
from (
Select c_l_l, d_l_l, d_r
from (
Select c_l, d_l, e_r
from (
Select c, d
from t1
where (40 < d)
) T1(c_l, d_l)
full join (
Select e
from t2
where (d = ((c - e) + 45))
) T2(e_r)
on (5 > (e_r * 76))
) T1(c_l_l, d_l_l, e_r_l)
left join (
Select d
from t3
where (53 = c)
) T2(d_r)
on (75 > 36)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, c_l
from (
Select e_l, c_l, b_r_r
from (
select e, c
from (
Select e, c, b, d
from t5
where (d = 36)
) T1
union all
select c, b
from (
select c, b
from (
Select c, b
from t4
where ((29 + 6) > d)
) T1
union all
select c, b
from (
Select c, b, d
from t2
where (c = 13)
) T2
) T2
) T1(e_l, c_l)
left join (
Select d_l, c_r, b_r
from (
Select a, d
from t2
where (a > (d - e))
) T1(a_l, d_l)
full join (
Select c, a, b
from t5
where (b = 40)
) T2(c_r, a_r, b_r)
on (c_r < c_r)
) T2(d_l_r, c_r_r, b_r_r)
on (b_r_r = b_r_r)
) T1
union all
select c, b
from (
Select c, b
from t5
where (46 = 17)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test38exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #********************************************
    _testmgr.testcase_end(desc)

