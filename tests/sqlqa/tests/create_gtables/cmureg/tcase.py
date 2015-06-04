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

import a08dat1_ddl
import a08dat2_ddl
import uw00_ddl
import uw01_ddl
import uw02_ddl
import uw03_ddl
import uw04_ddl
import uw05_ddl
import uw06_ddl
import uw07_ddl
import uw08_ddl
import uw09_ddl
import uw10_ddl
import uw11_ddl
import uw12_ddl
import uw13_ddl
import uw14_ddl
import uw15_ddl
import uw16_ddl
import uw17_ddl
import uw18_ddl
import uw19_ddl
import uw20_ddl
import a01dat_ddl
import t005dat_ddl
import t005da1_ddl
import t005da2_ddl
import wiscb1_ddl
import wiscb2_ddl
import wiscb3_ddl
import wiscb4_ddl
import wiscb5_ddl
import blk00_ddl
import blk01_ddl
import blk02_ddl
import blk03_ddl
import blk04_ddl
import blk07_ddl
import blk09_ddl
import b2pns01_ddl
import b2uwl02_ddl
import b2pns03_ddl
import b2unl15_ddl
import b2uns09_ddl
import btuns01_ddl
import b3uns03_ddl
import b2uns01_ddl
import b3uns01_ddl
import b3uns05_ddl
import btpnl17a_ddl
import dat10500_ddl
import dat50_ddl
import dat100_ddl
import dat200_ddl
import dat400_ddl
import dat800_ddl
import dat1600_ddl
import dat3200_ddl
import dat6400_ddl
import big210_ddl
import big210a_ddl
import b2pwl02_ddl 
import customer1_ddl
import customer2_ddl
import customer3_ddl
import customer4_ddl
import lineitem1_ddl
import lineitem2_ddl
import lineitem3_ddl
import lineitem4_ddl
import orders1_ddl
import orders2_ddl
import orders3_ddl
import orders4_ddl
import part1_ddl
import part2_ddl
import part3_ddl
import part4_ddl
import partsupp1_ddl
import partsupp2_ddl
import partsupp3_ddl
import partsupp4_ddl
import supplier1_ddl
import supplier2_ddl
import supplier3_ddl
import supplier4_ddl
import nation_ddl
import region_ddl
import wisc8m8p0_ddl
import wisc8m8p1_ddl
import wisc8m8p2_ddl
import wisc8m8p3_ddl
import wisc8m8p4_ddl
import wisc8m8p5_ddl
import wisc8m8p6_ddl
import wisc8m8p7_ddl
from ...lib import hpdci
import defs
import table

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

def test001(desc='Create tables'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    prop_template = defs.test_dir + '/../../lib/t4properties.template'
    prop_file = defs.work_dir + '/t4properties'
    hpdci.create_jdbc_propfile(prop_template, prop_file, defs.w_catalog, defs.w_schema)

    tablelist = [['a08dat1', 'a08dat1.dat', ',', 12],
                 ['a08dat2', 'a08dat2.dat', ',', 18],
                 ['uw00', 'uw00.dat', ',', 250],
                 ['uw01', 'uw01.dat', ',', 250],
                 ['uw02', 'uw02.dat', ',', 250],
                 ['uw03', 'uw03.dat', ',', 250],
                 ['uw04', 'uw04.dat', ',', 250],
                 ['uw05', 'uw05.dat', ',', 250],
                 ['uw06', 'uw06.dat', ',', 250],
                 ['uw07', 'uw07.dat', ',', 250],
                 ['uw08', 'uw08.dat', ',', 250],
                 ['uw09', 'uw09.dat', ',', 250],
                 ['uw10', 'uw10.dat', ',', 250],
                 ['uw11', 'uw11.dat', ',', 250],
                 ['uw12', 'uw12.dat', ',', 250],
                 ['uw13', 'uw13.dat', ',', 250],
                 ['uw14', 'uw14.dat', ',', 250],
                 ['uw15', 'uw15.dat', ',', 250],
                 ['uw16', 'uw16.dat', ',', 250],
                 ['uw17', 'uw17.dat', ',', 250],
                 ['uw18', 'uw18.dat', ',', 250],
                 ['uw19', 'uw19.dat', ',', 250],
                 ['uw20', 'uw20.dat', ',', 250],
                 ['a01dat', 'a01dat.dat', ',', 1485],
                 ['t005dat', 't005dat.dat', ',', 1400],
                 ['t005da1', 't005da1.dat', ',', 30],
                 ['t005da2', 't005da2.dat', ',', 20],
                 ['wiscb1', 'wiscb1.dat', ',', 100000],
                 ['wiscb2', 'wiscb2.dat', ',', 100000],
                 ['wiscb3', 'wiscb3.dat', ',', 100000],
                 ['wiscb4', 'wiscb4.dat', ',', 100000],
                 ['wiscb5', 'wiscb5.dat', ',', 100000],
                 ['blk00', 'blk00.dat', ',', 100000],
                 ['blk01', 'blk01.dat', ',', 100000],
                 ['blk02', 'blk02.dat', ',', 100000],
                 ['blk03', 'blk03.dat', ',', 100000],
                 ['blk04', 'blk04.dat', ',', 100000],
                 ['blk07', 'blk07.dat', ',', 20000],
                 ['blk09', 'blk09.dat', ',', 20000],
                 ['b2pns01', 'b2pns01.dat', ',', 1500],
                 ['b2uwl02', 'b2uwl02.dat', ',', 5000],
                 ['b2pns03', 'b2pns03.dat', ',', 1500],
                 ['b2unl15', 'b2unl15.dat', ',', 150000],
                 ['b2uns09', 'b2uns09.dat', ',', 1500],
                 ['btuns01', 'btuns01.dat', ',', 1500],
                 ['b3uns03', 'b3uns03.dat', ',', 1500],
                 ['b2uns01', 'b2uns01.dat', ',', 1500],
                 ['b3uns01', 'b3uns01.dat', ',', 1500],
                 ['b3uns05', 'b3uns05.dat', ',', 1500],
                 ['btpnl17a', 'btpnl17a.dat', ',', 2000],
                 ['dat10500', 'dat10500.dat', ',', 10500],
                 ['dat50', 'dat50.dat', ',', 50],
                 ['dat100', 'dat100.dat', ',', 100],
                 ['dat200', 'dat200.dat', ',', 200],
                 ['dat400', 'dat400.dat', ',', 400],
                 ['dat800', 'dat800.dat', ',', 800],
                 ['dat1600', 'dat1600.dat', ',', 1600],
                 ['dat3200', 'dat3200.dat', ',', 3200],
                 ['dat6400', 'dat6400.dat', ',', 6400],
                 ['big210', 'big210.dat', ',', 500000],
                 ['big210a', 'big210a.dat', ',', 12800],
                 ['b2pwl02', 'b2pwl02.2gb', ',', 2000000],
                 ['customer1', 'customer.tbl.1', ',', 3750],
                 ['customer2', 'customer.tbl.2', ',', 3750],
                 ['customer3', 'customer.tbl.3', ',', 3750],
                 ['customer4', 'customer.tbl.4', ',', 3750],
                 ['lineitem1', 'lineitem.tbl.1', ',', 150390],
                 ['lineitem2', 'lineitem.tbl.2', ',', 149424],
                 ['lineitem3', 'lineitem.tbl.3', ',', 150005],
                 ['lineitem4', 'lineitem.tbl.4', ',', 150753],
                 ['orders1', 'orders.tbl.1', ',', 37500],
                 ['orders2', 'orders.tbl.2', ',', 37500],
                 ['orders3', 'orders.tbl.3', ',', 37500],
                 ['orders4', 'orders.tbl.4', ',', 37500],
                 ['part1', 'part.tbl.1', ',', 5000],
                 ['part2', 'part.tbl.2', ',', 5000],
                 ['part3', 'part.tbl.3', ',', 5000],
                 ['part4', 'part.tbl.4', ',', 5000],
                 ['partsupp1', 'partsupp.tbl.1', ',', 20000],
                 ['partsupp2', 'partsupp.tbl.2', ',', 20000],
                 ['partsupp3', 'partsupp.tbl.3', ',', 20000],
                 ['partsupp4', 'partsupp.tbl.4', ',', 20000],
                 ['supplier1', 'supplier.tbl.1', ',', 250],
                 ['supplier2', 'supplier.tbl.2', ',', 250],
                 ['supplier3', 'supplier.tbl.3', ',', 250],
                 ['supplier4', 'supplier.tbl.4', ',', 250],
                 ['nation', 'nation.tbl', ',', 25],
                 ['region', 'region.tbl', ',', 5],
                 ['wisc8m8p0', 'wisc8m.8p0', '\t', 1000000],
                 ['wisc8m8p1', 'wisc8m.8p1', '\t', 1000000],
                 ['wisc8m8p2', 'wisc8m.8p2', '\t', 1000000],
                 ['wisc8m8p3', 'wisc8m.8p3', '\t', 1000000],
                 ['wisc8m8p4', 'wisc8m.8p4', '\t', 1000000],
                 ['wisc8m8p5', 'wisc8m.8p5', '\t', 1000000],
                 ['wisc8m8p6', 'wisc8m.8p6', '\t', 1000000],
                 ['wisc8m8p7', 'wisc8m.8p7', '\t', 1000000]]

    for item in tablelist:
        table.create_and_load(_testmgr, prop_file, item[0], item[1], item[2], item[3])
   
    _testmgr.testcase_end(desc)

