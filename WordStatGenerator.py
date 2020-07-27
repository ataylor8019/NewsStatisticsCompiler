#!/usr/bin/env python3

import datetime
import json
import jsonlines
import os
import os.path
import argparse
import re
from wordCountController import masterWordCountController

#Order of events:
# 1) set up initial parameters (news source, date)
# 2) Set up article list
# 3) Set up newsDataController internal bookkeeping and operations
# 4) Open record file for writing, pass file name and initial formatting data to controller
# 5) Begin loop through all files in directory - on match
#    a) Set up subject workspace in controller for current subject (specified by name of file found)
#    b) Begin reading through found file - for each line in found file
#        i) read json data in line, create article workspace, add to article workspace
#        ii) calculate statistic data for article
#        iii) sort statistic data
#    c) Sort the data gathered during subject file read
#    d) Write information gathered for subject, individual articles to the record file opened in 4
# 6) Sort global data gathered during all valid subject file reads gathered in 5
# 7) Write global headers and data
# 8) End program

def showHeader():
    print("Welcome to News Article Word Statistic Generator 1.2")
    print("Please choose one of the following options: \n")

def showMainProgramOptions():
    print("1) Scan News Articles")
    print("2) Exit \n\n")

def showNewsSourceHeader():
    print("Choose one of the following options below to scan their news source files:\n")

def showNewsSourceOptions():
    print("1) ap")
    print("2) npr")
    print("3) reuters")
    print("4) Return to main menu\n")

def mainMenuFilter():
    askAgain=True
    while (askAgain):
        rawUserInput=input("Execute Option: ")

        inputMatch=re.fullmatch("^[12]$", rawUserInput)

        if inputMatch:
            return int(rawUserInput)
        else:
            continue

def newsMenuFilter():
    askAgain=True
    
    while (askAgain):

        rawUserInput=input("Select news source:")

        inputMatch=re.fullmatch("^[1-4]$", rawUserInput)
        if inputMatch:
            return int(rawUserInput)
        else:
            continue

def directoryLoop(dataController, articleInfoListArgument):

# 5. Begin loop through all files in directory
    for fileItem in os.scandir(path="."):    # Begin main file read loop
        lock=re.match(rf"{newssource}.*?(([wW]orld)|([pP]olitics)|([tT]echnology)|([bB]usiness)).*?", fileItem.name)    #Find any file that has those subjects in the name
        
        if lock:    #Found a file that contains a desired subject. Begin reading that file
            currentFile=fileItem.name    #Get the filename
            currentSubject=lock.group(1)    #Get the subject
            
#      a) Set up subject workspace in controller for current subject (specified by name of file found)
            dataController.prepareSubjectValueDictionaryDataMemberDictionary(currentSubject)    #Add a dictionary entry for the current subject
            
#      b) Begin reading through found file - for each line in found file
            with jsonlines.open(currentFile,'r') as jsonFileToRead:    #Open the filename we stored, perform json reading operations using the work controller
                try:
                    jsonFileLoop(dataController, jsonFileToRead, articleInfoListArgument, currentSubject)
                except:
                    print("JSON object malformed or nonexistent")
                    print("Skipping file " + currentFile + ": file is not recognized as a JSON Lines file")
                    continue

#      c) Sort the data gathered during subject file read
                dataController.sortGlobalSubjectValueWordDictionary(currentSubject)    #Sort the data we have gotten out of the current subject file that is now in the current subject dictionary
                # ^^^ end of subject value entry, we can sort the words in the currentSubject value by occurrence ^^^

#      d) Write information gathered for subject, individual articles to the record file opened in 4
            subjectArticleWriteLoop(dataController, articleInfoListArgument, currentSubject)
                
            subjectSummaryWrite(dataController, currentSubject)
            articleInfoList.clear()    #clear all articles from the list, prepare for use for the next subject
            ## end writing individual subject values

# 6. Sort global data gathered during all valid subject file reads gathered in 5
    dataController.sortGlobalSubjectWordDictionary()    #Sort the data for all words gottten out of all the subject files, and stored in the global word count dictionary
    # ^^^ end of all subjects in news source, we can sort the words in all subjects in the news source by occurrence ^^^
    #newsDataController.writeSubjectRule()

# 7. Write global headers and data
    dataController.writeFinalCloserRule()
    dataController.writeGlobalDataSummaryHeader()
    dataController.writeProcessedGlobalData()
    dataController.writeFinalCloserRule()
    dataController.writeEOFLine()

    print("News data scan and stat logging complete\n")






def jsonFileLoop(dataController, jsonFileToRead, articleInfoListArgument, currentSubjectArgument):
    for jsonObject in jsonFileToRead:
#       i) read json data in line, create article workspace, add to article workspace
        dataController.processTitle(jsonObject, articleInfoListArgument)
                        
        if not dataController.isArticleNonAd():
                continue
        dataController.prepareForArticleWordCount()
        dataController.setDateEntry(jsonObject)
#       ii) calculate statistic data for article
        dataController.processArticleParagraphs(jsonObject, currentSubjectArgument)
#        iii) sort statistic data
        dataController.sortArticleWordDictionary()


def subjectArticleWriteLoop(dataController, articleInfoListArgument, currentSubjectArgument):
#d) Write information gathered for subject, individual articles to the record file opened in 4
    dataController.writeSubjectDataHeader(currentSubjectArgument)
    dataController.writeSubjectRule()
    
    dataController.writeArticleSegmentHeader()
    firstTime=True 
    for entry in articleInfoListArgument:    #Begin writing article data to the file
        if entry==None:
            continue
        if not firstTime:
            dataController.writeArticleTerminatorRule()
        firstTime=False
        dataController.writeProcessedArticleData(entry)

def subjectSummaryWrite(dataController, currentSubjectArgument):
    dataController.writeSubjectTerminatorRule()
    ##  write subject values here (remember to add subject entry)
    dataController.writeGlobalBySubjectValueDataHeader(currentSubjectArgument)    #Write Global subject value information to the file
    dataController.writeProcessedGlobalBySubjectValueData(currentSubjectArgument)
    dataController.writeSubjectTerminatorRule()




# 1. Set up initial parameters




processParser=argparse.ArgumentParser()
processParser.add_argument("--newssource")
inputArguments=processParser.parse_args()
newssource=inputArguments.newssource

#Setup menu loop
loopMainMenu=True



#if no argument has been passed to the variable "newssource", begin menu routine to get the variable
if newssource == None:

    while (loopMainMenu):

        showHeader()
        showMainProgramOptions()
        initialMenuEntry=mainMenuFilter()
        
        if (initialMenuEntry==2):
            os._exit(0)
        
        showNewsSourceHeader()
        showNewsSourceOptions()
        newsAction=newsMenuFilter()
        
        if (newsAction==1):
            newssource = "ap"
        elif (newsAction==2):
            newssource = "npr"
        elif (newsAction==3):
            newssource = "reuters"
        elif (newsAction==4):
            continue
        
        loopMainMenu=False
    # while (loopMainMenu):
        # loopMainMenu = showMainMenu()

nowDate=datetime.datetime.now()
nowDateString=nowDate.strftime("%m%d%Y_%H%M%S")


# 2. Set up articleInfoList article title tracking variable
articleInfoList=[]    #Setup article lists

# 3. Set up newsDataController internal bookkeeping and operations 
newsDataController=masterWordCountController()    #Setup work controller
newsDataController.commonInit()    #Initialize the controller
newsDataController.prepareGlobalSubjectStatDictionary()    #Setup subject dictionaries to hold word data
newsDataController.prepareGlobalSubjectValueDictionary()

# 4. Open record file for writing, pass file name and initial formatting data to controller
with open(newssource + '.' + nowDateString + '.stats.txt','w+', encoding="utf-8") as newsRecord:    #Open output file to hold result data
    newsDataController.setStatFilename(newsRecord)    #Pass the filename to the work controller
    newsDataController.writeMasterReportHeader(newssource)
    newsDataController.writeHeaderRule()

    directoryLoop(newsDataController, articleInfoList)





# # 5. Begin loop through all files in directory
    # for fileItem in os.scandir(path="."):    # Begin main file read loop
        # lock=re.match(rf"{newssource}.*?(([wW]orld)|([pP]olitics)|([tT]echnology)|([bB]usiness)).*?", fileItem.name)    #Find any file that has those subjects in the name
        
        # if lock:    #Found a file that contains a desired subject. Begin reading that file
            # currentFile=fileItem.name    #Get the filename
            # currentSubject=lock.group(1)    #Get the subject
            
# #      a) Set up subject workspace in controller for current subject (specified by name of file found)
            # newsDataController.prepareSubjectValueDictionaryDataMemberDictionary(currentSubject)    #Add a dictionary entry for the current subject
            
# #      b) Begin reading through found file - for each line in found file
            # with jsonlines.open(currentFile,'r') as jsonFileToRead:    #Open the filename we stored, perform json reading operations using the work controller
                # try:
                    # for jsonObject in jsonFileToRead:
# #          i) read json data in line, create article workspace, add to article workspace
                        # newsDataController.processTitle(jsonObject, articleInfoList)
                        
                        # if not newsDataController.isArticleNonAd():
                            # continue
                        # newsDataController.prepareForArticleWordCount()
                        # newsDataController.setDateEntry(jsonObject)
# #         ii) calculate statistic data for article
                        # newsDataController.processArticleParagraphs(jsonObject, currentSubject)
# #        iii) sort statistic data
                        # newsDataController.sortArticleWordDictionary()
                # except:
                    # print("JSON object malformed or nonexistent")
                    # print("Skipping file " + currentFile + ": file is not recognized as a JSON Lines file")
                    # continue

# #      c) Sort the data gathered during subject file read
                # newsDataController.sortGlobalSubjectValueWordDictionary(currentSubject)    #Sort the data we have gotten out of the current subject file that is now in the current subject dictionary
                # # ^^^ end of subject value entry, we can sort the words in the currentSubject value by occurrence ^^^

# #      d) Write information gathered for subject, individual articles to the record file opened in 4
            # newsDataController.writeSubjectDataHeader(currentSubject)
            # newsDataController.writeSubjectRule()

            # newsDataController.writeArticleSegmentHeader()
            # firstTime=True 
            # for entry in articleInfoList:    #Begin writing article data to the file
                # if entry==None:
                    # continue
                # if not firstTime:
                    # newsDataController.writeArticleTerminatorRule()
                # firstTime=False
                # newsDataController.writeProcessedArticleData(entry)
                
            # newsDataController.writeSubjectTerminatorRule()
            # ##  write subject values here (remember to add subject entry)
            # newsDataController.writeGlobalBySubjectValueDataHeader(currentSubject)    #Write Global subject value information to the file
            # newsDataController.writeProcessedGlobalBySubjectValueData(currentSubject)
            # newsDataController.writeSubjectTerminatorRule()
            # articleInfoList.clear()    #clear all articles from the list, prepare for use for the next subject
            # ## end writing individual subject values

# # 6. Sort global data gathered during all valid subject file reads gathered in 5
    # newsDataController.sortGlobalSubjectWordDictionary()    #Sort the data for all words gottten out of all the subject files, and stored in the global word count dictionary
    # # ^^^ end of all subjects in news source, we can sort the words in all subjects in the news source by occurrence ^^^
    # #newsDataController.writeSubjectRule()

# # 7. Write global headers and data
    # newsDataController.writeFinalCloserRule()
    # newsDataController.writeGlobalDataSummaryHeader()
    # newsDataController.writeProcessedGlobalData()
    # newsDataController.writeFinalCloserRule()
    # newsDataController.writeEOFLine()

    # print("News data scan and stat logging complete\n")

# 8. End program