from config import personConfig
import os,cv2
class posture:
    def __init__(self):
        pass
    @staticmethod
    def getPostureWeight(isGrovel,isHoldShift,isSquat):
        verticalWeights=1
        if isGrovel:
            verticalWeights=personConfig.grovel
        elif isSquat:
            verticalWeights=personConfig.squat
        if isHoldShift:
            verticalWeights=verticalWeights*personConfig.holdBreath
        return verticalWeights
    @staticmethod
    def resetPosture(*args):
        argsList=[]
        for i in range(len(args)):
            argsList.append(False)
        return argsList