# PATENT APPLICATION CLAIMS
## Zero-Error Sanskrit Tokenization System with Multi-Candidate Morphological Analysis

**Application Type**: Utility Patent  
**Technology Field**: Natural Language Processing, Computational Linguistics, Sanskrit Language Processing  
**Inventor**: Ganesh  
**Date**: January 27, 2026

---

## INDEPENDENT CLAIMS

### CLAIM 1: Core System (Primary Independent Claim)

A computer-implemented method for zero-error lossless tokenization of Sanskrit text, the method comprising:

**a)** receiving, by a computing device, input text in Sanskrit language encoded in Devanagari script;

**b)** maintaining a comprehensive grammar rule database comprising:
   - (i) at least 130 Sandhi phonetic transformation rules categorized into vowel Sandhi, consonant Sandhi, visarga Sandhi, and special Vedic Sandhi;
   - (ii) at least 160 Vibhakti case-ending patterns covering eight grammatical cases, three grammatical numbers, and multiple stem types;
   - (iii) at least 55 Pratyaya suffix patterns including kṛt pratyayas, taddhita pratyayas, and strī pratyayas;

**c)** generating, for each word boundary in the input text, a plurality of candidate splits by:
   - (i) applying said Sandhi transformation rules in reverse to identify potential word boundaries;
   - (ii) validating each candidate split against a Sanskrit vocabulary database containing word frequency information;
   - (iii) analyzing each component word using said Vibhakti patterns to determine grammatical case, number, and gender;
   - (iv) analyzing each component word using said Pratyaya patterns to identify derivational morphology;

**d)** calculating, for each candidate split, a composite confidence score using a weighted algorithm comprising:
   - (i) a first weight of 40% applied to a Sandhi rule priority value, wherein said priority value ranges from 1 to 10 based on rule specificity;
   - (ii) a second weight of 30% applied to a vocabulary frequency score derived from corpus-based word occurrence statistics;
   - (iii) a third weight of 30% applied to a grammatical validity score based on recognition of Vibhakti and Pratyaya patterns;

**e)** selecting the candidate split with the highest composite confidence score as the optimal tokenization;

**f)** generating output tokens representing the selected tokenization; and

**g)** verifying mathematical reversibility by confirming that reconstructing the input text from said output tokens produces an exact character-by-character match with the original input text, wherein said verification guarantees zero information loss.

---

### CLAIM 2: Multi-Candidate Engine (Secondary Independent Claim)

A system for morphological analysis of Sanskrit text comprising:

**a)** a Sandhi analysis engine configured to:
   - (i) store a database of Sandhi transformation rules, each rule comprising a left pattern, right pattern, result pattern, and priority value;
   - (ii) identify, for a given word, all applicable Sandhi rules based on pattern matching;
   - (iii) apply reverse transformation to generate multiple candidate word splits;

**b)** a Vibhakti analysis engine configured to:
   - (i) store patterns for case endings across multiple stem types including a-stems, ā-stems, i-stems, ī-stems, u-stems, ū-stems, ṛ-stems, and consonant-stems;
   - (ii) analyze word endings to identify grammatical case, number, and gender;
   - (iii) extract word stems by removing identified case endings;

**c)** a Pratyaya analysis engine configured to:
   - (i) store patterns for verbal and nominal suffixes;
   - (ii) identify suffix types including infinitives, absolutives, participles, agent nouns, abstract nouns, and possessive formations;
   - (iii) extract base forms by removing identified suffixes;

**d)** an integrated scoring module configured to:
   - (i) receive candidate analyses from said Sandhi, Vibhakti, and Pratyaya engines;
   - (ii) access a vocabulary database with frequency statistics;
   - (iii) compute a weighted composite score using predetermined percentages for Sandhi rule priority, vocabulary frequency, and grammatical validity;
   - (iv) rank candidates based on said composite scores;

**e)** a verification module configured to ensure that tokenization output can be reconstructed into the original input without loss of information.

---

### CLAIM 3: Data Structure (Independent Claim)

A non-transitory computer-readable storage medium storing a structured Sanskrit grammar database comprising:

**a)** a first data structure containing Sandhi transformation rules, each rule comprising:
   - (i) a unique rule identifier;
   - (ii) a category identifier selected from vowel Sandhi, consonant Sandhi, visarga Sandhi, and special Sandhi;
   - (iii) a left boundary pattern in Devanagari Unicode;
   - (iv) a right boundary pattern in Devanagari Unicode;
   - (v) a transformation result pattern in Devanagari Unicode;
   - (vi) a priority integer value between 1 and 10;
   - (vii) a reference to corresponding Pāṇinian sūtra;
   - (viii) directional transformation flags for forward and reverse application;

**b)** a second data structure containing Vibhakti case-ending patterns, each pattern comprising:
   - (i) an ending suffix in Devanagari Unicode;
   - (ii) a case enumeration value;
   - (iii) a number enumeration value;
   - (iv) an optional gender enumeration value;
   - (v) a stem type identifier;
   - (vi) a pattern priority value;

**c)** a third data structure containing Pratyaya suffix patterns, each pattern comprising:
   - (i) a suffix string in Devanagari Unicode;
   - (ii) a pratyaya type identifier;
   - (iii) a category identifier for subcategorization;
   - (iv) a semantic meaning description;
   - (v) example word instances;

**d)** a fourth data structure containing vocabulary entries with frequency counts derived from a corpus of at least 90,000 Sanskrit verses.

---

## DEPENDENT CLAIMS

### Claims Dependent on Claim 1:

**CLAIM 4:** The method of claim 1, wherein said Sandhi transformation rules comprise:
   - (a) 33 vowel Sandhi rules including savarna dīrgha, guṇa, vṛddhi, and yaṇ transformations;
   - (b) 50 consonant Sandhi rules including complete anusvāra conversion set, gemination rules, aspiration changes, and retroflex conversions;
   - (c) 20 visarga Sandhi rules covering transformations before vowels and consonants;
   - (d) 27 special Sandhi rules including pragṛhya exceptions, lopa deletions, samprasāraṇa, and Vedic meter preservation rules.

**CLAIM 5:** The method of claim 1, wherein calculating the vocabulary frequency score comprises:
   - (a) retrieving occurrence counts for left and right component words from a corpus-derived database;
   - (b) applying logarithmic scaling to said occurrence counts;
   - (c) computing a geometric mean of logarithmically scaled frequencies;
   - (d) normalizing the result to a range of 0.0 to 1.0.

**CLAIM 6:** The method of claim 1, wherein calculating the grammatical validity score comprises:
   - (a) assigning a first value of 0.2 if the left component has recognized Vibhakti pattern;
   - (b) assigning a second value of 0.2 if the right component has recognized Vibhakti pattern;
   - (c) assigning a third value of 0.2 if the left component has recognized Pratyaya pattern;
   - (d) assigning a fourth value of 0.2 if the right component has recognized Pratyaya pattern;
   - (e) assigning a bonus value of 0.2 if both components have recognized grammatical patterns;
   - (f) summing said values to produce the grammatical validity score.

**CLAIM 7:** The method of claim 1, wherein generating candidate splits further comprises:
   - (a) applying a greedy longest-match algorithm from left to right;
   - (b) applying a greedy longest-match algorithm from right to left;
   - (c) applying a balanced splitting algorithm targeting equal-sized components;
   - (d) considering a no-split option when the entire word exists in the vocabulary database.

**CLAIM 8:** The method of claim 1, wherein the verification step comprises:
   - (a) concatenating all output tokens in sequence;
   - (b) comparing the concatenated result with the original input text using byte-level comparison;
   - (c) generating a verification failure signal if any character mismatch is detected;
   - (d) triggering a fallback tokenization mode if verification fails.

**CLAIM 9:** The method of claim 1, further comprising:
   - (a) preserving Vedic accent marks including udātta, anudātta, and svarita in the output tokens;
   - (b) preserving original whitespace characters as separate tokens;
   - (c) maintaining Unicode normalization consistency throughout the process.

**CLAIM 10:** The method of claim 1, wherein the Vibhakti patterns cover:
   - (a) eight grammatical cases: prathamā (nominative), dvitīyā (accusative), tṛtīyā (instrumental), caturthī (dative), pañcamī (ablative), ṣaṣṭhī (genitive), saptamī (locative), and sambodhana (vocative);
   - (b) three grammatical numbers: ekavacana (singular), dvivacana (dual), and bahuvacana (plural);
   - (c) three genders: puṃliṅga (masculine), strīliṅga (feminine), and napuṃsakaliṅga (neuter).

### Claims Dependent on Claim 2:

**CLAIM 11:** The system of claim 2, wherein the Sandhi analysis engine implements bidirectional transformation capability supporting both:
   - (a) forward application to combine separate words into sandhi-joined forms; and
   - (b) reverse application to split sandhi-joined forms into constituent words.

**CLAIM 12:** The system of claim 2, wherein the integrated scoring module is configured to:
   - (a) generate a maximum of N candidate splits, where N is a configurable parameter;
   - (b) sort candidates by composite score in descending order;
   - (c) return the top-ranked candidate as the optimal result.

**CLAIM 13:** The system of claim 2, further comprising a compound word analyzer configured to:
   - (a) identify potential samāsa (compound) formations;
   - (b) apply multiple decomposition strategies including left-greedy, right-greedy, and balanced splitting;
   - (c) classify compounds by type including dvandva, tatpuruṣa, karmadhāraya, dvigu, bahuvrīhi, and avyayībhāva;
   - (d) assign confidence scores to decomposition hypotheses.

**CLAIM 14:** The system of claim 2, wherein the verification module implements:
   - (a) automatic integrity checking after each tokenization operation;
   - (b) collection of verification metrics including character count matching, Unicode normalization consistency, and byte-level equality;
   - (c) generation of diagnostic information upon verification failure.

### Claims Dependent on Claim 3:

**CLAIM 15:** The storage medium of claim 3, wherein the vocabulary database contains:
   - (a) at least 300,000 unique Sanskrit word forms;
   - (b) frequency statistics derived from a corpus containing verses from Vedas, Upaniṣads, Mahābhārata, Rāmāyaṇa, and Bhagavad Gītā;
   - (c) metadata associating each word with identified grammatical patterns.

**CLAIM 16:** The storage medium of claim 3, wherein the Sandhi rule data structure further includes:
   - (a) example word pairs demonstrating the rule application;
   - (b) transliteration of patterns in IAST (International Alphabet of Sanskrit Transliteration);
   - (c) flags indicating applicability in Classical vs. Vedic Sanskrit contexts.

---

## APPARATUS CLAIMS

**CLAIM 17:** An apparatus for processing Sanskrit text comprising:
   - (a) a processor;
   - (b) a memory storing instructions that, when executed by the processor, cause the apparatus to perform the method of claim 1;
   - (c) a storage device containing the grammar database of claim 3;
   - (d) an input interface for receiving Sanskrit text;
   - (e) an output interface for providing tokenization results.

---

## METHOD OF USE CLAIMS

**CLAIM 18:** A method of preparing Sanskrit text for machine learning comprising:
   - (a) tokenizing Sanskrit text using the method of claim 1;
   - (b) removing whitespace tokens from the tokenization output;
   - (c) creating a vocabulary mapping from unique tokens to numerical identifiers;
   - (d) converting tokenized text into numerical sequences suitable for neural network input.

**CLAIM 19:** A method of Sanskrit text search comprising:
   - (a) tokenizing a search query using the method of claim 1;
   - (b) tokenizing a corpus of Sanskrit documents using the method of claim 1;
   - (c) matching query tokens against corpus tokens with morphological awareness;
   - (d) ranking search results based on token overlap and grammatical compatibility.

**CLAIM 20:** A method of Sanskrit language education comprising:
   - (a) receiving student-entered Sanskrit text;
   - (b) applying the method of claim 1 to tokenize said text;
   - (c) displaying the recognized Vibhakti and Pratyaya patterns for each token;
   - (d) providing grammatical explanations based on the identified patterns;
   - (e) highlighting potential errors when verification fails.

---

## CLAIM SUMMARY

**Total Claims**: 20  
**Independent Claims**: 3 (Claims 1, 2, 3)  
**Dependent Claims**: 17 (Claims 4-20)

**Claim Scope**:
- Core method claims (1, 4-10)
- System/apparatus claims (2, 11-14, 17)
- Data structure claims (3, 15-16)
- Method of use claims (18-20)

---

## CLAIM STRATEGY NOTES

### Broadest Protection
Claim 1 provides broadest protection covering the core method with specific technical details.

### Alternative Formulations
Claims 2 and 3 provide alternative protection angles (system architecture and data structure).

### Defensive Claims
Claims 4-16 narrow the scope to specific technical implementations, making it harder to design around the patent.

### Commercial Applications
Claims 18-20 cover specific commercial uses, strengthening commercial value.

### International Strategy
Claims are drafted to be compatible with:
- USPTO (United States)
- IPO (India) - particularly relevant for Sanskrit
- EPO (Europe)
- Through PCT for international filing

---

## PROSECUTION STRATEGY

### Anticipated Rejections
- **Prior Art**: Traditional Sanskrit grammarians (Pāṇini, Patañjali) - argue computer implementation is novel
- **Obviousness**: Combination of known NLP techniques - argue specific weighting algorithm and zero-error guarantee are non-obvious
- **Software Patent**: May face challenges in Europe - emphasize technical effects and data structure innovations

### Response Preparation
- Maintain robust prior art comparison (see separate document)
- Prepare technical effect arguments (speed, accuracy, losslessness)
- Document surprising results (100% test pass rate on real texts)

---

**Document Version**: 1.0  
**Last Updated**: January 27, 2026  
**Status**: Draft for Attorney Review
