## Microservice Architecture and System Design with Python & Kubernetes

This repository refers to the [freeCodeCamp.org](https://www.freecodecamp.org/) hands-on tutorial about microservices architecture and distributed systems using Python, Kubernetes, RabbitMQ, MongoDB, and MySQL.

Watch the [YouTube video](https://www.youtube.com/watch?v=hmkF77F9TLw) for more information.

### Application to convert video files to mp3

<img width="1931" height="939" alt="microservices" src="https://github.com/user-attachments/assets/25941e23-36ee-415c-a4d9-4e12871fc091" />

### Description

1. User `uploads video` to be converted to mp3
2. The request will first hit our `API Gateway`
3. The Gateway will `store the video in mongoDB` and `put a message in the queue (RabbitMQ)` letting downstream services that there is a video to be processed in mongoDB
4. The `video_to_mp3`  converter service will consume messages from the queue. It will then
  * get the ID of the video from the message
  * pull that video from mongoDB
  * convert to mp3
  * store the mp3 on mongoDB
  * put a new message on the Queue to be consumed by the notification service that says "the conversion job is done"
6. The notification service consumes those messages from the queue and sends an email notification to the client informing the client that the mp3 for the video that he/she uploaded is "ready for download"
7. The client will use a `unique ID` acquired from the notification + his/her `JWT` to make a request to the API Gateway to download the mp3
8. The API Gateway will pull the mp3 from mongoDB and serve it to the client 









### Frameworks used




