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
    
def test001(desc="""Joins Set 39"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select e, a
from (
Select e, a, d
from t2
where (2 = a)
) T1
union all
select e, a
from (
select e, a
from (
Select e, a, b
from t4
where ((56 - b) > (d - 77))
) T1
union all
select c, b
from (
Select c, b
from t4
where (d < a)
) T2
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test39exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
select c
from (
Select c, a, b
from t5
where ((d + (c - 62)) > 51)
) T1
union all
select e
from (
select e
from (
Select e, a, b, d
from t3
where (d = (35 + d))
) T1
union all
select a_l
from (
select a_l
from (
Select a_l, b_l, e_r, c_r
from (
Select e, a, b
from t2
where (c = 50)
) T1(e_l, a_l, b_l)
left join (
Select e, c, d
from t1
where (5 < d)
) T2(e_r, c_r, d_r)
on (95 = 81)
) T1
union all
select d
from (
Select d
from t3
where ((87 - (31 - 19)) = b)
) T2
) T2
) T2
) T1
union all
select e_l_l
from (
Select e_l_l, b_r, d_r
from (
Select e_l, d_l, e_r
from (
Select e, d
from t3
where (b = c)
) T1(e_l, d_l)
inner join (
Select e, a, b
from t2
where (64 = 50)
) T2(e_r, a_r, b_r)
on ((e_l - d_l) < (((e_l - e_l) + d_l) * e_r))
) T1(e_l_l, d_l_l, e_r_l)
left join (
Select c, b, d
from t5
where (e > 66)
) T2(c_r, b_r, d_r)
on (83 = 41)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test39exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, a
from t1
where (((((95 * 92) - c) - b) - 7) = 32)
) T1
union all
select b, d
from (
Select b, d
from t3
where (e > 4)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test39exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
select b, d
from (
Select b, d
from t3
where (d = d)
) T1
union all
select c, d
from (
Select c, d
from t1
where (c > b)
) T2
) T1
union all
select d
from (
Select d
from t1
where ((b * a) > a)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test39exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
Select a, b, d
from t1
where (90 < 3)
) T1
union all
select e, c
from (
Select e, c
from t3
where (c < c)
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
select e, c
from (
Select e, c
from t3
where ((63 + 25) = 8)
) T1
union all
select c_l, b_r
from (
Select c_l, b_r
from (
select c
from (
Select c, a, d
from t2
where (91 = a)
) T1
union all
select c
from (
Select c
from t5
where (e > 67)
) T2
) T1(c_l)
left join (
Select a, b
from t5
where (77 = (e - e))
) T2(a_r, b_r)
on (83 = 95)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test39exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, d
from (
Select c, d
from t1
where (73 > e)
) T1
union all
select e, c
from (
select e, c, b, d
from (
Select e, c, b, d
from t3
where (93 = (51 + (c * (b - ((a * c) * b)))))
) T1
union all
select e_l, c_l, c_l_r, d_l_r
from (
Select e_l, c_l, c_l_r, d_l_r
from (
Select e, c, b
from t3
where (53 = (c + e))
) T1(e_l, c_l, b_l)
left join (
Select c_l, d_l, c_l_r, c_r_r
from (
select c, d
from (
Select c, d
from t2
where (d = (10 - e))
) T1
union all
select c, b
from (
Select c, b, d
from t4
where (d = b)
) T2
) T1(c_l, d_l)
full join (
Select c_l, c_r
from (
select c, b
from (
Select c, b
from t3
where (d < 21)
) T1
union all
select c_r_l, a_r
from (
Select c_r_l, a_r
from (
Select b_l, c_r
from (
Select c, b
from t5
where (38 = 77)
) T1(c_l, b_l)
left join (
Select c
from t2
where (85 < 15)
) T2(c_r)
on (b_l < (13 * 22))
) T1(b_l_l, c_r_l)
full join (
Select a
from t1
where (48 = b)
) T2(a_r)
on (c_r_l = (a_r * 20))
) T2
) T1(c_l, b_l)
inner join (
select e, c
from (
Select e, c
from t1
where (72 < 32)
) T1
union all
select e, c
from (
Select e, c, a
from t3
where (57 < 64)
) T2
) T2(e_r, c_r)
on (87 = (c_l * (96 - c_r)))
) T2(c_l_r, c_r_r)
on (63 > 62)
) T2(c_l_r, d_l_r, c_l_r_r, c_r_r_r)
on (61 < 45)
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
    _dci.expect_file(output, defs.test_dir + """/Test39exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, d_l
from (
Select e_l, d_l, c_r
from (
Select e, d
from t5
where (56 = (2 + c))
) T1(e_l, d_l)
full join (
Select c, b
from t3
where (57 = ((d + (c + 46)) + 91))
) T2(c_r, b_r)
on (d_l = c_r)
) T1
union all
select c_l, e_l_r
from (
Select c_l, e_l_r
from (
Select c, b
from t4
where (47 < (69 * 87))
) T1(c_l, b_l)
left join (
Select e_l, d_r
from (
select e
from (
Select e
from t4
where (54 < b)
) T1
union all
select c
from (
Select c, b
from t3
where (33 = e)
) T2
) T1(e_l)
inner join (
Select d
from t4
where (b = (32 + b))
) T2(d_r)
on ((53 + e_l) = d_r)
) T2(e_l_r, d_r_r)
on (58 = c_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test39exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b
from t2
where (d > 22)
) T1
union all
select e, c
from (
Select e, c
from t3
where (14 > (71 + e))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test39exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

