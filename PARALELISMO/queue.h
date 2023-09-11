#define NAME 64

typedef struct{
  int socketFileDescriptor;
  int id;
  char name[NAME];
} ClientService;

typedef struct{
  ClientService *queueClients[20];
  int init;
  int end;
  int size;
} Queue;

void queueConstructor(Queue *queue){
  queue->init = 0;
  queue->end = 0;
  queue->size = sizeof(queue->queueClients) / sizeof(*queue->queueClients);
}

void addQueue(Queue *queue, ClientService *client){
  if (queue->end > queue->size){
    return;
  }
  queue->queueClients[queue->end] = client;
  queue->end++;
};

ClientService *removeQueue(Queue *queue){
  if (queue->end > 0){
    ClientService *clientAux = queue->queueClients[0];
    for (int i = 0; i < queue->end; i++)
      queue->queueClients[i] = queue->queueClients[i + 1];
    queue->end--;

    return clientAux;
  }
}