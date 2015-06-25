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
#include <time.h>

#define	MAX_PARAMS		4

/*
------------------------------------------------------------------
   TestSQLSetConnectAttr: Tests SQLSetEnvAttr                  
------------------------------------------------------------------
*/
PassFail TestMXSQLSetEnvAttr(TestInfo *pTestInfo)
{   
	TEST_DECLARE;
	char		Heading[MAX_STRING_SIZE];
 	RETCODE		returncode;
 	SQLHANDLE 	henv;
 	SQLHANDLE 	hdbc;
 	SQLHANDLE	hstmt, hstmt1;
	int			i, j;
	int			k =0;
	SQLINTEGER	*StringLengthPtr = NULL;
	SQLUINTEGER	pvParamInt;
	char				TempBuf1[MAX_STRING_SIZE];
	char				TempBuf2[MAX_STRING_SIZE];
	  
	struct {
		SQLINTEGER	Attribute;
		SQLUINTEGER	vParamInt[MAX_PARAMS+1];
	} OptionInt[] = {			 
//  environment attributes
		{SQL_ATTR_CONNECTION_POOLING,SQL_CP_ONE_PER_DRIVER,SQL_CP_ONE_PER_HENV,SQL_CP_OFF,999,},
		{SQL_ATTR_CP_MATCH,SQL_CP_STRICT_MATCH,SQL_CP_RELAXED_MATCH,999,},
		{SQL_ATTR_ODBC_VERSION,SQL_OV_ODBC2,SQL_OV_ODBC3,999,},
		{SQL_ATTR_OUTPUT_NTS,SQL_TRUE,SQL_FALSE,999,},
		{999,}};

	char		buf[MAX_STRING_SIZE];
	char		State[STATE_SIZE];
	SDWORD	NativeError;
	BOOL MsgDisplayed;
	clock_t start, finish;
	double  duration,duration1;


	MsgDisplayed=FALSE;


	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API =>SQLSetEnvAttr/GetEnvAttr | SQLGetEnvAttr | setenv.c\n");

	TEST_INIT;

//==========================================================================================================


	TESTCASE_BEGIN("Setup for SQLSet/GetEnvAttributes tests\n");

/*RS: Call disabled temporarily since the driver is already disconnected and causes an access violation with MDAC 2.8
	returncode = SQLDisconnect((SQLHANDLE)pTestInfo->hdbc);
*/
	returncode = FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3);
	if (pTestInfo->hdbc == (SQLHANDLE)NULL)
	{
		LogMsg(ERRMSG,"Unable to connect\n");
		TEST_FAILED;
		TEST_RETURN;
	}
	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
	hstmt1 = (SQLHANDLE)pTestInfo->hstmt;
	TESTCASE_END; // end of setup

//==========================================================================================================
	for (i = 0; OptionInt[i].Attribute != 999; i++) 
	{
		for (j = 0; OptionInt[i].vParamInt[j] != 999; j++)					
		{ 

			sprintf(Heading,"Test Positive functionality of SQLSetEnvAttr "
									"for %s and ParamValue: %s\n",
									ConnectionOptionToChar(OptionInt[i].Attribute,TempBuf1),
									ConnectionParamToChar(OptionInt[i].Attribute,OptionInt[i].vParamInt[j],TempBuf2));
			TESTCASE_BEGIN(Heading);
			 
			returncode = SQLAllocHandle(SQL_HANDLE_ENV,(SQLHANDLE)NULL,(SQLHANDLE *)&henv);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle - Env"))
			{ 
				TEST_FAILED;
				TEST_RETURN;
			} 
			// set the ODBC behavior version.
			if (!SQL_SUCCEEDED(SQLSetEnvAttr((SQLHANDLE)henv, SQL_ATTR_ODBC_VERSION,
			   (SQLPOINTER) SQL_OV_ODBC3, SQL_IS_INTEGER)))
			     LogMsg(SHORTTIMESTAMP+LINEAFTER,"SQLSetEnvAttr/SQL_ATTR_ODBC_VERSION error\n");
			  
			returncode = SQLSetEnvAttr((SQLHANDLE)henv,OptionInt[i].Attribute,(void *)OptionInt[i].vParamInt[j],0);
			if(  (OptionInt[i].Attribute == SQL_ATTR_OUTPUT_NTS) && (OptionInt[i].vParamInt[j] == SQL_FALSE) )
            { 
                if(!CHECKRC(SQL_ERROR,returncode,"SQLSetEnvAttr")) {
			  	    TEST_FAILED;
                    LogAllErrorsVer3(henv,hdbc,hstmt);
                }
				TEST_RETURN;  // This is the last attribute 
            }
/* new: this is what is in the UNIX UNICODE version */
                       #ifdef unixcli  // The following 2 attributes are not supported in Unix 
                       else if((OptionInt[i].Attribute == SQL_ATTR_CONNECTION_POOLING) || (OptionInt[i].Attribute == SQL_ATTR_CP_MATCH))
                       {
                               if(!CHECKRC(SQL_ERROR,returncode,"SQLSetEnvAttr"))  {
                                       TEST_FAILED;
                   LogAllErrorsVer3(henv,hdbc,hstmt);
               }
                               TESTCASE_END;
                               continue;             // skip the rest of the whilie-loop
                       }
                       #endif
/* end of new */
			else
            {
                if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetEnvAttr")) {
				  	TEST_FAILED;
                    LogAllErrorsVer3(henv,hdbc,hstmt);
                }
			} 

			returncode = SQLGetEnvAttr((SQLHANDLE)henv,OptionInt[i].Attribute,&pvParamInt,0,StringLengthPtr);
		    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetEnvAttr"))
			{ 
			   TEST_FAILED;
               LogAllErrorsVer3(henv,hdbc,hstmt);
  			   TEST_RETURN;
			}  
			else
			{ 
				if (OptionInt[i].vParamInt[j] == pvParamInt) 
				{ 
						LogMsg(NONE,"expect: %d and actual: %d are matched\n",OptionInt[i].vParamInt[j],pvParamInt);
						switch(OptionInt[i].Attribute) 
						{ 
							case SQL_ATTR_CONNECTION_POOLING :
								switch(OptionInt[i].vParamInt[j]) 
								{ 
									case SQL_CP_OFF :
			
										break;
									case SQL_CP_ONE_PER_DRIVER :

										break;
									case SQL_CP_ONE_PER_HENV :
											returncode = SQLSetEnvAttr((SQLHANDLE)henv, SQL_ATTR_CP_MATCH,
																		(SQLPOINTER) SQL_CP_RELAXED_MATCH, SQL_IS_INTEGER);
											if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetEnvAttr"))
											{ 
												TEST_FAILED;
                                                LogAllErrorsVer3(henv,hdbc,hstmt);
												TEST_RETURN;
											} 
											while (k < 10) 
											{  
												returncode = SQLAllocHandle(SQL_HANDLE_DBC,(SQLHANDLE)henv,(SQLHANDLE *)&hdbc);
												if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle -DBC"))
												{ 
													TEST_FAILED;
                                                    LogAllErrorsVer3(henv,hdbc,hstmt);
													TEST_RETURN;
												} 
	
												start = clock();
												returncode = SQLConnect((SQLHANDLE)hdbc,
															(SQLCHAR*)pTestInfo->DataSource, SQL_NTS,
															(SQLCHAR*)pTestInfo->UserID, SQL_NTS,
															(SQLCHAR*)pTestInfo->Password, SQL_NTS);
 												if ( returncode != SQL_SUCCESS && returncode != SQL_SUCCESS_WITH_INFO)
												{ 
													LogAllErrorsVer3(henv,hdbc,hstmt);
													TEST_FAILED;
												} 
												else
												{ 
													LogMsg(SHORTTIMESTAMP+LINEAFTER,"Connected successfully %d time \n",k);
													finish = clock();
													duration = (double)(finish - start) / CLOCKS_PER_SEC;
                                                    if ( k == 0)
													duration1 = duration;
													else
                                                    {  
													 if(duration >= duration1)
                                                     {
														TEST_FAILED;
													    LogMsg(SHORTTIMESTAMP+LINEAFTER,"first connect took %2.1f seconds unexpected  less than second connect %2.1f seconds\n", duration1,duration);
                                                     }
                                                    }    
													returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
													if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle - STMT"))
													{ 
													    LogAllErrorsVer3(henv,hdbc,hstmt);
													    TEST_FAILED;
													}  
													SQLExecDirect(hstmt,(SQLCHAR*)(SQLCHAR *)"CREATE TABLE TESTB(PARTID integer,DESCRIPTION char(50),PRICE real) NO PARTITION", SQL_NTS);
													SQLExecDirect(hstmt,(SQLCHAR*)(SQLCHAR *)"DROP TABLE TESTB", SQL_NTS);
													SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
												} 
												SQLDisconnect((SQLHANDLE)hdbc);
												if (!SQL_SUCCEEDED(SQLFreeHandle(SQL_HANDLE_DBC, (SQLHANDLE)hdbc)))
												LogMsg(SHORTTIMESTAMP+LINEAFTER,"Could not free handle hdbc");
												k++;
											}
											SQLFreeHandle(SQL_HANDLE_ENV, (SQLHANDLE)henv);
						         			break;
                                } 
								break;
							case SQL_ATTR_CP_MATCH :
								switch(OptionInt[i].vParamInt[j]) 
								{ 
									case SQL_CP_STRICT_MATCH :
										break;
									case SQL_CP_RELAXED_MATCH :
										break;
								}
								break;
							case SQL_ATTR_ODBC_VERSION :
								returncode = SQLAllocHandle(SQL_HANDLE_DBC,(SQLHANDLE)henv,(SQLHANDLE *)&hdbc);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle -DBC"))
								{ 
									TEST_FAILED;
									TEST_RETURN;
								} 
	
								SQLConnect((SQLHANDLE)hdbc,
											(SQLCHAR*)pTestInfo->DataSource, SQL_NTS,
											(SQLCHAR*)pTestInfo->UserID, SQL_NTS,
											(SQLCHAR*)pTestInfo->Password, SQL_NTS);
								if ( returncode != SQL_SUCCESS && returncode != SQL_SUCCESS_WITH_INFO)
								{ 
									LogAllErrorsVer3(henv,hdbc,hstmt);
									TEST_FAILED;
								} 
								else
								{ 
									LogMsg(SHORTTIMESTAMP+LINEAFTER,"Connected successfully \n");
									returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
									if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle - STMT"))
									{ 
										LogAllErrorsVer3(henv,hdbc,hstmt);
										TEST_FAILED;
									}  
									SQLExecute(hstmt);
									   /* Log any hstmt error messages */
									returncode = SQLError((SQLHANDLE)NULL, 0, hstmt, (SQLCHAR*)State, &NativeError, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
								} 
								switch(OptionInt[i].vParamInt[j]) 
								{ 
									case SQL_OV_ODBC3 :
										if ( strcmp(State,"HY010") )
                                        TEST_FAILED; 
										break;
									case SQL_OV_ODBC2 :
										if ( strcmp(State,"S1010") )
                                        TEST_FAILED;
										break;
								}
								SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
								SQLDisconnect((SQLHANDLE)hdbc);
								if (!SQL_SUCCEEDED(SQLFreeHandle(SQL_HANDLE_DBC, (SQLHANDLE)hdbc)))
								LogMsg(SHORTTIMESTAMP+LINEAFTER,"Could not free handle hdbc");
								SQLFreeHandle(SQL_HANDLE_ENV, (SQLHANDLE)henv);
								break;
							case SQL_ATTR_OUTPUT_NTS :
								switch(OptionInt[i].vParamInt[j]) 
								{
									case SQL_TRUE :
									
										break;
									case SQL_FALSE :
										
										break;
								}
								break;						
						}  // end main switch
						TESTCASE_END;
				}//end if check of get set match  	 
				else
				{ 
					TEST_FAILED;
					LogMsg(ERRMSG,"expect: %d and actual: %d are not matched\n",OptionInt[i].vParamInt[j],pvParamInt);
				} 
			}//else stmt of ifelse getenvattr pass/fail ends
		}//for j loop
	}//for i loop

	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLSetEnvAttr/GetEnvAttr.\n");
	TEST_RETURN;
}
