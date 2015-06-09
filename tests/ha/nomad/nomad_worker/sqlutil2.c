/******************
** include files **
******************/
#include "include.h"
#include "defines.h"
#include "ODBCcommon.h"
#include "table.h"
#include "struct.h"
#include "globals.h"
#include "sqlutil.h"
#include "sqlutil2.h"

/***********************************************************************
** SetKeyColumnValue()
**
** This function sets the specified key value into the set of key columns.
** This function is needed in the case of multi-column keys.  One key column
** is set to the key value and all other key columns are set to a random
** default value.
************************************************************************/
ReturnStatus *SetKeyColumnValue(table_description *tab_ptr,long KeyValue)
{
	key_info *pKey;
	ColumnInfo *pCol;
	char *pMessage;
	ReturnStatus *pReturnStatus;
	TableInfo *pTable;
	short i;
	RETCODE rc;

	pTable=tab_ptr->pTable;
	pReturnStatus=NULL;

	// copy default values from key descriptions into column values
	pKey=tab_ptr->key_ptr;
	for(i=0;i<pTable->KeyColCount;i++){
		pCol=&(pTable->ColPtr[pKey->ColNum]);
		memcpy(pCol->Value.pChar,pKey->DefaultValue,pCol->DataTypeLen);
		pKey++;
		}

	// overlay the key column used with our key value
	memcpy(pCol->Value.pChar,&KeyValue,sizeof(KeyValue));
	rc=SQLBindParameter(tab_ptr->hstmt,i,SQL_PARAM_INPUT,SQL_C_LONG,
		pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
		pCol->Value.pChar,0,NULL);
	pMessage=CHECKRC_STR(SQL_SUCCESS,rc,"SQLBindParameter");
	if(pMessage!=NULL){
		pReturnStatus=BuildReturnStatus(RT_ODBC,rc,pMessage,NULL);
		free(pMessage);
		if(gDebug) assert(FALSE);
		return(pReturnStatus);
		}

	return(pReturnStatus);
	}


