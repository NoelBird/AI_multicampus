import pandas as pd
df = pd.read_csv("CSV/01_data.csv")
df_Name = df['Name']
df_Name_Country = df[['Name', 'Country']]

df_row_0 = df.loc[0]  # series
# print(df_row_0)
df_row_0_3 = df.loc[[0, 3]]  # data frame
# print(df_row_0_3)

df_row_2to5 = df.loc[2:5]

df_col_0 = df.iloc[:, 0]

df_Con_group = df.groupby('Country')
df_Con_group
df_Con_group['Age'].mean()