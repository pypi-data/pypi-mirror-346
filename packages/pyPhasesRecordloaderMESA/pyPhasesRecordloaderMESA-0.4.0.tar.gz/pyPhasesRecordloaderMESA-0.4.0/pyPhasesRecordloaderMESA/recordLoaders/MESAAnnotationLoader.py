from typing import List
from pyPhasesRecordloaderSHHS.recordLoaders.SHHSAnnotationLoader import SHHSAnnotationLoader
from pyPhasesRecordloader import Event


class MESAAnnotationLoader(SHHSAnnotationLoader):
    
    eventMapLeg = {
        "Limb movement - left|Limb Movement (Left)": "LegMovement-Left",
        "Periodic leg movement - left|PLM (Left)": "LegMovement-Left",
        "Limb movement - right|Limb Movement (Right)": "LegMovement-Right",
        "Periodic leg movement - right|PLM (Right)": "LegMovement-Right",
    }

    def loadAnnotation(self, xmlFile) -> List[Event]:
        allEvents = super().loadAnnotation(xmlFile)

        allEvents += self.loadEvents(
            "[EventType='Limb Movement|Limb Movement']",
            self.eventMapLeg,
        )

        return allEvents