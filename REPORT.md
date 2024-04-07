# Report

## Identified Data Issues

The preprocessing showed the following issues within the dataset:

1. **Missing Attribute**:
   - The `group_vehicle_number` attribute is missing in several files.

2. **Duplicate Metadata Entries**:
   - One file contained duplicate copy of the entire metadata.

3. **Invalid Unicode Sequence**:
   - Invalid Unicode escape sequences were found, that caused decoding errors during the json parsing:
    E.g: `pedestr\ufian`.

4. **Missed String Termination**:
   - One file contains not properly terminated string, as result of invalid unicode sequence. E.g: `cl\ufoud\ufy`.

5. **Invalid Datatype**:
   - One file has attribute `total_driven_km` that has value of type float instead of string: E.g: 0.005

## Approach to Problem Identification
The initial idea was to initialize a pandas DataFrame, where the columns would be the elements of a json file with valid metadata and the data would be list of dictionaries, where each dictionary represents one concrete instance in our dataset.

The assumption was that some errors will be thrown in the JSON parsing phase indicating the problems with the data. If not, the data would be analyzed manually, applying some statistical and exploratory analysis techniques, such as using the `unique` method etc.

### Parsing Errors Encountered:

During the JSON parsing with Python, the following errors were encountered, each pointing to a specific type of data issue:

- `Error decoding JSON from ./data/gmdm_2412.json: Invalid \uXXXX escape: line 1 column 133 (char 132)`
- `Error decoding JSON from ./data/gmdm_2634.json: Extra data: line 2 column 1 (char 165)`
- `Error decoding JSON from ./data/gmdm_3200.json: Invalid \uXXXX escape: line 1 column 133 (char 132)`

### Pydantic Validation:

Additional validation was performed using the Pydantic library, which checks for the presence of defined attributes and verifies if their datatypes are as expected. This validation process provided information about missing attributes and invalid datatypes.
