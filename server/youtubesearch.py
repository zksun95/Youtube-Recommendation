from googleapiclient.discovery import build


class YouTubeSearch:
    '''   
        Assert:
            ys=youtubesearch('API_KEY.txt')
            
        Get video response:
            vresponse=ys.videosearch(q='JOJO',maxResults=25)
            
        Get next page:
            vresponse_next=ys.videosearch(q='JOJO',maxResults=25,pageToken=vresponse['nextPageToken'])
            
        Get one page of comments:
            videoId=vresponse['items'][0]['id']['videoId']
            cresponse=ys.commentsearh(videoId=videoId,maxResults=25)
            
        Get comment list of one page of comments:
            cslist=ys.get_cslist(cresponse)
            
        Get all comments list:
            cslist=ys.get_all_comments(videoId=videoId,maxResults=50(,maxComments=1000))
            
        Get information about a specific video:
            vi=ys.videoinfo(id=videoId)
    '''
    def __init__(self,SECRET_FILE_NAME='API_KEY.txt'):   
        self.SECRET_FILE_NAME = SECRET_FILE_NAME
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
        self.API_SERVICE_NAME = 'youtube'
        self.API_VERSION = 'v3'
        self.service=self.get_authenticated_service()
    
    def get_authenticated_service(self):
        f=open(self.SECRET_FILE_NAME,'r')
        API=f.read()
        f.close()
        return build(self.API_SERVICE_NAME, self.API_VERSION, developerKey=API)

    # Remove keyword arguments that are not set
    def remove_empty_kwargs(self,**kwargs):
        good_kwargs = {}
        if kwargs is not None:
            for key, value in kwargs.items():
                if value:
                    good_kwargs[key] = value
        return good_kwargs
    
    def videosearch(self,**kwargs):
        '''
            Arguments:
                q : keyword
                maxResults : max number of return results
                nextPageToken : need when request the next page; also need the same q
        '''
        kwargs['part']='snippet'
        kwargs['type']='video'
        kwargs= self.remove_empty_kwargs(**kwargs)
        response=self.service.search().list(**kwargs).execute()
        return response
    
    def videoinfo(self,**kwargs):
        '''
            Arguments:
                id : videoId
        '''
        kwargs['part']='snippet,contentDetails,statistics'
        kwargs = self.remove_empty_kwargs(**kwargs)
        response = self.service.videos().list(**kwargs).execute()
        return response

    def commentsearch(self,**kwargs):
        '''
            Arguments:
                videoId : the videoId
                maxResults : max number of return results
                nextPageToken : need when request the next page; also need the same videoId.
        '''
        kwargs['part']='snippet,replies'
        kwargs= self.remove_empty_kwargs(**kwargs)
        response=self.service.commentThreads().list(**kwargs).execute()
        return response
    
    def get_cslist(self,cs):
        '''
            Input a commentresponse instance.
            Return a list contains comment text and likecount.
        '''
        cslist=[]
        for comment in cs['items']:
            info=comment['snippet']['topLevelComment']['snippet']
            cslist.append({'text':info['textOriginal'],'count':info['likeCount']+1})
        return cslist
    
    def get_all_comment(self,**kwargs):
        '''
            Get all comments of a video.
            Return a comment list.
        '''
        maxComments=0
        if 'maxComments' in kwargs:
            maxComments=kwargs['maxComments']
            kwargs.pop('maxComments')
        response=self.commentsearch(**kwargs)
        cslist=self.get_cslist(response)
        while ('nextPageToken' in response) and (maxComments==0 or len(cslist)<maxComments):
            kwargs['pageToken']=response['nextPageToken']
            response=self.commentsearch(**kwargs)
            cslist+=self.get_cslist(response)
        return cslist