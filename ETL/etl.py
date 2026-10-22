import pandas as pd
from hdfs import InsecureClient
from io import BytesIO

client = InsecureClient(
    'http://SANDBOX_IP:50070',
    user='maria_dev'
)

hdfs_file_path = '/user/maria_dev/datasets/penguins.csv'
with client.read(hdfs_file_path) as reader:
    df = pd.read_csv(BytesIO(reader.read()))

df.head()
print("Dataset shape:", df.shape)
print("Total rows:", df.shape[0])
print("Total columns:", df.shape[1])
print(df.columns.tolist())
df.info()
df.describe(include='all')

print("Missing values in each column:")
print(df.isnull().sum())
print("Total missing values:", df.isnull().sum().sum())

missing_percentage = (df.isnull().sum() / len(df)) * 100

print(missing_percentage.round(2))

cleaned_df = df.copy()
cleaned_df = cleaned_df.dropna(axis=1, how='all')

print("Empty columns removed.")
print("Shape after removing empty columns:", cleaned_df.shape)

numeric_cols = cleaned_df.select_dtypes(
    include='number'
).columns

#handle Numerical Missing Values
for col in numeric_cols:
    cleaned_df[col] = cleaned_df[col].fillna(
        cleaned_df[col].median()
    )

print("Numerical missing values handled.")

#Handle Categorical Missing Values
categorical_cols = cleaned_df.select_dtypes(
    include=['object', 'category', 'string']
).columns

for col in categorical_cols:
    if cleaned_df[col].isnull().any():
        mode_values = cleaned_df[col].mode(dropna=True)

        if not mode_values.empty:
            cleaned_df[col] = cleaned_df[col].fillna(
                mode_values.iloc[0]
            )

print("Categorical missing values handled.")

#convert body mass into kilogram
if 'body_mass_g' in cleaned_df.columns:
    cleaned_df['body_mass_kg'] = (
        cleaned_df['body_mass_g'] / 1000
    )

    cleaned_df.drop(columns=['body_mass_g'], inplace=True)

    print("Body mass converted from grams to kilograms.")
else:
    print("body_mass_g column not found.")
    print("Available columns:", cleaned_df.columns.tolist())

#Varify data after cleaning
print("Missing values after cleaning:")
print(cleaned_df.isnull().sum())

print("\nTotal missing values:")
print(cleaned_df.isnull().sum().sum())

print("\nCleaned dataset shape:", cleaned_df.shape)

cleaned_df.head()

#Create Output Dir
output_dir = '/user/maria_dev/datasets/clean'
output_path = output_dir + '/penguins_clean.csv'

client.makedirs(output_dir)

print("Output directory created:", output_dir)

#upload cleaned dataset
with client.write(
    output_path,
    overwrite=True,
    encoding='utf-8'
) as writer:
    cleaned_df.to_csv(writer, index=False)

print("Cleaned dataset uploaded successfully!")
print("HDFS path:", output_path)

# Verify HDFS upload
if client.status(output_path, strict=False):
    print("SUCCESS: File exists in HDFS.")

    print("File details:")
    print(client.status(output_path))
else:
    print("ERROR: File was not found in HDFS.")

#read CSV from HDFS
with client.read(output_path) as reader:
    verify_df = pd.read_csv(BytesIO(reader.read()))

print("Uploaded file preview:")
display(verify_df.head())

print("Uploaded file shape:", verify_df.shape)
print("Missing values:", verify_df.isnull().sum().sum())

