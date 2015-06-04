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
    
def test001(desc="""Joins Set 32"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select e
from (
Select e, d
from t2
where (76 = 54)
) T1
union all
select d
from (
Select d
from t2
where (e = 51)
) T2
order by 1
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
select d_l, b_r
from (
select d_l, b_r
from (
Select d_l, b_r, d_r
from (
Select d
from t2
where (b = 94)
) T1(d_l)
inner join (
Select b, d
from t5
where (c = (d * 24))
) T2(b_r, d_r)
on (91 = 52)
) T1
union all
select a, d
from (
Select a, d
from t5
where (1 = (e + 22))
) T2
) T1
union all
select b_l_l, a_r
from (
Select b_l_l, a_r
from (
Select b_l, e_r, c_r
from (
Select b
from t1
where (e = 28)
) T1(b_l)
full join (
Select e, c
from t5
where (83 = a)
) T2(e_r, c_r)
on (b_l = 13)
) T1(b_l_l, e_r_l, c_r_l)
inner join (
select a, b, d
from (
Select a, b, d
from t1
where (22 = (a * 31))
) T1
union all
select e, c, d
from (
Select e, c, d
from t3
where (32 = ((a * a) - 47))
) T2
) T2(a_r, b_r, d_r)
on (27 = a_r)
) T2
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
select e
from (
select e, c
from (
Select e, c, a, b
from t5
where (e = e)
) T1
union all
select b_l, b_l_r
from (
select b_l, b_l_r
from (
Select b_l, b_l_r
from (
Select b
from t1
where (a > 48)
) T1(b_l)
left join (
Select c_l, b_l, e_r
from (
Select c, b
from t2
where ((e + 72) = b)
) T1(c_l, b_l)
inner join (
Select e, c
from t1
where (c = 38)
) T2(e_r, c_r)
on (e_r = 4)
) T2(c_l_r, b_l_r, e_r_r)
on ((b_l_r + b_l) = b_l_r)
) T1
union all
select a, d
from (
Select a, d
from t5
where (60 = (b * (25 - (74 + 20))))
) T2
) T2
) T1
union all
select d
from (
Select d
from t2
where ((86 - a) = 78)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t3
where (((a * (a - a)) - 7) > b)
) T1
union all
select e_l
from (
Select e_l, b_r_r_r, b_l_r
from (
Select e
from t2
where (((85 - 14) * e) > c)
) T1(e_l)
full join (
Select b_l, b_r_r
from (
Select b
from t3
where (((42 * (e + (d + (b - 55)))) + 52) < 98)
) T1(b_l)
full join (
Select a_l_l, b_r_l, b_r
from (
Select a_l, b_r
from (
Select a
from t4
where (a = e)
) T1(a_l)
inner join (
Select c, b, d
from t2
where (((c + d) + (b - b)) = 90)
) T2(c_r, b_r, d_r)
on (a_l = 69)
) T1(a_l_l, b_r_l)
left join (
Select b
from t1
where (23 > (70 + b))
) T2(b_r)
on (b_r_l < (a_l_l + 51))
) T2(a_l_l_r, b_r_l_r, b_r_r)
on (b_r_r = b_r_r)
) T2(b_l_r, b_r_r_r)
on (e_l < 11)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c, b, d
from t1
where (17 = 10)
) T1
union all
select a
from (
Select a
from t5
where (c > (38 * ((b * d) - 31)))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l, d_r
from (
Select d_l, d_r
from (
select d
from (
Select d
from t3
where (b > (85 * e))
) T1
union all
select c_l_l
from (
Select c_l_l, e_r_r_l, c_r
from (
Select c_l, e_r_r
from (
select c, d
from (
select c, d
from (
Select c, d
from t1
where (83 > ((67 - (43 * 97)) + d))
) T1
union all
select e, a
from (
Select e, a, b
from t1
where (e < d)
) T2
) T1
union all
select a_l_l_l, c_r_l_l
from (
Select a_l_l_l, c_r_l_l, b_r
from (
select a_l_l, c_r_l
from (
Select a_l_l, c_r_l, e_r, b_r
from (
Select a_l, c_r
from (
Select e, a
from t5
where (48 = (d - (48 - e)))
) T1(e_l, a_l)
left join (
Select c
from t5
where ((a - 71) < (b * d))
) T2(c_r)
on (21 = 69)
) T1(a_l_l, c_r_l)
left join (
Select e, b
from t5
where (64 < 26)
) T2(e_r, b_r)
on ((b_r * c_r_l) = e_r)
) T1
union all
select e, a
from (
Select e, a
from t2
where ((61 + a) > e)
) T2
) T1(a_l_l_l, c_r_l_l)
left join (
Select c, b
from t4
where (61 < 34)
) T2(c_r, b_r)
on (49 < 22)
) T2
) T1(c_l, d_l)
left join (
Select c_l, e_r
from (
Select c
from t2
where (69 < 39)
) T1(c_l)
full join (
select e
from (
Select e, c, b, d
from t4
where (57 = e)
) T1
union all
select c
from (
Select c
from t2
where ((a - d) = (a - (22 - e)))
) T2
) T2(e_r)
on (c_l = 92)
) T2(c_l_r, e_r_r)
on (c_l = c_l)
) T1(c_l_l, e_r_r_l)
inner join (
Select c
from t2
where (e = d)
) T2(c_r)
on (22 > 52)
) T2
) T1(d_l)
left join (
Select c, a, d
from t4
where (a < 6)
) T2(c_r, a_r, d_r)
on (d_r = d_r)
) T1
union all
select b_l, d_r
from (
Select b_l, d_r
from (
Select c, b
from t5
where (b > 9)
) T1(c_l, b_l)
full join (
Select d
from t4
where (13 < (68 + a))
) T2(d_r)
on (b_l < b_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
select e, b
from (
Select e, b, d
from t1
where ((0 + (90 * 14)) = 19)
) T1
union all
select c, d
from (
Select c, d
from t5
where (30 = (78 + 91))
) T2
) T1
union all
select e_l, a_l
from (
Select e_l, a_l, b_r
from (
Select e, a
from t3
where (a = 15)
) T1(e_l, a_l)
left join (
Select b
from t2
where (71 = d)
) T2(b_r)
on (a_l = 63)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, c_r_r, d_l_r
from (
Select e_l, c_r_r, d_l_r
from (
Select e
from t3
where (55 > (94 * (47 + e)))
) T1(e_l)
left join (
Select d_l, c_r
from (
Select b, d
from t3
where (85 < 2)
) T1(b_l, d_l)
left join (
Select c, b
from t4
where ((83 + ((57 + b) * c)) > d)
) T2(c_r, b_r)
on ((d_l * (66 + 41)) < 61)
) T2(d_l_r, c_r_r)
on (35 = e_l)
) T1
union all
select b_r_l, e_l_l, c_r
from (
Select b_r_l, e_l_l, c_r, a_r
from (
Select e_l, b_l, d_l, b_r
from (
Select e, b, d
from t4
where ((b - 63) > 36)
) T1(e_l, b_l, d_l)
full join (
Select c, b
from t5
where (14 = 22)
) T2(c_r, b_r)
on (e_l = e_l)
) T1(e_l_l, b_l_l, d_l_l, b_r_l)
left join (
Select c, a, b, d
from t3
where (a = a)
) T2(c_r, a_r, b_r, d_r)
on (71 = a_r)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t3
where (d > 28)
) T1
union all
select a
from (
Select a
from t4
where ((3 + (b + b)) < 15)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a
from t3
where (79 = d)
) T1
union all
select b_l, b_l_r
from (
Select b_l, b_l_r
from (
Select b
from t3
where (10 = d)
) T1(b_l)
inner join (
Select b_l, c_r_r, e_l_l_r
from (
select a, b
from (
Select a, b, d
from t3
where (48 = (39 * b))
) T1
union all
select e, d
from (
Select e, d
from t5
where (((1 - (c * 50)) + 47) > 98)
) T2
) T1(a_l, b_l)
left join (
Select e_l_l, c_r
from (
Select e_l, b_r_r, b_l_r
from (
Select e
from t4
where (a > 80)
) T1(e_l)
left join (
Select c_l, b_l, b_r
from (
Select c, b
from t4
where (((e * b) * 29) < e)
) T1(c_l, b_l)
left join (
Select b
from t3
where (a = e)
) T2(b_r)
on (c_l < c_l)
) T2(c_l_r, b_l_r, b_r_r)
on (32 < (e_l - 40))
) T1(e_l_l, b_r_r_l, b_l_r_l)
full join (
Select c, b, d
from t4
where (47 > 32)
) T2(c_r, b_r, d_r)
on ((c_r + 24) = e_l_l)
) T2(e_l_l_r, c_r_r)
on (98 < 49)
) T2(b_l_r, c_r_r_r, e_l_l_r_r)
on (b_l_r > b_l)
) T2
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
select c, a
from (
Select c, a
from t2
where (75 > (b + a))
) T1
union all
select c_l, b_l
from (
Select c_l, b_l, c_l_r, a_r_r
from (
Select c, a, b
from t3
where (42 < (36 + (d + d)))
) T1(c_l, a_l, b_l)
full join (
Select c_l, a_r
from (
select c
from (
Select c
from t2
where (21 > e)
) T1
union all
select a
from (
Select a, b
from t5
where (c = 29)
) T2
) T1(c_l)
left join (
Select e, c, a
from t1
where (22 = d)
) T2(e_r, c_r, a_r)
on (a_r = 74)
) T2(c_l_r, a_r_r)
on (c_l_r < (75 + 42))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t2
where ((e * b) < 21)
) T1
union all
select a_l
from (
Select a_l, d_r_r, e_l_r
from (
Select a
from t3
where (b > 2)
) T1(a_l)
inner join (
Select e_l, d_r
from (
Select e, b
from t5
where (14 = 55)
) T1(e_l, b_l)
left join (
Select a, d
from t5
where (98 = 93)
) T2(a_r, d_r)
on (e_l > ((d_r * d_r) + e_l))
) T2(e_l_r, d_r_r)
on (a_l = 49)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a, d
from (
Select c, a, d
from t3
where ((51 * 76) > 70)
) T1
union all
select c, a, b
from (
Select c, a, b
from t5
where (d > d)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l_l
from (
Select a_l_l, c_l_l, d_r_l, e_r, c_r
from (
Select c_l, a_l, c_r, d_r
from (
Select c, a
from t2
where (b < 11)
) T1(c_l, a_l)
left join (
Select c, d
from t4
where (c = a)
) T2(c_r, d_r)
on (d_r = (d_r * 87))
) T1(c_l_l, a_l_l, c_r_l, d_r_l)
inner join (
select e, c
from (
Select e, c, b
from t2
where ((c - (e + 3)) = 31)
) T1
union all
select b, d
from (
Select b, d
from t3
where (((75 - e) * 20) < 61)
) T2
) T2(e_r, c_r)
on ((a_l_l - a_l_l) = d_r_l)
) T1
union all
select e
from (
Select e
from t1
where (b = 97)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b
from t1
where (47 = 65)
) T1
union all
select a_l, b_l_r
from (
Select a_l, b_l_r
from (
Select a
from t4
where (55 > (d * 9))
) T1(a_l)
left join (
Select a_l, b_l, a_l_l_r, e_l_r_l_r
from (
Select a, b
from t4
where ((34 * 36) = (c * 79))
) T1(a_l, b_l)
full join (
Select a_l_l, e_l_r_l, e_r, c_r
from (
select a_l, e_l_r
from (
Select a_l, e_l_r
from (
Select a
from t3
where (b = a)
) T1(a_l)
left join (
Select e_l, e_r
from (
Select e
from t1
where (d = e)
) T1(e_l)
left join (
Select e, c, d
from t2
where (92 > 30)
) T2(e_r, c_r, d_r)
on (e_l = 6)
) T2(e_l_r, e_r_r)
on (a_l < 74)
) T1
union all
select c, a
from (
Select c, a, b
from t2
where (c = 95)
) T2
) T1(a_l_l, e_l_r_l)
left join (
Select e, c, d
from t3
where ((c - (d + 6)) = 87)
) T2(e_r, c_r, d_r)
on (a_l_l > (a_l_l + (e_l_r_l - 83)))
) T2(a_l_l_r, e_l_r_l_r, e_r_r, c_r_r)
on (a_l_l_r < e_l_r_l_r)
) T2(a_l_r, b_l_r, a_l_l_r_r, e_l_r_l_r_r)
on (a_l > 61)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
select d
from (
Select d
from t4
where (c < c)
) T1
union all
select e
from (
Select e, c, a, d
from t1
where (c < (e * 80))
) T2
) T1
union all
select e
from (
Select e, a, d
from t5
where (39 = 15)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
Select e, a
from t1
where ((b + 48) = b)
) T1
union all
select e, c
from (
Select e, c
from t4
where ((a - c) = 46)
) T2
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
select b, d
from (
Select b, d
from t1
where (c > 20)
) T1
union all
select e, d
from (
Select e, d
from t4
where (a = 50)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
Select e, a, b, d
from t2
where ((10 - 79) < (65 - (97 * 13)))
) T1
union all
select e, b
from (
Select e, b
from t5
where (25 = 47)
) T2
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
select b, d
from (
Select b, d
from t5
where (61 = 56)
) T1
union all
select c, d
from (
Select c, d
from t3
where (30 = c)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test32exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #**********************************************
    _testmgr.testcase_end(desc)

