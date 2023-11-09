from config import personConfig,gunConfig
import os,cv2
class posture:
    def __init__(self):
        pass
    @staticmethod
    def getPostureWeight(isGrovel,isHoldShift,isSquat,gunType):
        verticalWeights=1
        if isGrovel:
            verticalWeights=personConfig.PostureWeight[gunType]["posture"]["grovel"]
        elif isSquat:
            verticalWeights=personConfig.PostureWeight[gunType]["posture"]["squat"]
        if isHoldShift:
            verticalWeights=verticalWeights*personConfig.PostureWeight[gunType]["hold"]
        return verticalWeights
    @staticmethod
    def resetPosture(*args):
        argsList=[]
        for i in range(len(args)):
            argsList.append(False)
        return argsList