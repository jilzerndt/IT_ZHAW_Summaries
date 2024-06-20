#include <stdio.h>
#include <stdlib.h>
#include <netdb.h>
#include "snp_error_handler.h"


void ExitOnError(int Status, char* Text) {
   if (Status < 0) {
      fprintf(stderr, "%s: %s\n", Text, gai_strerror(Status));
      exit(1);
   }
}


