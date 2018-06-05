import asyncio
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import websockets
import time
import json

from sentiment import CommentSentiment
from youtubesearch import YouTubeSearch


sc = SparkContext()
ssc = StreamingContext(sc, 5)
# lines = ssc.socketTextStream("localhost", 9092)

# words = lines.flatMap(lambda line: line.split(" "))
# pairs = words.map(lambda word: (word, 1))
# wordCounts = pairs.reduceByKey(lambda x, y: x + y)

# # Print the first ten elements of each RDD generated in this DStream to the console
# # print("1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
# print("0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000: ")
# words.foreachRDD(lambda x: print(x))
# print("1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111: ")
# wordCounts.pprint()
# print("2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222: ")


# ssc.start()             # Start the computation
# ssc.awaitTermination()


#sc.setLogLevel('WARN')

#ssc = StreamingContext(sc, 5)

kvs = KafkaUtils.createDirectStream(ssc, ['test'], {'bootstrap.servers':'localhost:9092'})
#kvs = KafkaUtils.createDirectStream(ssc, ['test'], {"metadata.broker.list": "localhost:9092"})



kvs.pprint()

ssc.start()
ssc.awaitTermination()