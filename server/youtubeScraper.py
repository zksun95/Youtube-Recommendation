import requests
from threading import Thread, Event
from youtubesearch import YouTubeSearch


class YoutubeScraper(Thread):
    """
    Performs a Youtube Search, selects N videos (ordered by upload date) and monitors their comments.
    Previous comments will also be extracted.
    """

    SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
    COMMENT_THREADS_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'

    def __init__(self, search_q, callback, maxResults):
        self.ys=YouTubeSearch()
        #q='JOJO\'s bizarre adventure'
        #vs=ys.videosearch(q=q,maxResults=maxResults)
        #videoId=vs['items'][i]['id']['videoId']
        self.stop_event = Event()
        self.maxResults = maxResults
        Thread.__init__(self)
        #self.api_key = api_key
        self.search_q = search_q
        #self.n_vids = 50 if n_vids > 50 else n_vids
        self.callback = callback
        #self.regionCode = region_code
        #self.interval = interval
        self.videos_ids = None
        #self.last_comment_per_video = None


    def fetch_videos(self):
        """
        Performs the Youtube Search and selects the top newest {n_vids} videos.
        """
        # params = self.__generate_search_params()
        # json_result = requests.get(self.SEARCH_URL, params).json()

        # if not json_result['items']:
        #     raise ValueError(json_result)
        
        # self.videos_ids = [item['id']['videoId'] for item in json_result['items']]
        # self.last_comment_per_video = {}
        vs = self.ys.videosearch(q=self.search_q,maxResults=self.maxResults)
        self.videos_ids = [item['id']['videoId'] for item in vs['items']]
        #self.last_comment_per_video = {}
        #videoId=vs['items'][i]['id']['videoId']

    def __extract_comments(self, video_id, page_token=None):
        """
        Performs the comment threads request and calls callback for each comment.
        Returns the json_result.
        """
        try:
            cslist = self.ys.get_all_comment(videoId=video_id, maxResults=100, maxComments=2000)
        except:
            return None

        
        # params = self.__generate_comment_threads_params(page_token)
        # params['videoId'] = video_id
        # json_result = requests.get(self.COMMENT_THREADS_URL, params).json()

        
        #if 'text' not in cslist or len(cslist) == 0:
        #    return None

        for comment in cslist:
            # In case we reached the last comment registred
            
            # last_comment_id = self.last_comment_per_video[video_id] if video_id in self.last_comment_per_video else None
            # if last_comment_id is not None and item['id'] == last_comment_id:
            #     break

            # comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
            self.callback(video_id, comment['text'], comment['count'])

        return cslist


    def run(self):
        """
        Starts the monitoring process with the given interval.
        The callback method is called everytime a new comment is retrieved
        """
        print('Start generating comments...')
        if self.videos_ids is None:
            raise ValueError('No video ids available, call fetch_videos first.')

        for video_id in self.videos_ids:
            
            print(video_id)

            json_result = self.__extract_comments(video_id)

            if json_result is None:
                #self.last_comment_per_video[video_id] = None
                print('{} has no comments.'.format(video_id))
                continue

            #self.last_comment_per_video[video_id] = json_result['items'][0]['id']

            # Check if there are next pages
            # while 'nextPageToken' in json_result:
            #     json_result = self.__extract_comments(video_id, json_result['nextPageToken'])

        # Start monitoring
        print('End')
        # while not self.stop_event.wait(self.interval):
        #     self.__check_for_new_comments()

    def stop(self):
        """
        Sets the stop_event
        """
        self.stop_event.set()
