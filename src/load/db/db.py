import psycopg
from psycopg.errors import UniqueViolation
from dotenv import load_dotenv  # Install python-dotenv using `pip install python-dotenv`
import os
import csv


# Load environment variables from .env file
load_dotenv()

PATH="../../../data/transform.csv"

def connect_to_db():
    try:
        # Retrieve the database URL from environment variables
        database_url = os.getenv("DB_URL")
        if not database_url:
            raise ValueError("DATABASE_URL is not set in the environment.")
        
        # Connect to the database
        conn = psycopg.connect(database_url)
        print("Connection established!")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def print_column_types(cursor):
    query = """SELECT column_name, data_type 
               FROM information_schema.columns 
               WHERE table_schema = 'data_analyst_job' AND table_name = 'jobs';"""
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)
    except Exception as e:
        print(f"Error fetching column types: {e}")

def insert_jobs(cursor, jobs):
    """Insert job data into the database."""
    try:
        insert_query = """
        INSERT INTO data_analyst_job.jobs 
        (Job_Id, Title, Company_Name, Experience, Salary, Locations, Job_Date, Descriptions, Skills)
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.executemany(insert_query, jobs)
        print("Jobs inserted successfully.")
    except Exception as e:
        print(f"Error inserting jobs: {e}")
        cursor.connection.rollback()
        return False
    return True

def insert_from_csv(cursor, csv_file_path):
    """
    Insert data from a CSV file into the database, ensuring no duplicate Job_Id values.
    :param cursor: Database cursor
    :param csv_file_path: Path to the CSV file
    """
    try:
        with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file) 
            
            # Iterate over each row in the CSV
            for row in csv_reader:
                job_id = row.get("Job Id")
                title = row.get("Title")
                company_name = row.get("Company Name")
                experience = row.get("Experience")
                salary = row.get("Salary")
                locations = row.get("Locations")
                job_date = row.get("Date")
                descriptions = row.get("Descriptions")
                skills = row.get("Skills")

                # Check if the Job_Id already exists
                check_query = "SELECT COUNT(*) FROM data_analyst_job.jobs WHERE Job_Id = %s"
                cursor.execute(check_query, (job_id,))
                exists = cursor.fetchone()[0] > 0

                if exists:
                    print(f"Skipping Job_Id {job_id}: already exists.")
                    continue  

                # Insert the new row into the table
                insert_query = """
                INSERT INTO data_analyst_job.jobs 
                (Job_Id, Title, Company_Name, Experience, Salary, Locations, Job_Date, Descriptions, Skills)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                try:
                    cursor.execute(
                        insert_query,
                        (job_id, title, company_name, experience, salary, locations, job_date, descriptions, skills),
                    )
                    print(f"Inserted Job_Id {job_id} successfully.")
                except UniqueViolation:
                    print(f"Job_Id {job_id} caused a unique constraint violation. Skipping.")
    except Exception as e:
        print(f"Error processing the CSV file: {e}")

def main():
    conn = connect_to_db()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        # Ensure the schema and table exist
        create_schema_query = "CREATE SCHEMA IF NOT EXISTS data_analyst_job"
        cur.execute(create_schema_query)

        create_table_query = """
        CREATE TABLE IF NOT EXISTS data_analyst_job.jobs (
            Job_Id VARCHAR(20) PRIMARY KEY,
            Title VARCHAR(255) NOT NULL,
            Company_Name VARCHAR(255) NOT NULL,
            Experience VARCHAR(100),
            Salary VARCHAR(100),
            Locations VARCHAR(255),
            Job_Date VARCHAR(255),
            Descriptions TEXT,
            Skills TEXT
        );
        """
        cur.execute(create_table_query)

        # # Alter the column type for Job_Id if needed
        # alter_column_query = "ALTER TABLE data_analyst_job.jobs ALTER COLUMN Job_Id TYPE VARCHAR(20);"
        # cur.execute(alter_column_query)
        # print("Column Job_Id type altered successfully.")

        # Print column types for verification
        query = """
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_schema = 'data_analyst_job' AND table_name = 'jobs';
        """
        cur.execute(query)
        column_types = cur.fetchall()
        print("Column types in data_analyst_job.jobs:")
        for column in column_types:
            print(column)

        # # List of jobs to insert
        # jobs = [
        #     ("DAVE0001", "Data Verification Analyst", "Foundation Ai", "0-5 Yrs", "Not disclosed", 
        #      "Kolkata, Mumbai, New Delhi, Hyderabad, Pune, Chennai, Bengaluru", "1 Day Ago", 
        #      "Foundation AI is looking for Data Verification Analyst to join our dynamic team and emb...", 
        #      "metadatapythondata analysisdata managementdata analyticsdata validationconfigurationdata mining"),
             
        #     ("TEME0007", "Team Member Data Analyst", "Bajaj Allianz General Insurance", "0-4 Yrs", "Not disclosed", 
        #      "Pune", "13 Days Ago", 
        #      "Comprehend customize report requirement by stakeholders (NHOD, zonal heads, vertical he...", 
        #      "AutomationData validationProcess efficiencyActuarialData qualityData analyticsData AnalystManager Quality Control")
        # ]

        # # Insert the job data
        # if insert_jobs(cur, jobs):
        #     print("Jobs inserted successfully.")

        # Show the table content
         
         # inserting csv file into database
        #------------------------------------

        insert_from_csv(cur,PATH)
        #------------------------------------

        cur.execute("SELECT * FROM data_analyst_job.jobs WHERE experience = %s", ("0-2 Yrs",))
        rows = cur.fetchall()
        print("Data in data_analyst_job.jobs:")
        for row in rows:
            print(row)

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()  # Rollback any changes if an error occurs
    finally:
        cur.close()  # Explicitly close the cursor
        conn.commit()  # Commit if no errors
        conn.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()
