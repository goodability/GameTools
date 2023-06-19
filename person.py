from config import personConfig
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
    def resetPosture(isGrovel,isHoldShift,isSquat):
        isGrovel=False
        isHoldShift=False
        isSquat=False
        return isGrovel,isSquat,isHoldShift