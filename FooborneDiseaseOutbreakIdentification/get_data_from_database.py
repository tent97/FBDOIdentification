import pymssql
import csv
import pandas as pd
import os
#连接服务器
def conn():
    connect = pymssql.connect('(local)', 'sa', '123456', 'food_borne_disease_2019') #服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    return connect
def get_data_from_database(outbreak_ID,bus_disease_GUID,action):
    #According to the input case list, retrieve the data from the database, and generate the CSV file according to the specific information of the case data
    if action=="predict":
        root="predict_data"
    elif action=="train":
        root="train_data"
    connect=conn()
    cursor=connect.cursor()
    if action=="predict":
        filefullpath="E:\\FooborneDiseaseOutbreakIdentification\\predict_data\\search_result.csv"
    elif action=="train":
        filefullpath="E:\\FooborneDiseaseOutbreakIdentification\\train_data\\search_result.csv"
        
    if os.path.exists(filefullpath):
        os.remove(filefullpath)
    for i in range(len(bus_disease_GUID)):
        sql = " SELECT * FROM BusDiseases "+ \
        "RIGHT JOIN BusSymptoms on BusDiseases.Disease_GUID = BusSymptoms.Disease_GUID "+ \
        "RIGHT JOIN BusExPosures on BusDiseases.Disease_GUID = BusExPosures.Disease_GUID "+ \
        "RIGHT JOIN BusDiagnosis on BusDiseases.Disease_GUID = BusDiagnosis.Disease_GUID "+ \
        "WHERE BusDiseases.Disease_GUID='%s';" %(bus_disease_GUID[i])
        cursor.execute(sql)
        results = cursor.fetchall()
        
        #Write the query results to search_ result.csv
        with open("{root}/search_result.csv".format(root=root),"a+",newline='',encoding='utf-8') as csvfile:
            for row in results:
                writer = csv.writer(csvfile)
                writer.writerow(row)
    
    data=pd.read_csv("{root}/search_result.csv".format(root=root),header=None,dtype=object)
    
    data=data.drop_duplicates(subset=None,keep='first',inplace=False)
    indexs=['Disease_ID', 'Disease_GUID', 'User_GUID', 'Disease_CaseNo', 'Disease_IsReExam', 'Disease_PatientNo', 'Disease_IsPaint', 'Disease_HospitalNo', 'Disease_PatientName', 'Disease_Guardian', 'Disease_IDNumber', 'Disease_Sex', 'Disease_Birthday', 'Disease_AgeName', 'Disease_Age', 'Disease_PatientUnit', 'Disease_Tel', 'Disease_Hometown', 'Disease_Province', 'Disease_City', 'Disease_District', 'Disease_Address', 'Disease_Occupation', 'Disease_SickTime', 'Disease_TreatTime', 'Disease_DeadTime', 'Disease_CreatedTime', 'Disease_LastEditTime', 'Disease_IsFoodborne', 'Disease_FoodborneCount', 'Disease_IsSurvey', 'Disease_SignsName', 'Disease_InitialResult', 'Disease_Medicalhistory', 'Disease_CreateBy', 'Disease_CreateUnitGuid', 'Disease_IsAttchment', 'Disease_Remark', 'Disease_State', 'Disease_Level', 'Disease_SampleCounts', 'Disease_UnitGuid', 'Disease_IsUseAntibiotic', 'Disease_AntibioticName', 'Disease_BackUnitGuid', 'Disease_BackReason', 'Disease_RequestBack', 'Disease_CurUnitGuid', 'Disease_CurState', 'Disease_CurLevel', 'Disease_CurSourceState', 'Disease_CurStateDescription', 'Disease_LastUnitGuid', 'Disease_TestResult', 'Disease_ReturnCount', 'Disease_SubmitDatetime', 'Disease_AuditDatetime', 'Disease_Clinicians', 'Disease_OtherIsill', 'Disease_Source', 'Disease_AddTime', 'Disease_IsUpdate', 'Disease_IsTimely', 'Disease_UpdateContent', 'Virus_TestResult', 'Pathogens_TestResult', 'Disease_Type', 'Symptom_ID', 'Symptom_GUID', 'Disease_GUID', 'Symptom_Name', 'Symptom_Code', 'Symptom_Value', 'Symptom_FCode', 'Symptom_Unit', 'Symptom_Expression', 'ExPosure_ID', 'ExPosure_GUID', 'Disease_GUID', 'ExPosure_Name', 'ExPosure_TypeName', 'ExPosure_TypeCode', 'ExPosure_ProcessingName', 'ExPosure_ProcessingCode', 'ExPosure_Brand', 'ExPosure_Factory', 'ExPosure_EatPlaceTypeName', 'ExPosure_EatPlaceTypeCode', 'ExPosure_BuyPlaceTypeName', 'ExPosure_BuyPlaceTypeCode', 'ExPosure_IsBuyDomestic', 'ExPosure_BuyProvince', 'ExPosure_BuyCity', 'ExPosure_BuyDistrict', 'ExPosure_BuyAddress', 'ExPosure_IsEatDomestic', 'ExPosure_EatProvince', 'ExPosure_EatCity', 'ExPosure_EatDistrict', 'ExPosure_EatAddress', 'ExPosure_EatNum', 'ExPosure_Eattime', 'ExPosure_OtherIsill', 'ExPosure_State', 'ExPosure_IsUpdate', 'ExPosure_UpdateContent', 'Diagnosis_ID', 'Diagnosis_GUID', 'Disease_GUID', 'Diagnosis_Name', 'Diagnosis_Code', 'Diagnosis_Value']
    data.columns=indexs
    data['Incident_GUID'] = [outbreak_ID]*len(data) 
    columns=['Incident_GUID','Disease_ID','Disease_GUID','User_GUID','Disease_Age',
             'Disease_PatientUnit','Disease_Hometown','Disease_Province','Disease_District','Disease_Address','Disease_Occupation',
             'Disease_SickTime','Disease_TreatTime','Disease_IsFoodborne','Disease_FoodborneCount','Disease_OtherIsill',
             'Disease_Type','Symptom_Code','Symptom_FCode','ExPosure_Name','ExPosure_TypeCode','ExPosure_ProcessingCode','ExPosure_EatPlaceTypeCode',
             'ExPosure_BuyPlaceTypeCode','ExPosure_IsBuyDomestic','ExPosure_BuyProvince','ExPosure_BuyCity','ExPosure_BuyDistrict','ExPosure_BuyAddress',
             'ExPosure_IsEatDomestic','ExPosure_EatProvince','ExPosure_EatCity','ExPosure_EatDistrict','ExPosure_EatAddress','ExPosure_EatNum',
             'ExPosure_Eattime','ExPosure_OtherIsill','Diagnosis_Code']  
    data2=data[columns]
    data2.to_csv("{root}/search_result_1.csv".format(root=root),index=False,header=True)
    data3=pd.read_csv("{root}/search_result_1.csv".format(root=root),dtype=object)
    data3=data3.drop(["Disease_GUID.1"],axis=1)
    data3=data3.drop(["Disease_GUID.2"],axis=1)
    data3=data3.drop(["Disease_GUID.3"],axis=1)
    return data3