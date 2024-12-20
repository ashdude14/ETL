#  Automated Data Extraction, Transformation, and Loading (ETL) Pipeline with Airflow and Selenium

## Objective: Airflow is employed to run Python scripts that automate the web scraping, data transformation, and loading tasks.

- To ensure a consistent execution environment, the entire solution is containerized using Docker. Docker allows the encapsulation of all      dependencies, including the necessary libraries, the Selenium web driver, and a compatible web browser (e.g., Chrome), ensuring the system runs seamlessly across different environments. This containerized approach minimizes the risk of dependency conflicts and simplifies deployment and scaling.

- The data processing pipeline also includes a crucial deduplication step, ensuring that duplicate records are not inserted into the data warehouse, maintaining data quality. The extracted data is transformed into a structured format (such as JSON, CSV, or DataFrame) that aligns with the target data warehouse schema.

- Additionally, the project is managed using Jira, which helps in tracking progress, assigning tasks, and collaborating with other developers. This project structure ensures a scalable, maintainable, and efficient ETL pipeline with minimal manual intervention, making it suitable for automating data extraction and loading from websites on a regular basis. By leveraging Docker and Apache Airflow, this solution provides flexibility and scalability for future enhancements and integration with other data sources.


![diagram](./asset/basic.png)


## Key Components:

### 1. Data Extraction:
 **Selenium Web Scraping** :
 
- <b>Detailed Implementation </b> : [see here!]("https://www.github.com/ashdude14/DA4)

- As described in the attached github repo to gather through web scraping there are mendatory steps to follow -
   
   - Download web driver for respective brower.
   - Setting up the Path for the web driver executable application and target website Url in my case it is <i>naukri.com</i>. 
   - Run the code and ensure that it should automate withouth <i>headless</i> mode.
- Here we need to customize all the steps inside the container which will increase memory overhead and execution time, also the process should only run without <i>headless option it will be somewhat complicated because to work with GUI inside the Docker container, we need to mention the ```display server``` with ```x11``` service of ```Xvfb``` library of Dockerfile. </i> To optimize this Automation of website, we are using the image which is available as ```selenium/standalone-chrome``` in <i> DockerHub<i> and this reduces the overall size of container and increases speed of execution.


### 2. Data Deduplication:
- **Manual Deduplication**: Before loading the extracted data into the data warehouse, deduplication will be performed to avoid inserting duplicate records. This ensures data quality and prevents redundancy.

### 3. Data Transformation:
- **Data Structuring**: The extracted data will be transformed into a structured format (e.g., JSON, CSV, or DataFrame) that aligns with the target data warehouse schema.

### 4. Data Loading:
- **Database Interaction**: The structured data will be loaded into a SQL-based data warehouse, such as SQL Server or a free-tier SQL database. SQL queries will be used for the insertion of data into the database.

### 5. Airflow Orchestration:
- **DAG Creation**: A Directed Acyclic Graph (DAG) will be created within Apache Airflow to schedule and automate the ETL pipeline. The DAG will be configured to run weekly and trigger the Python script that performs the data extraction, transformation, and loading.
- **PythonOperator**: The PythonOperator in Airflow will be used to execute the Python script that automates the website interaction and data processing.

### 6. Containerization:
- **Dockerization**: To ensure a consistent and isolated execution environment, Docker will be used to containerize the entire solution. This includes packaging the necessary libraries, the Selenium web driver, and other dependencies within the Docker container.
    - Why Docker??
    
     ![docker](./asset/docker.jpg)

- **Web Browser and Web Driver**: The Docker container will also include a compatible web browser (e.g., Chrome) and its corresponding web driver, ensuring compatibility with Selenium.

### 7. Project Management:
- **Jira**: Jira will be used as a project management tool to track progress, assign tasks, and collaborate with other developers on the project. This ensures that the development process remains organized and transparent.


## Architecture:

![architecture](./asset/architecture-components.png)

## Technical Stack:
- **Python** for scripting and automation
- **Selenium** for web scraping
- **Apache Airflow** for orchestration and scheduling
- **Docker** for containerization
- **SQL Server/Postgres** for the data warehouse
- **Jira** for project management and team collaboration

## Workflow:
1. **Data Extraction**: The data is scraped from the website using Selenium.
2. **Data Deduplication**: The extracted data is deduplicated to remove any redundancy.
3. **Data Transformation**: The data is transformed into a structured format suitable for database storage.
4. **Data Loading**: The transformed data is inserted into the data warehouse.
5. **Airflow Scheduling**: The ETL process is scheduled and automated using Airflow to run weekly.
6. **Containerization**: The entire process is containerized using Docker, with all dependencies and tools bundled in a single image.

## Deliverables:
- A fully functional ETL pipeline with automated web scraping.
- Docker container with all dependencies and web drivers.
- A scheduled Airflow DAG for automation.
- A project management plan with tasks tracked via Jira.

