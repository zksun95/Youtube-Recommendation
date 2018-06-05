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
    sentence = preprocessing(sentence)
    p = sentence.polarity
    return (x[0], (p*x[2], x[2]))

async def echo(websocket, path):
    async for message in websocket:
        if(message!="hello2"):
            
            print("22222222222222222222222222222222222")
            print(message)
            await websocket.send("Start generating stream ...")
            comments_provider = CommentsProvider(message, 50)
            comments_provider.start()

        # for i in range(5):
        #     await websocket.send("[1,2,3]")
        #     time.sleep(2)
        #     await websocket.send("123")
        #sc = SparkContext()
        #ssc = StreamingContext(sc, 1)
        # lines = ssc.socketTextStream("localhost", 9092)
        # words = lines.flatMap(lambda line: line.split(" "))
        # # data = lines.flatMap(lambda line: line.split("|||"))

        # # comments = data.map(lambda x: filterComments(x))
        # # validComments = comments.filter(lambda x: x[2] != -1)
        # # commentsPolar = validComments.map(lambda x: getPolar(x))
        # # result = commentsPolar.reduceByKey(lambda x, y: (x[0]+y[0], x[1]+y[1]))
        
        # #pairs = words.map(lambda word: (word, 1))
        # #wordCounts = pairs.reduceByKey(lambda x, y: x + y)

        # # Print the first ten elements of each RDD generated in this DStream to the console
        # # print("1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
        # # wordCounts.pprint()

        # words.foreachRDD(print)
        # ssc.start()             # Start the computation
        # ssc.awaitTermination()
        #sc.setLogLevel('WARN')

        #ssc = StreamingContext(sc, 5)

        #kvs = KafkaUtils.createDirectStream(ssc, ['test'], {'bootstrap.servers':'localhost:9092'})
        #kvs = KafkaUtils.createDirectStream(ssc, ['test'], {"metadata.broker.list": "localhost:9092"})
        



        # kvs.pprint()

        # ssc.start()
        # ssc.awaitTermination()


asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 2055))
asyncio.get_event_loop().run_forever()



