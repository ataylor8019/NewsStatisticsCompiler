#wordCountModel.py
#v1.0x
#
#By Allan Taylor
#
#03/2020
#



import datetime

class masterWordCountModel():

    __titleKey=None                                #Title of article currently being scanned
    __individualLabelKey=None                      #Label for dictionary holding count of word occurrence in article named by __titleKey variable - associated value is itself a dictionary made up of keys (words counted) and their values (count of each word encountered)
    __aggregateLabelKey=None                       #Label for dictionary holding count of all words in article/subject/source
    __uniqueLabelKey=None                          #Label for dictionary holding count of unique words in article/subject/source
    __subjectLabelKey=None                         #Label specifying subject data for __globalCollectionDictionary - holds subdictionaries, labeled by subject name, which themselves contain subdictionaries and subject specific statistical data
    __subjectValueLabelKey=None                    #Label specifying the current subject being scanned
    __globalLabelKey=None                          #Label specifying global data across entire news source
    __articleCollectionDictionary={}               #Dictonary responsible for holding stat data for scanned articles - all other aggregate and global data is derived from entries in this dictionary as the scan proceeds - the key to this dictionary is the __titleKey variable, whose associated value is a sub dictionary containing word statistic data
    __globalCollectionDictionary={}                #Master dictionary: holds all sub dictionaries, anonymous or otherwise - at top level, contains two keys, whose names are specified by the variables __globalLabelKey and __subjectLabelKey - all sub values and dictionaries are assigned under one of these two keys
    __currentArticleDateDateFormat=None            #Variable holding the date of the article currently being scanned in a format that the datetime module can work with (it is a pure datetime object that can have datetime operations performed on it)
    __currentArticleDateStringFormat=""            #Variable holding the date of the article currently being scanned in a format that is printable (it is a string object)
    __earliestDateDateFormat=datetime.datetime.max                  #Variable holding the earliest date of all articles in news source in a datetime object
    __latestDateDateFormat=datetime.datetime.min                    #Variable holding the latest date of all articles in news source in a datetime object
    __earliestDateStringFormat=""                  #Variable holding the earliest date of all articles in news source in a string object
    __latestDateStringFormat=""                    #Variable holding the latest date of all articles in news source in a string object

# !!! IMPORTANT NOTE: When reviewing code, comments, be sure to read closely, so as to be able to discern which dictionary keys are returning values, and which dictionary keys are returning sub dictionaries !!!

    def setGlobalLabelKey(self, globalLabelKey):        #set key specifying entry holding global values data in __globalCollectionDictionary
        self.__globalLabelKey = globalLabelKey

    def setSubjectLabelKey(self, subjectLabelKey):    #set key specifying entry holding subject specific values data in __globalCollectionDictionary
        self.__subjectLabelKey = subjectLabelKey

    def setSubjectValueLabelKey(self, subjectValueLabelKey):    #set key to name of subject currently being worked on, key is assigned to individual subjectValue sub dictionary in __globalCollectionDictionary
        self.__subjectValueLabelKey = subjectValueLabelKey

    def setTitleKey(self, titleKey):    #set key to title of article, is assigned to __articleCollectionDictionary
        self.__titleKey = titleKey

    def getTitleKey(self):
        return self.__titleKey

    def setIndividualLabelKey(self, individualLabelKey):    #set key specifying entry holding individual word list and counts of those words for given dictionary - key is recycled among __articleCollectionDictionary, subjectValue sub dictionaries, and __globalCollectionDictionary
        self.__individualLabelKey = individualLabelKey

    def setAggregateLabelKey(self, aggregateLabelKey):    #set key to value holding aggregate word count for given dictionary - key is recycled among __articleCollectionDictionary, subjectValue sub dictionaries, and __globalCollectionDictionary
        self.__aggregateLabelKey = aggregateLabelKey

    def setUniqueLabelKey(self, uniqueLabelKey):    #set key to value holding unique word count for given dictionary - key is recycled among __articleCollectionDictionary, subjectValue sub dictionaries, and __globalCollectionDictionary
        self.__uniqueLabelKey = uniqueLabelKey

    def setArticleCollectionDictionaryTitleMemberDictionary(self):    #set dictionary entry in __articleCollectionDictionary having key named by __titleKey to empty dictionary, execute function to initialize that dictionary to statistic holding values - typically done when reading a new article in a news file
        self.__articleCollectionDictionary[self.__titleKey]={}
        self.setTitleDictionaryGeneralWordDataMemberDictionary()

    def setTitleDictionaryGeneralWordDataMemberDictionary(self):    #set dictionary entry in __articleCollectionDictionary having key named by __titleKey to word statistic holding dictionary, including __individualLabelKey entry having a value of an empty sub dictionary
        self.__articleCollectionDictionary[self.__titleKey]={self.__aggregateLabelKey: 0, self.__uniqueLabelKey: 0, self.__individualLabelKey: {}}
    
    def setGlobalCollectionDictionaryGlobalStatDictionary(self):
        self.__globalCollectionDictionary[self.__globalLabelKey]={self.__aggregateLabelKey: 0, self.__uniqueLabelKey: 0, self.__individualLabelKey: {}}    #Creates an entry in __globalCollectionDictionary (usually named "global data") that holds a dictionary that holds both word statistic data and a smaller dictionary that holds individual word count data

    def setGlobalCollectionDictionarySubjectDataMemberDictionary(self):
        self.__globalCollectionDictionary[self.__subjectLabelKey]={}    #Creates an entry in the globalCollectionDictionary (usually named "subject data") that holds keys that correspond to the multiple subjects scanned into it (Usually named things like "World", "Politics", "Technology", "Local"...)

    def setSubjectDictionaryGeneralSubjectValueDataMemberDictionary(self, subjectValue):    #creates a key in the __subjectLabelKey sub dictionary of __globalCollectionDictionary, named in subjectValue, having the value of a sub dictionary that holds word statistic data - this data is aggregated from all articles in a scanned news subject file
        self.__globalCollectionDictionary[self.__subjectLabelKey][subjectValue]={self.__aggregateLabelKey: 0, self.__uniqueLabelKey: 0, self.__individualLabelKey: {}}    #Set current subject in dictionary referred to by the subject key in the __globalCollectionDictionary to a dictionary that can hold word statistic data

    # def setGlobalGeneralWordDataDictionary(self):
        # self.__globalGeneralWordDataDictionary={self.__aggregateLabelKey: 0, self.__uniqueLabelKey: 0, self.__individualLabelKey: self.__globalIndividualWordDataDictionary}

    def addTermToGeneralWordDataDictionary(self, wordToAdd):    #performs increment of word statistic values encounted in scanned article
        if wordToAdd in self.returnGeneralWordDataDictionaryIndividualWordDataMemberDictionary():    #Increments __articleCollectionDictionary wordToAdd value entry, that is, if you encounter a word, it updates the dictionary logging the number of times that word has been encountered
            self.returnGeneralWordDataDictionaryIndividualWordDataMemberDictionary()[wordToAdd]+=1
        else:
            self.returnGeneralWordDataDictionaryIndividualWordDataMemberDictionary()[wordToAdd]=1
            self.__articleCollectionDictionary[self.__titleKey][self.__uniqueLabelKey]+=1        #If here, word has never been encountered before. Sets the wordToAdd value entry to 1 (since there is at least one occurrence of the word) and updates the unique count entry (the word has never been seen before, so it's another unique word)

    def addTermToGlobalStatDictionary(self, wordToAdd):    #performs increment of word statistic values aggregated globally from all articles and subjects in a given news source
        if wordToAdd in self.__globalCollectionDictionary[self.__globalLabelKey][self.__individualLabelKey]:    #increments value belonging to wordToAdd key of word statistic sub dictionary by 1 if the word already exists
            self.__globalCollectionDictionary[self.__globalLabelKey][self.__individualLabelKey][wordToAdd]+=1
        else:
            self.__globalCollectionDictionary[self.__globalLabelKey][self.__individualLabelKey][wordToAdd]=1    #if here, word has never been encountered before - set the value of the wordToAdd key to 1 (there is at least one occurrence of the word now), increment the __uniqueLabelKey by 1
            self.__globalCollectionDictionary[self.__globalLabelKey][self.__uniqueLabelKey]+=1

    def addTermToSubjectValueDataMemberDictionary(self, wordToAdd, subjectValue):    #performs increment of word statistic values aggregated from all articles within a given subject in a given news source
        if wordToAdd in self.__globalCollectionDictionary[self.__subjectLabelKey][subjectValue][self.__individualLabelKey]:
            self.__globalCollectionDictionary[self.__subjectLabelKey][subjectValue][self.__individualLabelKey][wordToAdd]+=1
        else:
            self.__globalCollectionDictionary[self.__subjectLabelKey][subjectValue][self.__individualLabelKey][wordToAdd]=1
            self.__globalCollectionDictionary[self.__subjectLabelKey][subjectValue][self.__uniqueLabelKey]+=1
    
    def addTermToWordCountDictionaries(self, wordToAdd, subjectValue):    #wrapper function generally used by external controllers - increments _articleCollectionDictionary statistics, as well as current subject aggregate and global statistic data in __globalCollectionDictionary, one after the other
        self.addTermToGeneralWordDataDictionary(wordToAdd)
        self.addTermToSubjectValueDataMemberDictionary(wordToAdd, subjectValue)
        self.addTermToGlobalStatDictionary(wordToAdd)

    def returnGeneralWordDataDictionaryIndividualWordDataMemberDictionary(self):    #returns subdictionary keyed to __individualLabelKey, belonging to the dictionary whose key is __titleKey, within the __articleCollectionDictionary dictionary
        return self.__articleCollectionDictionary[self.__titleKey][self.__individualLabelKey]

    def returnGeneralWordDataDictionaryAggregateWordDataMember(self):    #returns value keyed to __aggregateLabelKey, belonging to the dictionary whose key is __titleKey, within the __articleCollectionDictionary dictionary
        return self.__articleCollectionDictionary[self.__titleKey][self.__aggregateLabelKey] 

    def returnGeneralWordDataDictionaryUniqueWordDataMember(self):    #returns value keyed to __uniqueLabelKey, belonging to the dictionary whose key is __titleKey, within the __articleCollectionDictionary dictionary
        return self.__articleCollectionDictionary[self.__titleKey][self.__uniqueLabelKey]

    def returnGlobalStatDictionaryIndividualWordDataMemberDictionary(self):    #returns subdictionary keyed to __individualLabelKey, belonging to the dictionary whose key is __titleKey, within the __globalCollectionDictionary dictionary
        return self.__globalCollectionDictionary[self.__globalLabelKey][self.__individualLabelKey]

    def returnGlobalStatDictionaryAggregateWordDataMember(self):    #returns value keyed to __aggregateLabelKey, belonging to the dictionary whose key is __titleKey, within the __globalCollectionDictionary dictionary
        return self.__globalCollectionDictionary[self.__globalLabelKey][self.__aggregateLabelKey]

    def returnGlobalStatDictionaryUniqueWordDataMember(self):    #returns value keyed to __uniqueLabelKey, belonging to the dictionary whose key is __titleKey, within the __globalCollectionDictionary dictionary
        return self.__globalCollectionDictionary[self.__globalLabelKey][self.__uniqueLabelKey]

    def returnGlobalSubjectValueDictionaryIndividualWordDataMemberDictionary(self, subjectValue):    #returns value (being a subdictionary) keyed to __individualLabelKey of the subdictionary keyed to current subjectValue, keyed to the __subjectLabelKey in the __globalCollectionDictionary
        return self.__globalCollectionDictionary[self.__subjectLabelKey][subjectValue][self.__individualLabelKey]

    def returnGlobalSubjectValueDictionaryAggregateWordDataMember(self, subjectValue):    #returns value keyed to __aggregateLabelKey of the subdictionary keyed to current subjectValue, keyed to the __subjectLabelKey in the __globalCollectionDictionary
        return self.__globalCollectionDictionary[self.__subjectLabelKey][subjectValue][self.__aggregateLabelKey]

    def returnGlobalSubjectValueDictionaryUniqueWordDataMember(self, subjectValue):    #returns value keyed to __uniqueLabelKey of the subdictionary keyed to current subjectValue, keyed to the __subjectLabelKey in the __globalCollectionDictionary
        return self.__globalCollectionDictionary[self.__subjectLabelKey][subjectValue][self.__uniqueLabelKey]

    def incrementTitleAggregateWordDataMember(self):
        self.__articleCollectionDictionary[self.__titleKey][self.__aggregateLabelKey]+=1        #increment total word count of currently scanned article

    def incrementGlobalStatDictionaryAggregateWordDataMember(self):
        self.__globalCollectionDictionary[self.__globalLabelKey][self.__aggregateLabelKey]+=1        #increment total word count of entire news source

    def incrementGlobalSubjectValueDictionaryAggregateWordDataMember(self, subjectValue):
        self.__globalCollectionDictionary[self.__subjectLabelKey][subjectValue][self.__aggregateLabelKey]+=1        #increment total word count of current subject in news source
        

    #Overview of sort functions: perform list comprehension of dictionary holding word statistical data (whether for articles, subjects, or the entire news source)
    #current dictionary holding word statistical data is cleared, set to none, replaced with sorted dictionary generated from list comprehension, so as to
    #avoid any issues whatsoever with unintentional or failed changes to the public facing word statistical data dictionary due to being a mutable object
    def sortWordDictionary(self):
        sortedParagraphList={k:v for k,v in sorted(self.returnGeneralWordDataDictionaryIndividualWordDataMemberDictionary().items(), key=lambda item: item[1], reverse=True)}
        self.__articleCollectionDictionary[self.__titleKey][self.__individualLabelKey].clear()
        self.__articleCollectionDictionary[self.__titleKey][self.__individualLabelKey] = None
        self.__articleCollectionDictionary[self.__titleKey][self.__individualLabelKey] = sortedParagraphList

    def sortGlobalStatWordDictionary(self):
        sortedGlobalStatIndividualWordCountList={k:v for k,v in sorted(self.__globalCollectionDictionary[self.__globalLabelKey][self.__individualLabelKey].items(), key=lambda item: item[1], reverse=True)}
        self.__globalCollectionDictionary[self.__globalLabelKey][self.__individualLabelKey].clear()
        self.__globalCollectionDictionary[self.__globalLabelKey][self.__individualLabelKey]=None
        self.__globalCollectionDictionary[self.__globalLabelKey][self.__individualLabelKey]=sortedGlobalStatIndividualWordCountList

    def sortGlobalSubjectValueWordDictionary(self, subjectValue):
        sortedGlobalSubjectValueIndividualWordCountList={k:v for k,v in sorted(self.__globalCollectionDictionary[self.__subjectLabelKey][subjectValue][self.__individualLabelKey].items(), key=lambda item: item[1], reverse=True)}
        self.__globalCollectionDictionary[self.__subjectLabelKey][subjectValue][self.__individualLabelKey].clear()
        self.__globalCollectionDictionary[self.__subjectLabelKey][subjectValue][self.__individualLabelKey]=None
        self.__globalCollectionDictionary[self.__subjectLabelKey][subjectValue][self.__individualLabelKey]=sortedGlobalSubjectValueIndividualWordCountList


    #Reads in the date of the current article being read (taken from a JSON entry most likely), converts it to a date object
    def setCurrentArticleDateString(self, dateString):
        self.__currentArticleDateStringFormat=dateString
        self.convertCurrentArticleDateStringToDate()

    #checks to see if the date of the article currently being read is earlier than the current earliest article date
    #if so, update the __earliestDateDateFormat variable with the current article date
    def calculateEarliestDate(self):
        if (self.__currentArticleDateDateFormat < self.__earliestDateDateFormat):
            self.__earliestDateDateFormat = self.__currentArticleDateDateFormat

    #checks to see if the date of the article currently being read is later than the current latest article date
    #if so, update the __latestDateDateFormat variable with the current article date
    def calculateLatestDate(self):
        if (self.__currentArticleDateDateFormat > self.__latestDateDateFormat):
            self.__latestDateDateFormat = self.__currentArticleDateDateFormat

    #Converts date to string object for presentation by view
    def convertEarliestDateDateToString(self):
        self.__earliestDateStringFormat=self.__earliestDateDateFormat.strftime("%B %d, %Y")
    
    #Converts date to string object for presentation by view
    def convertCurrentArticleDateStringToDate(self):
        self.__currentArticleDateDateFormat=datetime.datetime.strptime(self.__currentArticleDateStringFormat, "%B %d, %Y")
    
    #Converts date to string object for presentation by view
    def convertLatestDateDateToString(self):
        self.__latestDateStringFormat=self.__latestDateDateFormat.strftime("%B %d, %Y")

    #wrapper function, calculates earliest and latest dates of articles read
    def sortDate(self):
        self.calculateEarliestDate()
        self.calculateLatestDate()

    #returns date object of earliest date read of all articles scanned
    def getEarliestDate(self):
        return self.__earliestDateDateFormat

    #returns date object of latest date read of all articles scanned
    def getLatestDate(self):
        return self.__latestDateDateFormat

