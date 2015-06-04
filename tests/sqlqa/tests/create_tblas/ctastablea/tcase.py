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
	## New functionality for Create table As (sql statement) Allows users
	## to create a table based on the data attributes of a Select query and
	## to populate the table using the data returned from the query. 
	## This set of tests uses the rules used to generate and specify file 
	## attributes such as partitioning info,keys,etc.
	#############################################################################

def test001(desc="""CTAST001 Create a table with hash partition"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# expect a single partitioned table
	# POS has to be off if you don't specify a primary key.
	# ----------------------------------------------------------

	stmt = """showcontrol all;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """select * from Male_actors;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_selected_msg(output,'4')

	stmt = """create table ctast001 store by (m_no) hash partition by (m_no) as select m_no,
			m_name,m_realname from Male_actors;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_any_substr(output,'1199')

	stmt = """create table ctast001 store by (m_no) as select m_no,
			m_name,m_realname from Male_actors;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_inserted_msg(output,'4')

	stmt = """get statistics;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """showddl ctast001;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """select * from ctast001;"""
	output = _dci.cmdexec(stmt)
	_dci.unexpect_any_substr(output,'ERROR')
	_dci.expect_selected_msg(output,'4')

	_testmgr.testcase_end(desc)
	
def test002(desc="""CTAST002 Create a table with user defined key"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# currently (1/24/07) unique primary index currently works with mode_teradata '==on' only
	# this supposedly might be changed.
	# ----------------------------------------------------------

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """create table F_actors(
			f_no          int not null not droppable,
			f_name        varchar(30) not null,
			f_realname    varchar(50) default null,
			f_birthday    date  constraint md1f check (f_birthday > date '1900-01-01'),
			primary key (f_no));"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """create table ctast002 unique primary index(f_no) as select * from F_actors;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'0')

	_testmgr.testcase_end(desc)
	
def test003(desc="""CTAST003 Create a table with a store by key"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """create table Ma_actors (
			m_no          int not null not droppable unique,
			m_name        varchar(30) not null,
			m_realname    varchar(50) default null,
			m_birthday    date  constraint md2m check (m_birthday > date '1900-01-01'))
			store by (m_no);"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """create table ctast003 store by (m_no) as select * from Ma_actors;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'0')

	stmt = """showddl table ctast003;"""
	output = _dci.cmdexec(stmt)

	_testmgr.testcase_end(desc)
	
#def test004(desc="""CTAST004 Create a table with a surrogate key - original table has one"""):
#	global _testmgr
#	global _testlist
#	global _dci
#	if not _testmgr.testcase_begin(_testlist): return
#
#	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """create table mytabid(col1 largeint generated by default as IDENTITY not null not droppable, col2 char(8), col3 char(50), primary key (col1) not droppable) store by primary key;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """insert into mytabid (col2, col3) values ('AAAABBBB','this is a test of 50');"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'1')
#
#	stmt = """insert into mytabid (col2,col3) values ('BBBBCCCC','this is a test of 60');"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'1')
#
#	stmt = """select * from mytabid;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output,'2')
#
#	stmt = """create table newtabid4 (col1 largeint generated by default as IDENTITY not null not droppable primary key, col2 char(8), col3 char (50)) as select * from  mytabid;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'2')
#
#	stmt = """alter table newtabid4 alter column col1 set increment by 2;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """insert into newtabid4 (col1,col2,col3) values (default,'BBBBDDDD','this is another test of surrogate key');"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_error_msg(output,'8102')
#
#	stmt = """alter table newtabid4 alter column col1 set increment by 1;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """insert into newtabid4 (col1,col2,col3) values (default,'BBBBDDDD','this is another test of surrogate key');"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'1')
#
#	#new row should have an identity generated in col1
#	#update statistics for table newtabid4 on every column;
#	stmt = """select * from newtabid4;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output,'3')
#
#	_testmgr.testcase_end(desc)
#
#def test005(desc="""CTAST005 Create a table with a surrogate key when original doesn't have one"""):
#	global _testmgr
#	global _testlist
#	global _dci
#	if not _testmgr.testcase_begin(_testlist): return
#
#	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """create table mytabid2 (col1 largeint not null not droppable primary key, col2 char(8), col3 char(50)) store by primary key;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """insert into mytabid2 (col1,col2, col3) values (1,'AAAABBBB','this is a test of 50');"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'1')
#
#	stmt = """insert into mytabid2 (col1,col2,col3) values (2,'BBBBCCCC','this is a test of 60');"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'1')
#
#	stmt = """select * from mytabid2;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output,'2')
#
#	stmt = """create table newtabid5 (col1 largeint generated by default as IDENTITY not null not droppable primary key, col2 char(8), col3 char (50)) as select * from  mytabid2;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'2')
#
#	stmt = """select * from newtabid5;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output,'2')
#
#	stmt = """insert into newtabid5 (col2,col3) values ('BBBBDDDD','this is another test of surrogate key');"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'1')
#
#	stmt = """select * from newtabid5;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output,'3')
#
#	_testmgr.testcase_end(desc)
#	
#def test006(desc="""CTAST006 try adding a new column to table with create as select - not supported."""):
#	global _testmgr
#	global _testlist
#	global _dci
#	if not _testmgr.testcase_begin(_testlist): return
#
#	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """create table actors2 (
#			m_no          int not null not droppable ,
#			m_name        varchar(30) not null,
#			m_realname    varchar(50) default null,
#			m_birthday    date  constraint md3 check (m_birthday > date '1900-01-01'),
#			primary key (m_no));"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """create table ctast006 (sa largeint generated by default as IDENTITY not null not droppable primary key,
#			M_no int,m_name varchar(30),m_realname varchar(50)) as select m_no,m_name,m_realname from  actors2;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_any_substr(output,"""*ERROR[4023]*""")
#
#	_testmgr.testcase_end(desc)
	
#def test007(desc="""CTAST007 Create a table with multiple columns as store by key"""):
#	global _testmgr
#	global _testlist
#	global _dci
#	if not _testmgr.testcase_begin(_testlist): return
#
#	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """control query default pos reset;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """set list_count 5;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """create table """ + defs.w_catalog + """.""" + defs.w_schema + """.ctast007 store by (l_orderkey,l_linenumber) as
#		select l_orderkey,l_partkey, l_linenumber,l_quantity,l_extendedprice,l_discount,l_tax from """ + defs.tpch2x_schema + """.lineitem where l_linenumber = 4 and l_orderkey = 842980 
#		and l_partkey = 376312 and l_suppkey = 11367;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'1')
#
#	stmt = """showddl table ctast007;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """select count(*) from ctast007 order by l_orderkey;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """set list_count 4000000;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """control query default Pos reset;"""
#	output = _dci.cmdexec(stmt)
#
#	_testmgr.testcase_end(desc)
	
def test008(desc="""CTAST008 Create a table with foreign key - doesn't work"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	# ----------------------------------------------------------
	# this test case doesn't work. create table like tablename also doesn't work because the foreign key is not created
	# as well. Thus I am expecting a syntax error
	# ----------------------------------------------------------

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	#Movie_titles and directors created by setup program
	stmt = """create table ctast008 store by (mv_no) constraint mlktemp.mlksch.fa_fk18 foreign key(mv_director,mv_movietype)
			references directors(d_no,"d_specialty") as select * from Movie_titles;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_any_substr(output,'ERROR[15001]')	

	_testmgr.testcase_end(desc)

#def test009(desc="""CTAST009 Create a table with range partition"""):
#	global _testmgr
#	global _testlist
#	global _dci
#	if not _testmgr.testcase_begin(_testlist): return
#
#	# ----------------------------------------------------------
#	# did so with lineitem, however, need to insert into lineitem.
#	# ----------------------------------------------------------
#   
#	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """set list_count 5;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """create table """ + defs.w_catalog + """.""" + defs.w_schema + """.ctast009 store by (l_orderkey,l_linenumber) range partition (
#			add first key ( 3000001) location """ + gvars.g_disc2 + """,
#			add first key ( 6000001) location """ + gvars.g_disc3 + """,
#			add first key ( 9000001) location """ + gvars.g_disc4 + """)
#			attribute extent (1024, 1024)  maxextents 512
#			as select l_orderkey,l_partkey,
#			l_linenumber,l_quantity,l_extendedprice,l_discount,l_tax from """ + defs.tpch2x_schema + """.lineitem;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'11997996')
#
#	stmt = """showddl table ctast009;"""
#	output = _dci.cmdexec(stmt)
#	
#	stmt = """select * from ctast009;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output,'5')
#
#	_testmgr.testcase_end(desc)

def test010(desc="""CTAST010 Create a table with original table being a view"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """set list_count 5;"""
        output = _dci.cmdexec(stmt)
	
	stmt = """CREATE TABLE V2d1a ( 
            i3N LARGEINT NOT NULL not droppable primary key 
          , Q2V0 DOUBLE PRECISION NO DEFAULT NOT NULL 
          , i2 DOUBLE PRECISION NOT NULL 
          , i1N NUMERIC (18, 16) NOT NULL 
          );"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """CREATE VIEW V1d1  AS 
			SELECT V2d1a.Q2V0,  i1N,  i2,  V2d1a.i3N FROM V2d1a
			;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """INSERT INTO V2d1a VALUES (  864211, 4.146968999E12, -7.084418209285129E12, 7.054830343030204);"""
	output = _dci.cmdexec(stmt)

	stmt = """INSERT INTO V2d1a ( i2, Q2V0, i3N, i1N ) VALUES ( 
      -7.084417643170539E12, 4.146970664E12,  864214, 4.205888759360089);"""
	output = _dci.cmdexec(stmt)

	stmt = """INSERT INTO V2d1a ( i2, Q2V0, i1N, i3N )  VALUES ( 
      -7.084416963833031E12, 4.146972328E12, 0.4176203480982519,  864213);"""
	output = _dci.cmdexec(stmt)

	stmt = """INSERT INTO V2d1a VALUES (  864216, 4.146973993E12, -7.084416171272606E12, 5.734658853957269);"""
	output = _dci.cmdexec(stmt)

	stmt = """INSERT INTO V2d1a ( Q2V0, i3N, i1N, i2 )  VALUES ( 
      4.146975658E12,  864215, 4.703908181114327, -7.084415265489263E12);"""
	output = _dci.cmdexec(stmt)
	
	stmt = """INSERT INTO V2d1a ( i2, i1N, Q2V0, i3N )  VALUES ( 
      -7.084414246483001E2, 3.399289928122861, 4.146977322E12,  864218);"""
	output = _dci.cmdexec(stmt)

	stmt = """select * from v2d1a order by i3N desc;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """select * from v1d1 order by i3N asc;"""
	output = _dci.cmdexec(stmt)

	stmt = """create table ctast010 store by (i3N) salt using 4 partitions 
			as select * from v1d1;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'6')

	output = _testmgr.shell_call("""sleep 15""")
	stmt = """showddl ctast010;"""
	output = _dci.cmdexec(stmt)	

	stmt = """select * from ctast010 order by i3N;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_selected_msg(output,'5')

	_testmgr.testcase_end(desc)
	
def test011(desc="""CTAST011 Create a table with one that has multiple indexes on it."""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

        # ----------------------------------------------------------
        # indexes are not created
        # ----------------------------------------------------------
	
	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """CREATE TABLE d3 ( 
            i1 FLOAT (22) NOT NULL 
          , i2 DECIMAL (7,0) NO DEFAULT NOT NULL 
          , i3 FLOAT (54) NOT NULL 
          ) no partition;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
	
	stmt = """CREATE INDEX d3IND0 ON d3 (i3 DESC);"""
	output = _dci.cmdexec(stmt)
	
	stmt = """CREATE INDEX d3IND1 ON d3 (i1);"""
	output = _dci.cmdexec(stmt)

	stmt = """CREATE INDEX d3IND3 ON d3 (i2, i3 ASCENDING);"""
	output = _dci.cmdexec(stmt)
	
	stmt = """CREATE INDEX d3IND4 ON d3 (i1);"""
	output = _dci.cmdexec(stmt)

	stmt = """INSERT INTO d3 VALUES ( 1.811298E12,   -2125, -5.376315255537452E12);"""
	output = _dci.cmdexec(stmt)
	

	stmt = """INSERT INTO d3 ( i1, i2, i3 )  VALUES ( 
      1.811302E12,   -2115, -5.376314393586318E12);"""
	output = _dci.cmdexec(stmt)
	
	stmt = """INSERT INTO d3 ( i1, i2, i3 )  VALUES ( 
      1.811305E12,   -2105, -5.376313531635185E12);"""
	output = _dci.cmdexec(stmt)
	
	stmt = """INSERT INTO d3 VALUES ( 1.81131E12,   -2095, -5.376312669684051E12);"""
	output = _dci.cmdexec(stmt)

	stmt = """INSERT INTO d3 VALUES ( 1.811315E12,   -2085, -5.376311807732916E12);"""
	output = _dci.cmdexec(stmt)

	stmt = """update statistics for table d3 on every column;"""
	output = _dci.cmdexec(stmt)

	stmt = """create table ctast011 store by (i2) as select * from d3;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'5')

	stmt = """showddl ctast011;"""
	output = _dci.cmdexec(stmt)

	_testmgr.testcase_end(desc)
	
#def test012(desc="""CTAST012 Create a table from materialized view"""):
#	global _testmgr
#	global _testlist
#	global _dci
#	if not _testmgr.testcase_begin(_testlist): return
#	
#	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """create table mytableVw (col1 largeint generated by default as IDENTITY not null not droppable primary key,
#			col2 decimal (5,2) not null,
#			col3 int ,
#			col4 char(10));
#			insert into mytableVW (col2,col3,col4) values(34.56,1,'row 1'),
#			(48.34,2,'row 2'),
#			(54.12,3,'row 3');"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#	stmt = """insert into mytableVW (col2,col3,col4) values(34.56,1,'row 1'),
#			(48.34,2,'row 2'),(54.12,3,'row 3');"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """select * from mytableVW;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """create MV tabitha_2
#			refresh on request
#			initialize on refresh 
#			as
#			select col1, sum(col2) sumdec, count(col3) cntint
#			from 
#			mytableVW
#			group by col1;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """refresh tabitha_2;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """select * from tabitha_2;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_selected_msg(output,'3')
#	
#	stmt = """create table ctast012 store by (col1) as select * from tabitha_2;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'3')
#	
#	stmt = """select * from ctast012;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_selected_msg(output,'3')
#
#	_testmgr.testcase_end(desc)

def test013(desc="""CTAST013 Create a table with join"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
	output = _dci.cmdexec(stmt)

	stmt = """set list_count 5;"""
        output = _dci.cmdexec(stmt)

	stmt = """select mv_no,mv_name,mv_yearmade from Movie_titles join Male_actors
			on (mv_malestar=m_no) join Female_actors on (mv_femalestar=f_no);"""
	output = _dci.cmdexec(stmt)

	stmt = """create table ctast013 store by (mv_no) as
			select mv_no,mv_name,mv_yearmade from Movie_titles join Male_actors
			on (mv_malestar=m_no) join Female_actors on (mv_femalestar=f_no);"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'6')

	stmt = """select * from ctast013 order by mv_yearmade;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_selected_msg(output,'5')
 
	_testmgr.testcase_end(desc)	
	
#def test014(desc="""Create a table  lineitem with range partitions"""):
#        global _testmgr
#        global _testlist
#        global _dci
#        if not _testmgr.testcase_begin(_testlist): return
#	
#	stmt = """set list_count 5;"""
#	output = _dci.cmdexec(stmt)
#
#	stmt = """create table ctast014 location """ + gvars.g_disc1 + """ store by (l_orderkey,l_linenumber)
#			range partition (
#			   add first key ( 3000001) location """ + gvars.g_disc2 + """,
#			   add first key ( 6000001) location """ + gvars.g_disc3 + """,
#			   add first key ( 9000001) location """ + gvars.g_disc4 + """)
#			attribute extent (1024, 1024), maxextents 512 as select l_orderkey,l_partkey,
#			l_linenumber,l_quantity,l_extendedprice,l_discount,l_tax from """ + defs.tpch2x_schema + """.lineitem;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_inserted_msg(output,'11997996')
#
#	stmt = """select * from ctast014 order by l_linenumber;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output,'5')
#
#	_testmgr.testcase_end(desc)
#
#def test015(desc="""CTAST015 Create a table with hash partition"""):
#	global _testmgr
#	global _testlist
#	global _dci
#	if not _testmgr.testcase_begin(_testlist): return
#
#	stmt = """set list_count 5;"""
#	output = _dci.cmdexec(stmt)	
#
#	stmt = """create table ctast015 location """ + gvars.g_disc1 + """ store by (l_orderkey desc) hash partition as 
#			select l_orderkey,l_partkey, l_linenumber,l_quantity,
#			l_extendedprice,l_discount,l_tax from """ + defs.tpch2x_schema + """.lineitem
#			where l_linenumber = 4 and l_orderkey = 842980
#			and l_partkey = 376312 and l_suppkey = 11367;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'11997996')
#
#	stmt = """select * from ctast015 order by l_orderkey;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_selected_msg(output,'5')
#
#	_testmgr.testcase_end(desc)
#	
#def test016(desc="""CTAST016 Create a table from a large table"""):
#	global _testmgr
#	global _testlist
#	global _dci
#	if not _testmgr.testcase_begin(_testlist): return
#
#	#reset line_count.
#	stmt = """set list_count 4000000;"""
#	output = _dci.cmdexec(stmt)	
#
#	stmt = """create table ctast016 store by (l_orderkey) as select l_orderkey,l_partkey,
#			l_linenumber,l_quantity,l_extendedprice,l_discount,l_tax from """ + defs.tpch2x_schema + """.lineitem;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_inserted_msg(output,'11997996')
#
#	stmt = """select count(*) from ctast016;"""
#	output = _dci.cmdexec(stmt)	
#	_dci.expect_selected_msg(output,'1')
#
#	_testmgr.testcase_end(desc)
	
def test017(desc="""CTAST017 Create a table using select [all]"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	stmt = """CREATE TABLE d17n (
            i1 SMALLINT NO HEADING  not null not droppable
          , i2 DOUBLE PRECISION 
          , i3 DEC     (9, 7) DEFAULT 15 HEADING 'i3' CONSTRAINT i3001362MRwxpd4 NOT NULL NOT DROPPABLE 
          ) 

          STORE BY (i1)
          ;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)
   
	stmt = """INSERT INTO d17n (i1, i2, i3)  VALUES ( 
           11, -9506588.156259237,   5.377708);"""
	output = _dci.cmdexec(stmt)
	
	stmt = """INSERT INTO d17n VALUES (      42, -9390654.154353635, 11.3170288);"""
	output = _dci.cmdexec(stmt)
 
	stmt = """INSERT INTO d17n VALUES (      48, -9158786.150542434,  -0.202204);"""
	output = _dci.cmdexec(stmt)

	stmt = """update statistics for table d17n on every column;"""
	output = _dci.cmdexec(stmt)

	stmt = """create table ctast017 store by (i1) as select ALL i1,i2,i3 from d17n;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'3')

	output = _testmgr.shell_call("""sleep 15""")
	stmt = """showddl ctast017;"""
	output = _dci.cmdexec(stmt)	

	stmt = """select * from ctast017 order by i3;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_selected_msg(output,'3')

	_testmgr.testcase_end(desc)
	
def test018(desc="""CTAST018 Create table b like table a as select * from a"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

        # ----------------------------------------------------------
        # indexes, references etc are not created with either the create table like
        # ----------------------------------------------------------

	
	stmt = """CREATE TABLE d4 (
            i1 SMALLINT NO HEADING  
          , i2 DOUBLE PRECISION 
          , i3 DEC     (9, 7) DEFAULT 15 HEADING 'i3' CONSTRAINT i3001362MRwxpd4 NOT NULL NOT DROPPABLE 
          ) 
          STORE BY (i3)
          ;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """INSERT INTO d4 (i1, i2, i3)  VALUES ( 
           11, -9506588.156259237,   5.377708);"""
	output = _dci.cmdexec(stmt)
	
	stmt = """INSERT INTO d4 VALUES (      42, -9390654.154353635, 11.3170288);"""
	output = _dci.cmdexec(stmt)
 
	stmt = """INSERT INTO d4 VALUES (    null, -9158786.150542434,  -0.202204);"""
	output = _dci.cmdexec(stmt)

	stmt = """CREATE INDEX d4IND0 ON d4 (i3 ASCENDING) POPULATE;"""
	output = _dci.cmdexec(stmt)

	stmt = """select * from d4;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """showddl d4;"""
	output = _dci.cmdexec(stmt)

	stmt = """create table ctast018 like d4 as select * from d4;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'3')	

	output = _testmgr.shell_call("""sleep 15""")
	stmt = """showddl ctast018;"""
	output = _dci.cmdexec(stmt)	

	stmt = """select * from d4 order by i1,i2,i3;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_selected_msg(output,'3')

	_testmgr.testcase_end(desc)
	
def test019(desc="""CTAST019 Create a table as from several tables with a bit more complicated select"""):
	global _testmgr
	global _testlist
	global _dci
	if not _testmgr.testcase_begin(_testlist): return

	stmt = """set list_count 4000000;"""
        output = _dci.cmdexec(stmt)
	
	stmt = """drop table v2d1;"""
	output = _dci.cmdexec(stmt)	
	
	stmt = """drop table d3;"""
	output = _dci.cmdexec(stmt)	
	
	stmt = """drop table d2;"""
	output = _dci.cmdexec(stmt)	

	stmt = """drop view v1d1;"""
	output = _dci.cmdexec(stmt)	

	stmt = """CREATE TABLE V2d1 ( 
            i1 VARCHAR (9) NOT NULL primary key
          , i2 CHAR (7) NOT NULL 
          , i3 CHAR (22) 
          , Q2V0 CHAR (856) NOT NULL 
          , Q2V1 VARCHAR (19) NOT NULL 
          , Q2V2 DOUBLE PRECISION NOT NULL 
          , S2V0 CHAR (576) NO DEFAULT 
          , S2V1 FLOAT (22) NOT NULL 
          , S2V2 CHAR (90) NOT NULL 
          , S2V3 VARCHAR (5) NOT NULL 
          , S2V4 VARCHAR (626) NOT NULL 
          );"""
	output = _dci.cmdexec(stmt)
	_dci.expect_complete_msg(output)

	stmt = """CREATE TABLE d2 ( 
            i1 CHAR (17) 
          , i2 CHAR (8) 
          , i3 CHAR (9) 
          , G0 NUMERIC (4,0) NOT NULL 
          , primary key (G0)
          );"""
	output = _dci.cmdexec(stmt)	
	
	stmt = """CREATE TABLE d3 ( 
            G4 REAL 
          , G3 DECIMAL (4,0) NOT NULL 
          , G0 DOUBLE PRECISION NOT NULL 
          , G2 DOUBLE PRECISION NOT NULL 
          , G5 DECIMAL (9,0) NOT NULL 
          , i1 CHAR (19) 
          , G1 DEC     (18, 7) NO DEFAULT 
          , i3 CHAR (15) NO DEFAULT NOT NULL 
          , i2 VARCHAR (7) 
          , primary key (G5,G3)
          );"""
	output = _dci.cmdexec(stmt)	

	stmt = """CREATE VIEW V1d1  AS 
			SELECT  V2d1.Q2V2,  V2d1.Q2V1,  Q2V0,  i2,  V2d1.i3,  V2d1.i1 FROM V2d1;"""
	output = _dci.cmdexec(stmt)	

	stmt = """CREATE VIEW d1  AS 
			SELECT  V1d1.i1,  i3,  V1d1.i2 FROM V1d1;"""
	output = _dci.cmdexec(stmt)

	stmt = """CREATE INDEX d2IND1 ON d2 (i3);"""
	output = _dci.cmdexec(stmt)
	
	stmt = """CREATE INDEX d2IND0 ON d2 (i3);"""
	output = _dci.cmdexec(stmt)

 	stmt = """INSERT INTO d3 ( i2, i3, G3, i1, G2, G4, G5, G0, G1 )  VALUES ( 
			'M98Y7', 'ZSTD1QNE''''''''''''''',     530, 'KKKKKKKKKKKB3C3W366', 7.440252639185534E12, -2.542272E10, 
            8, 9.885438897E12, 7698895.127545047);"""
	output = _dci.cmdexec(stmt)    

 	stmt = """INSERT INTO V2d1 ( i2, i3, Q2V0, Q2V1, Q2V2, S2V0, S2V1, S2V2, S2V3, S2V4, i1 )  VALUES ( 
      'J46O8VB', '              HD6K7X32', 
      '                  -638551.222614012 -368931.7298497554 -944461.7161694473 465642.5931425444 -260 429 422 -257 58 370419.80129721924 -13 -118578.93686721206 303 -808471.4602774938 402430.69861205784 -434280.6362823837  254259.4179746986 194127.5525793871 793403.5524897485 -339096.4391121203 -128363.28922810638 -112 -17 -77 34 -387 -143 -362 -469 327 277 -268 389 828645.1319112992 -220409.29491536797 343922.71777530643 221449.466491136 794204.0796175797 -832141.5191507033 210 -325 -366058.0937106048 636592.3521131813 261554.38655818067 -27 -105418.70883746957 448 929411.7611442893 476554.6227092324 -764892.995771075 -231662.8448151676 -531253.5775830238 -215 285 -564874.0108395829 -96936.20603442588 -442 574628.9254308853 236 -498299.73193739407 -274375.67518722545 -935479.5592794162 -299 670367.3155788612 -55 -606751.307228387 952532.8660631967 ', 
               '4ITSJ5BH', 1.6769646763095176E13, 
      'NNNNNNNNNNNNNNNNNNNNNNNNNC6DFW13X All lions walked beneath Henry! I6DFW13X D6DFW13X H6DFW13X 76DFW13X 36DFW13X J6DFW13X 66DFW13X L6DFW13X -216 5085.137525524362 686223.356434949 -142 -375 461 Many sheep got out beneath Joseph. Y6DFW13X M6DFW13X V6DFW13X 46DFW13X 26DFW13X 126 -857289.2234817806 F6DFW13X Callie and Joseph crawled rapidly near some house.  -220158.23302417784 56DFW chickens those scampered near P6DFW13X Michael 86DFW13X S6DFW skedaddled nervously close to Michelle and Chet ambled loudly beneath the string! Ed and Michelle sprang quickly through all house. ', 
      9.082419E11, 
      'aaaa  68 654106.7610370179 2E0LJ68W NE0LJ68W UE0LJ68W sprinted 5E0LJ68W 0E0LJ68W  SE0LJ68W', 
      'R87Q3', 
      '-495 958808.6672876857 -4 892854.4385558595 -214 697678.4958457709 -497 -499 -702213.8103519478 727321.1129645817 -34 999798.0398531773 -461392.3901706041 -394 299546.35553724016 123 150927.3699062469 95 -647936.6243112463 -693843.7900217506 231974.76395513187 -409 -453 -978510.3502608261 -341839.07226948615 351 -399349.9223635708 -626582.8270955225 -248 -150 -196 572726.3845601629 -416 -468 958689.6283879634 -275 -476025.55299019936 832336.9979527032 470462.5055925045 314 318 -65 -19 378 606068.788766915 368 -301850.33327037597 -983491.6278701694 288730.02611108474 -87 -595325.2214972373 ', 
      '5E0CSH3W');"""
	output = _dci.cmdexec(stmt) 

 	stmt = """INSERT INTO d3 VALUES ( -2.542065E10,     539, 9.885440177E12, 7.440254244100341E12,       9, 
      'X3C3W366           ', 7699051.055338961, '383''''''''''''''''''''''''', 'G98Y7');"""
	output = _dci.cmdexec(stmt) 

 	stmt = """INSERT INTO V2d1 ( S2V3, S2V2, Q2V1, Q2V2, S2V1, i1, i2, S2V4, S2V0, Q2V0, i3 )  VALUES ( 
      'B87Q3', 
      '88crawled ZE0LJ TE0LJ -735648.4712553399 XE0LJ68W -89237.87957471912 BE0LJ JE0LJ  WE0LJ68W', 
               'JITSJ5BH', 1.6769647104943445E13, 9.082442E11, 'CE0CSH3W', '546O8VB', 
      '-195 -18 -15676.630809097667 -375678.849919703 -139  -655191.0810534816 71 -903037.6715741288 -822018.9753801721 -865053.9586165191 -760956.4139915206 333 -244 127 191324.31225504354 -289 -72 523836.69263408286 322133.7548704727 -960112.7342938058 -563894.8418911725 -729714.1952946838 320 -681488.9100655292 -348052.893921923 -359 -38 687251.4814086109 314808.2568723168 -108948.29464457673 473 30 -313843.3135321153 -291 -173127.81950460537 184 914482.8024484043 320 117888.44981021201 21289.112205752637 320423.75381608214 -854092.5734112255 -192 ', 
      '                                       thoughtfully Crows and goats and sheep. Oh My! A sibling and Emma rushed loudly beside one of the beach.  All dolphins hightailed under Claire. 87 528995.570676029 169 211112.35605219728 238032.2714166278 -178 -481 -142938.3762856325 Biff slide near quite a few sharks??? walked -155 16DFW CVDFW13X IVDFW Crows and whales and horses. Oh My! DVDFW13X HVDFW13X 7VDFW13X 3VDFW13X JVDFW13X 6VDFW13X LVDFW13X 321604.3315489914 YVDFW13X MVDFW13X VVDFW13X Callie sprinted sloppily! Issac hopped gracefully! 4VDFW 2VDFW FVDFW13X 5VDFW  PVDFW13X ', 
      '396 -40790.893858793774 46 -431 468859.6213845371 -148 297 -83 305789.93405365176 631992.4308669118 66871.85419325228 108 -943691.3869927692 -786547.2341081979 -676631.1610610818 211 692836.8786096543 -757237.5862828121 -117364.81875423773 -432492.4003677495 60671.880780479405 -130 3 258 170 96 410 71 270 344 50 -37 134.18247980508022 -168 430010.2260615672 -131 -476 653513.0720774401 -115248.71741531673 290 -65 -76385.62399616803 -631205.5447607419 -36 -452 24 -828896.7570736823 183046.48274186603 440 827096.8464733935 -106 383461.55035100225 137055.56527096475 -675874.4505947101 -804426.4377012271 262 -494 -65 -137 588494.435164823 -239817.83935273974 58635.81111991219 -122 249389.81766557088 435 -281 546885.3667019107 19376.50725163007 495854.68532695575 117 -62 452664.26866562245 72489.65659995424 -153 411 55                                ', 
      '              VD6K7X32');"""
	output = _dci.cmdexec(stmt) 

 	stmt = """INSERT INTO d2 VALUES ( '              399', 'A32Y    ', 'QC5PL139Z',     574);"""
	output = _dci.cmdexec(stmt) 

 	stmt = """INSERT INTO V2d1 ( Q2V1, S2V2, Q2V0, S2V4, i2, i3, S2V0, i1, S2V3, S2V1, Q2V2 )  VALUES ( 
               'OITSJ5BH', 
      'sauntered all beach -698440.1575702077 Genelle 825515.8799644464 wood 1E0LJ68W  EE0LJ68Www', 
      '249348.68213667162 461777.73613329 -356314.9771675718 -900030.0591897776 283 346986.3587821892 143 63 -541274.9375393521 -634867.2442870766 674684.9887484415  30901.467225046945 -26983.19818533142 -302 -854152.6583871619 70  -446  -48 594393.1392283803 287 686488.2538760405 294920.9785987579 182 -112 387589.0024296825  -211749.89075142215 625803.409411991 897970.9889271164 -480 311 360 725361.2985124716 355 3 -121 368 266944.30323095573 51 -565084.6554482377 757430.5860891736 -52 -309692.20888016187 -381 -720552.2118465328 -588058.8511529462 464 283892.91371076554 212 135 -426 489 -49 434 71608.65168158896 -283 -158 -339 -497693.4134008981 133740.1936617617 -444 -603970.4817399404 148 327 -57641.745869672275 -402 543411.2104884388 -438007.97861932404 388 -264 -466181.53198371816 -412 -348544.0809066815 -18 130143.0502073858 -1 .................', 
      '-250235.35203934368 659849.8541986835 135 394 -175 394493.6376146765 -492 -370 -500454.4764228116 -439 -372873.6805606785 -168 138175.11091988883 -584563.3985187823 662619.7994856243 270724.6995261442 913657.6120943737 -834575.7454841353 269886.87624778855 -114  -71 -355012.80082039325 -543037.2284337061 462 -339840.91240291554 491 -544627.0003573574  948128.4235732686 390075.92526240577 -285 486 131 -54 -485 473554.4842238843 -298 52480.57318860316 51 415 917624.0968198099 53 92 102 -184 -920077.8249452355 230 ', 
      'D46O8VB', '8D6K7X32              ', 
                                                       null, 
      'XE0CSH3W', 'V87Q3', 9.082465E11, 1.676964744679172E13);"""
	output = _dci.cmdexec(stmt) 

 	stmt = """INSERT INTO V2d1 ( i3, Q2V0, S2V0, S2V4, i2, i1, S2V1, Q2V2, Q2V1, S2V2, S2V3 )  VALUES ( 
      'HHHHHHHHHHHHHH7D6K7X32', 
      ' 849237.611080722 -173186.40586023813 -400 526530.5338332187 -221 324926.69179618056 -115  -220 98 402 -391809.0335389563 -430 -405 370 716181.3828998834 -426 578243.3854994525 -944838.4247755435 701148.3664662128 -969858.6110578191 126851.15830841195 512439.5430125948 630037.3135219277 51 -262503.97213008057 245652.14040925726 436 -253686.9950325807 464301.3592824703 161 -68 184498.8352564997 359 -117098.17327246035 491 876228.9999098061 -230132.7796690917 -190 -189 -409056.4800275329 316401.88146077795 -423 342 -232 111 841695.7162824271 -262077.42599685967 17 -358447.8057125064 16996.28294203605 266 -212 -927215.2705315367 -235985.96640692593 625655.5413063255 2 493800.28230704437 -430 -112883.93951657589 157  331 218 -812957.7949909132 -596836.808774542 64 315 232 -861572.5572121007 -395279.3218586402 445 22  DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD', 
      'X6DFW13X a few 06DFW R6DFW desk A6DFW O6DFW13X all Michelle wormed luckily. Callie jumped cautiously. -144 Z6DFW13X Q6DFW13X T6DFW13X U6DFW13X G6DFW13X N6DFW13X E6DFW13X Genelle split through the sheep??? -674852.3478056863 -272815.51533256646 236 -408 -393 934039.0559418641 Worms and elk and cows. Oh My! Michael and Emma rolled rapidly beside several crane. chickens several B6DFW13X 96DFW K6DFW13X -238690.3930809208 W6DFW13X -431 -180 Some eels scampered over Michael??? Iola and Michelle wormed nervously towards quite a few desk!                                        ', 
      '-344 945330.0125724876 468 -387 -423 69 43880.97614354151 853264.2698873258 17914.635294742184 -13925.385385193047 -550944.041683078 886387.3304918767 363 74849.13478626823 -979069.6374277375 -771182.8228398851 -19 -229 343 692058.7853387278 2153.025877948967 442 676220.256575723 -760736.4780040517 926768.9601038359 27 -197444.531585705 -684856.3823327558 -468 -356 -382866.67436268425 -22193.12014669762 274 124341.30657063308 -48262.38148569793 -93 -56 308 115236.02253945055 -476 -96 -761396.7521102662 609184.5066879175 -353 35 903571.5984987577 -127200.41026296641 194 116 814802.3704337105 135 ', 
      'B46O8VB', '7E0CSH3W', 9.08243E11, 1.676964693401931E13,          'TITSJ5BH', 
      '8E0LJ68W -103763.76759413409 -315816.16648012353 flew FE0LJ  4E0LJ68W                     ', 
      'D87Q3');"""
	output = _dci.cmdexec(stmt) 

 	stmt = """INSERT INTO d2 ( i1, i2, i3, G0 )  VALUES ( 
      'ABZ5EAGQ         ', 'luckily\', 'A5PL139ZM',     579);"""
	output = _dci.cmdexec(stmt) 

 	stmt = """INSERT INTO d2 ( i3, i2, G0, i1 )  VALUES ( 
      ' 75PL139Z', 'EEEEEthe',     600, 'OBZ5EAGQaaaaaaaaa');"""
	output = _dci.cmdexec(stmt)

 	stmt = """INSERT INTO d3 VALUES ( -2.542253E10,     521, 9.885437617E12, 7.440251435499429E12,       7, 
      'QQQQQQQQQQQH3C3W366',            null, '       6STD1QNE', 'C98Y7');"""
	output = _dci.cmdexec(stmt)

 	stmt = """INSERT INTO d2 VALUES ( '-324?????????????', 'lots ofb', ' 15PL139Z',     592);"""
	output = _dci.cmdexec(stmt)

 	stmt = """INSERT INTO d3 VALUES ( -2.542084E10,     548, 9.885441458E12, 7.44025625024385E12,      10,
	'\"\"\"\"\"\"\"\"\"\"\"13C3W366', 7698959.305064012, '              O', 'W98Y7');"""
	output = _dci.cmdexec(stmt)

 	stmt = """INSERT INTO V2d1 ( i1, i3, Q2V1, S2V4, S2V2, S2V3, S2V1, S2V0, Q2V2, i2, Q2V0 )  VALUES ( 
      'WE0CSH3W', 'CD6K7X32BBBBBBBBBBBBBB',          'LITSJ5BH', 
      '979996.5528221123 -876780.2567804137 -480067.28888164664 -441 880113.5406475386 482 -472 -473026.40751394944 -180979.9387850652 465 -393 -672933.3474799895 163 948132.8573706499 -332 -313 402  -34 -799457.0693400962 420 599401.5155608538 765113.3280326177 -779169.1605329883 947940.4854882506 -21 481 742668.0470277108 329 521726.696769292 -291 -480 301 -283 311 44 152 157 270 -601375.0173351391 794180.1541641171 -86  290 58 -551482.1549311726 -458760.95434657205 5446.591107784538 514984.68902980397 170707.92667635018 570635.1147535786 200008.49057288398 ', 
      'rolled my mother 6E0LJ68W IE0LJ YE0LJ VE0LJ68W OE0LJ68W around  LE0LJ68W                  ', 
      '487Q3', 9.082454E11, 
      '569339.5721459438 905152.9541728531 -9 278 158 315770.2345878093 -417 Janine and Biff skipped kindly under one of the store. An Indian dashed over all worms. Madelyn hopped angrily. Ed ambled sloppily! 8VDFW13X SVDFW13X XVDFW13X 0VDFW13X Wolves and dogs and fish. Oh My! RVDFW13X AVDFW13X OVDFW13X ZVDFW13X QVDFW13X -776507.8633794384 -643085.2024414744 287 -752500.8002258331 -475 78582.89969981345 lots of -293 through leisurely tree 504672.5664017305 TVDFW13X 405 UVDFW13X Claire hotfooted leisurely. an Englishman sauntered thoughtfully. A few rats got out towards Vince. ', 
      1.6769647275867582E13, 'X46O8VB', 
      '-231 -132 443 -812686.5213191428 265 86 -134 -997417.0468897929  -187866.9506219133 933279.3088283676 810974.4928782978 -16 85 -99 -85 225 58386.91380629502 -61 130058.31545664603 828273.3313996892 196 -284108.39637346566 241796.65468843258 965074.4337680063 347 182243.96735175606 -369 738359.8928704925 -632793.7914514965 -423 -573520.79383447 667017.7194019132 960099.2787366253 -148773.00608315866  -602810.8919886227 196074.60089841182 -263 -376 574160.1999502112 -740034.940965711 362 164 483762.3140818062 -3032.5832082232228 -840594.8810912592 -451578.9321024255 -121 -764941.8851157483 341 673909.7052822735 475 604096.6292281898 -453276.68778119085 941442.151673283 -91 430 -113287.93414205743 187 -160 781127.3448286192 296 529704.7422575795 78 324 -848567.4642625505 -469940.302114666 -364279.55521113065                                        ');"""
	output = _dci.cmdexec(stmt)

 	stmt = """INSERT INTO d2 VALUES ( '766559.7669208099', 'sprinted', 'p35PL139Z',     609);"""
	output = _dci.cmdexec(stmt)

 	stmt = """INSERT INTO d3 VALUES ( -2.54246E10,     512, 9.885436336E12, 7.440250633042025E12,       6, 
      ']]]]]]]]]]]93C3W366', 7698848.048478021, '378""""""""""""',    null);"""
	output = _dci.cmdexec(stmt)

 	stmt = """INSERT INTO d2 ( i3, i2, i1, G0 )  VALUES ( 
      'P5PL139Zf',     null, '120WWWWWWWWWWWWWW',     585);"""
	output = _dci.cmdexec(stmt)

 	stmt = """select i1, i2, i3 from d1;"""
	output = _dci.cmdexec(stmt)

 	stmt = """select i1, i2, i3 from d2;"""
	output = _dci.cmdexec(stmt)
	
 	stmt = """select i1, i2, i3 from d3;"""
	output = _dci.cmdexec(stmt)

 	stmt = """select T2.i3 FROM D2 T0, D1 T1, D2 T2 WHERE T2.i1 <> T0.i3;"""
	output = _dci.cmdexec(stmt)

	stmt = """create table tabitha (i3 char(17) not null not droppable) store by (i3) as select T2.i3
			FROM D2 T0, D1 T1, D2 T2
			WHERE
			T2.i1 <> T0.i3;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_inserted_msg(output,'180')

	output = _testmgr.shell_call("""sleep 60""")
	stmt = """showddl tabitha;"""
	output = _dci.cmdexec(stmt)		

	stmt = """select * from tabitha;"""
	output = _dci.cmdexec(stmt)	
	_dci.expect_selected_msg(output,'180')

	stmt = """select count(*) from tabitha for read uncommitted access;"""
	output = _dci.cmdexec(stmt)
	_dci.expect_any_substr(output,' 180')
	
	_testmgr.testcase_end(desc)

#def test020(desc="""Create a table with  volatile table"""):
#        global _testmgr
#        global _testlist
#        global _dci
#        if not _testmgr.testcase_begin(_testlist): return
#
#        stmt = """Create volatile table voltabl1 (
#                              i1 largeINT NO HEADING
#          		    , i2 DOUBLE PRECISION
#          		    , i3 DEC     (9, 7) DEFAULT 15 NOT NULL NOT DROPPABLE           )
#
#        		    STORE BY (i3);"""
#        output = _dci.cmdexec(stmt)
#	_dci.expect_complete_msg(output)
#
#        stmt = """INSERT INTO voltabl1 (i1, i2, i3)  VALUES (
#	           11, -9506588.156259237,   5.377708) ;"""
#        output = _dci.cmdexec(stmt)
#        _dci.expect_inserted_msg(output,'1')
#
#	stmt = """INSERT INTO voltabl1 VALUES (      42, -9390654.154353635, 11.3170288) ;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_inserted_msg(output,'1')
#
#	stmt = """INSERT INTO voltabl1 VALUES (    12, -9158786.150542434,  -0.202204) ;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_inserted_msg(output,'1')
#
#        stmt = """select * from voltabl1;"""
#        output = _dci.cmdexec(stmt)
#        _dci.expect_selected_msg(output,'3')
#
#	stmt = """create table ctast020 (i1 largeint generated by default as IDENTITY not null not droppable primary key,i2 double precision ,i3 dec (9,7)) store by (i1) as select * from voltabl1;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_inserted_msg(output,'3')
#
#	stmt = """INSERT INTO ctast020  (i2,i3) VALUES ( -8390654.153353635, 12.3171288) ;"""	
#	output = _dci.cmdexec(stmt)
#	_dci.expect_inserted_msg(output,'1')
#
#	stmt = """select * from ctast020 order by i1;"""
#	output = _dci.cmdexec(stmt)
#	_dci.expect_selected_msg(output,'4')
#
#        _testmgr.testcase_end(desc)

