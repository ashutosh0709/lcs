import os
############################################################################################################################3


def connectToS3():
    from dotenv import load_dotenv
    load_dotenv()
    import boto3

    region_name = os.getenv("region_name")
    service_name = os.getenv('service_name')
    aws_access_key_id = os.getenv('aws_access_key_id')
    aws_secret_access_key = os.getenv('aws_secret_access_key')
    bucketname = os.getenv('bucketname')


    s3 = boto3.client(
    service_name=service_name,
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
    )

    return bucketname , s3 

##################################################################################################################################

def downloadCrawledFileFromS3(filename , bucketname , s3):

    abs_file_path_s3 = "downloaded_articles/" + str(filename)
    print(abs_file_path_s3)

    curr_path = os.getcwd()
   # os.chdir("../")                     
    src_path = os.getcwd()
    new_path = os.path.join(src_path ,'downloaded_articles')
    os.chdir(new_path)

    s3.download_file(bucketname,abs_file_path_s3 , filename)
    print('True')

    os.chdir(curr_path)



###################################################################################################################################

def connecttoDb():
    # database connecions:

    arangodb_username = os.getenv("arangodb_username")
    arangodb_password = os.getenv('arangodb_password')
    database_name = os.getenv('database_name')
    keyword_url_collection = os.getenv('crawler_model_tracker')
    arangoURL = os.getenv('arangoURL')

    from pyArango.connection import Connection
    conn = Connection(arangoURL=arangoURL, username=arangodb_username, password=arangodb_password) # arangoURL=arangoURL , 
 
    try:
        db = conn.createDatabase(name=database_name) #handles creation of db
    except:
        db = conn[database_name]         # handles opening of created db
    print(db)

    try:
        articles_Collection = db.createCollection(name=keyword_url_collection) #creating a new collection on db = school
    except:
        articles_Collection = db[keyword_url_collection] #connecting if already exists.


    return articles_Collection , db
######################################################################################################################################
# THIS GOES OVER THE DATABASE AND DOWNLOADS NEW ARTICLES.

def downloadNewArticles(articles_Collection , db , bucketname , s3):
    aql = "FOR x IN crawler_model_tracker RETURN x"
    queryResult = db.AQLQuery(aql, rawResults=True, batchSize=100)
    for entry in queryResult: 
        if entry.get('locally_cached') == False:
            filename = entry.get('filename')
            downloadCrawledFileFromS3(filename , bucketname , s3)
            # change db-collection(locally_cached)-entry-to-true
            doc = articles_Collection[filename]
            doc['locally_cached'] = True
            doc.save()

########################################################################################################################################
