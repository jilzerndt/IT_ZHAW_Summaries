/* ----------------------------------------------------------------------------
 * --  _____       ______  _____                                              -
 * -- |_   _|     |  ____|/ ____|                                             -
 * --   | |  _ __ | |__  | (___    Institute of Embedded Systems              -
 * --   | | | '_ \|  __|  \___ \   Zuercher Hochschule Winterthur             -
 * --  _| |_| | | | |____ ____) |  (University of Applied Sciences)           -
 * -- |_____|_| |_|______|_____/   8401 Winterthur, Switzerland               -
 * ----------------------------------------------------------------------------
 */
/**
 * @file
 * @brief Lab implementation
 */
#include <stdio.h>
#include <stdlib.h>

#include "person.h"
#include "list.h"

#include "tcp_server.h"

static int shutdown = 0;

void perror_and_exit(const char *context) { perror(context); exit(EXIT_FAILURE); } // das muss noch an einen anderen Ort, scia

void store_person_list_to_file(FILE  *fs)
{
	char person_csv_string[60];

	person_t* person = list_getFirst();
	while(person != NULL) {
		person_to_csv_string(person,person_csv_string);
		fprintf(fs,"%s\n",person_csv_string);
		person = list_getNext();
	} 
}

void store_person_list()
{
	char* fileName = "person_list.csv";
	FILE *f = fopen (fileName, "w");

   store_person_list_to_file(f);
	if (fclose(f) != 0) perror_and_exit("fclose");
}

void load_person_list_from_file(FILE *fs)
{
	const int buf_size = 60;
	char person_csv_string[buf_size];
	person_t person;
	int r = 0;
	char* rs = 0;

	do {
      rs= fgets(person_csv_string, buf_size,fs);
     	if(rs !=NULL){
			person_from_csv_string(&person,person_csv_string);
	   	list_insert(&person);
		} 
	} while(rs !=0);
}

void load_person_list()
{
	char* fileName = "person_list.csv";
	FILE *f = fopen (fileName, "r");

	if (f == NULL) 
	{
		f = fopen (fileName, "w");
	}
	else
	{
   	load_person_list_from_file(f);
	}
	if (f == NULL) perror_and_exit("fopen");

	if (fclose(f) != 0) perror_and_exit("fclose");
}


void handleRequestPers(char* requestBuffer, int requestLen)
{
    const int responseBufferLen = 1000;
    char  responseBuffer[responseBufferLen];        // Daten-Buffer für die Antwort

    char cmd = requestBuffer[0];
    person_t person;
    switch(cmd)
    {
        case 'I':
        { 
	 		printf("handleRequestPers, cmd=%c, len=%d, &requestBuffer[2]=%s\n",cmd,requestLen, &requestBuffer[2]);
            person_from_csv_string(&person,&requestBuffer[2]);
            int retval = list_insert(&person);
			responseBuffer[0] = (char)retval;
            sendResponse(responseBuffer, 1);
        }
        break;            
        case 'R': 
        {
            person_from_csv_string(&person,&requestBuffer[2]);
			int retval = list_remove(&person);
			responseBuffer[0] = (char)retval;
            sendResponse(responseBuffer, 1);
        };
        break;
    	case 'C' :
    	{
            list_clear();
		}
		break;
    	case 'S':{ 
			//send noOfRecords
	        char recordBuffer[MAX_LEN];
	        char noOfRecords =list_size();

			sendResponse(&noOfRecords, 1);
	        printf("handleRequestPers: show, noOfRecords=%d\n",noOfRecords ) ;
	        //loop over personList and send person records to client;
		    person_t* p = list_getFirst();
	        while (p != NULL)
			{
		       	char cvs_len = 1+person_to_csv_string(p,recordBuffer);//add 1 for terminating \0
	          	printf("handleRequest: show, cvs_len=%d, recordBuffer=%s\n",cvs_len,recordBuffer) ;
			    
	          	sendResponse(&cvs_len, 1);
	          	sendResponse(recordBuffer, cvs_len);
	        	p= list_getNext();
        	};
     	}
		break;
      	case 'T': 
	 	{
			shutdown = 1;
		}
     	default:
		{
 			printf("handleRequestPers, invalid command cmd=%x\n",cmd);
		}
		break;
    }
}


/**
 * @brief Main entry point.
 * @param[in] argc  The size of the argv array.
 * @param[in] argv  The command line arguments...
 * @returns Returns EXIT_SUCCESS (=0) on success, EXIT_FAILURE (=1) there is an expression syntax error.
 */
int main(int argc, char* argv[])
{
	// BEGIN-STUDENTS-TO-ADD-CODE

	// END-STUDENTS-TO-ADD-CODE
    return EXIT_SUCCESS;
}
