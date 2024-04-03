import csv

def generate_insert_statements(csv_file_path, output_file_path):
    type_descriptions = {}
    utilities = {}
    locations = {}
    makes = {}
    insert_statements = []

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # Print column names for debugging
        print(f"Column names are: {', '.join(reader.fieldnames)}")
        for row in reader:
            # Adjust column accesses according to the printed column names
            type_description = row['TypeDescription'].strip()  # Using .strip() to remove any leading/trailing spaces
            # Similar adjustments for other fields...
            utility_name = row['UtilityName'].strip()
            location_key = (row['City'].strip(), row['County'].strip(), row['State'].strip(), row['Postal Code'].strip(), row['2020 Census Tract'].strip())
            make_model_key = (row['Make'].strip(), row['Model'].strip())
            type_description = row['TypeDescription']
            if type_description not in type_descriptions:
                type_descriptions[type_description] = len(type_descriptions) + 1
                insert_statements.append(f"INSERT INTO ElectricVehicleTypes (TypeDescription) VALUES ('{type_description}');")
            
            utility_name = row['UtilityName']
            if utility_name not in utilities:
                utilities[utility_name] = len(utilities) + 1
                insert_statements.append(f"INSERT INTO ElectricUtilities (UtilityName) VALUES ('{utility_name}');")

            location_key = (row['City'], row['County'], row['State'], row['Postal Code'], row['2020 Census Tract'])
            if location_key not in locations:
                locations[location_key] = len(locations) + 1
                insert_statements.append(f"INSERT INTO Locations (City, County, State, PostalCode, CensusTract) VALUES ('{location_key[0]}', '{location_key[1]}', '{location_key[2]}', {location_key[3]}, {location_key[4]});")

            make_model_key = (row['Make'], row['Model'])
            if make_model_key not in makes:
                makes[make_model_key] = len(makes) + 1
                insert_statements.append(f"INSERT INTO Makes (Make, Model) VALUES ('{make_model_key[0]}', '{make_model_key[1]}');")

            vehicle_values = (
                row['VIN'],
                row['Model Year'],
                makes[make_model_key],
                locations[location_key],
                type_descriptions[type_description],
                row['CAFVEligibility'],
                row['Electric Range'],
                row['Base MSRP'],
                row['Vehicle Location'],
                row['DOL Vehicle ID'],
                utilities[utility_name]
            )
            insert_statements.append("INSERT INTO Vehicles (VIN, ModelYear, MakeID, LocationID, ElectricVehicleTypeID, CAFVEligibility, ElectricRange, BaseMSRP, VehicleLocation, DOLVehicleID, ElectricUtilityID) VALUES " + str(vehicle_values) + ";")

    with open(output_file_path, 'w', encoding='utf-8') as f:
        for statement in insert_statements:
            f.write(statement + "\n")
# path to the data
csv_file_path = '\\Electric_Vehicle_Population_Data.csv'
output_file_path = 'data.txt'
generate_insert_statements(csv_file_path, output_file_path)
