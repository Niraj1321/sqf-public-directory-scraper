import pymysql
import datetime


current_date=datetime.date.today().strftime("%d%m%Y")



conn = pymysql.connect(
    host="localhost",
    user="root",
    password="aman@123",
    database="sqf_data"
)
cursor = conn.cursor()

organization_name=rf"organizations_data_{current_date}"
certificate_table=rf"certifications_{current_date}"
query1= rf"""
    CREATE TABLE IF NOT EXISTS {organization_name}(
        Organization_ID VARCHAR(100) PRIMARY KEY,
        Organization_Name VARCHAR(255),
        Trading_Name VARCHAR(255),
        Physical_Address_Line_1 VARCHAR(255),
        Physical_Address_Line_2 VARCHAR(255),
        Physical_City VARCHAR(255),
        Physical_State_Name VARCHAR(255),
        Physical_Zip VARCHAR(255),
        Physical_Country_Name VARCHAR(100),
        Business_Type_Name VARCHAR(100)
    );
"""

query2 = rf"""
    CREATE TABLE IF NOT EXISTS {certificate_table}(
        View VARCHAR(255),
        Core_Certification_Type_Name VARCHAR(500),
        Certification_Number VARCHAR(100),
        Condensed_Site_Info TEXT,
        Expiration_Date VARCHAR(20),
        Certification_Status_Column VARCHAR(100),
        CID VARCHAR(100),
        Location_ID VARCHAR(100),
        Qualifications_List TEXT,
        Products TEXT,
        Physical_Address_Line_1 VARCHAR(255),
        Physical_Address_Line_2 VARCHAR(255),
        Physical_State VARCHAR(100),
        Physical_City VARCHAR(100),
        Physical_Zip VARCHAR(200),
        Codes_List TEXT,
        Certification_Issue_Date VARCHAR(20),
        Recertification_Date VARCHAR(20),
        Core_Organization_CB_Organization_Name VARCHAR(255),
        Select_Site VARCHAR(255),
        Audit_Scope TEXT,
        Core_Certification_Type VARCHAR(100),
        Core_Organization_Location VARCHAR(255),
        Parent_Certification VARCHAR(100)
    );
"""

cursor.execute(query1)
cursor.execute(query2)
conn.commit()