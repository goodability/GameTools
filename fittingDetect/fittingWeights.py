from config import fittingConfig,gunConfig

class getFittingWeights:
    def __init__(self):
        pass
    @staticmethod
    def getWeights(gun,muzzleType,gripType,stockType):
        AllWeights=1
        muzzleWeights=1
        gripWeights=1
        stockWeights=1
        #判断枪口类型权重
        try:
            if muzzleType==fittingConfig.muzzleComensatorName:
                muzzleWeights=gunConfig.guns[gun]["muzzle"]["compensator"]
            elif muzzleType==fittingConfig.noFireName:
                muzzleWeights=gunConfig.guns[gun]["muzzle"]["noFirer"]
            elif muzzleType==fittingConfig.silencerName:
                muzzleWeights=gunConfig.guns[gun]["muzzle"]["silencer"]
        except:
            muzzleWeights=1
        #判断握把权重
        try:
            if gripType==fittingConfig.verticalGripName:
                gripWeights=gunConfig.guns[gun]["grip"]["verticalGrip"]
            elif gripType==fittingConfig.lightGripName:
                gripWeights=gunConfig.guns[gun]["grip"]["lightGrip"]
            elif gripType==fittingConfig.thumbGripName:
                gripWeights=gunConfig.guns[gun]["grip"]["thumbGrip"]
            elif gripType==fittingConfig.redGripName:
                gripWeights=gunConfig.guns[gun]["grip"]["redGrip"]
            elif gripType==fittingConfig.triangularGripName:
                gripWeights=gunConfig.guns[gun]["grip"]["triangularGrip"]
        except:
            gripWeights=1
        #判断枪托权重
        try:
            if stockType==fittingConfig.lightStockName:
                stockWeights=gunConfig.guns[gun]["stock"]["lightStock"]
            elif stockType==fittingConfig.heavyStockName:
                stockWeights=gunConfig.guns[gun]["stock"]["heavyStock"]
        except:
            stockWeights=1
        muzzleWeights=1-muzzleWeights
        gripWeights=1-gripWeights
        stockWeights=1-stockWeights
        AllWeights=AllWeights-muzzleWeights-gripWeights-stockWeights
        return AllWeights