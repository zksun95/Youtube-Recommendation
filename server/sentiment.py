from textblob import TextBlob
import nltk

nltk.download('punkt')

true=True

class CommentSentiment:
    '''
        answer=CommentSentiment(commentlist).polarity()
        answer:{'polarity':float,'count':int}
    '''
    def __init__(self,cslist=[{'text':'','count':0}]):
        self.comments=cslist
        
    def preprocessing(self,sentence):
        try:
            sentence=sentence.translate(to='en')
        except:
            sentence=sentence
        sentence=TextBlob(' '.join(sentence.words.lemmatize()))
        return sentence
    
    def polarity(self):
        polar=0
        like=0
        for text in self.comments:
            sentence=TextBlob(text['text'])
            #sentence=self.preprocessing(sentence)
            p=sentence.polarity
            if p!=0:
                polar+=p*text['count']
                like+=text['count']
        if like==0:
            return {'polarity':0,'count':0}
        return {'polarity':polar/float(like),'count':like}