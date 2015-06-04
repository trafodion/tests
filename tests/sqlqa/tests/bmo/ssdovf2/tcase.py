# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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

import os
from ...lib import hpdci
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None

def _init(hptestmgr, testlist=[]):
	global _testmgr
	global _testlist
	global _dci

	_testmgr = hptestmgr
	_testlist = testlist
	# default hpdci was created using 'SQL' as the proc name.
	# this default instance shows 'SQL>' as the prompt in the log file.
	_dci = _testmgr.get_default_dci_proc()

def test001(desc="""b01"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='b01'
	
	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)	

	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY '5';"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)	

	stmt = """prepare xx from 
			select [first 5]   F01.val01, D01.val01, D02.val01, D03.val01
			From F01
			inner join D01 on D01.pk=F01.fk_d01
			inner join D02 on D02.pk=F01.fk_d02
			left join D03 on D03.pk=F01.fk_d03
			order by 1,2,3,4;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)

	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '5')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY reset;"""
	output = _dci.cmdexec(stmt)
	
	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')
	_dci.expect_any_substr(output, 'EX_HASHJ')

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

def test002(desc="""b02"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='b02'
	
	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY '5';"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """prepare xx from 
			select [first 5] T01.val02, T02.val02
			from
			(
			Select F01.val02, D01.val01
			From F01
			right join D01 on D01.pk=F01.fk_d01
			where D01.val01>0
			) as T01(val01,val02)
			right join
			(
			Select F02.val02, D02.val01
			From F02
			right join D02 on D02.pk=F02.fk_d02
			where D02.val01>1
			) as T02(val01,val02)
			on (T01.val02=T02.val02)
			where T02.val02>4
			order by 1,2;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)

	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '0')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """cqd SSD_BMO_MAX_MEM_THRESHOLD_IN_MB reset;"""
	output = _dci.cmdexec(stmt)
	
	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')
	_dci.expect_any_substr(output, 'EX_HASHJ')

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

def test003(desc="""b03"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='b03'

	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY '1';"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)	

	stmt = """prepare xx from 
			select [first 5]   TF01.val01, max(TD01.val01), count(TD03.val01), sum(TD03.val01), count(*)
			From
			(select F01.val01, F01.fk_d01, F01.fk_d02, F01.fk_d03
			From F01
			Where F01.val01>0) as TF01(val01,fk_d01,fk_d02,fk_d03)
			inner join
			(select D01.val01,count(D01.pk)
			from D01
			where D01.val01>0
			group by D01.val01) as TD01(val01,pk) on (TD01.pk=TF01.fk_d01
			AND TD01.pk>0 AND TF01.fk_d01>0)
			full outer join
			(select D02.val01,count(D02.pk)
			from D02
			where D02.val01>0
			group by D02.val01) as TD02(val01,pk) on (TD02.pk=TF01.fk_d02
			AND TD02.pk>0 AND TF01.fk_d02>0)
			full outer join
			(select D03.val01,count(D03.pk)
			from D03
			where D03.val01>0
			group by D03.val01) as TD03(val01,pk) on (TD03.pk=TF01.fk_d03
			AND TD03.pk>0 AND TF01.fk_d03>0)
			where TF01.val01>0 and TD01.val01 >0 and TD02.val01>0
			group by TF01.val01
			order by 1,2,3,4,5;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)
	
	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '0')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """cqd EXE_DIAGNOSTIC_EVENTS reset;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY reset;"""
	output = _dci.cmdexec(stmt)
	
	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')
	_dci.expect_any_substr(output, 'EX_HASHJ')

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

def test004(desc="""b04"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='b04'
	
	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY '1';"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """prepare xx from 
			select [first 15]   F01.val01, F01.val02
			From F01
			Where F01.val01>0 AND exists
			(
			select D01.val01
			From D01
			Where D01.val01 > 0 AND exists
			(
			select D02.val02
			From D02
			Where D02.val01>0
			)
			)
			order by 1,2;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)

	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '15')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY reset;"""
	output = _dci.cmdexec(stmt)
	
	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')
	_dci.expect_any_substr(output, 'EX_HASHJ')

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

def test005(desc="""b05"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='b05'

	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY '5';"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)	

	stmt = """prepare xx from 
			select [first 5] T01.val02, T02.val02
			from
			(
			Select F01.val02, D01.val01
			From F01
			right join D01 on D01.pk=F01.fk_d01
			where D01.val01>0
			) as T01(val01,val02)
			right join
			(
			Select F02.val01, F02.val02
			From F02
			where not exists
			(select val01
			from D02
			where D02.val02=F02.fk_d02
			)
			) as T02(val01,val02)
			on (T01.val02=T02.val01)
			where T02.val01>0
			order by 1,2;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)

	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '5')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY reset;"""
	output = _dci.cmdexec(stmt)
	
	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')
	_dci.expect_any_substr(output, 'EX_HASHJ')

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

def test006(desc="""b07"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='b07'

	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY '1';"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """prepare xx from 
			select [first 5]   TF01.val01, max(TD01.val01), count(TD02.val01), sum(TD03.val01), count(*)
			From
			(select F01.val01, F01.fk_d01, F01.fk_d02, F01.fk_d03
			From F01
			Where F01.val01>0) as TF01(val01,fk_d01,fk_d02,fk_d03)
			inner join
			(select D01.val01,count(D01.pk)
			from D01
			where D01.val01>0
			group by D01.val01) as TD01(val01,pk) on (TD01.pk=TF01.fk_d01
			AND TD01.pk>0 AND TF01.fk_d01>0)
			full outer join
			(select D02.val01,count(D02.pk)
			from D02
			where D02.val01>0
			group by D02.val01) as TD02(val01,pk) on (TD02.pk=TF01.fk_d02
			AND TD02.pk>0 AND TF01.fk_d02>0)
			full outer join
			(select D03.val01,count(D03.pk)
			from D03
			where D03.val01>0
			group by D03.val01) as TD03(val01,pk) on (TD03.pk=TF01.fk_d03
			AND TD03.pk>0 AND TF01.fk_d03>0)
			where TF01.val01>0 and TD01.val01 >0 and TD02.val01>0
			group by TF01.val01
			order by 1,2,3,4,5;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)
	
	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '0')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY reset;"""
	output = _dci.cmdexec(stmt)
	
	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')
	_dci.expect_any_substr(output, 'EX_HASHJ')
	_dci.expect_any_substr(output, 'EX_HASH_GRBY')
	
	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

def test007(desc="""b08"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='b08'

	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY '5';"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)	

	stmt = """prepare xx from 
			SELECT [first 10]F01.val01, D01.val01, D02.val01 From F01
			inner join D01 on D01.pk=F01.fk_d01 and D01.pk=9
			left join D02 on D02.pk=F01.fk_d02 order by 1,2,3 ;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)

	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '10')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY reset;"""
	output = _dci.cmdexec(stmt)
	
	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')
	_dci.expect_any_substr(output, 'EX_HASHJ')

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

def test008(desc="""b21"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='b21'

	stmt = """cqd EXE_MEM_LIMIT_PER_BMO_IN_MB '4';"""
	output = _dci.cmdexec(stmt)
	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY '1';"""
	output = _dci.cmdexec(stmt)
	
	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)	

	stmt = """prepare xx from 
			select [first 5]   F01.val01, D01.val01, D02.val01, D03.val01
			From F01
			inner join D01 on D01.pk=F01.fk_d01
			left join D02 on D02.pk=F01.fk_d02
			inner join D03 on D03.pk=F01.fk_d03
			order by 1,2,3,4;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)
	
	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '5')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """cqd EXE_MEM_LIMIT_PER_BMO_IN_MB reset;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY reset;"""
	output = _dci.cmdexec(stmt)

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')
	_dci.expect_any_substr(output, 'EX_HASHJ')

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

def test009(desc="""b22"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='b22'

	stmt = """cqd EXE_MEM_LIMIT_PER_BMO_IN_MB '4';"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY '1';"""
	output = _dci.cmdexec(stmt)

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """prepare xx from 
			select [first 50]   F01.val01, D01.val01, D02.val01, D03.val01
			From F01
			left join D01 on D01.pk=F01.fk_d01
			inner join D02 on D02.pk=F01.fk_d02
			inner join D03 on D03.pk=F01.fk_d03
			order by 1,2,3,4;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)

	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '50')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
		
	stmt = """cqd EXE_MEM_LIMIT_PER_BMO_IN_MB reset;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY reset;"""
	output = _dci.cmdexec(stmt)

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')
	_dci.expect_any_substr(output, 'EX_HASHJ')

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

def test010(desc="""b23"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='b23'

	stmt = """cqd EXE_MEM_LIMIT_PER_BMO_IN_MB '4';"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY '1';"""
	output = _dci.cmdexec(stmt)
	
	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """prepare xx from 
			select [first 5]   F01.val01, D01.val01, D02.val01, D03.val01
			From F01
			left join D01 on D01.pk=F01.fk_d01
			inner join D02 on D02.pk=F01.fk_d02
			left join D03 on D03.pk=F01.fk_d03
			order by 1,2,3,4;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)

	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '5')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
		
	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY reset;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_MEM_LIMIT_PER_BMO_IN_MB reset;"""
	output = _dci.cmdexec(stmt)

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')
	_dci.expect_any_substr(output, 'EX_HASHJ')

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

def test011(desc="""b17"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='b17'	

	stmt = """cqd EXE_MEM_LIMIT_PER_BMO_IN_MB '3';"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY '1';"""
	output = _dci.cmdexec(stmt)

	stmt = """cqd EXE_TEST_FORCE_CLUSTER_SPLIT_AFTER_MB '2';"""
	output = _dci.cmdexec(stmt)

	stmt = """cqd EXE_TEST_FORCE_HASH_LOOP_AFTER_NUM_BUFFERS '2';"""
	output = _dci.cmdexec(stmt)

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """prepare xx from 
			select * from Sales S left outer join Customers C on S.Cust_Id = C.Cust_Id order by 1;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)

	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '4')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
		
	stmt = """cqd EXE_MEM_LIMIT_PER_BMO_IN_MB reset;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY reset;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_FORCE_CLUSTER_SPLIT_AFTER_MB reset;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_FORCE_HASH_LOOP_AFTER_NUM_BUFFERS reset;"""
	output = _dci.cmdexec(stmt)

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

def test012(desc="""b18"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='b18'

	stmt = """cqd EXE_MEM_LIMIT_PER_BMO_IN_MB '3';"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY '1';"""
	output = _dci.cmdexec(stmt)

	stmt = """cqd EXE_TEST_FORCE_CLUSTER_SPLIT_AFTER_MB '2';"""
	output = _dci.cmdexec(stmt)

	stmt = """cqd EXE_TEST_FORCE_HASH_LOOP_AFTER_NUM_BUFFERS '2';"""
	output = _dci.cmdexec(stmt)

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """prepare xx from 
			select * from Sales S full outer join Customers C on S.Cust_Id = C.Cust_Id order by 1;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)

	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '5')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
		
	stmt = """cqd EXE_MEM_LIMIT_PER_BMO_IN_MB reset;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY reset;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_FORCE_CLUSTER_SPLIT_AFTER_MB reset;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_FORCE_HASH_LOOP_AFTER_NUM_BUFFERS reset;"""
	output = _dci.cmdexec(stmt)

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')
	_dci.expect_any_substr(output, 'EX_HASHJ')

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)

def test013(desc="""b20"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	id='b20'	

	stmt = """cqd EXE_MEM_LIMIT_PER_BMO_IN_MB '3';"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY '1';"""
	output = _dci.cmdexec(stmt)

	stmt = """cqd EXE_TEST_FORCE_CLUSTER_SPLIT_AFTER_MB '2';"""
	output = _dci.cmdexec(stmt)

	stmt = """cqd EXE_TEST_FORCE_HASH_LOOP_AFTER_NUM_BUFFERS '2';"""
	output = _dci.cmdexec(stmt)

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """prepare xx from 
			select * from Customers C where not exists ( select * from Sales S where S.Cust_Id = C.Cust_Id) order by 1;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_prepared_msg(output)
	
	stmt = """explain options 'f' xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """log """ + defs.work_dir + """/exp_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """explain xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """execute xx;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output, '1')

	stmt = """log """ + defs.work_dir + """/cur_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid current progress;"""
	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)

	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	qid = os.popen("""cat """ + defs.work_dir + """/cur_""" + id + """.log | grep '^Qid' | awk '{ print $2 }'""").read()	
	output = _testmgr.shell_call("""echo 'qid=""" + qid + """'""")
	
	stmt = """log """ + defs.work_dir + """/qid_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/def_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)

	stmt = """get statistics for qid """ + qid + """ default;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log """ + defs.work_dir + """/acc_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """get statistics for qid """ + qid + """ accumulated;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)

	stmt = """log """ + defs.work_dir + """/var_""" + id + """.log clear;"""
	output = _dci.cmdexec(stmt)
	stmt = """select variable_info from
			  table(statistics(NULL,'QID=""" + qid + """'));"""
	output = _dci.cmdexec(stmt)
	
	stmt = """log off;"""
	output = _dci.cmdexec(stmt)
		
	stmt = """cqd EXE_MEM_LIMIT_PER_BMO_IN_MB reset;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_HASH_FORCE_OVERFLOW_EVERY reset;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_FORCE_CLUSTER_SPLIT_AFTER_MB reset;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """cqd EXE_TEST_FORCE_HASH_LOOP_AFTER_NUM_BUFFERS reset;"""
	output = _dci.cmdexec(stmt)

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'Id TDB Name')
	_dci.expect_any_substr(output, 'EX_SORT')
	_dci.expect_any_substr(output, 'EX_HASHJ')

	output = _testmgr.shell_call("""cat """ + defs.work_dir + """/cur_""" + id + """.log""")
	_dci.expect_any_substr(output, 'MMAP')

	_testmgr.testcase_end(desc)
