#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <signal.h>
#include <netdb.h>
#include <pthread.h>
#include <string.h>
#include <time.h>

#define MAXLINE 4096
#define NAMELEN 64
#define TRUE 1


char name[NAMELEN];
int flag = 0;


void receiveMessage(int socketFileDescriptor){
  char message[MAXLINE + NAMELEN] = {};
  while (1){
    int receive = recv(socketFileDescriptor, message, MAXLINE + NAMELEN, 0);
    if (receive > 0){
      isForMe(message);
      printf("%s", message);
      prompt();
    }
    if (receive == 0){
      break;
    }
    memset(message, 0, sizeof(message));
  }
}

void isForMe(char *buffer){
  int initMessage = 0;
  char nameMessage[NAMELEN] = {};
  size_t lengthBuffer = strlen(buffer);
  for (int i = 1; i < lengthBuffer; i++){
    if (buffer[i] == ':'){
      initMessage = i + 1;
      break;
    }
  }
  if (initMessage != 0 && buffer[initMessage] == '_'){
    int namePosition = 0;
    for (int i = initMessage + 1; i < lengthBuffer; i++){
      if (buffer[i] == '_'){
        initMessage = i + 1;
        break;
      }
      nameMessage[namePosition] = buffer[i];
      namePosition++;
    }
  }
  if (strcmp(nameMessage, name) != 0)
    return;
  for (int i = initMessage; i < lengthBuffer; i++){
    buffer[i] = buffer[i] - 1;
  }
}

void sendMessage(int socketFileDescriptor){

  char buffer[MAXLINE] = {};
  char message[MAXLINE + NAMELEN] = {};
  while (TRUE){
    prompt();
    fgets(buffer, MAXLINE, stdin);
    purgeBuffer(buffer, MAXLINE);
    isPrivate(buffer);
    sprintf(message, "%s:%s\n", name, buffer);
    send(socketFileDescriptor, message, strlen(message), 0);
    bzero(message, MAXLINE + NAMELEN);
    bzero(buffer, MAXLINE);
  }

}

void isPrivate(char *buffer){
  int initName = 0;
  int initMessage = 0;
  size_t lengthBuffer = strlen(buffer);
  if (buffer[0] == '_'){
    for (int i = 1; i < lengthBuffer; i++){
      if (buffer[i] == '_'){
        initName = i + 1;
        break;
      }
    }
  }
  if (initName != 0){
    for (int i = initName; i < lengthBuffer; i++){
      buffer[i] = buffer[i] + 1;
    }
  }
}

void purgeBuffer(char *buffer, int length){
  for (int i = 0; i < length; i++){
    if (buffer[i] == '\n'){
      buffer[i] = '\0';
      break;
    }
  }
}

void prompt(){
  printf("\r%s", ">");
  fflush(stdout);
}

void ctrlC(){
  flag = 1;
}

void enterName(){
  printf("Ingresa un nombre: ");
  fgets(name, NAMELEN, stdin);
}


int main(int argc, char *argv[]){
  int socketService; // descriptor socket

  struct sockaddr_in adr;

  /* address of the socket destination */
  struct hostent *hp, *gethostbyname();

  if (argc != 3){
    fprintf(stderr, "Use: %s <host> <port (2222)>\n", argv[0]);
    exit(1);
  }

  /* Create socket */
  if ((socketService = socket(PF_INET, SOCK_STREAM, 0)) == -1){
    perror("Imposible creacion del socket");
    exit(2);
  }

  /* Search address internet server*/
  if ((hp = gethostbyname(argv[1])) == NULL){
    perror("Error: Nombre de la maquina desconocido");
    exit(3);
  }

  /* Preparation of the socket destination */
  adr.sin_family = PF_INET;
  adr.sin_addr.s_addr = htonl(argv[1]);
  adr.sin_port = htons(atoi(argv[2]));
  bcopy(hp->h_addr, &adr.sin_addr, hp->h_length);

  /* Conect socket server */
  if (connect(socketService, (struct sockaddr *)&adr, sizeof(adr)) == -1){
    perror("Connect failed");
    exit(4);
  }

  signal(SIGINT, ctrlC);
  srand(time(NULL));

  while (TRUE){
    enterName();
    purgeBuffer(name, NAMELEN);
    if (strlen(name) > 3){
      printf("Tu nombre será %s\n", name);
      break;
    }
  }
  printf("Formato de mensaje privado: _nombre_mensaje\n");

  fflush(stdin);
  send(socketService, name, NAMELEN, 0);

  pthread_t receiveMessageThread;

  if (pthread_create(&receiveMessageThread, NULL, (void *)receiveMessage, (void *)socketService) != 0){
    printf("Error thread");
    exit(1);
  }

  pthread_t sendMessageThread;

  if (pthread_create(&sendMessageThread, NULL, (void *)sendMessage, (void *)socketService) != 0){
    printf("Error thread");
    exit(1);
  }

  while (TRUE){
    if (flag){
      printf("\nVuelve pronto\n");
      break;
    }
  }
  close(socketService);
}

