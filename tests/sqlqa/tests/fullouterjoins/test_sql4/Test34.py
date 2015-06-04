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
    
def test001(desc="""Joins Set 34"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select e_l_l, b_l_l, e_r
from (
Select e_l_l, b_l_l, e_r
from (
Select e_l, b_l, e_r
from (
Select e, c, b
from t4
where ((c + 86) = 33)
) T1(e_l, c_l, b_l)
inner join (
Select e, a
from t5
where ((b + e) > 80)
) T2(e_r, a_r)
on (b_l > (7 * (14 * e_r)))
) T1(e_l_l, b_l_l, e_r_l)
left join (
Select e, d
from t1
where (29 = 76)
) T2(e_r, d_r)
on ((66 * b_l_l) < 59)
) T1
union all
select e, c, d
from (
Select e, c, d
from t5
where (e = 51)
) T2
order by 1, 2, 3
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
select b, d
from (
Select b, d
from t2
where (8 > 67)
) T1
union all
select d_l, b_r
from (
Select d_l, b_r
from (
Select e, d
from t5
where (89 > d)
) T1(e_l, d_l)
left join (
Select b, d
from t3
where (c > 9)
) T2(b_r, d_r)
on (b_r < d_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test34exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, b_l, a_r_r, d_l_r
from (
Select a_l, b_l, a_r_r, d_l_r
from (
Select a, b
from t4
where (e = (86 * e))
) T1(a_l, b_l)
left join (
Select d_l, a_r
from (
Select d
from t5
where (d = e)
) T1(d_l)
left join (
Select a
from t5
where (0 > (22 + (a + (69 * (d * (54 * 7))))))
) T2(a_r)
on (a_r = (53 + 96))
) T2(d_l_r, a_r_r)
on (a_r_r < 70)
) T1
union all
select a_l_l, b_r_l, c_r, d_r
from (
Select a_l_l, b_r_l, c_r, d_r
from (
Select a_l, b_r
from (
Select a
from t4
where (d > d)
) T1(a_l)
left join (
Select e, c, b, d
from t4
where ((30 + c) < 99)
) T2(e_r, c_r, b_r, d_r)
on (a_l > 58)
) T1(a_l_l, b_r_l)
inner join (
select c, d
from (
select c, d
from (
Select c, d
from t2
where (12 = (38 + c))
) T1
union all
select c, b
from (
Select c, b, d
from t2
where (b > 86)
) T2
) T1
union all
select e, c
from (
Select e, c
from t1
where (39 = (c - a))
) T2
) T2(c_r, d_r)
on (d_r = 91)
) T2
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test34exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a, b
from (
Select e, a, b
from t1
where (97 = 25)
) T1
union all
select e, c, b
from (
Select e, c, b
from t5
where (c = a)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test34exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
Select a, b
from t5
where (c = c)
) T1
union all
select e, c
from (
Select e, c, b
from t2
where (b = 92)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test34exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t3
where (7 = 60)
) T1
union all
select e
from (
Select e, c
from t4
where (d > 73)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test34exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
Select a, b
from t4
where (84 = (c - 92))
) T1
union all
select c_l, b_l
from (
Select c_l, b_l, b_r
from (
Select c, a, b
from t2
where (b < c)
) T1(c_l, a_l, b_l)
left join (
select a, b
from (
Select a, b, d
from t4
where (37 < (a + 18))
) T1
union all
select c, d
from (
Select c, d
from t1
where (c = b)
) T2
) T2(a_r, b_r)
on (b_r = c_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test34exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t1
where ((b * c) < 30)
) T1
union all
select e_l
from (
Select e_l, b_l, c_r
from (
Select e, b
from t3
where (e = 92)
) T1(e_l, b_l)
left join (
Select c
from t1
where (c = a)
) T2(c_r)
on (23 = (94 + b_l))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test34exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t4
where ((4 * (83 + 91)) > (e - e))
) T1
union all
select a_l
from (
Select a_l, e_r
from (
Select e, a
from t1
where ((d + (17 * 36)) = 32)
) T1(e_l, a_l)
full join (
Select e, a
from t1
where (77 = (82 * 15))
) T2(e_r, a_r)
on (36 = (2 * e_r))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test34exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

