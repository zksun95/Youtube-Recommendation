Recommend videos based on the comments from youtube data api. Using kafak and pyspark to process the streaming data. NLP part could be improved...

## Prerequisites 
- ZooKeeper server
- Kafka server
- Kafka Python
- pySpark
- NLTK
- And some prerequisites of YouTube API, you can find them at https://developers.google.com/youtube/v3/quickstart/python

**You have to put your own youtube data api key in /server/API_KEY.txt**

## Before each step, make sure the port will be used is idle.
(Very important! Sit near a wireless router:) Good luck!)

(In 3 & 4, you may need: spark-streaming-kafka-assembly_2.11-1.6.3.jar)

 1. Run ZooKeeper server (on defult port);
 2. Run Kafka Server and create a tpoic "test" (on defult port);
 3. Run (spark submit) producer_socket.py (will run on port 2055);
 4. Run (spark submit) dataprocess_server_socket.py (will run on port 2033);
 5. Run ssr.py (will run on port 5678);
 6. Put (index.html, style.css, app.js) in local machine's server file;
 7. Browse localhost/index.html in browser, type a keyword and click search;
 8. Wait for the results... They will appear in real time...
