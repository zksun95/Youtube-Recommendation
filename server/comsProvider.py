from youtubeScraper import YoutubeScraper
from kafka import KafkaProducer


class CommentsProvider:
    """
    Uses YoutubeScraper and provides comments using a KafkaProducer
    """

    def __init__(self, search_q, maxResults):
        self.youtube = YoutubeScraper(search_q, self.__on_comment, maxResults)
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        self.producer.send('test', b'some_message_bytes')

    def __on_comment(self, video_id, comment, count):
        self.producer.send("test", bytes('{}||{}||{}'.format(video_id, comment, count), 'utf-8'))
        #print(video_id, comment)
        print(video_id)

    def start(self):
        
        self.youtube.fetch_videos()
        print('Video Ids:', self.youtube.videos_ids)
        self.youtube.run()

#comments_provider = CommentsProvider('Movie Trailer', 50)
#comments_provider.start()