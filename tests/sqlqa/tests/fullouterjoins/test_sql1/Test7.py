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
    
def test001(desc='Joins Set 7'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select a, d
from (
Select a, d
from t4
where (a = a)
) T1
union all
select a, d
from (
select a, d
from (
Select a, d
from t5
where (c = (d - 77))
) T1
union all
select e, c
from (
Select e, c, b, d
from t1
where (32 > (c + 33))
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
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s1')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t4
where (d = ((b - 82) - 25))
) T1
union all
select e
from (
Select e, a
from t4
where ((e * ((89 + 40) + d)) > a)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s2')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, d_r
from (
Select e_l, d_r
from (
Select e
from t4
where (a > (e + (b * (a * (10 + 67)))))
) T1(e_l)
left join (
Select e, c, d
from t4
where (24 = a)
) T2(e_r, c_r, d_r)
on (e_l = e_l)
) T1
union all
select e_l, c_l
from (
Select e_l, c_l, d_l, a_r_r, c_r_r, d_l_r
from (
Select e, c, d
from t2
where (d > 21)
) T1(e_l, c_l, d_l)
inner join (
Select d_l, c_r, a_r
from (
select d
from (
Select d
from t1
where ((c * d) < a)
) T1
union all
select b
from (
Select b, d
from t5
where (18 < 71)
) T2
) T1(d_l)
inner join (
Select c, a, d
from t1
where (98 < c)
) T2(c_r, a_r, d_r)
on (47 = (d_l * d_l))
) T2(d_l_r, c_r_r, a_r_r)
on ((65 - 15) > 45)
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
select e, b, d
from (
Select e, b, d
from t4
where (((c * c) - (b - 21)) > e)
) T1
union all
select c, a, d
from (
Select c, a, d
from t2
where (84 = (35 + e))
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s4')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l_l, d_r
from (
Select e_l_l, d_r
from (
Select e_l, c_r
from (
Select e, b
from t2
where (76 = (62 - b))
) T1(e_l, b_l)
left join (
Select c
from t3
where (c = 11)
) T2(c_r)
on (c_r < c_r)
) T1(e_l_l, c_r_l)
left join (
Select d
from t2
where (87 = a)
) T2(d_r)
on ((e_l_l + (e_l_l + e_l_l)) = (28 + 95))
) T1
union all
select a, b
from (
Select a, b, d
from t5
where (d > d)
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
select a_r_r_l, e_r
from (
Select a_r_r_l, e_r, c_r, b_r
from (
Select c_l, a_r_r
from (
Select c, b
from t5
where (61 = (63 + a))
) T1(c_l, b_l)
full join (
Select a_l, a_r, b_r
from (
Select e, a
from t1
where (c = a)
) T1(e_l, a_l)
left join (
Select c, a, b
from t1
where ((b - (11 + a)) = (12 * (e * a)))
) T2(c_r, a_r, b_r)
on (14 > a_l)
) T2(a_l_r, a_r_r, b_r_r)
on (a_r_r = c_l)
) T1(c_l_l, a_r_r_l)
inner join (
Select e, c, b
from t1
where (80 = (b + 58))
) T2(e_r, c_r, b_r)
on (89 < a_r_r_l)
) T1
union all
select b_l, b_r
from (
Select b_l, b_r
from (
Select c, b, d
from t2
where (e > 31)
) T1(c_l, b_l, d_l)
full join (
Select c, b, d
from t2
where (51 < b)
) T2(c_r, b_r, d_r)
on ((2 - (21 - ((95 + b_l) - (48 * b_l)))) > 33)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s6')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t3
where (a < 97)
) T1
union all
select b
from (
Select b, d
from t3
where (b = (0 + e))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s7')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t1
where ((68 * a) < d)
) T1
union all
select d
from (
Select d
from t3
where (70 < 7)
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
select d
from (
Select d
from t4
where (92 > 8)
) T1
union all
select c
from (
Select c
from t3
where (92 = d)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s9')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, a_l
from (
Select e_l, a_l, d_l, e_r
from (
Select e, a, d
from t5
where (95 = (61 + (a - 51)))
) T1(e_l, a_l, d_l)
inner join (
Select e
from t1
where (24 > a)
) T2(e_r)
on ((31 * 13) = 17)
) T1
union all
select e_l, b_r
from (
Select e_l, b_r
from (
Select e
from t3
where (d > a)
) T1(e_l)
left join (
Select b
from t5
where (e = 98)
) T2(b_r)
on (b_r < b_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s10')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t5
where (b < (70 - 74))
) T1
union all
select c
from (
Select c, a, b
from t4
where (20 < 72)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s11')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a, d
from (
Select c, a, d
from t1
where (e < c)
) T1
union all
select c_l, a_l, e_r
from (
Select c_l, a_l, e_r, a_r
from (
Select c, a
from t4
where (e < 52)
) T1(c_l, a_l)
left join (
Select e, a
from t3
where (26 = (38 + 48))
) T2(e_r, a_r)
on (((35 + (c_l * 87)) + 38) > 51)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s12')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l, b_r
from (
Select d_l, b_r
from (
Select d
from t2
where ((72 - d) < (b - 64))
) T1(d_l)
inner join (
Select b
from t5
where (45 > ((14 * b) - 96))
) T2(b_r)
on (60 = 46)
) T1
union all
select a_l_l, b_r
from (
Select a_l_l, b_r
from (
Select a_l, a_r
from (
Select a
from t5
where (b = 78)
) T1(a_l)
inner join (
Select a
from t2
where ((71 + b) = 7)
) T2(a_r)
on (53 = (a_l + 55))
) T1(a_l_l, a_r_l)
full join (
select b
from (
Select b
from t1
where (43 = b)
) T1
union all
select b
from (
Select b, d
from t4
where ((27 + 4) < 65)
) T2
) T2(b_r)
on (31 < 46)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s13')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l_l
from (
Select c_l_l, a_r_l, c_r_l, e_r_l_r_r, b_r_r_r
from (
Select c_l, c_r, a_r
from (
Select c, a
from t5
where (2 = 2)
) T1(c_l, a_l)
full join (
Select c, a, d
from t3
where (2 > 89)
) T2(c_r, a_r, d_r)
on (c_l = 97)
) T1(c_l_l, c_r_l, a_r_l)
full join (
Select b_l, b_r_r, d_r_r, e_r_l_r
from (
Select c, b
from t3
where (a > (81 * ((d - a) + (62 + 39))))
) T1(c_l, b_l)
left join (
Select e_r_l, b_r, d_r
from (
Select e_l, a_l, e_r
from (
Select e, a
from t4
where (a < a)
) T1(e_l, a_l)
left join (
Select e
from t4
where (7 > b)
) T2(e_r)
on (a_l = 30)
) T1(e_l_l, a_l_l, e_r_l)
left join (
Select b, d
from t4
where (60 < d)
) T2(b_r, d_r)
on ((62 * e_r_l) = d_r)
) T2(e_r_l_r, b_r_r, d_r_r)
on (b_r_r < 3)
) T2(b_l_r, b_r_r_r, d_r_r_r, e_r_l_r_r)
on (((c_l_l + a_r_l) + (38 * a_r_l)) = ((45 + a_r_l) * 27))
) T1
union all
select a
from (
Select a
from t2
where (b > e)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s14')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, c_r
from (
select e_l, c_r
from (
Select e_l, c_r
from (
Select e, b
from t2
where ((a + c) > c)
) T1(e_l, b_l)
inner join (
select c
from (
Select c, a
from t5
where ((c + a) > (26 + ((35 * 15) * a)))
) T1
union all
select c
from (
Select c
from t5
where (49 = 1)
) T2
) T2(c_r)
on (90 > e_l)
) T1
union all
select e, b
from (
Select e, b, d
from t3
where (94 = 56)
) T2
) T1
union all
select e, a
from (
Select e, a
from t5
where ((46 + 61) > d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s15')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b, d
from t5
where (26 < e)
) T1
union all
select b_l, b_r
from (
Select b_l, b_r
from (
select e, b
from (
Select e, b
from t5
where (93 = (71 - 29))
) T1
union all
select a_l, b_l
from (
Select a_l, b_l, c_l_r, d_r_r_r
from (
Select c, a, b
from t4
where (a < c)
) T1(c_l, a_l, b_l)
inner join (
Select c_l, c_l_r, d_r_r
from (
Select c
from t1
where (12 < 94)
) T1(c_l)
inner join (
Select c_l, a_r, d_r
from (
Select c
from t2
where (a < a)
) T1(c_l)
left join (
select a, b, d
from (
Select a, b, d
from t5
where (a < 0)
) T1
union all
select d_l, e_r, c_r
from (
Select d_l, e_r, c_r
from (
select d
from (
Select d
from t3
where ((b + a) = 66)
) T1
union all
select a_l_l
from (
Select a_l_l, a_r
from (
Select a_l, b_r
from (
select a
from (
Select a
from t4
where ((0 + 61) > c)
) T1
union all
select c
from (
Select c, a
from t3
where (84 < (11 * (83 + 36)))
) T2
) T1(a_l)
left join (
select b
from (
Select b
from t3
where ((c - 19) = 22)
) T1
union all
select b_l
from (
Select b_l, d_l, d_r_r, b_l_r
from (
Select c, b, d
from t5
where (63 > (9 - e))
) T1(c_l, b_l, d_l)
full join (
Select b_l, d_r
from (
Select b
from t3
where ((24 - 89) = (b + 5))
) T1(b_l)
full join (
Select c, a, d
from t3
where (73 = 32)
) T2(c_r, a_r, d_r)
on (63 > b_l)
) T2(b_l_r, d_r_r)
on (d_l = (b_l + d_r_r))
) T2
) T2(b_r)
on (a_l > 10)
) T1(a_l_l, b_r_l)
inner join (
Select e, a, b, d
from t3
where (84 = b)
) T2(e_r, a_r, b_r, d_r)
on ((a_l_l * a_l_l) < (a_l_l + a_l_l))
) T2
) T1(d_l)
left join (
Select e, c, b
from t4
where (95 = e)
) T2(e_r, c_r, b_r)
on (7 = 97)
) T2
) T2(a_r, b_r, d_r)
on (34 = (92 + 53))
) T2(c_l_r, a_r_r, d_r_r)
on (c_l > 65)
) T2(c_l_r, c_l_r_r, d_r_r_r)
on (b_l < ((d_r_r_r + d_r_r_r) * 70))
) T2
) T1(e_l, b_l)
left join (
Select c, b, d
from t1
where (b = e)
) T2(c_r, b_r, d_r)
on (10 = 45)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s16')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t4
where (2 > b)
) T1
union all
select b
from (
Select b
from t5
where (((94 - 39) * (b - 35)) > d)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s17')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
select e
from (
select e
from (
Select e, c, b, d
from t5
where (14 < (a - b))
) T1
union all
select b
from (
Select b
from t5
where (d < d)
) T2
) T1
union all
select e
from (
Select e, d
from t4
where (d = (52 * e))
) T2
) T1
union all
select e_l_l
from (
Select e_l_l, d_r
from (
Select e_l, d_r
from (
Select e, d
from t1
where (85 = 57)
) T1(e_l, d_l)
full join (
Select d
from t5
where (d = ((b - c) - 87))
) T2(d_r)
on (d_r < 75)
) T1(e_l_l, d_r_l)
left join (
Select d
from t4
where (17 = 93)
) T2(d_r)
on (e_l_l = d_r)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s18')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t5
where (((c + 95) + 81) < ((68 * 32) - b))
) T1
union all
select e
from (
Select e
from t2
where (e = (62 * 40))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s19')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b, d
from t5
where (0 = e)
) T1
union all
select a, b
from (
Select a, b
from t5
where (97 < c)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", 'a1s20')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    #********************************************
    
    _testmgr.testcase_end(desc)

