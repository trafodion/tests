#define USER_REQUESTED_STOP    1
#define OK                     2
#define FINISHED               3
#define STARTED                4
#define INIT_TABLES            5
#define ERROR_STOP             6
#define STATUS_RETRIES       100

#define STOP_ON_ERROR {if(gStopOnError==TRUE) stop_on_error();}

extern void post_status(short msg_num);
extern void check_for_stop();
extern void stop_on_error();
extern short consist_check(table_description *table_ptr);

