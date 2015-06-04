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
    
def test001(desc="""Incompatible CHARSET causes tdm_arkcmp crash"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    _dci.showcontrol_showall_on() 
    stmt = """showcontrol default CHARSET;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_any_substr(output, """DEFAULT_CHARSET*ISO88591""")
    # Implicit conversion between charsets is no longer supported in Trafodion.
    # Now the default value needs to be specified as the same charset.
    # See LP BUG https://bugs.launchpad.net/bugs/1395890 for more details
    # stmt = """create table t1 (c1 int, c2 char(10) character set ucs2 default 'a') no partition;"""
    stmt = """create table t1 (c1 int, c2 char(10) character set ucs2 default _UCS2'a') no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Implicit conversion between charsets is no longer supported in Trafodion.
    # Now the default value needs to be specified as the same charset.
    # See LP BUG https://bugs.launchpad.net/bugs/1395890 for more details
    stmt = """create table t2 (c1 int, c2 char(10) character set ucs2 default _iso88591'a')
no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """create table t3 (c1 int, c2 char(10))
no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into t1 (c1) values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into t1 values (2, 'b');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into t1 values (3, _ucs2'c');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.exp""", """a1s1""")
    
    stmt = """insert into t3 values (3, _ucs2'c');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """select * from t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.exp""", """a1s3""")
    
    # cleanup
    _dci.showcontrol_showall_reset()
    # _dci.expect_complete_msg(output)
    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t3;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test002(desc="""NULL values were merged into other value interval"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table T01
(
col_id largeint not null primary key
,col_int int
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into T01(col_id)
select c1*10+c2
from (values(1)) T
transpose 0,1,2,3,4,5,6,7,8,9 as c1
transpose 0,1,2,3,4,5,6,7,8,9 as c2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 100)
    
    stmt = """update T01 set col_int=0  where col_id between 0 and 9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 10)
    stmt = """update T01 set col_int=1 where col_id between 10 and 19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 10)
    stmt = """update T01 set col_int=2 where col_id between 20 and 24;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    stmt = """update T01 set col_int=3 where col_id between 25 and 34;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 10)
    stmt = """update T01 set col_int=4 where col_id between 35 and 44;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 10)
    stmt = """update T01 set col_int=5 where col_id between 45 and 49;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    stmt = """update T01 set col_int=6 where col_id between 50 and 59;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 10)
    stmt = """update T01 set col_int=7 where col_id between 60 and 69;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 10)
    stmt = """update T01 set col_int=8 where col_id between 70 and 74;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    stmt = """update T01 set col_int=9 where col_id between 75 and 84;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 10)
    stmt = """update T01 set col_int=null where col_id between 85 and 99;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 15)
    stmt = """control query default USTAT_PROCESS_GAPS 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ustat_gap_percent '25.0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ustat_freq_size_percent '14.0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table T01 on col_int generate 4 intervals;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showstats for table T01 on col_int detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """15*1 (NULL)""")
    
    # cleanup
    stmt = """control query default USTAT_PROCESS_GAPS reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ustat_gap_percent reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ustat_freq_size_percent reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table T01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""Compiler picks ESP plan for very small table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # bugzilla 2192
    
    stmt = """CREATE TABLE tab_lineitem (L_ORDERKEY INTEGER NOT NULL NOT DROPPABLE,
L_PARTKEY INTEGER NOT NULL NOT DROPPABLE,
L_SUPPKEY INTEGER NOT NULL NOT DROPPABLE,
L_LINENUMBER INTEGER NOT NULL NOT DROPPABLE,
L_QUANTITY DECIMAL(15,2) NOT NULL NOT DROPPABLE,
L_EXTENDEDPRICE DECIMAL(15,2) NOT NULL NOT DROPPABLE,
L_DISCOUNT DECIMAL(15,2) NOT NULL NOT DROPPABLE,
L_TAX DECIMAL(15,2) NOT NULL NOT DROPPABLE,
L_RETURNFLAG CHAR(1) NOT NULL NOT DROPPABLE,
L_LINESTATUS CHAR(1) NOT NULL NOT DROPPABLE,
L_SHIPDATE DATE NOT NULL NOT DROPPABLE,
L_COMMITDATE DATE NOT NULL NOT DROPPABLE,
L_RECEIPTDATE DATE NOT NULL NOT DROPPABLE,
L_SHIPINSTRUCT CHAR(25) NOT NULL NOT DROPPABLE,
L_SHIPMODE CHAR(10) NOT NULL NOT DROPPABLE,
L_COMMENT VARCHAR(44) NOT NULL NOT DROPPABLE,
primary key (l_orderkey, l_linenumber) NOT DROPPABLE) number of partitions 2
store by primary key ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE tab_orders (O_ORDERKEY INTEGER NOT NULL NOT DROPPABLE,
O_CUSTKEY INTEGER NOT NULL NOT DROPPABLE,
O_tab_ordersTATUS CHAR(1) NOT NULL NOT DROPPABLE,
O_TOTALPRICE DECIMAL(15,2) NOT NULL NOT DROPPABLE,
O_ORDERDATE DATE NOT NULL NOT DROPPABLE,
O_ORDERPRIORITY CHAR(15) NOT NULL NOT DROPPABLE,
O_CLERK CHAR(15) NOT NULL NOT DROPPABLE,
O_SHIPPRIORITY INTEGER NOT NULL NOT DROPPABLE,
O_COMMENT VARCHAR(79) NOT NULL NOT DROPPABLE,
primary key (o_orderkey) NOT DROPPABLE) number of partitions 2
store by primary key ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tab_orders values
(193,331,'F',102889.64,date '1993-08-08','1-URGENT','Clerk-000000025',0,'C1ONm713zmnL363Qnki56xihj0gyRhLh3Q0C7jQ1njMC0i0N442PAC'),
(226,1411,'F',278333.63,date '1993-03-10','2-HIGH','Clerk-000000756',0,'g7C LNzwj34w5 LC7hM1m5CkSB7nMm0QyBxw6niy6R02MNSC4Q3n0Lx1xBNAgnLyhil50Ok4hL'),
(259,401,'F',185844.64,date '1993-09-29','4-NOT SPECIFIED','Clerk-000000601',0,'w3S1zl5 BjRNM5xN0Sn 6ii57LynimP2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """insert into tab_lineitem values (193,381,38,1,14,17939.32,0.06,0.03,'A','F',date '1993-10-30',date '1993-10-09',date '1993-11-11','COLLECT COD','MAIL','glzNC5L3NAR k l771A'),
(193,535,26, 2,37,53114.61,0.05,0.00, 'A','F',date '1993-08-14',date '1993-09-24',date '1993-09-08','TAKE BACK RETURN','TRUCK','n2Qzh24mNL12Mw'),
(1284,1855,42,2, 12,21082.20,0.01,0.02,'N','O',date '1996-02-23',date '1996-03-03',date '1996-03-11','DELIVER IN PERSON','MAIL','OSilkLgBkNSxL3 C13NCwS7h01yyRBBQPOl2Q');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """update statistics for table tab_orders on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table tab_lineitem on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select * from tab_orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    stmt = """select * from tab_lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """cqd query_cache '0';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare Q04BAD from SELECT o_orderkey FROM tab_orders
WHERE o_orderdate >= DATE '1993-07-01' AND o_orderdate < DATE '1993-10-01'
AND EXISTS (SELECT * FROM tab_lineitem WHERE l_orderkey = o_orderkey ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' Q04BAD;"""
    output = _dci.cmdexec(stmt)
    #explain Q04BAD;
    
    stmt = """select cast(SEQ_NUM as numeric(2)) as SEQ,
cast(RIGHT_CHILD_SEQ_NUM as numeric(2)) as R_IGHT,
cast(LEFT_CHILD_SEQ_NUM as numeric(2)) as L_EFT,
cast(OPERATOR as char(25)) as OPERATOR,
cast(TNAME as char(25)) as TNAME,
cast(cardinality as numeric(18,8)) as EST_ROWS
from TABLE (explain(NULL,'Q04BAD')) ;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """ESP_EXCHANGE""")
    
    stmt = """execute Q04BAD;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    # cleanup
    stmt = """drop table tab_orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tab_lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """cqd query_cache reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""mxcmp crashed on update at EncodedValue::constructorFunction"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table T_008_JAN (
empnum  numeric(4) unsigned not null not droppable,
sale    numeric(4) unsigned,
profit  numeric(3) unsigned,
bonus   numeric(4) unsigned,
entry_no int not null not droppable,
primary key(entry_no,empnum));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table T_008_FEB (
empnum  numeric(4) unsigned not null,
sale    numeric(4) unsigned,
profit  numeric(3) unsigned,
bonus   numeric(4) unsigned,
entry_no int not null,
primary key(entry_no,empnum));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table T_008_MAR (
empnum  numeric(4) unsigned not null,
sale    numeric(4) unsigned,
profit  numeric(3) unsigned,
bonus   numeric(4) unsigned,
entry_no int not null,
primary key(entry_no,empnum));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into T_008_JAN values
(1, 1000.00, 10, null,1), (3, 200.00, 20, 5,2), (5, 900.00, 40,10,3),
(5, 100.00, null, 10,4), (7, 50.00, 10, 20,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """insert into T_008_FEB values
(1, 100.00, 20, 20,1), (1, 200.00, 10, null,2), (3, null, null,null,3),
(5, 102.00, 10, null,4), (7, 150.00, 30, null,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """insert into T_008_MAR values
(1, 90.00, 10, 4,1), (3, 100.00, 20, 4,2), (3, 20.00, 20, 5,3),
(3, 100.00, 30, null,4), (5, 1.00, 50, 30,5), (5, 19.00, 20, 10,6),
(7, 80.00, 20, 10,7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    
    # on statement MJV on 3 tables
    stmt = """create materialized view T_008_MV1
refresh on statement
initialize on create
as
select T_008_Jan.empnum as empnum,
(T_008_Feb.bonus + T_008_Mar.bonus) as feb_mar_bonus,
(T_008_Jan.sale + T_008_Mar.sale) as jan_mar_sale,
(T_008_Jan.profit + T_008_Feb.profit + T_008_Mar.profit) as jan_feb_mar_profit,
T_008_Mar.sale as mar_sale
from T_008_Jan, T_008_Feb, T_008_Mar
where  T_008_Jan.empnum = T_008_Feb.empnum
and  T_008_Feb.empnum = T_008_Mar.empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '12112')
    _dci.expect_complete_msg(output)
    
    # update column 'bonus' in 't_008_feb' to null, which will
    # effect 'feb_mar_bonus'
    
    stmt = """prepare s1 from
update T_008_Feb
set bonus = null
where empnum = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    # cleanup
    stmt = """drop mv T_008_MV1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table T_008_JAN;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table T_008_FEB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table T_008_MAR;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""MVQR: MXCMP crash on DROP SCHEMA CASCADE when MVQR is ON"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #-------------------- set up section ----------------
    
    # stmt = """control query default MVQR_REWRITE_LEVEL '1';"""
    # output = _dci.cmdexec(stmt)
    # stmt = """control query default MVQR_REWRITE_ENABLED_OPTION 'ON';"""
    # output = _dci.cmdexec(stmt)
    # stmt = """control query default MVQR_PUBLISH_TO 'PRIVATE';"""
    # output = _dci.cmdexec(stmt)
    # stmt = """control query default REF_CONSTRAINT_NO_ACTION_LIKE_RESTRICT '1';"""
    # output = _dci.cmdexec(stmt)
    # stmt = """control query default MVQR_ALL_JBBS_IN_QD 'ON';"""
    # output = _dci.cmdexec(stmt)
    # stmt = """control query default MVQR_USE_EXTRA_HUB_TABLES 'ON';"""
    # output = _dci.cmdexec(stmt)
    # stmt = """cqd HIDE_INDEXES 'ALL';"""
    # output = _dci.cmdexec(stmt)
    
    stmt = """prepare checkPlan from
select operator, tname
from table(explain(NULL, 'QUERYSTMT'))
where operator like '%_SCAN%'
order by tname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """create table fact (
fday   int,
fmonth int,
fyear  int,
fitem  int,
fquant int,
fprice numeric (8,2),
dimkey int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table fact2 (
qitem  int,
qquant int,
qprice numeric (8,2),
qdimkey int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table dim1 (dkey int not null not droppable primary key, dimdata int, fk1 int)
store by primary key no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table dim2 (dkey int not null not droppable primary key, dimdata int, fk1 int)
store by primary key no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table dim3 (dkey int not null not droppable primary key, dimdata int, fk1 int)
store by primary key no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table fact  add constraint fact1_fk foreign key (dimkey) references dim1(dkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table fact2 add constraint fact2_fk foreign key (qdimkey) references dim1(dkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table dim1  add constraint dim1_fk foreign key (fk1) references dim2(dkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table dim2  add constraint dim2_fk foreign key (fk1) references dim3(dkey);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create mv outputs_mjv1
refresh on request
initialized on create
as  select fprice, fquant,
fday oday, fmonth omonth, fyear oyear,
dimkey
from fact;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Hub table + extra-hub table.
    
    stmt = """create mv outputs_mjv2
refresh on request
initialized on create
as  select fprice, fquant,
dimkey, dimdata,
fday oday, fmonth omonth, fyear oyear
from fact, dim1
where dimkey=dkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # 3 cascaded dimension tables
    
    stmt = """create mv outputs_mjv3
refresh on request
initialized on create
as  select fprice, fquant,
dimkey, dim3.dimdata
from fact, dim1, dim2, dim3
where dimkey=dim1.dkey
and dim1.fk1=dim2.dkey
and dim2.fk1=dim3.dkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Two hub + one extra-hub
    stmt = """create mv outputs_mjv4
refresh on request
initialized on create
as  select fprice, fquant,
qprice,
qdimkey, dimdata
from fact f1, fact2 f2, dim1
where dimkey=dkey
and fitem=qitem
and qdimkey=dkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #****************************************
    # MAVs
    #****************************************
    stmt = """create mv outputs_mav1
refresh on request
initialized on create
as  select sum(fprice*fquant) total_price,
sum(dimdata) sumdata,
fday oday, fmonth omonth, fyear oyear
from fact, dim1
where dimkey=dkey
group by fday, fmonth, fyear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create mv outputs_mav2
refresh on request
initialized on create
as  select sum(fprice*fquant) total_price,
sum(dimdata) sumdata,
fmonth omonth, fyear oyear
from fact, dim1
where dimkey=dkey
group by fmonth, fyear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create mv outputs_mav3
refresh on request
initialized on create
as  select sum(fprice*fquant) total_price,
sum(dimdata) sumdata,
fyear oyear
from fact, dim1
where dimkey=dkey
group by fyear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create mv outputs_mav4
refresh on request
initialized on create
as  select count(*)                 countstar,
count(dimdata)           count_d,
--count(distinct dimdata)  count_dis_d,
sum(dimdata)             sum_d,
--sum(distinct dimdata)    sum_dis_d,
min(dimdata)             min_d,
max(dimdata)             max_d,
stddev(dimdata)          stddev_d,
stddev(dimdata, fyear)   stddev_dy,
stddev(dimdata, fmonth)  stddev_dm,
variance(dimdata)        variance_d,
sum(dimdata*dimdata)     sum_dd,
fyear                    oyear,
fmonth                   omonth
from fact, dim1
where dimkey=dkey
group by fyear, fmonth;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create mv outputs_mav5
refresh on request
initialized on create
as  select count(*)                 countstar,
count(dimdata)           count_d,
sum(dimdata)             sum_d,
min(dimdata)             min_d,
max(dimdata)             max_d,
stddev(dimdata)          stddev_d,
stddev(dimdata, fyear)   stddev_dy,
stddev(dimdata, fmonth)  stddev_dm,
variance(dimdata)        variance_d,
sum(dimdata*dimdata)     sum_dd,
fyear                    oyear
from fact, dim1
where dimkey=dkey
group by fyear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #*****************************************
    # Simple join query
    #*****************************************
    
    stmt = """prepare QueryStmt from
select fprice*fquant total_price,
dimkey, dimdata,
fday oday, fmonth omonth, fyear oyear
from fact, dim1
where dimkey=dkey
order by dimkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # Verify the MV is picked by the optimizer.
    stmt = """prepare QueryStmt from
select fprice*fquant total_price,
dimkey, dimdata,
fday oday, fmonth omonth, fyear oyear
from fact, dim1
where dimkey=dkey
order by dimkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #******************************************
    # Check Rollup over an MV grouping column.
    #******************************************
    stmt = """create table Table1 (
a int not null
, b int
, c int
, d int
, e int
, primary key(a)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into Table1 values
(1,0,1,1,1)
,(2,1,1,1,2)
,(3,1,1,1,3)
,(6,1,2,2,6)
,(7,1,2,1,7)
,(8,1,2,1,8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    
    # Insert some rows with NULL values.
    stmt = """insert into Table1(a,b,d,e) values
(4,0,  2,4)
,(5,0,  2,5)
,(9,1,  1,9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """select t1.b, t1.c, count(*) countstar
from Table1 t1
where t1.a>0
group by t1.b,t1.c ;"""
    output = _dci.cmdexec(stmt)
    
    # An incremental MV will have a system added COUNT(*) column.
    stmt = """create mv MAVwithCountStar
REFRESH ON REQUEST
INITIALIZE ON CREATE
ENABLE QUERY REWRITE
as select t1.b,
t1.c,
sum(t1.e) sum_e
from Table1 t1
where t1.a>0
group by t1.b,t1.c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Lets look at the data in the MV
    stmt = """select *, SYS_COUNTSTAR1
from MAVwithCountStar;"""
    output = _dci.cmdexec(stmt)
    
    # A recompute MV will not have it.
    stmt = """create mv MAVwithoutCountStar
RECOMPUTE
INITIALIZE ON CREATE
ENABLE QUERY REWRITE
as select t1.b,
t1.c,
sum(t1.e) sum_e
from Table1 t1
where t1.a>0
group by t1.b,t1.c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare QueryStmt from
select t1.b,
count(*)             countstar,
count(t1.c)          count_c,
sum(t1.c)            sum_c,
count(distinct t1.c) count_d_c,
sum(distinct t1.c)   sum_d_c,
max(c)               max_c,
--sum(t1.c + 5)        sum_cplus5,
--sum(t1.c * t1.c)     sum_csquare
t1.b + sum(t1.e)     sume_plus_b
from Table1 t1
where t1.a>0
group by t1.b
order by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """create table aq7_t1 (
pk int not null not droppable,
weekday int,
primary key (pk))
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table aq7_t2 (
a int not null not droppable,
b int,
primary key (a))
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create mv aq7_mv1
REFRESH BY USER INITIALIZE BY USER ENABLE QUERY REWRITE
as  select (case weekday
when 1 then 'Sunday'
when 2 then 'Monday'
when 3 then 'Tuesday'
when 4 then 'Wednesday'
when 5 then 'Thursday'
when 6 then 'Friday'
when 7 then 'Saturday'
end) day_name,
count(*) count_star,
sum(b) sum_b
from aq7_t1, aq7_t2
where weekday = a
group by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop mv outputs_mjv1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop mv outputs_mjv2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop mv outputs_mjv3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop mv outputs_mjv4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop mv outputs_mav1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop mv outputs_mav2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop mv outputs_mav3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop mv outputs_mav4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop mv outputs_mav5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop mv MAVwithCountStar;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop mv MAVwithoutCountStar;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop mv aq7_mv1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table fact;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table fact2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table dim1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table dim2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table dim3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table aq7_t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table aq7_t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # cleanup
    # stmt = """control query default MVQR_REWRITE_CANDIDATES reset;"""
    # output = _dci.cmdexec(stmt)
    # stmt = """control query default MVQR_REWRITE_LEVEL reset;"""
    # output = _dci.cmdexec(stmt)
    # stmt = """control query default MVQR_REWRITE_ENABLED_OPTION reset;"""
    # output = _dci.cmdexec(stmt)
    # stmt = """control query default MVQR_PUBLISH_TO reset;"""
    # output = _dci.cmdexec(stmt)
    # stmt = """control query default REF_CONSTRAINT_NO_ACTION_LIKE_RESTRICT reset;"""
    # output = _dci.cmdexec(stmt)
    # stmt = """control query default MVQR_ALL_JBBS_IN_QD reset;"""
    # output = _dci.cmdexec(stmt)
    # stmt = """control query default MVQR_USE_EXTRA_HUB_TABLES reset;"""
    # output = _dci.cmdexec(stmt)
    # stmt = """control query default HIDE_INDEXES reset;"""
    # output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

