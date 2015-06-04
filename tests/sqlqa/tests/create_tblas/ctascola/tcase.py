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

def _init(hptestmgr, testlist=[]):
	global _testmgr
	global _testlist
	global _dci

	_testmgr = hptestmgr
	_testlist = testlist
	# default hpdci was created using 'SQL' as the proc name.
	# this default instance shows 'SQL>' as the prompt in the log file.
	_dci = _testmgr.get_default_dci_proc()
	
	#############################################################################
	## These testcases have been written for the 'Create table as Select' feature
	##  The general idea for the feature was to allow a user to create a table like
	##   an existing table but populate it with the data at the same time.
	##  The creation of the table is done at the column attribute level and at the 
	##   table attribute level. This particular set of tests is testing the syntax 
	##   for the feature at the column attribute level. The specification used is 
	##   CREATE TABLE AS (CTAS) SQL STATEMENT.
	##   Syntax - Create table <tablename>[<column-attributes><table-attributes>] as <select-query>
	##  Tables used most frequently are created in the setup.
	#############################################################################

def test001(desc="""CTAS001"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# All columns selected - new table should have same columns and attributes as
	# original - but no primary key since I didn't specify it. and table is empty
	# ----------------------------------------------------------

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """create table Actors(
			f_no          int not null not droppable,
			f_name        varchar(30) not null,
			f_realname    varchar(50) default null,
			f_birthday    date  constraint md1a check (f_birthday > date '1900-01-01'),
			primary key (f_no)
			);"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	#turn pos off because I'm not specifying a primary key (works same with mode_teradata).
	stmt = """control query default POS 'OFF';"""
	output = _dci.cmdexec(stmt)
	 
	stmt = """Create table ctas001a as select f_no,f_name,f_realname,f_birthday from Actors;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_any_substr(output,'--- 0 row(s) inserted.')

	#the ddl should have all columns created with the column data types and column names unless specified as different as the original table
	stmt = """showddl table ctas001a;"""
	output = _dci.cmdexec(stmt)

	stmt = """select * from ctas001a;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_file(output, defs.test_dir + """/a001exp""", """a01s01""")
	_dci.expect_selected_msg(output,'0')

	#should also work as below getting the same results
	stmt = """create table ctas001b as select * from Actors;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_inserted_msg(output,'0')
	
	stmt = """showddl table ctas001b;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """select * from ctas001b;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output,'0')

	stmt = """control query default POS reset;"""
	output = _dci.cmdexec(stmt)
	
	_testmgr.testcase_end(desc)
	
def test002(desc="""CTAS002"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# All columns selected - new table should have same columns and attributes as 
	# original - but no primary key since I didn't specify it. and table isn't empty
	# Female_actors table created by setup script
	# ----------------------------------------------------------
	
	stmt = """control query default POS 'OFF';"""
	output = _dci.cmdexec(stmt)

	stmt = """Create table ctas002a as select f_no,f_name,f_realname,f_birthday from Female_actors;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_any_substr(output,'--- 5 row(s) inserted.')	

	stmt = """showddl table ctas002a;"""
	output = _dci.cmdexec(stmt)

	stmt = """select * from ctas002a order by f_no;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_file(output, defs.test_dir + """/a002exp""", """a02s02""")	

	#again with syntax more general
	
	stmt = """Create table ctas002b as select * from Female_actors;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_any_substr(output,'--- 5 row(s) inserted.')	

	stmt = """showddl table ctas002b;"""
	output = _dci.cmdexec(stmt)	

	stmt = """select * from ctas002b order by f_no;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_file(output, defs.test_dir + """/a002exp""", """a02s04""")	

	stmt = """control query default POS reset;"""
	output = _dci.cmdexec(stmt)

	_testmgr.testcase_end(desc)
	
def test003(desc="""CTAS003"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# error - an expression f_no+1 must be renamed
	# Female_actors table created by setup script
	# ----------------------------------------------------------

	
	stmt = """create table ctas003n store by (f_no) as select f_no+1 from Female_actors;"""
	output = _dci.cmdexec(stmt)
	output = _dci.expect_error_msg(output,'1099')

	_testmgr.testcase_end(desc)

def test004(desc="""CTAS004"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# correct expresssion as opposed to ctas003;
	# the integers in the new table are increased by 1.
	# Female_actors table created by setup script
	# ----------------------------------------------------------

	stmt = """create table ctas004 store by (n_no) as select f_no+1 n_no from Female_actors;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_any_substr(output,'--- 5 row(s) inserted.')		

	stmt = """showddl table ctas004;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """select * from ctas004 order by n_no;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_file(output, defs.test_dir + """/a004exp""", """a01s01""")	

	_testmgr.testcase_end(desc)

def test005(desc="""CTAS005"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# error data attributes must be compatible ie char vs int will not work;
	# It will work with mode_teradata
	# Female_actors table created by setup script
	# ----------------------------------------------------------

	stmt = """create table ctas005n (a_no char not null not droppable) store by (a_no) as select f_no from Female_actors;"""
	output = _dci.cmdexec(stmt)
	output = _dci.expect_error_msg(output,'4039')	

	_testmgr.testcase_end(desc)
	
def test006(desc="""CTAS006"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# data attributes must be compatible ie largeint vs int;
	# Female_actors table created by setup script
	# ----------------------------------------------------------

	stmt = """create table ctas006 (a largeint not null not droppable) store by (a) as select f_no from Female_actors;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_any_substr(output,'--- 5 row(s) inserted.')	
	
	stmt = """showddl table ctas006;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """select * from ctas006 order by a;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_file(output, defs.test_dir + """/a006exp""", """a06s1""")	

	_testmgr.testcase_end(desc)

def test007(desc="""CTAS007"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# select subset of table
	# Female_actors table created by setup script
	# ----------------------------------------------------------

	stmt = """create table ctas007 (w int not null not droppable,x char(30),y char(50)) store by (w) as select f_no,f_name,f_realname from Female_actors;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_any_substr(output,'--- 5 row(s) inserted.')
	
	stmt = """showddl table ctas007;"""
	output = _dci.cmdexec(stmt)	

	stmt = """select * from ctas007 order by w;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_file(output, defs.test_dir + """/a007exp""", """a07s2""")	

	_testmgr.testcase_end(desc)
	
def test008(desc="""CTAS008"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# error col attributes must contain all corresponding attributes;
	# Female_actors table created by setup script
	# ----------------------------------------------------------

	stmt = """create table ctas008(w largeint not null not droppable) store by (w) as select f_no,f_name,f_realname from Female_actors;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_any_substr(output,'ERROR[4023]')

	_testmgr.testcase_end(desc)
	
def test009(desc="""CTAS009"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# now use all of the values you want
	# Female_actors table created by setup script
	# ----------------------------------------------------------

	stmt = """create table ctas009(w largeint not null not droppable, x varchar(30), y varchar(50),z date) store by (w) as select f_no,f_name,f_realname,f_birthday from Female_actors;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_any_substr(output,'--- 5 row(s) inserted.')

	stmt = """showddl table ctas009;"""
	output = _dci.cmdexec(stmt)	

	stmt = """select * from ctas009 order by z;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_file(output, defs.test_dir + """/a009exp""", """a09s1""")	

	_testmgr.testcase_end(desc)
	
def test010(desc="""CTAS010"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# create table name (a) as select ....  verifying 'heading' attribute
	# heading isn't supported by create table as unless specified
	# ----------------------------------------------------------

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """showcontrol all;"""
	output = _dci.cmdexec(stmt)

	stmt = """Create table member(memnum  int  no default not null not droppable heading 'Member Number',
			first_name char(15) default ' ' not null not droppable heading 'First Name',
			last_name char(20) default ' ' not null not droppable  heading 'Last Name',
			primary key(memnum));"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)	

	stmt = """Alter table member add constraint memnum_constrnt check (memnum between 0001 and 9999);"""
	output = _dci.cmdexec(stmt)

	stmt = """create index xname on member (last_name,first_name);"""
	output = _dci.cmdexec(stmt)
	
	stmt = """showddl table member;"""
	output = _dci.cmdexec(stmt)	
	
	stmt = """insert into member values (0001,'Alpha','male');"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')
	
	stmt = """insert into member values (0002,'Alpha','female');"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')

	stmt = """insert into member values (0003,'Beta','male');"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')	
	
	stmt = """insert into member values (0004,'Beta','female');"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')

	stmt = """select * from member order by memnum;"""
	output = _dci.cmdexec(stmt)

	stmt = """create table crtas10a store by (memnum) as select memnum, first_name,last_name from member;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_inserted_msg(output,'4')	

	stmt = """showddl table crtas10a;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """select * from crtas10a order by memnum;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_file(output, defs.test_dir + """/a010exp""", """a10s4""")

	stmt = """create table crtas10b (memnum heading 'mynum', first_name heading 'ab', last_name heading 'fm') store by (mynum) as select memnum, first_name,last_name from member;"""
	output = _dci.cmdexec(stmt)

	stmt = """showddl crtas10b;"""
	output = _dci.cmdexec(stmt)

	_testmgr.testcase_end(desc)	

def test011(desc="""CTAS011"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# create table name (a) as select ....  COLUMN ATTRIBUTE testing mixed heading
	# ----------------------------------------------------------

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """showcontrol all;"""
	output = _dci.cmdexec(stmt)

	stmt = """Create table member2(memnum  int  no default not null not droppable no heading,
			first_name char(15) default ' ' not null not droppable heading 'First Name',
			last_name char(20) default ' ' not null not droppable  heading 'Last Name',
			primary key(memnum));"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """Alter table member2 add constraint memnum2_constrnt check (memnum between 0001 and 9999);"""
	output = _dci.cmdexec(stmt)

	stmt = """create index xname2 on member2 (last_name,first_name);"""
	output = _dci.cmdexec(stmt)

	stmt = """showddl table member2;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """insert into member2 values (0001,'Alpha','male');"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')
	
	stmt = """insert into member2 values (0002,'Alpha','female');"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')

	stmt = """insert into member2 values (0003,'Beta','male');"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')	
	
	stmt = """insert into member2 values (0004,'Beta','female');"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')

	stmt = """select * from member2 order by memnum;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_file(output, defs.test_dir + """/a011exp""", """a11s2""")

	stmt = """showddl table member2;"""
	output = _dci.cmdexec(stmt)

	#should get a heading also, since heading is a column attribute 
	stmt = """create table crtas11a store by (memnum) as select memnum, first_name,last_name from member;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_any_substr(output,'--- 4 row(s) inserted.')	

	stmt = """showddl table crtas11a;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """select * from crtas11a order by memnum;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_file(output, defs.test_dir + """/a011exp""", """a11s4""")

	stmt = """create table crtas11b(memnum int not null not droppable heading 'mynum', first_name char(15) heading 'ab', last_name char(20) no heading) store by (memnum) as select memnum, first_name,last_name from member;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_any_substr(output,'--- 4 row(s) inserted.')	

	stmt = """showddl table crtas11b;"""
	output = _dci.cmdexec(stmt)

	_testmgr.testcase_end(desc)

def test012(desc="""CTAS012"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# create table name (a) as select ....  COLUMN ATTRIBUTE testing upshift
	# ----------------------------------------------------------

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """Create table member3 (memnum  int  no default not null not droppable heading 'Member number',
			first_name char(15) upshift default ' ' not null not droppable heading 'First Name' ,
			last_name char(20)  default ' ' not null not droppable  heading 'Last Name' ,
			primary key(memnum));"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """Alter table member3 add constraint memnum3_constrnt check (memnum between 0001 and 9999);"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """create index xname3 on member3 (last_name,first_name);"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """showddl table member3;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """insert into member3 values (0001,'Alpha','male');"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')
	
	stmt = """insert into member3 values (0002,'Alpha','female');"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')

	stmt = """insert into member3 values (0003,'Beta','male');"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')	
	
	stmt = """insert into member3 values (0004,'Beta','female');"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')

	stmt = """select * from member3 order by memnum;"""
	output = _dci.cmdexec(stmt)

	stmt = """create table crtas12a store by (memnum) as select memnum, first_name,last_name from member;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_any_substr(output,'--- 4 row(s) inserted.')	

	stmt = """showddl table crtas12a;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """insert into crtas12a values (0005,'chi','female');"""
	output = _dci.cmdexec(stmt)
  
	stmt = """select * from crtas12a order by memnum;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_file(output, defs.test_dir + """/a012exp""", """a12s4""")

	stmt = """create table crtas12c (memnum int not null not droppable, first_name char(20) upshift, last_name char(30)) store by (memnum) as select memnum, first_name,last_name from member3;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'4')

	stmt = """update statistics for table crtas12c on every column;"""
	output = _dci.cmdexec(stmt)

	stmt = """select * from crtas12c order by 1,2;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_file(output, defs.test_dir + """/a012exp""", """a12s3""")

	#new inserted line should be in uppercase

	_testmgr.testcase_end(desc)
	
#def test013(desc="""CTAS013"""):
#	global _testmgr
#	global _testlist
#	global _dci
#	if not _testmgr.testcase_begin(_testlist): return
#
#	# ----------------------------------------------------------
#	# create table name (a) testing all (except nchar,nchar varying) data-types, using subset of rows
#	# ----------------------------------------------------------
#
#	stmt = """set list_count 25;"""
#	output = _dci.cmdexec(stmt)
#
#	# move following create table and loading data to setup file
#	# the same table b2uwl02 is also used by CTAS016
#	# create table to select from
#
#	stmt = """create table """ + defs.w_catalog + """.""" + defs.w_schema + """.ctas13a store by (sbin0_uniq) as select * from """ + defs.w_catalog + """.g_sqldopt.b2uwl02;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'0')	
#
#	stmt = """update statistics for table ctas13a on every column;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """showddl table ctas13a;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """select count(*) from """ + defs.w_catalog + """.""" + defs.w_schema + """.ctas13a order by sbin0_uniq;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_file(output, defs.test_dir + """/a013exp""", """a13s1""")
#
#	_testmgr.testcase_end(desc)	
	
def test014(desc="""CTAS014"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# datatypes - with column attributes and datatype info-date/time/timestamp
	# test puts on and off cqd's to show results of statement on particular applicable cqd
	# ----------------------------------------------------------

	stmt = """control query default mode_teradata off;"""
	output = _dci.cmdexec(stmt)

	stmt = """create table dt_time (field1  int not null not droppable primary key, 
			field2  date,
			field3  char (10),
			field4  timestamp(0),
			field5  timestamp(6),
			field6  time);"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """insert into dt_time values(1,current_date,'01-12-2007',current_timestamp,current_timestamp,current_time);"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')

	stmt = """create table ctas014a (time_o timestamp not null not droppable) store by(time_o) as select field4 from dt_time;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')

	stmt = """select * from ctas014a;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_selected_msg(output,'1')
	
	#try time into timestamp
	stmt = """create table ctas014b (time_o time not null not droppable) store by(time_o) as select field4 from dt_time;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_error_msg(output,'4039')
	
	stmt = """create table ctas014bc(time_o time not null not droppable) store by(time_o) as select cast(field4 as time) from dt_time;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')

	stmt = """showddl table ctas014bc;"""
	output = _dci.cmdexec(stmt)	

	stmt = """select * from ctas014bc;"""
	output = _dci.cmdexec(stmt)	

	#try reverse
	stmt = """create table ctas014c (time_o timestamp not null not droppable) store by(time_o) as select field6 from dt_time;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_error_msg(output,'4039')

	stmt = """create table ctas014ca (time_o timestamp not null not droppable) store by(time_o) as select cast(field6 as timestamp) from dt_time;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')

	stmt = """select * from ctas014ca;"""
	output = _dci.cmdexec(stmt)	

	#default control query defaults except for POS 'off' so I don't need a key;
	stmt = """create table ctas014d (dtfield date, intfield int not null not droppable) store by (intfield) as select field5,field1 from dt_time;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_error_msg(output,'4039')	

	stmt = """create table ctas014da (dtfield date, intfield int not null not droppable) store by (intfield) as select cast(field5 as date),field1 from dt_time;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'1')

	stmt = """select * from ctas014da;"""
	output = _dci.cmdexec(stmt)		

	stmt = """create table ctas014e (dtfield integer, intfield int not null not droppable) store by (intfield) as select field2 ,field1 from dt_time;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_error_msg(output,'4039')

	stmt = """create table ctas014ea (dtfield integer, intfield int not null not droppable) store by (intfield) as select cast(field2 as integer),field1 from dt_time;"""
	output = _dci.cmdexec(stmt)

	stmt = """select * from ctas014ea;"""
	output = _dci.cmdexec(stmt)

	stmt = """drop table dt_time;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """drop table ctas014a;"""
	output = _dci.cmdexec(stmt)

	stmt = """drop table ctas014b;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """drop table ctas014c;"""
	output = _dci.cmdexec(stmt)

	stmt = """drop table ctas014d;"""
	output = _dci.cmdexec(stmt)

	stmt = """drop table ctas014e;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """control query default mode_teradata reset;"""
	output = _dci.cmdexec(stmt)	

	_testmgr.testcase_end(desc)

#def test015(desc="""CTAS015"""):
#	global _testmgr
#	global _testlist
#	global _dci
#	if not _testmgr.testcase_begin(_testlist): return
#
#	# ----------------------------------------------------------
#	# datatypes - with column attributes and identity syntax
#	# test puts on and off cqd's to show results of statement on particular applicable cqd
#	# ----------------------------------------------------------
#
#	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """create table ctasch (col1 largeint generated by default as IDENTITY not null not droppable primary key,
#			col2  char(8) not null not droppable,
#			col3  varchar(50) ,
#			col4 char varying(50),
#			col5 pic x(10));"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """insert into ctasch (col2,col3,col4,col5) values ('AAAAAAAA','BBBBBBBBBBBBBBBCCCCCCCcccccccc','DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD','this is a');"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'1')
#
#	stmt = """insert into ctasch (col2,col3,col4,col5) values ('XXXXXXXX','this field is 50 char','this field is varying to 50','field pic');"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'1')
#
#	stmt = """select * from ctasch;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output,'2')
#
#	stmt = """create table ctas015a like ctasch as select * from ctasch;"""
#	output = _dci.cmdexec(stmt)
#	_dci.unexpect_any_substr(output,'ERROR')
#	_dci.expect_inserted_msg(output,'2')
#	_dci.expect_complete_msg(output)
#	
#	stmt = """alter table ctas015a alter column col1 set increment by 2;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#	
#	stmt = """insert into ctas015a (col2,col3,col4,col5) values ('zzzzzzzz','fffffffxxxxxx','eeeeeeeeeedddddddddddddd','zzzzzzzzzz');"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_error_msg(output,'8102')
#
#	stmt = """alter table ctas015a alter column col1 set increment by 1;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """insert into ctas015a (col2,col3,col4,col5) values ('zzzzzzzz','fffffffxxxxxx','eeeeeeeeeedddddddddddddd','zzzzzzzzzz');"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_inserted_msg(output,'1')
#
#	stmt = """insert into ctas015a (col2) values('YYYYYYYY');"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_inserted_msg(output,'1')
#	
#	stmt = """update statistics for table ctas015a on every column;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """select * from ctas015a;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output,'4')
#
#	stmt = """create table ctas015b (col1 largeint generated by default as IDENTITY not null not droppable,col2 char(8)) store by (col1) as select col1,col2 from ctasch;"""
#	output = _dci.cmdexec(stmt)
#	_dci.unexpect_any_substr(output,'ERROR')
#	_dci.expect_inserted_msg(output,'2')
#	_dci.expect_complete_msg(output)
#
#	stmt = """insert into ctas015b (col2) values('YYYYYYYY');"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_any_substr(output,'[3412]')
#	_dci.expect_inserted_msg(output,'1')
#
#	stmt = """create table ctas015c (col1 largeint generated by default as IDENTITY not null not droppable primary key,col2 char(8)) store by (col1) as select col1,col2 from ctasch;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_inserted_msg(output,'2')
#	_dci.expect_complete_msg(output)
#
#	stmt = """alter table ctas015c alter column col1 set increment by 2;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """insert into ctas015c (col1,col2) values (default,'zzzzzzzz');"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_error_msg(output,'8102')
#
#	stmt = """alter table ctas015c alter column col1 set increment by 1;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """insert into ctas015c (col1,col2) values (default,'zzzzzzzz');"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_inserted_msg(output)
#
#	stmt = """insert into ctas015c (col2) values('YYYYYYYY');"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_inserted_msg(output)
#
#	stmt = """update statistics for table ctas015c on every column;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """showddl table ctas015c;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """select col1 from ctas015c;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output,'4')
#	_dci.expect_file(output, defs.test_dir + """/a015exp""", """a15s1""")	
#
#	_testmgr.testcase_end(desc)
	
#def test016(desc="""CTAS016"""):
#	global _testmgr
#	global _testlist
#	global _dci
#	if not _testmgr.testcase_begin(_testlist): return
#
#	# ----------------------------------------------------------
#	# datatypes - with column attributes and datatype info-numeric
#	# ----------------------------------------------------------
#
#	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#	
#	
#	stmt = """set list_count 5;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """create table """ + defs.w_catalog + """.""" + defs.w_schema + """.ctas016 (
#			char2_2 char(2) not null not droppable,
#			sbinneg15_nuniq Largeint,
#			sdecneg15_100 Decimal(9) signed no default,
#			real17_n100 Real ,
#			double15_uniq  Double Precision,
#			double14_nuniq Float(23)) 
#			store by (char2_2) as 
#			select
#			char2_2, 
#			sbinneg15_nuniq,
#			sdecneg15_100,
#			real17_n100,
#			double15_uniq,
#			double14_nuniq
#			from """ + defs.w_catalog + """.g_sqldopt.b2uwl02;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """update statistics for table """ + defs.w_catalog + """.""" + defs.w_schema + """.ctas016 on every column;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """select * from """ + defs.w_catalog + """.""" + defs.w_schema + """.ctas016 order by SBINNEG15_NUNIQ;"""
#	output = _dci.cmdexec(stmt)
#	_dci.unexpect_any_substr(output,'ERROR')
#
#	#float(23) and double ok
#	stmt = """create table """ + defs.w_catalog + """.""" + defs.w_schema + """.ctas016a (char2_2 char(2) not null not droppable,field1 largeint,field2 double precision, field3 float(23)) store by (char2_2) as select distinct char2_2,sbinneg15_nuniq,double14_nuniq,double14_nuniq from ctas016;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'0')
#	
#	stmt = """get statistics;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """select * from ctas016a order by field1;"""
#	output = _dci.cmdexec(stmt)
#	_dci.unexpect_any_substr(output,'ERROR')	
#
#	#double precision into float
#	stmt = """create table ctas016b (char2_2 char(2) not null not droppable,field1 largeint ,field2 double precision , field3 float(23)) store by (char2_2) as select char2_2,sbinneg15_nuniq,double15_uniq,double15_uniq from ctas016;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'0')	
#
#	stmt = """get statistics;"""
#	output = _dci.cmdexec(stmt)	
#
#	stmt = """select * from ctas016b order by field1;"""
#	output = _dci.cmdexec(stmt)
#	_dci.unexpect_any_substr(output,'ERROR')
#
#	#double precision into real
#	stmt = """create table ctas016c(
#			char2_2 char(2) not null not droppable,
#			field1 largeint,
#			field2 double precision,
#			field3 real) store by (char2_2) as select char2_2,sbinneg15_nuniq,double15_uniq,double15_uniq from ctas016;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'0')	
#
#	stmt = """select * from ctas016c where char2_2 = 'AA' order by field1;"""
#	output = _dci.cmdexec(stmt)
#	_dci.unexpect_any_substr(output,'ERROR')	
#
#	#real datatype into double precision
#	stmt = """create table ctas016d (char2_2 char(2) not null not droppable,field1 largeint ,field2 double precision , field3 real) store by (char2_2) as select char2_2,sbinneg15_nuniq,real17_n100,real17_n100 from ctas016;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'0')	
#
#	stmt = """select * from ctas016d order by field1;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output,'0')	
#
#	#real datatype and decimal
#	stmt = """create table ctas016e(char2_2 char(2) not null not droppable,field1 largeint,field2 Decimal(9) signed no default, field3 real) store by (char2_2) as select char2_2,sbinneg15_nuniq,real17_n100,real17_n100 from ctas016;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'0')
#
#	stmt = """update statistics for table ctas016e on every column;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """select * from ctas016e;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output,'0')
#
#	#decimal datatype to real
#	stmt = """create table ctas016f(char2_2 char(2) not null not droppable,field1 largeint ,field2 Decimal(9) signed no default, field3 real) store by (char2_2) as select char2_2,sbinneg15_nuniq,sdecneg15_100,sdecneg15_100 from ctas016;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'0')
#
#	stmt = """get statistics;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """select * from ctas016f order by char2_2;"""
#	output = _dci.cmdexec(stmt)
#	_dci.unexpect_any_substr(output,'ERROR')
#
#	#double precision into float
#	stmt = """create table ctas016g (char2_2 char(2) not null not droppable,field1 largeint,field2 Decimal(9) signed no default, field3 float(23)) store by (char2_2) as select char2_2,sbinneg15_nuniq,double15_uniq,double15_uniq from ctas016;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'0')
#
#	stmt = """get statistics;"""
#	output = _dci.cmdexec(stmt)	
#
#	stmt = """select * from ctas016g order by field1;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output,'0')
#
#	stmt = """create table ctas016h (char2_2 char(2) not null not droppable,field1 largeint,field2 Decimal(9) signed no default, field3 float(23)) store by (char2_2) as select char2_2,sbinneg15_nuniq,sdecneg15_100,sdecneg15_100 from ctas016;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'0')
#
#	stmt = """get statistics;"""
#	output = _dci.cmdexec(stmt)	
#	
#	stmt = """select * from ctas016h order by field1;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output,'0')
#
#	stmt = """set list_count 4000000;"""
#	output = _dci.cmdexec(stmt)	
#
#	_testmgr.testcase_end(desc)
#	
#def test017(desc="""CTAS017"""):
#	global _testmgr
#	global _testlist
#	global _dci
#	if not _testmgr.testcase_begin(_testlist): return
#
#	# ----------------------------------------------------------
#	# datatypes - with column attributes and datatype info-date/char/varchar
#	# test puts on and off cqd's to show results of statement on particular applicable cqd
#	# ----------------------------------------------------------
#
#	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """create table ctascha (col1 largeint generated by default as IDENTITY not null not droppable primary key,
#			col2  char(8) not null not droppable,
#			col3  varchar(50) ,
#			col4 char varying(50),
#			col5 pic x(10));"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_complete_msg(output)
#
#	stmt = """insert into ctascha (col2,col3,col4,col5) values ('AAAAAAAA','BBBBBBBBBBBBBBBCCCCCCCcccccccc','DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD','this is a');"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_inserted_msg(output,'1')
#	
#	stmt = """insert into ctascha (col2,col3,col4,col5) values ('XXXXXXXX','this field is 50 char','this field is varying to 50','field pic');"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_inserted_msg(output,'1')
#
#	stmt = """select * from ctascha order by col2;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_selected_msg(output,'2')
#
#	stmt = """create table ctas017d (char8 char(8) not null not droppable,vchar50 varchar(50)) store by (char8) as select col5,col3 from ctascha;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_any_substr(output,'[8402]')
#
#	stmt = """create table ctas017e (picx pic x(10) not null not droppable,vchar50 varchar(50)) store by (picx) as select col2,col3 from ctascha;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_inserted_msg(output,'2')
#
#	stmt = """select * from ctas017e order by picx desc;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_file(output, defs.test_dir + """/a017exp""", """a17s1""")
#
#	stmt = """create table ctas017f (col2 char(8) not null not droppable primary key,vchar50 varchar(50)) store by (col2) as select col2,col3 from ctascha;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_inserted_msg(output,'2')
#
#	stmt = """select * from ctas017f order by col2 desc;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_selected_msg(output,'2')
#	_dci.expect_file(output, defs.test_dir + """/a017exp""", """a17s2""")
#
#	stmt = """create table ctas017g (picx pic x(10) not null not droppable,vchar50 varchar(50),mchar char(50)) store by (picx) as select col2,col3,col4 from ctascha;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_inserted_msg(output,'2')
#
#	stmt = """showddl ctas017g;"""
#	output = _dci.cmdexec(stmt)	
#
#	stmt = """select * from ctas017g order by picx desc;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_file(output, defs.test_dir + """/a017exp""", """a17s3""")
#
#	_testmgr.testcase_end(desc)

def test018(desc="""CTAS018"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# create a table that combines the two tables of female_actors union male_actors
	# interested more in the column combinations at this point
	# ----------------------------------------------------------

	stmt = """create table ctas018 (pkey largeint not null not droppable, st_name varchar(30),r_realname varchar(50),
			b_birthday date constraint md18 check (b_birthday > date '1900-01-01'))    
			store by (pkey) as select * from Female_actors union select * from Male_actors
			;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'9')	

	stmt = """select * from ctas018 order by pkey;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_selected_msg(output,'9')

	stmt = """showddl table ctas018;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_complete_msg(output)
	
	_testmgr.testcase_end(desc)	

def test019(desc="""CTAS019"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# datatypes - with column attributes and datatype
	# ----------------------------------------------------------

	stmt = """create table ctas019 store by (pkey) as select pkey,st_name,mv_director from ctas018,Movie_titles where pkey=mv_femalestar;"""
	output = _dci.cmdexec(stmt)
	_dci.unexpect_any_substr(output,'ERROR')
	_dci.expect_inserted_msg(output,'7')

	stmt = """select * from ctas019 order by pkey;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_selected_msg(output,'7')

	stmt = """showddl table ctas019;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_complete_msg(output)

	_testmgr.testcase_end(desc)
	
def test020(desc="""CTAS020"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# datatypes - with column attributes join
	# ----------------------------------------------------------

	stmt = """create table ctas020 store by (mv_no) as
			select mv_no,mv_name,mv_yearmade from Movie_titles join Male_actors
			on (mv_malestar=m_no) join Female_actors on (mv_femalestar=f_no)
			where Male_actors.m_name='Cary Grant'
			and Female_actors.f_name='Grace Kelly';"""
	output = _dci.cmdexec(stmt)
	_dci.expect_inserted_msg(output,'1')

	stmt = """showddl table ctas020;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_complete_msg(output)

	stmt = """select * from ctas020;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_selected_msg(output,'1')
	_dci.expect_file(output, defs.test_dir + """/a020exp""", """a20s1""")	

	_testmgr.testcase_end(desc)	
