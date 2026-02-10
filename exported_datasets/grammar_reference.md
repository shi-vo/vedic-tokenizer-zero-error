# Sanskrit Grammar Reference
*Generated from Vedic Tokenizer*

## Sandhi Rules Catalog

This document contains all 46 Sandhi (phonetic transformation) rules 
implemented in the tokenizer, organized by category.

---

## SVARA SANDHI (33 rules)

### VS01: a + a → ā

**Pāṇini Sūtra**: 6.1.101

**Pattern**: `अ` + `अ` → `आ`

**Priority**: 10/10

**Examples**:
- `रम` + `अति` → `रमाति`

---

### VS02: ā + a → ā

**Pāṇini Sūtra**: 6.1.101

**Pattern**: `आ` + `अ` → `आ`

**Priority**: 10/10

**Examples**:
- `रमा` + `अति` → `रमाति`

---

### VS03: a + ā → ā

**Pāṇini Sūtra**: 6.1.101

**Pattern**: `अ` + `आ` → `आ`

**Priority**: 10/10

**Examples**:
- `तत्र` + `आगच्छति` → `तत्रागच्छति`

---

### VS04: ā + ā → ā

**Pāṇini Sūtra**: 6.1.101

**Pattern**: `आ` + `आ` → `आ`

**Priority**: 9/10

**Examples**:
- `रमा` + `आगच्छति` → `रमागच्छति`

---

### VS05: i + i → ī

**Pāṇini Sūtra**: 6.1.101

**Pattern**: `इ` + `इ` → `ई`

**Priority**: 9/10

**Examples**:
- `कवि` + `इन्द्रः` → `कवीन्द्रः`

---

### VS06: ī + i → ī

**Pāṇini Sūtra**: 6.1.101

**Pattern**: `ई` + `इ` → `ई`

**Priority**: 9/10

**Examples**:
- `नदी` + `इव` → `नदीव`

---

### VS07: u + u → ū

**Pāṇini Sūtra**: 6.1.101

**Pattern**: `उ` + `उ` → `ऊ`

**Priority**: 8/10

**Examples**:
- `साधु` + `उक्तिः` → `साधूक्तिः`

---

### VS08: ū + u → ū

**Pāṇini Sūtra**: 6.1.101

**Pattern**: `ऊ` + `उ` → `ऊ`

**Priority**: 8/10

**Examples**:
- `वधू` + `उक्तिः` → `वधूक्तिः`

---

### VS09: a + i → e (guna)

**Pāṇini Sūtra**: 6.1.87

**Pattern**: `अ` + `इ` → `ए`

**Priority**: 10/10

**Examples**:
- `रम` + `इति` → `रमेति`

---

### VS10: a + ī → e (guna)

**Pāṇini Sūtra**: 6.1.87

**Pattern**: `अ` + `ई` → `ए`

**Priority**: 10/10

**Examples**:
- `परम` + `ईश्वरः` → `परमेश्वरः`

---

### VS11: ā + i → e (guna)

**Pāṇini Sūtra**: 6.1.87

**Pattern**: `आ` + `इ` → `ए`

**Priority**: 9/10

**Examples**:
- `रमा` + `इति` → `रमेति`

---

### VS12: ā + ī → e (guna)

**Pāṇini Sūtra**: 6.1.87

**Pattern**: `आ` + `ई` → `ए`

**Priority**: 9/10

**Examples**:
- `महा` + `ईशः` → `महेशः`

---

### VS13: a + u → o (guna)

**Pāṇini Sūtra**: 6.1.87

**Pattern**: `अ` + `उ` → `ओ`

**Priority**: 10/10

**Examples**:
- `सुर` + `उत्तमः` → `सुरोत्तमः`

---

### VS14: a + ū → o (guna)

**Pāṇini Sūtra**: 6.1.87

**Pattern**: `अ` + `ऊ` → `ओ`

**Priority**: 9/10

**Examples**:
- `परम` + `ऊर्जितः` → `परमोर्जितः`

---

### VS15: ā + u → o (guna)

**Pāṇini Sūtra**: 6.1.87

**Pattern**: `आ` + `उ` → `ओ`

**Priority**: 9/10

**Examples**:
- `महा` + `उदयः` → `महोदयः`

---

### VS16: ā + ū → o (guna)

**Pāṇini Sūtra**: 6.1.87

**Pattern**: `आ` + `ऊ` → `ओ`

**Priority**: 9/10

**Examples**:
- `महा` + `ऊर्जः` → `महोर्जः`

---

### VS17: a + ṛ → ar (guna)

**Pāṇini Sūtra**: 6.1.87

**Pattern**: `अ` + `ऋ` → `अर्`

**Priority**: 8/10

**Examples**:
- `महा` + `ऋषिः` → `महर्षिः`

---

### VS18: ā + ṛ → ar (guna)

**Pāṇini Sūtra**: 6.1.87

**Pattern**: `आ` + `ऋ` → `अर्`

**Priority**: 8/10

**Examples**:
- `महा` + `ऋषिः` → `महर्षिः`

---

### VS19: a + e → ai (vriddhi)

**Pāṇini Sūtra**: 6.1.88

**Pattern**: `अ` + `ए` → `ऐ`

**Priority**: 8/10

**Examples**:
- `तथा` + `एव` → `तथैव`

---

### VS20: ā + e → ai (vriddhi)

**Pāṇini Sūtra**: 6.1.88

**Pattern**: `आ` + `ए` → `ऐ`

**Priority**: 7/10

**Examples**:
- `सदा` + `एव` → `सदैव`

---

### VS21: a + ai → ai (vriddhi)

**Pāṇini Sūtra**: 6.1.88

**Pattern**: `अ` + `ऐ` → `ऐ`

**Priority**: 7/10

**Examples**:
- `तत्र` + `ऐश्वर्यम्` → `तत्रैश्वर्यम्`

---

### VS22: a + o → au (vriddhi)

**Pāṇini Sūtra**: 6.1.88

**Pattern**: `अ` + `ओ` → `औ`

**Priority**: 8/10

**Examples**:
- `वन` + `ओषधिः` → `वनौषधिः`

---

### VS23: ā + o → au (vriddhi)

**Pāṇini Sūtra**: 6.1.88

**Pattern**: `आ` + `ओ` → `औ`

**Priority**: 7/10

**Examples**:
- `महा` + `ओजः` → `महौजः`

---

### VS24: a + au → au (vriddhi)

**Pāṇini Sūtra**: 6.1.88

**Pattern**: `अ` + `औ` → `औ`

**Priority**: 7/10

**Examples**:
- `परम` + `औषधम्` → `परमौषधम्`

---

### VS25: i + a → ya (yan)

**Pāṇini Sūtra**: 6.1.77

**Pattern**: `इ` + `अ` → `य`

**Priority**: 10/10

**Examples**:
- `प्रति` + `अर्थः` → `प्रत्यर्थः`

---

### VS26: ī + a → ya (yan)

**Pāṇini Sūtra**: 6.1.77

**Pattern**: `ई` + `अ` → `य`

**Priority**: 9/10

**Examples**:
- `नदी` + `अत्र` → `नद्यत्र`

---

### VS27: u + a → va (yan)

**Pāṇini Sūtra**: 6.1.77

**Pattern**: `उ` + `अ` → `व`

**Priority**: 9/10

**Examples**:
- `सु` + `आगतः` → `स्वागतः`

---

### VS28: ū + a → va (yan)

**Pāṇini Sūtra**: 6.1.77

**Pattern**: `ऊ` + `अ` → `व`

**Priority**: 8/10

**Examples**:
- `वधू` + `आगमनम्` → `वध्वागमनम्`

---

### VS29: ṛ + a → ra (yan)

**Pāṇini Sūtra**: 6.1.77

**Pattern**: `ऋ` + `अ` → `र`

**Priority**: 7/10

**Examples**:
- `पितृ` + `आदेशः` → `पित्रादेशः`

---

### VS30: i + ā → yā

**Pāṇini Sūtra**: 6.1.77

**Pattern**: `इ` + `आ` → `या`

**Priority**: 9/10

**Examples**:
- `प्रति` + `आह` → `प्रत्याह`

---

### VS31: i + u → yu

**Pāṇini Sūtra**: 6.1.77

**Pattern**: `इ` + `उ` → `यु`

**Priority**: 8/10

**Examples**:
- `अति` + `उत्तमः` → `अत्युत्तमः`

---

### VS32: u + ā → vā

**Pāṇini Sūtra**: 6.1.77

**Pattern**: `उ` + `आ` → `वा`

**Priority**: 8/10

**Examples**:
- `सु` + `आगतः` → `स्वागतः`

---

### VS33: u + i → vi

**Pāṇini Sūtra**: 6.1.77

**Pattern**: `उ` + `इ` → `वि`

**Priority**: 7/10

**Examples**:
- `अनु` + `इष्टः` → `अन्विष्टः`

---

## VYANJANA SANDHI (10 rules)

### CS01: k + g → gg

**Pattern**: `क्` + `ग` → `ग्ग`

**Priority**: 8/10

**Examples**:
- `वाक्` + `गतः` → `वाग्गतः`

---

### CS02: t + j → jj

**Pattern**: `त्` + `ज` → `ज्ज`

**Priority**: 8/10

**Examples**:
- `तत्` + `जलम्` → `तज्जलम्`

---

### CS03: t + c → cc

**Pāṇini Sūtra**: 8.4.40

**Pattern**: `त्` + `च` → `च्च`

**Priority**: 9/10

**Examples**:
- `तत्` + `च` → `तच्च`

---

### CS04: t + ś → cch

**Pattern**: `त्` + `श` → `च्छ`

**Priority**: 8/10

**Examples**:
- `तत्` + `शास्त्रम्` → `तच्छास्त्रम्`

---

### CS05: d + dh → ddh

**Pattern**: `द्` + `ध` → `द्ध`

**Priority**: 7/10

**Examples**:
- `तद्` + `धनम्` → `तद्धनम्`

---

### CS06: r + n → rṇ

**Pāṇini Sūtra**: 8.4.1

**Pattern**: `र्` + `न` → `र्ण`

**Priority**: 9/10

**Examples**:
- `प्र` + `नाम` → `प्रणाम`

---

### CS07: ṣ + n → ṣṇ

**Pattern**: `ष्` + `न` → `ष्ण`

**Priority**: 8/10

**Examples**:
- `विष` + `नाशः` → `विष्णाशः`

---

### CS08: m + k → ṃk

**Pāṇini Sūtra**: 8.3.23

**Pattern**: `म्` + `क` → `ं`

**Priority**: 10/10

**Examples**:
- `रामम्` + `करोति` → `रामं`

---

### CS09: m + c → ṃc

**Pattern**: `म्` + `च` → `ं`

**Priority**: 10/10

**Examples**:
- `तम्` + `च` → `तं`

---

### CS10: m + t → ṃt

**Pattern**: `म्` + `त` → `ं`

**Priority**: 10/10

**Examples**:
- `तम्` + `तु` → `तं`

---

## VISARGA SANDHI (3 rules)

### VIS01: aḥ + a → o'

**Pāṇini Sūtra**: 6.1.114

**Pattern**: `अः` + `अ` → `ओऽ`

**Priority**: 10/10

**Examples**:
- `रामः` + `अत्र` → `रामोऽत्र`

---

### VIS02: aḥ + ā → o

**Pattern**: `अः` + `आ` → `ओ`

**Priority**: 9/10

**Examples**:
- `रामः` + `आगच्छति` → `रामो`

---

### VIS03: aḥ + i → o

**Pattern**: `अः` + `इ` → `ओ`

**Priority**: 8/10

**Examples**:
- `रामः` + `इच्छति` → `रामो`

---

