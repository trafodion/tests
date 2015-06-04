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
    
def test001(desc="""Joins Set 22"""):
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
from t2
where (a = c)
) T1
union all
select b
from (
Select b, d
from t2
where ((63 - (71 + a)) = 40)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test22exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l, e_r
from (
Select b_l, e_r
from (
Select b
from t5
where (59 < 69)
) T1(b_l)
left join (
Select e
from t5
where (d > (d * 22))
) T2(e_r)
on (b_l < (b_l + b_l))
) T1
union all
select e, d
from (
Select e, d
from t3
where (a < d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test22exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l, c_r_r_r_r
from (
Select b_l, c_r_r_r_r
from (
Select c, b
from t5
where (25 = 60)
) T1(c_l, b_l)
full join (
Select a_r_l, b_l_l, c_r_r_r
from (
Select b_l, a_r
from (
Select b
from t5
where (e = e)
) T1(b_l)
full join (
Select c, a
from t2
where (c > (50 - (84 - (e * 6))))
) T2(c_r, a_r)
on (a_r = a_r)
) T1(b_l_l, a_r_l)
inner join (
Select d_l, a_l_r, c_r_r
from (
Select e, b, d
from t2
where (b < 38)
) T1(e_l, b_l, d_l)
left join (
Select a_l, c_r
from (
Select a
from t2
where (a < d)
) T1(a_l)
left join (
Select c
from t5
where (e < 55)
) T2(c_r)
on (75 = c_r)
) T2(a_l_r, c_r_r)
on (61 = d_l)
) T2(d_l_r, a_l_r_r, c_r_r_r)
on (c_r_r_r = (b_l_l * c_r_r_r))
) T2(a_r_l_r, b_l_l_r, c_r_r_r_r)
on (b_l = (c_r_r_r_r * 73))
) T1
union all
select e, a
from (
Select e, a, d
from t5
where (59 = 59)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test22exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t4
where (70 > 97)
) T1
union all
select b_r_l
from (
Select b_r_l, c_r_l, a_l_r, a_r_l_r_r
from (
Select c_l, b_l, e_r, c_r, b_r
from (
Select e, c, b, d
from t3
where (89 > 59)
) T1(e_l, c_l, b_l, d_l)
full join (
Select e, c, b
from t4
where (50 < b)
) T2(e_r, c_r, b_r)
on (75 > c_r)
) T1(c_l_l, b_l_l, e_r_l, c_r_l, b_r_l)
full join (
Select a_l, a_r_l_r
from (
Select a, b, d
from t3
where (e = b)
) T1(a_l, b_l, d_l)
left join (
Select a_r_l, a_r
from (
select d_l_l, c_r, a_r
from (
Select d_l_l, c_r, a_r
from (
Select d_l, a_r, b_r
from (
Select d
from t2
where (e = 59)
) T1(d_l)
left join (
Select a, b
from t2
where (62 > 13)
) T2(a_r, b_r)
on (85 < b_r)
) T1(d_l_l, a_r_l, b_r_l)
left join (
Select c, a, b
from t1
where (c > 57)
) T2(c_r, a_r, b_r)
on (((47 - a_r) + a_r) > 92)
) T1
union all
select e, c, a
from (
Select e, c, a
from t2
where (0 > 78)
) T2
) T1(d_l_l_l, c_r_l, a_r_l)
inner join (
Select e, a
from t2
where (73 > 41)
) T2(e_r, a_r)
on (a_r > 46)
) T2(a_r_l_r, a_r_r)
on (a_l = 28)
) T2(a_l_r, a_r_l_r_r)
on (a_l_r > c_r_l)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test22exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l
from (
Select a_l, d_l, c_r
from (
Select a, d
from t5
where (59 < e)
) T1(a_l, d_l)
inner join (
Select c
from t4
where (80 = 56)
) T2(c_r)
on (d_l = 23)
) T1
union all
select c
from (
Select c
from t5
where (e < 97)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test22exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b
from t1
where (70 = 29)
) T1
union all
select c, a
from (
Select c, a, d
from t4
where (a > d)
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
Select e
from t5
where (((74 * a) * 93) > (59 + a))
) T1
union all
select e
from (
Select e, a
from t3
where (d > 72)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test22exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b
from t1
where (12 > e)
) T1
union all
select c_r_r_l_l, e_l_r
from (
Select c_r_r_l_l, e_l_r, e_r_r
from (
Select a_l_l, c_r_r_l, a_r, d_r
from (
Select a_l, b_l, c_r_r
from (
Select a, b
from t1
where ((48 - (21 + 18)) = e)
) T1(a_l, b_l)
left join (
Select c_l, c_r, d_r
from (
select c
from (
Select c, b, d
from t5
where (62 < d)
) T1
union all
select c
from (
Select c
from t4
where (b = (27 * a))
) T2
) T1(c_l)
left join (
Select c, d
from t4
where (b = d)
) T2(c_r, d_r)
on (c_r > (c_r - (15 * d_r)))
) T2(c_l_r, c_r_r, d_r_r)
on (50 = (67 - 74))
) T1(a_l_l, b_l_l, c_r_r_l)
left join (
Select a, d
from t5
where (c < 97)
) T2(a_r, d_r)
on ((83 - d_r) < 33)
) T1(a_l_l_l, c_r_r_l_l, a_r_l, d_r_l)
left join (
Select e_l, a_l, e_r
from (
Select e, a
from t1
where (82 = c)
) T1(e_l, a_l)
left join (
Select e, b, d
from t3
where ((((e * 84) * 52) - 21) = 1)
) T2(e_r, b_r, d_r)
on (24 < e_l)
) T2(e_l_r, a_l_r, e_r_r)
on ((e_l_r - e_l_r) < c_r_r_l_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test22exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

