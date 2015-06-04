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
    
    stmt = """create volatile table vt_wm000
(
seqno   integer         not null        not droppable,    

smin1   smallint                default null,    

inte1   integer                 default null,    

lint1   largeint                default null,    

nume1   numeric(9,3)            default null,    

deci1   decimal(18,9)           default null,    

pict1   pic s9(13)v9(5)         default null,    

flot1   float (52)              default null,    

real1   real                    default null,    

dblp1   double precision        default null,    

char1   char (12)               default null,    

vchr1   varchar (12)            default null,    

primary key (seqno)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into vt_wm000 select * from wm000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create volatile table vt_wm001
(
seqno   integer         not null        not droppable,    

smin1   smallint                default null,    

inte1   integer                 default null,    

lint1   largeint                default null,    

nume1   numeric(9,3)            default null,    

deci1   decimal(18,9)           default null,    

pict1   pic s9(13)v9(5)         default null,    

flot1   float (52)              default null,    

real1   real                    default null,    

dblp1   double precision        default null,    

char1   char (12)               default null,    

vchr1   varchar (12)            default null,    

primary key (seqno)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into vt_wm001 select * from wm001;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create volatile table vt_wm004 as select * from wm004;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create volatile table vt_tbl_null_001 as select * from tbl_null_001;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create volatile table vt_wm000_medium
(
seqno	integer		not null	not droppable,    

smin1	smallint		default null,    

inte1	integer			default null,    

lint1	largeint		default null,    

nume1	numeric(9,3)		default null,    

deci1	decimal(18,9)		default null,    

pict1	pic s9(13)v9(5)		default null,    

flot1	float (52)		default null,    

real1	real			default null,    

dblp1	double precision	default null,    

char1	char (12)		default null,    

vchr1	varchar (12)		default null,    

primary key (seqno)
) ;"""
    output = _dci.cmdexec(stmt)
    
    # stmt = """insert into vt_wm000_medium select * from wm000_medium;"""
    # output = _dci.cmdexec(stmt)
    
    stmt = """create volatile table vt_wm000_large
(
seqno	integer		not null	not droppable,    

smin1	integer		default null,    

inte1	integer			default null,    

lint1	largeint		default null,    

nume1	numeric(9,3)		default null,    

deci1	decimal(18,9)		default null,    

pict1	pic s9(13)v9(5)		default null,    

flot1	float (52)		default null,    

real1	real			default null,    

dblp1	double precision	default null,    

char1	char (12)		default null,    

vchr1	varchar (12)		default null,    

primary key (seqno)
) ;"""
    output = _dci.cmdexec(stmt)
    
    # stmt = """insert into vt_wm000_large select * from wm000_large;"""
    # output = _dci.cmdexec(stmt)
    
    stmt = """create volatile table vt_wm000_large2
(
seqno	integer		not null	not droppable,    

smin1	integer		default null,    

inte1	integer			default null,    

lint1	largeint		default null,    

nume1	numeric(9,3)		default null,    

deci1	decimal(18,9)		default null,    

pict1	pic s9(13)v9(5)		default null,    

flot1	float (52)		default null,    

real1	real			default null,    

dblp1	double precision	default null,    

char1	char (12)		default null,    

vchr1	varchar (12)		default null,    

primary key (seqno)
) ;"""
    output = _dci.cmdexec(stmt)
    
    # stmt = """insert into vt_wm000_large2 select * from wm000_large2;"""
    # output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table vt_wm000 on every column;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table vt_wm001 on every column;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table vt_wm004 on every column;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table vt_tbl_null_001 on every column;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table vt_wm000_medium on every column;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table vt_wm000_large on every column;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table vt_wm000_large2 on every column;"""
    output = _dci.cmdexec(stmt)
    
