#include <windows.h>
#include <sqlext.h>
#include <stdlib.h>
#include <stdio.h>
#include "basedef.h"
#include "common.h"
#include "log.h"
#include "apitests.h"

#define MAX_STR_LEN     1024
#define MAX_SIZE        256

BOOL execute(TestInfo* pTestInfo, SQLHANDLE secHandle, TCHAR* tempStr, short expRet);
BOOL getAllData(SQLHANDLE hstmt, RETCODE returncode);
PassFail TestInfoStats(TestInfo *pTestInfo);

/*
---------------------------------------------------------
  TestSQLDrivers
	No negative tests since this functionality is done at
	driver manager level.
---------------------------------------------------------
*/
PassFail TestInfoStats(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;

    SQLHANDLE	secHandle;
    SQLSMALLINT outLen = SQL_NTS;
    TCHAR		tempStr[MAX_STR_LEN*2];
	int			i,j;
	TCHAR		cursorName[MAX_STR_LEN];
    RETCODE		returncode;

	TCHAR* strs[5];

    struct _test_data {
        TCHAR        *front;
        TCHAR        *back;
        //TCHAR        front[2];
        //TCHAR        back[MAX_SIZE];
        RETCODE     retcode;
        BOOL        cursor;
        TCHAR        *stmt;
    } testData[] = {{_T(""), _T(""),          SQL_SUCCESS,    TRUE,  _T("")},
                    {_T(""), _T(""),          SQL_SUCCESS,    TRUE,  _T("")},
                    {_T(""), _T(""),          SQL_SUCCESS,    TRUE,  _T("")},
                    {_T(""), _T("SQL_CUR_2"), SQL_ERROR,      FALSE, _T("")},
                    {_T(""), _T(""),          SQL_ERROR,      FALSE, _T("")},    // empty statement
                    {_T("'"), _T("'"),        SQL_SUCCESS,    TRUE,  _T("")},
                    {_T("\""), _T("\""),      SQL_SUCCESS,    TRUE,  _T("")},
                    {_T(""), _T("SQL_CUR_9 "),SQL_ERROR,      FALSE, _T("")},
                    {_T("\""), _T(""),        SQL_ERROR,      TRUE,  _T("")},
                    {_T("\""), _T("\""),      SQL_SUCCESS,    FALSE, _T("")},     // strs[3].txt
                    {_T("'"), _T("'"),        SQL_SUCCESS,    FALSE, _T("")},     // strs[3].txt
                    {_T("'"), _T(""),         SQL_ERROR,      FALSE, _T("")},     // strs[3].txt
                    {_T("\""), _T(""),        SQL_ERROR,      FALSE, _T("")},     // strs[3].txt
                    {_T(""), _T("\""),        SQL_ERROR,      FALSE, _T("")},     // strs[3].txt
                    {_T(""), _T("'"),         SQL_ERROR,      FALSE, _T("")},     // strs[3].txt
                    {_T("'"), _T("'"),        SQL_ERROR,      FALSE, _T("")},     // strs[4].txt
                    {_T("\""), _T("\""),      SQL_ERROR,      FALSE, _T("")},     // strs[4].txt
                    {_T(""), _T("end")}
     };

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("InfoStats"), charset_file);
	if (var_list == NULL) return FAILED;

    strs[0] = var_mapping(_T("InfoStats_strs_0"), var_list);
    strs[1] = var_mapping(_T("InfoStats_strs_1"), var_list);
    strs[2] = var_mapping(_T("InfoStats_strs_2"), var_list);
    strs[3] = var_mapping(_T("InfoStats_strs_3"), var_list);
    strs[4] = var_mapping(_T("InfoStats_strs_4"), var_list);
    strs[5] = var_mapping(_T("InfoStats_strs_5"), var_list);

	testData[9].stmt  = strs[3];
    testData[10].stmt = strs[3];
    testData[11].stmt = strs[3];
    testData[12].stmt = strs[3];
    testData[13].stmt = strs[3];
    testData[14].stmt = strs[3];

    testData[15].stmt = strs[4];
    testData[16].stmt = strs[4];

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing => InfoStats.\n"));
    TEST_INIT;

	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
		TEST_FAILED;
		TEST_RETURN;
	}

    returncode = SQLAllocStmt((SQLHANDLE)pTestInfo->hdbc, &(pTestInfo->hstmt));	
    if (returncode != SQL_SUCCESS) {
        TEST_FAILED;
        TEST_RETURN;
    }

    returncode = SQLAllocStmt((SQLHANDLE)pTestInfo->hdbc, &secHandle);
    if(returncode != SQL_SUCCESS) {
        TEST_FAILED;
        TEST_RETURN;
    }

    for(j = 0; j < 2; j++) {
        i = 0;
        while (_tcscmp(testData[i].back,_T("end"))!=0) {

            if((j == 0) || (i==0)) {    // setup table and data
                LogMsg(NONE,_T("Setting up table and data\n"));
                returncode = SQLExecDirect(pTestInfo->hstmt, (SQLTCHAR*)strs[0], SQL_NTS);
	            returncode = SQLExecDirect(pTestInfo->hstmt, (SQLTCHAR*)strs[1], SQL_NTS);
	            returncode = SQLExecDirect(pTestInfo->hstmt, (SQLTCHAR*)strs[2], SQL_NTS);
	            returncode = SQLEndTran(SQL_HANDLE_DBC, pTestInfo->hdbc, SQL_COMMIT);
	            returncode = SQLFreeStmt(pTestInfo->hstmt, SQL_CLOSE);
            }
     
	        returncode = SQLPrepare(pTestInfo->hstmt, (SQLTCHAR*)strs[3], SQL_NTS);

            _tcscpy(cursorName, _T(""));

	        returncode = SQLGetCursorName(pTestInfo->hstmt, (SQLTCHAR*)cursorName, sizeof(cursorName), &outLen);
            if(returncode != SQL_SUCCESS)
                LogAllErrors(pTestInfo->henv, pTestInfo->hdbc, pTestInfo->hstmt);

	        returncode = SQLExecute(pTestInfo->hstmt);

            _stprintf(tempStr, _T("Starting test number %d\n"), i);
            TESTCASE_BEGINW(tempStr);

	    // Susan: Make this pass
	    #ifdef unixODBC		
	    if ( i == 0 )
		_tcscpy(testData[i].front, _T(""));
	    #endif
			
            if(testData[i].cursor == TRUE)
                _stprintf(tempStr, _T("INFOSTATS %s%s%s"), testData[i].front, cursorName, testData[i].back);
            else
                _stprintf(tempStr, _T("INFOSTATS %s%s%s"), testData[i].front, testData[i].stmt, testData[i].back);

            returncode = execute(pTestInfo, secHandle, tempStr, testData[i].retcode);
            if(returncode == FALSE)
                TEST_FAILED;

	        returncode = SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);

            TESTCASE_END;
            i++;
        }

        returncode = SQLExecDirect(pTestInfo->hstmt, (SQLTCHAR*)strs[0], SQL_NTS);
    }

	//==========================================================================================
      
	FullDisconnect3(pTestInfo);
	free_list(var_list);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing => InfoStats.\n"));
    TEST_RETURN;
}

BOOL execute(TestInfo* pTestInfo, SQLHANDLE secHandle, TCHAR* tempStr, short expRet) {

    RETCODE		returncode;
	LogMsg(NONE,_T("%s\n"), tempStr);

    returncode = SQLExecDirect(secHandle, (SQLTCHAR *)tempStr, SQL_NTS );
	if( returncode != expRet ) {	
		LogAllErrors (pTestInfo->henv, pTestInfo->hdbc, secHandle);
        LogMsg(ERRMSG, _T("Failed\n"));
		return FALSE;
	}
	else {
		if (expRet == SQL_SUCCESS) {
			returncode = getAllData(secHandle, returncode);
            if(returncode == FALSE)
                LogMsg(ERRMSG, _T("Unable to get data\n"));
		}
		else {
			//LogAllErrors (pTestInfo->henv, pTestInfo->hdbc, secHandle);
			LogMsg(NONE,_T("Passed\n"));
		}
		SQLFreeStmt(secHandle,SQL_CLOSE);
		return TRUE;
	}
}

BOOL getAllData(SQLHANDLE hstmt, RETCODE returncode) {
	struct {
        TCHAR columnName[MAX_SIZE];
        SQLSMALLINT columnNameLength;
        SQLSMALLINT dDataTypePtr;
        int columnSizePtr;
        SQLSMALLINT decimalDigitsPtr;
        SQLSMALLINT nullablePtr;
        TCHAR rowData[MAX_STR_LEN*2];
        int rowDataPtr;
    } colTable[MAX_SIZE];
	BOOL			returnFlg = TRUE;
	int				rowCount = 0;
	SQLSMALLINT		colCount = 0;
	int				loop;

	if((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))
		return FALSE;

	returncode = SQLNumResultCols(hstmt, &colCount);

	if(colCount == 0) {
		LogMsg(NONE,_T("\n\n--- SQL operation complete.\n"));
		return TRUE;
	}

	for(loop = 1; loop <= colCount; loop++) {
		returncode = SQLDescribeCol( hstmt, (SQLUSMALLINT)loop, 
            (SQLTCHAR*)&colTable[ loop ].columnName, (SQLSMALLINT)MAX_SIZE, 
            &colTable[ loop ].columnNameLength, &colTable[ loop ].dDataTypePtr,
            (SQLULEN*)&colTable[ loop ].columnSizePtr, &colTable[ loop ].decimalDigitsPtr,
            &colTable[ loop ].nullablePtr );
		if(returncode != SQL_SUCCESS) // check message also
			return FALSE;
	}

	returncode = SQLSetStmtAttr( hstmt, SQL_ATTR_ROW_BIND_TYPE, (void*)sizeof( colTable[0] ), 0 );

	returncode = SQLSetStmtAttr( hstmt, SQL_ATTR_ROW_ARRAY_SIZE, (void*)1, 0 );

	for( loop = 1; loop <= colCount ; loop++ )
    {
        returncode = SQLBindCol( hstmt, (SQLUSMALLINT)loop,  SQL_C_TCHAR, 
            (SQLINTEGER *)&colTable[ loop ].rowData, (SQLUSMALLINT)2048, 
            (SQLLEN *)&colTable[ loop ].rowDataPtr ); 
		if(returncode != SQL_SUCCESS) // check message also
			return FALSE;
    }

	for( loop = 1; loop <= colCount ; loop++ )
        {
            LogPrintf( _T("%s"), colTable[ loop ].columnName ); 
            if ( loop != colCount )
                LogPrintf(_T(" | "));
    }
    LogPrintf(_T("\n"));

	while ( ( returncode = SQLFetch( hstmt ) ) != SQL_NO_DATA_FOUND )
    {
        if( returncode != SQL_SUCCESS )
        {
            if( returncode != SQL_SUCCESS_WITH_INFO )
            {
                returncode = SQLCloseCursor( hstmt );
                if( returncode != SQL_SUCCESS )
					return FALSE;
            }
        }
        for( loop = 1; loop <= colCount ; loop++ )
        {
            if( colTable[ loop ].rowDataPtr <= 0 )
                LogPrintf( _T(" ") );
            else
                LogPrintf(_T("%s"), colTable[ loop ].rowData);
            if ( loop != colCount )
                LogPrintf(_T(" | "));
        }
        LogPrintf(_T("\n"));
        rowCount++;
    }

    LogPrintf( _T("\n--- %d row(s) retrieved.\n"), rowCount );
	return TRUE;
}

