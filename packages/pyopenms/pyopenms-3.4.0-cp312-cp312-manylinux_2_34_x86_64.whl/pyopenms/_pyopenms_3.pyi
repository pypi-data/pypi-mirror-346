from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_NASequence_fromString(s: Union[bytes, str, String] ) -> NASequence:
    """
    Cython signature: NASequence fromString(const String & s)
    """
    ...


class AAIndex:
    """
    Cython implementation of _AAIndex

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AAIndex.html>`_
    """
    
    def aliphatic(self, aa: bytes ) -> float:
        """
        Cython signature: double aliphatic(char aa)
        """
        ...
    
    def acidic(self, aa: bytes ) -> float:
        """
        Cython signature: double acidic(char aa)
        """
        ...
    
    def basic(self, aa: bytes ) -> float:
        """
        Cython signature: double basic(char aa)
        """
        ...
    
    def polar(self, aa: bytes ) -> float:
        """
        Cython signature: double polar(char aa)
        """
        ...
    
    def getKHAG800101(self, aa: bytes ) -> float:
        """
        Cython signature: double getKHAG800101(char aa)
        """
        ...
    
    def getVASM830103(self, aa: bytes ) -> float:
        """
        Cython signature: double getVASM830103(char aa)
        """
        ...
    
    def getNADH010106(self, aa: bytes ) -> float:
        """
        Cython signature: double getNADH010106(char aa)
        """
        ...
    
    def getNADH010107(self, aa: bytes ) -> float:
        """
        Cython signature: double getNADH010107(char aa)
        """
        ...
    
    def getWILM950102(self, aa: bytes ) -> float:
        """
        Cython signature: double getWILM950102(char aa)
        """
        ...
    
    def getROBB760107(self, aa: bytes ) -> float:
        """
        Cython signature: double getROBB760107(char aa)
        """
        ...
    
    def getOOBM850104(self, aa: bytes ) -> float:
        """
        Cython signature: double getOOBM850104(char aa)
        """
        ...
    
    def getFAUJ880111(self, aa: bytes ) -> float:
        """
        Cython signature: double getFAUJ880111(char aa)
        """
        ...
    
    def getFINA770101(self, aa: bytes ) -> float:
        """
        Cython signature: double getFINA770101(char aa)
        """
        ...
    
    def getARGP820102(self, aa: bytes ) -> float:
        """
        Cython signature: double getARGP820102(char aa)
        """
        ...
    
    def calculateGB(self, seq: AASequence , T: float ) -> float:
        """
        Cython signature: double calculateGB(AASequence & seq, double T)
        """
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


class BaseFeature:
    """
    Cython implementation of _BaseFeature

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1BaseFeature.html>`_
      -- Inherits from ['UniqueIdInterface', 'RichPeak2D']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void BaseFeature()
        """
        ...
    
    @overload
    def __init__(self, in_0: BaseFeature ) -> None:
        """
        Cython signature: void BaseFeature(BaseFeature &)
        """
        ...
    
    def getQuality(self) -> float:
        """
        Cython signature: float getQuality()
        Returns the overall quality
        """
        ...
    
    def setQuality(self, q: float ) -> None:
        """
        Cython signature: void setQuality(float q)
        Sets the overall quality
        """
        ...
    
    def getWidth(self) -> float:
        """
        Cython signature: float getWidth()
        Returns the features width (full width at half max, FWHM)
        """
        ...
    
    def setWidth(self, q: float ) -> None:
        """
        Cython signature: void setWidth(float q)
        Sets the width of the feature (FWHM)
        """
        ...
    
    def getCharge(self) -> int:
        """
        Cython signature: int getCharge()
        Returns the charge state
        """
        ...
    
    def setCharge(self, q: int ) -> None:
        """
        Cython signature: void setCharge(int q)
        Sets the charge state
        """
        ...
    
    def getAnnotationState(self) -> int:
        """
        Cython signature: AnnotationState getAnnotationState()
        State of peptide identifications attached to this feature. If one ID has multiple hits, the output depends on the top-hit only
        """
        ...
    
    def getPeptideIdentifications(self) -> List[PeptideIdentification]:
        """
        Cython signature: libcpp_vector[PeptideIdentification] getPeptideIdentifications()
        Returns the PeptideIdentification vector
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
    
    def __richcmp__(self, other: BaseFeature, op: int) -> Any:
        ... 


class BinnedSpectrum:
    """
    Cython implementation of _BinnedSpectrum

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1BinnedSpectrum.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void BinnedSpectrum()
        """
        ...
    
    @overload
    def __init__(self, in_0: BinnedSpectrum ) -> None:
        """
        Cython signature: void BinnedSpectrum(BinnedSpectrum &)
        """
        ...
    
    @overload
    def __init__(self, in_0: MSSpectrum , size: float , unit_ppm: bool , spread: int , offset: float ) -> None:
        """
        Cython signature: void BinnedSpectrum(MSSpectrum, float size, bool unit_ppm, unsigned int spread, float offset)
        """
        ...
    
    def getBinSize(self) -> float:
        """
        Cython signature: float getBinSize()
        Returns the bin size
        """
        ...
    
    def getBinSpread(self) -> int:
        """
        Cython signature: unsigned int getBinSpread()
        Returns the bin spread
        """
        ...
    
    def getBinIndex(self, mz: float ) -> int:
        """
        Cython signature: unsigned int getBinIndex(float mz)
        Returns the bin index of a given m/z position
        """
        ...
    
    def getBinLowerMZ(self, i: int ) -> float:
        """
        Cython signature: float getBinLowerMZ(size_t i)
        Returns the lower m/z of a bin given its index
        """
        ...
    
    def getBinIntensity(self, mz: float ) -> float:
        """
        Cython signature: float getBinIntensity(double mz)
        Returns the bin intensity at a given m/z position
        """
        ...
    
    def getPrecursors(self) -> List[Precursor]:
        """
        Cython signature: libcpp_vector[Precursor] getPrecursors()
        """
        ...
    
    def isCompatible(self, a: BinnedSpectrum , b: BinnedSpectrum ) -> bool:
        """
        Cython signature: bool isCompatible(BinnedSpectrum & a, BinnedSpectrum & b)
        """
        ...
    
    def getOffset(self) -> float:
        """
        Cython signature: float getOffset()
        Returns offset
        """
        ...
    
    def __richcmp__(self, other: BinnedSpectrum, op: int) -> Any:
        ... 


class CVMappingRule:
    """
    Cython implementation of _CVMappingRule

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVMappingRule.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVMappingRule()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVMappingRule ) -> None:
        """
        Cython signature: void CVMappingRule(CVMappingRule &)
        """
        ...
    
    def setIdentifier(self, identifier: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(String identifier)
        Sets the identifier of the rule
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        Returns the identifier of the rule
        """
        ...
    
    def setElementPath(self, element_path: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setElementPath(String element_path)
        Sets the path of the DOM element, where this rule is allowed
        """
        ...
    
    def getElementPath(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getElementPath()
        Returns the path of the DOM element, where this rule is allowed
        """
        ...
    
    def setRequirementLevel(self, level: int ) -> None:
        """
        Cython signature: void setRequirementLevel(RequirementLevel level)
        Sets the requirement level of this rule
        """
        ...
    
    def getRequirementLevel(self) -> int:
        """
        Cython signature: RequirementLevel getRequirementLevel()
        Returns the requirement level of this rule
        """
        ...
    
    def setCombinationsLogic(self, combinations_logic: int ) -> None:
        """
        Cython signature: void setCombinationsLogic(CombinationsLogic combinations_logic)
        Sets the combination operator of the rule
        """
        ...
    
    def getCombinationsLogic(self) -> int:
        """
        Cython signature: CombinationsLogic getCombinationsLogic()
        Returns the combinations operator of the rule
        """
        ...
    
    def setScopePath(self, path: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setScopePath(String path)
        Sets the scope path of the rule
        """
        ...
    
    def getScopePath(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getScopePath()
        Returns the scope path of the rule
        """
        ...
    
    def setCVTerms(self, cv_terms: List[CVMappingTerm] ) -> None:
        """
        Cython signature: void setCVTerms(libcpp_vector[CVMappingTerm] cv_terms)
        Sets the terms which are allowed
        """
        ...
    
    def getCVTerms(self) -> List[CVMappingTerm]:
        """
        Cython signature: libcpp_vector[CVMappingTerm] getCVTerms()
        Returns the allowed terms
        """
        ...
    
    def addCVTerm(self, cv_terms: CVMappingTerm ) -> None:
        """
        Cython signature: void addCVTerm(CVMappingTerm cv_terms)
        Adds a term to the allowed terms
        """
        ...
    
    def __richcmp__(self, other: CVMappingRule, op: int) -> Any:
        ...
    CombinationsLogic : __CombinationsLogic
    RequirementLevel : __RequirementLevel 


class CVTerm_ControlledVocabulary:
    """
    Cython implementation of _CVTerm_ControlledVocabulary

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVTerm_ControlledVocabulary.html>`_
    """
    
    name: Union[bytes, str, String]
    
    id: Union[bytes, str, String]
    
    parents: Set[bytes]
    
    children: Set[bytes]
    
    obsolete: bool
    
    description: Union[bytes, str, String]
    
    synonyms: List[bytes]
    
    unparsed: List[bytes]
    
    xref_type: int
    
    xref_binary: List[bytes]
    
    units: Set[bytes]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVTerm_ControlledVocabulary()
        """
        ...
    
    @overload
    def __init__(self, rhs: CVTerm_ControlledVocabulary ) -> None:
        """
        Cython signature: void CVTerm_ControlledVocabulary(CVTerm_ControlledVocabulary rhs)
        """
        ...
    
    @overload
    def toXMLString(self, ref: Union[bytes, str, String] , value: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String toXMLString(String ref, String value)
        Get mzidentml formatted string. i.e. a cvparam xml element, ref should be the name of the ControlledVocabulary (i.e. cv.name()) containing the CVTerm (e.g. PSI-MS for the psi-ms.obo - gets loaded in all cases like that??), value can be empty if not available
        """
        ...
    
    @overload
    def toXMLString(self, ref: Union[bytes, str, String] , value: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> Union[bytes, str, String]:
        """
        Cython signature: String toXMLString(String ref, DataValue value)
        Get mzidentml formatted string. i.e. a cvparam xml element, ref should be the name of the ControlledVocabulary (i.e. cv.name()) containing the CVTerm (e.g. PSI-MS for the psi-ms.obo - gets loaded in all cases like that??), value can be empty if not available
        """
        ...
    
    def getXRefTypeName(self, type: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String getXRefTypeName(XRefType_CVTerm_ControlledVocabulary type)
        """
        ...
    
    def isHigherBetterScore(self, term: CVTerm_ControlledVocabulary ) -> bool:
        """
        Cython signature: bool isHigherBetterScore(CVTerm_ControlledVocabulary term)
        """
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


class ChromatogramTools:
    """
    Cython implementation of _ChromatogramTools

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ChromatogramTools.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ChromatogramTools()
        """
        ...
    
    @overload
    def __init__(self, in_0: ChromatogramTools ) -> None:
        """
        Cython signature: void ChromatogramTools(ChromatogramTools &)
        """
        ...
    
    def convertChromatogramsToSpectra(self, epx: MSExperiment ) -> None:
        """
        Cython signature: void convertChromatogramsToSpectra(MSExperiment & epx)
        Converts the chromatogram to a list of spectra with instrument settings
        """
        ...
    
    def convertSpectraToChromatograms(self, epx: MSExperiment , remove_spectra: bool , force_conversion: bool ) -> None:
        """
        Cython signature: void convertSpectraToChromatograms(MSExperiment & epx, bool remove_spectra, bool force_conversion)
        Converts e.g. SRM spectra to chromatograms
        """
        ... 


class ChromeleonFile:
    """
    Cython implementation of _ChromeleonFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ChromeleonFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ChromeleonFile()
        Load Chromeleon HPLC text file and save it into a `MSExperiment`.
        """
        ...
    
    @overload
    def __init__(self, in_0: ChromeleonFile ) -> None:
        """
        Cython signature: void ChromeleonFile(ChromeleonFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , experiment: MSExperiment ) -> None:
        """
        Cython signature: void load(const String & filename, MSExperiment & experiment)
        Load the file's data and metadata, and save it into a `MSExperiment`
        """
        ... 


class ControlledVocabulary:
    """
    Cython implementation of _ControlledVocabulary

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ControlledVocabulary.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ControlledVocabulary()
        """
        ...
    
    @overload
    def __init__(self, in_0: ControlledVocabulary ) -> None:
        """
        Cython signature: void ControlledVocabulary(ControlledVocabulary &)
        """
        ...
    
    def name(self) -> Union[bytes, str, String]:
        """
        Cython signature: String name()
        Returns the CV name (set in the load method)
        """
        ...
    
    def loadFromOBO(self, name: Union[bytes, str, String] , filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void loadFromOBO(String name, String filename)
        Loads the CV from an OBO file
        """
        ...
    
    def exists(self, id: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool exists(String id)
        Returns true if the term is in the CV. Returns false otherwise.
        """
        ...
    
    def hasTermWithName(self, name: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasTermWithName(String name)
        Returns true if a term with the given name is in the CV. Returns false otherwise
        """
        ...
    
    def getTerm(self, id: Union[bytes, str, String] ) -> CVTerm_ControlledVocabulary:
        """
        Cython signature: CVTerm_ControlledVocabulary getTerm(String id)
        Returns a term specified by ID
        """
        ...
    
    def getTermByName(self, name: Union[bytes, str, String] , desc: Union[bytes, str, String] ) -> CVTerm_ControlledVocabulary:
        """
        Cython signature: CVTerm_ControlledVocabulary getTermByName(String name, String desc)
        Returns a term specified by name
        """
        ...
    
    def getAllChildTerms(self, terms: Set[bytes] , parent: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void getAllChildTerms(libcpp_set[String] terms, String parent)
        Writes all child terms recursively into terms
        """
        ...
    
    def isChildOf(self, child: Union[bytes, str, String] , parent: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool isChildOf(String child, String parent)
        Returns True if `child` is a child of `parent`
        """
        ... 


class DecoyGenerator:
    """
    Cython implementation of _DecoyGenerator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DecoyGenerator.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DecoyGenerator()
        """
        ...
    
    @overload
    def __init__(self, in_0: DecoyGenerator ) -> None:
        """
        Cython signature: void DecoyGenerator(DecoyGenerator &)
        """
        ...
    
    def setSeed(self, in_0: int ) -> None:
        """
        Cython signature: void setSeed(uint64_t)
        """
        ...
    
    def reverseProtein(self, protein: AASequence ) -> AASequence:
        """
        Cython signature: AASequence reverseProtein(const AASequence & protein)
        Reverses the protein sequence
        """
        ...
    
    def reversePeptides(self, protein: AASequence , protease: Union[bytes, str, String] ) -> AASequence:
        """
        Cython signature: AASequence reversePeptides(const AASequence & protein, const String & protease)
        Reverses the protein's peptide sequences between enzymatic cutting positions
        """
        ...
    
    def shufflePeptides(self, aas: AASequence , protease: Union[bytes, str, String] , max_attempts: int ) -> AASequence:
        """
        Cython signature: AASequence shufflePeptides(const AASequence & aas, const String & protease, const int max_attempts)
        Shuffle the protein's peptide sequences between enzymatic cutting positions, each peptide is shuffled @param max_attempts times to minimize sequence identity
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


class ExperimentalSettings:
    """
    Cython implementation of _ExperimentalSettings

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ExperimentalSettings.html>`_
      -- Inherits from ['DocumentIdentifier', 'MetaInfoInterface']

    Description of the experimental settings, provides meta-information
    about an LC-MS/MS injection.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ExperimentalSettings()
        """
        ...
    
    @overload
    def __init__(self, in_0: ExperimentalSettings ) -> None:
        """
        Cython signature: void ExperimentalSettings(ExperimentalSettings &)
        """
        ...
    
    def getSourceFiles(self) -> List[SourceFile]:
        """
        Cython signature: libcpp_vector[SourceFile] getSourceFiles()
        Returns a reference to the source data file
        """
        ...
    
    def setSourceFiles(self, source_files: List[SourceFile] ) -> None:
        """
        Cython signature: void setSourceFiles(libcpp_vector[SourceFile] source_files)
        Sets the source data file
        """
        ...
    
    def getDateTime(self) -> DateTime:
        """
        Cython signature: DateTime getDateTime()
        Returns the date the experiment was performed
        """
        ...
    
    def setDateTime(self, date_time: DateTime ) -> None:
        """
        Cython signature: void setDateTime(DateTime date_time)
        Sets the date the experiment was performed
        """
        ...
    
    def getSample(self) -> Sample:
        """
        Cython signature: Sample getSample()
        Returns a reference to the sample description
        """
        ...
    
    def setSample(self, sample: Sample ) -> None:
        """
        Cython signature: void setSample(Sample sample)
        Sets the sample description
        """
        ...
    
    def getContacts(self) -> List[ContactPerson]:
        """
        Cython signature: libcpp_vector[ContactPerson] getContacts()
        Returns a reference to the list of contact persons
        """
        ...
    
    def setContacts(self, contacts: List[ContactPerson] ) -> None:
        """
        Cython signature: void setContacts(libcpp_vector[ContactPerson] contacts)
        Sets the list of contact persons
        """
        ...
    
    def getInstrument(self) -> Instrument:
        """
        Cython signature: Instrument getInstrument()
        Returns a reference to the MS instrument description
        """
        ...
    
    def setInstrument(self, instrument: Instrument ) -> None:
        """
        Cython signature: void setInstrument(Instrument instrument)
        Sets the MS instrument description
        """
        ...
    
    def getHPLC(self) -> HPLC:
        """
        Cython signature: HPLC getHPLC()
        Returns a reference to the description of the HPLC run
        """
        ...
    
    def setHPLC(self, hplc: HPLC ) -> None:
        """
        Cython signature: void setHPLC(HPLC hplc)
        Sets the description of the HPLC run
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
    
    def getProteinIdentifications(self) -> List[ProteinIdentification]:
        """
        Cython signature: libcpp_vector[ProteinIdentification] getProteinIdentifications()
        Returns a reference to the protein ProteinIdentification vector
        """
        ...
    
    def setProteinIdentifications(self, protein_identifications: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void setProteinIdentifications(libcpp_vector[ProteinIdentification] protein_identifications)
        Sets the protein ProteinIdentification vector
        """
        ...
    
    def getFractionIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFractionIdentifier()
        Returns fraction identifier
        """
        ...
    
    def setFractionIdentifier(self, fraction_identifier: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFractionIdentifier(String fraction_identifier)
        Sets the fraction identifier
        """
        ...
    
    def setIdentifier(self, id: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(String id)
        Sets document identifier (e.g. an LSID)
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        Retrieve document identifier (e.g. an LSID)
        """
        ...
    
    def setLoadedFileType(self, file_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLoadedFileType(String file_name)
        Sets the file_type according to the type of the file loaded from, preferably done whilst loading
        """
        ...
    
    def getLoadedFileType(self) -> int:
        """
        Cython signature: int getLoadedFileType()
        Returns the file_type (e.g. featureXML, consensusXML, mzData, mzXML, mzML, ...) of the file loaded
        """
        ...
    
    def setLoadedFilePath(self, file_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLoadedFilePath(String file_name)
        Sets the file_name according to absolute path of the file loaded, preferably done whilst loading
        """
        ...
    
    def getLoadedFilePath(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getLoadedFilePath()
        Returns the file_name which is the absolute path to the file loaded
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
    
    def __richcmp__(self, other: ExperimentalSettings, op: int) -> Any:
        ... 


class FIAMSScheduler:
    """
    Cython implementation of _FIAMSScheduler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FIAMSScheduler.html>`_

      ADD PYTHON DOCUMENTATION HERE
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FIAMSScheduler()
        Scheduler for FIA-MS data batches. Works with FIAMSDataProcessor
        """
        ...
    
    @overload
    def __init__(self, in_0: FIAMSScheduler ) -> None:
        """
        Cython signature: void FIAMSScheduler(FIAMSScheduler &)
        """
        ...
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , base_dir: Union[bytes, str, String] , load_cached_: bool ) -> None:
        """
        Cython signature: void FIAMSScheduler(String filename, String base_dir, bool load_cached_)
        """
        ...
    
    def run(self) -> None:
        """
        Cython signature: void run()
        Run the FIA-MS data analysis for the batch defined in the @filename_
        """
        ...
    
    def getBaseDir(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getBaseDir()
        Returns the base directory for the relevant paths from the csv file
        """
        ... 


class FeatureFinderAlgorithmPicked:
    """
    Cython implementation of _FeatureFinderAlgorithmPicked

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureFinderAlgorithmPicked.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureFinderAlgorithmPicked()
        """
        ...
    
    def run(self, input_map: MSExperiment , output: FeatureMap , param: Param , seeds: FeatureMap ) -> None:
        """
        Cython signature: void run(MSExperiment & input_map, FeatureMap & output, Param & param, FeatureMap & seeds)
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


class FeatureHandle:
    """
    Cython implementation of _FeatureHandle

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureHandle.html>`_
      -- Inherits from ['Peak2D', 'UniqueIdInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureHandle()
        Representation of a Peak2D, RichPeak2D or Feature
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureHandle ) -> None:
        """
        Cython signature: void FeatureHandle(FeatureHandle &)
        """
        ...
    
    @overload
    def __init__(self, map_index: int , point: Peak2D , element_index: int ) -> None:
        """
        Cython signature: void FeatureHandle(uint64_t map_index, Peak2D & point, uint64_t element_index)
        """
        ...
    
    def getMapIndex(self) -> int:
        """
        Cython signature: uint64_t getMapIndex()
        Returns the map index
        """
        ...
    
    def setMapIndex(self, i: int ) -> None:
        """
        Cython signature: void setMapIndex(uint64_t i)
        Sets the map index
        """
        ...
    
    def setCharge(self, charge: int ) -> None:
        """
        Cython signature: void setCharge(int charge)
        Sets the charge
        """
        ...
    
    def getCharge(self) -> int:
        """
        Cython signature: int getCharge()
        Returns the charge
        """
        ...
    
    def setWidth(self, width: float ) -> None:
        """
        Cython signature: void setWidth(float width)
        Sets the width (FWHM)
        """
        ...
    
    def getWidth(self) -> float:
        """
        Cython signature: float getWidth()
        Returns the width (FWHM)
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
    
    def __richcmp__(self, other: FeatureHandle, op: int) -> Any:
        ... 


class FeatureMap:
    """
    Cython implementation of _FeatureMap

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureMap.html>`_
      -- Inherits from ['UniqueIdInterface', 'DocumentIdentifier', 'RangeManagerRtMzInt', 'MetaInfoInterface']

    A container for features.
    
    A feature map is a container holding features, which represent
    chemical entities (peptides, proteins, small molecules etc.) found
    in an LC-MS/MS experiment.
    
    This class supports direct iteration in Python.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureMap()
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureMap ) -> None:
        """
        Cython signature: void FeatureMap(FeatureMap &)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: int size()
        """
        ...
    
    def __getitem__(self, in_0: int ) -> Feature:
        """
        Cython signature: Feature & operator[](size_t)
        """
        ...
    def __setitem__(self, key: int, value: Feature ) -> None:
        """Cython signature: Feature & operator[](size_t)"""
        ...
    
    @overload
    def push_back(self, spec: Feature ) -> None:
        """
        Cython signature: void push_back(Feature spec)
        """
        ...
    
    @overload
    def push_back(self, spec: MRMFeature ) -> None:
        """
        Cython signature: void push_back(MRMFeature spec)
        """
        ...
    
    @overload
    def sortByIntensity(self, ) -> None:
        """
        Cython signature: void sortByIntensity()
        Sorts the peaks according to ascending intensity
        """
        ...
    
    @overload
    def sortByIntensity(self, reverse: bool ) -> None:
        """
        Cython signature: void sortByIntensity(bool reverse)
        Sorts the peaks according to ascending intensity. Order is reversed if argument is `true` ( reverse = true )
        """
        ...
    
    def sortByPosition(self) -> None:
        """
        Cython signature: void sortByPosition()
        Sorts features by position. Lexicographical comparison (first RT then m/z) is done
        """
        ...
    
    def sortByRT(self) -> None:
        """
        Cython signature: void sortByRT()
        Sorts features by RT position
        """
        ...
    
    def sortByMZ(self) -> None:
        """
        Cython signature: void sortByMZ()
        Sorts features by m/z position
        """
        ...
    
    def sortByOverallQuality(self) -> None:
        """
        Cython signature: void sortByOverallQuality()
        Sorts features by ascending overall quality. Order is reversed if argument is `true` ( reverse = true )
        """
        ...
    
    def swap(self, in_0: FeatureMap ) -> None:
        """
        Cython signature: void swap(FeatureMap &)
        """
        ...
    
    def swapFeaturesOnly(self, swapfrom: FeatureMap ) -> None:
        """
        Cython signature: void swapFeaturesOnly(FeatureMap swapfrom)
        Swaps the feature content (plus its range information) of this map
        """
        ...
    
    @overload
    def clear(self, ) -> None:
        """
        Cython signature: void clear()
        Clears all data and meta data
        """
        ...
    
    @overload
    def clear(self, clear_meta_data: bool ) -> None:
        """
        Cython signature: void clear(bool clear_meta_data)
        Clears all data and meta data. If 'true' is passed as an argument, all meta data is cleared in addition to the data
        """
        ...
    
    def __add__(self: FeatureMap, other: FeatureMap) -> FeatureMap:
        ...
    
    def __iadd__(self: FeatureMap, other: FeatureMap) -> FeatureMap:
        ...
    
    def updateRanges(self) -> None:
        """
        Cython signature: void updateRanges()
        """
        ...
    
    def getProteinIdentifications(self) -> List[ProteinIdentification]:
        """
        Cython signature: libcpp_vector[ProteinIdentification] getProteinIdentifications()
        """
        ...
    
    def setProteinIdentifications(self, in_0: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void setProteinIdentifications(libcpp_vector[ProteinIdentification])
        Sets the protein identifications
        """
        ...
    
    def getUnassignedPeptideIdentifications(self) -> List[PeptideIdentification]:
        """
        Cython signature: libcpp_vector[PeptideIdentification] getUnassignedPeptideIdentifications()
        """
        ...
    
    def setUnassignedPeptideIdentifications(self, in_0: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void setUnassignedPeptideIdentifications(libcpp_vector[PeptideIdentification])
        Sets the unassigned peptide identifications
        """
        ...
    
    def getDataProcessing(self) -> List[DataProcessing]:
        """
        Cython signature: libcpp_vector[DataProcessing] getDataProcessing()
        """
        ...
    
    def setDataProcessing(self, in_0: List[DataProcessing] ) -> None:
        """
        Cython signature: void setDataProcessing(libcpp_vector[DataProcessing])
        Sets the description of the applied data processing
        """
        ...
    
    @overload
    def setPrimaryMSRunPath(self, s: List[bytes] ) -> None:
        """
        Cython signature: void setPrimaryMSRunPath(StringList & s)
        Sets the file path to the primary MS run (usually the mzML file obtained after data conversion from raw files)
        """
        ...
    
    @overload
    def setPrimaryMSRunPath(self, s: List[bytes] , e: MSExperiment ) -> None:
        """
        Cython signature: void setPrimaryMSRunPath(StringList & s, MSExperiment & e)
        Sets the file path to the primary MS run using the mzML annotated in the MSExperiment argument `e`
        """
        ...
    
    def getPrimaryMSRunPath(self, toFill: List[bytes] ) -> None:
        """
        Cython signature: void getPrimaryMSRunPath(StringList & toFill)
        Returns the file path to the first MS run
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
    
    def setIdentifier(self, id: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(String id)
        Sets document identifier (e.g. an LSID)
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        Retrieve document identifier (e.g. an LSID)
        """
        ...
    
    def setLoadedFileType(self, file_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLoadedFileType(String file_name)
        Sets the file_type according to the type of the file loaded from, preferably done whilst loading
        """
        ...
    
    def getLoadedFileType(self) -> int:
        """
        Cython signature: int getLoadedFileType()
        Returns the file_type (e.g. featureXML, consensusXML, mzData, mzXML, mzML, ...) of the file loaded
        """
        ...
    
    def setLoadedFilePath(self, file_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLoadedFilePath(String file_name)
        Sets the file_name according to absolute path of the file loaded, preferably done whilst loading
        """
        ...
    
    def getLoadedFilePath(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getLoadedFilePath()
        Returns the file_name which is the absolute path to the file loaded
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
    
    def getMinMZ(self) -> float:
        """
        Cython signature: double getMinMZ()
        Returns the minimum m/z
        """
        ...
    
    def getMaxMZ(self) -> float:
        """
        Cython signature: double getMaxMZ()
        Returns the maximum m/z
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
    
    def __richcmp__(self, other: FeatureMap, op: int) -> Any:
        ...
    
    def __iter__(self) -> Feature:
       ... 


class Fitter1D:
    """
    Cython implementation of _Fitter1D

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Fitter1D.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Fitter1D()
        Abstract base class for all 1D-dimensional model fitter
        """
        ...
    
    @overload
    def __init__(self, in_0: Fitter1D ) -> None:
        """
        Cython signature: void Fitter1D(Fitter1D &)
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


class GaussTraceFitter:
    """
    Cython implementation of _GaussTraceFitter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1GaussTraceFitter.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void GaussTraceFitter()
        Fitter for RT profiles using a Gaussian background model
        """
        ...
    
    @overload
    def __init__(self, in_0: GaussTraceFitter ) -> None:
        """
        Cython signature: void GaussTraceFitter(GaussTraceFitter &)
        """
        ...
    
    def fit(self, traces: MassTraces ) -> None:
        """
        Cython signature: void fit(MassTraces & traces)
        Override important methods
        """
        ...
    
    def getLowerRTBound(self) -> float:
        """
        Cython signature: double getLowerRTBound()
        Returns the lower RT bound
        """
        ...
    
    def getUpperRTBound(self) -> float:
        """
        Cython signature: double getUpperRTBound()
        Returns the upper RT bound
        """
        ...
    
    def getHeight(self) -> float:
        """
        Cython signature: double getHeight()
        Returns height of the fitted gaussian model
        """
        ...
    
    def getCenter(self) -> float:
        """
        Cython signature: double getCenter()
        Returns center of the fitted gaussian model
        """
        ...
    
    def getFWHM(self) -> float:
        """
        Cython signature: double getFWHM()
        Returns FWHM of the fitted gaussian model
        """
        ...
    
    def getSigma(self) -> float:
        """
        Cython signature: double getSigma()
        Returns Sigma of the fitted gaussian model
        """
        ...
    
    def checkMaximalRTSpan(self, max_rt_span: float ) -> bool:
        """
        Cython signature: bool checkMaximalRTSpan(double max_rt_span)
        """
        ...
    
    def checkMinimalRTSpan(self, rt_bounds: List[float, float] , min_rt_span: float ) -> bool:
        """
        Cython signature: bool checkMinimalRTSpan(libcpp_pair[double,double] & rt_bounds, double min_rt_span)
        """
        ...
    
    def computeTheoretical(self, trace: MassTrace , k: int ) -> float:
        """
        Cython signature: double computeTheoretical(MassTrace & trace, size_t k)
        """
        ...
    
    def getArea(self) -> float:
        """
        Cython signature: double getArea()
        Returns area of the fitted gaussian model
        """
        ...
    
    def getGnuplotFormula(self, trace: MassTrace , function_name: bytes , baseline: float , rt_shift: float ) -> Union[bytes, str, String]:
        """
        Cython signature: String getGnuplotFormula(MassTrace & trace, char function_name, double baseline, double rt_shift)
        """
        ...
    
    def getValue(self, rt: float ) -> float:
        """
        Cython signature: double getValue(double rt)
        Returns value of the fitted gaussian model
        """
        ... 


class IDMapper:
    """
    Cython implementation of _IDMapper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IDMapper.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IDMapper()
        Annotates an MSExperiment, FeatureMap or ConsensusMap with peptide identifications
        """
        ...
    
    @overload
    def __init__(self, in_0: IDMapper ) -> None:
        """
        Cython signature: void IDMapper(IDMapper &)
        """
        ...
    
    @overload
    def annotate(self, map_: MSExperiment , ids: List[PeptideIdentification] , protein_ids: List[ProteinIdentification] , clear_ids: bool , mapMS1: bool ) -> None:
        """
        Cython signature: void annotate(MSExperiment & map_, libcpp_vector[PeptideIdentification] & ids, libcpp_vector[ProteinIdentification] & protein_ids, bool clear_ids, bool mapMS1)
        Mapping method for peak maps\n
        
        The identifications stored in a PeptideIdentification instance can be added to the
        corresponding spectrum
        Note that a PeptideIdentication is added to ALL spectra which are within the allowed RT and MZ boundaries
        
        
        :param map: MSExperiment to receive the identifications
        :param peptide_ids: PeptideIdentification for the MSExperiment
        :param protein_ids: ProteinIdentification for the MSExperiment
        :param clear_ids: Reset peptide and protein identifications of each scan before annotating
        :param map_ms1: Attach Ids to MS1 spectra using RT mapping only (without precursor, without m/z)
        :raises:
          Exception: MissingInformation is thrown if entries of 'peptide_ids' do not contain 'MZ' and 'RT' information
        """
        ...
    
    @overload
    def annotate(self, map_: MSExperiment , fmap: FeatureMap , clear_ids: bool , mapMS1: bool ) -> None:
        """
        Cython signature: void annotate(MSExperiment & map_, FeatureMap & fmap, bool clear_ids, bool mapMS1)
        Mapping method for peak maps\n
        
        Add peptide identifications stored in a feature map to their
        corresponding spectrum
        This function converts the feature map to a vector of peptide identifications (all peptide IDs from each feature are taken)
        and calls the respective annotate() function
        RT and m/z are taken from the peptides, or (if missing) from the feature itself
        
        
        :param map: MSExperiment to receive the identifications
        :param fmap: FeatureMap with PeptideIdentifications for the MSExperiment
        :param clear_ids: Reset peptide and protein identifications of each scan before annotating
        :param map_ms1: Attach Ids to MS1 spectra using RT mapping only (without precursor, without m/z)
        """
        ...
    
    @overload
    def annotate(self, map_: FeatureMap , ids: List[PeptideIdentification] , protein_ids: List[ProteinIdentification] , use_centroid_rt: bool , use_centroid_mz: bool , spectra: MSExperiment ) -> None:
        """
        Cython signature: void annotate(FeatureMap & map_, libcpp_vector[PeptideIdentification] & ids, libcpp_vector[ProteinIdentification] & protein_ids, bool use_centroid_rt, bool use_centroid_mz, MSExperiment & spectra)
        Mapping method for peak maps\n
        
        If all features have at least one convex hull, peptide positions are matched against the bounding boxes of the convex hulls by default. If not, the positions of the feature centroids are used. The respective coordinates of the centroids are also used for matching (in place of the corresponding ranges from the bounding boxes) if 'use_centroid_rt' or 'use_centroid_mz' are true\n
        
        In any case, tolerance in RT and m/z dimension is applied according to the global parameters 'rt_tolerance' and 'mz_tolerance'. Tolerance is understood as "plus or minus x", so the matching range is actually increased by twice the tolerance value\n
        
        If several features (incl. tolerance) overlap the position of a peptide identification, the identification is annotated to all of them
        
        
        :param map: MSExperiment to receive the identifications
        :param ids: PeptideIdentification for the MSExperiment
        :param protein_ids: ProteinIdentification for the MSExperiment
        :param use_centroid_rt: Whether to use the RT value of feature centroids even if convex hulls are present
        :param use_centroid_mz: Whether to use the m/z value of feature centroids even if convex hulls are present
        :param spectra: Whether precursors not contained in the identifications are annotated with an empty PeptideIdentification object containing the scan index
        :raises:
          Exception: MissingInformation is thrown if entries of 'ids' do not contain 'MZ' and 'RT' information
        """
        ...
    
    @overload
    def annotate(self, map_: ConsensusMap , ids: List[PeptideIdentification] , protein_ids: List[ProteinIdentification] , measure_from_subelements: bool , annotate_ids_with_subelements: bool , spectra: MSExperiment ) -> None:
        """
        Cython signature: void annotate(ConsensusMap & map_, libcpp_vector[PeptideIdentification] & ids, libcpp_vector[ProteinIdentification] & protein_ids, bool measure_from_subelements, bool annotate_ids_with_subelements, MSExperiment & spectra)
        Mapping method for peak maps\n
        
        If all features have at least one convex hull, peptide positions are matched against the bounding boxes of the convex hulls by default. If not, the positions of the feature centroids are used. The respective coordinates of the centroids are also used for matching (in place of the corresponding ranges from the bounding boxes) if 'use_centroid_rt' or 'use_centroid_mz' are true\n
        
        In any case, tolerance in RT and m/z dimension is applied according to the global parameters 'rt_tolerance' and 'mz_tolerance'. Tolerance is understood as "plus or minus x", so the matching range is actually increased by twice the tolerance value\n
        
        If several features (incl. tolerance) overlap the position of a peptide identification, the identification is annotated to all of them
        
        
        :param map: MSExperiment to receive the identifications
        :param ids: PeptideIdentification for the MSExperiment
        :param protein_ids: ProteinIdentification for the MSExperiment
        :param measure_from_subelements: Boolean operator set to true if distance estimate from FeatureHandles instead of Centroid
        :param annotate_ids_with_subelements: Boolean operator set to true if store map index of FeatureHandle in peptide identification
        :param spectra: Whether precursors not contained in the identifications are annotated with an empty PeptideIdentification object containing the scan index
        :raises:
          Exception: MissingInformation is thrown if entries of 'ids' do not contain 'MZ' and 'RT' information
        """
        ...
    
    def mapPrecursorsToIdentifications(self, spectra: MSExperiment , ids: List[PeptideIdentification] , mz_tol: float , rt_tol: float ) -> IDMapper_SpectraIdentificationState:
        """
        Cython signature: IDMapper_SpectraIdentificationState mapPrecursorsToIdentifications(MSExperiment spectra, libcpp_vector[PeptideIdentification] & ids, double mz_tol, double rt_tol)
        Mapping of peptide identifications to spectra\n
        This helper function partitions all spectra into those that had:
        - no precursor (e.g. MS1 spectra),
        - at least one identified precursor,
        - or only unidentified precursor
        
        
        :param spectra: The mass spectra
        :param ids: The peptide identifications
        :param mz_tol: Tolerance used to map to precursor m/z
        :param rt_tol: Tolerance used to map to spectrum retention time
        :return: A struct of vectors holding spectra indices of the partitioning
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


class IDMapper_SpectraIdentificationState:
    """
    Cython implementation of _IDMapper_SpectraIdentificationState

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IDMapper_SpectraIdentificationState.html>`_
    """
    
    no_precursors: List[int]
    
    identified: List[int]
    
    unidentified: List[int]
    
    def __init__(self) -> None:
        """
        Cython signature: void IDMapper_SpectraIdentificationState()
        """
        ... 


class IDRipper:
    """
    Cython implementation of _IDRipper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1IDRipper.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void IDRipper()
        Ripping protein/peptide identification according their file origin
        """
        ...
    
    def rip(self, rfis: List[RipFileIdentifier] , rfcs: List[RipFileContent] , proteins: List[ProteinIdentification] , peptides: List[PeptideIdentification] , full_split: bool , split_ident_runs: bool ) -> None:
        """
        Cython signature: void rip(libcpp_vector[RipFileIdentifier] & rfis, libcpp_vector[RipFileContent] & rfcs, libcpp_vector[ProteinIdentification] & proteins, libcpp_vector[PeptideIdentification] & peptides, bool full_split, bool split_ident_runs)
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


class IMSWeights:
    """
    Cython implementation of _IMSWeights

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ims::Weights_1_1IMSWeights.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IMSWeights()
        """
        ...
    
    @overload
    def __init__(self, in_0: IMSWeights ) -> None:
        """
        Cython signature: void IMSWeights(IMSWeights)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: int size()
        Gets size of a set of weights
        """
        ...
    
    def getWeight(self, i: int ) -> int:
        """
        Cython signature: unsigned long int getWeight(int i)
        Gets a scaled integer weight by index
        """
        ...
    
    def setPrecision(self, precision: float ) -> None:
        """
        Cython signature: void setPrecision(double precision)
        Sets a new precision to scale double values to integer
        """
        ...
    
    def getPrecision(self) -> float:
        """
        Cython signature: double getPrecision()
        Gets precision.
        """
        ...
    
    def back(self) -> int:
        """
        Cython signature: unsigned long int back()
        Gets a last weight
        """
        ...
    
    def getAlphabetMass(self, i: int ) -> float:
        """
        Cython signature: double getAlphabetMass(int i)
        Gets an original (double) alphabet mass by index
        """
        ...
    
    def getParentMass(self, decomposition: List[int] ) -> float:
        """
        Cython signature: double getParentMass(libcpp_vector[unsigned int] & decomposition)
        Returns a parent mass for a given `decomposition`
        """
        ...
    
    def swap(self, index1: int , index2: int ) -> None:
        """
        Cython signature: void swap(int index1, int index2)
        Exchanges weight and mass at index1 with weight and mass at index2
        """
        ...
    
    def divideByGCD(self) -> bool:
        """
        Cython signature: bool divideByGCD()
        Divides the integer weights by their gcd. The precision is also adjusted
        """
        ...
    
    def getMinRoundingError(self) -> float:
        """
        Cython signature: double getMinRoundingError()
        """
        ...
    
    def getMaxRoundingError(self) -> float:
        """
        Cython signature: double getMaxRoundingError()
        """
        ... 


class IdentificationRuns:
    """
    Cython implementation of _IdentificationRuns

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1IdentificationRuns.html>`_
    """
    
    def __init__(self, prot_ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void IdentificationRuns(libcpp_vector[ProteinIdentification] & prot_ids)
        """
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


class IsobaricQuantifierStatistics:
    """
    Cython implementation of _IsobaricQuantifierStatistics

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsobaricQuantifierStatistics.html>`_
    """
    
    channel_count: int
    
    iso_number_ms2_negative: int
    
    iso_number_reporter_negative: int
    
    iso_number_reporter_different: int
    
    iso_solution_different_intensity: float
    
    iso_total_intensity_negative: float
    
    number_ms2_total: int
    
    number_ms2_empty: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IsobaricQuantifierStatistics()
        """
        ...
    
    @overload
    def __init__(self, in_0: IsobaricQuantifierStatistics ) -> None:
        """
        Cython signature: void IsobaricQuantifierStatistics(IsobaricQuantifierStatistics &)
        """
        ...
    
    def reset(self) -> None:
        """
        Cython signature: void reset()
        """
        ... 


class ItraqEightPlexQuantitationMethod:
    """
    Cython implementation of _ItraqEightPlexQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ItraqEightPlexQuantitationMethod.html>`_
      -- Inherits from ['IsobaricQuantitationMethod']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ItraqEightPlexQuantitationMethod()
        iTRAQ 8 plex quantitation to be used with the IsobaricQuantitation
        """
        ...
    
    @overload
    def __init__(self, in_0: ItraqEightPlexQuantitationMethod ) -> None:
        """
        Cython signature: void ItraqEightPlexQuantitationMethod(ItraqEightPlexQuantitationMethod &)
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


class MSDataSqlConsumer:
    """
    Cython implementation of _MSDataSqlConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSDataSqlConsumer.html>`_
    """
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , run_id: int , buffer_size: int , full_meta: bool , lossy_compression: bool , linear_mass_acc: float ) -> None:
        """
        Cython signature: void MSDataSqlConsumer(String filename, uint64_t run_id, int buffer_size, bool full_meta, bool lossy_compression, double linear_mass_acc)
        """
        ...
    
    @overload
    def __init__(self, in_0: MSDataSqlConsumer ) -> None:
        """
        Cython signature: void MSDataSqlConsumer(MSDataSqlConsumer &)
        """
        ...
    
    def flush(self) -> None:
        """
        Cython signature: void flush()
        Flushes the data for good
        
        After calling this function, no more data is held in the buffer but the
        class is still able to receive new data
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        Write a spectrum to the output file
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        Write a chromatogram to the output file
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


class MSNumpressCoder:
    """
    Cython implementation of _MSNumpressCoder

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSNumpressCoder.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MSNumpressCoder()
        """
        ...
    
    @overload
    def __init__(self, in_0: MSNumpressCoder ) -> None:
        """
        Cython signature: void MSNumpressCoder(MSNumpressCoder &)
        """
        ...
    
    def encodeNP(self, in_: List[float] , result: String , zlib_compression: bool , config: NumpressConfig ) -> None:
        """
        Cython signature: void encodeNP(libcpp_vector[double] in_, String & result, bool zlib_compression, NumpressConfig config)
        Encodes a vector of floating point numbers into a Base64 string using numpress
        
        This code is obtained from the proteowizard implementation
        ./pwiz/pwiz/data/msdata/BinaryDataEncoder.cpp (adapted by Hannes Roest)
        
        This function will first apply the numpress encoding to the data, then
        encode the result in base64 (with optional zlib compression before
        base64 encoding)
        
        :note In case of error, result string is empty
        
        
        :param in: The vector of floating point numbers to be encoded
        :param result: The resulting string
        :param zlib_compression: Whether to apply zlib compression after numpress compression
        :param config: The numpress configuration defining the compression strategy
        """
        ...
    
    def decodeNP(self, in_: Union[bytes, str, String] , out: List[float] , zlib_compression: bool , config: NumpressConfig ) -> None:
        """
        Cython signature: void decodeNP(const String & in_, libcpp_vector[double] & out, bool zlib_compression, NumpressConfig config)
        Decodes a Base64 string to a vector of floating point numbers using numpress
        
        This code is obtained from the proteowizard implementation
        ./pwiz/pwiz/data/msdata/BinaryDataEncoder.cpp (adapted by Hannes Roest)
        
        This function will first decode the input base64 string (with optional
        zlib decompression after decoding) and then apply numpress decoding to
        the data
        
        
        :param in: The base64 encoded string
        :param out: The resulting vector of doubles
        :param zlib_compression: Whether to apply zlib de-compression before numpress de-compression
        :param config: The numpress configuration defining the compression strategy
        :raises:
          Exception: ConversionError if the string cannot be converted
        """
        ...
    
    def encodeNPRaw(self, in_: List[float] , result: String , config: NumpressConfig ) -> None:
        """
        Cython signature: void encodeNPRaw(libcpp_vector[double] in_, String & result, NumpressConfig config)
        Encode the data vector "in" to a raw byte array
        
        :note In case of error, "result" is given back unmodified
        :note The result is not a string but a raw byte array and may contain zero bytes
        
        This performs the raw numpress encoding on a set of data and does no
        Base64 encoding on the result. Therefore the result string is likely
        *unsafe* to handle and is a raw byte array.
        
        Please use the safe versions above unless you need access to the raw
        byte arrays
        
        
        :param in: The vector of floating point numbers to be encoded
        :param result: The resulting string
        :param config: The numpress configuration defining the compression strategy
        """
        ...
    
    def decodeNPRaw(self, in_: Union[bytes, str, String] , out: List[float] , config: NumpressConfig ) -> None:
        """
        Cython signature: void decodeNPRaw(const String & in_, libcpp_vector[double] & out, NumpressConfig config)
        Decode the raw byte array "in" to the result vector "out"
        
        :note The string in should *only* contain the data and _no_ extra
        null terminating byte
        
        This performs the raw numpress decoding on a raw byte array (not Base64
        encoded). Therefore the input string is likely *unsafe* to handle and is
        basically a byte container
        
        Please use the safe versions above unless you need access to the raw
        byte arrays
        
        
        :param in: The base64 encoded string
        :param out: The resulting vector of doubles
        :param config: The numpress configuration defining the compression strategy
        """
        ...
    NumpressCompression : __NumpressCompression 


class MSPFile:
    """
    Cython implementation of _MSPFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSPFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MSPFile()
        File adapter for MSP files (NIST spectra library)
        """
        ...
    
    @overload
    def __init__(self, in_0: MSPFile ) -> None:
        """
        Cython signature: void MSPFile(MSPFile &)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , exp: MSExperiment ) -> None:
        """
        Cython signature: void store(String filename, MSExperiment & exp)
        Stores a map in a MSPFile file
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , ids: List[PeptideIdentification] , exp: MSExperiment ) -> None:
        """
        Cython signature: void load(String filename, libcpp_vector[PeptideIdentification] & ids, MSExperiment & exp)
        Loads a map from a MSPFile file
        
        
        :param exp: PeakMap which contains the spectra after reading
        :param filename: The filename of the experiment
        :param ids: Output parameter which contains the peptide identifications from the spectra annotations
        """
        ... 


class MapAlignmentAlgorithmIdentification:
    """
    Cython implementation of _MapAlignmentAlgorithmIdentification

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MapAlignmentAlgorithmIdentification.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MapAlignmentAlgorithmIdentification()
        """
        ...
    
    @overload
    def align(self, in_0: List[MSExperiment] , in_1: List[TransformationDescription] , in_2: int ) -> None:
        """
        Cython signature: void align(libcpp_vector[MSExperiment] &, libcpp_vector[TransformationDescription] &, int)
        """
        ...
    
    @overload
    def align(self, in_0: List[FeatureMap] , in_1: List[TransformationDescription] , in_2: int ) -> None:
        """
        Cython signature: void align(libcpp_vector[FeatureMap] &, libcpp_vector[TransformationDescription] &, int)
        """
        ...
    
    @overload
    def align(self, in_0: List[ConsensusMap] , in_1: List[TransformationDescription] , in_2: int ) -> None:
        """
        Cython signature: void align(libcpp_vector[ConsensusMap] &, libcpp_vector[TransformationDescription] &, int)
        """
        ...
    
    @overload
    def setReference(self, in_0: MSExperiment ) -> None:
        """
        Cython signature: void setReference(MSExperiment &)
        """
        ...
    
    @overload
    def setReference(self, in_0: FeatureMap ) -> None:
        """
        Cython signature: void setReference(FeatureMap &)
        """
        ...
    
    @overload
    def setReference(self, in_0: ConsensusMap ) -> None:
        """
        Cython signature: void setReference(ConsensusMap &)
        """
        ...
    
    @overload
    def setReference(self, in_0: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void setReference(libcpp_vector[PeptideIdentification] &)
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


class MapAlignmentEvaluationAlgorithmPrecision:
    """
    Cython implementation of _MapAlignmentEvaluationAlgorithmPrecision

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MapAlignmentEvaluationAlgorithmPrecision.html>`_
      -- Inherits from ['MapAlignmentEvaluationAlgorithm']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MapAlignmentEvaluationAlgorithmPrecision()
        """
        ... 


class MetaboliteFeatureDeconvolution:
    """
    Cython implementation of _MetaboliteFeatureDeconvolution

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaboliteFeatureDeconvolution.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaboliteFeatureDeconvolution()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaboliteFeatureDeconvolution ) -> None:
        """
        Cython signature: void MetaboliteFeatureDeconvolution(MetaboliteFeatureDeconvolution &)
        """
        ...
    
    def compute(self, fm_in: FeatureMap , fm_out: FeatureMap , cons_map: ConsensusMap , cons_map_p: ConsensusMap ) -> None:
        """
        Cython signature: void compute(FeatureMap & fm_in, FeatureMap & fm_out, ConsensusMap & cons_map, ConsensusMap & cons_map_p)
        Compute a zero-charge feature map from a set of charged features
        
        Find putative ChargePairs, then score them and hand over to ILP
        
        
        :param fm_in: Input feature-map
        :param fm_out: Output feature-map (sorted by position and augmented with user params)
        :param cons_map: Output of grouped features belonging to a charge group
        :param cons_map_p: Output of paired features connected by an edge
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
    CHARGEMODE_MFD : __CHARGEMODE_MFD 


class MsInspectFile:
    """
    Cython implementation of _MsInspectFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MsInspectFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MsInspectFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MsInspectFile ) -> None:
        """
        Cython signature: void MsInspectFile(MsInspectFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , feature_map: FeatureMap ) -> None:
        """
        Cython signature: void load(const String & filename, FeatureMap & feature_map)
        Loads a MsInspect file into a featureXML
        
        The content of the file is stored in `features`
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void store(const String & filename, MSSpectrum & spectrum)
        Stores a featureXML as a MsInspect file
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


class NASequence:
    """
    Cython implementation of _NASequence

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NASequence.html>`_

    Representation of an RNA sequence
    This class represents nucleic acid sequences in OpenMS. An NASequence
    instance primarily contains a sequence of ribonucleotides.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void NASequence()
        """
        ...
    
    @overload
    def __init__(self, in_0: NASequence ) -> None:
        """
        Cython signature: void NASequence(NASequence &)
        """
        ...
    
    def getSequence(self) -> List[Ribonucleotide]:
        """
        Cython signature: libcpp_vector[const Ribonucleotide *] getSequence()
        """
        ...
    
    def __getitem__(self, index: int ) -> Ribonucleotide:
        """
        Cython signature: const Ribonucleotide * operator[](size_t index)
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Check if sequence is empty
        """
        ...
    
    def setSequence(self, seq: List[Ribonucleotide] ) -> None:
        """
        Cython signature: void setSequence(const libcpp_vector[const Ribonucleotide *] & seq)
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the peptide as string with modifications embedded in brackets
        """
        ...
    
    def setFivePrimeMod(self, modification: Ribonucleotide ) -> None:
        """
        Cython signature: void setFivePrimeMod(const Ribonucleotide * modification)
        Sets the 5' modification
        """
        ...
    
    def getFivePrimeMod(self) -> Ribonucleotide:
        """
        Cython signature: const Ribonucleotide * getFivePrimeMod()
        Returns the name (ID) of the N-terminal modification, or an empty string if none is set
        """
        ...
    
    def setThreePrimeMod(self, modification: Ribonucleotide ) -> None:
        """
        Cython signature: void setThreePrimeMod(const Ribonucleotide * modification)
        Sets the 3' modification
        """
        ...
    
    def getThreePrimeMod(self) -> Ribonucleotide:
        """
        Cython signature: const Ribonucleotide * getThreePrimeMod()
        """
        ...
    
    def get(self, index: int ) -> Ribonucleotide:
        """
        Cython signature: const Ribonucleotide * get(size_t index)
        Returns the residue at position index
        """
        ...
    
    def set(self, index: int , r: Ribonucleotide ) -> None:
        """
        Cython signature: void set(size_t index, const Ribonucleotide * r)
        Sets the residue at position index
        """
        ...
    
    @overload
    def getFormula(self, ) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula()
        Returns the formula of the peptide
        """
        ...
    
    @overload
    def getFormula(self, type_: int , charge: int ) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula(NASFragmentType type_, int charge)
        """
        ...
    
    @overload
    def getAverageWeight(self, ) -> float:
        """
        Cython signature: double getAverageWeight()
        Returns the average weight of the peptide
        """
        ...
    
    @overload
    def getAverageWeight(self, type_: int , charge: int ) -> float:
        """
        Cython signature: double getAverageWeight(NASFragmentType type_, int charge)
        """
        ...
    
    @overload
    def getMonoWeight(self, ) -> float:
        """
        Cython signature: double getMonoWeight()
        Returns the mono isotopic weight of the peptide
        """
        ...
    
    @overload
    def getMonoWeight(self, type_: int , charge: int ) -> float:
        """
        Cython signature: double getMonoWeight(NASFragmentType type_, int charge)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        Returns the number of residues
        """
        ...
    
    def getPrefix(self, length: int ) -> NASequence:
        """
        Cython signature: NASequence getPrefix(size_t length)
        Returns a peptide sequence of the first index residues
        """
        ...
    
    def getSuffix(self, length: int ) -> NASequence:
        """
        Cython signature: NASequence getSuffix(size_t length)
        Returns a peptide sequence of the last index residues
        """
        ...
    
    def getSubsequence(self, start: int , length: int ) -> NASequence:
        """
        Cython signature: NASequence getSubsequence(size_t start, size_t length)
        Returns a peptide sequence of number residues, beginning at position index
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the peptide as string with modifications embedded in brackets
        """
        ...
    
    def __richcmp__(self, other: NASequence, op: int) -> Any:
        ...
    NASFragmentType : __NASFragmentType
    
    fromString: __static_NASequence_fromString 


class NLargest:
    """
    Cython implementation of _NLargest

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NLargest.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void NLargest()
        """
        ...
    
    @overload
    def __init__(self, in_0: NLargest ) -> None:
        """
        Cython signature: void NLargest(NLargest &)
        """
        ...
    
    def filterSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterSpectrum(MSSpectrum & spec)
        Keep only n-largest peaks in spectrum
        """
        ...
    
    def filterPeakSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrum(MSSpectrum & spec)
        Keep only n-largest peaks in spectrum
        """
        ...
    
    def filterPeakMap(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void filterPeakMap(MSExperiment & exp)
        Keep only n-largest peaks in each spectrum of a peak map
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


class NumpressConfig:
    """
    Cython implementation of _NumpressConfig

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NumpressConfig.html>`_
    """
    
    numpressFixedPoint: float
    
    numpressErrorTolerance: float
    
    np_compression: int
    
    estimate_fixed_point: bool
    
    linear_fp_mass_acc: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void NumpressConfig()
        """
        ...
    
    @overload
    def __init__(self, in_0: NumpressConfig ) -> None:
        """
        Cython signature: void NumpressConfig(NumpressConfig &)
        """
        ...
    
    def setCompression(self, compression: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCompression(const String & compression)
        """
        ... 


class OpenSwathDataAccessHelper:
    """
    Cython implementation of _OpenSwathDataAccessHelper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OpenSwathDataAccessHelper.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OpenSwathDataAccessHelper()
        """
        ...
    
    @overload
    def __init__(self, in_0: OpenSwathDataAccessHelper ) -> None:
        """
        Cython signature: void OpenSwathDataAccessHelper(OpenSwathDataAccessHelper &)
        """
        ...
    
    def convertToOpenMSSpectrum(self, sptr: OSSpectrum , spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void convertToOpenMSSpectrum(shared_ptr[OSSpectrum] sptr, MSSpectrum & spectrum)
        Converts a SpectrumPtr to an OpenMS Spectrum
        """
        ...
    
    def convertToOpenMSChromatogram(self, cptr: OSChromatogram , chromatogram: MSChromatogram ) -> None:
        """
        Cython signature: void convertToOpenMSChromatogram(shared_ptr[OSChromatogram] cptr, MSChromatogram & chromatogram)
        Converts a ChromatogramPtr to an OpenMS Chromatogram
        """
        ...
    
    def convertToOpenMSChromatogramFilter(self, chromatogram: MSChromatogram , cptr: OSChromatogram , rt_min: float , rt_max: float ) -> None:
        """
        Cython signature: void convertToOpenMSChromatogramFilter(MSChromatogram & chromatogram, shared_ptr[OSChromatogram] cptr, double rt_min, double rt_max)
        """
        ...
    
    def convertTargetedExp(self, transition_exp_: TargetedExperiment , transition_exp: LightTargetedExperiment ) -> None:
        """
        Cython signature: void convertTargetedExp(TargetedExperiment & transition_exp_, LightTargetedExperiment & transition_exp)
        Converts from the OpenMS TargetedExperiment to the OpenMs LightTargetedExperiment
        """
        ...
    
    def convertPeptideToAASequence(self, peptide: LightCompound , aa_sequence: AASequence ) -> None:
        """
        Cython signature: void convertPeptideToAASequence(LightCompound & peptide, AASequence & aa_sequence)
        Converts from the LightCompound to an OpenMS AASequence (with correct modifications)
        """
        ...
    
    def convertTargetedCompound(self, pep: Peptide , p: LightCompound ) -> None:
        """
        Cython signature: void convertTargetedCompound(Peptide pep, LightCompound & p)
        Converts from the OpenMS TargetedExperiment Peptide to the LightTargetedExperiment Peptide
        """
        ... 


class PI_PeakArea:
    """
    Cython implementation of _PI_PeakArea

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PI_PeakArea.html>`_
    """
    
    area: float
    
    height: float
    
    apex_pos: float
    
    hull_points: '_np.ndarray[Any, _np.dtype[_np.float32]]'
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PI_PeakArea()
        """
        ...
    
    @overload
    def __init__(self, in_0: PI_PeakArea ) -> None:
        """
        Cython signature: void PI_PeakArea(PI_PeakArea &)
        """
        ... 


class PI_PeakBackground:
    """
    Cython implementation of _PI_PeakBackground

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PI_PeakBackground.html>`_
    """
    
    area: float
    
    height: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PI_PeakBackground()
        """
        ...
    
    @overload
    def __init__(self, in_0: PI_PeakBackground ) -> None:
        """
        Cython signature: void PI_PeakBackground(PI_PeakBackground &)
        """
        ... 


class PI_PeakShapeMetrics:
    """
    Cython implementation of _PI_PeakShapeMetrics

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PI_PeakShapeMetrics.html>`_
    """
    
    width_at_5: float
    
    width_at_10: float
    
    width_at_50: float
    
    start_position_at_5: float
    
    start_position_at_10: float
    
    start_position_at_50: float
    
    end_position_at_5: float
    
    end_position_at_10: float
    
    end_position_at_50: float
    
    total_width: float
    
    tailing_factor: float
    
    asymmetry_factor: float
    
    slope_of_baseline: float
    
    baseline_delta_2_height: float
    
    points_across_baseline: int
    
    points_across_half_height: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PI_PeakShapeMetrics()
        """
        ...
    
    @overload
    def __init__(self, in_0: PI_PeakShapeMetrics ) -> None:
        """
        Cython signature: void PI_PeakShapeMetrics(PI_PeakShapeMetrics &)
        """
        ... 


class PeakIntegrator:
    """
    Cython implementation of _PeakIntegrator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeakIntegrator.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeakIntegrator()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeakIntegrator ) -> None:
        """
        Cython signature: void PeakIntegrator(PeakIntegrator &)
        """
        ...
    
    def getDefaultParameters(self, in_0: Param ) -> None:
        """
        Cython signature: void getDefaultParameters(Param)
        """
        ...
    
    @overload
    def integratePeak(self, chromatogram: MSChromatogram , left: float , right: float ) -> PI_PeakArea:
        """
        Cython signature: PI_PeakArea integratePeak(MSChromatogram & chromatogram, double left, double right)
        """
        ...
    
    @overload
    def integratePeak(self, spectrum: MSSpectrum , left: float , right: float ) -> PI_PeakArea:
        """
        Cython signature: PI_PeakArea integratePeak(MSSpectrum & spectrum, double left, double right)
        """
        ...
    
    @overload
    def estimateBackground(self, chromatogram: MSChromatogram , left: float , right: float , peak_apex_pos: float ) -> PI_PeakBackground:
        """
        Cython signature: PI_PeakBackground estimateBackground(MSChromatogram & chromatogram, double left, double right, double peak_apex_pos)
        """
        ...
    
    @overload
    def estimateBackground(self, spectrum: MSSpectrum , left: float , right: float , peak_apex_pos: float ) -> PI_PeakBackground:
        """
        Cython signature: PI_PeakBackground estimateBackground(MSSpectrum & spectrum, double left, double right, double peak_apex_pos)
        """
        ...
    
    @overload
    def calculatePeakShapeMetrics(self, chromatogram: MSChromatogram , left: float , right: float , peak_height: float , peak_apex_pos: float ) -> PI_PeakShapeMetrics:
        """
        Cython signature: PI_PeakShapeMetrics calculatePeakShapeMetrics(MSChromatogram & chromatogram, double left, double right, double peak_height, double peak_apex_pos)
        """
        ...
    
    @overload
    def calculatePeakShapeMetrics(self, spectrum: MSSpectrum , left: float , right: float , peak_height: float , peak_apex_pos: float ) -> PI_PeakShapeMetrics:
        """
        Cython signature: PI_PeakShapeMetrics calculatePeakShapeMetrics(MSSpectrum & spectrum, double left, double right, double peak_height, double peak_apex_pos)
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


class PepXMLFile:
    """
    Cython implementation of _PepXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PepXMLFile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void PepXMLFile()
        """
        ...
    
    @overload
    def load(self, filename: Union[bytes, str, String] , protein_ids: List[ProteinIdentification] , peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void load(String filename, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ...
    
    @overload
    def load(self, filename: Union[bytes, str, String] , protein_ids: List[ProteinIdentification] , peptide_ids: List[PeptideIdentification] , experiment_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void load(String filename, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids, String experiment_name)
        """
        ...
    
    @overload
    def load(self, filename: Union[bytes, str, String] , protein_ids: List[ProteinIdentification] , peptide_ids: List[PeptideIdentification] , experiment_name: Union[bytes, str, String] , lookup: SpectrumMetaDataLookup ) -> None:
        """
        Cython signature: void load(String filename, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids, String experiment_name, SpectrumMetaDataLookup lookup)
        """
        ...
    
    @overload
    def store(self, filename: Union[bytes, str, String] , protein_ids: List[ProteinIdentification] , peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void store(String filename, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ...
    
    @overload
    def store(self, filename: Union[bytes, str, String] , protein_ids: List[ProteinIdentification] , peptide_ids: List[PeptideIdentification] , mz_file: Union[bytes, str, String] , mz_name: Union[bytes, str, String] , peptideprophet_analyzed: bool , rt_tolerance: float ) -> None:
        """
        Cython signature: void store(String filename, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids, String mz_file, String mz_name, bool peptideprophet_analyzed, double rt_tolerance)
        """
        ...
    
    def keepNativeSpectrumName(self, keep: bool ) -> None:
        """
        Cython signature: void keepNativeSpectrumName(bool keep)
        """
        ...
    
    def setParseUnknownScores(self, parse_unknown_scores: bool ) -> None:
        """
        Cython signature: void setParseUnknownScores(bool parse_unknown_scores)
        """
        ... 


class PercolatorOutfile:
    """
    Cython implementation of _PercolatorOutfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PercolatorOutfile.html>`_

    Class for reading Percolator tab-delimited output files
    
    For PSM-level output, the file extension should be ".psms"
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PercolatorOutfile()
        """
        ...
    
    @overload
    def __init__(self, in_0: PercolatorOutfile ) -> None:
        """
        Cython signature: void PercolatorOutfile(PercolatorOutfile &)
        """
        ...
    
    def getScoreType(self, score_type_name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: PercolatorOutfile_ScoreType getScoreType(String score_type_name)
        Returns a score type given its name
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , proteins: ProteinIdentification , peptides: List[PeptideIdentification] , lookup: SpectrumMetaDataLookup , output_score: int ) -> None:
        """
        Cython signature: void load(const String & filename, ProteinIdentification & proteins, libcpp_vector[PeptideIdentification] & peptides, SpectrumMetaDataLookup & lookup, PercolatorOutfile_ScoreType output_score)
        Loads a Percolator output file
        """
        ...
    PercolatorOutfile_ScoreType : __PercolatorOutfile_ScoreType 


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


class PrecursorPurity:
    """
    Cython implementation of _PrecursorPurity

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PrecursorPurity.html>`_

    Precursor purity or noise estimation
    
    This class computes metrics for precursor isolation window purity (or noise)
    The function extracts the peaks from an isolation window targeted for fragmentation
    and determines which peaks are isotopes of the target and which come from other sources
    The intensities of the assumed target peaks are summed up as the target intensity
    Using this information it calculates an intensity ratio for the relative intensity of the target
    compared to other sources
    These metrics are combined over the previous and the next MS1 spectrum
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PrecursorPurity()
        """
        ...
    
    @overload
    def __init__(self, in_0: PrecursorPurity ) -> None:
        """
        Cython signature: void PrecursorPurity(PrecursorPurity &)
        """
        ...
    
    def computePrecursorPurity(self, ms1: MSSpectrum , pre: Precursor , precursor_mass_tolerance: float , precursor_mass_tolerance_unit_ppm: bool ) -> PurityScores:
        """
        Cython signature: PurityScores computePrecursorPurity(MSSpectrum ms1, Precursor pre, double precursor_mass_tolerance, bool precursor_mass_tolerance_unit_ppm)
        Compute precursor purity metrics for one MS2 precursor
        
        Note: This function is implemented in a general way and can also be used for e.g. MS3 precursor isolation windows in MS2 spectra
        Spectra annotated with charge 0 will be treated as charge 1.
        
        
        :param ms1: The Spectrum containing the isolation window
        :param pre: The precursor containing the definition the isolation window
        :param precursor_mass_tolerance: The precursor tolerance. Is used for determining the targeted peak and deisotoping
        :param precursor_mass_tolerance_unit_ppm: The unit of the precursor tolerance
        """
        ... 


class ProteinHit:
    """
    Cython implementation of _ProteinHit

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteinHit.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProteinHit()
        """
        ...
    
    @overload
    def __init__(self, score: float , rank: int , accession: Union[bytes, str, String] , sequence: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void ProteinHit(double score, unsigned int rank, String accession, String sequence)
        """
        ...
    
    @overload
    def __init__(self, in_0: ProteinHit ) -> None:
        """
        Cython signature: void ProteinHit(ProteinHit &)
        """
        ...
    
    def getScore(self) -> float:
        """
        Cython signature: float getScore()
        Returns the score of the protein hit
        """
        ...
    
    def getRank(self) -> int:
        """
        Cython signature: unsigned int getRank()
        Returns the rank of the protein hit
        """
        ...
    
    def getSequence(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSequence()
        Returns the protein sequence
        """
        ...
    
    def getAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getAccession()
        Returns the accession of the protein
        """
        ...
    
    def getDescription(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getDescription()
        Returns the description of the protein
        """
        ...
    
    def getCoverage(self) -> float:
        """
        Cython signature: double getCoverage()
        Returns the coverage (in percent) of the protein hit based upon matched peptides
        """
        ...
    
    def setScore(self, in_0: float ) -> None:
        """
        Cython signature: void setScore(float)
        Sets the score of the protein hit
        """
        ...
    
    def setRank(self, in_0: int ) -> None:
        """
        Cython signature: void setRank(unsigned int)
        Sets the rank
        """
        ...
    
    def setSequence(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSequence(String)
        Sets the protein sequence
        """
        ...
    
    def setAccession(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAccession(String)
        Sets the accession of the protein
        """
        ...
    
    def setDescription(self, description: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDescription(String description)
        Sets the description of the protein
        """
        ...
    
    def setCoverage(self, in_0: float ) -> None:
        """
        Cython signature: void setCoverage(double)
        Sets the coverage (in percent) of the protein hit based upon matched peptides
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
    
    def __richcmp__(self, other: ProteinHit, op: int) -> Any:
        ... 


class PurityScores:
    """
    Cython implementation of _PurityScores

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PurityScores.html>`_
    """
    
    total_intensity: float
    
    target_intensity: float
    
    signal_proportion: float
    
    target_peak_count: int
    
    interfering_peak_count: int
    
    interfering_peaks: MSSpectrum
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PurityScores()
        """
        ...
    
    @overload
    def __init__(self, in_0: PurityScores ) -> None:
        """
        Cython signature: void PurityScores(PurityScores &)
        """
        ... 


class QcMLFile:
    """
    Cython implementation of _QcMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1QcMLFile.html>`_
      -- Inherits from ['XMLHandler', 'XMLFile', 'ProgressLogger']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void QcMLFile()
        """
        ...
    
    def exportIDstats(self, filename: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String exportIDstats(const String & filename)
        """
        ...
    
    def addRunQualityParameter(self, r: Union[bytes, str, String] , qp: QualityParameter ) -> None:
        """
        Cython signature: void addRunQualityParameter(String r, QualityParameter qp)
        Adds a QualityParameter to run by the name r
        """
        ...
    
    def addRunAttachment(self, r: Union[bytes, str, String] , at: Attachment ) -> None:
        """
        Cython signature: void addRunAttachment(String r, Attachment at)
        Adds a attachment to run by the name r
        """
        ...
    
    def addSetQualityParameter(self, r: Union[bytes, str, String] , qp: QualityParameter ) -> None:
        """
        Cython signature: void addSetQualityParameter(String r, QualityParameter qp)
        Adds a QualityParameter to set by the name r
        """
        ...
    
    def addSetAttachment(self, r: Union[bytes, str, String] , at: Attachment ) -> None:
        """
        Cython signature: void addSetAttachment(String r, Attachment at)
        Adds a attachment to set by the name r
        """
        ...
    
    @overload
    def removeAttachment(self, r: Union[bytes, str, String] , ids: List[bytes] , at: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeAttachment(String r, libcpp_vector[String] & ids, String at)
        Removes attachments referencing an id given in ids, from run/set r. All attachments if no attachment name is given with at
        """
        ...
    
    @overload
    def removeAttachment(self, r: Union[bytes, str, String] , at: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeAttachment(String r, String at)
        Removes attachment with cv accession at from run/set r
        """
        ...
    
    def removeAllAttachments(self, at: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeAllAttachments(String at)
        Removes attachment with cv accession at from all runs/sets
        """
        ...
    
    def removeQualityParameter(self, r: Union[bytes, str, String] , ids: List[bytes] ) -> None:
        """
        Cython signature: void removeQualityParameter(String r, libcpp_vector[String] & ids)
        Removes QualityParameter going by one of the ID attributes given in ids
        """
        ...
    
    def merge(self, addendum: QcMLFile , setname: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void merge(QcMLFile & addendum, String setname)
        Merges the given QCFile into this one
        """
        ...
    
    def collectSetParameter(self, setname: Union[bytes, str, String] , qp: Union[bytes, str, String] , ret: List[bytes] ) -> None:
        """
        Cython signature: void collectSetParameter(String setname, String qp, libcpp_vector[String] & ret)
        Collects the values of given QPs (as CVid) of the given set
        """
        ...
    
    def exportAttachment(self, filename: Union[bytes, str, String] , qpname: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String exportAttachment(String filename, String qpname)
        Returns a String of a tab separated rows if found empty string else from run/set by the name filename of the qualityparameter by the name qpname
        """
        ...
    
    def getRunNames(self, ids: List[bytes] ) -> None:
        """
        Cython signature: void getRunNames(libcpp_vector[String] & ids)
        Gives the names of the registered runs in the vector ids
        """
        ...
    
    def existsRun(self, filename: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool existsRun(String filename)
        Returns true if the given run id is present in this file, if checkname is true it also checks the names
        """
        ...
    
    def existsSet(self, filename: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool existsSet(String filename)
        Returns true if the given set id is present in this file, if checkname is true it also checks the names
        """
        ...
    
    def existsRunQualityParameter(self, filename: Union[bytes, str, String] , qpname: Union[bytes, str, String] , ids: List[bytes] ) -> None:
        """
        Cython signature: void existsRunQualityParameter(String filename, String qpname, libcpp_vector[String] & ids)
        Returns the ids of the parameter name given if found in given run empty else
        """
        ...
    
    def existsSetQualityParameter(self, filename: Union[bytes, str, String] , qpname: Union[bytes, str, String] , ids: List[bytes] ) -> None:
        """
        Cython signature: void existsSetQualityParameter(String filename, String qpname, libcpp_vector[String] & ids)
        Returns the ids of the parameter name given if found in given set, empty else
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(const String & filename)
        Store the qcML file
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void load(const String & filename)
        Load a QCFile
        """
        ...
    
    def registerRun(self, id_: Union[bytes, str, String] , name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void registerRun(String id_, String name)
        Registers a run in the qcml file with the respective mappings
        """
        ...
    
    def registerSet(self, id_: Union[bytes, str, String] , name: Union[bytes, str, String] , names: Set[bytes] ) -> None:
        """
        Cython signature: void registerSet(String id_, String name, libcpp_set[String] & names)
        Registers a set in the qcml file with the respective mappings
        """
        ...
    
    def exportQP(self, filename: Union[bytes, str, String] , qpname: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String exportQP(String filename, String qpname)
        Returns a String value in quotation of a QualityParameter by the name qpname in run/set by the name filename
        """
        ...
    
    def exportQPs(self, filename: Union[bytes, str, String] , qpnames: List[bytes] ) -> Union[bytes, str, String]:
        """
        Cython signature: String exportQPs(String filename, StringList qpnames)
        Returns a String of a tab separated QualityParameter by the name qpname in run/set by the name filename
        """
        ...
    
    def getRunIDs(self, ids: List[bytes] ) -> None:
        """
        Cython signature: void getRunIDs(libcpp_vector[String] & ids)
        Gives the ids of the registered runs in the vector ids
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
    
    def getVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVersion()
        Return the version of the schema
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


class QualityParameter:
    """
    Cython implementation of _QualityParameter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1QualityParameter.html>`_
    """
    
    name: Union[bytes, str, String]
    
    id: Union[bytes, str, String]
    
    value: Union[bytes, str, String]
    
    cvRef: Union[bytes, str, String]
    
    cvAcc: Union[bytes, str, String]
    
    unitRef: Union[bytes, str, String]
    
    unitAcc: Union[bytes, str, String]
    
    flag: Union[bytes, str, String]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void QualityParameter()
        """
        ...
    
    @overload
    def __init__(self, in_0: QualityParameter ) -> None:
        """
        Cython signature: void QualityParameter(QualityParameter &)
        """
        ...
    
    def toXMLString(self, indentation_level: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String toXMLString(unsigned int indentation_level)
        """
        ...
    
    def __richcmp__(self, other: QualityParameter, op: int) -> Any:
        ... 


class RANSAC:
    """
    Cython implementation of _RANSAC[_RansacModelLinear]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1RANSAC[_RansacModelLinear].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RANSAC()
        """
        ...
    
    @overload
    def __init__(self, seed: int ) -> None:
        """
        Cython signature: void RANSAC(uint64_t seed)
        """
        ...
    
    def ransac(self, pairs: List[List[float, float]] , n: int , k: int , t: float , d: int , relative_d: bool ) -> List[List[float, float]]:
        """
        Cython signature: libcpp_vector[libcpp_pair[double,double]] ransac(libcpp_vector[libcpp_pair[double,double]] pairs, size_t n, size_t k, double t, size_t d, bool relative_d)
        """
        ... 


class RANSACParam:
    """
    Cython implementation of _RANSACParam

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1RANSACParam.html>`_
    """
    
    n: int
    
    k: int
    
    t: float
    
    d: int
    
    relative_d: bool
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RANSACParam()
        A simple struct to carry all the parameters required for a RANSAC run
        """
        ...
    
    @overload
    def __init__(self, p_n: int , p_k: int , p_t: float , p_d: int , p_relative_d: bool ) -> None:
        """
        Cython signature: void RANSACParam(size_t p_n, size_t p_k, double p_t, size_t p_d, bool p_relative_d)
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


class RANSACQuadratic:
    """
    Cython implementation of _RANSAC[_RansacModelQuadratic]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1RANSAC[_RansacModelQuadratic].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RANSACQuadratic()
        """
        ...
    
    @overload
    def __init__(self, seed: int ) -> None:
        """
        Cython signature: void RANSACQuadratic(uint64_t seed)
        """
        ...
    
    def ransac(self, pairs: List[List[float, float]] , n: int , k: int , t: float , d: int , relative_d: bool ) -> List[List[float, float]]:
        """
        Cython signature: libcpp_vector[libcpp_pair[double,double]] ransac(libcpp_vector[libcpp_pair[double,double]] pairs, size_t n, size_t k, double t, size_t d, bool relative_d)
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


class RipFileContent:
    """
    Cython implementation of _RipFileContent

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1RipFileContent.html>`_
    """
    
    def __init__(self, prot_idents: List[ProteinIdentification] , pep_idents: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void RipFileContent(libcpp_vector[ProteinIdentification] & prot_idents, libcpp_vector[PeptideIdentification] & pep_idents)
        """
        ...
    
    def getProteinIdentifications(self) -> List[ProteinIdentification]:
        """
        Cython signature: libcpp_vector[ProteinIdentification] getProteinIdentifications()
        """
        ...
    
    def getPeptideIdentifications(self) -> List[PeptideIdentification]:
        """
        Cython signature: libcpp_vector[PeptideIdentification] getPeptideIdentifications()
        """
        ... 


class RipFileIdentifier:
    """
    Cython implementation of _RipFileIdentifier

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1RipFileIdentifier.html>`_
    """
    
    def __init__(self, id_runs: IdentificationRuns , pep_id: PeptideIdentification , file_origin_map: Dict[Union[bytes, str, String], int] , origin_annotation_fmt: int , split_ident_runs: bool ) -> None:
        """
        Cython signature: void RipFileIdentifier(IdentificationRuns & id_runs, PeptideIdentification & pep_id, libcpp_map[String,unsigned int] & file_origin_map, OriginAnnotationFormat origin_annotation_fmt, bool split_ident_runs)
        """
        ...
    
    def getIdentRunIdx(self) -> int:
        """
        Cython signature: unsigned int getIdentRunIdx()
        """
        ...
    
    def getFileOriginIdx(self) -> int:
        """
        Cython signature: unsigned int getFileOriginIdx()
        """
        ...
    
    def getOriginFullname(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOriginFullname()
        """
        ...
    
    def getOutputBasename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOutputBasename()
        """
        ... 


class Sample:
    """
    Cython implementation of _Sample

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Sample.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Sample()
        """
        ...
    
    @overload
    def __init__(self, in_0: Sample ) -> None:
        """
        Cython signature: void Sample(Sample &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        """
        ...
    
    def getOrganism(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOrganism()
        """
        ...
    
    def setOrganism(self, organism: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setOrganism(String organism)
        """
        ...
    
    def getNumber(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNumber()
        Returns the sample number
        """
        ...
    
    def setNumber(self, number: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNumber(String number)
        Sets the sample number (e.g. sample ID)
        """
        ...
    
    def getComment(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getComment()
        Returns the comment (default "")
        """
        ...
    
    def setComment(self, comment: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setComment(String comment)
        Sets the comment (may contain newline characters)
        """
        ...
    
    def getState(self) -> int:
        """
        Cython signature: SampleState getState()
        Returns the state of aggregation (default SAMPLENULL)
        """
        ...
    
    def setState(self, state: int ) -> None:
        """
        Cython signature: void setState(SampleState state)
        Sets the state of aggregation
        """
        ...
    
    def getMass(self) -> float:
        """
        Cython signature: double getMass()
        Returns the mass (in gram) (default 0.0)
        """
        ...
    
    def setMass(self, mass: float ) -> None:
        """
        Cython signature: void setMass(double mass)
        Sets the mass (in gram)
        """
        ...
    
    def getVolume(self) -> float:
        """
        Cython signature: double getVolume()
        Returns the volume (in ml) (default 0.0)
        """
        ...
    
    def setVolume(self, volume: float ) -> None:
        """
        Cython signature: void setVolume(double volume)
        Sets the volume (in ml)
        """
        ...
    
    def getConcentration(self) -> float:
        """
        Cython signature: double getConcentration()
        Returns the concentration (in g/l) (default 0.0)
        """
        ...
    
    def setConcentration(self, concentration: float ) -> None:
        """
        Cython signature: void setConcentration(double concentration)
        Sets the concentration (in g/l)
        """
        ...
    
    def getSubsamples(self) -> List[Sample]:
        """
        Cython signature: libcpp_vector[Sample] getSubsamples()
        Returns a reference to the vector of subsamples that were combined to create this sample
        """
        ...
    
    def setSubsamples(self, subsamples: List[Sample] ) -> None:
        """
        Cython signature: void setSubsamples(libcpp_vector[Sample] subsamples)
        Sets the vector of subsamples that were combined to create this sample
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
    
    def __richcmp__(self, other: Sample, op: int) -> Any:
        ...
    SampleState : __SampleState 


class SemanticValidator:
    """
    Cython implementation of _SemanticValidator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1SemanticValidator.html>`_
    """
    
    def __init__(self, mapping: CVMappings , cv: ControlledVocabulary ) -> None:
        """
        Cython signature: void SemanticValidator(CVMappings mapping, ControlledVocabulary cv)
        """
        ...
    
    def validate(self, filename: Union[bytes, str, String] , errors: List[bytes] , warnings: List[bytes] ) -> bool:
        """
        Cython signature: bool validate(String filename, StringList errors, StringList warnings)
        """
        ...
    
    def locateTerm(self, path: Union[bytes, str, String] , parsed_term: SemanticValidator_CVTerm ) -> bool:
        """
        Cython signature: bool locateTerm(String path, SemanticValidator_CVTerm & parsed_term)
        Checks if a CVTerm is allowed in a given path
        """
        ...
    
    def setTag(self, tag: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTag(String tag)
        Sets the CV parameter tag name (default 'cvParam')
        """
        ...
    
    def setAccessionAttribute(self, accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAccessionAttribute(String accession)
        Sets the name of the attribute for accessions in the CV parameter tag name (default 'accession')
        """
        ...
    
    def setNameAttribute(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNameAttribute(String name)
        Sets the name of the attribute for accessions in the CV parameter tag name (default 'name')
        """
        ...
    
    def setValueAttribute(self, value: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setValueAttribute(String value)
        Sets the name of the attribute for accessions in the CV parameter tag name (default 'value')
        """
        ...
    
    def setCheckTermValueTypes(self, check: bool ) -> None:
        """
        Cython signature: void setCheckTermValueTypes(bool check)
        Sets if CV term value types should be check (enabled by default)
        """
        ...
    
    def setCheckUnits(self, check: bool ) -> None:
        """
        Cython signature: void setCheckUnits(bool check)
        Sets if CV term units should be check (disabled by default)
        """
        ...
    
    def setUnitAccessionAttribute(self, accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setUnitAccessionAttribute(String accession)
        Sets the name of the unit accession attribute (default 'unitAccession')
        """
        ...
    
    def setUnitNameAttribute(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setUnitNameAttribute(String name)
        Sets the name of the unit name attribute (default 'unitName')
        """
        ... 


class SemanticValidator_CVTerm:
    """
    Cython implementation of _SemanticValidator_CVTerm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1SemanticValidator_CVTerm.html>`_
    """
    
    accession: Union[bytes, str, String]
    
    name: Union[bytes, str, String]
    
    value: Union[bytes, str, String]
    
    has_value: bool
    
    unit_accession: Union[bytes, str, String]
    
    has_unit_accession: bool
    
    unit_name: Union[bytes, str, String]
    
    has_unit_name: bool
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SemanticValidator_CVTerm()
        """
        ...
    
    @overload
    def __init__(self, in_0: SemanticValidator_CVTerm ) -> None:
        """
        Cython signature: void SemanticValidator_CVTerm(SemanticValidator_CVTerm &)
        """
        ... 


class SpectrumAccessOpenMS:
    """
    Cython implementation of _SpectrumAccessOpenMS

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumAccessOpenMS.html>`_
      -- Inherits from ['ISpectrumAccess']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMS()
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMS ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMS(SpectrumAccessOpenMS &)
        """
        ...
    
    @overload
    def __init__(self, ms_experiment: MSExperiment ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMS(shared_ptr[MSExperiment] & ms_experiment)
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


class SpectrumAccessTransforming:
    """
    Cython implementation of _SpectrumAccessTransforming

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumAccessTransforming.html>`_
      -- Inherits from ['ISpectrumAccess']
    """
    
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


class SpectrumAlignment:
    """
    Cython implementation of _SpectrumAlignment

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumAlignment.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumAlignment()
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAlignment ) -> None:
        """
        Cython signature: void SpectrumAlignment(SpectrumAlignment &)
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


class TMTEighteenPlexQuantitationMethod:
    """
    Cython implementation of _TMTEighteenPlexQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TMTEighteenPlexQuantitationMethod.html>`_
      -- Inherits from ['IsobaricQuantitationMethod']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TMTEighteenPlexQuantitationMethod()
        """
        ...
    
    @overload
    def __init__(self, in_0: TMTEighteenPlexQuantitationMethod ) -> None:
        """
        Cython signature: void TMTEighteenPlexQuantitationMethod(TMTEighteenPlexQuantitationMethod &)
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


class TransformationXMLFile:
    """
    Cython implementation of _TransformationXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TransformationXMLFile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void TransformationXMLFile()
        """
        ...
    
    def load(self, in_0: Union[bytes, str, String] , in_1: TransformationDescription , fit_model: bool ) -> None:
        """
        Cython signature: void load(String, TransformationDescription &, bool fit_model)
        """
        ...
    
    def store(self, in_0: Union[bytes, str, String] , in_1: TransformationDescription ) -> None:
        """
        Cython signature: void store(String, TransformationDescription)
        """
        ... 


class TransitionTSVFile:
    """
    Cython implementation of _TransitionTSVFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TransitionTSVFile.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TransitionTSVFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: TransitionTSVFile ) -> None:
        """
        Cython signature: void TransitionTSVFile(TransitionTSVFile &)
        """
        ...
    
    def convertTargetedExperimentToTSV(self, filename: bytes , targeted_exp: TargetedExperiment ) -> None:
        """
        Cython signature: void convertTargetedExperimentToTSV(char * filename, TargetedExperiment & targeted_exp)
        Write out a targeted experiment (TraML structure) into a tsv file
        """
        ...
    
    @overload
    def convertTSVToTargetedExperiment(self, filename: bytes , filetype: int , targeted_exp: TargetedExperiment ) -> None:
        """
        Cython signature: void convertTSVToTargetedExperiment(char * filename, FileType filetype, TargetedExperiment & targeted_exp)
        Read in a tsv/mrm file and construct a targeted experiment (TraML structure)
        """
        ...
    
    @overload
    def convertTSVToTargetedExperiment(self, filename: bytes , filetype: int , targeted_exp: LightTargetedExperiment ) -> None:
        """
        Cython signature: void convertTSVToTargetedExperiment(char * filename, FileType filetype, LightTargetedExperiment & targeted_exp)
        Read in a tsv file and construct a targeted experiment (Light transition structure)
        """
        ...
    
    def validateTargetedExperiment(self, targeted_exp: TargetedExperiment ) -> None:
        """
        Cython signature: void validateTargetedExperiment(TargetedExperiment targeted_exp)
        Validate a TargetedExperiment (check that all ids are unique)
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


class WindowMower:
    """
    Cython implementation of _WindowMower

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1WindowMower.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void WindowMower()
        """
        ...
    
    @overload
    def __init__(self, in_0: WindowMower ) -> None:
        """
        Cython signature: void WindowMower(WindowMower &)
        """
        ...
    
    def filterPeakSpectrumForTopNInSlidingWindow(self, spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrumForTopNInSlidingWindow(MSSpectrum & spectrum)
        Sliding window version (slower)
        """
        ...
    
    def filterPeakSpectrumForTopNInJumpingWindow(self, spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrumForTopNInJumpingWindow(MSSpectrum & spectrum)
        Jumping window version (faster)
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


class XQuestResultXMLFile:
    """
    Cython implementation of _XQuestResultXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1XQuestResultXMLFile.html>`_
      -- Inherits from ['XMLFile']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void XQuestResultXMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: XQuestResultXMLFile ) -> None:
        """
        Cython signature: void XQuestResultXMLFile(XQuestResultXMLFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , pep_ids: List[PeptideIdentification] , prot_ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void load(const String & filename, libcpp_vector[PeptideIdentification] & pep_ids, libcpp_vector[ProteinIdentification] & prot_ids)
        Load the content of the xquest.xml file into the provided data structures
        
        :param filename: Filename of the file which is to be loaded
        :param pep_ids: Where the spectra with identifications of the input file will be loaded to
        :param prot_ids: Where the protein identification of the input file will be loaded to
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , poid: List[ProteinIdentification] , peid: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void store(const String & filename, libcpp_vector[ProteinIdentification] & poid, libcpp_vector[PeptideIdentification] & peid)
        Stores the identifications in a xQuest XML file
        """
        ...
    
    def getNumberOfHits(self) -> int:
        """
        Cython signature: int getNumberOfHits()
        Returns the total number of hits in the file
        """
        ...
    
    def getMinScore(self) -> float:
        """
        Cython signature: double getMinScore()
        Returns minimum score among the hits in the file
        """
        ...
    
    def getMaxScore(self) -> float:
        """
        Cython signature: double getMaxScore()
        Returns maximum score among the hits in the file
        """
        ...
    
    @overload
    def writeXQuestXMLSpec(self, out_file: Union[bytes, str, String] , base_name: Union[bytes, str, String] , preprocessed_pair_spectra: OPXL_PreprocessedPairSpectra , spectrum_pairs: List[List[int, int]] , all_top_csms: List[List[CrossLinkSpectrumMatch]] , spectra: MSExperiment , test_mode: bool ) -> None:
        """
        Cython signature: void writeXQuestXMLSpec(const String & out_file, const String & base_name, OPXL_PreprocessedPairSpectra preprocessed_pair_spectra, libcpp_vector[libcpp_pair[size_t,size_t]] spectrum_pairs, libcpp_vector[libcpp_vector[CrossLinkSpectrumMatch]] all_top_csms, MSExperiment spectra, const bool & test_mode)
        Writes spec.xml output containing matching peaks between heavy and light spectra after comparing and filtering
        
        :param out_file: Path and filename for the output file
        :param base_name: The base_name should be the name of the input spectra file without the file ending. Used as part of an identifier string for the spectra
        :param preprocessed_pair_spectra: The preprocessed spectra after comparing and filtering
        :param spectrum_pairs: Indices of spectrum pairs in the input map
        :param all_top_csms: CrossLinkSpectrumMatches, from which the IDs were generated. Only spectra with matches are written out
        :param spectra: The spectra, that were searched as a PeakMap. The indices in spectrum_pairs correspond to spectra in this map
        """
        ...
    
    @overload
    def writeXQuestXMLSpec(self, out_file: Union[bytes, str, String] , base_name: Union[bytes, str, String] , all_top_csms: List[List[CrossLinkSpectrumMatch]] , spectra: MSExperiment , test_mode: bool ) -> None:
        """
        Cython signature: void writeXQuestXMLSpec(const String & out_file, const String & base_name, libcpp_vector[libcpp_vector[CrossLinkSpectrumMatch]] all_top_csms, MSExperiment spectra, const bool & test_mode)
        Writes spec.xml output containing spectra for visualization. This version of the function is meant to be used for label-free linkers
        
        :param out_file: Path and filename for the output file
        :param base_name: The base_name should be the name of the input spectra file without the file ending. Used as part of an identifier string for the spectra
        :param all_top_csms: CrossLinkSpectrumMatches, from which the IDs were generated. Only spectra with matches are written out
        :param spectra: The spectra, that were searched as a PeakMap
        """
        ...
    
    def getVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVersion()
        Return the version of the schema
        """
        ... 


class AnnotationState:
    None
    FEATURE_ID_NONE : int
    FEATURE_ID_SINGLE : int
    FEATURE_ID_MULTIPLE_SAME : int
    FEATURE_ID_MULTIPLE_DIVERGENT : int
    SIZE_OF_ANNOTATIONSTATE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __CHARGEMODE_MFD:
    None
    QFROMFEATURE : int
    QHEURISTIC : int
    QALL : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __CombinationsLogic:
    None
    OR : int
    AND : int
    XOR : int

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


class Measure:
    None
    MEASURE_PPM : int
    MEASURE_DA : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __NASFragmentType:
    None
    Full : int
    Internal : int
    FivePrime : int
    ThreePrime : int
    AIon : int
    BIon : int
    CIon : int
    XIon : int
    YIon : int
    ZIon : int
    Precursor : int
    BIonMinusH20 : int
    YIonMinusH20 : int
    BIonMinusNH3 : int
    YIonMinusNH3 : int
    NonIdentified : int
    Unannotated : int
    WIon : int
    AminusB : int
    DIon : int
    SizeOfNASFragmentType : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __NumpressCompression:
    None
    NONE : int
    LINEAR : int
    PIC : int
    SLOF : int
    SIZE_OF_NUMPRESSCOMPRESSION : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class OriginAnnotationFormat:
    None
    FILE_ORIGIN : int
    MAP_INDEX : int
    ID_MERGE_INDEX : int
    UNKNOWN_OAF : int
    SIZE_OF_ORIGIN_ANNOTATION_FORMAT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __PercolatorOutfile_ScoreType:
    None
    QVALUE : int
    POSTERRPROB : int
    SCORE : int
    SIZE_OF_SCORETYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __RequirementLevel:
    None
    MUST : int
    SHOULD : int
    MAY : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __SampleState:
    None
    SAMPLENULL : int
    SOLID : int
    LIQUID : int
    GAS : int
    SOLUTION : int
    EMULSION : int
    SUSPENSION : int
    SIZE_OF_SAMPLESTATE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class XRefType_CVTerm_ControlledVocabulary:
    None
    XSD_STRING : int
    XSD_INTEGER : int
    XSD_DECIMAL : int
    XSD_NEGATIVE_INTEGER : int
    XSD_POSITIVE_INTEGER : int
    XSD_NON_NEGATIVE_INTEGER : int
    XSD_NON_POSITIVE_INTEGER : int
    XSD_BOOLEAN : int
    XSD_DATE : int
    XSD_ANYURI : int
    NONE : int

    def getMapping(self) -> Dict[int, str]:
       ... 

