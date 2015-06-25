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

#define NAME_LEN		300
#define NUM_OUTPUTS		8
#define REM_LEN			254
#define NUM_PATTERN		5

/*
---------------------------------------------------------
   TestSQLProcedureColumns
---------------------------------------------------------
*/
PassFail TestMXSQLProcedureColumns(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
 	char			Heading[MAX_HEADING_SIZE];
 	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;
CHAR                    *myTestSch = "ODBC_PROCCOL_TEST";
CHAR                    createSchStr[128];
CHAR                    setSchStr[128];
CHAR                    dropSchStr[128];

	CHAR			*ProcStr;
    CHAR            ServerName[NAME_LEN];
    char            SerName[4];
    SQLSMALLINT     serLen;
  	CHAR			ProcCatalog[NAME_LEN],ProcSchema[NAME_LEN],ProcName[NAME_LEN];
    CHAR            ColName[NAME_LEN];
	CHAR			oProcCatalog[NAME_LEN];
	CHAR			oProcSchema[NAME_LEN];
	CHAR			oProcName[NAME_LEN];
	CHAR			oColName[NAME_LEN];
	SWORD			oColType;
	SWORD			oColDataType;
	CHAR			oColTypeName[NAME_LEN];
	SDWORD			oColSize;
	SDWORD			oBufferLen;
	SWORD			oDecDigits;
	SWORD			oColRadix;
	SWORD			oColNullable;
	CHAR			oRemark[REM_LEN];
	CHAR			oColDef[NAME_LEN];
	SWORD			oSQLDataType;
	SWORD			oSQLDateTimeSub;
	SDWORD			oCharOctetLen;
	SDWORD			oOrdinalPos;
	CHAR			oIsNullable[NAME_LEN];
	SQLLEN		oProcCataloglen; 
	SQLLEN		oProcSchemalen;
	SQLLEN		oProcNamelen;
	SQLLEN		oColNamelen;
	SQLLEN		oColTypelen;
	SQLLEN		oColDataTypelen;
	SQLLEN		oColTypeNamelen;
	SQLLEN		oColSizelen;
	SQLLEN		oBufferLenlen;
	SQLLEN		oDecDigitslen;
	SQLLEN		oColRadixlen;
	SQLLEN		oColNullablelen;
	SQLLEN		oRemarklen;
	SQLLEN		oColDeflen;
	SQLLEN		oSQLDataTypelen;
	SQLLEN		oSQLDateTimeSublen;
	SQLLEN		oCharOctetLenlen;
	SQLLEN		oOrdinalPoslen;
	SQLLEN		oIsNullablelen;

	struct	
	{
		CHAR		*DropProc;
		CHAR		*CrtProc;
	} CreateProc[] = {
							{"DROP PROCEDURE N4210_REG",
							 "CREATE PROCEDURE N4210_REG (IN IN1 TIME) EXTERNAL NAME 'Procs.N4210' EXTERNAL PATH '/home/SQFQA/SPJRoot/odbctest_spjs' LANGUAGE JAVA PARAMETER STYLE JAVA NO SQL NO ISOLATE"},
							{"DROP PROCEDURE N4260_REG",
							 "CREATE PROCEDURE N4260_REG (IN IN1 REAL, INOUT INOUT1 INTEGER) EXTERNAL NAME 'Procs.N4260' EXTERNAL PATH '/home/SQFQA/SPJRoot/odbctest_spjs' LANGUAGE JAVA PARAMETER STYLE JAVA NO SQL NO ISOLATE"},
							{"DROP PROCEDURE N4261_REG",
 							 "CREATE PROCEDURE N4261_REG (IN IN1 NUMERIC, INOUT INOUT1 REAL) EXTERNAL NAME 'Procs.N4261' EXTERNAL PATH '/home/SQFQA/SPJRoot/odbctest_spjs' LANGUAGE JAVA PARAMETER STYLE JAVA NO SQL NO ISOLATE"},
							{"DROP PROCEDURE N4264_REG",
 							 "CREATE PROCEDURE N4264_REG (IN IN1 VARCHAR(30), OUT OUT1 VARCHAR(45)) EXTERNAL NAME 'Procs.N4264' EXTERNAL PATH '/home/SQFQA/SPJRoot/odbctest_spjs' LANGUAGE JAVA PARAMETER STYLE JAVA NO SQL NO ISOLATE"},	
							{"DROP PROCEDURE N4267_REG",
 							 "CREATE PROCEDURE N4267_REG (IN IN1 NUMERIC, INOUT INOUT1 REAL) EXTERNAL NAME 'Procs.N4267' EXTERNAL PATH '/home/SQFQA/SPJRoot/odbctest_spjs' LANGUAGE JAVA PARAMETER STYLE JAVA NO SQL NO ISOLATE"},
							{"endloop","endloop"}
					};

	struct
	{
		CHAR       *ProcName;
		CHAR		*ColName;
		SWORD		ColType;
		SWORD		ColDataType;
		CHAR		*ColTypeName;
		SDWORD		ColSize;
		SDWORD		BufferLen;
		SWORD		DecDigits;
		SWORD		ColRadix;
		SWORD		ColNullable;
		CHAR		*Remark;
		CHAR       *ColDef;
		SWORD       SQLDataType;
		SWORD       SQLDateTimeSub;
		SDWORD		CharOctetLen;
		SDWORD		OrdinalPos;
		CHAR		*IsNullable;
	} ProcCol[] = {
/*		{"N4210", "IN1",	SQL_PARAM_INPUT,		SQL_TYPE_TIME,	"TIME",			8,	 6, 0, <Null>,	SQL_NULLABLE, <Null>, <Null>, 9,	  2, <Null>, 1, "YES"},
		{"N4260", "IN1",	SQL_PARAM_INPUT,		SQL_REAL,		"REAL",			22,  4, 0, 2,		SQL_NULLABLE, <Null>, <Null>, 7, <Null>, <Null>, 1, "YES"},
		{"N4260", "INOUT1", SQL_PARAM_INPUT_OUTPUT, SQL_INTEGER, "INTEGER SIGNED",	10,  4, 0, 10,		SQL_NULLABLE, <Null>, <Null>, 4, <Null>, <Null>, 2, "YES"},
		{"N4261", "IN1",	SQL_PARAM_INPUT,		SQL_NUMERIC, "NUMERIC",			9,  11, 0, 10,		SQL_NULLABLE, <Null>, <Null>, 2, <Null>, <Null>, 1, "YES"},
		{"N4261", "INOUT1", SQL_PARAM_INPUT_OUTPUT, SQL_REAL,	 "REAL",			22,  4, 0, 2,		SQL_NULLABLE, <Null>, <Null>, 7, <Null>, <Null>, 2, "YES"},
		{"N4264", "IN1",	SQL_PARAM_INPUT,		SQL_VARCHAR, "VARCHAR",			30, 30, 0, <Null>,	SQL_NULLABLE, <Null>, <Null>, 12,<Null>,     30, 1, "YES"},
		{"N4264", "OUT1",	SQL_PARAM_OUTPUT,		SQL_VARCHAR, "VARCHAR",			45, 45, 0, <Null>,	SQL_NULLABLE, <Null>, <Null>, 12,<Null>,     45, 2, "YES"},
		{"N4267", "IN1",	SQL_PARAM_INPUT,		SQL_NUMERIC, "NUMERIC",			9,  11, 0, 10,		SQL_NULLABLE, <Null>, <Null>, 2, <Null>, <Null>, 1, "YES"},
		{"N4267", "INOUT1", SQL_PARAM_INPUT_OUTPUT, SQL_REAL,	 "REAL",			22,	 4, 0, 2,		SQL_NULLABLE, <Null>, <Null>, 7, <Null>, <Null>, 2, "YES"},
*/
		{"N4210_REG", "IN1",	SQL_PARAM_INPUT,		SQL_TYPE_TIME,	"TIME",			8,	 6, 0, 0,	SQL_NULLABLE, "", "", 9, 2, 0, 1, "YES"},
		{"N4260_REG", "IN1",	SQL_PARAM_INPUT,		SQL_REAL,		"REAL",			22,  4, 0, 2,	SQL_NULLABLE, "", "", 7, 0, 0, 1, "YES"},
		{"N4260_REG", "INOUT1", SQL_PARAM_INPUT_OUTPUT, SQL_INTEGER, "INTEGER SIGNED",	10,  4, 0, 10,	SQL_NULLABLE, "", "", 4, 0, 0, 2, "YES"},
		{"N4261_REG", "IN1",	SQL_PARAM_INPUT,		SQL_NUMERIC, "NUMERIC SIGNED",	9,  11, 0, 10,	SQL_NULLABLE, "", "", 2, 0, 0, 1, "YES"},
		{"N4261_REG", "INOUT1", SQL_PARAM_INPUT_OUTPUT, SQL_REAL,	 "REAL",			22,  4, 0, 2,	SQL_NULLABLE, "", "", 7, 0, 0, 2, "YES"},
		{"N4264_REG", "IN1",	SQL_PARAM_INPUT,		SQL_VARCHAR, "VARCHAR",			30, 30, 0, 0,	SQL_NULLABLE, "", "", 12,0, 30,1, "YES"},
		{"N4264_REG", "OUT1",	SQL_PARAM_OUTPUT,		SQL_VARCHAR, "VARCHAR",			45, 45, 0, 0,	SQL_NULLABLE, "", "", 12,0, 45,2, "YES"},
		{"N4267_REG", "IN1",	SQL_PARAM_INPUT,		SQL_NUMERIC, "NUMERIC SIGNED",	9,  11, 0, 10,	SQL_NULLABLE, "", "", 2, 0, 0, 1, "YES"},
		{"N4267_REG", "INOUT1", SQL_PARAM_INPUT_OUTPUT, SQL_REAL,	 "REAL",			22,	 4, 0, 2,	SQL_NULLABLE, "", "", 7, 0, 0, 2, "YES"},
		{"endloop",}
	};

	
	int	i = 0, k = 0;
    char *charNameUCS2 = "WIDE CHARACTER";
	char *varcharNameUCS2 = "WIDE VARCHAR";
	
	LogMsg(SHORTTIMESTAMP,"Begin testing API => MX Specific SQLProcedureColumns | SQLProcedureColumns | MXProcCol.c\n");

//=================================================================================================
	if(isUCS2) {
		LogMsg(NONE,"Setup for UCS2 mode testing: ColSize,BufferLen and CharOctetlen has to be doubled\n");

		k = sizeof(ProcCol)/sizeof(ProcCol[0]);
		while(i < k) {
			if(ProcCol[i].ColDataType == SQL_CHAR)
			{
				//ProcCol[i].ColDataType = SQL_WCHAR;
				//ProcCol[i].SQLDataType = SQL_WCHAR;
				//ProcCol[i].ColTypeName = charNameUCS2;
				ProcCol[i].ColSize *= 2;  //--> This is in character, no need to double
				ProcCol[i].BufferLen *= 2;
				ProcCol[i].CharOctetLen *= 2;
			}
			else if (ProcCol[i].ColDataType == SQL_VARCHAR)
			{
				//ProcCol[i].ColDataType = SQL_WVARCHAR;
				//ProcCol[i].SQLDataType = SQL_WVARCHAR;
				//ProcCol[i].ColTypeName = varcharNameUCS2;
				ProcCol[i].ColSize *= 2; //--> This is in character, no need to double
				ProcCol[i].BufferLen *= 2;
				ProcCol[i].CharOctetLen *= 2;
			}
			else if (ProcCol[i].ColDataType == SQL_LONGVARCHAR)
			{
				//ProcCol[i].ColDataType = SQL_WLONGVARCHAR;
				//ProcCol[i].SQLDataType = SQL_WLONGVARCHAR;
				//ProcCol[i].ColTypeName = varcharNameUCS2;
				ProcCol[i].ColSize *= 2; //--> This is in character, no need to double
				ProcCol[i].BufferLen *= 2;
				ProcCol[i].CharOctetLen *= 2;
			}
			else {}

			i++;
		}
		i = 0;
		k = 0;
	}
//=================================================================================================

	
	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLProcedureColumns tests\n");

	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,"Unable to connect\n");
		//TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
 	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect3(pTestInfo);
		//TEST_FAILED;
		TEST_RETURN;
	}

    returncode = SQLGetInfo(hdbc, SQL_SERVER_NAME, (SQLPOINTER)&ServerName, NAME_LEN, &serLen);

    strncpy(SerName, ServerName+1, 3);
    SerName[3] = '\0';

   /* sq: This test calls SQLProcedures() with wildcard characters.  It
    * needs its own empty schema to create the procedures,  Otherwise the
    * standard schema that everybody uses may already have other procedures
    * created and will be returned by SQLProcedures() to confuse the test.
    */
   sprintf (createSchStr, "CREATE SCHEMA %s.%s", pTestInfo->Catalog, myTestSch);
   sprintf (setSchStr, "SET SCHEMA %s.%s", pTestInfo->Catalog, myTestSch);
   sprintf (dropSchStr, "DROP SCHEMA %s.%s cascade", pTestInfo->Catalog, myTestSch);
   returncode = SQLExecDirect(hstmt,(SQLCHAR*) dropSchStr,SQL_NTS);
   returncode = SQLExecDirect(hstmt,(SQLCHAR*) createSchStr,SQL_NTS);
   returncode = SQLExecDirect(hstmt,(SQLCHAR*) setSchStr,SQL_NTS);

	ProcStr = (char *)malloc(MAX_NOS_SIZE);

	while (_stricmp(CreateProc[i].DropProc,"endloop") != 0)
	{
		sprintf(ProcStr,CreateProc[i].DropProc);
		SQLExecDirect(hstmt,(SQLCHAR*) ProcStr,SQL_NTS); // cleanup
		sprintf(ProcStr,CreateProc[i].CrtProc);
		replace_str(ProcStr,"$$$",SerName);
		sprintf(Heading,"Adding Procedure => %s\n",ProcStr);
		TESTCASE_BEGIN(Heading);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)ProcStr,SQL_NTS);
		if(returncode != SQL_SUCCESS)
		{
            TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;
		i++;
	}

	strcpy(ProcCatalog, pTestInfo->Catalog);
	strcpy(ProcSchema, myTestSch /*pTestInfo->Schema*/);
	
	sprintf(Heading,"Test Positive Functionality of SQLProcedureColumns \n");
	TESTCASE_BEGIN(Heading);
	returncode = SQLProcedureColumns(hstmt,(SQLCHAR*)pTestInfo->Catalog,(SWORD)strlen(pTestInfo->Catalog),(SQLCHAR*)myTestSch/*pTestInfo->Schema*/,(SWORD)strlen(myTestSch/*pTestInfo->Schema*/),(SQLCHAR *)"%",(SWORD)1,(SQLCHAR *)"%",(SWORD)1);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLProcedureColumns"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
	if (returncode == SQL_SUCCESS)
		{
			strcpy(oProcCatalog,"");
			strcpy(oProcSchema,"");
			strcpy(oProcName,"");
			strcpy(oColName,"");
			oColType = 0;
			oColDataType = 0;
			strcpy(oColTypeName,"");
			oColSize = 0;
			oBufferLen = 0;
			oDecDigits = 0;
			oColRadix = 0;
			oColNullable = 0;
			strcpy(oRemark,"");
			strcpy(oColDef,"");
			oSQLDataType = 0;
			oSQLDateTimeSub = 0;
			oCharOctetLen = 0;
			oOrdinalPos = 0;
			strcpy(oIsNullable,"");
			SQLBindCol(hstmt,1,SQL_C_CHAR,oProcCatalog,NAME_LEN,&oProcCataloglen);
			SQLBindCol(hstmt,2,SQL_C_CHAR,oProcSchema,NAME_LEN,&oProcSchemalen);
			SQLBindCol(hstmt,3,SQL_C_CHAR,oProcName,NAME_LEN,&oProcNamelen);
			SQLBindCol(hstmt,4,SQL_C_CHAR,oColName,NAME_LEN,&oColNamelen);
			SQLBindCol(hstmt,5,SQL_C_SHORT,&oColType,0,&oColTypelen);
			SQLBindCol(hstmt,6,SQL_C_SHORT,&oColDataType,0,&oColDataTypelen);
			SQLBindCol(hstmt,7,SQL_C_CHAR,oColTypeName,NAME_LEN,&oColTypeNamelen);
			SQLBindCol(hstmt,8,SQL_C_LONG,&oColSize,0,&oColSizelen);
			SQLBindCol(hstmt,9,SQL_C_LONG,&oBufferLen,0,&oBufferLenlen);
			SQLBindCol(hstmt,10,SQL_C_SHORT,&oDecDigits,0,&oDecDigitslen);
			SQLBindCol(hstmt,11,SQL_C_SHORT,&oColRadix,0,&oColRadixlen);
			SQLBindCol(hstmt,12,SQL_C_SHORT,&oColNullable,0,&oColNullablelen);
			SQLBindCol(hstmt,13,SQL_C_CHAR,oRemark,REM_LEN,&oRemarklen);
			SQLBindCol(hstmt,14,SQL_C_CHAR,oColDef,NAME_LEN,&oColDeflen);
			SQLBindCol(hstmt,15,SQL_C_SHORT,&oSQLDataType,0,&oSQLDataTypelen);
			SQLBindCol(hstmt,16,SQL_C_SHORT,&oSQLDateTimeSub,0,&oSQLDateTimeSublen);
			SQLBindCol(hstmt,17,SQL_C_LONG,&oCharOctetLen,0,&oCharOctetLenlen);
			SQLBindCol(hstmt,18,SQL_C_LONG,&oOrdinalPos,0,&oOrdinalPoslen);
			SQLBindCol(hstmt,19,SQL_C_CHAR,oIsNullable,NAME_LEN,&oIsNullablelen);
			k = 0;
			i = 0;
			while (returncode == SQL_SUCCESS)
			{
				if(strcmp(ProcCol[i].ProcName,"endloop") == 0)
					break;
				returncode = SQLFetch(hstmt);
				if((returncode!=SQL_NO_DATA_FOUND) &&(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")))
					{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
					}
				else
					{
					if (returncode == SQL_SUCCESS)
						{
						k++;
						sprintf(Heading,"SQLProcedureColumns: Comparing Results\n");
						TESTCASE_BEGIN(Heading);
						if ((_stricmp(ProcCatalog,oProcCatalog) == 0) 
						&& (_stricmp(ProcSchema,oProcSchema) == 0) 
						&& (_stricmp(ProcCol[i].ProcName,oProcName) == 0) 
						&& (_stricmp(ProcCol[i].ColName,oColName) == 0) 
						&& (ProcCol[i].ColType == oColType) 
						&& (ProcCol[i].ColDataType == oColDataType) 
						&& (_stricmp(ProcCol[i].ColTypeName,oColTypeName) == 0) 
						&& (ProcCol[i].ColSize == oColSize)
						&& (ProcCol[i].BufferLen == oBufferLen)
						&& (ProcCol[i].DecDigits == oDecDigits)
						&& (ProcCol[i].ColRadix == oColRadix)
						&& (ProcCol[i].ColNullable == oColNullable)
						&& (_stricmp(ProcCol[i].Remark,oRemark) == 0)
 						&& (_stricmp(ProcCol[i].ColDef,oColDef) == 0)
						&& (ProcCol[i].SQLDataType == oSQLDataType)
						&& (ProcCol[i].SQLDateTimeSub == oSQLDateTimeSub)
						&& (ProcCol[i].CharOctetLen == oCharOctetLen)
						&& (ProcCol[i].OrdinalPos == oOrdinalPos)
						&& (_stricmp(ProcCol[i].IsNullable,oIsNullable) == 0)){
							//LogMsg(NONE,"ProcCatalog expect: %s and actual: %s are matched\n",ProcCatalog,oProcCatalog);
							//LogMsg(NONE,"ProcSchema expect: %s and actual: %s are matched\n",ProcSchema,oProcSchema);
							//LogMsg(NONE,"ProcName expect: %s and actual: %s are matched\n",ProcCol[i].ProcName,oProcName);
							//LogMsg(NONE,"ColName expect: %s and actual: %s are matched\n",ProcCol[i].ColName,oColName);
							//LogMsg(NONE,"ColType expect: %d and actual: %d are matched\n",ProcCol[i].ColType,oColType);
							//LogMsg(NONE,"ColDataType expect: %d and actual: %d are matched\n",ProcCol[i].ColDataType,oColDataType);
							//LogMsg(NONE,"ColTypeName expect: %s and actual: %s are matched\n",ProcCol[i].ColTypeName,oColTypeName);
							//LogMsg(NONE,"ColSize expect: %d and actual: %d are matched\n",ProcCol[i].ColSize,oColSize);
							//LogMsg(NONE,"BufferLen expect: %d and actual: %d are matched\n",ProcCol[i].BufferLen,oBufferLen);
							//LogMsg(NONE,"DecDigits expect: %d and actual: %d are matched\n",ProcCol[i].DecDigits,oDecDigits);
							//LogMsg(NONE,"ColRadix expect: %d and actual: %d are matched\n",ProcCol[i].ColRadix,oColRadix);
							//LogMsg(NONE,"ColNullable expect: %d and actual: %d are matched\n",ProcCol[i].ColNullable,oColNullable);
							//LogMsg(NONE,"Remark expect: %s and actual: %s are matched\n",ProcCol[i].Remark,oRemark);
							//LogMsg(NONE,"ColDef expect: %s and actual: %s are matched\n",ProcCol[i].ColDef,oColDef);
							//LogMsg(NONE,"SQLDataType expect: %d and actual: %d are matched\n",ProcCol[i].SQLDataType,oSQLDataType);
							//LogMsg(NONE,"SQLDateTimeSub expect: %d and actual: %d are matched\n",ProcCol[i].SQLDateTimeSub,oSQLDateTimeSub);
							//LogMsg(NONE,"CharOctetLen expect: %d and actual: %d are matched\n",ProcCol[i].CharOctetLen,oCharOctetLen);
							//LogMsg(NONE,"OrdinalPos expect: %d and actual: %d are matched\n",ProcCol[i].OrdinalPos,oOrdinalPos);
							//LogMsg(NONE,"IsNullable expect: %s and actual: %s are matched\n",ProcCol[i].IsNullable,oIsNullable);
							}	
						else
							{
							TEST_FAILED;	
							if (_stricmp(ProcCatalog,oProcCatalog) != 0)
								LogMsg(ERRMSG,"ProcCatalog expect: %s and actual: %s are not matched\n",ProcCatalog,oProcCatalog);
							else
								LogMsg(NONE,"ProcCatalog expect: %s and actual: %s are matched\n",ProcCatalog,oProcCatalog);
							if (_stricmp(ProcSchema,oProcSchema) != 0) 
								LogMsg(ERRMSG,"ProcSchema expect: %s and actual: %s are not matched\n",ProcSchema,oProcSchema);
							else
								LogMsg(NONE,"ProcSchema expect: %s and actual: %s are matched\n",ProcSchema,oProcSchema);
							if (_stricmp(ProcCol[i].ProcName,oProcName) != 0) 
								LogMsg(ERRMSG,"ProcName expect: %s and actual: %s are not matched\n",ProcCol[i].ProcName,oProcName);
							else
								LogMsg(NONE,"ProcName expect: %s and actual: %s are matched\n",ProcCol[i].ProcName,oProcName);							
							if (_stricmp(ProcCol[i].ColName,oColName) != 0) 
								LogMsg(ERRMSG,"ColName expect: %s and actual: %s are not matched\n",ProcCol[i].ColName,oColName);
							else
								LogMsg(NONE,"ColName expect: %s and actual: %s are matched\n",ProcCol[i].ColName,oColName);
							if (ProcCol[i].ColType != oColType) 
								LogMsg(ERRMSG,"ColType expect: %d and actual: %d are not matched\n",ProcCol[i].ColType,oColType);
							else	
								LogMsg(NONE,"ColType expect: %d and actual: %d are matched\n",ProcCol[i].ColType,oColType);
							if (ProcCol[i].ColDataType != oColDataType) 
								LogMsg(ERRMSG,"ColDataType expect: %d and actual: %d are not matched\n",ProcCol[i].ColDataType,oColDataType);
							else	
								LogMsg(NONE,"ColDataType expect: %d and actual: %d are matched\n",ProcCol[i].ColDataType,oColDataType);
							if (_stricmp(ProcCol[i].ColTypeName,oColTypeName) != 0) 
								LogMsg(ERRMSG,"ColTypeName expect: %s and actual: %s are not matched\n",ProcCol[i].ColTypeName,oColTypeName);
							else							
								LogMsg(NONE,"ColTypeName expect: %s and actual: %s are matched\n",ProcCol[i].ColTypeName,oColTypeName);
							if (ProcCol[i].ColSize != oColSize)
								LogMsg(ERRMSG,"ColSize expect: %d and actual: %d are not matched\n",ProcCol[i].ColSize,oColSize);
							else	
								LogMsg(NONE,"ColSize expect: %d and actual: %d are matched\n",ProcCol[i].ColSize,oColSize);
							if (ProcCol[i].BufferLen != oBufferLen)
								LogMsg(ERRMSG,"BufferLen expect: %d and actual: %d are not matched\n",ProcCol[i].BufferLen,oBufferLen);
							else	
								LogMsg(NONE,"BufferLen expect: %d and actual: %d are matched\n",ProcCol[i].BufferLen,oBufferLen);							
							if (ProcCol[i].DecDigits != oDecDigits)
								LogMsg(ERRMSG,"DecDigits expect: %d and actual: %d are not matched\n",ProcCol[i].DecDigits,oDecDigits);
							else	
								LogMsg(NONE,"DecDigits expect: %d and actual: %d are matched\n",ProcCol[i].DecDigits,oDecDigits);					
							if (ProcCol[i].ColRadix != oColRadix)
								LogMsg(ERRMSG,"ColRadix expect: %d and actual: %d are not matched\n",ProcCol[i].ColRadix,oColRadix);
							else	
								LogMsg(NONE,"ColRadix expect: %d and actual: %d are matched\n",ProcCol[i].ColRadix,oColRadix);						
							if (ProcCol[i].ColNullable != oColNullable)
								LogMsg(ERRMSG,"ColNullable expect: %d and actual: %d are not matched\n",ProcCol[i].ColNullable,oColNullable);
							else	
								LogMsg(NONE,"ColNullable expect: %d and actual: %d are matched\n",ProcCol[i].ColNullable,oColNullable);						
							if (_stricmp(ProcCol[i].Remark,oRemark) != 0)
								LogMsg(ERRMSG,"Remark expect: %s and actual: %s are not matched\n",ProcCol[i].Remark,oRemark);
							else	
								LogMsg(NONE,"Remark expect: %s and actual: %s are matched\n",ProcCol[i].Remark,oRemark);
							if (_stricmp(ProcCol[i].ColDef,oColDef) != 0)
								LogMsg(ERRMSG,"Remark expect: %s and actual: %s are not matched\n",ProcCol[i].ColDef,oColDef);
							else	
								LogMsg(NONE,"Remark expect: %s and actual: %s are matched\n",ProcCol[i].ColDef,oColDef);
							if (ProcCol[i].SQLDataType != oSQLDataType)
								LogMsg(ERRMSG,"SQLDataType expect: %d and actual: %d are not matched\n",ProcCol[i].SQLDataType,oSQLDataType);
							else	
								LogMsg(NONE,"SQLDataType expect: %d and actual: %d are matched\n",ProcCol[i].SQLDataType,oSQLDataType);
							if (ProcCol[i].SQLDateTimeSub != oSQLDateTimeSub)
								LogMsg(ERRMSG,"SQLDateTimeSub expect: %d and actual: %d are not matched\n",ProcCol[i].SQLDateTimeSub,oSQLDateTimeSub);
							else	
								LogMsg(NONE,"SQLDateTimeSub expect: %d and actual: %d are matched\n",ProcCol[i].SQLDateTimeSub,oSQLDateTimeSub);
							if (ProcCol[i].CharOctetLen != oCharOctetLen)
								LogMsg(ERRMSG,"CharOctetLen expect: %d and actual: %d are not matched\n",ProcCol[i].CharOctetLen,oCharOctetLen);
							else	
								LogMsg(NONE,"CharOctetLen expect: %d and actual: %d are matched\n",ProcCol[i].CharOctetLen,oCharOctetLen);
							if (ProcCol[i].OrdinalPos != oOrdinalPos)
								LogMsg(ERRMSG,"OrdinalPos expect: %d and actual: %d are not matched\n",ProcCol[i].OrdinalPos,oOrdinalPos);
							else	
								LogMsg(NONE,"OrdinalPos expect: %d and actual: %d are matched\n",ProcCol[i].OrdinalPos,oOrdinalPos);
							if (_stricmp(ProcCol[i].IsNullable,oIsNullable) != 0)
								LogMsg(ERRMSG,"IsNullable expect: %s and actual: %s are not matched\n",ProcCol[i].IsNullable,oIsNullable);
							else	
								LogMsg(NONE,"IsNullable expect: %s and actual: %s are matched\n",ProcCol[i].IsNullable,oIsNullable);
							}
						}
					}
					if(k == 0)
					{
						TEST_FAILED;
						LogMsg(ERRMSG,"No Data Found => Atleast one row should be fetched\n");
					}
			TESTCASE_END;
			strcpy(oProcCatalog,"");
			strcpy(oProcSchema,"");
			strcpy(oProcName,"");
			strcpy(oColName,"");
			oColType = 0;
			oColDataType = 0;
			strcpy(oColTypeName,"");
			oColSize = 0;
			oBufferLen = 0;
			oDecDigits = 0;
			oColRadix = 0;
			oColNullable = 0;
			strcpy(oRemark,"");
			strcpy(oColDef,"");
			oSQLDataType = 0;
			oSQLDateTimeSub = 0;
			oCharOctetLen = 0;
			oOrdinalPos = 0;
			strcpy(oIsNullable,"");
			i++;
			} // while
		}
	SQLFreeStmt(hstmt,SQL_UNBIND);
	SQLFreeStmt(hstmt,SQL_CLOSE);
	

	//========================================================================================================

	sprintf(Heading,"SQLProcedureColumns: Negative test with NULL handle\n");
	TESTCASE_BEGIN(Heading);

	hstmt = (SQLHANDLE)NULL;
	strcpy(ProcName,"junkproc");
	strcpy(ColName,"C1");

	returncode = SQLProcedureColumns(hstmt,(SQLCHAR*)pTestInfo->Catalog,(SWORD)strlen(pTestInfo->Catalog),(SQLCHAR*)myTestSch/*pTestInfo->Schema*/,(SWORD)strlen(myTestSch/*pTestInfo->Schema*/),(SQLCHAR*)ProcName,(SWORD)strlen(ProcName),(SQLCHAR*)ColName,(SWORD)strlen(ColName));
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLProcedureColumns"))
	{
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
	}
	returncode = SQLExecDirect(hstmt,(SQLCHAR*) dropSchStr,SQL_NTS);
	TESTCASE_END;

	//========================================================================================================

	free(ProcStr);
	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => MX Specific SQLProcedureColumns.\n");
	TEST_RETURN;
}
