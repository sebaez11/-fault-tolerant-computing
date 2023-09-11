# **Tutorial: Running a Chat Program in C**

In this tutorial, we will walk you through the process of running a simple chat program written in C. This program consists of a server (`server.c`) and a client (`client.c`) that can communicate with each other. We will also explain the use of the `pthread` library.

## **Prerequisites:**
- A C compiler (GCC recommended)
- Basic knowledge of working with the terminal

## **Step 1: Compiling the Client and Server Programs**

Open your terminal and navigate to the directory where your `client.c` and `server.c` files are located. Use the following commands to compile both the client and server programs:

```bash
gcc client.c -pthread -o client
gcc server.c -pthread -o server
```

The `-pthread` flag is necessary because the programs use POSIX threads (`pthread`) for multithreading. This flag tells the compiler to link the `pthread` library.

## **Step 2: Running the Server**

Start the server by running the following command:

```bash
./server
```

The server will start listening on port 2222 (you can change this in the code if needed). It will display a message like "Chatroom corre en el puerto: 2222"

## **Step 3: Running a Client**

Open a new terminal window for the client. Navigate to the same directory and run the client program:

```bash
./client 127.0.0.1 2222
```

## **Step 4: Chatting**

Once the client is connected, you'll be prompted to enter your name. After that, you can start sending messages. Type a message and press Enter to send it. Other clients connected to the server will receive your messages, and you'll see their messages in your terminal as well.

![Server side](https://lh3.googleusercontent.com/u/3/drive-viewer/AITFw-wRLeOAVUAq19fX1KjQAYgo0veiiXmgtrWBufqSoDIhyYZaU1blxgoWZJlFjy2Wp6730ahgIlGwny7mNR7F7JznTCm9Bg=w1920-h937)

![Client number one](https://lh3.googleusercontent.com/u/3/drive-viewer/AITFw-wNotdquhggyVL1m_pzNBSjzp4olXfOcftRZCJCukHhcjaWgPSf8SFKMnZIP77cRZ_HIleWe6qGck6qtTnRQvNAc-fOSg=w1920-h937)

![Client number two](https://lh3.googleusercontent.com/u/3/drive-viewer/AITFw-xVCheUaq3m3gM3icusvz2MKg0b1V1L2iwDcjlXe8efoXetavdK-xZPr5liIzne66UFYPUBXubtzQm8GCBCAG0xVTLP=w1920-h937)

![Client number three](https://lh3.googleusercontent.com/u/3/drive-viewer/AITFw-yl_6D_7lfl16EuuVPB9DFmlHiM37ELigj6EiafsJKbi6ou6yn14f1qAPr3QhYwtVP5ALwRim-eabo2g161Vv_OijFV=w1920-h937)

## **Step 5: Exiting**

To exit the client, press Ctrl+C in the terminal where the client is running. This will gracefully disconnect from the server.

# **Understanding pthread Library:**

The `pthread` library in C stands for POSIX threads and provides a way to create and manage threads. Threads are lightweight processes that can run concurrently, making it easier to perform multiple tasks simultaneously. In the chat program, `pthread` is used to create two threads:

1. **Thread for Receiving Messages:** This thread constantly listens for incoming messages from the server and displays them in the client's terminal.

2. **Thread for Sending Messages:** This thread allows the user to input and send messages to the server while also displaying a prompt for user input.

By using `pthread`, the chat program can handle both sending and receiving messages without blocking the user interface. It enables efficient multitasking, ensuring that the client can send and receive messages concurrently.

That's it! You now have a basic chat program up and running, and you understand the role of the `pthread` library in achieving concurrent communication. Feel free to explore the code and modify it to suit your needs or add more features. Happy coding!

