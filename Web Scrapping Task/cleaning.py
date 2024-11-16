import pandas as pd

# 'companies.csv' is in the current working directory or you provide the correct path
df = pd.read_csv('F:/companies.csv')

# Print the shape of the DataFrame (rows, columns)
print("Shape of the data before cleaning:", df.shape)

num_duplicates = df.duplicated().sum()

# Calculate the number of missing values in each column
missing_values_per_column = df.isnull().sum()

# Calculate the total number of missing values
total_missing_values = missing_values_per_column.sum()

print("\nChecking missing and duplicate values before cleaning")
print(f"Total number of duplicate rows: {num_duplicates}")
print("\nMissing values per column:")
print(missing_values_per_column)
print(f"\nTotal number of missing values: {total_missing_values}")

# Remove duplicate rows, modifying the DataFrame in place
df.drop_duplicates(inplace=True)

# Remove rows with missing values
df.dropna(inplace=True)

num_duplicates = df.duplicated().sum()

# Calculate the number of missing values in each column
missing_values_per_column = df.isnull().sum()

# Calculate the total number of missing values
total_missing_values = missing_values_per_column.sum()

print("\nChecking missing and duplicate values after cleaning")
print(f"Total number of duplicate rows: {num_duplicates}")
print("\nMissing values per column:")
print(missing_values_per_column)
print(f"\nTotal number of missing values: {total_missing_values}")

print("\nShape of the data after cleaning:", df.shape)

# Save the cleaned DataFrame to a CSV file
df.to_csv('F:/cleaned_company_data.csv', index=False)

print("\nCleaned data saved to 'cleaned_company_data.csv'")

