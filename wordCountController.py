from wordCountModel import masterWordCountModel
from wordCountView import masterWordCountView
from bs4 import BeautifulSoup
import re
import datetime



class masterWordCountController():    #Responsible for passing input to model and writing output from view to file

    __model=None
    __view=None
    __statFile=None

    def __init__(self):    #create model, view objects, pass model to view 
        self.__model=masterWordCountModel()
        self.__view=masterWordCountView(self.__model)

    def commonInit(self):    #initialize keys and dictionaries for article, subject, and global levels
        self.__model.setIndividualLabelKey("individual word count")
        self.__model.setAggregateLabelKey("total word count")
        self.__model.setUniqueLabelKey("unique word count")
        self.__model.setGlobalLabelKey("global data")
        self.__model.setSubjectLabelKey("subject data")

    def setCurrentSubject(self, currentSubject):    #Set subject to subject name of file being scanned
        self.__model.setSubjectValueLabelKey(currentSubject)

    def getWordCount(self, paragraphString, subjectValue):    #count the words in each paragraph string passed
        try:
            if paragraphString != None:
                #Updated the below to more accurately capture acronyms. Also removed error where words connected with ellipses were captured.
                preCountableParagraph = re.findall("((?:\w\.){2,})|(\w+[\u2019\'\.]?\w+)",paragraphString)
                #countableParagraph = [x for x in preCountableParagraph if x not in ["a","an","the","A","An","The"]]
                
                try:
                    for wordGroup in preCountableParagraph:
                        print(wordGroup)
                        for wordItem in wordGroup:
                            if wordItem != '' and wordItem not in ["a","an","the","A","An","The"]:
                                self.__model.addTermToWordCountDictionaries(wordItem.upper(), subjectValue)
                                self.__model.incrementGlobalStatDictionaryAggregateWordDataMember()
                                self.__model.incrementGlobalSubjectValueDictionaryAggregateWordDataMember(subjectValue)
                                self.__model.incrementTitleAggregateWordDataMember()
                except Exception as ex:
                    print("Paragraph parsing failed\n")
                    print("Paragraph object missing data or contains unexpected data (such as an unclosed or unexpected HTML tag)")
                    print("Failed in getWordCount")
                    print(ex)
        except:
            print("Error in regex scan or list comprehension of paragraph object")
            print("Failed in getWordCount")

    def setStatFilename(self,filename):    #Set the file that is being worked with
        self.__statFile=filename

    def processTitle(self, jsonObject, titleList):    #Set the article title that is currently being worked with, word statistic data will initially be bound to this key
        try:
            titleKey=jsonObject.get("title")
            titleList.append(titleKey)
            self.__model.setTitleKey(titleKey)
        except:
            print("title key irretrievable or malformed")
            print("Failed in processTitle")

    def setDateEntry(self, jsonObject):    #Get the date that the currently scanned article was written
        try:
            dateStringHolder = jsonObject.get("articleDate")
        
            dateStringMatch = re.search("(([jJ]anuary)|([fF]ebruary)|([mM]arch)|([aA]pril)|([mM]ay)|([jJ]une)|([jJ]uly)|([aA]ugust)|([sS]eptember)|([oO]ctober)|([nN]ovember)|([dD]ecember))\s[0-9]{1,2},\s[0-9]{4}", dateStringHolder)
            dateString=dateStringMatch[0]
            if dateString != None:
                self.__model.setCurrentArticleDateString(dateString)
                self.__model.sortDate()
        except:
            print("articleDate key irretrievable or malformed")
            print("Failed in setDateEntry")

    def processArticleParagraphs(self, jsonObject, subjectValue):    #Articles are composed of paragraphs, this feeds individual paragraphs to the word count function getWordCount by using BeautifulSoup to break down the tags using xml parsing
        try:
            bodyList = jsonObject.get("articleBodyText")
            for p in bodyList:
                paragraph = BeautifulSoup(p, features="lxml")
                self.getWordCount(paragraph.string, subjectValue)
        except:
            print("articleBodyText key irretrievable or malformed")
            print("Failed in processArticleParagraphs")

    def prepareForArticleWordCount(self):    #Setup dictionary to collect article word statistic data
        try:
            self.__model.setArticleCollectionDictionaryTitleMemberDictionary()
        except:
            print("Failed to set ArticleCollectionDictionaryTitleMemberDictionary")
            print("Failed in prepareForArticleWordCount")

    def prepareGlobalSubjectStatDictionary(self):    #Setup dictionary to collect word statistics for entire news source in global dictionary 
        self.__model.setGlobalCollectionDictionaryGlobalStatDictionary()

    def prepareGlobalSubjectValueDictionary(self):    #Setup dictionary that holds subjects for entire news source in global dictionary
        self.__model.setGlobalCollectionDictionarySubjectDataMemberDictionary()

    def prepareSubjectValueDictionaryDataMemberDictionary(self, subjectValue):    #Setup dictionary for specific subject in global subject value dictionary
        self.__model.setSubjectDictionaryGeneralSubjectValueDataMemberDictionary(subjectValue)

    def isArticleNonAd(self):    #Gets result of ad test from view
        return self.__view.isArticleNonAd()

    def sortArticleWordDictionary(self):    #Sorts word keys in article dictionary by value size - in laymans terms, orders the word count from highest word count to lowest
        self.__model.sortWordDictionary()

    def sortGlobalSubjectWordDictionary(self):    #Sorts word keys in subject dictionary by value size - in laymans terms, orders the word count from highest word count to lowest
        self.__model.sortGlobalStatWordDictionary()

    def sortGlobalSubjectValueWordDictionary(self, subjectValue): #Sorts word keys in global subject dictionary by value size - in laymans terms, orders the word count from highest word count to lowest
        self.__model.sortGlobalSubjectValueWordDictionary(subjectValue)

    def writeMasterReportHeader(self, newsSource):    #Writes formatted report header to file
        nowDate=datetime.datetime.now()
        nowDateString=nowDate.strftime("%B %d, %Y")

        try:
            self.__statFile.write("Lexical Frequency Report \n")
            self.__statFile.write("Word Frequency Listings By Subject, Article\n")
            self.__statFile.write("Raw News Source: " + newsSource + "\n")
            self.__statFile.write("Date Written: " + nowDateString + "\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeMasterReportHeader")

    def writeSubjectDataHeader(self, subject):    #Writes subject header for a given subject
        try:
            self.__statFile.write("Begin Statistical Data For Subject " + subject + "\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeSubjectDataHeader")

    def writeArticleDataHeader(self):
        try:
            self.__statFile.write("Word Frequency By Article\n")
            self.__statFile.write("Source: Reuters\n")
            self.__statFile.write("Beta\n")
            self.__statFile.write("\n")
            self.__statFile.write("\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeArticleDataHeader")

    def writeArticleSegmentHeader(self):    #Writes header for article section in a given subject
        try:
            self.__statFile.write("Article Listings:\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeArticleSegmentHeader")

    def writeSourceDataHeader(self):    
        try:
            self.__statFile.write("Global Article Word Analysis\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeSourceDataHeader")

    def writeGlobalDataSummaryHeader(self):    #Writes header for global summary of all data
        try:
            self.__statFile.write("Global Article Word Analysis - all subjects\n\n")
            self.__statFile.write("First Article Date: " + self.__view.getEarliestDateString() + "\n")
            self.__statFile.write("Last Article Date: " + self.__view.getLatestDateString() + "\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeGlobalDataSummaryHeader")

    def writeGlobalBySubjectValueDataHeader(self, subjectValue):    #Writes header signifying beginning of data output for given subject
        try:
            self.__statFile.write("Global Article Word Analysis - for subject " + subjectValue + "\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeGlobalBySubjectValueDataHeader")

    def writeProcessedArticleData(self, articleTitle):    #Write formatted data for a given article
        self.__model.setTitleKey(articleTitle)
        self.__statFile.write(articleTitle + "\n")
        self.__statFile.write("\t" + "total word count: " )
        self.__statFile.write(self.__view.getArticleTotalWordCount())
        self.__statFile.write("\t" + "unique word count: " )
        self.__statFile.write(self.__view.getArticleUniqueWordCount())
        self.__statFile.write("\t" + "individual word counts: " + "\n")
        for entry in self.__view.getArticleIndividualWordCounts():
            self.__statFile.write(entry)
        self.__statFile.write("\n\n")

    def writeProcessedGlobalData(self):    #Write formatted data for all data in news source
        try:
            self.__statFile.write("\t" + "Global Total Word Count - all subjects: ")
            self.__statFile.write(self.__view.getSubjectTotalWordCount())
            self.__statFile.write("\t" + "Global Unique Word Count - all subjects: ")
            self.__statFile.write(self.__view.getSubjectUniqueWordCount())
            self.__statFile.write("\t" + "Global Individual Word Count - all subjects: " + "\n")
            for entry in self.__view.getSubjectIndividualWordCount():
                self.__statFile.write(entry)
            self.__statFile.write("\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeProcessedGlobalData")

    def writeProcessedGlobalBySubjectValueData(self, subjectValue):    #Writes header for summary of data in given subject
        try:
            self.__statFile.write("\t" + "Global Total Word Count - for subject " + subjectValue + ": ")
            self.__statFile.write(self.__view.getSubjectValueTotalWordCount(subjectValue))
            self.__statFile.write("\t" + "Global Unique Word Count - for subject " + subjectValue + ": ")
            self.__statFile.write(self.__view.getSubjectValueUniqueWordCount(subjectValue))
            self.__statFile.write("\t" + "Global Individual Word Counts - for subject " + subjectValue + ": " + "\n")
            for entry in self.__view.getSubjectValueIndividualWordCount(subjectValue):
                self.__statFile.write(entry)
            self.__statFile.write("\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeProcessedGlobalBySubjectValueData")

    def writeHeaderRule(self):    #Writes header rule for entire report
        try:
            self.__statFile.write(("=" * 79) + "\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeHeaderRule")

    def writeFinalCloserRule(self):    #Writes rule lines used in final closer section (generally the final news source word statistic summary)
        try:
            self.__statFile.write(("=" * 79) + "\n")
            self.__statFile.write(("=" * 79) + "\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeFinalCloserRule")

    def writeArticleTerminatorRule(self):    #Writes rule lines signifying end of individual article
        try:
            self.__statFile.write(("-" * 79) + "\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeArticleTerminatorRule")

    def writeSubjectTerminatorRule(self):    #Writes rule line signifying end of subject
        try:
            self.__statFile.write(("*" * 79) + "\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeSubjectTerminatorRule")

    def writeSubjectRule(self):    #Writes rule lines signifying beginning of subject entry
        try:
            self.__statFile.write(("|" * 79) + "\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeSubjectRule")

    def writeEOFLine(self):    #Writes end of file terminator string
        try:
            self.__statFile.write("EndOfFile")
        except:
            print("Failed to write to report file")
            print("Failed in writeEOFLine")