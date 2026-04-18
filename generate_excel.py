import pymysql
import pandas as pd
import db_config as db


# Query the table
query1 = rf"SELECT * FROM {db.organization_name}"
query2 = rf"SELECT * FROM {db.certificate_table}"

# Use pandas to read SQL into a DataFrame
df1 = pd.read_sql(query1, db.conn)
df2 = pd.read_sql(query2, db.conn)

db.conn.close()

df2 = df2.drop_duplicates()
df2 = df2.drop(columns=["View", "CID", "Select_Site", "Core_Certification_Type", "Core_Organization_Location", "Parent_Certification"])
df2 = df2.rename(columns={
    "Core_Certification_Type_Name":"Audit Name",
    "Certification_Status_Column":"Certification_Status",
    "Physical_Address_Line_1":"Address_Line_1",
    "Physical_Address_Line_2":"Address_Line_2",
    "Physical_State":"State",
    "Physical_City":"City",
    "Physical_Zip":"Zip",
    "Core_Organization_CB_Organization_Name":"CB_Organization_Name"
})

# Export to Excel
df1.to_excel(rf"SQF_{db.organization_name}.xlsx", index=False)
df2.to_excel(rf"SQF_{db.certificate_table}.xlsx", index=False)

print("Excel file generated successfully!")
