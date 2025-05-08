<p align="center">
  <img src="https://raw.githubusercontent.com/eriknovak/anonipy/main/docs/assets/imgs/logo.png" alt="logo" height="100" style="height: 100px;">
</p>

<p align="center">
  <i>Data anonymization package, supporting different anonymization strategies</i>
</p>

<p align="center">
  <a href="https://github.com/eriknovak/anonipy/actions/workflows/unittests.yaml" target="_blank">
    <img src="https://github.com/eriknovak/anonipy/actions/workflows/unittests.yaml/badge.svg" alt="Test" />
  </a>
  <a href="https://pypi.org/project/anonipy" target="_blank">
    <img src="https://img.shields.io/pypi/v/anonipy?color=%2334D058&amp;label=pypi%20package" alt="Package version" />
  </a>
  <a href="https://pypi.org/project/anonipy" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/anonipy.svg?color=%2334D058" alt="Supported Python versions" />
  </a>
  <a href="https://pypi.org/project/anonipy" target="_blank">
    <img src="https://static.pepy.tech/badge/anonipy/month" alt="Monthly package downloads" />
  </a>
  <a href="https://pypi.org/project/anonipy" target="_blank">
    <img src="https://static.pepy.tech/badge/anonipy" alt="Total package downloads" />
  </a>
</p>

---

**Documentation:** [https://eriknovak.github.io/anonipy](https://eriknovak.github.io/anonipy)

**Source code:** [https://github.com/eriknovak/anonipy](https://github.com/eriknovak/anonipy)

---

The anonipy package is a python package for data anonymization. It is designed to be simple to use and highly customizable, supporting different anonymization strategies. Powered by LLMs.

## Install

```bash
pip install anonipy
```

## Upgrade

```bash
pip install anonipy --upgrade
```

## Example

```python
original_text = """\
Medical Record

Patient Name: John Doe
Date of Birth: 15-01-1985
Date of Examination: 20-05-2024
Social Security Number: 123-45-6789

Examination Procedure:
John Doe underwent a routine physical examination. The procedure included measuring vital signs (blood pressure, heart rate, temperature), a comprehensive blood panel, and a cardiovascular stress test. The patient also reported occasional headaches and dizziness, prompting a neurological assessment and an MRI scan to rule out any underlying issues.

Medication Prescribed:

Ibuprofen 200 mg: Take one tablet every 6-8 hours as needed for headache and pain relief.
Lisinopril 10 mg: Take one tablet daily to manage high blood pressure.
Next Examination Date:
15-11-2024
"""
```

Use the language detector to detect the language of the text:

```python
from anonipy.utils.language_detector import LanguageDetector

language_detector = LanguageDetector()
language = language_detector(original_text)
```

Prepare the entity extractor and extract the personal infomation from the original text:

```python
from anonipy.anonymize.extractors import NERExtractor

# define the labels to be extracted and anonymized
labels = [
    {"label": "name", "type": "string"},
    {"label": "social security number", "type": "custom"},
    {"label": "date of birth", "type": "date"},
    {"label": "date", "type": "date"},
]

# initialize the NER extractor for the language and labels
extractor = NERExtractor(labels, lang=language, score_th=0.5)

# extract the entities from the original text
doc, entities = extractor(original_text)

# display the entities in the original text
extractor.display(doc)
```

Use generators to create substitutes for the entities:

```python
from anonipy.anonymize.generators import (
    LLMLabelGenerator,
    DateGenerator,
    NumberGenerator,
)

# initialize the generators
llm_generator = LLMLabelGenerator()
date_generator = DateGenerator()
number_generator = NumberGenerator()

# prepare the anonymization mapping
def anonymization_mapping(text, entity):
    if entity.type == "string":
        return llm_generator.generate(entity, temperature=0.7)
    if entity.label == "date":
        return date_generator.generate(entity, output_gen="MIDDLE_OF_THE_MONTH")
    if entity.label == "date of birth":
        return date_generator.generate(entity, output_gen="MIDDLE_OF_THE_YEAR")
    if entity.label == "social security number":
        return number_generator.generate(entity)
    return "[REDACTED]"
```

Anonymize the text using the anonymization mapping:

```python
from anonipy.anonymize.strategies import PseudonymizationStrategy

# initialize the pseudonymization strategy
pseudo_strategy = PseudonymizationStrategy(mapping=anonymization_mapping)

# anonymize the original text
anonymized_text, replacements = pseudo_strategy.anonymize(original_text, entities)
```

## Acknowledgements

[Anonipy](https://eriknovak.github.io/anonipy/) is developed by the
[Department for Artificial Intelligence](http://ailab.ijs.si/) at the
[Jozef Stefan Institute](http://www.ijs.si/), and other contributors.

The project has received funding from the European Union's Horizon Europe research
and innovation programme under Grant Agreement No 101080288 ([PREPARE](https://prepare-rehab.eu/)).

<figure >
  <img src="https://github.com/eriknovak/anonipy/blob/main/docs/assets/imgs/EU.png?raw=true" alt=European Union flag" width="80" />
</figure>
