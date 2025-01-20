import os
import pandas as pd

# Path to the folder containing log files
folder_path = '/Users/xuyuan/workspace/PopFunc-paper/BMA_simulation/beast'

# Function to calculate the 95% credible set for a given file
def calculate_credible_set_for_file(file_path):
    df = pd.read_csv(file_path, sep='\t')
    I_data = df['I']

    frequencies = I_data.value_counts().sort_values(ascending=False)
    cumulative_frequencies = frequencies.cumsum() / frequencies.sum()

    credible_set = []
    for value, cumulative in cumulative_frequencies.items():
        credible_set.append(value)
        if cumulative >= 0.95:
            break

    return credible_set, frequencies / frequencies.sum()

# Counters for success and failure
total_success = 0
total_fail = 0
failed_files = []
true_indicator_probabilities = []
highest_indicator_probabilities = []

# Process all files in the folder
for i in range(100):
    file_name = f'SVS_Coal-{i}.log'
    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        credible_set, probabilities = calculate_credible_set_for_file(file_path)

        df = pd.read_csv(file_path, sep='\t')
        true_I = df['I'].iloc[0]

        true_probability = probabilities.get(true_I, 0)
        highest_probability = probabilities.max()

        true_indicator_probabilities.append(true_probability)
        highest_indicator_probabilities.append(highest_probability)

        if true_I in credible_set:
            result = "Success"
            total_success += 1
        else:
            result = "Fail"
            total_fail += 1
            failed_files.append(file_name)

        print(f"File {file_name}: True I={true_I}, Set={credible_set}, "
              f"True Prob={true_probability:.4f}, Highest Prob={highest_probability:.4f} - {result}")
    else:
        print(f"File {file_name} does not exist.")

# Calculate averages
average_true_probability = sum(true_indicator_probabilities) / len(true_indicator_probabilities) if true_indicator_probabilities else 0
average_highest_probability = sum(highest_indicator_probabilities) / len(highest_indicator_probabilities) if highest_indicator_probabilities else 0

# Output summary
print(f"\nSummary:")
print(f"Total Success: {total_success}")
print(f"Total Fail: {total_fail}")
if failed_files:
    print(f"Failed files: {', '.join(failed_files)}")
else:
    print("All files passed.")
print(f"Average posterior probability of true indicator: {average_true_probability:.4f}")
print(f"Average posterior probability of highest posterior indicator: {average_highest_probability:.4f}")
