import json

# List of child properties to remove
properties_to_remove = [
"usCongressBioId",
"middleName",
"honorificPrefix",
"unaccentedFamilyName",
"unaccentedGivenName",
"unaccentedMiddleName",
"birthCirca",
"deathCirca",
"relationship",
"jobType",
"congress",
"caucusAffiliation",
"creativeWork",
"researchRecord",
"deleted",
"image",
"startDate",
"startCirca",
"note",
"endDate",
"endCirca"
"departureReason",
]

# Recursive function to remove specified properties
def remove_properties(obj, properties):
    if isinstance(obj, dict):
        for prop in properties:
            if prop in obj:
                del obj[prop]
        for key in obj.keys():
            remove_properties(obj[key], properties)
    elif isinstance(obj, list):
        for item in obj:
            remove_properties(item, properties)

# Function to remove subsequent occurrences of 'congressAffiliation' within 'jobPositions'
def remove_subsequent_affiliations(member):
    if 'jobPositions' in member and isinstance(member['jobPositions'], list):
        first_affiliation_found = False
        new_job_positions = []  # List to hold job positions that are not empty
        for job_position in member['jobPositions']:
            if 'congressAffiliation' in job_position:
                if first_affiliation_found:
                    continue  # Skip subsequent affiliations
                else:
                    first_affiliation_found = True
            new_job_positions.append(job_position)
        member['jobPositions'] = new_job_positions  # Update with non-empty job positions

# Read data from file
with open('C:\\Users\\PastorOnTheTech\\Documents\\Python Prjoects\\Database IT\\merged.json', 'r') as infile:
    data = json.load(infile)

# Remove specified properties from each object
remove_properties(data, properties_to_remove)

# Remove subsequent occurrences of 'congressAffiliation' from each object
for member in data:
    remove_subsequent_affiliations(member)

# Write modified data to new file
with open('output_file.json', 'w') as outfile:
    json.dump(data, outfile, indent=2)

