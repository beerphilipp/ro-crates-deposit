# RO-Crates Data Deposit


- Create an API Token
    - Go to `https://test.researchdata.tuwien.ac.at/account/settings/applications/tokens/new/` and create a new token.

- Copy and rename the file `credentials.template.py` to `credentials.py` and fill in your API key.


## JSON Notes

- `processing`: function that needs to be applied to the `from` value
- `onlyIf`: only counts and uses this `from` value if this function returns `True`