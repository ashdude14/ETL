import psycopg
from dotenv import load_dotenv # install
import os

load_dotenv()

def connect_to_db():
    try:
        database_url = os.getenv("DB_URL")
        if not database_url:
            raise ValueError("DATABASE_URL is not set in the environment.")
        
        conn = psycopg.connect(database_url)
        print("Connection established!")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


def execute_query(cursor, query, fetch_results=True):
    try:
        cursor.execute(query)  
        if fetch_results:
            return cursor.fetchall()  
        return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

def insert_jobs(cursor, jobs):
    """Insert job data into the database."""
    try:
        # Define the INSERT query
        insert_query = """
        INSERT INTO data_analyst_job.jobs 
        (Job_Id, Title, Company_Name, Experience, Salary, Locations, Job_Date, Descriptions, Skills)
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        # Execute the insert queries
        cursor.executemany(insert_query, jobs)
        print("Jobs inserted successfully.")
    except Exception as e:
        print(f"Error inserting jobs: {e}")

    except Exception as e:
        print(f"Error inserting jobs: {e}")
        cursor.connection.rollback()  # Rollback in case of error
        return False
    return True


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

        jobs = [
            ("DAVE0001", "Data Verification Analyst", "Foundation Ai", "0-5 Yrs", "Not disclosed", 
             "Kolkata, Mumbai, New Delhi, Hyderabad, Pune, Chennai, Bengaluru", "1 Day Ago", 
             "Foundation AI is looking for Data Verification Analyst to join our dynamic team and emb...", 
             "metadatapythondata analysisdata managementdata analyticsdata validationconfigurationdata mining"),
                         
            ("TEME0007", "Team Member Data Analyst", "Bajaj Allianz General Insurance", "0-4 Yrs", "Not disclosed", 
             "Pune", "13 Days Ago", 
             "Comprehend customize report requirement by stakeholders (NHOD, zonal heads, vertical he...", 
             "AutomationData validationProcess efficiencyActuarialData qualityData analyticsData AnalystManager Quality Control") ]

        # Insert the job data
        insert_jobs(cur, jobs)

        # Show the table content
        cur.execute("SELECT * FROM data_analyst_job.jobs;")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()  # Rollback any changes if an error occurs
    finally:
        conn.commit()  # Commit if no errors
        conn.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
import psycopg
from dotenv import load_dotenv  # Install python-dotenv using `pip install python-dotenv`
import os

# Load environment variables from .env file
load_dotenv()

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


def execute_query(cursor, query, fetch_results=True):
    try:
        cursor.execute(query)  # Execute the query
        if fetch_results:
            return cursor.fetchall()  # Fetch all results if required
        return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None


def insert_jobs(cursor, jobs):
    """Insert job data into the database."""
    try:
        # Define the INSERT query
        insert_query = """
        INSERT INTO data_analyst_job.jobs 
        (Job_Id, Title, Company_Name, Experience, Salary, Locations, Job_Date, Descriptions, Skills)
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        # Log the job data for debugging
        print("Inserting jobs:", jobs)
        
        # Execute the insert queries
        cursor.executemany(insert_query, jobs)
        print("Jobs inserted successfully.")
    except Exception as e:
        print(f"Error inserting jobs: {e}")
        cursor.connection.rollback()  # Rollback in case of error
        return False
    return True


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

        # List of jobs to insert
        jobs = [
            ("DAVE0001", "Data Verification Analyst", "Foundation Ai", "0-5 Yrs", "Not disclosed", 
             "Kolkata, Mumbai, New Delhi, Hyderabad, Pune, Chennai, Bengaluru", "1 Day Ago", 
             "Foundation AI is looking for Data Verification Analyst to join our dynamic team and emb...", 
             "metadatapythondata analysisdata managementdata analyticsdata validationconfigurationdata mining"),
             
            ("TEME0007", "Team Member Data Analyst", "Bajaj Allianz General Insurance", "0-4 Yrs", "Not disclosed", 
             "Pune", "13 Days Ago", 
             "Comprehend customize report requirement by stakeholders (NHOD, zonal heads, vertical he...", 
             "AutomationData validationProcess efficiencyActuarialData qualityData analyticsData AnalystManager Quality Control")
        ]

        # Insert the job data
        insert_jobs(cur, jobs)

        # Show the table content
        cur.execute("SELECT * FROM data_analyst_job.jobs;")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()  # Rollback any changes if an error occurs
    finally:
        conn.commit()  # Commit if no errors
        conn.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
