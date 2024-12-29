import pandas as pd
import zipfile
import logging

# Constants
DATA_FILE = "../../data/data.zip"  # Ensure the correct path to the ZIP file
OUTPUT_FILE = "../../data/transform.csv"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

try:
    # Extract and read the CSV file from the ZIP
    with zipfile.ZipFile(DATA_FILE, 'r') as z:
        csv_filename = z.namelist()[0]  # Get the first file name inside the ZIP
        df = pd.read_csv(z.open(csv_filename))
    
    logging.info("Data loaded successfully.")
    logging.info(f"Preview of data:\n{df.head()}")

    # Initialize an empty DataFrame for cleaned data
    df_cleaned = pd.DataFrame()
    i = 0

    # Process rows in groups of 6
    while i + 5 < df.shape[0]:
        df_cleaned_temp = pd.DataFrame()
        df_cleaned_temp['Title'] = df.iloc[i]
        df_cleaned_temp['Company Name'] = df.iloc[i + 1].astype(str).str.split('|').str[0].str.strip()

        # Split row data dynamically
        split_data = df.iloc[i + 2].astype(str).str.split('|', expand=True).apply(lambda x: x.str.strip())
        num_cols = split_data.shape[1]

        # Handle varying numbers of columns in split_data
        if num_cols >= 3:
            df_cleaned_temp[['Experience', 'Salary', 'Locations']] = split_data.iloc[:, :3]
        elif num_cols == 2:
            df_cleaned_temp[['Experience', 'Salary']] = split_data.iloc[:, :2]
            df_cleaned_temp['Locations'] = None
        elif num_cols == 1:
            df_cleaned_temp['Experience'] = split_data.iloc[:, 0]
            df_cleaned_temp['Salary'] = None
            df_cleaned_temp['Locations'] = None
        else:
            df_cleaned_temp[['Experience', 'Salary', 'Locations']] = None

        # Add other columns
        df_cleaned_temp['Descriptions'] = df.iloc[i + 3]
        df_cleaned_temp['Skills'] = df.iloc[i + 4]
        df_cleaned_temp['Date'] = df.iloc[i + 5].astype(str).str.split('|').str[0].fillna("Not Available").str.strip()

        # Create Job Id
        title_value = str(df_cleaned_temp['Title'].iloc[0])  # Ensure it's a string
        if title_value != 'nan' and title_value != '':
            job_id_prefix = ''.join([word[:2].upper() for word in title_value.split()[:2]])
        else:
            job_id_prefix = 'XX'

        df_cleaned_temp['Job Id'] = job_id_prefix + str(i + 1).zfill(4)

        # Append to the main DataFrame
        df_cleaned = pd.concat([df_cleaned, df_cleaned_temp], ignore_index=True)

        # Move to the next set of rows
        i += 6

    # Rearrange columns
    df_cleaned = df_cleaned[['Job Id', 'Title', 'Company Name', 'Experience', 'Salary', 'Locations', 'Date', 'Descriptions', 'Skills']]

    # Save the cleaned DataFrame to a CSV file
    df_cleaned.to_csv(OUTPUT_FILE, index=False)
    logging.info(f"CSV file created successfully at {OUTPUT_FILE}.")
except Exception as e:
    logging.error(f"An error occurred: {e}")
