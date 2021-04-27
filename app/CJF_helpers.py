

import pandas as pd

from re import sub
from datetime import datetime
from decimal import Decimal

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tweepy

#Graph 1
# def fixer1(x):
#     try:
#         return Decimal(sub(r'[^\d.]', '', x))
#     except:
#         return 0

# def graph1(dF):
# 	dF_Revenue = dF[['Amount','CloseDate']].copy()

# 	dF_Revenue['Amount']= dF_Revenue['Amount'].apply(fixer1)
# 	Results = dF_Revenue[['Amount','CloseDate']].groupby(['CloseDate']).sum()
# 	return Results




# Revenue
def fixer(x):
    try:
        return float(Decimal(sub(r'[^\d.]', '', x)))
    except:
        return float(0)
    
    
def dateTrunc(x):
    x = str(x)
    dateObj = datetime.strptime(x, "%m/%d/%Y")
    dateTrunc = dateObj.replace(day=1)
    return dateTrunc, dateObj.strftime("%B"),  dateObj.strftime("%Y")


def graph1(dF):
	dF_Revenue = dF[['Amount','CloseDate']].copy()
	dF_Revenue = dF_Revenue.dropna()


	dF_Revenue['Amount']= dF_Revenue['Amount'].apply(fixer)
	dF_Revenue['CloseDate'], dF_Revenue['month'], dF_Revenue['year'] = zip(*dF_Revenue['CloseDate'].apply(dateTrunc))

	dF_Revenue = dF_Revenue[dF_Revenue['CloseDate']>='2020-01-01']

	Results = dF_Revenue[['Amount','month','year']].groupby(['month','year']).sum()#.unstack('year')
	Results = Results.reset_index()

	fullDictList = []
	for y in ('January','February','March','April','May','June','July','August','September','November','December'):
	    dictResult = {}
	    for x in ('2020','2021'):
	        dictResult['Month'] = y
	        try:
	            dictResult[x] = round(Results[(Results['month'] == y) & (Results['year'] == x)]['Amount'].values[0])
	        except:
	            pass
	        
	    fullDictList.append(dictResult)

	return(fullDictList)






def graph2(dF):
	dF_Revenue = dF[['Amount','CloseDate']].copy()
	dF_Revenue = dF_Revenue.dropna()


	dF_Revenue['Amount']= dF_Revenue['Amount'].apply(fixer)
	dF_Revenue['CloseDate'], dF_Revenue['month'], dF_Revenue['year'] = zip(*dF_Revenue['CloseDate'].apply(dateTrunc))

	dF_Revenue = dF_Revenue[dF_Revenue['CloseDate']>='2020-01-01']

	Results = dF_Revenue[['Amount','month','year']].groupby(['month','year']).mean()#.unstack('year')
	Results = Results.reset_index()

	fullDictList = []
	for y in ('January','February','March','April','May','June','July','August','September','November','December'):
	    dictResult = {}
	    for x in ('2020','2021'):
	        dictResult['Month'] = y
	        try:
	            dictResult[x] = round(Results[(Results['month'] == y) & (Results['year'] == x)]['Amount'].values[0],2)
	        except:
	            pass
	        
	    fullDictList.append(dictResult)

	return(fullDictList)









def dateTruncG3(x):
    x = str(x)
    dateObj = datetime.strptime(x, "%m/%d/%Y")
    dateTrunc = dateObj.replace(month=1,day=1).strftime('%Y-%m-%d')
    return dateTrunc
    
    

def graph3(dF):
    dF_Revenue = dF[['Amount','CloseDate']].copy()
    dF_Revenue = dF_Revenue.dropna()

    dF_Revenue['Amount']= dF_Revenue['Amount'].apply(fixer)
    dF_Revenue['CloseDate'] = dF_Revenue['CloseDate'].apply(dateTruncG3)

    Results = dF_Revenue[['Amount','CloseDate']].groupby(['CloseDate']).count()
    Results = Results.reset_index()
    #
    Results['AvgThreeYear'] = round(Results.iloc[:,1].rolling(window=3).mean(),)
    Results = Results[Results['CloseDate']>='2015-01-01']
    Results['Year'] = Results['CloseDate']
    Results = Results[['Year','Amount','AvgThreeYear']]
    #Results['CloseDate'] = Results['CloseDate']

    return Results.to_dict(orient='records')




def graph4(dF):
	dFg4 = dF.copy()
	dF_Frequency = dFg4[['NSFID','Amount']].groupby(['NSFID']).size().reset_index()
	dF_Frequency.columns = ['id','count']
	dF_Frequency = dF_Frequency.groupby(['count']).size().reset_index()
	dF_Frequency.columns = ['NumberDonations','Occurences']
	return dF_Frequency.to_dict(orient='records')











############# TWITTER STUFF ##########

def twitter():

	#### Setup Fields ####
	# Authenticate to Twitter
	auth = tweepy.OAuthHandler("L5sWNg9PIpp3XFmjZf4hPFzQN", "VifEmM54l0x54xezPLobqtTYpuOxHaQJOWzPNFQVdl07t9CUJv")
	auth.set_access_token("1381841810985734147-8vLsFYBcx4cJLZwBsuYUluNVqKc2mb", "A56jfdV3IyVNDi2LMhr91gudbCgOAFgejFsk9PU3B9s5j")

	# Grab sentiment model
	SentimementModel = SentimentIntensityAnalyzer()

	# Create API object
	api = tweepy.API(auth, wait_on_rate_limit=True,  wait_on_rate_limit_notify=True)

	# twitter handle to check
	screen_name = "NavySEALfnd"

	# number of statuses to be fetched
	count = 10

	#build list of comments
	comments = []

	#build list of sentimentsGraphData
	sentiments = []

	#build list of favorites
	favorites = []

	#build list of retweets
	retweets = []

	#build tweetNumber
	x = 0

	#initiate object to return
	contextObj = {}

	#### Do Data Stuff ####
	# fetching the statuses
	statuses = api.user_timeline(screen_name, count = count,include_entities=True)
	print('checker')

	# printing the statuses
	for status in statuses:
	   # print(status.text)

	    tweetText = sub(r"http\S+", "", status.text)
	    
	    comments.append(tweetText)
	    favorites.append(status.favorite_count)
	    retweets.append(status.retweet_count)


	    
	    sentimentDict = {}
	    sentiment = (SentimementModel.polarity_scores(status.text)['compound']+1)/2
	    sentimentDict['TweetNumber'] = str(x)
	    sentimentDict['SentimentScore'] = round(sentiment,2)
	    sentiments.append(sentimentDict)
	    x+=1





	print('checker 2')
	contextObj['latestTweet'] = comments[0]
	contextObj['latestFavorites'] = favorites[0] # used
	contextObj['latestRetweet'] = retweets[0]
	#contextObj['maxFavorites'] = max(favorites)
	contextObj['percentChange'] = round(favorites[0]/(sum(favorites)-favorites[0])*100) #used

	contextObj['sentimentData'] = sentiments
	return (contextObj)