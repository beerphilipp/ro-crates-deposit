# RO-Crates Data Deposit

Command line tool to deposit a [RO-Crate directory](https://www.researchobject.org/ro-crate/) to an [InvenioRDM](https://inveniordm.web.cern.ch/). 

## Requirements

- [`Python 3.x`](https://www.python.org/downloads/)

## Usage

- Create an InvenioRDM API token
  - go to `<base_url>/account/settings/applications/tokens/new/`
  - in case of TU Wien, go to: [https://test.researchdata.tuwien.ac.at/account/settings/applications/tokens/new/](https://test.researchdata.tuwien.ac.at/account/settings/applications/tokens/new/)

![](./images/researchdata.png)


- Set up the environmental variables
  - copy and rename `credentials.template.py` to `credentials.py` in the same folder
  - open `credentials.py` with a text editor and fill in your API key in the `api_key` variable
  - fill in the InvenioRDM base URL in the `repository_base_url` variable
    - in case of TU Wien: use `https://test.researchdata.tuwien.ac.at/`


- Set up the Python environment
  - Run `python3 -m pip install -r requirements.txt`

- Uploa the RO-Crate directory
  - Run `python3 deposit.py <ro-crate-dir>` with the RO-Crate directory as parameter. The record is saved as a draft and not published
  - Run `python3 deposit.py -p <ro-crate-dir>` with the RO-Crate directory as parameter to publish the record.
  - Run `python3 deposit.py -h` for help.

> **NOTE:** This tool is a *best-effort* approach. After converting the metadata file, the resulting DataCite file is stored as `datacite-out.json` in the root directory. Users can adjust the generated DataCite file as needed. To use the adjusted DataCite file for upload and skip the process of conversion, run the program as follows:\
 `python3 deposit.py -d <datacite-file> <ro-crate-dir>`.

## File structure

The project consists of the following structure:

- `/mapping`: Contains code for the mapping process
  - `converter.py`: Python script used to map between RO-Crates and DataCite. Not to be called by the user.
  - `mapping.json`: Encodes the mapping between RO-Crates and DataCite. See [Mapping](#mapping) for more. 
  - `condition_functions.py`: Defines functions used for the mapping. See [Conditon Functions](#condition-functions) for more.
  - `processing_functions.py`: Defines functions used for the mapping. See [Processing Functions](#processing-functions) for more.
- `/upload`: Contains code for the upload process
  - `uploader.py`: Python script used to upload the files to the InvenioRDM. Not to be called by the user.
- `deposit.py`: Starting point. Used to map and upload the RO-Crate directory.
- `credentials.template.py`: Template file for the environment variables.

## Mapping

The project aims at decoupling the definition of the mapping between RO-Crates and DataCite from code. This means, that users can quickly change/add/remove mapping rules without code changes. 

The mapping is implemented in `/mapping/converter.py`. The mapping rules are defined in `/mapping/mapping.json`. Processing functions and condition functions are defined in `/mapping/processing_functions.py` and `condition_functions.py`, respectively. A textual description including shortcomings and assumptions of the mapping can be found in [mapping-notes.md](./mapping-notes.md).

### Mapping format

The mapping is defined in `/mapping/mapping.json` and consists of **Mapping Collections** and **Mapping Rules**.

#### Mapping Collections

A Mapping Collection bundles different mapping rules together, e.g. rules that define the mapping between `author` in RO-Crates and `creators` in DataCite. Each mapping collection contains the following keys:

| Key    |  Description |    Possible values | Mandatory?  |
|---------------|-------------- | ---------------  |-------------|
| `mappings`   |  contains the mapping rules   |  mapping rules          | yes (unless `_ignore` is present)         |
| `_ignore`     |  ignores the mapping rule if present     | any  | no   |
| `ifNonePresent` | in case no mapping rule is applied, the value defined here is applied | see below | no

##### `ifNonePresent`

`ifNonePresent` can be used to specify what happens if no Mapping Rule of the defined Mapping Rules in the current Mapping Collection is applied. The value of the field is an array of the following form: 

```json
{
  "<to_query>": "<value>"
}
```

In case no Mapping Rule is applied, the value specified in `<value>` is applied to the field defined by `<to_query>` in the DataCite.

#### Mapping Rules

A Mapping Rule defines which fields from RO-Crates are mapped to which fields in DataCite.

Each rule may contain the following keys:


| Key    |  Description |    Possible values | Mandatory?  |
|---------------|-------------- | ---------------  |-------------|
| `from`   |  defines the source in the RO-Crates file   |  query string (see below)          | yes         |
| `to`     |  defines the target in the DataCite file     | query string (see below)        | yes         |
| `value`  | allows value transformations | may be a string, array, or object | no |
| `processing` | uses a processing function | string starting with `$` and referencing an existing processing function | no |
| `onlyIf` | uses a condition function | string starting with `?` and referencing an existing condition function | no |    
| `_ignore` | ignores the rule if present | any | no |    

#### `from` and `to` querying

To define the mapping between RO-Crates and DataCite, it is necessary to specify which field in RO-Crates is mapped to which field in DataCite. This is achieved by specifying the `from` and `to` fields in a Mapping Rule.

**Example**

Given the following RO-Crates metadata file:

```json
{
    "@context": "https://w3id.org/ro/crate/1.1/context", 
    "@graph": [
        {
            "@type": "CreativeWork",
            "@id": "ro-crate-metadata.json",
            "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
            "about": {"@id": "./"}
        },  
        {
            "@id": "./",
            "@type": "Dataset",
            "name": "Name",
            "author": {"@id": "https://orcid.org/0000-0002-8367-6908"}
        },
        {
            "@id": "https://orcid.org/0000-0002-8367-6908",
            "@type": "Person",
            "name": "J. Xuan"
        }
    ]
}
```

Speficifying the `title` field is achieved with `title`. In case the value of a key refers to another object, such as in the case of authors, querying is done using the `$` charater. Refering to the `name` field of an `author` is done using `$author.name`. It is important to note, that the `author` field may be an array. Therefore, it is necessary to mark this as a possible array. Refering to this value can be done by using the `[]` characters, i.e., `$author[].name`.

Specifying the DataCite field is done in a similar fashion.



#### Processing functions

Processing functions are functions that are applied to the raw source value extracted from the RO-Crates metadata file. When a processing function wants to be applied to a mapping rule, the `processing` entry is assigned the value `$<function_name>`. The function then needs to be implemented in `/mapping/processing_functions.py`. 

**Example**

Given is the following mapping of the author type:

```json
"person_or_org_type_mapping": {
    "from": "$author.@type",
    "to": "metadata.creators[].person_or_org.type",
    "processing": "$authorProcessing"
}
```

The value `Person` in the RO-Crates metadata file should be mapped to the value `personal`. Also, the value `Organization` should be mapped to the value `organizational`. The function `authorProcessing` can now be implemented in `/mapping/processing_functions.py` to achieve this logic. Note that the value of the `processing` key in the mapping rule and the function name need to coincide:

```py
def authorProcessing(value):
    if value == "Person":
        return "personal"
    elif value == "Organization":
        return "organizational"
    else:
        return ""
```


#### Condition functions

Condition functions are similar to processing functions. Condition functions can be used to restrict when a mapping rule should be executed. The mapping is executed, if the function defined in the `onlyIf` key returns true.

**Example**

The mapping of DOI identifiers looks as follows:

```json
"alternate_mapping": {
  "from": "identifier",
  "to": "metadata.identifiers[]",
  "value": {
      "scheme": "doi",
      "identifier": "@@this"
  },
  "processing": "$doi_processing",
  "onlyIf": "?doi"
}
```

The mapping should only be executed, if the value in the `identifier` field in the RO-Crates metadata file is indeed a DOI identifier. This check can be achieved by defining the `doi` function in `/mapping/condition_functions.py`. Note that the value of the `onlyIf` key in the mapping rule and the function name need to coincide:

```py
def doi(value):
    return value.startswith("https://doi.org/")
```


#### Value formatting

A value can also be formatted, e.g. as needed when a value in RO-Crate needs to be transformed to another value in DataCite. Although this can also be achived using a processing function, value transformations provide an easier alternative. Every occurence of `@@this` is replaced by the source value.

**Example**

Given the following mapping rule:
```json
"languages_mapping_direct": {
  "from": "inLanguage",
  "to": "metadata.languages[]",
  "value": {
    "id": "@@this"
  }
}
```

The RO-Crate entry 
```json
...
"inLanguage": "en"
...
```

is transferred into 

```json
"metadata": {
  "languages": [
    {
      "id": "en"
    }
  ]
}
```

#### Flow

This figure illustrates how the functions that are applied in a mapping rule.

![](./images/mapping_rule_flow.svg)

## Results

TODO: Add Results

## Known problems

- Problem 1