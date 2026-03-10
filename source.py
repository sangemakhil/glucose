import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
from google.colab import files

# Upload files using Colab's file upload functionality
def upload_files():
    print("Please upload your glucose data file:")
    uploaded = files.upload()  # Allows user to upload files interactively
    return uploaded

# Load glucose data from uploaded Excel file
def load_glucose_data(file_name):
    try:
        glucose_data = pd.read_excel(file_name, engine='openpyxl', skiprows=6)  # Specify engine for .xlsx files
        glucose_data.columns = [
            "Index", "Timestamp", "Event Type", "Event Subtype", "Patient Info",
            "Device Info", "Source Device ID", "Glucose Value (mg/dL)", "Insulin Value (u)",
            "Carb Value (grams)", "Duration (hh:mm:ss)",
            "Glucose Rate of Change (mg/dL/min)", "Transmitter Time", "Transmitter ID"
        ]
        glucose_data = glucose_data[["Timestamp", "Glucose Value (mg/dL)"]].dropna()
        glucose_data["Timestamp"] = pd.to_datetime(glucose_data["Timestamp"], errors='coerce')
        glucose_data["Glucose Value (mg/dL)"] = pd.to_numeric(glucose_data["Glucose Value (mg/dL)"], errors='coerce')
        glucose_data = glucose_data.dropna()  # Drop rows with NaN values after conversion
        print("Glucose Data Loaded Successfully:")
        print(glucose_data.head())
        return glucose_data
    except Exception as e:
        print(f"Error loading glucose data: {e}")
        return None

# Load food diary data from a CSV file
def load_food_diary(file_path):
    """
    Loads food diary data from a specified CSV file path.
    The CSV file should have columns: 'Date', 'Time', 'Food'.
    """
    try:
        food_diary = pd.read_csv(file_path)
        if not {"Date", "Time", "Food"}.issubset(food_diary.columns):
            raise ValueError("Food diary file must contain 'Date', 'Time', and 'Food' columns.")

        # Convert to list of dictionaries
        food_diary_data = food_diary.to_dict(orient="records")
        print("Food Diary Data Loaded Successfully:")
        for entry in food_diary_data[:5]:  # Show only the first 5 entries for brevity
            print(f"Date: {entry['Date']}, Time: {entry['Time']}, Food: {entry['Food']}")
        return food_diary_data
    except Exception as e:
        print(f"Error loading food diary: {e}")
        return None

# Function to identify spikes in glucose and calculate duration
def detect_spikes_and_durations(glucose_data, threshold=140):
    spikes = []
    start_time = None
    max_glucose = 0
    for i, row in glucose_data.iterrows():
        if row["Glucose Value (mg/dL)"] > threshold:
            if start_time is None:
                start_time = row["Timestamp"]
            max_glucose = max(max_glucose, row["Glucose Value (mg/dL)"])
        elif start_time is not None:
            # End of a spike
            duration = (row["Timestamp"] - start_time).total_seconds()
            spikes.append({
                "start_time": start_time,
                "end_time": row["Timestamp"],
                "duration_seconds": duration,
                "max_glucose": max_glucose
            })
            start_time = None
            max_glucose = 0  # Reset for next spike

    return spikes

# Plot glucose data with food diary overlay and highlight spikes
def plot_glucose_with_food_and_spikes(glucose_data, food_diary, spikes):
    plt.figure(figsize=(14, 7))

    # Plot glucose data
    plt.plot(glucose_data["Timestamp"], glucose_data["Glucose Value (mg/dL)"], label="Glucose Level", color="blue")

    # Overlay food diary entries
    for entry in food_diary:
        # Parse entry time
        entry_time = datetime.strptime(f"{entry['Date']} {entry['Time']}", "%Y-%m-%d %I:%M %p")
        plt.axvline(entry_time, color="red", linestyle="--", alpha=0.7)
        plt.text(entry_time, glucose_data["Glucose Value (mg/dL)"].max() * 0.9, entry['Food'],
                 rotation=90, verticalalignment='center', fontsize=8, color="red")

    # Highlight spikes
    for spike in spikes:
        plt.axvspan(spike["start_time"], spike["end_time"], color='yellow', alpha=0.3)
        plt.text(spike["start_time"], spike["max_glucose"] * 0.8, f"Spike {spike['max_glucose']}",
                 color="black", fontsize=10, verticalalignment='bottom')

    # Graph labels and legend
    plt.title("Glucose Levels Over Time with Food Diary Entries and Spikes")
    plt.xlabel("Timestamp")
    plt.ylabel("Glucose Value (mg/dL)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Upload glucose data file interactively
    uploaded_files = upload_files()
    glucose_file_name = list(uploaded_files.keys())[0]  # Get the uploaded glucose file name

    # Specify the path to the food diary CSV file
    food_diary_file_path = "/path/to/food_diary.csv"

    # Load glucose data
    glucose_data = load_glucose_data(glucose_file_name)

    # Load food diary data
    food_diary = load_food_diary(food_diary_file_path)

    # Detect spikes and calculate durations
    if glucose_data is not None and food_diary is not None:
        spikes = detect_spikes_and_durations(glucose_data)

        # Plot glucose data with food diary and spike highlights
        plot_glucose_with_food_and_spikes(glucose_data, food_diary, spikes)

        # Output details of spikes and their corresponding durations
        for spike in spikes:
            print(f"Spike detected from {spike['start_time']} to {spike['end_time']} with max glucose {spike['max_glucose']} mg/dL and duration {spike['duration_seconds']} seconds")
