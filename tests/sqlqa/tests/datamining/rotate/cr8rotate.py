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
    
def test001(desc="""cr8rotate"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # cr8tbls.sql
    # jclear
    # 25 Apr 1997
    # setup for the transpose tests
    #
    # create catalog;
    
    # Tests 1 - 9
    
    stmt = """create table table1 (
a int ,
b int,
yn char (1),
cnt int not null primary key
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into table1 values (1, 5, 'y', 1);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1 values (1, 10, 'n',2);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1 values (2, 5, 'n', 3);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1 values (2, 10, 'y',4);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table1 values (2, 10, 'n',5);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table table2 (
a int not null primary key,
b int,
c int,
d char (2),
e char (2),
f char (2)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into table2 values (
1, 10, 100, 'd1', 'e1', 'f1'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into table2 values (
2, 20, 200, 'd2', 'e2', 'f2'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from table2;"""
    output = _dci.cmdexec(stmt)
    
    # Tests 11 - 19
    
    stmt = """create table intsimpl (
lname char(6) not null primary key,
a int,
b int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into intsimpl values ('Smith', 1, 10);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intsimpl values ('Brown', 2, 20);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table smalsimp (
lname char(6) not null primary key,
a smallint,
b smallint
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into smalsimp values ('Smith', 1, 10);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalsimp values ('Brown', 2, 20);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table intxtab (
lname char (6),
num   int,
bread int,
milk  int,
fruit int,
cnt int not null primary key
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into intxtab values ('Smith', 1, 5, 2, 4, 1);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Green', 2, 4, 3, 0, 2);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Tiger', 3, 2, 0, 0, 3);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Brown', 4, 5, 2, 1, 4);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Jones', 5, 1, 1, 2, 5);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Tiger', 3, 2, 3, 1, 6);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Jones', 5, 1, 5, 0, 7);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Smith', 1, 1, 1, 5, 8);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Brown', 4, 1, 5, 0, 9);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Jones', 5, 5, 4, 2, 10);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Green', 2, 2, 3, 4, 11);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Tiger', 3, 1, 5, 1, 12);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Green', 2, 1, 1, 5, 13);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Tiger', 3, 1, 5, 4, 14);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Green', 2, 5, 4, 5, 15);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Jones', 5, 5, 0, 4, 16);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Tiger', 3, 2, 5, 1, 17);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Green', 2, 4, 1, 5, 18);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Jones', 5, 1, 3, 4, 19);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Tiger', 3, 1, 2, 5, 20);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Green', 2, 1, 3, 4, 21);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Brown', 4, 5, 0, 1, 22);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Smith', 1, 1, 0, 5, 23);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Brown', 4, 2, 2, 4, 24);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Tiger', 3, 5, 1, 5, 25);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into intxtab values ('Smith', 1, 2, 1, 4, 26);"""
    output = _dci.cmdexec(stmt)
    
    # Tests 21 - 29
    
    stmt = """create table smalxtab (
lname char (6),
num   smallint,
bread smallint,
milk  smallint,
fruit smallint,
cnt int not null primary key
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into smalxtab values ('Smith', 1, 5, 2, 4, 1);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Green', 2, 4, 3, 0, 2);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Tiger', 3, 2, 0, 0, 3);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Brown', 4, 5, 2, 1, 4);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Jones', 5, 1, 1, 2, 5);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Tiger', 3, 2, 3, 1, 6);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Jones', 5, 1, 5, 0, 7);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Smith', 1, 1, 1, 5, 8);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Brown', 4, 1, 5, 0, 9);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Jones', 5, 5, 4, 2, 10);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Green', 2, 2, 3, 4, 11);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Tiger', 3, 1, 5, 1, 12);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Green', 2, 1, 1, 5, 13);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Tiger', 3, 1, 5, 4, 14);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Green', 2, 5, 4, 5, 15);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Jones', 5, 5, 0, 4, 16);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Tiger', 3, 2, 5, 1, 17);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Green', 2, 4, 1, 5, 18);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Jones', 5, 1, 3, 4, 19);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Tiger', 3, 1, 2, 5, 20);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Green', 2, 1, 3, 4, 21);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Brown', 4, 5, 0, 1, 22);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Smith', 1, 1, 0, 5, 23);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Brown', 4, 2, 2, 4, 24);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Tiger', 3, 5, 1, 5, 25);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into smalxtab values ('Smith', 1, 2, 1, 4, 26);"""
    output = _dci.cmdexec(stmt)
    
    # Tests 31 - 39
    
    stmt = """create table flotsimp (
num float (6),
a   float (6),
b   float (6),
cnt int not null primary key
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table realsimp (
num real  ,
a   real,
b   real,
cnt int not null primary key
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table dblsimp (
num double precision ,
a   double precision,
b   double precision,
cnt int not null primary key
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into flotsimp values (1.1e0, 11.11e0, 111.111e0, 1);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotsimp values (2.2e0, 22.22e0, 222.222e0, 2);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into realsimp select * from flotsimp;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into dblsimp select * from flotsimp;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from flotsimp;"""
    output = _dci.cmdexec(stmt)
    # expect a count of 2
    
    stmt = """select count (*) from realsimp;"""
    output = _dci.cmdexec(stmt)
    # expect a count of 2
    
    stmt = """select count (*) from dblsimp;"""
    output = _dci.cmdexec(stmt)
    # expect a count of 2
    
    stmt = """create table flotxtab (
num float (6) ,
a   float (12),
b   float (12),
c   float (12),
d   float (12),
cnt int not null primary key
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table realxtab (
num real,
a   real,
b   real,
c   real,
d   real,
cnt int not null primary key
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table dblxtab (
num double precision,
a   double precision,
b   double precision,
c   double precision,
d   double precision,
cnt int not null primary key
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into flotxtab values (
1.0e0, 15331.100e0, 888.209e0, 20869.8224e0, 9435.1966e0,1 );"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
2.0e0, 12103.29258e0, 28937.3043e0, 19749.28565e0, 17664.16204e0,2);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
3.0e0, 15916.26966e0, 2896.5012e0, 31117.8494e0, 28112.12025e0, 3);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
4.0e0, 14832.1002e0, 20366.7759e0, 26378.2983e0, 8972.26696e0, 4);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
5.0e0, 15730.3386e0, 28841.26098e0, 10416.29903e0, 8541.1153e0, 5);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
6.0e0, 919.13775e0, 25001.21583e0, 13014.29192e0, 12494.2337e0, 6);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
7.0e0, 19913.7176e0, 28734.20396e0, 18837.6345e0, 1872.7256e0, 7);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
8.0e0, 23155.9364e0, 28471.22339e0, 32588.32543e0, 15157.2441e0, 8);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
9.0e0, 27527.8953e0, 28940.28611e0, 17183.3111e0, 17846.5581e0,9);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
10.0e0, 23800.21008e0, 4693.24525e0, 32627.6294e0, 5485.9328e0, 10);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
11.0e0, 19264.7302e0, 21585.15479e0, 18547.24370e0, 12507.11123e0, 11);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
12.0e0, 18906.13660e0, 1888.17868e0, 6798.15702e0, 26851.30728e0, 12);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
13.0e0, 10697.104e0, 17801.4938e0, 10487.17266e0, 6989.17177e0, 13);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
14.0e0, 20496.19154e0, 31989.4195e0, 15396.5512e0, 1349.5570e0, 14);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
15.0e0, 7224.21400e0, 2674.18685e0, 8272.7088e0, 9690.32210e0, 15);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
16.0e0, 24269.9227e0, 25585.1523e0, 9209.661e0, 12415.4686e0, 16);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
17.0e0, 24545.14416e0, 21257.14737e0, 9827.3062e0, 3980.18414e0, 17);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
18.0e0, 30087.30688e0, 16242.15388e0, 13843.12070e0, 30398.5534e0, 18);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
19.0e0, 10841.32264e0, 2442.22599e0, 16212.2445e0, 1459.26878e0, 19);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
20.0e0, 29683.12905e0, 29907.10175e0, 19125.7972e0, 31343.27362e0, 20);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
21.0e0, 31094.12665e0, 8818.16288e0, 19337.27389e0, 29658.5075e0, 21);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
22.0e0, 27142.1281e0, 7090.11517e0, 32357.16312e0, 17472.4236e0, 22);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
23.0e0, 25420.11421e0, 27775.16732e0, 22438.30735e0, 21456.30334e0, 23);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
24.0e0, 26613.30270e0, 19948.12088e0, 489.30539e0, 4893.18508e0, 24);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into flotxtab values (
25.0e0, 26161.9899e0, 24750.30333e0, 27793.31181e0, 32159.19024e0, 25);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into realxtab select * from flotxtab;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dblxtab select * from flotxtab;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from flotxtab;"""
    output = _dci.cmdexec(stmt)
    # expect a count of 25
    
    stmt = """select count (*) from realxtab;"""
    output = _dci.cmdexec(stmt)
    # expect a count of 25
    
    stmt = """select count (*) from dblxtab;"""
    output = _dci.cmdexec(stmt)
    # expect a count of 25
    
    # Tests 41 - 49
    
    stmt = """create table charsimp (
lname char(6)  not null primary key,
a char (6),
b char (6)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table vcharsim (
lname varchar(10)  not null primary key,
a varchar (10),
b varchar (10)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into charsimp values ('Smith', 'Bozo', 'Bimbo');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charsimp values ('Brown', 'Frodo', 'Zaphod');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into vcharsim select * from charsimp;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from charsimp;"""
    output = _dci.cmdexec(stmt)
    # expect a count of 2
    
    stmt = """select count (*) from vcharsim;"""
    output = _dci.cmdexec(stmt)
    # expect a count of 2
    
    stmt = """create table charxtab (
lname char (6),
a     char (6),
b     char (6),
c     char (6),
d     char (6)  not null primary key
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table vcharxtb (
lname varchar (10),
a     varchar (10),
b     varchar (10),
c     varchar (10),
d     varchar (10)  not null primary key
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into charxtab values
('Smith', 'Baxryo', 'Vykugo', 'Bjmkfu', 'Wrvrhl');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Green', 'Vgunnf', 'Xvfxuj', 'Lascgu', 'Qvsxba');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Tiger', 'Mvbxgo', 'Osmwic', 'Krynvh', 'Wpjamh');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Brown', 'Bfbixc', 'Mobuak', 'Uermsw', 'Hkkqhx');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Jones', 'Zebbno', 'Udbsmc', 'Gqkgqk', 'Iyjnxm');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Tiger', 'Tkboea', 'Znrlqs', 'Dgktvy', 'Iqtsne');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Jones', 'Ajocap', 'Xmdens', 'Ghcxxv', 'Ciyjro');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Smith', 'Hlsvlr', 'Aqkcgf', 'Fyqkqv', 'Rhsvcy');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Brown', 'Dcuwuj', 'Mnopbr', 'Cvkinp', 'Nrqfwk');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Jones', 'Melbhv', 'Ctejxo', 'Tkfpfy', 'Xojbsq');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Green', 'Sswvmd', 'Zikvew', 'Buahrl', 'Yumcfe');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Tiger', 'Zdayqs', 'Rptowo', 'Xuhivv', 'Agchus');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Green', 'Argvls', 'Tvgtba', 'Wqyjgy', 'Ohymcw');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Tiger', 'Lqprri', 'Utjmjy', 'Chenji', 'Jgnocm');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Green', 'Cbddcm', 'Wyvrjy', 'Lpekfh', 'Jduliw');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Jones', 'Kodsvm', 'Bfqkjj', 'Viwynt', 'Kjofoh');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Tiger', 'Emwfwn', 'Lugoci', 'Bjuwnt', 'Yrrftk');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Green', 'Nhnyud', 'Yyluqj', 'Lhvvxe', 'Jqhlfs');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Jones', 'Wmxhew', 'Lojuas', 'Hdpuhc', 'Mgwmbj');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Tiger', 'Lkmhid', 'Sejwqx', 'Ydqbnp', 'Tcipjg');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Green', 'Ajnxgq', 'Dooxbw', 'Llpkfd', 'Eelpcs');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Brown', 'Hayptb', 'Temjdx', 'Mmjehp', 'Eiennb');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Smith', 'Iwxaib', 'Vlghwl', 'Devnku', 'Thyvgq');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Brown', 'Iwsvdd', 'Udbqwc', 'Sqanrg', 'Eyncrs');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Tiger', 'Arbyep', 'Timonm', 'Fvraad', 'Xyqgsx');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into charxtab values
('Smith', 'Dsorqa', 'Bijluq', 'Xljayt', 'Qstovb');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into vcharxtb select * from charxtab;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from charxtab;"""
    output = _dci.cmdexec(stmt)
    # expect a count of 26
    
    stmt = """select count (*) from vcharxtb;"""
    output = _dci.cmdexec(stmt)
    # expect a count of 26
    
    # Tests 51 - 59
    
    stmt = """create table datesimp (
num date  not null primary key,
a   date,
b   date
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table timesimp (
num time  not null primary key,
a   time,
b   time
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into datesimp values (
date '1995-06-01',
date '1996-06-01',
date '1997-06-01'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into datesimp values (
date '1990-06-01'  ,
date '1991-06-01',
date '1992-06-01'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into timesimp values (
time '10:30:00'  ,
time '11:30:00',
time '12:30:00'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into timesimp values (
time '20:30:00'  ,
time '21:30:00',
time '22:30:00'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from datesimp;"""
    output = _dci.cmdexec(stmt)
    # expect a count of 2
    
    stmt = """select count (*) from timesimp;"""
    output = _dci.cmdexec(stmt)
    # expect a count of 2
    
    # ===========================================
    
    stmt = """create table dtxtab (
num  int  ,
a    date not null primary key,
b    date,
c    date,
d    date
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into dtxtab values (
2039,
date '1950-04-21',
date '1950-02-24',
date '1950-02-11',
date '1974-05-01'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1980,
date '1990-07-18',
date '2028-07-23',
date '2000-07-24',
date '1988-02-10'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1951,
date '2007-08-04',
date '1983-07-22',
date '1967-05-06',
date '1962-11-21'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1986,
date '1970-08-26',
date '2016-12-09',
date '2022-07-22',
date '1950-11-12'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
2022,
date '1967-07-10',
date '2025-09-24',
date '2002-06-26',
date '1989-07-12'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1957,
date '2039-05-23',
date '2036-01-20',
date '1993-01-19',
date '1981-12-05'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
2029,
date '1980-12-12',
date '2015-07-06',
date '1981-06-05',
date '2006-07-06'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1950,
date '1951-10-16',
date '1998-04-28',
date '2030-05-19',
date '2017-06-17'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1990,
date '1986-04-19',
date '2025-03-20',
date '2023-10-27',
date '2032-03-15'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
2007,
date '2022-05-10',
date '2039-05-14',
date '2016-12-24',
date '1971-11-09'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1970,
date '1957-02-12',
date '1964-01-02',
date '1965-08-15',
date '1955-11-26'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1967,
date '2029-08-04',
date '2027-07-17',
date '2027-01-22',
date '2029-12-14'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
2030,
date '2030-08-15',
date '1987-01-20',
date '2013-09-28',
date '2033-01-11'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1960,
date '1960-07-19',
date '1997-11-06',
date '1996-01-27',
date '2006-09-27'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1997,
date '1997-03-20',
date '1951-03-03',
date '1977-04-10',
date '2000-01-24'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1961,
date '1961-05-06',
date '1961-10-17',
date '1951-05-07',
date '2014-01-14'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1974,
date '1974-12-17',
date '1982-10-03',
date '1958-03-15',
date '2015-10-21'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1965,
date '1965-06-27',
date '2005-01-19',
date '1982-09-12',
date '2027-02-09'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1978,
date '1978-10-05',
date '1983-04-08',
date '1963-03-21',
date '1993-10-19'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1971,
date '1971-09-22',
date '1953-05-16',
date '1964-11-19',
date '1985-07-08'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1977,
date '1977-04-22',
date '1984-04-09',
date '2038-09-07',
date '1981-05-09'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1982,
date '1982-12-03',
date '1980-02-05',
date '1989-12-26',
date '2020-05-11'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
2016,
date '2016-07-14',
date '2035-05-28',
date '1960-09-07',
date '1960-06-07'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1994,
date '1994-11-13',
date '2027-03-29',
date '1950-06-03',
date '1962-10-08'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into dtxtab values (
1982,
date '1982-12-22',
date '2021-01-04',
date '1950-10-20',
date '2013-03-15'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tmxtab (
num  int  not null primary key,
a    time,
b    time,
c    time,
d    time
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tmxtab values (
20, time '01:43:16', time '07:29:04', time '12:10:14', time '08:18:21');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
25, time '05:03:20', time '09:16:43', time '07:34:18', time '23:10:42');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
6, time '22:40:14', time '10:56:08', time '13:10:23', time '11:18:18');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
19, time '15:38:53', time '10:26:27', time '06:48:57', time '19:32:45');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
10, time '02:48:29', time '01:40:30', time '17:54:03', time '17:00:03');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
2, time '17:09:22', time '06:52:49', time '05:34:37', time '19:04:45');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
0, time '17:29:51', time '06:04:53', time '04:52:59', time '17:52:15');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
9, time '16:11:10', time '04:31:33', time '04:30:16', time '18:19:12');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
13, time '08:10:49', time '06:54:06', time '16:38:45', time '10:20:02');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
18, time '09:30:22', time '18:21:47', time '07:50:32', time '11:55:35');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
16, time '04:05:04', time '00:49:24', time '18:23:46', time '14:50:09');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
22, time '00:46:52', time '10:25:42', time '20:27:29', time '09:45:31');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
23, time '08:35:52', time '02:37:37', time '20:15:31', time '06:52:23');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
3, time '23:44:14', time '04:17:20', time '20:45:10', time '20:26:11');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
11, time '04:07:07', time '17:30:47', time '02:13:26', time '14:23:54');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
4, time '12:01:25', time '03:32:02', time '09:00:35', time '21:18:14');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
1, time '18:36:33', time '07:57:03', time '16:20:10', time '11:41:12');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
21, time '06:52:43', time '20:45:54', time '15:21:14', time '05:14:01');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
12, time '01:59:31', time '02:53:31', time '19:43:34', time '18:54:27');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
17, time '01:48:22', time '12:33:02', time '21:41:06', time '09:12:59');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
5, time '16:57:13', time '02:50:42', time '16:02:46', time '02:22:31');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
15, time '23:29:34', time '02:41:51', time '06:45:55', time '16:20:46');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
8, time '03:09:53', time '11:19:36', time '19:20:42', time '05:45:27');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
14, time '17:12:32', time '05:14:34', time '12:38:52', time '01:25:05');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tmxtab values (
7, time '22:48:57', time '06:18:46', time '10:30:30', time '03:23:07');"""
    output = _dci.cmdexec(stmt)
    
    # Tests 61 - 69
    
    stmt = """create table ivlsimp (
num interval year (4)  not null primary key,
a   interval year (4),
b   interval year (4)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into ivlsimp values (
interval '1990' year (4),
interval '1990' year (4),
interval '1990' year (4)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into ivlsimp values (
interval '1997' year (4),
interval '1998' year (4),
interval '1999' year (4)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from ivlsimp;"""
    output = _dci.cmdexec(stmt)
    # expect a count of 2
    
    # ===========================================
    
    stmt = """create table ivlxtab (
num  int  not null primary key,
a    interval year (4),
b    interval year (4),
c    interval year (4),
d    interval year (4)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into ivlxtab values (
8,
interval '2007' year (4),
interval '1957' year (4),
interval '2027' year (4),
interval '2037' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
12,
interval '1950' year (4),
interval '2024' year (4),
interval '1975' year (4),
interval '1981' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
9,
interval '2010' year (4),
interval '1953' year (4),
interval '2002' year (4),
interval '2015' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
15,
interval '1983' year (4),
interval '1977' year (4),
interval '1960' year (4),
interval '2028' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
13,
interval '1994' year (4),
interval '1956' year (4),
interval '1959' year (4),
interval '2030' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
6,
interval '2015' year (4),
interval '2010' year (4),
interval '2028' year (4),
interval '1994' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
24,
interval '1996' year (4),
interval '2002' year (4),
interval '1956' year (4),
interval '2020' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
10,
interval '2021' year (4),
interval '2018' year (4),
interval '2038' year (4),
interval '1959' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
1,
interval '2000' year (4),
interval '2012' year (4),
interval '1982' year (4),
interval '1954' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
7,
interval '2037' year (4),
interval '1999' year (4),
interval '1958' year (4),
interval '1957' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
17,
interval '2003' year (4),
interval '1970' year (4),
interval '1980' year (4),
interval '2029' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
3,
interval '1999' year (4),
interval '1989' year (4),
interval '1966' year (4),
interval '2027' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
19,
interval '1951' year (4),
interval '2024' year (4),
interval '2006' year (4),
interval '2035' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
23,
interval '1955' year (4),
interval '1964' year (4),
interval '2029' year (4),
interval '1963' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
4,
interval '1957' year (4),
interval '2007' year (4),
interval '2029' year (4),
interval '2028' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
18,
interval '2024' year (4),
interval '1978' year (4),
interval '2025' year (4),
interval '2011' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
2,
interval '1993' year (4),
interval '2011' year (4),
interval '2021' year (4),
interval '1981' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
21,
interval '1997' year (4),
interval '1997' year (4),
interval '1968' year (4),
interval '2019' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
11,
interval '1950' year (4),
interval '2026' year (4),
interval '1961' year (4),
interval '2033' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
16,
interval '2033' year (4),
interval '1972' year (4),
interval '1982' year (4),
interval '1970' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
5,
interval '1978' year (4),
interval '1988' year (4),
interval '2036' year (4),
interval '1983' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
22,
interval '2019' year (4),
interval '1962' year (4),
interval '2003' year (4),
interval '1967' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
20,
interval '2032' year (4),
interval '1985' year (4),
interval '1950' year (4),
interval '2010' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
14,
interval '2017' year (4),
interval '1962' year (4),
interval '1958' year (4),
interval '1983' year (4)
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ivlxtab values (
25,
interval '1964' year (4),
interval '1972' year (4),
interval '1955' year (4),
interval '2009' year (4)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from ivlxtab;"""
    output = _dci.cmdexec(stmt)
    # expect a count of 25
    
    #-------- eof ----------
    
    _testmgr.testcase_end(desc)

