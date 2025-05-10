from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_SpectrumMetaDataLookup_addMissingIMToPeptideIDs(in_0: List[PeptideIdentification] , exp: MSExperiment ) -> bool:
    """
    Cython signature: bool addMissingIMToPeptideIDs(libcpp_vector[PeptideIdentification], MSExperiment exp)
    """
    ...

def __static_SpectrumMetaDataLookup_addMissingRTsToPeptideIDs(in_0: List[PeptideIdentification] , exp: MSExperiment ) -> bool:
    """
    Cython signature: bool addMissingRTsToPeptideIDs(libcpp_vector[PeptideIdentification], MSExperiment exp)
    """
    ...

def __static_SpectrumMetaDataLookup_addMissingSpectrumReferences(in_0: List[PeptideIdentification] , filename: Union[bytes, str, String] , stop_on_error: bool , override_spectra_data: bool , override_spectra_references: bool , proteins: List[ProteinIdentification] ) -> bool:
    """
    Cython signature: bool addMissingSpectrumReferences(libcpp_vector[PeptideIdentification], String filename, bool stop_on_error, bool override_spectra_data, bool override_spectra_references, libcpp_vector[ProteinIdentification] proteins)
    """
    ...

def __static_AASequence_fromString(s: Union[bytes, str, String] ) -> AASequence:
    """
    Cython signature: AASequence fromString(String s)
        deprecated. Use AASequence(String) instead.
    """
    ...

def __static_AASequence_fromStringPermissive(s: Union[bytes, str, String] , permissive: bool ) -> AASequence:
    """
    Cython signature: AASequence fromStringPermissive(String s, bool permissive)
        deprecated. Use AASequence(String, bool) instead.
    """
    ...

def __static_TransformationModelBSpline_getDefaultParameters(params: Param ) -> None:
    """
    Cython signature: void getDefaultParameters(Param & params)
    """
    ...

def __static_SpectrumMetaDataLookup_getSpectrumMetaData(spectrum: MSSpectrum , meta: SpectrumMetaData ) -> None:
    """
    Cython signature: void getSpectrumMetaData(MSSpectrum spectrum, SpectrumMetaData & meta)
    """
    ...

def __static_ChromatogramExtractor_prepare_coordinates(output_chromatograms: List[OSChromatogram] , extraction_coordinates: List[ExtractionCoordinates] , targeted: TargetedExperiment , rt_extraction_window: float , ms1: bool , ms1_isotopes: int ) -> None:
    """
    Cython signature: void prepare_coordinates(libcpp_vector[shared_ptr[OSChromatogram]] & output_chromatograms, libcpp_vector[ExtractionCoordinates] & extraction_coordinates, TargetedExperiment & targeted, double rt_extraction_window, bool ms1, int ms1_isotopes)
    """
    ...

def __static_IMTypes_toDriftTimeUnit(dtu_string: bytes ) -> int:
    """
    Cython signature: DriftTimeUnit toDriftTimeUnit(const libcpp_string & dtu_string)
    """
    ...

def __static_IMTypes_toIMFormat(IM_format: bytes ) -> int:
    """
    Cython signature: IMFormat toIMFormat(const libcpp_string & IM_format)
    """
    ...

def __static_IMTypes_toString(value: int ) -> bytes:
    """
    Cython signature: libcpp_string toString(const DriftTimeUnit value)
    """
    ...

def __static_IMTypes_toString(value: int ) -> bytes:
    """
    Cython signature: libcpp_string toString(const IMFormat value)
    """
    ...


class AASeqWithMass:
    """
    Cython implementation of _AASeqWithMass

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AASeqWithMass.html>`_
    """
    
    peptide_mass: float
    
    peptide_seq: AASequence
    
    position: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AASeqWithMass()
        """
        ...
    
    @overload
    def __init__(self, in_0: AASeqWithMass ) -> None:
        """
        Cython signature: void AASeqWithMass(AASeqWithMass &)
        """
        ... 


class AASequence:
    """
    Cython implementation of _AASequence

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AASequence.html>`_

    Representation of a peptide/protein sequence
    This class represents amino acid sequences in OpenMS. An AASequence
    instance primarily contains a sequence of residues.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AASequence()
        """
        ...
    
    @overload
    def __init__(self, in_0: AASequence ) -> None:
        """
        Cython signature: void AASequence(AASequence &)
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void AASequence(const String &)
        Constructor from amino acid sequence (e.g. "PEPTM(Oxidatio)IDE")
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[bytes, str, String] , permissive: bool ) -> None:
        """
        Cython signature: void AASequence(const String &, bool permissive)
        Constructor from amino acid sequence (e.g. "PEPTM(Oxidatio)IDE"), permissive allows for '+', '*', and '#' in the sequence
        """
        ...
    
    def __add__(self: AASequence, other: AASequence) -> AASequence:
        ...
    
    def __iadd__(self: AASequence, other: AASequence) -> AASequence:
        ...
    
    def __getitem__(self, in_0: int ) -> Residue:
        """
        Cython signature: Residue operator[](size_t)
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Check if sequence is empty
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the peptide as string with modifications embedded in brackets
        """
        ...
    
    def toUnmodifiedString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toUnmodifiedString()
        Returns the peptide as string without any modifications
        """
        ...
    
    def toUniModString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toUniModString()
        Returns the peptide as string with UniMod-style modifications embedded in brackets
        """
        ...
    
    @overload
    def toBracketString(self, ) -> Union[bytes, str, String]:
        """
        Cython signature: String toBracketString()
        Create a TPP compatible string of the modified sequence using bracket notation. Uses integer mass by default
        """
        ...
    
    @overload
    def toBracketString(self, integer_mass: bool ) -> Union[bytes, str, String]:
        """
        Cython signature: String toBracketString(bool integer_mass)
        Create a TPP compatible string of the modified sequence using bracket notation
        """
        ...
    
    @overload
    def toBracketString(self, integer_mass: bool , mass_delta: bool ) -> Union[bytes, str, String]:
        """
        Cython signature: String toBracketString(bool integer_mass, bool mass_delta)
        Create a TPP compatible string of the modified sequence using bracket notation.
        """
        ...
    
    @overload
    def toBracketString(self, integer_mass: bool , mass_delta: bool , fixed_modifications: List[bytes] ) -> Union[bytes, str, String]:
        """
        Cython signature: String toBracketString(bool integer_mass, bool mass_delta, libcpp_vector[String] fixed_modifications)
        Create a TPP compatible string of the modified sequence using bracket notation
        """
        ...
    
    @overload
    def setModification(self, index: int , modification: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setModification(size_t index, const String & modification)
        Sets the modification of the residue at position index. If an empty string is passed replaces the residue with its unmodified version
        """
        ...
    
    @overload
    def setModification(self, index: int , modification: ResidueModification ) -> None:
        """
        Cython signature: void setModification(size_t index, const ResidueModification & modification)
        Sets the modification of AA at index by providing a ResidueModification object. Stricter than just looking for the name and adds the Modification to the DB if not present
        """
        ...
    
    def setModificationByDiffMonoMass(self, index: int , diffMonoMass: float ) -> None:
        """
        Cython signature: void setModificationByDiffMonoMass(size_t index, double diffMonoMass)
        Modifies the residue at index in the sequence and potentially in the ResidueDB
        """
        ...
    
    @overload
    def setNTerminalModification(self, modification: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNTerminalModification(String modification)
        Sets the N-terminal modification (by lookup in the mod names of the ModificationsDB). Throws if nothing is found (since the name is not enough information to create a new mod)
        """
        ...
    
    @overload
    def setNTerminalModification(self, mod: ResidueModification ) -> None:
        """
        Cython signature: void setNTerminalModification(const ResidueModification & mod)
        Sets the N-terminal modification (copies and adds to database if not present)
        """
        ...
    
    def setNTerminalModificationByDiffMonoMass(self, diffMonoMass: float , protein_term: bool ) -> None:
        """
        Cython signature: void setNTerminalModificationByDiffMonoMass(double diffMonoMass, bool protein_term)
        Sets the N-terminal modification by the monoisotopic mass difference it introduces (creates a "user-defined" mod if not present)
        """
        ...
    
    @overload
    def setCTerminalModification(self, modification: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCTerminalModification(String modification)
        Sets the C-terminal modification (by lookup in the mod names of the ModificationsDB). Throws if nothing is found (since the name is not enough information to create a new mod)
        """
        ...
    
    @overload
    def setCTerminalModification(self, mod: ResidueModification ) -> None:
        """
        Cython signature: void setCTerminalModification(const ResidueModification & mod)
        Sets the C-terminal modification (copies and adds to database if not present)
        """
        ...
    
    def setCTerminalModificationByDiffMonoMass(self, diffMonoMass: float , protein_term: bool ) -> None:
        """
        Cython signature: void setCTerminalModificationByDiffMonoMass(double diffMonoMass, bool protein_term)
        Sets the C-terminal modification by the monoisotopic mass difference it introduces (creates a "user-defined" mod if not present)
        """
        ...
    
    def getNTerminalModificationName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNTerminalModificationName()
        Returns the name (ID) of the N-terminal modification, or an empty string if none is set
        """
        ...
    
    def getNTerminalModification(self) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getNTerminalModification()
        Returns a copy of the name N-terminal modification object, or None
        """
        ...
    
    def getCTerminalModificationName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCTerminalModificationName()
        Returns the name (ID) of the C-terminal modification, or an empty string if none is set
        """
        ...
    
    def getCTerminalModification(self) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getCTerminalModification()
        Returns a copy of the name C-terminal modification object, or None
        """
        ...
    
    def getResidue(self, index: int ) -> Residue:
        """
        Cython signature: Residue getResidue(size_t index)
        Returns the residue at position index
        """
        ...
    
    @overload
    def getFormula(self, ) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula()
        Convenience function with ResidueType=Full and charge = 0 by default
        """
        ...
    
    @overload
    def getFormula(self, type_: int , charge: int ) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula(ResidueType type_, int charge)
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
        Cython signature: double getAverageWeight(ResidueType type_, int charge)
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
        Cython signature: double getMonoWeight(ResidueType type_, int charge)
        """
        ...
    
    @overload
    def getMZ(self, charge: int ) -> float:
        """
        Cython signature: double getMZ(int charge)
        Returns the mass-to-charge ratio of the peptide
        """
        ...
    
    @overload
    def getMZ(self, charge: int , type_: int ) -> float:
        """
        Cython signature: double getMZ(int charge, ResidueType type_)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        Returns the number of residues
        """
        ...
    
    def getPrefix(self, index: int ) -> AASequence:
        """
        Cython signature: AASequence getPrefix(size_t index)
        Returns a peptide sequence of the first index residues
        """
        ...
    
    def getSuffix(self, index: int ) -> AASequence:
        """
        Cython signature: AASequence getSuffix(size_t index)
        Returns a peptide sequence of the last index residues
        """
        ...
    
    def getSubsequence(self, index: int , number: int ) -> AASequence:
        """
        Cython signature: AASequence getSubsequence(size_t index, unsigned int number)
        Returns a peptide sequence of number residues, beginning at position index
        """
        ...
    
    def has(self, residue: Residue ) -> bool:
        """
        Cython signature: bool has(Residue residue)
        Returns true if the peptide contains the given residue
        """
        ...
    
    def hasSubsequence(self, peptide: AASequence ) -> bool:
        """
        Cython signature: bool hasSubsequence(AASequence peptide)
        Returns true if the peptide contains the given peptide
        """
        ...
    
    def hasPrefix(self, peptide: AASequence ) -> bool:
        """
        Cython signature: bool hasPrefix(AASequence peptide)
        Returns true if the peptide has the given prefix
        """
        ...
    
    def hasSuffix(self, peptide: AASequence ) -> bool:
        """
        Cython signature: bool hasSuffix(AASequence peptide)
        Returns true if the peptide has the given suffix
        """
        ...
    
    def hasNTerminalModification(self) -> bool:
        """
        Cython signature: bool hasNTerminalModification()
        Predicate which is true if the peptide is N-term modified
        """
        ...
    
    def hasCTerminalModification(self) -> bool:
        """
        Cython signature: bool hasCTerminalModification()
        Predicate which is true if the peptide is C-term modified
        """
        ...
    
    def isModified(self) -> bool:
        """
        Cython signature: bool isModified()
        Returns true if any of the residues or termini are modified
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the peptide as string with modifications embedded in brackets
        """
        ...
    
    def __richcmp__(self, other: AASequence, op: int) -> Any:
        ...
    
    fromString: __static_AASequence_fromString
    
    fromStringPermissive: __static_AASequence_fromStringPermissive 


class AccurateMassSearchEngine:
    """
    Cython implementation of _AccurateMassSearchEngine

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AccurateMassSearchEngine.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AccurateMassSearchEngine()
        """
        ...
    
    @overload
    def __init__(self, in_0: AccurateMassSearchEngine ) -> None:
        """
        Cython signature: void AccurateMassSearchEngine(AccurateMassSearchEngine &)
        """
        ...
    
    def queryByMZ(self, observed_mz: float , observed_charge: int , ion_mode: Union[bytes, str, String] , in_3: List[AccurateMassSearchResult] , observed_adduct: EmpiricalFormula ) -> None:
        """
        Cython signature: void queryByMZ(double observed_mz, int observed_charge, String ion_mode, libcpp_vector[AccurateMassSearchResult] &, EmpiricalFormula & observed_adduct)
        """
        ...
    
    def queryByFeature(self, feature: Feature , feature_index: int , ion_mode: Union[bytes, str, String] , in_3: List[AccurateMassSearchResult] ) -> None:
        """
        Cython signature: void queryByFeature(Feature feature, size_t feature_index, String ion_mode, libcpp_vector[AccurateMassSearchResult] &)
        """
        ...
    
    def queryByConsensusFeature(self, cfeat: ConsensusFeature , cf_index: int , number_of_maps: int , ion_mode: Union[bytes, str, String] , results: List[AccurateMassSearchResult] ) -> None:
        """
        Cython signature: void queryByConsensusFeature(ConsensusFeature cfeat, size_t cf_index, size_t number_of_maps, String ion_mode, libcpp_vector[AccurateMassSearchResult] & results)
        """
        ...
    
    @overload
    def run(self, in_0: FeatureMap , in_1: MzTab ) -> None:
        """
        Cython signature: void run(FeatureMap &, MzTab &)
        """
        ...
    
    @overload
    def run(self, in_0: FeatureMap , in_1: MzTabM ) -> None:
        """
        Cython signature: void run(FeatureMap &, MzTabM &)
        """
        ...
    
    @overload
    def run(self, in_0: ConsensusMap , in_1: MzTab ) -> None:
        """
        Cython signature: void run(ConsensusMap &, MzTab &)
        """
        ...
    
    def init(self) -> None:
        """
        Cython signature: void init()
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


class Acquisition:
    """
    Cython implementation of _Acquisition

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Acquisition.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Acquisition()
        """
        ...
    
    @overload
    def __init__(self, in_0: Acquisition ) -> None:
        """
        Cython signature: void Acquisition(Acquisition &)
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        """
        ...
    
    def setIdentifier(self, identifier: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(const String & identifier)
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
    
    def __richcmp__(self, other: Acquisition, op: int) -> Any:
        ... 


class CVTermList:
    """
    Cython implementation of _CVTermList

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVTermList.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVTermList()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVTermList ) -> None:
        """
        Cython signature: void CVTermList(CVTermList &)
        """
        ...
    
    def setCVTerms(self, terms: List[CVTerm] ) -> None:
        """
        Cython signature: void setCVTerms(libcpp_vector[CVTerm] & terms)
        Sets the CV terms
        """
        ...
    
    def replaceCVTerm(self, term: CVTerm ) -> None:
        """
        Cython signature: void replaceCVTerm(CVTerm & term)
        Replaces the specified CV term
        """
        ...
    
    def replaceCVTerms(self, cv_terms: List[CVTerm] , accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void replaceCVTerms(libcpp_vector[CVTerm] cv_terms, String accession)
        """
        ...
    
    def consumeCVTerms(self, cv_term_map: Dict[bytes,List[CVTerm]] ) -> None:
        """
        Cython signature: void consumeCVTerms(libcpp_map[String,libcpp_vector[CVTerm]] cv_term_map)
        Merges the given map into the member map, no duplicate checking
        """
        ...
    
    def getCVTerms(self) -> Dict[bytes,List[CVTerm]]:
        """
        Cython signature: libcpp_map[String,libcpp_vector[CVTerm]] getCVTerms()
        Returns the accession string of the term
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
        Cython signature: bool hasCVTerm(String accession)
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
    
    def __richcmp__(self, other: CVTermList, op: int) -> Any:
        ... 


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


class ClusterProxyKD:
    """
    Cython implementation of _ClusterProxyKD

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ClusterProxyKD.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ClusterProxyKD()
        """
        ...
    
    @overload
    def __init__(self, in_0: ClusterProxyKD ) -> None:
        """
        Cython signature: void ClusterProxyKD(ClusterProxyKD &)
        """
        ...
    
    @overload
    def __init__(self, size: int , avg_distance: float , center_index: int ) -> None:
        """
        Cython signature: void ClusterProxyKD(size_t size, double avg_distance, size_t center_index)
        """
        ...
    
    def getSize(self) -> int:
        """
        Cython signature: size_t getSize()
        """
        ...
    
    def isValid(self) -> bool:
        """
        Cython signature: bool isValid()
        """
        ...
    
    def getAvgDistance(self) -> float:
        """
        Cython signature: double getAvgDistance()
        """
        ...
    
    def getCenterIndex(self) -> int:
        """
        Cython signature: size_t getCenterIndex()
        """
        ...
    
    def __richcmp__(self, other: ClusterProxyKD, op: int) -> Any:
        ... 


class ColumnHeader:
    """
    Cython implementation of _ColumnHeader

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ConsensusMap_1_1ColumnHeader.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    filename: Union[bytes, str, String]
    
    label: Union[bytes, str, String]
    
    size: int
    
    unique_id: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ColumnHeader()
        """
        ...
    
    @overload
    def __init__(self, in_0: ColumnHeader ) -> None:
        """
        Cython signature: void ColumnHeader(ColumnHeader &)
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
    
    def __richcmp__(self, other: ColumnHeader, op: int) -> Any:
        ... 


class ConfidenceScoring:
    """
    Cython implementation of _ConfidenceScoring

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConfidenceScoring.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ConfidenceScoring()
        """
        ...
    
    @overload
    def __init__(self, in_0: ConfidenceScoring ) -> None:
        """
        Cython signature: void ConfidenceScoring(ConfidenceScoring &)
        """
        ...
    
    def initialize(self, targeted: TargetedExperiment , n_decoys: int , n_transitions: int , trafo: TransformationDescription ) -> None:
        """
        Cython signature: void initialize(TargetedExperiment & targeted, size_t n_decoys, size_t n_transitions, TransformationDescription trafo)
        """
        ...
    
    def initializeGlm(self, intercept: float , rt_coef: float , int_coef: float ) -> None:
        """
        Cython signature: void initializeGlm(double intercept, double rt_coef, double int_coef)
        """
        ...
    
    def scoreMap(self, map: FeatureMap ) -> None:
        """
        Cython signature: void scoreMap(FeatureMap & map)
        Score a feature map -> make sure the class is properly initialized
        """
        ... 


class ConsensusIDAlgorithmBest:
    """
    Cython implementation of _ConsensusIDAlgorithmBest

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithmBest.html>`_
      -- Inherits from ['ConsensusIDAlgorithmIdentity']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusIDAlgorithmBest()
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


class ConsensusMap:
    """
    Cython implementation of _ConsensusMap

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ConsensusMap_1_1ConsensusMap.html>`_
      -- Inherits from ['UniqueIdInterface', 'DocumentIdentifier', 'RangeManagerRtMzInt', 'MetaInfoInterface']

    A container for consensus elements.
    
    A ConsensusMap is a container holding 2-dimensional consensus elements
    (ConsensusFeature) which in turn represent analytes that have been
    quantified across multiple LC-MS/MS experiments. Each analyte in a
    ConsensusFeature is linked to its original LC-MS/MS run, the links are
    maintained by the ConsensusMap class.
    The map is implemented as a vector of elements of type ConsensusFeature.
    
    To be consistent, all maps who are referenced by ConsensusFeature objects
    (through a unique id) need to be registered in this class.
    
    This class supports direct iteration in Python.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ConsensusMap()
        """
        ...
    
    @overload
    def __init__(self, in_0: ConsensusMap ) -> None:
        """
        Cython signature: void ConsensusMap(ConsensusMap &)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: int size()
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        """
        ...
    
    def reserve(self, s: int ) -> None:
        """
        Cython signature: void reserve(size_t s)
        """
        ...
    
    def __getitem__(self, in_0: int ) -> ConsensusFeature:
        """
        Cython signature: ConsensusFeature & operator[](size_t)
        """
        ...
    def __setitem__(self, key: int, value: ConsensusFeature ) -> None:
        """Cython signature: ConsensusFeature & operator[](size_t)"""
        ...
    
    def push_back(self, spec: ConsensusFeature ) -> None:
        """
        Cython signature: void push_back(ConsensusFeature spec)
        """
        ...
    
    def appendRows(self, in_0: ConsensusMap ) -> ConsensusMap:
        """
        Cython signature: ConsensusMap appendRows(ConsensusMap)
        Add consensus map entries as new rows
        """
        ...
    
    def appendColumns(self, in_0: ConsensusMap ) -> ConsensusMap:
        """
        Cython signature: ConsensusMap appendColumns(ConsensusMap)
        Add consensus map entries as new columns
        """
        ...
    
    @overload
    def clear(self, clear_meta_data: bool ) -> None:
        """
        Cython signature: void clear(bool clear_meta_data)
        Clears all data and meta data
        """
        ...
    
    @overload
    def clear(self, ) -> None:
        """
        Cython signature: void clear()
        """
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
        Returns a const reference to the description of the applied data processing
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
        Sets the file paths to the primary MS run (stored in ColumnHeaders)
        """
        ...
    
    @overload
    def setPrimaryMSRunPath(self, s: List[bytes] , e: MSExperiment ) -> None:
        """
        Cython signature: void setPrimaryMSRunPath(StringList & s, MSExperiment & e)
        """
        ...
    
    def getPrimaryMSRunPath(self, toFill: List[bytes] ) -> None:
        """
        Cython signature: void getPrimaryMSRunPath(StringList & toFill)
        Returns the MS run path (stored in ColumnHeaders)
        """
        ...
    
    @overload
    def sortByIntensity(self, reverse: bool ) -> None:
        """
        Cython signature: void sortByIntensity(bool reverse)
        Sorts the peaks according to ascending intensity.
        """
        ...
    
    @overload
    def sortByIntensity(self, ) -> None:
        """
        Cython signature: void sortByIntensity()
        """
        ...
    
    def sortByRT(self) -> None:
        """
        Cython signature: void sortByRT()
        Sorts the peaks according to RT position
        """
        ...
    
    def sortByMZ(self) -> None:
        """
        Cython signature: void sortByMZ()
        Sorts the peaks according to m/z position
        """
        ...
    
    def sortByPosition(self) -> None:
        """
        Cython signature: void sortByPosition()
        Lexicographically sorts the peaks by their position (First RT then m/z)
        """
        ...
    
    @overload
    def sortByQuality(self, reverse: bool ) -> None:
        """
        Cython signature: void sortByQuality(bool reverse)
        Sorts the peaks according to ascending quality.
        """
        ...
    
    @overload
    def sortByQuality(self, ) -> None:
        """
        Cython signature: void sortByQuality()
        """
        ...
    
    def sortBySize(self) -> None:
        """
        Cython signature: void sortBySize()
        Sorts with respect to the size (number of elements)
        """
        ...
    
    def sortByMaps(self) -> None:
        """
        Cython signature: void sortByMaps()
        Sorts with respect to the sets of maps covered by the consensus features (lexicographically)
        """
        ...
    
    def getExperimentType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getExperimentType()
        Non-mutable access to the experiment type
        """
        ...
    
    def setExperimentType(self, experiment_type: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setExperimentType(String experiment_type)
        Mutable access to the experiment type
        """
        ...
    
    def sortPeptideIdentificationsByMapIndex(self) -> None:
        """
        Cython signature: void sortPeptideIdentificationsByMapIndex()
        Sorts PeptideIdentifications of consensus features with respect to their map index.
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
    
    def __richcmp__(self, other: ConsensusMap, op: int) -> Any:
        ...
    
    def __iter__(self) -> ConsensusFeature:
       ... 


class ConsensusMapNormalizerAlgorithmThreshold:
    """
    Cython implementation of _ConsensusMapNormalizerAlgorithmThreshold

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusMapNormalizerAlgorithmThreshold.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusMapNormalizerAlgorithmThreshold()
        """
        ...
    
    def computeCorrelation(self, input_map: ConsensusMap , ratio_threshold: float , acc_filter: Union[bytes, str, String] , desc_filter: Union[bytes, str, String] ) -> List[float]:
        """
        Cython signature: libcpp_vector[double] computeCorrelation(ConsensusMap & input_map, double ratio_threshold, const String & acc_filter, const String & desc_filter)
        Determines the ratio of all maps to the map with the most features
        """
        ...
    
    def normalizeMaps(self, input_map: ConsensusMap , ratios: List[float] ) -> None:
        """
        Cython signature: void normalizeMaps(ConsensusMap & input_map, libcpp_vector[double] & ratios)
        Applies the given ratio to the maps of the consensusMap
        """
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


class FeatureFileOptions:
    """
    Cython implementation of _FeatureFileOptions

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureFileOptions.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureFileOptions()
        Options for loading files containing features.
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureFileOptions ) -> None:
        """
        Cython signature: void FeatureFileOptions(FeatureFileOptions &)
        """
        ...
    
    def setMetadataOnly(self, in_0: bool ) -> None:
        """
        Cython signature: void setMetadataOnly(bool)
        Sets whether or not to load only meta data
        """
        ...
    
    def getMetadataOnly(self) -> bool:
        """
        Cython signature: bool getMetadataOnly()
        Returns whether or not to load only meta data
        """
        ...
    
    def setSizeOnly(self, in_0: bool ) -> None:
        """
        Cython signature: void setSizeOnly(bool)
        Sets whether or not to load only feature count
        """
        ...
    
    def getSizeOnly(self) -> bool:
        """
        Cython signature: bool getSizeOnly()
        Returns whether or not to load only meta data
        """
        ...
    
    def setLoadConvexHull(self, in_0: bool ) -> None:
        """
        Cython signature: void setLoadConvexHull(bool)
        Sets whether or not to load convex hull
        """
        ...
    
    def getLoadConvexHull(self) -> bool:
        """
        Cython signature: bool getLoadConvexHull()
        Returns whether or not to load convex hull
        """
        ...
    
    def setLoadSubordinates(self, in_0: bool ) -> None:
        """
        Cython signature: void setLoadSubordinates(bool)
        Sets whether or not load subordinates
        """
        ...
    
    def getLoadSubordinates(self) -> bool:
        """
        Cython signature: bool getLoadSubordinates()
        Returns whether or not to load subordinates
        """
        ...
    
    def setRTRange(self, range_: DRange1 ) -> None:
        """
        Cython signature: void setRTRange(DRange1 & range_)
        Restricts the range of RT values for peaks to load
        """
        ...
    
    def hasRTRange(self) -> bool:
        """
        Cython signature: bool hasRTRange()
        Returns true if an RT range has been set
        """
        ...
    
    def getRTRange(self) -> DRange1:
        """
        Cython signature: DRange1 getRTRange()
        Returns the RT range
        """
        ...
    
    def setMZRange(self, range_: DRange1 ) -> None:
        """
        Cython signature: void setMZRange(DRange1 & range_)
        Restricts the range of MZ values for peaks to load
        """
        ...
    
    def hasMZRange(self) -> bool:
        """
        Cython signature: bool hasMZRange()
        Returns true if an MZ range has been set
        """
        ...
    
    def getMZRange(self) -> DRange1:
        """
        Cython signature: DRange1 getMZRange()
        Returns the MZ range
        """
        ...
    
    def setIntensityRange(self, range_: DRange1 ) -> None:
        """
        Cython signature: void setIntensityRange(DRange1 & range_)
        Restricts the range of intensity values for peaks to load
        """
        ...
    
    def hasIntensityRange(self) -> bool:
        """
        Cython signature: bool hasIntensityRange()
        Returns true if an intensity range has been set
        """
        ...
    
    def getIntensityRange(self) -> DRange1:
        """
        Cython signature: DRange1 getIntensityRange()
        Returns the intensity range
        """
        ... 


class FeatureFinderIdentificationAlgorithm:
    """
    Cython implementation of _FeatureFinderIdentificationAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureFinderIdentificationAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler']

    Algorithm class for FeatureFinderIdentification
    
    External IDs (peptides_ext, proteins_ext) may be empty,
    in which case no machine learning or FDR estimation will be performed.
    Optional seeds from e.g. untargeted FeatureFinders can be added with
    seeds.
    Results will be written to features .
    Caution: peptide IDs will be shrunk to best hit, FFid metavalues added
    and potential seed IDs added.
    
    Usage:
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureFinderIdentificationAlgorithm()
        """
        ...
    
    @overload
    def run(self, peptides: List[PeptideIdentification] , proteins: List[ProteinIdentification] , peptides_ext: List[PeptideIdentification] , proteins_ext: List[ProteinIdentification] , features: FeatureMap ) -> None:
        """
        Cython signature: void run(libcpp_vector[PeptideIdentification] peptides, libcpp_vector[ProteinIdentification] & proteins, libcpp_vector[PeptideIdentification] peptides_ext, libcpp_vector[ProteinIdentification] proteins_ext, FeatureMap & features)
        Run feature detection
        
        
        :param peptides: Vector of identified peptides
        :param proteins: Vector of identified proteins
        :param peptides_ext: Vector of external identified peptides, can be used to transfer ids from other runs
        :param proteins_ext: Vector of external identified proteins, can be used to transfer ids from other runs
        :param features: Feature detection results will be added here
        """
        ...
    
    @overload
    def run(self, peptides: List[PeptideIdentification] , proteins: List[ProteinIdentification] , peptides_ext: List[PeptideIdentification] , proteins_ext: List[ProteinIdentification] , features: FeatureMap , seeds: FeatureMap ) -> None:
        """
        Cython signature: void run(libcpp_vector[PeptideIdentification] peptides, libcpp_vector[ProteinIdentification] & proteins, libcpp_vector[PeptideIdentification] peptides_ext, libcpp_vector[ProteinIdentification] proteins_ext, FeatureMap & features, FeatureMap & seeds)
        Run feature detection
        
        
        :param peptides: Vector of identified peptides
        :param proteins: Vector of identified proteins
        :param peptides_ext: Vector of external identified peptides, can be used to transfer ids from other runs
        :param proteins_ext: Vector of external identified proteins, can be used to transfer ids from other runs
        :param features: Feature detection results will be added here
        :param seeds: Optional seeds for feature detection from e.g. untargeted FeatureFinders
        """
        ...
    
    @overload
    def run(self, peptides: List[PeptideIdentification] , proteins: List[ProteinIdentification] , peptides_ext: List[PeptideIdentification] , proteins_ext: List[ProteinIdentification] , features: FeatureMap , seeds: FeatureMap , spectra_file: String ) -> None:
        """
        Cython signature: void run(libcpp_vector[PeptideIdentification] peptides, libcpp_vector[ProteinIdentification] & proteins, libcpp_vector[PeptideIdentification] peptides_ext, libcpp_vector[ProteinIdentification] proteins_ext, FeatureMap & features, FeatureMap & seeds, String & spectra_file)
        Run feature detection
        
        
        :param peptides: Vector of identified peptides
        :param proteins: Vector of identified proteins
        :param peptides_ext: Vector of external identified peptides, can be used to transfer ids from other runs
        :param proteins_ext: Vector of external identified proteins, can be used to transfer ids from other runs
        :param features: Feature detection results will be added here
        :param seeds: Optional seeds for feature detection from e.g. untargeted FeatureFinders
        :param spectra_file: Path will be stored in features in case the MSExperiment has no proper primaryMSRunPath
        """
        ...
    
    def runOnCandidates(self, features: FeatureMap ) -> None:
        """
        Cython signature: void runOnCandidates(FeatureMap & features)
        Run feature detection on identified features (e.g. loaded from an IdXML file)
        """
        ...
    
    def setMSData(self, in_0: MSExperiment ) -> None:
        """
        Cython signature: void setMSData(const MSExperiment &)
        Sets ms data
        """
        ...
    
    def getMSData(self) -> MSExperiment:
        """
        Cython signature: MSExperiment getMSData()
        Returns ms data as MSExperiment
        """
        ...
    
    def getChromatograms(self) -> MSExperiment:
        """
        Cython signature: MSExperiment getChromatograms()
        Returns chromatogram data as MSExperiment
        """
        ...
    
    def getLibrary(self) -> TargetedExperiment:
        """
        Cython signature: TargetedExperiment getLibrary()
        Returns constructed assay library
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


class FeatureGroupingAlgorithmUnlabeled:
    """
    Cython implementation of _FeatureGroupingAlgorithmUnlabeled

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureGroupingAlgorithmUnlabeled.html>`_
      -- Inherits from ['FeatureGroupingAlgorithm']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureGroupingAlgorithmUnlabeled()
        """
        ...
    
    def group(self, maps: List[FeatureMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void group(libcpp_vector[FeatureMap] & maps, ConsensusMap & out)
        """
        ...
    
    def addToGroup(self, map_id: int , feature_map: FeatureMap ) -> None:
        """
        Cython signature: void addToGroup(int map_id, FeatureMap feature_map)
        """
        ...
    
    def setReference(self, map_id: int , map: FeatureMap ) -> None:
        """
        Cython signature: void setReference(int map_id, FeatureMap map)
        """
        ...
    
    def getResultMap(self) -> ConsensusMap:
        """
        Cython signature: ConsensusMap getResultMap()
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


class FileTypes:
    """
    Cython implementation of _FileTypes

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FileTypes.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FileTypes()
        Centralizes the file types recognized by FileHandler
        """
        ...
    
    @overload
    def __init__(self, in_0: FileTypes ) -> None:
        """
        Cython signature: void FileTypes(FileTypes &)
        """
        ...
    
    def typeToName(self, t: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String typeToName(FileType t)
        Returns the name/extension of the type
        """
        ...
    
    def typeToMZML(self, t: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String typeToMZML(FileType t)
        Returns the mzML name
        """
        ...
    
    def nameToType(self, name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: FileType nameToType(String name)
        Converts a file type name into a Type
        
        
        :param name: A case-insensitive name (e.g. FASTA or Fasta, etc.)
        """
        ... 


class IDConflictResolverAlgorithm:
    """
    Cython implementation of _IDConflictResolverAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IDConflictResolverAlgorithm.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IDConflictResolverAlgorithm()
        Resolves ambiguous annotations of features with peptide identifications
        """
        ...
    
    @overload
    def __init__(self, in_0: IDConflictResolverAlgorithm ) -> None:
        """
        Cython signature: void IDConflictResolverAlgorithm(IDConflictResolverAlgorithm &)
        """
        ...
    
    @overload
    def resolve(self, features: FeatureMap ) -> None:
        """
        Cython signature: void resolve(FeatureMap & features)
        Resolves ambiguous annotations of features with peptide identifications\n
        
        The the filtered identifications are added to the vector of unassigned peptides
        and also reduced to a single best hit
        
        
        :param keep_matching: Keeps all IDs that match the modified sequence of the best hit in the feature (e.g. keeps all IDs in a ConsensusMap if id'd same across multiple runs)
        """
        ...
    
    @overload
    def resolve(self, features: ConsensusMap ) -> None:
        """
        Cython signature: void resolve(ConsensusMap & features)
        Resolves ambiguous annotations of consensus features with peptide identifications\n
        
        The the filtered identifications are added to the vector of unassigned peptides
        and also reduced to a single best hit
        
        
        :param keep_matching: Keeps all IDs that match the modified sequence of the best hit in the feature (e.g. keeps all IDs in a ConsensusMap if id'd same across multiple runs)
        """
        ...
    
    @overload
    def resolveBetweenFeatures(self, features: FeatureMap ) -> None:
        """
        Cython signature: void resolveBetweenFeatures(FeatureMap & features)
        In a single (feature/consensus) map, features with the same (possibly modified) sequence and charge state may appear\n
        
        This filter removes the peptide sequence annotations from features, if a higher-intensity feature with the same (charge, sequence)
        combination exists in the map. The total number of features remains unchanged. In the final output, each (charge, sequence) combination
        appears only once, i.e. no multiplicities
        """
        ...
    
    @overload
    def resolveBetweenFeatures(self, features: ConsensusMap ) -> None:
        """
        Cython signature: void resolveBetweenFeatures(ConsensusMap & features)
        In a single (feature/consensus) map, features with the same (possibly modified) sequence and charge state may appear\n
        
        This filter removes the peptide sequence annotations from features, if a higher-intensity feature with the same (charge, sequence)
        combination exists in the map. The total number of features remains unchanged. In the final output, each (charge, sequence) combination
        appears only once, i.e. no multiplicities
        """
        ... 


class ILPDCWrapper:
    """
    Cython implementation of _ILPDCWrapper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ILPDCWrapper.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ILPDCWrapper()
        """
        ...
    
    @overload
    def __init__(self, in_0: ILPDCWrapper ) -> None:
        """
        Cython signature: void ILPDCWrapper(ILPDCWrapper &)
        """
        ...
    
    def compute(self, fm: FeatureMap , pairs: List[ChargePair] , verbose_level: int ) -> float:
        """
        Cython signature: double compute(FeatureMap fm, libcpp_vector[ChargePair] & pairs, size_t verbose_level)
        Compute optimal solution and return value of objective function. If the input feature map is empty, a warning is issued and -1 is returned
        """
        ... 


class IMTypes:
    """
    Cython implementation of _IMTypes

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IMTypes.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IMTypes()
        """
        ...
    
    @overload
    def __init__(self, in_0: IMTypes ) -> None:
        """
        Cython signature: void IMTypes(IMTypes &)
        """
        ...
    
    @overload
    def determineIMFormat(self, exp: MSExperiment ) -> int:
        """
        Cython signature: IMFormat determineIMFormat(const MSExperiment & exp)
        """
        ...
    
    @overload
    def determineIMFormat(self, spec: MSSpectrum ) -> int:
        """
        Cython signature: IMFormat determineIMFormat(const MSSpectrum & spec)
        """
        ...
    
    toDriftTimeUnit: __static_IMTypes_toDriftTimeUnit
    
    toIMFormat: __static_IMTypes_toIMFormat
    
    toString: __static_IMTypes_toString
    
    toString: __static_IMTypes_toString 


class KDTreeFeatureNode:
    """
    Cython implementation of _KDTreeFeatureNode

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1KDTreeFeatureNode.html>`_
    """
    
    @overload
    def __init__(self, in_0: KDTreeFeatureNode ) -> None:
        """
        Cython signature: void KDTreeFeatureNode(KDTreeFeatureNode &)
        """
        ...
    
    @overload
    def __init__(self, data: KDTreeFeatureMaps , idx: int ) -> None:
        """
        Cython signature: void KDTreeFeatureNode(KDTreeFeatureMaps * data, size_t idx)
        """
        ...
    
    def __getitem__(self, i: int ) -> float:
        """
        Cython signature: double operator[](size_t i)
        """
        ...
    
    def getIndex(self) -> int:
        """
        Cython signature: size_t getIndex()
        Returns index of corresponding feature in data_
        """
        ... 


class LabeledPairFinder:
    """
    Cython implementation of _LabeledPairFinder

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1LabeledPairFinder.html>`_
      -- Inherits from ['BaseGroupFinder']

    The LabeledPairFinder allows the matching of labeled features (features with a fixed distance)
    
    Finds feature pairs that have a defined distance in RT and m/z in the same map
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void LabeledPairFinder()
        """
        ...
    
    def run(self, input_maps: List[ConsensusMap] , result_map: ConsensusMap ) -> None:
        """
        Cython signature: void run(libcpp_vector[ConsensusMap] & input_maps, ConsensusMap & result_map)
        Runs the LabeledPairFinder algorithm
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


class LinearInterpolation:
    """
    Cython implementation of _LinearInterpolation[double,double]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1LinearInterpolation[double,double].html>`_

    Provides access to linearly interpolated values (and
    derivatives) from discrete data points.  Values beyond the given range
    of data points are implicitly taken as zero.
    
    The input is just a vector of values ("Data").  These are interpreted
    as the y-coordinates at the x-coordinate positions 0,...,data_.size-1.
    
    The interpolated data can also be scaled and shifted in
    the x-dimension by an affine mapping.  That is, we have "inside" and
    "outside" x-coordinates.  The affine mapping can be specified in two
    ways:
    - using setScale() and setOffset(),
    - using setMapping()
    
    By default the identity mapping (scale=1, offset=0) is used.
    
    Using the value() and derivative() methods you can sample linearly
    interpolated values for a given x-coordinate position of the data and
    the derivative of the data
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LinearInterpolation()
        """
        ...
    
    @overload
    def __init__(self, in_0: LinearInterpolation ) -> None:
        """
        Cython signature: void LinearInterpolation(LinearInterpolation &)
        """
        ...
    
    @overload
    def __init__(self, scale: float , offset: float ) -> None:
        """
        Cython signature: void LinearInterpolation(double scale, double offset)
        """
        ...
    
    def value(self, arg_pos: float ) -> float:
        """
        Cython signature: double value(double arg_pos)
        Returns the interpolated value
        """
        ...
    
    def addValue(self, arg_pos: float , arg_value: float ) -> None:
        """
        Cython signature: void addValue(double arg_pos, double arg_value)
        Performs linear resampling. The `arg_value` is split up and added to the data points around `arg_pos`
        """
        ...
    
    def derivative(self, arg_pos: float ) -> float:
        """
        Cython signature: double derivative(double arg_pos)
        Returns the interpolated derivative
        """
        ...
    
    def getData(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] getData()
        Returns the internal random access container from which interpolated values are being sampled
        """
        ...
    
    def setData(self, data: List[float] ) -> None:
        """
        Cython signature: void setData(libcpp_vector[double] & data)
        Assigns data to the internal random access container from which interpolated values are being sampled
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Returns `true` if getData() is empty
        """
        ...
    
    def key2index(self, pos: float ) -> float:
        """
        Cython signature: double key2index(double pos)
        The transformation from "outside" to "inside" coordinates
        """
        ...
    
    def index2key(self, pos: float ) -> float:
        """
        Cython signature: double index2key(double pos)
        The transformation from "inside" to "outside" coordinates
        """
        ...
    
    def getScale(self) -> float:
        """
        Cython signature: double getScale()
        "Scale" is the difference (in "outside" units) between consecutive entries in "Data"
        """
        ...
    
    def setScale(self, scale: float ) -> None:
        """
        Cython signature: void setScale(double & scale)
        "Scale" is the difference (in "outside" units) between consecutive entries in "Data"
        """
        ...
    
    def getOffset(self) -> float:
        """
        Cython signature: double getOffset()
        "Offset" is the point (in "outside" units) which corresponds to "Data[0]"
        """
        ...
    
    def setOffset(self, offset: float ) -> None:
        """
        Cython signature: void setOffset(double & offset)
        "Offset" is the point (in "outside" units) which corresponds to "Data[0]"
        """
        ...
    
    @overload
    def setMapping(self, scale: float , inside: float , outside: float ) -> None:
        """
        Cython signature: void setMapping(double & scale, double & inside, double & outside)
        """
        ...
    
    @overload
    def setMapping(self, inside_low: float , outside_low: float , inside_high: float , outside_high: float ) -> None:
        """
        Cython signature: void setMapping(double & inside_low, double & outside_low, double & inside_high, double & outside_high)
        """
        ...
    
    def getInsideReferencePoint(self) -> float:
        """
        Cython signature: double getInsideReferencePoint()
        """
        ...
    
    def getOutsideReferencePoint(self) -> float:
        """
        Cython signature: double getOutsideReferencePoint()
        """
        ...
    
    def supportMin(self) -> float:
        """
        Cython signature: double supportMin()
        """
        ...
    
    def supportMax(self) -> float:
        """
        Cython signature: double supportMax()
        """
        ... 


class LowessSmoothing:
    """
    Cython implementation of _LowessSmoothing

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1LowessSmoothing.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void LowessSmoothing()
        """
        ...
    
    def smoothData(self, x: List[float] , y: List[float] , y_smoothed: List[float] ) -> None:
        """
        Cython signature: void smoothData(libcpp_vector[double] x, libcpp_vector[double] y, libcpp_vector[double] & y_smoothed)
        Smoothing method that receives x and y coordinates (e.g., RT and intensities) and computes smoothed intensities
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


class MRMIonSeries:
    """
    Cython implementation of _MRMIonSeries

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMIonSeries.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMIonSeries()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMIonSeries ) -> None:
        """
        Cython signature: void MRMIonSeries(MRMIonSeries &)
        """
        ...
    
    def annotateTransitionCV(self, tr: ReactionMonitoringTransition , annotation: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void annotateTransitionCV(ReactionMonitoringTransition & tr, String annotation)
        Annotates transition with CV terms
        
        
        :param tr: The transition to annotate
        :param annotation: The fragment ion annotation
        """
        ...
    
    def annotateTransition(self, tr: ReactionMonitoringTransition , peptide: Peptide , precursor_mz_threshold: float , product_mz_threshold: float , enable_reannotation: bool , fragment_types: List[bytes] , fragment_charges: List[int] , enable_specific_losses: bool , enable_unspecific_losses: bool , round_decPow: int ) -> None:
        """
        Cython signature: void annotateTransition(ReactionMonitoringTransition & tr, Peptide peptide, double precursor_mz_threshold, double product_mz_threshold, bool enable_reannotation, libcpp_vector[String] fragment_types, libcpp_vector[size_t] fragment_charges, bool enable_specific_losses, bool enable_unspecific_losses, int round_decPow)
        Annotates transition
        
        
        :param tr: The transition to annotate
        :param peptide: The corresponding peptide
        :param precursor_mz_threshold: The m/z threshold for annotation of the precursor ion
        :param product_mz_threshold: The m/z threshold for annotation of the fragment ion
        :param enable_reannotation: Whether the original (e.g. SpectraST) annotation should be used or reannotation should be conducted
        :param fragment_types: The fragment ion types for reannotation
        :param fragment_charges: The fragment ion charges for reannotation
        :param enable_specific_losses: Whether specific neutral losses should be considered
        :param enable_unspecific_losses: Whether unspecific neutral losses (H2O1, H3N1, C1H2N2, C1H2N1O1) should be considered
        :param round_decPow: Round precursor and product m/z values to decimal power (default: -4)
        """
        ... 


class MRMScoring:
    """
    Cython implementation of _MRMScoring

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1MRMScoring.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMScoring()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMScoring ) -> None:
        """
        Cython signature: void MRMScoring(MRMScoring &)
        """
        ...
    
    def calcXcorrCoelutionScore(self) -> float:
        """
        Cython signature: double calcXcorrCoelutionScore()
        Calculate the cross-correlation coelution score. The score is a distance where zero indicates perfect coelution
        """
        ...
    
    def calcXcorrCoelutionWeightedScore(self, normalized_library_intensity: List[float] ) -> float:
        """
        Cython signature: double calcXcorrCoelutionWeightedScore(libcpp_vector[double] & normalized_library_intensity)
        Calculate the weighted cross-correlation coelution score
        
        The score is a distance where zero indicates perfect coelution. The
        score is weighted by the transition intensities, non-perfect coelution
        in low-intensity transitions should thus become less important
        """
        ...
    
    def calcSeparateXcorrContrastCoelutionScore(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] calcSeparateXcorrContrastCoelutionScore()
        Calculate the separate cross-correlation contrast score
        """
        ...
    
    def calcXcorrPrecursorContrastCoelutionScore(self) -> float:
        """
        Cython signature: double calcXcorrPrecursorContrastCoelutionScore()
        Calculate the precursor cross-correlation contrast score against the transitions
        
        The score is a distance where zero indicates perfect coelution
        """
        ...
    
    def calcXcorrShapeScore(self) -> float:
        """
        Cython signature: double calcXcorrShapeScore()
        Calculate the cross-correlation shape score
        
        The score is a correlation measure where 1 indicates perfect correlation
        and 0 means no correlation.
        """
        ...
    
    def calcXcorrShapeWeightedScore(self, normalized_library_intensity: List[float] ) -> float:
        """
        Cython signature: double calcXcorrShapeWeightedScore(libcpp_vector[double] & normalized_library_intensity)
        Calculate the weighted cross-correlation shape score
        
        The score is a correlation measure where 1 indicates perfect correlation
        and 0 means no correlation. The score is weighted by the transition
        intensities, non-perfect coelution in low-intensity transitions should
        thus become less important
        """
        ...
    
    def calcSeparateXcorrContrastShapeScore(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] calcSeparateXcorrContrastShapeScore()
        Calculate the separate cross-correlation contrast shape score
        """
        ...
    
    def calcXcorrPrecursorContrastShapeScore(self) -> float:
        """
        Cython signature: double calcXcorrPrecursorContrastShapeScore()
        Calculate the precursor cross-correlation shape score against the transitions
        """
        ...
    
    def calcRTScore(self, peptide: LightCompound , normalized_experimental_rt: float ) -> float:
        """
        Cython signature: double calcRTScore(LightCompound & peptide, double normalized_experimental_rt)
        """
        ...
    
    def calcMIScore(self) -> float:
        """
        Cython signature: double calcMIScore()
        """
        ...
    
    def calcMIWeightedScore(self, normalized_library_intensity: List[float] ) -> float:
        """
        Cython signature: double calcMIWeightedScore(const libcpp_vector[double] & normalized_library_intensity)
        """
        ...
    
    def calcMIPrecursorScore(self) -> float:
        """
        Cython signature: double calcMIPrecursorScore()
        """
        ...
    
    def calcMIPrecursorContrastScore(self) -> float:
        """
        Cython signature: double calcMIPrecursorContrastScore()
        """
        ...
    
    def calcMIPrecursorCombinedScore(self) -> float:
        """
        Cython signature: double calcMIPrecursorCombinedScore()
        """
        ...
    
    def calcSeparateMIContrastScore(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] calcSeparateMIContrastScore()
        """
        ...
    
    def getMIMatrix(self) -> MatrixDouble:
        """
        Cython signature: MatrixDouble getMIMatrix()
        """
        ... 


class MRMTransitionGroupPicker:
    """
    Cython implementation of _MRMTransitionGroupPicker

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMTransitionGroupPicker.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMTransitionGroupPicker()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMTransitionGroupPicker ) -> None:
        """
        Cython signature: void MRMTransitionGroupPicker(MRMTransitionGroupPicker &)
        """
        ...
    
    @overload
    def pickTransitionGroup(self, transition_group: LightMRMTransitionGroupCP ) -> None:
        """
        Cython signature: void pickTransitionGroup(LightMRMTransitionGroupCP transition_group)
        """
        ...
    
    @overload
    def pickTransitionGroup(self, transition_group: MRMTransitionGroupCP ) -> None:
        """
        Cython signature: void pickTransitionGroup(MRMTransitionGroupCP transition_group)
        """
        ...
    
    def createMRMFeature(self, transition_group: LightMRMTransitionGroupCP , picked_chroms: List[MSChromatogram] , smoothed_chroms: List[MSChromatogram] , chr_idx: int , peak_idx: int ) -> MRMFeature:
        """
        Cython signature: MRMFeature createMRMFeature(LightMRMTransitionGroupCP transition_group, libcpp_vector[MSChromatogram] & picked_chroms, libcpp_vector[MSChromatogram] & smoothed_chroms, const int chr_idx, const int peak_idx)
        """
        ...
    
    def remove_overlapping_features(self, picked_chroms: List[MSChromatogram] , best_left: float , best_right: float ) -> None:
        """
        Cython signature: void remove_overlapping_features(libcpp_vector[MSChromatogram] & picked_chroms, double best_left, double best_right)
        """
        ...
    
    def findLargestPeak(self, picked_chroms: List[MSChromatogram] , chr_idx: int , peak_idx: int ) -> None:
        """
        Cython signature: void findLargestPeak(libcpp_vector[MSChromatogram] & picked_chroms, int & chr_idx, int & peak_idx)
        """
        ...
    
    def findWidestPeakIndices(self, picked_chroms: List[MSChromatogram] , chrom_idx: int , point_idx: int ) -> None:
        """
        Cython signature: void findWidestPeakIndices(libcpp_vector[MSChromatogram] & picked_chroms, int & chrom_idx, int & point_idx)
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


class MSDataCachedConsumer:
    """
    Cython implementation of _MSDataCachedConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSDataCachedConsumer.html>`_

    Transforming and cached writing consumer of MS data
    
    Is able to transform a spectrum on the fly while it is read using a
    function pointer that can be set on the object. The spectra is then
    cached to disk using the functions provided in CachedMzMLHandler.
    """
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void MSDataCachedConsumer(String filename)
        """
        ...
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , clear: bool ) -> None:
        """
        Cython signature: void MSDataCachedConsumer(String filename, bool clear)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        Write a spectrum to the output file
        
        May delete data from spectrum (if clearData is set)
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        Write a chromatogram to the output file
        
        May delete data from chromatogram (if clearData is set)
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


class MapConversion:
    """
    Cython implementation of _MapConversion

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MapConversion.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MapConversion()
        """
        ...
    
    @overload
    def __init__(self, in_0: MapConversion ) -> None:
        """
        Cython signature: void MapConversion(MapConversion &)
        """
        ...
    
    @overload
    def convert(self, input_map_index: int , input_map: FeatureMap , output_map: ConsensusMap , n: int ) -> None:
        """
        Cython signature: void convert(uint64_t input_map_index, FeatureMap input_map, ConsensusMap & output_map, size_t n)
        """
        ...
    
    @overload
    def convert(self, input_map_index: int , input_map: MSExperiment , output_map: ConsensusMap , n: int ) -> None:
        """
        Cython signature: void convert(uint64_t input_map_index, MSExperiment & input_map, ConsensusMap & output_map, size_t n)
        """
        ...
    
    @overload
    def convert(self, input_map: ConsensusMap , keep_uids: bool , output_map: FeatureMap ) -> None:
        """
        Cython signature: void convert(ConsensusMap input_map, bool keep_uids, FeatureMap & output_map)
        """
        ... 


class MascotGenericFile:
    """
    Cython implementation of _MascotGenericFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MascotGenericFile.html>`_
      -- Inherits from ['ProgressLogger', 'DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MascotGenericFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MascotGenericFile ) -> None:
        """
        Cython signature: void MascotGenericFile(MascotGenericFile &)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , experiment: MSExperiment ) -> None:
        """
        Cython signature: void store(const String & filename, MSExperiment & experiment)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , exp: MSExperiment ) -> None:
        """
        Cython signature: void load(const String & filename, MSExperiment & exp)
        Loads a Mascot Generic File into a PeakMap
        
        
        :param filename: File name which the map should be read from
        :param exp: The map which is filled with the data from the given file
        :raises:
          Exception: FileNotFound is thrown if the given file could not be found
        """
        ...
    
    def getHTTPPeakListEnclosure(self, filename: Union[bytes, str, String] ) -> List[Union[bytes, str, String], Union[bytes, str, String]]:
        """
        Cython signature: libcpp_pair[String,String] getHTTPPeakListEnclosure(const String & filename)
        Enclosing Strings of the peak list body for HTTP submission\n
        
        Can be used to embed custom content into HTTP submission (when writing only the MGF header in HTTP format and then
        adding the peaks (in whatever format, e.g. mzXML) enclosed in this body
        The `filename` can later be found in the Mascot response
        """
        ...
    
    def updateMembers_(self) -> None:
        """
        Cython signature: void updateMembers_()
        Docu in base class
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


class MascotXMLFile:
    """
    Cython implementation of _MascotXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MascotXMLFile.html>`_
      -- Inherits from ['XMLFile']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MascotXMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MascotXMLFile ) -> None:
        """
        Cython signature: void MascotXMLFile(MascotXMLFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , protein_identification: ProteinIdentification , id_data: List[PeptideIdentification] , rt_mapping: SpectrumMetaDataLookup ) -> None:
        """
        Cython signature: void load(const String & filename, ProteinIdentification & protein_identification, libcpp_vector[PeptideIdentification] & id_data, SpectrumMetaDataLookup & rt_mapping)
        Loads data from a Mascot XML file
        
        
        :param filename: The file to be loaded
        :param protein_identification: Protein identifications belonging to the whole experiment
        :param id_data: The identifications with m/z and RT
        :param lookup: Helper object for looking up spectrum meta data
        :raises:
          Exception: FileNotFound is thrown if the file does not exists
        :raises:
          Exception: ParseError is thrown if the file does not suit to the standard
        """
        ...
    
    def initializeLookup(self, lookup: SpectrumMetaDataLookup , experiment: MSExperiment , scan_regex: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void initializeLookup(SpectrumMetaDataLookup & lookup, MSExperiment & experiment, const String & scan_regex)
        Initializes a helper object for looking up spectrum meta data (RT, m/z)
        
        
        :param lookup: Helper object to initialize
        :param experiment: Experiment containing the spectra
        :param scan_regex: Optional regular expression for extracting information from references to spectra
        """
        ...
    
    def getVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVersion()
        Return the version of the schema
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


class ModificationsDB:
    """
    Cython implementation of _ModificationsDB

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ModificationsDB.html>`_
    """
    
    def getNumberOfModifications(self) -> int:
        """
        Cython signature: size_t getNumberOfModifications()
        Returns the number of modifications read from the unimod.xml file
        """
        ...
    
    def searchModifications(self, mods: Set[ResidueModification] , mod_name: Union[bytes, str, String] , residue: Union[bytes, str, String] , term_spec: int ) -> None:
        """
        Cython signature: void searchModifications(libcpp_set[const ResidueModification *] & mods, const String & mod_name, const String & residue, TermSpecificity term_spec)
        Collects all modifications which have the given name as synonym
        
        If `residue` is set, only modifications with matching residue of origin are considered
        If `term_spec` is set, only modifications with matching term specificity are considered
        The resulting set of modifications will be empty if no modification exists that fulfills the criteria
        """
        ...
    
    @overload
    def getModification(self, index: int ) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getModification(size_t index)
        Returns the modification with the given index
        """
        ...
    
    @overload
    def getModification(self, mod_name: Union[bytes, str, String] ) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getModification(const String & mod_name)
        Returns the modification with the given name
        """
        ...
    
    @overload
    def getModification(self, mod_name: Union[bytes, str, String] , residue: Union[bytes, str, String] , term_spec: int ) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getModification(const String & mod_name, const String & residue, TermSpecificity term_spec)
        Returns the modification with the given arguments
        """
        ...
    
    def has(self, modification: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool has(String modification)
        Returns true if the modification exists
        """
        ...
    
    def addModification(self, new_mod: ResidueModification ) -> ResidueModification:
        """
        Cython signature: const ResidueModification * addModification(const ResidueModification & new_mod)
        Add a new modification to ModificationsDB. If the modification already exists (based on its fullID) it is not added. Returns the modification in the ModificationDB (which can differ from input if mod was already present).
        """
        ...
    
    def findModificationIndex(self, mod_name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t findModificationIndex(const String & mod_name)
        Returns the index of the modification in the mods_ vector; a unique name must be given
        """
        ...
    
    def searchModificationsByDiffMonoMass(self, mods: List[bytes] , mass: float , max_error: float , residue: Union[bytes, str, String] , term_spec: int ) -> None:
        """
        Cython signature: void searchModificationsByDiffMonoMass(libcpp_vector[String] & mods, double mass, double max_error, const String & residue, TermSpecificity term_spec)
        Collects all modifications with delta mass inside a tolerance window
        """
        ...
    
    def getBestModificationByDiffMonoMass(self, mass: float , max_error: float , residue: Union[bytes, str, String] , term_spec: int ) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getBestModificationByDiffMonoMass(double mass, double max_error, const String & residue, TermSpecificity term_spec)
        Returns the best matching modification for the given delta mass and residue
        
        Query the modifications DB to get the best matching modification with
        the given delta mass at the given residue (NULL pointer means no result,
        maybe the maximal error tolerance needs to be increased). Possible
        input for CAM modification would be a delta mass of 57 and a residue
        of "C".
        
        Note: If there are multiple possible matches with equal masses, it
        will choose the _first_ match which defaults to the first matching
        UniMod entry.
        
        
        :param residue: The residue at which the modifications occurs
        :param mass: The monoisotopic mass of the residue including the mass of the modification
        :param max_error: The maximal mass error in the modification search
        :return: A pointer to the best matching modification (or NULL if none was found)
        """
        ...
    
    def getAllSearchModifications(self, modifications: List[bytes] ) -> None:
        """
        Cython signature: void getAllSearchModifications(libcpp_vector[String] & modifications)
        Collects all modifications that can be used for identification searches
        """
        ...
    
    def isInstantiated(self) -> bool:
        """
        Cython signature: bool isInstantiated()
        Check whether ModificationsDB was instantiated before
        """
        ... 


class MzQCFile:
    """
    Cython implementation of _MzQCFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzQCFile.html>`_

    File adapter for mzQC files used to load and store mzQC files
    
    This class collects the data for the mzQC File
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MzQCFile()
        """
        ...
    
    def store(self, input_file: Union[bytes, str, String] , output_file: Union[bytes, str, String] , exp: MSExperiment , contact_name: Union[bytes, str, String] , contact_address: Union[bytes, str, String] , description: Union[bytes, str, String] , label: Union[bytes, str, String] , feature_map: FeatureMap , prot_ids: List[ProteinIdentification] , pep_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void store(String input_file, String output_file, MSExperiment & exp, String contact_name, String contact_address, String description, String label, FeatureMap & feature_map, libcpp_vector[ProteinIdentification] & prot_ids, libcpp_vector[PeptideIdentification] & pep_ids)
        Stores QC data in mzQC file with JSON format
        
        
        :param input_file: MzML input file name
        :param output_file: MzQC output file name
        :param exp: MSExperiment to extract QC data from, prior sortSpectra() and updateRanges() required
        :param contact_name: Name of the person creating the mzQC file
        :param contact_address: Contact address (mail/e-mail or phone) of the person creating the mzQC file
        :param description: Description and comments about the mzQC file contents
        :param label: Qnique and informative label for the run
        :param feature_map: FeatureMap from feature file (featureXML)
        :param prot_ids: Protein identifications from ID file (idXML)
        :param pep_ids: Protein identifications from ID file (idXML)
        """
        ... 


class NoiseEstimator:
    """
    Cython implementation of _NoiseEstimator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NoiseEstimator.html>`_
    """
    
    nr_windows: int
    
    mz_start: float
    
    window_length: float
    
    result_windows_even: List[float]
    
    result_windows_odd: List[float]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void NoiseEstimator()
        """
        ...
    
    @overload
    def __init__(self, in_0: NoiseEstimator ) -> None:
        """
        Cython signature: void NoiseEstimator(NoiseEstimator &)
        """
        ...
    
    @overload
    def __init__(self, nr_windows_: float , mz_start_: float , win_len_: float ) -> None:
        """
        Cython signature: void NoiseEstimator(double nr_windows_, double mz_start_, double win_len_)
        """
        ...
    
    def get_noise_value(self, mz: float ) -> float:
        """
        Cython signature: double get_noise_value(double mz)
        """
        ...
    
    def get_noise_even(self, mz: float ) -> float:
        """
        Cython signature: double get_noise_even(double mz)
        """
        ...
    
    def get_noise_odd(self, mz: float ) -> float:
        """
        Cython signature: double get_noise_odd(double mz)
        """
        ... 


class OPXL_PreprocessedPairSpectra:
    """
    Cython implementation of _OPXL_PreprocessedPairSpectra

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::OPXLDataStructs_1_1OPXL_PreprocessedPairSpectra.html>`_
    """
    
    spectra_linear_peaks: MSExperiment
    
    spectra_xlink_peaks: MSExperiment
    
    spectra_all_peaks: MSExperiment
    
    @overload
    def __init__(self, size: int ) -> None:
        """
        Cython signature: void OPXL_PreprocessedPairSpectra(size_t size)
        """
        ...
    
    @overload
    def __init__(self, in_0: OPXL_PreprocessedPairSpectra ) -> None:
        """
        Cython signature: void OPXL_PreprocessedPairSpectra(OPXL_PreprocessedPairSpectra &)
        """
        ... 


class Peak1D:
    """
    Cython implementation of _Peak1D

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Peak1D.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Peak1D()
        """
        ...
    
    @overload
    def __init__(self, in_0: Peak1D ) -> None:
        """
        Cython signature: void Peak1D(Peak1D &)
        """
        ...
    
    def getIntensity(self) -> float:
        """
        Cython signature: float getIntensity()
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
    
    def setIntensity(self, in_0: float ) -> None:
        """
        Cython signature: void setIntensity(float)
        """
        ...
    
    def getPos(self) -> float:
        """
        Cython signature: double getPos()
        """
        ...
    
    def setPos(self, pos: float ) -> None:
        """
        Cython signature: void setPos(double pos)
        """
        ...
    
    def __richcmp__(self, other: Peak1D, op: int) -> Any:
        ... 


class Precursor:
    """
    Cython implementation of _Precursor

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Precursor.html>`_
      -- Inherits from ['Peak1D', 'CVTermList']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Precursor()
        """
        ...
    
    @overload
    def __init__(self, in_0: Precursor ) -> None:
        """
        Cython signature: void Precursor(Precursor &)
        """
        ...
    
    def getActivationMethods(self) -> Set[int]:
        """
        Cython signature: libcpp_set[ActivationMethod] getActivationMethods()
        Returns the activation methods
        """
        ...
    
    def getActivationMethodsAsString(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getActivationMethodsAsString()
        Returns the full names (e.g., "Collision-induced dissociation") of the activation methods set on this instance
        """
        ...
    
    def getActivationMethodsAsShortString(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getActivationMethodsAsShortString()
        Returns the abbreviations (e.g., "CID") of the activation methods set on this instance
        """
        ...
    
    def setActivationMethods(self, activation_methods: Set[int] ) -> None:
        """
        Cython signature: void setActivationMethods(libcpp_set[ActivationMethod] activation_methods)
        Sets the activation methods
        """
        ...
    
    @staticmethod
    def getAllNamesOfActivationMethods() -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getAllNamesOfActivationMethods()
        Returns the full names (e.g., "Collision-induced dissociation") of ALL possible activation methods, not just those set on this instance
        """
        ...
    
    @staticmethod
    def getAllShortNamesOfActivationMethods() -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getAllShortNamesOfActivationMethods()
        Returns the abbreviations (e.g., "CID") of ALL possible activation methods, not just those set on this instance
        """
        ...
    
    def getActivationEnergy(self) -> float:
        """
        Cython signature: double getActivationEnergy()
        Returns the activation energy (in electronvolt)
        """
        ...
    
    def setActivationEnergy(self, activation_energy: float ) -> None:
        """
        Cython signature: void setActivationEnergy(double activation_energy)
        Sets the activation energy (in electronvolt)
        """
        ...
    
    def getIsolationWindowLowerOffset(self) -> float:
        """
        Cython signature: double getIsolationWindowLowerOffset()
        Returns the lower offset from the target m/z
        """
        ...
    
    def setIsolationWindowLowerOffset(self, bound: float ) -> None:
        """
        Cython signature: void setIsolationWindowLowerOffset(double bound)
        Sets the lower offset from the target m/z
        """
        ...
    
    def getDriftTime(self) -> float:
        """
        Cython signature: double getDriftTime()
        Returns the ion mobility drift time in milliseconds (-1 means it is not set)
        """
        ...
    
    def setDriftTime(self, drift_time: float ) -> None:
        """
        Cython signature: void setDriftTime(double drift_time)
        Sets the ion mobility drift time in milliseconds
        """
        ...
    
    def getIsolationWindowUpperOffset(self) -> float:
        """
        Cython signature: double getIsolationWindowUpperOffset()
        Returns the upper offset from the target m/z
        """
        ...
    
    def setIsolationWindowUpperOffset(self, bound: float ) -> None:
        """
        Cython signature: void setIsolationWindowUpperOffset(double bound)
        Sets the upper offset from the target m/z
        """
        ...
    
    def getDriftTimeWindowLowerOffset(self) -> float:
        """
        Cython signature: double getDriftTimeWindowLowerOffset()
        Returns the lower offset from the target ion mobility in milliseconds
        """
        ...
    
    def setDriftTimeWindowLowerOffset(self, drift_time: float ) -> None:
        """
        Cython signature: void setDriftTimeWindowLowerOffset(double drift_time)
        Sets the lower offset from the target ion mobility
        """
        ...
    
    def getDriftTimeWindowUpperOffset(self) -> float:
        """
        Cython signature: double getDriftTimeWindowUpperOffset()
        Returns the upper offset from the target ion mobility in milliseconds
        """
        ...
    
    def setDriftTimeWindowUpperOffset(self, drift_time: float ) -> None:
        """
        Cython signature: void setDriftTimeWindowUpperOffset(double drift_time)
        Sets the upper offset from the target ion mobility
        """
        ...
    
    def getCharge(self) -> int:
        """
        Cython signature: int getCharge()
        Returns the charge
        """
        ...
    
    def setCharge(self, charge: int ) -> None:
        """
        Cython signature: void setCharge(int charge)
        Sets the charge
        """
        ...
    
    def getPossibleChargeStates(self) -> List[int]:
        """
        Cython signature: libcpp_vector[int] getPossibleChargeStates()
        Returns the possible charge states
        """
        ...
    
    def setPossibleChargeStates(self, possible_charge_states: List[int] ) -> None:
        """
        Cython signature: void setPossibleChargeStates(libcpp_vector[int] possible_charge_states)
        Sets the possible charge states
        """
        ...
    
    def getUnchargedMass(self) -> float:
        """
        Cython signature: double getUnchargedMass()
        Returns the uncharged mass of the precursor, if charge is unknown, i.e. 0 best guess is its doubly charged
        """
        ...
    
    def getIntensity(self) -> float:
        """
        Cython signature: float getIntensity()
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
    
    def setIntensity(self, in_0: float ) -> None:
        """
        Cython signature: void setIntensity(float)
        """
        ...
    
    def getPos(self) -> float:
        """
        Cython signature: double getPos()
        """
        ...
    
    def setPos(self, pos: float ) -> None:
        """
        Cython signature: void setPos(double pos)
        """
        ...
    
    def setCVTerms(self, terms: List[CVTerm] ) -> None:
        """
        Cython signature: void setCVTerms(libcpp_vector[CVTerm] & terms)
        Sets the CV terms
        """
        ...
    
    def replaceCVTerm(self, term: CVTerm ) -> None:
        """
        Cython signature: void replaceCVTerm(CVTerm & term)
        Replaces the specified CV term
        """
        ...
    
    def replaceCVTerms(self, cv_terms: List[CVTerm] , accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void replaceCVTerms(libcpp_vector[CVTerm] cv_terms, String accession)
        """
        ...
    
    def consumeCVTerms(self, cv_term_map: Dict[bytes,List[CVTerm]] ) -> None:
        """
        Cython signature: void consumeCVTerms(libcpp_map[String,libcpp_vector[CVTerm]] cv_term_map)
        Merges the given map into the member map, no duplicate checking
        """
        ...
    
    def getCVTerms(self) -> Dict[bytes,List[CVTerm]]:
        """
        Cython signature: libcpp_map[String,libcpp_vector[CVTerm]] getCVTerms()
        Returns the accession string of the term
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
        Cython signature: bool hasCVTerm(String accession)
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
    
    def __richcmp__(self, other: Precursor, op: int) -> Any:
        ...
    ActivationMethod : __ActivationMethod 


class ProgressLogger:
    """
    Cython implementation of _ProgressLogger

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProgressLogger.html>`_

    Base class for all classes that want to report their progress
    
    Per default the progress log is disabled. Use setLogType to enable it
    
    Use startProgress, setProgress and endProgress for the actual logging
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProgressLogger()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProgressLogger ) -> None:
        """
        Cython signature: void ProgressLogger(ProgressLogger &)
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


class ProtXMLFile:
    """
    Cython implementation of _ProtXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProtXMLFile.html>`_

    Used to load (storing not supported, yet) ProtXML files
    
    This class is used to load (storing not supported, yet) documents that implement
    the schema of ProtXML files
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ProtXMLFile()
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , protein_ids: ProteinIdentification , peptide_ids: PeptideIdentification ) -> None:
        """
        Cython signature: void load(String filename, ProteinIdentification & protein_ids, PeptideIdentification & peptide_ids)
        Loads the identifications of an ProtXML file without identifier
        
        The information is read in and the information is stored in the
        corresponding variables
        
        :raises:
          Exception: FileNotFound is thrown if the file could not be found
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , protein_ids: ProteinIdentification , peptide_ids: PeptideIdentification , document_id: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(String filename, ProteinIdentification & protein_ids, PeptideIdentification & peptide_ids, String document_id)
        """
        ... 


class ProteaseDigestion:
    """
    Cython implementation of _ProteaseDigestion

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteaseDigestion.html>`_
      -- Inherits from ['EnzymaticDigestion']

    Class for the enzymatic digestion of proteins
    
    Digestion can be performed using simple regular expressions, e.g. [KR] | [^P] for trypsin.
    Also missed cleavages can be modeled, i.e. adjacent peptides are not cleaved
    due to enzyme malfunction/access restrictions. If n missed cleavages are allowed, all possible resulting
    peptides (cleaved and uncleaved) with up to n missed cleavages are returned.
    Thus no random selection of just n specific missed cleavage sites is performed.
    
    Usage:
    
    .. code-block:: python
    
          from pyopenms import *
          from urllib.request import urlretrieve
          #
          urlretrieve ("http://www.uniprot.org/uniprot/P02769.fasta", "bsa.fasta")
          #
          dig = ProteaseDigestion()
          dig.setEnzyme('Lys-C')
          bsa_string = "".join([l.strip() for l in open("bsa.fasta").readlines()[1:]])
          bsa_oms_string = String(bsa_string) # convert python string to OpenMS::String for further processing
          #
          minlen = 6
          maxlen = 30
          #
          # Using AASequence and digest
          result_digest = []
          result_digest_min_max = []
          bsa_aaseq = AASequence.fromString(bsa_oms_string)
          dig.digest(bsa_aaseq, result_digest)
          dig.digest(bsa_aaseq, result_digest_min_max, minlen, maxlen)
          print(result_digest[4].toString()) # GLVLIAFSQYLQQCPFDEHVK
          print(len(result_digest)) # 57 peptides
          print(result_digest_min_max[4].toString()) # LVNELTEFAK
          print(len(result_digest_min_max)) # 42 peptides
          #
          # Using digestUnmodified without the need for AASequence from the EnzymaticDigestion base class
          result_digest_unmodified = []
          dig.digestUnmodified(StringView(bsa_oms_string), result_digest_unmodified, minlen, maxlen)
          print(result_digest_unmodified[4].getString()) # LVNELTEFAK
          print(len(result_digest_unmodified)) # 42 peptides
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProteaseDigestion()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProteaseDigestion ) -> None:
        """
        Cython signature: void ProteaseDigestion(ProteaseDigestion &)
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
    def digest(self, protein: AASequence , output: List[AASequence] ) -> int:
        """
        Cython signature: size_t digest(AASequence & protein, libcpp_vector[AASequence] & output)
        """
        ...
    
    @overload
    def digest(self, protein: AASequence , output: List[AASequence] , min_length: int , max_length: int ) -> int:
        """
        Cython signature: size_t digest(AASequence & protein, libcpp_vector[AASequence] & output, size_t min_length, size_t max_length)
          Performs the enzymatic digestion of a protein.
        
        
          :param protein: Sequence to digest
          :param output: Digestion products (peptides)
          :param min_length: Minimal length of reported products
          :param max_length: Maximal length of reported products (0 = no restriction)
          :return: Number of discarded digestion products (which are not matching length restrictions)
        """
        ...
    
    def peptideCount(self, protein: AASequence ) -> int:
        """
        Cython signature: size_t peptideCount(AASequence & protein)
        Returns the number of peptides a digestion of protein would yield under the current enzyme and missed cleavage settings
        """
        ...
    
    @overload
    def isValidProduct(self, protein: AASequence , pep_pos: int , pep_length: int , ignore_missed_cleavages: bool , methionine_cleavage: bool ) -> bool:
        """
        Cython signature: bool isValidProduct(AASequence protein, size_t pep_pos, size_t pep_length, bool ignore_missed_cleavages, bool methionine_cleavage)
          Variant of EnzymaticDigestion::isValidProduct() with support for n-term protein cleavage and random D|P cleavage
        
          Checks if peptide is a valid digestion product of the enzyme, taking into account specificity and the flags provided here
        
        
          :param protein: Protein sequence
          :param pep_pos: Starting index of potential peptide
          :param pep_length: Length of potential peptide
          :param ignore_missed_cleavages: Do not compare MC's of potential peptide to the maximum allowed MC's
          :param allow_nterm_protein_cleavage: Regard peptide as n-terminal of protein if it starts only at pos=1 or 2 and protein starts with 'M'
          :param allow_random_asp_pro_cleavage: Allow cleavage at D|P sites to count as n/c-terminal
          :return: True if peptide has correct n/c terminals (according to enzyme, specificity and above flags)
        """
        ...
    
    @overload
    def isValidProduct(self, protein: Union[bytes, str, String] , pep_pos: int , pep_length: int , ignore_missed_cleavages: bool , methionine_cleavage: bool ) -> bool:
        """
        Cython signature: bool isValidProduct(String protein, size_t pep_pos, size_t pep_length, bool ignore_missed_cleavages, bool methionine_cleavage)
        Forwards to isValidProduct using protein.toUnmodifiedString()
        """
        ...
    
    @overload
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


class ProteinGroup:
    """
    Cython implementation of _ProteinGroup

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteinGroup.html>`_
    """
    
    probability: float
    
    accessions: List[bytes]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProteinGroup()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProteinGroup ) -> None:
        """
        Cython signature: void ProteinGroup(ProteinGroup &)
        """
        ... 


class ProteinIdentification:
    """
    Cython implementation of _ProteinIdentification

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteinIdentification.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProteinIdentification()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProteinIdentification ) -> None:
        """
        Cython signature: void ProteinIdentification(ProteinIdentification &)
        """
        ...
    
    def getHits(self) -> List[ProteinHit]:
        """
        Cython signature: libcpp_vector[ProteinHit] getHits()
        Returns the protein hits
        """
        ...
    
    def insertHit(self, input: ProteinHit ) -> None:
        """
        Cython signature: void insertHit(ProteinHit input)
        Appends a protein hit
        """
        ...
    
    def setHits(self, hits: List[ProteinHit] ) -> None:
        """
        Cython signature: void setHits(libcpp_vector[ProteinHit] hits)
        Sets the protein hits
        """
        ...
    
    def getProteinGroups(self) -> List[ProteinGroup]:
        """
        Cython signature: libcpp_vector[ProteinGroup] getProteinGroups()
        Returns the protein groups
        """
        ...
    
    def insertProteinGroup(self, group: ProteinGroup ) -> None:
        """
        Cython signature: void insertProteinGroup(ProteinGroup group)
        Appends a new protein group
        """
        ...
    
    def getIndistinguishableProteins(self) -> List[ProteinGroup]:
        """
        Cython signature: libcpp_vector[ProteinGroup] getIndistinguishableProteins()
        Returns the indistinguishable proteins
        """
        ...
    
    def insertIndistinguishableProteins(self, group: ProteinGroup ) -> None:
        """
        Cython signature: void insertIndistinguishableProteins(ProteinGroup group)
        Appends new indistinguishable proteins
        """
        ...
    
    def getSignificanceThreshold(self) -> float:
        """
        Cython signature: double getSignificanceThreshold()
        Returns the protein significance threshold value
        """
        ...
    
    def setSignificanceThreshold(self, value: float ) -> None:
        """
        Cython signature: void setSignificanceThreshold(double value)
        Sets the protein significance threshold value
        """
        ...
    
    def getScoreType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getScoreType()
        Returns the protein score type
        """
        ...
    
    def setScoreType(self, type: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setScoreType(String type)
        Sets the protein score type
        """
        ...
    
    def isHigherScoreBetter(self) -> bool:
        """
        Cython signature: bool isHigherScoreBetter()
        Returns true if a higher score represents a better score
        """
        ...
    
    def setHigherScoreBetter(self, higher_is_better: bool ) -> None:
        """
        Cython signature: void setHigherScoreBetter(bool higher_is_better)
        Sets the orientation of the score (is higher better?)
        """
        ...
    
    def sort(self) -> None:
        """
        Cython signature: void sort()
        Sorts the protein hits according to their score
        """
        ...
    
    def assignRanks(self) -> None:
        """
        Cython signature: void assignRanks()
        Sorts the protein hits by score and assigns ranks (best score has rank 1)
        """
        ...
    
    def computeCoverage(self, pep_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void computeCoverage(libcpp_vector[PeptideIdentification] pep_ids)
        Compute the coverage (in percent) of all ProteinHits given PeptideHits
        """
        ...
    
    def getDateTime(self) -> DateTime:
        """
        Cython signature: DateTime getDateTime()
        Returns the date of the protein identification run
        """
        ...
    
    def setDateTime(self, date: DateTime ) -> None:
        """
        Cython signature: void setDateTime(DateTime date)
        Sets the date of the protein identification run
        """
        ...
    
    def setSearchEngine(self, search_engine: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSearchEngine(String search_engine)
        Sets the search engine type
        """
        ...
    
    def getSearchEngine(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSearchEngine()
        Returns the type of search engine used
        """
        ...
    
    def setSearchEngineVersion(self, search_engine_version: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSearchEngineVersion(String search_engine_version)
        Sets the search engine version
        """
        ...
    
    def getSearchEngineVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSearchEngineVersion()
        Returns the search engine version
        """
        ...
    
    def setSearchParameters(self, search_parameters: SearchParameters ) -> None:
        """
        Cython signature: void setSearchParameters(SearchParameters search_parameters)
        Sets the search parameters
        """
        ...
    
    def getSearchParameters(self) -> SearchParameters:
        """
        Cython signature: SearchParameters getSearchParameters()
        Returns the search parameters
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        Returns the identifier
        """
        ...
    
    def setIdentifier(self, id_: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(String id_)
        Sets the identifier
        """
        ...
    
    @overload
    def setPrimaryMSRunPath(self, s: List[bytes] ) -> None:
        """
        Cython signature: void setPrimaryMSRunPath(StringList & s)
        Set the file paths to the primary MS runs (usually the mzML files obtained after data conversion from raw files)
        
        
        :param raw: Store paths to the raw files (or equivalent) rather than mzMLs
        """
        ...
    
    @overload
    def setPrimaryMSRunPath(self, s: List[bytes] , raw: bool ) -> None:
        """
        Cython signature: void setPrimaryMSRunPath(StringList & s, bool raw)
        """
        ...
    
    @overload
    def addPrimaryMSRunPath(self, s: List[bytes] ) -> None:
        """
        Cython signature: void addPrimaryMSRunPath(StringList & s)
        """
        ...
    
    @overload
    def addPrimaryMSRunPath(self, s: List[bytes] , raw: bool ) -> None:
        """
        Cython signature: void addPrimaryMSRunPath(StringList & s, bool raw)
        """
        ...
    
    @overload
    def getPrimaryMSRunPath(self, output: List[bytes] ) -> None:
        """
        Cython signature: void getPrimaryMSRunPath(StringList & output)
        """
        ...
    
    @overload
    def getPrimaryMSRunPath(self, output: List[bytes] , raw: bool ) -> None:
        """
        Cython signature: void getPrimaryMSRunPath(StringList & output, bool raw)
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
    
    def __richcmp__(self, other: ProteinIdentification, op: int) -> Any:
        ...
    PeakMassType : __PeakMassType 


class ProteinInference:
    """
    Cython implementation of _ProteinInference

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteinInference.html>`_

    [experimental class] given a peptide quantitation, infer corresponding protein quantities
    
    Infers protein ratios from peptide ratios (currently using unique peptides only).
    Use the IDMapper class to add protein and peptide information to a
    quantitative ConsensusMap prior to this step
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProteinInference()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProteinInference ) -> None:
        """
        Cython signature: void ProteinInference(ProteinInference &)
        """
        ...
    
    def infer(self, consensus_map: ConsensusMap , reference_map: int ) -> None:
        """
        Cython signature: void infer(ConsensusMap & consensus_map, unsigned int reference_map)
        Given a peptide quantitation, infer corresponding protein quantities
        
        Infers protein ratios from peptide ratios (currently using unique peptides only).
        Use the IDMapper class to add protein and peptide information to a
        quantitative ConsensusMap prior to this step
        
        
        :param consensus_map: Peptide quantitation with ProteinIdentifications attached, where protein quantitation will be attached
        :param reference_map: Index of (iTRAQ) reference channel within the consensus map
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


class SearchParameters:
    """
    Cython implementation of _SearchParameters

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SearchParameters.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    db: Union[bytes, str, String]
    
    db_version: Union[bytes, str, String]
    
    taxonomy: Union[bytes, str, String]
    
    charges: Union[bytes, str, String]
    
    mass_type: int
    
    fixed_modifications: List[bytes]
    
    variable_modifications: List[bytes]
    
    missed_cleavages: int
    
    fragment_mass_tolerance: float
    
    fragment_mass_tolerance_ppm: bool
    
    precursor_mass_tolerance: float
    
    precursor_mass_tolerance_ppm: bool
    
    digestion_enzyme: DigestionEnzymeProtein
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SearchParameters()
        """
        ...
    
    @overload
    def __init__(self, in_0: SearchParameters ) -> None:
        """
        Cython signature: void SearchParameters(SearchParameters &)
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
    
    def __richcmp__(self, other: SearchParameters, op: int) -> Any:
        ... 


class SignalToNoiseEstimatorMedianRapid:
    """
    Cython implementation of _SignalToNoiseEstimatorMedianRapid

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SignalToNoiseEstimatorMedianRapid.html>`_
    """
    
    @overload
    def __init__(self, in_0: SignalToNoiseEstimatorMedianRapid ) -> None:
        """
        Cython signature: void SignalToNoiseEstimatorMedianRapid(SignalToNoiseEstimatorMedianRapid &)
        """
        ...
    
    @overload
    def __init__(self, window_length: float ) -> None:
        """
        Cython signature: void SignalToNoiseEstimatorMedianRapid(double window_length)
        """
        ...
    
    @overload
    def estimateNoise(self, in_0: _Interfaces_Spectrum ) -> NoiseEstimator:
        """
        Cython signature: NoiseEstimator estimateNoise(shared_ptr[_Interfaces_Spectrum])
        """
        ...
    
    @overload
    def estimateNoise(self, in_0: _Interfaces_Chromatogram ) -> NoiseEstimator:
        """
        Cython signature: NoiseEstimator estimateNoise(shared_ptr[_Interfaces_Chromatogram])
        """
        ...
    
    @overload
    def estimateNoise(self, mz_array: List[float] , int_array: List[float] ) -> NoiseEstimator:
        """
        Cython signature: NoiseEstimator estimateNoise(libcpp_vector[double] mz_array, libcpp_vector[double] int_array)
        """
        ... 


class SimpleSearchEngineAlgorithm:
    """
    Cython implementation of _SimpleSearchEngineAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SimpleSearchEngineAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SimpleSearchEngineAlgorithm()
        """
        ...
    
    @overload
    def __init__(self, in_0: SimpleSearchEngineAlgorithm ) -> None:
        """
        Cython signature: void SimpleSearchEngineAlgorithm(SimpleSearchEngineAlgorithm &)
        """
        ...
    
    def search(self, in_mzML: Union[bytes, str, String] , in_db: Union[bytes, str, String] , prot_ids: List[ProteinIdentification] , pep_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void search(const String & in_mzML, const String & in_db, libcpp_vector[ProteinIdentification] & prot_ids, libcpp_vector[PeptideIdentification] & pep_ids)
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


class SourceFile:
    """
    Cython implementation of _SourceFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SourceFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SourceFile()
        Description of a file location, used to store the origin of (meta) data
        """
        ...
    
    @overload
    def __init__(self, in_0: SourceFile ) -> None:
        """
        Cython signature: void SourceFile(SourceFile &)
        """
        ...
    
    def getNameOfFile(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNameOfFile()
        Returns the file name
        """
        ...
    
    def setNameOfFile(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNameOfFile(String)
        Sets the file name
        """
        ...
    
    def getPathToFile(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getPathToFile()
        Returns the file path
        """
        ...
    
    def setPathToFile(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setPathToFile(String)
        Sets the file path
        """
        ...
    
    def getFileSize(self) -> float:
        """
        Cython signature: float getFileSize()
        Returns the file size in MB
        """
        ...
    
    def setFileSize(self, in_0: float ) -> None:
        """
        Cython signature: void setFileSize(float)
        Sets the file size in MB
        """
        ...
    
    def getFileType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFileType()
        Returns the file type
        """
        ...
    
    def setFileType(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFileType(String)
        Sets the file type
        """
        ...
    
    def getChecksum(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getChecksum()
        Returns the file's checksum
        """
        ...
    
    def setChecksum(self, in_0: Union[bytes, str, String] , in_1: int ) -> None:
        """
        Cython signature: void setChecksum(String, ChecksumType)
        Sets the file's checksum
        """
        ...
    
    def getChecksumType(self) -> int:
        """
        Cython signature: ChecksumType getChecksumType()
        Returns the checksum type
        """
        ...
    
    def getNativeIDType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNativeIDType()
        Returns the native ID type of the spectra
        """
        ...
    
    def setNativeIDType(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNativeIDType(String)
        Sets the native ID type of the spectra
        """
        ...
    
    def getNativeIDTypeAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNativeIDTypeAccession()
        Returns the nativeID of the spectra
        """
        ...
    
    def setNativeIDTypeAccession(self, accesssion: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNativeIDTypeAccession(const String & accesssion)
        Sets the native ID of the spectra
        """
        ... 


class SpectrumAccessQuadMZTransforming:
    """
    Cython implementation of _SpectrumAccessQuadMZTransforming

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumAccessQuadMZTransforming.html>`_
      -- Inherits from ['SpectrumAccessTransforming']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumAccessQuadMZTransforming()
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessQuadMZTransforming ) -> None:
        """
        Cython signature: void SpectrumAccessQuadMZTransforming(SpectrumAccessQuadMZTransforming &)
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMS , a: float , b: float , c: float , ppm: bool ) -> None:
        """
        Cython signature: void SpectrumAccessQuadMZTransforming(shared_ptr[SpectrumAccessOpenMS], double a, double b, double c, bool ppm)
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMSCached , a: float , b: float , c: float , ppm: bool ) -> None:
        """
        Cython signature: void SpectrumAccessQuadMZTransforming(shared_ptr[SpectrumAccessOpenMSCached], double a, double b, double c, bool ppm)
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMSInMemory , a: float , b: float , c: float , ppm: bool ) -> None:
        """
        Cython signature: void SpectrumAccessQuadMZTransforming(shared_ptr[SpectrumAccessOpenMSInMemory], double a, double b, double c, bool ppm)
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


class SpectrumAccessSqMass:
    """
    Cython implementation of _SpectrumAccessSqMass

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumAccessSqMass.html>`_
      -- Inherits from ['ISpectrumAccess']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumAccessSqMass()
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessSqMass ) -> None:
        """
        Cython signature: void SpectrumAccessSqMass(SpectrumAccessSqMass &)
        """
        ...
    
    @overload
    def __init__(self, in_0: MzMLSqliteHandler , indices: List[int] ) -> None:
        """
        Cython signature: void SpectrumAccessSqMass(MzMLSqliteHandler, libcpp_vector[int] indices)
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


class SpectrumLookup:
    """
    Cython implementation of _SpectrumLookup

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumLookup.html>`_
    """
    
    rt_tolerance: float
    
    def __init__(self) -> None:
        """
        Cython signature: void SpectrumLookup()
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Check if any spectra were set
        """
        ...
    
    def readSpectra(self, spectra: MSExperiment , scan_regexp: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void readSpectra(MSExperiment spectra, String scan_regexp)
        Read and index spectra for later look-up
        
        :param spectra: Container of spectra
        :param scan_regexp: Regular expression for matching scan numbers in spectrum native IDs (must contain the named group "?<SCAN>". For example, "scan=(?<SCAN>\\d+)").
        """
        ...
    
    def findByRT(self, rt: float ) -> int:
        """
        Cython signature: size_t findByRT(double rt)
        Look up spectrum by retention time (RT)
        
        :param rt: Retention time to look up
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByNativeID(self, native_id: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t findByNativeID(String native_id)
        Look up spectrum by native ID
        
        :param native_id: Native ID to look up
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByIndex(self, index: int , count_from_one: bool ) -> int:
        """
        Cython signature: size_t findByIndex(size_t index, bool count_from_one)
        Look up spectrum by index (position in the vector of spectra)
        
        :param index: Index to look up
        :param count_from_one: Do indexes start counting at one (default zero)?
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByScanNumber(self, scan_number: int ) -> int:
        """
        Cython signature: size_t findByScanNumber(size_t scan_number)
        Look up spectrum by scan number (extracted from the native ID)
        
        :param scan_number: Scan number to look up
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByReference(self, spectrum_ref: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t findByReference(String spectrum_ref)
        Look up spectrum by reference
        
        :param spectrum_ref: Spectrum reference to parse
        :returns: Index of the spectrum that matched
        """
        ...
    
    def addReferenceFormat(self, regexp: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addReferenceFormat(String regexp)
        Register a possible format for a spectrum reference
        
        :param regexp: Regular expression defining the format
        """
        ...
    
    def extractScanNumber(self, native_id: Union[bytes, str, String] , native_id_type_accession: Union[bytes, str, String] ) -> int:
        """
        Cython signature: int extractScanNumber(const String & native_id, const String & native_id_type_accession)
        """
        ... 


class SpectrumMetaData:
    """
    Cython implementation of _SpectrumMetaData

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumMetaData.html>`_
    """
    
    rt: float
    
    precursor_rt: float
    
    precursor_mz: float
    
    precursor_charge: int
    
    ms_level: int
    
    scan_number: int
    
    native_id: Union[bytes, str, String]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumMetaData()
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumMetaData ) -> None:
        """
        Cython signature: void SpectrumMetaData(SpectrumMetaData &)
        """
        ... 


class SpectrumMetaDataLookup:
    """
    Cython implementation of _SpectrumMetaDataLookup

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumMetaDataLookup.html>`_
      -- Inherits from ['SpectrumLookup']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void SpectrumMetaDataLookup()
        """
        ...
    
    @overload
    def readSpectra(self, spectra: MSExperiment , scan_regexp: Union[bytes, str, String] , get_precursor_rt: bool ) -> None:
        """
        Cython signature: void readSpectra(MSExperiment spectra, String scan_regexp, bool get_precursor_rt)
        Read spectra and store their meta data
        
        :param SpectrumContainer: Spectrum container class, must support `size` and `operator[]`
        :param spectra: Container of spectra
        :param scan_regexp: Regular expression for matching scan numbers in spectrum native IDs (must contain the named group "?<SCAN>")
        :param get_precursor_rt: Assign precursor retention times? (This relies on all precursor spectra being present and in the right order.)
        """
        ...
    
    @overload
    def readSpectra(self, spectra: MSExperiment , scan_regexp: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void readSpectra(MSExperiment spectra, String scan_regexp)
        Read and index spectra for later look-up
        
        :param spectra: Container of spectra
        :param scan_regexp: Regular expression for matching scan numbers in spectrum native IDs (must contain the named group "?<SCAN>". For example, "scan=(?<SCAN>\\d+)").
        """
        ...
    
    @overload
    def getSpectrumMetaData(self, index: int , meta: SpectrumMetaData ) -> None:
        """
        Cython signature: void getSpectrumMetaData(size_t index, SpectrumMetaData & meta)
        Look up meta data of a spectrum
        
        :param index: Index of the spectrum
        :param meta: Meta data output
        """
        ...
    
    @overload
    def getSpectrumMetaData(self, spectrum_ref: Union[bytes, str, String] , meta: SpectrumMetaData ) -> None:
        """
        Cython signature: void getSpectrumMetaData(String spectrum_ref, SpectrumMetaData & meta)
        Extract meta data from a spectrum
        
        :param spectrum: Spectrum input
        :param meta: Meta data output
        :param scan_regexp: Regular expression for extracting scan number from spectrum native ID
        :param precursor_rts: RTs of potential precursor spectra of different MS levels
        """
        ...
    
    @overload
    def getSpectrumMetaData(self, spectrum_ref: Union[bytes, str, String] , meta: SpectrumMetaData , flags: bytes ) -> None:
        """
        Cython signature: void getSpectrumMetaData(String spectrum_ref, SpectrumMetaData & meta, unsigned char flags)
        Extract meta data via a spectrum reference
        
        :param spectrum_ref: Spectrum reference to parse
        :param metadata: Meta data output
        :param flags: What meta data to extract
        """
        ...
    
    def setSpectraDataRef(self, spectra_data: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSpectraDataRef(const String & spectra_data)
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Check if any spectra were set
        """
        ...
    
    def findByRT(self, rt: float ) -> int:
        """
        Cython signature: size_t findByRT(double rt)
        Look up spectrum by retention time (RT)
        
        :param rt: Retention time to look up
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByNativeID(self, native_id: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t findByNativeID(String native_id)
        Look up spectrum by native ID
        
        :param native_id: Native ID to look up
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByIndex(self, index: int , count_from_one: bool ) -> int:
        """
        Cython signature: size_t findByIndex(size_t index, bool count_from_one)
        Look up spectrum by index (position in the vector of spectra)
        
        :param index: Index to look up
        :param count_from_one: Do indexes start counting at one (default zero)?
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByScanNumber(self, scan_number: int ) -> int:
        """
        Cython signature: size_t findByScanNumber(size_t scan_number)
        Look up spectrum by scan number (extracted from the native ID)
        
        :param scan_number: Scan number to look up
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByReference(self, spectrum_ref: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t findByReference(String spectrum_ref)
        Look up spectrum by reference
        
        :param spectrum_ref: Spectrum reference to parse
        :returns: Index of the spectrum that matched
        """
        ...
    
    def addReferenceFormat(self, regexp: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addReferenceFormat(String regexp)
        Register a possible format for a spectrum reference
        
        :param regexp: Regular expression defining the format
        """
        ...
    
    def extractScanNumber(self, native_id: Union[bytes, str, String] , native_id_type_accession: Union[bytes, str, String] ) -> int:
        """
        Cython signature: int extractScanNumber(const String & native_id, const String & native_id_type_accession)
        """
        ...
    
    addMissingIMToPeptideIDs: __static_SpectrumMetaDataLookup_addMissingIMToPeptideIDs
    
    addMissingRTsToPeptideIDs: __static_SpectrumMetaDataLookup_addMissingRTsToPeptideIDs
    
    addMissingSpectrumReferences: __static_SpectrumMetaDataLookup_addMissingSpectrumReferences
    
    getSpectrumMetaData: __static_SpectrumMetaDataLookup_getSpectrumMetaData 


class SqrtScaler:
    """
    Cython implementation of _SqrtScaler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SqrtScaler.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SqrtScaler()
        """
        ...
    
    @overload
    def __init__(self, in_0: SqrtScaler ) -> None:
        """
        Cython signature: void SqrtScaler(SqrtScaler &)
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


class String:
    """
    Cython implementation of _String

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1String.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void String()
        """
        ...
    
    def __richcmp__(self, other: String, op: int) -> Any:
        ... 


class TransformationModelBSpline:
    """
    Cython implementation of _TransformationModelBSpline

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TransformationModelBSpline.html>`_
      -- Inherits from ['TransformationModel']
    """
    
    def __init__(self, data: List[TM_DataPoint] , params: Param ) -> None:
        """
        Cython signature: void TransformationModelBSpline(libcpp_vector[TM_DataPoint] & data, Param & params)
        """
        ...
    
    def getDefaultParameters(self, in_0: Param ) -> None:
        """
        Cython signature: void getDefaultParameters(Param &)
        Gets the default parameters
        """
        ...
    
    def evaluate(self, value: float ) -> float:
        """
        Cython signature: double evaluate(double value)
        Evaluates the model at the given values
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
    
    getDefaultParameters: __static_TransformationModelBSpline_getDefaultParameters 


class TransformationModelInterpolated:
    """
    Cython implementation of _TransformationModelInterpolated

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TransformationModelInterpolated.html>`_
      -- Inherits from ['TransformationModel']
    """
    
    def __init__(self, data: List[TM_DataPoint] , params: Param ) -> None:
        """
        Cython signature: void TransformationModelInterpolated(libcpp_vector[TM_DataPoint] & data, Param & params)
        """
        ...
    
    def getDefaultParameters(self, in_0: Param ) -> None:
        """
        Cython signature: void getDefaultParameters(Param &)
        Gets the default parameters
        """
        ...
    
    def evaluate(self, value: float ) -> float:
        """
        Cython signature: double evaluate(double value)
        Evaluate the interpolation model at the given value
        
        :param value: The position where the interpolation should be evaluated
        :returns: The interpolated value
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


class __ActivationMethod:
    None
    CID : int
    PSD : int
    PD : int
    SID : int
    BIRD : int
    ECD : int
    IMD : int
    SORI : int
    HCID : int
    LCID : int
    PHD : int
    ETD : int
    ETciD : int
    EThcD : int
    PQD : int
    TRAP : int
    HCD : int
    INSOURCE : int
    LIFT : int
    SIZE_OF_ACTIVATIONMETHOD : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class ChecksumType:
    None
    UNKNOWN_CHECKSUM : int
    SHA1 : int
    MD5 : int
    SIZE_OF_CHECKSUMTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class DriftTimeUnit:
    None
    NONE : int
    MILLISECOND : int
    VSSC : int
    FAIMS_COMPENSATION_VOLTAGE : int
    SIZE_OF_DRIFTTIMEUNIT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class FileType:
    None
    UNKNOWN : int
    DTA : int
    DTA2D : int
    MZDATA : int
    MZXML : int
    FEATUREXML : int
    IDXML : int
    CONSENSUSXML : int
    MGF : int
    INI : int
    TOPPAS : int
    TRANSFORMATIONXML : int
    MZML : int
    CACHEDMZML : int
    MS2 : int
    PEPXML : int
    PROTXML : int
    MZIDENTML : int
    QCML : int
    GELML : int
    TRAML : int
    MSP : int
    OMSSAXML : int
    MASCOTXML : int
    PNG : int
    XMASS : int
    TSV : int
    PEPLIST : int
    HARDKLOER : int
    KROENIK : int
    FASTA : int
    EDTA : int
    CSV : int
    TXT : int
    OBO : int
    HTML : int
    XML : int
    ANALYSISXML : int
    XSD : int
    PSQ : int
    MRM : int
    SQMASS : int
    PQP : int
    OSW : int
    PSMS : int
    PARAMXML : int
    SIZE_OF_TYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class IMFormat:
    None
    NONE : int
    CONCATENATED : int
    MULTIPLE_SPECTRA : int
    MIXED : int
    SIZE_OF_IMFORMAT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class LogType:
    None
    CMD : int
    GUI : int
    NONE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __PeakMassType:
    None
    MONOISOTOPIC : int
    AVERAGE : int
    SIZE_OF_PEAKMASSTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class QuotingMethod:
    None
    NONE : int
    ESCAPE : int
    DOUBLE : int

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

