# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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
import setup

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

    output = _dci.cmdexec("""drop table f00;""")
    output = _dci.cmdexec("""drop table f01;""")

    stmt = """create table f00(
colkey int unsigned not null,
colint int signed,
colsint smallint signed,
collint largeint,
colnum numeric(11,3),
colflt float,
coldec decimal(11,2),
coldate date,
coltime time,
colts timestamp,
colchriso char(75) character set iso88591,
colchrucs2 char(80) character set utf8,
colvchriso varchar(85) character set iso88591,
colvchrucs2 varchar(90) character set utf8,
primary key (colkey))
salt using 8 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """load into f00 select
c1+c2*10+c3*100,
(c1+c2*10+c3*100) - 500,
((c1+c2*10+c3*100) - 500) * 10,
((c1+c2*10+c3*100) * 100000) + 549755813888,
cast((c1+c2*10+c3*100) - 500 as numeric(11,3)),
cast(((c1+c2*10+c3*100) - 500) * 100.06837 as float),
cast(c1+c2*10+c3*100 as decimal(11,2)),
cast(converttimestamp(210614299200000000 +
(86400000000 * (c1+c2*10+c3*100))) as date),
time'00:00:00' + cast(mod(c1+c2*10+c3*100,3)
as interval minute),
converttimestamp(210614299200000000 + (86400000000 *
(c1+c2*10+c3*100)) + (1000000 * (c1+c2*10+c3*100)) +
(60000000 * (c1+c2*10)) + (3600000000 * (c1+c2*10))),
cast(c1+c2*10+c3*100 as char(3) character set iso88591) || 'abcdefghijklmnop',
cast(c1+c2*10+c3*100 as char(3) character set ucs2) || 'zyxwvutsrqponmlki',
cast(c1+c2*10+c3*100 as varchar(3) character set iso88591) || 'blahblahblah',
cast(c1+c2*10+c3*100 as varchar(3) character set ucs2) || 'diddlediddlededo'
from (values(1)) t
transpose 0,1,2,3,4,5,6,7,8,9 as c1
transpose 0,1,2,3,4,5,6,7,8,9 as c2
transpose 0,1,2,3,4,5,6,7,8,9 as c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table f01(colchr char(13), colvchr varchar(13));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into f01 values
('abcdefghijklm', 'abcdefghijklm'),
('abcdefghijklm', 'abcdef      '),
('1234567890123', '1234567890123'),
('1234567      ', '1234567'),
('12345        ', '12345'),
('1234%67890123', '1234%67890123'),
('1234567_90123', '1234567_90123');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '7')


def test_between(desc="""between predicate"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: between predicate"""

    ### BETWEEN PREDICATE: HQC cacheable but not parameterized.

    setup.resetHQC()

    # new HQC entry; non-parameterized literals
    defs.qry = """select count(*) from f00 where colkey between -150 and 99;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT COUNT ( * ) FROM F00""" +
                 """ WHERE COLKEY BETWEEN - #NP# AND #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '3135300A39390A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '100')

    # new HQC entry; non-parameterized literals
    defs.qry = """select * from f00 where colkey between -100 and 11;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F00 WHERE COLKEY BETWEEN - #NP# AND #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '3130300A31310A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '11')
    _dci.expect_file(output, defs.expfile, 'BTWN001')

    # new HQC entry; non-parameterized literals
    defs.qry = """select count(*) from f00 where colkey between 10 and 19;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT COUNT ( * ) FROM F00""" +
                 """ WHERE COLKEY BETWEEN #NP# AND #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '31300A31390A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '10')

    # new HQC entry; non-parameterized literals
    defs.qry = """select count(*) from f00 where colnum between 34 and 169;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT COUNT ( * ) FROM F00""" +
                 """ WHERE COLNUM BETWEEN #NP# AND #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '33340A3136390A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '136')

    # new HQC entry; non-parameterized literals
    defs.qry = """select * from f00
where (coldate, colchriso)
between (date'1963-05-06', '490abcdefghijklmnop')
and (date'1963-06-07', '522abcdefghijklmnop');"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F00 WHERE ( COLDATE , COLCHRISO )""" +
                 """ BETWEEN ( DATE #NP# , #NP# )""" +
                 """ AND ( DATE #NP# , #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 4
    defs.npliterals = ('27313936332D30352D3036270A' +
                       '273439306162636465666768696A6B6C6D6E6F70270A' +
                       '27313936332D30362D3037270A' +
                       '273532326162636465666768696A6B6C6D6E6F70270A')
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '33')
    _dci.expect_file(output, defs.expfile, 'BTWN002')

    _testmgr.testcase_end(desc)


def test_like(desc="""like predicate"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: like predicate"""

    ### LIKE PREDICATE: HQC cacheable, NOT parameterized

    setup.resetHQC()

    stmt = defs.prepXX + """select * from f01 where colchr like '1234567';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHR LIKE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2731323334353637270A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from f01 where colchr like '12345%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LIKE001')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHR LIKE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313233343525270A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from f01
where colchr like '123_567890123';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LIKE002')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHR LIKE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '273132335F353637383930313233270A'
    setup.verifyHQCEntryExists()

    # expect = Not HQC Cacheable but added to SQC
    stmt = defs.prepXX + """select * from f01
where colchr like '%67890123';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LIKE003')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHR LIKE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27253637383930313233270A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from f01
where colchr not like '12345%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LIKE004')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHR NOT LIKE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313233343525270A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from f01
where colchr not like '123_567890123';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LIKE005')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHR NOT LIKE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '273132335F353637383930313233270A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from f01
where colchr not like '%890123';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LIKE006')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHR NOT LIKE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2725383930313233270A'
    setup.verifyHQCEntryExists()

    setup.resetHQC()

    stmt = defs.prepXX + """select * from f01 where colvchr like '1234567';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LIKE007')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHR LIKE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2731323334353637270A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from f01 where colvchr like '12345%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LIKE001')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHR LIKE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313233343525270A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from f01
where colvchr like '123_567890123';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LIKE002')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHR LIKE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '273132335F353637383930313233270A'
    setup.verifyHQCEntryExists()

    # expect = Not HQC Cacheable but added to SQC
    stmt = defs.prepXX + """select * from f01
where colvchr like '%67890123';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LIKE003')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHR LIKE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27253637383930313233270A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from f01
where colvchr not like '12345%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LIKE004')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHR NOT LIKE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313233343525270A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from f01
where colvchr not like '123_567890123';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LIKE005')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHR NOT LIKE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '273132335F353637383930313233270A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from f01
where colvchr not like '%890123';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LIKE006')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHR NOT LIKE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2725383930313233270A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_in(desc="""in predicate"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: in predicate"""

    ### IN PREDICATE: HQC cacheable, NOT parameterized

    setup.resetHQC()

    stmt = defs.prepXX + """select * from f00
where colint IN (-500, -300, -100, 100, 300, 500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'IN001')
    defs.hkey = ("""SELECT * FROM F00 WHERE COLINT IN""" +
                 """ ( - #NP# , - #NP# , - #NP# , #NP# , #NP# , #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 6
    defs.npliterals = '3530300A3330300A3130300A3130300A3330300A3530300A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from f00
where colint IN (-400, -200, -10, 10, 200, 400);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'IN002')
    defs.hkey = ("""SELECT * FROM F00 WHERE COLINT IN ( - #NP# ,""" +
                 """ - #NP# , - #NP# , #NP# , #NP# , #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 6
    defs.npliterals = '3430300A3230300A31300A31300A3230300A3430300A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from f00
where colint IN (25, 50, 75, 100, 125, 150, 175, 200, 225,
250, 275, 300, 325, 350, 375, 400, 425, 450, 475);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'IN003')
    defs.hkey = ("""SELECT * FROM F00 WHERE COLINT IN ( #NP# ,""" +
                 """ #NP# , #NP# , #NP# , #NP# , #NP# , #NP# ,""" +
                 """ #NP# , #NP# , #NP# , #NP# , #NP# , #NP# ,""" +
                 """ #NP# , #NP# , #NP# , #NP# , #NP# , #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 19
    defs.npliterals = ('32350A35300A37350A' +
                       '3130300A3132350A3135300A3137350A' +
                       '3230300A3232350A3235300A3237350A' +
                       '3330300A3332350A3335300A3337350A' +
                       '3430300A3432350A3435300A3437350A')
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from f00
where colchrucs2 IN ('73 zyxwvutsrqponmlkj', '149zyxwvutsrqponmlkj',
'269zyxwvutsrqponmlkj', '88 zyxwvutsrqponmlkj', '321zyxwvutsrqponmlkj');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'IN004')
    defs.hkey = ("""SELECT * FROM F00 WHERE COLCHRUCS2 IN (""" +
                 """ #NP# , #NP# , #NP# , #NP# , #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 5
    defs.npliterals = ('273733207A797877767574737271706F6E6D6C6B6A270A' +
                       '273134397A797877767574737271706F6E6D6C6B6A270A' +
                       '273236397A797877767574737271706F6E6D6C6B6A270A' +
                       '273838207A797877767574737271706F6E6D6C6B6A270A' +
                       '273332317A797877767574737271706F6E6D6C6B6A270A')
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from f00
where colvchrucs2 IN ('9diddlediddlededo', '400diddlediddlededo',
'57diddlediddlededo', '5diddlediddlededo', '0diddlediddlededo');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'IN005')
    defs.hkey = ("""SELECT * FROM F00 WHERE COLVCHRUCS2 IN""" +
                 """ ( #NP# , #NP# , #NP# , #NP# , #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 5
    defs.npliterals = ('2739646964646C65646964646C656465646F270A' +
                       '27343030646964646C65646964646C656465646F270A' +
                       '273537646964646C65646964646C656465646F270A' +
                       '2735646964646C65646964646C656465646F270A' +
                       '2730646964646C65646964646C656465646F270A')
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from f00 where (colnum, coldate)
IN (values (89.000, date'1963-08-13'), (1.79E2, date'1963-11-11'),
(369, date'1964-05-19'), (3.9E+1, date'1963-06-24'),
(259.00, date'1964-01-30'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'IN006')
    defs.hkey = ("""SELECT * FROM F00 WHERE ( COLNUM , COLDATE )""" +
                 """ IN ( VALUES ( #NP# , DATE #NP# ) ,""" +
                 """ ( #NP# , DATE #NP# ) , ( #NP# , DATE #NP# ) ,""" +
                 """ ( #NP# , DATE #NP# ) , ( #NP# , DATE #NP# ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 10
    defs.npliterals = ('38392E3030300A27313936332D30382D3133270A' +
                       '312E373945320A27313936332D31312D3131270A' +
                       '3336390A27313936342D30352D3139270A' +
                       '332E39452B310A27313936332D30362D3234270A' +
                       '3235392E30300A27313936342D30312D3330270A')
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)
