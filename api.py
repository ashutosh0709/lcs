from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

#################################################################################################################
from flask import request
import os
from time import sleep
from datetime import datetime

##################################################################
def convertFileToVar(article_filename):

    file = open(article_filename)                                                                     
    var = file.read()                                                                                  
    file.close()
    return var
###################################################################################################
# threading to implement refresing of newly crawled articles to download every5 minutes.

def refreshDownloadOfNewlyCrawledArticles():
    
    from main_pipe import refreshDownloadForNewArticles

    while(True):
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        refreshDownloadForNewArticles()
        print(current_time)
        sleep(60 ) # 1 minute refresh rate.
        

###############################################

from threading import Thread
x = Thread(target=refreshDownloadOfNewlyCrawledArticles) # starting the refresher thread.
x.start()


###################################################################################################
class LoacalCachingSerivce(Resource):
    def get(self):
        filename = request.form['text']
        print(filename)
        article = ""

        curr_path = os.getcwd()
        src_path = os.getcwd()
        new_path = os.path.join(src_path ,'downloaded_articles')
        os.chdir(new_path)

        try:
                article = str(convertFileToVar(filename))
        except: 
                article = ""

        os.chdir(curr_path)

        return {'filename': filename , 'article': article}

################################################################################################################

api.add_resource(LoacalCachingSerivce, '/lcs')

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8003)

