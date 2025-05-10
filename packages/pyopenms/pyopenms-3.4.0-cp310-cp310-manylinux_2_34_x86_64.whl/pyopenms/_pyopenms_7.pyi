from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_InternalCalibration_applyTransformation(pcs: List[Precursor] , trafo: MZTrafoModel ) -> None:
    """
    Cython signature: void applyTransformation(libcpp_vector[Precursor] & pcs, MZTrafoModel & trafo)
    """
    ...

def __static_InternalCalibration_applyTransformation(spec: MSSpectrum , target_mslvl: List[int] , trafo: MZTrafoModel ) -> None:
    """
    Cython signature: void applyTransformation(MSSpectrum & spec, IntList & target_mslvl, MZTrafoModel & trafo)
    """
    ...

def __static_InternalCalibration_applyTransformation(exp: MSExperiment , target_mslvl: List[int] , trafo: MZTrafoModel ) -> None:
    """
    Cython signature: void applyTransformation(MSExperiment & exp, IntList & target_mslvl, MZTrafoModel & trafo)
    """
    ...

def __static_TransformationDescription_getModelTypes(result: List[bytes] ) -> None:
    """
    Cython signature: void getModelTypes(StringList result)
    """
    ...

def __static_CachedmzML_load(filename: Union[bytes, str, String] , exp: CachedmzML ) -> None:
    """
    Cython signature: void load(const String & filename, CachedmzML & exp)
    """
    ...

def __static_ExperimentalDesignFile_load(tsv_file: Union[bytes, str, String] , in_1: bool ) -> ExperimentalDesign:
    """
    Cython signature: ExperimentalDesign load(const String & tsv_file, bool)
    """
    ...

def __static_DateTime_now() -> DateTime:
    """
    Cython signature: DateTime now()
    """
    ...

def __static_PercolatorInfile_store(pin_file: Union[bytes, str, String] , peptide_ids: List[PeptideIdentification] , feature_set: List[bytes] , in_3: bytes , min_charge: int , max_charge: int ) -> None:
    """
    Cython signature: void store(String pin_file, libcpp_vector[PeptideIdentification] peptide_ids, StringList feature_set, libcpp_string, int min_charge, int max_charge)
    """
    ...

def __static_CachedmzML_store(filename: Union[bytes, str, String] , exp: MSExperiment ) -> None:
    """
    Cython signature: void store(const String & filename, MSExperiment exp)
    """
    ...


class AbsoluteQuantitationMethod:
    """
    Cython implementation of _AbsoluteQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AbsoluteQuantitationMethod.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AbsoluteQuantitationMethod()
        """
        ...
    
    @overload
    def __init__(self, in_0: AbsoluteQuantitationMethod ) -> None:
        """
        Cython signature: void AbsoluteQuantitationMethod(AbsoluteQuantitationMethod &)
        """
        ...
    
    def setLLOD(self, llod: float ) -> None:
        """
        Cython signature: void setLLOD(double llod)
        """
        ...
    
    def setULOD(self, ulod: float ) -> None:
        """
        Cython signature: void setULOD(double ulod)
        """
        ...
    
    def getLLOD(self) -> float:
        """
        Cython signature: double getLLOD()
        """
        ...
    
    def getULOD(self) -> float:
        """
        Cython signature: double getULOD()
        """
        ...
    
    def setLLOQ(self, lloq: float ) -> None:
        """
        Cython signature: void setLLOQ(double lloq)
        """
        ...
    
    def setULOQ(self, uloq: float ) -> None:
        """
        Cython signature: void setULOQ(double uloq)
        """
        ...
    
    def getLLOQ(self) -> float:
        """
        Cython signature: double getLLOQ()
        """
        ...
    
    def getULOQ(self) -> float:
        """
        Cython signature: double getULOQ()
        """
        ...
    
    def checkLOD(self, value: float ) -> bool:
        """
        Cython signature: bool checkLOD(double value)
        """
        ...
    
    def checkLOQ(self, value: float ) -> bool:
        """
        Cython signature: bool checkLOQ(double value)
        """
        ...
    
    def setComponentName(self, component_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setComponentName(const String & component_name)
        """
        ...
    
    def setISName(self, IS_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setISName(const String & IS_name)
        """
        ...
    
    def setFeatureName(self, feature_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFeatureName(const String & feature_name)
        """
        ...
    
    def getComponentName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getComponentName()
        """
        ...
    
    def getISName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getISName()
        """
        ...
    
    def getFeatureName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFeatureName()
        """
        ...
    
    def setConcentrationUnits(self, concentration_units: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setConcentrationUnits(const String & concentration_units)
        """
        ...
    
    def getConcentrationUnits(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getConcentrationUnits()
        """
        ...
    
    def setTransformationModel(self, transformation_model: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTransformationModel(const String & transformation_model)
        """
        ...
    
    def setTransformationModelParams(self, transformation_model_param: Param ) -> None:
        """
        Cython signature: void setTransformationModelParams(Param transformation_model_param)
        """
        ...
    
    def getTransformationModel(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTransformationModel()
        """
        ...
    
    def getTransformationModelParams(self) -> Param:
        """
        Cython signature: Param getTransformationModelParams()
        """
        ...
    
    def setNPoints(self, n_points: int ) -> None:
        """
        Cython signature: void setNPoints(int n_points)
        """
        ...
    
    def setCorrelationCoefficient(self, correlation_coefficient: float ) -> None:
        """
        Cython signature: void setCorrelationCoefficient(double correlation_coefficient)
        """
        ...
    
    def getNPoints(self) -> int:
        """
        Cython signature: int getNPoints()
        """
        ...
    
    def getCorrelationCoefficient(self) -> float:
        """
        Cython signature: double getCorrelationCoefficient()
        """
        ... 


class BSpline2d:
    """
    Cython implementation of _BSpline2d

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1BSpline2d.html>`_
    """
    
    def __init__(self, x: List[float] , y: List[float] , wave_length: float , boundary_condition: int , num_nodes: int ) -> None:
        """
        Cython signature: void BSpline2d(libcpp_vector[double] x, libcpp_vector[double] y, double wave_length, BoundaryCondition boundary_condition, size_t num_nodes)
        """
        ...
    
    def solve(self, y: List[float] ) -> bool:
        """
        Cython signature: bool solve(libcpp_vector[double] y)
        Solve the spline curve for a new set of y values. Returns false if the solution fails
        """
        ...
    
    def eval(self, x: float ) -> float:
        """
        Cython signature: double eval(double x)
        Returns the evaluation of the smoothed curve at a particular x value. If current state is not ok(), returns zero
        """
        ...
    
    def derivative(self, x: float ) -> float:
        """
        Cython signature: double derivative(double x)
        Returns the first derivative of the spline curve at the given position x. Returns zero if the current state is not ok()
        """
        ...
    
    def ok(self) -> bool:
        """
        Cython signature: bool ok()
        Returns whether the spline fit was successful
        """
        ...
    
    def debug(self, enable: bool ) -> None:
        """
        Cython signature: void debug(bool enable)
        Enable or disable debug messages from the B-spline library
        """
        ... 


class CVReference:
    """
    Cython implementation of _CVReference

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVReference.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVReference()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVReference ) -> None:
        """
        Cython signature: void CVReference(CVReference &)
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String & name)
        Sets the name of the CV reference
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the CV reference
        """
        ...
    
    def setIdentifier(self, identifier: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(const String & identifier)
        Sets the CV identifier which is referenced
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        Returns the CV identifier which is referenced
        """
        ...
    
    def __richcmp__(self, other: CVReference, op: int) -> Any:
        ... 


class CachedmzML:
    """
    Cython implementation of _CachedmzML

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CachedmzML.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CachedmzML()
        A class that uses on-disk caching to read and write spectra and chromatograms
        """
        ...
    
    @overload
    def __init__(self, in_0: CachedmzML ) -> None:
        """
        Cython signature: void CachedmzML(CachedmzML &)
        """
        ...
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void CachedmzML(String filename)
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        """
        ...
    
    def getSpectrum(self, idx: int ) -> MSSpectrum:
        """
        Cython signature: MSSpectrum getSpectrum(size_t idx)
        """
        ...
    
    def getChromatogram(self, idx: int ) -> MSChromatogram:
        """
        Cython signature: MSChromatogram getChromatogram(size_t idx)
        """
        ...
    
    def getMetaData(self) -> MSExperiment:
        """
        Cython signature: MSExperiment getMetaData()
        """
        ...
    
    load: __static_CachedmzML_load
    
    store: __static_CachedmzML_store 


class ChromatogramSettings:
    """
    Cython implementation of _ChromatogramSettings

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ChromatogramSettings.html>`_
      -- Inherits from ['MetaInfoInterface']

    Description of the chromatogram settings, provides meta-information
    about a single chromatogram.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ChromatogramSettings()
        """
        ...
    
    @overload
    def __init__(self, in_0: ChromatogramSettings ) -> None:
        """
        Cython signature: void ChromatogramSettings(ChromatogramSettings &)
        """
        ...
    
    def getProduct(self) -> Product:
        """
        Cython signature: Product getProduct()
        Returns the product ion
        """
        ...
    
    def setProduct(self, p: Product ) -> None:
        """
        Cython signature: void setProduct(Product p)
        Sets the product ion
        """
        ...
    
    def getNativeID(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNativeID()
        Returns the native identifier for the spectrum, used by the acquisition software.
        """
        ...
    
    def setNativeID(self, native_id: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNativeID(String native_id)
        Sets the native identifier for the spectrum, used by the acquisition software.
        """
        ...
    
    def getComment(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getComment()
        Returns the free-text comment
        """
        ...
    
    def setComment(self, comment: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setComment(String comment)
        Sets the free-text comment
        """
        ...
    
    def getInstrumentSettings(self) -> InstrumentSettings:
        """
        Cython signature: InstrumentSettings getInstrumentSettings()
        Returns the instrument settings of the current spectrum
        """
        ...
    
    def setInstrumentSettings(self, instrument_settings: InstrumentSettings ) -> None:
        """
        Cython signature: void setInstrumentSettings(InstrumentSettings instrument_settings)
        Sets the instrument settings of the current spectrum
        """
        ...
    
    def getAcquisitionInfo(self) -> AcquisitionInfo:
        """
        Cython signature: AcquisitionInfo getAcquisitionInfo()
        Returns the acquisition info
        """
        ...
    
    def setAcquisitionInfo(self, acquisition_info: AcquisitionInfo ) -> None:
        """
        Cython signature: void setAcquisitionInfo(AcquisitionInfo acquisition_info)
        Sets the acquisition info
        """
        ...
    
    def getSourceFile(self) -> SourceFile:
        """
        Cython signature: SourceFile getSourceFile()
        Returns the source file
        """
        ...
    
    def setSourceFile(self, source_file: SourceFile ) -> None:
        """
        Cython signature: void setSourceFile(SourceFile source_file)
        Sets the source file
        """
        ...
    
    def getPrecursor(self) -> Precursor:
        """
        Cython signature: Precursor getPrecursor()
        Returns the precursors
        """
        ...
    
    def setPrecursor(self, precursor: Precursor ) -> None:
        """
        Cython signature: void setPrecursor(Precursor precursor)
        Sets the precursors
        """
        ...
    
    def getDataProcessing(self) -> List[DataProcessing]:
        """
        Cython signature: libcpp_vector[shared_ptr[DataProcessing]] getDataProcessing()
        Returns the description of the applied processing
        """
        ...
    
    def setDataProcessing(self, in_0: List[DataProcessing] ) -> None:
        """
        Cython signature: void setDataProcessing(libcpp_vector[shared_ptr[DataProcessing]])
        Sets the description of the applied processing
        """
        ...
    
    def setChromatogramType(self, type: int ) -> None:
        """
        Cython signature: void setChromatogramType(ChromatogramType type)
        Sets the chromatogram type
        """
        ...
    
    def getChromatogramType(self) -> int:
        """
        Cython signature: ChromatogramType getChromatogramType()
        Get the chromatogram type
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
    
    def __richcmp__(self, other: ChromatogramSettings, op: int) -> Any:
        ...
    ChromatogramType : __ChromatogramType 


class ConsensusIDAlgorithm:
    """
    Cython implementation of _ConsensusIDAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def apply(self, ids: List[PeptideIdentification] , number_of_runs: int ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & ids, size_t number_of_runs)
        Calculates the consensus ID for a set of peptide identifications of one spectrum or (consensus) feature
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


class ConsensusIDAlgorithmAverage:
    """
    Cython implementation of _ConsensusIDAlgorithmAverage

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithmAverage.html>`_
      -- Inherits from ['ConsensusIDAlgorithmIdentity']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusIDAlgorithmAverage()
        """
        ...
    
    def apply(self, ids: List[PeptideIdentification] , number_of_runs: int ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & ids, size_t number_of_runs)
        Calculates the consensus ID for a set of peptide identifications of one spectrum or (consensus) feature
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


class ConsensusIDAlgorithmPEPIons:
    """
    Cython implementation of _ConsensusIDAlgorithmPEPIons

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithmPEPIons.html>`_
      -- Inherits from ['ConsensusIDAlgorithmSimilarity']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusIDAlgorithmPEPIons()
        """
        ...
    
    def apply(self, ids: List[PeptideIdentification] , number_of_runs: int ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & ids, size_t number_of_runs)
        Calculates the consensus ID for a set of peptide identifications of one spectrum or (consensus) feature
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


class ConsensusIDAlgorithmPEPMatrix:
    """
    Cython implementation of _ConsensusIDAlgorithmPEPMatrix

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithmPEPMatrix.html>`_
      -- Inherits from ['ConsensusIDAlgorithmSimilarity']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusIDAlgorithmPEPMatrix()
        """
        ...
    
    def apply(self, ids: List[PeptideIdentification] , number_of_runs: int ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & ids, size_t number_of_runs)
        Calculates the consensus ID for a set of peptide identifications of one spectrum or (consensus) feature
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


class ConsensusMapNormalizerAlgorithmMedian:
    """
    Cython implementation of _ConsensusMapNormalizerAlgorithmMedian

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ConsensusMapNormalizerAlgorithmMedian_1_1ConsensusMapNormalizerAlgorithmMedian.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusMapNormalizerAlgorithmMedian()
        """
        ...
    
    def computeMedians(self, input_map: ConsensusMap , medians: List[float] , acc_filter: Union[bytes, str, String] , desc_filter: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t computeMedians(ConsensusMap & input_map, libcpp_vector[double] & medians, const String & acc_filter, const String & desc_filter)
        Computes medians of all maps and returns index of map with most features
        """
        ...
    
    def normalizeMaps(self, input_map: ConsensusMap , method: int , acc_filter: Union[bytes, str, String] , desc_filter: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void normalizeMaps(ConsensusMap & input_map, NormalizationMethod method, const String & acc_filter, const String & desc_filter)
        Normalizes the maps of the consensusMap
        """
        ... 


class DateTime:
    """
    Cython implementation of _DateTime

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DateTime.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DateTime()
        """
        ...
    
    @overload
    def __init__(self, in_0: DateTime ) -> None:
        """
        Cython signature: void DateTime(DateTime &)
        """
        ...
    
    def setDate(self, date: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDate(String date)
        """
        ...
    
    def setTime(self, date: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTime(String date)
        """
        ...
    
    def getDate(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getDate()
        """
        ...
    
    def getTime(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTime()
        """
        ...
    
    def now(self) -> DateTime:
        """
        Cython signature: DateTime now()
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def get(self) -> Union[bytes, str, String]:
        """
        Cython signature: String get()
        """
        ...
    
    def set(self, date: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void set(String date)
        """
        ...
    
    now: __static_DateTime_now 


class ExperimentalDesignFile:
    """
    Cython implementation of _ExperimentalDesignFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ExperimentalDesignFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ExperimentalDesignFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: ExperimentalDesignFile ) -> None:
        """
        Cython signature: void ExperimentalDesignFile(ExperimentalDesignFile &)
        """
        ...
    
    load: __static_ExperimentalDesignFile_load 


class GNPSMGFFile:
    """
    Cython implementation of _GNPSMGFFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1GNPSMGFFile.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void GNPSMGFFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: GNPSMGFFile ) -> None:
        """
        Cython signature: void GNPSMGFFile(GNPSMGFFile &)
        """
        ...
    
    def store(self, consensus_file_path: Union[bytes, str, String] , mzml_file_paths: List[bytes] , out: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(const String & consensus_file_path, const StringList & mzml_file_paths, const String & out)
        Export consensus file from default workflow to GNPS MGF format
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


class GaussFitResult:
    """
    Cython implementation of _GaussFitResult

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1GaussFitResult.html>`_
    """
    
    A: float
    
    x0: float
    
    sigma: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void GaussFitResult()
        """
        ...
    
    @overload
    def __init__(self, in_0: float , in_1: float , in_2: float ) -> None:
        """
        Cython signature: void GaussFitResult(double, double, double)
        """
        ...
    
    @overload
    def __init__(self, in_0: GaussFitResult ) -> None:
        """
        Cython signature: void GaussFitResult(GaussFitResult &)
        """
        ...
    
    def eval(self, in_0: float ) -> float:
        """
        Cython signature: double eval(double)
        """
        ... 


class GaussFitter:
    """
    Cython implementation of _GaussFitter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1GaussFitter.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void GaussFitter()
        Implements a fitter for Gaussian functions
        """
        ...
    
    def setInitialParameters(self, result: GaussFitResult ) -> None:
        """
        Cython signature: void setInitialParameters(GaussFitResult & result)
        Sets the initial parameters used by the fit method as initial guess for the Gaussian
        """
        ...
    
    def fit(self, points: '_np.ndarray[Any, _np.dtype[_np.float32]]' ) -> GaussFitResult:
        """
        Cython signature: GaussFitResult fit(libcpp_vector[DPosition2] points)
        Fits a Gaussian distribution to the given data points
        """
        ... 


class HPLC:
    """
    Cython implementation of _HPLC

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1HPLC.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void HPLC()
        Representation of a HPLC experiment
        """
        ...
    
    @overload
    def __init__(self, in_0: HPLC ) -> None:
        """
        Cython signature: void HPLC(HPLC &)
        """
        ...
    
    def getInstrument(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getInstrument()
        Returns a reference to the instument name
        """
        ...
    
    def setInstrument(self, instrument: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setInstrument(String instrument)
        Sets the instument name
        """
        ...
    
    def getColumn(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getColumn()
        Returns a reference to the column description
        """
        ...
    
    def setColumn(self, column: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setColumn(String column)
        Sets the column description
        """
        ...
    
    def getTemperature(self) -> int:
        """
        Cython signature: int getTemperature()
        Returns the temperature (in degree C)
        """
        ...
    
    def setTemperature(self, temperature: int ) -> None:
        """
        Cython signature: void setTemperature(int temperature)
        Sets the temperature (in degree C)
        """
        ...
    
    def getPressure(self) -> int:
        """
        Cython signature: unsigned int getPressure()
        Returns the pressure (in bar)
        """
        ...
    
    def setPressure(self, pressure: int ) -> None:
        """
        Cython signature: void setPressure(unsigned int pressure)
        Sets the pressure (in bar)
        """
        ...
    
    def getFlux(self) -> int:
        """
        Cython signature: unsigned int getFlux()
        Returns the flux (in microliter/sec)
        """
        ...
    
    def setFlux(self, flux: int ) -> None:
        """
        Cython signature: void setFlux(unsigned int flux)
        Sets the flux (in microliter/sec)
        """
        ...
    
    def getComment(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getComment()
        Returns the comments
        """
        ...
    
    def setComment(self, comment: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setComment(String comment)
        Sets the comments
        """
        ...
    
    def getGradient(self) -> Gradient:
        """
        Cython signature: Gradient getGradient()
        Returns a mutable reference to the used gradient
        """
        ...
    
    def setGradient(self, gradient: Gradient ) -> None:
        """
        Cython signature: void setGradient(Gradient gradient)
        Sets the used gradient
        """
        ... 


class IMSAlphabet:
    """
    Cython implementation of _IMSAlphabet

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ims::IMSAlphabet_1_1IMSAlphabet.html>`_

    Holds an indexed list of bio-chemical elements.\n
    
    Presents an indexed list of bio-chemical elements of type (or derived from
    type) 'Element'. Due to indexed structure 'Alphabet' can be used similar
    to std::vector, for example to add a new element to 'Alphabet' function
    push_back(element_type) can be used. Elements or their properties (such
    as element's mass) can be accessed by index in a constant time. On the other
    hand accessing elements by their names takes linear time. Due to this and
    also the fact that 'Alphabet' is 'heavy-weighted' (consisting of
    'Element' -s or their derivatives where the depth of derivation as well is
    undefined resulting in possibly 'heavy' access operations) it is recommended
    not use 'Alphabet' directly in operations where fast access to
    'Element' 's properties is required. Instead consider to use
    'light-weighted' equivalents, such as 'Weights'
    
    
    :param map: MSExperiment to receive the identifications
    :param fmap: FeatureMap with PeptideIdentifications for the MSExperiment
    :param clear_ids: Reset peptide and protein identifications of each scan before annotating
    :param map_ms1: Attach Ids to MS1 spectra using RT mapping only (without precursor, without m/z)
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IMSAlphabet()
        """
        ...
    
    @overload
    def __init__(self, in_0: IMSAlphabet ) -> None:
        """
        Cython signature: void IMSAlphabet(IMSAlphabet &)
        """
        ...
    
    @overload
    def __init__(self, elements: List[IMSElement] ) -> None:
        """
        Cython signature: void IMSAlphabet(libcpp_vector[IMSElement] & elements)
        """
        ...
    
    @overload
    def getElement(self, name: bytes ) -> IMSElement:
        """
        Cython signature: IMSElement getElement(libcpp_string & name)
        Gets the element with 'index' and returns element with the given index in alphabet
        """
        ...
    
    @overload
    def getElement(self, index: int ) -> IMSElement:
        """
        Cython signature: IMSElement getElement(int index)
        Gets the element with 'index'
        """
        ...
    
    def getName(self, index: int ) -> bytes:
        """
        Cython signature: libcpp_string getName(int index)
        Gets the symbol of the element with an 'index' in alphabet
        """
        ...
    
    @overload
    def getMass(self, name: bytes ) -> float:
        """
        Cython signature: double getMass(libcpp_string & name)
        Gets mono isotopic mass of the element with the symbol 'name'
        """
        ...
    
    @overload
    def getMass(self, index: int ) -> float:
        """
        Cython signature: double getMass(int index)
        Gets mass of the element with an 'index' in alphabet
        """
        ...
    
    def getMasses(self, isotope_index: int ) -> List[float]:
        """
        Cython signature: libcpp_vector[double] getMasses(int isotope_index)
        Gets masses of elements isotopes given by 'isotope_index'
        """
        ...
    
    def getAverageMasses(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] getAverageMasses()
        Gets average masses of elements
        """
        ...
    
    def hasName(self, name: bytes ) -> bool:
        """
        Cython signature: bool hasName(libcpp_string & name)
        Returns true if there is an element with symbol 'name' in the alphabet, false - otherwise
        """
        ...
    
    @overload
    def push_back(self, name: bytes , value: float ) -> None:
        """
        Cython signature: void push_back(libcpp_string & name, double value)
        Adds a new element with 'name' and mass 'value'
        """
        ...
    
    @overload
    def push_back(self, element: IMSElement ) -> None:
        """
        Cython signature: void push_back(IMSElement & element)
        Adds a new 'element' to the alphabet
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        Clears the alphabet data
        """
        ...
    
    def sortByNames(self) -> None:
        """
        Cython signature: void sortByNames()
        Sorts the alphabet by names
        """
        ...
    
    def sortByValues(self) -> None:
        """
        Cython signature: void sortByValues()
        Sorts the alphabet by mass values
        """
        ...
    
    def load(self, fname: String ) -> None:
        """
        Cython signature: void load(String & fname)
        Loads the alphabet data from the file 'fname' using the default parser. If there is no file 'fname', throws an 'IOException'
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: int size()
        """
        ...
    
    def setElement(self, name: bytes , mass: float , forced: bool ) -> None:
        """
        Cython signature: void setElement(libcpp_string & name, double mass, bool forced)
        Overwrites an element in the alphabet with the 'name' with a new element constructed from the given 'name' and 'mass'
        """
        ...
    
    def erase(self, name: bytes ) -> bool:
        """
        Cython signature: bool erase(libcpp_string & name)
        Removes the element with 'name' from the alphabet
        """
        ... 


class IMSElement:
    """
    Cython implementation of _IMSElement

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ims::IMSElement_1_1IMSElement.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IMSElement()
        Represents a chemical atom with name and isotope distribution
        """
        ...
    
    @overload
    def __init__(self, in_0: IMSElement ) -> None:
        """
        Cython signature: void IMSElement(IMSElement &)
        """
        ...
    
    @overload
    def __init__(self, name: bytes , isotopes: IMSIsotopeDistribution ) -> None:
        """
        Cython signature: void IMSElement(libcpp_string & name, IMSIsotopeDistribution & isotopes)
        """
        ...
    
    @overload
    def __init__(self, name: bytes , mass: float ) -> None:
        """
        Cython signature: void IMSElement(libcpp_string & name, double mass)
        """
        ...
    
    @overload
    def __init__(self, name: bytes , nominal_mass: int ) -> None:
        """
        Cython signature: void IMSElement(libcpp_string & name, unsigned int nominal_mass)
        """
        ...
    
    def getName(self) -> bytes:
        """
        Cython signature: libcpp_string getName()
        Gets element's name
        """
        ...
    
    def setName(self, name: bytes ) -> None:
        """
        Cython signature: void setName(libcpp_string & name)
        Sets element's name
        """
        ...
    
    def getSequence(self) -> bytes:
        """
        Cython signature: libcpp_string getSequence()
        Gets element's sequence
        """
        ...
    
    def setSequence(self, sequence: bytes ) -> None:
        """
        Cython signature: void setSequence(libcpp_string & sequence)
        Sets element's sequence
        """
        ...
    
    def getNominalMass(self) -> int:
        """
        Cython signature: unsigned int getNominalMass()
        Gets element's nominal mass
        """
        ...
    
    def getMass(self, index: int ) -> float:
        """
        Cython signature: double getMass(int index)
        Gets mass of element's isotope 'index'
        """
        ...
    
    def getAverageMass(self) -> float:
        """
        Cython signature: double getAverageMass()
        Gets element's average mass
        """
        ...
    
    def getIonMass(self, electrons_number: int ) -> float:
        """
        Cython signature: double getIonMass(int electrons_number)
        Gets ion mass of element. By default ion lacks 1 electron, but this can be changed by setting other 'electrons_number'
        """
        ...
    
    def getIsotopeDistribution(self) -> IMSIsotopeDistribution:
        """
        Cython signature: IMSIsotopeDistribution getIsotopeDistribution()
        Gets element's isotope distribution
        """
        ...
    
    def setIsotopeDistribution(self, isotopes: IMSIsotopeDistribution ) -> None:
        """
        Cython signature: void setIsotopeDistribution(IMSIsotopeDistribution & isotopes)
        Sets element's isotope distribution
        """
        ...
    
    def __richcmp__(self, other: IMSElement, op: int) -> Any:
        ... 


class InternalCalibration:
    """
    Cython implementation of _InternalCalibration

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1InternalCalibration.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void InternalCalibration()
        A mass recalibration method using linear/quadratic interpolation (robust/weighted) of given reference masses
        """
        ...
    
    @overload
    def __init__(self, in_0: InternalCalibration ) -> None:
        """
        Cython signature: void InternalCalibration(InternalCalibration &)
        """
        ...
    
    @overload
    def fillCalibrants(self, in_0: MSExperiment , in_1: List[InternalCalibration_LockMass] , tol_ppm: float , lock_require_mono: bool , lock_require_iso: bool , failed_lock_masses: CalibrationData , verbose: bool ) -> int:
        """
        Cython signature: size_t fillCalibrants(MSExperiment, libcpp_vector[InternalCalibration_LockMass], double tol_ppm, bool lock_require_mono, bool lock_require_iso, CalibrationData & failed_lock_masses, bool verbose)
        Extract calibrants from Raw data (mzML)\n
        
        Lock masses are searched in each spectrum and added to the internal calibrant database\n
        
        Filters can be used to exclude spurious peaks, i.e. require the calibrant peak to be monoisotopic or
        to have a +1 isotope (should not be used for very low abundant calibrants)
        If a calibrant is not found, it is added to a 'failed_lock_masses' database which is returned and not stored internally.
        The intensity of the peaks describe the reason for failed detection: 0.0 - peak not found with the given ppm tolerance;
        1.0 - peak is not monoisotopic (can only occur if 'lock_require_mono' is true)
        2.0 - peak has no +1 isotope (can only occur if 'lock_require_iso' is true)
        
        
        :param exp: Peak map containing the lock masses
        :param ref_masses: List of lock masses
        :param tol_ppm: Search window for lock masses in 'exp'
        :param lock_require_mono: Require that a lock mass is the monoisotopic peak (i.e. not an isotope peak) -- lock mass is rejected otherwise
        :param lock_require_iso: Require that a lock mass has isotope peaks to its right -- lock mass is rejected otherwise
        :param failed_lock_masses: Set of calibration masses which were not found, i.e. their expected m/z and RT positions
        :param verbose: Print information on 'lock_require_XXX' matches during search
        :return: Number of calibration masses found
        """
        ...
    
    @overload
    def fillCalibrants(self, in_0: FeatureMap , in_1: float ) -> int:
        """
        Cython signature: size_t fillCalibrants(FeatureMap, double)
        Extract calibrants from identifications\n
        
        Extracts only the first hit from the first peptide identification of each feature
        Hits are sorted beforehand
        Ambiguities should be resolved before, e.g. using IDFilter
        RT and m/z are taken from the features, not from the identifications (for an exception see below)!\n
        
        Unassigned peptide identifications are also taken into account!
        RT and m/z are naturally taken from the IDs, since to feature is assigned
        If you do not want these IDs, remove them from the feature map before calling this function\n
        
        A filtering step is done in the m/z dimension using 'tol_ppm'
        Since precursor masses could be annotated wrongly (e.g. isotope peak instead of mono),
        larger outliers are removed before accepting an ID as calibrant
        
        
        :param fm: FeatureMap with peptide identifications
        :param tol_ppm: Only accept ID's whose theoretical mass deviates at most this much from annotated
        :return: Number of calibration masses found
        """
        ...
    
    @overload
    def fillCalibrants(self, in_0: List[PeptideIdentification] , in_1: float ) -> int:
        """
        Cython signature: size_t fillCalibrants(libcpp_vector[PeptideIdentification], double)
        Extract calibrants from identifications\n
        
        Extracts only the first hit from each peptide identification
        Hits are sorted beforehand
        Ambiguities should be resolved before, e.g. using IDFilter\n
        
        Unassigned peptide identifications are also taken into account!
        RT and m/z are naturally taken from the IDs, since to feature is assigned
        If you do not want these IDs, remove them from the feature map before calling this function\n
        
        A filtering step is done in the m/z dimension using 'tol_ppm'
        Since precursor masses could be annotated wrongly (e.g. isotope peak instead of mono),
        larger outliers are removed before accepting an ID as calibrant
        
        
        :param pep_ids: Peptide ids (e.g. from an idXML file)
        :param tol_ppm: Only accept ID's whose theoretical mass deviates at most this much from annotated
        :return: Number of calibration masses found
        """
        ...
    
    def getCalibrationPoints(self) -> CalibrationData:
        """
        Cython signature: CalibrationData getCalibrationPoints()
        Get container of calibration points\n
        
        Filled using fillCalibrants() methods
        
        
        :return: Container of calibration points
        """
        ...
    
    def calibrate(self, in_0: MSExperiment , in_1: List[int] , in_2: int , rt_chunk: float , use_RANSAC: bool , post_ppm_median: float , post_ppm_MAD: float , file_models: Union[bytes, str, String] , file_models_plot: Union[bytes, str, String] , file_residuals: Union[bytes, str, String] , file_residuals_plot: Union[bytes, str, String] , rscript_executable: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool calibrate(MSExperiment, libcpp_vector[int], MZTrafoModel_MODELTYPE, double rt_chunk, bool use_RANSAC, double post_ppm_median, double post_ppm_MAD, String file_models, String file_models_plot, String file_residuals, String file_residuals_plot, String rscript_executable)
        Apply calibration to data\n
        
        For each spectrum, a calibration model will be computed and applied.
        Make sure to call fillCalibrants() before, so a model can be created.\n
        
        The MSExperiment will be sorted by RT and m/z if unsorted.
        
        
        :param exp: MSExperiment holding the Raw data to calibrate
        :param target_mslvl: MS-levels where calibration should be applied to
        :param model_type: Linear or quadratic model; select based on your instrument
        :param rt_chunk: RT-window size (one-sided) of calibration points to collect around each spectrum. Set to negative values, to build one global model instead.
        :param use_RANSAC: Remove outliers before fitting a model?!
        :param post_ppm_median: The median ppm error of the calibrants must be at least this good after calibration; otherwise this method returns false(fail)
        :param post_ppm_MAD: The median absolute deviation of the calibrants must be at least this good after calibration; otherwise this method returns false(fail)
        :param file_models: Output CSV filename, where model parameters are written to (pass empty string to skip)
        :param file_models_plot: Output PNG image model parameters (pass empty string to skip)
        :param file_residuals: Output CSV filename, where ppm errors of calibrants before and after model fitting parameters are written to (pass empty string to skip)
        :param file_residuals_plot: Output PNG image of the ppm errors of calibrants (pass empty string to skip)
        :param rscript_executable: Full path to the Rscript executable
        :return: true upon successful calibration
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
    
    applyTransformation: __static_InternalCalibration_applyTransformation
    
    applyTransformation: __static_InternalCalibration_applyTransformation
    
    applyTransformation: __static_InternalCalibration_applyTransformation 


class InternalCalibration_LockMass:
    """
    Cython implementation of _InternalCalibration_LockMass

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1InternalCalibration_LockMass.html>`_
    """
    
    mz: float
    
    ms_level: int
    
    charge: int
    
    @overload
    def __init__(self, mz_: float , lvl_: int , charge_: int ) -> None:
        """
        Cython signature: void InternalCalibration_LockMass(double mz_, int lvl_, int charge_)
        """
        ...
    
    @overload
    def __init__(self, in_0: InternalCalibration_LockMass ) -> None:
        """
        Cython signature: void InternalCalibration_LockMass(InternalCalibration_LockMass &)
        """
        ... 


class IsobaricChannelInformation:
    """
    Cython implementation of _IsobaricChannelInformation

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IsobaricQuantitationMethod_1_1IsobaricChannelInformation.html>`_
    """
    
    name: Union[bytes, str, String]
    
    id: int
    
    description: Union[bytes, str, String]
    
    center: float
    
    affected_channels: List[int]
    
    @overload
    def __init__(self, name: Union[bytes, str, String] , id_: int , description: Union[bytes, str, String] , center: float , affected_channels: List[int] ) -> None:
        """
        Cython signature: void IsobaricChannelInformation(String name, int id_, String description, double center, libcpp_vector[int] affected_channels)
        """
        ...
    
    @overload
    def __init__(self, in_0: IsobaricChannelInformation ) -> None:
        """
        Cython signature: void IsobaricChannelInformation(IsobaricChannelInformation &)
        """
        ... 


class IsobaricIsotopeCorrector:
    """
    Cython implementation of _IsobaricIsotopeCorrector

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsobaricIsotopeCorrector.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IsobaricIsotopeCorrector()
        """
        ...
    
    @overload
    def __init__(self, in_0: IsobaricIsotopeCorrector ) -> None:
        """
        Cython signature: void IsobaricIsotopeCorrector(IsobaricIsotopeCorrector &)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: ItraqEightPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, ItraqEightPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: ItraqFourPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, ItraqFourPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: TMTSixPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, TMTSixPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: TMTTenPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, TMTTenPlexQuantitationMethod * quant_method)
        """
        ... 


class IsobaricQuantifier:
    """
    Cython implementation of _IsobaricQuantifier

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsobaricQuantifier.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, in_0: IsobaricQuantifier ) -> None:
        """
        Cython signature: void IsobaricQuantifier(IsobaricQuantifier &)
        """
        ...
    
    @overload
    def __init__(self, quant_method: ItraqFourPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricQuantifier(ItraqFourPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: ItraqEightPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricQuantifier(ItraqEightPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: TMTSixPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricQuantifier(TMTSixPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: TMTTenPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricQuantifier(TMTTenPlexQuantitationMethod * quant_method)
        """
        ...
    
    def quantify(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap ) -> None:
        """
        Cython signature: void quantify(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out)
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


class KDTreeFeatureMaps:
    """
    Cython implementation of _KDTreeFeatureMaps

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1KDTreeFeatureMaps.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void KDTreeFeatureMaps()
        Stores a set of features, together with a 2D tree for fast search
        """
        ...
    
    @overload
    def __init__(self, maps: List[FeatureMap] , param: Param ) -> None:
        """
        Cython signature: void KDTreeFeatureMaps(libcpp_vector[FeatureMap] & maps, Param & param)
        """
        ...
    
    @overload
    def __init__(self, maps: List[ConsensusMap] , param: Param ) -> None:
        """
        Cython signature: void KDTreeFeatureMaps(libcpp_vector[ConsensusMap] & maps, Param & param)
        """
        ...
    
    @overload
    def addMaps(self, maps: List[FeatureMap] ) -> None:
        """
        Cython signature: void addMaps(libcpp_vector[FeatureMap] & maps)
        Add `maps` and balance kd-tree
        """
        ...
    
    @overload
    def addMaps(self, maps: List[ConsensusMap] ) -> None:
        """
        Cython signature: void addMaps(libcpp_vector[ConsensusMap] & maps)
        """
        ...
    
    def rt(self, i: int ) -> float:
        """
        Cython signature: double rt(size_t i)
        """
        ...
    
    def mz(self, i: int ) -> float:
        """
        Cython signature: double mz(size_t i)
        """
        ...
    
    def intensity(self, i: int ) -> float:
        """
        Cython signature: float intensity(size_t i)
        """
        ...
    
    def charge(self, i: int ) -> int:
        """
        Cython signature: int charge(size_t i)
        """
        ...
    
    def mapIndex(self, i: int ) -> int:
        """
        Cython signature: size_t mapIndex(size_t i)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def treeSize(self) -> int:
        """
        Cython signature: size_t treeSize()
        """
        ...
    
    def numMaps(self) -> int:
        """
        Cython signature: size_t numMaps()
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def optimizeTree(self) -> None:
        """
        Cython signature: void optimizeTree()
        """
        ...
    
    def getNeighborhood(self, index: int , result_indices: List[int] , rt_tol: float , mz_tol: float , mz_ppm: bool , include_features_from_same_map: bool , max_pairwise_log_fc: float ) -> None:
        """
        Cython signature: void getNeighborhood(size_t index, libcpp_vector[size_t] & result_indices, double rt_tol, double mz_tol, bool mz_ppm, bool include_features_from_same_map, double max_pairwise_log_fc)
        Fill `result` with indices of all features compatible (wrt. RT, m/z, map index) to the feature with `index`
        """
        ...
    
    def queryRegion(self, rt_low: float , rt_high: float , mz_low: float , mz_high: float , result_indices: List[int] , ignored_map_index: int ) -> None:
        """
        Cython signature: void queryRegion(double rt_low, double rt_high, double mz_low, double mz_high, libcpp_vector[size_t] & result_indices, size_t ignored_map_index)
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


class LinearResamplerAlign:
    """
    Cython implementation of _LinearResamplerAlign

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1LinearResamplerAlign.html>`_
      -- Inherits from ['LinearResampler']
    """
    
    def __init__(self, in_0: LinearResamplerAlign ) -> None:
        """
        Cython signature: void LinearResamplerAlign(LinearResamplerAlign &)
        """
        ...
    
    def raster(self, input: MSSpectrum ) -> None:
        """
        Cython signature: void raster(MSSpectrum & input)
        Applies the resampling algorithm to an MSSpectrum
        """
        ...
    
    def rasterExperiment(self, input: MSExperiment ) -> None:
        """
        Cython signature: void rasterExperiment(MSExperiment & input)
        Resamples the data in an MSExperiment
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


class MRMMapping:
    """
    Cython implementation of _MRMMapping

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMMapping.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MRMMapping()
        """
        ...
    
    def mapExperiment(self, input_chromatograms: MSExperiment , targeted_exp: TargetedExperiment , output: MSExperiment ) -> None:
        """
        Cython signature: void mapExperiment(MSExperiment input_chromatograms, TargetedExperiment targeted_exp, MSExperiment & output)
        Maps input chromatograms to assays in a targeted experiment
        
        The output chromatograms are an annotated copy of the input chromatograms
        with native id, precursor information and peptide sequence (if available)
        annotated in the chromatogram files
        
        The algorithm tries to match a given set of chromatograms and targeted
        assays. It iterates through all the chromatograms retrieves one or more
        matching targeted assay for the chromatogram. By default, the algorithm
        assumes that a 1:1 mapping exists. If a chromatogram cannot be mapped
        (does not have a corresponding assay) the algorithm issues a warning, the
        user can specify that the program should abort in such a case (see
        error_on_unmapped)
        
        :note If multiple mapping is enabled (see map_multiple_assays parameter)
        then each mapped assay will get its own chromatogram that contains the
        same raw data but different meta-annotation. This *can* be useful if the
        same transition is used to monitor multiple analytes but may also
        indicate a problem with too wide mapping tolerances
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


class MSChromatogram:
    """
    Cython implementation of _MSChromatogram

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSChromatogram.html>`_
      -- Inherits from ['ChromatogramSettings', 'RangeManagerRtInt']

    The representation of a chromatogram.
    Raw data access is proved by `get_peaks` and `set_peaks`, which yields numpy arrays
    Iterations yields access to underlying peak objects but is slower
    Extra data arrays can be accessed through getFloatDataArrays / getIntegerDataArrays / getStringDataArrays
    See help(ChromatogramSettings) for information about meta-information
    
    Usage:
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MSChromatogram()
        """
        ...
    
    @overload
    def __init__(self, in_0: MSChromatogram ) -> None:
        """
        Cython signature: void MSChromatogram(MSChromatogram &)
        """
        ...
    
    def getMZ(self) -> float:
        """
        Cython signature: double getMZ()
        Returns the mz of the product entry, makes sense especially for MRM scans
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
        Cython signature: void setName(String)
        Sets the name
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def reserve(self, n: int ) -> None:
        """
        Cython signature: void reserve(size_t n)
        """
        ...
    
    def resize(self, n: int ) -> None:
        """
        Cython signature: void resize(size_t n)
        Resize the peak array
        """
        ...
    
    def __getitem__(self, in_0: int ) -> ChromatogramPeak:
        """
        Cython signature: ChromatogramPeak & operator[](size_t)
        """
        ...
    def __setitem__(self, key: int, value: ChromatogramPeak ) -> None:
        """Cython signature: ChromatogramPeak & operator[](size_t)"""
        ...
    
    def updateRanges(self) -> None:
        """
        Cython signature: void updateRanges()
        """
        ...
    
    def clear(self, in_0: int ) -> None:
        """
        Cython signature: void clear(int)
        Clears all data and meta data
        
        
        :param clear_meta_data: If true, all meta data is cleared in addition to the data
        """
        ...
    
    def push_back(self, in_0: ChromatogramPeak ) -> None:
        """
        Cython signature: void push_back(ChromatogramPeak)
        Append a peak
        """
        ...
    
    def isSorted(self) -> bool:
        """
        Cython signature: bool isSorted()
        Checks if all peaks are sorted with respect to ascending RT
        """
        ...
    
    def sortByIntensity(self, reverse: bool ) -> None:
        """
        Cython signature: void sortByIntensity(bool reverse)
        Lexicographically sorts the peaks by their intensity
        
        
        Sorts the peaks according to ascending intensity. Meta data arrays will be sorted accordingly
        """
        ...
    
    def sortByPosition(self) -> None:
        """
        Cython signature: void sortByPosition()
        Lexicographically sorts the peaks by their position
        
        
        The chromatogram is sorted with respect to position. Meta data arrays will be sorted accordingly
        """
        ...
    
    def findNearest(self, in_0: float ) -> int:
        """
        Cython signature: int findNearest(double)
        Binary search for the peak nearest to a specific RT
        :note: Make sure the chromatogram is sorted with respect to RT! Otherwise the result is undefined
        
        
        :param rt: The searched for mass-to-charge ratio searched
        :return: Returns the index of the peak.
        :raises:
          Exception: Precondition is thrown if the chromatogram is empty (not only in debug mode)
        """
        ...
    
    def getFloatDataArrays(self) -> List[FloatDataArray]:
        """
        Cython signature: libcpp_vector[FloatDataArray] getFloatDataArrays()
        Returns a reference to the float meta data arrays
        """
        ...
    
    def getIntegerDataArrays(self) -> List[IntegerDataArray]:
        """
        Cython signature: libcpp_vector[IntegerDataArray] getIntegerDataArrays()
        Returns a reference to the integer meta data arrays
        """
        ...
    
    def getStringDataArrays(self) -> List[StringDataArray]:
        """
        Cython signature: libcpp_vector[StringDataArray] getStringDataArrays()
        Returns a reference to the string meta data arrays
        """
        ...
    
    def setFloatDataArrays(self, fda: List[FloatDataArray] ) -> None:
        """
        Cython signature: void setFloatDataArrays(libcpp_vector[FloatDataArray] fda)
        Sets the float meta data arrays
        """
        ...
    
    def setIntegerDataArrays(self, ida: List[IntegerDataArray] ) -> None:
        """
        Cython signature: void setIntegerDataArrays(libcpp_vector[IntegerDataArray] ida)
        Sets the integer meta data arrays
        """
        ...
    
    def setStringDataArrays(self, sda: List[StringDataArray] ) -> None:
        """
        Cython signature: void setStringDataArrays(libcpp_vector[StringDataArray] sda)
        Sets the string meta data arrays
        """
        ...
    
    def getProduct(self) -> Product:
        """
        Cython signature: Product getProduct()
        Returns the product ion
        """
        ...
    
    def setProduct(self, p: Product ) -> None:
        """
        Cython signature: void setProduct(Product p)
        Sets the product ion
        """
        ...
    
    def getNativeID(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNativeID()
        Returns the native identifier for the spectrum, used by the acquisition software.
        """
        ...
    
    def setNativeID(self, native_id: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNativeID(String native_id)
        Sets the native identifier for the spectrum, used by the acquisition software.
        """
        ...
    
    def getComment(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getComment()
        Returns the free-text comment
        """
        ...
    
    def setComment(self, comment: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setComment(String comment)
        Sets the free-text comment
        """
        ...
    
    def getInstrumentSettings(self) -> InstrumentSettings:
        """
        Cython signature: InstrumentSettings getInstrumentSettings()
        Returns the instrument settings of the current spectrum
        """
        ...
    
    def setInstrumentSettings(self, instrument_settings: InstrumentSettings ) -> None:
        """
        Cython signature: void setInstrumentSettings(InstrumentSettings instrument_settings)
        Sets the instrument settings of the current spectrum
        """
        ...
    
    def getAcquisitionInfo(self) -> AcquisitionInfo:
        """
        Cython signature: AcquisitionInfo getAcquisitionInfo()
        Returns the acquisition info
        """
        ...
    
    def setAcquisitionInfo(self, acquisition_info: AcquisitionInfo ) -> None:
        """
        Cython signature: void setAcquisitionInfo(AcquisitionInfo acquisition_info)
        Sets the acquisition info
        """
        ...
    
    def getSourceFile(self) -> SourceFile:
        """
        Cython signature: SourceFile getSourceFile()
        Returns the source file
        """
        ...
    
    def setSourceFile(self, source_file: SourceFile ) -> None:
        """
        Cython signature: void setSourceFile(SourceFile source_file)
        Sets the source file
        """
        ...
    
    def getPrecursor(self) -> Precursor:
        """
        Cython signature: Precursor getPrecursor()
        Returns the precursors
        """
        ...
    
    def setPrecursor(self, precursor: Precursor ) -> None:
        """
        Cython signature: void setPrecursor(Precursor precursor)
        Sets the precursors
        """
        ...
    
    def getDataProcessing(self) -> List[DataProcessing]:
        """
        Cython signature: libcpp_vector[shared_ptr[DataProcessing]] getDataProcessing()
        Returns the description of the applied processing
        """
        ...
    
    def setDataProcessing(self, in_0: List[DataProcessing] ) -> None:
        """
        Cython signature: void setDataProcessing(libcpp_vector[shared_ptr[DataProcessing]])
        Sets the description of the applied processing
        """
        ...
    
    def setChromatogramType(self, type: int ) -> None:
        """
        Cython signature: void setChromatogramType(ChromatogramType type)
        Sets the chromatogram type
        """
        ...
    
    def getChromatogramType(self) -> int:
        """
        Cython signature: ChromatogramType getChromatogramType()
        Get the chromatogram type
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
    
    def getMinRT(self) -> float:
        """
        Cython signature: double getMinRT()
        Returns the minimum RT
        """
        ...
    
    def getMaxRT(self) -> float:
        """
        Cython signature: double getMaxRT()
        Returns the maximum RT
        """
        ...
    
    def getMinIntensity(self) -> float:
        """
        Cython signature: double getMinIntensity()
        Returns the minimum intensity
        """
        ...
    
    def getMaxIntensity(self) -> float:
        """
        Cython signature: double getMaxIntensity()
        Returns the maximum intensity
        """
        ...
    
    def clearRanges(self) -> None:
        """
        Cython signature: void clearRanges()
        Resets all range dimensions as empty
        """
        ...
    
    def __richcmp__(self, other: MSChromatogram, op: int) -> Any:
        ...
    
    def __iter__(self) -> ChromatogramPeak:
       ... 


class MSstatsFile:
    """
    Cython implementation of _MSstatsFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSstatsFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MSstatsFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MSstatsFile ) -> None:
        """
        Cython signature: void MSstatsFile(MSstatsFile &)
        """
        ...
    
    def storeLFQ(self, filename: String , consensus_map: ConsensusMap , design: ExperimentalDesign , reannotate_filenames: List[bytes] , is_isotope_label_type: bool , bioreplicate: String , condition: String , retention_time_summarization_method: String ) -> None:
        """
        Cython signature: void storeLFQ(String & filename, ConsensusMap & consensus_map, ExperimentalDesign & design, StringList & reannotate_filenames, bool is_isotope_label_type, String & bioreplicate, String & condition, String & retention_time_summarization_method)
        Store label free experiment (MSstats)
        """
        ...
    
    def storeISO(self, filename: String , consensus_map: ConsensusMap , design: ExperimentalDesign , reannotate_filenames: List[bytes] , bioreplicate: String , condition: String , mixture: String , retention_time_summarization_method: String ) -> None:
        """
        Cython signature: void storeISO(String & filename, ConsensusMap & consensus_map, ExperimentalDesign & design, StringList & reannotate_filenames, String & bioreplicate, String & condition, String & mixture, String & retention_time_summarization_method)
        Store isobaric experiment (MSstatsTMT)
        """
        ... 


class MassDecompositionAlgorithm:
    """
    Cython implementation of _MassDecompositionAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MassDecompositionAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MassDecompositionAlgorithm()
        """
        ...
    
    def getDecompositions(self, decomps: List[MassDecomposition] , weight: float ) -> None:
        """
        Cython signature: void getDecompositions(libcpp_vector[MassDecomposition] & decomps, double weight)
        Returns the possible decompositions given the weight
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


class MassExplainer:
    """
    Cython implementation of _MassExplainer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MassExplainer.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MassExplainer()
        Computes empirical formulas for given mass differences using a set of allowed elements
        """
        ...
    
    @overload
    def __init__(self, in_0: MassExplainer ) -> None:
        """
        Cython signature: void MassExplainer(MassExplainer &)
        """
        ...
    
    @overload
    def __init__(self, adduct_base: List[Adduct] ) -> None:
        """
        Cython signature: void MassExplainer(libcpp_vector[Adduct] adduct_base)
        """
        ...
    
    @overload
    def __init__(self, q_min: int , q_max: int , max_span: int , thresh_logp: float ) -> None:
        """
        Cython signature: void MassExplainer(int q_min, int q_max, int max_span, double thresh_logp)
        """
        ...
    
    def setAdductBase(self, adduct_base: List[Adduct] ) -> None:
        """
        Cython signature: void setAdductBase(libcpp_vector[Adduct] adduct_base)
        Sets the set of possible adducts
        """
        ...
    
    def getAdductBase(self) -> List[Adduct]:
        """
        Cython signature: libcpp_vector[Adduct] getAdductBase()
        Returns the set of adducts
        """
        ...
    
    def getCompomerById(self, id: int ) -> Compomer:
        """
        Cython signature: Compomer getCompomerById(size_t id)
        Returns a compomer by its Id (useful after a query() )
        """
        ...
    
    def compute(self) -> None:
        """
        Cython signature: void compute()
        Fill map with possible mass-differences along with their explanation
        """
        ... 


class MetaInfoInterface:
    """
    Cython implementation of _MetaInfoInterface

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaInfoInterface.html>`_

    Interface for classes that can store arbitrary meta information
    (Type-Name-Value tuples).
    
    MetaInfoInterface is a base class for all classes that use one MetaInfo
    object as member.  If you want to add meta information to a class, let it
    publicly inherit the MetaInfoInterface.  Meta information is an array of
    Type-Name-Value tuples.
    
    Usage:
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaInfoInterface()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaInfoInterface ) -> None:
        """
        Cython signature: void MetaInfoInterface(MetaInfoInterface &)
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
    
    def __richcmp__(self, other: MetaInfoInterface, op: int) -> Any:
        ... 


class MetaInfoRegistry:
    """
    Cython implementation of _MetaInfoRegistry

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaInfoRegistry.html>`_

    Registry which assigns unique integer indices to strings
    
    When registering a new name an index >= 1024 is assigned.
    Indices from 1 to 1023 are reserved for fast access and will never change:
    1 - isotopic_range
    2 - cluster_id
    3 - label
    4 - icon
    5 - color
    6 - RT
    7 - MZ
    8 - predicted_RT
    9 - predicted_RT_p_value
    10 - spectrum_reference
    11 - ID
    12 - low_quality
    13 - charge
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaInfoRegistry()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaInfoRegistry ) -> None:
        """
        Cython signature: void MetaInfoRegistry(MetaInfoRegistry &)
        """
        ...
    
    def registerName(self, name: Union[bytes, str, String] , description: Union[bytes, str, String] , unit: Union[bytes, str, String] ) -> int:
        """
        Cython signature: unsigned int registerName(const String & name, const String & description, const String & unit)
        Registers a string, stores its description and unit, and returns the corresponding index. If the string is already registered, it returns the index of the string
        """
        ...
    
    @overload
    def setDescription(self, index: int , description: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDescription(unsigned int index, const String & description)
        Sets the description (String), corresponding to an index
        """
        ...
    
    @overload
    def setDescription(self, name: Union[bytes, str, String] , description: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDescription(const String & name, const String & description)
        Sets the description (String), corresponding to a name
        """
        ...
    
    @overload
    def setUnit(self, index: int , unit: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setUnit(unsigned int index, const String & unit)
        Sets the unit (String), corresponding to an index
        """
        ...
    
    @overload
    def setUnit(self, name: Union[bytes, str, String] , unit: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setUnit(const String & name, const String & unit)
        Sets the unit (String), corresponding to a name
        """
        ...
    
    def getIndex(self, name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: unsigned int getIndex(const String & name)
        Returns the integer index corresponding to a string. If the string is not registered, returns UInt(-1) (= UINT_MAX)
        """
        ...
    
    def getName(self, index: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String getName(unsigned int index)
        Returns the corresponding name to an index
        """
        ...
    
    @overload
    def getDescription(self, index: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String getDescription(unsigned int index)
        Returns the description of an index
        """
        ...
    
    @overload
    def getDescription(self, name: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String getDescription(const String & name)
        Returns the description of a name
        """
        ...
    
    @overload
    def getUnit(self, index: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String getUnit(unsigned int index)
        Returns the unit of an index
        """
        ...
    
    @overload
    def getUnit(self, name: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String getUnit(const String & name)
        Returns the unit of a name
        """
        ... 


class MetaboTargetedAssay:
    """
    Cython implementation of _MetaboTargetedAssay

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaboTargetedAssay.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaboTargetedAssay()
        This class provides methods for the extraction of targeted assays for metabolomics
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaboTargetedAssay ) -> None:
        """
        Cython signature: void MetaboTargetedAssay(MetaboTargetedAssay &)
        """
        ...
    
    def extractMetaboTargetedAssay(self, spectra: MSExperiment , feature_ms2_index: FeatureMapping_FeatureToMs2Indices , precursor_rt_tol: float , precursor_mz_distance: float , cosine_sim_threshold: float , transition_threshold: float , min_fragment_mz: float , max_fragment_mz: float , method_consensus_spectrum: bool , exclude_ms2_precursor: bool , file_counter: int ) -> List[MetaboTargetedAssay]:
        """
        Cython signature: libcpp_vector[MetaboTargetedAssay] extractMetaboTargetedAssay(MSExperiment & spectra, FeatureMapping_FeatureToMs2Indices & feature_ms2_index, double & precursor_rt_tol, double & precursor_mz_distance, double & cosine_sim_threshold, double & transition_threshold, double & min_fragment_mz, double & max_fragment_mz, bool & method_consensus_spectrum, bool & exclude_ms2_precursor, unsigned int & file_counter)
        Extract a vector of MetaboTargetedAssays without using fragment annotation
        
        
        :param spectra: Input of MSExperiment with spectra information
        :param feature_ms2_spectra_map: FeatureMapping class with associated MS2 spectra
        :param precursor_rt_tol: Retention time tolerance of the precursor
        :param precursor_mz_distance: Max m/z distance of the precursor entries of two spectra to be merged
        :param cosine_sim_threshold: Cosine similarty threshold for the usage of SpectraMerger
        :param transition_threshold: Intensity threshold for MS2 peak used in MetaboTargetedAssay
        :param min_fragment_mz: Minimum m/z a fragment ion has to have to be considered as a transition
        :param max_fragment_mz: Maximum m/z a fragment ion has to have to be considered as a transition
        :param method_consensus_spectrum: Boolean to use consensus spectrum method
        :param exclude_ms2_precursor: Boolean to exclude MS2 precursor from MetaboTargetedAssay
        :return: Vector of MetaboTargetedAssay
        """
        ...
    
    def extractMetaboTargetedAssayFragmentAnnotation(self, v_cmp_spec: List[MetaboTargetedAssay_CompoundTargetDecoyPair] , transition_threshold: float , min_fragment_mz: float , max_fragment_mz: float , use_exact_mass: bool , exclude_ms2_precursor: bool ) -> List[MetaboTargetedAssay]:
        """
        Cython signature: libcpp_vector[MetaboTargetedAssay] extractMetaboTargetedAssayFragmentAnnotation(libcpp_vector[MetaboTargetedAssay_CompoundTargetDecoyPair] & v_cmp_spec, double & transition_threshold, double & min_fragment_mz, double & max_fragment_mz, bool & use_exact_mass, bool & exclude_ms2_precursor)
        Extract a vector of MetaboTargetedAssays using fragment
        
        
        :param v_cmp_spec: Vector of CompoundInfo with associated fragment annotated MSspectrum
        :param transition_threshold: Intensity threshold for MS2 peak used in MetaboTargetedAssay
        :param min_fragment_mz: Minimum m/z a fragment ion has to have to be considered as a transition
        :param max_fragment_mz: Maximum m/z a fragment ion has to have to be considered as a transition
        :param use_exact_mass: Boolean if exact mass should be used as peak mass for annotated fragments
        :param exclude_ms2_precursor: Boolean to exclude MS2 precursor from MetaboTargetedAssay
        :param file_counter: Count if multiple files are used.
        :return: Vector of MetaboTargetedAssay
        """
        ...
    
    def pairCompoundWithAnnotatedTDSpectraPairs(self, v_cmpinfo: List[SiriusMSFile_CompoundInfo] , annotated_spectra: List[SiriusFragmentAnnotation_SiriusTargetDecoySpectra] ) -> List[MetaboTargetedAssay_CompoundTargetDecoyPair]:
        """
        Cython signature: libcpp_vector[MetaboTargetedAssay_CompoundTargetDecoyPair] pairCompoundWithAnnotatedTDSpectraPairs(libcpp_vector[SiriusMSFile_CompoundInfo] & v_cmpinfo, libcpp_vector[SiriusFragmentAnnotation_SiriusTargetDecoySpectra] & annotated_spectra)
        Pair compound information (SiriusMSFile) with the annotated target and decoy spectrum from SIRIUS/Passatutto based on the m_id (unique identifier composed of description_filepath_native_id_k introduced in the SiriusMSConverter)
        
        
        :param v_cmpinfo: Vector of SiriusMSFile::CompoundInfo
        :param annotated_spectra: Vector of SiriusTargetDecoySpectra
        :return: Vector of MetaboTargetedAssay::CompoundTargetDecoyPair
        """
        ... 


class MetaboTargetedAssay_CompoundTargetDecoyPair:
    """
    Cython implementation of _MetaboTargetedAssay_CompoundTargetDecoyPair

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaboTargetedAssay_CompoundTargetDecoyPair.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaboTargetedAssay_CompoundTargetDecoyPair()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaboTargetedAssay_CompoundTargetDecoyPair ) -> None:
        """
        Cython signature: void MetaboTargetedAssay_CompoundTargetDecoyPair(MetaboTargetedAssay_CompoundTargetDecoyPair &)
        """
        ... 


class ModificationDefinitionsSet:
    """
    Cython implementation of _ModificationDefinitionsSet

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ModificationDefinitionsSet.html>`_

    Representation of a set of modification definitions
    
    This class enhances the modification definitions as defined in the
    class ModificationDefinition into a set of definitions. This is also
    e.g. used as input parameters in search engines.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ModificationDefinitionsSet()
        """
        ...
    
    @overload
    def __init__(self, in_0: ModificationDefinitionsSet ) -> None:
        """
        Cython signature: void ModificationDefinitionsSet(ModificationDefinitionsSet &)
        """
        ...
    
    @overload
    def __init__(self, fixed_modifications: List[bytes] , variable_modifications: List[bytes] ) -> None:
        """
        Cython signature: void ModificationDefinitionsSet(StringList fixed_modifications, StringList variable_modifications)
        """
        ...
    
    def setMaxModifications(self, max_mod: int ) -> None:
        """
        Cython signature: void setMaxModifications(size_t max_mod)
        Sets the maximal number of modifications allowed per peptide
        """
        ...
    
    def getMaxModifications(self) -> int:
        """
        Cython signature: size_t getMaxModifications()
        Return the maximal number of modifications allowed per peptide
        """
        ...
    
    def getNumberOfModifications(self) -> int:
        """
        Cython signature: size_t getNumberOfModifications()
        Returns the number of modifications stored in this set
        """
        ...
    
    def getNumberOfFixedModifications(self) -> int:
        """
        Cython signature: size_t getNumberOfFixedModifications()
        Returns the number of fixed modifications stored in this set
        """
        ...
    
    def getNumberOfVariableModifications(self) -> int:
        """
        Cython signature: size_t getNumberOfVariableModifications()
        Returns the number of variable modifications stored in this set
        """
        ...
    
    def addModification(self, mod_def: ModificationDefinition ) -> None:
        """
        Cython signature: void addModification(ModificationDefinition & mod_def)
        Adds a modification definition to the set
        """
        ...
    
    @overload
    def setModifications(self, mod_defs: Set[ModificationDefinition] ) -> None:
        """
        Cython signature: void setModifications(libcpp_set[ModificationDefinition] & mod_defs)
        Sets the modification definitions
        """
        ...
    
    @overload
    def setModifications(self, fixed_modifications: Union[bytes, str, String] , variable_modifications: String ) -> None:
        """
        Cython signature: void setModifications(const String & fixed_modifications, String & variable_modifications)
        Set the modification definitions from a string
        
        The strings should contain a comma separated list of modifications. The names
        can be PSI-MOD identifier or any other unique name supported by PSI-MOD. TermSpec
        definitions and other specific definitions are given by the modifications themselves.
        """
        ...
    
    @overload
    def setModifications(self, fixed_modifications: List[bytes] , variable_modifications: List[bytes] ) -> None:
        """
        Cython signature: void setModifications(StringList & fixed_modifications, StringList & variable_modifications)
        Same as above, but using StringList instead of comma separated strings
        """
        ...
    
    def getModifications(self) -> Set[ModificationDefinition]:
        """
        Cython signature: libcpp_set[ModificationDefinition] getModifications()
        Returns the stored modification definitions
        """
        ...
    
    def getFixedModifications(self) -> Set[ModificationDefinition]:
        """
        Cython signature: libcpp_set[ModificationDefinition] getFixedModifications()
        Returns the stored fixed modification definitions
        """
        ...
    
    def getVariableModifications(self) -> Set[ModificationDefinition]:
        """
        Cython signature: libcpp_set[ModificationDefinition] getVariableModifications()
        Returns the stored variable modification definitions
        """
        ...
    
    @overload
    def getModificationNames(self, fixed_modifications: List[bytes] , variable_modifications: List[bytes] ) -> None:
        """
        Cython signature: void getModificationNames(StringList & fixed_modifications, StringList & variable_modifications)
        Populates the output lists with the modification names (use e.g. for
        """
        ...
    
    @overload
    def getModificationNames(self, ) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getModificationNames()
        Returns only the names of the modifications stored in the set
        """
        ...
    
    def getFixedModificationNames(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getFixedModificationNames()
        Returns only the names of the fixed modifications
        """
        ...
    
    def getVariableModificationNames(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getVariableModificationNames()
        Returns only the names of the variable modifications
        """
        ...
    
    def isCompatible(self, peptide: AASequence ) -> bool:
        """
        Cython signature: bool isCompatible(AASequence & peptide)
        Returns true if the peptide is compatible with the definitions, e.g. does not contain other modifications
        """
        ...
    
    def inferFromPeptides(self, peptides: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void inferFromPeptides(libcpp_vector[PeptideIdentification] & peptides)
        Infers the sets of defined modifications from the modifications present on peptide identifications
        """
        ... 


class MultiplexDeltaMassesGenerator:
    """
    Cython implementation of _MultiplexDeltaMassesGenerator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MultiplexDeltaMassesGenerator.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MultiplexDeltaMassesGenerator()
        """
        ...
    
    @overload
    def __init__(self, in_0: MultiplexDeltaMassesGenerator ) -> None:
        """
        Cython signature: void MultiplexDeltaMassesGenerator(MultiplexDeltaMassesGenerator &)
        """
        ...
    
    @overload
    def __init__(self, labels: Union[bytes, str, String] , missed_cleavages: int , label_mass_shift: Dict[Union[bytes, str, String], float] ) -> None:
        """
        Cython signature: void MultiplexDeltaMassesGenerator(String labels, int missed_cleavages, libcpp_map[String,double] label_mass_shift)
        """
        ...
    
    def generateKnockoutDeltaMasses(self) -> None:
        """
        Cython signature: void generateKnockoutDeltaMasses()
        """
        ...
    
    def getDeltaMassesList(self) -> List[MultiplexDeltaMasses]:
        """
        Cython signature: libcpp_vector[MultiplexDeltaMasses] getDeltaMassesList()
        """
        ...
    
    def getLabelShort(self, label: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String getLabelShort(String label)
        """
        ...
    
    def getLabelLong(self, label: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String getLabelLong(String label)
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


class MultiplexDeltaMassesGenerator_Label:
    """
    Cython implementation of _MultiplexDeltaMassesGenerator_Label

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MultiplexDeltaMassesGenerator_Label.html>`_
    """
    
    short_name: Union[bytes, str, String]
    
    long_name: Union[bytes, str, String]
    
    description: Union[bytes, str, String]
    
    delta_mass: float
    
    def __init__(self, sn: Union[bytes, str, String] , ln: Union[bytes, str, String] , d: Union[bytes, str, String] , dm: float ) -> None:
        """
        Cython signature: void MultiplexDeltaMassesGenerator_Label(String sn, String ln, String d, double dm)
        """
        ... 


class MzDataFile:
    """
    Cython implementation of _MzDataFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzDataFile.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzDataFile()
        File adapter for MzData files
        """
        ...
    
    @overload
    def __init__(self, in_0: MzDataFile ) -> None:
        """
        Cython signature: void MzDataFile(MzDataFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , map: MSExperiment ) -> None:
        """
        Cython signature: void load(const String & filename, MSExperiment & map)
        Loads a map from a MzData file
        
        
        :param filename: Directory of the file with the file name
        :param map: It has to be a MSExperiment or have the same interface
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , map: MSExperiment ) -> None:
        """
        Cython signature: void store(const String & filename, MSExperiment & map)
        Stores a map in a MzData file
        
        
        :param filename: Directory of the file with the file name
        :param map: It has to be a MSExperiment or have the same interface
        :raises:
          Exception: UnableToCreateFile is thrown if the file could not be created
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        Returns the options for loading/storing
        """
        ...
    
    def setOptions(self, in_0: PeakFileOptions ) -> None:
        """
        Cython signature: void setOptions(PeakFileOptions)
        Sets options for loading/storing
        """
        ...
    
    def isSemanticallyValid(self, filename: Union[bytes, str, String] , errors: List[bytes] , warnings: List[bytes] ) -> bool:
        """
        Cython signature: bool isSemanticallyValid(const String & filename, StringList & errors, StringList & warnings)
        Checks if a file is valid with respect to the mapping file and the controlled vocabulary
        
        
        :param filename: File name of the file to be checked
        :param errors: Errors during the validation are returned in this output parameter
        :param warnings: Warnings during the validation are returned in this output parameter
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
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


class MzIdentMLFile:
    """
    Cython implementation of _MzIdentMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzIdentMLFile.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzIdentMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzIdentMLFile ) -> None:
        """
        Cython signature: void MzIdentMLFile(MzIdentMLFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , poid: List[ProteinIdentification] , peid: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void load(String filename, libcpp_vector[ProteinIdentification] & poid, libcpp_vector[PeptideIdentification] & peid)
        Loads the identifications from a MzIdentML file
        
        
        :param filename: File name of the file to be checked
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsin
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , poid: List[ProteinIdentification] , peid: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void store(String filename, libcpp_vector[ProteinIdentification] & poid, libcpp_vector[PeptideIdentification] & peid)
        Stores the identifications in a MzIdentML file
        
        
        :raises:
          Exception: UnableToCreateFile is thrown if the file could not be created
        """
        ...
    
    def isSemanticallyValid(self, filename: Union[bytes, str, String] , errors: List[bytes] , warnings: List[bytes] ) -> bool:
        """
        Cython signature: bool isSemanticallyValid(String filename, StringList errors, StringList warnings)
        Checks if a file is valid with respect to the mapping file and the controlled vocabulary
        
        
        :param filename: File name of the file to be checked
        :param errors: Errors during the validation are returned in this output parameter
        :param warnings: Warnings during the validation are returned in this output parameter
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
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


class MzMLSqliteHandler:
    """
    Cython implementation of _MzMLSqliteHandler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1MzMLSqliteHandler.html>`_
    """
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , run_id: int ) -> None:
        """
        Cython signature: void MzMLSqliteHandler(String filename, uint64_t run_id)
        """
        ...
    
    @overload
    def __init__(self, in_0: MzMLSqliteHandler ) -> None:
        """
        Cython signature: void MzMLSqliteHandler(MzMLSqliteHandler &)
        """
        ...
    
    def readExperiment(self, exp: MSExperiment , meta_only: bool ) -> None:
        """
        Cython signature: void readExperiment(MSExperiment & exp, bool meta_only)
        Read an experiment into an MSExperiment structure
        
        
        :param exp: The result data structure
        :param meta_only: Only read the meta data
        """
        ...
    
    def readSpectra(self, exp: List[MSSpectrum] , indices: List[int] , meta_only: bool ) -> None:
        """
        Cython signature: void readSpectra(libcpp_vector[MSSpectrum] & exp, libcpp_vector[int] indices, bool meta_only)
        Read a set of spectra (potentially restricted to a subset)
        
        
        :param exp: The result data structure
        :param indices: A list of indices restricting the resulting spectra only to those specified here
        :param meta_only: Only read the meta data
        """
        ...
    
    def readChromatograms(self, exp: List[MSChromatogram] , indices: List[int] , meta_only: bool ) -> None:
        """
        Cython signature: void readChromatograms(libcpp_vector[MSChromatogram] & exp, libcpp_vector[int] indices, bool meta_only)
        Read a set of chromatograms (potentially restricted to a subset)
        
        
        :param exp: The result data structure
        :param indices: A list of indices restricting the resulting spectra only to those specified here
        :param meta_only: Only read the meta data
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        Returns number of spectra in the file, reutrns the number of spectra
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        Returns the number of chromatograms in the file
        """
        ...
    
    def setConfig(self, write_full_meta: bool , use_lossy_compression: bool , linear_abs_mass_acc: float ) -> None:
        """
        Cython signature: void setConfig(bool write_full_meta, bool use_lossy_compression, double linear_abs_mass_acc)
        Sets file configuration
        
        
        :param write_full_meta: Whether to write a complete mzML meta data structure into the RUN_EXTRA field (allows complete recovery of the input file)
        :param use_lossy_compression: Whether to use lossy compression (ms numpress)
        :param linear_abs_mass_acc: Accepted loss in mass accuracy (absolute m/z, in Th)
        """
        ...
    
    def getSpectraIndicesbyRT(self, RT: float , deltaRT: float , indices: List[int] ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] getSpectraIndicesbyRT(double RT, double deltaRT, libcpp_vector[int] indices)
        Returns spectral indices around a specific retention time
        
        :param RT: The retention time
        :param deltaRT: Tolerance window around RT (if less or equal than zero, only the first spectrum *after* RT is returned)
        :param indices: Spectra to consider (if empty, all spectra are considered)
        :return: The indices of the spectra within RT +/- deltaRT
        """
        ...
    
    def writeExperiment(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void writeExperiment(MSExperiment exp)
        Write an MSExperiment to disk
        """
        ...
    
    def createTables(self) -> None:
        """
        Cython signature: void createTables()
        Create data tables for a new file
        """
        ...
    
    def writeSpectra(self, spectra: List[MSSpectrum] ) -> None:
        """
        Cython signature: void writeSpectra(libcpp_vector[MSSpectrum] spectra)
        Writes a set of spectra to disk
        """
        ...
    
    def writeChromatograms(self, chroms: List[MSChromatogram] ) -> None:
        """
        Cython signature: void writeChromatograms(libcpp_vector[MSChromatogram] chroms)
        Writes a set of chromatograms to disk
        """
        ...
    
    def writeRunLevelInformation(self, exp: MSExperiment , write_full_meta: bool ) -> None:
        """
        Cython signature: void writeRunLevelInformation(MSExperiment exp, bool write_full_meta)
        Write the run-level information for an experiment into tables
        
        This is a low level function, do not call this function unless you know what you are doing
        
        
        :param exp: The result data structure
        :param meta_only: Only read the meta data
        """
        ...
    
    def getRunID(self) -> int:
        """
        Cython signature: uint64_t getRunID()
        Extract the `RUN` ID from the sqMass file
        """
        ... 


class OSChromatogramMeta:
    """
    Cython implementation of _OSChromatogramMeta

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1OSChromatogramMeta.html>`_
    """
    
    index: int
    
    id: bytes
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OSChromatogramMeta()
        """
        ...
    
    @overload
    def __init__(self, in_0: OSChromatogramMeta ) -> None:
        """
        Cython signature: void OSChromatogramMeta(OSChromatogramMeta &)
        """
        ... 


class OSW_ChromExtractParams:
    """
    Cython implementation of _OSW_ChromExtractParams

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OSW_ChromExtractParams.html>`_
    """
    
    min_upper_edge_dist: float
    
    mz_extraction_window: float
    
    ppm: bool
    
    extraction_function: bytes
    
    rt_extraction_window: float
    
    extra_rt_extract: float
    
    im_extraction_window: float
    
    def __init__(self, in_0: OSW_ChromExtractParams ) -> None:
        """
        Cython signature: void OSW_ChromExtractParams(OSW_ChromExtractParams &)
        """
        ... 


class PScore:
    """
    Cython implementation of _PScore

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PScore.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PScore()
        """
        ...
    
    @overload
    def __init__(self, in_0: PScore ) -> None:
        """
        Cython signature: void PScore(PScore &)
        """
        ...
    
    def calculateIntensityRankInMZWindow(self, mz: List[float] , intensities: List[float] , mz_window: float ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] calculateIntensityRankInMZWindow(libcpp_vector[double] & mz, libcpp_vector[double] & intensities, double mz_window)
        Calculate local (windowed) peak ranks
        
        The peak rank is defined as the number of neighboring peaks in +/- (mz_window/2) that have higher intensity
        The result can be used to efficiently filter spectra for top 1..n peaks in mass windows
        
        
        :param mz: The m/z positions of the peaks
        :param intensities: The intensities of the peaks
        :param mz_window: The window in Thomson centered at each peak
        """
        ...
    
    def calculateRankMap(self, peak_map: MSExperiment , mz_window: float ) -> List[List[int]]:
        """
        Cython signature: libcpp_vector[libcpp_vector[size_t]] calculateRankMap(MSExperiment & peak_map, double mz_window)
        Precalculated, windowed peak ranks for a whole experiment
        
        The peak rank is defined as the number of neighboring peaks in +/- (mz_window/2) that have higher intensity
        
        
        :param peak_map: Fragment spectra used for rank calculation. Typically a peak map after removal of all MS1 spectra
        :param mz_window: Window in Thomson centered at each peak
        """
        ...
    
    def calculatePeakLevelSpectra(self, spec: MSSpectrum , ranks: List[int] , min_level: int , max_level: int ) -> Dict[int, MSSpectrum]:
        """
        Cython signature: libcpp_map[size_t,MSSpectrum] calculatePeakLevelSpectra(MSSpectrum & spec, libcpp_vector[size_t] & ranks, size_t min_level, size_t max_level)
        Calculates spectra for peak level between min_level to max_level and stores them in the map
        
        A spectrum of peak level n retains the (n+1) top intensity peaks in a sliding mz_window centered at each peak
        """
        ...
    
    @overload
    def computePScore(self, fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool , peak_level_spectra: Dict[int, MSSpectrum] , theo_spectra: List[MSSpectrum] , mz_window: float ) -> float:
        """
        Cython signature: double computePScore(double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm, libcpp_map[size_t,MSSpectrum] & peak_level_spectra, libcpp_vector[MSSpectrum] & theo_spectra, double mz_window)
        Computes the PScore for a vector of theoretical spectra
        
        Similar to Andromeda, a vector of theoretical spectra can be provided that e.g. contain loss spectra or higher charge spectra depending on the sequence.
        The best score obtained by scoring all those theoretical spectra against the experimental ones is returned
        
        
        :param fragment_mass_tolerance: Mass tolerance for matching peaks
        :param fragment_mass_tolerance_unit_ppm: Whether Thomson or ppm is used
        :param peak_level_spectra: Spectra for different peak levels (=filtered by maximum rank).
        :param theo_spectra: Theoretical spectra as obtained e.g. from TheoreticalSpectrumGenerator
        :param mz_window: Window in Thomson centered at each peak
        """
        ...
    
    @overload
    def computePScore(self, fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool , peak_level_spectra: Dict[int, MSSpectrum] , theo_spectrum: MSSpectrum , mz_window: float ) -> float:
        """
        Cython signature: double computePScore(double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm, libcpp_map[size_t,MSSpectrum] & peak_level_spectra, MSSpectrum & theo_spectrum, double mz_window)
        Computes the PScore for a single theoretical spectrum
        
        
        :param fragment_mass_tolerance: Mass tolerance for matching peaks
        :param fragment_mass_tolerance_unit_ppm: Whether Thomson or ppm is used
        :param peak_level_spectra: Spectra for different peak levels (=filtered by maximum rank)
        :param theo_spectra: Theoretical spectra as obtained e.g. from TheoreticalSpectrumGenerator
        :param mz_window: Window in Thomson centered at each peak
        """
        ... 


class PeakPickerChromatogram:
    """
    Cython implementation of _PeakPickerChromatogram

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeakPickerChromatogram.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeakPickerChromatogram()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeakPickerChromatogram ) -> None:
        """
        Cython signature: void PeakPickerChromatogram(PeakPickerChromatogram &)
        """
        ...
    
    def pickChromatogram(self, chromatogram: MSChromatogram , picked_chrom: MSChromatogram ) -> None:
        """
        Cython signature: void pickChromatogram(MSChromatogram & chromatogram, MSChromatogram & picked_chrom)
        Finds peaks in a single chromatogram and annotates left/right borders
        
        It uses a modified algorithm of the PeakPickerHiRes
        
        This function will return a picked chromatogram
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


class PeakPickerIterative:
    """
    Cython implementation of _PeakPickerIterative

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeakPickerIterative.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeakPickerIterative()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeakPickerIterative ) -> None:
        """
        Cython signature: void PeakPickerIterative(PeakPickerIterative &)
        """
        ...
    
    def pick(self, input: MSSpectrum , output: MSSpectrum ) -> None:
        """
        Cython signature: void pick(MSSpectrum & input, MSSpectrum & output)
        This will pick one single spectrum. The PeakPickerHiRes is used to
        generate seeds, these seeds are then used to re-center the mass and
        compute peak width and integrated intensity of the peak
        
        Finally, other peaks that would fall within the primary peak are
        discarded
        
        The output are the remaining peaks
        """
        ...
    
    def pickExperiment(self, input: MSExperiment , output: MSExperiment ) -> None:
        """
        Cython signature: void pickExperiment(MSExperiment & input, MSExperiment & output)
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


class PeakWidthEstimator:
    """
    Cython implementation of _PeakWidthEstimator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeakWidthEstimator.html>`_

    Rough estimation of the peak width at m/z
    
    Based on the peaks of the dataset (peak position & width) and the peak
    boundaries as reported by the PeakPickerHiRes, the typical peak width is
    estimated for arbitrary m/z using a spline interpolationThis struct can be used to store both peak or feature indices`
    """
    
    @overload
    def __init__(self, in_0: PeakWidthEstimator ) -> None:
        """
        Cython signature: void PeakWidthEstimator(PeakWidthEstimator &)
        """
        ...
    
    @overload
    def __init__(self, exp_picked: MSExperiment , boundaries: List[List[PeakBoundary]] ) -> None:
        """
        Cython signature: void PeakWidthEstimator(MSExperiment exp_picked, libcpp_vector[libcpp_vector[PeakBoundary]] & boundaries)
        """
        ...
    
    def getPeakWidth(self, mz: float ) -> float:
        """
        Cython signature: double getPeakWidth(double mz)
        Returns the estimated peak width at m/z
        """
        ... 


class PercolatorInfile:
    """
    Cython implementation of _PercolatorInfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PercolatorInfile.html>`_

    Class for storing Percolator tab-delimited input files
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PercolatorInfile()
        """
        ...
    
    @overload
    def __init__(self, in_0: PercolatorInfile ) -> None:
        """
        Cython signature: void PercolatorInfile(PercolatorInfile &)
        """
        ...
    
    store: __static_PercolatorInfile_store 


class QTCluster:
    """
    Cython implementation of _QTCluster

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1QTCluster.html>`_
    """
    
    def __init__(self, in_0: QTCluster ) -> None:
        """
        Cython signature: void QTCluster(QTCluster &)
        """
        ...
    
    def getCenterRT(self) -> float:
        """
        Cython signature: double getCenterRT()
        Returns the RT value of the cluster
        """
        ...
    
    def getCenterMZ(self) -> float:
        """
        Cython signature: double getCenterMZ()
        Returns the m/z value of the cluster center
        """
        ...
    
    def getXCoord(self) -> int:
        """
        Cython signature: int getXCoord()
        Returns the x coordinate in the grid
        """
        ...
    
    def getYCoord(self) -> int:
        """
        Cython signature: int getYCoord()
        Returns the y coordinate in the grid
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        Returns the size of the cluster (number of elements, incl. center)
        """
        ...
    
    def getQuality(self) -> float:
        """
        Cython signature: double getQuality()
        Returns the cluster quality and recomputes if necessary
        """
        ...
    
    def getAnnotations(self) -> Set[AASequence]:
        """
        Cython signature: libcpp_set[AASequence] getAnnotations()
        Returns the set of peptide sequences annotated to the cluster center
        """
        ...
    
    def setInvalid(self) -> None:
        """
        Cython signature: void setInvalid()
        Sets current cluster as invalid (also frees some memory)
        """
        ...
    
    def isInvalid(self) -> bool:
        """
        Cython signature: bool isInvalid()
        Whether current cluster is invalid
        """
        ...
    
    def initializeCluster(self) -> None:
        """
        Cython signature: void initializeCluster()
        Has to be called before adding elements (calling
        """
        ...
    
    def finalizeCluster(self) -> None:
        """
        Cython signature: void finalizeCluster()
        Has to be called after adding elements (after calling
        """
        ...
    
    def __richcmp__(self, other: QTCluster, op: int) -> Any:
        ... 


class QTClusterFinder:
    """
    Cython implementation of _QTClusterFinder

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1QTClusterFinder.html>`_
      -- Inherits from ['BaseGroupFinder']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void QTClusterFinder()
        """
        ...
    
    @overload
    def run(self, input_maps: List[ConsensusMap] , result_map: ConsensusMap ) -> None:
        """
        Cython signature: void run(libcpp_vector[ConsensusMap] & input_maps, ConsensusMap & result_map)
        """
        ...
    
    @overload
    def run(self, input_maps: List[FeatureMap] , result_map: ConsensusMap ) -> None:
        """
        Cython signature: void run(libcpp_vector[FeatureMap] & input_maps, ConsensusMap & result_map)
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


class RansacModelQuadratic:
    """
    Cython implementation of _RansacModelQuadratic

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1RansacModelQuadratic.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RansacModelQuadratic()
        """
        ...
    
    @overload
    def __init__(self, in_0: RansacModelQuadratic ) -> None:
        """
        Cython signature: void RansacModelQuadratic(RansacModelQuadratic &)
        """
        ... 


class ResidueDB:
    """
    Cython implementation of _ResidueDB

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ResidueDB.html>`_
    """
    
    def getNumberOfResidues(self) -> int:
        """
        Cython signature: size_t getNumberOfResidues()
        Returns the number of residues stored
        """
        ...
    
    def getNumberOfModifiedResidues(self) -> int:
        """
        Cython signature: size_t getNumberOfModifiedResidues()
        Returns the number of modified residues stored
        """
        ...
    
    def getResidue(self, name: Union[bytes, str, String] ) -> Residue:
        """
        Cython signature: const Residue * getResidue(const String & name)
        Returns a pointer to the residue with name, 3 letter code or 1 letter code name
        """
        ...
    
    @overload
    def getModifiedResidue(self, name: Union[bytes, str, String] ) -> Residue:
        """
        Cython signature: const Residue * getModifiedResidue(const String & name)
        Returns a pointer to a modified residue given a modification name
        """
        ...
    
    @overload
    def getModifiedResidue(self, residue: Residue , name: Union[bytes, str, String] ) -> Residue:
        """
        Cython signature: const Residue * getModifiedResidue(Residue * residue, const String & name)
        Returns a pointer to a modified residue given a residue and a modification name
        """
        ...
    
    def getResidues(self, residue_set: Union[bytes, str, String] ) -> Set[Residue]:
        """
        Cython signature: libcpp_set[const Residue *] getResidues(const String & residue_set)
        Returns a set of all residues stored in this residue db
        """
        ...
    
    def getResidueSets(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getResidueSets()
        Returns all residue sets that are registered which this instance
        """
        ...
    
    def hasResidue(self, name: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasResidue(const String & name)
        Returns true if the db contains a residue with the given name
        """
        ... 


class RibonucleotideDB:
    """
    Cython implementation of _RibonucleotideDB

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1RibonucleotideDB.html>`_
    """
    
    def getRibonucleotide(self, code: bytes ) -> Ribonucleotide:
        """
        Cython signature: const Ribonucleotide * getRibonucleotide(const libcpp_string & code)
        """
        ...
    
    def getRibonucleotidePrefix(self, code: bytes ) -> Ribonucleotide:
        """
        Cython signature: const Ribonucleotide * getRibonucleotidePrefix(const libcpp_string & code)
        """
        ... 


class SavitzkyGolayFilter:
    """
    Cython implementation of _SavitzkyGolayFilter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SavitzkyGolayFilter.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SavitzkyGolayFilter()
        """
        ...
    
    @overload
    def __init__(self, in_0: SavitzkyGolayFilter ) -> None:
        """
        Cython signature: void SavitzkyGolayFilter(SavitzkyGolayFilter &)
        """
        ...
    
    def filter(self, spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void filter(MSSpectrum & spectrum)
        Removed the noise from an MSSpectrum containing profile data
        """
        ...
    
    def filterExperiment(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void filterExperiment(MSExperiment & exp)
        Removed the noise from an MSExperiment containing profile data
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


class SequestInfile:
    """
    Cython implementation of _SequestInfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SequestInfile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SequestInfile()
        Sequest input file adapter
        """
        ...
    
    @overload
    def __init__(self, in_0: SequestInfile ) -> None:
        """
        Cython signature: void SequestInfile(SequestInfile &)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(const String & filename)
        Stores the experiment data in a Sequest input file that can be used as input for Sequest shell execution
        
        :param filename: the name of the file in which the infile is stored into
        """
        ...
    
    def getEnzymeInfoAsString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getEnzymeInfoAsString()
        Returns the enzyme list as a string
        """
        ...
    
    def getDatabase(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getDatabase()
        Returns the used database
        """
        ...
    
    def setDatabase(self, database: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDatabase(const String & database)
        Sets the used database
        """
        ...
    
    def getNeutralLossesForIons(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNeutralLossesForIons()
        Returns whether neutral losses are considered for the a-, b- and y-ions
        """
        ...
    
    def setNeutralLossesForIons(self, neutral_losses_for_ions: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNeutralLossesForIons(const String & neutral_losses_for_ions)
        Sets whether neutral losses are considered for the a-, b- and y-ions
        """
        ...
    
    def getIonSeriesWeights(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIonSeriesWeights()
        Returns the weights for the a-, b-, c-, d-, v-, w-, x-, y- and z-ion series
        """
        ...
    
    def setIonSeriesWeights(self, ion_series_weights: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIonSeriesWeights(const String & ion_series_weights)
        Sets the weights for the a-, b-, c-, d-, v-, w-, x-, y- and z-ion series
        """
        ...
    
    def getPartialSequence(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getPartialSequence()
        Returns the partial sequences (space delimited) that have to occur in the theoretical spectra
        """
        ...
    
    def setPartialSequence(self, partial_sequence: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setPartialSequence(const String & partial_sequence)
        Sets the partial sequences (space delimited) that have to occur in the theoretical spectra
        """
        ...
    
    def getSequenceHeaderFilter(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSequenceHeaderFilter()
        Returns the sequences (space delimited) that have to occur, or be absent (preceded by a tilde) in the header of a protein to be considered
        """
        ...
    
    def setSequenceHeaderFilter(self, sequence_header_filter: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSequenceHeaderFilter(const String & sequence_header_filter)
        Sets the sequences (space delimited) that have to occur, or be absent (preceded by a tilde) in the header of a protein to be considered
        """
        ...
    
    def getProteinMassFilter(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getProteinMassFilter()
        Returns the protein mass filter (either min and max mass, or mass and tolerance value in percent)
        """
        ...
    
    def setProteinMassFilter(self, protein_mass_filter: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setProteinMassFilter(const String & protein_mass_filter)
        Sets the protein mass filter (either min and max mass, or mass and tolerance value in percent)
        """
        ...
    
    def getPeakMassTolerance(self) -> float:
        """
        Cython signature: float getPeakMassTolerance()
        Returns the peak mass tolerance
        """
        ...
    
    def setPeakMassTolerance(self, peak_mass_tolerance: float ) -> None:
        """
        Cython signature: void setPeakMassTolerance(float peak_mass_tolerance)
        Sets the peak mass tolerance
        """
        ...
    
    def getPrecursorMassTolerance(self) -> float:
        """
        Cython signature: float getPrecursorMassTolerance()
        Returns the precursor mass tolerance
        """
        ...
    
    def setPrecursorMassTolerance(self, precursor_mass_tolerance: float ) -> None:
        """
        Cython signature: void setPrecursorMassTolerance(float precursor_mass_tolerance)
        Sets the precursor mass tolerance
        """
        ...
    
    def getMatchPeakTolerance(self) -> float:
        """
        Cython signature: float getMatchPeakTolerance()
        Returns the match peak tolerance
        """
        ...
    
    def setMatchPeakTolerance(self, match_peak_tolerance: float ) -> None:
        """
        Cython signature: void setMatchPeakTolerance(float match_peak_tolerance)
        Sets the match peak tolerance
        """
        ...
    
    def getIonCutoffPercentage(self) -> float:
        """
        Cython signature: float getIonCutoffPercentage()
        Returns the the cutoff of the ratio matching theoretical peaks/theoretical peaks
        """
        ...
    
    def setIonCutoffPercentage(self, ion_cutoff_percentage: float ) -> None:
        """
        Cython signature: void setIonCutoffPercentage(float ion_cutoff_percentage)
        Sets the ion cutoff of the ratio matching theoretical peaks/theoretical peaks
        """
        ...
    
    def getPeptideMassUnit(self) -> int:
        """
        Cython signature: size_t getPeptideMassUnit()
        Returns the peptide mass unit
        """
        ...
    
    def setPeptideMassUnit(self, peptide_mass_unit: int ) -> None:
        """
        Cython signature: void setPeptideMassUnit(size_t peptide_mass_unit)
        Sets the peptide mass unit
        """
        ...
    
    def getOutputLines(self) -> int:
        """
        Cython signature: size_t getOutputLines()
        Returns the number of peptides to be displayed
        """
        ...
    
    def setOutputLines(self, output_lines: int ) -> None:
        """
        Cython signature: void setOutputLines(size_t output_lines)
        Sets the number of peptides to be displayed
        """
        ...
    
    def getEnzymeNumber(self) -> int:
        """
        Cython signature: size_t getEnzymeNumber()
        Returns the enzyme used for cleavage (by means of the number from a list of enzymes)
        """
        ...
    
    def getEnzymeName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getEnzymeName()
        Returns the enzyme used for cleavage
        """
        ...
    
    def setEnzyme(self, enzyme_name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t setEnzyme(String enzyme_name)
        Sets the enzyme used for cleavage (by means of the number from a list of enzymes)
        """
        ...
    
    def getMaxAAPerModPerPeptide(self) -> int:
        """
        Cython signature: size_t getMaxAAPerModPerPeptide()
        Returns the maximum number of amino acids containing the same modification in a peptide
        """
        ...
    
    def setMaxAAPerModPerPeptide(self, max_aa_per_mod_per_peptide: int ) -> None:
        """
        Cython signature: void setMaxAAPerModPerPeptide(size_t max_aa_per_mod_per_peptide)
        Sets the maximum number of amino acids containing the same modification in a peptide
        """
        ...
    
    def getMaxModsPerPeptide(self) -> int:
        """
        Cython signature: size_t getMaxModsPerPeptide()
        Returns the maximum number of modifications that are allowed in a peptide
        """
        ...
    
    def setMaxModsPerPeptide(self, max_mods_per_peptide: int ) -> None:
        """
        Cython signature: void setMaxModsPerPeptide(size_t max_mods_per_peptide)
        Sets the maximum number of modifications that are allowed in a peptide
        """
        ...
    
    def getNucleotideReadingFrame(self) -> int:
        """
        Cython signature: size_t getNucleotideReadingFrame()
        Returns the nucleotide reading frame
        """
        ...
    
    def setNucleotideReadingFrame(self, nucleotide_reading_frame: int ) -> None:
        """
        Cython signature: void setNucleotideReadingFrame(size_t nucleotide_reading_frame)
        Sets the nucleotide reading frame
        """
        ...
    
    def getMaxInternalCleavageSites(self) -> int:
        """
        Cython signature: size_t getMaxInternalCleavageSites()
        Returns the maximum number of internal cleavage sites
        """
        ...
    
    def setMaxInternalCleavageSites(self, max_internal_cleavage_sites: int ) -> None:
        """
        Cython signature: void setMaxInternalCleavageSites(size_t max_internal_cleavage_sites)
        Sets the maximum number of internal cleavage sites
        """
        ...
    
    def getMatchPeakCount(self) -> int:
        """
        Cython signature: size_t getMatchPeakCount()
        Returns the number of top abundant peaks to match with theoretical ones
        """
        ...
    
    def setMatchPeakCount(self, match_peak_count: int ) -> None:
        """
        Cython signature: void setMatchPeakCount(size_t match_peak_count)
        Sets the number of top abundant peaks to with theoretical ones
        """
        ...
    
    def getMatchPeakAllowedError(self) -> int:
        """
        Cython signature: size_t getMatchPeakAllowedError()
        Returns the number of top abundant peaks that are allowed not to match with a theoretical peak
        """
        ...
    
    def setMatchPeakAllowedError(self, match_peak_allowed_error: int ) -> None:
        """
        Cython signature: void setMatchPeakAllowedError(size_t match_peak_allowed_error)
        Sets the number of top abundant peaks that are allowed not to match with a theoretical peak
        """
        ...
    
    def getShowFragmentIons(self) -> bool:
        """
        Cython signature: bool getShowFragmentIons()
        Returns whether fragment ions shall be displayed
        """
        ...
    
    def setShowFragmentIons(self, show_fragments: bool ) -> None:
        """
        Cython signature: void setShowFragmentIons(bool show_fragments)
        Sets whether fragment ions shall be displayed
        """
        ...
    
    def getPrintDuplicateReferences(self) -> bool:
        """
        Cython signature: bool getPrintDuplicateReferences()
        Returns whether all proteins containing a found peptide should be displayed
        """
        ...
    
    def setPrintDuplicateReferences(self, print_duplicate_references: bool ) -> None:
        """
        Cython signature: void setPrintDuplicateReferences(bool print_duplicate_references)
        Sets whether all proteins containing a found peptide should be displayed
        """
        ...
    
    def getRemovePrecursorNearPeaks(self) -> bool:
        """
        Cython signature: bool getRemovePrecursorNearPeaks()
        Returns whether peaks near (15 amu) the precursor peak are removed
        """
        ...
    
    def setRemovePrecursorNearPeaks(self, remove_precursor_near_peaks: bool ) -> None:
        """
        Cython signature: void setRemovePrecursorNearPeaks(bool remove_precursor_near_peaks)
        Sets whether peaks near (15 amu) the precursor peak are removed
        """
        ...
    
    def getMassTypeParent(self) -> bool:
        """
        Cython signature: bool getMassTypeParent()
        Returns the mass type of the parent (0 - monoisotopic, 1 - average mass)
        """
        ...
    
    def setMassTypeParent(self, mass_type_parent: bool ) -> None:
        """
        Cython signature: void setMassTypeParent(bool mass_type_parent)
        Sets the mass type of the parent (0 - monoisotopic, 1 - average mass)
        """
        ...
    
    def getMassTypeFragment(self) -> bool:
        """
        Cython signature: bool getMassTypeFragment()
        Returns the mass type of the fragments (0 - monoisotopic, 1 - average mass)
        """
        ...
    
    def setMassTypeFragment(self, mass_type_fragment: bool ) -> None:
        """
        Cython signature: void setMassTypeFragment(bool mass_type_fragment)
        Sets the mass type of the fragments (0 - monoisotopic, 1 - average mass)
        """
        ...
    
    def getNormalizeXcorr(self) -> bool:
        """
        Cython signature: bool getNormalizeXcorr()
        Returns whether normalized xcorr values are displayed
        """
        ...
    
    def setNormalizeXcorr(self, normalize_xcorr: bool ) -> None:
        """
        Cython signature: void setNormalizeXcorr(bool normalize_xcorr)
        Sets whether normalized xcorr values are displayed
        """
        ...
    
    def getResiduesInUpperCase(self) -> bool:
        """
        Cython signature: bool getResiduesInUpperCase()
        Returns whether residues are in upper case
        """
        ...
    
    def setResiduesInUpperCase(self, residues_in_upper_case: bool ) -> None:
        """
        Cython signature: void setResiduesInUpperCase(bool residues_in_upper_case)
        Sets whether residues are in upper case
        """
        ...
    
    def addEnzymeInfo(self, enzyme_info: List[bytes] ) -> None:
        """
        Cython signature: void addEnzymeInfo(libcpp_vector[String] & enzyme_info)
        Adds an enzyme to the list and sets is as used
        """
        ...
    
    def handlePTMs(self, modification_line: Union[bytes, str, String] , modifications_filename: Union[bytes, str, String] , monoisotopic: bool ) -> None:
        """
        Cython signature: void handlePTMs(const String & modification_line, const String & modifications_filename, bool monoisotopic)
        """
        ...
    
    def __richcmp__(self, other: SequestInfile, op: int) -> Any:
        ... 


class StringDataArray:
    """
    Cython implementation of _StringDataArray

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::DataArrays_1_1StringDataArray.html>`_
      -- Inherits from ['MetaInfoDescription']

    The representation of extra string data attached to a spectrum or chromatogram.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void StringDataArray()
        """
        ...
    
    @overload
    def __init__(self, in_0: StringDataArray ) -> None:
        """
        Cython signature: void StringDataArray(StringDataArray &)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def resize(self, n: int ) -> None:
        """
        Cython signature: void resize(size_t n)
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def push_back(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void push_back(String)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the peak annotations
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the peak annotations
        """
        ...
    
    def getDataProcessing(self) -> List[DataProcessing]:
        """
        Cython signature: libcpp_vector[shared_ptr[DataProcessing]] getDataProcessing()
        Returns a reference to the description of the applied processing
        """
        ...
    
    def setDataProcessing(self, in_0: List[DataProcessing] ) -> None:
        """
        Cython signature: void setDataProcessing(libcpp_vector[shared_ptr[DataProcessing]])
        Sets the description of the applied processing
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
    
    def __richcmp__(self, other: StringDataArray, op: int) -> Any:
        ... 


class StringView:
    """
    Cython implementation of _StringView

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1StringView.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void StringView()
        """
        ...
    
    @overload
    def __init__(self, in_0: bytes ) -> None:
        """
        Cython signature: void StringView(const libcpp_string &)
        """
        ...
    
    @overload
    def __init__(self, in_0: StringView ) -> None:
        """
        Cython signature: void StringView(StringView &)
        """
        ...
    
    def substr(self, start: int , end: int ) -> StringView:
        """
        Cython signature: StringView substr(size_t start, size_t end)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def getString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getString()
        """
        ...
    
    def __richcmp__(self, other: StringView, op: int) -> Any:
        ... 


class TheoreticalSpectrumGeneratorXLMS:
    """
    Cython implementation of _TheoreticalSpectrumGeneratorXLMS

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TheoreticalSpectrumGeneratorXLMS.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TheoreticalSpectrumGeneratorXLMS()
        """
        ...
    
    @overload
    def __init__(self, in_0: TheoreticalSpectrumGeneratorXLMS ) -> None:
        """
        Cython signature: void TheoreticalSpectrumGeneratorXLMS(TheoreticalSpectrumGeneratorXLMS &)
        """
        ...
    
    def getLinearIonSpectrum(self, spectrum: MSSpectrum , peptide: AASequence , link_pos: int , frag_alpha: bool , charge: int , link_pos_2: int ) -> None:
        """
        Cython signature: void getLinearIonSpectrum(MSSpectrum & spectrum, AASequence peptide, size_t link_pos, bool frag_alpha, int charge, size_t link_pos_2)
            Generates fragment ions not containing the cross-linker for one peptide
        
            B-ions are generated from the beginning of the peptide up to the first linked position,
            y-ions are generated from the second linked position up the end of the peptide.
            If link_pos_2 is 0, a mono-link or cross-link is assumed and the second position is the same as the first position.
            For a loop-link two different positions can be set and link_pos_2 must be larger than link_pos
            The generated ion types and other additional settings are determined by the tool parameters
        
            :param spectrum: The spectrum to which the new peaks are added. Does not have to be empty, the generated peaks will be pushed onto it
            :param peptide: The peptide to fragment
            :param link_pos: The position of the cross-linker on the given peptide
            :param frag_alpha: True, if the fragmented peptide is the Alpha peptide. Used for ion-name annotation
            :param charge: The maximal charge of the ions
            :param link_pos_2: A second position for the linker, in case it is a loop link
        """
        ...
    
    @overload
    def getXLinkIonSpectrum(self, spectrum: MSSpectrum , peptide: AASequence , link_pos: int , precursor_mass: float , frag_alpha: bool , mincharge: int , maxcharge: int , link_pos_2: int ) -> None:
        """
        Cython signature: void getXLinkIonSpectrum(MSSpectrum & spectrum, AASequence peptide, size_t link_pos, double precursor_mass, bool frag_alpha, int mincharge, int maxcharge, size_t link_pos_2)
            Generates fragment ions containing the cross-linker for one peptide
        
            B-ions are generated from the first linked position up to the end of the peptide,
            y-ions are generated from the beginning of the peptide up to the second linked position.
            If link_pos_2 is 0, a mono-link or cross-link is assumed and the second position is the same as the first position.
            For a loop-link two different positions can be set and link_pos_2 must be larger than link_pos.
            Since in the case of a cross-link a whole second peptide is attached to the other side of the cross-link,
            a precursor mass for the two peptides and the linker is needed.
            In the case of a loop link the precursor mass is the mass of the only peptide and the linker.
            Although this function is more general, currently it is mainly used for loop-links and mono-links,
            because residues in the second, unknown peptide cannot be considered for possible neutral losses.
            The generated ion types and other additional settings are determined by the tool parameters
        
            :param spectrum: The spectrum to which the new peaks are added. Does not have to be empty, the generated peaks will be pushed onto it
            :param peptide: The peptide to fragment
            :param link_pos: The position of the cross-linker on the given peptide
            :param precursor_mass: The mass of the whole cross-link candidate or the precursor mass of the experimental MS2 spectrum.
            :param frag_alpha: True, if the fragmented peptide is the Alpha peptide. Used for ion-name annotation.
            :param mincharge: The minimal charge of the ions
            :param maxcharge: The maximal charge of the ions, it should be the precursor charge and is used to generate precursor ion peaks
            :param link_pos_2: A second position for the linker, in case it is a loop link
        """
        ...
    
    @overload
    def getXLinkIonSpectrum(self, spectrum: MSSpectrum , crosslink: ProteinProteinCrossLink , frag_alpha: bool , mincharge: int , maxcharge: int ) -> None:
        """
        Cython signature: void getXLinkIonSpectrum(MSSpectrum & spectrum, ProteinProteinCrossLink crosslink, bool frag_alpha, int mincharge, int maxcharge)
            Generates fragment ions containing the cross-linker for a pair of peptides
        
            B-ions are generated from the first linked position up to the end of the peptide,
            y-ions are generated from the beginning of the peptide up to the second linked position.
            This function generates neutral loss ions by considering both linked peptides.
            Only one of the peptides, decided by @frag_alpha, is fragmented.
            This function is not suitable to generate fragments for mono-links or loop-links.
            This simplifies the function, but it has to be called twice to get all fragments of a peptide pair.
            The generated ion types and other additional settings are determined by the tool parameters
        
            :param spectrum: The spectrum to which the new peaks are added. Does not have to be empty, the generated peaks will be pushed onto it
            :param crosslink: ProteinProteinCrossLink to be fragmented
            :param link_pos: The position of the cross-linker on the given peptide
            :param precursor_mass: The mass of the whole cross-link candidate or the precursor mass of the experimental MS2 spectrum
            :param frag_alpha: True, if the fragmented peptide is the Alpha peptide
            :param mincharge: The minimal charge of the ions
            :param maxcharge: The maximal charge of the ions, it should be the precursor charge and is used to generate precursor ion peaks
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


class ThresholdMower:
    """
    Cython implementation of _ThresholdMower

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ThresholdMower.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ThresholdMower()
        """
        ...
    
    @overload
    def __init__(self, in_0: ThresholdMower ) -> None:
        """
        Cython signature: void ThresholdMower(ThresholdMower &)
        """
        ...
    
    def filterSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterSpectrum(MSSpectrum & spec)
        """
        ...
    
    def filterPeakSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrum(MSSpectrum & spec)
        """
        ...
    
    def filterPeakMap(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void filterPeakMap(MSExperiment & exp)
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


class TransformationDescription:
    """
    Cython implementation of _TransformationDescription

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::TransformationDescription_1_1TransformationDescription.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TransformationDescription()
        """
        ...
    
    @overload
    def __init__(self, in_0: TransformationDescription ) -> None:
        """
        Cython signature: void TransformationDescription(TransformationDescription &)
        """
        ...
    
    def getDataPoints(self) -> List[TM_DataPoint]:
        """
        Cython signature: libcpp_vector[TM_DataPoint] getDataPoints()
        Returns the data points
        """
        ...
    
    @overload
    def setDataPoints(self, data: List[TM_DataPoint] ) -> None:
        """
        Cython signature: void setDataPoints(libcpp_vector[TM_DataPoint] & data)
        Sets the data points. Removes the model that was previously fitted to the data (if any)
        """
        ...
    
    @overload
    def setDataPoints(self, data: List[List[float, float]] ) -> None:
        """
        Cython signature: void setDataPoints(libcpp_vector[libcpp_pair[double,double]] & data)
        Sets the data points (backwards-compatible overload). Removes the model that was previously fitted to the data (if any)
        """
        ...
    
    def apply(self, in_0: float ) -> float:
        """
        Cython signature: double apply(double)
        Applies the transformation to `value`
        """
        ...
    
    @overload
    def fitModel(self, model_type: Union[bytes, str, String] , params: Param ) -> None:
        """
        Cython signature: void fitModel(String model_type, Param params)
        Fits a model to the data
        """
        ...
    
    @overload
    def fitModel(self, model_type: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void fitModel(String model_type)
        Fits a model to the data
        """
        ...
    
    def getModelType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getModelType()
        Gets the type of the fitted model
        """
        ...
    
    def getModelParameters(self) -> Param:
        """
        Cython signature: Param getModelParameters()
        Returns the model parameters
        """
        ...
    
    def invert(self) -> None:
        """
        Cython signature: void invert()
        Computes an (approximate) inverse of the transformation
        """
        ...
    
    def getDeviations(self, diffs: List[float] , do_apply: bool , do_sort: bool ) -> None:
        """
        Cython signature: void getDeviations(libcpp_vector[double] & diffs, bool do_apply, bool do_sort)
        Get the deviations between the data pairs
        
        :param diffs: Output
        :param do_apply: Get deviations after applying the model?
        :param do_sort: Sort `diffs` before returning?
        """
        ...
    
    def getStatistics(self) -> TransformationStatistics:
        """
        Cython signature: TransformationStatistics getStatistics()
        """
        ...
    
    getModelTypes: __static_TransformationDescription_getModelTypes 


class TransformationStatistics:
    """
    Cython implementation of _TransformationStatistics

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::TransformationDescription_1_1TransformationStatistics.html>`_
    """
    
    xmin: float
    
    xmax: float
    
    ymin: float
    
    ymax: float
    
    percentiles_before: Dict[int, float]
    
    percentiles_after: Dict[int, float]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TransformationStatistics()
        """
        ...
    
    @overload
    def __init__(self, in_0: TransformationStatistics ) -> None:
        """
        Cython signature: void TransformationStatistics(TransformationStatistics &)
        """
        ... 


class XMLHandler:
    """
    Cython implementation of _XMLHandler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1XMLHandler.html>`_
    """
    
    def __init__(self, filename: Union[bytes, str, String] , version: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void XMLHandler(const String & filename, const String & version)
        """
        ...
    
    def reset(self) -> None:
        """
        Cython signature: void reset()
        """
        ...
    
    def error(self, mode: int , msg: Union[bytes, str, String] , line: int , column: int ) -> None:
        """
        Cython signature: void error(ActionMode mode, const String & msg, unsigned int line, unsigned int column)
        """
        ...
    
    def warning(self, mode: int , msg: Union[bytes, str, String] , line: int , column: int ) -> None:
        """
        Cython signature: void warning(ActionMode mode, const String & msg, unsigned int line, unsigned int column)
        """
        ...
    ActionMode : __ActionMode 


class __ActionMode:
    None
    LOAD : int
    STORE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class BoundaryCondition:
    None
    BC_ZERO_ENDPOINTS : int
    BC_ZERO_FIRST : int
    BC_ZERO_SECOND : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __ChromatogramType:
    None
    MASS_CHROMATOGRAM : int
    TOTAL_ION_CURRENT_CHROMATOGRAM : int
    SELECTED_ION_CURRENT_CHROMATOGRAM : int
    BASEPEAK_CHROMATOGRAM : int
    SELECTED_ION_MONITORING_CHROMATOGRAM : int
    SELECTED_REACTION_MONITORING_CHROMATOGRAM : int
    ELECTROMAGNETIC_RADIATION_CHROMATOGRAM : int
    ABSORPTION_CHROMATOGRAM : int
    EMISSION_CHROMATOGRAM : int
    SIZE_OF_CHROMATOGRAM_TYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class NormalizationMethod:
    None
    NM_SCALE : int
    NM_SHIFT : int

    def getMapping(self) -> Dict[int, str]:
       ... 

