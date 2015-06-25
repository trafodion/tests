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

/* Need to make sure that the ID used here as SQ_GRANTEE is
 *           registered on the target system.  There is a script
 *           src/scripts/regLDAPuser.sql that can be obeyed from sqlci
 *           on the target, if the IDs have not been registered.
 */
/* SQ */ #define SQ_GRANTEE "QAUSER_EXECS" /* "DB__ROOT" */

#define NAME_LEN		300
#define NUM_TABPRIV_OUTPUTS	8
#define REM_LEN		254
#define NUM_PATTERN	5
#define COLNAME_LEN		128
#define	RGB_MAX_LEN		50
#define STR_LEN     258    //added to test SQLBindCols and SQLFetch
#define TOTALATTRIBS			18


/*
---------------------------------------------------------
   TestSQLTablePrivileges
---------------------------------------------------------
*/
PassFail TestMXSQLTablePrivileges( TestInfo *pTestInfo)
{
	TEST_DECLARE;
 	TCHAR			Heading[MAX_HEADING_SIZE];
 	RETCODE			returncode;
 	SQLHANDLE 		henv = (SQLHANDLE)NULL;
 	SQLHANDLE 		hdbc = (SQLHANDLE)NULL;
 	SQLHANDLE		hstmt = (SQLHANDLE)NULL, hstmt1 = (SQLHANDLE)NULL;
	TCHAR			TableQualifier[NAME_LEN],TableOwner[NAME_LEN],*TableStr;

	TCHAR			*TableName;
	TCHAR			*Grantor; //Assume that we log on as role.user

	TCHAR			oTableQualifier[NAME_LEN];  
	TCHAR			oTableOwner[NAME_LEN];
	TCHAR			oTableName[NAME_LEN];
	TCHAR			oGrantor[NAME_LEN];
	TCHAR			oGrantee[NAME_LEN];
	TCHAR			oPrivilege[NAME_LEN];
	TCHAR			oIs_Grantable[3];

	SQLLEN		oTableQualifierlen;
	SQLLEN		oTableOwnerlen;
	SQLLEN		oTableNamelen;
	SQLLEN		oGrantorlen;
	SQLLEN		oGranteelen;
	SQLLEN		oPrivilegelen;
	SQLLEN		oIs_Grantablelen;

	struct
	{
		TCHAR		*Col;
		TCHAR		*Grantee;
		TCHAR		*Is_Grantable;
		TCHAR		*Privilege;
	} TableCol[] = {
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("DELETE")},
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("DELETE,SELECT")},
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("SELECT")},
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("DELETE")},
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("INSERT")},
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("UPDATE")},
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("REFERENCES")},
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("SELECT")},
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("INSERT")},
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("REFERENCES")},
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("UPDATE")},
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("REFERENCES")},
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("UPDATE")},
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("INSERT"),},
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("SELECT")},
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("REFERENCES,SELECT")},
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("DELETE,INSERT,SELECT")},
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("INSERT,REFERENCES,UPDATE")},
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("SELECT,DELETE,INSERT,UPDATE")},
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("DELETE,INSERT,REFERENCES,UPDATE"),},
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("DELETE,INSERT,REFERENCES,SELECT,UPDATE")},

		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("DELETE")},					//char UCS2
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("SELECT")},					//varchar UCS2
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("DELETE")},					//long varchar UCS2

		#ifdef UNICODE
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("DELETE")},					//char utf8
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("SELECT")},					//varchar utf8
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("DELETE")},					//long varchar utf8
		#endif
		//Bignum
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("DELETE")},						//Bignum
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("SELECT")},						//Bignum
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("INSERT")},						//Bignum
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("UPDATE")},						//Bignum
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("REFERENCES")},					//Bignum
		{_T("--"),_T(SQ_GRANTEE),_T("YES"),_T("SELECT,DELETE,INSERT,UPDATE")},	//Bignum
		{_T("--"),_T(SQ_GRANTEE),_T("NO"),_T("INSERT,REFERENCES,UPDATE")},		//Bignum
		{_T("endloop"),}
	};

	struct
	{
		TCHAR		*TabQua;
		TCHAR		*TabOwner;
		TCHAR		*TabName;
		RETCODE		CheckCode;
	} ColumnWC[] = {								// wild cards from here 
							{_T("--"),_T("--"),_T("--"), SQL_SUCCESS},// Have a row with all valid values here so that 
							{_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
							{_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
							{_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
							{_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
							{_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
							{_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
							{_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
							{_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
							{_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
							{_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
							{_T("--"),_T("--"),_T("--"), SQL_SUCCESS},
							{_T("--"),_T("--"),_T("--"), SQL_ERROR},
							{_T("--"),_T("--"),_T("--"), SQL_ERROR},
							{_T("--"),_T("--"),_T("--"), SQL_ERROR},
							{_T("--"),_T("--"),_T("--"), SQL_ERROR},
							{_T("--"),_T("--"),_T("--"), SQL_ERROR}, 
							{_T("--"),_T("--"),_T("--"), SQL_ERROR}, 
							{_T("--"),_T("--"),_T("--"), SQL_ERROR}, 
							{_T("--"),_T("--"),_T("--"), SQL_ERROR},
							{_T("endloop"),}
						};

	struct
	{
		TCHAR		*TabQua;
		SWORD		TabQuaLen;
		TCHAR		*TabOwner;
		SWORD		TabOwnerLen;
		TCHAR		*TabName;
		SWORD		TabNameLen;
		TCHAR		*ColName;
		SWORD		ColNameLen;
	} ColumnWC2[] = {								//	wild cards from here
							{_T("--"), (SWORD)-1, _T("--"),(SWORD)-1, _T("--"),(SWORD)-1, _T(""), (SWORD)-1},
							{_T("--"), (SWORD)4,  _T("--"),(SWORD)2,  _T("--"),(SWORD)2,  _T(""), (SWORD)2},
//							{"TEST_CATALOG", (SWORD)0, "TEST_SCHEMA",(SWORD)0, "TEST_TABLE",(SWORD)0, _T(""), (SWORD)0},
							{_T("endloop"),}
						};

	int cols;
	int	iatt;
	SWORD numOfCols = 0;
	SWORD pcbDesc;
	SQLLEN pfDesc;
	TCHAR cn[COLNAME_LEN];
	SWORD cl;
	SWORD st;
	SQLULEN cp;
	SWORD cs, cnull;
	TCHAR rgbDesc[RGB_MAX_LEN];
	TCHAR *CharOutput[12];
	SQLLEN stringlength;	//	Attributes for columns added for negative testing
	UWORD DescrType[] = 
				{
					SQL_COLUMN_AUTO_INCREMENT,SQL_COLUMN_CASE_SENSITIVE,SQL_COLUMN_COUNT,
					SQL_COLUMN_DISPLAY_SIZE,SQL_COLUMN_LENGTH,SQL_COLUMN_MONEY,
					SQL_COLUMN_NULLABLE,SQL_COLUMN_PRECISION,SQL_COLUMN_SCALE,
					SQL_COLUMN_SEARCHABLE,SQL_COLUMN_TYPE,SQL_COLUMN_UNSIGNED,
					SQL_COLUMN_UPDATABLE,SQL_COLUMN_NAME,SQL_COLUMN_TYPE_NAME,
					SQL_COLUMN_OWNER_NAME,SQL_COLUMN_QUALIFIER_NAME,SQL_COLUMN_TABLE_NAME,
					SQL_COLUMN_LABEL
				};

	TCHAR	*TestColumn;
	int		i = 0, k = 0;

    struct {
        TCHAR cat[STR_LEN];
        TCHAR sch[STR_LEN];
        TCHAR tab[STR_LEN];
    } displayBuf;

//	DWORD	nSize;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLTablePrivileges"), charset_file);
	if (var_list == NULL) return FAILED;

	TableName = var_mapping(_T("SQLTablePrivileges_TableName"), var_list);
	Grantor = var_mapping(_T("SQLTablePrivileges_Grantor"), var_list);
	TestColumn = var_mapping(_T("SQLTablePrivileges_TestColumn"), var_list);

	TableCol[0].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_0"), var_list);
	TableCol[1].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_1"), var_list);
	TableCol[2].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_2"), var_list);
	TableCol[3].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_3"), var_list);
	TableCol[4].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_4"), var_list);
	TableCol[5].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_5"), var_list);
	TableCol[6].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_6"), var_list);
	TableCol[7].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_7"), var_list);
	TableCol[8].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_8"), var_list);
	TableCol[9].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_9"), var_list);
	TableCol[10].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_10"), var_list);
	TableCol[11].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_11"), var_list);
	TableCol[12].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_12"), var_list);
	TableCol[13].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_13"), var_list);
	TableCol[14].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_14"), var_list);
	TableCol[15].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_15"), var_list);
	TableCol[16].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_16"), var_list);
	TableCol[17].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_17"), var_list);
	TableCol[18].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_18"), var_list);
	TableCol[19].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_19"), var_list);
	TableCol[20].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_20"), var_list);
	TableCol[21].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_21"), var_list);
	TableCol[22].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_22"), var_list);
	TableCol[23].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_23"), var_list);
#ifdef UNICODE
	TableCol[24].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_24"), var_list);
	TableCol[25].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_25"), var_list);
	TableCol[26].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_26"), var_list);
	TableCol[27].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_27"), var_list);
	TableCol[28].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_28"), var_list);
	TableCol[29].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_29"), var_list);
	TableCol[30].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_30"), var_list);
	TableCol[31].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_31"), var_list);
	TableCol[32].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_32"), var_list);
	TableCol[33].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_33"), var_list);
#else
	TableCol[24].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_24"), var_list);
	TableCol[25].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_25"), var_list);
	TableCol[26].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_26"), var_list);
	TableCol[27].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_27"), var_list);
	TableCol[28].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_28"), var_list);
	TableCol[29].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_29"), var_list);
	TableCol[30].Col = var_mapping(_T("SQLTablePrivileges_TableCol_Col_30"), var_list);
#endif


	ColumnWC[0].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_0"), var_list);
	ColumnWC[0].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_0"), var_list);
	ColumnWC[0].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_0"), var_list);

	ColumnWC[1].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_1"), var_list);
	ColumnWC[1].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_1"), var_list);
	ColumnWC[1].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_1"), var_list);

	ColumnWC[2].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_2"), var_list);
	ColumnWC[2].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_2"), var_list);
	ColumnWC[2].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_2"), var_list);

	ColumnWC[3].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_3"), var_list);
	ColumnWC[3].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_3"), var_list);
	ColumnWC[3].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_3"), var_list);

	ColumnWC[4].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_4"), var_list);
	ColumnWC[4].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_4"), var_list);
	ColumnWC[4].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_4"), var_list);

	ColumnWC[5].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_5"), var_list);
	ColumnWC[5].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_5"), var_list);
	ColumnWC[5].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_5"), var_list);

	ColumnWC[6].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_6"), var_list);
	ColumnWC[6].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_6"), var_list);
	ColumnWC[6].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_6"), var_list);

	ColumnWC[7].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_7"), var_list);
	ColumnWC[7].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_7"), var_list);
	ColumnWC[7].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_7"), var_list);

	ColumnWC[8].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_8"), var_list);
	ColumnWC[8].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_8"), var_list);
	ColumnWC[8].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_8"), var_list);

	ColumnWC[9].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_9"), var_list);
	ColumnWC[9].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_9"), var_list);
	ColumnWC[9].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_9"), var_list);

	ColumnWC[10].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_10"), var_list);
	ColumnWC[10].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_10"), var_list);
	ColumnWC[10].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_10"), var_list);

	ColumnWC[11].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_11"), var_list);
	ColumnWC[11].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_11"), var_list);
	ColumnWC[11].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_11"), var_list);

	ColumnWC[12].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_12"), var_list);
	ColumnWC[12].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_12"), var_list);
	ColumnWC[12].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_12"), var_list);

	ColumnWC[13].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_13"), var_list);
	ColumnWC[13].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_13"), var_list);
	ColumnWC[13].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_13"), var_list);

	ColumnWC[14].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_14"), var_list);
	ColumnWC[14].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_14"), var_list);
	ColumnWC[14].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_14"), var_list);

	ColumnWC[15].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_15"), var_list);
	ColumnWC[15].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_15"), var_list);
	ColumnWC[15].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_15"), var_list);

	ColumnWC[16].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_16"), var_list);
	ColumnWC[16].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_16"), var_list);
	ColumnWC[16].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_16"), var_list);

	ColumnWC[17].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_17"), var_list);
	ColumnWC[17].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_17"), var_list);
	ColumnWC[17].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_17"), var_list);

	ColumnWC[18].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_18"), var_list);
	ColumnWC[18].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_18"), var_list);
	ColumnWC[18].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_18"), var_list);

	ColumnWC[19].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabQua_19"), var_list);
	ColumnWC[19].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabOwner_19"), var_list);
	ColumnWC[19].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC_TabName_19"), var_list);

	ColumnWC2[0].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC2_TabQua_0"), var_list);
	ColumnWC2[0].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC2_TabOwner_0"), var_list);
	ColumnWC2[0].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC2_TabName_0"), var_list);

	ColumnWC2[1].TabQua = var_mapping(_T("SQLTablePrivileges_ColumnWC2_TabQua_1"), var_list);
	ColumnWC2[1].TabOwner = var_mapping(_T("SQLTablePrivileges_ColumnWC2_TabOwner_1"), var_list);
	ColumnWC2[1].TabName = var_mapping(_T("SQLTablePrivileges_ColumnWC2_TabName_1"), var_list);

//=================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => SQLTablePrivileges.\n"));


	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLTablePrivileges tests\n");

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

	TESTCASE_END;  // end of setup
 
	_tcscpy(TableQualifier,pTestInfo->Catalog);
	_tcscpy(TableOwner,pTestInfo->Schema);

	returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_METADATA_ID,(SQLPOINTER)SQL_TRUE,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}

	TableStr = (TCHAR *)malloc(MAX_NOS_SIZE);
	i = 0;
	while (_tcsicmp(TableCol[i].Col,_T("endloop")) != 0)
	{
		_stprintf(Heading,_T("Test #%d\n"),i);
		TESTCASE_BEGINW(Heading);

		if (_tcsicmp(TableCol[i].Privilege,_T("ALL PRIVILEGES")) == 0)
			_tcscpy(TableCol[i].Privilege,_T("DELETE"));

		// clean up left over table, if any.  We don't care about returncode from SQLExecDirect
		_stprintf(TableStr,_T("drop table %s"),TableName);
		SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);
		
		// create table to test against
		_stprintf(TableStr,_T("create table %s (%s) no partition;"),TableName,TableCol[i].Col);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)TableStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		else
		{
			// execute GRANT statement to set up some table privileges
			_stprintf(TableStr,_T("GRANT %s ON %s TO \"%s\""),TableCol[i].Privilege,TableName,TableCol[i].Grantee);
			if (_tcsicmp(TableCol[i].Is_Grantable,_T("YES")) == 0)
				_tcscat(TableStr, _T(" WITH GRANT OPTION"));
			LogMsg(NONE,_T("%s\n"),TableStr);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)TableStr,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}
			else
			{
				// Execute SQLTablePrivileges for test table
				if (_tcslen(TableQualifier) == 0)
					returncode = SQLTablePrivileges(hstmt,NULL,0,(SQLTCHAR*)TableOwner,(SWORD)_tcslen(TableOwner),(SQLTCHAR*)TableName,(SWORD)_tcslen(TableName));
				else
					returncode = SQLTablePrivileges(hstmt,(SQLTCHAR*)TableQualifier,(SWORD)_tcslen(TableQualifier),(SQLTCHAR*)TableOwner,(SWORD)_tcslen(TableOwner),(SQLTCHAR*)TableName,(SWORD)_tcslen(TableName));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLTablePrivileges"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				else
				{
					LogMsg(NONE,_T("SQLTablePrivileges function call executed correctly.\n"));

					// clear all buffers
					_tcscpy(oTableQualifier,_T(""));
					_tcscpy(oTableOwner,_T(""));
					_tcscpy(oTableName,_T(""));
					_tcscpy(oGrantor,_T(""));
					_tcscpy(oGrantee,_T(""));
					_tcscpy(oPrivilege,_T(""));
					_tcscpy(oIs_Grantable,_T(""));

					// Bind all columns to recieve data returned from SQLTablePrivileges
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
					returncode = SQLBindCol(hstmt,4,SQL_C_TCHAR,oGrantor,NAME_LEN,&oGrantorlen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,5,SQL_C_TCHAR,oGrantee,NAME_LEN,&oGranteelen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,6,SQL_C_TCHAR,oPrivilege,NAME_LEN,&oPrivilegelen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
					}
					returncode = SQLBindCol(hstmt,7,SQL_C_TCHAR,oIs_Grantable,NAME_LEN,&oIs_Grantablelen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
					}
					
					
					// Loop, reading and checking all data retuned from SQLTablePrivileges call
					k = 0;
					while (returncode == SQL_SUCCESS)
					{
						returncode = SQLFetch(hstmt);
						if((returncode!=SQL_NO_DATA_FOUND) && (!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
						{
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
						}
						else 
						{
							// check for SQL_SUCCESS in case SQL_NO_DATA_FOUND was what was returned
							// compare results for rows where oGrantor is not the same as Grantor (DB__ROOT)
							if ((returncode == SQL_SUCCESS) && (_tcsicmp(Grantor,oGrantor) == 0) && (_tcsicmp(TableCol[i].Grantee,oGrantee) == 0))
							{
								k++;	// found a match, increment counter

								if ((_tcsicmp(TableQualifier,oTableQualifier) == 0) 
									&& (cwcscmp(TableOwner,oTableOwner,TRUE) == 0) 
									&& (cwcscmp(TableName,oTableName,TRUE) == 0) 
									//&& (_tcsicmp(oGrantor,Grantor) == 0) 
									//&& (_tcsicmp(TableCol[i].Grantee,oGrantee) == 0) // NOT NEEDED
									&& (_tcsstr(TableCol[i].Privilege,oPrivilege) != NULL) 
									&& (_tcsicmp(TableCol[i].Is_Grantable,oIs_Grantable) == 0) )
								{
									LogMsg(NONE,_T("SQLTablePrivileges: compare results of rows fetched for following column.\n"));
									LogMsg(NONE,_T("TableQualifier expect: %s and actual: %s are matched\n"),TableQualifier,oTableQualifier);
									LogMsg(NONE,_T("TableOwner expect: %s and actual: %s are matched\n"),TableOwner,oTableOwner);
									LogMsg(NONE,_T("TableName expect: %s and actual: %s are matched\n"),TableName,oTableName);
									LogMsg(NONE,_T("Grantor expect: %s and actual: %s are matched\n"),Grantor,oGrantor);
									LogMsg(NONE,_T("Grantee expect: %s and actual: %s are matched\n"),TableCol[i].Grantee,oGrantee);
									LogMsg(NONE,_T("Privilege expect: %s and actual: %s are matched\n"),TableCol[i].Privilege,oPrivilege);
									LogMsg(NONE,_T("Is_Grantable expect: %s and actual: %s are matched\n"),TableCol[i].Is_Grantable,oIs_Grantable);
								}
								else
								{
									TEST_FAILED;	
									LogMsg(NONE,_T("SQLTablePrivileges: compare results of rows fetched for following column.\n"));
									if (_tcsicmp(TableQualifier,oTableQualifier) != 0)
										LogMsg(ERRMSG,_T("TableQualifier expect: %s and actual: %s are not matched\n"),TableQualifier,oTableQualifier);
									if (cwcscmp(TableOwner,oTableOwner,TRUE) != 0) 
										LogMsg(ERRMSG,_T("TableOwner expect: %s and actual: %s are not matched\n"),TableOwner,oTableOwner);
									if (cwcscmp(TableName,oTableName,TRUE) != 0) 
										LogMsg(ERRMSG,_T("TableName expect: %s and actual: %s are not matched\n"),TableName,oTableName);
									//if (_tcsicmp(oGrantor,Grantor) != 0)
									//	LogMsg(ERRMSG,_T("Grantor expect: %s and actual: %s are not matched\n"),Grantor,oGrantor);
									//if (_tcsicmp(TableCol[i].Grantee,oGrantee) != 0)
									//	LogMsg(ERRMSG,_T("Grantee expect: %s and actual: %s are not matched\n"),TableCol[i].Grantee,oGrantee);
									if (_tcsstr(TableCol[i].Privilege,oPrivilege) == NULL)
										LogMsg(ERRMSG,_T("Privilege expect: %s and actual: %s are not matched\n"),TableCol[i].Privilege,oPrivilege);
									if (_tcsicmp(TableCol[i].Is_Grantable,oIs_Grantable) != 0)
										LogMsg(ERRMSG,_T("Is_Grantable expect: %s and actual: %s are not matched\n"),TableCol[i].Is_Grantable,oIs_Grantable);
								}
							}
						}
					}
					if(k == 0){
						TEST_FAILED;
						LogMsg(ERRMSG,_T("No matching grantee record for '%s' found\n   At least one row fetched should have matched\n"),
										  TableCol[i].Grantee);
						}
					SQLFreeStmt(hstmt,SQL_UNBIND);
					SQLFreeStmt(hstmt,SQL_CLOSE);
				}
			}
		}
		TESTCASE_END;
		
		// clean up SQL table
		_stprintf(TableStr,_T("drop table %s"),TableName);
		SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);
		i++;
	} 

	returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_METADATA_ID,(SQLPOINTER)SQL_FALSE,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}

//=======================================================================================

	i = 0;
	_stprintf(TableStr,_T("drop table %s.%s.%s"),ColumnWC[i].TabQua, ColumnWC[i].TabOwner, ColumnWC[i].TabName);
	SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);
	LogMsg(NONE,_T("%s\n"),TableStr);
	_stprintf(TableStr,_T("drop schema %s.%s cascade"),ColumnWC[i].TabQua, ColumnWC[i].TabOwner);
	SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);
	LogMsg(NONE,_T("%s\n"),TableStr);

	_stprintf(TableStr,_T("create schema %s.%s"),ColumnWC[i].TabQua, ColumnWC[i].TabOwner);
	LogMsg(NONE,_T("%s\n"),TableStr);
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
	}
	else
	{
		_stprintf(TableStr,_T("create table %s.%s.%s(%s char(10)) no partition;"),ColumnWC[i].TabQua, ColumnWC[i].TabOwner, ColumnWC[i].TabName, TestColumn);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
	}
	LogMsg(NONE,_T("%s\n"),TableStr);
	returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_METADATA_ID,(SQLPOINTER)SQL_FALSE,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}// end of setup
	if (returncode == SQL_SUCCESS) 
	{
		while (_tcsicmp(ColumnWC[i].TabQua,_T("endloop")) != 0)
		{
			_stprintf(Heading,_T("SQLTablePrivileges: wildcard options => \nTable Qualifier: %s \nTable Owner: %s \nTable Name: %s\n"), 
				printSymbol(ColumnWC[i].TabQua,displayBuf.cat), 
				printSymbol(ColumnWC[i].TabOwner,displayBuf.sch), 
				printSymbol(ColumnWC[i].TabName,displayBuf.tab));
			TESTCASE_BEGINW(Heading);
			if (_tcsicmp(ColumnWC[i].TabQua,_T("NULL")) == 0)
				ColumnWC[i].TabQua = NULL;
			if (_tcsicmp(ColumnWC[i].TabOwner,_T("NULL")) == 0)
				ColumnWC[i].TabOwner = NULL;
			if (_tcsicmp(ColumnWC[i].TabName,_T("NULL")) == 0)
				ColumnWC[i].TabName = NULL;

			if (ColumnWC[i].TabQua == NULL || ColumnWC[i].TabOwner == NULL || ColumnWC[i].TabName == NULL)
				returncode = SQLTablePrivileges(hstmt,(SQLTCHAR*)ColumnWC[i].TabQua,SQL_NTS,(SQLTCHAR*)ColumnWC[i].TabOwner,SQL_NTS,(SQLTCHAR*)removeQuotes(ColumnWC[i].TabName,displayBuf.tab),SQL_NTS);
			else
				returncode = SQLTablePrivileges(hstmt,(SQLTCHAR*)ColumnWC[i].TabQua,(SWORD)_tcslen(ColumnWC[i].TabQua),(SQLTCHAR*)ColumnWC[i].TabOwner,(SWORD)_tcslen(ColumnWC[i].TabOwner),(SQLTCHAR*)removeQuotes(ColumnWC[i].TabName,displayBuf.tab),(SWORD)_tcslen(displayBuf.tab));
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLTablePrivileges"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				LogMsg(NONE,_T("SQLTablePrivileges: SQLTablePrivileges function call executed correctly.\n"));
				_tcscpy(oTableQualifier,_T(""));
				_tcscpy(oTableOwner,_T(""));
				_tcscpy(oTableName,_T(""));
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

				returncode = SQLBindCol(hstmt,4,SQL_C_TCHAR,oGrantor,NAME_LEN,&oGrantorlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,5,SQL_C_TCHAR,oGrantee,NAME_LEN,&oGranteelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				
				returncode = SQLBindCol(hstmt,6,SQL_C_TCHAR,oPrivilege,NAME_LEN,&oPrivilegelen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,7,SQL_C_TCHAR,oIs_Grantable,NAME_LEN,&oIs_Grantablelen);
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
				}
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			TESTCASE_END;
			i++;
		}
	}

//======================================================================================================

	TESTCASE_BEGIN("SQLTablePrivileges: Negative test with invalid handle.\n");

	i = 0;
	returncode = SQLTablePrivileges(hstmt1,(SQLTCHAR*)ColumnWC[i].TabQua,(SWORD)_tcslen(ColumnWC[i].TabQua),(SQLTCHAR*)ColumnWC[i].TabOwner,(SWORD)_tcslen(ColumnWC[i].TabOwner),(SQLTCHAR*)ColumnWC[i].TabName,(SWORD)_tcslen(ColumnWC[i].TabName));
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLTables"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

//=========================================================================================

	TESTCASE_BEGIN("SQLTables: Negative test with NULL handle.\n");

	hstmt1 = (SQLHANDLE)NULL;
	i = 0;
	returncode = SQLTablePrivileges(hstmt1,(SQLTCHAR*)ColumnWC[i].TabQua,(SWORD)_tcslen(ColumnWC[i].TabQua),(SQLTCHAR*)ColumnWC[i].TabOwner,(SWORD)_tcslen(ColumnWC[i].TabOwner),(SQLTCHAR*)ColumnWC[i].TabName,(SWORD)_tcslen(ColumnWC[i].TabName));
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLTables"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

//=========================================================================================

	TESTCASE_BEGIN("SQLTablePrivileges: Negative test with invalid arg lengths.\n");

	returncode = SQLTablePrivileges(hstmt,(SQLTCHAR*)ColumnWC2[0].TabQua,ColumnWC2[0].TabQuaLen,(SQLTCHAR*)ColumnWC2[0].TabOwner,ColumnWC2[0].TabOwnerLen,(SQLTCHAR*)ColumnWC2[0].TabName,ColumnWC2[0].TabNameLen);
	LogMsg(NONE, _T("Input parameters: CatalogLen %d SchemaLen %d TableLen %d\n"), ColumnWC2[0].TabQuaLen, ColumnWC2[0].TabOwnerLen, ColumnWC2[0].TabNameLen);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLTablePrivileges"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}

	TESTCASE_END;

//=========================================================================================

	TESTCASE_BEGIN("SQLTablePrivileges: Positive test with invalid arg lengths.\n");

	returncode = SQLTablePrivileges(hstmt,(SQLTCHAR*)ColumnWC2[1].TabQua,ColumnWC2[1].TabQuaLen,(SQLTCHAR*)ColumnWC2[1].TabOwner,ColumnWC2[1].TabOwnerLen,(SQLTCHAR*)ColumnWC2[1].TabName,ColumnWC2[1].TabNameLen);
	LogMsg(NONE, _T("Input parameters: CatalogLen %d SchemaLen %d TableLen %d\n"), ColumnWC2[1].TabQuaLen, ColumnWC2[1].TabOwnerLen, ColumnWC2[1].TabNameLen);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLTablePrivileges"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	else {
		LogMsg(NONE,_T("SQLTablePrivileges: SQLTablePrivileges function call executed correctly.\n"));
		_tcscpy(oTableQualifier,_T(""));
		_tcscpy(oTableOwner,_T(""));
		_tcscpy(oTableName,_T(""));
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
		returncode = SQLBindCol(hstmt,4,SQL_C_TCHAR,oGrantor,NAME_LEN,&oGrantorlen);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
		{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
		}
		returncode = SQLBindCol(hstmt,5,SQL_C_TCHAR,oGrantee,NAME_LEN,&oGranteelen);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
		{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
		}
		
		returncode = SQLBindCol(hstmt,6,SQL_C_TCHAR,oPrivilege,NAME_LEN,&oPrivilegelen);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
		{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
		}
		returncode = SQLBindCol(hstmt,7,SQL_C_TCHAR,oIs_Grantable,NAME_LEN,&oIs_Grantablelen);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
		{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
		}
		k = 0;
		while (returncode == SQL_SUCCESS) 
		{
			returncode = SQLFetch(hstmt);
			if (returncode == SQL_SUCCESS) k++;
		}
		if(k > 0)
		{
			TEST_FAILED;
			LogMsg(ERRMSG,_T("Should be no data found - check for similar objects unintentionally appear\n"));
		}
	}

	TESTCASE_END;

//=========================================================================================

	TESTCASE_BEGIN("Testing SQLColAttribute, SQLDescribeCol, SQLBindCol and SQLFetch functions for catalog names.\n");

	returncode = SQLSetStmtAttr(hstmt,SQL_ATTR_METADATA_ID,(SQLPOINTER)SQL_FALSE,0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}// end of setup

	for(i = 0; i < 5; i++)
	{
		_stprintf(Heading,_T("======================================\nSQLTablePrivileges: wildcard options => \nTable Qualifier: %s \nTable Owner: %s \nTable Name: %s\n"), 
						printSymbol(ColumnWC[i].TabQua,displayBuf.cat), 
						printSymbol(ColumnWC[i].TabOwner,displayBuf.sch), 
						printSymbol(ColumnWC[i].TabName,displayBuf.tab));
		LogMsg(NONE,Heading);

		returncode = SQLTablePrivileges(hstmt,(SQLTCHAR*)ColumnWC[i].TabQua,(SWORD)_tcslen(ColumnWC[i].TabQua),
											  (SQLTCHAR*)removeQuotes(ColumnWC[i].TabOwner, displayBuf.sch),(SWORD)_tcslen(displayBuf.sch),
											  (SQLTCHAR*)removeQuotes(ColumnWC[i].TabName, displayBuf.tab),(SWORD)_tcslen(displayBuf.tab));
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColumns"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		LogMsg(NONE,_T("after the call\n"));

		returncode = SQLNumResultCols(hstmt, &numOfCols);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultsCol"))
		{
			TEST_FAILED;
			LogMsg(ERRMSG,_T("Test failed while executing call for SQLNUMRESULTSCOL"));
			LogAllErrors(henv,hdbc,hstmt);
		}
		for(cols = 0; cols < numOfCols; cols++)
		{
			returncode = SQLDescribeCol(hstmt,(SWORD)(cols+1),(SQLTCHAR*)cn,COLNAME_LEN,&cl,&st,&cp,&cs,&cnull);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDescribeCol"))
			{
				TEST_FAILED;
				LogMsg(ERRMSG,_T("Test failed while executing call for SQLDESCRIBECOL of column"));
				LogAllErrors(henv,hdbc,hstmt);
			}
			CharOutput[cols] = (TCHAR *)malloc(STR_LEN);
			for (iatt = 0; iatt <= TOTALATTRIBS; iatt++)
			{
				_tcscpy(rgbDesc,_T(""));
				pcbDesc = 0;
				pfDesc = 0;
				returncode = SQLColAttributes(hstmt,(SWORD)(cols+1),DescrType[iatt],rgbDesc,STR_LEN,&pcbDesc,&pfDesc);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColAttribute"))
				{
					TEST_FAILED;
					LogMsg(ERRMSG,_T("Test failed while executing call for SQLCOLATTRIBUTES of column : %d.\n"),i+1);
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
			returncode = SQLBindCol(hstmt,(SWORD)(cols+1),SQL_C_TCHAR,CharOutput[cols],STR_LEN,&stringlength);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
			{
				TEST_FAILED;
				LogMsg(ERRMSG,_T("Test failed while executing call for SQLBindCols of column : %d.\n"),cols);
				LogAllErrors(henv,hdbc,hstmt);
			}
		}

		k = 0;
		while (returncode == SQL_SUCCESS)
		{
			returncode = SQLFetch(hstmt);
			if(returncode == SQL_ERROR)
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			} else if (returncode == SQL_NO_DATA_FOUND) {
				break;
			}
			else {
				if (returncode == SQL_SUCCESS_WITH_INFO)
					LogAllErrors(henv,hdbc,hstmt);
				k++;
			}
		}
		if(k == 0)
		{
			TEST_FAILED;
			LogMsg(ERRMSG,_T("No Data Found => Atleast one row should be fetched\n"));
		}
		
		for(cols = 0; cols < numOfCols; cols++)
		{
			free(CharOutput[cols]);
		}
		TESTCASE_END;
	}

//=========================================================================================
	// Cleanup
	i=0;
	_stprintf(TableStr,_T("drop table %s.%s.%s"),ColumnWC[i].TabQua, ColumnWC[i].TabOwner, ColumnWC[i].TabName);
	SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);
	_stprintf(TableStr,_T("drop schema %s.%s cascade"),ColumnWC[i].TabQua, ColumnWC[i].TabOwner);
	SQLExecDirect(hstmt,(SQLTCHAR*) TableStr,SQL_NTS);

	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLTablePrivileges.\n"));
	free(TableStr); 
	free_list(var_list);
	TEST_RETURN;
}
