#ifndef _TCP_SERVER_H_
#define _TCP_SERVER_H_

/**
 * @brief Initialize the server and define the socket:
 *          1. getaddrinfo()
 *          2. socket()
 *          3. bind()
 * 
 * @param portNumber [IN] - set the port number where 
 *                          the server is listening to.
 */
void server_init(char* portNumber);


/**
 * @brief Get the number of bytes sent by client 
 * 
 * @param requestBuffer [IN] - pointer to a buffer where 
 *                             incoming data bytes will be stored.
 * @param max_len [IN] - maximum length of incoming data.
 * @return int - number of bytes received from client.
 */
int  getRequest(char* requestBuffer, int max_len);


/**
 * @brief Send response to client
 * 
 * @param response [IN] - pointer to a buffer.
 * @param resp_len [IN] - number of bytes to be send from buffer.
 */
void sendResponse(char* response, int resp_len);


/**
 * @brief Close the connection to the server if it has been 
 *        established.
 */
void server_close_connection(void);

#endif // _TCP_SERVER_H_


