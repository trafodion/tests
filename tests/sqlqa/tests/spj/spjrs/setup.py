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
import defs

_testmgr = None
_testlist = []
_dci = None
_dbrootdci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    _dci.setup_schema(defs.my_schema)
    _dbrootdci = _testmgr.get_dbroot_dci_proc()

    # set up spj path
    defs.set_spjpath()

    stmt = """grant component privilege manage_library on sql_operations to "public";"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_complete_msg(output)

    stmt = "create library " + defs.spjrs_lib + " file '" + defs.spjrs_path + "';"
    output = _dci.cmdexec(stmt)

    stmt = "create library " + defs.spjcall_lib + " file '" + defs.spjcall_path + "';"
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_get_date (out date) external name 'Jdbc_Get_Date.getDate' library qa_spjrs language java parameter style java  contains sql no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_get_long (out bigint) external name 'Jdbc_Get_Long.getLong' library qa_spjrs language java parameter style java  contains sql no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_get_short (out smallint) external name 'Jdbc_Get_Short.getShort' library qa_spjrs language java parameter style java  contains sql no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_get_string (out char(10)) external name 'Jdbc_Get_String.getString' library qa_spjrs language java parameter style java  contains sql no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_get_time (out time) external name 'Jdbc_Get_Time.getTime' library qa_spjrs language java parameter style java  contains sql no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_get_timestamp (out timestamp(6)) external name 'Jdbc_Get_Timestamp.getTimestamp' library qa_spjrs language java parameter style java  contains sql no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_io_double (inout double precision) external name 'Jdbc_IO_Double.ioDouble' library qa_spjrs language java parameter style java  no SQL no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_io_float (inout real) external name 'Jdbc_IO_Float.ioFloat' library qa_spjrs language java parameter style java no SQL no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_io_int (inout integer) external name 'Jdbc_IO_Int.ioInt' library qa_spjrs language java parameter style java no sql no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_io_long (inout bigint) external name 'Jdbc_IO_Long.ioLong' library qa_spjrs language java parameter style java no SQL no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_io_short (inout smallint) external name 'Jdbc_IO_Short.ioShort' library qa_spjrs language java parameter style java no SQL no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_io_string (inout char(25)) external name 'Jdbc_IO_String.ioString' library qa_spjrs language java parameter style java no SQL no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_io_vstring (inout varchar(25)) external name 'Jdbc_IO_VString.ioVString' library qa_spjrs language java parameter style java no SQL no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_io_time (inout time) external name 'Jdbc_IO_Time.ioTime' library qa_spjrs language java parameter style java no SQL no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_io_timestamp (inout timestamp) external name 'Jdbc_IO_Timestamp.ioTimestamp' library qa_spjrs language java parameter style java no SQL no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_set_float (in real, out integer) external name 'Jdbc_Set_Float.setFloat' library qa_spjrs language java parameter style java  contains sql no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_set_time (in time, out integer) external name 'Jdbc_Set_Time.setTime' library qa_spjrs language java parameter style java  contains sql no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_set_timestamp (in timestamp, out integer) external name 'Jdbc_Set_Timestamp.setTimestamp' library qa_spjrs language java parameter style java  contains sql no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure totalprice(IN qty NUMERIC (18),IN rate VARCHAR (10),INOUT price NUMERIC (18,2))
        external name 'Sales.totalPrice'
        library qa_spjrs
        language java
        parameter style java
        reads sql data;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_get_bigdecimal (out numeric(12,5))
        external name 'Jdbc_Get_BigDeci.getBigDecimal'
        library qa_spjrs
        language java
        parameter style java
        contains sql
        no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_get_double (out double precision)
        external name 'Jdbc_Get_Doub.getDouble'
        library qa_spjrs
        language java
        parameter style java
        contains sql
        no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_get_float (out real)
        external name 'Jdbc_Get_Flot.getFloat'
        library qa_spjrs
        language java
        parameter style java
        contains sql
        no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_get_int (out integer)
        external name 'Jdbc_Get_Integer.getInt'
        library qa_spjrs
        language java
        parameter style java
        contains sql
        no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure jdbc_get_vstring (out varchar(10))
        external name 'Jdbc_Get_VSting.getVString'
        library qa_spjrs
        language java
        parameter style java contains SQL
        no isolate;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create procedure InsertAutoCommitT(in in1 nchar(50))
        external name 'TestTransaction.InsertAutoCommit'
        LIBRARY qa_spjrs
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Create procedure InsertAutoCommitNT(in in1 nchar(50))
        external name 'TestTransaction.InsertAutoCommit'
        LIBRARY qa_spjrs
        NO TRANSACTION REQUIRED
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Create procedure InsertCommitT(in in1 nchar(50))
        external name 'TestTransaction.InsertCommit'
        LIBRARY qa_spjrs
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Create procedure InsertCommitNT(in in1 nchar(50))
        external name 'TestTransaction.InsertCommit'
        LIBRARY qa_spjrs
        NO TRANSACTION REQUIRED
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Create procedure InsertRollbackT(in in1 nchar(50))
        external name 'TestTransaction.InsertRollback'
        LIBRARY qa_spjrs
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Create procedure InsertRollbackNT(in in1 nchar(50))
        external name 'TestTransaction.InsertRollback'
        LIBRARY qa_spjrs
        NO TRANSACTION REQUIRED
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
