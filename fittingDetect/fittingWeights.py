from config import fittingConfig
class getFittingWeights:
    def __init__(self):
        pass
    @staticmethod
    def getWeights(muzzleType,gripType,stockType):
        AllWeights=1
        #判断枪口类型权重
        if muzzleType==fittingConfig.muzzleComensatorName:
            AllWeights=AllWeights*fittingConfig.muzzleComensator
        elif muzzleType==fittingConfig.noFireName:
            AllWeights=AllWeights*fittingConfig.noFirer
        elif muzzleType==fittingConfig.silencerName:
            AllWeights=AllWeights*fittingConfig.silencer
        #判断握把权重
        if gripType==fittingConfig.verticalGripName:
            AllWeights=AllWeights*fittingConfig.verticalGrip
        elif gripType==fittingConfig.lightGripName:
            AllWeights=AllWeights*fittingConfig.lightGrip
        elif gripType==fittingConfig.thumbGripName:
            AllWeights=AllWeights*fittingConfig.thumbGrip
        elif gripType==fittingConfig.redGripName:
            AllWeights=AllWeights*fittingConfig.redGrip
        elif gripType==fittingConfig.triangularGripName:
            AllWeights=AllWeights*fittingConfig.triangularGrip
        #判断枪托权重
        if stockType==fittingConfig.lightStockName:
            AllWeights=AllWeights*fittingConfig.lightStock
        elif stockType==fittingConfig.heavyStockName:
            AllWeights=AllWeights*fittingConfig.heavyStock
        return AllWeights