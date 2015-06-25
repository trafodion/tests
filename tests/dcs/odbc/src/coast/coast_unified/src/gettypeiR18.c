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
#include <string.h>
#include <windows.h>
#include <sqlext.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define	TYPE_LEN		128

/*
------------------------------------------------------------------
   TestSQLGetTypeInfo: Tests SQLGetTypeInfo                      
------------------------------------------------------------------
*/
PassFail TestSQLGetTypeInfoR18(TestInfo *pTestInfo)
{   
	TEST_DECLARE;
	TCHAR				Heading[MAX_STRING_SIZE];
  RETCODE			returncode;
  SQLHANDLE 			henv;
  SQLHANDLE 			hdbc;
  SQLHANDLE			hstmt;				  
  TCHAR				TempBuf[MAX_STRING_SIZE];	
  int				j = 0,END_LOOP;

	struct
	{
		TCHAR		*TYPE_NAME;
		SWORD		DATA_TYPE;
		SDWORD		PRECISION;
		TCHAR		*LITERAL_PREFIX;
		TCHAR		*LITERAL_SUFFIX;
		TCHAR		*CREATE_PARAMS;
		SWORD		NULLABLE;
		SWORD		CASE_SENSITIVE;
		SWORD		SEARCHABLE;
		SWORD		UNSIGNED_ATTRIBUTE;
		SWORD		MONEY;
		SWORD		AUTO_INCREMENT;
		TCHAR		*LOCAL_TYPE_NAME;
		SWORD		MINIMUM_SCALE;
		SWORD		MAXIMUM_SCALE;
	}	TypeInfo[] = 
		{//TYPENAME,DATATYPE,PREC,LITPRE,LITSUF,PARAM,NULL,CASE,SRCH,ATTR,MON,INC,LOC,MIN,MAX
			{_T(""),SQL_ALL_TYPES,0,_T(""),_T(""),_T(""),0,0,0,0,0,0,_T(""),0,0},	// this is for get all types
			{_T("CHAR"), SQL_CHAR, 32000, _T("'"), _T("'"), _T("max length"), SQL_NULLABLE, 1, SQL_SEARCHABLE, 0, 0, 0, _T("CHARACTER"), 0, 0},
			{_T("NCHAR"), SQL_WCHAR, 16000, _T("N'"), _T("'"), _T("max length"), SQL_NULLABLE, 1, SQL_SEARCHABLE, 0, 0, 0, _T("WIDE CHARACTER"), 0, 0},
			{_T("VARCHAR"), SQL_VARCHAR, 32000, _T("'"), _T("'"), _T("max length"), SQL_NULLABLE, 1, SQL_SEARCHABLE, 0, 0, 0, _T("VARCHAR"), 0, 0},
			{_T("NCHAR VARYING"), SQL_WVARCHAR, 16000, _T("N'"), _T("'"), _T("max length"), SQL_NULLABLE, 1, SQL_SEARCHABLE, 0, 0, 0, _T("WIDE VARCHAR"), 0, 0},
			{_T("DECIMAL"), SQL_DECIMAL, 18, _T(""), _T(""), _T("precision,scale"), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("DECIMAL"), 0, 18},
			{_T("NUMERIC"), SQL_NUMERIC, 128, _T(""), _T(""), _T("precision,scale"), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("NUMERIC"), 0, 128},
			{_T("SMALLINT"), SQL_SMALLINT, 5, _T(""), _T(""), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("SMALLINT"), 0, 0},
			{_T("INTEGER"), SQL_INTEGER, 10, _T(""), _T(""), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("INTEGER"), 0, 0},
			{_T("REAL"), SQL_REAL, 7, _T(""), _T(""), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("REAL"), 0, 0},
			{_T("FLOAT"), SQL_FLOAT, 15, _T(""), _T(""), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("FLOAT"), 0, 0},
			{_T("DOUBLE PRECISION"), SQL_DOUBLE, 15, _T(""), _T(""), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("DOUBLE"), 0, 0},
//			{_T("DATE"), SQL_DATE,  10,  _T("{d '"),  "'}",_T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("DATE"), 0, 0},
//			{_T("TIME"), SQL_TIME, 8, _T("{t '"), "'}", _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("TIME"), 0, 0},
//			{_T("TIMESTAMP"), SQL_TIMESTAMP, 23, _T("{ts '"), "'}", _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("TIMESTAMP"), 0, 6},
			{_T("DATE"), SQL_TYPE_DATE,  10,  _T("{d '"),  _T("'}"),_T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("DATE"), 0, 0},
			{_T("TIME"), SQL_TYPE_TIME, 8, _T("{t '"), _T("'}"), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("TIME"), 0, 0},
			{_T("TIMESTAMP"), SQL_TYPE_TIMESTAMP, 26, _T("{ts '"), _T("'}"), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("TIMESTAMP"), 0, 6},
			{_T("BIGINT"), SQL_BIGINT, 19, _T(""), _T(""), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("LARGEINT"), 0, 0},
//			{_T("LONG VARCHAR"), SQL_LONGVARCHAR, 4018, _T("'"), _T("'"), _T(""), SQL_NULLABLE, 1, SQL_SEARCHABLE, 0, 0, 0, _T("LONG VARCHAR"), 0, 0},
//			{_T("NCHAR VARYING"), SQL_WLONGVARCHAR, 4018, _T("N'"), _T("'"), _T("max length"), SQL_NULLABLE, 1, SQL_SEARCHABLE, 0, 0, 0, _T("WIDE LONG VARCHAR"), 0, 0},
//			{_T("BINARY"), SQL_BINARY, 4059, _T("'"), _T("'"), "max length", 1, 0, 0, 0, 0, 0, _T(""), 0, 0},
//			{_T("VARBINARY"), -3, 4059, _T("'"), _T("'"), "max length", 1, 0, 0, 0, 0, 0, _T(""), 0, 0},
//			{_T("LONG VARBINARY"), -4, 4059, _T("'"), _T("'"), "max length", 1, 0, 0, 0, 0, 0, _T(""), 0, 0},
//			{_T("TINYINT"), -6, 3, _T(""), _T(""), _T(""), 1, 0, SQL_ALL_EXCEPT_LIKE, 1, 0, 0, _T(""), 0, 0},
//			{_T("BIT"), -7, 1, _T(""), _T(""), _T(""), 1, 0, SQL_UNSEARCHABLE, 0, 0, 0, _T(""), 0, 0},
			{_T("INTERVAL"), SQL_INTERVAL_YEAR, 0, _T("{INTERVAL '"), _T("' YEAR}"), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("INTERVAL"), 0, 0},
			{_T("INTERVAL"), SQL_INTERVAL_MONTH, 0, _T("{INTERVAL '"), _T("' MONTH}"), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("INTERVAL"), 0, 0},
			{_T("INTERVAL"), SQL_INTERVAL_DAY, 0, _T("{INTERVAL '"), _T("' DAY}"), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("INTERVAL"), 0, 0},
			{_T("INTERVAL"), SQL_INTERVAL_HOUR, 0, _T("{INTERVAL '"), _T("' HOUR}"), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("INTERVAL"), 0, 0},
			{_T("INTERVAL"), SQL_INTERVAL_MINUTE, 0, _T("{INTERVAL '"), _T("' MINUTE}"), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("INTERVAL"), 0, 0},
			{_T("INTERVAL"), SQL_INTERVAL_SECOND, 0, _T("{INTERVAL '"), _T("' SECOND}"), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("INTERVAL"), 0, 0},
			{_T("INTERVAL"), SQL_INTERVAL_YEAR_TO_MONTH, 0, _T("{INTERVAL '"), _T("' YEAR TO MONTH}"), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("INTERVAL"), 0, 0},
			{_T("INTERVAL"), SQL_INTERVAL_DAY_TO_HOUR, 0, _T("{INTERVAL '"), _T("' DAY TO HOUR}"), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("INTERVAL"), 0, 0},
			{_T("INTERVAL"), SQL_INTERVAL_DAY_TO_MINUTE, 0, _T("{INTERVAL '"), _T("' DAY TO MINUTE}"), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("INTERVAL"), 0, 0},
			{_T("INTERVAL"), SQL_INTERVAL_DAY_TO_SECOND, 0, _T("{INTERVAL '"), _T("' DAY TO SECOND}"), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("INTERVAL"), 0, 0},
			{_T("INTERVAL"), SQL_INTERVAL_HOUR_TO_MINUTE, 0, _T("{INTERVAL '"), _T("' HOUR TO MINUTE}"), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("INTERVAL"), 0, 0},
			{_T("INTERVAL"), SQL_INTERVAL_HOUR_TO_SECOND, 0, _T("{INTERVAL '"), _T("' HOUR TO SECOND}"), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("INTERVAL"), 0, 0},
			{_T("INTERVAL"), SQL_INTERVAL_MINUTE_TO_SECOND, 0, _T("{INTERVAL '"), _T("' MINUTE TO SECOND}"), _T(""), SQL_NULLABLE, 0, SQL_ALL_EXCEPT_LIKE, 0, 0, 0, _T("INTERVAL"), 0, 0},
			{_T(""),999,}	
	};



		TCHAR		oTYPE_NAME[TYPE_LEN];
		SWORD		oDATA_TYPE, fSqlType1;
		SDWORD		oPRECISION;
		TCHAR		oLITERAL_PREFIX[TYPE_LEN];
		TCHAR		oLITERAL_SUFFIX[TYPE_LEN];
		TCHAR		oCREATE_PARAMS[TYPE_LEN];
		SWORD		oNULLABLE;
		SWORD		oCASE_SENSITIVE;
		SWORD		oSEARCHABLE;
		SWORD		oUNSIGNED_ATTRIBUTE;
		SWORD		oMONEY;
		SWORD		oAUTO_INCREMENT;
		TCHAR		oLOCAL_TYPE_NAME[TYPE_LEN];
		SWORD		oMINIMUM_SCALE;
		SWORD		oMAXIMUM_SCALE;

		SQLLEN	oTYPE_NAMElen;	
		SQLLEN	oDATA_TYPElen;
		SQLLEN	oPRECISIONlen;
		SQLLEN	oLITERAL_PREFIXlen;
		SQLLEN	oLITERAL_SUFFIXlen;
		SQLLEN	oCREATE_PARAMSlen;
		SQLLEN	oNULLABLElen;
		SQLLEN	oCASE_SENSITIVElen;
		SQLLEN	oSEARCHABLElen;
		SQLLEN	oUNSIGNED_ATTRIBUTElen;
		SQLLEN	oMONEYlen;
		SQLLEN	oAUTO_INCREMENTlen;
		SQLLEN	oLOCAL_TYPE_NAMElen;
		SQLLEN	oMINIMUM_SCALElen;
		SQLLEN	oMAXIMUM_SCALElen;

   	/* Set up some local variables to save on typing in longer ones */
      
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLGetTypeInfo for R1.8.\n"));

	TEST_INIT;
	TESTCASE_BEGIN("Setup for SQLGetTypeInfo tests for R1.8\n");

	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
		TEST_FAILED;
		TEST_RETURN;
	}

  	/* Set up some local variables to save on typing in longer ones */
	henv = pTestInfo->henv;
	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle")){
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	
	TESTCASE_END; // end of setup

//=========================================================================================
					 
/*	if (MX_MP_SPECIFIC == MX_SPECIFIC)
		END_LOOP = SQL_BINARY;
	else if (MX_MP_SPECIFIC == MP_SPECIFIC)
		END_LOOP = 999;
	else
	{
		LogMsg(ERRMSG,_T("gettypeinfo test failed.\n"));
		TEST_RETURN;
	}
*/	
	END_LOOP = 999;
	j = 0;
	while (TypeInfo[j].DATA_TYPE != END_LOOP) 
	{
		_stprintf(Heading,_T("Test Positive functionality of SQLGetTypeInfo for data type: %s\n"),
									SQLTypeToChar(TypeInfo[j].DATA_TYPE,TempBuf));
		TESTCASE_BEGINW(Heading);

		returncode = SQLGetTypeInfo(hstmt,TypeInfo[j].DATA_TYPE);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetTypeInfo"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		else
		{
			if (TypeInfo[j].DATA_TYPE != 0) 
			{ 
				_tcscpy(oTYPE_NAME,_T(""));
				oDATA_TYPE = 0; 
				oPRECISION = 0;
				_tcscpy(oLITERAL_PREFIX,_T(""));
				_tcscpy(oLITERAL_SUFFIX,_T(""));
				_tcscpy(oCREATE_PARAMS,_T(""));
				oNULLABLE = 0;
				oCASE_SENSITIVE = 0;
				oSEARCHABLE = 0;
				oUNSIGNED_ATTRIBUTE = 0;
				oMONEY = 0;
				oAUTO_INCREMENT = 0;
				_tcscpy(oLOCAL_TYPE_NAME,_T(""));
				oMINIMUM_SCALE = 0;
				oMAXIMUM_SCALE = 0;
				returncode = SQLBindCol(hstmt,1,SQL_C_TCHAR,oTYPE_NAME,TYPE_LEN,&oTYPE_NAMElen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,2,SQL_C_SHORT,&oDATA_TYPE,0,&oDATA_TYPElen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,3,SQL_C_LONG,&oPRECISION,0,&oPRECISIONlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,4,SQL_C_TCHAR,oLITERAL_PREFIX,TYPE_LEN,&oLITERAL_PREFIXlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,5,SQL_C_TCHAR,oLITERAL_SUFFIX,TYPE_LEN,&oLITERAL_SUFFIXlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,6,SQL_C_TCHAR,oCREATE_PARAMS,TYPE_LEN,&oCREATE_PARAMSlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,7,SQL_C_SHORT,&oNULLABLE,0,&oNULLABLElen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,8,SQL_C_SHORT,&oCASE_SENSITIVE,0,&oCASE_SENSITIVElen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,9,SQL_C_SHORT,&oSEARCHABLE,0,&oSEARCHABLElen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,10,SQL_C_SHORT,&oUNSIGNED_ATTRIBUTE,0,&oUNSIGNED_ATTRIBUTElen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,11,SQL_C_SHORT,&oMONEY,0,&oMONEYlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,12,SQL_C_SHORT,&oAUTO_INCREMENT,0,&oAUTO_INCREMENTlen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,13,SQL_C_TCHAR,oLOCAL_TYPE_NAME,TYPE_LEN,&oLOCAL_TYPE_NAMElen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,14,SQL_C_SHORT,&oMINIMUM_SCALE,0,&oMINIMUM_SCALElen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLBindCol(hstmt,15,SQL_C_SHORT,&oMAXIMUM_SCALE,0,&oMAXIMUM_SCALElen);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
				{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
				}
				returncode = SQLFetch(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					LogMsg(NONE,_T("Comparing results\n"));
					if ((_tcsicmp(TypeInfo[j].TYPE_NAME,oTYPE_NAME) == 0)
							&& (TypeInfo[j].DATA_TYPE == oDATA_TYPE)
							&& (TypeInfo[j].PRECISION == oPRECISION)
							&& (_tcsicmp(TypeInfo[j].LITERAL_PREFIX,oLITERAL_PREFIX) == 0)
							&& (_tcsicmp(TypeInfo[j].LITERAL_SUFFIX,oLITERAL_SUFFIX) == 0)
							&& (_tcsicmp(TypeInfo[j].CREATE_PARAMS,oCREATE_PARAMS) == 0)
							&& (TypeInfo[j].NULLABLE == oNULLABLE)
							&& (TypeInfo[j].CASE_SENSITIVE == oCASE_SENSITIVE)
							&& (TypeInfo[j].SEARCHABLE == oSEARCHABLE)
							&& (TypeInfo[j].UNSIGNED_ATTRIBUTE == oUNSIGNED_ATTRIBUTE)
							&& (TypeInfo[j].MONEY == oMONEY)
							&& (TypeInfo[j].AUTO_INCREMENT == oAUTO_INCREMENT)
							&& (_tcsicmp(TypeInfo[j].LOCAL_TYPE_NAME,oLOCAL_TYPE_NAME) == 0)
							&& (TypeInfo[j].MINIMUM_SCALE == oMINIMUM_SCALE)
							&& (TypeInfo[j].MAXIMUM_SCALE == oMAXIMUM_SCALE))
					{
						LogMsg(NONE,_T("Data Type Name actual: %s and expected: %s are matched\n"),oTYPE_NAME,TypeInfo[j].TYPE_NAME);
						LogMsg(NONE,_T("Data Type actual: %d and expected: %d are matched\n"),oDATA_TYPE,TypeInfo[j].DATA_TYPE);
						LogMsg(NONE,_T("Precision actual: %d and expected: %d are matched\n"),oPRECISION,TypeInfo[j].PRECISION);
						LogMsg(NONE,_T("Literal Prefix actual: %s and expected: %s are matched\n"),oLITERAL_PREFIX,TypeInfo[j].LITERAL_PREFIX);
						LogMsg(NONE,_T("Literal Suffix actual: %s and expected: %s are matched\n"),oLITERAL_SUFFIX,TypeInfo[j].LITERAL_SUFFIX);
						LogMsg(NONE,_T("Create Params actual: %s and expected: %s are matched\n"),oCREATE_PARAMS,TypeInfo[j].CREATE_PARAMS);
						LogMsg(NONE,_T("Nullable actual: %d and expected: %d are matched\n"),oNULLABLE,TypeInfo[j].NULLABLE);
						LogMsg(NONE,_T("Case sensitive actual: %d and expected: %d are matched\n"),oCASE_SENSITIVE,TypeInfo[j].CASE_SENSITIVE);
						LogMsg(NONE,_T("Searchable actual: %d and expected: %d are matched\n"),oSEARCHABLE,TypeInfo[j].SEARCHABLE);
						LogMsg(NONE,_T("Unsigned attribute actual: %d and expected: %d are matched\n"),oUNSIGNED_ATTRIBUTE,TypeInfo[j].UNSIGNED_ATTRIBUTE);
						LogMsg(NONE,_T("Money actual: %d and expected: %d are matched\n"),oMONEY,TypeInfo[j].MONEY);
						LogMsg(NONE,_T("Auto Increment actual: %d and expected: %d are matched\n"),oAUTO_INCREMENT,TypeInfo[j].AUTO_INCREMENT);
						LogMsg(NONE,_T("Local Type name actual: %s and expected: %s are matched\n"),oLOCAL_TYPE_NAME,TypeInfo[j].LOCAL_TYPE_NAME);
						LogMsg(NONE,_T("Minimum Scale actual: %d and expected: %d are matched\n"),oMINIMUM_SCALE,TypeInfo[j].MINIMUM_SCALE);
						LogMsg(NONE,_T("Maximum Scale actual: %d and expected: %d are matched\n"),oMAXIMUM_SCALE,TypeInfo[j].MAXIMUM_SCALE);
					}	
					else
					{
						TEST_FAILED;	
						if (_tcsicmp(TypeInfo[j].TYPE_NAME,oTYPE_NAME) != 0)
							LogMsg(ERRMSG,_T("Data Type Name actual: %s and expected: %s are not matched\n"),oTYPE_NAME,TypeInfo[j].TYPE_NAME);
						if (TypeInfo[j].DATA_TYPE != oDATA_TYPE)
							LogMsg(ERRMSG,_T("Data Type actual: %d and expected: %d are not matched\n"),oDATA_TYPE,TypeInfo[j].DATA_TYPE);
						if (TypeInfo[j].PRECISION != oPRECISION)
							LogMsg(ERRMSG,_T("Precision actual: %d and expected: %d are not matched\n"),oPRECISION,TypeInfo[j].PRECISION);
						if (_tcsicmp(TypeInfo[j].LITERAL_PREFIX,oLITERAL_PREFIX) != 0)
							LogMsg(ERRMSG,_T("Literal Prefix actual: %s and expected: %s are not matched\n"),oLITERAL_PREFIX,TypeInfo[j].LITERAL_PREFIX);
						if (_tcsicmp(TypeInfo[j].LITERAL_SUFFIX,oLITERAL_SUFFIX) != 0)
							LogMsg(ERRMSG,_T("Literal Suffix actual: %s and expected: %s are not matched\n"),oLITERAL_SUFFIX,TypeInfo[j].LITERAL_SUFFIX);
						if (_tcsicmp(TypeInfo[j].CREATE_PARAMS,oCREATE_PARAMS) != 0)
							LogMsg(ERRMSG,_T("Create Params actual: %s and expected: %s are not matched\n"),oCREATE_PARAMS,TypeInfo[j].CREATE_PARAMS);
						if (TypeInfo[j].NULLABLE != oNULLABLE)
							LogMsg(ERRMSG,_T("Nullable actual: %d and expected: %d are not matched\n"),oNULLABLE,TypeInfo[j].NULLABLE);
						if (TypeInfo[j].CASE_SENSITIVE != oCASE_SENSITIVE)
							LogMsg(ERRMSG,_T("Case sensitive actual: %d and expected: %d are not matched\n"),oCASE_SENSITIVE,TypeInfo[j].CASE_SENSITIVE);
						if (TypeInfo[j].SEARCHABLE != oSEARCHABLE)
							LogMsg(ERRMSG,_T("Searchable actual: %d and expected: %d are not matched\n"),oSEARCHABLE,TypeInfo[j].SEARCHABLE);
						if (TypeInfo[j].UNSIGNED_ATTRIBUTE != oUNSIGNED_ATTRIBUTE)
							LogMsg(ERRMSG,_T("Unsigned attribute actual: %d and expected: %d are not matched\n"),oUNSIGNED_ATTRIBUTE,TypeInfo[j].UNSIGNED_ATTRIBUTE);
						if (TypeInfo[j].MONEY != oMONEY)
							LogMsg(ERRMSG,_T("Money actual: %d and expected: %d are not matched\n"),oMONEY,TypeInfo[j].MONEY);
						if (TypeInfo[j].AUTO_INCREMENT != oAUTO_INCREMENT)
							LogMsg(ERRMSG,_T("Auto Increment actual: %d and expected: %d are not matched\n"),oAUTO_INCREMENT,TypeInfo[j].AUTO_INCREMENT);
						if (_tcsicmp(TypeInfo[j].LOCAL_TYPE_NAME,oLOCAL_TYPE_NAME) != 0)
							LogMsg(ERRMSG,_T("Local Type name actual: %s and expected: %s are not matched\n"),oLOCAL_TYPE_NAME,TypeInfo[j].LOCAL_TYPE_NAME);
						if (TypeInfo[j].MINIMUM_SCALE != oMINIMUM_SCALE)
							LogMsg(ERRMSG,_T("Minimum Scale actual: %d and expected: %d are not matched\n"),oMINIMUM_SCALE,TypeInfo[j].MINIMUM_SCALE);
						if (TypeInfo[j].MAXIMUM_SCALE != oMAXIMUM_SCALE)
							LogMsg(ERRMSG,_T("Maximum Scale actual: %d and expected: %d are not matched\n"),oMAXIMUM_SCALE,TypeInfo[j].MAXIMUM_SCALE);
					}
				} 					
			}
		}
		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);	// This is a bug this should be after the inner for loop.
		j++;
	} 															
	
//==========================================================================================
	
	TESTCASE_BEGIN("SQLGetTypeInfo: Negative test for invalid data type\n");

	fSqlType1 = 50;
	returncode = SQLGetTypeInfo(hstmt,fSqlType1);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLGetTypeInfo"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

//=========================================================================================

	_stprintf(Heading,_T("SQLGetTypeInfo: Negative test with invalid handle\n"));
	TESTCASE_BEGINW(Heading);

	hstmt = (SQLHANDLE)NULL;
	fSqlType1 = 1;
	returncode = SQLGetTypeInfo(hstmt,fSqlType1);
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLGetTypeInfo"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	TESTCASE_END;

//=========================================================================================

	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLGetTypeInfo.\n"));
	TEST_RETURN;
}
