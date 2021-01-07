# -*- coding: utf-8 -*-
import pandas as pd
def combine_same_disease_GUID(data):
    #search_ result_ final_ filter.csv In, the same case ID corresponds to multiple data, and the data requiring the same case Id need to be merged
    data=data.astype("str")
    all_data=data.values
    selected_data=[]
    selected_data.append(all_data[0])
    #conbine option
    for i in range(1,len(all_data)):
        if all_data[i][2]==selected_data[-1][2]:
            for j in range(len(all_data[0])):
  
                if all_data[i][j] not in selected_data[-1][j].split("|"):
  
                    selected_data[-1][j]=selected_data[-1][j]+"|"+all_data[i][j]             
        else:
            selected_data.append(all_data[i])  
    #deduplicate funciton
    def deduplication(list1):
        mylist=list(set(list1.split("|")))   
        mylist_filter="|".join(mylist);
        return mylist_filter
    selected_data1=selected_data
    for i in range(len(selected_data)):
        for j in range(len(selected_data[0])):
            selected_data1[i][j]=deduplication(selected_data[i][j])
    #Filter useful data columns based on different operations
    
    columns=['Incident_GUID','Disease_ID','Disease_GUID','User_GUID','Disease_Age','Disease_PatientUnit','Disease_Hometown',
             'Disease_Province','Disease_District','Disease_Address','Disease_Occupation','Disease_SickTime','Disease_TreatTime',
             'Disease_IsFoodborne','Disease_FoodborneCount','Disease_OtherIsill','Disease_Type','Symptom_Code','Symptom_FCode',
             'ExPosure_Name','ExPosure_TypeCode','ExPosure_ProcessingCode','ExPosure_EatPlaceTypeCode','ExPosure_BuyPlaceTypeCode',
             'ExPosure_IsBuyDomestic','ExPosure_BuyProvince','ExPosure_BuyCity','ExPosure_BuyDistrict','ExPosure_BuyAddress',
             'ExPosure_IsEatDomestic','ExPosure_EatProvince','ExPosure_EatCity','ExPosure_EatDistrict','ExPosure_EatAddress',
             'ExPosure_EatNum','ExPosure_Eattime','ExPosure_OtherIsill','Diagnosis_Code']
    
    result=pd.DataFrame(selected_data)
    result1=result[[i for i in range(0,38)]]
    
    
    result1.columns = columns
    result2=pd.DataFrame(selected_data1)
    result3=result2[[i for i in range(0,38)]]
    
    result3.columns = columns
    #Save the merged data according to the Case ID to search_ result_ conbined_ final_ 1.csv
    
    #Fill in the vacancy value and deal with the abnormal data
    result3['Disease_PatientUnit']=result3['Disease_PatientUnit'].fillna('未填写')
    result3['ExPosure_IsBuyDomestic']=result3['ExPosure_IsBuyDomestic'].fillna('1')
    result3['ExPosure_BuyProvince']=result3['ExPosure_BuyProvince'].fillna('0')
    result3['ExPosure_BuyCity']=result3['ExPosure_BuyCity'].fillna('0')
    result3['ExPosure_BuyDistrict']=result3['ExPosure_BuyDistrict'].fillna('0')
    result3['ExPosure_EatProvince']=result3['ExPosure_EatProvince'].fillna('0')
    result3['ExPosure_EatCity']=result3['ExPosure_EatCity'].fillna('0')
    result3['ExPosure_EatDistrict']=result3['ExPosure_EatDistrict'].fillna('0')
    def deduplication1(list1):
        mylist=list(set(list1.split("|"))) 
        your_list = [x for x in mylist if x != '']
        mylist_filter=your_list[0]
        return mylist_filter
    ExPosure_IsBuyDomestic_list=result3['ExPosure_IsBuyDomestic'].astype(str).tolist()
    ExPosure_BuyProvince_list=result3['ExPosure_BuyProvince'].astype(str).tolist()
    ExPosure_BuyCity_list=result3['ExPosure_BuyCity'].astype(str).tolist()
    ExPosure_BuyDistrict_list=result3['ExPosure_BuyDistrict'].astype(str).tolist()
    ExPosure_EatProvince_list=result3['ExPosure_EatProvince'].astype(str).tolist()
    ExPosure_EatCity_list=result3['ExPosure_EatCity'].astype(str).tolist()
    ExPosure_EatDistrict_list=result3['ExPosure_EatDistrict'].astype(str).tolist()
    ExPosure_Eattime_list=result3['ExPosure_Eattime'].astype(str).tolist()
    for i in range(len(ExPosure_IsBuyDomestic_list)):
        filtered_list=deduplication1(ExPosure_IsBuyDomestic_list[i])
        ExPosure_IsBuyDomestic_list[i]=filtered_list  
    for i in range(len(ExPosure_BuyProvince_list)):
        filtered_list=deduplication1(ExPosure_BuyProvince_list[i])
        ExPosure_BuyProvince_list[i]=filtered_list
        
    for i in range(len(ExPosure_BuyCity_list)):
        filtered_list=deduplication1(ExPosure_BuyCity_list[i])
        ExPosure_BuyCity_list[i]=filtered_list
        
    for i in range(len(ExPosure_BuyDistrict_list)):
        filtered_list=deduplication1(ExPosure_BuyDistrict_list[i])
        ExPosure_BuyDistrict_list[i]=filtered_list
        
    for i in range(len(ExPosure_EatProvince_list)):
        filtered_list=deduplication1(ExPosure_EatProvince_list[i])
        ExPosure_EatProvince_list[i]=filtered_list
        
    for i in range(len(ExPosure_EatCity_list)):
        filtered_list=deduplication1(ExPosure_EatCity_list[i])
        ExPosure_EatCity_list[i]=filtered_list
        
    for i in range(len(ExPosure_EatDistrict_list)):
        filtered_list=deduplication1(ExPosure_EatDistrict_list[i])
        ExPosure_EatDistrict_list[i]=filtered_list
    
    for i in range(len(ExPosure_Eattime_list)):
        filtered_list=deduplication1(ExPosure_Eattime_list[i])
        ExPosure_Eattime_list[i]=filtered_list
    result3['ExPosure_IsBuyDomestic']=ExPosure_IsBuyDomestic_list
    result3['ExPosure_BuyProvince']=ExPosure_BuyProvince_list
    result3['ExPosure_BuyCity']=ExPosure_BuyCity_list
    result3['ExPosure_BuyDistrict']=ExPosure_BuyDistrict_list
    result3['ExPosure_EatProvince']=ExPosure_EatProvince_list
    result3['ExPosure_EatCity']=ExPosure_EatCity_list
    result3['ExPosure_EatDistrict']=ExPosure_EatDistrict_list
    result3['ExPosure_Eattime']=ExPosure_Eattime_list
    return result3



    
    
    






















