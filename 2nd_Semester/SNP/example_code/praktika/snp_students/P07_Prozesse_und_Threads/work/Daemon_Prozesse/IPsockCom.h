//*****************************************************************************
// ipCom.c          IP Socket Functions
// Original Autor:  M. Thaler, M. Pellaton (Modul BSY)
//*****************************************************************************

#ifndef IP_COM_SOCKETS
#define IP_COM_SOCKETS

#define COM_BUF_SIZE 512

#define PIDperror()\
     fprintf(stderr,"fatal error, daemon with PID %d: ",getpid());

int getTimeFromServer(char *host, int port, char *buffer, int bufferLen);
int StartTimeServer(int PortNumber);
int WaitForClient(int sfd, char *buffer);

#endif

//***************************************************************************
