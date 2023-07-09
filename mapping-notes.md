# Notes on Mapping

## Mapping of resource type

- `resource_type` is a mandatory field in DataCite
-  RO-Crate does not have a field that describes the type of the entire directory
-  Therefore, we assume the type to be `dataset`

## Mapping of creators

- an `author` in RO-Crate is mapped to a `creator` in DataCite, alongside with their affiliations
- if the `@id` field of an author is an ORCiD, the ORCiD field is parsed and added in DataCite
- consists of `person or organization` and `affiliation`
- if no creator exists, the creator is chosen to be the value `:unkn`

## Mapping of contributors

- similar to creator mapping

## Mapping of title

- the `name` field is mapped to the `title` field
- in case `name` does not exist, it falls back to using the value of `@alternativeName`
- in case neither of those exist, `title` is assigned `:unkn`

## Mapping of additional title

- `@alternativeName` is mapped to `additional_titles`
- a new array entry in `additional_titles` is added
- the `lang` field is omitted, since we do not get information on the language of the additional title from RO-Crates.

## Mapping of publication date

- the `datePublished` field is mapped to `metadata.publication_date`
- the DataCite field may only contain the date, but not the time
- we try to guess the format and parse the date
- If no `datepublished` value is present, the `publication_date` is assigned the value `:unav`

## Mapping of description

- `description` field is mapped as-is to `metadata.description`

## Mapping of additional description

- RO-Crates does not have any additional description. This `additional_descriptions` field in DataCite is thus never assigned any value.

## Mapping of rights/licenses

- the `identifier` field in DataCite is not mapped, since it defaults to SPDX this would require knowlege of the mapping of a licence URL to the SPDX id (https://spdx.org/licenses/)
- in case the RO-Crate does not reference another object, but contains a direct value the following is applied
  - if the value is a URL: only set the link value in the DataCite file
  - if the value is freetext: only set the description value in the DataCite file

## Mapping of subjects

- `keywords` field is mapped to `subjects` field

## Mapping of languages

- `inLanugage` is mapped to `metadata.languages`
- we try to understand what a language is given free text and then map it to the ISO-639-3 language code (as expected by InvenioRDM)
- if we cannot find out what language it is, we omit the field

## Mapping of dates

- `temporalCoverage` is mapped as-ios to `metadata.dates`. The type of the date is "other" and the description is "Temporal Coverage".

## Mapping of version

- maps the `version` field to `metadata.version`

## Mapping of publisher

- maps `publisher.name` to `metadata.publisher`
- if no publisher exists, the value is `:unkn`

## Mapping of identifier

- the `identifier` field of RO-Crate is mapped to to `identifier` array in DataCite
- the mapping currently only processes DOIs
- adding new schemes can easily be added in `mapping/mapping.json` 

## Mapping of sizes

- `contentSize` field is mapped to `metadata.sizes`

## Mapping of formats

- `encodingFormat` field is mapped to `metadata.formats`

## Mapping of locations

- we currently only support free text locations and locations in the geonames scheme
- support for other schemes can easily be added in `mapping/mapping.json`
- the `contentLocation` field is mapped to the `locations` field in RO-Crate.

## Mapping of funding references

- only the funder's name is mapped, since the ID in DataCite needs to be of a controlled vocabulary (and we don't know this controlled vocabulary)

## Embargo mapping

- if the `datePublished` field in the RO-Crate metadata file is in the future, an embargo is applied to the resource
- the processing of the data to set the embargo period is a best-effort approach and is located in `mapping/processing_functions.py#embargoDateProcessing`
