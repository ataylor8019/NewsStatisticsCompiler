#wordCountView.py
#v1.0x
#
#By Allan Taylor
#
#03/2020
#
#


import wordCountModel
import datetime

class masterWordCountView():

    __model=None    #exists to hold model created by externally calling controller, so that large model objects are not continually being passed
                    #in getter/setter functions
    def __init__(self, model):
        self.__model = model

    def getArticleTotalWordCount(self):    #returns total word count of article, formats with line break for write to file
        return str(self.__model.returnGeneralWordDataDictionaryAggregateWordDataMember()) + "\n"

    def getArticleUniqueWordCount(self):    #returns unique word occurrence of article, formats with line break for write to file
        return str(self.__model.returnGeneralWordDataDictionaryUniqueWordDataMember()) + "\n"
    
    def getArticleIndividualWordCounts(self):    #gets dictionary holding word counts for every word in a given article, cycles through, returns key and value in dictionary (the word and how many times it occurs) formatted with tabs and a line break for write to file
        for entry in self.__model.returnGeneralWordDataDictionaryIndividualWordDataMemberDictionary().items():
            yield "\t\t" + str(entry[0]) + ": " + str(entry[1]) + "\n"

    def getEarliestDateString(self):    #gets earliest date of all articles read, formats as string for write to file
        returnDate=self.__model.getEarliestDate()
        return returnDate.strftime("%B %d, %Y")

    def getLatestDateString(self):    #gets latest date of all articles read, formats as string for write to file
        returnDate=self.__model.getLatestDate()
        return returnDate.strftime("%B %d, %Y")

    def getSubjectTotalWordCount(self):    #returns total word count of subject, formats with line break for write to file
        return str(self.__model.returnGlobalStatDictionaryAggregateWordDataMember()) + "\n"

    def getSubjectUniqueWordCount(self):    #returns unique word occurrence of subject, formats with line break for write to file
        return str(self.__model.returnGlobalStatDictionaryUniqueWordDataMember()) + "\n"

    def getSubjectIndividualWordCount(self):    #gets dictionary holding word counts for every word in a given subject, cycles through, returns key and value in dictionary (the word and how many times it occurs) formatted with tabs and a line break for write to file
        for entry in self.__model.returnGlobalStatDictionaryIndividualWordDataMemberDictionary().items():
            yield "\t\t" + str(entry[0]) + ": " + str(entry[1]) + "\n"

    def getSubjectValueTotalWordCount(self, subjectValue):    #returns total word count for entire news source
        return str(self.__model.returnGlobalSubjectValueDictionaryAggregateWordDataMember(subjectValue)) + "\n"

    def getSubjectValueUniqueWordCount(self, subjectValue):    #returns unique word count for entire news source
        return str(self.__model.returnGlobalSubjectValueDictionaryUniqueWordDataMember(subjectValue)) + "\n"

    def getSubjectValueIndividualWordCount(self, subjectValue):    #gets dictionary holding word counts for every word in a the entire news source, cycles through, returns key and value in dictionary (the word and how many times it occurs) formatted with tabs and a line break for write to file 
        for entry in self.__model.returnGlobalSubjectValueDictionaryIndividualWordDataMemberDictionary(subjectValue).items():
            yield "\t\t" + str(entry[0]) + ": " + str(entry[1]) + "\n"

    def isArticleNonAd(self):    #performs test to see if article is ad - ads don't have titles, if there's a title, this isn't an ad, if there isn't, then it is, boolean is set accordingly
        if self.__model.getTitleKey() != None: 
            return True

        return False