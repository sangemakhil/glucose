import pandas as pd
from docx import Document
from datetime import datetime, timedelta
import re

def extract_and_process_word_data_corrected(file_path):
    """
    Extracts and processes food diary data with corrected date handling.
    """
    data = []
    current_date = None
    last_valid_date = None

    doc = Document(file_path)
    for table in doc.tables:
        for row in table.rows[1:]:  # Skip header row
            cells = [cell.text.strip() for cell in row.cells]
            if not any(cells):  # Skip empty rows
                continue

            # Extract Date and Time
            date_time = cells[0]
            date_match = re.match(r"(\d{1,2}/\d{1,2}/\d{4})|(\d{1,2}/\d{1,2})", date_time)
            time_match = re.search(r"(\d{1,2}:\d{2}\s*[ap]\.?m\.?)", date_time, re.IGNORECASE)

            # Update current date if a new date is found
            if date_match:
                raw_date = date_match.group(0)
                if len(raw_date.split("/")) == 2:  # MM/DD format
                    # Assume the most recent year if only MM/DD is given
                    current_date = f"{raw_date}/{datetime.now().year}"
                else:
                    current_date = raw_date

                try:
                    last_valid_date = datetime.strptime(current_date, "%m/%d/%Y")
                except ValueError:
                    last_valid_date = None

            # Propagate the last valid date for missing entries
            if last_valid_date:
                formatted_date = last_valid_date.strftime("%Y-%m-%d")
            else:
                formatted_date = "Invalid Date"

            # Extract and standardize time
            time = time_match.group(1) if time_match else "Missing Time"

            # Detect PM-to-AM transitions
            if time != "Missing Time" and "PM" in time.upper():
                last_time = datetime.strptime(time, "%I:%M %p")
                if "AM" in time.upper() and last_time.hour < 12 and last_valid_date:
                    last_valid_date += timedelta(days=1)  # Increment the date for AM after PM

            # Extract and clean other columns
            food = cells[1] if len(cells) > 1 else "Missing Food"
            amount = cells[2] if len(cells) > 2 else "Missing Amount"
            preparation = cells[3] if len(cells) > 3 else "Missing Preparation"
            prepared_by = cells[4] if len(cells) > 4 else "Missing Prepared By"
            activity_before = cells[5] if len(cells) > 5 else "Missing Activity Before"
            activity_after = cells[6] if len(cells) > 6 else "Missing Activity After"

            # Append structured data
            data.append({
                "Date": formatted_date,
                "Time": time,
                "Food": food,
                "Amount": amount,
                "Preparation": preparation,
                "Prepared By": prepared_by,
                "Activity Before": activity_before,
                "Activity After": activity_after
            })

    return pd.DataFrame(data)

def save_to_excel(df, output_path):
    """
    Saves the cleaned DataFrame to an Excel file.
    """
    df.to_excel(output_path, index=False)
    print(f"Data saved to {output_path}")

# Path to the uploaded file
file_path = '/content/Food Diary 2215.docx'

# Process and save data
output_path_corrected = 'Food_Diary_Corrected_Output.xlsx'

structured_data_corrected = extract_and_process_word_data_corrected(file_path)
save_to_excel(structured_data_corrected, output_path_corrected)

print(f"Processed file saved to: {output_path_corrected}")
