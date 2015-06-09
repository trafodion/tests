#include "include.h"
#include "defines.h"
#include "ODBCcommon.h"
#include "bitlib.h"
#include "table.h"
#include "struct.h"
#include "sqlutil.h"
#include "status.h"
#include "globals.h"


//=====================================
// External declarations
//=====================================
extern short do_delete(table_description *tab_ptr,Bitmap *bmap_ptr,long starting_record,
					 long record_count,Boolean abort_flag);
extern short do_select(table_description *tab_ptr,Bitmap *bmap_ptr,
					 short requested_record_count,Boolean abort_flag);
extern short do_insert(table_description *tab_ptr,Bitmap *bmap_ptr,
					 short requested_record_count,Boolean abort_flag);
extern short do_update(table_description *tab_ptr,Bitmap *bmap_ptr,
					 short requested_record_count,Boolean abort_flag);


/********************************************************************
** adjust_percents()
**
** modifies the <g_percent> array to be a range of
** percentages not just individual percentages
** Example: 10,10,55,25 would become 10,20,75,100
********************************************************************/
short adjust_percents()
   {
   short i;
   short total;
   short fill_items;
   short fill_percent;

   /* count how many percentages were NOT specified by the user as well... */
   /* ...as the total percent of what s/he did specify */
   total=0;
   fill_items=0;
   for(i=0;i<MAX_ACTION_TYPES;i++) {
      if(g_percent[i]==NOT_SPECIFIED) fill_items++;
      else total+=(short)g_percent[i];
      }

   /* if not all percentages add to 100% then fill in percent for actions...*/
   /* ...not specified by the user */
   if(fill_items>0){
      fill_percent=(100-total)/fill_items;
      for(i=0;i<MAX_ACTION_TYPES;i++){
         if(g_percent[i]==NOT_SPECIFIED) g_percent[i]=fill_percent;
         }
      }

   /* modify percentatges to be a range */
   total=(short)g_percent[0];
   for(i=1;i<MAX_ACTION_TYPES;i++){
      total+=(short)g_percent[i];
      g_percent[i]=total;
      }

   /* this will never happen but, just in case something got clobbered */
   if(total>100) {
      LogMsg(INTERNALERRMSG,
             "in adjust_percents() at line %ld\n"
             "<total> is %d but should never be greater than 100\n"
             "Dump of <g_percent[]>:\n",
             __LINE__,total);
      for(i=0;i<MAX_ACTION_TYPES;i++){
         LogMsg(0,"   g_percent[%d] = %d\n",i,g_percent[i]);
         }
      LogMsg(LINEAFTER,"");
      return(FAILURE);
      }
   return(SUCCESS);
   } /* end of adjust_percents() */


/********************************************************************
** choose_action: returns a randomly selected action type number
**                based on the percentage weights for choosing an
**                action (which were read in from the startup infile)
********************************************************************/
short choose_action(void)
{
   short i;
   short choice;

   choice=RANDOM_NUM1(100);
   for(i=0;i<MAX_ACTION_TYPES;i++) {
      if(g_percent[i]>choice) return(i);
      }
   return(DO_NOTHING);
   } /* end of choose_action() */


/**********************************************************************
** do_action()
**
** This function will call the appropriate function to execute an action
** based upon the <action_type> given it.
**********************************************************************/
void do_action(short action_type,short table_num,Bitmap *bitmap_ptr,
               Boolean aborting)
{
   table_description *tab_ptr;
   long record_num;
   long record_count;
   Bitmap *TempBmapPtr;
   short i;
	long temp_start;
	long temp_req;

   tab_ptr=gpTableDesc[table_num];
   post_status(OK);
   check_for_stop();

   switch(action_type) {
      case RANDOM_INSERT:
         do_insert(tab_ptr,bitmap_ptr,1,aborting);
         break;
      case RANDOM_UPDATE:
         do_update(tab_ptr,bitmap_ptr,1,aborting);
         break;

      case RANDOM_DELETE:

         /* search bitmap for a record to delete */
    	 record_num=find_next_bitblock(BIT_ON,(bitmap *)bitmap_ptr->MapPtr,
    	                               tab_ptr->max_range-1,
    	                               LongRandRange(tab_ptr->min_range,tab_ptr->max_range),
    	                               CIRCULAR_SEARCH,
    	                               1,&record_count);

         /* if no records left to delete then nothing can be done */
         if(record_num==BIT_NOT_FOUND) {
            if(gTrace){
               LogMsg(0,"No record to delete in %s\n",tab_ptr->pTable->TableName);
               }
            if(gDebug) assert(FALSE);
            return;
            }

         do_delete(tab_ptr,bitmap_ptr,record_num,record_count,aborting);
         break;

      case RANDOM_SELECT:
         do_select(tab_ptr,bitmap_ptr,1,aborting);
         break;
      case SEQ_INSERT:
         do_insert(tab_ptr,bitmap_ptr,
                   (short)RANDOM_RANGE(min_subset_size,max_subset_size),
                   aborting);
         break;
	  case SEQ_UPDATE:
         do_update(tab_ptr,bitmap_ptr,
                   (short)RANDOM_RANGE(min_subset_size,max_subset_size),
                   aborting);
         break;

      case SEQ_DELETE:

          /* search bitmap for a full block of the right size */
           temp_start=LongRandRange(tab_ptr->min_range,tab_ptr->max_range),
           temp_req=(long)RANDOM_RANGE(min_subset_size,max_subset_size),
           record_num=find_next_bitblock(BIT_ON,(bitmap *)bitmap_ptr->MapPtr,
     	                               tab_ptr->max_range-1,
     	                               temp_start,
     	                               CIRCULAR_SEARCH,
     	                               temp_req,
     	                               &record_count);
      LogMsg(DEBUGMSG,"starting=%lu, requested=%lu, actual=%lu, actual start=%lu\n",
		temp_start,temp_req,record_count,record_num);
         /* if no records left to delete then nothing can be done */
         if(record_num==BIT_NOT_FOUND) {
            if(gTrace){
               LogMsg(0,"No records to sequentially delete in %s\n",
                      tab_ptr->pTable->TableName);
               }
            if(gDebug) assert(FALSE);
            }
			else {
				do_delete(tab_ptr,bitmap_ptr,record_num,record_count,aborting);
			}
         break;

      case SEQ_SELECT:
         do_select(tab_ptr,bitmap_ptr,
                   (short)RANDOM_RANGE(min_subset_size,max_subset_size),
                   aborting);
         break;
      case VSBB_INSERT:
         if(gTrace) LogMsg(0,"   VSBB INSERTs not working, yet.\n");
         break;
/*         do_vsbb_insert(tab_ptr,bitmap_ptr,
                        (short)RANDOM_RANGE(min_vsbb_size,max_vsbb_size),
                        aborting);
         break;
*/
      case VSBB_SELECT:
         if(gTrace) LogMsg(0,"   VSBB SELECTs not working, yet.\n");
         break;
      case VSBB_UPDATE:
         if(gTrace) LogMsg(0,"   VSBB UPDATEs not working, yet.\n");
         break;
/*         do_vsbb_update(tab_ptr,bitmap_ptr,
                        (short)RANDOM_RANGE(min_vsbb_size,max_vsbb_size),
                        aborting);
         break;
*/
      case DO_NOTHING:
         if(gTrace) LogMsg(0,"   DO NOTHING\n");
         break;
      case SEQ_DELETE_ALL:
         /* For the ALL case, don't bother checking if there are any... */
         /* ...rows in the range to be deleted.  Just do the delete */
         do_delete(tab_ptr,bitmap_ptr,
                   tab_ptr->min_range,tab_ptr->max_range,aborting);
         break;

      case RANDOM_INSERT_ALL:

         /* compute how many records we need to attampt to insert */
         record_count=tab_ptr->max_range-tab_ptr->min_range+1;

         /* make a temporary bitmap to use for the inserts because... */
         /*...we want to attempt to insert ALL records in the range... */
         /*...not just the ones we think aren't there */
         TempBmapPtr=QACreateBitmap(tab_ptr->max_records);
         SetBitBlock(BIT_ON,TempBmapPtr,0,tab_ptr->max_records);
         SetBitBlock(BIT_OFF,TempBmapPtr,tab_ptr->min_range,record_count);

         /* loop through all records randomly trying to insert them */
         for(i=0;i<record_count;i++){

            /* search bitmap for a record we haven't tried to insert, yet */
            record_num=FindNextBit(BIT_OFF,TempBmapPtr,
                          LongRand(record_count)+tab_ptr->min_range,
                          CIRCULAR_SEARCH);

 /*>>>    do_insert(tab_ptr,TempBmapPtr->MapPtr,record_num,1,aborting);*/

            }

         /* Now, set all bits on in the normal bitmap */
			SetBitBlock(BIT_ON,bitmap_ptr,tab_ptr->min_range,record_count);
         break;

      case RANDOM_DELETE_ALL:
      case RANDOM_UPDATE_ALL:
      case RANDOM_SELECT_ALL:
      case SEQ_INSERT_ALL:
      case SEQ_UPDATE_ALL:
      case SEQ_SELECT_ALL:
      case VSBB_INSERT_ALL:
      case VSBB_UPDATE_ALL:
      case VSBB_SELECT_ALL:
         LogMsg(LINEAFTER,
                "I hate to tell you this but, an ALL-type action is supposed\n"
                "to be executed right here and Marvin hasn't finished the\n"
                "code.  So, complain to him not me, ok?\n");
         break;
/*      case ALTER_ADD_COLUMN:
         if(gTrace) LogMsg(0,"   ALTER TABLE ADD COLUMN not working, yet.\n");
         break;
*/
/*         DoAddColumn(tab_ptr);
         break;
*/
//      case CREATE_DROP_TABLE:
//         break;
//      case CREATE_KEEP_TABLE:
//         break;
      default:
         LogMsg(INTERNALERRMSG+LINEAFTER,
                "Hey, <action_type> = %d which is an invalid value and\n"
                "probably means I have a bug inside me, Oh, GROSS!\n",
                action_type);
         if(gDebug) assert(FALSE);
         break;
      } /* end: switch(action_type)... */
   g_action_count++;
   } /* end: do_action() */


/**********************************************************************
** execute_by_percent()
**
** This function will execute random actions against randomly selected
** tables based on percentage weights specified by the user.  It will
** execute for approx. <run_time> seconds.
**********************************************************************/
void execute_by_percent(time_t run_time)
{
   short i;
   short j;
   Bitmap *bitmap_temp_ptr[MAX_TABLES];
   short action_count;
   short action_type;
   short table_num;
   short concurrent_trans;
   Boolean done;
   short Connected;
   short iterations;
   time_t start_time;
   time_t time1;
   time_t time2;
   time_t elapsed_time;
   Boolean aborting;
   HENV	EnvironmentHandle[MAX_CONCURRENT_TRANS];
   HDBC	ConnectionHandle[MAX_CONCURRENT_TRANS];
   HSTMT	StmtHandle[MAX_CONCURRENT_TRANS];
	HENV	CurrentEnvironmentHandle;
	HDBC	CurrentConnectionHandle;
	HSTMT	CurrentStmtHandle;
	RETCODE	rc;
	short ConcurrentCount;

   concurrent_trans=RANDOM_RANGE((short)min_concurrent_trans,
                                        (short)max_concurrent_trans);
   iterations=0;
   start_time=time(NULL);
   time1=start_time;
   done=FALSE;
   while(!done){

      /* start all transactions now and work them off one at a time */
		ConcurrentCount=0;
		Connected=TRUE;
      for(i=0;(i<concurrent_trans) && Connected;i++) {
	      if(gTrace){
		      LogMsg(TIMESTAMP,"Starting connection %d of %d\n",i+1,concurrent_trans);
			   }
			Connected=FullConnect(gDataSource,gUID,gPWD,
								&EnvironmentHandle[i],&ConnectionHandle[i]);
			if(Connected){
				rc=SQLAllocStmt(ConnectionHandle[i],&StmtHandle[i]);
				if(!CHECKRC(SQL_SUCCESS,rc,"SQLAllocStmt")){
					LogAllErrors(EnvironmentHandle[i],ConnectionHandle[i],StmtHandle[i]);
					if(gDebug) assert(FALSE);
					}
				rc=SQLSetConnectOption(ConnectionHandle[i],SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_OFF);
				if(!CHECKRC(SQL_SUCCESS,rc,"SQLSetConnectOptions(SQL_AUTOCOMMIT_OFF)")){
					LogAllErrors(EnvironmentHandle[i],ConnectionHandle[i],StmtHandle[i]);
					if(gDebug) assert(FALSE);
					}
				ConcurrentCount++;
				}
			}

      /* loop for each transaction */
      for(i=0;i<ConcurrentCount;i++) {
	      if(gTrace){
		      LogMsg(NONE,"\nStarting work for connection %d\n",i+1);
			   }
			CurrentEnvironmentHandle=EnvironmentHandle[i];
			CurrentConnectionHandle=ConnectionHandle[i];
			CurrentStmtHandle=StmtHandle[i];

         /* use a copy of all tables' bitmaps because this transaction... */
         /* ...may abort whether it is supposed to or not */
         for(j=0;j<gTableCount;j++){
            bitmap_temp_ptr[j]=QACreateBitmap(gpTableDesc[j]->max_records);
            CopyBitmap(bitmap_temp_ptr[j],gpTableDesc[j]->BitmapPtr);
            }

         /* decide whether this transaction will be aborted or not */
         if(RANDOM_NUM1(100)<=abort_trans) aborting=TRUE;
         else aborting=FALSE;

			// >>> need to decide how to handle DTC transaction
			// >>> ????

         /* choose number of actions in this transaction */
         action_count=RANDOM_RANGE((short)min_actions_per_trans,(short)max_actions_per_trans);

         /* >>> should not do zerosum adjustments until the end of all */
         /* >>> actions in this transaction */
         /* >>> right now they're done in the action functions, */
         /* >>> as each action is done */
         /* loop for each action */
         for(j=0;j<action_count;j++) {

            /* choose action */
            action_type=choose_action();

            /* choose a table for this action to use */
            table_num=(short)RANDOM_NUM0(gTableCount-1);
				gpTableDesc[table_num]->henv=CurrentEnvironmentHandle;
				gpTableDesc[table_num]->hdbc=CurrentConnectionHandle;
				gpTableDesc[table_num]->hstmt=CurrentStmtHandle;

            /* do the selected action */
            do_action(action_type,table_num,bitmap_temp_ptr[table_num],
                      aborting);

            } /* end: for(j=0... */

         if(aborting){
            if(gTrace) LogMsg(0,"-- SQLTransact(SQL_ROLLBACK)\n");
				rc=SQLTransact(CurrentEnvironmentHandle,
									CurrentConnectionHandle,
									SQL_ROLLBACK);
				if(!CHECKRC(SQL_SUCCESS,rc,"SQLTransact(SQL_ROLLBACK)")){
					LogAllErrors(CurrentEnvironmentHandle,CurrentConnectionHandle,CurrentStmtHandle);
					if(gDebug) assert(FALSE);
					}
            g_trans_abort++;
            }
         else {
            if(gTrace) LogMsg(0,"-- SQLTransact(SQL_COMMIT)\n");
				rc=SQLTransact(CurrentEnvironmentHandle,
									CurrentConnectionHandle,
									SQL_COMMIT);
				if(!CHECKRC(SQL_SUCCESS,rc,"SQLTransact(SQL_COMMIT)")){
					LogAllErrors(CurrentEnvironmentHandle,CurrentConnectionHandle,CurrentStmtHandle);
					if(gDebug) assert(FALSE);
					}
            g_trans_commit++;

            /* if no errors then make temporary bitmaps the good bitmaps */
            for(j=0;j<gTableCount;j++){
	            CopyBitmap(gpTableDesc[j]->BitmapPtr,bitmap_temp_ptr[j]);
               }
            } /* end else */

         if(gTrace) LogMsg(0,"---------------------------------------\n");

         /* return space used by temporary bitmaps */
         for(j=0;j<gTableCount;j++){
				FreeBitmap(bitmap_temp_ptr[j]);
            }
         } /* end: for(i=0... (loop for each transaction) */

      /* is it time to check tables for consistency? */
      time2=time(NULL);
      if(difftime(time2,time1)>=gCheckInterval){
         time1=time2;

         /* loop for each table and check its consistency */
         for(i=0;i<gTableCount;i++){
            rc=consist_check(gpTableDesc[i]);
            /*>>> handle errors, maybe let user specify what to do */
            }
         }

      if(run_time>0){
         elapsed_time=(long)difftime(time(NULL),start_time);
         if(elapsed_time>run_time) done=TRUE;
         }
      else if(run_time<0) done=TRUE;

      for(i=0;i<ConcurrentCount;i++) {
			rc=SQLFreeStmt(StmtHandle[i],SQL_DROP);
			//>>>> need to check errors
			FullDisconnect(EnvironmentHandle[i],ConnectionHandle[i]);
			}

      } /* end: while(!done) loop */

   } /* end of execute_by_percent() */


/**********************************************************************
** execute_by_action()
**
** This function will execute a given action a specified number of
** repetitions.  The command will execute against a randomly selected
** table (from the list of available tables).
**********************************************************************/
void execute_by_action(short action_type,short action_count)
{
   short i;
   short j;
   short table_num;
   short error;
   Boolean aborting;
   Bitmap *bitmap_temp_ptr[MAX_TABLES];
   time_t time1;
   time_t time2;
	HENV	CurrentEnvironmentHandle;
	HDBC	CurrentConnectionHandle;
	HSTMT	CurrentStmtHandle;
	RETCODE	rc;

   time1=time(NULL);
   action_type=-action_type;

   /* start a transaction */
   if(gTrace) LogMsg(TIMESTAMP,"Starting a connection\n");
	error=FullConnect(gDataSource,gUID,gPWD,
							&CurrentEnvironmentHandle,&CurrentConnectionHandle);
	rc=SQLAllocStmt(CurrentConnectionHandle,&CurrentStmtHandle);
   /*>>> handle errors */
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLAllocStmt")){
		LogAllErrors(CurrentEnvironmentHandle,CurrentConnectionHandle,CurrentStmtHandle);
		if(gDebug) assert(FALSE);
		}
	rc=SQLSetConnectOption(CurrentConnectionHandle,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_OFF);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLSetConnectOption(SQL_AUTOCOMMIT_OFF)")){
		LogAllErrors(CurrentEnvironmentHandle,CurrentConnectionHandle,CurrentStmtHandle);
		if(gDebug) assert(FALSE);
		}

   /* use a copy of all tables' bitmaps because this transaction... */
   /* ...may abort whether it is supposed to or not */
   for(j=0;j<gTableCount;j++){
      bitmap_temp_ptr[j]=QACreateBitmap(gpTableDesc[j]->max_records);
      CopyBitmap(bitmap_temp_ptr[j],gpTableDesc[j]->BitmapPtr);
      }

   /* decide whether this transaction will be aborted or not */
   if((rand()%100)+1<=abort_trans) aborting=TRUE;
   else aborting=FALSE;

	// >>> need to decide how to handle DTC transaction
	// >>> ????

   /* >>> should not do zerosum adjustments until the end of all */
   /* >>> actions in this transaction */
   /* >>> right now they're done in the action functions, */
   /* >>> as each action is done */
   /* loop for number of repetitions */
   for(j=0;j<action_count;j++) {

      /* choose a table for this action to use */
      table_num=(short)RANDOM_NUM0(gTableCount-1);

      /* do the selected action */
      do_action(action_type,table_num,bitmap_temp_ptr[table_num],aborting);

      } /* end: for(j=0... */

   if(aborting){
		rc=SQLTransact(CurrentEnvironmentHandle,
							CurrentConnectionHandle,
							SQL_ROLLBACK);
		if(!CHECKRC(SQL_SUCCESS,rc,"SQLTransact(SQL_ROLLBACK)")){
			LogAllErrors(CurrentEnvironmentHandle,CurrentConnectionHandle,CurrentStmtHandle);
			if(gDebug) assert(FALSE);
			}
		g_trans_abort++;
		}
	else {
		rc=SQLTransact(CurrentEnvironmentHandle,
							CurrentConnectionHandle,
							SQL_COMMIT);
		if(!CHECKRC(SQL_SUCCESS,rc,"SQLTransact(SQL_COMMIT)")){
			LogAllErrors(CurrentEnvironmentHandle,CurrentConnectionHandle,CurrentStmtHandle);
			if(gDebug) assert(FALSE);
			}
      g_trans_commit++;

      /* if no errors then make temporary bitmaps the good bitmaps */
      if(error==0) {
         for(j=0;j<gTableCount;j++){
            CopyBitmap(gpTableDesc[j]->BitmapPtr,bitmap_temp_ptr[j]);
            }
         }
      } /* end else */

   /* return space used by temporary bitmaps */
   for(j=0;j<gTableCount;j++){
		FreeBitmap(bitmap_temp_ptr[j]);
      }

   /* is it time to check tables for consistency? */
   time2=time(NULL);
   if(difftime(time2,time1)>=gCheckInterval){
      time1=time2;

      /* loop for each table and check its consistency */
      for(i=0;i<gTableCount;i++){
            error=consist_check(gpTableDesc[i]);
         /*>>> handle errors, maybe let user specify what to do */
         }
      }

	rc=SQLFreeStmt(CurrentStmtHandle,SQL_DROP);
	//>>>> need to check errors
	FullDisconnect(CurrentEnvironmentHandle,CurrentConnectionHandle);

   } /* end of execute_by_action() */

