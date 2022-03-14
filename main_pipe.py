from dac import connectToS3 , downloadCrawledFileFromS3 , connecttoDb , downloadNewArticles
########################################################################################################################################
########################################################################################################################################
# pipeline:
def refreshDownloadForNewArticles():
    bucketname , s3 = connectToS3()
    articles_Collection , db = connecttoDb()
    downloadNewArticles(articles_Collection , db , bucketname , s3)




