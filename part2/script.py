from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt


# Load sensitive info from environment variables
load_dotenv()
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')

# Create a connection to the PostgreSQL database
try:
    engine = create_engine(f'postgresql://{db_user}:{db_password}@localhost:5432/{db_name}')
except Exception as e:
    print("Could not connect to the database.")
    exit(1)

# Import the SQL long query from the sql file
with open('query.sql', 'r') as f:
    query = f.read()

# Load the sql query results into pandas dataframe
df = pd.read_sql(query, con=engine)

# Make sure the 'cohort_month' column is in date format not object format
df['cohort_month'] = pd.to_datetime(df['cohort_month'])

# Use 'cohort_month' as the index, so it will be the x-axis in the plot
df.set_index('cohort_month', inplace=True)

# Plot the retention rates columns for each cohort month as lines with dots
retention_cols = [col for col in df.columns]
df[retention_cols].plot(marker='o')

plt.title('Weekly Retention Rate by Cohort Month')
plt.ylabel('Retention Rate (%)')
plt.xlabel('Cohort Month')
plt.show()