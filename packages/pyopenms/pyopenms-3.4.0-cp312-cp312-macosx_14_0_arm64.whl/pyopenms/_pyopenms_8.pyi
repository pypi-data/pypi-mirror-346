from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_OpenMSOSInfo_getBinaryArchitecture() -> Union[bytes, str, String]:
    """
    Cython signature: String getBinaryArchitecture()
    """
    ...

def __static_OpenMSBuildInfo_getBuildType() -> Union[bytes, str, String]:
    """
    Cython signature: String getBuildType()
    """
    ...

def __static_TransformationDescription_getModelTypes(result: List[bytes] ) -> None:
    """
    Cython signature: void getModelTypes(StringList result)
    """
    ...

def __static_OpenMSOSInfo_getOSInfo() -> OpenMSOSInfo:
    """
    Cython signature: OpenMSOSInfo getOSInfo()
    """
    ...

def __static_OpenMSBuildInfo_getOpenMPMaxNumThreads() -> int:
    """
    Cython signature: size_t getOpenMPMaxNumThreads()
    """
    ...

def __static_OpenMSBuildInfo_isOpenMPEnabled() -> bool:
    """
    Cython signature: bool isOpenMPEnabled()
    """
    ...

def __static_CachedmzML_load(filename: Union[bytes, str, String] , exp: CachedmzML ) -> None:
    """
    Cython signature: void load(const String & filename, CachedmzML & exp)
    """
    ...

def __static_ChromatogramExtractor_prepare_coordinates(output_chromatograms: List[OSChromatogram] , extraction_coordinates: List[ExtractionCoordinates] , targeted: TargetedExperiment , rt_extraction_window: float , ms1: bool , ms1_isotopes: int ) -> None:
    """
    Cython signature: void prepare_coordinates(libcpp_vector[shared_ptr[OSChromatogram]] & output_chromatograms, libcpp_vector[ExtractionCoordinates] & extraction_coordinates, TargetedExperiment & targeted, double rt_extraction_window, bool ms1, int ms1_isotopes)
    """
    ...

def __static_OpenMSBuildInfo_setOpenMPNumThreads(num_threads: int ) -> None:
    """
    Cython signature: void setOpenMPNumThreads(int num_threads)
    """
    ...

def __static_CachedmzML_store(filename: Union[bytes, str, String] , exp: MSExperiment ) -> None:
    """
    Cython signature: void store(const String & filename, MSExperiment exp)
    """
    ...


class AQS_featureConcentration:
    """
    Cython implementation of _AQS_featureConcentration

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AQS_featureConcentration.html>`_
    """
    
    feature: Feature
    
    IS_feature: Feature
    
    actual_concentration: float
    
    IS_actual_concentration: float
    
    concentration_units: Union[bytes, str, String]
    
    dilution_factor: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AQS_featureConcentration()
        """
        ...
    
    @overload
    def __init__(self, in_0: AQS_featureConcentration ) -> None:
        """
        Cython signature: void AQS_featureConcentration(AQS_featureConcentration &)
        """
        ... 


class AQS_runConcentration:
    """
    Cython implementation of _AQS_runConcentration

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AQS_runConcentration.html>`_
    """
    
    sample_name: Union[bytes, str, String]
    
    component_name: Union[bytes, str, String]
    
    IS_component_name: Union[bytes, str, String]
    
    actual_concentration: float
    
    IS_actual_concentration: float
    
    concentration_units: Union[bytes, str, String]
    
    dilution_factor: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AQS_runConcentration()
        """
        ...
    
    @overload
    def __init__(self, in_0: AQS_runConcentration ) -> None:
        """
        Cython signature: void AQS_runConcentration(AQS_runConcentration &)
        """
        ... 


class AbsoluteQuantitationStandards:
    """
    Cython implementation of _AbsoluteQuantitationStandards

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AbsoluteQuantitationStandards.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AbsoluteQuantitationStandards()
        """
        ...
    
    @overload
    def __init__(self, in_0: AbsoluteQuantitationStandards ) -> None:
        """
        Cython signature: void AbsoluteQuantitationStandards(AbsoluteQuantitationStandards &)
        """
        ...
    
    def getComponentFeatureConcentrations(self, run_concentrations: List[AQS_runConcentration] , feature_maps: List[FeatureMap] , component_name: Union[bytes, str, String] , feature_concentrations: List[AQS_featureConcentration] ) -> None:
        """
        Cython signature: void getComponentFeatureConcentrations(libcpp_vector[AQS_runConcentration] & run_concentrations, libcpp_vector[FeatureMap] & feature_maps, const String & component_name, libcpp_vector[AQS_featureConcentration] & feature_concentrations)
        """
        ... 


class AbsoluteQuantitationStandardsFile:
    """
    Cython implementation of _AbsoluteQuantitationStandardsFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AbsoluteQuantitationStandardsFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AbsoluteQuantitationStandardsFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: AbsoluteQuantitationStandardsFile ) -> None:
        """
        Cython signature: void AbsoluteQuantitationStandardsFile(AbsoluteQuantitationStandardsFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , run_concentrations: List[AQS_runConcentration] ) -> None:
        """
        Cython signature: void load(const String & filename, libcpp_vector[AQS_runConcentration] & run_concentrations)
        """
        ... 


class AnnotationStatistics:
    """
    Cython implementation of _AnnotationStatistics

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AnnotationStatistics.html>`_
    """
    
    states: List[int]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AnnotationStatistics()
        """
        ...
    
    @overload
    def __init__(self, in_0: AnnotationStatistics ) -> None:
        """
        Cython signature: void AnnotationStatistics(AnnotationStatistics &)
        """
        ...
    
    def __richcmp__(self, other: AnnotationStatistics, op: int) -> Any:
        ... 


class Attachment:
    """
    Cython implementation of _Attachment

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::QcMLFile_1_1Attachment.html>`_
    """
    
    name: Union[bytes, str, String]
    
    id: Union[bytes, str, String]
    
    value: Union[bytes, str, String]
    
    cvRef: Union[bytes, str, String]
    
    cvAcc: Union[bytes, str, String]
    
    unitRef: Union[bytes, str, String]
    
    unitAcc: Union[bytes, str, String]
    
    binary: Union[bytes, str, String]
    
    qualityRef: Union[bytes, str, String]
    
    colTypes: List[bytes]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Attachment()
        """
        ...
    
    @overload
    def __init__(self, in_0: Attachment ) -> None:
        """
        Cython signature: void Attachment(Attachment &)
        """
        ...
    
    def toXMLString(self, indentation_level: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String toXMLString(unsigned int indentation_level)
        """
        ...
    
    def toCSVString(self, separator: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String toCSVString(String separator)
        """
        ...
    
    def __richcmp__(self, other: Attachment, op: int) -> Any:
        ... 


class CVMappingTerm:
    """
    Cython implementation of _CVMappingTerm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVMappingTerm.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVMappingTerm()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVMappingTerm ) -> None:
        """
        Cython signature: void CVMappingTerm(CVMappingTerm &)
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
    
    def setUseTermName(self, use_term_name: bool ) -> None:
        """
        Cython signature: void setUseTermName(bool use_term_name)
        Sets whether the term name should be used, instead of the accession
        """
        ...
    
    def getUseTermName(self) -> bool:
        """
        Cython signature: bool getUseTermName()
        Returns whether the term name should be used, instead of the accession
        """
        ...
    
    def setUseTerm(self, use_term: bool ) -> None:
        """
        Cython signature: void setUseTerm(bool use_term)
        Sets whether the term itself can be used (or only its children)
        """
        ...
    
    def getUseTerm(self) -> bool:
        """
        Cython signature: bool getUseTerm()
        Returns true if the term can be used, false if only children are allowed
        """
        ...
    
    def setTermName(self, term_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTermName(String term_name)
        Sets the name of the term
        """
        ...
    
    def getTermName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTermName()
        Returns the name of the term
        """
        ...
    
    def setIsRepeatable(self, is_repeatable: bool ) -> None:
        """
        Cython signature: void setIsRepeatable(bool is_repeatable)
        Sets whether this term can be repeated
        """
        ...
    
    def getIsRepeatable(self) -> bool:
        """
        Cython signature: bool getIsRepeatable()
        Returns true if this term can be repeated, false otherwise
        """
        ...
    
    def setAllowChildren(self, allow_children: bool ) -> None:
        """
        Cython signature: void setAllowChildren(bool allow_children)
        Sets whether children of this term are allowed
        """
        ...
    
    def getAllowChildren(self) -> bool:
        """
        Cython signature: bool getAllowChildren()
        Returns true if the children of this term are allowed to be used
        """
        ...
    
    def setCVIdentifierRef(self, cv_identifier_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCVIdentifierRef(String cv_identifier_ref)
        Sets the CV identifier reference string, e.g. UO for unit obo
        """
        ...
    
    def getCVIdentifierRef(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCVIdentifierRef()
        Returns the CV identifier reference string
        """
        ...
    
    def __richcmp__(self, other: CVMappingTerm, op: int) -> Any:
        ... 


class CachedSwathFileConsumer:
    """
    Cython implementation of _CachedSwathFileConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CachedSwathFileConsumer.html>`_
      -- Inherits from ['FullSwathFileConsumer']
    """
    
    @overload
    def __init__(self, in_0: CachedSwathFileConsumer ) -> None:
        """
        Cython signature: void CachedSwathFileConsumer(CachedSwathFileConsumer &)
        """
        ...
    
    @overload
    def __init__(self, cachedir: Union[bytes, str, String] , basename: Union[bytes, str, String] , nr_ms1_spectra: int , nr_ms2_spectra: List[int] ) -> None:
        """
        Cython signature: void CachedSwathFileConsumer(String cachedir, String basename, size_t nr_ms1_spectra, libcpp_vector[int] nr_ms2_spectra)
        """
        ...
    
    def setExpectedSize(self, s: int , c: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t s, size_t c)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings exp)
        """
        ...
    
    def retrieveSwathMaps(self, maps: List[SwathMap] ) -> None:
        """
        Cython signature: void retrieveSwathMaps(libcpp_vector[SwathMap] & maps)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        """
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


class ChromatogramExtractor:
    """
    Cython implementation of _ChromatogramExtractor

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ChromatogramExtractor.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ChromatogramExtractor()
        """
        ...
    
    @overload
    def __init__(self, in_0: ChromatogramExtractor ) -> None:
        """
        Cython signature: void ChromatogramExtractor(ChromatogramExtractor &)
        """
        ...
    
    def extractChromatograms(self, input: SpectrumAccessOpenMS , output: List[OSChromatogram] , extraction_coordinates: List[ExtractionCoordinates] , mz_extraction_window: float , ppm: bool , im_extraction_window: float , filter: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void extractChromatograms(shared_ptr[SpectrumAccessOpenMS] input, libcpp_vector[shared_ptr[OSChromatogram]] & output, libcpp_vector[ExtractionCoordinates] extraction_coordinates, double mz_extraction_window, bool ppm, double im_extraction_window, String filter)
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
    
    prepare_coordinates: __static_ChromatogramExtractor_prepare_coordinates 


class CoarseIsotopePatternGenerator:
    """
    Cython implementation of _CoarseIsotopePatternGenerator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CoarseIsotopePatternGenerator.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CoarseIsotopePatternGenerator()
        """
        ...
    
    @overload
    def __init__(self, max_isotope: int ) -> None:
        """
        Cython signature: void CoarseIsotopePatternGenerator(size_t max_isotope)
        """
        ...
    
    @overload
    def __init__(self, max_isotope: int , round_masses: bool ) -> None:
        """
        Cython signature: void CoarseIsotopePatternGenerator(size_t max_isotope, bool round_masses)
        """
        ...
    
    def run(self, in_0: EmpiricalFormula ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution run(EmpiricalFormula)
        """
        ...
    
    def getRoundMasses(self) -> bool:
        """
        Cython signature: bool getRoundMasses()
        Returns the current value of the flag to round masses to integer values (true) or return accurate masses (false)
        """
        ...
    
    def setRoundMasses(self, round_masses_: bool ) -> None:
        """
        Cython signature: void setRoundMasses(bool round_masses_)
        Sets the round_masses_ flag to round masses to integer values (true) or return accurate masses (false)
        """
        ...
    
    def getMaxIsotope(self) -> int:
        """
        Cython signature: size_t getMaxIsotope()
        Returns the currently set maximum isotope
        """
        ...
    
    def setMaxIsotope(self, max_isotope: int ) -> None:
        """
        Cython signature: void setMaxIsotope(size_t max_isotope)
        Sets the maximal isotope with 'max_isotope'
        """
        ...
    
    def estimateFromPeptideWeight(self, average_weight: float ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution estimateFromPeptideWeight(double average_weight)
        Estimate Peptide Isotopedistribution from weight and number of isotopes that should be reported
        """
        ...
    
    def estimateFromPeptideWeightAndS(self, average_weight: float , S: int ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution estimateFromPeptideWeightAndS(double average_weight, unsigned int S)
        Estimate peptide IsotopeDistribution from average weight and exact number of sulfurs
        """
        ...
    
    def estimateFromRNAWeight(self, average_weight: float ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution estimateFromRNAWeight(double average_weight)
        Estimate Nucleotide Isotopedistribution from weight
        """
        ...
    
    def estimateFromDNAWeight(self, average_weight: float ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution estimateFromDNAWeight(double average_weight)
        Estimate Nucleotide Isotopedistribution from weight
        """
        ...
    
    def estimateFromWeightAndComp(self, average_weight: float , C: float , H: float , N: float , O: float , S: float , P: float ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution estimateFromWeightAndComp(double average_weight, double C, double H, double N, double O, double S, double P)
        """
        ...
    
    def estimateFromWeightAndCompAndS(self, average_weight: float , S: int , C: float , H: float , N: float , O: float , P: float ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution estimateFromWeightAndCompAndS(double average_weight, unsigned int S, double C, double H, double N, double O, double P)
        Estimate IsotopeDistribution from weight, exact number of sulfurs, and average remaining composition
        """
        ...
    
    def estimateForFragmentFromPeptideWeight(self, average_weight_precursor: float , average_weight_fragment: float , precursor_isotopes: Set[int] ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution estimateForFragmentFromPeptideWeight(double average_weight_precursor, double average_weight_fragment, libcpp_set[unsigned int] & precursor_isotopes)
        Estimate peptide fragment IsotopeDistribution from the precursor's average weight, fragment's average weight, and a set of isolated precursor isotopes
        """
        ...
    
    def estimateForFragmentFromPeptideWeightAndS(self, average_weight_precursor: float , S_precursor: int , average_weight_fragment: float , S_fragment: int , precursor_isotopes: Set[int] ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution estimateForFragmentFromPeptideWeightAndS(double average_weight_precursor, unsigned int S_precursor, double average_weight_fragment, unsigned int S_fragment, libcpp_set[unsigned int] & precursor_isotopes)
        Estimate peptide fragment IsotopeDistribution from the precursor's average weight,
        number of sulfurs in the precursor, fragment's average weight, number of sulfurs in the fragment,
        and a set of isolated precursor isotopes.
        """
        ...
    
    def approximateFromPeptideWeight(self, mass: float , num_peaks: int , charge: int ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution approximateFromPeptideWeight(double mass, unsigned int num_peaks, unsigned int charge)
        Roughly approximate peptide IsotopeDistribution from monoisotopic weight using Poisson distribution.
        m/z values approximated by adding one neutron mass (divided by charge) for every peak, starting at
        the given monoisotopic weight. Foundation from: Bellew et al, https://dx.doi.org/10.1093/bioinformatics/btl276
        This method is around 50 times faster than estimateFromPeptideWeight, but only an approximation.
        The following are the intensities of the first 6 peaks generated for a monoisotopic mass of 1000:
        estimateFromPeptideWeight:    0.571133000;0.306181000;0.095811100;0.022036900;0.004092170;0.000644568
        approximateFromPeptideWeight: 0.573753000;0.318752000;0.088542200;0.016396700;0.002277320;0.000253036
        KL divergences of the first 20 intensities of estimateFromPeptideWeight and this approximation range from 4.97E-5 for a
        monoisotopic mass of 20 to 0.0144 for a mass of 2500. For comparison, when comparing an observed pattern with a
        theoretical ground truth, the observed pattern is said to be an isotopic pattern if the KL between the two is below 0.05
        for 2 peaks and below 0.6 for >=6 peaks by Guo Ci Teo et al.
        """
        ...
    
    def approximateIntensities(self, mass: float , num_peaks: int ) -> List[float]:
        """
        Cython signature: libcpp_vector[double] approximateIntensities(double mass, unsigned int num_peaks)
        Roughly approximate peptidic isotope pattern intensities from monoisotopic weight using Poisson distribution.
        Foundation from: Bellew et al, https://dx.doi.org/10.1093/bioinformatics/btl276
        This method is around 100 times faster than estimateFromPeptideWeight, but only an approximation, see approximateFromPeptideWeight.
        """
        ...
    
    def estimateForFragmentFromRNAWeight(self, average_weight_precursor: float , average_weight_fragment: float , precursor_isotopes: Set[int] ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution estimateForFragmentFromRNAWeight(double average_weight_precursor, double average_weight_fragment, libcpp_set[unsigned int] & precursor_isotopes)
        Estimate RNA fragment IsotopeDistribution from the precursor's average weight,
        fragment's average weight, and a set of isolated precursor isotopes
        """
        ...
    
    def estimateForFragmentFromDNAWeight(self, average_weight_precursor: float , average_weight_fragment: float , precursor_isotopes: Set[int] ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution estimateForFragmentFromDNAWeight(double average_weight_precursor, double average_weight_fragment, libcpp_set[unsigned int] & precursor_isotopes)
        Estimate DNA fragment IsotopeDistribution from the precursor's average weight,
        fragment's average weight, and a set of isolated precursor isotopes.
        """
        ...
    
    def estimateForFragmentFromWeightAndComp(self, average_weight_precursor: float , average_weight_fragment: float , precursor_isotopes: Set[int] , C: float , H: float , N: float , O: float , S: float , P: float ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution estimateForFragmentFromWeightAndComp(double average_weight_precursor, double average_weight_fragment, libcpp_set[unsigned int] & precursor_isotopes, double C, double H, double N, double O, double S, double P)
        Estimate fragment IsotopeDistribution from the precursor's average weight,
        fragment's average weight, a set of isolated precursor isotopes, and average composition
        """
        ...
    
    def calcFragmentIsotopeDist(self, fragment_isotope_dist: IsotopeDistribution , comp_fragment_isotope_dist: IsotopeDistribution , precursor_isotopes: Set[int] , fragment_mono_mass: float ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution calcFragmentIsotopeDist(IsotopeDistribution & fragment_isotope_dist, IsotopeDistribution & comp_fragment_isotope_dist, libcpp_set[unsigned int] & precursor_isotopes, double fragment_mono_mass)
        Calculate isotopic distribution for a fragment molecule
        """
        ... 


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


class ConsensusIDAlgorithmWorst:
    """
    Cython implementation of _ConsensusIDAlgorithmWorst

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithmWorst.html>`_
      -- Inherits from ['ConsensusIDAlgorithmIdentity']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusIDAlgorithmWorst()
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


class DIAScoring:
    """
    Cython implementation of _DIAScoring

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DIAScoring.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void DIAScoring()
        """
        ...
    
    def dia_ms1_massdiff_score(self, precursor_mz: float , spectrum: List[OSSpectrum] , im_range: RangeMobility , ppm_score: float ) -> bool:
        """
        Cython signature: bool dia_ms1_massdiff_score(double precursor_mz, libcpp_vector[shared_ptr[OSSpectrum]] spectrum, RangeMobility & im_range, double & ppm_score)
        """
        ...
    
    def dia_ms1_isotope_scores_averagine(self, precursor_mz: float , spectrum: List[OSSpectrum] , charge_state: int , im_range: RangeMobility , isotope_corr: float , isotope_overlap: float ) -> None:
        """
        Cython signature: void dia_ms1_isotope_scores_averagine(double precursor_mz, libcpp_vector[shared_ptr[OSSpectrum]] spectrum, int charge_state, RangeMobility & im_range, double & isotope_corr, double & isotope_overlap)
        """
        ...
    
    def dia_ms1_isotope_scores(self, precursor_mz: float , spectrum: List[OSSpectrum] , im_range: RangeMobility , isotope_corr: float , isotope_overlap: float , sum_formula: EmpiricalFormula ) -> None:
        """
        Cython signature: void dia_ms1_isotope_scores(double precursor_mz, libcpp_vector[shared_ptr[OSSpectrum]] spectrum, RangeMobility & im_range, double & isotope_corr, double & isotope_overlap, EmpiricalFormula & sum_formula)
        """
        ...
    
    def score_with_isotopes(self, spectrum: List[OSSpectrum] , transitions: List[LightTransition] , im_range: RangeMobility , dotprod: float , manhattan: float ) -> None:
        """
        Cython signature: void score_with_isotopes(libcpp_vector[shared_ptr[OSSpectrum]] spectrum, libcpp_vector[LightTransition] transitions, RangeMobility & im_range, double & dotprod, double & manhattan)
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


class DistanceMatrix:
    """
    Cython implementation of _DistanceMatrix[float]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DistanceMatrix[float].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DistanceMatrix()
        """
        ...
    
    @overload
    def __init__(self, in_0: DistanceMatrix ) -> None:
        """
        Cython signature: void DistanceMatrix(DistanceMatrix &)
        """
        ...
    
    @overload
    def __init__(self, dimensionsize: int , value: float ) -> None:
        """
        Cython signature: void DistanceMatrix(size_t dimensionsize, float value)
        """
        ...
    
    def getValue(self, i: int , j: int ) -> float:
        """
        Cython signature: float getValue(size_t i, size_t j)
        """
        ...
    
    def setValue(self, i: int , j: int , value: float ) -> None:
        """
        Cython signature: void setValue(size_t i, size_t j, float value)
        """
        ...
    
    def setValueQuick(self, i: int , j: int , value: float ) -> None:
        """
        Cython signature: void setValueQuick(size_t i, size_t j, float value)
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def resize(self, dimensionsize: int , value: float ) -> None:
        """
        Cython signature: void resize(size_t dimensionsize, float value)
        """
        ...
    
    def reduce(self, j: int ) -> None:
        """
        Cython signature: void reduce(size_t j)
        """
        ...
    
    def dimensionsize(self) -> int:
        """
        Cython signature: size_t dimensionsize()
        """
        ...
    
    def updateMinElement(self) -> None:
        """
        Cython signature: void updateMinElement()
        """
        ...
    
    def getMinElementCoordinates(self) -> List[int, int]:
        """
        Cython signature: libcpp_pair[size_t,size_t] getMinElementCoordinates()
        """
        ...
    
    def __richcmp__(self, other: DistanceMatrix, op: int) -> Any:
        ... 


class ElutionModelFitter:
    """
    Cython implementation of _ElutionModelFitter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ElutionModelFitter.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ElutionModelFitter()
        Helper class for fitting elution models to features
        """
        ...
    
    @overload
    def __init__(self, in_0: ElutionModelFitter ) -> None:
        """
        Cython signature: void ElutionModelFitter(ElutionModelFitter &)
        """
        ...
    
    def fitElutionModels(self, features: FeatureMap ) -> None:
        """
        Cython signature: void fitElutionModels(FeatureMap & features)
        Fit models of elution profiles to all features (and validate them)
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


class EmgModel:
    """
    Cython implementation of _EmgModel

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1EmgModel.html>`_
      -- Inherits from ['InterpolationModel']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void EmgModel()
        Exponentially modified gaussian distribution model for elution profiles
        """
        ...
    
    @overload
    def __init__(self, in_0: EmgModel ) -> None:
        """
        Cython signature: void EmgModel(EmgModel &)
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


class FIAMSDataProcessor:
    """
    Cython implementation of _FIAMSDataProcessor

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FIAMSDataProcessor.html>`_
      -- Inherits from ['DefaultParamHandler']

      ADD PYTHON DOCUMENTATION HERE
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FIAMSDataProcessor()
        Data processing for FIA-MS data
        """
        ...
    
    @overload
    def __init__(self, in_0: FIAMSDataProcessor ) -> None:
        """
        Cython signature: void FIAMSDataProcessor(FIAMSDataProcessor &)
        """
        ...
    
    def run(self, experiment: MSExperiment , n_seconds: float , output: MzTab , load_cached_spectrum: bool ) -> bool:
        """
        Cython signature: bool run(MSExperiment & experiment, float & n_seconds, MzTab & output, bool load_cached_spectrum)
        Run the full analysis for the experiment for the given time interval\n
        
        The workflow steps are:
        - the time axis of the experiment is cut to the interval from 0 to n_seconds
        - the spectra are summed into one along the time axis with the bin size determined by mz and instrument resolution
        - data is smoothed by applying the Savitzky-Golay filter
        - peaks are picked
        - the accurate mass search for all the picked peaks is performed
        
        The intermediate summed spectra and picked peaks can be saved to the filesystem.
        Also, the results of the accurate mass search and the signal-to-noise information
        of the resulting spectrum is saved.
        
        
        :param experiment: Input MSExperiment
        :param n_seconds: Input number of seconds
        :param load_cached_spectrum: Load the cached picked spectrum if exists
        :param output: Output of the accurate mass search results
        :return: A boolean indicating if the picked spectrum was loaded from the cached file
        """
        ...
    
    def extractPeaks(self, input_: MSSpectrum ) -> MSSpectrum:
        """
        Cython signature: MSSpectrum extractPeaks(MSSpectrum & input_)
        Pick peaks from the summed spectrum
        
        
        :param input: Input vector of spectra
        :return: A spectrum with picked peaks
        """
        ...
    
    def convertToFeatureMap(self, input_: MSSpectrum ) -> FeatureMap:
        """
        Cython signature: FeatureMap convertToFeatureMap(MSSpectrum & input_)
        Convert a spectrum to a feature map with the corresponding polarity\n
        
        Applies `SavitzkyGolayFilter` and `PeakPickerHiRes`
        
        
        :param input: Input a picked spectrum
        :return: A feature map with the peaks converted to features and polarity from the parameters
        """
        ...
    
    def trackNoise(self, input_: MSSpectrum ) -> MSSpectrum:
        """
        Cython signature: MSSpectrum trackNoise(MSSpectrum & input_)
        Estimate noise for each peak\n
        
        Uses `SignalToNoiseEstimatorMedianRapid`
        
        
        :param input: Input a picked spectrum
        :return: A spectrum object storing logSN information
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


class FeatureFindingMetabo:
    """
    Cython implementation of _FeatureFindingMetabo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureFindingMetabo.html>`_
      -- Inherits from ['ProgressLogger', 'DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureFindingMetabo()
        Method for the assembly of mass traces belonging to the same isotope
        pattern, i.e., that are compatible in retention times, mass-to-charge ratios,
        and isotope abundances
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureFindingMetabo ) -> None:
        """
        Cython signature: void FeatureFindingMetabo(FeatureFindingMetabo &)
        """
        ...
    
    def run(self, input_mtraces: List[Kernel_MassTrace] , output_featmap: FeatureMap , output_chromatograms: List[List[MSChromatogram]] ) -> None:
        """
        Cython signature: void run(libcpp_vector[Kernel_MassTrace] input_mtraces, FeatureMap & output_featmap, libcpp_vector[libcpp_vector[MSChromatogram]] & output_chromatograms)
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


class FineIsotopePatternGenerator:
    """
    Cython implementation of _FineIsotopePatternGenerator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FineIsotopePatternGenerator.html>`_

    Isotope pattern generator for fine isotope distributions.
    Generates isotopes until a stop condition (threshold) is reached,
    the lower the threshold the more isotopes are generated. The
    parameter use_total_prob defines whether the stop condition is
    interpreted as the total probability that the distribution should
    cover (default) or as a threshold for individual peaks. Finally,
    the absolute parameter specifies for individual peak thresholding
    if the threshold is absolute or relative.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FineIsotopePatternGenerator()
        """
        ...
    
    @overload
    def __init__(self, threshold: float ) -> None:
        """
        Cython signature: void FineIsotopePatternGenerator(double threshold)
        """
        ...
    
    @overload
    def __init__(self, threshold: float , use_total_prob: bool ) -> None:
        """
        Cython signature: void FineIsotopePatternGenerator(double threshold, bool use_total_prob)
        """
        ...
    
    @overload
    def __init__(self, threshold: float , use_total_prob: bool , absolute: bool ) -> None:
        """
        Cython signature: void FineIsotopePatternGenerator(double threshold, bool use_total_prob, bool absolute)
        """
        ...
    
    def setThreshold(self, threshold: float ) -> None:
        """
        Cython signature: void setThreshold(double threshold)
        """
        ...
    
    def getThreshold(self) -> float:
        """
        Cython signature: double getThreshold()
        """
        ...
    
    def setAbsolute(self, absolute: bool ) -> None:
        """
        Cython signature: void setAbsolute(bool absolute)
        """
        ...
    
    def getAbsolute(self) -> bool:
        """
        Cython signature: bool getAbsolute()
        """
        ...
    
    def setTotalProbability(self, total: bool ) -> None:
        """
        Cython signature: void setTotalProbability(bool total)
        """
        ...
    
    def getTotalProbability(self) -> bool:
        """
        Cython signature: bool getTotalProbability()
        """
        ...
    
    def run(self, in_0: EmpiricalFormula ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution run(EmpiricalFormula)
        """
        ... 


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


class HyperScore:
    """
    Cython implementation of _HyperScore

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1HyperScore.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void HyperScore()
        An implementation of the X!Tandem HyperScore PSM scoring function
        """
        ...
    
    @overload
    def __init__(self, in_0: HyperScore ) -> None:
        """
        Cython signature: void HyperScore(HyperScore &)
        """
        ...
    
    def compute(self, fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool , exp_spectrum: MSSpectrum , theo_spectrum: MSSpectrum ) -> float:
        """
        Cython signature: double compute(double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm, MSSpectrum & exp_spectrum, MSSpectrum & theo_spectrum)
        Compute the (ln transformed) X!Tandem HyperScore\n
        
        1. the dot product of peak intensities between matching peaks in experimental and theoretical spectrum is calculated
        2. the HyperScore is calculated from the dot product by multiplying by factorials of matching b- and y-ions
        
        
        :note: Peak intensities of the theoretical spectrum are typically 1 or TIC normalized, but can also be e.g. ion probabilities
        :param fragment_mass_tolerance: Mass tolerance applied left and right of the theoretical spectrum peak position
        :param fragment_mass_tolerance_unit_ppm: Unit of the mass tolerance is: Thomson if false, ppm if true
        :param exp_spectrum: Measured spectrum
        :param theo_spectrum: Theoretical spectrum Peaks need to contain an ion annotation as provided by TheoreticalSpectrumGenerator
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


class Instrument:
    """
    Cython implementation of _Instrument

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Instrument.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Instrument()
        Description of a MS instrument
        """
        ...
    
    @overload
    def __init__(self, in_0: Instrument ) -> None:
        """
        Cython signature: void Instrument(Instrument &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the instrument
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the instrument
        """
        ...
    
    def getVendor(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVendor()
        Returns the instrument vendor
        """
        ...
    
    def setVendor(self, vendor: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setVendor(String vendor)
        Sets the instrument vendor
        """
        ...
    
    def getModel(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getModel()
        Returns the instrument model
        """
        ...
    
    def setModel(self, model: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setModel(String model)
        Sets the instrument model
        """
        ...
    
    def getCustomizations(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCustomizations()
        Returns a description of customizations
        """
        ...
    
    def setCustomizations(self, customizations: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCustomizations(String customizations)
        Sets the a description of customizations
        """
        ...
    
    def getIonSources(self) -> List[IonSource]:
        """
        Cython signature: libcpp_vector[IonSource] getIonSources()
        Returns the ion source list
        """
        ...
    
    def setIonSources(self, ion_sources: List[IonSource] ) -> None:
        """
        Cython signature: void setIonSources(libcpp_vector[IonSource] ion_sources)
        Sets the ion source list
        """
        ...
    
    def getMassAnalyzers(self) -> List[MassAnalyzer]:
        """
        Cython signature: libcpp_vector[MassAnalyzer] getMassAnalyzers()
        Returns the mass analyzer list
        """
        ...
    
    def setMassAnalyzers(self, mass_analyzers: List[MassAnalyzer] ) -> None:
        """
        Cython signature: void setMassAnalyzers(libcpp_vector[MassAnalyzer] mass_analyzers)
        Sets the mass analyzer list
        """
        ...
    
    def getIonDetectors(self) -> List[IonDetector]:
        """
        Cython signature: libcpp_vector[IonDetector] getIonDetectors()
        Returns the ion detector list
        """
        ...
    
    def setIonDetectors(self, ion_detectors: List[IonDetector] ) -> None:
        """
        Cython signature: void setIonDetectors(libcpp_vector[IonDetector] ion_detectors)
        Sets the ion detector list
        """
        ...
    
    def getSoftware(self) -> Software:
        """
        Cython signature: Software getSoftware()
        Returns the instrument software
        """
        ...
    
    def setSoftware(self, software: Software ) -> None:
        """
        Cython signature: void setSoftware(Software software)
        Sets the instrument software
        """
        ...
    
    def getIonOptics(self) -> int:
        """
        Cython signature: IonOpticsType getIonOptics()
        Returns the ion optics type
        """
        ...
    
    def setIonOptics(self, ion_optics: int ) -> None:
        """
        Cython signature: void setIonOptics(IonOpticsType ion_optics)
        Sets the ion optics type
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
    
    def __richcmp__(self, other: Instrument, op: int) -> Any:
        ... 


class IonSource:
    """
    Cython implementation of _IonSource

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IonSource.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IonSource()
        Description of an ion source (part of a MS Instrument)
        """
        ...
    
    @overload
    def __init__(self, in_0: IonSource ) -> None:
        """
        Cython signature: void IonSource(IonSource &)
        """
        ...
    
    def getPolarity(self) -> int:
        """
        Cython signature: Polarity getPolarity()
        Returns the ionization mode
        """
        ...
    
    def setPolarity(self, polarity: int ) -> None:
        """
        Cython signature: void setPolarity(Polarity polarity)
        Sets the ionization mode
        """
        ...
    
    def getInletType(self) -> int:
        """
        Cython signature: InletType getInletType()
        Returns the inlet type
        """
        ...
    
    def setInletType(self, inlet_type: int ) -> None:
        """
        Cython signature: void setInletType(InletType inlet_type)
        Sets the inlet type
        """
        ...
    
    def getIonizationMethod(self) -> int:
        """
        Cython signature: IonizationMethod getIonizationMethod()
        Returns the ionization method
        """
        ...
    
    def setIonizationMethod(self, ionization_type: int ) -> None:
        """
        Cython signature: void setIonizationMethod(IonizationMethod ionization_type)
        Sets the ionization method
        """
        ...
    
    def getOrder(self) -> int:
        """
        Cython signature: int getOrder()
        Returns the position of this part in the whole Instrument
        
        Order can be ignored, as long the instrument has this default setup:
          - one ion source
          - one or many mass analyzers
          - one ion detector
        
        For more complex instruments, the order should be defined.
        """
        ...
    
    def setOrder(self, order: int ) -> None:
        """
        Cython signature: void setOrder(int order)
        Sets the order
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
    
    def __richcmp__(self, other: IonSource, op: int) -> Any:
        ...
    InletType : __InletType
    IonizationMethod : __IonizationMethod
    Polarity : __Polarity 


class IsotopeDistribution:
    """
    Cython implementation of _IsotopeDistribution

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsotopeDistribution.html>`_

    Isotope distribution class
    
    A container that holds an isotope distribution. It consists of mass values
    and their correspondent probabilities (stored in the intensity slot)
    
    Isotope distributions can be calculated using either the
    CoarseIsotopePatternGenerator for quantized atomic masses which group
    isotopes with the same atomic number. Alternatively, the
    FineIsotopePatternGenerator can be used that calculates hyperfine isotopic
    distributions
    
    This class only describes the container that holds the isotopic
    distribution, calculations are done using classes derived from
    IsotopePatternGenerator
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IsotopeDistribution()
        """
        ...
    
    @overload
    def __init__(self, in_0: IsotopeDistribution ) -> None:
        """
        Cython signature: void IsotopeDistribution(IsotopeDistribution &)
        """
        ...
    
    def set(self, distribution: List[Peak1D] ) -> None:
        """
        Cython signature: void set(libcpp_vector[Peak1D] & distribution)
        Overwrites the container which holds the distribution using 'distribution'
        """
        ...
    
    def insert(self, mass: float , intensity: float ) -> None:
        """
        Cython signature: void insert(double mass, float intensity)
        """
        ...
    
    def getContainer(self) -> List[Peak1D]:
        """
        Cython signature: libcpp_vector[Peak1D] & getContainer()
        Returns the container which holds the distribution
        """
        ...
    
    def getMax(self) -> float:
        """
        Cython signature: double getMax()
        Returns the maximal weight isotope which is stored in the distribution
        """
        ...
    
    def getMin(self) -> float:
        """
        Cython signature: double getMin()
        Returns the minimal weight isotope which is stored in the distribution
        """
        ...
    
    def getMostAbundant(self) -> Peak1D:
        """
        Cython signature: Peak1D getMostAbundant()
        Returns the most abundant isotope which is stored in the distribution
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        Returns the size of the distribution which is the number of isotopes in the distribution
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        Clears the distribution and resets max isotope to 0
        """
        ...
    
    def renormalize(self) -> None:
        """
        Cython signature: void renormalize()
        Renormalizes the sum of the probabilities of the isotopes to 1
        """
        ...
    
    def trimRight(self, cutoff: float ) -> None:
        """
        Cython signature: void trimRight(double cutoff)
        Trims the right side of the isotope distribution to isotopes with a significant contribution
        """
        ...
    
    def trimLeft(self, cutoff: float ) -> None:
        """
        Cython signature: void trimLeft(double cutoff)
        Trims the left side of the isotope distribution to isotopes with a significant contribution
        """
        ...
    
    def merge(self, in_0: float , in_1: float ) -> None:
        """
        Cython signature: void merge(double, double)
        Merges distributions of arbitrary data points with constant defined resolution
        """
        ...
    
    def resize(self, size: int ) -> None:
        """
        Cython signature: void resize(unsigned int size)
        Resizes distribution container
        """
        ...
    
    def trimIntensities(self, cutoff: float ) -> None:
        """
        Cython signature: void trimIntensities(double cutoff)
        Remove intensities below the cutoff
        """
        ...
    
    def sortByIntensity(self) -> None:
        """
        Cython signature: void sortByIntensity()
        Sort isotope distribution by intensity
        """
        ...
    
    def sortByMass(self) -> None:
        """
        Cython signature: void sortByMass()
        Sort isotope distribution by mass
        """
        ...
    
    def averageMass(self) -> float:
        """
        Cython signature: double averageMass()
        Compute average mass of isotope distribution (weighted average of all isotopes)
        """
        ...
    
    def __iter__(self) -> Peak1D:
       ...
    Sorted : __Sorted 


class IsotopePattern:
    """
    Cython implementation of _IsotopePattern

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::FeatureFinderAlgorithmPickedHelperStructs_1_1IsotopePattern.html>`_
    """
    
    spectrum: List[int]
    
    intensity: List[float]
    
    mz_score: List[float]
    
    theoretical_mz: List[float]
    
    theoretical_pattern: TheoreticalIsotopePattern
    
    @overload
    def __init__(self, size: int ) -> None:
        """
        Cython signature: void IsotopePattern(size_t size)
        """
        ...
    
    @overload
    def __init__(self, in_0: IsotopePattern ) -> None:
        """
        Cython signature: void IsotopePattern(IsotopePattern &)
        """
        ... 


class Kernel_MassTrace:
    """
    Cython implementation of _Kernel_MassTrace

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Kernel_MassTrace.html>`_
    """
    
    fwhm_mz_avg: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Kernel_MassTrace()
        """
        ...
    
    @overload
    def __init__(self, in_0: Kernel_MassTrace ) -> None:
        """
        Cython signature: void Kernel_MassTrace(Kernel_MassTrace &)
        """
        ...
    
    @overload
    def __init__(self, trace_peaks: List[Peak2D] ) -> None:
        """
        Cython signature: void Kernel_MassTrace(const libcpp_vector[Peak2D] & trace_peaks)
        """
        ...
    
    def getSize(self) -> int:
        """
        Cython signature: size_t getSize()
        Returns the number of peaks contained in the mass trace
        """
        ...
    
    def getLabel(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getLabel()
        Returns label of mass trace
        """
        ...
    
    def setLabel(self, label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLabel(String label)
        Sets label of mass trace
        """
        ...
    
    def getCentroidMZ(self) -> float:
        """
        Cython signature: double getCentroidMZ()
        Returns the centroid m/z
        """
        ...
    
    def getCentroidRT(self) -> float:
        """
        Cython signature: double getCentroidRT()
        Returns the centroid RT
        """
        ...
    
    def getCentroidSD(self) -> float:
        """
        Cython signature: double getCentroidSD()
        Returns the centroid SD
        """
        ...
    
    def getFWHM(self) -> float:
        """
        Cython signature: double getFWHM()
        Returns FWHM
        """
        ...
    
    def getTraceLength(self) -> float:
        """
        Cython signature: double getTraceLength()
        Returns the length of the trace (as difference in RT)
        """
        ...
    
    def getFWHMborders(self) -> List[int, int]:
        """
        Cython signature: libcpp_pair[size_t,size_t] getFWHMborders()
        Returns FWHM boarders
        """
        ...
    
    def getSmoothedIntensities(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] getSmoothedIntensities()
        Returns smoothed intensities (empty if no smoothing was explicitly done beforehand!)
        """
        ...
    
    def getAverageMS1CycleTime(self) -> float:
        """
        Cython signature: double getAverageMS1CycleTime()
        Returns average scan time of mass trace
        """
        ...
    
    def computeSmoothedPeakArea(self) -> float:
        """
        Cython signature: double computeSmoothedPeakArea()
        Sums all non-negative (smoothed!) intensities in the mass trace
        """
        ...
    
    def computePeakArea(self) -> float:
        """
        Cython signature: double computePeakArea()
        Sums intensities of all peaks in the mass trace
        """
        ...
    
    def computeIntensitySum(self) -> float:
        """
        Cython signature: double computeIntensitySum()
        Sum all peak intensities in the mass trace
        """
        ...
    
    def findMaxByIntPeak(self, in_0: bool ) -> int:
        """
        Cython signature: size_t findMaxByIntPeak(bool)
        Returns the index of the mass trace's highest peak within the MassTrace container (based either on raw or smoothed intensities)
        """
        ...
    
    def estimateFWHM(self, in_0: bool ) -> int:
        """
        Cython signature: size_t estimateFWHM(bool)
        Estimates FWHM of chromatographic peak in seconds (based on either raw or smoothed intensities)
        """
        ...
    
    def computeFwhmArea(self) -> float:
        """
        Cython signature: double computeFwhmArea()
        """
        ...
    
    def computeFwhmAreaSmooth(self) -> float:
        """
        Cython signature: double computeFwhmAreaSmooth()
        Computes chromatographic peak area within the FWHM range.
        """
        ...
    
    def getIntensity(self, in_0: bool ) -> float:
        """
        Cython signature: double getIntensity(bool)
        Returns the intensity
        """
        ...
    
    def getMaxIntensity(self, in_0: bool ) -> float:
        """
        Cython signature: double getMaxIntensity(bool)
        Returns the max intensity
        """
        ...
    
    def getConvexhull(self) -> ConvexHull2D:
        """
        Cython signature: ConvexHull2D getConvexhull()
        Returns the mass trace's convex hull
        """
        ...
    
    def setCentroidSD(self, tmp_sd: float ) -> None:
        """
        Cython signature: void setCentroidSD(double & tmp_sd)
        """
        ...
    
    def setSmoothedIntensities(self, db_vec: List[float] ) -> None:
        """
        Cython signature: void setSmoothedIntensities(libcpp_vector[double] & db_vec)
        Sets smoothed intensities (smoothing is done externally, e.g. by LowessSmoothing)
        """
        ...
    
    def updateSmoothedMaxRT(self) -> None:
        """
        Cython signature: void updateSmoothedMaxRT()
        """
        ...
    
    def updateWeightedMeanRT(self) -> None:
        """
        Cython signature: void updateWeightedMeanRT()
        Compute & update centroid RT as a intensity-weighted mean of RTs
        """
        ...
    
    def updateSmoothedWeightedMeanRT(self) -> None:
        """
        Cython signature: void updateSmoothedWeightedMeanRT()
        """
        ...
    
    def updateMedianRT(self) -> None:
        """
        Cython signature: void updateMedianRT()
        Compute & update centroid RT as median position of intensities
        """
        ...
    
    def updateMedianMZ(self) -> None:
        """
        Cython signature: void updateMedianMZ()
        Compute & update centroid m/z as median of m/z values
        """
        ...
    
    def updateMeanMZ(self) -> None:
        """
        Cython signature: void updateMeanMZ()
        Compute & update centroid m/z as mean of m/z values
        """
        ...
    
    def updateWeightedMeanMZ(self) -> None:
        """
        Cython signature: void updateWeightedMeanMZ()
        Compute & update centroid m/z as weighted mean of m/z values
        """
        ...
    
    def updateWeightedMZsd(self) -> None:
        """
        Cython signature: void updateWeightedMZsd()
        Compute & update m/z standard deviation of mass trace as weighted mean of m/z values
        
        Make sure to call update(Weighted)(Mean|Median)MZ() first! <br>
        use getCentroidSD() to get result
        """
        ...
    
    def setQuantMethod(self, method: int ) -> None:
        """
        Cython signature: void setQuantMethod(MT_QUANTMETHOD method)
        Determine if area or median is used for quantification
        """
        ...
    
    def getQuantMethod(self) -> int:
        """
        Cython signature: MT_QUANTMETHOD getQuantMethod()
        Check if area or median is used for quantification
        """
        ... 


class LightMRMTransitionGroupCP:
    """
    Cython implementation of _MRMTransitionGroup[_MSChromatogram,_LightTransition]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMTransitionGroup[_MSChromatogram,_LightTransition].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightMRMTransitionGroupCP()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightMRMTransitionGroupCP ) -> None:
        """
        Cython signature: void LightMRMTransitionGroupCP(LightMRMTransitionGroupCP &)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def getTransitionGroupID(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTransitionGroupID()
        """
        ...
    
    def setTransitionGroupID(self, tr_gr_id: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTransitionGroupID(String tr_gr_id)
        """
        ...
    
    def getTransitions(self) -> List[LightTransition]:
        """
        Cython signature: libcpp_vector[LightTransition] getTransitions()
        """
        ...
    
    def getTransitionsMuteable(self) -> List[LightTransition]:
        """
        Cython signature: libcpp_vector[LightTransition] getTransitionsMuteable()
        """
        ...
    
    def addTransition(self, transition: LightTransition , key: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addTransition(LightTransition transition, String key)
        """
        ...
    
    def getTransition(self, key: Union[bytes, str, String] ) -> LightTransition:
        """
        Cython signature: LightTransition getTransition(String key)
        """
        ...
    
    def hasTransition(self, key: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasTransition(String key)
        """
        ...
    
    def getChromatograms(self) -> List[MSChromatogram]:
        """
        Cython signature: libcpp_vector[MSChromatogram] getChromatograms()
        """
        ...
    
    def addChromatogram(self, chromatogram: MSChromatogram , key: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addChromatogram(MSChromatogram chromatogram, String key)
        """
        ...
    
    def getChromatogram(self, key: Union[bytes, str, String] ) -> MSChromatogram:
        """
        Cython signature: MSChromatogram getChromatogram(String key)
        """
        ...
    
    def hasChromatogram(self, key: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasChromatogram(String key)
        """
        ...
    
    def getPrecursorChromatograms(self) -> List[MSChromatogram]:
        """
        Cython signature: libcpp_vector[MSChromatogram] getPrecursorChromatograms()
        """
        ...
    
    def addPrecursorChromatogram(self, chromatogram: MSChromatogram , key: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addPrecursorChromatogram(MSChromatogram chromatogram, String key)
        """
        ...
    
    def getPrecursorChromatogram(self, key: Union[bytes, str, String] ) -> MSChromatogram:
        """
        Cython signature: MSChromatogram getPrecursorChromatogram(String key)
        """
        ...
    
    def hasPrecursorChromatogram(self, key: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasPrecursorChromatogram(String key)
        """
        ...
    
    def getFeatures(self) -> List[MRMFeature]:
        """
        Cython signature: libcpp_vector[MRMFeature] getFeatures()
        """
        ...
    
    def getFeaturesMuteable(self) -> List[MRMFeature]:
        """
        Cython signature: libcpp_vector[MRMFeature] getFeaturesMuteable()
        """
        ...
    
    def addFeature(self, feature: MRMFeature ) -> None:
        """
        Cython signature: void addFeature(MRMFeature feature)
        """
        ...
    
    def getBestFeature(self) -> MRMFeature:
        """
        Cython signature: MRMFeature getBestFeature()
        """
        ...
    
    def getLibraryIntensity(self, result: List[float] ) -> None:
        """
        Cython signature: void getLibraryIntensity(libcpp_vector[double] result)
        """
        ...
    
    def subset(self, tr_ids: List[Union[bytes, str]] ) -> LightMRMTransitionGroupCP:
        """
        Cython signature: LightMRMTransitionGroupCP subset(libcpp_vector[libcpp_utf8_string] tr_ids)
        """
        ...
    
    def isInternallyConsistent(self) -> bool:
        """
        Cython signature: bool isInternallyConsistent()
        """
        ...
    
    def chromatogramIdsMatch(self) -> bool:
        """
        Cython signature: bool chromatogramIdsMatch()
        """
        ... 


class LogConfigHandler:
    """
    Cython implementation of _LogConfigHandler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1LogConfigHandler.html>`_
    """
    
    def parse(self, setting: List[bytes] ) -> Param:
        """
        Cython signature: Param parse(const StringList & setting)
        Translates the given list of parameter settings into a LogStream configuration
        
        Translates the given list of parameter settings into a LogStream configuration.
        Usually this list stems from a command line call.
        
        Each element in the stringlist should follow this naming convention
        
        <LOG_NAME> <ACTION> <PARAMETER>
        
        with
        - LOG_NAME: DEBUG,INFO,WARNING,ERROR,FATAL_ERROR
        - ACTION: add,remove,clear
        - PARAMETER: for 'add'/'remove' it is the stream name (cout, cerr or a filename), 'clear' does not require any further parameter
        
        Example:
        `DEBUG add debug.log`
        
        This function will **not** apply to settings to the log handlers. Use configure() for that.
        
        :param setting: StringList containing the configuration options
        :raises ParseError: In case of an invalid configuration.
        :return: Param object containing all settings, that can be applied using the LogConfigHandler.configure() method
        """
        ...
    
    def configure(self, param: Param ) -> None:
        """
        Cython signature: void configure(const Param & param)
        Applies the given parameters (@p param) to the current configuration
        
        <LOG_NAME> <ACTION> <PARAMETER> <STREAMTYPE>
        
        LOG_NAME: DEBUG, INFO, WARNING, ERROR, FATAL_ERROR
        ACTION: add, remove, clear
        PARAMETER: for 'add'/'remove' it is the stream name ('cout', 'cerr' or a filename), 'clear' does not require any further parameter
        STREAMTYPE: FILE, STRING (for a StringStream, which you can grab by this name using getStream() )
        
        You cannot specify a file named "cout" or "cerr" even if you specify streamtype 'FILE' - the handler will mistake this for the
        internal streams, but you can use "./cout" to print to a file named cout.
        
        A classical configuration would contain a list of settings e.g.
        
        `DEBUG add debug.log FILE`
        `INFO remove cout FILE` (FILE will be ignored)
        `INFO add string_stream1 STRING`
        
        :raises ElementNotFound: If the LogStream (first argument) does not exist.
        :raises FileNotWritable: If a file (or stream) should be opened as log file (or stream) that is not accessible.
        :raises IllegalArgument: If a stream should be registered, that was already registered with a different type.
        """
        ...
    
    def setLogLevel(self, log_level: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLogLevel(const String & log_level)
        Sets a minimum log_level by removing all streams from loggers lower than that level.
        Valid levels are from low to high: "DEBUG", "INFO", "WARNING", "ERROR", "FATAL_ERROR"
        """
        ... 


class MRMTransitionGroupCP:
    """
    Cython implementation of _MRMTransitionGroup[_MSChromatogram,_ReactionMonitoringTransition]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMTransitionGroup[_MSChromatogram,_ReactionMonitoringTransition].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMTransitionGroupCP()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMTransitionGroupCP ) -> None:
        """
        Cython signature: void MRMTransitionGroupCP(MRMTransitionGroupCP &)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def getTransitionGroupID(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTransitionGroupID()
        """
        ...
    
    def setTransitionGroupID(self, tr_gr_id: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTransitionGroupID(String tr_gr_id)
        """
        ...
    
    def getTransitions(self) -> List[ReactionMonitoringTransition]:
        """
        Cython signature: libcpp_vector[ReactionMonitoringTransition] getTransitions()
        """
        ...
    
    def getTransitionsMuteable(self) -> List[ReactionMonitoringTransition]:
        """
        Cython signature: libcpp_vector[ReactionMonitoringTransition] getTransitionsMuteable()
        """
        ...
    
    def addTransition(self, transition: ReactionMonitoringTransition , key: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addTransition(ReactionMonitoringTransition transition, String key)
        """
        ...
    
    def getTransition(self, key: Union[bytes, str, String] ) -> ReactionMonitoringTransition:
        """
        Cython signature: ReactionMonitoringTransition getTransition(String key)
        """
        ...
    
    def hasTransition(self, key: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasTransition(String key)
        """
        ...
    
    def getChromatograms(self) -> List[MSChromatogram]:
        """
        Cython signature: libcpp_vector[MSChromatogram] getChromatograms()
        """
        ...
    
    def addChromatogram(self, chromatogram: MSChromatogram , key: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addChromatogram(MSChromatogram chromatogram, String key)
        """
        ...
    
    def getChromatogram(self, key: Union[bytes, str, String] ) -> MSChromatogram:
        """
        Cython signature: MSChromatogram getChromatogram(String key)
        """
        ...
    
    def hasChromatogram(self, key: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasChromatogram(String key)
        """
        ...
    
    def getPrecursorChromatograms(self) -> List[MSChromatogram]:
        """
        Cython signature: libcpp_vector[MSChromatogram] getPrecursorChromatograms()
        """
        ...
    
    def addPrecursorChromatogram(self, chromatogram: MSChromatogram , key: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addPrecursorChromatogram(MSChromatogram chromatogram, String key)
        """
        ...
    
    def getPrecursorChromatogram(self, key: Union[bytes, str, String] ) -> MSChromatogram:
        """
        Cython signature: MSChromatogram getPrecursorChromatogram(String key)
        """
        ...
    
    def hasPrecursorChromatogram(self, key: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasPrecursorChromatogram(String key)
        """
        ...
    
    def getFeatures(self) -> List[MRMFeature]:
        """
        Cython signature: libcpp_vector[MRMFeature] getFeatures()
        """
        ...
    
    def getFeaturesMuteable(self) -> List[MRMFeature]:
        """
        Cython signature: libcpp_vector[MRMFeature] getFeaturesMuteable()
        """
        ...
    
    def addFeature(self, feature: MRMFeature ) -> None:
        """
        Cython signature: void addFeature(MRMFeature feature)
        """
        ...
    
    def getBestFeature(self) -> MRMFeature:
        """
        Cython signature: MRMFeature getBestFeature()
        """
        ...
    
    def getLibraryIntensity(self, result: List[float] ) -> None:
        """
        Cython signature: void getLibraryIntensity(libcpp_vector[double] result)
        """
        ...
    
    def subset(self, tr_ids: List[Union[bytes, str]] ) -> MRMTransitionGroupCP:
        """
        Cython signature: MRMTransitionGroupCP subset(libcpp_vector[libcpp_utf8_string] tr_ids)
        """
        ...
    
    def isInternallyConsistent(self) -> bool:
        """
        Cython signature: bool isInternallyConsistent()
        """
        ...
    
    def chromatogramIdsMatch(self) -> bool:
        """
        Cython signature: bool chromatogramIdsMatch()
        """
        ... 


class MSDataAggregatingConsumer:
    """
    Cython implementation of _MSDataAggregatingConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSDataAggregatingConsumer.html>`_
    """
    
    def __init__(self, in_0: MSDataAggregatingConsumer ) -> None:
        """
        Cython signature: void MSDataAggregatingConsumer(MSDataAggregatingConsumer &)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        """
        ...
    
    def consumeChromatogram(self, in_0: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram &)
        """
        ...
    
    def setExpectedSize(self, expectedSpectra: int , expectedChromatograms: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t expectedSpectra, size_t expectedChromatograms)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings & exp)
        """
        ... 


class MSPGenericFile:
    """
    Cython implementation of _MSPGenericFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSPGenericFile.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MSPGenericFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MSPGenericFile ) -> None:
        """
        Cython signature: void MSPGenericFile(MSPGenericFile &)
        """
        ...
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , library: MSExperiment ) -> None:
        """
        Cython signature: void MSPGenericFile(const String & filename, MSExperiment & library)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , library: MSExperiment ) -> None:
        """
        Cython signature: void load(const String & filename, MSExperiment & library)
        Load the file's data and metadata, and save it into an `MSExperiment`
        
        
        :param filename: Path to the MSP input file
        :param library: The variable into which the extracted information will be saved
        :raises:
          Exception: FileNotFound If the file could not be found
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , library: MSExperiment ) -> None:
        """
        Cython signature: void store(const String & filename, const MSExperiment & library)
        Save data and metadata into a file
        
        
        :param filename: Path to the MSP input file
        :param library: The variable from which extracted information will be saved
        :raises:
          Exception: FileNotWritable If the file is not writable
        """
        ...
    
    def getDefaultParameters(self, params: Param ) -> None:
        """
        Cython signature: void getDefaultParameters(Param & params)
        Returns the class' default parameters
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


class MapAlignmentAlgorithmPoseClustering:
    """
    Cython implementation of _MapAlignmentAlgorithmPoseClustering

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MapAlignmentAlgorithmPoseClustering.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MapAlignmentAlgorithmPoseClustering()
        """
        ...
    
    @overload
    def align(self, in_0: FeatureMap , in_1: TransformationDescription ) -> None:
        """
        Cython signature: void align(FeatureMap, TransformationDescription &)
        """
        ...
    
    @overload
    def align(self, in_0: MSExperiment , in_1: TransformationDescription ) -> None:
        """
        Cython signature: void align(MSExperiment, TransformationDescription &)
        """
        ...
    
    @overload
    def setReference(self, in_0: FeatureMap ) -> None:
        """
        Cython signature: void setReference(FeatureMap)
        Sets the reference for the alignment
        """
        ...
    
    @overload
    def setReference(self, in_0: MSExperiment ) -> None:
        """
        Cython signature: void setReference(MSExperiment)
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


class MassTrace:
    """
    Cython implementation of _MassTrace

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::FeatureFinderAlgorithmPickedHelperStructs_1_1MassTrace.html>`_
    """
    
    max_rt: float
    
    theoretical_int: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MassTrace()
        """
        ...
    
    @overload
    def __init__(self, in_0: MassTrace ) -> None:
        """
        Cython signature: void MassTrace(MassTrace &)
        """
        ...
    
    def getConvexhull(self) -> ConvexHull2D:
        """
        Cython signature: ConvexHull2D getConvexhull()
        """
        ...
    
    def updateMaximum(self) -> None:
        """
        Cython signature: void updateMaximum()
        """
        ...
    
    def getAvgMZ(self) -> float:
        """
        Cython signature: double getAvgMZ()
        """
        ...
    
    def isValid(self) -> bool:
        """
        Cython signature: bool isValid()
        """
        ... 


class MassTraceDetection:
    """
    Cython implementation of _MassTraceDetection

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MassTraceDetection.html>`_
      -- Inherits from ['ProgressLogger', 'DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MassTraceDetection()
        """
        ...
    
    @overload
    def __init__(self, in_0: MassTraceDetection ) -> None:
        """
        Cython signature: void MassTraceDetection(MassTraceDetection &)
        """
        ...
    
    def run(self, input_map: MSExperiment , traces: List[Kernel_MassTrace] , max_traces: int ) -> None:
        """
        Cython signature: void run(MSExperiment & input_map, libcpp_vector[Kernel_MassTrace] & traces, size_t max_traces)
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


class MassTraces:
    """
    Cython implementation of _MassTraces

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::FeatureFinderAlgorithmPickedHelperStructs_1_1MassTraces.html>`_
    """
    
    max_trace: int
    
    baseline: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MassTraces()
        """
        ...
    
    @overload
    def __init__(self, in_0: MassTraces ) -> None:
        """
        Cython signature: void MassTraces(MassTraces &)
        """
        ...
    
    def getPeakCount(self) -> int:
        """
        Cython signature: size_t getPeakCount()
        """
        ...
    
    def isValid(self, seed_mz: float , trace_tolerance: float ) -> bool:
        """
        Cython signature: bool isValid(double seed_mz, double trace_tolerance)
        """
        ...
    
    def getTheoreticalmaxPosition(self) -> int:
        """
        Cython signature: size_t getTheoreticalmaxPosition()
        """
        ...
    
    def updateBaseline(self) -> None:
        """
        Cython signature: void updateBaseline()
        """
        ...
    
    def getRTBounds(self) -> List[float, float]:
        """
        Cython signature: libcpp_pair[double,double] getRTBounds()
        """
        ... 


class MetaInfo:
    """
    Cython implementation of _MetaInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaInfo.html>`_

    A Type-Name-Value tuple class
    
    MetaInfo maps an index (an integer corresponding to a string) to
    DataValue objects.  The mapping of strings to the index is performed by
    the MetaInfoRegistry, which can be accessed by the method registry()
    
    There are two versions of nearly all members. One which operates with a
    string name and another one which operates on an index. The index version
    is always faster, as it does not need to look up the index corresponding
    to the string in the MetaInfoRegistry
    
    If you wish to add a MetaInfo member to a class, consider deriving that
    class from MetaInfoInterface, instead of simply adding MetaInfo as
    member. MetaInfoInterface implements a full interface to a MetaInfo
    member and is more memory efficient if no meta info gets added
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaInfo()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaInfo ) -> None:
        """
        Cython signature: void MetaInfo(MetaInfo &)
        """
        ...
    
    @overload
    def getValue(self, name: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getValue(String name)
        Returns the value corresponding to a string
        """
        ...
    
    @overload
    def getValue(self, index: int ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getValue(unsigned int index)
        Returns the value corresponding to an index
        """
        ...
    
    @overload
    def getValue(self, name: Union[bytes, str, String] , default_value: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getValue(String name, DataValue default_value)
        Returns the value corresponding to a string
        """
        ...
    
    @overload
    def getValue(self, index: int , default_value: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getValue(unsigned int index, DataValue default_value)
        Returns the value corresponding to an index
        """
        ...
    
    @overload
    def exists(self, name: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool exists(String name)
        Returns if this MetaInfo is set
        """
        ...
    
    @overload
    def exists(self, index: int ) -> bool:
        """
        Cython signature: bool exists(unsigned int index)
        Returns if this MetaInfo is set
        """
        ...
    
    @overload
    def setValue(self, name: Union[bytes, str, String] , value: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setValue(String name, DataValue value)
        Sets the DataValue corresponding to a name
        """
        ...
    
    @overload
    def setValue(self, index: int , value: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setValue(unsigned int index, DataValue value)
        Sets the DataValue corresponding to an index
        """
        ...
    
    @overload
    def removeValue(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeValue(String name)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    @overload
    def removeValue(self, index: int ) -> None:
        """
        Cython signature: void removeValue(unsigned int index)
        Removes the DataValue corresponding to `index` if it exists
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getKeysAsIntegers(self, keys: List[int] ) -> None:
        """
        Cython signature: void getKeysAsIntegers(libcpp_vector[unsigned int] & keys)
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        Removes all meta values
        """
        ...
    
    def registry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry registry()
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


class MzMLSpectrumDecoder:
    """
    Cython implementation of _MzMLSpectrumDecoder

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzMLSpectrumDecoder.html>`_

    A class to decode input strings that contain an mzML chromatogram or spectrum tag
    
    It uses xercesc to parse a string containing either a exactly one mzML
    spectrum or chromatogram (from <chromatogram> to </chromatogram> or
    <spectrum> to </spectrum> tag). It returns the data contained in the
    binaryDataArray for Intensity / mass-to-charge or Intensity / time
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzMLSpectrumDecoder()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzMLSpectrumDecoder ) -> None:
        """
        Cython signature: void MzMLSpectrumDecoder(MzMLSpectrumDecoder &)
        """
        ...
    
    def domParseChromatogram(self, in_: Union[bytes, str, String] , cptr: _Interfaces_Chromatogram ) -> None:
        """
        Cython signature: void domParseChromatogram(String in_, shared_ptr[_Interfaces_Chromatogram] & cptr)
        Extract data from a string which contains a full mzML chromatogram
        
        Extracts data from the input string which is expected to contain exactly
        one <chromatogram> tag (from <chromatogram> to </chromatogram>). This
        function will extract the contained binaryDataArray and provide the
        result as Chromatogram
        
        
        :param in: Input string containing the raw XML
        :param cptr: Resulting chromatogram
        """
        ...
    
    def domParseSpectrum(self, in_: Union[bytes, str, String] , cptr: _Interfaces_Spectrum ) -> None:
        """
        Cython signature: void domParseSpectrum(String in_, shared_ptr[_Interfaces_Spectrum] & cptr)
        Extract data from a string which contains a full mzML spectrum
        
        Extracts data from the input string which is expected to contain exactly
        one <spectrum> tag (from <spectrum> to </spectrum>). This function will
        extract the contained binaryDataArray and provide the result as Spectrum
        
        
        :param in: Input string containing the raw XML
        :param cptr: Resulting spectrum
        """
        ...
    
    def setSkipXMLChecks(self, only: bool ) -> None:
        """
        Cython signature: void setSkipXMLChecks(bool only)
        Whether to skip some XML checks (e.g. removing whitespace inside base64 arrays) and be fast instead
        """
        ... 


class MzMLSwathFileConsumer:
    """
    Cython implementation of _MzMLSwathFileConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzMLSwathFileConsumer.html>`_
      -- Inherits from ['FullSwathFileConsumer']
    """
    
    @overload
    def __init__(self, in_0: MzMLSwathFileConsumer ) -> None:
        """
        Cython signature: void MzMLSwathFileConsumer(MzMLSwathFileConsumer)
        """
        ...
    
    @overload
    def __init__(self, cachedir: Union[bytes, str, String] , basename: Union[bytes, str, String] , nr_ms1_spectra: int , nr_ms2_spectra: List[int] ) -> None:
        """
        Cython signature: void MzMLSwathFileConsumer(String cachedir, String basename, size_t nr_ms1_spectra, libcpp_vector[int] nr_ms2_spectra)
        """
        ...
    
    @overload
    def __init__(self, known_window_boundaries: List[SwathMap] , cachedir: Union[bytes, str, String] , basename: Union[bytes, str, String] , nr_ms1_spectra: int , nr_ms2_spectra: List[int] ) -> None:
        """
        Cython signature: void MzMLSwathFileConsumer(libcpp_vector[SwathMap] known_window_boundaries, String cachedir, String basename, size_t nr_ms1_spectra, libcpp_vector[int] nr_ms2_spectra)
        """
        ...
    
    def setExpectedSize(self, s: int , c: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t s, size_t c)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings exp)
        """
        ...
    
    def retrieveSwathMaps(self, maps: List[SwathMap] ) -> None:
        """
        Cython signature: void retrieveSwathMaps(libcpp_vector[SwathMap] & maps)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        """
        ... 


class NoopMSDataWritingConsumer:
    """
    Cython implementation of _NoopMSDataWritingConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NoopMSDataWritingConsumer.html>`_

    Consumer class that perform no operation
    
    This is sometimes necessary to fulfill the requirement of passing an
    valid MSDataWritingConsumer object or pointer but no operation is
    required
    """
    
    def __init__(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void NoopMSDataWritingConsumer(String filename)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings & exp)
        """
        ...
    
    def setExpectedSize(self, expectedSpectra: int , expectedChromatograms: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t expectedSpectra, size_t expectedChromatograms)
        """
        ...
    
    def addDataProcessing(self, d: DataProcessing ) -> None:
        """
        Cython signature: void addDataProcessing(DataProcessing d)
        """
        ...
    
    def getNrSpectraWritten(self) -> int:
        """
        Cython signature: size_t getNrSpectraWritten()
        """
        ...
    
    def getNrChromatogramsWritten(self) -> int:
        """
        Cython signature: size_t getNrChromatogramsWritten()
        """
        ... 


class OMSSACSVFile:
    """
    Cython implementation of _OMSSACSVFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OMSSACSVFile.html>`_

    File adapter for OMSSACSV files
    
    The files contain the results of the OMSSA algorithm in a comma separated manner. This file adapter is able to
    load the data from such a file into the structures of OpenMS
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OMSSACSVFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: OMSSACSVFile ) -> None:
        """
        Cython signature: void OMSSACSVFile(OMSSACSVFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , protein_identification: ProteinIdentification , id_data: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void load(const String & filename, ProteinIdentification & protein_identification, libcpp_vector[PeptideIdentification] & id_data)
        Loads a OMSSA file
        
        The content of the file is stored in `features`
        
        
        :param filename: The name of the file to read from
        :param protein_identification: The protein ProteinIdentification data
        :param id_data: The peptide ids of the file
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ... 


class OSBinaryDataArray:
    """
    Cython implementation of _OSBinaryDataArray

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1OSBinaryDataArray.html>`_
    """
    
    data: List[float]
    
    description: bytes
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OSBinaryDataArray()
        """
        ...
    
    @overload
    def __init__(self, in_0: OSBinaryDataArray ) -> None:
        """
        Cython signature: void OSBinaryDataArray(OSBinaryDataArray &)
        """
        ... 


class OSChromatogram:
    """
    Cython implementation of _OSChromatogram

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1OSChromatogram.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OSChromatogram()
        """
        ...
    
    @overload
    def __init__(self, in_0: OSChromatogram ) -> None:
        """
        Cython signature: void OSChromatogram(OSChromatogram &)
        """
        ... 


class OSSpectrum:
    """
    Cython implementation of _OSSpectrum

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1OSSpectrum.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OSSpectrum()
        """
        ...
    
    @overload
    def __init__(self, in_0: OSSpectrum ) -> None:
        """
        Cython signature: void OSSpectrum(OSSpectrum &)
        """
        ... 


class OpenMSBuildInfo:
    """
    Cython implementation of _OpenMSBuildInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1OpenMSBuildInfo.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OpenMSBuildInfo()
        """
        ...
    
    @overload
    def __init__(self, in_0: OpenMSBuildInfo ) -> None:
        """
        Cython signature: void OpenMSBuildInfo(OpenMSBuildInfo &)
        """
        ...
    
    getBuildType: __static_OpenMSBuildInfo_getBuildType
    
    getOpenMPMaxNumThreads: __static_OpenMSBuildInfo_getOpenMPMaxNumThreads
    
    isOpenMPEnabled: __static_OpenMSBuildInfo_isOpenMPEnabled
    
    setOpenMPNumThreads: __static_OpenMSBuildInfo_setOpenMPNumThreads 


class OpenMSOSInfo:
    """
    Cython implementation of _OpenMSOSInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1OpenMSOSInfo.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OpenMSOSInfo()
        """
        ...
    
    @overload
    def __init__(self, in_0: OpenMSOSInfo ) -> None:
        """
        Cython signature: void OpenMSOSInfo(OpenMSOSInfo &)
        """
        ...
    
    def getOSAsString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOSAsString()
        """
        ...
    
    def getArchAsString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getArchAsString()
        """
        ...
    
    def getOSVersionAsString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOSVersionAsString()
        """
        ...
    
    getBinaryArchitecture: __static_OpenMSOSInfo_getBinaryArchitecture
    
    getOSInfo: __static_OpenMSOSInfo_getOSInfo 


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


class PlainMSDataWritingConsumer:
    """
    Cython implementation of _PlainMSDataWritingConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PlainMSDataWritingConsumer.html>`_
    """
    
    def __init__(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void PlainMSDataWritingConsumer(String filename)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings & exp)
        Set experimental settings for the whole file
        
        
        :param exp: Experimental settings to be used for this file (from this and the first spectrum/chromatogram, the class will deduce most of the header of the mzML file)
        """
        ...
    
    def setExpectedSize(self, expectedSpectra: int , expectedChromatograms: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t expectedSpectra, size_t expectedChromatograms)
        Set expected size of spectra and chromatograms to be written
        
        These numbers will be written in the spectrumList and chromatogramList
        tag in the mzML file. Therefore, these will contain wrong numbers if
        the expected size is not set correctly
        
        
        :param expectedSpectra: Number of spectra expected
        :param expectedChromatograms: Number of chromatograms expected
        """
        ...
    
    def addDataProcessing(self, d: DataProcessing ) -> None:
        """
        Cython signature: void addDataProcessing(DataProcessing d)
        Optionally add a data processing method to each chromatogram and spectrum
        
        The provided DataProcessing object will be added to each chromatogram
        and spectrum written to to the mzML file
        
        
        :param d: The DataProcessing object to be added
        """
        ...
    
    def getNrSpectraWritten(self) -> int:
        """
        Cython signature: size_t getNrSpectraWritten()
        Returns the number of spectra written
        """
        ...
    
    def getNrChromatogramsWritten(self) -> int:
        """
        Cython signature: size_t getNrChromatogramsWritten()
        Returns the number of chromatograms written
        """
        ...
    
    def setOptions(self, opt: PeakFileOptions ) -> None:
        """
        Cython signature: void setOptions(PeakFileOptions opt)
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        """
        ... 


class RangeIntensity:
    """
    Cython implementation of _RangeIntensity

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1RangeIntensity.html>`_
      -- Inherits from ['RangeBase']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RangeIntensity()
        """
        ...
    
    @overload
    def __init__(self, in_0: RangeIntensity ) -> None:
        """
        Cython signature: void RangeIntensity(RangeIntensity &)
        """
        ...
    
    def setMinIntensity(self, min: float ) -> None:
        """
        Cython signature: void setMinIntensity(double min)
        """
        ...
    
    def setMaxIntensity(self, max: float ) -> None:
        """
        Cython signature: void setMaxIntensity(double max)
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
    
    def extendIntensity(self, value: float ) -> None:
        """
        Cython signature: void extendIntensity(double value)
        Extend the range such that it includes the given @p value
        """
        ...
    
    def containsIntensity(self, value: float ) -> bool:
        """
        Cython signature: bool containsIntensity(double value)
        Is value within [min, max]?
        """
        ...
    
    def setMin(self, min: float ) -> None:
        """
        Cython signature: void setMin(double min)
        """
        ...
    
    def setMax(self, max: float ) -> None:
        """
        Cython signature: void setMax(double max)
        """
        ...
    
    def getMin(self) -> float:
        """
        Cython signature: double getMin()
        """
        ...
    
    def getMax(self) -> float:
        """
        Cython signature: double getMax()
        """
        ...
    
    def extend(self, value: float ) -> None:
        """
        Cython signature: void extend(double value)
        Extend the range such that it includes the given @p value
        """
        ...
    
    def contains(self, value: float ) -> bool:
        """
        Cython signature: bool contains(double value)
        Is value within [min, max]?
        """
        ... 


class RangeMZ:
    """
    Cython implementation of _RangeMZ

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1RangeMZ.html>`_
      -- Inherits from ['RangeBase']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RangeMZ()
        """
        ...
    
    @overload
    def __init__(self, in_0: RangeMZ ) -> None:
        """
        Cython signature: void RangeMZ(RangeMZ &)
        """
        ...
    
    def setMinMZ(self, min: float ) -> None:
        """
        Cython signature: void setMinMZ(double min)
        """
        ...
    
    def setMaxMZ(self, max: float ) -> None:
        """
        Cython signature: void setMaxMZ(double max)
        """
        ...
    
    def getMinMZ(self) -> float:
        """
        Cython signature: double getMinMZ()
        """
        ...
    
    def getMaxMZ(self) -> float:
        """
        Cython signature: double getMaxMZ()
        """
        ...
    
    def extendMZ(self, value: float ) -> None:
        """
        Cython signature: void extendMZ(double value)
        Extend the range such that it includes the given @p value
        """
        ...
    
    def containsMZ(self, value: float ) -> bool:
        """
        Cython signature: bool containsMZ(double value)
        Is value within [min, max]?
        """
        ...
    
    def setMin(self, min: float ) -> None:
        """
        Cython signature: void setMin(double min)
        """
        ...
    
    def setMax(self, max: float ) -> None:
        """
        Cython signature: void setMax(double max)
        """
        ...
    
    def getMin(self) -> float:
        """
        Cython signature: double getMin()
        """
        ...
    
    def getMax(self) -> float:
        """
        Cython signature: double getMax()
        """
        ...
    
    def extend(self, value: float ) -> None:
        """
        Cython signature: void extend(double value)
        Extend the range such that it includes the given @p value
        """
        ...
    
    def contains(self, value: float ) -> bool:
        """
        Cython signature: bool contains(double value)
        Is value within [min, max]?
        """
        ... 


class RangeMobility:
    """
    Cython implementation of _RangeMobility

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1RangeMobility.html>`_
      -- Inherits from ['RangeBase']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RangeMobility()
        """
        ...
    
    @overload
    def __init__(self, in_0: RangeMobility ) -> None:
        """
        Cython signature: void RangeMobility(RangeMobility &)
        """
        ...
    
    def setMinMobility(self, min: float ) -> None:
        """
        Cython signature: void setMinMobility(double min)
        """
        ...
    
    def setMaxMobility(self, max: float ) -> None:
        """
        Cython signature: void setMaxMobility(double max)
        """
        ...
    
    def getMinMobility(self) -> float:
        """
        Cython signature: double getMinMobility()
        Returns the minimum Mobility
        """
        ...
    
    def getMaxMobility(self) -> float:
        """
        Cython signature: double getMaxMobility()
        Returns the maximum Mobility
        """
        ...
    
    def extendMobility(self, value: float ) -> None:
        """
        Cython signature: void extendMobility(double value)
        Extend the range such that it includes the given @p value
        """
        ...
    
    def containsMobility(self, value: float ) -> bool:
        """
        Cython signature: bool containsMobility(double value)
        Is value within [min, max]?
        """
        ...
    
    def setMin(self, min: float ) -> None:
        """
        Cython signature: void setMin(double min)
        """
        ...
    
    def setMax(self, max: float ) -> None:
        """
        Cython signature: void setMax(double max)
        """
        ...
    
    def getMin(self) -> float:
        """
        Cython signature: double getMin()
        """
        ...
    
    def getMax(self) -> float:
        """
        Cython signature: double getMax()
        """
        ...
    
    def extend(self, value: float ) -> None:
        """
        Cython signature: void extend(double value)
        Extend the range such that it includes the given @p value
        """
        ...
    
    def contains(self, value: float ) -> bool:
        """
        Cython signature: bool contains(double value)
        Is value within [min, max]?
        """
        ... 


class RangeRT:
    """
    Cython implementation of _RangeRT

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1RangeRT.html>`_
      -- Inherits from ['RangeBase']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RangeRT()
        """
        ...
    
    @overload
    def __init__(self, in_0: RangeRT ) -> None:
        """
        Cython signature: void RangeRT(RangeRT &)
        """
        ...
    
    def setMinRT(self, min: float ) -> None:
        """
        Cython signature: void setMinRT(double min)
        """
        ...
    
    def setMaxRT(self, max: float ) -> None:
        """
        Cython signature: void setMaxRT(double max)
        """
        ...
    
    def getMinRT(self) -> float:
        """
        Cython signature: double getMinRT()
        """
        ...
    
    def getMaxRT(self) -> float:
        """
        Cython signature: double getMaxRT()
        """
        ...
    
    def extendRT(self, value: float ) -> None:
        """
        Cython signature: void extendRT(double value)
        Extend the range such that it includes the given @p value
        """
        ...
    
    def containsRT(self, value: float ) -> bool:
        """
        Cython signature: bool containsRT(double value)
        Is value within [min, max]?
        """
        ...
    
    def setMin(self, min: float ) -> None:
        """
        Cython signature: void setMin(double min)
        """
        ...
    
    def setMax(self, max: float ) -> None:
        """
        Cython signature: void setMax(double max)
        """
        ...
    
    def getMin(self) -> float:
        """
        Cython signature: double getMin()
        """
        ...
    
    def getMax(self) -> float:
        """
        Cython signature: double getMax()
        """
        ...
    
    def extend(self, value: float ) -> None:
        """
        Cython signature: void extend(double value)
        Extend the range such that it includes the given @p value
        """
        ...
    
    def contains(self, value: float ) -> bool:
        """
        Cython signature: bool contains(double value)
        Is value within [min, max]?
        """
        ... 


class RansacModelLinear:
    """
    Cython implementation of _RansacModelLinear

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1RansacModelLinear.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RansacModelLinear()
        """
        ...
    
    @overload
    def __init__(self, in_0: RansacModelLinear ) -> None:
        """
        Cython signature: void RansacModelLinear(RansacModelLinear &)
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


class RegularSwathFileConsumer:
    """
    Cython implementation of _RegularSwathFileConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1RegularSwathFileConsumer.html>`_
      -- Inherits from ['FullSwathFileConsumer']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RegularSwathFileConsumer()
        """
        ...
    
    @overload
    def __init__(self, in_0: RegularSwathFileConsumer ) -> None:
        """
        Cython signature: void RegularSwathFileConsumer(RegularSwathFileConsumer &)
        """
        ...
    
    def setExpectedSize(self, s: int , c: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t s, size_t c)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings exp)
        """
        ...
    
    def retrieveSwathMaps(self, maps: List[SwathMap] ) -> None:
        """
        Cython signature: void retrieveSwathMaps(libcpp_vector[SwathMap] & maps)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        """
        ... 


class Ribonucleotide:
    """
    Cython implementation of _Ribonucleotide

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Ribonucleotide_1_1Ribonucleotide.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Ribonucleotide()
        """
        ...
    
    @overload
    def __init__(self, in_0: Ribonucleotide ) -> None:
        """
        Cython signature: void Ribonucleotide(Ribonucleotide &)
        """
        ...
    
    @overload
    def __init__(self, name: Union[bytes, str, String] , code: Union[bytes, str, String] , new_code: Union[bytes, str, String] , html_code: Union[bytes, str, String] , formula: EmpiricalFormula , origin: bytes , mono_mass: float , avg_mass: float , term_spec: int , baseloss_formula: EmpiricalFormula ) -> None:
        """
        Cython signature: void Ribonucleotide(String name, String code, String new_code, String html_code, EmpiricalFormula formula, char origin, double mono_mass, double avg_mass, TermSpecificityNuc term_spec, EmpiricalFormula baseloss_formula)
        """
        ...
    
    def getCode(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCode()
        Returns the short name
        """
        ...
    
    def setCode(self, code: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCode(String code)
        Sets the short name
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the ribonucleotide
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the ribonucleotide
        """
        ...
    
    def setFormula(self, formula: EmpiricalFormula ) -> None:
        """
        Cython signature: void setFormula(EmpiricalFormula formula)
        Sets empirical formula of the ribonucleotide (must be full, with N and C-terminus)
        """
        ...
    
    def getFormula(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula()
        Returns the empirical formula of the residue
        """
        ...
    
    def setAvgMass(self, avg_mass: float ) -> None:
        """
        Cython signature: void setAvgMass(double avg_mass)
        Sets average mass of the ribonucleotide
        """
        ...
    
    def getAvgMass(self) -> float:
        """
        Cython signature: double getAvgMass()
        Returns average mass of the ribonucleotide
        """
        ...
    
    def setMonoMass(self, mono_mass: float ) -> None:
        """
        Cython signature: void setMonoMass(double mono_mass)
        Sets monoisotopic mass of the ribonucleotide
        """
        ...
    
    def getMonoMass(self) -> float:
        """
        Cython signature: double getMonoMass()
        Returns monoisotopic mass of the ribonucleotide
        """
        ...
    
    def getNewCode(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNewCode()
        Returns the new code
        """
        ...
    
    def setNewCode(self, code: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNewCode(String code)
        Sets the new code
        """
        ...
    
    def getOrigin(self) -> bytes:
        """
        Cython signature: char getOrigin()
        Returns the code of the unmodified base (e.g., "A", "C", ...)
        """
        ...
    
    def setOrigin(self, origin: bytes ) -> None:
        """
        Cython signature: void setOrigin(char origin)
        Sets the code of the unmodified base (e.g., "A", "C", ...)
        """
        ...
    
    def setHTMLCode(self, html_code: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setHTMLCode(String html_code)
        Sets the HTML (RNAMods) code
        """
        ...
    
    def getHTMLCode(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getHTMLCode()
        Returns the HTML (RNAMods) code
        """
        ...
    
    def setTermSpecificity(self, term_spec: int ) -> None:
        """
        Cython signature: void setTermSpecificity(TermSpecificityNuc term_spec)
        Sets the terminal specificity
        """
        ...
    
    def getTermSpecificity(self) -> int:
        """
        Cython signature: TermSpecificityNuc getTermSpecificity()
        Returns the terminal specificity
        """
        ...
    
    def getBaselossFormula(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getBaselossFormula()
        Returns sum formula after loss of the nucleobase
        """
        ...
    
    def setBaselossFormula(self, formula: EmpiricalFormula ) -> None:
        """
        Cython signature: void setBaselossFormula(EmpiricalFormula formula)
        Sets sum formula after loss of the nucleobase
        """
        ...
    
    def isModified(self) -> bool:
        """
        Cython signature: bool isModified()
        True if the ribonucleotide is a modified one
        """
        ...
    
    def __richcmp__(self, other: Ribonucleotide, op: int) -> Any:
        ... 


class Seed:
    """
    Cython implementation of _Seed

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::FeatureFinderAlgorithmPickedHelperStructs_1_1Seed.html>`_
    """
    
    spectrum: int
    
    peak: int
    
    intensity: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Seed()
        """
        ...
    
    @overload
    def __init__(self, in_0: Seed ) -> None:
        """
        Cython signature: void Seed(Seed &)
        """
        ...
    
    def __richcmp__(self, other: Seed, op: int) -> Any:
        ... 


class SimplePeak:
    """
    Cython implementation of _SimplePeak

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SimplePeak.html>`_
    """
    
    mz: float
    
    charge: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SimplePeak()
        A simple struct to represent peaks with mz and charge and sort them easily
        """
        ...
    
    @overload
    def __init__(self, mz: float , charge: int ) -> None:
        """
        Cython signature: void SimplePeak(double mz, int charge)
        """
        ...
    
    @overload
    def __init__(self, in_0: SimplePeak ) -> None:
        """
        Cython signature: void SimplePeak(SimplePeak &)
        """
        ... 


class SimpleTSGXLMS:
    """
    Cython implementation of _SimpleTSGXLMS

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SimpleTSGXLMS.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SimpleTSGXLMS()
        Generates theoretical spectra for cross-linked peptides
        
        The spectra this class generates are vectors of SimplePeaks
        This class generates the same peak types as TheoreticalSpectrumGeneratorXLMS
        and the interface is very similar, but it is simpler and faster
        SimplePeak only contains an mz value and a charge. No intensity values
        or String annotations or other additional DataArrays are generated
        """
        ...
    
    @overload
    def __init__(self, in_0: SimpleTSGXLMS ) -> None:
        """
        Cython signature: void SimpleTSGXLMS(SimpleTSGXLMS &)
        """
        ...
    
    def getLinearIonSpectrum(self, spectrum: List[SimplePeak] , peptide: AASequence , link_pos: int , charge: int , link_pos_2: int ) -> None:
        """
        Cython signature: void getLinearIonSpectrum(libcpp_vector[SimplePeak] & spectrum, AASequence peptide, size_t link_pos, int charge, size_t link_pos_2)
        Generates fragment ions not containing the cross-linker for one peptide
        
        B-ions are generated from the beginning of the peptide up to the first linked position,
        y-ions are generated from the second linked position up the end of the peptide
        If link_pos_2 is 0, a mono-link or cross-link is assumed and the second position is the same as the first position
        For a loop-link two different positions can be set and link_pos_2 must be larger than link_pos
        The generated ion types and other additional settings are determined by the tool parameters
        
        :param spectrum: The spectrum to which the new peaks are added. Does not have to be empty, the generated peaks will be pushed onto it
        :param peptide: The peptide to fragment
        :param link_pos: The position of the cross-linker on the given peptide
        :param charge: The maximal charge of the ions
        :param link_pos_2: A second position for the linker, in case it is a loop link
        """
        ...
    
    @overload
    def getXLinkIonSpectrum(self, spectrum: List[SimplePeak] , peptide: AASequence , link_pos: int , precursor_mass: float , mincharge: int , maxcharge: int , link_pos_2: int ) -> None:
        """
        Cython signature: void getXLinkIonSpectrum(libcpp_vector[SimplePeak] & spectrum, AASequence peptide, size_t link_pos, double precursor_mass, int mincharge, int maxcharge, size_t link_pos_2)
        Generates fragment ions containing the cross-linker for one peptide
        
        B-ions are generated from the first linked position up to the end of the peptide,
        y-ions are generated from the beginning of the peptide up to the second linked position
        If link_pos_2 is 0, a mono-link or cross-link is assumed and the second position is the same as the first position
        For a loop-link two different positions can be set and link_pos_2 must be larger than link_pos
        Since in the case of a cross-link a whole second peptide is attached to the other side of the cross-link,
        a precursor mass for the two peptides and the linker is needed
        In the case of a loop link the precursor mass is the mass of the only peptide and the linker
        Although this function is more general, currently it is mainly used for loop-links and mono-links,
        because residues in the second, unknown peptide cannot be considered for possible neutral losses
        The generated ion types and other additional settings are determined by the tool parameters
        
        :param spectrum: The spectrum to which the new peaks are added. Does not have to be empty, the generated peaks will be pushed onto it
        :param peptide: The peptide to fragment
        :param link_pos: The position of the cross-linker on the given peptide
        :param precursor_mass: The mass of the whole cross-link candidate or the precursor mass of the experimental MS2 spectrum
        :param mincharge: The minimal charge of the ions
        :param maxcharge: The maximal charge of the ions, it should be the precursor charge and is used to generate precursor ion peaks
        :param link_pos_2: A second position for the linker, in case it is a loop link
        """
        ...
    
    @overload
    def getXLinkIonSpectrum(self, spectrum: List[SimplePeak] , crosslink: ProteinProteinCrossLink , frag_alpha: bool , mincharge: int , maxcharge: int ) -> None:
        """
        Cython signature: void getXLinkIonSpectrum(libcpp_vector[SimplePeak] & spectrum, ProteinProteinCrossLink crosslink, bool frag_alpha, int mincharge, int maxcharge)
        Generates fragment ions containing the cross-linker for a pair of peptides
        
        B-ions are generated from the first linked position up to the end of the peptide,
        y-ions are generated from the beginning of the peptide up to the second linked position
        This function generates neutral loss ions by considering both linked peptides
        Only one of the peptides, decided by @frag_alpha, is fragmented
        This simplifies the function, but it has to be called twice to get all fragments of a peptide pair
        The generated ion types and other additional settings are determined by the tool parameters
        This function is not suitable to generate fragments for mono-links or loop-links
        
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


class SpectraMerger:
    """
    Cython implementation of _SpectraMerger

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectraMerger.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectraMerger()
        Merges blocks of MS or MS2 spectra
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectraMerger ) -> None:
        """
        Cython signature: void SpectraMerger(SpectraMerger &)
        """
        ...
    
    def mergeSpectraBlockWise(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void mergeSpectraBlockWise(MSExperiment & exp)
        """
        ...
    
    def mergeSpectraPrecursors(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void mergeSpectraPrecursors(MSExperiment & exp)
        Merges spectra with similar precursors (must have MS2 level)
        """
        ...
    
    def average(self, exp: MSExperiment , average_type: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void average(MSExperiment & exp, String average_type)
        Average over neighbouring spectra
        
        :param exp: Experimental data to be averaged
        :param average_type: Averaging type to be used ("gaussian" or "tophat")
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


class SpectrumAlignmentScore:
    """
    Cython implementation of _SpectrumAlignmentScore

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumAlignmentScore.html>`_
      -- Inherits from ['DefaultParamHandler']

    Similarity score via spectra alignment
    
    This class implements a simple scoring based on the alignment of spectra. This alignment
    is implemented in the SpectrumAlignment class and performs a dynamic programming alignment
    of the peaks, minimizing the distances between the aligned peaks and maximizing the number
    of peak pairs
    
    The scoring is done via the simple formula score = sum / (sqrt(sum1 * sum2)). sum is the
    product of the intensities of the aligned peaks, with the given exponent (default is 2)
    sum1 and sum2 are the sum of the intensities squared for each peak of both spectra respectively
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumAlignmentScore()
        Similarity score via spectra alignment
        
        This class implements a simple scoring based on the alignment of spectra. This alignment
        is implemented in the SpectrumAlignment class and performs a dynamic programming alignment
        of the peaks, minimizing the distances between the aligned peaks and maximizing the number
        of peak pairs
        
        The scoring is done via the simple formula score = sum / (sqrt(sum1 * sum2)). sum is the
        product of the intensities of the aligned peaks, with the given exponent (default is 2)
        sum1 and sum2 are the sum of the intensities squared for each peak of both spectra respectively
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAlignmentScore ) -> None:
        """
        Cython signature: void SpectrumAlignmentScore(SpectrumAlignmentScore &)
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


class TMTTenPlexQuantitationMethod:
    """
    Cython implementation of _TMTTenPlexQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TMTTenPlexQuantitationMethod.html>`_
      -- Inherits from ['IsobaricQuantitationMethod']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TMTTenPlexQuantitationMethod()
        """
        ...
    
    @overload
    def __init__(self, in_0: TMTTenPlexQuantitationMethod ) -> None:
        """
        Cython signature: void TMTTenPlexQuantitationMethod(TMTTenPlexQuantitationMethod &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        """
        ...
    
    def getChannelInformation(self) -> List[IsobaricChannelInformation]:
        """
        Cython signature: libcpp_vector[IsobaricChannelInformation] getChannelInformation()
        """
        ...
    
    def getNumberOfChannels(self) -> int:
        """
        Cython signature: size_t getNumberOfChannels()
        """
        ...
    
    def getIsotopeCorrectionMatrix(self) -> MatrixDouble:
        """
        Cython signature: MatrixDouble getIsotopeCorrectionMatrix()
        """
        ...
    
    def getReferenceChannel(self) -> int:
        """
        Cython signature: size_t getReferenceChannel()
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
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
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


class TheoreticalIsotopePattern:
    """
    Cython implementation of _TheoreticalIsotopePattern

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::FeatureFinderAlgorithmPickedHelperStructs_1_1TheoreticalIsotopePattern.html>`_
    """
    
    intensity: List[float]
    
    optional_begin: int
    
    optional_end: int
    
    max: float
    
    trimmed_left: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TheoreticalIsotopePattern()
        """
        ...
    
    @overload
    def __init__(self, in_0: TheoreticalIsotopePattern ) -> None:
        """
        Cython signature: void TheoreticalIsotopePattern(TheoreticalIsotopePattern &)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
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


class XLPrecursor:
    """
    Cython implementation of _XLPrecursor

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1XLPrecursor.html>`_
    """
    
    precursor_mass: float
    
    alpha_index: int
    
    beta_index: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void XLPrecursor()
        """
        ...
    
    @overload
    def __init__(self, in_0: XLPrecursor ) -> None:
        """
        Cython signature: void XLPrecursor(XLPrecursor &)
        """
        ... 


class __InletType:
    None
    INLETNULL : int
    DIRECT : int
    BATCH : int
    CHROMATOGRAPHY : int
    PARTICLEBEAM : int
    MEMBRANESEPARATOR : int
    OPENSPLIT : int
    JETSEPARATOR : int
    SEPTUM : int
    RESERVOIR : int
    MOVINGBELT : int
    MOVINGWIRE : int
    FLOWINJECTIONANALYSIS : int
    ELECTROSPRAYINLET : int
    THERMOSPRAYINLET : int
    INFUSION : int
    CONTINUOUSFLOWFASTATOMBOMBARDMENT : int
    INDUCTIVELYCOUPLEDPLASMA : int
    MEMBRANE : int
    NANOSPRAY : int
    SIZE_OF_INLETTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class IonOpticsType:
    None
    UNKNOWN : int
    MAGNETIC_DEFLECTION : int
    DELAYED_EXTRACTION : int
    COLLISION_QUADRUPOLE : int
    SELECTED_ION_FLOW_TUBE : int
    TIME_LAG_FOCUSING : int
    REFLECTRON : int
    EINZEL_LENS : int
    FIRST_STABILITY_REGION : int
    FRINGING_FIELD : int
    KINETIC_ENERGY_ANALYZER : int
    STATIC_FIELD : int
    SIZE_OF_IONOPTICSTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __IonizationMethod:
    None
    IONMETHODNULL : int
    ESI : int
    EI : int
    CI : int
    FAB : int
    TSP : int
    LD : int
    FD : int
    FI : int
    PD : int
    SI : int
    TI : int
    API : int
    ISI : int
    CID : int
    CAD : int
    HN : int
    APCI : int
    APPI : int
    ICP : int
    NESI : int
    MESI : int
    SELDI : int
    SEND : int
    FIB : int
    MALDI : int
    MPI : int
    DI : int
    FA : int
    FII : int
    GD_MS : int
    NICI : int
    NRMS : int
    PI : int
    PYMS : int
    REMPI : int
    AI : int
    ASI : int
    AD : int
    AUI : int
    CEI : int
    CHEMI : int
    DISSI : int
    LSI : int
    PEI : int
    SOI : int
    SPI : int
    SUI : int
    VI : int
    AP_MALDI : int
    SILI : int
    SALDI : int
    SIZE_OF_IONIZATIONMETHOD : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class MT_QUANTMETHOD:
    None
    MT_QUANT_AREA : int
    MT_QUANT_MEDIAN : int
    SIZE_OF_MT_QUANTMETHOD : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __Polarity:
    None
    POLNULL : int
    POSITIVE : int
    NEGATIVE : int
    SIZE_OF_POLARITY : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class SIDE:
    None
    LEFT : int
    RIGHT : int
    BOTH : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __Sorted:
    None
    INTENSITY : int
    MASS : int
    UNDEFINED : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class TermSpecificityNuc:
    None
    ANYWHERE : int
    FIVE_PRIME : int
    THREE_PRIME : int
    NUMBER_OF_TERM_SPECIFICITY : int

    def getMapping(self) -> Dict[int, str]:
       ... 

