# Notes on Mapping

## Resource Type mapping

- `resource_type` is a mandatory field in DataCite
-  RO-Crate does not have a field that describes the type of the entire directory
-  Therefore, we assume the type to be `dataset`

## Creators mapping

- consists of `person or organization` and `affiliation`
- each parts are mapped to DataCite
- if none of the values exist, returns empty String
   

## Title mapping

- the `name` field is mapped to the `title` field as-is.
- in case `name` does not exist, it falls back to using the value of `@alternativeName`
- in case neither of those exist, `title` is assigned `:unkn`

## Additional title mapping

- `@alternativeName` is mapped to `additional_titles`
- a new array entry in `additional_titles` is added
- the `lang` field is omitted, since we do not get information on the language of the additional title from RO-Crates.

## Mapping of publication date

- the `datePublished` field is mapped to `metadata.publication_date`. The value is mapped as-is. Processing of the value can be added in `mapping/processing_functions.py#dateProcessing`
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

## Contributors mapping

- similar mapping like in `Creators` mapping


## Subjects mapping

- `keywords` field is mapped to `"metadata.subjects[]` field
- it is an array and gets all the values from keywords

## Languages mapping

- `inLanugage` is mapped to `metadata.languages[]` array and gets all the values from inLanguage
- the mapping can happen with `inLanguage.name` property, in this case `metadata.languages[]` gets the values 

## Dates mapping

- `temporalCoverage` is mapped to `metadata.dates.date`, and gets the value from the RO Crate

## Version mapping

- maps the `version` field to `metadata.version`

## Publisher mapping

- maps `publisher.name` to `metadata.publisher`

## Identifier mapping

- the `identifier` field of RO-Crate is mapped to `pids`
- the mapping currently only processes DOIs
- adding new schemes can easily be added in `mapping/mapping.json` 

## Related identifier mapping

- maps `thumbnail.@id` to `metadata.related_identifiers.identifier`
- must be DOI format, if not, returns empty string

## Sizes mapping

- `contentSize` field is mapped to `metadata.sizes`

## Formats mapping

- `encodingFormat` field is mapped to `metadata.formats`

## Locations mapping

- can be the `$contentLocation.name` attribute, which is mapped to `metadata.locations[].features[].place`

- also can be the `$contentLocation.@id`, this field is mapped to `metadata.locations[].features[].identifiers[]`

## Funding references mapping

- in OFR format, the `$funder.@id` is mapped to `metadata.funding.funder.id`
- in ROR, `$funder.@id` relates to `metadata.funding.funder.id`
- as for award field, `$funder.Person.award` has a mapping to `metadata.funding.funder.award.id`

## References mapping

- the references are got from `exifData.@id` and mapped to `metadata.references[].identifier` array

## Embargo mapping

- if the `datePublished` field in the RO-Crate metadata file is in the future, an embargo is applied to the resource
- the processing of the data to set the embargo period is a best-effort approach and is located in `mapping/processing_functions.py#embargoDateProcessing`