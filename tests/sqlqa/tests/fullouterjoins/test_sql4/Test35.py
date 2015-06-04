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
    
def test001(desc="""Joins Set 35"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select d_l
from (
Select d_l, e_l_r
from (
Select d
from t5
where ((a + (a - (e * 73))) = 9)
) T1(d_l)
full join (
Select e_l, d_r
from (
Select e
from t2
where (23 = 90)
) T1(e_l)
left join (
Select c, b, d
from t1
where (21 = b)
) T2(c_r, b_r, d_r)
on (85 = e_l)
) T2(e_l_r, d_r_r)
on (45 < 73)
) T1
union all
select d
from (
select d
from (
Select d
from t4
where (c < 63)
) T1
union all
select c
from (
Select c, a
from t4
where (49 = 40)
) T2
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t3
where (28 > 32)
) T1
union all
select b
from (
select b
from (
Select b
from t2
where (a < (a - 28))
) T1
union all
select e
from (
Select e, b
from t1
where (89 = 16)
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
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b
from t1
where ((a - c) = c)
) T1
union all
select e, c
from (
Select e, c, a
from t2
where (e < 21)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l
from (
Select e_l, b_r
from (
select e, a
from (
Select e, a
from t3
where (29 < (56 + (63 + ((b - c) - c))))
) T1
union all
select e, a
from (
Select e, a, d
from t4
where (8 = a)
) T2
) T1(e_l, a_l)
left join (
Select b
from t2
where ((b + b) = 52)
) T2(b_r)
on (3 = b_r)
) T1
union all
select e
from (
Select e
from t1
where (90 = a)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, a, b, d
from t3
where (b = (86 + (b * 79)))
) T1
union all
select a
from (
Select a
from t2
where (30 = 72)
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
select c, a
from (
Select c, a
from t5
where (c = (c * ((74 - 71) - (c + c))))
) T1
union all
select e, c
from (
select e, c
from (
Select e, c, a, d
from t3
where ((44 * 57) = (81 + e))
) T1
union all
select c, d
from (
Select c, d
from t3
where (12 > 2)
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
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t3
where (d > b)
) T1
union all
select c
from (
select c, a
from (
Select c, a, d
from t1
where (b = c)
) T1
union all
select c, a
from (
Select c, a
from t5
where (c = a)
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
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t3
where ((42 - b) = e)
) T1
union all
select e_l
from (
Select e_l, e_r
from (
Select e
from t1
where (((69 + a) + d) = a)
) T1(e_l)
left join (
Select e
from t2
where ((b * 78) < 85)
) T2(e_r)
on (e_r = 68)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t1
where (a = (73 * b))
) T1
union all
select e
from (
Select e, c
from t2
where (66 = 54)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_r_l, b_l_l, d_l_l
from (
Select a_r_l, b_l_l, d_l_l, b_l_l_r
from (
Select b_l, d_l, c_r, a_r
from (
Select b, d
from t1
where (43 = 4)
) T1(b_l, d_l)
left join (
Select c, a
from t1
where (60 = a)
) T2(c_r, a_r)
on (c_r > d_l)
) T1(b_l_l, d_l_l, c_r_l, a_r_l)
left join (
Select a_l_r_l, b_l_l, e_r, c_r
from (
select b_l, a_l_r
from (
Select b_l, a_l_r
from (
Select a, b
from t3
where (38 = b)
) T1(a_l, b_l)
full join (
Select a_l, d_l, c_r
from (
Select a, d
from t3
where (3 = a)
) T1(a_l, d_l)
inner join (
Select e, c, b
from t3
where ((e - 94) = a)
) T2(e_r, c_r, b_r)
on (11 > 43)
) T2(a_l_r, d_l_r, c_r_r)
on ((b_l * ((56 - 66) * 36)) < (((((51 * a_l_r) - 73) * b_l) - b_l) - b_l))
) T1
union all
select e_l_l, e_r
from (
Select e_l_l, e_r
from (
Select e_l, d_r
from (
select e, c
from (
Select e, c, a
from t2
where ((e + b) = c)
) T1
union all
select a, b
from (
Select a, b
from t5
where (e > (35 - 69))
) T2
) T1(e_l, c_l)
left join (
Select d
from t2
where (91 > c)
) T2(d_r)
on (36 = (80 + e_l))
) T1(e_l_l, d_r_l)
left join (
Select e
from t5
where (c > c)
) T2(e_r)
on (35 = (e_r * ((e_l_l * 64) * 8)))
) T2
) T1(b_l_l, a_l_r_l)
left join (
Select e, c
from t3
where ((92 - a) > 45)
) T2(e_r, c_r)
on (e_r = (e_r * b_l_l))
) T2(a_l_r_l_r, b_l_l_r, e_r_r, c_r_r)
on (b_l_l < 20)
) T1
union all
select c_l, a_l, a_r
from (
Select c_l, a_l, a_r
from (
Select c, a, d
from t5
where (b < 63)
) T1(c_l, a_l, d_l)
left join (
Select a
from t1
where (d = c)
) T2(a_r)
on (84 < a_l)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c
from t3
where (54 < b)
) T1
union all
select a
from (
Select a
from t4
where (83 = e)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b
from t3
where (d > 91)
) T1
union all
select c, a
from (
Select c, a, d
from t4
where (71 < 10)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t5
where (c > 3)
) T1
union all
select e_l
from (
Select e_l, c_r, b_r
from (
Select e
from t2
where (b = e)
) T1(e_l)
left join (
select c, b
from (
Select c, b, d
from t2
where (e > 54)
) T1
union all
select e, a
from (
select e, a
from (
Select e, a, b, d
from t5
where (c = b)
) T1
union all
select e, d
from (
select e, d
from (
Select e, d
from t4
where (91 = 35)
) T1
union all
select d_l, b_r
from (
Select d_l, b_r
from (
Select d
from t4
where (55 < 69)
) T1(d_l)
full join (
Select b
from t2
where ((e - b) > 89)
) T2(b_r)
on (43 = b_r)
) T2
) T2
) T2
) T2(c_r, b_r)
on (b_r < (((c_r - e_l) - 64) - 87))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_r_l, e_l_l_l
from (
Select b_r_l, e_l_l_l, d_r
from (
Select e_l_l, a_r_l, b_r
from (
Select e_l, a_r
from (
select e, c
from (
Select e, c, b, d
from t2
where (e > 95)
) T1
union all
select e, c
from (
Select e, c
from t3
where (e < 39)
) T2
) T1(e_l, c_l)
inner join (
select a
from (
Select a
from t4
where (11 = c)
) T1
union all
select b
from (
Select b
from t2
where (38 < (c + d))
) T2
) T2(a_r)
on (a_r = a_r)
) T1(e_l_l, a_r_l)
left join (
Select b
from t2
where (((e + 68) + 48) > 48)
) T2(b_r)
on (a_r_l = 60)
) T1(e_l_l_l, a_r_l_l, b_r_l)
left join (
Select d
from t3
where ((10 - d) < (b * (74 * 27)))
) T2(d_r)
on (e_l_l_l = d_r)
) T1
union all
select c, a
from (
Select c, a
from t4
where (d > 75)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, a, d
from t4
where (36 < 99)
) T1
union all
select b
from (
Select b
from t5
where (e = ((e + 57) - (68 * a)))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t4
where (11 = b)
) T1
union all
select b_l
from (
Select b_l, a_r
from (
Select b
from t1
where (70 > b)
) T1(b_l)
left join (
Select e, a
from t4
where (e = e)
) T2(e_r, a_r)
on (80 = (36 + a_r))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a, b
from (
Select c, a, b
from t3
where ((85 * e) = d)
) T1
union all
select e, c, b
from (
Select e, c, b
from t3
where (((((87 * 14) * c) - 89) - e) = a)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, d_r
from (
select a_l, d_r
from (
Select a_l, d_r
from (
Select a
from t1
where (a = 83)
) T1(a_l)
inner join (
Select d
from t3
where (57 = 28)
) T2(d_r)
on (45 = d_r)
) T1
union all
select a, b
from (
select a, b
from (
Select a, b, d
from t1
where (a < 33)
) T1
union all
select a, b
from (
Select a, b
from t2
where (40 = 85)
) T2
) T2
) T1
union all
select d_r_l_r_r_r_l, b_r
from (
Select d_r_l_r_r_r_l, b_r
from (
select d_l_l, e_r_l, c_l_r, d_r_l_r_r_r
from (
Select d_l_l, e_r_l, c_l_r, d_r_l_r_r_r
from (
Select d_l, e_r, b_r
from (
Select d
from t4
where (b = 22)
) T1(d_l)
full join (
Select e, b
from t2
where (e > (a - b))
) T2(e_r, b_r)
on (12 < e_r)
) T1(d_l_l, e_r_l, b_r_l)
full join (
Select c_l, d_r_l_r_r
from (
Select e, c
from t2
where (c = (89 + (14 - 15)))
) T1(e_l, c_l)
full join (
Select d_l, d_r_l_r
from (
Select d
from t2
where (b > d)
) T1(d_l)
left join (
select d_r_l, b_r
from (
Select d_r_l, b_r
from (
Select c_l, d_r
from (
Select c
from t1
where (27 = e)
) T1(c_l)
full join (
Select d
from t2
where ((47 * d) < b)
) T2(d_r)
on ((91 * (d_r * 26)) = c_l)
) T1(c_l_l, d_r_l)
left join (
select b
from (
Select b
from t1
where (23 > (19 - c))
) T1
union all
select c
from (
Select c, b
from t2
where ((((d + e) + (84 * b)) + (12 * 47)) < d)
) T2
) T2(b_r)
on (51 < 95)
) T1
union all
select e, b
from (
Select e, b
from t2
where (d = (22 + 73))
) T2
) T2(d_r_l_r, b_r_r)
on (83 > d_l)
) T2(d_l_r, d_r_l_r_r)
on ((52 - ((59 - 10) * 69)) > 86)
) T2(c_l_r, d_r_l_r_r_r)
on (c_l_r < (43 * 28))
) T1
union all
select c_l, a_l, c_r, d_r
from (
Select c_l, a_l, c_r, d_r
from (
select c, a
from (
Select c, a
from t5
where ((83 - 4) < (a - 26))
) T1
union all
select b_l_r_r_l, a_l_l
from (
Select b_l_r_r_l, a_l_l, b_l_l, b_r, d_r
from (
Select a_l, b_l, b_l_r_r, a_l_r, e_l_r_r
from (
Select a, b
from t3
where (4 > e)
) T1(a_l, b_l)
full join (
select a_l, e_l_r, b_l_r
from (
Select a_l, e_l_r, b_l_r
from (
Select a
from t1
where (32 > c)
) T1(a_l)
left join (
select e_l, b_l
from (
Select e_l, b_l, a_l_r, e_r_r
from (
Select e, b
from t1
where (81 = c)
) T1(e_l, b_l)
full join (
Select a_l, b_l, e_r
from (
Select a, b
from t4
where (4 = 50)
) T1(a_l, b_l)
left join (
Select e
from t2
where (e > d)
) T2(e_r)
on ((64 - b_l) < 60)
) T2(a_l_r, b_l_r, e_r_r)
on (e_r_r < e_l)
) T1
union all
select e, c
from (
Select e, c
from t5
where ((b * (d + a)) < e)
) T2
) T2(e_l_r, b_l_r)
on (b_l_r = (b_l_r + 16))
) T1
union all
select b_r_r_r_l, d_l_l, b_r_r_l_r
from (
Select b_r_r_r_l, d_l_l, b_r_r_l_r, a_r_r, a_l_r_l_r, c_r_r
from (
Select d_l, b_r_r_r, d_r_l_r
from (
Select d
from t3
where (29 = e)
) T1(d_l)
full join (
Select d_r_l, b_r_r, e_r_l_r
from (
Select c_l, d_r
from (
select c
from (
Select c, a
from t1
where (13 > 74)
) T1
union all
select a
from (
Select a
from t2
where (b = b)
) T2
) T1(c_l)
full join (
Select d
from t5
where (0 > e)
) T2(d_r)
on (d_r > 84)
) T1(c_l_l, d_r_l)
left join (
Select e_r_l, b_r
from (
Select c_l, e_r, c_r
from (
Select e, c, a
from t5
where (e > e)
) T1(e_l, c_l, a_l)
left join (
Select e, c, d
from t2
where ((c - 56) = a)
) T2(e_r, c_r, d_r)
on (76 = c_r)
) T1(c_l_l, e_r_l, c_r_l)
left join (
Select a, b
from t1
where (b < a)
) T2(a_r, b_r)
on ((b_r + b_r) > 67)
) T2(e_r_l_r, b_r_r)
on (13 = 44)
) T2(d_r_l_r, b_r_r_r, e_r_l_r_r)
on (((d_l * (76 + b_r_r_r)) * 78) > 54)
) T1(d_l_l, b_r_r_r_l, d_r_l_r_l)
full join (
Select a_l_r_l, b_r_r_l, c_r, a_r, d_r
from (
Select d_l_r_l, a_l_r, b_r_r
from (
Select a_l, d_l_r
from (
Select a
from t4
where (b = 49)
) T1(a_l)
left join (
Select a_l, d_l, b_l_r
from (
Select a, d
from t5
where (((a - c) + a) = (99 * (86 + 46)))
) T1(a_l, d_l)
full join (
Select b_l, b_r_l_l_r
from (
Select b
from t5
where (46 > a)
) T1(b_l)
full join (
Select b_r_l_l, c_r_l, c_r, a_r, b_r
from (
Select b_r_l, b_l_l, c_r
from (
Select b_l, b_r
from (
Select b
from t4
where (c > 68)
) T1(b_l)
left join (
Select c, b
from t3
where (40 = 68)
) T2(c_r, b_r)
on (((b_l - (b_r * ((b_r * 39) - (34 * b_l)))) * 93) = (16 * b_l))
) T1(b_l_l, b_r_l)
left join (
Select c
from t3
where (b < c)
) T2(c_r)
on (c_r < c_r)
) T1(b_r_l_l, b_l_l_l, c_r_l)
left join (
Select c, a, b, d
from t2
where (c > 59)
) T2(c_r, a_r, b_r, d_r)
on (c_r_l < b_r)
) T2(b_r_l_l_r, c_r_l_r, c_r_r, a_r_r, b_r_r)
on (b_r_l_l_r > 54)
) T2(b_l_r, b_r_l_l_r_r)
on ((b_l_r + a_l) = b_l_r)
) T2(a_l_r, d_l_r, b_l_r_r)
on (a_l = 18)
) T1(a_l_l, d_l_r_l)
left join (
Select a_l, d_l, b_r
from (
Select c, a, d
from t4
where ((73 - (17 + a)) = 4)
) T1(c_l, a_l, d_l)
full join (
Select a, b, d
from t1
where (e = 99)
) T2(a_r, b_r, d_r)
on (28 = 61)
) T2(a_l_r, d_l_r, b_r_r)
on ((a_l_r - a_l_r) < 80)
) T1(d_l_r_l_l, a_l_r_l, b_r_r_l)
full join (
Select c, a, d
from t5
where (d = 95)
) T2(c_r, a_r, d_r)
on (85 < a_r)
) T2(a_l_r_l_r, b_r_r_l_r, c_r_r, a_r_r, d_r_r)
on (d_l_l = b_r_r_r_l)
) T2
) T2(a_l_r, e_l_r_r, b_l_r_r)
on (b_l > b_l_r_r)
) T1(a_l_l, b_l_l, b_l_r_r_l, a_l_r_l, e_l_r_r_l)
left join (
Select b, d
from t4
where (a > 35)
) T2(b_r, d_r)
on (d_r > 94)
) T2
) T1(c_l, a_l)
left join (
Select c, d
from t4
where (b < d)
) T2(c_r, d_r)
on (((82 - 92) + (a_l + d_r)) > 54)
) T2
) T1(d_l_l_l, e_r_l_l, c_l_r_l, d_r_l_r_r_r_l)
left join (
Select b
from t1
where (e < b)
) T2(b_r)
on (d_r_l_r_r_r_l > b_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l
from (
Select c_l, a_l, c_r_r_r
from (
Select c, a
from t4
where (e > ((75 - c) * (b * 12)))
) T1(c_l, a_l)
left join (
Select c_l, a_l_r, c_r_r
from (
Select c
from t2
where (27 > b)
) T1(c_l)
inner join (
Select a_l, d_l, c_r
from (
Select a, d
from t5
where (88 = 59)
) T1(a_l, d_l)
full join (
Select c, b
from t4
where (b = 71)
) T2(c_r, b_r)
on (45 = c_r)
) T2(a_l_r, d_l_r, c_r_r)
on ((28 - c_l) = (a_l_r + (c_r_r - c_r_r)))
) T2(c_l_r, a_l_r_r, c_r_r_r)
on (11 = c_l)
) T1
union all
select d
from (
Select d
from t2
where (53 = d)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t5
where ((74 - a) > e)
) T1
union all
select e
from (
Select e, a, d
from t2
where ((c * a) < 22)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test35exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

