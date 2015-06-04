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

import time
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
 
def test001(desc="""a01 add 2 fix columns (start with fix columns)"""):
# -------------------------------------------------------------------
#testcase a01 a01 add mix columns (start with fix columns)
# -------------------------------------------------------------------
# Simple add columne test
# table starts with fix columns. add 1 fixed column and 1 variable column
# -------------------------------------------------------------------
# base table:
# column 1: orders int
# column 2: ch1      varchar(1)
# add column:
#   column 3: px1      pic x(1)
#   column 4: ch2      char(1)
# -------------------------------------------------------------------
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table a01table;"""
    output = _dci.cmdexec(stmt)
    
    # table start with 2 fixed length field
    stmt = """create table a01table (
    orders int no default not null
  , ch1 varchar(1) 
  , primary key (orders ASC) not droppable
  );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a01table values (1,'a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """insert into a01table values (2,'b');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """insert into a01table values (3,'c');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """insert into a01table values (4,'d');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """insert into a01table values (5,'e');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """insert into a01table values (6,'f');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """insert into a01table values (7,'g');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """insert into a01table values (8,'h');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """insert into a01table values (9,'i');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """insert into a01table values (10,'j');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add column: fixed length field, no default
    stmt = """alter table a01table add column px1 PIC X(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a01table values (11,'k','1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a01table (orders, ch1) values (12,'l');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a01table values (13,'m','2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a01table (orders, ch1) values (14,'n');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a01table (orders, px1) values (99,'2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """update a01table set px1 = '0' where orders < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,4)

    # -------------------------------------------------------------------
    # RG:
    #Test failed on orders=13 and 99. Missing px1 values.
    # expected px1 for orders 13 and 99 to be 2, but got ?
    # -------------------------------------------------------------------
    
    stmt = """select * from a01table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')

    # add column: variable length field, default literal
    stmt = """alter table a01table add column ch2 char (1) default 'Z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # insert partial rows

    stmt = """insert into a01table values (15,'o','3','A');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a01table (orders, ch1) values (16,'p');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)   
    stmt = """insert into a01table (orders, ch1, px1) values (17,'p','B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a01table (orders) values (18);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)    

    #insert full rows
    stmt = """insert into a01table values (19,'q','4','C');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a01table values (20,'r','5','D');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a01table values (21,'s','6','E');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    #run some different select statements
    #fetch rows based on key values (unique fetch)  
    stmt = """select * from a01table where px1 = 'B' order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')

    stmt = """select * from a01table where orders >= 20 or orders < 3 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    #fetch a range of rows (subset fetch)
    stmt = """select * from a01table where px1 = '2' order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')

    stmt = """select * from a01table where ch2 < 'E' order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')

    #fetch rows where the default value is null
    #fetch rows where the default value is not null

    stmt = """select * from a01table where ch1 is NULL order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')

    stmt = """select * from a01table where px1 is NOT NULL order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')

    #run some update tests (verify with selects after each update)
    #update an added column based on a key column values (unique fetch)
    #update an added column with the previous values
    #update a rnage of added columns
    #do some delete statements (verify with selected after delete)

    stmt = """set param ?p0 '0';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 '2';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 '7';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 'g';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 'W';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p5 3;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p6 20;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p7 10;"""
    output = _dci.cmdexec(stmt)

    stmt = """update a01table set px1 = ?p1 where orders < ?p5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,2)

    stmt = """update a01table set ch2 = ?p2, px1 = ?p1 where ch1 = ?p3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update a01table set ch1 = ?p0 where orders > ?p6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,2)

    stmt = """update a01table set ch2 = ?p4 where orders <= ?p7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,10)
    
    stmt = """select * from a01table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02 add 8 columns (start with mix columns)"""):
# -------------------------------------------------------------------
# add 8 more columns to the table with various fixed and variable
# length columns
# -------------------------------------------------------------------
# base table:
# column 1: orders int
# column 2: ch1   varchar(1)
# column 3: num1     numeric (9,2) unsigned
# add column:
#   column 4: vch1     varchar(1)
#   column 5: sma1     smallint unsigned
#   column 6: vch2     varchar(255)
#   column 7: int1     int unsigned
#   column 8: vch3     varchar(2)
#   column 9: dec1     dec(9,2) unsigned
# -------------------------------------------------------------------
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """alter table a02table drop constraint int_a02;"""
    output = _dci.cmdexec(stmt)
    stmt = """alter table a2itable drop constraint int_c02;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a2itable cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a02table cascade;"""
    output = _dci.cmdexec(stmt)

    #table start with 2 fixed length field
    stmt = """create table a02table (
    orders int no default not null
  , ch1 varchar(1) 
  , num1 NUMERIC (9,2) UNSIGNED default null no heading
  , primary key (orders ASC) not droppable
  );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a02table (orders, ch1) values (1,'a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)
    stmt = """insert into a02table (orders, ch1) values (2,'b');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)
    stmt = """insert into a02table (orders, ch1) values (3,'c');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)

    stmt = """insert into a02table values (11,'k',1.01);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table (orders, ch1) values (12,'l');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table values (13,'m',2.02);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    #expected 6 rows 
    stmt = """select * from a02table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    # -------------------------------------------------------------------
    # add column 3: variable length field, no default 
    # -------------------------------------------------------------------
    stmt = """alter table a02table add vch1 char varying(1) heading '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #insert partial rows
    stmt = """insert into a02table values (15,'o',3.03,'A');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table (orders, ch1) values (16,'p');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table (orders, ch1, num1) values (17,'p',4.04);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table (orders) values (18);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    #insert full rows
    stmt = """insert into a02table values (19,'q',5,'B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table values (20,'r',6.00,'C');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    #12 rows
    stmt = """select * from a02table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    #run  some different select statements
    # fetch rows based on key values(unique fetch)
    stmt = """select * from a02table where num1 > 1 and num1 <= 4.5 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    stmt = """select * from a02table where orders = 13 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    #fetch a range of rows (subset fetch)
    stmt = """select * from a02table where num1 < 5.50 and vch1 is not null order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    stmt = """select * from a02table where vch1 >= 'B' order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    #fetch rows where the default value is null
    #fetch rows where the default value is not null
    stmt = """select * from a02table where num1 is NOT NULL and vch1 is null order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    stmt = """select * from a02table where vch1 is NOT NULL order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')

    #run some update tests (verify with selects after each update)
    #update an added column based on a key column values (unique fetch)
    #update an added column with the previous values
    #update a rnage of added columns
    #do some delete statements (verify with selected after delete)
    stmt = """update a02table set vch1 = '6' where num1 = 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,1)
    stmt = """update a02table set num1 = num1 * num1 where vch1 is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,9)
    stmt = """select num1, vch1 from a02table where num1 is not null order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    # -------------------------------------------------------------------
    # add column 4: fixed length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a02table add column sma1 SMALLINT UNSIGNED DEFAULT NULL
  heading 'SmallInt';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into a02table (orders, sma1) values (51,21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table values (52,'S',5.01,'D',22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    # -------------------------------------------------------------------
    # add column 5: variable length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a02table add vch2 CHARACTER VARYING(255);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into a02table (orders, vch2) values (61,'character varying(255)');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table values (62,'V',5.02,'E',23,'variable length column');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table (orders, num1, sma1, vch2)
   values (63, 5.03, 24, 'variable length column vch2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """update a02table set sma1 = 99 where vch2 like '%vch2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    stmt = """select orders, num1, sma1, vch2 from a02table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    # -------------------------------------------------------------------
    # add column 6: fixed length field, default NULL
    # -------------------------------------------------------------------
    # record format in tuple: orders, ch1, num1, sma1, int1, vch1, vch2
    # physical order in row : orders, ch1, num1, vch1, sma1, vch2, int1
    # -------------------------------------------------------------------
    stmt = """alter table a02table add column int1 int unsigned 
  constraint int_a02 check (int1 < 10000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into a02table values 
  (71, 'I', 7.02, 'F', 700, 'VARCHAR', 100); """
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table (orders, int1) values (72,200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table (orders, vch2, int1) values (73,'VCH2', 300);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table (orders, vch1, sma1, int1) values (74, '2', 72, 400);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    # -------------------------------------------------------------------
    # add column 7: variable length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a02table add vch3 CHARACTER VARYING(2) heading 'VARYING(2)';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into a02table (orders, num1, sma1, int1) 
  values (81,8.08,81,81);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table (orders, vch3) values (82,'AB');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table (orders, ch1, vch1, vch2, vch3) 
   values (83,'8','8','vch1_83','83');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """update a02table set vch3 = 'CD' where ch1 = 'k';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    stmt = """insert into a02table values
   (84,'8', 8.234, '8', 84, 
   'Bill and Joe ran softly near one of the hill. Some birds sprinted over Madelyn! Racoons and cats and blue birds. Oh My! Violet and Fred rushed sadly towards some door! Genelle and Janine split steadily across one of the string???',
    84, '83');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    #expected 25 rows
    stmt = """select * from a02table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')

    # -------------------------------------------------------------------
    # add column 8: variable length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a02table add column dec1 DEC(9,2) UNSIGNED;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into a02table values 
  (91,'9',9.1,'9',91,
  'EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE007P6RRT Mom sprinted beneath those worms??? A few horses got out beside Derek??? Those dogs ambled across dad??? An American and Ben leaped neatly over those string??? ',
  91, '91', 9.1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table (orders, dec1) values (92,9.20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """select count(*) from a02table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output,'27')
    stmt = """select orders, vch2, int1 from a02table where ch1 is NULL and int1 > 300 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    stmt = """select orders, vch2, int1 from a02table where dec1 is NOT NULL order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    stmt = """select orders, vch3 from a02table where dec1 < 10 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    stmt = """select orders, int1, sma1, vch1, vch2, vch3 from a02table where vch3 = 'AB' order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    stmt = """update a02table set vch2 = 'VVCCHH2',
               vch3 = 'VV',
               sma1 = 65535,
               dec1 = 1234567.89
       where orders < 20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,11)
    stmt = """select avg(num1), sum(sma1), max(dec1) from a02table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    stmt = """select count(*) from a02table;"""
    output = _dci.cmdexec(stmt)
    
    # delete orders=71
    stmt = """delete from a02table where num1 = 7.02 and ch1 = 'I';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,1)
    
    stmt = """delete from a02table where orders in (2,51,52,81,82,92);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,6)
    
    # 20 rows left
    stmt = """select orders, num1, sma1, dec1 from a02table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    
    stmt = """select orders, vch1, int1, vch3 from a02table where vch2 = 'VVCCHH2' order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    
    # -------------------------------------------------------------------
    # dup a02table to a2itable, constraint on, target new;
    # -------------------------------------------------------------------
    stmt = """create table a2itable like a02table;"""
    output = _dci.cmdexec(stmt)
    time.sleep(5)
    
    stmt = """alter table a2itable add constraint idx_a2i check (int1 < 10000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a2itable select * from a02table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,20)
  
    # -------------------------------------------------------------------
    # add column 9: fixed length field, default 
    # -------------------------------------------------------------------
    stmt = """alter table a2itable add num10 NUMERIC (9,2) SIGNED default 7.2 
  heading 'num_10';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a2itable (orders,num1) values (101,1.01);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a2itable (orders,ch1,vch2,num10) 
  values (102,'A','VCH6',1.02);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # -------------------------------------------------------------------
    # add column 10: variable length field, default literal
    # -------------------------------------------------------------------
    stmt = """alter table a2itable add vch11 char varying(1) default 'a' heading 'vch11';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # insert partial rows
    stmt = """insert into a2itable (orders,ch1,num1,vch1,sma1,vch2,int1,vch3,dec1,num10)
  values (103,'A',3.03,'A',303,'VCHAR_6',3030,'EE',33.03, 333.33);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a2itable (orders, num10, vch11) values (104,1.04,'4');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # insert full rows
    stmt = """insert into a2itable values 
  (106,'A',1.06,'A',106,'VVV_VVV',1060,'66',10.06, 106.00,'a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # expected 25 rows
    stmt = """select orders, num10, vch3, vch11 from a2itable order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s23')
    
    # run some different select statements
    # fetch rows based on key values (unique fetch)
    stmt = """select * from a2itable where vch3 = 'EE' order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s24')
    
    # fetch a range of rows (subset fetch)
    stmt = """select * from a2itable where num10 < 2.00 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s25')

    # run some update tests (verify with selects after each update)
    # update an added column based on a key column values (unique fetch)
    # update an added column with the previous values
    # update a rnage of added columns
    # do some delete statements (verify with selected after delete)
    stmt = """update a2itable set num10 = num10 + 10.10,
                    vch3 = 'NN' where dec1 is NOT NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,13)

    stmt = """select orders, num10, vch3, dec1 from a2itable where dec1 is NOT NULL order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s25a')

    stmt = """set param ?a02 '0';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?i02 0;"""
    output = _dci.cmdexec(stmt)

    stmt = """update a2itable set vch11 = ?a02,
  num1 = ?i02, sma1 = ?i02, int1 = ?i02, dec1 = ?i02 where orders = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """select orders, vch11, num1, sma1, int1, dec1 from a2itable where orders < 3 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s26')
    
    # delete row orders =20
    stmt = """delete from a2itable where dec1 is NULL and orders < 50;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    #expected 24 rows
    stmt = """select orders, vch3, num10, vch11, dec1 from a2itable 
   where dec1 <> 1234567.89 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s27')
    
    # -------------------------------------------------------------------
    # add column 11: fixed length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a2itable add column sma12 SMALLINT SIGNED default -1
  check (sma12 < 65535 and sma12 > -100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a2itable (orders, sma1, vch3) values (112,12,'12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a2itable (orders, sma12) values (113, 113);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # -------------------------------------------------------------------
    # add column 12: variable length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a2itable add column vch13 CHARACTER VARYING(255) 
  default 'xxxxxxxxxx';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # alter table a2itable add column int1 int unsigned
    #   constraint int1_a2i check (int1 < 10000);
    
    stmt = """insert into a2itable (orders, vch1, int1) values (114,'A',11400);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8101')
    
    stmt = """insert into a2itable (orders, vch1, int1) values (114,'A',1140);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """update a2itable set vch13 = vch2 where orders = 61;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """select orders, vch13, vch2 from a2itable where orders = 61;"""
    output = _dci.cmdexec(stmt)
   
    # -------------------------------------------------------------------
    # add column 13: fixed length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a2itable add column int14 int signed default -100 
  constraint int_c02 check (int14 < 1234567890);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a2itable values 
  (115, 'A', 7.02, 'A', 700, 'VARCHAR', 100,'VV',9.02,
   9.02,'Y', 1, 'COL_14_VCH13', 100); """
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a2itable (orders, int1, vch11) values (116,116,'Z');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    

    stmt = """update a2itable set int14 = int14 - 1, sma12 = sma12 + 100 
  where orders < 50 or orders > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,20)

    stmt = """select count(*) from a2itable;"""
    output=_dci.cmdexec(stmt)
    _dci.expect_str_token(output, '29')
    stmt = """select orders, int14, sma12 from a2itable where orders between 50 and 100 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,9)
    stmt = """select count(*) from a2itable;"""
    output=_dci.cmdexec(stmt)
    _dci.expect_str_token(output, '29')
    # -------------------------------------------------------------------
    # add column 14: variable length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a2itable add column vch15 CHARACTER VARYING(2) default 'zz';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # add odd columns
    stmt = """insert into a2itable (orders, num10, vch3, int14, ch1) 
  values (120,1.20,'V8',120, 'y');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    #add even columns
    stmt = """insert into a2itable (orders, ch1, vch1, vch2, vch3, vch11) 
   values (121,'X','x','vch2_varchar255','xx','x');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a2itable (orders,vch13) values (123,'the following are eligible for membership: non-profit organizations, educational institutions, market researchers, publishers, consultants, governments, and organizations and businesses who do not create, market or sell computer products or services.');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """update a2itable set vch15 = 'CD' where ch1 = 'y';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """select orders, vch15, ch1 from a2itable order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s28')
    

    # -------------------------------------------------------------------
    # add column 15: variable length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a2itable add column dec16 DEC(9,7) SIGNED default -9.99;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a2itable values 
  (124,'B',12.4,'b',124,'VCH6_COL16',1240,'Bb',1.24,
   11.24,'b',1124,'VCH13_COL16',11240,'bB',12.1234567);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a2itable (orders, dec16) values (125,-1.00001);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select count(*) from a2itable where orders > 100;"""
    output = _dci.cmdexec(stmt)

    stmt = """select orders, num1, vch3, sma12, vch15 from a2itable where ch1 = '8' 
order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s29')
    
    stmt = """select orders, int1, sma1, vch11, vch13, vch15 from a2itable where vch1 = 'x' order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s30')
    
    stmt = """update a2itable set 
    ch1   = 'q',
    num1  = 1.23,
    vch1  = 'Q',
    vch2  = 'Such book shall be kept at the principal office of the Corporation and shall be subject to the rights of inspection required by law as set forth in Section 2.9 of these Bylaws. The Administrator shall be responsible for maintaining such book.',
    vch11 = 'q',
    vch15 = 'CD',
    sma1  = 123,
    vch13 = 'Such book shall be kept at the principal office of the Corporation and shall be subject to the rights of inspection required by law as set forth in Section 2.9 of these Bylaws. The Administrator shall be responsible for maintaining such book.',
    int14 = 123456789
  where orders = 123; """
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """select * from a2itable where orders = 123 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s31')
    
    # -------------------------------------------------------------------
    # add column 16: variable length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a2itable add column vch17 varchar(80) upshift default '12345678901234567890123456789012345678901234567890123456789012345678901234567890' 
  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a2itable (orders, dec1, num10, dec16) 
  values (127, 12.7, 12.7, 12.7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a2itable (orders, dec1, num10, dec16, int1)
  values (128, 12.8, 12.8, 12.8, 114400);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8101')
    
    stmt = """insert into a2itable (orders, dec1, num10, dec16, int1)
  values (128, 12.8, 12.8, 12.8, 1128);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """delete from a2itable where num1 is NULL
            and sma12 = -1 and int14 = -100 and orders < 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,5)
    
    # expected 31 rows selected
    stmt = """select count(*) from a2itable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output,'31')
    
    stmt = """select orders, num1, dec1, int1, vch2 from a2itable where orders < 500 order by orders; """
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s32')
        
    _testmgr.testcase_end(desc)

# -------------------------------------------------------------------
# testcase test003 a03 add 3 mix columns (start with fix columns)
# -------------------------------------------------------------------
# start with only fixed length fields
# Add fixed column and variable column in sequence
# -------------------------------------------------------------------
# base table:
# column 1: sma1 smallint
# column 2: int2 int
# insert couple rows
#   add column 3 - fixed, no default 
# insert couple rows
#   add column 4 - fixed, default     
# insert couple full rows
# insert couple rows without added columns
#   add column 5 - variable length, no default
# run some different select statements
#   * fetch rows based on key values (unique fetch)
#   * fetch a range of rows (subset fetch)
#   * fetch rows where the default value is null
#   * fetch rows where the default values is not null
# run some update statements
#   * update an added column based on a key column value
#   * update an added column with previous value
#   * update a range of add columns
# -------------------------------------------------------------------
def test003(desc="""a03 add 3 mix columns (start with fix columns)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table a03table;"""
    output = _dci.cmdexec(stmt)
    
    # table start with 2 fixed length field
    stmt = """create table a03table (
    sma1 smallint no default not null
  , int2 integer
  , vch1 varchar(1)
)
store by (sma1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a03table values (1,1,'1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)

    # -------------------------------------------------------------------
    # add column 3: fixed length field, primary key
    # -------------------------------------------------------------------

    stmt = """alter table a03table add int3 int signed default 1
  constraint int3_c primary key asc not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    time.sleep(5)

    stmt = """insert into a03table values (2,2,'2',2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a03table values (3,3,'3',3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # -------------------------------------------------------------------
    # add column 4: fixed length field, default NULL
    # -------------------------------------------------------------------

    stmt = """alter table a03table add i64_4 largeint 
   default null heading 'LargeInt';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a03table (sma1, int3, i64_4) values (4, 4, 1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)

    stmt = """insert into a03table values (5,5,'5',5,2000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)

    stmt = """insert into a03table values (6,6,'6',6,3000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)

    stmt = """insert into a03table (sma1, int2, int3) values (7,7,7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)

    stmt = """insert into a03table (sma1, int3) values (8,8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)
    
    stmt = """select * from a03table order by sma1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')

    # -------------------------------------------------------------------
    # add column 5: variable length field, default literal
    # -------------------------------------------------------------------

    stmt = """alter table a03table add column vch5 VARCHAR(5) UPSHIFT 
   default 'aaaaa' heading '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # fetch row based on key values
    stmt = """select * from a03table where int3 = 7 order by sma1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    stmt = """select * from a03table where int3 <= 3 order by sma1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')

    stmt = """select * from a03table where i64_4 is NULL order by sma1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')

   
    stmt = """select * from a03table where int2 is NOT NULL order by sma1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')

    # update an added column based on key column
    stmt = """update a03table set vch5 = 'abcde' where 
    int3 = 8 and i64_4 is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    #stmt = """select * from a03table;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')

    # i64_4 default is null
    # update a range of add columns plus previous value
    stmt = """update a03table set i64_4 = i64_4 + 100000 
        where int3 >= 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """select * from a03table order by sma1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')

    stmt = """insert into a03table values (9,9,'9',9,987654321,'vch5');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a03table (sma1, int3, vch5) values (10, 10, 'VarCh');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """select * from a03table order by sma1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')

    _testmgr.testcase_end(desc)
# -------------------------------------------------------------------
#testcase a04 a04 add mix columns (start with variable length columns)
# -------------------------------------------------------------------
# Simple add columne test
# Table starts with only variable length columns 
# Add fixed column and variable column in sequence
# base table:
# column 1: varchar 
# column 2: varchar
# insert couple rows
#   add column 3 - fixed, no default 
# insert couple rows
#   add column 4 - fixed, default     
# insert couple full rows
# insert couple rows without added columns
#   add column 5 - variable length, no default
# run some different select statements
#   * fetch rows based on key values (unique fetch)
#   * fetch a range of rows (subset fetch)
#   * fetch rows where the default value is null
#   * fetch rows where the default values is not null
# run some update statements
#   * update an added column based on a key column value
#   * update an added column with previous value
#   * update a range of add columns
# -------------------------------------------------------------------
def test004(desc="""a04 add mix columns (start with variable length columns)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """control query default pos 'off';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table a04table;"""
    output = _dci.cmdexec(stmt)
    
    # table start with 2 fixed length field
    stmt = """create table a04table (
    vch1 VARCHAR(3)
  , vch2 CHAR VARYING(3)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # insert row 1 to 3
    stmt = """insert into a04table values ('aaa','AAA');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)

    stmt = """insert into a04table values ('bbb','BBB');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)

    stmt = """insert into a04table values ('ccc','CCC');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)
    
    # a04.2:
    # -------------------------------------------------------------------
    # add column 3: int3 int default 1;
    # -------------------------------------------------------------------

    stmt = """alter table a04table add int3 int signed default 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # a04.3: insert row 4
    stmt = """insert into a04table (vch1, vch2) values ('ddd','DDD');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    #  insert row 5
    stmt = """insert into a04table values ('eee','EEE',3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)

    # -------------------------------------------------------------------
    # add column 4: i64_4 largeint, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a04table add i64_4 largeint 
   default null heading 'LargeInt';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # insert row 6 to 10
    stmt = """insert into a04table (vch1, int3, i64_4) values ('fff', 4, 1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a04table values ('555','GGG',5,2000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a04table values ('666','H',6,3000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a04table (vch1, vch2, int3) values ('77','7',7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a04table (vch2, int3) values ('88',8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output) 
   
    stmt = """select * from a04table order by vch1,vch2,int3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    # -------------------------------------------------------------------
    # add column 5: vch5 VARCHAR(5), UPSHIFT default literal heading ''
    # -------------------------------------------------------------------
    stmt = """alter table a04table add column vch5 VARCHAR(5) UPSHIFT 
   default 'aaaaa' heading '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from a04table order by vch1,vch2,int3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    # fetch row based on key values
    stmt = """select * from a04table where int3 = 7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,1)
    
    stmt = """select * from a04table where vch2 is NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,1)

    stmt = """select * from a04table where i64_4 is NOT NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,3)

    # update an added column based on key column
    stmt = """update a04table set vch5 = 'abcde', 
        i64_4 = 8000 where vch5 = 'AAAAA' and int3 = 8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """select * from a04table order by vch1,vch2,int3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')

    # i64_4 default is null
    # update a range of add columns plus previous value
    stmt = """update a04table set i64_4 = i64_4 + 100000 
        where int3 >= 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,6)
    
    stmt = """update a04table set int3 = i64_4 / 2 where vch1 = 'fff';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """select * from a04table order by vch1,vch2,int3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    stmt = """insert into a04table values ('9','X',9,987654321,'vch5');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a04table (int3, vch5) values (10, 'Var10');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a04table (vch1, int3, vch5) values ('11', 11, 'Var11');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """update a04table set int3 = int3 * int3 + 2 where vch1 < 'ccc';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,7)
    
    stmt = """select * from a04table order by vch1,vch2,int3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    # -------------------------------------------------------------------
    # add column 6: vch6 VARCHAR(3) default NULL
    # -------------------------------------------------------------------

    stmt = """alter table a04table add column vch6 VARCHAR(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from a04table order by vch1,vch2,int3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    stmt = """insert into a04table (int3, vch5) values (12,'Var12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a04table values ('13', 'y', 13,123456789,'Var13','V13');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a04table (int3) values (14);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """update a04table set vch6 = 'CCC',
                   vch5 = 'CCC',
                   vch2 = 'CCC',
                   i64_4 = 101010,
                   vch1 = 'CCC'
  where int3 between 1 and 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,7)  

    stmt = """select * from a04table order by vch1,vch2,int3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    # -------------------------------------------------------------------
    # add column 7: pic7 picture s9(9)v9(2), default value
    # add column 8: pic8 pic 9(4)v9(3) display sign is leading, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a04table add column pic7 picture S9(9)V9(2) DISPLAY default -0.77;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table a04table add column pic8 pic 9(4)V9(3) DISPLAY SIGN IS LEADING;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ----------------------------------------------------------------------
    # NE: Missing NULL values after alter add column to a no partition table
    # ----------------------------------------------------------------------
    stmt = """select * from a04table order by vch1,vch2, int3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    stmt = """insert into a04table (int3, vch6) values (15,'V15');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a04table values ('16', 'z', 16,163456789,'Var16','V16',7.16,8.16);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a04table (int3, pic7) values (17, 17.17);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a04table (int3, pic8) values (18, 18.18);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)    

    stmt = """update a04table set pic7 = -100.01,
                   pic8 = 100.01
  where int3 < 100 and i64_4 is NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,6)    

    # ----------------------------------------------------------------------
    # NE: Missing NULL values after alter add column to a no partition table
    # ----------------------------------------------------------------------

    stmt = """select * from a04table order by vch1,vch2,int3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    
    # -------------------------------------------------------------------
    # add column 9: variable length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a04table add column vch9 varchar(1) default null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ----------------------------------------------------------------------
    # NE: Missing NULL values after alter add column to a no partition table
    # ----------------------------------------------------------------------
    stmt = """select * from a04table order by vch1,vch2,int3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    
    stmt = """insert into a04table (int3, pic7) values (19, 19.19);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a04table values 
  ('20', '20', 20, 203456789, 'Var20', 'V20', -9.20, 9.20, '9');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """update a04table set pic8 = 200.22,
               vch9 = 'g',
               vch1 = 'ggg'
  where pic7 = -.77 and int3 > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,2)
    
    # ----------------------------------------------------------------------
    # NE: Missing NULL values after alter add column to a no partition table
    # ----------------------------------------------------------------------

    stmt = """select * from a04table order by vch1,vch2,int3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    
    stmt = """control query default pos 'multi_node';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    
# -------------------------------------------------------------------
#testcase test005 a05 add columns: default current date,time,user,timestamp
# -------------------------------------------------------------------
# Simple add columne test
# Exercise DATE, TIME, TIMESTAMP and default CURRENT_DATE, CURRENT_TIME,
# CURRENT_TIMESTAMP, CURRENT_USER, SESSION_USER, and USER.
# Table starts with a fixed and a variable columns
# Add fixed columns and variable columns in sequence
# DUP table with added columns to a new table
# Add more columns to the new table
# -------------------------------------------------------------------
def test005(desc="""a05 add columns: default current date,time,user,timestamp"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table a05table;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a5itable;"""
    output = _dci.cmdexec(stmt)
    
    # table start with 2 fixed length field
    stmt = """create table a05table (
    int1 integer no default not null
  , vch2 CHAR VARYING(8) 
  , primary key (int1 asc) not droppable
)
store by primary key
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # insert couple rows 
    # row 1 and 2
    stmt = """insert into a05table (int1, vch2) values (1,'row_1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a05table values (2,'row_2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """select * from a05table order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    # -------------------------------------------------------------------
    # add column 3: dt00 DATE default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a05table add column dt00 DATE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # row 3 and 4
    stmt = """insert into a05table values (3, 'row_3', date '2005-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a05table values (4, 'row_4', date '2005-01-02');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # -------------------------------------------------------------------
    # add column 4: tidf TIME default CURRENT_TIME
    # -------------------------------------------------------------------

    stmt = """alter table a05table add tidf TIME default CURRENT_TIME;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # row 5 and 6
    stmt = """insert into a05table values (5, 'row_5', date '2005-01-03', CURRENT_TIME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a05table values (6, 'row_6', date '2005-01-04', time '06:06:06');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # -------------------------------------------------------------------
    # add column 5: usr0 VARCHAR(20) default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a05table add usr0 varchar(20) default '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a05table order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    # row 7 and 8
    stmt = """insert into a05table (int1, vch2) values (7, 'row_7'); """
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a05table values 
  (8, 'row_8', date '2005-01-05', time '08:08:08', ''); """
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # -------------------------------------------------------------------
    # add column 6: tsdf
    # -------------------------------------------------------------------
    stmt = """alter table a05table add column tsdf TIMESTAMP default CURRENT_TIMESTAMP;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a05table order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    # insert row 9, 10, and 11
    stmt = """insert into a05table (int1, usr0) values (9, '');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a05table (int1, tsdf) values 
  (10, timestamp '1010-01-31:01:31:00.123456');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a05table values 
  (11, 'row_11', date '1011-01-31', time '11:11:11', '', 
      timestamp '1994-01-31:01:31:00.123456');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """select * from a05table order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    # -------------------------------------------------------------------
    # add column 7: ts00 TIMESTAMP(0) default CURRENT_TIMESTAMP
    # -------------------------------------------------------------------
    stmt = """alter table a05table add ts00 TIMESTAMP(0) default CURRENT_TIMESTAMP;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # row 12, 13, 14
    stmt = """insert into a05table (int1, dt00, ts00 ) values 
  (12, date '1996-01-31', timestamp '1996-01-31:12:12:12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a05table (int1, usr0, tsdf ) values 
  (13, 'user', timestamp '1997-01-31:13:13:13.123456');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a05table values 
  (14, 'row_14', date '1998-01-31', time '08:00:00', 'tank', 
   timestamp '1998-01-31:01:31:00.123456', 
   timestamp '1998-02-28:14:14:14');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a05table order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    # -------------------------------------------------------------------
    # add column 8: usr1 char(18) default USER
    # -------------------------------------------------------------------
    stmt = """alter table a05table add usr1 char(18) default '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a05table order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')

    # row 15
    stmt = """insert into a05table (int1, usr0) values (15,'qadev.sqlqaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # row 16
    stmt = """insert into a05table values 
  (16, 'row_16', date '2000-01-31', time '08:00:00', 'noe.smith',
   timestamp '2000-01-31:01:31:00.123456', 
   timestamp '2000-02-28:08:08:08','');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a05table order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    # -------------------------------------------------------------------
    # add column 9: usrs varchar(20) default SESSION_USER
    # -------------------------------------------------------------------
    stmt = """alter table a05table add usrs varchar(20) default '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from a05table order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')

    #varible select
    stmt = """select * from a05table where int1 = 10 order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s81')
    
    #stmt = """select * from a05table where usr0 = '' order by int1;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s82')
    
    #stmt = """select * from a05table where usr1 = '' order by int1;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s83')

    stmt = """select * from a05table 
  where dt00 = date '2005-01-01' and
        tidf = time '12:00:00' and
        tsdf = timestamp '0001-01-01:12:00:00.000000' and usrs = '' order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s84')
    
    stmt = """update a05table set usr1 = 'theone',
       dt00 = date '3005-12-31',
       tidf = time '13:00:00',
       tsdf = cast(current_date as timestamp),
       usrs = 'theone'
  where dt00 <= CURRENT_DATE and dt00 > date '2003-01-01';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,5)
    
    #stmt = """update a05table set usrs = '' where usr1 = '';"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_updated_msg(output,9)

    stmt = """select * from a05table order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    stmt = """alter table a05table add column dt01 DATE default CURRENT_DATE;;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a05table add ti01 TIME(1) default CURRENT_TIME;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table a05table add column ts01 TIMESTAMP(1) default CURRENT_TIMESTAMP;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a05table add usr2 VARCHAR(18) default 'me';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a05table where int1 < 2 or int1 >= 15 order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s91')
    
    stmt = """select usr1, usrs, dt01, ti01, ts01, usr2 from a05table
  where int1 > 15 order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s92')
    
    stmt = """select * from a05table order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    # $SQL_complete_msg
    # dup a05table to a5itable;
    # create table a5itable like a05table;
    stmt = """create table a5itable (
    int1 integer no default not null
  , vch2 CHAR (8)
  , dt00 date
  , tidf time default current_time
  , usr0 varchar(20) default ''
  , tsdf timestamp default current_timestamp
  , ts00 timestamp(0) default current_timestamp
  , usr1 char(18) default ''
  , usrs varchar(20) default ''
  , dt01 date default current_date
  , ti01 time(1) default current_time
  , ts01 timestamp(1) default current_timestamp
  , usr2 varchar(18) default 'me'
  , primary key (int1 asc) not droppable
)
store by primary key
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a5itable select * from a05table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,16)
    
    stmt = """select * from a5itable order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    stmt = """alter table a5itable add column vch3 varchar (8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a5itable add ti02 TIME(2) default time '11:59:59.59';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a5itable order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')

    stmt = """insert into a5itable (int1, dt01, usr2) values
  (20, date '2005-03-31', 'DBA');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
        
    stmt = """insert into a5itable values
  (21, 'row_21', CURRENT_DATE, CURRENT_TIME, '',
       CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'user1', 'users', 
       date '2999-01-21', time '21:00:00.0',  
       timestamp '2006-01-21:01:21:00.0',
       'user2', 'vch3', CURRENT_TIME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
        
    stmt = """insert into a5itable (int1, ti01, ti02, ts01) values 
  (22, time '03:33:00.1', time '03:33:00.12', 
       timestamp '3003-03-21:03:33:00.1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
        
    stmt = """select ti02, ti01, ti02, ts01 from a5itable where int1 > 15 order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,4)
    
    stmt = """select int1, vch3, dt01, ti01, ts01, usr2 from a5itable order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    
    stmt = """delete from a5itable where ti02 < time '11:00:00' and vch3 is NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """select dt01, ti01, ts01, usr2 from a5itable where
       dt01 = date '0001-01-01' and ti01 = time '12:00:00' and
       ts01 = timestamp '0001-01-01:12:00:00' and
       usr2 = 'me' and int1 < 10 order by int1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from a5itable where 
       dt01 = date '0001-01-01' and ti01 = time '12:00:00' and
       ts01 = timestamp '0001-01-01:12:00:00' and
       usr2 = 'me' and int1 < 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,9)

    # $SQL_deleted_msg 3
    # delete from a5itable where dt00 is NULL and usrs = '';

    # #expectfile $test_dir/a05exp a05s13
    # select int1, vch2, dt00, ts00, tidf, tsdf from a5itable order by int1;

    # #expectfile $test_dir/a05exp a05s14
    # select int1, dt01, ti01, ts01, ti02 from a5itable order by int1;

    # #expectfile $test_dir/a05exp a05s15
    # select int1, usr0, usr1, usr2, usrs, vch3 from a5itable order by int1;

    _testmgr.testcase_end(desc)

    # -------------------------------------------------------------------
    #testcase a06 a06 add columns: time, date, timestamp, interval
    # -------------------------------------------------------------------
    # Simple add columne test
    # Exercise DATE, TIME, TIMESTAMP, INTERVAL and variable length columns
    # Table starts with fixed columns
    # Add fixed columns and variable columns in sequence
    # -------------------------------------------------------------------
def test006(desc="""add columns: time, date, timestamp, interval"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop view a6_view1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view a6_view2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a06table;"""
    output = _dci.cmdexec(stmt)
    
    # # table start with 2 fixed length field
    stmt = """create table a06table (
    orders varchar(3) not null
  , dt00 DATE 
  , ti00 TIME default TIME '11:11:11'
  , ts00 TIMESTAMP(2) 
  , primary key (orders asc) not droppable
)
store by primary key
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # insert couple rows 
    # row 1 and 2
    stmt = """insert into a06table (orders) values ('1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a06table values ('2', DATE '2001-01-02', 
         TIME '12:34:56', TIMESTAMP '2001-01-02:12:34:56');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """select * from a06table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    # -------------------------------------------------------------------
    # add column 5: s12_2 INTERVAL SECOND(12,2);
    # -------------------------------------------------------------------
    stmt = """alter table a06table add column s12_2 INTERVAL SECOND(12,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # row 3 and 4
    stmt = """insert into a06table (orders, dt00) values ('3', date '2005-01-01'); """
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a06table (orders, s12_2) 
  values ('4', interval - '10.0' second(12,2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # -------------------------------------------------------------------
    # add column 6: yr4 INTERVAL YEAR(4) 
    # -------------------------------------------------------------------

    stmt = """alter table a06table add yr4 interval year(4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # add row 5, 6 and 7
    stmt = """insert into a06table values 
  ('5', date '2005-01-01', time '15:00:00', timestamp '2005-01-01:15:00:00',
   interval '5.5' second(12,2), interval '1005' year(4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a06table values 
  ('6', date '2006-01-01', time '16:00:00', timestamp '2006-01-01:16:00:00',
   interval '6000.55' second(12,2), interval '1006' year(4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a06table (orders, ti00, s12_2)values 
  ('7', time '17:00:00', interval '7000.55' second(12,2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    # -------------------------------------------------------------------
    #  add column 7: mo00 INTERVAL MONTH default interval '0' month
    # -------------------------------------------------------------------
    stmt = """alter table a06table add mo00 INTERVAL month default interval '0' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a06table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    # row 8 and 9
    stmt = """insert into a06table (orders, s12_2, yr4) values 
  ('8', interval '7.2' second(12,2), interval '1717' year(4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a06table values 
  ('9', date '2006-09-09', time '19:00:00', timestamp '2009-01-01:19:00:00',
   interval '9000.55' second(12,2), interval '1009' year(4),
   interval '29' month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a06table order by orders;"""
    output = _dci.cmdexec(stmt)
    # -------------------------------------------------------------------
    # add column 8: vchar8 VARCHAR(8) default 'interval'
    # -------------------------------------------------------------------
    stmt = """alter table a06table add column vchar8 VARCHAR(8) default 'interval';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a06table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    #  insert row 9, 10, and 11
    stmt = """insert into a06table (orders, mo00) values ('10', interval + '10' month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a06table values 
  ('11', date '2006-10-10', time '10:10:00', timestamp '2009-10-10:10:10:10',
   interval '10.10' second(12,2), interval + '10' year(4),
   interval - '2' month, 'row_11');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a06table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    # -------------------------------------------------------------------
    # add column 9: day18 INTERVAL day(18)
    # -------------------------------------------------------------------
    stmt = """alter table a06table add day18 INTERVAL day(18);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # row 12 & 13
    stmt = """insert into a06table (orders, dt00, ts00, s12_2, mo00 ) values 
  ('12', date '1996-01-31', timestamp '1996-01-31:12:12:12',
       interval '1212.12' second(12,2), interval '12' month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a06table values
  ('13', date '2006-10-13', time '13:13:03', timestamp '2003-10-13:13:10:10',
   interval '13.13' second(12,2), interval + '13' year(4),
   interval + '2' month, 'row_13',interval '13' day);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """update a06table set day18 = interval '18888' day(18) where yr4 is null;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update a06table set dt00 = current_date, ts00 = current_timestamp 
   where s12_2 = interval - '10.00' second(12,2)
      or s12_2 = interval '10.10' second(12,2); """
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from a06table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    # -------------------------------------------------------------------
    # add column 10: mo_mo interval month to month
    # -------------------------------------------------------------------
    stmt = """alter table a06table add mo_mo interval month to month 
  default interval '11' month to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # -------------------------------------------------------------------
    # add column 11: d07_s5 interval day(7) to second(5)
    # -------------------------------------------------------------------
    stmt = """alter table a06table add d07_s5 interval day(7) to second(5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # -------------------------------------------------------------------
    #  add column 12: h08_s0 interval hour(8) to second(0)
    # -------------------------------------------------------------------
    stmt = """alter table a06table add h08_s0 interval hour(8) to second(0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # -------------------------------------------------------------------
    # add column 13: m10_s interval minute(10) to second
    # -------------------------------------------------------------------
    stmt = """alter table a06table add m10_s interval minute(10) to second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view a6_view1 as select
  orders, s12_2, mo_mo, h08_s0, vchar8 from a06table 
   where orders >= '10';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select count(*) from a6_view1;"""
    output = _dci.cmdexec(stmt)
    #_dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6v1')

    # -------------------------------------------------------------------
    #  add column 14: y11_m interval year(11) to month
    # -------------------------------------------------------------------
    stmt = """alter table a06table add y11_m interval year(11) to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a06table (orders,y11_m) values 
  ('20', interval '1414-01' year(11) to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # -------------------------------------------------------------------
    # add column 15: s5f1 interval second(5,1)
    # -------------------------------------------------------------------
    stmt = """alter table a06table add s5f1 interval second(5,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a06table (orders, s12_2, y11_m) values
  ('21', interval '2121.21' second(12,2), 
         interval '100000-11' year(11) to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # -------------------------------------------------------------------
    #  add column 16: h02_s6 interval hour(2) to second(6)
    # -------------------------------------------------------------------
    stmt = """alter table a06table add h02_s6 interval hour(2) to second(6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a06table (orders, s5f1, m10_s,vchar8) values 
  ('22', interval '55555.5' second(5,1),
         interval '55555:55.123456' minute(10) to second, 'R22');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a06table (orders, s5f1, h02_s6,vchar8) values 
  ('23', interval '23232.3' second(5,1), 
       interval '23:23:23.123456' hour(2) to second(6), 'R23');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """select * from a06table order by orders;"""
    output = _dci.cmdexec(stmt)
    # -------------------------------------------------------------------
    #  add column 13: vchar3 VARCHAR(3) 
    # -------------------------------------------------------------------
    stmt = """alter table a06table add vchar3 VARCHAR(3) upshift;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a06table order by orders;"""
    output = _dci.cmdexec(stmt)

    stmt = """update a06table set s5f1 = interval '12345.0' second(5,1) where orders < '10';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view a6_view2 as select
  orders, yr4, y11_m, h02_s6, vchar3 from a06table
   where orders >= '10' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from a6_view1 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6v1')

    stmt = """select * from a6_view2 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6v2')
    
    # insert no added columns
    stmt = """insert into a06table (orders, ti00, s12_2, mo00, vchar8) values
  ('14', time '14:14:00', interval '14.14' second(12,2), 
       interval '14' month, 'row_14');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # insert some added columns
    stmt = """insert into a06table (orders, s12_2, d07_s5, s5f1, mo00) values
  ('15', interval '15.15' second(12,2), 
       interval '7:07:07:07.12345' day(7) to second(5),
       interval '5.1' second(5,1), interval '15' month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a06table (orders, s12_2, m10_s, y11_m, vchar3, mo00) values
  ('16', interval '16.16' second(12,2), 
       interval '16:16.123456' minute(10) to second,
       interval '1616-06' year(11) to month, 'r16', interval '16' month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    #  insert full row
    stmt = """insert into a06table values 
  ('17', date '1991-07-31', time '17:30:30', 
       timestamp '1991-07-31:17:30:30', 
       interval '17.17' second(12,2),
       interval '17' year(4),
       interval '17' month, 'row_17',
       interval '170000' day(18),
       interval '17' month to month,
       interval '1700000:17:17:17.12345' day(7) to second(5),
       interval '17:17:17' hour(8) to second(0),
       interval '1700000000:17.123456' minute(10) to second,
       interval '1700000-11' year(11) to month,
       interval '17000.7' second(5,1),
       interval '17:17:17.123456' hour(2) to second(6), 'r17');"""
    output = _dci.cmdexec(stmt)

    stmt = """select * from a06table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')

    stmt = """delete from a06table where s12_2 < interval '10.00' second(12,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,3)
    
    stmt = """delete from a06table where y11_m is NULL and orders <= '5';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,11)
    
    stmt = """select * from a06table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')

    stmt = """select * from a6_view2 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')

    _testmgr.testcase_end(desc)
    
# -------------------------------------------------------------------
#testcase a07 a07 more on time, date, timestamp, and interval
# -------------------------------------------------------------------
# Exercise DATE, TIME, TIMESTAMP, INTERVAL and variable length columns
# Table starts with fixed columns
# Add fixed columns and variable columns in sequence
# -------------------------------------------------------------------
def test007(desc="""a07 more on time, date, timestamp, and interval"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table a07table;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view a7_view2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a07table;"""
    output = _dci.cmdexec(stmt)
    
    ## table start with 2 fixed length field
    stmt = """create table a07table (
    orders int not null
  , dt00 DATE 
  , ti00 TIME default TIME '11:11:11'
  , ts00 TIMESTAMP(2) 
  , usr0 varchar(13) default 'leo'
  , primary key (orders asc) not droppable
)
store by primary key
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # insert couple rows 
    # row 1 and 2
    stmt = """insert into a07table (orders) values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a07table (orders, dt00, ti00, ts00)
   values (2, DATE '2001-01-02', 
         TIME '12:34:56', TIMESTAMP '2001-01-02:12:34:56');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """select * from a07table order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    # -------------------------------------------------------------------
    # add column 5: s12_2 INTERVAL SECOND(12,2);
    # -------------------------------------------------------------------
    stmt = """alter table a07table add column s12_2 INTERVAL SECOND(12,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # row 3 and 4
    stmt = """insert into a07table (orders, dt00) values (3, date '2005-01-01'); """
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a07table (orders, s12_2) values (4, interval - '10.0' second(12,2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    # -------------------------------------------------------------------
    # add column 6: yr4 INTERVAL YEAR(4) 
    # -------------------------------------------------------------------
    stmt = """alter table a07table add yr4 interval year(4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a07table values 
  (5, date '2005-01-01', time '15:00:00', timestamp '2005-01-01:15:00:00',
   'HPQ.DBAdmin', interval '5.5' second(12,2), interval '1005' year(4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a07table values 
  (6, date '2006-01-01', time '16:00:00', timestamp '2006-01-01:16:00:00',
   'HPQ.TEG', interval '6000.55' second(12,2), interval '1006' year(4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a07table (orders, ti00, s12_2)values 
  (7, time '17:00:00', interval '7000.55' second(12,2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # -------------------------------------------------------------------
    # add column 7: mo00 INTERVAL MONTH default interval '0' month
    # -------------------------------------------------------------------
    stmt = """alter table a07table add mo00 INTERVAL month default interval '0' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from a07table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')

    #  row 7 and 8
    stmt = """insert into a07table (orders, s12_2, yr4) values 
  (8, interval '7.2' second(12,2), interval '1717' year(4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a07table values 
  (9, date '2006-09-09', time '19:00:00', timestamp '2009-01-01:19:00:00',
   'QADEV.SQLQA', interval '9000.55' second(12,2), interval '1009' year(4),
   interval '29' month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """select * from a07table order by orders;"""
    output = _dci.cmdexec(stmt)

    # -------------------------------------------------------------------
    # add column 8: vchar8 VARCHAR(8) default 'INTERVAL'
    # -------------------------------------------------------------------
    stmt = """alter table a07table add column vchar8 VARCHAR(8) default 'column_8'
  heading 'column_8';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a07table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')

    # insert row 9, 10, and 11
    stmt = """insert into a07table (orders, mo00) values (10, interval + '10' month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a07table values 
  (11, date '2006-10-10', time '10:10:00', timestamp '2009-10-10:10:10:10',
   'QADEV.TSANG', interval '10.10' second(12,2), interval + '10' year(4),
   interval - '2' month, 'row_11');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a07table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')

    # -------------------------------------------------------------------
    # add column 9: day18 INTERVAL day(18)
    # -------------------------------------------------------------------
    stmt = """alter table a07table add day18 INTERVAL day(18);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # row 12 & 13
    stmt = """insert into a07table (orders, dt00, ts00, s12_2, mo00 ) values 
  (12, date '1996-01-31', timestamp '1996-01-31:12:12:12',
       interval '1212.12' second(12,2), interval '12' month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a07table values
  (13, date '2006-10-13', time '13:13:03', timestamp '2003-10-13:13:10:10',
   'DBA', interval '13.13' second(12,2), interval + '13' year(4),
   interval + '2' month, 'row_13',interval '13' day);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from a07table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    # -------------------------------------------------------------------
    # add column 10: mo_mo interval month to month
    # -------------------------------------------------------------------
    stmt = """alter table a07table add mo_mo interval month to month 
  default interval '11' month to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # -------------------------------------------------------------------
    # add column 11: d07_s5 interval day(7) to second(5)
    # -------------------------------------------------------------------
    stmt = """alter table a07table add d07_s5 interval day(7) to second(5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # -------------------------------------------------------------------
    # add column 12: h08_s0 interval hour(8) to second(0)
    # -------------------------------------------------------------------
    stmt = """alter table a07table add h08_s0 interval hour(8) to second(0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # -------------------------------------------------------------------
    # add column 13: m10_s interval minute(10) to second
    # -------------------------------------------------------------------
    stmt = """alter table a07table add m10_s interval minute(10) to second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # -------------------------------------------------------------------
    # add column 14: y11_m interval year(11) to month
    # -------------------------------------------------------------------
    stmt = """alter table a07table add y11_m interval year(11) to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a07table (orders,y11_m) values 
  (20, interval '1414-01' year(11) to month);"""
    output = _dci.cmdexec(stmt)

    # -------------------------------------------------------------------
    # # add column 15: s5f1 interval second(5,1)
    # -------------------------------------------------------------------
    stmt = """alter table a07table add s5f1 interval second(5,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a07table (orders, s12_2, vchar8) values
  (21, interval '2121.21' second(12,2), 'R21');"""
    output = _dci.cmdexec(stmt)
    
    # -------------------------------------------------------------------
    # add column 16: h02_s6 interval hour(2) to second(6)
    # -------------------------------------------------------------------
    stmt = """alter table a07table add h02_s6 interval minute(10) to second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a07table (orders, vchar8, s5f1) values 
  (22, 'R22', interval '55555.5' second(5,1));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a07table (orders, s5f1, h02_s6) values 
  (23, interval '23232.3' second(5,1), 
       interval '23:23:23.123456' hour(2) to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """select * from a07table order by orders;"""
    output = _dci.cmdexec(stmt)
     
    # -------------------------------------------------------------------
    # add column 13: vchar3 VARCHAR(3) 
    # -------------------------------------------------------------------
    stmt = """alter table a07table add vchar3 VARCHAR(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view a7_view1 as select
  orders, s12_2, mo_mo, h08_s0, vchar8 from a07table 
   where orders >= 5 and orders <= 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view a7_view2 as select
  orders, y11_m, h02_s6, vchar3 from a07table
   where orders >= 13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # insert no added columns
    stmt = """insert into a07table (orders, ti00, s12_2, mo00, vchar8) values
  (14, time '14:14:00', interval '14.14' second(12,2), 
       interval '14' month, 'row_14');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # insert some added columns
    stmt = """insert into a07table (orders, s12_2, d07_s5, s5f1, mo00) values
  (15, interval '15.15' second(12,2), 
       interval '7:07:07:07.12345' day(7) to second(5),
       interval '5.1' second(5,1), interval '15' month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a07table (orders, s12_2, m10_s, y11_m, vchar3, mo00) values
  (16, interval '16.16' second(12,2), 
       interval '16:16.123456' minute(10) to second,
       interval '1616-06' year(11) to month, 'R16', interval '16' month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # insert full row
    stmt = """insert into a07table values 
  (17, date '1991-07-31', time '17:30:30', 
       timestamp '1991-07-31:17:30:30', 
       '',
       interval '17.17' second(12,2),
       interval '17' year(4),
       interval '17' month, 'row_17',
       interval '170000' day(18),
       interval '17' month to month,
       interval '1700000:17:17:17.12345' day(7) to second(5),
       interval '17:17:17' hour(8) to second(0),
       interval '1700000000:17.123456' minute(10) to second,
       interval '1700000-11' year(11) to month,
       interval '17000.7' second(5,1),
       interval '17:17:17.123456' hour(2) to second(6), 'R17');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """select * from a07table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
   
    stmt = """select * from a7_view1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
   
    stmt = """select * from a7_view2 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')

    _testmgr.testcase_end(desc)

    # -------------------------------------------------------------------
    #testcase a08 a08 add various fixed and variable length columns
    # -------------------------------------------------------------------
    # Simple add columne test
    # Table starts with only fixed length columns
    # Add 7 fixed column and variable column in sequence
    # create table a08table like a08table
    # add 8 more columns to the table with various fixed and variable
    # length columns
    # -------------------------------------------------------------------
    # base table:
    # column 1: orders int
    # column 2: ch1   varchar(1)
    # add column:
    #   column 3: num1     numeric (9,2) unsigned
    #   column 4: vch1     varchar(1)
    #   column 5: sma1     smallint unsigned
    #   column 6: vch2     varchar(255)
    #   column 7: int1     int unsigned
    #   column 8: vch3     varchar(2)
    #   column 9: dec1     dec(9,2) unsigned
    # -------------------------------------------------------------------
def test008(desc="""a08 add various fixed and variable length columns"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """alter table a08table drop constraint int_uniq;"""
    output = _dci.cmdexec(stmt)
    stmt = """alter table a08table drop constraint int14_c;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a08table cascade;"""
    output = _dci.cmdexec(stmt)
    
    # table start with 2 fixed length field
    stmt = """create table a08table (
    orders int no default not null
  , ch1 varchar(1) 
  , primary key (orders ASC) not droppable
  )
  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a08table values (1,'a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)
    stmt = """insert into a08table values (2,'b');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)
    stmt = """insert into a08table values (3, 'c');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)

    # -------------------------------------------------------------------
    # add column 3: fixed length field, no default
    # -------------------------------------------------------------------
    stmt = """alter table a08table add column num1 NUMERIC (9,2) UNSIGNED 
  default null no heading;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a08table values (11,'k',1.01);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table (orders, ch1) values (12,'l');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table values (13,'m',2.02);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # expected 6 rows
    stmt = """select * from a08table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    # -------------------------------------------------------------------
    # add column 4: variable length field, default literal
    # -------------------------------------------------------------------
    stmt = """alter table a08table add vch1 char varying(1) heading '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # insert partial rows
    stmt = """insert into a08table values (15,'o',3.03,'A');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table (orders, ch1) values (16,'p');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table (orders, ch1, num1) values (17,'p',4.04);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table (orders) values (18);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # insert full rows
    stmt = """insert into a08table values (19,'q',5,'B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table values (20,'r',6.00,'C');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # 12 rows
    stmt = """select * from a08table order by orders;"""
    output = _dci.cmdexec(stmt)
    #_dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    
    # run some update tests (verify with selects after each update)
    # update an added column based on a key column values (unique fetch)
    # update an added column with the previous values
    # update a rnage of added columns
    # do some delete statements (verify with selected after delete)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update a08table set vch1 = '6' where num1 = 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,1)

    stmt = """update a08table set num1 = num1 * num1 where vch1 is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,9)

    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # -------------------------------------------------------------------
    # add column 5: fixed length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a08table add column sma1 SMALLINT UNSIGNED DEFAULT NULL
  heading 'SmallInt';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a08table (orders, sma1) values (51,21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table values (52,'S',5.01,'D',22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # -------------------------------------------------------------------
    # add column 6: variable length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a08table add vch2 CHARACTER VARYING(255);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a08table (orders, vch2) values (61,'character varying(255)');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table values (62,'V',5.02,'E',23,'variable length column');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table (orders, num1, sma1, vch2)
   values (63, 5.03, 24, 'variable length column vch2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """update a08table set sma1 = 99 where vch2 like '%vch2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """select orders, sma1, vch1, vch2 from a08table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    time.sleep(5)
    
    stmt = """select orders, sma1, vch1, vch2 from a08table order by orders
  for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    # -------------------------------------------------------------------
    # add column 7: fixed length field, default NULL
    # -------------------------------------------------------------------
    # physical order: orders, ch1, num1, sma1, int1, vch1, vch2
    stmt = """alter table a08table add column int1 int unsigned 
  constraint int_uniq check (int1 < 10000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a08table values 
  (71, 'I', 7.02, 'F', 700, 'VARCHAR', 100); """
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table (orders, int1) values (72,200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a08table (orders, vch2, int1) values (73,'VCH2', 300); """
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table (orders, vch1, sma1, int1) values (74, '2', 72, 400);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    # -------------------------------------------------------------------
    # add column 8: variable length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a08table add vch3 CHARACTER VARYING(2) heading 'VARYING(2)';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # add odd columns
    stmt = """insert into a08table (orders, num1, sma1, int1) 
  values (81,8.08,81,81);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table (orders, vch3) values (82,'AB');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # add even columns
    stmt = """insert into a08table (orders, ch1, vch1, vch2, vch3) 
   values (83,'8','8','vch2_83','83');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """update a08table set vch3 = 'CD' where ch1 = 'k';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """insert into a08table values
   (84,'8', 8.234, '8', 84, 
   'Bill and Joe ran softly near one of the hill. Some birds sprinted over Madelyn! Racoons and cats and blue birds. Oh My! Violet and Fred rushed sadly towards some door! Genelle and Janine split steadily across one of the string???',
    84, '83');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select orders, num1, vch3, int1 from a08table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s12')
    
    # -------------------------------------------------------------------
    ## add column 9: variable length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a08table add column dec1 DEC(9,2) UNSIGNED;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a08table values 
  (91,'9',9.1,'9',91,
  'EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE007P6RRT Mom sprinted beneath those worms??? A few horses got out beside Derek??? Those dogs ambled across dad??? An American and Ben leaped neatly over those string??? ',
  91, '91', 9.1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table (orders, dec1) values (92,9.20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select count(*) from a08table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output,'27')
    
    stmt = """select orders, vch2, int1 from a08table where ch1 is NULL and int1 > 300 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s13')
    
    stmt = """select orders, vch2, int1 from a08table where dec1 is NOT NULL order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s14')
    
    stmt = """select orders, vch3 from a08table where dec1 < 10 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s15')
    
    stmt = """select orders, int1, sma1, vch1, vch2, vch3 from a08table where vch3 = 'AB' order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s16')
    
    stmt = """update a08table set vch2 = 'VVCCHH2',
               vch3 = 'VV',
               sma1 = 65535,
               dec1 = 1234567.89
       where orders < 20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,11)
    
    stmt = """select avg(num1), sum(sma1), max(dec1) from a08table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s18')
    
    stmt = """delete from a08table where num1 = 7.02 and ch1 = 'I';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,1)
    
    #stmt = """delete from a08table where orders in (2,51,52,81,82,92);"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_deleted_msg(output,6)

    stmt = """select * from a08table where orders < 20 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s21')
    # -------------------------------------------------------------------
    # add column 10: fixed length field, default 
    # -------------------------------------------------------------------
    stmt = """alter table a08table add num10 NUMERIC (9,2) SIGNED default 7.2 
  heading 'num_10';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a08table (orders,num1) values (101,1.01);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table (orders,ch1,vch2,num10) 
  values (102,'A','VCH6',1.02);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    time.sleep
    
    # -------------------------------------------------------------------
    # add column 11: variable length field, default literal
    # -------------------------------------------------------------------
    stmt = """select * from a08table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,28)
    
    # run some different select statements
    # fetch rows based on key values (unique fetch)
    # vch3 didn't get updated. It was rollbacked.
    stmt = """select * from a08table where vch3 = 'EE' order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,0)
    
    # fetch a range of rows (subset fetch)
    stmt = """select * from a08table where num10 < 2.00 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s25')
    
    # run some update tests (verify with selects after each update)
    # update an added column based on a key column values (unique fetch)
    # update an added column with the previous values
    # update a rnage of added columns
    # do some delete statements (verify with selected after delete)
    stmt = """update a08table set num10 = num10 + 10.10,
                    vch3 = 'NN' where dec1 is NOT NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,13)

    stmt = """select orders, num10, vch3, dec1 from a08table order by orders;"""
    output = _dci.cmdexec(stmt)

    stmt = """alter table a08table add vch11 char varying(1) heading 'col11';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set param ?a02 '0';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?i02 0;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update a08table set vch11 = ?a02,
  num1 = ?i02, sma1 = ?i02, int1 = ?i02, dec1 = ?i02 where orders = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """select orders, vch11, num1, sma1, int1, dec1 from a08table where orders < 3 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s26')

    stmt = """select orders, vch3, num10, vch11, dec1 from a08table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s27')
    # -------------------------------------------------------------------
    # add column 12: fixed length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a08table add column sma12 SMALLINT SIGNED default -1
  check (sma12 < 65535 and sma12 > -100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a08table (orders, sma1, vch3) values (112,12,'12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table (orders, sma12) values (113, 113);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # -------------------------------------------------------------------
    # add column 13: variable length field, default NULL 
    # -------------------------------------------------------------------
    stmt = """alter table a08table add column vch13 CHARACTER VARYING(255) 
  default 'xxx';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a08table (orders, vch1, int1) values (114,'A',11400);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8101')

    stmt = """insert into a08table (orders, vch1, int1) values (114,'A',1140);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """update a08table set vch13 = vch2 where orders = 61;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """select orders, substring(vch13,1,10), substring(vch2,1,20) 
  from a08table where orders = 61 or orders <= 115 and orders >= 110
    order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s27a')
    
    # -------------------------------------------------------------------
    # add column 14: fixed length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a08table add column int14 int signed default -100 
  constraint int14_c check (int14 < 1234567890);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a08table values 
  (115, 'A', 7.02, 'A', 700, 'VARCHAR', 100,'VV',9.02,
   9.02,'Y', 1, 'COL_14_VCH13', 100); """
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table (orders, int1, vch11) values (116,116,'Z');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """update a08table set int14 = int14 - 1, sma12 = sma12 + 100 
  where orders < 50 or orders > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,19)

    stmt = """select orders, int14, sma12 from a08table where orders between 50 and 100 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,14)
    
    # -------------------------------------------------------------------
    # add column 15: variable length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a08table add column vch15 CHARACTER VARYING(2) default 'zz';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #add odd columns
    stmt = """insert into a08table (orders, num10, vch3, int14, ch1) 
  values (120,1.20,'V8',120, 'y');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    #add even columns
    stmt = """insert into a08table (orders, ch1, vch1, vch2, vch3, vch11) 
   values (121,'X','x','vch2_varchar255','xx','x');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a08table (orders,vch13) values (123,'the following are eligible for membership: non-profit organizations, educational institutions, market researchers, publishers, consultants, governments, and organizations and businesses who do not create, market or sell computer products or services.');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # MODE_0: $SQL_updated_msg 5
    # MODE_1: $SQL_updated_msg 6
    stmt = """update a08table set vch15 = 'CD' where ch1 in ('8','A','y');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s28a')
    
    stmt = """select orders, vch15, ch1 from a08table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s28')
    
    # -------------------------------------------------------------------
    # add column 16: variable length field, default NULL
    # -------------------------------------------------------------------
    stmt = """alter table a08table add column dec16 DEC(9,7) SIGNED default -9.99;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a08table values 
  (124,'B',12.4,'b',124,'VCH6_COL16',1240,'Bb',1.24,
   11.24,'b',1124,'VCH13_COL16',11240,'bB',12.1234567);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a08table (orders, dec16) values (125,-1.00001);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select orders, num1, vch3, sma12, vch15 from a08table where ch1 = '8' order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s29')
    
    stmt = """select orders, int1, sma1, vch11, vch13, vch15 from a08table where vch1 = 'x' order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s30')
    
    stmt = """update a08table set 
    ch1   = 'q',
    num1  = 1.23,
    vch1  = 'Q',
    vch2  = 'Such book shall be kept at the principal office of the Corporation and shall be subject to the rights of inspection required by law as set forth in Section 2.9 of these Bylaws. The Administrator shall be responsible for maintaining such book.',
    vch11 = 'q',
    sma1  = 123,
    vch13 = 'Such book shall be kept at the principal office of the Corporation and shall be subject to the rights of inspection required by law as set forth in Section 2.9 of these Bylaws. The Administrator shall be responsible for maintaining such book.',
    int14 = 123456789
  where orders = 123;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """select * from a08table where orders = 123 order by orders;"""
    output = _dci.cmdexec(stmt)
    time.sleep(5)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s31')

    # -------------------------------------------------------------------
    # add column 17: variable length field
    # -------------------------------------------------------------------
    stmt = """alter table a08table add column vch17 varchar(80) upshift default 'vch17'; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a08table (orders, dec1, num10, dec16, int1) 
  values (127, 12.7, 12.7, 12.7, 114400);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8101')

    stmt = """insert into a08table (orders, ch1, vch15, vch17) 
  values (128, 'J', 'jj', '12345678901234567890123456789012345678901234567890123456789012345678901234567890');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """update a08table set vch17 = 'vahalla' where orders < 110;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,28)
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    time.sleep(5)
    
    stmt = """select count(*) from a08table;"""
    output=_dci.cmdexec(stmt)
    _dci.expect_str_token(output, '38')
    
    stmt = """select orders, dec1, ch1, int1, vch15 from a08table where orders > 123 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s32')
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """delete from a08table where num1 is NULL
   and sma12 = -1 and int14 = -100 and orders > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,2)
    
    stmt = """update a08table set vch17 = 'denali' where orders > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,10)

    stmt = """select orders, sma12, int14, vch17 from a08table where orders > 100 order by orders;"""
    output = _dci.cmdexec(stmt)

    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    time.sleep(5)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """delete from a08table where orders < 100 and vch17 = 'VCH17';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,26)
    
    stmt = """insert into a08table (orders, vch17) values (1, 'row_1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a08table (orders, vch15) values (3, 'XP');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select orders, vch15, vch17 from a08table where orders < 5 order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s35')
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    time.sleep(5)
    
    stmt = """select orders, vch15, vch17 from a08table order by orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,38)
    
    # -------------------------------------------------------------------
    # add column 18: fix length field
    # -------------------------------------------------------------------
    stmt = """alter table a08table add ch18 char(512);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update a08table set vch17 = 'bryce',
                   ch18 = 'yellowstone' where num10 = 17.30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,13)

    # -------------------------------------------------------------------
    # add column 19: fix length field
    # -------------------------------------------------------------------
    stmt = """alter table a08table add column int19 int default 191919;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # -------------------------------------------------------------------
    # add column 20: variable length field
    # -------------------------------------------------------------------
    stmt = """alter table a08table add column vch20 varchar(1024);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update a08table set vch20 = 'shasta' 
  where vch2 = 'VVCCHH2' and ch18 = 'yellowstone';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,11)
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    time.sleep(5)
    
    stmt = """update a08table set vch20 = 'bigbend' where orders > 120;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,4)
    
    _testmgr.testcase_end(desc)
# -------------------------------------------------------------------
#testcase a09 a09 verify missing data after add variable column
# -------------------------------------------------------------------
def test009(desc="""a09 verify missing data after add variable column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table a09table;"""
    output = _dci.cmdexec(stmt)
    
    # table starts with fixed length columns only
    stmt = """create table a09table (
    int1 int no default not null
  , sma2 smallint default -1
  , vch2 varchar(3)
  , primary key (int1 asc) not droppable
  )
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a09table values (1,1,'1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # -------------------------------------------------------------------
   # add fixed length column, no default
    # -------------------------------------------------------------------
    stmt = """alter table a09table add column int3 int unsigned;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a09table values (2,2,'2',2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a09table (int1, sma2) values (3, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a09table values (4,4,'4',4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # -------------------------------------------------------------------
    # add fixed length column, default literal
    # -------------------------------------------------------------------
    stmt = """alter table a09table add column int4 int default 3000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # insert partial rows
    stmt = """insert into a09table (int1, int3) values (5,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a09table values (6,6,'6',6,6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    #stmt = """select * from a09table;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s02')

    # -------------------------------------------------------------------
    # add fixed length column, no default
    # -------------------------------------------------------------------
    stmt = """alter table a09table add lgt5 largeint;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a09table values (7,7,'7',7,7,7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a09table values (8,8,'8',8,8,8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a09table (int1, int4) values (9,9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a09table (int1, sma2, int3) values (10,10,10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # -------------------------------------------------------------------
    # add fixed length column, default literal
    # -------------------------------------------------------------------
    stmt = """alter table a09table add column num6 numeric(7,2) default 6000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a09table (int1, int3, int4) values (11,11,11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a09table values (12,12,'12',12,12,12,12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a09table (int1, sma2, lgt5) values (13,13,13);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a09table values (14,14,'14',14,14,14,14);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a09table (int1, lgt5, num6) values (15,15,15);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # -------------------------------------------------------------------
    # add fixed length column, default current_user
    # -------------------------------------------------------------------
    stmt = """alter table a09table add usr7 char(16) default '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a09table (int1, sma2, int4) values (16,16,16);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a09table (int1, int3, usr7) values (17,17,'usr17');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # -------------------------------------------------------------------
    # add fixed length column, default current_date
    # -------------------------------------------------------------------
    stmt = """alter table a09table add dt08 date default current_date;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a09table (int1, int4, num6) values (18,18,18);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a09table values (19,19,'19',19,19,19,19,'usr19',date '2000-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a09table (int1, int3, num6, usr7) values 
  (20,20,20,'usr20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # -------------------------------------------------------------------
    # add fixed length column, default current_time
    # -------------------------------------------------------------------
    stmt = """alter table a09table add ti09 time default current_time;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a09table (int1, int4, dt08) values
  (21,21,date '2021-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a09table values (22,22,'22',22,22,22,22,'usr22',
  date '2022-12-31', time '22:22:22');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # -------------------------------------------------------------------
    # add fixed length column, default current_time
    # -------------------------------------------------------------------
    stmt = """alter table a09table add ts10 timestamp default current_timestamp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a09table (int1, int4, usr7, dt08) values
  (23,23,'usr23', date '2023-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a09table values (24,24,'24',24,24,24,24,'usr24',
  date '2024-12-31', time '20:24:24', timestamp '2024-12-31:20:24:24');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
   
    # -------------------------------------------------------------------
    # add fixed length column, default current_time
    # -------------------------------------------------------------------
    stmt = """alter table a09table add vch11 varchar(1) default null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from a09table order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s04')
    
    stmt = """select * from a09table where int1 = 15 order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s05')

    stmt = """select * from a09table where int1 < 10 order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s06')

    stmt = """select * from a09table where int3 is null order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s07')
    
    stmt = """select * from a09table where lgt5 is not null order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s08')
    
    stmt = """update a09table set num6 = int1 where int1 =10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update a09table set usr7 = 'LEO',
                    ti09 = time '19:19:19' where int1 < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,4)
    
    stmt = """update a09table set dt08 = date '1999-12-31', 
                    ts10 = timestamp '1999-12-31:20:20:20'
   where int1 > 3 and int1 < 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,6)

    stmt = """update a09table set int4 = int4 + 2000,
                    num6 = num6 - 10000  where int1 = 15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
   
    stmt = """select int1, num6, usr7, ti09, dt08, int4 from a09table 
  where int1 <= 10 or int1 = 15 order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s10')
    
    stmt = """select * from a09table order by int1;"""
    output = _dci.cmdexec(stmt)

    stmt = """showddl a09table;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

# -------------------------------------------------------------------