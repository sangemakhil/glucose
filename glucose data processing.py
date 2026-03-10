import pandas as pd

def process_glucose_files(file_paths, output_path):
    """
    Process glucose data files, extract relevant data, and save combined cleaned data to a CSV file.

    :param file_paths: List of file paths to process
    :param output_path: Path to save the combined CSV file
    """
    # Columns of interest
    columns_of_interest = ["Timestamp (YYYY-MM-DDThh:mm:ss)", "Glucose Value (mg/dL)"]
    processed_data = []

    for file_path in file_paths:
        try:
            # Read the file completely without skipping rows
            raw_data = pd.read_csv(file_path, header=None)

            # Identify the header row dynamically by looking for expected columns
            header_row_index = raw_data[raw_data.iloc[:, 1].str.contains("Timestamp", na=False)].index[0]

            # Read the data again with the correct header
            data = pd.read_csv(file_path, skiprows=header_row_index)

            # Select only the columns of interest
            if set(columns_of_interest).issubset(data.columns):
                cleaned_data = data[columns_of_interest].copy()

                # Rename columns for uniformity
                cleaned_data.columns = ["Timestamp", "Glucose Reading"]

                # Clean and standardize timestamp format
                cleaned_data["Timestamp"] = pd.to_datetime(cleaned_data["Timestamp"], errors="coerce")

                # Drop rows with invalid timestamps or glucose readings
                cleaned_data.dropna(subset=["Timestamp", "Glucose Reading"], inplace=True)

                # Separate Date and Time into individual columns
                cleaned_data["Date"] = cleaned_data["Timestamp"].dt.date
                cleaned_data["Time"] = cleaned_data["Timestamp"].dt.strftime('%H:%M')  # Format time without seconds

                # Drop the original Timestamp column
                cleaned_data.drop(columns=["Timestamp"], inplace=True)

                # Rearrange columns: Date, Time, Glucose Reading
                cleaned_data = cleaned_data[["Date", "Time", "Glucose Reading"]]

                # Append to the list
                processed_data.append(cleaned_data)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    # Combine all data into a single DataFrame if data exists
    if processed_data:
        final_combined_data = pd.concat(processed_data, ignore_index=True)

        # Drop duplicate readings based on Date, Time, and glucose value
        final_combined_data.drop_duplicates(subset=["Date", "Time", "Glucose Reading"], inplace=True)

        # Sort by Date and Time
        final_combined_data.sort_values(by=["Date", "Time"], inplace=True)

        # Save to a CSV file
        final_combined_data.to_csv(output_path, index=False)
        print(f"Data successfully saved to {output_path}")
    else:
        print("No valid data was found in the files.")

# Example usage
file_paths = [
    '2230-V1-data.csv',
    '2230-V2-data.csv',
    
]
output_path = 'glucose_data.csv'

process_glucose_files(file_paths, output_path)
