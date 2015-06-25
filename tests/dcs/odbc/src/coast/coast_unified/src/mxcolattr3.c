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

#define	RGB_MAX_LEN		50
#define	RGB_COLUMNS		6
#define	PF_COLUMNS		14
#define DIFF_WAYS		3

/*
---------------------------------------------------------
   TestSQLColAttribute
---------------------------------------------------------
*/
PassFail TestMXSQLColAttributeVer3(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	TCHAR		TempStr[50];
	TCHAR		Heading[MAX_STRING_SIZE];
	RETCODE		returncode;
	SQLHANDLE 	henv;
 	SQLHANDLE 	hdbc;
 	SQLHANDLE	hstmt;
	SWORD		numcol;
	SQLUSMALLINT		icol = 0,iatt = 0;
	SWORD		totalatt = 20;
	SQLTCHAR		rgbDesc[RGB_MAX_LEN], expDesc[RGB_MAX_LEN];
	SQLSMALLINT	pcbDesc;
    TCHAR        temp[1024];

#define			NUMBER_OF_COLUMNS		29

#ifdef _LP64
	SQLINTEGER pfDesc_4bytes; 
	SQLLEN	   pfDesc_8bytes; 
#endif
    SQLLEN		pfDesc; // 4 bytes
	int			dw;
	TCHAR		tableName[MAX_TABLE_NAME]; //testcolatt1
	TCHAR		columnName[NUMBER_OF_COLUMNS][MAX_COLUMN_NAME];
	TCHAR		*ExecDirStr[4];

	// The values in this struct corelate to those in DescType[].
	struct
	{
		SDWORD	pDes[PF_COLUMNS]; 
		TCHAR		*rDes[RGB_COLUMNS];
	} ColAttr[] = {
#ifdef UNICODE 
					{0, 1, NUMBER_OF_COLUMNS,  10,  10, 0, 1,  10,  0, 3,  1,  1, 1, 2,columnName[0] ,_T("CHAR (10) CHARACTER SET UCS2"),            pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[0]},
					{0, 1, NUMBER_OF_COLUMNS,  10,  10, 0, 1,  10,  0, 3, 12, 12, 1, 2,columnName[1] ,_T("VARCHAR (10) CHARACTER SET UCS2"),         pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[1]},
#else
					{0, 1, NUMBER_OF_COLUMNS,  10,  10, 0, 1,  10,  0, 3,  1,  1, 1, 2,columnName[0] ,_T("CHAR"),            pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[0]},
					{0, 1, NUMBER_OF_COLUMNS,  10,  10, 0, 1,  10,  0, 3, 12, 12, 1, 2,columnName[1] ,_T("VARCHAR"),         pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[1]},
#endif
					{0, 0, NUMBER_OF_COLUMNS,  12,  12, 1, 1,  10,  5, 2,  3,  3, 0, 2,columnName[2] ,_T("DECIMAL"),         pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[2]},
					{0, 0, NUMBER_OF_COLUMNS,   7,   7, 1, 1,   5,  2, 2,  3,  3, 1, 2,columnName[3] ,_T("DECIMAL"),         pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[3]},
					{0, 0, NUMBER_OF_COLUMNS,  12,  12, 1, 1,  10,  5, 2,  2,  2, 0, 2,columnName[4] ,_T("NUMERIC"),         pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[4]},
					{0, 0, NUMBER_OF_COLUMNS,   7,   7, 1, 1,   5,  2, 2,  2,  2, 1, 2,columnName[5] ,_T("NUMERIC"),         pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[5]},
					{0, 0, NUMBER_OF_COLUMNS,   6,   2, 0, 1,   5,  0, 2,  5,  5, 0, 2,columnName[6] ,_T("SMALLINT"),        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[6]},
					{0, 0, NUMBER_OF_COLUMNS,   5,   2, 0, 1,   5,  0, 2,  5,  5, 1, 2,columnName[7] ,_T("SMALLINT"),        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[7]},
					{0, 0, NUMBER_OF_COLUMNS,  11,   4, 0, 1,  10,  0, 2,  4,  4, 0, 2,columnName[8] ,_T("INTEGER"),         pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[8]},
					{0, 0, NUMBER_OF_COLUMNS,  10,   4, 0, 1,  10,  0, 2,  4,  4, 1, 2,columnName[9] ,_T("INTEGER"),         pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[9]},
					{0, 0, NUMBER_OF_COLUMNS,  13,   4, 0, 1,   7,  0, 2,  7,  7, 0, 2,columnName[10],_T("REAL"),            pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[10]},
					{0, 0, NUMBER_OF_COLUMNS,  22,   8, 0, 1,  15,  0, 2,  8,  8, 0, 2,columnName[11],_T("DOUBLE PRECISION"),pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[11]},
					{0, 0, NUMBER_OF_COLUMNS,  22,   8, 0, 1,  15,  0, 2,  8,  8, 0, 2,columnName[12],_T("DOUBLE PRECISION"),pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[12]},
					{0, 0, NUMBER_OF_COLUMNS,  10,  10, 0, 1,   0,  0, 2,  9, 91, 1, 2,columnName[13],_T("DATE"),            pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[13]},
					{0, 0, NUMBER_OF_COLUMNS,   8,   8, 0, 1,   0,  0, 2,  9, 92, 1, 2,columnName[14],_T("TIME"),            pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[14]},
					{0, 0, NUMBER_OF_COLUMNS,  26,  26, 0, 1,   6,  0, 2,  9, 93, 1, 2,columnName[15],_T("TIMESTAMP"),       pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[15]},
					{0, 0, NUMBER_OF_COLUMNS,  20,  20, 0, 1,  19,  0, 2, -5, -5, 0, 2,columnName[16],_T("BIGINT"),          pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[16]},
#ifdef UNICODE
					{0, 1, NUMBER_OF_COLUMNS,2000,2000, 0, 1,2000,  0, 3, 12, 12, 1, 2,columnName[17],_T("VARCHAR (2000) CHARACTER SET UCS2"),		 pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[17]},
#else
					{0, 1, NUMBER_OF_COLUMNS,2000,2000, 0, 1,2000,  0, 3, 12, 12, 1, 2,columnName[17],_T("VARCHAR"),		 pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[17]},
#endif
					{0, 0, NUMBER_OF_COLUMNS,  21,  21, 0, 1,  19,  0, 2,  2,  2, 0, 2,columnName[18] ,_T("NUMERIC"),        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[18]},
					{0, 0, NUMBER_OF_COLUMNS,  21,  21, 1, 1,  19,  6, 2,  2,  2, 0, 2,columnName[19] ,_T("NUMERIC"),        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[19]},
					{0, 0, NUMBER_OF_COLUMNS, 130, 130, 0, 1, 128,  0, 2,  2,  2, 0, 2,columnName[20] ,_T("NUMERIC"),        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[20]},
					{0, 0, NUMBER_OF_COLUMNS, 130, 130, 1, 1, 128,128, 2,  2,  2, 0, 2,columnName[21] ,_T("NUMERIC"),        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[21]},
					{0, 0, NUMBER_OF_COLUMNS, 130, 130, 1, 1, 128, 64, 2,  2,  2, 0, 2,columnName[22] ,_T("NUMERIC"),        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[22]},
					{0, 0, NUMBER_OF_COLUMNS,  12,  12, 1, 1,  10,  5, 2,  2,  2, 1, 2,columnName[23] ,_T("NUMERIC"),        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[23]},
					{0, 0, NUMBER_OF_COLUMNS,  20,  20, 1, 1,  18,  5, 2,  2,  2, 1, 2,columnName[24] ,_T("NUMERIC"),        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[24]},
					{0, 0, NUMBER_OF_COLUMNS,  32,  32, 1, 1,  30, 10, 2,  2,  2, 1, 2,columnName[25] ,_T("NUMERIC"),        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[25]},
				#ifdef UNICODE
					{0, 1, NUMBER_OF_COLUMNS,  40,  40, 0, 1,  40,  0, 3, 1,   1, 1, 2,columnName[26] ,_T("CHAR (10) CHARACTER SET UTF8"),			pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[26]},
					{0, 1, NUMBER_OF_COLUMNS,  40,  40, 0, 1,  40,  0, 3, 12, 12, 1, 2,columnName[27] ,_T("VARCHAR (10) CHARACTER SET UTF8"),		pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[27]},
					{0, 1, NUMBER_OF_COLUMNS,2000,2000, 0, 1,2000,  0, 3, 12, 12, 1, 2,columnName[28] ,_T("VARCHAR (500) CHARACTER SET UTF8"),		pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[28]}
				#else
					{0, 1, NUMBER_OF_COLUMNS,  10,  10, 0, 1,  10,  0, 3, 1,   1, 1, 2,columnName[26] ,_T("CHAR (10) CHARACTER SET UCS2"),			pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[26]},
					{0, 1, NUMBER_OF_COLUMNS,  10,  10, 0, 1,  10,  0, 3, 12, 12, 1, 2,columnName[27] ,_T("VARCHAR (10) CHARACTER SET UCS2"),		pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[27]},
					{0, 1, NUMBER_OF_COLUMNS,2000,2000, 0, 1,2000,  0, 3, 12, 12, 1, 2,columnName[28] ,_T("VARCHAR (2000) CHARACTER SET UCS2"),		pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[28]}
				#endif
					};

	SQLUSMALLINT	DescType[] = {
					SQL_DESC_AUTO_UNIQUE_VALUE,
					SQL_DESC_CASE_SENSITIVE,
					SQL_DESC_COUNT,
					SQL_DESC_DISPLAY_SIZE,
					SQL_DESC_LENGTH,
					SQL_DESC_FIXED_PREC_SCALE,
					SQL_DESC_NULLABLE,
					SQL_DESC_PRECISION,
					SQL_DESC_SCALE,
					SQL_DESC_SEARCHABLE,
					SQL_DESC_TYPE,
					SQL_DESC_CONCISE_TYPE,
					SQL_DESC_UNSIGNED,
					SQL_DESC_UPDATABLE,
					SQL_DESC_NAME,
					SQL_DESC_TYPE_NAME,
					SQL_DESC_SCHEMA_NAME,
					SQL_DESC_CATALOG_NAME,
					SQL_DESC_TABLE_NAME,
					SQL_DESC_LABEL
					};

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLColumnAttributes30"), charset_file);
	if (var_list == NULL) return FAILED;

	//print_list(var_list);
	_tcscpy(tableName,var_mapping(_T("SQLColumnAttributes30_tableName_1"), var_list));

	_tcscpy(columnName[0],var_mapping(_T("SQLColumnAttributes30_columnName_1"), var_list));
	_tcscpy(columnName[1],var_mapping(_T("SQLColumnAttributes30_columnName_2"), var_list));
	_tcscpy(columnName[2],var_mapping(_T("SQLColumnAttributes30_columnName_3"), var_list));
	_tcscpy(columnName[3],var_mapping(_T("SQLColumnAttributes30_columnName_4"), var_list));
	_tcscpy(columnName[4],var_mapping(_T("SQLColumnAttributes30_columnName_5"), var_list));
	_tcscpy(columnName[5],var_mapping(_T("SQLColumnAttributes30_columnName_6"), var_list));
	_tcscpy(columnName[6],var_mapping(_T("SQLColumnAttributes30_columnName_7"), var_list));
	_tcscpy(columnName[7],var_mapping(_T("SQLColumnAttributes30_columnName_8"), var_list));
	_tcscpy(columnName[8],var_mapping(_T("SQLColumnAttributes30_columnName_9"), var_list));
	_tcscpy(columnName[9],var_mapping(_T("SQLColumnAttributes30_columnName_10"), var_list));
	_tcscpy(columnName[10],var_mapping(_T("SQLColumnAttributes30_columnName_11"), var_list));
	_tcscpy(columnName[11],var_mapping(_T("SQLColumnAttributes30_columnName_12"), var_list));
	_tcscpy(columnName[12],var_mapping(_T("SQLColumnAttributes30_columnName_13"), var_list));
	_tcscpy(columnName[13],var_mapping(_T("SQLColumnAttributes30_columnName_14"), var_list));
	_tcscpy(columnName[14],var_mapping(_T("SQLColumnAttributes30_columnName_15"), var_list));
	_tcscpy(columnName[15],var_mapping(_T("SQLColumnAttributes30_columnName_16"), var_list));
	_tcscpy(columnName[16],var_mapping(_T("SQLColumnAttributes30_columnName_17"), var_list));
	_tcscpy(columnName[17],var_mapping(_T("SQLColumnAttributes30_columnName_18"), var_list));
	_tcscpy(columnName[18],var_mapping(_T("SQLColumnAttributes30_columnName_19"), var_list));
	_tcscpy(columnName[19],var_mapping(_T("SQLColumnAttributes30_columnName_20"), var_list));
	_tcscpy(columnName[20],var_mapping(_T("SQLColumnAttributes30_columnName_21"), var_list));
	_tcscpy(columnName[21],var_mapping(_T("SQLColumnAttributes30_columnName_22"), var_list));
	_tcscpy(columnName[22],var_mapping(_T("SQLColumnAttributes30_columnName_23"), var_list));
	_tcscpy(columnName[23],var_mapping(_T("SQLColumnAttributes30_columnName_24"), var_list));
	_tcscpy(columnName[24],var_mapping(_T("SQLColumnAttributes30_columnName_25"), var_list));
	_tcscpy(columnName[25],var_mapping(_T("SQLColumnAttributes30_columnName_26"), var_list));
	_tcscpy(columnName[26],var_mapping(_T("SQLColumnAttributes30_columnName_27"), var_list));
	_tcscpy(columnName[27],var_mapping(_T("SQLColumnAttributes30_columnName_28"), var_list));
	_tcscpy(columnName[28],var_mapping(_T("SQLColumnAttributes30_columnName_29"), var_list));

	ExecDirStr[0] = var_mapping(_T("SQLColumnAttributes30_ExecDirStr_1"), var_list);
	ExecDirStr[1] = var_mapping(_T("SQLColumnAttributes30_ExecDirStr_2"), var_list);
	ExecDirStr[2] = var_mapping(_T("SQLColumnAttributes30_ExecDirStr_3"), var_list);
	ExecDirStr[3] = var_mapping(_T("SQLColumnAttributes30_ExecDirStr_4"), var_list);

//===========================================================================================================

	//if(isUCS2) {
	//	LogMsg(NONE,_T("Setup for UCS2 mode testing: ColPrec has to be doubled\n"));

	//	numcol = sizeof(ColAttr)/sizeof(ColAttr[0]);
	//	for(icol=0; icol<numcol; icol++) {
	//		if(_tcsicmp(ColAttr[icol].rDes[1],_T("CHAR")) == 0) {
	//			ColAttr[icol].rDes[1] = _T("NCHAR");
	//			ColAttr[icol].pDes[10] = SQL_WCHAR;
	//			ColAttr[icol].pDes[11] = SQL_WCHAR;
	//		}
	//		else if (_tcsicmp(ColAttr[icol].rDes[1],_T("VARCHAR")) == 0) {
	//			ColAttr[icol].rDes[1] = _T("NVARCHAR");
	//			ColAttr[icol].pDes[10] = SQL_WVARCHAR;
	//			ColAttr[icol].pDes[11] = SQL_WVARCHAR;
	//		}
	//		else if (_tcsicmp(ColAttr[icol].rDes[1],_T("LONG VARCHAR")) == 0) {
	//			ColAttr[icol].rDes[1] = _T("LONG NVARCHAR");
	//			ColAttr[icol].pDes[10] = SQL_WLONGVARCHAR;
	//			ColAttr[icol].pDes[11] = SQL_WLONGVARCHAR;
	//		}
	//		else {}
	//		//for(iatt=0; iatt<totalatt; iatt++) {
	//			//if((DescType[iatt]==SQL_COLUMN_DISPLAY_SIZE) ||
	//			//	(DescType[iatt]==SQL_COLUMN_LENGTH) ||
	//			//	(DescType[iatt]==SQL_COLUMN_PRECISION))
	//			//if (DescType[iatt]==SQL_COLUMN_PRECISION)
	//			//	ColAttr[icol].pDes[iatt] *= 2;
	//		//}
	//	}
	//	icol = 0;
	//	iatt = 0;
	//	numcol = 0;
	//}

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing 3.0 API => MX Specific SQLColumnAttribute.\n"));
	TEST_INIT;
	   
 	TESTCASE_BEGIN("Setup for SQLColAttribute tests\n");

	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	
	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[1],SQL_NTS); /* create table */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[2],SQL_NTS); /* insert into table */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
		LogAllErrorsVer3(henv,hdbc,hstmt);
		SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
		TEST_FAILED;
		TEST_RETURN;
		}
	TESTCASE_END; // end of setup
	
	for (dw = 0; dw < DIFF_WAYS; dw++)
	{
		switch (dw)
		{
			case 0:
			{
				TESTCASE_BEGIN("SQLColAttribute tests after SQLPrepare\n");
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)ExecDirStr[3], SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
					TEST_FAILED;
					TEST_RETURN;
				}
				break;
			}
			case 1:
			{
				TESTCASE_BEGIN("SQLColAttribute tests after SQLPrepare & SQLExecute\n");
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)ExecDirStr[3], SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
					TEST_FAILED;
					TEST_RETURN;
				}
				returncode = SQLExecute(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
					TEST_FAILED;
					TEST_RETURN;
				}
				break;
			}
			case 2:
			{
				TESTCASE_BEGIN("SQLColAttribute tests after SQLExecDirect\n");
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[3], SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
					TEST_FAILED;
					TEST_RETURN;
				}
				break;
			}
			default: ;
		}
		returncode=SQLNumResultCols(hstmt, &numcol);	// remove this since colatt don't work after prepare. 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultsCols")){
			LogAllErrorsVer3(henv,hdbc,hstmt);
			SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
			TEST_FAILED;
			TEST_RETURN;
			}
		if(numcol<1){
			LogMsg(LINEAFTER,_T("SQLNumResultCols says %d columns are in the result set\n\
							This is incorrect.  Expecting at least 1 or more columns\n"),numcol);
			SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
			TEST_FAILED;
			TEST_RETURN;
			}	 // till here remove 

		TESTCASE_END;

		for (icol = 1; icol <= numcol; icol++){
			for (iatt = 0; iatt < totalatt; iatt++){
		 		_tcscpy((TCHAR*)rgbDesc,_T(""));
				pcbDesc = 0;
				pfDesc = 0;

                //SQLDescAttrToChar(DescType[iatt], temp);
                //_tprintf(_T("SQLColAttribute on: %s for column %d\n"), temp, icol);

				_stprintf(Heading,_T("SQLColAttribute: Positive test for column %d\n"),icol);
				TESTCASE_BEGINW(Heading);
#ifdef _LP64      
                pfDesc_8bytes = 0;          				
                pfDesc_4bytes = 0;
                if(DescType[iatt] == SQL_DESC_DISPLAY_SIZE ||
				   DescType[iatt] == SQL_DESC_LENGTH ||
				   DescType[iatt] == SQL_DESC_OCTET_LENGTH ||
				   DescType[iatt] == SQL_DESC_COUNT)
			       returncode = SQLColAttribute(hstmt,icol,DescType[iatt],rgbDesc,RGB_MAX_LEN,&pcbDesc,&pfDesc_8bytes);
				else
  				   returncode = SQLColAttribute(hstmt,icol,DescType[iatt],rgbDesc,RGB_MAX_LEN,&pcbDesc,(SQLLEN*)&pfDesc_4bytes);
				if(pfDesc_4bytes != 0)
				   pfDesc_8bytes = pfDesc_4bytes ;
#else
				returncode = SQLColAttribute(hstmt,icol,DescType[iatt],rgbDesc,RGB_MAX_LEN,&pcbDesc,&pfDesc);
#endif
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColAttribute")){
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TEST_FAILED;
                    SQLDescAttrToChar(DescType[iatt], temp);
                    LogMsg(ERRMSG, _T("SQLColAttribute error on: %s\n"), temp);
                }
				if (iatt < PF_COLUMNS){
					_tcscpy ((TCHAR*)expDesc, _T(""));
					if (_tcscmp("SQL_DESC_CATALOG_NAME", SQLDescAttrToChar(DescType[iatt],TempStr)) == 0)
					_tcscpy ((TCHAR*)expDesc, _T("TRAFODION"));
#ifdef _LP64
					if ((cwcscmp((TCHAR*)rgbDesc,(TCHAR*)expDesc,TRUE) == 0) && (pcbDesc == 0) && (ColAttr[icol-1].pDes[iatt] == pfDesc_8bytes
						/* this is the UNICODE version, there are a few exceptions. */
						|| (ColAttr[icol-1].pDes[iatt] == SQL_VARCHAR && pfDesc_8bytes == SQL_WVARCHAR)
						|| (ColAttr[icol-1].pDes[iatt] == SQL_CHAR && pfDesc_8bytes == SQL_WCHAR)
						/* end of */
						)) 
#else
					if ((cwcscmp((TCHAR*)rgbDesc,(TCHAR*)expDesc,TRUE) == 0) && (pcbDesc == 0) && (ColAttr[icol-1].pDes[iatt] == pfDesc
						/* this is the UNICODE version, there are a few exceptions. */
						|| (ColAttr[icol-1].pDes[iatt] == SQL_VARCHAR && pfDesc == SQL_WVARCHAR)
						|| (ColAttr[icol-1].pDes[iatt] == SQL_CHAR && pfDesc == SQL_WCHAR)
						/* end of */
						)) 
#endif
					{
						/*
						LogMsg(NONE,_T("Column C%d & ColAtt %s\n"),icol,SQLDescAttrToChar(DescType[iatt],TempStr));
						LogMsg(NONE,_T("CharacterAttributePtr Expected: '%s'\tActual: '%s'\n"),expDesc,rgbDesc);
						LogMsg(NONE,_T("StringLengthPtr Expected: %d\tActual: %d\n"),pcbDesc,0);
						LogMsg(NONE,_T("NumericAttributePtr Expected: %d\tActual: %d\n"),ColAttr[icol-1].pDes[iatt],pfDesc);
						*/
					}
					else{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("Column C%d & ColAtt %s, line %d\n"),icol,SQLDescAttrToChar(DescType[iatt],TempStr),__LINE__);
							LogMsg(ERRMSG,_T("CharacterAttributePtr Expected: '%s'\tActual: '%s', line %d\n"),expDesc,rgbDesc,__LINE__);
							LogMsg(ERRMSG,_T("StringLengthPtr Expected: %d\tActual: %d, line %d\n"),pcbDesc,0,__LINE__);
#ifdef _LP64    
							LogMsg(ERRMSG,_T("NumericAttributePtr Expected: %d\tActual: %d, line %d\n"),ColAttr[icol-1].pDes[iatt],pfDesc_8bytes,__LINE__);
#else
							LogMsg(ERRMSG,_T("NumericAttributePtr Expected: %d\tActual: %d, line %d\n"),ColAttr[icol-1].pDes[iatt],pfDesc,__LINE__);
#endif
						}
					}
				else{
#ifdef _LP64
					if ((cwcscmp((TCHAR*)ColAttr[icol-1].rDes[iatt-PF_COLUMNS],(TCHAR*)rgbDesc, TRUE) == 0
						/* this is the UNICODE version, there are a few exceptions. */
						|| (cwcscmp((TCHAR*)ColAttr[icol-1].rDes[iatt-PF_COLUMNS],_T("VARCHAR"), TRUE) == 0 &&
							cwcscmp((TCHAR*)rgbDesc,_T("NCHAR VARYING"), TRUE) == 0)
						|| (cwcscmp((TCHAR*)ColAttr[icol-1].rDes[iatt-PF_COLUMNS],_T("CHAR"), TRUE) == 0 &&
							cwcscmp((TCHAR*)rgbDesc,_T("NCHAR"), TRUE) == 0)
						/* end of */
						) && (pcbDesc == (SWORD)_tcslen((const char*)rgbDesc)*sizeof(TCHAR)) && (pfDesc_8bytes == 0)) 
#else
					if ((cwcscmp((TCHAR*)ColAttr[icol-1].rDes[iatt-PF_COLUMNS],(TCHAR*)rgbDesc, TRUE) == 0
						/* this is the UNICODE version, there are a few exceptions. */
						|| (cwcscmp((TCHAR*)ColAttr[icol-1].rDes[iatt-PF_COLUMNS],_T("VARCHAR"), TRUE) == 0 &&
							cwcscmp((TCHAR*)rgbDesc,_T("NCHAR VARYING"), TRUE) == 0)
						|| (cwcscmp((TCHAR*)ColAttr[icol-1].rDes[iatt-PF_COLUMNS],_T("CHAR"), TRUE) == 0 &&
							cwcscmp((TCHAR*)rgbDesc,_T("NCHAR"), TRUE) == 0)
						/* end of */
						) && (pcbDesc == (SWORD)_tcslen((const TCHAR *)rgbDesc)*sizeof(TCHAR)) && (pfDesc == 0)) 
#endif
					{
						/*
						LogMsg(NONE,_T("Column C%d & ColAtt %s\n"),icol,SQLDescAttrToChar(DescType[iatt],TempStr));
						LogMsg(NONE,_T("CharacterAttributePtr Expected: '%s'\tActual: '%s'\n"),ColAttr[icol-1].rDes[iatt-PF_COLUMNS],rgbDesc);
						LogMsg(NONE,_T("StringLengthPtr Expected: %d\tActual: %d\n"),_tcslen(rgbDesc)*sizeof(TCHAR),pcbDesc);
						LogMsg(NONE,_T("NumericAttributePtr Expected: %d\tActual: %d\n"),0,pfDesc);
						*/
					}	
					else{
						TEST_FAILED;	
						LogMsg(ERRMSG,_T("Column C%d & ColAtt %s\n"),icol,SQLDescAttrToChar(DescType[iatt],TempStr));
						LogMsg(ERRMSG,_T("CharacterAttributePtr Expected: '%s'\tActual: '%s', Line = %d\n"),ColAttr[icol-1].rDes[iatt-PF_COLUMNS],rgbDesc,__LINE__);
						LogMsg(ERRMSG,_T("StringLengthPtr Expected: %d\tActual: %d\n"),_tcslen((TCHAR*)rgbDesc)*sizeof(TCHAR),pcbDesc);
						LogMsg(ERRMSG,_T("NumericAttributePtr Expected: %d\tActual: %d\n"),0,pfDesc);
						}
					}
				TESTCASE_END;
				} /* end iatt loop */
			} /* end icol loop */

			returncode = SQLFetch(hstmt);
            returncode = SQLFreeStmt(hstmt, SQL_CLOSE);
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[0],SQL_NTS); /* cleanup */
	returncode = SQLFreeHandle(SQL_HANDLE_STMT,hstmt);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeStmt"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	FullDisconnect3(pTestInfo);

	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => MX Specific SQLColumnAttribute.\n"));

	free_list(var_list);

	TEST_RETURN;
}
