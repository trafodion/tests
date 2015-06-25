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


#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define NAME_LEN			128+1
#define NUM_OUTPUTS			8
#define REM_LEN				254
#define NUM_PATTERN			5
#define	NUM_PRIVILEGES		5

/*
---------------------------------------------------------
   MX Specific TestSQLColumnPrivileges
---------------------------------------------------------
*/
PassFail TestMXSQLColumnPrivileges( TestInfo *pTestInfo)
{
	TEST_DECLARE;
 	TCHAR			Heading[MAX_HEADING_SIZE];
 	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;

	TCHAR			TableQualifier[NAME_LEN],TableOwner[NAME_LEN],Is_Grantable[4];
	TCHAR			*TableStr;

	TCHAR			*TableName;
	TCHAR			*Grantor;
	TCHAR			oTableQualifier[NAME_LEN];  
	TCHAR			oTableOwner[NAME_LEN];
	TCHAR			oTableName[NAME_LEN];
	TCHAR			oColName[NAME_LEN];
	TCHAR			oGrantor[NAME_LEN]; 
	TCHAR			oGrantee[NAME_LEN];
	TCHAR			oPrivilege[NAME_LEN];
	TCHAR			oIs_Grantable[4];

	SQLLEN		oTableQualifierlen; 
	SQLLEN		oTableOwnerlen;
	SQLLEN		oTableNamelen;
	SQLLEN		oColNamelen;
	SQLLEN		oGrantorlen;
	SQLLEN		oGranteelen;
	SQLLEN		oPrivilegelen;
	SQLLEN		oIs_Grantablelen;
	
	struct
	{
		TCHAR		*Col;
		TCHAR		*ColType;
		TCHAR		*Grantee;
		TCHAR		*Privilege;
	} TableCol[] = {
						{_T("--"),_T("char(10) CHARACTER SET ISO88591"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("--"),_T("varchar(10) CHARACTER SET ISO88591"),_T("DB__ROOT"),_T("UPDATE")},
						{_T("--"),_T("long varchar CHARACTER SET ISO88591"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("--"),_T("decimal(10,5)"),_T("DB__ROOT"),_T("UPDATE")},
						{_T("--"),_T("numeric(10,5)"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("--"),_T("smallint"),_T("DB__ROOT"),_T("UPDATE")},
						{_T("--"),_T("integer"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("--"),_T("bigint"),_T("DB__ROOT"),_T("UPDATE")},
						{_T("--"),_T("real"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("--"),_T("float"),_T("DB__ROOT"),_T("UPDATE")},
						{_T("--"),_T("double precision"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("--"),_T("date"),_T("DB__ROOT"),_T("UPDATE")},
						{_T("--"),_T("time"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("--"),_T("timestamp"),_T("DB__ROOT"),_T("UPDATE")},
						{_T("--"),_T("numeric(19,0)"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("--"),_T("numeric(19,6)"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("--"),_T("numeric(128,0)"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("--"),_T("numeric(128,128)"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("--"),_T("numeric(10,5) unsigned"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("--"),_T("numeric(18,5) unsigned"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("--"),_T("numeric(30,10) unsigned"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("--"),_T("char(10) CHARACTER SET UCS2"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("--"),_T("varchar(10) CHARACTER SET UCS2"),_T("DB__ROOT"),_T("UPDATE")},
						{_T("--"),_T("long varchar CHARACTER SET UCS2"),_T("DB__ROOT"),_T("REFERENCES")},
						{_T("endloop"),}
					};

	struct
	{
		TCHAR		*TabQua;
		TCHAR		*TabOwner;
		TCHAR		*TabName;
		TCHAR		*ColName;
		RETCODE		CheckCode;
	} ColumnWC[] = {								/* wild cards from here */
						{_T("--"),_T("--"),_T("--"),_T("--")},	// Have a row with all valid values here so that 
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_ERROR}, 
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_ERROR}, 
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_SUCCESS}, 
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_ERROR},
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
						{_T("--"),_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
						{_T("endloop"),}
					};

	int	i = 0, k = 0;
//	DWORD	nSize;

    struct {
        TCHAR cat[NAME_LEN];
        TCHAR sch[NAME_LEN];
        TCHAR tab[NAME_LEN];
        TCHAR col[NAME_LEN];
    } displayBuf;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLColumnPrivileges"), charset_file);
	if (var_list == NULL) return FAILED;

	TableName = var_mapping(_T("SQLColumnPrivileges_TableName"), var_list);
	Grantor = var_mapping(_T("SQLColumnPrivileges_Grantor"), var_list);

	TableCol[0].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_0"), var_list);
	TableCol[1].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_1"), var_list);
	TableCol[2].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_2"), var_list);
	TableCol[3].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_3"), var_list);
	TableCol[4].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_4"), var_list);
	TableCol[5].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_5"), var_list);
	TableCol[6].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_6"), var_list);
	TableCol[7].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_7"), var_list);
	TableCol[8].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_8"), var_list);
	TableCol[9].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_9"), var_list);
	TableCol[10].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_10"), var_list);
	TableCol[11].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_11"), var_list);
	TableCol[12].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_12"), var_list);
	TableCol[13].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_13"), var_list);
	TableCol[14].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_14"), var_list);
	TableCol[15].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_15"), var_list);
	TableCol[16].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_16"), var_list);
	TableCol[17].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_17"), var_list);
	TableCol[18].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_18"), var_list);
	TableCol[19].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_19"), var_list);
	TableCol[20].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_20"), var_list);
	TableCol[21].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_21"), var_list);
	TableCol[22].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_22"), var_list);
	TableCol[23].Col = var_mapping(_T("SQLColumnPrivileges_TableCol_Col_23"), var_list);

	ColumnWC[0].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_0"), var_list);
	ColumnWC[0].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_0"), var_list);
	ColumnWC[0].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_0"), var_list);
	ColumnWC[0].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_0"), var_list);

	ColumnWC[1].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_1"), var_list);
	ColumnWC[1].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_1"), var_list);
	ColumnWC[1].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_1"), var_list);
	ColumnWC[1].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_1"), var_list);

	ColumnWC[2].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_2"), var_list);
	ColumnWC[2].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_2"), var_list);
	ColumnWC[2].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_2"), var_list);
	ColumnWC[2].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_2"), var_list);

	ColumnWC[3].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_3"), var_list);
	ColumnWC[3].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_3"), var_list);
	ColumnWC[3].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_3"), var_list);
	ColumnWC[3].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_3"), var_list);

	ColumnWC[4].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_4"), var_list);
	ColumnWC[4].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_4"), var_list);
	ColumnWC[4].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_4"), var_list);
	ColumnWC[4].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_4"), var_list);

	ColumnWC[5].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_5"), var_list);
	ColumnWC[5].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_5"), var_list);
	ColumnWC[5].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_5"), var_list);
	ColumnWC[5].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_5"), var_list);

	ColumnWC[6].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_6"), var_list);
	ColumnWC[6].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_6"), var_list);
	ColumnWC[6].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_6"), var_list);
	ColumnWC[6].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_6"), var_list);

	ColumnWC[7].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_7"), var_list);
	ColumnWC[7].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_7"), var_list);
	ColumnWC[7].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_7"), var_list);
	ColumnWC[7].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_7"), var_list);

	ColumnWC[8].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_8"), var_list);
	ColumnWC[8].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_8"), var_list);
	ColumnWC[8].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_8"), var_list);
	ColumnWC[8].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_8"), var_list);

	ColumnWC[9].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_9"), var_list);
	ColumnWC[9].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_9"), var_list);
	ColumnWC[9].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_9"), var_list);
	ColumnWC[9].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_9"), var_list);

	ColumnWC[10].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_10"), var_list);
	ColumnWC[10].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_10"), var_list);
	ColumnWC[10].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_10"), var_list);
	ColumnWC[10].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_10"), var_list);

	ColumnWC[11].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_11"), var_list);
	ColumnWC[11].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_11"), var_list);
	ColumnWC[11].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_11"), var_list);
	ColumnWC[11].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_11"), var_list);

	ColumnWC[12].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_12"), var_list);
	ColumnWC[12].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_12"), var_list);
	ColumnWC[12].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_12"), var_list);
	ColumnWC[12].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_12"), var_list);

	ColumnWC[13].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_13"), var_list);
	ColumnWC[13].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_13"), var_list);
	ColumnWC[13].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_13"), var_list);
	ColumnWC[13].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_13"), var_list);

	ColumnWC[14].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_14"), var_list);
	ColumnWC[14].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_14"), var_list);
	ColumnWC[14].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_14"), var_list);
	ColumnWC[14].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_14"), var_list);

	ColumnWC[15].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_15"), var_list);
	ColumnWC[15].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_15"), var_list);
	ColumnWC[15].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_15"), var_list);
	ColumnWC[15].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_15"), var_list);

	ColumnWC[16].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_16"), var_list);
	ColumnWC[16].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_16"), var_list);
	ColumnWC[16].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_16"), var_list);
	ColumnWC[16].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_16"), var_list);

	ColumnWC[17].TabQua = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabQua_17"), var_list);
	ColumnWC[17].TabOwner = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabOwner_17"), var_list);
	ColumnWC[17].TabName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_TabName_17"), var_list);
	ColumnWC[17].ColName = var_mapping(_T("SQLColumnPrivileges_ColumnWC_ColName_17"), var_list);

//=================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => MX Specific SQLColumnPrivileges.\n"));

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLColumnPrivileges tests\n");
	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	TESTCASE_END; 
	returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_METADATA_ID,(SQLPOINTER)SQL_TRUE,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}// end of setup

	_tcscpy(TableQualifier,pTestInfo->Catalog);
	_tcscpy(TableOwner,pTestInfo->Schema);

	TableStr = (TCHAR *)malloc(MAX_NOS_SIZE);
	_tcscpy(Is_Grantable, _T(""));

	i = 0;
	while (_tcsicmp(TableCol[i].Col,_T("endloop")) != 0)
	{
		_stprintf(TableStr,_T("drop table %s"),TableName);
		SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);	//Clean up

		_stprintf(TableStr, _T("create table %s (%s %s) no partition;"),TableName,TableCol[i].Col,TableCol[i].ColType);
		_stprintf(Heading,TableStr);
		_tcscat(Heading,_T("\n"));

		TESTCASE_BEGINW(Heading);

		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)TableStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		else
		{
			TESTCASE_END;

			_stprintf(TableStr,_T("GRANT %s ON %s TO \"%s\""),TableCol[i].Privilege,TableName,TableCol[i].Grantee);
			if ((i % 2) == 0)
				_tcscpy(Is_Grantable, _T("YES"));
			else
				_tcscpy(Is_Grantable, _T("NO"));
			if (_tcsicmp(Is_Grantable,_T("YES")) == 0)
				_tcscat(TableStr, _T(" WITH GRANT OPTION"));

			_stprintf(Heading,TableStr);
			_tcscat(Heading,_T("\n"));
			TESTCASE_BEGINW(Heading);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)TableStr,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			TESTCASE_END;

			_stprintf(Heading,_T("Test #%d:"),i);
			TESTCASE_BEGINW(Heading);
			if (_tcslen(TableQualifier) == 0) {
				returncode = SQLColumnPrivileges(hstmt,NULL,0,(SQLTCHAR*)TableOwner,(SWORD)_tcslen(TableOwner),(SQLTCHAR*)TableName,(SWORD)_tcslen(TableName),(SQLTCHAR*)TableCol[i].Col,(SWORD)_tcslen(TableCol[i].Col));
				LogMsg(NONE,_T("SQLColPriv(hstmt,NULL,0,%s, %d, %s, %d, %s, %d)\n"),  (SQLTCHAR*)TableOwner,(SWORD)_tcslen(TableOwner),(SQLTCHAR*)TableName,(SWORD)_tcslen(TableName),(SQLTCHAR*)TableCol[i].Col,(SWORD)_tcslen(TableCol[i].Col));
			} else {
				returncode = SQLColumnPrivileges(hstmt,(SQLTCHAR*)TableQualifier,(SWORD)_tcslen(TableQualifier),(SQLTCHAR*)TableOwner,(SWORD)_tcslen(TableOwner),(SQLTCHAR*)TableName,(SWORD)_tcslen(TableName),(SQLTCHAR*)TableCol[i].Col,(SWORD)_tcslen(TableCol[i].Col));
				LogMsg(NONE,_T("SQLColPriv(hstmt,%s ,%d ,%s, %d, %s, %d, %s, %d)\n"), (SQLTCHAR*)TableQualifier,(SWORD)_tcslen(TableQualifier),(SQLTCHAR*)TableOwner,(SWORD)_tcslen(TableOwner),(SQLTCHAR*)TableName,(SWORD)_tcslen(TableName),(SQLTCHAR*)TableCol[i].Col,(SWORD)_tcslen(TableCol[i].Col));
			}
			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumnPrivileges"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			else
			{
				_tcscpy(oTableQualifier,_T(""));
				_tcscpy(oTableOwner,_T(""));
				_tcscpy(oTableName,_T(""));
				_tcscpy(oColName,_T(""));
				_tcscpy(oGrantor,_T(""));
				_tcscpy(oGrantee,_T(""));
				_tcscpy(oPrivilege,_T(""));
				_tcscpy(oIs_Grantable,_T(""));
				returncode = SQLBindCol(hstmt,1,SQL_C_TCHAR,oTableQualifier,NAME_LEN,&oTableQualifierlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,2,SQL_C_TCHAR,oTableOwner,NAME_LEN,&oTableOwnerlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,3,SQL_C_TCHAR,oTableName,NAME_LEN,&oTableNamelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}

				returncode = SQLBindCol(hstmt,4,SQL_C_TCHAR,oColName,NAME_LEN,&oColNamelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,5,SQL_C_TCHAR,oGrantor,NAME_LEN,&oGrantorlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,6,SQL_C_TCHAR,oGrantee,NAME_LEN,&oGranteelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				
				returncode = SQLBindCol(hstmt,7,SQL_C_TCHAR,oPrivilege,NAME_LEN,&oPrivilegelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,8,SQL_C_TCHAR,oIs_Grantable,NAME_LEN,&oIs_Grantablelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}

				do 
				{
					returncode = SQLFetch(hstmt);

				} while ((returncode == SQL_SUCCESS) &&
					(_tcsicmp(oGrantor,Grantor)));
				
				if((returncode!=SQL_NO_DATA_FOUND) && (!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				else if (returncode == SQL_SUCCESS)
				{
					_stprintf(Heading,_T("\nSQLColumnPrivileges: compare results of columns fetched for following column \n"));
					_tcscat(Heading,_T("The Column Name is ")); 
					_tcscat(Heading,TableCol[i].Col);
					_tcscat(Heading,_T("\n"));
					LogMsg(NONE,Heading);

					if (cwcscmp(TableQualifier,oTableQualifier,TRUE) == 0) {
						LogMsg(NONE,_T("TableQualifier expect: %s and actual: %s are matched\n"),TableQualifier,oTableQualifier);
					}
					else {
						LogMsg(ERRMSG,_T("TableQualifier expect: %s and actual: %s are not matched\n"),TableQualifier,oTableQualifier);
						TEST_FAILED;	
					}

					if (cwcscmp(TableOwner,oTableOwner,TRUE) == 0) {
						LogMsg(NONE,_T("TableOwner expect: %s and actual: %s are matched\n"),TableOwner,oTableOwner);
					}
					else {
						LogMsg(ERRMSG,_T("TableOwner expect: %s and actual: %s are not matched\n"),TableOwner,oTableOwner);
						TEST_FAILED;	
					}

					if(cwcscmp(TableName,oTableName,TRUE) == 0) {
						LogMsg(NONE,_T("TableName expect: %s and actual: %s are matched\n"),TableName,oTableName);
					}
					else {
						LogMsg(ERRMSG,_T("TableName expect: %s and actual: %s are not matched\n"),TableName,oTableName);
						TEST_FAILED;	
					}

					if (cwcscmp(TableCol[i].Col,oColName,TRUE) == 0) {
						LogMsg(NONE,_T("ColName expect: %s and actual: %s are matched\n"),TableCol[i].Col,oColName);
					}
					else {
						LogMsg(ERRMSG,_T("ColName expect: %s and actual: %s are not matched\n"),TableCol[i].Col,oColName);
						TEST_FAILED;	
					}

					if(_tcsicmp(oGrantor,Grantor) == 0) {
						LogMsg(NONE,_T("Grantor expect: %s and actual: %s are matched\n"),Grantor,oGrantor);
					}
					else {
						LogMsg(ERRMSG,_T("Grantor expect: %s and actual: %s are not matched\n"),Grantor,oGrantor);
						TEST_FAILED;	
					}

					if (_tcsicmp(oGrantee,TableCol[i].Grantee) == 0) {
						LogMsg(NONE,_T("Grantee expect: %s and actual: %s are matched\n"),TableCol[i].Grantee,oGrantee);
					}
					else {
						LogMsg(ERRMSG,_T("Grantee expect: %s and actual: %s are not matched\n"),TableCol[i].Grantee,oGrantee);
						TEST_FAILED;	
					}

					if (_tcsicmp(TableCol[i].Privilege,oPrivilege) == 0) {
						LogMsg(NONE,_T("Privilege expect: %s and actual: %s are matched\n"),TableCol[i].Privilege,oPrivilege);
					}
					else {
						LogMsg(ERRMSG,_T("Privilege expect: %s and actual: %s are not matched\n"),TableCol[i].Privilege,oPrivilege);
						TEST_FAILED;	
					}

					if (_tcsicmp(Is_Grantable,oIs_Grantable) == 0) {
						LogMsg(NONE,_T("Is_Grantable expect: %s and actual: %s are matched\n"),Is_Grantable,oIs_Grantable);
					}
					else
					{
						LogMsg(ERRMSG,_T("Is_Grantable expect: %s and actual: %s are not matched\n"),Is_Grantable,oIs_Grantable);
						TEST_FAILED;	
					}
				}
				else
				{
					LogMsg(ERRMSG,_T("No Data Found => Atleast one row should be fetched.\n"));
					TEST_FAILED;
				}
			}
			SQLFreeStmt(hstmt,SQL_UNBIND);
			SQLFreeStmt(hstmt,SQL_CLOSE);
		}
		TESTCASE_END;

		_tcscpy(TableStr,_T(""));
		_stprintf(TableStr,_T("REVOKE %s ON %s FROM \"%s\""),TableCol[i].Privilege,TableName,TableCol[i].Grantee);
		_stprintf(Heading,TableStr);
		_tcscat(Heading,_T("\n"));

		TESTCASE_BEGINW(Heading);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)TableStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;
		_stprintf(TableStr,_T("drop table %s"),TableName);
		SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);
		i++;
	} 
	
//=======================================================================================

	returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_METADATA_ID,(SQLPOINTER)SQL_FALSE,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	i = 0;
	_stprintf(TableStr,_T("drop table %s.%s.%s"),ColumnWC[i].TabQua, ColumnWC[i].TabOwner, ColumnWC[i].TabName);
	SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);
	_stprintf(TableStr,_T("drop schema %s.%s cascade"),ColumnWC[i].TabQua, ColumnWC[i].TabOwner);
	SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
	}
	else
	{
		_stprintf(TableStr,_T("create schema %s.%s"),ColumnWC[i].TabQua, ColumnWC[i].TabOwner);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		else
		{
			_stprintf(TableStr,_T("create table %s.%s.%s(%s char(10)) no partition;"),ColumnWC[i].TabQua, ColumnWC[i].TabOwner, ColumnWC[i].TabName, ColumnWC[i].ColName);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
		}
	}
	if (returncode == SQL_SUCCESS) 
	{
		while (_tcsicmp(ColumnWC[i].TabQua,_T("endloop")) != 0)
		{
			_stprintf(Heading,_T("SQLColumnPrivileges: wildcard options => \nTable Qualifier: %s\n Table Owner: %s\n Table Name: %s\n Column Name: %s \n"),
				printSymbol(ColumnWC[i].TabQua,displayBuf.cat),
                printSymbol(ColumnWC[i].TabOwner,displayBuf.sch),
				printSymbol(ColumnWC[i].TabName,displayBuf.tab),
                printSymbol(ColumnWC[i].ColName,displayBuf.col));
			TESTCASE_BEGINW(Heading);
			if (_tcsicmp(ColumnWC[i].TabQua,_T("NULL")) == 0)
				ColumnWC[i].TabQua = NULL;
			if (_tcsicmp(ColumnWC[i].TabOwner,_T("NULL")) == 0)
				ColumnWC[i].TabOwner = NULL;
			if (_tcsicmp(ColumnWC[i].TabName,_T("NULL")) == 0)
				ColumnWC[i].TabName = NULL;
			if (ColumnWC[i].TabQua == NULL || ColumnWC[i].TabOwner == NULL || ColumnWC[i].TabName == NULL)
				returncode = SQLColumnPrivileges(hstmt,(SQLTCHAR*)ColumnWC[i].TabQua,SQL_NTS,(SQLTCHAR*)ColumnWC[i].TabOwner,SQL_NTS,(SQLTCHAR*)ColumnWC[i].TabName,SQL_NTS,(SQLTCHAR*)removeQuotes(ColumnWC[i].ColName,displayBuf.col),SQL_NTS);
			else
				returncode = SQLColumnPrivileges(hstmt,(SQLTCHAR*)ColumnWC[i].TabQua,(SWORD)_tcslen(ColumnWC[i].TabQua),
													   (SQLTCHAR*)ColumnWC[i].TabOwner,(SWORD)_tcslen(ColumnWC[i].TabOwner),
                                                       (SQLTCHAR*)removeQuotes(ColumnWC[i].TabName,displayBuf.tab),(SWORD)_tcslen(displayBuf.tab),
                                                       (SQLTCHAR*)removeQuotes(ColumnWC[i].ColName,displayBuf.col),(SWORD)_tcslen(displayBuf.col));			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumnPrivileges"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				LogMsg(NONE,_T("SQLColumnPrivileges: SQLColumnPrivileges function call executed correctly.\n"));
				_tcscpy(oTableQualifier,_T(""));
				_tcscpy(oTableOwner,_T(""));
				_tcscpy(oTableName,_T(""));
				_tcscpy(oColName,_T(""));
				_tcscpy(oGrantor,_T(""));
				_tcscpy(oGrantee,_T(""));
				_tcscpy(oPrivilege,_T(""));
				_tcscpy(oIs_Grantable,_T(""));
				returncode = SQLBindCol(hstmt,1,SQL_C_TCHAR,oTableQualifier,NAME_LEN,&oTableQualifierlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				} 

				returncode = SQLBindCol(hstmt,2,SQL_C_TCHAR,oTableOwner,NAME_LEN,&oTableOwnerlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,3,SQL_C_TCHAR,oTableName,NAME_LEN,&oTableNamelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}

				returncode = SQLBindCol(hstmt,4,SQL_C_TCHAR,oColName,NAME_LEN,&oColNamelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,5,SQL_C_TCHAR,oGrantor,NAME_LEN,&oGrantorlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,6,SQL_C_TCHAR,oGrantee,NAME_LEN,&oGranteelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				
				returncode = SQLBindCol(hstmt,7,SQL_C_TCHAR,oPrivilege,NAME_LEN,&oPrivilegelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,8,SQL_C_TCHAR,oIs_Grantable,NAME_LEN,&oIs_Grantablelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				k = 0;
				while (returncode == SQL_SUCCESS) 
				{
					returncode = SQLFetch(hstmt);
					if((returncode!=SQL_NO_DATA_FOUND) && (!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					if (returncode == SQL_SUCCESS)
						k++;
				}
				if(k == 0 && ColumnWC[i].CheckCode == SQL_SUCCESS)
				{
					TEST_FAILED;
					LogMsg(ERRMSG,_T("No Data Found => Atleast one row should be fetched\n"));
				} else {
                    LogMsg(NONE,_T("Number of rows fetched: %d\n"), k);
                }
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			TESTCASE_END;
			i++;
		}
	}


	// Cleanup
	i = 0;
	_stprintf(TableStr,_T("drop table %s.%s.%s"),ColumnWC[i].TabQua, ColumnWC[i].TabOwner, ColumnWC[i].TabName);
	SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);
	_stprintf(TableStr,_T("drop schema %s.%s cascade"),ColumnWC[i].TabQua, ColumnWC[i].TabOwner);
	SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);

//==================================================================================================

	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => MX Specific SQLColumnPrivileges.\n"));
	free(TableStr);
	free_list(var_list);
	TEST_RETURN;
}
