import wordCountModel
import datetime

class masterWordCountView():

    __model=None
    def __init__(self, model):
        self.__model = model

    def getArticleTotalWordCount(self):
        return str(self.__model.returnGeneralWordDataDictionaryAggregateWordDataMember()) + "\n"

    def getArticleUniqueWordCount(self):
        return str(self.__model.returnGeneralWordDataDictionaryUniqueWordDataMember()) + "\n"
    
    def getArticleIndividualWordCounts(self):
        for entry in self.__model.returnGeneralWordDataDictionaryIndividualWordDataMemberDictionary().items():
            yield "\t\t" + str(entry[0]) + ": " + str(entry[1]) + "\n"

    def getEarliestDateString(self):
        returnDate=self.__model.getEarliestDate()
        return returnDate.strftime("%B %d, %Y")

    def getLatestDateString(self):
        returnDate=self.__model.getLatestDate()
        return returnDate.strftime("%B %d, %Y")
    
    def getSourceTotalWordCount(self):
        return str(self.__model.returnGlobalGeneralWordDataDictionaryAggregateWordDataMember()) + "\n"

    def getSourceUniqueWordCount(self):
        return str(self.__model.returnGlobalGeneralWordDataDictionaryUniqueWordDataMember()) + "\n"
    
    def getSourceIndividualWordCounts(self):
        for entry in self.__model.returnGlobalIndividualWordDataMemberDictionary().items():
            yield "\t\t" + str(entry[0]) + ": " + str(entry[1]) + "\n"

    def getSubjectTotalWordCount(self):
        return str(self.__model.returnGlobalStatDictionaryAggregateWordDataMember()) + "\n"

    def getSubjectUniqueWordCount(self):
        return str(self.__model.returnGlobalStatDictionaryUniqueWordDataMember()) + "\n"

    def getSubjectIndividualWordCount(self):
        for entry in self.__model.returnGlobalStatDictionaryIndividualWordDataMemberDictionary().items():
            yield "\t\t" + str(entry[0]) + ": " + str(entry[1]) + "\n"

    def getSubjectValueTotalWordCount(self, subjectValue):
        return str(self.__model.returnGlobalSubjectValueDictionaryAggregateWordDataMember(subjectValue)) + "\n"

    def getSubjectValueUniqueWordCount(self, subjectValue):
        return str(self.__model.returnGlobalSubjectValueDictionaryUniqueWordDataMember(subjectValue)) + "\n"

    def getSubjectValueIndividualWordCount(self, subjectValue):
        for entry in self.__model.returnGlobalSubjectValueDictionaryIndividualWordDataMemberDictionary(subjectValue).items():
            yield "\t\t" + str(entry[0]) + ": " + str(entry[1]) + "\n"

    def isArticleNonAd(self):
        if self.__model.getTitleKey() != None: 
            return True

        return False