from config import fittingConfig
class getFittingWeights:
    def __init__(self):
        pass
    @staticmethod
    def getWeights(muzzleType,gripType,stockType):
        AllWeights=1
        muzzleWeights=1
        gripWeights=1
        stockWeights=1
        #判断枪口类型权重
        if muzzleType==fittingConfig.muzzleComensatorName:
            muzzleWeights=fittingConfig.muzzleComensator
        elif muzzleType==fittingConfig.noFireName:
            muzzleWeights=fittingConfig.noFirer
        elif muzzleType==fittingConfig.silencerName:
            muzzleWeights=fittingConfig.silencer
        #判断握把权重
        if gripType==fittingConfig.verticalGripName:
            gripWeights=fittingConfig.verticalGrip
        elif gripType==fittingConfig.lightGripName:
            gripWeights=fittingConfig.lightGrip
        elif gripType==fittingConfig.thumbGripName:
            gripWeights=fittingConfig.thumbGrip
        elif gripType==fittingConfig.redGripName:
            gripWeights=fittingConfig.redGrip
        elif gripType==fittingConfig.triangularGripName:
            gripWeights=fittingConfig.triangularGrip
        #判断枪托权重
        if stockType==fittingConfig.lightStockName:
            stockWeights=fittingConfig.lightStock
        elif stockType==fittingConfig.heavyStockName:
            stockWeights=fittingConfig.heavyStock
        muzzleWeights=1-muzzleWeights
        gripWeights=1-gripWeights
        stockWeights=1-stockWeights
        AllWeights=AllWeights-muzzleWeights-gripWeights-stockWeights
        return AllWeights