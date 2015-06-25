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
#include <windows.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define COLNAME_LEN	300
/*
---------------------------------------------------------
   TestSQLDescribeColVer3 for MP Specific
---------------------------------------------------------
*/
PassFail TestMXSQLDescribeColVer3(TestInfo *pTestInfo)
{
	TEST_DECLARE;
 	char			Heading[MAX_STRING_SIZE];
	RETCODE			returncode;
	SQLHANDLE 		henv, hdbc, hstmt;
	UWORD			icol;
	SWORD			numcol, st, cs, cnull, cl, colsize = 2;
	SQLULEN         cp; 
	CHAR			cn[COLNAME_LEN];
	CHAR			*colname[21];
	CHAR			*ExecDirStr[12];

#ifndef _WM
	SWORD			SQLType[] = {SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,
									SQL_REAL,SQL_DOUBLE,SQL_DOUBLE,SQL_TYPE_DATE,SQL_TYPE_TIME,SQL_TYPE_TIMESTAMP,SQL_LONGVARCHAR,SQL_BIGINT,
									SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC};
	SQLULEN			ColPrec[] = {254,254,18,18,5,10,7,15,15,10,8,26,2000,19,19,19,128,128,10,18,30};
#else
	SWORD			SQLType[] = {SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,
									SQL_REAL,SQL_DOUBLE,SQL_DOUBLE,SQL_CHAR,SQL_TYPE_TIME,SQL_TYPE_TIMESTAMP,SQL_LONGVARCHAR,SQL_BIGINT,
									SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC};
	SQLULEN			ColPrec[] = {254,254,18,18,5,10,7,15,15,8,8,26,2000,19,19,19,128,128,10,18,30};
#endif
	SWORD			ColScale[]= {0,  0,  6, 6, 0,0, 0,0, 0, 0, 0,6, 0,   0, 0, 6, 0,  128,5, 5, 10};
	char			TempType1[50],TempType2[50];
	SWORD			ColNullable[] = {SQL_NULLABLE,SQL_NO_NULLS,SQL_NULLABLE};

	CHAR			*TestCase[] = {
					"before preparing stmt ",
					"before preparing & executing stmt ",
					"before preparing, executing & fetching stmt ",
					"before execdirect stmt ",
					"before execdirect & fetching stmt ",
					"before preparing param stmt ",
					"before preparing & binding stmt ",
					"before preparing, binding & executing stmt ",
					"before preparing, binding, executing & fetching stmt "
					};

	int				lend = 9, iend = 3;
	SQLUSMALLINT	i = 0, l = 0;
	SQLLEN			cbIn = SQL_NTS;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLDescribeColumns30", charset_file);
	if (var_list == NULL) return FAILED;
//================Modified for Longvarchar Changes===========================================================
	if(!pTestInfo->bLongOn)
	{
		SWORD iNoLong = SQL_VARCHAR;
		SQLType[12] = iNoLong;
	}
//================Modified for Longvarchar Changes===========================================================
	//print_list(var_list);
	colname[0] = var_mapping("SQLDescribeColumns30_colname_1", var_list);
	colname[1] = var_mapping("SQLDescribeColumns30_colname_2", var_list);
	colname[2] = var_mapping("SQLDescribeColumns30_colname_3", var_list);
	colname[3] = var_mapping("SQLDescribeColumns30_colname_4", var_list);
	colname[4] = var_mapping("SQLDescribeColumns30_colname_5", var_list);
	colname[5] = var_mapping("SQLDescribeColumns30_colname_6", var_list);
	colname[6] = var_mapping("SQLDescribeColumns30_colname_7", var_list);
	colname[7] = var_mapping("SQLDescribeColumns30_colname_8", var_list);
	colname[8] = var_mapping("SQLDescribeColumns30_colname_9", var_list);
	colname[9] = var_mapping("SQLDescribeColumns30_colname_10", var_list);
	colname[10] = var_mapping("SQLDescribeColumns30_colname_11", var_list);
	colname[11] = var_mapping("SQLDescribeColumns30_colname_12", var_list);
	colname[12] = var_mapping("SQLDescribeColumns30_colname_13", var_list);
	colname[13] = var_mapping("SQLDescribeColumns30_colname_14", var_list);
	colname[14] = var_mapping("SQLDescribeColumns30_colname_15", var_list);
	colname[15] = var_mapping("SQLDescribeColumns30_colname_16", var_list);
	colname[16] = var_mapping("SQLDescribeColumns30_colname_17", var_list);
	colname[17] = var_mapping("SQLDescribeColumns30_colname_18", var_list);
	colname[18] = var_mapping("SQLDescribeColumns30_colname_19", var_list);
	colname[19] = var_mapping("SQLDescribeColumns30_colname_20", var_list);
	colname[20] = var_mapping("SQLDescribeColumns30_colname_21", var_list);

	ExecDirStr[0] = var_mapping("SQLDescribeColumns30_ExecDirStr_1", var_list);
	ExecDirStr[1] = var_mapping("SQLDescribeColumns30_ExecDirStr_2", var_list);
	ExecDirStr[2] = var_mapping("SQLDescribeColumns30_ExecDirStr_3", var_list);
	ExecDirStr[3] = var_mapping("SQLDescribeColumns30_ExecDirStr_4", var_list);
	ExecDirStr[4] = var_mapping("SQLDescribeColumns30_ExecDirStr_5", var_list);
	ExecDirStr[5] = var_mapping("SQLDescribeColumns30_ExecDirStr_6", var_list);
	ExecDirStr[6] = var_mapping("SQLDescribeColumns30_ExecDirStr_7", var_list);
	ExecDirStr[7] = var_mapping("SQLDescribeColumns30_ExecDirStr_8", var_list);
	ExecDirStr[8] = var_mapping("SQLDescribeColumns30_ExecDirStr_9", var_list);
	ExecDirStr[9] = var_mapping("SQLDescribeColumns30_ExecDirStr_10", var_list);
	ExecDirStr[10] = var_mapping("SQLDescribeColumns30_ExecDirStr_11", var_list);
	ExecDirStr[11] = var_mapping("SQLDescribeColumns30_ExecDirStr_12", var_list);

//=========================================================================================

	if(isUCS2) {
		LogMsg(NONE,"Setup for UCS2 mode testing: ColPrec has to be doubled\n");

        ExecDirStr[3] = replace_str(ExecDirStr[3],"$$$","127");
        ExecDirStr[4] = replace_str(ExecDirStr[4],"$$$","127");
        ExecDirStr[5] = replace_str(ExecDirStr[5],"$$$","127");

		l = sizeof(SQLType)/sizeof(SQLType[0]);
		while(i < l) {
			if(SQLType[i] == SQL_CHAR) {
				//SQLType[i] = SQL_WCHAR;
				ColPrec[i] *= 2;  //--> This is in character, so no need to double
			}
			else if (SQLType[i] == SQL_VARCHAR) {
				//SQLType[i] = SQL_WVARCHAR;
			}
			else if (SQLType[i] == SQL_LONGVARCHAR)	{
				//SQLType[i] = SQL_WLONGVARCHAR;
				ColPrec[i] *= 2;  //--> This is in character, so no need to double
			}
			else {
			}
			i++;
		}
		i = 0;
		l = 0;
	} else {
        ExecDirStr[3] = replace_str(ExecDirStr[3],"$$$","254");
        ExecDirStr[4] = replace_str(ExecDirStr[4],"$$$","254");
        ExecDirStr[5] = replace_str(ExecDirStr[5],"$$$","254");
    }

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => MX Specific SQLDescribeColumns | SQLDescribeColumns30 | sqldescribecolver3.c\n");
	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLDescribCol tests\n");

	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,"Unable to connect\n");
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
	hdbc = pTestInfo->hdbc;
	hstmt = (SQLHANDLE)pTestInfo->hstmt;
	
	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END;  // end of setup
	for (l = 0; l < lend; l++)
	{
		for (i = 0; i < iend; i++)
		{
			//==================================================================================
			sprintf(Heading,"SQLDescribeCol: Test #%d.%d\n",l,i);
			TESTCASE_BEGIN(Heading);
			if ((i != (iend-1)) && (l < 5))
			{
				rerutncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i],SQL_NTS); /* cleanup */
				 if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
                                        {
                                                LogAllErrorsVer3(henv,hdbc,hstmt);
                                                TEST_FAILED;
                                        }

                                returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i+iend],SQL_NTS); /* create table */
				LogMsg(NONE,"%s\n", ExecDirStr[i+iend]);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				else
				{
					returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend],SQL_NTS); /* insert into table */
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						TEST_FAILED;
					}
					else
					{
						LogMsg(NONE,"SQLDescribeCol: %s\n",TestCase[l]);
						LogMsg(NONE,"     %s\n",ExecDirStr[i+iend+iend+iend]);
						switch( l )
						{
							case 0:
								returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
								{
									LogAllErrorsVer3(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								break;
							case 1 :
								returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
								{
									LogAllErrorsVer3(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								else
								{
									returncode = SQLExecute(hstmt);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
									{
										LogAllErrorsVer3(henv,hdbc,hstmt);
										TEST_FAILED;
									}
								}
								break;
							case 2 :
								returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
								{
									LogAllErrorsVer3(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								else
								{
									returncode = SQLExecute(hstmt);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
									{
										LogAllErrorsVer3(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									else
									{
										returncode = SQLFetch(hstmt);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
									}
								}
								break;
							case 3 :
								returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
								{
									LogAllErrorsVer3(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								break;
							case 4 :
								returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
								{
									LogAllErrorsVer3(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								else
								{
									returncode = SQLFetch(hstmt);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
									{
										LogAllErrorsVer3(henv,hdbc,hstmt);
										TEST_FAILED;
									}
								}
								break;
						}
						if (returncode == SQL_SUCCESS)
						{
							returncode=SQLNumResultCols(hstmt, &numcol);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultCols"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
							}
							for (icol = 1; icol <= numcol; icol++)
							{
								LogMsg(LINEBEFORE,"SQLDescribeCol: checking Column #%d\n",icol);
								returncode = SQLDescribeCol(hstmt,icol,(SQLCHAR*)cn,COLNAME_LEN,&cl,&st,&cp,&cs,&cnull);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDescribeCol"))
								{
									TEST_FAILED;
									LogAllErrorsVer3(henv,hdbc,hstmt);
								}
								colsize=strlen(colname[icol-1]);
								if(isCharSet == TRUE)
									colsize -= 2;
								if ((cstrcmp(cn,colname[icol-1],FALSE,isCharSet) == 0) 
									 && (cl == colsize) 
									 && (st == SQLType[icol-1]) 
									 && (cp == ColPrec[icol-1]) 
									 && (cs == ColScale[icol-1]) 
									 && (cnull == ColNullable[i]))
								{
									//LogMsg(NONE,"colname expect: %s and actual: %s are matched\n",colname[icol-1],cn);
									//LogMsg(NONE,"ColNameLen expect: %d and actual: %d are matched\n",colsize,cl);
									//LogMsg(NONE,"SQLType expect: %s and actual: %s are matched\n",
									//SQLTypeToChar(SQLType[icol-1],TempType1),SQLTypeToChar(st,TempType2));
									//LogMsg(NONE,"ColPrec expect: %d and actual: %d are matched\n",ColPrec[icol-1],cp);
									//LogMsg(NONE,"ColScale expect: %d and actual: %d are matched\n",ColScale[icol-1],cs);
									//LogMsg(NONE,"ColNullable expect: %s and actual: %s are matched\n\n",
									//SQLNullToChar(ColNullable[i],TempType1),SQLNullToChar(cnull,TempType2));
								}
								else
								{
									TEST_FAILED;	
									if (cstrcmp(cn,colname[icol-1],FALSE,isCharSet) != 0)
										LogMsg(ERRMSG,"colname expect: %s and actual: %s are not matched\n",colname[icol-1],cn);
									if (cl != colsize)
										LogMsg(ERRMSG,"ColNameLen expect: %d and actual: %d are not matched\n",colsize,cl);
									if (st != SQLType[icol-1])
										LogMsg(ERRMSG,"SQLType expect: %s and actual: %s are not matched\n",
											SQLTypeToChar(SQLType[icol-1],TempType1),SQLTypeToChar(st,TempType2));
									if (cp != ColPrec[icol-1])
										LogMsg(ERRMSG,"ColPrec expect: %d and actual: %d are not matched\n",ColPrec[icol-1],cp);
									if (cs != ColScale[icol-1])
										LogMsg(ERRMSG,"ColScale expect: %d and actual: %d are not matched\n",ColScale[icol-1],cs);
									if (cnull != ColNullable[i])
										LogMsg(ERRMSG,"ColNullable expect: %s and actual: %s are not matched\n\n",
											SQLNullToChar(ColNullable[i],TempType1),SQLNullToChar(cnull,TempType2));
								}
							} /* end icol loop */
						}
						else
						{
							TEST_FAILED;
							LogAllErrorsVer3(henv,hdbc,hstmt);
						}
						SQLFreeStmt(hstmt,SQL_CLOSE);
						SQLExecDirect(hstmt,(SQLCHAR*) ExecDirStr[i],SQL_NTS); /* cleanup */
					}
				}
			}
			else if ((i == (iend-1)) && (l >= 5))
			{
				SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i],SQL_NTS); /* cleanup */ 
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i+iend],SQL_NTS); /* create table */
				LogMsg(NONE,"%s\n", ExecDirStr[i+iend]);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				else
				{
					returncode = SQLExecDirect(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend],SQL_NTS); /* insert into table */
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						TEST_FAILED;
					}
					else
					{
						LogMsg(NONE,"SQLDescribeCol: %s\n",TestCase[l]);
						LogMsg(NONE,"     %s\n",ExecDirStr[i+iend+iend+iend]);
						switch( l ) 
						{
							case 5 :
								returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
								{
									LogAllErrorsVer3(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								break;
							case 6 :
								returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
								{
									LogAllErrorsVer3(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								else
								{
									returncode = SQLBindParameter(hstmt,1,SQL_PARAM_INPUT,SQL_C_CHAR,SQL_CHAR,2000,0,(SQLPOINTER) "0123456789",300,&cbIn);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
									{
										LogAllErrorsVer3(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									returncode = SQLBindParameter(hstmt,2,SQL_PARAM_INPUT,SQL_C_CHAR,SQL_CHAR,2000,0,(SQLPOINTER)"0123456789",300,&cbIn);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
									{
										LogAllErrorsVer3(henv,hdbc,hstmt);
										TEST_FAILED;
									}
								}
								break;
							case 7 :
								returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
								{
									LogAllErrorsVer3(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								else
								{
									returncode = SQLBindParameter(hstmt,1,SQL_PARAM_INPUT,SQL_C_CHAR,SQL_CHAR,2000,0,(SQLPOINTER)"0123456789",300,&cbIn);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
									{
										LogAllErrorsVer3(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									returncode = SQLBindParameter(hstmt,2,SQL_PARAM_INPUT,SQL_C_CHAR,SQL_CHAR,2000,0,(SQLPOINTER)"0123456789",300,&cbIn);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
									{
										LogAllErrorsVer3(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									returncode = SQLExecute(hstmt);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
									{
										LogAllErrorsVer3(henv,hdbc,hstmt);
										TEST_FAILED;
									}
								}
								break;
							  case 8 :
								returncode = SQLPrepare(hstmt,(SQLCHAR*)ExecDirStr[i+iend+iend+iend], SQL_NTS);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
								{
									LogAllErrorsVer3(henv,hdbc,hstmt);
									TEST_FAILED;
								}
								else
								{
									returncode = SQLBindParameter(hstmt,1,SQL_PARAM_INPUT,SQL_C_CHAR,SQL_CHAR,2000,0,(SQLPOINTER)"0123456789",300,&cbIn);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
									{
										LogAllErrorsVer3(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									returncode = SQLBindParameter(hstmt,2,SQL_PARAM_INPUT,SQL_C_CHAR,SQL_CHAR,2000,0,(SQLPOINTER)"0123456789",300,&cbIn);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
									{
										LogAllErrorsVer3(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									returncode = SQLExecute(hstmt);
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
									{
										LogAllErrorsVer3(henv,hdbc,hstmt);
										TEST_FAILED;
									}
									else
									{
										returncode = SQLFetch(hstmt);
										if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
										{
											LogAllErrorsVer3(henv,hdbc,hstmt);
											TEST_FAILED;
										}
									}
								}
								break;
						}
						if (returncode == SQL_SUCCESS)
						{
							SQLNumResultCols(hstmt, &numcol);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumResultCols"))
							{
								LogAllErrorsVer3(henv,hdbc,hstmt);
								TEST_FAILED;
							}
							for (icol = 1; icol <= numcol; icol++)
							{
								LogMsg(LINEBEFORE,"SQLDescribeCol: checking Column #%d\n",icol);
								returncode = SQLDescribeCol(hstmt,icol,(SQLCHAR*)cn,COLNAME_LEN,&cl,&st,&cp,&cs,&cnull);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDescribeCol"))
								{
									TEST_FAILED;
									LogAllErrorsVer3(henv,hdbc,hstmt);
								}
								colsize=strlen(colname[icol-1]);
								if(isCharSet == TRUE)
									colsize -= 2;
								if ((cstrcmp(cn,colname[icol-1],FALSE,isCharSet) == 0) 
									 && (cl == colsize) 
									 && (st == SQLType[icol-1]) 
									 && (cp == ColPrec[icol-1]) 
									 && (cs == ColScale[icol-1]) 
									 && (cnull == ColNullable[i]))
								{
									//LogMsg(NONE,"colname expect: %s and actual: %s are matched\n",colname[icol-1],cn);
									//LogMsg(NONE,"ColNameLen expect: %d and actual: %d are matched\n",colsize,cl);
									//LogMsg(NONE,"SQLType expect: %s and actual: %s are matched\n",
									//	SQLTypeToChar(SQLType[icol-1],TempType1),SQLTypeToChar(st,TempType2));
									//LogMsg(NONE,"ColPrec expect: %d and actual: %d are matched\n",ColPrec[icol-1],cp);
									//LogMsg(NONE,"ColScale expect: %d and actual: %d are matched\n",ColScale[icol-1],cs);
									//LogMsg(NONE,"ColNullable expect: %s and actual: %s are matched\n\n",
									//	SQLNullToChar(ColNullable[i],TempType1),SQLNullToChar(cnull,TempType2));
								}
								else
								{
									TEST_FAILED;	
									if (cstrcmp(cn,colname[icol-1],FALSE,isCharSet) != 0)
										LogMsg(ERRMSG,"colname expect: %s and actual: %s are not matched\n",colname[icol-1],cn);
									if (cl != colsize)
										LogMsg(ERRMSG,"ColNameLen expect: %d and actual: %d are not matched\n",colsize,cl);
									if (st != SQLType[icol-1])
										LogMsg(ERRMSG,"SQLType expect: %s and actual: %s are not matched\n",
											SQLTypeToChar(SQLType[icol-1],TempType1),SQLTypeToChar(st,TempType2));
									if (cp != ColPrec[icol-1])
										LogMsg(ERRMSG,"ColPrec expect: %d and actual: %d are not matched\n",ColPrec[icol-1],cp);
									if (cs != ColScale[icol-1])
										LogMsg(ERRMSG,"ColScale expect: %d and actual: %d are not matched\n",ColScale[icol-1],cs);
									if (cnull != ColNullable[i])
										LogMsg(ERRMSG,"ColNullable expect: %s and actual: %s are not matched\n\n",
											SQLNullToChar(ColNullable[i],TempType1),SQLNullToChar(cnull,TempType2));
								}
							}
						}
					}
					SQLFreeStmt(hstmt,SQL_CLOSE);
					SQLExecDirect(hstmt,(SQLCHAR*) ExecDirStr[i],SQL_NTS); 
				}
			}
			TESTCASE_END;
		} /* iend loop */
	} /* lend loop */
	SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => MX Specific SQLDescribeColumns.\n");
	free_list(var_list);
	TEST_RETURN;
}
