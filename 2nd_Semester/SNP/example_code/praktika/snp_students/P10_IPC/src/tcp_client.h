#ifndef _TCP_CLIENT_H_
#define _TCP_CLIENT_H_

/**
 * @brief Connect the client to a specific server via a specific port. 
 *        Sets up address information, create socket and connect.
 *        The socket address is the triad of transport protocol, IP address
 *        and port number.
 * 
 * @param ServerName [IN] char array of an IP or resolvable hostname
 * @param PortNumber [IN] char array of a port
 * @return int - returns socket for communication purpose
 */
int  client_connect  (const char* ServerName, const char* PortNumber);

/**
 * @brief Receive data from communication socket. 
 * 
 * @param communicationSocket [IN] - Communication socket
 * @param buffer [IN] - pointer to a buffer to be written with received data
 * @param len [IN] - number of bytes to be able to receive and store in buffer
 * @return int - return number of chars received.
 */
int  receiveResponse (int communicationSocket, char* buffer,int len);

/**
 * @brief Send TCP request to the given socket.
 * 
 * @param communicationSocket [IN] - Communication socket
 * @param buffer [IN] - pointer to a buffer to be send
 * @param len [IN] - number of bytes to be send of buffer
 */
void sendRequest     (int communicationSocket, char* buffer, int len);
#endif // _TCP_CLIENT_H_
