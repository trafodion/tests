#include "defines.h"
#include "include.h"
#include "ODBCcommon.h"
#include "table.h"
#include "struct.h"
#include "globals.h"

/*************************************************************************
** do_select()
**
** Randomly chooses a record or subset of sequential records to be
** read from the specified table and then attempts to read them.
*************************************************************************/
short do_select(table_description *tab_ptr,Bitmap *bmap_ptr,
					 short requested_record_count,Boolean abort_flag)
{
   long record_num;
   long last_record_num;
   long actual_record_count;
   long record_count;
   char *key_column_name;
   char fields[80];
   char select_str[SQL_MAX_COMMAND_LENGTH];
   char command_line[SQL_MAX_COMMAND_LENGTH];
	RETCODE rc;
	ColumnInfo *pCol;
	HENV	henv;
	HDBC	hdbc;
	HSTMT	hstmt;

   henv=tab_ptr->henv;
   hdbc=tab_ptr->hdbc;
   hstmt=tab_ptr->hstmt;
//	abort_flag=abort_flag;

	LogMsg(NONE,"\n");

   /* search bitmap for a full block of the right size */
   record_num=FindNextBitBlock(BIT_ON,bmap_ptr,
                               LongRand((long)tab_ptr->max_records-1),
                               CIRCULAR_SEARCH,
                               requested_record_count,&record_count);

   /* if no records to read then nothing can be done */
   if(record_num==BIT_NOT_FOUND) {
      if(gTrace){
         LogMsg(0,"No records to select in %s\n",tab_ptr->pTable->TableName);
         if(gDebug) assert(FALSE);
         }
      return(SUCCESS);
      }

   /* build the SELECT statement used to read the records */
	pCol=&(tab_ptr->pTable->ColPtr[tab_ptr->key_column_used]);
   strcpy(select_str,"SELECT %s FROM %s WHERE %s>=?p1");

	rc=SQLBindParameter(hstmt,1,SQL_PARAM_INPUT,SQL_C_LONG,
								pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
								&record_num,0,NULL);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
		LogAllErrors(henv,hdbc,hstmt);
      if(gDebug) assert(FALSE);
      return(FAILURE);
      }

   last_record_num=record_num+record_count-1;
   if(last_record_num>tab_ptr->max_records){
      strcat(select_str," OR %s<=?p2");
      last_record_num-=tab_ptr->max_records;
      }
   else {
      strcat(select_str," AND %s<=?p2");
      }

   LogMsg(TIMESTAMP+INFOMSG,"Selecting %lu records from %lu to %lu\n",
   		record_count,record_num,last_record_num);

	rc=SQLBindParameter(hstmt,2,SQL_PARAM_INPUT,SQL_C_LONG,
								pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
								&last_record_num,0,NULL);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
		LogAllErrors(henv,hdbc,hstmt);
      if(gDebug) assert(FALSE);
      return(FAILURE);
      }

   /* handle case where key is SYSKEY */
   key_column_name=pCol->CName;

   switch(tab_ptr->pTable->Organization){
      case ENTRY_SEQ:
      case KEY_SEQ:
         strcpy(fields,"*");
         break;
      case RELATIVE_TABLE:
         strcpy(fields,"SYSKEY,*");
         break;
      }


   /* PREPARE the SELECT statement */
   sprintf(command_line,select_str,fields,tab_ptr->pTable->TableName,
           key_column_name,key_column_name);

   /* provide trace information if flag set */
	if(gTrace){
		LogMsg(NONE,"   Parameter1=%ld,  Parameter2=%ld\n",record_num,last_record_num);
		LogMsg(0,"   %s\n",command_line);
		}

	rc=SQLPrepare(hstmt,command_line,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLPrepare")){
		LogAllErrors(henv,hdbc,hstmt);
      if(gDebug) assert(FALSE);
      return(FAILURE);
      }

   /* execute the prepared SELECT statement to read each record */
	rc=SQLExecute(hstmt);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecute")){
		LogAllErrors(henv,hdbc,hstmt);
      if(gDebug) assert(FALSE);
      return(FAILURE);
      }

	//>>>maybe should bind columns before doing the fetch
//	if(!(BindAllColumns(tab_ptr))) return(FAILURE);

	actual_record_count=0;
   while((rc>=SQL_SUCCESS)&&(rc!=SQL_NO_DATA)){
		rc=SQLFetch(hstmt);
		if(rc!=SQL_NO_DATA){
			if(!CHECKRC(SQL_SUCCESS,rc,"SQLFetch")){
				LogAllErrors(henv,hdbc,hstmt);
		      if(gDebug) assert(FALSE);
				return(FAILURE);
				}

	      actual_record_count++;

			/* >>> can't check abort bit since this transaction may have other...*/
			/*...actions which set it */

	      /* once sucessfully read then mark bit in bitmap */
		   /* (just in case its out-of-date) */
	      SetBit(BIT_ON,bmap_ptr,record_num);
			}
      }

   /* check that no more than the records requested were read (sanity check) */
   if((rc==SQL_NO_DATA)&&(actual_record_count>record_count)){
      LogMsg(ERRMSG,"SELECT read %d but, should have read %d records\n",
             actual_record_count,record_count);
      if(gDebug) assert(FALSE);
      }

	rc=SQLFreeStmt(hstmt,SQL_CLOSE);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLFreeStmt")){
		LogAllErrors(henv,hdbc,hstmt);
      if(gDebug) assert(FALSE);
      return(FAILURE);
      }

   if(gTrace){
      LogMsg(0,"   -- %ld records selected\n",actual_record_count);
      }
   return(SUCCESS);
   }
