from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta



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



# -------------------------- FIRST APPROACH USING SQL QUERY AND LINE GRAPH VISUALIZATION -----------------------------

# Import the SQL long query from the sql file
with open('cohort_analysis.sql', 'r') as f:
    query = f.read()

# Load the sql query results into pandas dataframe
result = pd.read_sql(query, con=engine)

# Make sure the 'cohort_month' column is in date format not object format
result['Cohort Month'] = pd.to_datetime(result['Cohort Month'])

# Use 'cohort_month' as the index, so it will be the x-axis in the plot
result.set_index('Cohort Month', inplace=True)

# VISUALIZATION : Uncomment from line 42 to 46 and comment from line 152 to 155 to get the 'Line Graph' visualization
# result.plot(marker='o')
# plt.title('Weekly Retention Rate by Cohort Month')
# plt.ylabel('Retention Rate (%)')
# plt.xlabel('Cohort Month')
# plt.show()



# -------------------------- SECOND APPROACH USING PANDAS AND HEATMAP VISUALIZATION -----------------------------

# Load the users and events data from the database
users = pd.read_sql("""SELECT * FROM users""", con=engine)
events = pd.read_sql("""SELECT * FROM events""", con=engine)

# Convert 'signup_date' from object to datetime and create 'signup_month' column
users['signup_date'] = pd.to_datetime(users['signup_date'])
users['signup_month'] = users['signup_date'].dt.to_period('M').dt.to_timestamp()


# user_events dataframe: Join users and events, and flag if a user was active in each of the first 8 weeks after signup
filtered_users = users[users['signup_date'] < '2025-11-06'] # Only include users who signed up at least 8 weeks before the dataset end date, so all cohorts have 8 weeks of possible activity
user_events = pd.merge(filtered_users, events, how='left', on='user_id')

# Function to determine if a user was active in a specific week after signup
def is_active(row, week_number):
    
    if row['timestamp'] >= row['signup_date'] + timedelta(weeks = week_number - 1) and row['timestamp'] < row['signup_date'] + timedelta(weeks = week_number):
        return 1
    else:
        return 0

user_events['is_week1_active'] = user_events.apply(is_active, axis=1, args=(1,))
user_events['is_week2_active'] = user_events.apply(is_active, axis=1, args=(2,))
user_events['is_week3_active'] = user_events.apply(is_active, axis=1, args=(3,))
user_events['is_week4_active'] = user_events.apply(is_active, axis=1, args=(4,))
user_events['is_week5_active'] = user_events.apply(is_active, axis=1, args=(5,))
user_events['is_week6_active'] = user_events.apply(is_active, axis=1, args=(6,))
user_events['is_week7_active'] = user_events.apply(is_active, axis=1, args=(7,))
user_events['is_week8_active'] = user_events.apply(is_active, axis=1, args=(8,))


# user_events_weekly dataframe: Group by user_id and signup_month, and get the max value for each week active flag
user_events_weekly = user_events.groupby(['user_id', 'signup_month']) \
    [['is_week1_active', 'is_week2_active', 'is_week3_active', 'is_week4_active', \
    'is_week5_active', 'is_week6_active', 'is_week7_active', 'is_week8_active']] \
    .max().reset_index()


# user_events_cohort dataframe: Group by signup_month and sum the active flags for each week
user_events_cohort = user_events_weekly.groupby('signup_month') \
    [['is_week1_active', 'is_week2_active', 'is_week3_active', 'is_week4_active', \
    'is_week5_active', 'is_week6_active', 'is_week7_active', 'is_week8_active']] \
    .sum()

user_events_cohort = user_events_weekly.groupby('signup_month') \
    [['is_week1_active', 'is_week2_active', 'is_week3_active', 'is_week4_active', \
    'is_week5_active', 'is_week6_active', 'is_week7_active', 'is_week8_active']] \
    .sum().reset_index() \
    .rename(columns = {
        'signup_month': 'cohort_month',
        'is_week1_active': 'week1_active_users',
        'is_week2_active': 'week2_active_users',
        'is_week3_active': 'week3_active_users',
        'is_week4_active': 'week4_active_users',
        'is_week5_active': 'week5_active_users',
        'is_week6_active': 'week6_active_users',
        'is_week7_active': 'week7_active_users',
        'is_week8_active': 'week8_active_users',
    })


# cohorts dataframe: Calculate the total number of users in each cohort month
cohorts = users.groupby('signup_month')['user_id'].nunique().reset_index().rename(columns={'signup_month': 'cohort_month', 'user_id': 'total_users_count'})


# Final result 
result = pd.merge(user_events_cohort, cohorts, on='cohort_month')

# Function to calculate the retention rate for each week
def calculate_retention_rate(row, column):
    return round( row[column] / row['total_users_count'] * 100, 2 )


result['week1_active_users'] = result.apply(calculate_retention_rate, axis=1, args=('week1_active_users',))
result['week2_active_users'] = result.apply(calculate_retention_rate, axis=1, args=('week2_active_users',))
result['week3_active_users'] = result.apply(calculate_retention_rate, axis=1, args=('week3_active_users',))
result['week4_active_users'] = result.apply(calculate_retention_rate, axis=1, args=('week4_active_users',))
result['week5_active_users'] = result.apply(calculate_retention_rate, axis=1, args=('week5_active_users',))
result['week6_active_users'] = result.apply(calculate_retention_rate, axis=1, args=('week6_active_users',))
result['week7_active_users'] = result.apply(calculate_retention_rate, axis=1, args=('week7_active_users',))
result['week8_active_users'] = result.apply(calculate_retention_rate, axis=1, args=('week8_active_users',))

result.rename(columns= {
    'cohort_month': 'Cohort month',
    'week1_active_users': 'Week1',
    'week2_active_users': 'Week2',
    'week3_active_users': 'Week3',
    'week4_active_users': 'Week4',
    'week5_active_users': 'Week5',
    'week6_active_users': 'Week6',
    'week7_active_users': 'Week7',
    'week8_active_users': 'Week8'
}, inplace=True)

result = result[[col for col in result.columns if col != 'total_users_count']]

# Convert 'Cohort month' to date and set it as index
result['Cohort month'] = result['Cohort month'].dt.date
result.set_index('Cohort month', inplace=True)

# VISUALIZATION : Uncomment lines below and comment from line 42 to 46 to get the 'Heatmap' visualization
# sns.heatmap(result, annot=True, fmt='.2f', cmap='coolwarm', cbar_kws={'label': 'Retention rates (%)'})
# plt.title('Weekly Retention Rate by Cohort Month')
# plt.show()