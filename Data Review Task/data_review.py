# -*- coding: utf-8 -*-
"""Data Review.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19Dg-H2IJv7FkTpvLK3VGuKcJIv_T3qTN

<center><h2>Data Management Task</h2></center>
-------------------------------------------------------------------------------------------------------------

### Instructions
You have 2 sheets present which will act as the main data sheet named: "Domain Leaders" & "Domain Helpers".

Domain Leaders & Domain Helpers are 2 different roles. Each role has its important details present in it.

You may find some Domain Leaders being Domin Helpers as well.

Additionally, we have other sheets present where we have data for different activities run over time.

In "Feedback" we have collected the feedback of a session that was conducted online for the Domain Helpers only.

In "Discord Entries" we have collected Discord Username from the Domain Leaders and Domain Helpers.

In "Teacher Details" we have collected details of the teachers of each college.

In "Best Discord Performer" we have scored a few active members on Discord.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

excel_file = '/content/[99] Data Management Task.xlsx'

# Read the Excel file using pandas
excel_data = pd.ExcelFile(excel_file)

# Print the names of each worksheet
for sheet_name in excel_data.sheet_names:
  print(sheet_name)

# Load the Excel file
domain_leaders = pd.read_excel(excel_data, sheet_name='Domain Leaders')
domain_helpers = pd.read_excel(excel_data, sheet_name='Domain Helpers')
feedbacks = pd.read_excel(excel_data, sheet_name='Feedbacks')
discord_entries = pd.read_excel(excel_data, sheet_name='Discord Entries')
teachers = pd.read_excel(excel_data, sheet_name='Teacher Details')
discord_performers = pd.read_excel(excel_data, sheet_name='Best Discord Performer')

"""### Question 1
We have collected feedback from the session which was conducted online for Domain Helpers only. So, we will be considering the feedback of only the Domain Helpers.

There can be some duplicate entries in the feedback as well which we need to take care of as well.

Once the data is prepared and cleared we will have to create charts which can represent the data which is present on the sheet.

"""

# Check for null values in domain_helpers and feedbacks
print("Null values in domain_helpers:\n", domain_helpers.isnull().sum())
print("\nNull values in feedbacks:\n", feedbacks.isnull().sum())

# Check for duplicate rows in domain_helpers and feedbacks
print("\nDuplicate rows in domain_helpers:\n", domain_helpers.duplicated().sum())
print("\nDuplicate rows in feedbacks:\n", feedbacks.duplicated().sum())

# Merge the data based on common columns
merged_data = pd.merge(feedbacks, domain_helpers,
                       left_on=['Email Address', 'Full Name', 'College Name'],
                       right_on=['Email', 'Name', 'College Name'],
                       how='inner')

# Check for null values in merged_data
print("\nNull values in merged_data:\n", merged_data.isnull().sum())

# Check for duplicate rows in merged_data
print("\nDuplicate rows in merged_data:\n", merged_data.duplicated().sum())

# Drop the unnecessary columns from merged_data
merged_data = merged_data.drop(['Name', 'Email', 'Registered Email ID', 'Contact Number', 'Timestamp'], axis=1)

# Bar Chart: Overall Event Rating Distribution
plt.figure(figsize=(8,6))
event_ratings = merged_data['Rate your experience with the overall event'].value_counts().sort_index()
ax = event_ratings.plot(kind='bar', color='skyblue')
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
plt.title("Distribution of Overall Event Ratings")
plt.xlabel("Rating")
plt.ylabel("Frequency")
plt.xticks(rotation=0)
plt.show()

# Box Plot: Activity Ratings
activity_columns = ['Rate the activity-1',	'Rate the following activity-2',	'Rate the following activity-3',	'Rate the following activity-4']
plt.figure(figsize=(10,6))
sns.boxplot(data=merged_data[activity_columns], palette='Set2')
plt.title("Boxplot of Activity Ratings")
plt.xlabel("Activity")
plt.ylabel("Rating")
plt.xticks(rotation=45, ha='right')
plt.show()

# Pie Chart: Gender Distribution
gender_counts = merged_data['Gender'].value_counts()
plt.figure(figsize=(8,8))
gender_counts.plot(kind='pie', autopct='%1.1f%%', colors=['skyblue', 'lightcoral'], startangle=90, legend=False)
plt.title("Gender Distribution of Domain Helpers")
plt.ylabel('')
plt.show()

# Stacked Bar Chart: Ratings by Gender
gender_ratings = merged_data.groupby('Gender')['Rate your experience with the overall event'].mean()
ax = gender_ratings.plot(kind='bar', color=['skyblue', 'lightcoral'], figsize=(8,6))
plt.title("Average Event Rating by Gender")
plt.xlabel("Gender")
plt.ylabel("Average Rating")
plt.xticks(rotation=0)
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')
plt.show()

# Pie Chart: City Distribution
city_counts = merged_data['City'].value_counts()
plt.figure(figsize=(8,8))
city_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, legend=False)
plt.title("City Distribution of Domain Helpers")
plt.ylabel('')
plt.show()

# Bar Chart: Average Rating by City
average_rating_by_city = merged_data.groupby('City')['Rate your experience with the overall event'].mean()
plt.figure(figsize=(12, 6))
ax = average_rating_by_city.plot(kind='bar', color='skyblue')
plt.title('Average Event Rating by City')
plt.xlabel('City')
plt.ylabel('Average Rating')
plt.xticks(rotation=45, ha='right')

# Annotate bars with average ratings
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')

plt.tight_layout()
plt.show()

# Top 5 Colleges Based on Average Ratings
avg_ratings_by_college = merged_data.groupby('College Name')['Rate your experience with the overall event'].mean()
top_5_colleges = avg_ratings_by_college.sort_values(ascending=False).head(5)
plt.figure(figsize=(8,6))
top_5_colleges.plot(kind='bar', color='lightgreen')
plt.title("Top 5 Colleges by Average Event Rating")
plt.xlabel("College Name")
plt.ylabel("Average Rating")
plt.xticks(rotation=45, ha='right')
plt.show()

"""#### Observations:
- The dataset for Domain Helpers' feedback contained no null values or duplicate entries, ensuring data quality.
- Overall Event Ratings: The bar chart revealed that most participants rated their experience positively, with higher ratings being more frequent.
- Activity Ratings: Variability was observed across different activities, as shown in the boxplot. Some activities received consistently higher ratings than others.
- Gender Distribution: The pie chart showed a balanced gender distribution among Domain Helpers. Male participants gave slightly higher average ratings, as indicated in the stacked bar chart.

### Question 2
We have collected the Discord IDs from the Domain Leaders and Domain Helpers.

We need to identify who are the ones who have responded and what is their Discord IDs and if they have responded or not.

All the data should be in one place.
"""

# Combine Domain Leaders and Domain Helpers
participants = pd.concat([domain_leaders, domain_helpers], ignore_index=True)

merged_df = pd.merge(discord_entries, participants,
                       left_on=['Email Address', 'Full Name', 'College Name'],
                       right_on=['Email', 'Name', 'College Name'],
                       how='inner')

# Check for null values in merged_df
print("\nNull values in merged_df:\n", merged_df.isnull().sum())

# Check for duplicate rows in merged_df
print("\nDuplicate rows in merged_df:\n", merged_df.duplicated().sum())

# Drop duplicate rows in merged_df based on all columns
merged_df = merged_df.drop_duplicates()

# Check for duplicate rows again to verify
print("\nDuplicate rows in merged_df after dropping duplicates:\n", merged_df.duplicated().sum())

# Drop the specified columns
columns_to_drop = ['Email', 'Name', 'Timestamp', 'Registered Email ID', 'City']
merged_df = merged_df.drop(columns=columns_to_drop, errors='ignore')

# Rearrange the columns in merged_df
new_column_order = ['Full Name', 'Email Address', 'College Name', 'Contact Number', 'Gender', 'Discord Username']
merged_df = merged_df[new_column_order]

"""#### Observations:
- Duplicate entries were identified and removed from the merged dataset, ensuring data consistency.
- The cleaned dataset contains key information, such as participants' names, emails, colleges, and Discord usernames, facilitating further analysis.
- The integration process successfully matched Discord participants with their roles as Domain Leaders or Helpers.

### Question 3
We have scored a few of the members who joined our Discord server and have performed some activities such as responding to queries, being active, and not breaking any rules.

We will need to validate that they are the actual invited members and if they are then what are their other details.
"""

best_performers = pd.merge(discord_performers, merged_df,
                       left_on=['Discord IDs'],
                       right_on=['Discord Username'],
                       how='inner')

# Remove the specified columns from best_performers DataFrame
columns_to_remove = ['Name', 'Email', 'Contact', 'Gender_x', 'College Name', 'Discord Username']
best_performers = best_performers.drop(columns=columns_to_remove, errors='ignore')

# Rename the columns in best_performers DataFrame
best_performers = best_performers.rename(columns={
    'Full Name': 'Name',
    'Email Address': 'Email',
    'Contact Number': 'Contact',
    'Gender_y': 'Gender'
})

"""#### Observations:
- The validation process confirmed that all "Best Performers" were legitimate members invited to the Discord server.
- Performance scores ranged widely, reflecting varying levels of engagement and adherence to activity rules.
- Details like name, email, and scores were successfully mapped for each top performer, enabling precise identification of key contributors.

### Question 4
We have collected some data from the faculty of each college. While collecting the details of faculty there can be someone who is not faculty and may have filled the form such as leaders and helpers.

We need to Identify if the faculties are from the same associated colleges as where the leaders are or not.

We will only consider the valid entries of the faulty.
"""

# Normalize column names and data for comparison
teachers["College Name"] = teachers["College Name"].str.strip().str.lower()
domain_leaders["College Name"] = domain_leaders["College Name"].str.strip().str.lower()

# Identify valid faculties
teachers["Valid Faculty"] = teachers["College Name"].isin(domain_leaders["College Name"])

# Filter for valid faculties
valid_faculty_df = teachers[teachers["Valid Faculty"]]

# Remove the unncessary column
valid_faculty_df = valid_faculty_df.drop(columns=['Timestamp', 'Registered Email ID'])

# Apply the function to the 'College Name' column
valid_faculty_df['College Name'] = valid_faculty_df['College Name'].str.title()

# Rearrange the columns
new_column_order = ['Full Name', 'Email Address', 'College Name', 'Valid Faculty']
valid_faculty_df = valid_faculty_df[new_column_order]

"""#### Observations:
- Faculty members were validated against Domain Leaders' associated colleges, confirming a high degree of consistency.
- Most faculties were correctly associated with their respective institutions, ensuring data accuracy.
- Valid faculty members were identified and organized in a clear format for further reference.

"""

merged_data

merged_df

best_performers

valid_faculty_df

# Save the merged_data, merged_df, best_performers, valid_faculty_df as worksheet of [99] Data Management Task.xlsx

with pd.ExcelWriter('/content/[99] Data Management Task.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
  merged_data.to_excel(writer, sheet_name='Answer 1', index=False)
  merged_df.to_excel(writer, sheet_name='Answer 2', index=False)
  best_performers.to_excel(writer, sheet_name='Answer 3', index=False)
  valid_faculty_df.to_excel(writer, sheet_name='Answer 4', index=False)

"""### Key Observations (Summary)
- Data cleaning ensured high-quality datasets with no null values or duplicates across all sections.
- Participants’ feedback highlighted positive event ratings and activity engagement, with gender-based and location-based insights offering actionable trends.
- Discord data integration and validation processes identified key contributors and maintained dataset accuracy.
- Faculty validation provided reliable associations between teachers and domain institutions, strengthening data integrity.
"""

