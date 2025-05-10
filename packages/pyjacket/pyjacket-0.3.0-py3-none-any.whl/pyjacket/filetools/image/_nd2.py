import nd2


def read(file):
    return nd2.imread(file)

def write(filepath, data, meta):
    ...
    
    
def read_exif(filepath): ...


class MetadataND2:
    
    def __init__(self, filename: str):
        with nd2.ND2File(filename) as f:
            self._md = f.unstructured_metadata()
            
    def __repr__(self):
        props = [attr for attr in dir(self) if not attr.startswith('_')]
        s = ', '.join(props)
        return f"MetadataND2({s})"
     
    """___ Global ___"""
    @property
    def pixel_calibration(self) -> float:
        """get apparent pixel size (microns/pixel) at magnification used."""
        return (self._md
            .get("ImageCalibrationLV|0")
            .get("SLxCalibration")
            .get("Calibration")
        )  
    
    @property
    def total_duration(self):
        raise NotImplemented 
     
     
    """___ Light Source ___""" 
    @property
    def light_intensity(self):
        """Light intensity in percentage"""
        return (self._md
            .get('ImageMetadataSeqLV|0')
            .get('SLxPictureMetadata')
            .get('PicturePlanes')
            .get('SampleSetting')
            .get('0')
            .get('DeviceSetting')
            .get('MultiLaser_PowerLinePower0-00'))
    
     
    """___ Camera ___"""  
    @property        
    def exposure_time(self) -> float:
        """Duration of open shutter in ms"""
        return (self._md
            .get('ImageMetadataSeqLV|0')
            .get('SLxPictureMetadata')
            .get('PicturePlanes')
            .get('SampleSetting')
            .get('0')
            .get('ExposureTime'))
        
    @property
    def period(self) -> float:
        """Time interval between two frames = 1 / fps"""
        loop_pars = (self._md
            .get('ImageMetadataLV')
            .get('SLxExperiment')
            .get('LoopPars')
        )
        periods_selected = loop_pars.get('PeriodValid')  # list[0|1]
        periods = (loop_pars
            .get('Period')
            .get('')
        )
        # assume only one of the periods is selected
        period = periods[periods_selected.index(1)]  
        ms_per_frame = period.get("Period")  # ms
        return ms_per_frame
    
    @property
    def fps(self) -> float:
        """Frames per second"""
        return 1000 / self.period
    
    
    """___ Objective ___"""
    @property
    def magnification(self):
        return (self._md
            .get("ImageMetadataSeqLV|0")
            .get("SLxPictureMetadata")
            .get("PicturePlanes")
            .get("SampleSetting")
            .get("0")
            .get("ObjectiveSetting")
            .get("ObjectiveMag")
        )

    @property
    def numerical_aperture(self):
        return (self._md
            .get("ImageMetadataSeqLV|0")
            .get("SLxPictureMetadata")
            .get("PicturePlanes")
            .get("SampleSetting")
            .get("0")
            .get("ObjectiveSetting")
            .get("ObjectiveNA")
        )     
        

import nd2


def imread_nd2(file):
    return nd2.imread(file)


class MetadataND2:
    
    def __init__(self, filename: str):
        with nd2.ND2File(filename) as f:
            self._md = f.unstructured_metadata()
            
    def __repr__(self):
        props = [attr for attr in dir(self) if not attr.startswith('_')]
        s = ', '.join(props)
        return f"MetadataND2({s})"
     
    """___ Global ___"""
    @property
    def pixel_calibration(self) -> float:
        """get apparent pixel size (microns/pixel) at magnification used."""
        return (self._md
            .get("ImageCalibrationLV|0")
            .get("SLxCalibration")
            .get("Calibration")
        )  
    
    @property
    def total_duration(self):
        raise NotImplemented 
     
     
    """___ Light Source ___""" 
    @property
    def light_intensity(self):
        """Light intensity in percentage"""
        return (self._md
            .get('ImageMetadataSeqLV|0')
            .get('SLxPictureMetadata')
            .get('PicturePlanes')
            .get('SampleSetting')
            .get('0')
            .get('DeviceSetting')
            .get('MultiLaser_PowerLinePower0-00'))
    
     
    """___ Camera ___"""  
    @property        
    def exposure_time(self) -> float:
        """Duration of open shutter in ms"""
        return (self._md
            .get('ImageMetadataSeqLV|0')
            .get('SLxPictureMetadata')
            .get('PicturePlanes')
            .get('SampleSetting')
            .get('0')
            .get('ExposureTime'))
        
    @property
    def period(self) -> float:
        """Time interval between two frames = 1 / fps"""
        loop_pars = (self._md
            .get('ImageMetadataLV')
            .get('SLxExperiment')
            .get('LoopPars')
        )
        periods_selected = loop_pars.get('PeriodValid')  # list[0|1]
        periods = (loop_pars
            .get('Period')
            .get('')
        )
        # assume only one of the periods is selected
        period = periods[periods_selected.index(1)]  
        ms_per_frame = period.get("Period")  # ms
        return ms_per_frame
    
    @property
    def fps(self) -> float:
        """Frames per second"""
        return 1000 / self.period
    
    
    """___ Objective ___"""
    @property
    def magnification(self):
        return (self._md
            .get("ImageMetadataSeqLV|0")
            .get("SLxPictureMetadata")
            .get("PicturePlanes")
            .get("SampleSetting")
            .get("0")
            .get("ObjectiveSetting")
            .get("ObjectiveMag")
        )

    @property
    def numerical_aperture(self):
        return (self._md
            .get("ImageMetadataSeqLV|0")
            .get("SLxPictureMetadata")
            .get("PicturePlanes")
            .get("SampleSetting")
            .get("0")
            .get("ObjectiveSetting")
            .get("ObjectiveNA")
        )     
        

    
if __name__ == '__main__':
    # FILENAME = r"D:\Data\FluorescenceFlow\230331_mpARF1_syOr\tritc003.nd2"
    FILENAME = r"D:\Data\FluorescenceFlow\230417\03164A7_mid\photodegrdation\site05_p1_100mbar007.nd2"


    meta = MetadataND2(FILENAME)
    # data = imread_nd2(FILENAME)
    
    print(meta.exposure_time)
    print(meta.light_intensity)
    print(meta.period)
    print(meta.fps)
    print(meta.magnification)
    print(meta.numerical_aperture)
    print(meta.pixel_calibration)

    
if __name__ == '__main__':
    # FILENAME = r"D:\Data\FluorescenceFlow\230331_mpARF1_syOr\tritc003.nd2"
    FILENAME = r"D:\Data\FluorescenceFlow\230417\03164A7_mid\photodegrdation\site05_p1_100mbar007.nd2"


    meta = MetadataND2(FILENAME)
    # data = imread_nd2(FILENAME)
    
    print(meta.exposure_time)
    print(meta.light_intensity)
    print(meta.period)
    print(meta.fps)
    print(meta.magnification)
    print(meta.numerical_aperture)
    print(meta.pixel_calibration)