import asyncio
import websockets
import time
import json
import os

from sentiment import CommentSentiment
from youtubesearch import YouTubeSearch

async def echo(websocket, path):
    async for message in websocket:
        print(message)
        if message=='start':
            path_to_watch = "./data"
            before = dict ([(f, None) for f in os.listdir (path_to_watch)])
            dic={'videoId':'','polarity':0.0,'count':0}
            DIC=[]
        else:
            after = dict ([(f, None) for f in os.listdir (path_to_watch)])
            added = [f for f in after if not f in before]
            for text in added[:-1]:
                path_new=path_to_watch+'/'+text
                print(path_new)
                new_file=dict ([(f, None) for f in os.listdir (path_new)])
                while ('part-00007' not in new_file):
                    break
                for i in range(8):
                    try:
                        f=open(path_new+"/part-0000"+str(i),'r')
                        fdata=f.read()
                        f.close()
                    except:
                        continue
                    if fdata != '':
                        sentences=fdata.split('\n')
                        for sentence in sentences[:-1]:
                            sentence=sentence[1:-1]
                            data=sentence.split(', ')
                            if data[0][1:-1] not in DIC:
                                DIC.append(data[0][1:-1])
                                if dic['videoId'] != '':
                                    ys=YouTubeSearch()
                                    vi=ys.videoinfo(id = dic['videoId'])
                                    answer={'polarity':dic['polarity']/(dic['count']+1)}
                                    answer['url']='https://www.youtube.com/watch?v='+dic['videoId']
                                    answer['title']=vi['items'][0]['snippet']['title']
                                    answer['publishedAt']=vi['items'][0]['snippet']['publishedAt']
                                    answer['thumbnails']=vi['items'][0]['snippet']['thumbnails']['medium']['url']
                                    if 'likeCount' in vi['items'][0]['statistics']:
                                        answer['like']=vi['items'][0]['statistics']['likeCount']
                                        answer['dislike']=vi['items'][0]['statistics']['dislikeCount']
                                    else:
                                        continue
                                    json_answer = json.dumps(answer)
                                    type(json_answer)
                                    print('111')
                                    await websocket.send(json_answer)
                                dic['videoId']=data[0][1:-1]
                                dic['polarity']=float(data[1])
                                dic['count']=int(data[2])
                            else:
                                dic['polarity']+=float(data[1])
                                dic['count']+=int(data[2])
                before[text]=None
                print(path_new)



asyncio.get_event_loop().run_until_complete(websockets.serve(echo, '127.0.0.1', 5678))
asyncio.get_event_loop().run_forever()

