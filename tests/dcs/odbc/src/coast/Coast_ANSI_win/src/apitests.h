/**
  @@@ START COPYRIGHT @@@

  (C) Copyright 2015 Hewlett-Packard Development Company, L.P.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  @@@ END COPYRIGHT @@@
*/

#ifndef __APITESTSH      /* this prevents multiple copies of this... */
#define __APITESTSH      /* ...include file from being #included... */

#include "basedef.h"
#include "common.h"

#ifdef __cplusplus
    #ifdef aCC_COMPILER
        PassFail TestSQLAllocConnect(TestInfo *pTestInfo);
        PassFail TestSQLAllocEnv(TestInfo *pTestInfo);
        PassFail TestSQLAllocStmt(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
        PassFail TestSQLBrowseConnect(TestInfo *pTestInfo);
        PassFail TestSQLColAttributes(TestInfo *pTestInfo);
        PassFail TestSQLConnect(TestInfo *pTestInfo);
        PassFail TestSQLDataSources(TestInfo *pTestInfo);
        PassFail TestSQLDescribeCol(TestInfo *pTestInfo);
        PassFail TestSQLDriverConnect(TestInfo *pTestInfo);
        PassFail TestSQLDrivers(TestInfo *pTestInfo);
        PassFail TestSQLError(TestInfo *pTestInfo);
        PassFail TestSQLExecDirect(TestInfo *pTestInfo);
        PassFail TestSQLDescribeParam(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
        PassFail TestSQLExecute(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
        PassFail TestSQLExtendedFetch(TestInfo *pTestInfo);
        PassFail TestSQLFetch(TestInfo *pTestInfo);
        PassFail TestSQLGetFunctions(TestInfo *pTestInfo);
        PassFail TestSQLGetTypeInfo(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
        PassFail TestSQLGetTypeInfoR18(TestInfo *pTestInfo);
        PassFail TestSQLMoreResults(TestInfo *pTestInfo);
        PassFail TestSQLMoreResultsVer3(TestInfo *pTestInfo);
        PassFail TestSQLNativeSql(TestInfo *pTestInfo);
        PassFail TestSQLNumParams(TestInfo *pTestInfo);
        PassFail TestSQLNumResultCols(TestInfo *pTestInfo);
        PassFail TestSQLParamOptions(TestInfo *pTestInfo);
        PassFail TestSQLPrepare(TestInfo *pTestInfo);
        PassFail TestSQLPrimaryKeys(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
        PassFail TestSQLRowCount(TestInfo *pTestInfo);
        PassFail TestSQLSetPos(TestInfo *pTestInfo);
        PassFail TestSQLSetScrollOptions(TestInfo *pTestInfo);
        PassFail TestSQLSetConnectOption(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
        PassFail TestSQLSetCursorName(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
        PassFail TestSQLSetStmtOption(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
        PassFail TestSQLSpecialColumns(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
        PassFail TestSQLStatistics(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
        PassFail TestSQLTransact(TestInfo *pTestInfo);

        // Scalar functions
        PassFail TestMXConvertFunctions(TestInfo *pTestInfo);
        PassFail TestNumericFunctions(TestInfo *pTestInfo);
        PassFail TestStringFunctions(TestInfo *pTestInfo);
        PassFail TestSystemFunctions(TestInfo *pTestInfo);
        PassFail TestMXTimeDateFunctions(TestInfo *pTestInfo);

        // MX Specific APIs
        PassFail TestMXSQLAllocHandle(TestInfo *pTestInfo);
        PassFail TestMXSQLSetConnectAttr(TestInfo *pTestInfo);
        PassFail TestMXSQLEndTran(TestInfo *pTestInfo);
        PassFail TestMXSQLCloseCursor(TestInfo *pTestInfo);
        PassFail TestMXSQLCopyDesc(TestInfo *pTestInfo);
        PassFail TestMXSQLSetEnvAttr(TestInfo *pTestInfo);
        PassFail TestMXSQLGetDescRec(TestInfo *pTestInfo);			//also tests SQLSetDescRec
        PassFail TestMXSQLSetGetDescFields(TestInfo *pTestInfo);
        PassFail TestMXSQLGetDiagRec(TestInfo *pTestInfo);
        PassFail TestMXSQLGetDiagField(TestInfo *pTestInfo);
        PassFail TestMXSQLSetStmtAttr(TestInfo *pTestInfo);
        PassFail TestMXSQLColAttributeVer3(TestInfo *pTestInfo);
        PassFail TestMXSQLBindCol(TestInfo *pTestInfo);
        PassFail TestMXSQLBindColVer3(TestInfo *pTestInfo);
        PassFail TestMXSQLBindParameter(TestInfo *pTestInfo);
        PassFail TestMXSQLBindParameterVer3(TestInfo *pTestInfo);
        PassFail TestMXSQLCancel(TestInfo *pTestInfo);
        PassFail TestMXSQLColAttributes(TestInfo *pTestInfo);
        PassFail TestMXSQLColumnPrivileges(TestInfo *pTestInfo);
        PassFail TestMXSQLColumns(TestInfo *pTestInfo);
        PassFail TestMXSQLDescribeCol(TestInfo *pTestInfo);
        PassFail TestMXSQLDescribeColVer3(TestInfo *pTestInfo);
        PassFail TestMXSQLFetchScroll(TestInfo *pTestInfo);
        PassFail TestMXSQLForeignKeys(TestInfo *pTestInfo);
        PassFail TestMXSQLGetData(TestInfo *pTestInfo);
        PassFail TestMXSQLGetDataVer3(TestInfo *pTestInfo);
        PassFail TestMXSQLGetInfo(TestInfo *pTestInfo);
        PassFail TestMXSQLGetInfoVer3(TestInfo *pTestInfo);
        PassFail TestMXSQLPutData(TestInfo *pTestInfo);
        PassFail TestMXSQLTablePrivileges(TestInfo *pTestInfo);
        PassFail TestMXSQLTables(TestInfo *pTestInfo);
        PassFail TestMXResourceGovern(TestInfo *pTestInfo);

        PassFail TestNOSCreate(TestInfo *pTestInfo, LPCTSTR InputFileString);

        // Interval Data Type Tests
        PassFail TestMXSQLBindParameterInterval(TestInfo *pTestInfo);
        PassFail TestMXSQLBindColInterval(TestInfo *pTestInfo);
        PassFail TestMXSQLGetDataInterval(TestInfo *pTestInfo);

        // Stored Procedures
        PassFail TestMXSQLProcedureColumns(TestInfo *pTestInfo);
        PassFail TestMXSQLProcedures(TestInfo *pTestInfo);
        
        // Partial DateTime Conversions
        PassFail TestMXPartialDateTimeInputConversions(TestInfo *pTestInfo);
        PassFail TestMXPartialDateTimeOutputConversions(TestInfo *pTestInfo);
        PassFail TestMXSQLUnicode(TestInfo *pTestInfo);

		// TRAF and NDCS feature tests.
		PassFail TestQueryID (TestInfo *pTestInfo);
		PassFail TestHash2 (TestInfo *pTestInfo);
		PassFail TestLargeBlock(TestInfo *pTestInfo);
        PassFail TestInfoStats(TestInfo *pTestInfo);
    #else
        extern "C" {
            extern PassFail TestSQLAllocConnect(TestInfo *pTestInfo);
            extern PassFail TestSQLAllocEnv(TestInfo *pTestInfo);
            extern PassFail TestSQLAllocStmt(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
            extern PassFail TestSQLBrowseConnect(TestInfo *pTestInfo);
            extern PassFail TestSQLColAttributes(TestInfo *pTestInfo);
            extern PassFail TestSQLConnect(TestInfo *pTestInfo);
            extern PassFail TestSQLDataSources(TestInfo *pTestInfo);
            extern PassFail TestSQLDescribeCol(TestInfo *pTestInfo);
            extern PassFail TestSQLDriverConnect(TestInfo *pTestInfo);
            extern PassFail TestSQLDrivers(TestInfo *pTestInfo);
            extern PassFail TestSQLError(TestInfo *pTestInfo);
            extern PassFail TestSQLExecDirect(TestInfo *pTestInfo);
            extern PassFail TestSQLDescribeParam(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
            extern PassFail TestSQLExecute(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
            extern PassFail TestSQLExtendedFetch(TestInfo *pTestInfo);
            extern PassFail TestSQLFetch(TestInfo *pTestInfo);
            extern PassFail TestSQLGetFunctions(TestInfo *pTestInfo);
            extern PassFail TestSQLGetTypeInfo(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
            extern PassFail TestSQLGetTypeInfoR18(TestInfo *pTestInfo);
            extern PassFail TestSQLMoreResults(TestInfo *pTestInfo);
            extern PassFail TestSQLMoreResultsVer3(TestInfo *pTestInfo);
            extern PassFail TestSQLNativeSql(TestInfo *pTestInfo);
            extern PassFail TestSQLNumParams(TestInfo *pTestInfo);
            extern PassFail TestSQLNumResultCols(TestInfo *pTestInfo);
            extern PassFail TestSQLParamOptions(TestInfo *pTestInfo);
            extern PassFail TestSQLPrepare(TestInfo *pTestInfo);
            extern PassFail TestSQLPrimaryKeys(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
            extern PassFail TestSQLRowCount(TestInfo *pTestInfo);
            extern PassFail TestSQLSetPos(TestInfo *pTestInfo);
            extern PassFail TestSQLSetScrollOptions(TestInfo *pTestInfo);
            extern PassFail TestSQLSetConnectOption(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
            extern PassFail TestSQLSetCursorName(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
            extern PassFail TestSQLSetStmtOption(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
            extern PassFail TestSQLSpecialColumns(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
            extern PassFail TestSQLStatistics(TestInfo *pTestInfo, int MX_MP_SPECIFIC);
            extern PassFail TestSQLTransact(TestInfo *pTestInfo);

            // Scalar functions
            extern PassFail TestMXConvertFunctions(TestInfo *pTestInfo);
            extern PassFail TestNumericFunctions(TestInfo *pTestInfo);
            extern PassFail TestStringFunctions(TestInfo *pTestInfo);
            extern PassFail TestSystemFunctions(TestInfo *pTestInfo);
            extern PassFail TestMXTimeDateFunctions(TestInfo *pTestInfo);
    
            // MX Specific APIs
            extern PassFail TestMXSQLAllocHandle(TestInfo *pTestInfo);
            extern PassFail TestMXSQLSetConnectAttr(TestInfo *pTestInfo);
            extern PassFail TestMXSQLEndTran(TestInfo *pTestInfo);
            extern PassFail TestMXSQLCloseCursor(TestInfo *pTestInfo);
            extern PassFail TestMXSQLCopyDesc(TestInfo *pTestInfo);
            extern PassFail TestMXSQLSetEnvAttr(TestInfo *pTestInfo);
            extern PassFail TestMXSQLGetDescRec(TestInfo *pTestInfo);			//also tests SQLSetDescRec
            extern PassFail TestMXSQLSetGetDescFields(TestInfo *pTestInfo);
            extern PassFail TestMXSQLGetDiagRec(TestInfo *pTestInfo);
            extern PassFail TestMXSQLGetDiagField(TestInfo *pTestInfo);
            extern PassFail TestMXSQLSetStmtAttr(TestInfo *pTestInfo);
            extern PassFail TestMXSQLColAttributeVer3(TestInfo *pTestInfo);
            extern PassFail TestMXSQLBindCol(TestInfo *pTestInfo);
            extern PassFail TestMXSQLBindColVer3(TestInfo *pTestInfo);
            extern PassFail TestMXSQLBindParameter(TestInfo *pTestInfo);
            extern PassFail TestMXSQLBindParameterVer3(TestInfo *pTestInfo);
            extern PassFail TestMXSQLCancel(TestInfo *pTestInfo);
            extern PassFail TestMXSQLColAttributes(TestInfo *pTestInfo);
            extern PassFail TestMXSQLColumnPrivileges(TestInfo *pTestInfo);
            extern PassFail TestMXSQLColumns(TestInfo *pTestInfo);
            extern PassFail TestMXSQLDescribeCol(TestInfo *pTestInfo);
            extern PassFail TestMXSQLDescribeColVer3(TestInfo *pTestInfo);
            extern PassFail TestMXSQLFetchScroll(TestInfo *pTestInfo);
            extern PassFail TestMXSQLForeignKeys(TestInfo *pTestInfo);
            extern PassFail TestMXSQLGetData(TestInfo *pTestInfo);
            extern PassFail TestMXSQLGetDataVer3(TestInfo *pTestInfo);
            extern PassFail TestMXSQLGetInfo(TestInfo *pTestInfo);
            extern PassFail TestMXSQLGetInfoVer3(TestInfo *pTestInfo);
            extern PassFail TestMXSQLPutData(TestInfo *pTestInfo);
            extern PassFail TestMXSQLTablePrivileges(TestInfo *pTestInfo);
            extern PassFail TestMXSQLTables(TestInfo *pTestInfo);
            extern PassFail TestMXResourceGovern(TestInfo *pTestInfo);

            extern PassFail TestNOSCreate(TestInfo *pTestInfo, LPCTSTR InputFileString);

            // Interval Data Type Tests
            extern PassFail TestMXSQLBindParameterInterval(TestInfo *pTestInfo);
            extern PassFail TestMXSQLBindColInterval(TestInfo *pTestInfo);
            extern PassFail TestMXSQLGetDataInterval(TestInfo *pTestInfo);

            // Stored Procedures
            extern PassFail TestMXSQLProcedureColumns(TestInfo *pTestInfo);
            extern PassFail TestMXSQLProcedures(TestInfo *pTestInfo);

            // Partial DateTime Conversions
            extern PassFail TestMXPartialDateTimeInputConversions(TestInfo *pTestInfo);
            extern PassFail TestMXPartialDateTimeOutputConversions(TestInfo *pTestInfo);
            extern PassFail TestMXSQLUnicode(TestInfo *pTestInfo);

			// TRAF and NDCS feature tests.
			extern PassFail TestQueryID(TestInfo *pTestInfo);
			extern PassFail TestHash2(TestInfo *pTestInfo);
			extern PassFail TestLargeBlock(TestInfo *pTestInfo);
            extern PassFail TestInfoStats(TestInfo *pTestInfo);
        }
        #endif
#endif
#endif
