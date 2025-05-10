from pyPhasesRecordloader.recordLoaders.CSVMetaLoader import CSVMetaLoader
from pyPhasesRecordloaderSHHS.recordLoaders.RecordLoaderSHHS import RecordLoaderSHHS

from pyPhasesRecordloaderMESA.recordLoaders.MESAAnnotationLoader import MESAAnnotationLoader


class RecordLoaderMESA(RecordLoaderSHHS):
    def getFilePathSignal(self, recordId):
        return f"{self.filePath}/polysomnography/edfs/{recordId}.edf"

    def getFilePathAnnotation(self, recordId):
        return f"{self.filePath}/polysomnography/annotations-events-nsrr/{recordId}-nsrr.xml"

    def getRelevantCols(self):
        return {
            # "gender": "gender1",
            # "age": "sleepage5c",
            "sLatency": "slp_lat5",
            "rLatency": "rem_lat15",
            "waso": "waso5",
            "sEfficiency": "slp_eff5",
            "indexPlms": "avgplm5",
            "indexPlmsArousal": "avgplma5",
            # for countArousal
            "arnrembp5": "arnrembp5",
            "arnremop5": "arnremop5",
            "arrembp5": "arrembp5",
            "arremop5": "arremop5",
            # therapy / diagnostics
            # % N1, N2, N3, R
            # not existing
            #"bmi
        }
    
    def getHarmonizedCols(self):
        return {
            "age": "nsrr_age",
            "gender": "nsrr_sex",
            "tst": "nsrr_tst_f1",
            "ahi": "nsrr_ahi_hp4r",
            "indexArousal": "nsrr_phrnumar_f1",
            "race": "nsrr_race",
        }
    
    def getMetaData(self, recordName):
        metaData = super().getMetaData(recordName, loadMetadataFromCSV=False)
        metaData["recordId"] = recordName
        harmonizedColumns = self.getHarmonizedCols()
        relevantColumns = self.getRelevantCols()
        csvLoader = CSVMetaLoader(
            f"{self.filePath}/datasets/mesa-sleep-dataset-0.7.0.csv", idColumn="mesaid", relevantRows=relevantColumns
        )
        csvMetaData = csvLoader.getMetaData(int(recordName[11:]))
        metaData.update(csvMetaData)
        
        csvLoader = CSVMetaLoader(
            f"{self.filePath}/datasets/mesa-sleep-harmonized-dataset-0.7.0.csv", idColumn="mesaid", relevantRows=harmonizedColumns
        )
        csvMetaData = csvLoader.getMetaData(int(recordName[11:]))
        metaData.update(csvMetaData)

        metaData["countArousal"] = metaData["arnrembp5"] + metaData["arnremop5"] + metaData["arremop5"] + metaData["arrembp5"]

        return metaData

    def getAllMetaData(self):
        harmonizedColumns = self.getHarmonizedCols()
        relevantCols = self.getRelevantCols()

        csvLoader = CSVMetaLoader(
            f"{self.filePath}/datasets/mesa-sleep-dataset-0.7.0.csv", idColumn="mesaid", relevantRows=relevantCols
        )
        metaData = csvLoader.getAllMetaData()
        csvLoader = CSVMetaLoader(
            f"{self.filePath}/datasets/mesa-sleep-harmonized-dataset-0.7.0.csv", idColumn="mesaid", relevantRows=harmonizedColumns
        )
        # merge pandas frames
        csvMetaData = csvLoader.getAllMetaData()
        metaData = metaData.merge(csvMetaData, on="recordId")

        #padded record id
        metaData["recordId"] = metaData["recordId"].apply(lambda x: "mesa-sleep-" + str(x).zfill(4))
        return metaData
        
        
    def getEventList(self, recordName, targetFrequency=1):
        metaXML = self.getFilePathAnnotation(recordName)
        xmlLoader = MESAAnnotationLoader()

        eventArray = xmlLoader.loadAnnotation(metaXML)
        self.lightOff = xmlLoader.lightOff
        self.lightOn = xmlLoader.lightOn

        if targetFrequency != 1:
            eventArray = self.updateFrequencyForEventList(eventArray, targetFrequency)

        return eventArray