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

#define	RGB_MAX_LEN			50
#define	RGB_COLUMNS			6
#define	PF_COLUMNS			13
#define DIFF_WAYS			3
#define	NUMBER_OF_COLUMNS	26


/*
---------------------------------------------------------
   TestSQLColAttributes
---------------------------------------------------------
*/
PassFail TestMXSQLColAttributes(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	char		TempStr[50];
	char		Heading[MAX_STRING_SIZE];
	RETCODE		returncode;
	SQLHANDLE 	henv;
 	SQLHANDLE 	hdbc;
 	SQLHANDLE	hstmt;
	SWORD		numcol;
	UWORD		icol = 0,iatt = 0;
	SWORD		totalatt = 19;
	CHAR		rgbDesc[RGB_MAX_LEN];
	SWORD		pcbDesc;

#ifdef _LP64
	SQLINTEGER pfDesc_4bytes; //  
	SQLLEN	   pfDesc_8bytes; //  
#endif
	SQLLEN		pfDesc; // Use for 32 bit
	int			dw;
	CHAR		tableName[MAX_TABLE_NAME]; //testcolatt1
	CHAR		columnName[NUMBER_OF_COLUMNS][MAX_COLUMN_NAME];
	CHAR		*ExecDirStr[4];
	
	// The values in this struct corelate to those in DescType[].
	struct
	{
		SQLLEN	pDes[PF_COLUMNS]; 
		CHAR	*rDes[RGB_COLUMNS];
	} ColAttr[] = {
					{0, 1, NUMBER_OF_COLUMNS,  10,  10, 0, 1,  10,  0, 3,  1, 1, 2,columnName[0] ,"CHAR",            pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[0]},
					{0, 1, NUMBER_OF_COLUMNS,  10,  10, 0, 1,  10,  0, 3, 12, 1, 2,columnName[1] ,"VARCHAR",         pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[1]},
					{0, 0, NUMBER_OF_COLUMNS,  12,  12, 1, 1,  10,  5, 2,  3, 0, 2,columnName[2] ,"DECIMAL",         pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[2]},
					{0, 0, NUMBER_OF_COLUMNS,   7,   7, 1, 1,   5,  2, 2,  3, 1, 2,columnName[3] ,"DECIMAL",         pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[3]},
					{0, 0, NUMBER_OF_COLUMNS,  12,  12, 1, 1,  10,  5, 2,  2, 0, 2,columnName[4] ,"NUMERIC",         pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[4]},
					{0, 0, NUMBER_OF_COLUMNS,   7,   7, 1, 1,   5,  2, 2,  2, 1, 2,columnName[5] ,"NUMERIC",         pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[5]},
					{0, 0, NUMBER_OF_COLUMNS,   6,   2, 0, 1,   5,  0, 2,  5, 0, 2,columnName[6] ,"SMALLINT",        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[6]},
					{0, 0, NUMBER_OF_COLUMNS,  11,   4, 0, 1,  10,  0, 2,  4, 0, 2,columnName[7],"INTEGER",		     pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[7]},					
					{0, 0, NUMBER_OF_COLUMNS,  11,   4, 0, 1,  10,  0, 2,  4, 0, 2,columnName[8] ,"INTEGER",         pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[8]},
					{0, 0, NUMBER_OF_COLUMNS,  20,  20, 0, 1,  19,  0, 2, -5, 0, 2,columnName[9],"BIGINT",			 pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[9]},				
					{0, 0, NUMBER_OF_COLUMNS,  13,   4, 0, 1,   7,  0, 2,  7, 0, 2,columnName[10],"REAL",            pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[10]},
					{0, 0, NUMBER_OF_COLUMNS,  22,   8, 0, 1,  15,  0, 2,  8, 0, 2,columnName[11],"DOUBLE PRECISION",pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[11]},
					{0, 0, NUMBER_OF_COLUMNS,  22,   8, 0, 1,  15,  0, 2,  8, 0, 2,columnName[12],"DOUBLE PRECISION",pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[12]},
					{0, 0, NUMBER_OF_COLUMNS,  10,   6, 0, 1,  10,  0, 2,  9, 1, 2,columnName[13],"DATE",            pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[13]},
					{0, 0, NUMBER_OF_COLUMNS,   8,   6, 0, 1,   8,  0, 2, 10, 1, 2,columnName[14],"TIME",            pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[14]},
					{0, 0, NUMBER_OF_COLUMNS,  26,  16, 0, 1,  26,  6, 2, 11, 1, 2,columnName[15],"TIMESTAMP",       pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[15]},
					{0, 0, NUMBER_OF_COLUMNS,  20,  20, 0, 1,  19,  0, 2, -5, 0, 2,columnName[16],"BIGINT",          pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[16]},
					{0, 1, NUMBER_OF_COLUMNS,2000,2000, 0, 1,2000,  0, 3, -1, 1, 2,columnName[17],"LONG VARCHAR",    pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[17]},
					{0, 0, NUMBER_OF_COLUMNS,  21,  21, 0, 1,  19,  0, 2,  2, 0, 2,columnName[18] ,"NUMERIC",        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[18]},
                    {0, 0, NUMBER_OF_COLUMNS,  21,  21, 1, 1,  19,  6, 2,  2, 0, 2,columnName[19] ,"NUMERIC",        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[19]},
					{0, 0, NUMBER_OF_COLUMNS, 130, 130, 0, 1, 128,  0, 2,  2, 0, 2,columnName[20] ,"NUMERIC",        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[20]},
					{0, 0, NUMBER_OF_COLUMNS, 130, 130, 1, 1, 128,128, 2,  2, 0, 2,columnName[21] ,"NUMERIC",        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[21]},
					{0, 0, NUMBER_OF_COLUMNS, 130, 130, 1, 1, 128, 64, 2,  2, 0, 2,columnName[22] ,"NUMERIC",        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[22]},
					{0, 0, NUMBER_OF_COLUMNS,  12,  12, 1, 1,  10,  5, 2,  2, 1, 2,columnName[23] ,"NUMERIC",        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[23]},
					{0, 0, NUMBER_OF_COLUMNS,  20,  20, 1, 1,  18,  5, 2,  2, 1, 2,columnName[24] ,"NUMERIC",        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[24]},
					{0, 0, NUMBER_OF_COLUMNS,  32,  32, 1, 1,  30, 10, 2,  2, 1, 2,columnName[25] ,"NUMERIC",        pTestInfo->Schema, pTestInfo->Catalog,tableName, columnName[25]}	
                };
	UWORD		DescType[] = {
					SQL_COLUMN_AUTO_INCREMENT,
					SQL_COLUMN_CASE_SENSITIVE,
					SQL_COLUMN_COUNT,
					SQL_COLUMN_DISPLAY_SIZE,
					SQL_COLUMN_LENGTH,
					SQL_COLUMN_MONEY,
					SQL_COLUMN_NULLABLE,
					SQL_COLUMN_PRECISION,
					SQL_COLUMN_SCALE,
					SQL_COLUMN_SEARCHABLE,
					SQL_COLUMN_TYPE,
					SQL_COLUMN_UNSIGNED,
					SQL_COLUMN_UPDATABLE,
					SQL_COLUMN_NAME,
					SQL_COLUMN_TYPE_NAME,
					SQL_COLUMN_OWNER_NAME,
					SQL_COLUMN_QUALIFIER_NAME,
					SQL_COLUMN_TABLE_NAME,
					SQL_COLUMN_LABEL
					};

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLColumnAttribute", charset_file);
	if (var_list == NULL) return FAILED;
//================Modified for Longvarchar Changes===========================================================
if(!pTestInfo->bLongOn)
{
	char *noLong = "VARCHAR";
	ColAttr[17].pDes[10] = 12;
	ColAttr[17].rDes[1] = noLong;

}
//================Modified for Longvarchar Changes===========================================================
	//print_list(var_list);
	strcpy(tableName,var_mapping("SQLColumnAttribute_tableName_1", var_list));

	strcpy(columnName[0],var_mapping("SQLColumnAttribute_columnName_1", var_list));
	strcpy(columnName[1],var_mapping("SQLColumnAttribute_columnName_2", var_list));
	strcpy(columnName[2],var_mapping("SQLColumnAttribute_columnName_3", var_list));
	strcpy(columnName[3],var_mapping("SQLColumnAttribute_columnName_4", var_list));
	strcpy(columnName[4],var_mapping("SQLColumnAttribute_columnName_5", var_list));
	strcpy(columnName[5],var_mapping("SQLColumnAttribute_columnName_6", var_list));
	strcpy(columnName[6],var_mapping("SQLColumnAttribute_columnName_7", var_list));
	strcpy(columnName[7],var_mapping("SQLColumnAttribute_columnName_8", var_list));
	strcpy(columnName[8],var_mapping("SQLColumnAttribute_columnName_9", var_list));
	strcpy(columnName[9],var_mapping("SQLColumnAttribute_columnName_10", var_list));
	strcpy(columnName[10],var_mapping("SQLColumnAttribute_columnName_11", var_list));
	strcpy(columnName[11],var_mapping("SQLColumnAttribute_columnName_12", var_list));
	strcpy(columnName[12],var_mapping("SQLColumnAttribute_columnName_13", var_list));
	strcpy(columnName[13],var_mapping("SQLColumnAttribute_columnName_14", var_list));
	strcpy(columnName[14],var_mapping("SQLColumnAttribute_columnName_15", var_list));
	strcpy(columnName[15],var_mapping("SQLColumnAttribute_columnName_16", var_list));
	strcpy(columnName[16],var_mapping("SQLColumnAttribute_columnName_17", var_list));
	strcpy(columnName[17],var_mapping("SQLColumnAttribute_columnName_18", var_list));
	strcpy(columnName[18],var_mapping("SQLColumnAttribute_columnName_19", var_list));
	strcpy(columnName[19],var_mapping("SQLColumnAttribute_columnName_20", var_list));
	strcpy(columnName[20],var_mapping("SQLColumnAttribute_columnName_21", var_list));
	strcpy(columnName[21],var_mapping("SQLColumnAttribute_columnName_22", var_list));
	strcpy(columnName[22],var_mapping("SQLColumnAttribute_columnName_23", var_list));
	strcpy(columnName[23],var_mapping("SQLColumnAttribute_columnName_24", var_list));
	strcpy(columnName[24],var_mapping("SQLColumnAttribute_columnName_25", var_list));
	strcpy(columnName[25],var_mapping("SQLColumnAttribute_columnName_26", var_list));

	ExecDirStr[0] = var_mapping("SQLColumnAttribute_ExecDirStr_1", var_list);
	ExecDirStr[1] = var_mapping("SQLColumnAttribute_ExecDirStr_2", var_list);
	ExecDirStr[2] = var_mapping("SQLColumnAttribute_ExecDirStr_3", var_list);
	ExecDirStr[3] = var_mapping("SQLColumnAttribute_ExecDirStr_4", var_list);
//===========================================================================================================
	
	if(isUCS2) {
		LogMsg(NONE,"Setup for UCS2 mode testing: ColPrec has to be doubled\n");

		numcol = sizeof(ColAttr)/sizeof(ColAttr[0]);
		for(icol=0; icol<numcol; icol++) {
			if((stricmp(ColAttr[icol].rDes[1],"CHAR") == 0) ||
				(stricmp(ColAttr[icol].rDes[1],"VARCHAR") == 0) ||
				(stricmp(ColAttr[icol].rDes[1],"LONG VARCHAR") == 0)) {
					for(iatt=0; iatt<totalatt; iatt++) {
						if((DescType[iatt]==SQL_COLUMN_DISPLAY_SIZE) ||
							(DescType[iatt]==SQL_COLUMN_LENGTH) ||
							(DescType[iatt]==SQL_COLUMN_PRECISION))
							ColAttr[icol].pDes[iatt] *= 2;
					}
			}
		}
		icol = 0;
		iatt = 0;
		numcol = 0;
	}

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing 2.0 API => MX Specific SQLColumnAttributes | SQLColumnAttribute | mxcolatt.c\n");

    TEST_INIT;
	TESTCASE_BEGIN("Setup for SQLColAttributes tests\n");

	if(!FullConnect(pTestInfo))
	{
		LogMsg(NONE,"Unable to connect\n");
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

	SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[1],SQL_NTS); /* create table */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[2],SQL_NTS); /* insert into table */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
		LogAllErrors(henv,hdbc,hstmt);
		SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
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
				TESTCASE_BEGIN("SQLColAttributes tests after SQLPrepare\n");
				returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[3], SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
					TEST_FAILED;
					TEST_RETURN;
				}
				break;
			}
			case 1:
			{
				TESTCASE_BEGIN("SQLColAttributes tests after SQLPrepare & SQLExecute\n");
				returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[3], SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
					TEST_FAILED;
					TEST_RETURN;
				}
				returncode = SQLExecute(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
					TEST_FAILED;
					TEST_RETURN;
				}
				break;
			}
			case 2:
			{
				TESTCASE_BEGIN("SQLColAttributes tests after SQLExecDirect\n");
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[3], SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
					TEST_FAILED;
					TEST_RETURN;
				}
				break;
			}
			default: ;
		}
		returncode=SQLNumResultCols(hstmt, &numcol);	// remove this since colatt don't work after prepare. 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultsCols")){
			LogAllErrors(henv,hdbc,hstmt);
			SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
			TEST_FAILED;
			TEST_RETURN;
			}
		if(numcol<1){
			LogMsg(LINEAFTER,"SQLNumResultCols says %d columns are in the result set\n"
							"This is incorrect.  Expecting at least 1 or more columns\n",numcol);
			SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[0],SQL_NTS); /* cleanup */
			TEST_FAILED;
			TEST_RETURN;
			}	 // till here remove 

		TESTCASE_END;

		for (icol = 1; icol <= numcol; icol++){
			for (iatt = 0; iatt < totalatt; iatt++){
		 		strcpy(rgbDesc,"");
				pcbDesc = 0;
				pfDesc = 0;

				sprintf(Heading,"SQLColAttributes: Positive test for column %d\n",icol);
				TESTCASE_BEGIN(Heading);
#ifdef _LP64      
                pfDesc_8bytes = 0;          				
                pfDesc_4bytes = 0;
                if(DescType[iatt] == SQL_COLUMN_DISPLAY_SIZE ||
				   DescType[iatt] == SQL_COLUMN_LENGTH ||
				   DescType[iatt] == SQL_COLUMN_COUNT)
 				   returncode = SQLColAttributes(hstmt,icol,DescType[iatt],rgbDesc,RGB_MAX_LEN,&pcbDesc,&pfDesc_8bytes);
				else
 				   returncode = SQLColAttributes(hstmt,icol,DescType[iatt],rgbDesc,RGB_MAX_LEN,&pcbDesc,(SQLLEN*)&pfDesc_4bytes);
				if(pfDesc_4bytes != 0)
				   pfDesc_8bytes = pfDesc_4bytes ;
#else				
				returncode = SQLColAttributes(hstmt,icol,DescType[iatt],rgbDesc,RGB_MAX_LEN,&pcbDesc,&pfDesc);
#endif
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLColAttributes")){
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				if (iatt < PF_COLUMNS){
#ifdef _LP64
                    if ((_stricmp(rgbDesc,"") == 0) && (pcbDesc == 0) && (ColAttr[icol-1].pDes[iatt] == pfDesc_8bytes)) 
#else
					if ((_stricmp(rgbDesc,"") == 0) && (pcbDesc == 0) && (ColAttr[icol-1].pDes[iatt] == pfDesc)) 
#endif
					{
						/*LogMsg(NONE,"Column C%d & ColAtt %s\n",icol,SQLDescToChar(DescType[iatt],TempStr));
						LogMsg(NONE,"rgbDesc Expected: '%s'\tActual: '%s'\n","",rgbDesc);
						LogMsg(NONE,"pcbDesc Expected: %d\tActual: %d\n",0,pcbDesc);
                        LogMsg(NONE,"pfDesc Expected: %d\tActual: %d\n",ColAttr[icol-1].pDes[iatt],pfDesc);*/
					}
					else{
						if (strcmp(rgbDesc, "TRAFODION") != 0){
							LogMsg(NONE,"%d\n", iatt);
							TEST_FAILED;	
							LogMsg(ERRMSG,"Column C%d & ColAtt %s, Line = %d\n",icol,SQLDescToChar(DescType[iatt],TempStr),__LINE__);
							LogMsg(ERRMSG,"rgbDesc Expected: '%s'\tActual: '%s', Line = %d\n","",rgbDesc,__LINE__);
							LogMsg(ERRMSG,"pcbDesc Expected: %d\tActual: %d, Line = %d\n",0,pcbDesc,__LINE__);
							LogMsg(ERRMSG,"pfDesc Expected: %d\tActual: %d, Line = %d\n",ColAttr[icol-1].pDes[iatt],pfDesc,__LINE__);
							}
						}
					}
				else{
					if ((cstrcmp(ColAttr[icol-1].rDes[iatt-PF_COLUMNS],rgbDesc,TRUE,isCharSet) == 0) && (pcbDesc == (SWORD)strlen(rgbDesc)) && (pfDesc == 0)) 
					{
						/*
						LogMsg(NONE,"Column C%d & ColAtt %s\n",icol,SQLDescToChar(DescType[iatt],TempStr));
						LogMsg(NONE,"rgbDesc Expected: '%s'\tActual: '%s'\n",ColAttr[icol-1].rDes[iatt-PF_COLUMNS],rgbDesc);
						LogMsg(NONE,"pcbDesc Expected: %d\tActual: %d\n",strlen(rgbDesc),pcbDesc);
						LogMsg(NONE,"pfDesc Expected: %d\tActual: %d\n",0,pfDesc);
						*/
					}	
					else{
						if (strcmp(rgbDesc, "TRAFODION") != 0){
							TEST_FAILED;	
							LogMsg(ERRMSG,"Column C%d & ColAtt %s, Line = %d\n",icol,SQLDescToChar(DescType[iatt],TempStr),__LINE__);
							LogMsg(ERRMSG,"rgbDesc Expected: '%s'\tActual: '%s', Line = %d\n",ColAttr[icol-1].rDes[iatt-PF_COLUMNS],rgbDesc,__LINE__);
							LogMsg(ERRMSG,"pcbDesc Expected: %d\tActual: %d, Line = %d\n",strlen(rgbDesc),pcbDesc,__LINE__);
							LogMsg(ERRMSG,"pfDesc Expected: %d\tActual: %d, Line = %d\n",0,pfDesc,__LINE__);
							}
						}
					}
					
				TESTCASE_END;
				} /* end iatt loop */
			} /* end icol loop */

		SQLFreeStmt(hstmt,SQL_CLOSE);
	}
	SQLExecDirect(hstmt,(SQLCHAR*) ExecDirStr[0],SQL_NTS); /* cleanup */

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => MX Specific SQLColumnAttributes.\n");

	free_list(var_list);

	TEST_RETURN;
}
