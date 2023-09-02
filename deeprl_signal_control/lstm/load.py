import json
import numpy as np

# Load JSON data from the file
with open("values.json", "r") as json_file:
    data = json.load(json_file)

# Extract the predicted values from the loaded data
predicted_values = np.array(data["predicted_values"])

# Now you can use the predicted_values array as needed
print(predicted_values)
