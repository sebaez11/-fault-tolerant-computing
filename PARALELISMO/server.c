#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <signal.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <netdb.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include "queue.h"

#define PORT 2222
#define MAXLINE 4150
#define CLIENTS_LIMIT 5
#define TRUE 1

ClientService *clients[CLIENTS_LIMIT];

Queue *queue;

pthread_mutex_t clientMutex = PTHREAD_MUTEX_INITIALIZER;

int conections = 0;
int id = 1;

int createSocket(int type){
  int sockfd;
  struct sockaddr_in adr;
  int sizeAdr;

  if ((sockfd = socket(PF_INET, type, 0)) == -1){
    perror("Error: Imposible crear socket");
    exit(2);
  }

  bzero((char *)&adr, sizeof(adr));

  adr.sin_port = htons(PORT);
  adr.sin_addr.s_addr = htonl(INADDR_ANY);
  adr.sin_family = PF_INET;

  if (bind(sockfd, (struct sockaddr *)&adr, sizeof(adr)) == -1){
    perror("Binding was not possible");
    exit(3);
  }

  sizeAdr = sizeof(adr);

  if (getsockname(sockfd, (struct sockaddr *)&adr, &sizeAdr)){
    perror( "Error: Obtencion del nombre del sock");
    exit(4);
  }

  return (sockfd);
}

void createClient(ClientService *client){
  pthread_mutex_lock(&clientMutex);
  for (int i = 0; i < CLIENTS_LIMIT; ++i){
    if (!clients[i]){
      clients[i] = client;
      break;
    }
  }
  pthread_mutex_unlock(&clientMutex);
}

void deleteClient(int id){
  pthread_mutex_lock(&clientMutex);
  for (int i = 0; i < CLIENTS_LIMIT; i++){
    if (clients[i] && clients[i]->id == id){
      clients[i] = NULL;
      break;
    }
  }
  pthread_mutex_unlock(&clientMutex);
}

void sendMessage(char *message, int id){
  pthread_mutex_lock(&clientMutex);
  for (int i = 0; i < CLIENTS_LIMIT; ++i){
    if (clients[i] && clients[i]->id != id){
      if (send(clients[i]->socketFileDescriptor, message, strlen(message), 0) < 0){
        perror("ERROR: Fallo del descriptor");
        break;
      }
    }
  }
  pthread_mutex_unlock(&clientMutex);
}

void uniqueMessage(char *message, int id){
  pthread_mutex_lock(&clientMutex);
  for (int i = 0; i < CLIENTS_LIMIT; ++i){

    if (clients[i] && clients[i]->id == id){
      if (send(clients[i]->socketFileDescriptor, message, strlen(message), 0) < 0){
        perror("ERROR: Fallo del descriptor");
        break;
      }
      break;
    }
  }
  pthread_mutex_unlock(&clientMutex);
}

void manageClient(ClientService *clientThread){
  char buffer[MAXLINE];
  char name[NAME];
  int isLeave = 0;

  ClientService *client = clientThread;

  if (recv(client->socketFileDescriptor, name, NAME, 0) <= 0){
    isLeave = 1;
  }else{
    strcpy(client->name, name);
    sprintf(buffer,"%s se ha unido\n", client->name);
    printf("%s", buffer);
    sendMessage(buffer, client->id);
  }

  pthread_mutex_lock(&clientMutex);
  conections++;
  pthread_mutex_unlock(&clientMutex);

  bzero(buffer, MAXLINE);

  while (TRUE){
    if (isLeave){
      break;
    }

    int messageClient;

    if ((messageClient = recv(client->socketFileDescriptor, buffer, MAXLINE, 0)) > 0 && strlen(buffer) > 0){
      char responseMessage[MAXLINE];
      if (executeCommand(buffer, responseMessage, client->id)){
        uniqueMessage(responseMessage, client->id);
        bzero(responseMessage, MAXLINE);
      }
      else
        sendMessage(buffer, client->id);
    }else if (messageClient <= 0){
      sprintf(buffer,"%s se ha desconectado\n", client->name);
      printf("%s", buffer);
      sendMessage(buffer, client->id);
      isLeave = 1;
    }

    bzero(buffer, MAXLINE);
  }

  deleteClient(client->id);
  close(client->socketFileDescriptor);
  free(client);

  pthread_mutex_lock(&clientMutex);
  conections--;
  pthread_mutex_unlock(&clientMutex);

  if (queue->end > 0){
    ClientService *clientWaiting = removeQueue(queue);
    createClient(clientWaiting);
    responseJoinChat(clientWaiting);
  }

  pthread_detach(pthread_self());
}

void responseJoinChat(ClientService *clientThread){
  char buffer[MAXLINE];

  bzero(buffer, MAXLINE);
  sprintf(buffer, "Te has unido\n");
  send(clientThread->socketFileDescriptor, buffer, MAXLINE, 0);

  pthread_t thread;

  if (pthread_create(&thread, NULL, (void *)manageClient, (void *)clientThread) != 0){
    fprintf(stdout, "Internal Server Error\n");
    exit(1);
  }
}

int executeCommand(char *buffer, char *responseMessage, int id){
  int initCommand = 0;
  size_t lengthBuffer = strlen(buffer);

  for (int i = 1; i < lengthBuffer; i++){
    if (buffer[i] == '/'){
      initCommand = i + 1;
      break;
    }
  }

  if (initCommand != 0){
    char verifyWord[8];
    int counter = 0;
    for (int i = initCommand; i < lengthBuffer; i++){
      verifyWord[counter] = buffer[i];
      counter++;
    }
    if (strcmp(verifyWord, "users\n") != 0)
      return 0;

    strcat(responseMessage, "Users connected: \n\t");
    for (int i = 0; i < CLIENTS_LIMIT; ++i){
      if (clients[i] && clients[i]->id){
        char auxChar[MAXLINE];
        if (id != clients[i]->id)
          sprintf(auxChar, "- %s\n\t", clients[i]->name);
        else
          sprintf(auxChar,"- %s (you)\n\t", clients[i]->name);
        strcat(responseMessage, auxChar);
      }
    }
    strcat(responseMessage, "\n");
    return 1;
  }
  return 0;
}

int main(int argc, char *argv[]){

  pthread_t thread;
  int socketListen, socketService; // Descriptores de sockets
  struct sockaddr_in adr;

  queue = (Queue *)malloc(sizeof(Queue));
  queueConstructor(queue);

  int sizeAdr; // tamaño del socket

  signal(SIGPIPE, SIG_IGN);

  if ((socketListen = createSocket(SOCK_STREAM)) == -1){ // Creacion del socket de escucha
    fprintf(stderr, "Error: No se puede conectar/crear socket\n");
    exit(2);
  }

  listen(socketListen, 1024);

  fprintf(stdout, "Chatroom corre en el puerto: %d\n", PORT);

  while (TRUE){
    sizeAdr = sizeof(adr);
    socketService = accept(socketListen, (struct sockaddr *)&adr, &sizeAdr);

    ClientService *client = (ClientService *)malloc(sizeof(ClientService));
    client->socketFileDescriptor = socketService;
    client->id = id++;

    if (conections >= CLIENTS_LIMIT){
      char buffer[MAXLINE];

      addQueue(queue, client);
      sprintf(buffer, "Estas en la cola de espera para unirte\n");
      send(client->socketFileDescriptor, buffer, MAXLINE, 0);

      continue;
    }

    createClient(client);

    if (pthread_create(&thread, NULL, (void *)manageClient, (void *)client) != 0){
      fprintf(stdout, "Internal Server Error\n");
      exit(1);
    }
    sleep(1);
  }
}
