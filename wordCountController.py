from wordCountModel import masterWordCountModel
from wordCountView import masterWordCountView
from bs4 import BeautifulSoup
import re
import datetime



class masterWordCountController():

    __model=None
    __view=None
    __statFile=None

    def __init__(self):
        self.__model=masterWordCountModel()
        self.__view=masterWordCountView(self.__model)

    def commonInit(self):
        self.__model.setIndividualLabelKey("individual word count")
        self.__model.setAggregateLabelKey("total word count")
        self.__model.setUniqueLabelKey("unique word count")
        self.__model.setGlobalLabelKey("global data")
        self.__model.setSubjectLabelKey("subject data")
#        self.__model.setGlobalGeneralWordDataDictionary()

    def setCurrentSubject(self, currentSubject):
        self.__model.setSubjectValueLabelKey(currentSubject)

    def getWordCount(self, paragraphString, subjectValue):
        try:
            if paragraphString != None:
                preCountableParagraph = re.findall("([\w\d]+[\u2019\.]*?[\w\d]+|[\w\d]+)",paragraphString)
                countableParagraph = [x for x in preCountableParagraph if x not in ["a","an","the","A","An","The"]]
                
                try:
                    for wordItem in countableParagraph:
                        self.__model.addTermToWordCountDictionaries(wordItem.upper(), subjectValue)
                        self.__model.incrementGlobalStatDictionaryAggregateWordDataMember()
                        self.__model.incrementGlobalSubjectValueDictionaryAggregateWordDataMember(subjectValue)
                        self.__model.incrementTitleAggregateWordDataMember()
                except:
                    print("Paragraph parsing failed\n")
                    print("Paragraph object missing data or contains unexpected data (such as an unclosed or unexpected HTML tag)")
                    print("Failed in getWordCount")
        except:
            print("Error in regex scan or list comprehension of paragraph object")
            print("Failed in getWordCount")

    def setStatFilename(self,filename):
        self.__statFile=filename

    def processTitle(self, jsonObject, titleList):
        try:
            titleKey=jsonObject.get("title")
            titleList.append(titleKey)
            self.__model.setTitleKey(titleKey)
        except:
            print("title key irretrievable or malformed")
            print("Failed in processTitle")

    def setDateEntry(self, jsonObject):
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

    def processArticleParagraphs(self, jsonObject, subjectValue):
        try:
            bodyList = jsonObject.get("articleBodyText")
            for p in bodyList:
                paragraph = BeautifulSoup(p, features="lxml")
                self.getWordCount(paragraph.string, subjectValue)
        except:
            print("articleBodyText key irretrievable or malformed")
            print("Failed in processArticleParagraphs")

    def prepareForArticleWordCount(self):
        try:
            self.__model.setArticleCollectionDictionaryTitleMemberDictionary()
        except:
            print("Failed to set ArticleCollectionDictionaryTitleMemberDictionary")
            print("Failed in prepareForArticleWordCount")

    def prepareGlobalSubjectStatDictionary(self):
        self.__model.setGlobalCollectionDictionaryGlobalStatDictionary()

    def prepareGlobalSubjectValueDictionary(self):
        self.__model.setGlobalCollectionDictionarySubjectDataMemberDictionary()

    def prepareSubjectValueDictionaryDataMemberDictionary(self, subjectValue):
        self.__model.setSubjectDictionaryGeneralSubjectValueDataMemberDictionary(subjectValue)

    def isArticleNonAd(self):
        return self.__view.isArticleNonAd()

    def sortArticleWordDictionary(self):
        self.__model.sortWordDictionary()

#    def sortSourceWordDictionary(self):
#        self.__model.sortGlobalSourceWordDictionary()

    def sortGlobalSubjectWordDictionary(self):
        self.__model.sortGlobalStatWordDictionary()

    def sortGlobalSubjectValueWordDictionary(self, subjectValue):
        self.__model.sortGlobalSubjectValueWordDictionary(subjectValue)

    def writeMasterReportHeader(self, newsSource):
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

    def writeSubjectDataHeader(self, subject):
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

    def writeArticleSegmentHeader(self):
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

    def writeGlobalSubjectDataHeader(self):
        try:
            self.__statFile.write("Global Article Word Analysis - all subjects\n\n")
            self.__statFile.write("First Article Date: " + self.__view.getEarliestDateString() + "\n")
            self.__statFile.write("Last Article Date: " + self.__view.getLatestDateString() + "\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeGlobalSubjectDataHeader")

    def writeGlobalSubjectValueDataHeader(self, subjectValue):
        try:
            self.__statFile.write("Global Article Word Analysis - for subject " + subjectValue + "\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeGlobalSubjectValueDataHeader")

    def writeProcessedArticleData(self, articleTitle):
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

    def writeProcessedSourceData(self):
        try:
            self.__statFile.write("\t" + "global total word count: ")
            self.__statFile.write(self.__view.getSourceTotalWordCount())
            self.__statFile.write("\t" + "global unique word count: ")
            self.__statFile.write(self.__view.getSourceUniqueWordCount())
            self.__statFile.write("\t" + "global individual word counts: " + "\n")
            for entry in self.__view.getSourceIndividualWordCounts():
                self.__statFile.write(entry)
            self.__statFile.write("\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeProcessedSourceData")

    def writeProcessedGlobalSubjectData(self):
        try:
            self.__statFile.write("\t" + "global total word count - all subjects: ")
            self.__statFile.write(self.__view.getSubjectTotalWordCount())
            self.__statFile.write("\t" + "global unique word count - all subjects: ")
            self.__statFile.write(self.__view.getSubjectUniqueWordCount())
            self.__statFile.write("\t" + "global individual word counts - all subjects: " + "\n")
            for entry in self.__view.getSubjectIndividualWordCount():
                self.__statFile.write(entry)
            self.__statFile.write("\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeProcessedGlobalSubjectData")

    def writeProcessedGlobalSubjectValueData(self, subjectValue):
        try:
            self.__statFile.write("\t" + "global total word count - for subject " + subjectValue + ": ")
            self.__statFile.write(self.__view.getSubjectValueTotalWordCount(subjectValue))
            self.__statFile.write("\t" + "global unique word count - for subject " + subjectValue + ": ")
            self.__statFile.write(self.__view.getSubjectValueUniqueWordCount(subjectValue))
            self.__statFile.write("\t" + "global individual word counts - for subject " + subjectValue + ": " + "\n")
            for entry in self.__view.getSubjectValueIndividualWordCount(subjectValue):
                self.__statFile.write(entry)
            self.__statFile.write("\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeProcessedGlobalSubjectValueData")

    def writeHeaderRule(self):
        try:
            self.__statFile.write(("=" * 79) + "\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeHeaderRule")

    def writeArticleTerminatorRule(self):
        try:
            self.__statFile.write(("-" * 79) + "\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeArticleTerminatorRule")

    def writeTerminatorRule(self):
        try:
            self.__statFile.write(("*" * 79) + "\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeTerminatorRule")

    def writeSubjectRule(self):
        try:
            self.__statFile.write(("|" * 79) + "\n\n")
        except:
            print("Failed to write to report file")
            print("Failed in writeSubjectRule")