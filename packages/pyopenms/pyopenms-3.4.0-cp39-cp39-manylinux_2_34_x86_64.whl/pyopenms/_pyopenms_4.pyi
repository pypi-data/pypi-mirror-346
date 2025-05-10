from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_MRMRTNormalizer_chauvenet(residuals: List[float] , pos: int ) -> bool:
    """
    Cython signature: bool chauvenet(libcpp_vector[double] residuals, int pos)
    """
    ...

def __static_MRMRTNormalizer_chauvenet_probability(residuals: List[float] , pos: int ) -> float:
    """
    Cython signature: double chauvenet_probability(libcpp_vector[double] residuals, int pos)
    """
    ...

def __static_MRMRTNormalizer_computeBinnedCoverage(rtRange: List[float, float] , pairs: List[List[float, float]] , nrBins: int , minPeptidesPerBin: int , minBinsFilled: int ) -> bool:
    """
    Cython signature: bool computeBinnedCoverage(libcpp_pair[double,double] rtRange, libcpp_vector[libcpp_pair[double,double]] & pairs, int nrBins, int minPeptidesPerBin, int minBinsFilled)
    """
    ...

def __static_FileHandler_computeFileHash(filename: Union[bytes, str, String] ) -> Union[bytes, str, String]:
    """
    Cython signature: String computeFileHash(const String & filename)
    """
    ...

def __static_VersionDetails_create(in_0: Union[bytes, str, String] ) -> VersionDetails:
    """
    Cython signature: VersionDetails create(String)
    """
    ...

def __static_MZTrafoModel_enumToName(mt: int ) -> bytes:
    """
    Cython signature: libcpp_string enumToName(MZTrafoModel_MODELTYPE mt)
    """
    ...

def __static_MZTrafoModel_findNearest(tms: List[MZTrafoModel] , rt: float ) -> int:
    """
    Cython signature: size_t findNearest(libcpp_vector[MZTrafoModel] & tms, double rt)
    """
    ...

def __static_VersionInfo_getBranch() -> Union[bytes, str, String]:
    """
    Cython signature: String getBranch()
    """
    ...

def __static_TransformationModelLinear_getDefaultParameters(in_0: Param ) -> None:
    """
    Cython signature: void getDefaultParameters(Param &)
    """
    ...

def __static_CalibrationData_getMetaValues() -> List[bytes]:
    """
    Cython signature: StringList getMetaValues()
    """
    ...

def __static_VersionInfo_getRevision() -> Union[bytes, str, String]:
    """
    Cython signature: String getRevision()
    """
    ...

def __static_VersionInfo_getTime() -> Union[bytes, str, String]:
    """
    Cython signature: String getTime()
    """
    ...

def __static_FileHandler_getType(filename: Union[bytes, str, String] ) -> int:
    """
    Cython signature: int getType(const String & filename)
    """
    ...

def __static_FileHandler_getTypeByContent(filename: Union[bytes, str, String] ) -> int:
    """
    Cython signature: FileType getTypeByContent(const String & filename)
    """
    ...

def __static_FileHandler_getTypeByFileName(filename: Union[bytes, str, String] ) -> int:
    """
    Cython signature: FileType getTypeByFileName(const String & filename)
    """
    ...

def __static_VersionInfo_getVersion() -> Union[bytes, str, String]:
    """
    Cython signature: String getVersion()
    """
    ...

def __static_VersionInfo_getVersionStruct() -> VersionDetails:
    """
    Cython signature: VersionDetails getVersionStruct()
    """
    ...

def __static_FileHandler_hasValidExtension(filename: Union[bytes, str, String] , type_: int ) -> bool:
    """
    Cython signature: bool hasValidExtension(const String & filename, FileType type_)
    """
    ...

def __static_FileHandler_isSupported(type_: int ) -> bool:
    """
    Cython signature: bool isSupported(FileType type_)
    """
    ...

def __static_MZTrafoModel_isValidModel(trafo: MZTrafoModel ) -> bool:
    """
    Cython signature: bool isValidModel(MZTrafoModel & trafo)
    """
    ...

def __static_MZTrafoModel_nameToEnum(name: bytes ) -> int:
    """
    Cython signature: MZTrafoModel_MODELTYPE nameToEnum(libcpp_string name)
    """
    ...

def __static_MRMRTNormalizer_removeOutliersIterative(pairs: List[List[float, float]] , rsq_limit: float , coverage_limit: float , use_chauvenet: bool , outlier_detection_method: bytes ) -> List[List[float, float]]:
    """
    Cython signature: libcpp_vector[libcpp_pair[double,double]] removeOutliersIterative(libcpp_vector[libcpp_pair[double,double]] & pairs, double rsq_limit, double coverage_limit, bool use_chauvenet, libcpp_string outlier_detection_method)
    """
    ...

def __static_MRMRTNormalizer_removeOutliersRANSAC(pairs: List[List[float, float]] , rsq_limit: float , coverage_limit: float , max_iterations: int , max_rt_threshold: float , sampling_size: int ) -> List[List[float, float]]:
    """
    Cython signature: libcpp_vector[libcpp_pair[double,double]] removeOutliersRANSAC(libcpp_vector[libcpp_pair[double,double]] & pairs, double rsq_limit, double coverage_limit, size_t max_iterations, double max_rt_threshold, size_t sampling_size)
    """
    ...

def __static_MZTrafoModel_setCoefficientLimits(offset: float , scale: float , power: float ) -> None:
    """
    Cython signature: void setCoefficientLimits(double offset, double scale, double power)
    """
    ...

def __static_MZTrafoModel_setRANSACParams(p: RANSACParam ) -> None:
    """
    Cython signature: void setRANSACParams(RANSACParam p)
    """
    ...

def __static_FileHandler_stripExtension(file: Union[bytes, str, String] ) -> Union[bytes, str, String]:
    """
    Cython signature: String stripExtension(String file)
    """
    ...

def __static_FileHandler_swapExtension(filename: Union[bytes, str, String] , new_type: int ) -> Union[bytes, str, String]:
    """
    Cython signature: String swapExtension(String filename, FileType new_type)
    """
    ...


class AScore:
    """
    Cython implementation of _AScore

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AScore.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AScore()
        """
        ...
    
    @overload
    def __init__(self, in_0: AScore ) -> None:
        """
        Cython signature: void AScore(AScore &)
        """
        ...
    
    def compute(self, hit: PeptideHit , real_spectrum: MSSpectrum ) -> PeptideHit:
        """
        Cython signature: PeptideHit compute(PeptideHit & hit, MSSpectrum & real_spectrum)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class AbsoluteQuantitation:
    """
    Cython implementation of _AbsoluteQuantitation

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AbsoluteQuantitation.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AbsoluteQuantitation()
        """
        ...
    
    @overload
    def __init__(self, in_0: AbsoluteQuantitation ) -> None:
        """
        Cython signature: void AbsoluteQuantitation(AbsoluteQuantitation &)
        """
        ...
    
    def setQuantMethods(self, quant_methods: List[AbsoluteQuantitationMethod] ) -> None:
        """
        Cython signature: void setQuantMethods(libcpp_vector[AbsoluteQuantitationMethod] & quant_methods)
        """
        ...
    
    def getQuantMethods(self) -> List[AbsoluteQuantitationMethod]:
        """
        Cython signature: libcpp_vector[AbsoluteQuantitationMethod] getQuantMethods()
        """
        ...
    
    def calculateRatio(self, component_1: Feature , component_2: Feature , feature_name: Union[bytes, str, String] ) -> float:
        """
        Cython signature: double calculateRatio(Feature & component_1, Feature & component_2, const String & feature_name)
        """
        ...
    
    def applyCalibration(self, component: Feature , IS_component: Feature , feature_name: Union[bytes, str, String] , transformation_model: Union[bytes, str, String] , transformation_model_params: Param ) -> float:
        """
        Cython signature: double applyCalibration(const Feature & component, const Feature & IS_component, const String & feature_name, const String & transformation_model, const Param & transformation_model_params)
        """
        ...
    
    def quantifyComponents(self, unknowns: FeatureMap ) -> None:
        """
        Cython signature: void quantifyComponents(FeatureMap & unknowns)
        This function applies the calibration curve, hence quantifying all the components
        """
        ...
    
    def optimizeCalibrationCurveIterative(self, component_concentrations: List[AQS_featureConcentration] , feature_name: Union[bytes, str, String] , transformation_model: Union[bytes, str, String] , transformation_model_params: Param , optimized_params: Param ) -> bool:
        """
        Cython signature: bool optimizeCalibrationCurveIterative(libcpp_vector[AQS_featureConcentration] & component_concentrations, const String & feature_name, const String & transformation_model, const Param & transformation_model_params, Param & optimized_params)
        """
        ...
    
    def optimizeSingleCalibrationCurve(self, component_name: Union[bytes, str, String] , component_concentrations: List[AQS_featureConcentration] ) -> None:
        """
        Cython signature: void optimizeSingleCalibrationCurve(const String & component_name, libcpp_vector[AQS_featureConcentration] & component_concentrations)
        """
        ...
    
    def calculateBias(self, actual_concentration: float , calculated_concentration: float ) -> float:
        """
        Cython signature: double calculateBias(double actual_concentration, double calculated_concentration)
        This function calculates the bias of the calibration
        """
        ...
    
    def fitCalibration(self, component_concentrations: List[AQS_featureConcentration] , feature_name: Union[bytes, str, String] , transformation_model: Union[bytes, str, String] , transformation_model_params: Param ) -> Param:
        """
        Cython signature: Param fitCalibration(libcpp_vector[AQS_featureConcentration] & component_concentrations, const String & feature_name, const String & transformation_model, Param transformation_model_params)
        """
        ...
    
    def calculateBiasAndR(self, component_concentrations: List[AQS_featureConcentration] , feature_name: Union[bytes, str, String] , transformation_model: Union[bytes, str, String] , transformation_model_params: Param , biases: List[float] , correlation_coefficient: float ) -> None:
        """
        Cython signature: void calculateBiasAndR(libcpp_vector[AQS_featureConcentration] & component_concentrations, const String & feature_name, const String & transformation_model, Param & transformation_model_params, libcpp_vector[double] & biases, double & correlation_coefficient)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class AverageLinkage:
    """
    Cython implementation of _AverageLinkage

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AverageLinkage.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AverageLinkage()
        """
        ...
    
    @overload
    def __init__(self, in_0: AverageLinkage ) -> None:
        """
        Cython signature: void AverageLinkage(AverageLinkage &)
        """
        ... 


class BiGaussModel:
    """
    Cython implementation of _BiGaussModel

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1BiGaussModel.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void BiGaussModel()
        """
        ...
    
    @overload
    def __init__(self, in_0: BiGaussModel ) -> None:
        """
        Cython signature: void BiGaussModel(BiGaussModel &)
        """
        ...
    
    def setOffset(self, offset: float ) -> None:
        """
        Cython signature: void setOffset(double offset)
        """
        ...
    
    def setSamples(self) -> None:
        """
        Cython signature: void setSamples()
        """
        ...
    
    def getCenter(self) -> float:
        """
        Cython signature: double getCenter()
        """
        ... 


class BilinearInterpolation:
    """
    Cython implementation of _BilinearInterpolation[double,double]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1BilinearInterpolation[double,double].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void BilinearInterpolation()
        """
        ...
    
    @overload
    def __init__(self, in_0: BilinearInterpolation ) -> None:
        """
        Cython signature: void BilinearInterpolation(BilinearInterpolation &)
        """
        ...
    
    def value(self, arg_pos_0: float , arg_pos_1: float ) -> float:
        """
        Cython signature: double value(double arg_pos_0, double arg_pos_1)
        """
        ...
    
    def addValue(self, arg_pos_0: float , arg_pos_1: float , arg_value: float ) -> None:
        """
        Cython signature: void addValue(double arg_pos_0, double arg_pos_1, double arg_value)
        Performs bilinear resampling. The arg_value is split up and added to the data points around arg_pos. ("forward resampling")
        """
        ...
    
    def getData(self) -> MatrixDouble:
        """
        Cython signature: MatrixDouble getData()
        """
        ...
    
    def setData(self, data: MatrixDouble ) -> None:
        """
        Cython signature: void setData(MatrixDouble & data)
        Assigns data to the internal random access container storing the data. SourceContainer must be assignable to ContainerType
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        """
        ...
    
    def key2index_0(self, pos: float ) -> float:
        """
        Cython signature: double key2index_0(double pos)
        The transformation from "outside" to "inside" coordinates
        """
        ...
    
    def index2key_0(self, pos: float ) -> float:
        """
        Cython signature: double index2key_0(double pos)
        The transformation from "inside" to "outside" coordinates
        """
        ...
    
    def key2index_1(self, pos: float ) -> float:
        """
        Cython signature: double key2index_1(double pos)
        The transformation from "outside" to "inside" coordinates
        """
        ...
    
    def index2key_1(self, pos: float ) -> float:
        """
        Cython signature: double index2key_1(double pos)
        The transformation from "inside" to "outside" coordinates
        """
        ...
    
    def getScale_0(self) -> float:
        """
        Cython signature: double getScale_0()
        """
        ...
    
    def setScale_0(self, scale: float ) -> None:
        """
        Cython signature: void setScale_0(double & scale)
        """
        ...
    
    def getScale_1(self) -> float:
        """
        Cython signature: double getScale_1()
        """
        ...
    
    def setScale_1(self, scale: float ) -> None:
        """
        Cython signature: void setScale_1(double & scale)
        """
        ...
    
    def getOffset_0(self) -> float:
        """
        Cython signature: double getOffset_0()
        Accessor. "Offset" is the point (in "outside" units) which corresponds to "Data(0,0)"
        """
        ...
    
    def setOffset_0(self, offset: float ) -> None:
        """
        Cython signature: void setOffset_0(double & offset)
        """
        ...
    
    def getOffset_1(self) -> float:
        """
        Cython signature: double getOffset_1()
        Accessor. "Offset" is the point (in "outside" units) which corresponds to "Data(0,0)"
        """
        ...
    
    def setOffset_1(self, offset: float ) -> None:
        """
        Cython signature: void setOffset_1(double & offset)
        """
        ...
    
    @overload
    def setMapping_0(self, scale: float , inside: float , outside: float ) -> None:
        """
        Cython signature: void setMapping_0(double & scale, double & inside, double & outside)
        """
        ...
    
    @overload
    def setMapping_0(self, inside_low: float , outside_low: float , inside_high: float , outside_high: float ) -> None:
        """
        Cython signature: void setMapping_0(double & inside_low, double & outside_low, double & inside_high, double & outside_high)
        """
        ...
    
    @overload
    def setMapping_1(self, scale: float , inside: float , outside: float ) -> None:
        """
        Cython signature: void setMapping_1(double & scale, double & inside, double & outside)
        """
        ...
    
    @overload
    def setMapping_1(self, inside_low: float , outside_low: float , inside_high: float , outside_high: float ) -> None:
        """
        Cython signature: void setMapping_1(double & inside_low, double & outside_low, double & inside_high, double & outside_high)
        """
        ...
    
    def getInsideReferencePoint_0(self) -> float:
        """
        Cython signature: double getInsideReferencePoint_0()
        """
        ...
    
    def getInsideReferencePoint_1(self) -> float:
        """
        Cython signature: double getInsideReferencePoint_1()
        """
        ...
    
    def getOutsideReferencePoint_0(self) -> float:
        """
        Cython signature: double getOutsideReferencePoint_0()
        """
        ...
    
    def getOutsideReferencePoint_1(self) -> float:
        """
        Cython signature: double getOutsideReferencePoint_1()
        """
        ...
    
    def supportMin_0(self) -> float:
        """
        Cython signature: double supportMin_0()
        Lower boundary of the support, in "outside" coordinates
        """
        ...
    
    def supportMin_1(self) -> float:
        """
        Cython signature: double supportMin_1()
        Lower boundary of the support, in "outside" coordinates
        """
        ...
    
    def supportMax_0(self) -> float:
        """
        Cython signature: double supportMax_0()
        Upper boundary of the support, in "outside" coordinates
        """
        ...
    
    def supportMax_1(self) -> float:
        """
        Cython signature: double supportMax_1()
        Upper boundary of the support, in "outside" coordinates
        """
        ... 


class CVMappingFile:
    """
    Cython implementation of _CVMappingFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVMappingFile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void CVMappingFile()
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , cv_mappings: CVMappings , strip_namespaces: bool ) -> None:
        """
        Cython signature: void load(const String & filename, CVMappings & cv_mappings, bool strip_namespaces)
        Loads CvMappings from the given file
        """
        ... 


class CVTerm:
    """
    Cython implementation of _CVTerm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVTerm.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVTerm()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVTerm ) -> None:
        """
        Cython signature: void CVTerm(CVTerm &)
        """
        ...
    
    def setAccession(self, accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAccession(String accession)
        Sets the accession string of the term
        """
        ...
    
    def getAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getAccession()
        Returns the accession string of the term
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the term
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the term
        """
        ...
    
    def setCVIdentifierRef(self, cv_id_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCVIdentifierRef(String cv_id_ref)
        Sets the CV identifier reference string, e.g. UO for unit obo
        """
        ...
    
    def getCVIdentifierRef(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCVIdentifierRef()
        Returns the CV identifier reference string
        """
        ...
    
    def getValue(self) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getValue()
        Returns the value of the term
        """
        ...
    
    def setValue(self, value: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setValue(DataValue value)
        Sets the value of the term
        """
        ...
    
    def setUnit(self, unit: Unit ) -> None:
        """
        Cython signature: void setUnit(Unit & unit)
        Sets the unit of the term
        """
        ...
    
    def getUnit(self) -> Unit:
        """
        Cython signature: Unit getUnit()
        Returns the unit
        """
        ...
    
    def hasValue(self) -> bool:
        """
        Cython signature: bool hasValue()
        Checks whether the term has a value
        """
        ...
    
    def hasUnit(self) -> bool:
        """
        Cython signature: bool hasUnit()
        Checks whether the term has a unit
        """
        ...
    
    def __richcmp__(self, other: CVTerm, op: int) -> Any:
        ... 


class CalibrationData:
    """
    Cython implementation of _CalibrationData

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CalibrationData.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CalibrationData()
        """
        ...
    
    @overload
    def __init__(self, in_0: CalibrationData ) -> None:
        """
        Cython signature: void CalibrationData(CalibrationData &)
        """
        ...
    
    def getMZ(self, in_0: int ) -> float:
        """
        Cython signature: double getMZ(size_t)
        Retrieve the observed m/z of the i'th calibration point
        """
        ...
    
    def getRT(self, in_0: int ) -> float:
        """
        Cython signature: double getRT(size_t)
        Retrieve the observed RT of the i'th calibration point
        """
        ...
    
    def getIntensity(self, in_0: int ) -> float:
        """
        Cython signature: double getIntensity(size_t)
        Retrieve the intensity of the i'th calibration point
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        Number of calibration points
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Returns `True` if there are no peaks
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        Remove all calibration points
        """
        ...
    
    def setUsePPM(self, in_0: bool ) -> None:
        """
        Cython signature: void setUsePPM(bool)
        """
        ...
    
    def usePPM(self) -> bool:
        """
        Cython signature: bool usePPM()
        Current error unit (ppm or Th)
        """
        ...
    
    def insertCalibrationPoint(self, rt: float , mz_obs: float , intensity: float , mz_ref: float , weight: float , group: int ) -> None:
        """
        Cython signature: void insertCalibrationPoint(double rt, double mz_obs, float intensity, double mz_ref, double weight, int group)
        """
        ...
    
    def getNrOfGroups(self) -> int:
        """
        Cython signature: size_t getNrOfGroups()
        Number of peak groups (can be 0)
        """
        ...
    
    def getError(self, in_0: int ) -> float:
        """
        Cython signature: double getError(size_t)
        Retrieve the error for i'th calibrant in either ppm or Th (depending on usePPM())
        """
        ...
    
    def getRefMZ(self, in_0: int ) -> float:
        """
        Cython signature: double getRefMZ(size_t)
        Retrieve the theoretical m/z of the i'th calibration point
        """
        ...
    
    def getWeight(self, in_0: int ) -> float:
        """
        Cython signature: double getWeight(size_t)
        Retrieve the weight of the i'th calibration point
        """
        ...
    
    def getGroup(self, i: int ) -> int:
        """
        Cython signature: int getGroup(size_t i)
        Retrieve the group of the i'th calibration point
        """
        ...
    
    def median(self, in_0: float , in_1: float ) -> CalibrationData:
        """
        Cython signature: CalibrationData median(double, double)
        Compute the median in the given RT range for every peak group
        """
        ...
    
    def sortByRT(self) -> None:
        """
        Cython signature: void sortByRT()
        Sort calibration points by RT, to allow for valid RT chunking
        """
        ...
    
    getMetaValues: __static_CalibrationData_getMetaValues 


class Compomer:
    """
    Cython implementation of _Compomer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Compomer.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Compomer()
        """
        ...
    
    @overload
    def __init__(self, in_0: Compomer ) -> None:
        """
        Cython signature: void Compomer(Compomer &)
        """
        ...
    
    def add(self, a: Adduct , side: int ) -> None:
        """
        Cython signature: void add(Adduct & a, unsigned int side)
        """
        ...
    
    def isConflicting(self, cmp: Compomer , side_this: int , side_other: int ) -> bool:
        """
        Cython signature: bool isConflicting(Compomer & cmp, unsigned int side_this, unsigned int side_other)
        """
        ...
    
    def setID(self, id: int ) -> None:
        """
        Cython signature: void setID(size_t id)
        Sets an Id which allows unique identification of a compomer
        """
        ...
    
    def getID(self) -> int:
        """
        Cython signature: size_t getID()
        Returns Id which allows unique identification of this compomer
        """
        ...
    
    def getNetCharge(self) -> int:
        """
        Cython signature: int getNetCharge()
        Net charge of compomer (i.e. difference between left and right side of compomer)
        """
        ...
    
    def getMass(self) -> float:
        """
        Cython signature: double getMass()
        Mass of all contained adducts
        """
        ...
    
    def getPositiveCharges(self) -> int:
        """
        Cython signature: int getPositiveCharges()
        Summed positive charges of contained adducts
        """
        ...
    
    def getNegativeCharges(self) -> int:
        """
        Cython signature: int getNegativeCharges()
        Summed negative charges of contained adducts
        """
        ...
    
    def getLogP(self) -> float:
        """
        Cython signature: double getLogP()
        Returns the log probability
        """
        ...
    
    def getRTShift(self) -> float:
        """
        Cython signature: double getRTShift()
        Returns the log probability
        """
        ...
    
    @overload
    def getAdductsAsString(self, ) -> Union[bytes, str, String]:
        """
        Cython signature: String getAdductsAsString()
        Get adducts with their abundance as compact string for both sides
        """
        ...
    
    @overload
    def getAdductsAsString(self, side: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String getAdductsAsString(unsigned int side)
        Get adducts with their abundance as compact string (amounts are absolute unless side=BOTH)
        """
        ...
    
    def isSingleAdduct(self, a: Adduct , side: int ) -> bool:
        """
        Cython signature: bool isSingleAdduct(Adduct & a, unsigned int side)
        Check if Compomer only contains a single adduct on side @p side
        """
        ...
    
    @overload
    def removeAdduct(self, a: Adduct ) -> Compomer:
        """
        Cython signature: Compomer removeAdduct(Adduct & a)
        Remove ALL instances of the given adduct
        """
        ...
    
    @overload
    def removeAdduct(self, a: Adduct , side: int ) -> Compomer:
        """
        Cython signature: Compomer removeAdduct(Adduct & a, unsigned int side)
        """
        ...
    
    def getLabels(self, side: int ) -> List[bytes]:
        """
        Cython signature: StringList getLabels(unsigned int side)
        Returns the adduct labels from parameter(side) given. (LEFT or RIGHT)
        """
        ... 


class ConsensusXMLFile:
    """
    Cython implementation of _ConsensusXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusXMLFile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusXMLFile()
        """
        ...
    
    def load(self, in_0: Union[bytes, str, String] , in_1: ConsensusMap ) -> None:
        """
        Cython signature: void load(String, ConsensusMap &)
        Loads a consensus map from file and calls updateRanges
        """
        ...
    
    def store(self, in_0: Union[bytes, str, String] , in_1: ConsensusMap ) -> None:
        """
        Cython signature: void store(String, ConsensusMap &)
        Stores a consensus map to file
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        Mutable access to the options for loading/storing
        """
        ... 


class ContactPerson:
    """
    Cython implementation of _ContactPerson

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ContactPerson.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ContactPerson()
        """
        ...
    
    @overload
    def __init__(self, in_0: ContactPerson ) -> None:
        """
        Cython signature: void ContactPerson(ContactPerson &)
        """
        ...
    
    def getFirstName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFirstName()
        Returns the first name of the person
        """
        ...
    
    def setFirstName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFirstName(String name)
        Sets the first name of the person
        """
        ...
    
    def getLastName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getLastName()
        Returns the last name of the person
        """
        ...
    
    def setLastName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLastName(String name)
        Sets the last name of the person
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the full name of the person (gets split into first and last name internally)
        """
        ...
    
    def getInstitution(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getInstitution()
        Returns the affiliation
        """
        ...
    
    def setInstitution(self, institution: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setInstitution(String institution)
        Sets the affiliation
        """
        ...
    
    def getEmail(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getEmail()
        Returns the email address
        """
        ...
    
    def setEmail(self, email: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setEmail(String email)
        Sets the email address
        """
        ...
    
    def getURL(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getURL()
        Returns the URL associated with the contact person (e.g., the institute webpage
        """
        ...
    
    def setURL(self, email: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setURL(String email)
        Sets the URL associated with the contact person (e.g., the institute webpage
        """
        ...
    
    def getAddress(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getAddress()
        Returns the address
        """
        ...
    
    def setAddress(self, email: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAddress(String email)
        Sets the address
        """
        ...
    
    def getContactInfo(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getContactInfo()
        Returns miscellaneous info about the contact person
        """
        ...
    
    def setContactInfo(self, contact_info: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setContactInfo(String contact_info)
        Sets miscellaneous info about the contact person
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: ContactPerson, op: int) -> Any:
        ... 


class DataValue:
    """
    Cython implementation of _DataValue

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DataValue.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DataValue()
        """
        ...
    
    @overload
    def __init__(self, in_0: DataValue ) -> None:
        """
        Cython signature: void DataValue(DataValue &)
        """
        ...
    
    @overload
    def __init__(self, in_0: bytes ) -> None:
        """
        Cython signature: void DataValue(char *)
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void DataValue(const String &)
        """
        ...
    
    @overload
    def __init__(self, in_0: int ) -> None:
        """
        Cython signature: void DataValue(int)
        """
        ...
    
    @overload
    def __init__(self, in_0: float ) -> None:
        """
        Cython signature: void DataValue(double)
        """
        ...
    
    @overload
    def __init__(self, in_0: List[bytes] ) -> None:
        """
        Cython signature: void DataValue(StringList)
        """
        ...
    
    @overload
    def __init__(self, in_0: List[int] ) -> None:
        """
        Cython signature: void DataValue(IntList)
        """
        ...
    
    @overload
    def __init__(self, in_0: List[float] ) -> None:
        """
        Cython signature: void DataValue(DoubleList)
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void DataValue(ParamValue)
        """
        ...
    
    def toStringList(self) -> List[bytes]:
        """
        Cython signature: StringList toStringList()
        """
        ...
    
    def toDoubleList(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] toDoubleList()
        """
        ...
    
    def toIntList(self) -> List[int]:
        """
        Cython signature: libcpp_vector[int] toIntList()
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        """
        ...
    
    def toBool(self) -> bool:
        """
        Cython signature: bool toBool()
        """
        ...
    
    def valueType(self) -> int:
        """
        Cython signature: DataType valueType()
        """
        ...
    
    def isEmpty(self) -> int:
        """
        Cython signature: int isEmpty()
        """
        ...
    
    def getUnitType(self) -> int:
        """
        Cython signature: UnitType getUnitType()
        """
        ...
    
    def setUnitType(self, u: int ) -> None:
        """
        Cython signature: void setUnitType(UnitType u)
        """
        ...
    
    def hasUnit(self) -> bool:
        """
        Cython signature: bool hasUnit()
        """
        ...
    
    def getUnit(self) -> int:
        """
        Cython signature: int getUnit()
        """
        ...
    
    def setUnit(self, unit_id: int ) -> None:
        """
        Cython signature: void setUnit(int unit_id)
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        """
        ... 


class Date:
    """
    Cython implementation of _Date

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Date.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Date()
        """
        ...
    
    @overload
    def __init__(self, in_0: Date ) -> None:
        """
        Cython signature: void Date(Date &)
        """
        ...
    
    def set(self, date: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void set(const String & date)
        """
        ...
    
    def today(self) -> Date:
        """
        Cython signature: Date today()
        """
        ...
    
    def get(self) -> Union[bytes, str, String]:
        """
        Cython signature: String get()
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ... 


class DigestionEnzyme:
    """
    Cython implementation of _DigestionEnzyme

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DigestionEnzyme.html>`_

      Base class for digestion enzymes
    """
    
    @overload
    def __init__(self, in_0: DigestionEnzyme ) -> None:
        """
        Cython signature: void DigestionEnzyme(DigestionEnzyme &)
        """
        ...
    
    @overload
    def __init__(self, name: Union[bytes, str, String] , cleavage_regex: Union[bytes, str, String] , synonyms: Set[bytes] , regex_description: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void DigestionEnzyme(const String & name, const String & cleavage_regex, libcpp_set[String] & synonyms, String regex_description)
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String & name)
        Sets the name of the enzyme
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the enzyme
        """
        ...
    
    def setSynonyms(self, synonyms: Set[bytes] ) -> None:
        """
        Cython signature: void setSynonyms(libcpp_set[String] & synonyms)
        Sets the synonyms
        """
        ...
    
    def addSynonym(self, synonym: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addSynonym(const String & synonym)
        Adds a synonym
        """
        ...
    
    def getSynonyms(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getSynonyms()
        Returns the synonyms
        """
        ...
    
    def setRegEx(self, cleavage_regex: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setRegEx(const String & cleavage_regex)
        Sets the cleavage regex
        """
        ...
    
    def getRegEx(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getRegEx()
        Returns the cleavage regex
        """
        ...
    
    def setRegExDescription(self, value: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setRegExDescription(const String & value)
        Sets the regex description
        """
        ...
    
    def getRegExDescription(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getRegExDescription()
        Returns the regex description
        """
        ...
    
    def setValueFromFile(self, key: Union[bytes, str, String] , value: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool setValueFromFile(String key, String value)
        Sets the value of a member variable based on an entry from an input file
        """
        ...
    
    def __richcmp__(self, other: DigestionEnzyme, op: int) -> Any:
        ... 


class __DigestionFilter:
    """
    Cython implementation of _DigestionFilter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DigestionFilter.html>`_
    """
    
    digestion_: ProteaseDigestion
    
    ignore_missed_cleavages_: bool
    
    methionine_cleavage_: bool
    
    def __init__(self, entries: List[FASTAEntry] , digestion: ProteaseDigestion , ignore_missed_cleavages: bool , methionine_cleavage: bool ) -> None:
        """
        Cython signature: void DigestionFilter(libcpp_vector[FASTAEntry] & entries, ProteaseDigestion & digestion, bool ignore_missed_cleavages, bool methionine_cleavage)
        """
        ...
    
    def filterPeptideEvidences(self, peptides: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void filterPeptideEvidences(libcpp_vector[PeptideIdentification] & peptides)
        """
        ... 


class Element:
    """
    Cython implementation of _Element

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Element.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Element()
        """
        ...
    
    @overload
    def __init__(self, in_0: Element ) -> None:
        """
        Cython signature: void Element(Element &)
        """
        ...
    
    @overload
    def __init__(self, name: Union[bytes, str, String] , symbol: Union[bytes, str, String] , atomic_number: int , average_weight: float , mono_weight: float , isotopes: IsotopeDistribution ) -> None:
        """
        Cython signature: void Element(String name, String symbol, unsigned int atomic_number, double average_weight, double mono_weight, IsotopeDistribution isotopes)
        """
        ...
    
    def setAtomicNumber(self, atomic_number: int ) -> None:
        """
        Cython signature: void setAtomicNumber(unsigned int atomic_number)
        Sets unique atomic number
        """
        ...
    
    def getAtomicNumber(self) -> int:
        """
        Cython signature: unsigned int getAtomicNumber()
        Returns the unique atomic number
        """
        ...
    
    def setAverageWeight(self, weight: float ) -> None:
        """
        Cython signature: void setAverageWeight(double weight)
        Sets the average weight of the element
        """
        ...
    
    def getAverageWeight(self) -> float:
        """
        Cython signature: double getAverageWeight()
        Returns the average weight of the element
        """
        ...
    
    def setMonoWeight(self, weight: float ) -> None:
        """
        Cython signature: void setMonoWeight(double weight)
        Sets the mono isotopic weight of the element
        """
        ...
    
    def getMonoWeight(self) -> float:
        """
        Cython signature: double getMonoWeight()
        Returns the mono isotopic weight of the element
        """
        ...
    
    def setIsotopeDistribution(self, isotopes: IsotopeDistribution ) -> None:
        """
        Cython signature: void setIsotopeDistribution(IsotopeDistribution isotopes)
        Sets the isotope distribution of the element
        """
        ...
    
    def getIsotopeDistribution(self) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution getIsotopeDistribution()
        Returns the isotope distribution of the element
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the element
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the element
        """
        ...
    
    def setSymbol(self, symbol: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSymbol(String symbol)
        Sets symbol of the element
        """
        ...
    
    def getSymbol(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSymbol()
        Returns symbol of the element
        """
        ... 


class FASTAEntry:
    """
    Cython implementation of _FASTAEntry

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FASTAEntry.html>`_
    """
    
    identifier: Union[bytes, str, String]
    
    description: Union[bytes, str, String]
    
    sequence: Union[bytes, str, String]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FASTAEntry()
        """
        ...
    
    @overload
    def __init__(self, in_0: FASTAEntry ) -> None:
        """
        Cython signature: void FASTAEntry(FASTAEntry)
        """
        ...
    
    def headerMatches(self, rhs: FASTAEntry ) -> bool:
        """
        Cython signature: bool headerMatches(const FASTAEntry & rhs)
        """
        ...
    
    def sequenceMatches(self, rhs: FASTAEntry ) -> bool:
        """
        Cython signature: bool sequenceMatches(const FASTAEntry & rhs)
        """
        ... 


class FASTAFile:
    """
    Cython implementation of _FASTAFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FASTAFile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FASTAFile()
        This class serves for reading in and writing FASTA files
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , data: List[FASTAEntry] ) -> None:
        """
        Cython signature: void load(const String & filename, libcpp_vector[FASTAEntry] & data)
        Loads a FASTA file given by 'filename' and stores the information in 'data'
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , data: List[FASTAEntry] ) -> None:
        """
        Cython signature: void store(const String & filename, libcpp_vector[FASTAEntry] & data)
        Stores the data given by 'data' at the file 'filename'
        """
        ...
    
    def readStart(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void readStart(const String & filename)
        Prepares a FASTA file given by 'filename' for streamed reading using readNext()
        
        :raises:
            Exception:FileNotFound is thrown if the file does not exists
        :raises:
            Exception:ParseError is thrown if the file does not suit to the standard
        Reads the next FASTA entry from file
        
        If you want to read all entries in one go, use load()
        
        :return: true if entry was read; false if eof was reached
        :raises:
            Exception:FileNotFound is thrown if the file does not exists
        :raises:
            Exception:ParseError is thrown if the file does not suit to the standard
        """
        ...
    
    def readNext(self, protein: FASTAEntry ) -> bool:
        """
        Cython signature: bool readNext(FASTAEntry & protein)
        Reads the next FASTA entry from file
        
        If you want to read all entries in one go, use load()
        
        :return: true if entry was read; false if eof was reached
        :raises:
            Exception:FileNotFound is thrown if the file does not exists
        :raises:
            Exception:ParseError is thrown if the file does not suit to the standard
        """
        ...
    
    def atEnd(self) -> bool:
        """
        Cython signature: bool atEnd()
        Boolean function to check if streams is at end of file
        """
        ...
    
    def writeStart(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void writeStart(const String & filename)
        Prepares a FASTA file given by 'filename' for streamed writing using writeNext()
        
        :raises:
            Exception:UnableToCreateFile is thrown if the process is not able to write to the file (disk full?)
        Stores the data given by `protein`. Call writeStart() once before calling writeNext()
        
        Call writeEnd() when done to close the file!
        
        :raises:
            Exception:UnableToCreateFile is thrown if the process is not able to write to the file (disk full?)
        """
        ...
    
    def writeNext(self, protein: FASTAEntry ) -> None:
        """
        Cython signature: void writeNext(const FASTAEntry & protein)
        Stores the data given by `protein`. Call writeStart() once before calling writeNext()
        
        Call writeEnd() when done to close the file!
        
        :raises:
            Exception:UnableToCreateFile is thrown if the process is not able to write to the file (disk full?)
        """
        ...
    
    def writeEnd(self) -> None:
        """
        Cython signature: void writeEnd()
        Closes the file (flush). Called implicitly when FASTAFile object does out of scope
        """
        ... 


class FeatureFinderMultiplexAlgorithm:
    """
    Cython implementation of _FeatureFinderMultiplexAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureFinderMultiplexAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureFinderMultiplexAlgorithm()
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureFinderMultiplexAlgorithm ) -> None:
        """
        Cython signature: void FeatureFinderMultiplexAlgorithm(FeatureFinderMultiplexAlgorithm &)
        """
        ...
    
    def run(self, exp: MSExperiment , progress: bool ) -> None:
        """
        Cython signature: void run(MSExperiment & exp, bool progress)
        Main method for feature detection
        """
        ...
    
    def getFeatureMap(self) -> FeatureMap:
        """
        Cython signature: FeatureMap getFeatureMap()
        """
        ...
    
    def getConsensusMap(self) -> ConsensusMap:
        """
        Cython signature: ConsensusMap getConsensusMap()
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class FeatureXMLFile:
    """
    Cython implementation of _FeatureXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureXMLFile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureXMLFile()
        This class provides Input/Output functionality for feature maps
        """
        ...
    
    def load(self, in_0: Union[bytes, str, String] , in_1: FeatureMap ) -> None:
        """
        Cython signature: void load(String, FeatureMap &)
        Loads the file with name `filename` into `map` and calls updateRanges()
        """
        ...
    
    def store(self, in_0: Union[bytes, str, String] , in_1: FeatureMap ) -> None:
        """
        Cython signature: void store(String, FeatureMap &)
        Stores the map `feature_map` in file with name `filename`
        """
        ...
    
    def getOptions(self) -> FeatureFileOptions:
        """
        Cython signature: FeatureFileOptions getOptions()
        Access to the options for loading/storing
        """
        ...
    
    def setOptions(self, in_0: FeatureFileOptions ) -> None:
        """
        Cython signature: void setOptions(FeatureFileOptions)
        Setter for options for loading/storing
        """
        ...
    
    def loadSize(self, path: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t loadSize(String path)
        """
        ... 


class FileHandler:
    """
    Cython implementation of _FileHandler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FileHandler.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FileHandler()
        """
        ...
    
    def loadExperiment(self, in_0: Union[bytes, str, String] , in_1: MSExperiment ) -> None:
        """
        Cython signature: void loadExperiment(String, MSExperiment &)
        Loads a file into an MSExperiment
        
        
        :param filename: The file name of the file to load
        :param exp: The experiment to load the data into
        :param force_type: Forces to load the file with that file type. If no type is forced, it is determined from the extension (or from the content if that fails)
        :param log: Progress logging mode
        :param rewrite_source_file: Set's the SourceFile name and path to the current file. Note that this looses the link to the primary MS run the file originated from
        :param compute_hash: If source files are rewritten, this flag triggers a recomputation of hash values. A SHA1 string gets stored in the checksum member of SourceFile
        :return: true if the file could be loaded, false otherwise
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ...
    
    def storeExperiment(self, in_0: Union[bytes, str, String] , in_1: MSExperiment ) -> None:
        """
        Cython signature: void storeExperiment(String, MSExperiment)
        Stores an MSExperiment to a file\n
        
        The file type to store the data in is determined by the file name. Supported formats for storing are mzML, mzXML, mzData and DTA2D. If the file format cannot be determined from the file name, the mzML format is used
        
        
        :param filename: The name of the file to store the data in
        :param exp: The experiment to store
        :param log: Progress logging mode
        :raises:
          Exception: UnableToCreateFile is thrown if the file could not be written
        """
        ...
    
    def loadFeatures(self, in_0: Union[bytes, str, String] , in_1: FeatureMap ) -> None:
        """
        Cython signature: void loadFeatures(String, FeatureMap &)
        Loads a file into a FeatureMap
        
        
        :param filename: The file name of the file to load
        :param map: The FeatureMap to load the data into
        :param force_type: Forces to load the file with that file type. If no type is forced, it is determined from the extension (or from the content if that fails)
        :return: true if the file could be loaded, false otherwise
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        Access to the options for loading/storing
        """
        ...
    
    def setOptions(self, in_0: PeakFileOptions ) -> None:
        """
        Cython signature: void setOptions(PeakFileOptions)
        Sets options for loading/storing
        """
        ...
    
    computeFileHash: __static_FileHandler_computeFileHash
    
    getType: __static_FileHandler_getType
    
    getTypeByContent: __static_FileHandler_getTypeByContent
    
    getTypeByFileName: __static_FileHandler_getTypeByFileName
    
    hasValidExtension: __static_FileHandler_hasValidExtension
    
    isSupported: __static_FileHandler_isSupported
    
    stripExtension: __static_FileHandler_stripExtension
    
    swapExtension: __static_FileHandler_swapExtension 


class IBSpectraFile:
    """
    Cython implementation of _IBSpectraFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IBSpectraFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IBSpectraFile()
        Implements the export of consensusmaps into the IBSpectra format used by isobar to load quantification results
        """
        ...
    
    @overload
    def __init__(self, in_0: IBSpectraFile ) -> None:
        """
        Cython signature: void IBSpectraFile(IBSpectraFile &)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , cm: ConsensusMap ) -> None:
        """
        Cython signature: void store(const String & filename, ConsensusMap & cm)
        Writes the contents of the ConsensusMap cm into the file named by filename
        
        
        :param filename: The name of the file where the contents of cm should be stored
        :param cm: The ConsensusMap that should be exported to filename
        :raises:
          Exception: InvalidParameter if the ConsensusMap does not hold the result of an isobaric quantification experiment (e.g., itraq)
        """
        ... 


class IDFilter:
    """
    Cython implementation of _IDFilter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IDFilter.html>`_

    Finds the best-scoring hit in a vector of peptide or protein identifications\n
    
    This class provides functions for filtering collections of peptide or protein identifications according to various criteria.
    It also contains helper functions and classes (functors that implement predicates) that are used in this context.\n
    
    The filter functions modify their inputs, rather than creating filtered copies.\n
    
    Most filters work on the hit level, i.e. they remove peptide or protein hits from peptide or protein identifications (IDs).
    A few filters work on the ID level instead, i.e. they remove peptide or protein IDs from vectors thereof.
    Independent of this, the inputs for all filter functions are vectors of IDs, because the data most often comes in this form.
    This design also allows many helper objects to be set up only once per vector, rather than once per ID.\n
    
    The filter functions for vectors of peptide/protein IDs do not include clean-up steps (e.g. removal of IDs without hits, reassignment of hit ranks, ...).
    They only carry out their specific filtering operations.
    This is so filters can be chained without having to repeat clean-up operations.
    The group of clean-up functions provides helpers that are useful to ensure data integrity after filters have been applied, but it is up to the individual developer to use them when necessary.\n
    
    The filter functions for MS/MS experiments do include clean-up steps, because they filter peptide and protein IDs in conjunction and potential contradictions between the two must be eliminated.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IDFilter()
        """
        ...
    
    @overload
    def __init__(self, in_0: IDFilter ) -> None:
        """
        Cython signature: void IDFilter(IDFilter &)
        """
        ...
    
    @overload
    def countHits(self, identifications: List[PeptideIdentification] ) -> int:
        """
        Cython signature: size_t countHits(libcpp_vector[PeptideIdentification] identifications)
        Returns the total number of peptide hits in a vector of peptide identifications
        """
        ...
    
    @overload
    def countHits(self, identifications: List[ProteinIdentification] ) -> int:
        """
        Cython signature: size_t countHits(libcpp_vector[ProteinIdentification] identifications)
        Returns the total number of protein hits in a vector of protein identifications
        """
        ...
    
    @overload
    def getBestHit(self, identifications: List[PeptideIdentification] , assume_sorted: bool , best_hit: PeptideHit ) -> bool:
        """
        Cython signature: bool getBestHit(libcpp_vector[PeptideIdentification] identifications, bool assume_sorted, PeptideHit & best_hit)
        Finds the best-scoring hit in a vector of peptide or protein identifications\n
        
        If there are several hits with the best score, the first one is taken
        
        
        :param identifications: Vector of peptide or protein IDs, each containing one or more (peptide/protein) hits
        :param assume_sorted: Are hits sorted by score (best score first) already? This allows for faster query, since only the first hit needs to be looked at
        :param best_hit: Contains the best hit if successful in a vector of peptide identifications
        :return: true if a hit was present, false otherwise
        """
        ...
    
    @overload
    def getBestHit(self, identifications: List[ProteinIdentification] , assume_sorted: bool , best_hit: ProteinHit ) -> bool:
        """
        Cython signature: bool getBestHit(libcpp_vector[ProteinIdentification] identifications, bool assume_sorted, ProteinHit & best_hit)
        Finds the best-scoring hit in a vector of peptide or protein identifications
        
        If there are several hits with the best score, the first one is taken
        
        
        :param identifications: Vector of peptide or protein IDs, each containing one or more (peptide/protein) hits
        :param assume_sorted: Are hits sorted by score (best score first) already? This allows for faster query, since only the first hit needs to be looked at
        :param best_hit: Contains the best hit if successful in a vector of protein identifications
        :return: true if a hit was present, false otherwise
        """
        ...
    
    def extractPeptideSequences(self, peptides: List[PeptideIdentification] , sequences: Set[bytes] , ignore_mods: bool ) -> None:
        """
        Cython signature: void extractPeptideSequences(libcpp_vector[PeptideIdentification] & peptides, libcpp_set[String] & sequences, bool ignore_mods)
        Extracts all unique peptide sequences from a list of peptide IDs
        
        
        :param peptides:
        :param ignore_mods: Boolean operator default to false in case of any modifications in sequences during extraction
        :return: Sequences
        """
        ...
    
    @overload
    def updateHitRanks(self, identifications: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void updateHitRanks(libcpp_vector[PeptideIdentification] & identifications)
        Updates the hit ranks on all peptide or protein IDs
        """
        ...
    
    @overload
    def updateHitRanks(self, identifications: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void updateHitRanks(libcpp_vector[ProteinIdentification] & identifications)
        Updates the hit ranks on all peptide or protein IDs
        """
        ...
    
    def removeUnreferencedProteins(self, proteins: List[ProteinIdentification] , peptides: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void removeUnreferencedProteins(libcpp_vector[ProteinIdentification] & proteins, libcpp_vector[PeptideIdentification] & peptides)
        Removes protein hits from the protein IDs in a 'cmap' that are not referenced by a peptide in the features or if requested in the unassigned peptide list
        """
        ...
    
    def updateProteinReferences(self, peptides: List[PeptideIdentification] , proteins: List[ProteinIdentification] , remove_peptides_without_reference: bool ) -> None:
        """
        Cython signature: void updateProteinReferences(libcpp_vector[PeptideIdentification] & peptides, libcpp_vector[ProteinIdentification] & proteins, bool remove_peptides_without_reference)
        Removes references to missing proteins. Only PeptideEvidence entries that reference protein hits in 'proteins' are kept in the peptide hits
        """
        ...
    
    def updateProteinGroups(self, groups: List[ProteinGroup] , hits: List[ProteinHit] ) -> bool:
        """
        Cython signature: bool updateProteinGroups(libcpp_vector[ProteinGroup] & groups, libcpp_vector[ProteinHit] & hits)
        Update protein groups after protein hits were filtered
        
        
        :param groups: Input/output protein groups
        :param hits: Available protein hits (all others are removed from the groups)
        :return: Returns whether the groups are still valid (which is the case if only whole groups, if any, were removed)
        """
        ...
    
    @overload
    def removeEmptyIdentifications(self, ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void removeEmptyIdentifications(libcpp_vector[PeptideIdentification] & ids)
        Removes peptide or protein identifications that have no hits in them
        """
        ...
    
    @overload
    def removeEmptyIdentifications(self, ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void removeEmptyIdentifications(libcpp_vector[ProteinIdentification] & ids)
        Removes peptide or protein identifications that have no hits in them
        """
        ...
    
    @overload
    def filterHitsByScore(self, ids: List[PeptideIdentification] , threshold_score: float ) -> None:
        """
        Cython signature: void filterHitsByScore(libcpp_vector[PeptideIdentification] & ids, double threshold_score)
        Filters peptide or protein identifications according to the score of the hits. The score orientation has to be set to higherscorebetter in each PeptideIdentification. Only peptide/protein hits with a score at least as good as 'threshold_score' are kept
        """
        ...
    
    @overload
    def filterHitsByScore(self, ids: List[ProteinIdentification] , threshold_score: float ) -> None:
        """
        Cython signature: void filterHitsByScore(libcpp_vector[ProteinIdentification] & ids, double threshold_score)
        Filters peptide or protein identifications according to the score of the hits. The score orientation has to be set to higherscorebetter in each PeptideIdentification/ProteinIdentifiation. Only peptide/protein hits with a score at least as good as 'threshold_score' are kept
        """
        ...
    
    @overload
    def filterHitsByScore(self, experiment: MSExperiment , peptide_threshold_score: float , protein_threshold_score: float ) -> None:
        """
        Cython signature: void filterHitsByScore(MSExperiment & experiment, double peptide_threshold_score, double protein_threshold_score)
        Filters an MS/MS experiment according to score thresholds
        """
        ...
    
    def keepNBestSpectra(self, peptides: List[PeptideIdentification] , n: int ) -> None:
        """
        Cython signature: void keepNBestSpectra(libcpp_vector[PeptideIdentification] & peptides, size_t n)
        Filter identifications by "N best" PeptideIdentification objects (better PeptideIdentification means better [best] PeptideHit than other)
        """
        ...
    
    @overload
    def keepNBestHits(self, ids: List[PeptideIdentification] , n: int ) -> None:
        """
        Cython signature: void keepNBestHits(libcpp_vector[PeptideIdentification] & ids, size_t n)
        """
        ...
    
    @overload
    def keepNBestHits(self, ids: List[ProteinIdentification] , n: int ) -> None:
        """
        Cython signature: void keepNBestHits(libcpp_vector[ProteinIdentification] & ids, size_t n)
        """
        ...
    
    @overload
    def keepNBestHits(self, experiment: MSExperiment , n: int ) -> None:
        """
        Cython signature: void keepNBestHits(MSExperiment & experiment, size_t n)
        Filters an MS/MS experiment by keeping the N best peptide hits for every spectrum
        """
        ...
    
    @overload
    def filterHitsByRank(self, ids: List[PeptideIdentification] , min_rank: int , max_rank: int ) -> None:
        """
        Cython signature: void filterHitsByRank(libcpp_vector[PeptideIdentification] & ids, size_t min_rank, size_t max_rank)
        Filters peptide or protein identifications according to the ranking of the hits\n
        
        The hits between 'min_rank' and 'max_rank' (both inclusive) in each ID are kept
        Counting starts at 1, i.e. the best (highest/lowest scoring) hit has rank 1
        The ranks are (re-)computed before filtering
        'max_rank' is ignored if it is smaller than 'min_rank'
        
        
        Note: There may be several hits with the same rank in a peptide or protein ID (if the scores are the same). This method is useful if a range of higher hits is needed for decoy fairness analysis
        """
        ...
    
    @overload
    def filterHitsByRank(self, ids: List[ProteinIdentification] , min_rank: int , max_rank: int ) -> None:
        """
        Cython signature: void filterHitsByRank(libcpp_vector[ProteinIdentification] & ids, size_t min_rank, size_t max_rank)
        Filters peptide or protein identifications according to the ranking of the hits\n
        
        The hits between 'min_rank' and 'max_rank' (both inclusive) in each ID are kept
        Counting starts at 1, i.e. the best (highest/lowest scoring) hit has rank 1
        The ranks are (re-)computed before filtering
        'max_rank' is ignored if it is smaller than 'min_rank'
        
        
        Note: There may be several hits with the same rank in a peptide or protein ID (if the scores are the same). This method is useful if a range of higher hits is needed for decoy fairness analysis
        """
        ...
    
    @overload
    def removeDecoyHits(self, ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void removeDecoyHits(libcpp_vector[PeptideIdentification] & ids)
        Removes hits annotated as decoys from peptide or protein identifications. Checks for meta values named "target_decoy" and "isDecoy", and removes protein/peptide hits if the values are "decoy" and "true", respectively
        """
        ...
    
    @overload
    def removeDecoyHits(self, ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void removeDecoyHits(libcpp_vector[ProteinIdentification] & ids)
        Removes hits annotated as decoys from peptide or protein identifications. Checks for meta values named "target_decoy" and "isDecoy", and removes protein/peptide hits if the values are "decoy" and "true", respectively
        """
        ...
    
    @overload
    def removeHitsMatchingProteins(self, ids: List[PeptideIdentification] , accessions: Set[bytes] ) -> None:
        """
        Cython signature: void removeHitsMatchingProteins(libcpp_vector[PeptideIdentification] & ids, libcpp_set[String] accessions)
        Filters peptide or protein identifications according to the given proteins (negative)
        """
        ...
    
    @overload
    def removeHitsMatchingProteins(self, ids: List[ProteinIdentification] , accessions: Set[bytes] ) -> None:
        """
        Cython signature: void removeHitsMatchingProteins(libcpp_vector[ProteinIdentification] & ids, libcpp_set[String] accessions)
        Filters peptide or protein identifications according to the given proteins (negative)
        """
        ...
    
    @overload
    def keepHitsMatchingProteins(self, ids: List[PeptideIdentification] , accessions: Set[bytes] ) -> None:
        """
        Cython signature: void keepHitsMatchingProteins(libcpp_vector[PeptideIdentification] & ids, libcpp_set[String] accessions)
        Filters peptide or protein identifications according to the given proteins (positive)
        """
        ...
    
    @overload
    def keepHitsMatchingProteins(self, ids: List[ProteinIdentification] , accessions: Set[bytes] ) -> None:
        """
        Cython signature: void keepHitsMatchingProteins(libcpp_vector[ProteinIdentification] & ids, libcpp_set[String] accessions)
        Filters peptide or protein identifications according to the given proteins (positive)
        """
        ...
    
    @overload
    def keepHitsMatchingProteins(self, experiment: MSExperiment , proteins: List[FASTAEntry] ) -> None:
        """
        Cython signature: void keepHitsMatchingProteins(MSExperiment & experiment, libcpp_vector[FASTAEntry] & proteins)
        """
        ...
    
    def keepBestPeptideHits(self, peptides: List[PeptideIdentification] , strict: bool ) -> None:
        """
        Cython signature: void keepBestPeptideHits(libcpp_vector[PeptideIdentification] & peptides, bool strict)
        Filters peptide identifications keeping only the single best-scoring hit per ID
        
        
        :param peptides: Input/output
        :param strict: If set, keep the best hit only if its score is unique - i.e. ties are not allowed. (Otherwise all hits with the best score is kept.)
        """
        ...
    
    def filterPeptidesByLength(self, peptides: List[PeptideIdentification] , min_length: int , max_length: int ) -> None:
        """
        Cython signature: void filterPeptidesByLength(libcpp_vector[PeptideIdentification] & peptides, size_t min_length, size_t max_length)
        Filters peptide identifications according to peptide sequence length
        """
        ...
    
    def filterPeptidesByCharge(self, peptides: List[PeptideIdentification] , min_charge: int , max_charge: int ) -> None:
        """
        Cython signature: void filterPeptidesByCharge(libcpp_vector[PeptideIdentification] & peptides, size_t min_charge, size_t max_charge)
        Filters peptide identifications according to charge state
        """
        ...
    
    def filterPeptidesByRT(self, peptides: List[PeptideIdentification] , min_rt: int , max_rt: int ) -> None:
        """
        Cython signature: void filterPeptidesByRT(libcpp_vector[PeptideIdentification] & peptides, size_t min_rt, size_t max_rt)
        Filters peptide identifications by precursor RT, keeping only IDs in the given range
        """
        ...
    
    def filterPeptidesByMZ(self, peptides: List[PeptideIdentification] , min_mz: int , max_mz: int ) -> None:
        """
        Cython signature: void filterPeptidesByMZ(libcpp_vector[PeptideIdentification] & peptides, size_t min_mz, size_t max_mz)
        Filters peptide identifications by precursor m/z, keeping only IDs in the given range
        """
        ...
    
    def filterPeptidesByMZError(self, peptides: List[PeptideIdentification] , mass_error: float , unit_ppm: bool ) -> None:
        """
        Cython signature: void filterPeptidesByMZError(libcpp_vector[PeptideIdentification] & peptides, double mass_error, bool unit_ppm)
        Filter peptide identifications according to mass deviation
        """
        ...
    
    def filterPeptidesByRTPredictPValue(self, peptides: List[PeptideIdentification] , metavalue_key: Union[bytes, str, String] , threshold: float ) -> None:
        """
        Cython signature: void filterPeptidesByRTPredictPValue(libcpp_vector[PeptideIdentification] & peptides, const String & metavalue_key, double threshold)
        Filters peptide identifications according to p-values from RTPredict\n
        
        Filters the peptide hits by the probability (p-value) of a correct peptide identification having a deviation between observed and predicted RT equal to or greater than allowed
        
        
        :param peptides: Input/output
        :param metavalue_key: Name of the meta value that holds the p-value: "predicted_RT_p_value" or "predicted_RT_p_value_first_dim"
        :param threshold: P-value threshold
        """
        ...
    
    def removePeptidesWithMatchingModifications(self, peptides: List[PeptideIdentification] , modifications: Set[bytes] ) -> None:
        """
        Cython signature: void removePeptidesWithMatchingModifications(libcpp_vector[PeptideIdentification] & peptides, libcpp_set[String] & modifications)
        Removes all peptide hits that have at least one of the given modifications
        """
        ...
    
    def keepPeptidesWithMatchingModifications(self, peptides: List[PeptideIdentification] , modifications: Set[bytes] ) -> None:
        """
        Cython signature: void keepPeptidesWithMatchingModifications(libcpp_vector[PeptideIdentification] & peptides, libcpp_set[String] & modifications)
        Keeps only peptide hits that have at least one of the given modifications
        """
        ...
    
    def removePeptidesWithMatchingSequences(self, peptides: List[PeptideIdentification] , bad_peptides: List[PeptideIdentification] , ignore_mods: bool ) -> None:
        """
        Cython signature: void removePeptidesWithMatchingSequences(libcpp_vector[PeptideIdentification] & peptides, libcpp_vector[PeptideIdentification] & bad_peptides, bool ignore_mods)
        Removes all peptide hits with a sequence that matches one in 'bad_peptides'
        """
        ...
    
    def keepPeptidesWithMatchingSequences(self, peptides: List[PeptideIdentification] , bad_peptides: List[PeptideIdentification] , ignore_mods: bool ) -> None:
        """
        Cython signature: void keepPeptidesWithMatchingSequences(libcpp_vector[PeptideIdentification] & peptides, libcpp_vector[PeptideIdentification] & bad_peptides, bool ignore_mods)
        Removes all peptide hits with a sequence that does not match one in 'good_peptides'
        """
        ...
    
    def keepUniquePeptidesPerProtein(self, peptides: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void keepUniquePeptidesPerProtein(libcpp_vector[PeptideIdentification] & peptides)
        Removes all peptides that are not annotated as unique for a protein (by PeptideIndexer)
        """
        ...
    
    def removeDuplicatePeptideHits(self, peptides: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void removeDuplicatePeptideHits(libcpp_vector[PeptideIdentification] & peptides)
        Removes duplicate peptide hits from each peptide identification, keeping only unique hits (per ID)
        """
        ...
    
    def keepBestPerPeptide(self, peptides: List[PeptideIdentification] , ignore_mods: bool , ignore_charges: bool , nr_best_spectrum: int ) -> None:
        """
        Cython signature: void keepBestPerPeptide(libcpp_vector[PeptideIdentification] & peptides, bool ignore_mods, bool ignore_charges, size_t nr_best_spectrum)
        Filters PeptideHits from PeptideIdentification by keeping only the best peptide hits for every peptide sequence
        """
        ...
    
    def keepBestPerPeptidePerRun(self, prot_ids: List[ProteinIdentification] , peptides: List[PeptideIdentification] , ignore_mods: bool , ignore_charges: bool , nr_best_spectrum: int ) -> None:
        """
        Cython signature: void keepBestPerPeptidePerRun(libcpp_vector[ProteinIdentification] & prot_ids, libcpp_vector[PeptideIdentification] & peptides, bool ignore_mods, bool ignore_charges, size_t nr_best_spectrum)
        Filters PeptideHits from PeptideIdentification by keeping only the best peptide hits for every peptide sequence on a per run basis
        """
        ... 


class IndexedMzMLDecoder:
    """
    Cython implementation of _IndexedMzMLDecoder

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IndexedMzMLDecoder.html>`_

    A class to analyze indexedmzML files and extract the offsets of individual tags
    
    Specifically, this class allows one to extract the offsets of the <indexList>
    tag and of all <spectrum> and <chromatogram> tag using the indices found at
    the end of the indexedmzML XML structure
    
    While findIndexListOffset tries extracts the offset of the indexList tag from
    the last 1024 bytes of the file, this offset allows the function parseOffsets
    to extract all elements contained in the <indexList> tag and thus get access
    to all spectra and chromatogram offsets
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IndexedMzMLDecoder()
        """
        ...
    
    @overload
    def __init__(self, in_0: IndexedMzMLDecoder ) -> None:
        """
        Cython signature: void IndexedMzMLDecoder(IndexedMzMLDecoder &)
        """
        ...
    
    def findIndexListOffset(self, in_: Union[bytes, str, String] , buffersize: int ) -> streampos:
        """
        Cython signature: streampos findIndexListOffset(String in_, int buffersize)
        Tries to extract the indexList offset from an indexedmzML\n
        
        This function reads by default the last few (1024) bytes of the given
        input file and tries to read the content of the <indexListOffset> tag
        The idea is that somewhere in the last parts of the file specified by the
        input string, the string <indexListOffset>xxx</indexListOffset> occurs
        This function returns the xxx part converted to an integer\n
        
        Since this function cannot determine where it will start reading
        the XML, no regular XML parser can be used for this. Therefore it uses
        regex to do its job. It matches the <indexListOffset> part and any
        numerical characters that follow
        
        
        :param in: Filename of the input indexedmzML file
        :param buffersize: How many bytes of the input file should be searched for the tag
        :return: A positive integer containing the content of the indexListOffset tag, returns -1 in case of failure no tag was found (you can re-try with a larger buffersize but most likely its not an indexed mzML). Using -1 is what the reference docu recommends: http://en.cppreference.com/w/cpp/io/streamoff
        :raises:
          Exception: FileNotFound is thrown if file cannot be found
        :raises:
          Exception: ParseError if offset cannot be parsed
        """
        ... 


class InstrumentSettings:
    """
    Cython implementation of _InstrumentSettings

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1InstrumentSettings.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void InstrumentSettings()
        Description of the settings a MS Instrument was run with
        """
        ...
    
    @overload
    def __init__(self, in_0: InstrumentSettings ) -> None:
        """
        Cython signature: void InstrumentSettings(InstrumentSettings &)
        """
        ...
    
    def getPolarity(self) -> int:
        """
        Cython signature: Polarity getPolarity()
        Returns the polarity
        """
        ...
    
    def setPolarity(self, in_0: int ) -> None:
        """
        Cython signature: void setPolarity(Polarity)
        Sets the polarity
        """
        ...
    
    def getScanMode(self) -> int:
        """
        Cython signature: ScanMode getScanMode()
        Returns the scan mode
        """
        ...
    
    def setScanMode(self, scan_mode: int ) -> None:
        """
        Cython signature: void setScanMode(ScanMode scan_mode)
        Sets the scan mode
        """
        ...
    
    def getZoomScan(self) -> bool:
        """
        Cython signature: bool getZoomScan()
        Returns if this scan is a zoom (enhanced resolution) scan
        """
        ...
    
    def setZoomScan(self, zoom_scan: bool ) -> None:
        """
        Cython signature: void setZoomScan(bool zoom_scan)
        Sets if this scan is a zoom (enhanced resolution) scan
        """
        ...
    
    def getScanWindows(self) -> List[ScanWindow]:
        """
        Cython signature: libcpp_vector[ScanWindow] getScanWindows()
        Returns the m/z scan windows
        """
        ...
    
    def setScanWindows(self, scan_windows: List[ScanWindow] ) -> None:
        """
        Cython signature: void setScanWindows(libcpp_vector[ScanWindow] scan_windows)
        Sets the m/z scan windows
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: InstrumentSettings, op: int) -> Any:
        ... 


class InterpolationModel:
    """
    Cython implementation of _InterpolationModel

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1InterpolationModel.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void InterpolationModel()
        Abstract class for 1D-models that are approximated using linear interpolation
        """
        ...
    
    @overload
    def __init__(self, in_0: InterpolationModel ) -> None:
        """
        Cython signature: void InterpolationModel(InterpolationModel &)
        """
        ...
    
    def getIntensity(self, coord: float ) -> float:
        """
        Cython signature: double getIntensity(double coord)
        Access model predicted intensity at position 'pos'
        """
        ...
    
    def getScalingFactor(self) -> float:
        """
        Cython signature: double getScalingFactor()
        Returns the interpolation class
        """
        ...
    
    def setOffset(self, offset: float ) -> None:
        """
        Cython signature: void setOffset(double offset)
        Sets the offset of the model
        """
        ...
    
    def getCenter(self) -> float:
        """
        Cython signature: double getCenter()
        Returns the "center" of the model, particular definition (depends on the derived model)
        """
        ...
    
    def setSamples(self) -> None:
        """
        Cython signature: void setSamples()
        Sets sample/supporting points of interpolation wrt params
        """
        ...
    
    def setInterpolationStep(self, interpolation_step: float ) -> None:
        """
        Cython signature: void setInterpolationStep(double interpolation_step)
        Sets the interpolation step for the linear interpolation of the model
        """
        ...
    
    def setScalingFactor(self, scaling: float ) -> None:
        """
        Cython signature: void setScalingFactor(double scaling)
        Sets the scaling factor of the model
        """
        ...
    
    def getInterpolation(self) -> LinearInterpolation:
        """
        Cython signature: LinearInterpolation getInterpolation()
        Returns the interpolation class
        """
        ... 


class JavaInfo:
    """
    Cython implementation of _JavaInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1JavaInfo.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void JavaInfo()
        Detect Java and retrieve information
        """
        ...
    
    @overload
    def __init__(self, in_0: JavaInfo ) -> None:
        """
        Cython signature: void JavaInfo(JavaInfo &)
        """
        ...
    
    def canRun(self, java_executable: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool canRun(String java_executable)
        Determine if Java is installed and reachable\n
        
        The call fails if either Java is not installed or if a relative location is given and Java is not on the search PATH
        
        
        :param java_executable: Path to Java executable. Can be absolute, relative or just a filename
        :return: Returns false if Java executable can not be called; true if Java executable can be executed
        """
        ... 


class MRMDecoy:
    """
    Cython implementation of _MRMDecoy

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMDecoy.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMDecoy()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMDecoy ) -> None:
        """
        Cython signature: void MRMDecoy(MRMDecoy &)
        """
        ...
    
    def generateDecoys(self, exp: TargetedExperiment , dec: TargetedExperiment , method: Union[bytes, str, String] , aim_decoy_fraction: float , switchKR: bool , decoy_tag: Union[bytes, str, String] , max_attempts: int , identity_threshold: float , precursor_mz_shift: float , product_mz_shift: float , product_mz_threshold: float , fragment_types: List[bytes] , fragment_charges: List[int] , enable_specific_losses: bool , enable_unspecific_losses: bool , round_decPow: int ) -> None:
        """
        Cython signature: void generateDecoys(TargetedExperiment & exp, TargetedExperiment & dec, String method, double aim_decoy_fraction, bool switchKR, String decoy_tag, int max_attempts, double identity_threshold, double precursor_mz_shift, double product_mz_shift, double product_mz_threshold, libcpp_vector[String] fragment_types, libcpp_vector[size_t] fragment_charges, bool enable_specific_losses, bool enable_unspecific_losses, int round_decPow)
        Generate decoys from a TargetedExperiment
        
        Will generate decoy peptides for each target peptide provided in exp and
        write them into the decoy experiment
        
        Valid methods: shuffle, reverse, pseudo-reverse
        
        If theoretical is true, the target transitions will be returned but their
        masses will be adjusted to match the theoretical value of the fragment ion
        that is the most likely explanation for the product
        
        `mz_threshold` is used for the matching of theoretical ion series to the observed one
        
        To generate decoys with different precursor mass, use the "switchKR" flag
        which switches terminal K/R (switches K to R and R to K). This generates
        different precursor m/z and ensures that the y ion series has a different
        mass. For a description of the procedure, see (supplemental material)
        
        Bruderer et al. Mol Cell Proteomics. 2017. 10.1074/mcp.RA117.000314.
        """
        ...
    
    def findFixedResidues(self, sequence: Union[bytes, str, String] , keepN: bool , keepC: bool , keep_const_pattern: Union[bytes, str, String] ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] findFixedResidues(const String & sequence, bool keepN, bool keepC, const String & keep_const_pattern)
        Find all residues in a sequence that should not be reversed / shuffled
        
        
        :param sequence: The amino acid sequence
        :param keepN: Whether to keep N terminus constant
        :param keepC: Whether to keep C terminus constant
        :param keep_const_pattern: A string containing the AA to not change (e.g. 'KRP')
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class MRMFeaturePickerFile:
    """
    Cython implementation of _MRMFeaturePickerFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMFeaturePickerFile.html>`_

    _MRMFeaturePickerFile_ loads components and components groups parameters from a .csv file
    
    The structures defined in [MRMFeaturePicker](@ref MRMFeaturePicker) are used
    
    It is required that columns `component_name` and `component_group_name` are present.
    Lines whose `component_name`'s or `component_group_name`'s value is an empty string, will be skipped.
    The class supports the absence of information within other columns.
    
    A reduced example of the expected format (fewer columns are shown here):
    > component_name,component_group_name,TransitionGroupPicker:stop_after_feature,TransitionGroupPicker:PeakPickerChromatogram:sgolay_frame_length
    > arg-L.arg-L_1.Heavy,arg-L,2,15
    > arg-L.arg-L_1.Light,arg-L,2,17
    > orn.orn_1.Heavy,orn,3,21
    > orn.orn_1.Light,orn,3,13
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMFeaturePickerFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMFeaturePickerFile ) -> None:
        """
        Cython signature: void MRMFeaturePickerFile(MRMFeaturePickerFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , cp_list: List[MRMFP_ComponentParams] , cgp_list: List[MRMFP_ComponentGroupParams] ) -> None:
        """
        Cython signature: void load(const String & filename, libcpp_vector[MRMFP_ComponentParams] & cp_list, libcpp_vector[MRMFP_ComponentGroupParams] & cgp_list)
        Loads the file's data and saves it into vectors of `ComponentParams` and `ComponentGroupParams`
        
        The file is expected to contain at least two columns: `component_name` and `component_group_name`. Otherwise,
        an exception is thrown
        
        If a component group (identified by its name) is found multiple times, only the first one is saved
        
        
        :param filename: Path to the .csv input file
        :param cp_list: Component params are saved in this list
        :param cgp_list: Component Group params are saved in this list
        :raises:
          Exception: MissingInformation If the required columns are not found
        :raises:
          Exception: FileNotFound If input file is not found
        """
        ... 


class MRMFeatureQCFile:
    """
    Cython implementation of _MRMFeatureQCFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMFeatureQCFile.html>`_

    File adapter for MRMFeatureQC files
    
    Loads and stores .csv or .tsv files describing an MRMFeatureQC
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMFeatureQCFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMFeatureQCFile ) -> None:
        """
        Cython signature: void MRMFeatureQCFile(MRMFeatureQCFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , mrmfqc: MRMFeatureQC , is_component_group: bool ) -> None:
        """
        Cython signature: void load(const String & filename, MRMFeatureQC & mrmfqc, const bool is_component_group)
        Loads an MRMFeatureQC file
        
        
        :param filename: The path to the input file
        :param mrmfqc: The output class which will contain the criteria
        :param is_component_group: True if the user intends to load ComponentGroupQCs data, false otherwise
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ... 


class MRMRTNormalizer:
    """
    Cython implementation of _MRMRTNormalizer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMRTNormalizer.html>`_
    """
    
    chauvenet: __static_MRMRTNormalizer_chauvenet
    
    chauvenet_probability: __static_MRMRTNormalizer_chauvenet_probability
    
    computeBinnedCoverage: __static_MRMRTNormalizer_computeBinnedCoverage
    
    removeOutliersIterative: __static_MRMRTNormalizer_removeOutliersIterative
    
    removeOutliersRANSAC: __static_MRMRTNormalizer_removeOutliersRANSAC 


class MZTrafoModel:
    """
    Cython implementation of _MZTrafoModel

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MZTrafoModel.html>`_

    Create and apply models of a mass recalibration function
    
    The input is a list of calibration points (ideally spanning a wide m/z range to prevent extrapolation when applying to model)
    
    Models (LINEAR, LINEAR_WEIGHTED, QUADRATIC, QUADRATIC_WEIGHTED) can be trained using CalData points (or a subset of them)
    Calibration points can have different retention time points, and a model should be build such that it captures
    the local (in time) decalibration of the instrument, i.e. choose appropriate time windows along RT to calibrate the
    spectra in this RT region
    From the available calibrant data, a model is build. Later, any uncalibrated m/z value can be fed to the model, to obtain
    a calibrated m/z
    
    The input domain can either be absolute mass differences in [Th], or relative differences in [ppm]
    The models are build based on this input
    
    Outlier detection before model building via the RANSAC algorithm is supported for LINEAR and QUADRATIC models
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MZTrafoModel()
        """
        ...
    
    @overload
    def __init__(self, in_0: MZTrafoModel ) -> None:
        """
        Cython signature: void MZTrafoModel(MZTrafoModel &)
        """
        ...
    
    @overload
    def __init__(self, in_0: bool ) -> None:
        """
        Cython signature: void MZTrafoModel(bool)
        """
        ...
    
    def isTrained(self) -> bool:
        """
        Cython signature: bool isTrained()
        Returns true if the model have coefficients (i.e. was trained successfully)
        """
        ...
    
    def getRT(self) -> float:
        """
        Cython signature: double getRT()
        Get RT associated with the model (training region)
        """
        ...
    
    def predict(self, mz: float ) -> float:
        """
        Cython signature: double predict(double mz)
        Apply the model to an uncalibrated m/z value
        
        Make sure the model was trained (train()) and is valid (isValidModel()) before calling this function!
        
        Applies the function y = intercept + slope*mz + power*mz^2
        and returns y
        
        
        :param mz: The uncalibrated m/z value
        :return: The calibrated m/z value
        """
        ...
    
    @overload
    def train(self, cd: CalibrationData , md: int , use_RANSAC: bool , rt_left: float , rt_right: float ) -> bool:
        """
        Cython signature: bool train(CalibrationData cd, MZTrafoModel_MODELTYPE md, bool use_RANSAC, double rt_left, double rt_right)
        Train a model using calibrant data
        
        If the CalibrationData was created using peak groups (usually corresponding to mass traces),
        the median for each group is used as a group representative. This
        is more robust, and reduces the number of data points drastically, i.e. one value per group
        
        Internally, these steps take place:
        - apply RT filter
        - [compute median per group] (only if groups were given in 'cd')
        - set Model's rt position
        - call train() (see overloaded method)
        
        
        :param cd: List of calibrants
        :param md: Type of model (linear, quadratic, ...)
        :param use_RANSAC: Remove outliers before computing the model?
        :param rt_left: Filter 'cd' by RT; all calibrants with RT < 'rt_left' are removed
        :param rt_right: Filter 'cd' by RT; all calibrants with RT > 'rt_right' are removed
        :return: True if model was build, false otherwise
        """
        ...
    
    @overload
    def train(self, error_mz: List[float] , theo_mz: List[float] , weights: List[float] , md: int , use_RANSAC: bool ) -> bool:
        """
        Cython signature: bool train(libcpp_vector[double] error_mz, libcpp_vector[double] theo_mz, libcpp_vector[double] weights, MZTrafoModel_MODELTYPE md, bool use_RANSAC)
        Train a model using calibrant data
        
        Given theoretical and observed mass values (and corresponding weights),
        a model (linear, quadratic, ...) is build
        Outlier removal is applied before
        The 'obs_mz' can be either given as absolute masses in [Th] or relative deviations in [ppm]
        The MZTrafoModel must be constructed accordingly (see constructor). This has no influence on the model building itself, but
        rather on how 'predict()' works internally
        
        Outlier detection before model building via the RANSAC algorithm is supported for LINEAR and QUADRATIC models
        
        Internally, these steps take place:
        - [apply RANSAC] (depending on 'use_RANSAC')
        - build model and store its parameters internally
        
        
        :param error_mz: Observed Mass error (in ppm or Th)
        :param theo_mz: Theoretical m/z values, corresponding to 'error_mz'
        :param weights: For weighted models only: weight of calibrants; ignored otherwise
        :param md: Type of model (linear, quadratic, ...)
        :param use_RANSAC: Remove outliers before computing the model?
        :return: True if model was build, false otherwise
        """
        ...
    
    def getCoefficients(self, intercept: float , slope: float , power: float ) -> None:
        """
        Cython signature: void getCoefficients(double & intercept, double & slope, double & power)
        Get model coefficients
        
        Parameters will be filled with internal model parameters
        The model must be trained before; Exception is thrown otherwise!
        
        
        :param intercept: The intercept
        :param slope: The slope
        :param power: The coefficient for x*x (will be 0 for linear models)
        """
        ...
    
    @overload
    def setCoefficients(self, in_0: MZTrafoModel ) -> None:
        """
        Cython signature: void setCoefficients(MZTrafoModel)
        Copy model coefficients from another model
        """
        ...
    
    @overload
    def setCoefficients(self, in_0: float , in_1: float , in_2: float ) -> None:
        """
        Cython signature: void setCoefficients(double, double, double)
        Manually set model coefficients
        
        Can be used instead of train(), so manually set coefficients
        It must be exactly three values. If you want a linear model, set 'power' to zero
        If you want a constant model, set slope to zero in addition
        
        
        :param intercept: The offset
        :param slope: The slope
        :param power: The x*x coefficient (for quadratic models)
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        """
        ...
    
    enumToName: __static_MZTrafoModel_enumToName
    
    findNearest: __static_MZTrafoModel_findNearest
    
    isValidModel: __static_MZTrafoModel_isValidModel
    
    nameToEnum: __static_MZTrafoModel_nameToEnum
    
    setCoefficientLimits: __static_MZTrafoModel_setCoefficientLimits
    
    setRANSACParams: __static_MZTrafoModel_setRANSACParams 


class MatrixDouble:
    """
    Cython implementation of _Matrix[double]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Matrix[double].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MatrixDouble()
        """
        ...
    
    @overload
    def __init__(self, in_0: MatrixDouble ) -> None:
        """
        Cython signature: void MatrixDouble(MatrixDouble)
        """
        ...
    
    @overload
    def __init__(self, rows: int , cols: int , value: float ) -> None:
        """
        Cython signature: void MatrixDouble(size_t rows, size_t cols, double value)
        """
        ...
    
    def getValue(self, i: int , j: int ) -> float:
        """
        Cython signature: double getValue(size_t i, size_t j)
        """
        ...
    
    def setValue(self, i: int , j: int , value: float ) -> None:
        """
        Cython signature: void setValue(size_t i, size_t j, double value)
        """
        ...
    
    def rows(self) -> int:
        """
        Cython signature: size_t rows()
        """
        ...
    
    def cols(self) -> int:
        """
        Cython signature: size_t cols()
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def resize(self, rows: int , cols: int ) -> None:
        """
        Cython signature: void resize(size_t rows, size_t cols)
        """
        ... 


class MetaboTargetedTargetDecoy:
    """
    Cython implementation of _MetaboTargetedTargetDecoy

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaboTargetedTargetDecoy.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaboTargetedTargetDecoy()
        Resolve overlapping fragments and missing decoys for experimental specific decoy generation in targeted/pseudo targeted metabolomics
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaboTargetedTargetDecoy ) -> None:
        """
        Cython signature: void MetaboTargetedTargetDecoy(MetaboTargetedTargetDecoy &)
        """
        ...
    
    def constructTargetDecoyMassMapping(self, t_exp: TargetedExperiment ) -> List[MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping]:
        """
        Cython signature: libcpp_vector[MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping] constructTargetDecoyMassMapping(TargetedExperiment & t_exp)
        Constructs a mass mapping of targets and decoys using the unique m_id identifier
        
        
        :param t_exp: TransitionExperiment holds compound and transition information used for the mapping
        """
        ...
    
    def resolveOverlappingTargetDecoyMassesByDecoyMassShift(self, t_exp: TargetedExperiment , mappings: List[MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping] , mass_to_add: float , mz_tol: float , mz_tol_unit: String ) -> None:
        """
        Cython signature: void resolveOverlappingTargetDecoyMassesByDecoyMassShift(TargetedExperiment & t_exp, libcpp_vector[MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping] & mappings, double & mass_to_add, double & mz_tol, String & mz_tol_unit)
        Resolves overlapping target and decoy transition masses by adding a specifiable mass (e.g. CH2) to the overlapping decoy fragment
        
        
        :param t_exp: TransitionExperiment holds compound and transition information
        :param mappings: Map of identifier to target and decoy masses
        :param mass_to_add: (e.g. CH2)
        :param mz_tol: m/z tolerarance for target and decoy transition masses to be considered overlapping
        :param mz_tol_unit: m/z tolerance unit
        """
        ...
    
    def generateMissingDecoysByMassShift(self, t_exp: TargetedExperiment , mappings: List[MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping] , mass_to_add: float ) -> None:
        """
        Cython signature: void generateMissingDecoysByMassShift(TargetedExperiment & t_exp, libcpp_vector[MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping] & mappings, double & mass_to_add)
        Generate a decoy for targets where fragmentation tree re-rooting was not possible, by adding a specifiable mass to the target fragments
        
        
        :param t_exp: TransitionExperiment holds compound and transition information
        :param mappings: Map of identifier to target and decoy masses
        :param mass_to_add: The maximum number of transitions required per assay
        """
        ... 


class MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping:
    """
    Cython implementation of _MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping ) -> None:
        """
        Cython signature: void MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping(MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping &)
        """
        ... 


class NonNegativeLeastSquaresSolver:
    """
    Cython implementation of _NonNegativeLeastSquaresSolver

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NonNegativeLeastSquaresSolver.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void NonNegativeLeastSquaresSolver()
        """
        ...
    
    @overload
    def __init__(self, in_0: NonNegativeLeastSquaresSolver ) -> None:
        """
        Cython signature: void NonNegativeLeastSquaresSolver(NonNegativeLeastSquaresSolver &)
        """
        ...
    
    def solve(self, A: MatrixDouble , b: MatrixDouble , x: MatrixDouble ) -> int:
        """
        Cython signature: int solve(MatrixDouble & A, MatrixDouble & b, MatrixDouble & x)
        """
        ...
    RETURN_STATUS : __RETURN_STATUS 


class OMSSAXMLFile:
    """
    Cython implementation of _OMSSAXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OMSSAXMLFile.html>`_
      -- Inherits from ['XMLFile']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void OMSSAXMLFile()
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , protein_identification: ProteinIdentification , id_data: List[PeptideIdentification] , load_proteins: bool , load_empty_hits: bool ) -> None:
        """
        Cython signature: void load(const String & filename, ProteinIdentification & protein_identification, libcpp_vector[PeptideIdentification] & id_data, bool load_proteins, bool load_empty_hits)
        Loads data from a OMSSAXML file
        
        
        :param filename: The file to be loaded
        :param protein_identification: Protein identifications belonging to the whole experiment
        :param id_data: The identifications with m/z and RT
        :param load_proteins: If this flag is set to false, the protein identifications are not loaded
        :param load_empty_hits: Many spectra will not return a hit. Report empty peptide identifications?
        """
        ...
    
    def setModificationDefinitionsSet(self, rhs: ModificationDefinitionsSet ) -> None:
        """
        Cython signature: void setModificationDefinitionsSet(ModificationDefinitionsSet rhs)
        Sets the valid modifications
        """
        ...
    
    def getVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVersion()
        Return the version of the schema
        """
        ... 


class OPXLHelper:
    """
    Cython implementation of _OPXLHelper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OPXLHelper.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OPXLHelper()
        """
        ...
    
    @overload
    def __init__(self, in_0: OPXLHelper ) -> None:
        """
        Cython signature: void OPXLHelper(OPXLHelper &)
        """
        ...
    
    def enumerateCrossLinksAndMasses(self, peptides: List[AASeqWithMass] , cross_link_mass_light: float , cross_link_mass_mono_link: List[float] , cross_link_residue1: List[bytes] , cross_link_residue2: List[bytes] , spectrum_precursors: List[float] , precursor_correction_positions: List[int] , precursor_mass_tolerance: float , precursor_mass_tolerance_unit_ppm: bool ) -> List[XLPrecursor]:
        """
        Cython signature: libcpp_vector[XLPrecursor] enumerateCrossLinksAndMasses(libcpp_vector[AASeqWithMass] peptides, double cross_link_mass_light, DoubleList cross_link_mass_mono_link, StringList cross_link_residue1, StringList cross_link_residue2, libcpp_vector[double] & spectrum_precursors, libcpp_vector[int] & precursor_correction_positions, double precursor_mass_tolerance, bool precursor_mass_tolerance_unit_ppm)
        """
        ...
    
    def digestDatabase(self, fasta_db: List[FASTAEntry] , digestor: EnzymaticDigestion , min_peptide_length: int , cross_link_residue1: List[bytes] , cross_link_residue2: List[bytes] , fixed_modifications: ModifiedPeptideGenerator_MapToResidueType , variable_modifications: ModifiedPeptideGenerator_MapToResidueType , max_variable_mods_per_peptide: int ) -> List[AASeqWithMass]:
        """
        Cython signature: libcpp_vector[AASeqWithMass] digestDatabase(libcpp_vector[FASTAEntry] fasta_db, EnzymaticDigestion digestor, size_t min_peptide_length, StringList cross_link_residue1, StringList cross_link_residue2, ModifiedPeptideGenerator_MapToResidueType & fixed_modifications, ModifiedPeptideGenerator_MapToResidueType & variable_modifications, size_t max_variable_mods_per_peptide)
        """
        ...
    
    def buildCandidates(self, candidates: List[XLPrecursor] , precursor_corrections: List[int] , precursor_correction_positions: List[int] , peptide_masses: List[AASeqWithMass] , cross_link_residue1: List[bytes] , cross_link_residue2: List[bytes] , cross_link_mass: float , cross_link_mass_mono_link: List[float] , spectrum_precursor_vector: List[float] , allowed_error_vector: List[float] , cross_link_name: Union[bytes, str, String] ) -> List[ProteinProteinCrossLink]:
        """
        Cython signature: libcpp_vector[ProteinProteinCrossLink] buildCandidates(libcpp_vector[XLPrecursor] & candidates, libcpp_vector[int] & precursor_corrections, libcpp_vector[int] & precursor_correction_positions, libcpp_vector[AASeqWithMass] & peptide_masses, const StringList & cross_link_residue1, const StringList & cross_link_residue2, double cross_link_mass, DoubleList cross_link_mass_mono_link, libcpp_vector[double] & spectrum_precursor_vector, libcpp_vector[double] & allowed_error_vector, String cross_link_name)
        """
        ...
    
    def buildFragmentAnnotations(self, frag_annotations: List[PeptideHit_PeakAnnotation] , matching: List[List[int, int]] , theoretical_spectrum: MSSpectrum , experiment_spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void buildFragmentAnnotations(libcpp_vector[PeptideHit_PeakAnnotation] & frag_annotations, libcpp_vector[libcpp_pair[size_t,size_t]] matching, MSSpectrum theoretical_spectrum, MSSpectrum experiment_spectrum)
        """
        ...
    
    def buildPeptideIDs(self, peptide_ids: List[PeptideIdentification] , top_csms_spectrum: List[CrossLinkSpectrumMatch] , all_top_csms: List[List[CrossLinkSpectrumMatch]] , all_top_csms_current_index: int , spectra: MSExperiment , scan_index: int , scan_index_heavy: int ) -> None:
        """
        Cython signature: void buildPeptideIDs(libcpp_vector[PeptideIdentification] & peptide_ids, libcpp_vector[CrossLinkSpectrumMatch] top_csms_spectrum, libcpp_vector[libcpp_vector[CrossLinkSpectrumMatch]] & all_top_csms, size_t all_top_csms_current_index, MSExperiment spectra, size_t scan_index, size_t scan_index_heavy)
        """
        ...
    
    def addProteinPositionMetaValues(self, peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void addProteinPositionMetaValues(libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ...
    
    def addXLTargetDecoyMV(self, peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void addXLTargetDecoyMV(libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ...
    
    def addBetaAccessions(self, peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void addBetaAccessions(libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ...
    
    def removeBetaPeptideHits(self, peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void removeBetaPeptideHits(libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ...
    
    def addPercolatorFeatureList(self, prot_id: ProteinIdentification ) -> None:
        """
        Cython signature: void addPercolatorFeatureList(ProteinIdentification & prot_id)
        """
        ...
    
    def computeDeltaScores(self, peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void computeDeltaScores(libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ...
    
    def combineTopRanksFromPairs(self, peptide_ids: List[PeptideIdentification] , number_top_hits: int ) -> List[PeptideIdentification]:
        """
        Cython signature: libcpp_vector[PeptideIdentification] combineTopRanksFromPairs(libcpp_vector[PeptideIdentification] & peptide_ids, size_t number_top_hits)
        """
        ...
    
    def collectPrecursorCandidates(self, precursor_correction_steps: List[int] , precursor_mass: float , precursor_mass_tolerance: float , precursor_mass_tolerance_unit_ppm: bool , filtered_peptide_masses: List[AASeqWithMass] , cross_link_mass: float , cross_link_mass_mono_link: List[float] , cross_link_residue1: List[bytes] , cross_link_residue2: List[bytes] , cross_link_name: Union[bytes, str, String] , use_sequence_tags: bool , tags: List[Union[bytes, str]] ) -> List[ProteinProteinCrossLink]:
        """
        Cython signature: libcpp_vector[ProteinProteinCrossLink] collectPrecursorCandidates(IntList precursor_correction_steps, double precursor_mass, double precursor_mass_tolerance, bool precursor_mass_tolerance_unit_ppm, libcpp_vector[AASeqWithMass] filtered_peptide_masses, double cross_link_mass, DoubleList cross_link_mass_mono_link, StringList cross_link_residue1, StringList cross_link_residue2, String cross_link_name, bool use_sequence_tags, const libcpp_vector[libcpp_utf8_string] & tags)
        """
        ...
    
    def computePrecursorError(self, csm: CrossLinkSpectrumMatch , precursor_mz: float , precursor_charge: int ) -> float:
        """
        Cython signature: double computePrecursorError(CrossLinkSpectrumMatch csm, double precursor_mz, int precursor_charge)
        """
        ...
    
    def isoPeakMeans(self, csm: CrossLinkSpectrumMatch , num_iso_peaks_array: IntegerDataArray , matched_spec_linear_alpha: List[List[int, int]] , matched_spec_linear_beta: List[List[int, int]] , matched_spec_xlinks_alpha: List[List[int, int]] , matched_spec_xlinks_beta: List[List[int, int]] ) -> None:
        """
        Cython signature: void isoPeakMeans(CrossLinkSpectrumMatch & csm, IntegerDataArray & num_iso_peaks_array, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_linear_alpha, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_linear_beta, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_xlinks_alpha, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_xlinks_beta)
        """
        ... 


class OSSpectrumMeta:
    """
    Cython implementation of _OSSpectrumMeta

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1OSSpectrumMeta.html>`_
    """
    
    index: int
    
    id: bytes
    
    RT: float
    
    ms_level: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OSSpectrumMeta()
        """
        ...
    
    @overload
    def __init__(self, in_0: OSSpectrumMeta ) -> None:
        """
        Cython signature: void OSSpectrumMeta(OSSpectrumMeta &)
        """
        ... 


class OnDiscMSExperiment:
    """
    Cython implementation of _OnDiscMSExperiment

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OnDiscMSExperiment.html>`_

    Representation of a mass spectrometry experiment on disk.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OnDiscMSExperiment()
        """
        ...
    
    @overload
    def __init__(self, in_0: OnDiscMSExperiment ) -> None:
        """
        Cython signature: void OnDiscMSExperiment(OnDiscMSExperiment &)
        """
        ...
    
    @overload
    def openFile(self, filename: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool openFile(String filename)
        """
        ...
    
    @overload
    def openFile(self, filename: Union[bytes, str, String] , skipLoadingMetaData: bool ) -> bool:
        """
        Cython signature: bool openFile(String filename, bool skipLoadingMetaData)
        Open a specific file on disk
        
        This tries to read the indexed mzML by parsing the index and then reading the meta information into memory
        
        returns: Whether the parsing of the file was successful (if false, the file most likely was not an indexed mzML file)
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        Returns the total number of spectra available
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        Returns the total number of chromatograms available
        """
        ...
    
    def getExperimentalSettings(self) -> ExperimentalSettings:
        """
        Cython signature: shared_ptr[const ExperimentalSettings] getExperimentalSettings()
        Returns the meta information of this experiment (const access)
        """
        ...
    
    def getMetaData(self) -> MSExperiment:
        """
        Cython signature: shared_ptr[MSExperiment] getMetaData()
        Returns the meta information of this experiment
        """
        ...
    
    def getSpectrum(self, id: int ) -> MSSpectrum:
        """
        Cython signature: MSSpectrum getSpectrum(size_t id)
        Returns a single spectrum
        
        
        :param id: The index of the spectrum
        """
        ...
    
    def getSpectrumByNativeId(self, id: Union[bytes, str, String] ) -> MSSpectrum:
        """
        Cython signature: MSSpectrum getSpectrumByNativeId(String id)
        Returns a single spectrum
        
        
        :param id: The native identifier of the spectrum
        """
        ...
    
    def getChromatogram(self, id: int ) -> MSChromatogram:
        """
        Cython signature: MSChromatogram getChromatogram(size_t id)
        Returns a single chromatogram
        
        
        :param id: The index of the chromatogram
        """
        ...
    
    def getChromatogramByNativeId(self, id: Union[bytes, str, String] ) -> MSChromatogram:
        """
        Cython signature: MSChromatogram getChromatogramByNativeId(String id)
        Returns a single chromatogram
        
        
        :param id: The native identifier of the chromatogram
        """
        ...
    
    def getSpectrumById(self, id_: int ) -> _Interfaces_Spectrum:
        """
        Cython signature: shared_ptr[_Interfaces_Spectrum] getSpectrumById(int id_)
        Returns a single spectrum
        """
        ...
    
    def getChromatogramById(self, id_: int ) -> _Interfaces_Chromatogram:
        """
        Cython signature: shared_ptr[_Interfaces_Chromatogram] getChromatogramById(int id_)
        Returns a single chromatogram
        """
        ...
    
    def setSkipXMLChecks(self, skip: bool ) -> None:
        """
        Cython signature: void setSkipXMLChecks(bool skip)
        Sets whether to skip some XML checks and be fast instead
        """
        ... 


class OpenPepXLAlgorithm:
    """
    Cython implementation of _OpenPepXLAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OpenPepXLAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OpenPepXLAlgorithm()
        """
        ...
    
    @overload
    def __init__(self, in_0: OpenPepXLAlgorithm ) -> None:
        """
        Cython signature: void OpenPepXLAlgorithm(OpenPepXLAlgorithm &)
        """
        ...
    
    def run(self, unprocessed_spectra: MSExperiment , cfeatures: ConsensusMap , fasta_db: List[FASTAEntry] , protein_ids: List[ProteinIdentification] , peptide_ids: List[PeptideIdentification] , preprocessed_pair_spectra: OPXL_PreprocessedPairSpectra , spectrum_pairs: List[List[int, int]] , all_top_csms: List[List[CrossLinkSpectrumMatch]] , spectra: MSExperiment ) -> int:
        """
        Cython signature: OpenPepXLAlgorithm_ExitCodes run(MSExperiment & unprocessed_spectra, ConsensusMap & cfeatures, libcpp_vector[FASTAEntry] & fasta_db, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids, OPXL_PreprocessedPairSpectra & preprocessed_pair_spectra, libcpp_vector[libcpp_pair[size_t,size_t]] & spectrum_pairs, libcpp_vector[libcpp_vector[CrossLinkSpectrumMatch]] & all_top_csms, MSExperiment & spectra)
        Performs the main function of this class, the search for cross-linked peptides
        
        
        :param unprocessed_spectra: The input PeakMap of experimental spectra
        :param cfeatures: The input cfeatures
        :param fasta_db: The protein database containing targets and decoys
        :param protein_ids: A result vector containing search settings. Should contain one PeptideIdentification
        :param peptide_ids: A result vector containing cross-link spectrum matches as PeptideIdentifications and PeptideHits. Should be empty
        :param preprocessed_pair_spectra: A result structure containing linear and cross-linked ion spectra. Will be overwritten. This is only necessary for writing out xQuest type spectrum files
        :param spectrum_pairs: A result vector containing paired spectra indices. Should be empty. This is only necessary for writing out xQuest type spectrum files
        :param all_top_csms: A result vector containing cross-link spectrum matches as CrossLinkSpectrumMatches. Should be empty. This is only necessary for writing out xQuest type spectrum files
        :param spectra: A result vector containing the input spectra after preprocessing and filtering. Should be empty. This is only necessary for writing out xQuest type spectrum files
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ...
    OpenPepXLAlgorithm_ExitCodes : __OpenPepXLAlgorithm_ExitCodes 


class Param:
    """
    Cython implementation of _Param

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Param.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Param()
        """
        ...
    
    @overload
    def __init__(self, in_0: Param ) -> None:
        """
        Cython signature: void Param(Param &)
        """
        ...
    
    @overload
    def setValue(self, key: Union[bytes, str] , val: Union[int, float, bytes, str, List[int], List[float], List[bytes]] , desc: Union[bytes, str] , tags: List[Union[bytes, str]] ) -> None:
        """
        Cython signature: void setValue(libcpp_utf8_string key, ParamValue val, libcpp_utf8_string desc, libcpp_vector[libcpp_utf8_string] tags)
        """
        ...
    
    @overload
    def setValue(self, key: Union[bytes, str] , val: Union[int, float, bytes, str, List[int], List[float], List[bytes]] , desc: Union[bytes, str] ) -> None:
        """
        Cython signature: void setValue(libcpp_utf8_string key, ParamValue val, libcpp_utf8_string desc)
        """
        ...
    
    @overload
    def setValue(self, key: Union[bytes, str] , val: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setValue(libcpp_utf8_string key, ParamValue val)
        """
        ...
    
    def getValue(self, key: Union[bytes, str] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: ParamValue getValue(libcpp_utf8_string key)
        """
        ...
    
    def getValueType(self, key: Union[bytes, str] ) -> int:
        """
        Cython signature: ValueType getValueType(libcpp_utf8_string key)
        """
        ...
    
    def getEntry(self, in_0: Union[bytes, str] ) -> ParamEntry:
        """
        Cython signature: ParamEntry getEntry(libcpp_utf8_string)
        """
        ...
    
    def exists(self, key: Union[bytes, str] ) -> bool:
        """
        Cython signature: bool exists(libcpp_utf8_string key)
        """
        ...
    
    def addTag(self, key: Union[bytes, str] , tag: Union[bytes, str] ) -> None:
        """
        Cython signature: void addTag(libcpp_utf8_string key, libcpp_utf8_string tag)
        """
        ...
    
    def addTags(self, key: Union[bytes, str] , tags: List[Union[bytes, str]] ) -> None:
        """
        Cython signature: void addTags(libcpp_utf8_string key, libcpp_vector[libcpp_utf8_string] tags)
        """
        ...
    
    def hasTag(self, key: Union[bytes, str] , tag: Union[bytes, str] ) -> int:
        """
        Cython signature: int hasTag(libcpp_utf8_string key, libcpp_utf8_string tag)
        """
        ...
    
    def getTags(self, key: Union[bytes, str] ) -> List[bytes]:
        """
        Cython signature: libcpp_vector[libcpp_string] getTags(libcpp_utf8_string key)
        """
        ...
    
    def clearTags(self, key: Union[bytes, str] ) -> None:
        """
        Cython signature: void clearTags(libcpp_utf8_string key)
        """
        ...
    
    def getDescription(self, key: Union[bytes, str] ) -> str:
        """
        Cython signature: libcpp_utf8_output_string getDescription(libcpp_utf8_string key)
        """
        ...
    
    def setSectionDescription(self, key: Union[bytes, str] , desc: Union[bytes, str] ) -> None:
        """
        Cython signature: void setSectionDescription(libcpp_utf8_string key, libcpp_utf8_string desc)
        """
        ...
    
    def getSectionDescription(self, key: Union[bytes, str] ) -> str:
        """
        Cython signature: libcpp_utf8_output_string getSectionDescription(libcpp_utf8_string key)
        """
        ...
    
    def addSection(self, key: Union[bytes, str] , desc: Union[bytes, str] ) -> None:
        """
        Cython signature: void addSection(libcpp_utf8_string key, libcpp_utf8_string desc)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def insert(self, prefix: Union[bytes, str] , param: Param ) -> None:
        """
        Cython signature: void insert(libcpp_utf8_string prefix, Param param)
        """
        ...
    
    def remove(self, key: Union[bytes, str] ) -> None:
        """
        Cython signature: void remove(libcpp_utf8_string key)
        """
        ...
    
    def removeAll(self, prefix: Union[bytes, str] ) -> None:
        """
        Cython signature: void removeAll(libcpp_utf8_string prefix)
        """
        ...
    
    @overload
    def copy(self, prefix: Union[bytes, str] , in_1: bool ) -> Param:
        """
        Cython signature: Param copy(libcpp_utf8_string prefix, bool)
        """
        ...
    
    @overload
    def copy(self, prefix: Union[bytes, str] ) -> Param:
        """
        Cython signature: Param copy(libcpp_utf8_string prefix)
        """
        ...
    
    def merge(self, toMerge: Param ) -> None:
        """
        Cython signature: void merge(Param toMerge)
        """
        ...
    
    @overload
    def setDefaults(self, defaults: Param , prefix: Union[bytes, str] , showMessage: bool ) -> None:
        """
        Cython signature: void setDefaults(Param defaults, libcpp_utf8_string prefix, bool showMessage)
        """
        ...
    
    @overload
    def setDefaults(self, defaults: Param , prefix: Union[bytes, str] ) -> None:
        """
        Cython signature: void setDefaults(Param defaults, libcpp_utf8_string prefix)
        """
        ...
    
    @overload
    def setDefaults(self, defaults: Param ) -> None:
        """
        Cython signature: void setDefaults(Param defaults)
        """
        ...
    
    @overload
    def checkDefaults(self, name: Union[bytes, str] , defaults: Param , prefix: Union[bytes, str] ) -> None:
        """
        Cython signature: void checkDefaults(libcpp_utf8_string name, Param defaults, libcpp_utf8_string prefix)
        """
        ...
    
    @overload
    def checkDefaults(self, name: Union[bytes, str] , defaults: Param ) -> None:
        """
        Cython signature: void checkDefaults(libcpp_utf8_string name, Param defaults)
        """
        ...
    
    def getValidStrings(self, key: Union[bytes, str] ) -> List[Union[bytes, str]]:
        """
        Cython signature: libcpp_vector[libcpp_utf8_string] getValidStrings(libcpp_utf8_string key)
        """
        ...
    
    def setValidStrings(self, key: Union[bytes, str] , strings: List[Union[bytes, str]] ) -> None:
        """
        Cython signature: void setValidStrings(libcpp_utf8_string key, libcpp_vector[libcpp_utf8_string] strings)
        """
        ...
    
    def setMinInt(self, key: Union[bytes, str] , min: int ) -> None:
        """
        Cython signature: void setMinInt(libcpp_utf8_string key, int min)
        """
        ...
    
    def setMaxInt(self, key: Union[bytes, str] , max: int ) -> None:
        """
        Cython signature: void setMaxInt(libcpp_utf8_string key, int max)
        """
        ...
    
    def setMinFloat(self, key: Union[bytes, str] , min: float ) -> None:
        """
        Cython signature: void setMinFloat(libcpp_utf8_string key, double min)
        """
        ...
    
    def setMaxFloat(self, key: Union[bytes, str] , max: float ) -> None:
        """
        Cython signature: void setMaxFloat(libcpp_utf8_string key, double max)
        """
        ...
    
    def __richcmp__(self, other: Param, op: int) -> Any:
        ... 


class ParamValue:
    """
    Cython implementation of _ParamValue

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ParamValue.html>`_

    Class to hold strings, numeric values, vectors of strings and vectors of numeric values using the stl types
    
    - To choose one of these types, just use the appropriate constructor
    - Automatic conversion is supported and throws Exceptions in case of invalid conversions
    - An empty object is created with the default constructor
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ParamValue()
        """
        ...
    
    @overload
    def __init__(self, in_0: ParamValue ) -> None:
        """
        Cython signature: void ParamValue(ParamValue &)
        """
        ...
    
    @overload
    def __init__(self, in_0: bytes ) -> None:
        """
        Cython signature: void ParamValue(char *)
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[bytes, str] ) -> None:
        """
        Cython signature: void ParamValue(const libcpp_utf8_string &)
        """
        ...
    
    @overload
    def __init__(self, in_0: int ) -> None:
        """
        Cython signature: void ParamValue(int)
        """
        ...
    
    @overload
    def __init__(self, in_0: float ) -> None:
        """
        Cython signature: void ParamValue(double)
        """
        ...
    
    @overload
    def __init__(self, in_0: List[Union[bytes, str]] ) -> None:
        """
        Cython signature: void ParamValue(libcpp_vector[libcpp_utf8_string])
        """
        ...
    
    @overload
    def __init__(self, in_0: List[int] ) -> None:
        """
        Cython signature: void ParamValue(libcpp_vector[int])
        """
        ...
    
    @overload
    def __init__(self, in_0: List[float] ) -> None:
        """
        Cython signature: void ParamValue(libcpp_vector[double])
        """
        ...
    
    def toStringVector(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[libcpp_string] toStringVector()
        Explicitly convert ParamValue to string vector
        """
        ...
    
    def toDoubleVector(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] toDoubleVector()
        Explicitly convert ParamValue to DoubleList
        """
        ...
    
    def toIntVector(self) -> List[int]:
        """
        Cython signature: libcpp_vector[int] toIntVector()
        Explicitly convert ParamValue to IntList
        """
        ...
    
    def toBool(self) -> bool:
        """
        Cython signature: bool toBool()
        Converts the strings 'true' and 'false' to a bool
        """
        ...
    
    def valueType(self) -> int:
        """
        Cython signature: ValueType valueType()
        """
        ...
    
    def isEmpty(self) -> int:
        """
        Cython signature: int isEmpty()
        Test if the value is empty
        """
        ... 


class PeptideIdentification:
    """
    Cython implementation of _PeptideIdentification

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeptideIdentification.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeptideIdentification()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeptideIdentification ) -> None:
        """
        Cython signature: void PeptideIdentification(PeptideIdentification &)
        """
        ...
    
    def getHits(self) -> List[PeptideHit]:
        """
        Cython signature: libcpp_vector[PeptideHit] getHits()
        Returns the peptide hits as const
        """
        ...
    
    def insertHit(self, in_0: PeptideHit ) -> None:
        """
        Cython signature: void insertHit(PeptideHit)
        Appends a peptide hit
        """
        ...
    
    def setHits(self, in_0: List[PeptideHit] ) -> None:
        """
        Cython signature: void setHits(libcpp_vector[PeptideHit])
        Sets the peptide hits
        """
        ...
    
    def getSignificanceThreshold(self) -> float:
        """
        Cython signature: double getSignificanceThreshold()
        Returns the peptide significance threshold value
        """
        ...
    
    def setSignificanceThreshold(self, value: float ) -> None:
        """
        Cython signature: void setSignificanceThreshold(double value)
        Setting of the peptide significance threshold value
        """
        ...
    
    def getScoreType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getScoreType()
        """
        ...
    
    def setScoreType(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setScoreType(String)
        """
        ...
    
    def isHigherScoreBetter(self) -> bool:
        """
        Cython signature: bool isHigherScoreBetter()
        """
        ...
    
    def setHigherScoreBetter(self, in_0: bool ) -> None:
        """
        Cython signature: void setHigherScoreBetter(bool)
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        """
        ...
    
    def setIdentifier(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(String)
        """
        ...
    
    def hasMZ(self) -> bool:
        """
        Cython signature: bool hasMZ()
        """
        ...
    
    def getMZ(self) -> float:
        """
        Cython signature: double getMZ()
        """
        ...
    
    def setMZ(self, in_0: float ) -> None:
        """
        Cython signature: void setMZ(double)
        """
        ...
    
    def hasRT(self) -> bool:
        """
        Cython signature: bool hasRT()
        """
        ...
    
    def getRT(self) -> float:
        """
        Cython signature: double getRT()
        """
        ...
    
    def setRT(self, in_0: float ) -> None:
        """
        Cython signature: void setRT(double)
        """
        ...
    
    def getBaseName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getBaseName()
        """
        ...
    
    def setBaseName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setBaseName(String)
        """
        ...
    
    def getExperimentLabel(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getExperimentLabel()
        """
        ...
    
    def setExperimentLabel(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setExperimentLabel(String)
        """
        ...
    
    def assignRanks(self) -> None:
        """
        Cython signature: void assignRanks()
        """
        ...
    
    def sort(self) -> None:
        """
        Cython signature: void sort()
        """
        ...
    
    def sortByRank(self) -> None:
        """
        Cython signature: void sortByRank()
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        """
        ...
    
    def getReferencingHits(self, in_0: List[PeptideHit] , in_1: Set[bytes] ) -> List[PeptideHit]:
        """
        Cython signature: libcpp_vector[PeptideHit] getReferencingHits(libcpp_vector[PeptideHit], libcpp_set[String] &)
        Returns all peptide hits which reference to a given protein accession (i.e. filter by protein accession)
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: PeptideIdentification, op: int) -> Any:
        ... 


class PeptideIndexing:
    """
    Cython implementation of _PeptideIndexing

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeptideIndexing.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeptideIndexing()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeptideIndexing ) -> None:
        """
        Cython signature: void PeptideIndexing(PeptideIndexing &)
        """
        ...
    
    def run(self, proteins: List[FASTAEntry] , prot_ids: List[ProteinIdentification] , pep_ids: List[PeptideIdentification] ) -> int:
        """
        Cython signature: PeptideIndexing_ExitCodes run(libcpp_vector[FASTAEntry] & proteins, libcpp_vector[ProteinIdentification] & prot_ids, libcpp_vector[PeptideIdentification] & pep_ids)
        """
        ...
    
    def getDecoyString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getDecoyString()
        """
        ...
    
    def isPrefix(self) -> bool:
        """
        Cython signature: bool isPrefix()
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ...
    PeptideIndexing_ExitCodes : __PeptideIndexing_ExitCodes 


class ProbablePhosphoSites:
    """
    Cython implementation of _ProbablePhosphoSites

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProbablePhosphoSites.html>`_
    """
    
    first: int
    
    second: int
    
    seq_1: int
    
    seq_2: int
    
    peak_depth: int
    
    AScore: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProbablePhosphoSites()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProbablePhosphoSites ) -> None:
        """
        Cython signature: void ProbablePhosphoSites(ProbablePhosphoSites &)
        """
        ... 


class RNaseDigestion:
    """
    Cython implementation of _RNaseDigestion

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1RNaseDigestion.html>`_
      -- Inherits from ['EnzymaticDigestion']

    Class for the enzymatic digestion of RNA
    
    Usage:
    
    .. code-block:: python
    
          from pyopenms import *
          oligo = NASequence.fromString("pAUGUCGCAG");
    
          dig = RNaseDigestion()
          dig.setEnzyme("RNase_T1")
    
          result = []
          dig.digest(oligo, result)
          for fragment in result:
            print (fragment)
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RNaseDigestion()
        """
        ...
    
    @overload
    def __init__(self, in_0: RNaseDigestion ) -> None:
        """
        Cython signature: void RNaseDigestion(RNaseDigestion &)
        """
        ...
    
    @overload
    def setEnzyme(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setEnzyme(String name)
        Sets the enzyme for the digestion (by name)
        """
        ...
    
    @overload
    def setEnzyme(self, enzyme: DigestionEnzyme ) -> None:
        """
        Cython signature: void setEnzyme(DigestionEnzyme * enzyme)
        Sets the enzyme for the digestion
        """
        ...
    
    @overload
    def digest(self, rna: NASequence , output: List[NASequence] ) -> None:
        """
        Cython signature: void digest(NASequence & rna, libcpp_vector[NASequence] & output)
        """
        ...
    
    @overload
    def digest(self, rna: NASequence , output: List[NASequence] , min_length: int , max_length: int ) -> None:
        """
        Cython signature: void digest(NASequence & rna, libcpp_vector[NASequence] & output, size_t min_length, size_t max_length)
        Performs the enzymatic digestion of a (potentially modified) RNA
        
        :param rna: Sequence to digest
        :param output: Digestion productsq
        :param min_length: Minimal length of reported products
        :param max_length: Maximal length of reported products (0 = no restriction)
        :returns: Number of discarded digestion products (which are not matching length restrictions)
        Performs the enzymatic digestion of all RNA parent molecules in IdentificationData (id_data)
        
        :param id_data: IdentificationData object which includes sequences to digest
        :param min_length: Minimal length of reported products
        :param max_length: Maximal length of reported products (0 = no restriction)
        :returns: Number of discarded digestion products (which are not matching length restrictions)
        """
        ...
    
    def getMissedCleavages(self) -> int:
        """
        Cython signature: size_t getMissedCleavages()
        Returns the max. number of allowed missed cleavages for the digestion
        """
        ...
    
    def setMissedCleavages(self, missed_cleavages: int ) -> None:
        """
        Cython signature: void setMissedCleavages(size_t missed_cleavages)
        Sets the max. number of allowed missed cleavages for the digestion (default is 0). This setting is ignored when log model is used
        """
        ...
    
    def countInternalCleavageSites(self, sequence: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t countInternalCleavageSites(String sequence)
        Returns the number of internal cleavage sites for this sequence.
        """
        ...
    
    def getEnzymeName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getEnzymeName()
        Returns the enzyme for the digestion
        """
        ...
    
    def getSpecificity(self) -> int:
        """
        Cython signature: Specificity getSpecificity()
        Returns the specificity for the digestion
        """
        ...
    
    def setSpecificity(self, spec: int ) -> None:
        """
        Cython signature: void setSpecificity(Specificity spec)
        Sets the specificity for the digestion (default is SPEC_FULL)
        """
        ...
    
    def getSpecificityByName(self, name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: Specificity getSpecificityByName(String name)
        Returns the specificity by name. Returns SPEC_UNKNOWN if name is not valid
        """
        ...
    
    def digestUnmodified(self, sequence: StringView , output: List[StringView] , min_length: int , max_length: int ) -> int:
        """
        Cython signature: size_t digestUnmodified(StringView sequence, libcpp_vector[StringView] & output, size_t min_length, size_t max_length)
        Performs the enzymatic digestion of an unmodified sequence\n
        By returning only references into the original string this is very fast
        
        
        :param sequence: Sequence to digest
        :param output: Digestion products
        :param min_length: Minimal length of reported products
        :param max_length: Maximal length of reported products (0 = no restriction)
        :return: Number of discarded digestion products (which are not matching length restrictions)
        """
        ...
    
    def isValidProduct(self, sequence: Union[bytes, str, String] , pos: int , length: int , ignore_missed_cleavages: bool ) -> bool:
        """
        Cython signature: bool isValidProduct(String sequence, int pos, int length, bool ignore_missed_cleavages)
        Boolean operator returns true if the peptide fragment starting at position `pos` with length `length` within the sequence `sequence` generated by the current enzyme\n
        Checks if peptide is a valid digestion product of the enzyme, taking into account specificity and the MC flag provided here
        
        
        :param protein: Protein sequence
        :param pep_pos: Starting index of potential peptide
        :param pep_length: Length of potential peptide
        :param ignore_missed_cleavages: Do not compare MC's of potential peptide to the maximum allowed MC's
        :return: True if peptide has correct n/c terminals (according to enzyme, specificity and missed cleavages)
        """
        ... 


class RealMassDecomposer:
    """
    Cython implementation of _RealMassDecomposer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ims_1_1RealMassDecomposer.html>`_
    """
    
    @overload
    def __init__(self, in_0: RealMassDecomposer ) -> None:
        """
        Cython signature: void RealMassDecomposer(RealMassDecomposer)
        """
        ...
    
    @overload
    def __init__(self, weights: IMSWeights ) -> None:
        """
        Cython signature: void RealMassDecomposer(IMSWeights & weights)
        """
        ...
    
    def getNumberOfDecompositions(self, mass: float , error: float ) -> int:
        """
        Cython signature: uint64_t getNumberOfDecompositions(double mass, double error)
        Gets a number of all decompositions for amass with an error
        allowed. It's similar to thegetDecompositions(double,double) function
        but less space consuming, since doesn't use container to store decompositions
        
        
        :param mass: Mass to be decomposed
        :param error: Error allowed between given and result decomposition
        :return: Number of all decompositions for a given mass and error
        """
        ... 


class ScanWindow:
    """
    Cython implementation of _ScanWindow

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ScanWindow.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    begin: float
    
    end: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ScanWindow()
        """
        ...
    
    @overload
    def __init__(self, in_0: ScanWindow ) -> None:
        """
        Cython signature: void ScanWindow(ScanWindow &)
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: ScanWindow, op: int) -> Any:
        ... 


class SignalToNoiseEstimatorMeanIterative:
    """
    Cython implementation of _SignalToNoiseEstimatorMeanIterative[_MSSpectrum]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SignalToNoiseEstimatorMeanIterative[_MSSpectrum].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SignalToNoiseEstimatorMeanIterative()
        """
        ...
    
    @overload
    def __init__(self, in_0: SignalToNoiseEstimatorMeanIterative ) -> None:
        """
        Cython signature: void SignalToNoiseEstimatorMeanIterative(SignalToNoiseEstimatorMeanIterative &)
        """
        ...
    
    def init(self, c: MSSpectrum ) -> None:
        """
        Cython signature: void init(MSSpectrum & c)
        """
        ...
    
    def getSignalToNoise(self, index: int ) -> float:
        """
        Cython signature: double getSignalToNoise(size_t index)
        """
        ...
    IntensityThresholdCalculation : __IntensityThresholdCalculation 


class SplineInterpolatedPeaks:
    """
    Cython implementation of _SplineInterpolatedPeaks

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SplineInterpolatedPeaks.html>`_
    """
    
    @overload
    def __init__(self, mz: List[float] , intensity: List[float] ) -> None:
        """
        Cython signature: void SplineInterpolatedPeaks(libcpp_vector[double] mz, libcpp_vector[double] intensity)
        """
        ...
    
    @overload
    def __init__(self, raw_spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void SplineInterpolatedPeaks(MSSpectrum raw_spectrum)
        """
        ...
    
    @overload
    def __init__(self, raw_chromatogram: MSChromatogram ) -> None:
        """
        Cython signature: void SplineInterpolatedPeaks(MSChromatogram raw_chromatogram)
        """
        ...
    
    @overload
    def __init__(self, in_0: SplineInterpolatedPeaks ) -> None:
        """
        Cython signature: void SplineInterpolatedPeaks(SplineInterpolatedPeaks &)
        """
        ...
    
    def getPosMin(self) -> float:
        """
        Cython signature: double getPosMin()
        """
        ...
    
    def getPosMax(self) -> float:
        """
        Cython signature: double getPosMax()
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: int size()
        """
        ...
    
    def getNavigator(self, scaling: float ) -> SplineSpectrum_Navigator:
        """
        Cython signature: SplineSpectrum_Navigator getNavigator(double scaling)
        """
        ... 


class SplineSpectrum_Navigator:
    """
    Cython implementation of _SplineSpectrum_Navigator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SplineSpectrum_Navigator.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SplineSpectrum_Navigator()
        """
        ...
    
    @overload
    def __init__(self, in_0: SplineSpectrum_Navigator ) -> None:
        """
        Cython signature: void SplineSpectrum_Navigator(SplineSpectrum_Navigator)
        """
        ...
    
    @overload
    def __init__(self, packages: List[SplinePackage] , posMax: float , scaling: float ) -> None:
        """
        Cython signature: void SplineSpectrum_Navigator(libcpp_vector[SplinePackage] * packages, double posMax, double scaling)
        """
        ...
    
    def eval(self, pos: float ) -> float:
        """
        Cython signature: double eval(double pos)
        """
        ...
    
    def getNextPos(self, pos: float ) -> float:
        """
        Cython signature: double getNextPos(double pos)
        """
        ... 


class SwathMapMassCorrection:
    """
    Cython implementation of _SwathMapMassCorrection

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SwathMapMassCorrection.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SwathMapMassCorrection()
        """
        ...
    
    @overload
    def __init__(self, in_0: SwathMapMassCorrection ) -> None:
        """
        Cython signature: void SwathMapMassCorrection(SwathMapMassCorrection)
        """
        ... 


class Tagger:
    """
    Cython implementation of _Tagger

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Tagger.html>`_

    Constructor for Tagger
    
    The parameter `max_charge_` should be >= `min_charge_`
    Also `max_tag_length` should be >= `min_tag_length`
    
    :param min_tag_length: The minimal sequence tag length
    :param ppm: The tolerance for matching residue masses to peak delta masses
    :param max_tag_length: The maximal sequence tag length
    :param min_charge: Minimal fragment charge considered for each sequence tag
    :param max_charge: Maximal fragment charge considered for each sequence tag
    :param fixed_mods: A list of modification names. The modified residues replace the unmodified versions
    :param var_mods: A list of modification names. The modified residues are added as additional entries to the list of residues
    """
    
    @overload
    def __init__(self, in_0: Tagger ) -> None:
        """
        Cython signature: void Tagger(Tagger &)
        """
        ...
    
    @overload
    def __init__(self, min_tag_length: int , ppm: float , max_tag_length: int , min_charge: int , max_charge: int , fixed_mods: List[bytes] , var_mods: List[bytes] ) -> None:
        """
        Cython signature: void Tagger(size_t min_tag_length, double ppm, size_t max_tag_length, size_t min_charge, size_t max_charge, const StringList & fixed_mods, const StringList & var_mods)
        """
        ...
    
    @overload
    def getTag(self, mzs: List[float] , tags: List[Union[bytes, str]] ) -> None:
        """
        Cython signature: void getTag(const libcpp_vector[double] & mzs, libcpp_vector[libcpp_utf8_string] & tags)
        Generate tags from mass vector `mzs`
        
        The parameter `tags` is filled with one string per sequence tag
        It uses the standard residues from ResidueDB including
        the fixed and variable modifications given to the constructor
        
        :param mzs: A vector of mz values, containing the mz values from a centroided fragment spectrum
        :param tags: The vector of tags, that is filled with this function
        """
        ...
    
    @overload
    def getTag(self, spec: MSSpectrum , tags: List[Union[bytes, str]] ) -> None:
        """
        Cython signature: void getTag(const MSSpectrum & spec, libcpp_vector[libcpp_utf8_string] & tags)
        Generate tags from an MSSpectrum
        
        The parameter `tags` is filled with one string per sequence tag
        It uses the standard residues from ResidueDB including
        the fixed and variable modifications given to the constructor
        
        :param spec: A centroided fragment spectrum
        :param tags: The vector of tags, that is filled with this function
        """
        ...
    
    def setMaxCharge(self, max_charge: int ) -> None:
        """
        Cython signature: void setMaxCharge(size_t max_charge)
        Change the maximal charge considered by the tagger
        
        Allows to change the maximal considered charge e.g. based on a spectra
        precursor charge without calling the constructor multiple times
        
        :param max_charge: The new maximal charge
        """
        ... 


class TargetedExperiment:
    """
    Cython implementation of _TargetedExperiment

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TargetedExperiment.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TargetedExperiment()
        """
        ...
    
    @overload
    def __init__(self, in_0: TargetedExperiment ) -> None:
        """
        Cython signature: void TargetedExperiment(TargetedExperiment &)
        """
        ...
    
    def __add__(self: TargetedExperiment, other: TargetedExperiment) -> TargetedExperiment:
        ...
    
    def __iadd__(self: TargetedExperiment, other: TargetedExperiment) -> TargetedExperiment:
        ...
    
    def clear(self, clear_meta_data: bool ) -> None:
        """
        Cython signature: void clear(bool clear_meta_data)
        """
        ...
    
    def sortTransitionsByProductMZ(self) -> None:
        """
        Cython signature: void sortTransitionsByProductMZ()
        """
        ...
    
    def setCVs(self, cvs: List[CV] ) -> None:
        """
        Cython signature: void setCVs(libcpp_vector[CV] cvs)
        """
        ...
    
    def getCVs(self) -> List[CV]:
        """
        Cython signature: libcpp_vector[CV] getCVs()
        """
        ...
    
    def addCV(self, cv: CV ) -> None:
        """
        Cython signature: void addCV(CV cv)
        """
        ...
    
    def setContacts(self, contacts: List[Contact] ) -> None:
        """
        Cython signature: void setContacts(libcpp_vector[Contact] contacts)
        """
        ...
    
    def getContacts(self) -> List[Contact]:
        """
        Cython signature: libcpp_vector[Contact] getContacts()
        """
        ...
    
    def addContact(self, contact: Contact ) -> None:
        """
        Cython signature: void addContact(Contact contact)
        """
        ...
    
    def setPublications(self, publications: List[Publication] ) -> None:
        """
        Cython signature: void setPublications(libcpp_vector[Publication] publications)
        """
        ...
    
    def getPublications(self) -> List[Publication]:
        """
        Cython signature: libcpp_vector[Publication] getPublications()
        """
        ...
    
    def addPublication(self, publication: Publication ) -> None:
        """
        Cython signature: void addPublication(Publication publication)
        """
        ...
    
    def setTargetCVTerms(self, cv_terms: CVTermList ) -> None:
        """
        Cython signature: void setTargetCVTerms(CVTermList cv_terms)
        """
        ...
    
    def getTargetCVTerms(self) -> CVTermList:
        """
        Cython signature: CVTermList getTargetCVTerms()
        """
        ...
    
    def addTargetCVTerm(self, cv_term: CVTerm ) -> None:
        """
        Cython signature: void addTargetCVTerm(CVTerm cv_term)
        """
        ...
    
    def setTargetMetaValue(self, name: Union[bytes, str, String] , value: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setTargetMetaValue(String name, DataValue value)
        """
        ...
    
    def setInstruments(self, instruments: List[TargetedExperiment_Instrument] ) -> None:
        """
        Cython signature: void setInstruments(libcpp_vector[TargetedExperiment_Instrument] instruments)
        """
        ...
    
    def getInstruments(self) -> List[TargetedExperiment_Instrument]:
        """
        Cython signature: libcpp_vector[TargetedExperiment_Instrument] getInstruments()
        """
        ...
    
    def addInstrument(self, instrument: TargetedExperiment_Instrument ) -> None:
        """
        Cython signature: void addInstrument(TargetedExperiment_Instrument instrument)
        """
        ...
    
    def setSoftware(self, software: List[Software] ) -> None:
        """
        Cython signature: void setSoftware(libcpp_vector[Software] software)
        """
        ...
    
    def getSoftware(self) -> List[Software]:
        """
        Cython signature: libcpp_vector[Software] getSoftware()
        """
        ...
    
    def addSoftware(self, software: Software ) -> None:
        """
        Cython signature: void addSoftware(Software software)
        """
        ...
    
    def setProteins(self, proteins: List[Protein] ) -> None:
        """
        Cython signature: void setProteins(libcpp_vector[Protein] proteins)
        """
        ...
    
    def getProteins(self) -> List[Protein]:
        """
        Cython signature: libcpp_vector[Protein] getProteins()
        """
        ...
    
    def getProteinByRef(self, ref: Union[bytes, str, String] ) -> Protein:
        """
        Cython signature: Protein getProteinByRef(String ref)
        """
        ...
    
    def hasProtein(self, ref: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasProtein(String ref)
        """
        ...
    
    def addProtein(self, protein: Protein ) -> None:
        """
        Cython signature: void addProtein(Protein protein)
        """
        ...
    
    def setCompounds(self, rhs: List[Compound] ) -> None:
        """
        Cython signature: void setCompounds(libcpp_vector[Compound] rhs)
        """
        ...
    
    def getCompounds(self) -> List[Compound]:
        """
        Cython signature: libcpp_vector[Compound] getCompounds()
        """
        ...
    
    def addCompound(self, rhs: Compound ) -> None:
        """
        Cython signature: void addCompound(Compound rhs)
        """
        ...
    
    def hasCompound(self, ref: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasCompound(String ref)
        """
        ...
    
    def getCompoundByRef(self, ref: Union[bytes, str, String] ) -> Compound:
        """
        Cython signature: Compound getCompoundByRef(String ref)
        """
        ...
    
    def setPeptides(self, rhs: List[Peptide] ) -> None:
        """
        Cython signature: void setPeptides(libcpp_vector[Peptide] rhs)
        """
        ...
    
    def getPeptides(self) -> List[Peptide]:
        """
        Cython signature: libcpp_vector[Peptide] getPeptides()
        """
        ...
    
    def hasPeptide(self, ref: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasPeptide(String ref)
        """
        ...
    
    def getPeptideByRef(self, ref: Union[bytes, str, String] ) -> Peptide:
        """
        Cython signature: Peptide getPeptideByRef(String ref)
        """
        ...
    
    def addPeptide(self, rhs: Peptide ) -> None:
        """
        Cython signature: void addPeptide(Peptide rhs)
        """
        ...
    
    def setTransitions(self, transitions: List[ReactionMonitoringTransition] ) -> None:
        """
        Cython signature: void setTransitions(libcpp_vector[ReactionMonitoringTransition] transitions)
        """
        ...
    
    def getTransitions(self) -> List[ReactionMonitoringTransition]:
        """
        Cython signature: libcpp_vector[ReactionMonitoringTransition] getTransitions()
        """
        ...
    
    def addTransition(self, transition: ReactionMonitoringTransition ) -> None:
        """
        Cython signature: void addTransition(ReactionMonitoringTransition transition)
        """
        ...
    
    def setIncludeTargets(self, targets: List[IncludeExcludeTarget] ) -> None:
        """
        Cython signature: void setIncludeTargets(libcpp_vector[IncludeExcludeTarget] targets)
        """
        ...
    
    def getIncludeTargets(self) -> List[IncludeExcludeTarget]:
        """
        Cython signature: libcpp_vector[IncludeExcludeTarget] getIncludeTargets()
        """
        ...
    
    def addIncludeTarget(self, target: IncludeExcludeTarget ) -> None:
        """
        Cython signature: void addIncludeTarget(IncludeExcludeTarget target)
        """
        ...
    
    def setExcludeTargets(self, targets: List[IncludeExcludeTarget] ) -> None:
        """
        Cython signature: void setExcludeTargets(libcpp_vector[IncludeExcludeTarget] targets)
        """
        ...
    
    def getExcludeTargets(self) -> List[IncludeExcludeTarget]:
        """
        Cython signature: libcpp_vector[IncludeExcludeTarget] getExcludeTargets()
        """
        ...
    
    def addExcludeTarget(self, target: IncludeExcludeTarget ) -> None:
        """
        Cython signature: void addExcludeTarget(IncludeExcludeTarget target)
        """
        ...
    
    def setSourceFiles(self, source_files: List[SourceFile] ) -> None:
        """
        Cython signature: void setSourceFiles(libcpp_vector[SourceFile] source_files)
        """
        ...
    
    def getSourceFiles(self) -> List[SourceFile]:
        """
        Cython signature: libcpp_vector[SourceFile] getSourceFiles()
        """
        ...
    
    def addSourceFile(self, source_file: SourceFile ) -> None:
        """
        Cython signature: void addSourceFile(SourceFile source_file)
        """
        ...
    
    def containsInvalidReferences(self) -> bool:
        """
        Cython signature: bool containsInvalidReferences()
        """
        ...
    
    def __richcmp__(self, other: TargetedExperiment, op: int) -> Any:
        ... 


class TraceInfo:
    """
    Cython implementation of _TraceInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TraceInfo.html>`_
    """
    
    name: bytes
    
    description: bytes
    
    opened: bool
    
    @overload
    def __init__(self, n: Union[bytes, str] , d: Union[bytes, str] , o: bool ) -> None:
        """
        Cython signature: void TraceInfo(libcpp_utf8_string n, libcpp_utf8_string d, bool o)
        """
        ...
    
    @overload
    def __init__(self, in_0: TraceInfo ) -> None:
        """
        Cython signature: void TraceInfo(TraceInfo)
        """
        ... 


class TransformationModelLinear:
    """
    Cython implementation of _TransformationModelLinear

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TransformationModelLinear.html>`_
      -- Inherits from ['TransformationModel']
    """
    
    def __init__(self, data: List[TM_DataPoint] , params: Param ) -> None:
        """
        Cython signature: void TransformationModelLinear(libcpp_vector[TM_DataPoint] & data, Param & params)
        """
        ...
    
    def evaluate(self, value: float ) -> float:
        """
        Cython signature: double evaluate(double value)
        """
        ...
    
    def invert(self) -> None:
        """
        Cython signature: void invert()
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        """
        ...
    
    def weightData(self, data: List[TM_DataPoint] ) -> None:
        """
        Cython signature: void weightData(libcpp_vector[TM_DataPoint] & data)
        Weight the data by the given weight function
        """
        ...
    
    def checkValidWeight(self, weight: Union[bytes, str, String] , valid_weights: List[bytes] ) -> bool:
        """
        Cython signature: bool checkValidWeight(const String & weight, libcpp_vector[String] & valid_weights)
        Check for a valid weighting function string
        """
        ...
    
    def weightDatum(self, datum: float , weight: Union[bytes, str, String] ) -> float:
        """
        Cython signature: double weightDatum(double & datum, const String & weight)
        Weight the data according to the weighting function
        """
        ...
    
    def unWeightDatum(self, datum: float , weight: Union[bytes, str, String] ) -> float:
        """
        Cython signature: double unWeightDatum(double & datum, const String & weight)
        Apply the reverse of the weighting function to the data
        """
        ...
    
    def getValidXWeights(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getValidXWeights()
        Returns a list of valid x weight function stringss
        """
        ...
    
    def getValidYWeights(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getValidYWeights()
        Returns a list of valid y weight function strings
        """
        ...
    
    def unWeightData(self, data: List[TM_DataPoint] ) -> None:
        """
        Cython signature: void unWeightData(libcpp_vector[TM_DataPoint] & data)
        Unweight the data by the given weight function
        """
        ...
    
    def checkDatumRange(self, datum: float , datum_min: float , datum_max: float ) -> float:
        """
        Cython signature: double checkDatumRange(const double & datum, const double & datum_min, const double & datum_max)
        Check that the datum is within the valid min and max bounds
        """
        ...
    
    getDefaultParameters: __static_TransformationModelLinear_getDefaultParameters 


class TransitionPQPFile:
    """
    Cython implementation of _TransitionPQPFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TransitionPQPFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TransitionPQPFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: TransitionPQPFile ) -> None:
        """
        Cython signature: void TransitionPQPFile(TransitionPQPFile &)
        """
        ...
    
    def convertTargetedExperimentToPQP(self, filename: bytes , targeted_exp: TargetedExperiment ) -> None:
        """
        Cython signature: void convertTargetedExperimentToPQP(char * filename, TargetedExperiment & targeted_exp)
        Write out a targeted experiment (TraML structure) into a PQP file
        
        :param filename: The output file
        :param targeted_exp: The targeted experiment
        """
        ...
    
    @overload
    def convertPQPToTargetedExperiment(self, filename: bytes , targeted_exp: TargetedExperiment , legacy_traml_id: bool ) -> None:
        """
        Cython signature: void convertPQPToTargetedExperiment(char * filename, TargetedExperiment & targeted_exp, bool legacy_traml_id)
        Read in a PQP file and construct a targeted experiment (TraML structure)
        
        :param filename: The input file
        :param targeted_exp: The output targeted experiment
        :param legacy_traml_id: Should legacy TraML IDs be used (boolean)?
        """
        ...
    
    @overload
    def convertPQPToTargetedExperiment(self, filename: bytes , targeted_exp: LightTargetedExperiment , legacy_traml_id: bool ) -> None:
        """
        Cython signature: void convertPQPToTargetedExperiment(char * filename, LightTargetedExperiment & targeted_exp, bool legacy_traml_id)
        Read in a PQP file and construct a targeted experiment (Light transition structure)
        
        :param filename: The input file
        :param targeted_exp: The output targeted experiment
        :param legacy_traml_id: Should legacy TraML IDs be used (boolean)?
        """
        ...
    
    def convertTargetedExperimentToTSV(self, filename: bytes , targeted_exp: TargetedExperiment ) -> None:
        """
        Cython signature: void convertTargetedExperimentToTSV(char * filename, TargetedExperiment & targeted_exp)
        """
        ...
    
    @overload
    def convertTSVToTargetedExperiment(self, filename: bytes , filetype: int , targeted_exp: TargetedExperiment ) -> None:
        """
        Cython signature: void convertTSVToTargetedExperiment(char * filename, FileType filetype, TargetedExperiment & targeted_exp)
        """
        ...
    
    @overload
    def convertTSVToTargetedExperiment(self, filename: bytes , filetype: int , targeted_exp: LightTargetedExperiment ) -> None:
        """
        Cython signature: void convertTSVToTargetedExperiment(char * filename, FileType filetype, LightTargetedExperiment & targeted_exp)
        """
        ...
    
    def validateTargetedExperiment(self, targeted_exp: TargetedExperiment ) -> None:
        """
        Cython signature: void validateTargetedExperiment(TargetedExperiment targeted_exp)
        """
        ... 


class Unit:
    """
    Cython implementation of _Unit

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Unit.html>`_
    """
    
    accession: Union[bytes, str, String]
    
    name: Union[bytes, str, String]
    
    cv_ref: Union[bytes, str, String]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Unit()
        """
        ...
    
    @overload
    def __init__(self, in_0: Unit ) -> None:
        """
        Cython signature: void Unit(Unit)
        """
        ...
    
    @overload
    def __init__(self, p_accession: Union[bytes, str, String] , p_name: Union[bytes, str, String] , p_cv_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void Unit(const String & p_accession, const String & p_name, const String & p_cv_ref)
        """
        ...
    
    def __richcmp__(self, other: Unit, op: int) -> Any:
        ... 


class VersionDetails:
    """
    Cython implementation of _VersionDetails

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1VersionDetails.html>`_
    """
    
    version_major: int
    
    version_minor: int
    
    version_patch: int
    
    pre_release_identifier: Union[bytes, str, String]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void VersionDetails()
        """
        ...
    
    @overload
    def __init__(self, in_0: VersionDetails ) -> None:
        """
        Cython signature: void VersionDetails(VersionDetails &)
        """
        ...
    
    def __richcmp__(self, other: VersionDetails, op: int) -> Any:
        ...
    
    create: __static_VersionDetails_create 


class VersionInfo:
    """
    Cython implementation of _VersionInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1VersionInfo.html>`_
    """
    
    getBranch: __static_VersionInfo_getBranch
    
    getRevision: __static_VersionInfo_getRevision
    
    getTime: __static_VersionInfo_getTime
    
    getVersion: __static_VersionInfo_getVersion
    
    getVersionStruct: __static_VersionInfo_getVersionStruct 


class XFDRAlgorithm:
    """
    Cython implementation of _XFDRAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1XFDRAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void XFDRAlgorithm()
        """
        ...
    
    @overload
    def __init__(self, in_0: XFDRAlgorithm ) -> None:
        """
        Cython signature: void XFDRAlgorithm(XFDRAlgorithm &)
        """
        ...
    
    def run(self, peptide_ids: List[PeptideIdentification] , protein_id: ProteinIdentification ) -> int:
        """
        Cython signature: XFDRAlgorithm_ExitCodes run(libcpp_vector[PeptideIdentification] & peptide_ids, ProteinIdentification & protein_id)
        """
        ...
    
    def validateClassArguments(self) -> int:
        """
        Cython signature: XFDRAlgorithm_ExitCodes validateClassArguments()
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ...
    XFDRAlgorithm_ExitCodes : __XFDRAlgorithm_ExitCodes 


class DataType:
    None
    STRING_VALUE : int
    INT_VALUE : int
    DOUBLE_VALUE : int
    STRING_LIST : int
    INT_LIST : int
    DOUBLE_LIST : int
    EMPTY_VALUE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __IntensityThresholdCalculation:
    None
    MANUAL : int
    AUTOMAXBYSTDEV : int
    AUTOMAXBYPERCENT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class MZTrafoModel_MODELTYPE:
    None
    LINEAR : int
    LINEAR_WEIGHTED : int
    QUADRATIC : int
    QUADRATIC_WEIGHTED : int
    SIZE_OF_MODELTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __OpenPepXLAlgorithm_ExitCodes:
    None
    EXECUTION_OK : int
    ILLEGAL_PARAMETERS : int
    UNEXPECTED_RESULT : int
    INCOMPATIBLE_INPUT_DATA : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __PeptideIndexing_ExitCodes:
    None
    EXECUTION_OK : int
    DATABASE_EMPTY : int
    PEPTIDE_IDS_EMPTY : int
    ILLEGAL_PARAMETERS : int
    UNEXPECTED_RESULT : int
    DECOYSTRING_EMPTY : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __RETURN_STATUS:
    None
    SOLVED : int
    ITERATION_EXCEEDED : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class SIDE:
    None
    LEFT : int
    RIGHT : int
    BOTH : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class ScanMode:
    None
    UNKNOWN : int
    MASSSPECTRUM : int
    MS1SPECTRUM : int
    MSNSPECTRUM : int
    SIM : int
    SRM : int
    CRM : int
    CNG : int
    CNL : int
    PRECURSOR : int
    EMC : int
    TDF : int
    EMR : int
    EMISSION : int
    ABSORPTION : int
    SIZE_OF_SCANMODE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class UnitType:
    None
    UNIT_ONTOLOGY : int
    MS_ONTOLOGY : int
    OTHER : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class ValueType:
    None
    STRING_VALUE : int
    INT_VALUE : int
    DOUBLE_VALUE : int
    STRING_LIST : int
    INT_LIST : int
    DOUBLE_LIST : int
    EMPTY_VALUE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __XFDRAlgorithm_ExitCodes:
    None
    EXECUTION_OK : int
    ILLEGAL_PARAMETERS : int
    UNEXPECTED_RESULT : int

    def getMapping(self) -> Dict[int, str]:
       ... 

