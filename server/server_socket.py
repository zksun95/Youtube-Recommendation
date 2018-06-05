import asyncio
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from comsProvider import CommentsProvider
import websockets
import time
import json

from sentiment import CommentSentiment
from youtubesearch import YouTubeSearch
from textblob import TextBlob

def filterComments(x):
    x = x.split("||")
    if(len(x)==3):
        return (x[0],x[1],x[2])
    else:
        return (-1,-1,-1)

def preprocessing(sentence):
        try:
            sentence=sentence.translate(to='en')
        except:
            sentence=sentence
        sentence=TextBlob(' '.join(sentence.words.lemmatize()))
        return sentence

def getPolar(x):
    sentence = TextBlob(x[1])
    #sentence = preprocessing(sentence)
    p = sentence.polarity
    return (x[0], (p*float(x[2]), int(x[2])))

async def echo(websocket, path):
    async for message in websocket:
        print(message)
        await websocket.send("Start listening...")
        sc = SparkContext()
        ssc = StreamingContext(sc, 5)

        # lines = ssc.socketTextStream("localhost", 9092)
        kvs = KafkaUtils.createDirectStream(ssc, ['test'], {'bootstrap.servers':'localhost:9092'})

        # words = lines.flatMap(lambda line: line.split(" "))
        # data = lines.flatMap(lambda line: line.split("|||"))
        comments = kvs.map(lambda x: filterComments(x[1]))
        validComments = comments.filter(lambda x: x[2] != -1)
        #validComments.pprint()
        commentsPolar = validComments.map(lambda x: getPolar(x))
        #commentsPolar.foreachRDD(lambda x: websocket.send(x))
        #commentsPolar.pprint()
        result = commentsPolar.reduceByKey(lambda x, y: (x[0]+y[0], x[1]+y[1]))
        finalresult = result.map(lambda x: (x[0],x[1][0],x[1][1]))
        finalresult.saveAsTextFiles("data/time")
        #commentsPolar.pprint()
        #commentsPolar.saveAsTextFiles("data/"+str(int(time.time()))+".txt")
        
        # pairs = words.map(lambda word: (word, 1))
        #b wordCounts = pairs.reduceByKey(lambda x, y: x + y)

        # Print the first ten elements of each RDD generated in this DStream to the console
        print("1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
        # kvs.pprint()
        # comments.pprint()
        # validComments.pprint()
        # commentsPolar.pprint()
        
        #result.foreachRDD(lambda x: websocket.send(x))

        #words.foreachRDD(print)
        ssc.start()             # Start the computation
        ssc.awaitTermination()

        #kvs = KafkaUtils.createDirectStream(ssc, ['test'], {'bootstrap.servers':'localhost:9092'})
        #kvs = KafkaUtils.createDirectStream(ssc, ['test'], {"metadata.broker.list": "localhost:9092"})
        



        

        ssc.start()
        ssc.awaitTermination()


asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 2033))
asyncio.get_event_loop().run_forever()



