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
    
def test001(desc="""create tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table f00(
        colkey int not null,
        colint int not null,
        --   coldate date,
        colnum numeric(11,3),
        colchariso char(11) character set iso88591 not null,
        colcharucs2 char(11) character set ucs2 not null,
        colintn int,
        --   colts timestamp,
        colcharison char(13) character set iso88591,
        colcharucs2n char(13) character set ucs2,
        primary key(colint, colchariso, colcharucs2, colkey)
        )
        ;"""
    output = _dci.cmdexec(stmt)

    stmt = """upsert using load into f00 select
        c1+c2*10+c3*100+c4*1000+c5*10000, --colkey
        c1+c2*10+c3*100+c4*1000+c5*10000, --colint
        cast(c1+c2*10+c3*100+c4*1000+c5*10000 as numeric(11,3)), --colnum
        cast(c1+c2*10+c3*100+c4*1000+c5*10000 as char(11) character set iso88591), --colchariso
        cast(c1+c2*10+c3*100+c4*1000+c5*10000 as char(11) character set ucs2), --colcharucs2
        c1+c2*10+c3*100+c4*1000+c5*10000, --colintn
        cast(c1+c2*10+c3*100+c4*1000+c5*10000 as char(13) character set iso88591), --colvchriso
        cast(c1+c2*10+c3*100+c4*1000+c5*10000 as char(13) character set ucs2) --colvchrucs2
        from (values(1)) t
        transpose 0,1,2,3,4,5,6,7,8,9 as c1
        transpose 0,1,2,3,4,5,6,7,8,9 as c2
        transpose 0,1,2,3,4,5,6,7,8,9 as c3
        transpose 0,1,2,3,4,5,6,7,8,9 as c4
        transpose 0,1,2,3,4,5,6,7,8,9 as c5
        ;"""
    output = _dci.cmdexec(stmt)

    stmt = """update f00 set (colint, colcharucs2n) = (543210, NULL) where colkey between 54300 and 54899;"""
    output = _dci.cmdexec(stmt)

    stmt = """update f00 set (colint, colcharison) = (876543, NULL) where colkey between 87300 and 87999;"""
    output = _dci.cmdexec(stmt)

    stmt = """update f00 set colchariso = 'stuvwx' where colkey between 35100 and 35899;"""
    output = _dci.cmdexec(stmt)

    stmt = """update f00 set colchariso = 'abcdefghijk' where colkey between 80200 and 81099;"""
    output = _dci.cmdexec(stmt)

    stmt = """update f00 set colcharucs2 = 'stuvwx' where colkey between 65000 and 65699;"""
    output = _dci.cmdexec(stmt)

    stmt = """update f00 set colcharucs2 = 'abcdefghijk' where colkey between 79100 and 79999;"""
    output = _dci.cmdexec(stmt)

    stmt = """update f00 set colintn = NULL where colkey between 80000 and 85999;"""
    output = _dci.cmdexec(stmt)

    stmt = """update f00 set colintn = NULL where colkey between 14000 and 19999;"""
    output = _dci.cmdexec(stmt)

    stmt = """update f00 set colintn = NULL where colkey between 14900 and 15499;"""
    output = _dci.cmdexec(stmt)

    stmt = """update f00 set colintn = NULL where colkey between 89900 and 90499;"""
    output = _dci.cmdexec(stmt)

    stmt = """update statistics for table f00 on every column;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table d00(
        d00colkey int not null,
        d00colint int not null,
        --   d00coldate date,
        d00colnum numeric(11,3),
        d00colchariso char(11) character set iso88591 not null,
        d00colcharucs2 char(11) character set ucs2 not null,
        d00colintn int,
        --   d00colts timestamp,
        d00colcharison char(13) character set iso88591,
        d00colcharucs2n char(13) character set ucs2,
        primary key(d00colint, d00colkey, d00colchariso, d00colcharucs2)
        )
        ;"""
    output = _dci.cmdexec(stmt)

    stmt = """upsert using load into d00 select
        c1+c2*10+c3*100+c4*1000+c5*10000, --colkey
        c1+c2*10+c3*100+c4*1000+c5*10000, --colint
        cast(c1+c2*10+c3*100+c4*1000+c5*10000 as numeric(11,3)), --colnum
        cast(c1+c2*10+c3*100+c4*1000+c5*10000 as char(11) character set iso88591), --colchariso
        cast(c1+c2*10+c3*100+c4*1000+c5*10000 as char(11) character set ucs2), --colcharucs2
        c1+c2*10+c3*100+c4*1000+c5*10000, --colintn
        cast(c1+c2*10+c3*100+c4*1000+c5*10000 as char(13) character set iso88591), --colvchriso
        cast(c1+c2*10+c3*100+c4*1000+c5*10000 as char(13) character set ucs2) --colvchrucs2
        from (values(1)) t
        transpose 0,1,2,3,4,5,6,7,8,9 as c1
        transpose 0,1,2,3,4,5,6,7,8,9 as c2
        transpose 0,1,2,3,4,5,6,7,8,9 as c3
        transpose 0,1,2,3,4,5,6,7,8,9 as c4
        transpose 0,1,2,3,4,5,6,7,8,9 as c5
        ;"""
    output = _dci.cmdexec(stmt)

    stmt = """update d00 set (d00colint, d00colcharucs2n, d00colnum) = (543210, NULL, 543210.777) where d00colkey between 54200 and 54499;"""
    output = _dci.cmdexec(stmt)

    stmt = """update d00 set (d00colint, d00colcharison, d00colnum) = (876543, NULL, 876543.555) where d00colkey between 87500 and 87799;"""
    output = _dci.cmdexec(stmt)

    stmt = """update d00 set (d00colint, d00colchariso) = (349111, 'zyxwvuts') where d00colkey between 34900 and 35199;"""
    output = _dci.cmdexec(stmt)

    stmt = """update d00 set d00colchariso = 'mnopqrstu' where d00colkey between 80100 and 80399;"""
    output = _dci.cmdexec(stmt)

    stmt = """update d00 set d00colcharucs2 = 'zyxwvuts' where d00colkey between 65500 and 65799;"""
    output = _dci.cmdexec(stmt)

    stmt = """update d00 set d00colcharucs2 = 'mnopqrstu' where d00colkey between 79500 and 79799;"""
    output = _dci.cmdexec(stmt)

    stmt = """update d00 set d00colintn = NULL where d00colkey between 84000 and 87999;"""
    output = _dci.cmdexec(stmt)

    stmt = """update d00 set d00colintn = NULL where d00colkey between 17000 and 20999;"""
    output = _dci.cmdexec(stmt)

    stmt = """update d00 set d00colintn = NULL where d00colkey between 14800 and 15099;"""
    output = _dci.cmdexec(stmt)

    stmt = """update d00 set d00colintn = NULL where d00colkey between 90300 and 90599;"""
    output = _dci.cmdexec(stmt)

    stmt = """update statistics for table d00 on every column;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

