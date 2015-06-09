#include "include.h"
#include "defines.h"
#include "bitlib.h"
#include "table.h"
#include "ODBCcommon.h"

#include "globals.h"
//#include "globals.c"
//******************************************************************
//** GLOBALS.C - Declarations for global variables
//*******************************************************************
#include "commonglobals.c"
#define USAGE "Usage: NomadMaster <command-infile> <log-file> [ <random_seed> ] [ <debug_flag> ]"

char g_CommandLine[16384];

char g_errstr[10] = "***ERROR:";
char g_indent[10] = "         ";
char g_token_string[80];
short g_current_token;
test_desc g_info;
char g_nomad_volume[_MAX_PATH];
char g_testid_file[_MAX_PATH];
char g_input_line[MAX_LINE];
HENV ghenv;
HDBC ghdbc;
HSTMT ghstmt;

extern short get_next_line(void);
extern short parse_commands(void);
extern short create_process_infiles(void);
extern short start_processes(void);
extern short start_work(void);

/***********************************************************************
** initialize()
**
** This function initializes the global test information structure and
** gets and verifies information from the NOMAD configuration file.
************************************************************************/
void initialize(void)
{
   FILE *fp;
	RETCODE rc;
    int status;
	errno=0;

   /* clear all values to NULL or 0 in the structure */
   memset(&g_info,0,sizeof(g_info));

   /* get info from configuration file */
   fp=fopen(NOMAD_CONFIG_FILE,"r");
   if(fp==NULL){
      printf("%s unable to open '%s'\n",g_errstr,NOMAD_CONFIG_FILE);
      printf("          I have NOT been properly installed on this system\n");
      printf("          therefore, I cannot continue\n");
      /*>>> maybe have it assume default values or install/reinstall itself*/
		exit(EXIT_FAILURE);
      }
   else{
      sscanf(fget_s(g_input_line,MAX_LINE,fp),"%s ",g_nomad_volume);
      sscanf(fget_s(g_input_line,MAX_LINE,fp),"%s ",g_info.work_volume);
      sscanf(fget_s(g_input_line,MAX_LINE,fp),"%s ",g_info.catalog);
      sscanf(fget_s(g_input_line,MAX_LINE,fp),"%s ",g_info.object_file);
      sscanf(fget_s(g_input_line,MAX_LINE,fp),"%s ",gDataSource);
      sscanf(fget_s(g_input_line,MAX_LINE,fp),"%s ",gUID);
      sscanf(fget_s(g_input_line,MAX_LINE,fp),"%s ",gPWD);
      }

   /* make everything upper case */
   toupper_s(g_nomad_volume);
   toupper_s(g_info.work_volume);
   toupper_s(g_info.catalog);
	if(strcmp(gUID,"NULL")==0) gUID[0]=NULL;
	if(strcmp(gPWD,"NULL")==0) gPWD[0]=NULL;

	// >>>(need to fix this)create any directories
	if(strcmp(g_nomad_volume,".")!=0 && strcmp(g_nomad_volume,"..")!=0){
		if(mkdir(g_nomad_volume,S_IRWXU|S_IRWXG|S_IRWXO)!=0){
			printf("%s  unable to create NOMAD's main directory '%s'\n",
				g_errstr,g_nomad_volume);
			printf("   errno='%s'\n",strerror(errno));
			exit(EXIT_FAILURE);
			}
		}
	if(strcmp(g_info.work_volume,".")!=0 && strcmp(g_info.work_volume,"..")!=0){
		status=mkdir(g_info.work_volume,S_IRWXU|S_IRWXG|S_IRWXO);
		if(status!=0){
			printf("%s  unable to create NOMAD's work directory '%s'\n",
				g_errstr,g_info.work_volume);
			printf("   errno='%s'\n",strerror(errno));
			exit(EXIT_FAILURE);
			}
		}

   /* build testid filename */
   sprintf(g_testid_file,"%s/TestIDs.txt",g_nomad_volume);

	gpSQLTypeInfoList=GetSQLTypeInfo(gDataSource,gUID,gPWD);
	if(gpSQLTypeInfoList==NULL){
		printf("GetSQLTypeInfo() failed.  Check logfile for details.\n");
		if(gDebug) assert(FALSE);
		exit(EXIT_FAILURE);
		}

	// keep this connection and statement handle for all future ODBC needs
	if(!FullConnect(gDataSource,gUID,gPWD,&ghenv,&ghdbc)){
		printf("FullConnect failed\n");
		if(gDebug) assert(FALSE);
		exit(EXIT_FAILURE);
		}
	rc=SQLAllocHandle(SQL_HANDLE_STMT,ghdbc,&ghstmt);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLAllocStmt"))LogAllErrors(ghenv,ghdbc,NULL);

	rc=SQLGetInfo(ghdbc,SQL_MAX_ROW_SIZE,&gMaxRowSize,sizeof(gMaxRowSize),NULL);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLGetInfo"))LogAllErrors(ghenv,ghdbc,NULL);
	if(gMaxRowSize==0) gMaxRowSize=SQL_MAX_ROW_LENGTH;

   } /* end: initialize() */

/***********************************************************************
** init_nomad_env()
**
************************************************************************/
void init_nomad_env(void)
{
//   short i;

   /* create a new TESTxx file */
//   put_testid_info();

   /* create tables used to do VSBB inserts from */
/*   for(i=0;i<g_info.table_count;i++){
      build_vsbb_table(g_info.table_ptr[i]);
      }
*/
   } /* end: init_nomad_env() */


/**********************************************************************
** main.c
**
** Mainline for the NOMAD command interpreter (also refered to as the
** Master Process).
***********************************************************************/
int main(int argc,char *argv[])
{
	FILE *Mystdin;
	FILE *LogFilePtr;
	short rc;

	if(argc<3){
		printf("***ERROR: required parameters are missing\n");
		printf("%s\n",USAGE);
		exit(EXIT_FAILURE);
	}

	// get name of input command file which will be remapped to STDIN
	// all parms and commands are input through stdin file
	strcpy(gCommandFile,argv[1]);
	Mystdin=freopen(gCommandFile, "r", stdin );
   if(Mystdin==NULL){
   	printf("***ERROR: unable to open command infile, '%s'. Reason: %s\n",
   			gCommandFile,strerror(errno));
		printf("%s\n",USAGE);
   	exit(EXIT_FAILURE);
   }

   /* open and initialize log file */
   LogFilePtr=fopen(argv[2],"a");
   if(LogFilePtr==NULL){
   	printf("***ERROR: unable to open log file, '%s'.  Reason: %s\n",
   			argv[2],strerror(errno));
		printf("%s\n",USAGE);
   	exit(EXIT_FAILURE);
   }
   fclose(LogFilePtr);
   rc=LogInit(argv[2],5);
   if(rc!=SUCCESS){
   	printf("***ERROR: unable to initialize log file.\n");
   	exit(EXIT_FAILURE);
   }

   /* print header */
	LogMsg(LINEAFTER,"NOMAD: ODBC/SQL/TM Query/Transaction Generator (Version %d)\n"
                    "       Compiled: %s  %s\n\n",
				        VERSION,__DATE__,__TIME__);

   /* initialize some data structures, prime the parser, etc. */
   initialize();

   if(argc>3) {
      g_info.RandomSeed=(unsigned short)atoi(argv[3]);
      }
   else {
      /* initialize the random number generator */
      g_info.RandomSeed=(unsigned short)(time(NULL)&0x0000FFFF);
      }

   srand(g_info.RandomSeed);
   LogMsg(LINEAFTER,"Random Seed used for this run=%u\n",g_info.RandomSeed);

   /* set up trace options from run line */
   if(argc>4) gDebug=TRUE;
	else gDebug=FALSE;

   /* prime the parser's tokenizer by reading in the first line to parse */
   get_next_line();

   /* parse all commands from the infile */
   if(parse_commands()!=0) exit(EXIT_FAILURE);

   /* update all NOMAD environment files as needed */
   //>>>> not needed at the moment
//   init_nomad_env();

   /* create all proccess' infiles */
   rc=create_process_infiles();
	if(rc!=SUCCESS) exit(EXIT_FAILURE);

   // close global ODBC connection before starting worker processes
   FullDisconnect(ghenv,ghdbc);

   /* launch all processes */
   start_processes();

   /* notify all proceesses to begin their work */
   start_work();

   /* pause for a little while (to let all the processes get started)... */
   /* ...and then display status */

   /*>>>write a delay function*/

   /*>>> display_status function not yet written */
   /*>>> but worker processes write current status to NomadStatus.txt for now */
	//display_status(g_test_info.testid);
	exit(EXIT_SUCCESS);
   } /* end: main() */
