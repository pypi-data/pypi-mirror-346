from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_FeatureMapping_assignMS2IndexToFeature(spectra: MSExperiment , fm_info: FeatureMapping_FeatureMappingInfo , precursor_mz_tolerance: float , precursor_rt_tolerance: float , ppm: bool ) -> FeatureMapping_FeatureToMs2Indices:
    """
    Cython signature: FeatureMapping_FeatureToMs2Indices assignMS2IndexToFeature(MSExperiment & spectra, FeatureMapping_FeatureMappingInfo & fm_info, double precursor_mz_tolerance, double precursor_rt_tolerance, bool ppm)
    """
    ...

def __static_MetaboliteSpectralMatching_computeHyperScore(fragment_mass_error: float , fragment_mass_tolerance_unit_ppm: bool , exp_spectrum: MSSpectrum , db_spectrum: MSSpectrum , annotations: List[PeptideHit_PeakAnnotation] , mz_lower_bound: float ) -> float:
    """
    Cython signature: double computeHyperScore(double fragment_mass_error, bool fragment_mass_tolerance_unit_ppm, MSSpectrum exp_spectrum, MSSpectrum db_spectrum, libcpp_vector[PeptideHit_PeakAnnotation] & annotations, double mz_lower_bound)
    """
    ...

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

def __static_OpenMSBuildInfo_setOpenMPNumThreads(num_threads: int ) -> None:
    """
    Cython signature: void setOpenMPNumThreads(int num_threads)
    """
    ...


class AMSE_AdductInfo:
    """
    Cython implementation of _AMSE_AdductInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AMSE_AdductInfo.html>`_
    """
    
    def __init__(self, name: Union[bytes, str, String] , adduct: EmpiricalFormula , charge: int , mol_multiplier: int ) -> None:
        """
        Cython signature: void AMSE_AdductInfo(const String & name, EmpiricalFormula & adduct, int charge, unsigned int mol_multiplier)
        """
        ...
    
    def getNeutralMass(self, observed_mz: float ) -> float:
        """
        Cython signature: double getNeutralMass(double observed_mz)
        """
        ...
    
    def getMZ(self, neutral_mass: float ) -> float:
        """
        Cython signature: double getMZ(double neutral_mass)
        """
        ...
    
    def isCompatible(self, db_entry: EmpiricalFormula ) -> bool:
        """
        Cython signature: bool isCompatible(EmpiricalFormula db_entry)
        """
        ...
    
    def getCharge(self) -> int:
        """
        Cython signature: int getCharge()
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
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


class BayesianProteinInferenceAlgorithm:
    """
    Cython implementation of _BayesianProteinInferenceAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1BayesianProteinInferenceAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']

    Performs a Bayesian protein inference on Protein/Peptide identifications or ConsensusMap.
    
    - Filters for best n PSMs per spectrum.
    - Calculates and filters for best peptide per spectrum.
    - Builds a k-partite graph from the structures.
    - Finds and splits into connected components by DFS
    - Extends the graph by adding layers from indist. protein groups, peptides with the same parents and optionally
      some additional layers (peptide sequence, charge, replicate -> extended model = experimental)
    - Builds a factor graph representation of a Bayesian network using the Evergreen library
      See model param section. It is based on the Fido noisy-OR model with an option for
      regularizing the number of proteins per peptide.
    - Performs loopy belief propagation on the graph and queries protein, protein group and/or peptide posteriors
      See loopy_belief_propagation param section.
    - Learns best parameters via grid search if the parameters were not given in the param section.
    - Writes posteriors to peptides and/or proteins and adds indistinguishable protein groups to the underlying
      data structures.
    - Can make use of OpenMP to parallelize over connected components.
    
    Usage:
    
    .. code-block:: python
    
      from pyopenms import *
      from urllib.request import urlretrieve
      urlretrieve("https://raw.githubusercontent.com/OpenMS/OpenMS/develop/src/tests/class_tests/openms/data/BayesianProteinInference_test.idXML", "BayesianProteinInference_test.idXML")
      proteins = []
      peptides = []
      idf = IdXMLFile()
      idf.load("BayesianProteinInference_test.idXML", proteins, peptides)
      bpia = BayesianProteinInferenceAlgorithm()
      p = bpia.getParameters()
      p.setValue("update_PSM_probabilities", "false")
      bpia.setParameters(p)
      bpia.inferPosteriorProbabilities(proteins, peptides)
      #
      print(len(peptides)) # 9
      print(peptides[0].getHits()[0].getScore()) # 0.6
      print(proteins[0].getHits()[0].getScore()) # 0.624641
      print(proteins[0].getHits()[1].getScore()) # 0.648346
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void BayesianProteinInferenceAlgorithm()
        """
        ...
    
    @overload
    def __init__(self, debug_lvl: int ) -> None:
        """
        Cython signature: void BayesianProteinInferenceAlgorithm(unsigned int debug_lvl)
        """
        ...
    
    @overload
    def inferPosteriorProbabilities(self, proteinIDs: List[ProteinIdentification] , peptideIDs: List[PeptideIdentification] , greedy_group_resolution: bool ) -> None:
        """
        Cython signature: void inferPosteriorProbabilities(libcpp_vector[ProteinIdentification] & proteinIDs, libcpp_vector[PeptideIdentification] & peptideIDs, bool greedy_group_resolution)
        Optionally adds indistinguishable protein groups with separate scores, too
        Currently only takes first proteinID run and all peptides
        
        
        :param proteinIDs: Vector of protein identifications
        :param peptideIDs: Vector of peptide identifications
        :return: Writes its results into protein and (optionally also) peptide hits (as new score)
        """
        ...
    
    @overload
    def inferPosteriorProbabilities(self, proteinIDs: List[ProteinIdentification] , peptideIDs: List[PeptideIdentification] , greedy_group_resolution: bool , exp_des: ExperimentalDesign ) -> None:
        """
        Cython signature: void inferPosteriorProbabilities(libcpp_vector[ProteinIdentification] & proteinIDs, libcpp_vector[PeptideIdentification] & peptideIDs, bool greedy_group_resolution, ExperimentalDesign exp_des)
        Writes its results into protein and (optionally also) peptide hits (as new score).
        Optionally adds indistinguishable protein groups with separate scores, too
        Currently only takes first proteinID run and all peptides
        Experimental design can be used to create an extended graph with replicate information. (experimental)
        
        
        :param proteinIDs: Vector of protein identifications
        :param peptideIDs: Vector of peptide identifications
        :param exp_des: Experimental Design
        :return: Writes its results into protein and (optionally also) peptide hits (as new score)
        """
        ...
    
    @overload
    def inferPosteriorProbabilities(self, cmap: ConsensusMap , greedy_group_resolution: bool ) -> None:
        """
        Cython signature: void inferPosteriorProbabilities(ConsensusMap & cmap, bool greedy_group_resolution)
        Writes its results into protein and (optionally also) peptide hits (as new score)
        Optionally adds indistinguishable protein groups with separate scores, too
        Loops over all runs in the ConsensusMaps' protein IDs (experimental)
        
        
        :param cmap: ConsensusMaps with protein IDs
        :param greedy_group_resolution: Adds indistinguishable protein groups with separate scores
        :return: Writes its protein ID results into the ConsensusMap
        """
        ...
    
    @overload
    def inferPosteriorProbabilities(self, cmap: ConsensusMap , greedy_group_resolution: bool , exp_des: ExperimentalDesign ) -> None:
        """
        Cython signature: void inferPosteriorProbabilities(ConsensusMap & cmap, bool greedy_group_resolution, ExperimentalDesign exp_des)
        Writes its results into protein and (optionally also) peptide hits (as new score)
        Optionally adds indistinguishable protein groups with separate scores, too
        Loops over all runs in the ConsensusMaps' protein IDs (experimental)
        
        
        :param cmap: ConsensusMaps with protein IDs.
        :param greedy_group_resolution: Adds indistinguishable protein groups with separate scores
        :param exp_des: Experimental Design
        :return: Writes its protein ID results into the ConsensusMap
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


class CVTermListInterface:
    """
    Cython implementation of _CVTermListInterface

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVTermListInterface.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVTermListInterface()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVTermListInterface ) -> None:
        """
        Cython signature: void CVTermListInterface(CVTermListInterface &)
        """
        ...
    
    @overload
    def replaceCVTerms(self, cv_terms: Dict[bytes,List[CVTerm]] ) -> None:
        """
        Cython signature: void replaceCVTerms(libcpp_map[String,libcpp_vector[CVTerm]] & cv_terms)
        """
        ...
    
    @overload
    def replaceCVTerms(self, cv_terms: List[CVTerm] , accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void replaceCVTerms(libcpp_vector[CVTerm] & cv_terms, const String & accession)
        """
        ...
    
    def setCVTerms(self, terms: List[CVTerm] ) -> None:
        """
        Cython signature: void setCVTerms(libcpp_vector[CVTerm] & terms)
        """
        ...
    
    def replaceCVTerm(self, cv_term: CVTerm ) -> None:
        """
        Cython signature: void replaceCVTerm(CVTerm & cv_term)
        """
        ...
    
    def consumeCVTerms(self, cv_term_map: Dict[bytes,List[CVTerm]] ) -> None:
        """
        Cython signature: void consumeCVTerms(libcpp_map[String,libcpp_vector[CVTerm]] & cv_term_map)
        Merges the given map into the member map, no duplicate checking
        """
        ...
    
    def getCVTerms(self) -> Dict[bytes,List[CVTerm]]:
        """
        Cython signature: libcpp_map[String,libcpp_vector[CVTerm]] getCVTerms()
        """
        ...
    
    def addCVTerm(self, term: CVTerm ) -> None:
        """
        Cython signature: void addCVTerm(CVTerm & term)
        Adds a CV term
        """
        ...
    
    def hasCVTerm(self, accession: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasCVTerm(const String & accession)
        Checks whether the term has a value
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
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
    
    def __richcmp__(self, other: CVTermListInterface, op: int) -> Any:
        ... 


class ChannelInfo:
    """
    Cython implementation of _ChannelInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ChannelInfo.html>`_
    """
    
    description: bytes
    
    name: int
    
    id: int
    
    center: float
    
    active: bool 


class ChargedIndexSet:
    """
    Cython implementation of _ChargedIndexSet

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ChargedIndexSet.html>`_
    """
    
    charge: int
    
    def __init__(self) -> None:
        """
        Cython signature: void ChargedIndexSet()
        Index set with associated charge estimate
        """
        ... 


class ChromatogramExtractorAlgorithm:
    """
    Cython implementation of _ChromatogramExtractorAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ChromatogramExtractorAlgorithm.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ChromatogramExtractorAlgorithm()
        """
        ...
    
    @overload
    def __init__(self, in_0: ChromatogramExtractorAlgorithm ) -> None:
        """
        Cython signature: void ChromatogramExtractorAlgorithm(ChromatogramExtractorAlgorithm &)
        """
        ...
    
    def extractChromatograms(self, input: SpectrumAccessOpenMS , output: List[OSChromatogram] , extraction_coordinates: List[ExtractionCoordinates] , mz_extraction_window: float , ppm: bool , im_extraction_window: float , filter: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void extractChromatograms(shared_ptr[SpectrumAccessOpenMS] input, libcpp_vector[shared_ptr[OSChromatogram]] & output, libcpp_vector[ExtractionCoordinates] extraction_coordinates, double mz_extraction_window, bool ppm, double im_extraction_window, String filter)
          Extract chromatograms at the m/z and RT defined by the ExtractionCoordinates
        
        
        :param input: Input spectral map
        :param output: Output chromatograms (XICs)
        :param extraction_coordinates: Extracts around these coordinates (from
         rt_start to rt_end in seconds - extracts the whole chromatogram if
         rt_end - rt_start < 0).
        :param mz_extraction_window: Extracts a window of this size in m/z
          dimension in Th or ppm (e.g. a window of 50 ppm means an extraction of
          25 ppm on either side)
        :param ppm: Whether mz_extraction_window is in ppm or in Th
        :param filter: Which function to apply in m/z space (currently "tophat" only)
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


class ChromatogramPeak:
    """
    Cython implementation of _ChromatogramPeak

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ChromatogramPeak_1_1ChromatogramPeak.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ChromatogramPeak()
        A 1-dimensional raw data point or peak for chromatograms
        """
        ...
    
    @overload
    def __init__(self, in_0: ChromatogramPeak ) -> None:
        """
        Cython signature: void ChromatogramPeak(ChromatogramPeak &)
        """
        ...
    
    @overload
    def __init__(self, retention_time: DPosition1 , intensity: float ) -> None:
        """
        Cython signature: void ChromatogramPeak(DPosition1 retention_time, double intensity)
        """
        ...
    
    def getIntensity(self) -> float:
        """
        Cython signature: double getIntensity()
        Returns the intensity
        """
        ...
    
    def setIntensity(self, in_0: float ) -> None:
        """
        Cython signature: void setIntensity(double)
        Sets the intensity
        """
        ...
    
    def getPosition(self) -> DPosition1:
        """
        Cython signature: DPosition1 getPosition()
        """
        ...
    
    def setPosition(self, in_0: DPosition1 ) -> None:
        """
        Cython signature: void setPosition(DPosition1)
        """
        ...
    
    def getRT(self) -> float:
        """
        Cython signature: double getRT()
        Returns the retention time
        """
        ...
    
    def setRT(self, in_0: float ) -> None:
        """
        Cython signature: void setRT(double)
        Sets retention time
        """
        ...
    
    def getPos(self) -> float:
        """
        Cython signature: double getPos()
        Alias for getRT()
        """
        ...
    
    def setPos(self, in_0: float ) -> None:
        """
        Cython signature: void setPos(double)
        Alias for setRT()
        """
        ...
    
    def __richcmp__(self, other: ChromatogramPeak, op: int) -> Any:
        ... 


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


class ConsensusMapNormalizerAlgorithmQuantile:
    """
    Cython implementation of _ConsensusMapNormalizerAlgorithmQuantile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusMapNormalizerAlgorithmQuantile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusMapNormalizerAlgorithmQuantile()
        """
        ...
    
    def normalizeMaps(self, input_map: ConsensusMap ) -> None:
        """
        Cython signature: void normalizeMaps(ConsensusMap & input_map)
        """
        ...
    
    def resample(self, data_in: List[float] , data_out: List[float] , n_resampling_points: int ) -> None:
        """
        Cython signature: void resample(libcpp_vector[double] & data_in, libcpp_vector[double] & data_out, unsigned int n_resampling_points)
        Resamples data_in and writes the results to data_out
        """
        ...
    
    def extractIntensityVectors(self, map_: ConsensusMap , out_intensities: List[List[float]] ) -> None:
        """
        Cython signature: void extractIntensityVectors(ConsensusMap & map_, libcpp_vector[libcpp_vector[double]] & out_intensities)
        Extracts the intensities of the features of the different maps
        """
        ...
    
    def setNormalizedIntensityValues(self, feature_ints: List[List[float]] , map_: ConsensusMap ) -> None:
        """
        Cython signature: void setNormalizedIntensityValues(libcpp_vector[libcpp_vector[double]] & feature_ints, ConsensusMap & map_)
        Writes the intensity values in feature_ints to the corresponding features in map
        """
        ... 


class CubicSpline2d:
    """
    Cython implementation of _CubicSpline2d

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CubicSpline2d.html>`_
    """
    
    @overload
    def __init__(self, x: List[float] , y: List[float] ) -> None:
        """
        Cython signature: void CubicSpline2d(libcpp_vector[double] x, libcpp_vector[double] y)
        """
        ...
    
    @overload
    def __init__(self, in_0: CubicSpline2d ) -> None:
        """
        Cython signature: void CubicSpline2d(CubicSpline2d &)
        """
        ...
    
    @overload
    def __init__(self, m: Dict[float, float] ) -> None:
        """
        Cython signature: void CubicSpline2d(libcpp_map[double,double] m)
        """
        ...
    
    def eval(self, x: float ) -> float:
        """
        Cython signature: double eval(double x)
        Evaluates the cubic spline
        """
        ...
    
    def derivatives(self, x: float , order: int ) -> float:
        """
        Cython signature: double derivatives(double x, unsigned int order)
        Returns first, second or third derivative of cubic spline
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


class DigestionEnzymeProtein:
    """
    Cython implementation of _DigestionEnzymeProtein

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DigestionEnzymeProtein.html>`_
      -- Inherits from ['DigestionEnzyme']

    Representation of a digestion enzyme for proteins (protease)
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DigestionEnzymeProtein()
        """
        ...
    
    @overload
    def __init__(self, in_0: DigestionEnzymeProtein ) -> None:
        """
        Cython signature: void DigestionEnzymeProtein(DigestionEnzymeProtein &)
        """
        ...
    
    @overload
    def __init__(self, name: Union[bytes, str, String] , cleavage_regex: Union[bytes, str, String] , synonyms: Set[bytes] , regex_description: Union[bytes, str, String] , n_term_gain: EmpiricalFormula , c_term_gain: EmpiricalFormula , psi_id: Union[bytes, str, String] , xtandem_id: Union[bytes, str, String] , comet_id: int , omssa_id: int ) -> None:
        """
        Cython signature: void DigestionEnzymeProtein(String name, String cleavage_regex, libcpp_set[String] synonyms, String regex_description, EmpiricalFormula n_term_gain, EmpiricalFormula c_term_gain, String psi_id, String xtandem_id, unsigned int comet_id, unsigned int omssa_id)
        """
        ...
    
    def setNTermGain(self, value: EmpiricalFormula ) -> None:
        """
        Cython signature: void setNTermGain(EmpiricalFormula value)
        Sets the N-term gain
        """
        ...
    
    def setCTermGain(self, value: EmpiricalFormula ) -> None:
        """
        Cython signature: void setCTermGain(EmpiricalFormula value)
        Sets the C-term gain
        """
        ...
    
    def getNTermGain(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getNTermGain()
        Returns the N-term gain
        """
        ...
    
    def getCTermGain(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getCTermGain()
        Returns the C-term gain
        """
        ...
    
    def setPSIID(self, value: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setPSIID(String value)
        Sets the PSI ID
        """
        ...
    
    def getPSIID(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getPSIID()
        Returns the PSI ID
        """
        ...
    
    def setXTandemID(self, value: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setXTandemID(String value)
        Sets the X! Tandem enzyme ID
        """
        ...
    
    def getXTandemID(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getXTandemID()
        Returns the X! Tandem enzyme ID
        """
        ...
    
    def setCometID(self, value: int ) -> None:
        """
        Cython signature: void setCometID(int value)
        Sets the Comet enzyme ID
        """
        ...
    
    def getCometID(self) -> int:
        """
        Cython signature: int getCometID()
        Returns the Comet enzyme ID
        """
        ...
    
    def setOMSSAID(self, value: int ) -> None:
        """
        Cython signature: void setOMSSAID(int value)
        Sets the OMSSA enzyme ID
        """
        ...
    
    def getOMSSAID(self) -> int:
        """
        Cython signature: int getOMSSAID()
        Returns the OMSSA enzyme ID
        """
        ...
    
    def setMSGFID(self, value: int ) -> None:
        """
        Cython signature: void setMSGFID(int value)
        Sets the MSGFPlus enzyme id
        """
        ...
    
    def getMSGFID(self) -> int:
        """
        Cython signature: int getMSGFID()
        Returns the MSGFPlus enzyme id
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
    
    def __richcmp__(self, other: DigestionEnzymeProtein, op: int) -> Any:
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


class EmgFitter1D:
    """
    Cython implementation of _EmgFitter1D

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1EmgFitter1D.html>`_
      -- Inherits from ['LevMarqFitter1D']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void EmgFitter1D()
        Exponentially modified gaussian distribution fitter (1-dim.) using Levenberg-Marquardt algorithm (Eigen implementation) for parameter optimization
        """
        ...
    
    @overload
    def __init__(self, in_0: EmgFitter1D ) -> None:
        """
        Cython signature: void EmgFitter1D(EmgFitter1D &)
        """
        ... 


class ExtractionCoordinates:
    """
    Cython implementation of _ExtractionCoordinates

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ExtractionCoordinates.html>`_
    """
    
    mz: float
    
    mz_precursor: float
    
    rt_start: float
    
    rt_end: float
    
    ion_mobility: float
    
    id: bytes
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ExtractionCoordinates()
        """
        ...
    
    @overload
    def __init__(self, in_0: ExtractionCoordinates ) -> None:
        """
        Cython signature: void ExtractionCoordinates(ExtractionCoordinates)
        """
        ... 


class FalseDiscoveryRate:
    """
    Cython implementation of _FalseDiscoveryRate

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FalseDiscoveryRate.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FalseDiscoveryRate()
        """
        ...
    
    @overload
    def apply(self, forward_ids: List[PeptideIdentification] , reverse_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & forward_ids, libcpp_vector[PeptideIdentification] & reverse_ids)
        """
        ...
    
    @overload
    def apply(self, id: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & id)
        """
        ...
    
    @overload
    def apply(self, forward_ids: List[ProteinIdentification] , reverse_ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void apply(libcpp_vector[ProteinIdentification] & forward_ids, libcpp_vector[ProteinIdentification] & reverse_ids)
        """
        ...
    
    @overload
    def apply(self, id: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void apply(libcpp_vector[ProteinIdentification] & id)
        """
        ...
    
    def applyEstimated(self, ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void applyEstimated(libcpp_vector[ProteinIdentification] & ids)
        """
        ...
    
    @overload
    def applyEvaluateProteinIDs(self, ids: List[ProteinIdentification] , pepCutoff: float , fpCutoff: int , diffWeight: float ) -> float:
        """
        Cython signature: double applyEvaluateProteinIDs(libcpp_vector[ProteinIdentification] & ids, double pepCutoff, unsigned int fpCutoff, double diffWeight)
        """
        ...
    
    @overload
    def applyEvaluateProteinIDs(self, ids: ProteinIdentification , pepCutoff: float , fpCutoff: int , diffWeight: float ) -> float:
        """
        Cython signature: double applyEvaluateProteinIDs(ProteinIdentification & ids, double pepCutoff, unsigned int fpCutoff, double diffWeight)
        """
        ...
    
    @overload
    def applyBasic(self, run_info: List[ProteinIdentification] , ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void applyBasic(libcpp_vector[ProteinIdentification] & run_info, libcpp_vector[PeptideIdentification] & ids)
        """
        ...
    
    @overload
    def applyBasic(self, ids: List[PeptideIdentification] , higher_score_better: bool , charge: int , identifier: Union[bytes, str, String] , only_best_per_pep: bool ) -> None:
        """
        Cython signature: void applyBasic(libcpp_vector[PeptideIdentification] & ids, bool higher_score_better, int charge, String identifier, bool only_best_per_pep)
        """
        ...
    
    @overload
    def applyBasic(self, cmap: ConsensusMap , use_unassigned_peptides: bool ) -> None:
        """
        Cython signature: void applyBasic(ConsensusMap & cmap, bool use_unassigned_peptides)
        """
        ...
    
    @overload
    def applyBasic(self, id: ProteinIdentification , groups_too: bool ) -> None:
        """
        Cython signature: void applyBasic(ProteinIdentification & id, bool groups_too)
        """
        ...
    
    def applyPickedProteinFDR(self, id: ProteinIdentification , decoy_string: String , decoy_prefix: bool , groups_too: bool ) -> None:
        """
        Cython signature: void applyPickedProteinFDR(ProteinIdentification & id, String & decoy_string, bool decoy_prefix, bool groups_too)
        """
        ...
    
    @overload
    def rocN(self, ids: List[PeptideIdentification] , fp_cutoff: int ) -> float:
        """
        Cython signature: double rocN(libcpp_vector[PeptideIdentification] & ids, size_t fp_cutoff)
        """
        ...
    
    @overload
    def rocN(self, ids: ConsensusMap , fp_cutoff: int , include_unassigned_peptides: bool ) -> float:
        """
        Cython signature: double rocN(ConsensusMap & ids, size_t fp_cutoff, bool include_unassigned_peptides)
        """
        ...
    
    @overload
    def rocN(self, ids: ConsensusMap , fp_cutoff: int , identifier: Union[bytes, str, String] , include_unassigned_peptides: bool ) -> float:
        """
        Cython signature: double rocN(ConsensusMap & ids, size_t fp_cutoff, const String & identifier, bool include_unassigned_peptides)
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


class Feature:
    """
    Cython implementation of _Feature

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Feature.html>`_
      -- Inherits from ['UniqueIdInterface', 'RichPeak2D']

    An LC-MS feature
    
    The Feature class is used to describe the two-dimensional signal caused by an
    analyte. It can store a charge state and a list of peptide identifications
    (for peptides). The area occupied by the Feature in the LC-MS data set is
    represented by a list of convex hulls (one for each isotopic peak). There is
    also a convex hull for the entire Feature. The model description can store
    the parameters of a two-dimensional theoretical model of the underlying
    signal in LC-MS. Currently, non-peptide compounds are also represented as
    features
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Feature()
        """
        ...
    
    @overload
    def __init__(self, in_0: Feature ) -> None:
        """
        Cython signature: void Feature(Feature &)
        """
        ...
    
    def getQuality(self, index: int ) -> float:
        """
        Cython signature: float getQuality(size_t index)
        Returns the quality in dimension c
        """
        ...
    
    def setQuality(self, index: int , q: float ) -> None:
        """
        Cython signature: void setQuality(size_t index, float q)
        Sets the quality in dimension c
        """
        ...
    
    def getOverallQuality(self) -> float:
        """
        Cython signature: float getOverallQuality()
        Model and quality methods
        """
        ...
    
    def setOverallQuality(self, q: float ) -> None:
        """
        Cython signature: void setOverallQuality(float q)
        Sets the overall quality
        """
        ...
    
    def getSubordinates(self) -> List[Feature]:
        """
        Cython signature: libcpp_vector[Feature] getSubordinates()
        Returns the subordinate features
        """
        ...
    
    def setSubordinates(self, in_0: List[Feature] ) -> None:
        """
        Cython signature: void setSubordinates(libcpp_vector[Feature])
        Returns the subordinate features
        """
        ...
    
    def encloses(self, rt: float , mz: float ) -> bool:
        """
        Cython signature: bool encloses(double rt, double mz)
        Returns if the mass trace convex hulls of the feature enclose the position specified by `rt` and `mz`
        
        
        :param rt: Sequence to digest
        :param mz: Digestion products
        """
        ...
    
    def getConvexHull(self) -> ConvexHull2D:
        """
        Cython signature: ConvexHull2D getConvexHull()
        """
        ...
    
    def getConvexHulls(self) -> List[ConvexHull2D]:
        """
        Cython signature: libcpp_vector[ConvexHull2D] getConvexHulls()
        """
        ...
    
    def setConvexHulls(self, in_0: List[ConvexHull2D] ) -> None:
        """
        Cython signature: void setConvexHulls(libcpp_vector[ConvexHull2D])
        """
        ...
    
    def getWidth(self) -> float:
        """
        Cython signature: float getWidth()
        """
        ...
    
    def setWidth(self, q: float ) -> None:
        """
        Cython signature: void setWidth(float q)
        """
        ...
    
    def getCharge(self) -> int:
        """
        Cython signature: int getCharge()
        """
        ...
    
    def setCharge(self, q: int ) -> None:
        """
        Cython signature: void setCharge(int q)
        """
        ...
    
    def getAnnotationState(self) -> int:
        """
        Cython signature: AnnotationState getAnnotationState()
        """
        ...
    
    def getPeptideIdentifications(self) -> List[PeptideIdentification]:
        """
        Cython signature: libcpp_vector[PeptideIdentification] getPeptideIdentifications()
        Returns a reference to the PeptideIdentification vector
        """
        ...
    
    def setPeptideIdentifications(self, peptides: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void setPeptideIdentifications(libcpp_vector[PeptideIdentification] & peptides)
        Sets the PeptideIdentification vector
        """
        ...
    
    def getUniqueId(self) -> int:
        """
        Cython signature: size_t getUniqueId()
        Returns the unique id
        """
        ...
    
    def clearUniqueId(self) -> int:
        """
        Cython signature: size_t clearUniqueId()
        Clear the unique id. The new unique id will be invalid. Returns 1 if the unique id was changed, 0 otherwise
        """
        ...
    
    def hasValidUniqueId(self) -> int:
        """
        Cython signature: size_t hasValidUniqueId()
        Returns whether the unique id is valid. Returns 1 if the unique id is valid, 0 otherwise
        """
        ...
    
    def hasInvalidUniqueId(self) -> int:
        """
        Cython signature: size_t hasInvalidUniqueId()
        Returns whether the unique id is invalid. Returns 1 if the unique id is invalid, 0 otherwise
        """
        ...
    
    def setUniqueId(self, rhs: int ) -> None:
        """
        Cython signature: void setUniqueId(uint64_t rhs)
        Assigns a new, valid unique id. Always returns 1
        """
        ...
    
    def ensureUniqueId(self) -> int:
        """
        Cython signature: size_t ensureUniqueId()
        Assigns a valid unique id, but only if the present one is invalid. Returns 1 if the unique id was changed, 0 otherwise
        """
        ...
    
    def isValid(self, unique_id: int ) -> bool:
        """
        Cython signature: bool isValid(uint64_t unique_id)
        Returns true if the unique_id is valid, false otherwise
        """
        ...
    
    def getIntensity(self) -> float:
        """
        Cython signature: float getIntensity()
        Returns the data point intensity (height)
        """
        ...
    
    def getMZ(self) -> float:
        """
        Cython signature: double getMZ()
        Returns the m/z coordinate (index 1)
        """
        ...
    
    def getRT(self) -> float:
        """
        Cython signature: double getRT()
        Returns the RT coordinate (index 0)
        """
        ...
    
    def setMZ(self, in_0: float ) -> None:
        """
        Cython signature: void setMZ(double)
        Returns the m/z coordinate (index 1)
        """
        ...
    
    def setRT(self, in_0: float ) -> None:
        """
        Cython signature: void setRT(double)
        Returns the RT coordinate (index 0)
        """
        ...
    
    def setIntensity(self, in_0: float ) -> None:
        """
        Cython signature: void setIntensity(float)
        Returns the data point intensity (height)
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
    
    def __richcmp__(self, other: Feature, op: int) -> Any:
        ... 


class FeatureDeconvolution:
    """
    Cython implementation of _FeatureDeconvolution

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureDeconvolution.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureDeconvolution()
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureDeconvolution ) -> None:
        """
        Cython signature: void FeatureDeconvolution(FeatureDeconvolution &)
        """
        ...
    
    def compute(self, input: FeatureMap , output: FeatureMap , cmap1: ConsensusMap , cmap2: ConsensusMap ) -> None:
        """
        Cython signature: void compute(FeatureMap & input, FeatureMap & output, ConsensusMap & cmap1, ConsensusMap & cmap2)
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
    CHARGEMODE_FD : __CHARGEMODE_FD 


class FeatureGroupingAlgorithmKD:
    """
    Cython implementation of _FeatureGroupingAlgorithmKD

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureGroupingAlgorithmKD.html>`_
      -- Inherits from ['FeatureGroupingAlgorithm', 'ProgressLogger']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureGroupingAlgorithmKD()
        A feature grouping algorithm for unlabeled data
        """
        ...
    
    @overload
    def group(self, maps: List[FeatureMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void group(libcpp_vector[FeatureMap] & maps, ConsensusMap & out)
        """
        ...
    
    @overload
    def group(self, maps: List[ConsensusMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void group(libcpp_vector[ConsensusMap] & maps, ConsensusMap & out)
        """
        ...
    
    def transferSubelements(self, maps: List[ConsensusMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void transferSubelements(libcpp_vector[ConsensusMap] maps, ConsensusMap & out)
        Transfers subelements (grouped features) from input consensus maps to the result consensus map
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


class FeatureGroupingAlgorithmQT:
    """
    Cython implementation of _FeatureGroupingAlgorithmQT

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureGroupingAlgorithmQT.html>`_
      -- Inherits from ['FeatureGroupingAlgorithm']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureGroupingAlgorithmQT()
        """
        ...
    
    @overload
    def group(self, maps: List[FeatureMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void group(libcpp_vector[FeatureMap] & maps, ConsensusMap & out)
        """
        ...
    
    @overload
    def group(self, maps: List[ConsensusMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void group(libcpp_vector[ConsensusMap] & maps, ConsensusMap & out)
        """
        ...
    
    def transferSubelements(self, maps: List[ConsensusMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void transferSubelements(libcpp_vector[ConsensusMap] maps, ConsensusMap & out)
        Transfers subelements (grouped features) from input consensus maps to the result consensus map
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


class FeatureMapping:
    """
    Cython implementation of _FeatureMapping

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureMapping.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureMapping()
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureMapping ) -> None:
        """
        Cython signature: void FeatureMapping(FeatureMapping &)
        """
        ...
    
    assignMS2IndexToFeature: __static_FeatureMapping_assignMS2IndexToFeature 


class FeatureMapping_FeatureMappingInfo:
    """
    Cython implementation of _FeatureMapping_FeatureMappingInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureMapping_FeatureMappingInfo.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureMapping_FeatureMappingInfo()
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureMapping_FeatureMappingInfo ) -> None:
        """
        Cython signature: void FeatureMapping_FeatureMappingInfo(FeatureMapping_FeatureMappingInfo &)
        """
        ... 


class FeatureMapping_FeatureToMs2Indices:
    """
    Cython implementation of _FeatureMapping_FeatureToMs2Indices

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureMapping_FeatureToMs2Indices.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureMapping_FeatureToMs2Indices()
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureMapping_FeatureToMs2Indices ) -> None:
        """
        Cython signature: void FeatureMapping_FeatureToMs2Indices(FeatureMapping_FeatureToMs2Indices &)
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


class GaussFilter:
    """
    Cython implementation of _GaussFilter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1GaussFilter.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void GaussFilter()
        This class represents a Gaussian lowpass-filter which works on uniform as well as on non-uniform profile data
        """
        ...
    
    @overload
    def __init__(self, in_0: GaussFilter ) -> None:
        """
        Cython signature: void GaussFilter(GaussFilter &)
        """
        ...
    
    @overload
    def filter(self, spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void filter(MSSpectrum & spectrum)
        Smoothes an MSSpectrum containing profile data
        """
        ...
    
    @overload
    def filter(self, chromatogram: MSChromatogram ) -> None:
        """
        Cython signature: void filter(MSChromatogram & chromatogram)
        """
        ...
    
    def filterExperiment(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void filterExperiment(MSExperiment & exp)
        Smoothes an MSExperiment containing profile data
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


class InspectOutfile:
    """
    Cython implementation of _InspectOutfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1InspectOutfile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void InspectOutfile()
        This class serves to read in an Inspect outfile and write an idXML file
        """
        ...
    
    @overload
    def __init__(self, in_0: InspectOutfile ) -> None:
        """
        Cython signature: void InspectOutfile(InspectOutfile &)
        """
        ...
    
    def load(self, result_filename: Union[bytes, str, String] , peptide_identifications: List[PeptideIdentification] , protein_identification: ProteinIdentification , p_value_threshold: float , database_filename: Union[bytes, str, String] ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] load(const String & result_filename, libcpp_vector[PeptideIdentification] & peptide_identifications, ProteinIdentification & protein_identification, double p_value_threshold, const String & database_filename)
        Load the results of an Inspect search
        
        
        :param result_filename: Input parameter which is the file name of the input file
        :param peptide_identifications: Output parameter which holds the peptide identifications from the given file
        :param protein_identification: Output parameter which holds the protein identifications from the given file
        :param p_value_threshold:
        :param database_filename:
        :raises:
          Exception: FileNotFound is thrown if the given file could not be found
        :raises:
          Exception: ParseError is thrown if the given file could not be parsed
        :raises:
          Exception: FileEmpty is thrown if the given file is empty
        """
        ...
    
    def getWantedRecords(self, result_filename: Union[bytes, str, String] , p_value_threshold: float ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] getWantedRecords(const String & result_filename, double p_value_threshold)
        Loads only results which exceeds a given p-value threshold
        
        
        :param result_filename: The filename of the results file
        :param p_value_threshold: Only identifications exceeding this threshold are read
        :raises:
          Exception: FileNotFound is thrown if the given file could not be found
        :raises:
          Exception: FileEmpty is thrown if the given file is empty
        """
        ...
    
    def compressTrieDB(self, database_filename: Union[bytes, str, String] , index_filename: Union[bytes, str, String] , wanted_records: List[int] , snd_database_filename: Union[bytes, str, String] , snd_index_filename: Union[bytes, str, String] , append: bool ) -> None:
        """
        Cython signature: void compressTrieDB(const String & database_filename, const String & index_filename, libcpp_vector[size_t] & wanted_records, const String & snd_database_filename, const String & snd_index_filename, bool append)
        Generates a trie database from another one, using the wanted records only
        """
        ...
    
    def generateTrieDB(self, source_database_filename: Union[bytes, str, String] , database_filename: Union[bytes, str, String] , index_filename: Union[bytes, str, String] , append: bool , species: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void generateTrieDB(const String & source_database_filename, const String & database_filename, const String & index_filename, bool append, const String species)
        Generates a trie database from a given one (the type of database is determined by getLabels)
        """
        ...
    
    def getACAndACType(self, line: Union[bytes, str, String] , accession: String , accession_type: String ) -> None:
        """
        Cython signature: void getACAndACType(String line, String & accession, String & accession_type)
        Retrieve the accession type and accession number from a protein description line
        """
        ...
    
    def getLabels(self, source_database_filename: Union[bytes, str, String] , ac_label: String , sequence_start_label: String , sequence_end_label: String , comment_label: String , species_label: String ) -> None:
        """
        Cython signature: void getLabels(const String & source_database_filename, String & ac_label, String & sequence_start_label, String & sequence_end_label, String & comment_label, String & species_label)
        Retrieve the labels of a given database (at the moment FASTA and Swissprot)
        """
        ...
    
    def getSequences(self, database_filename: Union[bytes, str, String] , wanted_records: Dict[int, int] , sequences: List[bytes] ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] getSequences(const String & database_filename, libcpp_map[size_t,size_t] & wanted_records, libcpp_vector[String] & sequences)
        Retrieve sequences from a trie database
        """
        ...
    
    def getExperiment(self, exp: MSExperiment , type_: String , in_filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void getExperiment(MSExperiment & exp, String & type_, const String & in_filename)
        Get the experiment from a file
        """
        ...
    
    def getSearchEngineAndVersion(self, cmd_output: Union[bytes, str, String] , protein_identification: ProteinIdentification ) -> bool:
        """
        Cython signature: bool getSearchEngineAndVersion(const String & cmd_output, ProteinIdentification & protein_identification)
        Get the search engine and its version from the output of the InsPecT executable without parameters. Returns true on success, false otherwise
        """
        ...
    
    def readOutHeader(self, filename: Union[bytes, str, String] , header_line: Union[bytes, str, String] , spectrum_file_column: int , scan_column: int , peptide_column: int , protein_column: int , charge_column: int , MQ_score_column: int , p_value_column: int , record_number_column: int , DB_file_pos_column: int , spec_file_pos_column: int , number_of_columns: int ) -> None:
        """
        Cython signature: void readOutHeader(const String & filename, const String & header_line, int & spectrum_file_column, int & scan_column, int & peptide_column, int & protein_column, int & charge_column, int & MQ_score_column, int & p_value_column, int & record_number_column, int & DB_file_pos_column, int & spec_file_pos_column, size_t & number_of_columns)
        Read the header of an inspect output file and retrieve various information
        """
        ...
    
    def __richcmp__(self, other: InspectOutfile, op: int) -> Any:
        ... 


class IntegerDataArray:
    """
    Cython implementation of _IntegerDataArray

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::DataArrays_1_1IntegerDataArray.html>`_
      -- Inherits from ['MetaInfoDescription']

    The representation of extra integer data attached to a spectrum or chromatogram.
    Raw data access is proved by `get_peaks` and `set_peaks`, which yields numpy arrays
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IntegerDataArray()
        """
        ...
    
    @overload
    def __init__(self, in_0: IntegerDataArray ) -> None:
        """
        Cython signature: void IntegerDataArray(IntegerDataArray &)
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
    
    def reserve(self, n: int ) -> None:
        """
        Cython signature: void reserve(size_t n)
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def push_back(self, in_0: int ) -> None:
        """
        Cython signature: void push_back(int)
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
    
    def __richcmp__(self, other: IntegerDataArray, op: int) -> Any:
        ... 


class Internal_MzMLValidator:
    """
    Cython implementation of _Internal_MzMLValidator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1Internal_MzMLValidator.html>`_
    """
    
    def __init__(self, mapping: CVMappings , cv: ControlledVocabulary ) -> None:
        """
        Cython signature: void Internal_MzMLValidator(CVMappings & mapping, ControlledVocabulary & cv)
        """
        ... 


class IsobaricChannelExtractor:
    """
    Cython implementation of _IsobaricChannelExtractor

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsobaricChannelExtractor.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, in_0: IsobaricChannelExtractor ) -> None:
        """
        Cython signature: void IsobaricChannelExtractor(IsobaricChannelExtractor &)
        """
        ...
    
    @overload
    def __init__(self, quant_method: ItraqEightPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricChannelExtractor(ItraqEightPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: ItraqFourPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricChannelExtractor(ItraqFourPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: TMTSixPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricChannelExtractor(TMTSixPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: TMTTenPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricChannelExtractor(TMTTenPlexQuantitationMethod * quant_method)
        """
        ...
    
    def extractChannels(self, ms_exp_data: MSExperiment , consensus_map: ConsensusMap ) -> None:
        """
        Cython signature: void extractChannels(MSExperiment & ms_exp_data, ConsensusMap & consensus_map)
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


class IsotopeCluster:
    """
    Cython implementation of _IsotopeCluster

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsotopeCluster.html>`_
    """
    
    peaks: ChargedIndexSet
    
    scans: List[int]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IsotopeCluster()
        Stores information about an isotopic cluster (i.e. potential peptide charge variants)
        """
        ...
    
    @overload
    def __init__(self, in_0: IsotopeCluster ) -> None:
        """
        Cython signature: void IsotopeCluster(IsotopeCluster &)
        """
        ... 


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


class IsotopeLabelingMDVs:
    """
    Cython implementation of _IsotopeLabelingMDVs

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsotopeLabelingMDVs.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IsotopeLabelingMDVs()
        """
        ...
    
    @overload
    def __init__(self, in_0: IsotopeLabelingMDVs ) -> None:
        """
        Cython signature: void IsotopeLabelingMDVs(IsotopeLabelingMDVs &)
        """
        ...
    
    def isotopicCorrection(self, normalized_feature: Feature , corrected_feature: Feature , correction_matrix: MatrixDouble , correction_matrix_agent: int ) -> None:
        """
        Cython signature: void isotopicCorrection(const Feature & normalized_feature, Feature & corrected_feature, MatrixDouble & correction_matrix, const DerivatizationAgent & correction_matrix_agent)
        This function performs an isotopic correction to account for unlabeled abundances coming from
        the derivatization agent (e.g., tBDMS) using correction matrix method and is calculated as follows:
        
        
        :param normalized_feature: Feature with normalized values for each component and unlabeled chemical formula for each component group
        :param correction_matrix: Square matrix holding correction factors derived either experimentally or theoretically which describe how spectral peaks of naturally abundant 13C contribute to spectral peaks that overlap (or convolve) the spectral peaks of the corrected MDV of the derivatization agent
        :param correction_matrix_agent: Name of the derivatization agent, the internally stored correction matrix if the name of the agent is supplied, only "TBDMS" is supported for now
        :return: corrected_feature: Feature with corrected values for each component
        """
        ...
    
    def isotopicCorrections(self, normalized_featureMap: FeatureMap , corrected_featureMap: FeatureMap , correction_matrix: MatrixDouble , correction_matrix_agent: int ) -> None:
        """
        Cython signature: void isotopicCorrections(const FeatureMap & normalized_featureMap, FeatureMap & corrected_featureMap, MatrixDouble & correction_matrix, const DerivatizationAgent & correction_matrix_agent)
        This function performs an isotopic correction to account for unlabeled abundances coming from
        the derivatization agent (e.g., tBDMS) using correction matrix method and is calculated as follows:
        
        
        :param normalized_featuremap: FeatureMap with normalized values for each component and unlabeled chemical formula for each component group
        :param correction_matrix: Square matrix holding correction factors derived either experimentally or theoretically which describe how spectral peaks of naturally abundant 13C contribute to spectral peaks that overlap (or convolve) the spectral peaks of the corrected MDV of the derivatization agent
        :param correction_matrix_agent: Name of the derivatization agent, the internally stored correction matrix if the name of the agent is supplied, only "TBDMS" is supported for now
        :return corrected_featuremap: FeatureMap with corrected values for each component
        """
        ...
    
    def calculateIsotopicPurity(self, normalized_feature: Feature , experiment_data: List[float] , isotopic_purity_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void calculateIsotopicPurity(const Feature & normalized_feature, const libcpp_vector[double] & experiment_data, const String & isotopic_purity_name)
        This function calculates the isotopic purity of the MDV using the following formula:
        isotopic purity of tracer (atom % 13C) = n / [n + (M + n-1)/(M + n)],
        where n in M+n is represented as the index of the result
        The formula is extracted from "High-resolution 13C metabolic flux analysis",
        Long et al, doi:10.1038/s41596-019-0204-0
        
        
        :param normalized_feature: Feature with normalized values for each component and the number of heavy labeled e.g., carbons. Out is a Feature with the calculated isotopic purity for the component group
        :param experiment_data: Vector of experiment data in percent
        :param isotopic_purity_name: Name of the isotopic purity tracer to be saved as a meta value
        """
        ...
    
    def calculateMDVAccuracy(self, normalized_feature: Feature , feature_name: Union[bytes, str, String] , fragment_isotopomer_theoretical_formula: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void calculateMDVAccuracy(const Feature & normalized_feature, const String & feature_name, const String & fragment_isotopomer_theoretical_formula)
        This function calculates the accuracy of the MDV as compared to the theoretical MDV (only for 12C quality control experiments)
        using average deviation to the mean. The result is mapped to the meta value "average_accuracy" in the updated feature
        
        
        :param normalized_feature: Feature with normalized values for each component and the chemical formula of the component group. Out is a Feature with the component group accuracy and accuracy for the error for each component
        :param fragment_isotopomer_measured: Measured scan values
        :param fragment_isotopomer_theoretical_formula: Empirical formula from which the theoretical values will be generated
        """
        ...
    
    def calculateMDVAccuracies(self, normalized_featureMap: FeatureMap , feature_name: Union[bytes, str, String] , fragment_isotopomer_theoretical_formulas: Dict[Union[bytes, str], Union[bytes, str]] ) -> None:
        """
        Cython signature: void calculateMDVAccuracies(const FeatureMap & normalized_featureMap, const String & feature_name, const libcpp_map[libcpp_utf8_string,libcpp_utf8_string] & fragment_isotopomer_theoretical_formulas)
        This function calculates the accuracy of the MDV as compared to the theoretical MDV (only for 12C quality control experiments)
        using average deviation to the mean
        
        
        param normalized_featuremap: FeatureMap with normalized values for each component and the chemical formula of the component group. Out is a FeatureMap with the component group accuracy and accuracy for the error for each component
        param fragment_isotopomer_measured: Measured scan values
        param fragment_isotopomer_theoretical_formula: A map of ProteinName/peptideRef to Empirical formula from which the theoretical values will be generated
        """
        ...
    
    def calculateMDV(self, measured_feature: Feature , normalized_feature: Feature , mass_intensity_type: int , feature_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void calculateMDV(const Feature & measured_feature, Feature & normalized_feature, const MassIntensityType & mass_intensity_type, const String & feature_name)
        """
        ...
    
    def calculateMDVs(self, measured_featureMap: FeatureMap , normalized_featureMap: FeatureMap , mass_intensity_type: int , feature_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void calculateMDVs(const FeatureMap & measured_featureMap, FeatureMap & normalized_featureMap, const MassIntensityType & mass_intensity_type, const String & feature_name)
        """
        ... 


class ItraqConstants:
    """
    Cython implementation of _ItraqConstants

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ItraqConstants.html>`_

    Some constants used throughout iTRAQ classes
    
    Constants for iTRAQ experiments and a ChannelInfo structure to store information about a single channel
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ItraqConstants()
        """
        ...
    
    @overload
    def __init__(self, in_0: ItraqConstants ) -> None:
        """
        Cython signature: void ItraqConstants(ItraqConstants &)
        """
        ...
    
    def getIsotopeMatrixAsStringList(self, itraq_type: int , isotope_corrections: List[MatrixDouble] ) -> List[bytes]:
        """
        Cython signature: StringList getIsotopeMatrixAsStringList(int itraq_type, libcpp_vector[MatrixDouble] & isotope_corrections)
        Convert isotope correction matrix to stringlist\n
        
        Each line is converted into a string of the format channel:-2Da/-1Da/+1Da/+2Da ; e.g. '114:0/0.3/4/0'
        Useful for creating parameters or debug output
        
        
        :param itraq_type: Which matrix to stringify. Should be of values from enum ITRAQ_TYPES
        :param isotope_corrections: Vector of the two matrices (4plex, 8plex)
        """
        ...
    
    def updateIsotopeMatrixFromStringList(self, itraq_type: int , channels: List[bytes] , isotope_corrections: List[MatrixDouble] ) -> None:
        """
        Cython signature: void updateIsotopeMatrixFromStringList(int itraq_type, StringList & channels, libcpp_vector[MatrixDouble] & isotope_corrections)
        Convert strings to isotope correction matrix rows\n
        
        Each string of format channel:-2Da/-1Da/+1Da/+2Da ; e.g. '114:0/0.3/4/0'
        is parsed and the corresponding channel(row) in the matrix is updated
        Not all channels need to be present, missing channels will be left untouched
        Useful to update the matrix with user isotope correction values
        
        
        :param itraq_type: Which matrix to stringify. Should be of values from enum ITRAQ_TYPES
        :param channels: New channel isotope values as strings
        :param isotope_corrections: Vector of the two matrices (4plex, 8plex)
        """
        ...
    
    def translateIsotopeMatrix(self, itraq_type: int , isotope_corrections: List[MatrixDouble] ) -> MatrixDouble:
        """
        Cython signature: MatrixDouble translateIsotopeMatrix(int & itraq_type, libcpp_vector[MatrixDouble] & isotope_corrections)
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


class MRMFeatureFilter:
    """
    Cython implementation of _MRMFeatureFilter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMFeatureFilter.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMFeatureFilter()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMFeatureFilter ) -> None:
        """
        Cython signature: void MRMFeatureFilter(MRMFeatureFilter &)
        """
        ...
    
    def FilterFeatureMap(self, features: FeatureMap , filter_criteria: MRMFeatureQC , transitions: TargetedExperiment ) -> None:
        """
        Cython signature: void FilterFeatureMap(FeatureMap features, MRMFeatureQC filter_criteria, TargetedExperiment transitions)
        Flags or filters features and subordinates in a FeatureMap
        
        
        :param features: FeatureMap to flag or filter
        :param filter_criteria: MRMFeatureQC class defining QC parameters
        :param transitions: Transitions from a TargetedExperiment
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


class MSDataStoringConsumer:
    """
    Cython implementation of _MSDataStoringConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSDataStoringConsumer.html>`_

    Consumer class that simply stores the data
    
    This class is able to keep spectra and chromatograms passed to it in memory
    and the data can be accessed through getData()
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MSDataStoringConsumer()
        """
        ...
    
    @overload
    def __init__(self, in_0: MSDataStoringConsumer ) -> None:
        """
        Cython signature: void MSDataStoringConsumer(MSDataStoringConsumer &)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings & exp)
        Sets experimental settings
        """
        ...
    
    def setExpectedSize(self, expectedSpectra: int , expectedChromatograms: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t expectedSpectra, size_t expectedChromatograms)
        Sets expected size
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
    
    def getData(self) -> MSExperiment:
        """
        Cython signature: MSExperiment getData()
        """
        ... 


class MapAlignmentTransformer:
    """
    Cython implementation of _MapAlignmentTransformer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MapAlignmentTransformer.html>`_

    This class collects functions for applying retention time transformations to data structures
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MapAlignmentTransformer()
        """
        ...
    
    @overload
    def __init__(self, in_0: MapAlignmentTransformer ) -> None:
        """
        Cython signature: void MapAlignmentTransformer(MapAlignmentTransformer &)
        """
        ...
    
    @overload
    def transformRetentionTimes(self, in_0: MSExperiment , in_1: TransformationDescription , in_2: bool ) -> None:
        """
        Cython signature: void transformRetentionTimes(MSExperiment &, TransformationDescription &, bool)
        Applies the given transformation to a peak map
        """
        ...
    
    @overload
    def transformRetentionTimes(self, in_0: FeatureMap , in_1: TransformationDescription , in_2: bool ) -> None:
        """
        Cython signature: void transformRetentionTimes(FeatureMap &, TransformationDescription &, bool)
        Applies the given transformation to a feature map
        """
        ...
    
    @overload
    def transformRetentionTimes(self, in_0: ConsensusMap , in_1: TransformationDescription , in_2: bool ) -> None:
        """
        Cython signature: void transformRetentionTimes(ConsensusMap &, TransformationDescription &, bool)
        Applies the given transformation to a consensus map
        """
        ...
    
    @overload
    def transformRetentionTimes(self, in_0: List[PeptideIdentification] , in_1: TransformationDescription , in_2: bool ) -> None:
        """
        Cython signature: void transformRetentionTimes(libcpp_vector[PeptideIdentification] &, TransformationDescription &, bool)
        Applies the given transformation to peptide identifications
        """
        ... 


class MassDecomposition:
    """
    Cython implementation of _MassDecomposition

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MassDecomposition.html>`_

    Class represents a decomposition of a mass into amino acids
    
    This class represents a mass decomposition into amino acids. A
    decomposition are amino acids given with frequencies which add
    up to a specific mass.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MassDecomposition()
        """
        ...
    
    @overload
    def __init__(self, in_0: MassDecomposition ) -> None:
        """
        Cython signature: void MassDecomposition(MassDecomposition &)
        """
        ...
    
    @overload
    def __init__(self, deco: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void MassDecomposition(const String & deco)
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the decomposition as a string
        """
        ...
    
    def toExpandedString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toExpandedString()
        Returns the decomposition as a string; instead of frequencies the amino acids are repeated
        """
        ...
    
    def getNumberOfMaxAA(self) -> int:
        """
        Cython signature: size_t getNumberOfMaxAA()
        Returns the max frequency of this composition
        """
        ...
    
    def containsTag(self, tag: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool containsTag(const String & tag)
        Returns true if tag is contained in the mass decomposition
        """
        ...
    
    def compatible(self, deco: MassDecomposition ) -> bool:
        """
        Cython signature: bool compatible(MassDecomposition & deco)
        Returns true if the mass decomposition if contained in this instance
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the decomposition as a string
        """
        ... 


class MetaboliteSpectralMatching:
    """
    Cython implementation of _MetaboliteSpectralMatching

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaboliteSpectralMatching.html>`_
      -- Inherits from ['ProgressLogger', 'DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaboliteSpectralMatching()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaboliteSpectralMatching ) -> None:
        """
        Cython signature: void MetaboliteSpectralMatching(MetaboliteSpectralMatching &)
        """
        ...
    
    def run(self, exp: MSExperiment , speclib: MSExperiment , mz_tab: MzTab , out_spectra: String ) -> None:
        """
        Cython signature: void run(MSExperiment & exp, MSExperiment & speclib, MzTab & mz_tab, String & out_spectra)
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
    
    computeHyperScore: __static_MetaboliteSpectralMatching_computeHyperScore 


class ModificationDefinition:
    """
    Cython implementation of _ModificationDefinition

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ModificationDefinition.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ModificationDefinition()
        """
        ...
    
    @overload
    def __init__(self, in_0: ModificationDefinition ) -> None:
        """
        Cython signature: void ModificationDefinition(ModificationDefinition &)
        """
        ...
    
    @overload
    def __init__(self, mod: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void ModificationDefinition(const String & mod)
        """
        ...
    
    @overload
    def __init__(self, mod: Union[bytes, str, String] , fixed: bool ) -> None:
        """
        Cython signature: void ModificationDefinition(const String & mod, bool fixed)
        """
        ...
    
    @overload
    def __init__(self, mod: Union[bytes, str, String] , fixed: bool , max_occur: int ) -> None:
        """
        Cython signature: void ModificationDefinition(const String & mod, bool fixed, unsigned int max_occur)
        """
        ...
    
    @overload
    def __init__(self, mod: ResidueModification ) -> None:
        """
        Cython signature: void ModificationDefinition(ResidueModification & mod)
        """
        ...
    
    @overload
    def __init__(self, mod: ResidueModification , fixed: bool ) -> None:
        """
        Cython signature: void ModificationDefinition(ResidueModification & mod, bool fixed)
        """
        ...
    
    @overload
    def __init__(self, mod: ResidueModification , fixed: bool , max_occur: int ) -> None:
        """
        Cython signature: void ModificationDefinition(ResidueModification & mod, bool fixed, unsigned int max_occur)
        """
        ...
    
    def setFixedModification(self, fixed: bool ) -> None:
        """
        Cython signature: void setFixedModification(bool fixed)
        Sets whether this modification definition is fixed or variable (modification must occur vs. can occur)
        """
        ...
    
    def isFixedModification(self) -> bool:
        """
        Cython signature: bool isFixedModification()
        Returns if the modification if fixed true, else false
        """
        ...
    
    def setMaxOccurrences(self, num: int ) -> None:
        """
        Cython signature: void setMaxOccurrences(unsigned int num)
        Sets the maximal number of occurrences per peptide (unbounded if 0)
        """
        ...
    
    def getMaxOccurrences(self) -> int:
        """
        Cython signature: unsigned int getMaxOccurrences()
        Returns the maximal number of occurrences per peptide
        """
        ...
    
    def getModificationName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getModificationName()
        Returns the name of the modification
        """
        ...
    
    def setModification(self, modification: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setModification(const String & modification)
        Sets the modification, allowed are unique names provided by ModificationsDB
        """
        ...
    
    def getModification(self) -> ResidueModification:
        """
        Cython signature: ResidueModification getModification()
        """
        ...
    
    def __richcmp__(self, other: ModificationDefinition, op: int) -> Any:
        ... 


class MorpheusScore:
    """
    Cython implementation of _MorpheusScore

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MorpheusScore.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MorpheusScore()
        """
        ...
    
    @overload
    def __init__(self, in_0: MorpheusScore ) -> None:
        """
        Cython signature: void MorpheusScore(MorpheusScore &)
        """
        ...
    
    def compute(self, fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool , exp_spectrum: MSSpectrum , theo_spectrum: MSSpectrum ) -> MorpheusScore_Result:
        """
        Cython signature: MorpheusScore_Result compute(double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm, const MSSpectrum & exp_spectrum, const MSSpectrum & theo_spectrum)
        Returns Morpheus Score
        """
        ... 


class MorpheusScore_Result:
    """
    Cython implementation of _MorpheusScore_Result

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MorpheusScore_Result.html>`_
    """
    
    matches: int
    
    n_peaks: int
    
    score: float
    
    MIC: float
    
    TIC: float
    
    err: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MorpheusScore_Result()
        """
        ...
    
    @overload
    def __init__(self, in_0: MorpheusScore_Result ) -> None:
        """
        Cython signature: void MorpheusScore_Result(MorpheusScore_Result &)
        """
        ... 


class MzTab:
    """
    Cython implementation of _MzTab

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzTab.html>`_

    Data model of MzTab files
    
    Please see the official MzTab specification at https://code.google.com/p/mztab/
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzTab()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzTab ) -> None:
        """
        Cython signature: void MzTab(MzTab &)
        """
        ... 


class MzXMLFile:
    """
    Cython implementation of _MzXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzXMLFile.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzXMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzXMLFile ) -> None:
        """
        Cython signature: void MzXMLFile(MzXMLFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , exp: MSExperiment ) -> None:
        """
        Cython signature: void load(String filename, MSExperiment & exp)
        Loads a MSExperiment from a MzXML file
        
        
        :param exp: MSExperiment
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , exp: MSExperiment ) -> None:
        """
        Cython signature: void store(String filename, MSExperiment & exp)
        Stores a MSExperiment in a MzXML file
        
        
        :param exp: MSExperiment
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


class OpenSwathOSWWriter:
    """
    Cython implementation of _OpenSwathOSWWriter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OpenSwathOSWWriter.html>`_
    """
    
    @overload
    def __init__(self, output_filename: Union[bytes, str, String] , run_id: int , input_filename: Union[bytes, str, String] , uis_scores: bool ) -> None:
        """
        Cython signature: void OpenSwathOSWWriter(String output_filename, uint64_t run_id, String input_filename, bool uis_scores)
        """
        ...
    
    @overload
    def __init__(self, in_0: OpenSwathOSWWriter ) -> None:
        """
        Cython signature: void OpenSwathOSWWriter(OpenSwathOSWWriter &)
        """
        ...
    
    def isActive(self) -> bool:
        """
        Cython signature: bool isActive()
        """
        ...
    
    def writeHeader(self) -> None:
        """
        Cython signature: void writeHeader()
        Initializes file by generating SQLite tables
        """
        ...
    
    def prepareLine(self, compound: LightCompound , tr: LightTransition , output: FeatureMap , id_: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String prepareLine(LightCompound & compound, LightTransition * tr, FeatureMap & output, String id_)
        Prepare a single line (feature) for output
        
        The result can be flushed to disk using writeLines (either line by line or after collecting several lines)
        
        
        :param pep: The compound (peptide/metabolite) used for extraction
        :param transition: The transition used for extraction
        :param output: The feature map containing all features (each feature will generate one entry in the output)
        :param id: The transition group identifier (peptide/metabolite id)
        :return: A String to be written using writeLines
        """
        ...
    
    def writeLines(self, to_osw_output: List[bytes] ) -> None:
        """
        Cython signature: void writeLines(libcpp_vector[String] to_osw_output)
        Write data to disk
        
        Takes a set of pre-prepared data statements from prepareLine and flushes them to disk
        
        
        :param to_osw_output: Statements generated by prepareLine
        """
        ... 


class ParamNode:
    """
    Cython implementation of _ParamNode

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Param_1_1ParamNode.html>`_
    """
    
    name: Union[bytes, str, String]
    
    description: Union[bytes, str, String]
    
    entries: List[ParamEntry]
    
    nodes: List[ParamNode]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ParamNode()
        """
        ...
    
    @overload
    def __init__(self, in_0: ParamNode ) -> None:
        """
        Cython signature: void ParamNode(ParamNode &)
        """
        ...
    
    @overload
    def __init__(self, n: Union[bytes, str, String] , d: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void ParamNode(const String & n, const String & d)
        """
        ...
    
    def findParentOf(self, name: Union[bytes, str, String] ) -> ParamNode:
        """
        Cython signature: ParamNode * findParentOf(const String & name)
        """
        ...
    
    def findEntryRecursive(self, name: Union[bytes, str, String] ) -> ParamEntry:
        """
        Cython signature: ParamEntry * findEntryRecursive(const String & name)
        """
        ...
    
    @overload
    def insert(self, node: ParamNode , prefix: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void insert(ParamNode & node, const String & prefix)
        """
        ...
    
    @overload
    def insert(self, entry: ParamEntry , prefix: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void insert(ParamEntry & entry, const String & prefix)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def suffix(self, key: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String suffix(const String & key)
        """
        ...
    
    def __richcmp__(self, other: ParamNode, op: int) -> Any:
        ... 


class ProteaseDB:
    """
    Cython implementation of _ProteaseDB

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteaseDB.html>`_
    """
    
    def getEnzyme(self, name: Union[bytes, str, String] ) -> DigestionEnzymeProtein:
        """
        Cython signature: const DigestionEnzymeProtein * getEnzyme(const String & name)
        """
        ...
    
    def getEnzymeByRegEx(self, cleavage_regex: Union[bytes, str, String] ) -> DigestionEnzymeProtein:
        """
        Cython signature: const DigestionEnzymeProtein * getEnzymeByRegEx(const String & cleavage_regex)
        """
        ...
    
    def getAllNames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllNames(libcpp_vector[String] & all_names)
        """
        ...
    
    def getAllXTandemNames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllXTandemNames(libcpp_vector[String] & all_names)
        Returns all the enzyme names available for XTandem
        """
        ...
    
    def getAllOMSSANames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllOMSSANames(libcpp_vector[String] & all_names)
        Returns all the enzyme names available for OMSSA
        """
        ...
    
    def getAllCometNames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllCometNames(libcpp_vector[String] & all_names)
        Returns all the enzyme names available for Comet
        """
        ...
    
    def getAllMSGFNames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllMSGFNames(libcpp_vector[String] & all_names)
        Returns all the enzyme names available for MSGFPlus
        """
        ...
    
    def hasEnzyme(self, name: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasEnzyme(const String & name)
        """
        ...
    
    def hasRegEx(self, cleavage_regex: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasRegEx(const String & cleavage_regex)
        """
        ... 


class SiriusMSFile:
    """
    Cython implementation of _SiriusMSFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SiriusMSFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SiriusMSFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: SiriusMSFile ) -> None:
        """
        Cython signature: void SiriusMSFile(SiriusMSFile &)
        """
        ... 


class SiriusMSFile_AccessionInfo:
    """
    Cython implementation of _SiriusMSFile_AccessionInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SiriusMSFile_AccessionInfo.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SiriusMSFile_AccessionInfo()
        """
        ...
    
    @overload
    def __init__(self, in_0: SiriusMSFile_AccessionInfo ) -> None:
        """
        Cython signature: void SiriusMSFile_AccessionInfo(SiriusMSFile_AccessionInfo &)
        """
        ... 


class SiriusMSFile_CompoundInfo:
    """
    Cython implementation of _SiriusMSFile_CompoundInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SiriusMSFile_CompoundInfo.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SiriusMSFile_CompoundInfo()
        """
        ...
    
    @overload
    def __init__(self, in_0: SiriusMSFile_CompoundInfo ) -> None:
        """
        Cython signature: void SiriusMSFile_CompoundInfo(SiriusMSFile_CompoundInfo &)
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


class SpectralMatch:
    """
    Cython implementation of _SpectralMatch

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectralMatch.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectralMatch()
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectralMatch ) -> None:
        """
        Cython signature: void SpectralMatch(SpectralMatch &)
        """
        ...
    
    def getObservedPrecursorMass(self) -> float:
        """
        Cython signature: double getObservedPrecursorMass()
        """
        ...
    
    def setObservedPrecursorMass(self, in_0: float ) -> None:
        """
        Cython signature: void setObservedPrecursorMass(double)
        """
        ...
    
    def getObservedPrecursorRT(self) -> float:
        """
        Cython signature: double getObservedPrecursorRT()
        """
        ...
    
    def setObservedPrecursorRT(self, in_0: float ) -> None:
        """
        Cython signature: void setObservedPrecursorRT(double)
        """
        ...
    
    def getFoundPrecursorMass(self) -> float:
        """
        Cython signature: double getFoundPrecursorMass()
        """
        ...
    
    def setFoundPrecursorMass(self, in_0: float ) -> None:
        """
        Cython signature: void setFoundPrecursorMass(double)
        """
        ...
    
    def getFoundPrecursorCharge(self) -> int:
        """
        Cython signature: int getFoundPrecursorCharge()
        """
        ...
    
    def setFoundPrecursorCharge(self, in_0: int ) -> None:
        """
        Cython signature: void setFoundPrecursorCharge(int)
        """
        ...
    
    def getMatchingScore(self) -> float:
        """
        Cython signature: double getMatchingScore()
        """
        ...
    
    def setMatchingScore(self, in_0: float ) -> None:
        """
        Cython signature: void setMatchingScore(double)
        """
        ...
    
    def getObservedSpectrumIndex(self) -> int:
        """
        Cython signature: size_t getObservedSpectrumIndex()
        """
        ...
    
    def setObservedSpectrumIndex(self, in_0: int ) -> None:
        """
        Cython signature: void setObservedSpectrumIndex(size_t)
        """
        ...
    
    def getMatchingSpectrumIndex(self) -> int:
        """
        Cython signature: size_t getMatchingSpectrumIndex()
        """
        ...
    
    def setMatchingSpectrumIndex(self, in_0: int ) -> None:
        """
        Cython signature: void setMatchingSpectrumIndex(size_t)
        """
        ...
    
    def getPrimaryIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getPrimaryIdentifier()
        """
        ...
    
    def setPrimaryIdentifier(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setPrimaryIdentifier(String)
        """
        ...
    
    def getSecondaryIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSecondaryIdentifier()
        """
        ...
    
    def setSecondaryIdentifier(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSecondaryIdentifier(String)
        """
        ...
    
    def getCommonName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCommonName()
        """
        ...
    
    def setCommonName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCommonName(String)
        """
        ...
    
    def getSumFormula(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSumFormula()
        """
        ...
    
    def setSumFormula(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSumFormula(String)
        """
        ...
    
    def getInchiString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getInchiString()
        """
        ...
    
    def setInchiString(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setInchiString(String)
        """
        ...
    
    def getSMILESString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSMILESString()
        """
        ...
    
    def setSMILESString(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSMILESString(String)
        """
        ...
    
    def getPrecursorAdduct(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getPrecursorAdduct()
        """
        ...
    
    def setPrecursorAdduct(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setPrecursorAdduct(String)
        """
        ... 


class SpectrumAccessOpenMSCached:
    """
    Cython implementation of _SpectrumAccessOpenMSCached

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumAccessOpenMSCached.html>`_
      -- Inherits from ['ISpectrumAccess']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSCached()
        """
        ...
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSCached(String filename)
        An implementation of the Spectrum Access interface using on-disk caching
        
        This class implements the OpenSWATH Spectrum Access interface
        (ISpectrumAccess) using the CachedmzML class which is able to read and
        write a cached mzML file
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMSCached ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSCached(SpectrumAccessOpenMSCached &)
        """
        ...
    
    def getSpectrumById(self, id_: int ) -> OSSpectrum:
        """
        Cython signature: shared_ptr[OSSpectrum] getSpectrumById(int id_)
        Returns a pointer to a spectrum at the given string id
        """
        ...
    
    def getSpectraByRT(self, RT: float , deltaRT: float ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] getSpectraByRT(double RT, double deltaRT)
        Returns a vector of ids of spectra that are within RT +/- deltaRT
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        Returns the number of spectra available
        """
        ...
    
    def getChromatogramById(self, id_: int ) -> OSChromatogram:
        """
        Cython signature: shared_ptr[OSChromatogram] getChromatogramById(int id_)
        Returns a pointer to a chromatogram at the given id
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        Returns the number of chromatograms available
        """
        ...
    
    def getChromatogramNativeID(self, id_: int ) -> str:
        """
        Cython signature: libcpp_utf8_output_string getChromatogramNativeID(int id_)
        """
        ... 


class SpectrumAccessOpenMSInMemory:
    """
    Cython implementation of _SpectrumAccessOpenMSInMemory

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumAccessOpenMSInMemory.html>`_
      -- Inherits from ['ISpectrumAccess']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSInMemory()
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMS ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSInMemory(SpectrumAccessOpenMS &)
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMSCached ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSInMemory(SpectrumAccessOpenMSCached &)
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMSInMemory ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSInMemory(SpectrumAccessOpenMSInMemory &)
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessQuadMZTransforming ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSInMemory(SpectrumAccessQuadMZTransforming &)
        """
        ...
    
    def getSpectrumById(self, id_: int ) -> OSSpectrum:
        """
        Cython signature: shared_ptr[OSSpectrum] getSpectrumById(int id_)
        Returns a pointer to a spectrum at the given string id
        """
        ...
    
    def getSpectraByRT(self, RT: float , deltaRT: float ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] getSpectraByRT(double RT, double deltaRT)
        Returns a vector of ids of spectra that are within RT +/- deltaRT
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        Returns the number of spectra available
        """
        ...
    
    def getChromatogramById(self, id_: int ) -> OSChromatogram:
        """
        Cython signature: shared_ptr[OSChromatogram] getChromatogramById(int id_)
        Returns a pointer to a chromatogram at the given id
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        Returns the number of chromatograms available
        """
        ...
    
    def getChromatogramNativeID(self, id_: int ) -> str:
        """
        Cython signature: libcpp_utf8_output_string getChromatogramNativeID(int id_)
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


class SqMassConfig:
    """
    Cython implementation of _SqMassConfig

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SqMassConfig.html>`_
    """
    
    write_full_meta: bool
    
    use_lossy_numpress: bool
    
    linear_fp_mass_acc: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SqMassConfig()
        """
        ...
    
    @overload
    def __init__(self, in_0: SqMassConfig ) -> None:
        """
        Cython signature: void SqMassConfig(SqMassConfig &)
        """
        ... 


class SqMassFile:
    """
    Cython implementation of _SqMassFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SqMassFile.html>`_

    An class that uses on-disk SQLite database to read and write spectra and chromatograms
    
    This class provides functions to read and write spectra and chromatograms
    to disk using a SQLite database and store them in sqMass format. This
    allows users to access, select and filter spectra and chromatograms
    on-demand even in a large collection of data
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SqMassFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: SqMassFile ) -> None:
        """
        Cython signature: void SqMassFile(SqMassFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , map_: MSExperiment ) -> None:
        """
        Cython signature: void load(const String & filename, MSExperiment & map_)
        Read / Write a complete mass spectrometric experiment
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , map_: MSExperiment ) -> None:
        """
        Cython signature: void store(const String & filename, MSExperiment & map_)
        Store an MSExperiment in sqMass format
        """
        ...
    
    def setConfig(self, config: SqMassConfig ) -> None:
        """
        Cython signature: void setConfig(SqMassConfig config)
        """
        ... 


class StablePairFinder:
    """
    Cython implementation of _StablePairFinder

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1StablePairFinder.html>`_
      -- Inherits from ['BaseGroupFinder']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void StablePairFinder()
        """
        ...
    
    def run(self, input_maps: List[ConsensusMap] , result_map: ConsensusMap ) -> None:
        """
        Cython signature: void run(libcpp_vector[ConsensusMap] & input_maps, ConsensusMap & result_map)
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


class TMTSixPlexQuantitationMethod:
    """
    Cython implementation of _TMTSixPlexQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TMTSixPlexQuantitationMethod.html>`_
      -- Inherits from ['IsobaricQuantitationMethod']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TMTSixPlexQuantitationMethod()
        """
        ...
    
    @overload
    def __init__(self, in_0: TMTSixPlexQuantitationMethod ) -> None:
        """
        Cython signature: void TMTSixPlexQuantitationMethod(TMTSixPlexQuantitationMethod &)
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


class TextFile:
    """
    Cython implementation of _TextFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TextFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TextFile()
        This class provides some basic file handling methods for text files
        """
        ...
    
    @overload
    def __init__(self, in_0: TextFile ) -> None:
        """
        Cython signature: void TextFile(TextFile &)
        """
        ...
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , trim_linesalse: bool , first_n1: int ) -> None:
        """
        Cython signature: void TextFile(const String & filename, bool trim_linesalse, int first_n1)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , trim_linesalse: bool , first_n1: int ) -> None:
        """
        Cython signature: void load(const String & filename, bool trim_linesalse, int first_n1)
        Loads data from a text file
        
        :param filename: The input file name
        :param trim_lines: Whether or not the lines are trimmed when reading them from file
        :param first_n: If set, only `first_n` lines the lines from the beginning of the file are read
        :param skip_empty_lines: Should empty lines be skipped? If used in conjunction with `trim_lines`, also lines with only whitespace will be skipped. Skipped lines do not count towards the total number of read lines
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(const String & filename)
        Writes the data to a file
        """
        ...
    
    def addLine(self, line: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addLine(const String line)
        """
        ... 


class TheoreticalSpectrumGenerator:
    """
    Cython implementation of _TheoreticalSpectrumGenerator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TheoreticalSpectrumGenerator.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TheoreticalSpectrumGenerator()
        """
        ...
    
    @overload
    def __init__(self, in_0: TheoreticalSpectrumGenerator ) -> None:
        """
        Cython signature: void TheoreticalSpectrumGenerator(TheoreticalSpectrumGenerator &)
        """
        ...
    
    def getSpectrum(self, spec: MSSpectrum , peptide: AASequence , min_charge: int , max_charge: int ) -> None:
        """
        Cython signature: void getSpectrum(MSSpectrum & spec, AASequence & peptide, int min_charge, int max_charge)
        Generates a spectrum for a peptide sequence, with the ion types that are set in the tool parameters. If precursor_charge is set to 0 max_charge + 1 will be used
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


class XTandemInfile:
    """
    Cython implementation of _XTandemInfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1XTandemInfile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void XTandemInfile()
        """
        ...
    
    def setFragmentMassTolerance(self, tolerance: float ) -> None:
        """
        Cython signature: void setFragmentMassTolerance(double tolerance)
        """
        ...
    
    def getFragmentMassTolerance(self) -> float:
        """
        Cython signature: double getFragmentMassTolerance()
        """
        ...
    
    def setPrecursorMassTolerancePlus(self, tol: float ) -> None:
        """
        Cython signature: void setPrecursorMassTolerancePlus(double tol)
        """
        ...
    
    def getPrecursorMassTolerancePlus(self) -> float:
        """
        Cython signature: double getPrecursorMassTolerancePlus()
        """
        ...
    
    def setPrecursorMassToleranceMinus(self, tol: float ) -> None:
        """
        Cython signature: void setPrecursorMassToleranceMinus(double tol)
        """
        ...
    
    def getPrecursorMassToleranceMinus(self) -> float:
        """
        Cython signature: double getPrecursorMassToleranceMinus()
        """
        ...
    
    def setPrecursorErrorType(self, mono_isotopic: int ) -> None:
        """
        Cython signature: void setPrecursorErrorType(MassType mono_isotopic)
        """
        ...
    
    def getPrecursorErrorType(self) -> int:
        """
        Cython signature: MassType getPrecursorErrorType()
        """
        ...
    
    def setFragmentMassErrorUnit(self, unit: int ) -> None:
        """
        Cython signature: void setFragmentMassErrorUnit(ErrorUnit unit)
        """
        ...
    
    def getFragmentMassErrorUnit(self) -> int:
        """
        Cython signature: ErrorUnit getFragmentMassErrorUnit()
        """
        ...
    
    def setPrecursorMassErrorUnit(self, unit: int ) -> None:
        """
        Cython signature: void setPrecursorMassErrorUnit(ErrorUnit unit)
        """
        ...
    
    def getPrecursorMassErrorUnit(self) -> int:
        """
        Cython signature: ErrorUnit getPrecursorMassErrorUnit()
        """
        ...
    
    def setNumberOfThreads(self, threads: int ) -> None:
        """
        Cython signature: void setNumberOfThreads(unsigned int threads)
        """
        ...
    
    def getNumberOfThreads(self) -> int:
        """
        Cython signature: unsigned int getNumberOfThreads()
        """
        ...
    
    def setModifications(self, mods: ModificationDefinitionsSet ) -> None:
        """
        Cython signature: void setModifications(ModificationDefinitionsSet & mods)
        """
        ...
    
    def getModifications(self) -> ModificationDefinitionsSet:
        """
        Cython signature: ModificationDefinitionsSet getModifications()
        """
        ...
    
    def setOutputFilename(self, output: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setOutputFilename(const String & output)
        """
        ...
    
    def getOutputFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOutputFilename()
        """
        ...
    
    def setInputFilename(self, input_file: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setInputFilename(const String & input_file)
        """
        ...
    
    def getInputFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getInputFilename()
        """
        ...
    
    def setTaxonomyFilename(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTaxonomyFilename(const String & filename)
        """
        ...
    
    def getTaxonomyFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTaxonomyFilename()
        """
        ...
    
    def setDefaultParametersFilename(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDefaultParametersFilename(const String & filename)
        """
        ...
    
    def getDefaultParametersFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getDefaultParametersFilename()
        """
        ...
    
    def setTaxon(self, taxon: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTaxon(const String & taxon)
        """
        ...
    
    def getTaxon(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTaxon()
        """
        ...
    
    def setMaxPrecursorCharge(self, max_charge: int ) -> None:
        """
        Cython signature: void setMaxPrecursorCharge(int max_charge)
        """
        ...
    
    def getMaxPrecursorCharge(self) -> int:
        """
        Cython signature: int getMaxPrecursorCharge()
        """
        ...
    
    def setNumberOfMissedCleavages(self, missed_cleavages: int ) -> None:
        """
        Cython signature: void setNumberOfMissedCleavages(unsigned int missed_cleavages)
        """
        ...
    
    def getNumberOfMissedCleavages(self) -> int:
        """
        Cython signature: unsigned int getNumberOfMissedCleavages()
        """
        ...
    
    def setOutputResults(self, result: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setOutputResults(String result)
        """
        ...
    
    def getOutputResults(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOutputResults()
        """
        ...
    
    def setMaxValidEValue(self, value: float ) -> None:
        """
        Cython signature: void setMaxValidEValue(double value)
        """
        ...
    
    def getMaxValidEValue(self) -> float:
        """
        Cython signature: double getMaxValidEValue()
        """
        ...
    
    def setSemiCleavage(self, semi_cleavage: bool ) -> None:
        """
        Cython signature: void setSemiCleavage(bool semi_cleavage)
        """
        ...
    
    def setAllowIsotopeError(self, allow_isotope_error: bool ) -> None:
        """
        Cython signature: void setAllowIsotopeError(bool allow_isotope_error)
        """
        ...
    
    def write(self, filename: Union[bytes, str, String] , ignore_member_parameters: bool , force_default_mods: bool ) -> None:
        """
        Cython signature: void write(String filename, bool ignore_member_parameters, bool force_default_mods)
        """
        ...
    
    def setCleavageSite(self, cleavage_site: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCleavageSite(String cleavage_site)
        """
        ...
    
    def getCleavageSite(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCleavageSite()
        """
        ...
    ErrorUnit : __ErrorUnit
    MassType : __MassType 


class XTandemXMLFile:
    """
    Cython implementation of _XTandemXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1XTandemXMLFile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void XTandemXMLFile()
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , protein_identification: ProteinIdentification , id_data: List[PeptideIdentification] , mod_def_set: ModificationDefinitionsSet ) -> None:
        """
        Cython signature: void load(String filename, ProteinIdentification & protein_identification, libcpp_vector[PeptideIdentification] & id_data, ModificationDefinitionsSet & mod_def_set)
        """
        ... 


class __CHARGEMODE_FD:
    None
    QFROMFEATURE : int
    QHEURISTIC : int
    QALL : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __DerivatizationAgent:
    None
    NOT_SELECTED : int
    TBDMS : int
    SIZE_OF_DERIVATIZATIONAGENT : int

    def getMapping(self) -> Dict[int, str]:
       ...
    DerivatizationAgent : __DerivatizationAgent 


class __ErrorUnit:
    None
    DALTONS : int
    PPM : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class ITRAQ_TYPES:
    None
    FOURPLEX : int
    EIGHTPLEX : int
    TMT_SIXPLEX : int
    SIZE_OF_ITRAQ_TYPES : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __MassIntensityType:
    None
    NORM_MAX : int
    NORM_SUM : int
    SIZE_OF_MASSINTENSITYTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ...
    MassIntensityType : __MassIntensityType 


class __MassType:
    None
    MONOISOTOPIC : int
    AVERAGE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __Sorted:
    None
    INTENSITY : int
    MASS : int
    UNDEFINED : int

    def getMapping(self) -> Dict[int, str]:
       ... 

