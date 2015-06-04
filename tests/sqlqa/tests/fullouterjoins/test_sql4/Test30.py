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
    
def test001(desc="""Joins Set 30"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select a
from (
Select a
from t5
where (e = c)
) T1
union all
select c
from (
Select c, b
from t4
where (73 = ((e * a) + e))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test30exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, a, b, d
from t4
where (a = 66)
) T1
union all
select a
from (
select a
from (
Select a
from t3
where (45 < 12)
) T1
union all
select c
from (
Select c
from t2
where (c > 0)
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
    _dci.expect_file(output, defs.test_dir + """/Test30exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l
from (
Select e_l, c_l, d_l, c_r
from (
Select e, c, d
from t1
where (e < (c - c))
) T1(e_l, c_l, d_l)
full join (
select c
from (
Select c, b
from t2
where ((c * 63) < 20)
) T1
union all
select c
from (
Select c
from t4
where (d = 6)
) T2
) T2(c_r)
on (63 > 60)
) T1
union all
select b
from (
Select b
from t1
where (51 > (73 - (b + a)))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test30exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, d
from t5
where (((65 - 5) + e) = 59)
) T1
union all
select b, d
from (
select b, d
from (
Select b, d
from t4
where (e = 31)
) T1
union all
select b_l, e_r
from (
Select b_l, e_r, a_r
from (
Select c, a, b
from t5
where (17 > a)
) T1(c_l, a_l, b_l)
inner join (
Select e, a, b
from t5
where (b < c)
) T2(e_r, a_r, b_r)
on (a_r = 54)
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
    _dci.expect_file(output, defs.test_dir + """/Test30exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
select e, b
from (
Select e, b
from t5
where (43 = (d * 96))
) T1
union all
select e_l_l, c_r
from (
Select e_l_l, c_r
from (
Select e_l, b_r
from (
select e
from (
Select e
from t5
where ((c - a) = 95)
) T1
union all
select b
from (
Select b
from t2
where ((21 - a) = 46)
) T2
) T1(e_l)
left join (
Select c, b
from t2
where (47 = 97)
) T2(c_r, b_r)
on ((b_r - b_r) < 92)
) T1(e_l_l, b_r_l)
inner join (
Select c
from t2
where (67 > c)
) T2(c_r)
on (c_r = e_l_l)
) T2
) T1
union all
select a, b
from (
Select a, b, d
from t4
where (c = c)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test30exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t1
where ((44 * (92 * (c + 17))) > ((39 * c) - a))
) T1
union all
select e
from (
Select e, c, a
from t4
where (c = b)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test30exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l_l
from (
Select a_l_l, e_r, a_r, d_r
from (
select a_l
from (
Select a_l, b_l, a_l_r, c_l_r, e_l_r
from (
select a, b
from (
Select a, b, d
from t2
where (95 = 27)
) T1
union all
select c, d
from (
Select c, d
from t5
where (e > e)
) T2
) T1(a_l, b_l)
full join (
Select e_l, c_l, a_l, a_l_l_l_l_r, b_r_r
from (
Select e, c, a, d
from t1
where (c = 16)
) T1(e_l, c_l, a_l, d_l)
full join (
Select a_l_l_l_l, a_r, b_r
from (
Select b_r_l, a_l_l_l, d_r
from (
Select a_l_l, e_r_l, e_r, b_r
from (
select a_l, e_r
from (
Select a_l, e_r
from (
Select a
from t4
where (((d * 74) - 58) = 77)
) T1(a_l)
left join (
Select e, c, b
from t4
where (c > 11)
) T2(e_r, c_r, b_r)
on (a_l = a_l)
) T1
union all
select e, a
from (
Select e, a, b
from t3
where (b = 27)
) T2
) T1(a_l_l, e_r_l)
left join (
Select e, a, b
from t1
where (93 > a)
) T2(e_r, a_r, b_r)
on (b_r = 95)
) T1(a_l_l_l, e_r_l_l, e_r_l, b_r_l)
inner join (
Select e, a, d
from t5
where (20 > 2)
) T2(e_r, a_r, d_r)
on ((62 - 13) > a_l_l_l)
) T1(b_r_l_l, a_l_l_l_l, d_r_l)
left join (
Select c, a, b
from t5
where ((90 + (95 + (1 + (((d + 6) * 41) * 53)))) = e)
) T2(c_r, a_r, b_r)
on (a_l_l_l_l = a_r)
) T2(a_l_l_l_l_r, a_r_r, b_r_r)
on (0 = c_l)
) T2(e_l_r, c_l_r, a_l_r, a_l_l_l_l_r_r, b_r_r_r)
on (61 < b_l)
) T1
union all
select a
from (
select a
from (
Select a
from t4
where (7 = b)
) T1
union all
select c
from (
Select c
from t2
where ((98 - a) = e)
) T2
) T2
) T1(a_l_l)
left join (
Select e, a, d
from t2
where (90 < c)
) T2(e_r, a_r, d_r)
on ((((44 * d_r) + a_r) + a_l_l) = a_r)
) T1
union all
select d
from (
Select d
from t4
where ((d + c) < 84)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test30exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t5
where (b < e)
) T1
union all
select c
from (
Select c
from t4
where (c = 89)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test30exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #******************************************
    
    _testmgr.testcase_end(desc)

