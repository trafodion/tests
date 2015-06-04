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

#-------------------------
# testunit ddl04
# data in /g_data/sqldopt
#-------------------------
def save_ddl_to_obeyfile(objname, filename, schema=''):

    tmpfile = defs.work_dir + """/pass1_tmpfile"""

    output = _testmgr.shell_call("""rm """ + tmpfile)
    output = _testmgr.shell_call("""rm """ + filename)

    stmt = """log """ + tmpfile + """ clear, cmdtext off;"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl """ + objname + """;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)

    if schema == '':
        schema = defs.my_schema
    output = _testmgr.shell_call("""echo 'set schema """ + schema + """;' > """ + filename)
    output = _testmgr.shell_call("""cat """ + tmpfile + """ | grep -v log | grep -v 'SQL operation complete' >> """ + filename)
    # For triggers in case there is one
    output = _testmgr.shell_call("""echo '/' >> """ + filename)
    # IF the previous showddl got an error, the following ';' will make sure
    # that DCI does sit in a prompt when we feed this obey file to it.
    outout = _testmgr.shell_call("""echo ';' >> """ + filename)
    outout = _testmgr.shell_call("""echo 'exit;' >> """ + filename)

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""altered table -add constraint"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #-----------------------------------------
    
    #-----------------------------------
    # a01.1 add constraint - primary key
    #-----------------------------------
    
    stmt = """Create Table t1a011
(
sbin0_10            Numeric(18) signed    not null,
char0_2             Character(8)          not null,
udec0_uniq          Decimal(9) unsigned   not null,
ubin0_uniq          PIC 9(9) COMP         not null,
sdec0_500           PIC S9(9)             not null,
varchar0_10         varchar(16)      not null,
varchar1_20         varchar(8)       not null,
sbin1_5000          Numeric(4) signed     not null,
sdec1_4             Decimal(18) signed    not null,
char1_4             Character(8)          not null    

)
store by (udec0_uniq)
location """ + gvars.g_disc0 + """
hash partition (add location """ + gvars.g_disc1 + """, add location """ + gvars.g_disc2 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t1a011 add constraint ca011 primary key (ubin0_uniq ) droppable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t1a011;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t1a011;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t1a011""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t1a011;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t1a011;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t1a011;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #-------------------------------------
    # a01.2 add constraint - unique column
    #-------------------------------------
    
    # btpnl19
    stmt = """Create Table t1a012
(
sdec0_2             PIC S9(9)             not null,
varchar0_100        varchar(16)      not null,
char0_4             Character(8)          not null,
sbin0_uniq          Numeric(18) signed    not null,
udec0_100           Decimal(9) unsigned   not null,
ubin0_uniq          PIC 9(9) COMP         not null,
sdec1_20            Decimal(18) signed    not null,
varchar1_10         varchar(8)       not null,
sbin1_1000          Numeric(4) signed     not null,
char1_10            Character(4)          not null,
primary key ( sbin0_uniq ASC ) not droppable
)
store by primary key
location """ + gvars.g_disc0 + """
hash partition (add location """ + gvars.g_disc1 + """, add location """ + gvars.g_disc2 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t1a012 add constraint ct1a012 unique ( ubin0_uniq  ) droppable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t1a012;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t1a012;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t1a012""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t1a012;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t1a012;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t1a012;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #---------------------------------------
    #a01.3 add constraint - check constraint
    #---------------------------------------
    
    # btpnl03
    stmt = """Create Table t1a013
(
sbin0_10            Numeric(18) signed    not null,
char0_2             Character(8)          not null,
udec0_uniq          Decimal(9) unsigned   not null,
ubin0_1000          PIC 9(7)V9(2) COMP    not null,
sdec0_500           PIC S9(9)             not null,
varchar0_10         varchar(16)      not null,    

varchar1_20         varchar(8)       not null,
sbin1_5000          Numeric(4) signed     not null,
sdec1_4             Decimal(18) signed    not null,
char1_4             Character(8)          not null,    

primary key ( udec0_uniq  ASC ) not droppable
)
store by primary key location """ + gvars.g_disc6 + """
hash partition (add location """ + gvars.g_disc8 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t1a013 add constraint ct1a013 check (sdec1_4 < 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t1a013;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t1a013;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t1a013""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t1a013;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t1a013;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t1a013;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #----------------------------------
    #a01.4 add constarint - foreign key
    #----------------------------------
    
    # btpnl21
    stmt = """Create Table t1a014_1
(
ubin0_2             PIC 9(7)V9(2) COMP    not null,
sbin0_100           Numeric(18) signed    not null,
sdec0_10            PIC S9(9)             not null,
varchar0_uniq       varchar(16)      not null,
udec0_uniq          Decimal(9) unsigned   not null,
char0_10            Character(8)          not null,
char1_20            Character(32)         not null,
varchar1_4          varchar(8)       not null,
sdec1_uniq          Decimal(18) signed    not null,
sbin1_100           Numeric(4) signed     not null,
primary key  ( sbin1_100        ASC,
sdec1_uniq       ASC,
varchar1_4       DESC ) not droppable
)
store by primary key
location """ + gvars.g_disc1 + """
hash partition (add location """ + gvars.g_disc2 + """, add location """ + gvars.g_disc3 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create Table t1a014
(
ubin0_2             PIC 9(7)V9(2) COMP    not null,
sbin0_100           Numeric(18) signed    not null,
sdec0_10            PIC S9(9)             not null,
varchar0_uniq       varchar(16)      not null,
udec0_uniq          Decimal(9) unsigned   not null,
char0_10            Character(8)          not null,
char1_20            Character(32)         not null,
varchar1_4          varchar(8)       not null,
sdec1_uniq          Decimal(18) signed    not null,
sbin1_100           Numeric(4) signed     not null,
primary key  ( sbin1_100        ASC,
sdec1_uniq       ASC,
varchar1_4       DESC ) not droppable
)
store by primary key
location """ + gvars.g_disc1 + """
hash partition (add location """ + gvars.g_disc2 + """, add location """ + gvars.g_disc3 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t1a014 add constraint ct1a014
foreign key (sbin1_100,sdec1_uniq,varchar1_4)
references t1a014_1(sbin1_100,sdec1_uniq,varchar1_4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t1a014;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t1a014;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t1a014""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t1a014;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t1a014;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t1a014;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #------------------------------------------
    _testmgr.testcase_end(desc)

def test002(desc="""altered table -drop constraint"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #------------------------------------------
    
    #----------------------------------------------
    # a02.1 drop constraint - droppable primary key
    #----------------------------------------------
    
    stmt = """Create Table t2a021
(
sbin0_10            Numeric(18) signed    not null,
char0_2             Character(8)          not null,
udec0_uniq          Decimal(9) unsigned   not null,
ubin0_uniq          PIC 9(9) COMP         not null,
sdec0_500           PIC S9(9)             not null,
varchar0_10         varchar(16)      not null,
varchar1_20         varchar(8)       not null,
sbin1_5000          Numeric(4) signed     not null,
sdec1_4             Decimal(18) signed    not null,
char1_4             Character(8)          not null,    

constraint ct2a021 primary key  (udec0_uniq) droppable
)
store by (udec0_uniq)
location """ + gvars.g_disc8 + """
hash partition (add location """ + gvars.g_disc6 + """, add location """ + gvars.g_disc7 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t2a021 drop constraint ct2a021 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t2a021;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t2a021;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t2a021""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t2a021;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t2a021;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t2a021;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a02.2 drop constraint - drop unique constraint
    
    #btpnl19
    stmt = """Create Table t2a022
(
sdec0_2             PIC S9(9)             not null,
varchar0_100        varchar(16)      not null,
char0_4             Character(8)          not null,
sbin0_uniq          Numeric(18) signed    not null,
udec0_100           Decimal(9) unsigned   not null,
ubin0_uniq          PIC 9(9) COMP         not null,
sdec1_20            Decimal(18) signed    not null,
varchar1_10         varchar(8)       not null,
sbin1_1000          Numeric(4) signed     not null,
char1_10            Character(4)          not null,    

constraint ct2a022 unique (ubin0_uniq) droppable,
primary key ( sbin0_uniq ASC ) not droppable
)
store by primary key
location """ + gvars.g_disc4 + """
hash partition (add location """ + gvars.g_disc6 + """, add location """ + gvars.g_disc8 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t2a022 drop constraint ct2a022;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t2a022;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t2a022;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t2a022""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t2a022;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t2a022;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t2a022;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a02.3 drop constarint - drop check constraint
    #btpnl03
    stmt = """Create Table t2a023
(
sbin0_10            Numeric(18) signed    not null,
char0_2             Character(8)          not null,
udec0_uniq          Decimal(9) unsigned   not null,
ubin0_1000          PIC 9(7)V9(2) COMP    not null,
sdec0_500           PIC S9(9)             not null,
varchar0_10         varchar(16)      not null,    

varchar1_20         varchar(8)       not null,
sbin1_5000          Numeric(4) signed     not null,
sdec1_4             Decimal(18) signed    not null,
char1_4             Character(8)          not null,    

constraint ct2a023 check (sdec1_4 < 5) droppable,
primary key ( udec0_uniq  ASC ) not droppable
)
store by primary key location """ + gvars.g_disc6 + """
hash partition (add location """ + gvars.g_disc8 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t2a023 drop constraint ct2a023 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t2a023;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t2a023;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t2a023""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t2a023;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t2a023;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t2a023;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a02.4 drop constraint - drop foreign key
    
    # btpnl21
    stmt = """Create Table t2a024_1
(
ubin0_2             PIC 9(7)V9(2) COMP    not null,
sbin0_100           Numeric(18) signed    not null,
sdec0_10            PIC S9(9)             not null,
varchar0_uniq       varchar(16)      not null,
udec0_uniq          Decimal(9) unsigned   not null,
char0_10            Character(8)          not null,
char1_20            Character(32)         not null,
varchar1_4          varchar(8)       not null,
sdec1_uniq          Decimal(18) signed    not null,
sbin1_100           Numeric(4) signed     not null,
primary key  ( sbin1_100        ASC,
sdec1_uniq       ASC,
varchar1_4       DESC ) not droppable
)
store by primary key
location """ + gvars.g_disc1 + """
hash partition (add location """ + gvars.g_disc2 + """, add location """ + gvars.g_disc3 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create Table t2a024
(
ubin0_2             PIC 9(7)V9(2) COMP    not null,
sbin0_100           Numeric(18) signed    not null,
sdec0_10            PIC S9(9)             not null,
varchar0_uniq       varchar(16)      not null,
udec0_uniq          Decimal(9) unsigned   not null,
char0_10            Character(8)          not null,
char1_20            Character(32)         not null,
varchar1_4          varchar(8)       not null,
sdec1_uniq          Decimal(18) signed    not null,
sbin1_100           Numeric(4) signed     not null,
constraint ct2a024
foreign key (sbin1_100,sdec1_uniq,varchar1_4)
references t2a024_1(sbin1_100,sdec1_uniq,varchar1_4),
primary key  ( sbin1_100        ASC,
sdec1_uniq       ASC,
varchar1_4       DESC ) not droppable
)
store by primary key
location """ + gvars.g_disc1 + """
hash partition (add location """ + gvars.g_disc2 + """, add location """ + gvars.g_disc3 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t2a024 drop constraint ct2a024 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t2a024;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t2a024;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t2a024""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t2a024;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    _testmgr.testcase_end(desc)

def test003(desc="""altered table -add column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #a03.1 add column with default
    
    #btpns07
    stmt = """Create Table t3a031
(
varchar0_1000       varchar(1000)    not null,
-- length = 16 & 1000
char0_10            Character(32)         not null,
sbin0_4             Numeric(18) signed    not null,
udec0_20            Decimal(9) unsigned   not null,
ubin0_1000          PIC 9(7)V9(2) COMP    not null,
sdec0_uniq          PIC S9(9)             not null,
varchar1_uniq       varchar(128)     not null,
-- length = 16 & 64
sbin1_uniq          Numeric(4) signed     not null,
sdec1_2             Decimal(18) signed    not null,    
    
primary key ( varchar1_uniq ASC ) not droppable
)
store by primary key
location """ + gvars.g_disc1 + """
hash partition (add location """ + gvars.g_disc2 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t3a031 add column varchar2_uniq  varchar(64) default 'A'  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t3a031;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t3a031;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t3a031""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t3a031;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t3a031;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t3a031;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a03.2 add column with default, heading
    
    #btpns07
    stmt = """Create Table t3a032
(
varchar0_1000       varchar(1000)    not null,
-- length = 16 & 1000
char0_10            Character(32)         not null,
sbin0_4             Numeric(18) signed    not null,
udec0_20            Decimal(9) unsigned   not null,
ubin0_1000          PIC 9(7)V9(2) COMP    not null,
sdec0_uniq          PIC S9(9)             not null,
varchar1_uniq       varchar(128)     not null,
-- length = 16 & 64
sbin1_uniq          Numeric(4) signed     not null,
sdec1_2             Decimal(18) signed    not null,    
    
primary key ( varchar1_uniq ASC ) not droppable
)
store by primary key
location """ + gvars.g_disc1 + """
hash partition (add location """ + gvars.g_disc2 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t3a032 add column varchar2_uniq  varchar(64) default 'A' heading 'New Column' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t3a032;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t3a032;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t3a032""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t3a032;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t3a032;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t3a032;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a03.3 add column with default, heading, and not null
    #btpns07
    stmt = """Create Table t3a033
(
varchar0_1000       varchar(1000)    not null,
-- length = 16 & 1000
char0_10            Character(32)         not null,
sbin0_4             Numeric(18) signed    not null,
udec0_20            Decimal(9) unsigned   not null,
ubin0_1000          PIC 9(7)V9(2) COMP    not null,
sdec0_uniq          PIC S9(9)             not null,
varchar1_uniq       varchar(128)     not null,
-- length = 16 & 64
sbin1_uniq          Numeric(4) signed     not null,
sdec1_2             Decimal(18) signed    not null,    
    
primary key ( varchar1_uniq ASC ) not droppable
)
store by primary key
location """ + gvars.g_disc1 + """
hash partition (add location """ + gvars.g_disc2 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t3a033 add column varchar2_uniq  varchar(64)
default 'A' heading 'New Column' not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t3a033;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t3a033;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t3a033""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t3a033;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t3a033;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t3a033;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a03.4 add column with default, heading, and unique constraint
    #btpns07
    stmt = """Create Table t3a034
(
varchar0_1000       varchar(1000)    not null,
-- length = 16 & 1000
char0_10            Character(32)         not null,
sbin0_4             Numeric(18) signed    not null,
udec0_20            Decimal(9) unsigned   not null,
ubin0_1000          PIC 9(7)V9(2) COMP    not null,
sdec0_uniq          PIC S9(9)             not null,
varchar1_uniq       varchar(128)     not null,
-- length = 16 & 64
sbin1_uniq          Numeric(4) signed     not null,
sdec1_2             Decimal(18) signed    not null,    
    
primary key ( varchar1_uniq ASC ) not droppable
)
store by primary key
location """ + gvars.g_disc1 + """
hash partition (add location """ + gvars.g_disc2 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t3a034 add column varchar2_uniq  varchar(64)
default 'A' heading 'New Column' not null
constraint ct3a033 unique;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t3a034;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t3a034;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t3a034""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t3a034;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t3a034;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t3a034;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a03.5 add column with default, heading, and primary key constraint
    #btpns07
    stmt = """Create Table t3a035
(
varchar0_1000       varchar(1000)    not null,
-- length = 16 & 1000
char0_10            Character(32)         not null,
sbin0_4             Numeric(18) signed    not null,
udec0_20            Decimal(9) unsigned   not null,
ubin0_1000          PIC 9(7)V9(2) COMP    not null,
sdec0_uniq          PIC S9(9)             not null,
varchar1_uniq       varchar(128)     not null,
-- length = 16 & 64
sbin1_uniq          Numeric(4) signed     not null,
sdec1_2             Decimal(18) signed    not null    

)
store by (varchar1_uniq )
location """ + gvars.g_disc1 + """
hash partition (add location """ + gvars.g_disc2 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t3a035 add column varchar2_uniq  varchar(64)
default 'A' heading 'New Column' not null
constraint ct3a035 primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t3a035;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t3a035;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t3a035""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t3a035;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t3a035;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t3a035;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a03.6 add column with default, heading, and check constraint
    #btpns07
    stmt = """Create Table t3a036
(
varchar0_1000       varchar(1000)    not null,
-- length = 16 & 1000
char0_10            Character(32)         not null,
sbin0_4             Numeric(18) signed    not null,
udec0_20            Decimal(9) unsigned   not null,
ubin0_1000          PIC 9(7)V9(2) COMP    not null,
sdec0_uniq          PIC S9(9)             not null,
varchar1_uniq       varchar(128)     not null,
-- length = 16 & 64
sbin1_uniq          Numeric(4) signed     not null,
sdec1_2             Decimal(18) signed    not null    

)
store by (varchar1_uniq )
location """ + gvars.g_disc1 + """
hash partition (add location """ + gvars.g_disc2 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t3a036 add column varchar2_uniq  varchar(64)
default 'A' heading 'New Column' not null
constraint ct3a036 check (varchar2_uniq <> 'zqz') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t3a036;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t3a036;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t3a036""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t3a036;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t3a036;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t3a036;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a03.7 add column with default, heading, and reference
    #btpns07
    stmt = """Create Table t3a037_1
(
varchar0_1000       varchar(1000)    not null,
-- length = 16 & 1000
char0_10            Character(32)         not null,
sbin0_4             Numeric(18) signed    not null,
udec0_20            Decimal(9) unsigned   not null,
ubin0_1000          PIC 9(7)V9(2) COMP    not null,
sdec0_uniq          PIC S9(9)             not null,
varchar1_uniq       varchar(128)     not null,
-- length = 16 & 64
sbin1_uniq          Numeric(4) signed     not null,
sdec1_2             Decimal(18) signed    not null,
varchar2_uniq       varchar(64)      not null,
-- length = 8
primary key ( varchar2_uniq ASC ) not droppable
)
store by primary key
location """ + gvars.g_disc1 + """
hash partition (add location """ + gvars.g_disc2 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #btpns07
    stmt = """Create Table t3a037
(
varchar0_1000       varchar(1000)    not null,
-- length = 16 & 1000
char0_10            Character(32)         not null,
sbin0_4             Numeric(18) signed    not null,
udec0_20            Decimal(9) unsigned   not null,
ubin0_1000          PIC 9(7)V9(2) COMP    not null,
sdec0_uniq          PIC S9(9)             not null,
varchar1_uniq       varchar(128)     not null,
-- length = 16 & 64
sbin1_uniq          Numeric(4) signed     not null,
sdec1_2             Decimal(18) signed    not null    

)
store by (varchar1_uniq )
location """ + gvars.g_disc1 + """
hash partition (add location """ + gvars.g_disc2 + """);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t3a037 add column varchar2_uniq  varchar(64)
default 'A' heading 'New Column' not null
constraint ct3a037 references t3a037_1 (varchar2_uniq) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t3a037;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t3a037;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t3a037""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t3a037;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t3a037;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t3a037;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""altered table -alter attribute"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #a04.1 alter attribute allocate
    
    #btpnl23
    stmt = """Create Table t4a041
(
char0_20            Character(8)          not null,
sdec0_uniq          PIC S9(9)             not null,
varchar0_20         varchar(16)      not null,
ubin0_20            PIC 9(7)V9(2) COMP    not null,
sbin0_uniq          Numeric(18) signed    not null,
udec0_4             Decimal(9) unsigned   not null,
sbin1_500           Numeric(4) signed     not null,
sdec1_100           Decimal(18) signed    not null,
char1_uniq          Character(128)        not null,
varchar1_2          varchar(8)       not null,
primary key ( char1_uniq  DESC ) not droppable
)
store by primary key
attributes
extent (512, 512)
maxextents 218
allocate 128;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t4a041 attribute allocate 218;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
  
    stmt = """showlabel t4a041;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t4a041""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t4a041;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
   
    stmt = """showddl t4a041;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    stmt = """showlabel t4a041;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a04.2 alter attribute auditcompress and clearonpurge
    
    #btpns01
    stmt = """Create Table t4a042
(
char0_20            Character(8)          not null,
sbin0_2             Numeric(18) signed    not null,
udec0_10            Decimal(9) unsigned   not null,
varchar0_2          varchar(16)      not null,
sdec0_1000          PIC S9(9)             not null,
ubin0_20            PIC 9(7)V9(2) COMP    not null,    

char1_2             Character(16)         not null,
sdec1_uniq          Decimal(18) signed    not null,
sbin1_100           Numeric(4) signed     not null,
varchar1_uniq       varchar(8)       not null,
primary key (sdec1_uniq)
)
location """ + gvars.g_disc1 + """
hash partition (add location """ + gvars.g_disc2 + """, add location """ + gvars.g_disc3 + """)
attributes
auditcompress
no clearonpurge;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t4a042 attribute no auditcompress;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t4a042 attribute clearonpurge;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t4a042;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t4a042;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t4a042""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t4a042;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t4a042;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t4a042;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #a04.3 alter attribute maxextents
    
    #btpns05
    stmt = """Create Table t4a043
(
sdec0_2             PIC S9(9)             not null,
varchar0_100        varchar(16)      not null,
char0_4             Character(8)          not null,
sbin0_uniq          Numeric(18) signed    not null,
udec0_100           Decimal(9) unsigned   not null,
ubin0_uniq          PIC 9(7)V9(2) COMP    not null,
sdec1_20            Decimal(18) signed    not null,
varchar1_10         varchar(8)       not null,
sbin1_1000          Numeric(4) signed     not null,
char1_10            Character(4)          not null,
primary key ( sbin0_uniq DESC ) not droppable
)
store by primary key
location """ + gvars.g_disc1 + """
hash partition(add location """ + gvars.g_disc2 + """, add location """ + gvars.g_disc3 + """)
attributes
maxextents 768
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table t4a043 attribute maxextents 568;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t4a043;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t4a043;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    save_ddl_to_obeyfile("""t4a043""", defs.work_dir + """/obeyfile""") 
    
    stmt = """drop table t4a043;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    output = _testmgr.exec_dci_with_obeyfile(defs.work_dir + """/obeyfile""") 
    
    stmt = """showddl t4a043;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showlabel t4a043;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

