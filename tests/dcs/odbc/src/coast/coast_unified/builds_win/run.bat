REM @@@ START COPYRIGHT @@@
REM
REM (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
REM
REM  Licensed under the Apache License, Version 2.0 (the "License");
REM  you may not use this file except in compliance with the License.
REM  You may obtain a copy of the License at
REM
REM      http://www.apache.org/licenses/LICENSE-2.0
REM
REM  Unless required by applicable law or agreed to in writing, software
REM  distributed under the License is distributed on an "AS IS" BASIS,
REM  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
REM  See the License for the specific language governing permissions and
REM  limitations under the License.
REM
REM @@@ END COPYRIGHT @@@



WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLAllocEnv
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLAllocConnect
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLBindParameter
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLBrowseConnect
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLColumnAttribute
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLConnectDisconnect
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLDataSources
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLDescribeColumns
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLDriverConnect
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLDrivers
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLError
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLExecuteDirect
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLExecute
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLExtendedFetch
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLFetch
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLGetData
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLPutData
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLGetFunctions
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLGetInfo
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLMoreResults
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLAllocStmt
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLBindColumn
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLColumns
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLDescribeParam
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLGetTypeInfo
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLPrimaryKeys
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API ResourceGoverning
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLSetConnectOption
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLSetCursorName
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLSetStatementOption
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLSpecialColumns
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLStatistics
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLTables
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLNativeSql
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLNumParams
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLNumResultCols
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLPrepare
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLRowCount
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLTransact
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLAllocHandle
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLBindParameter30
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLCloseCursor
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLColumnAttributes30
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLCopyDescriptor
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLDescribeColumns30
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLEndTran
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLGetConnectAttr
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLGetDescField
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLGetDescRec
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLGetDiagField
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLGetDiagRec
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLGetEnvAttr
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLGetInfo30
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLGetStmtAttr
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLMoreResults30
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLBindCol30
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLGetData30
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLBindColInterval
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLGetDataInterval
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLBindParamInterval
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLForeignKeys
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLColumnPriv
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLTablePriv
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLGetTypeInfo3
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLProcedures
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLProcedureColumns
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLFetchScroll
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API Unicode
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API QueryID
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API Hash2
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API SQLCancel
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API LargeBlock
WCSCOAST.exe -d %ODBCTEST_DSN% -u %ODBCTEST_USER% -p %ODBCTEST_PASS% -c %ODBCTEST_CHARSET% -m %ODBCTEST_OS% -f API InfoStats

REM date
echo ""
echo "Test Results for COAST TESTS"
echo "----------------------------"

grep -ih 'TEST RESULT' *.log | tee summary.sum

echo "-------------------"
echo "END OF COAST TESTS"

chmod -R 777 *

