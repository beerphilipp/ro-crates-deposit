# Notes on Mapping

## Resource Type mapping

- `resource_type` is a mandatory field in Datacite
-  RO-Crate does not have a field that describes the type of the entire directory
-  Therefore, the value `:unkn` is assigned to the `resource_type` field

## Creators mapping

- consists of `person or organization` and `affiliation`
- each parts are mapped to DataCite
- if none of the values exist, returns empty String
   

## Title mapping

- the `name` field is mapped to the `title` field as-is.
- in case `name` does not exist, it falls back to using the value of `@alternativeName`
- in case neither of those exist, `title` is assigned `:unkn`

## Additional title mapping

- `@alternativeName`isn mapped to `additional_titles[]` array
- `title` gets the value of `metadata.additional_titles[]`
- in its type, `alternative-title` gets the value of `Alternative Title`

## Mapping of publication date

- the `datePublished` field is mapped to `metadata.publication_date`. The value is mapped as-is. Processing of the value can be added in `mapping/processing_functions.py#dateProcessing`
- If no `datepublished` value is present, the `publication_date` is assigned the value `:unav`

## Mapping of rights/licenses

- the `identifier` field in DataCite is not mapped, since it defaults to SPDX this would require knowlege of the mapping of a licence URL to the SPDX id (https://spdx.org/licenses/)
- in case the RO-Crate does not reference another object, but contains a direct value the following is applied
  - if the value is a URL: only set the link value in the DataCite file
  - if the value is freetext: only set the description value in the DataCite file

