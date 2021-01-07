import pandas as pd 
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from itertools import combinations
import time
from fuzzywuzzy import fuzz

#Extraction function of various features

#Action means to load data from different directories according to different operations and save the data in different directories,
def symptom_feature_extraction(data3):
       
    corpus=['23001001','23001002','23001003','23001004','23001005','23001006','23001007','23001008','23001009','23001010','23001011','23001012','23001013','23001014','23001015','23001016','23001017','23001018','23001019','23001020','23001022','23001023','23002001','23002002','23002003','23002004','23002005','23002006','23002007','23003001','23003002','23003003','23003004','23004001','23004002','23004003','23004004','23004005','23005001','23005002','23005003','23005004','23005005','23006001','23006002','23006003','23006004','23006005','23006007','23006008','23006009','23006010','23006011','23006012','23006013','23006015','23006016','23006017','23006018','23006019','23007001','23007002','23007003','23007006']
    Symptom_list=data3["Symptom_Code"].tolist()
    for i in range(len(Symptom_list)):
        Symptom_list[i]=" ".join(Symptom_list[i].split("|"))
    
    vectorizer = CountVectorizer()
    dt=vectorizer.fit_transform(corpus)
    column_names=vectorizer.get_feature_names()
    
    result=[]
    for i in range(len(Symptom_list)):
        symptom=vectorizer.transform([Symptom_list[i]]).toarray()[0]
        result.append(symptom)
    
    Symptom_Feature=pd.DataFrame(result)
    insident=data3['Incident_GUID'].tolist()
    disease=data3['Disease_GUID'].tolist()
    Symptom_Feature['Incident_GUID']=insident
    Symptom_Feature['Disease_GUID']=disease
    
    title_list=column_names
    title_list.append('Incident_GUID')
    title_list.append('Disease_GUID')
    Symptom_Feature.columns=title_list
    return Symptom_Feature
    
#diagnosis use this function
#buy place type code use this function
#eat place tyoe code use this function
#expose type code use this function

def extract_multiple_value_features(data3,column_name,corpus):   
    column_list=data3["{column_name}".format(column_name=column_name)].tolist()
    for i in range(len(column_list)):
        column_list[i]=" ".join(column_list[i].split("|"))
    
    vectorizer = CountVectorizer()
    dt=vectorizer.fit_transform(corpus)
    
    title_list=vectorizer.get_feature_names()
    
    result=[]
    for i in range(len(column_list)):
        feature=vectorizer.transform([column_list[i]]).toarray()[0]
        result.append(feature)
        
    feature_dataframe=pd.DataFrame(result)
    insident=data3['Incident_GUID'].tolist()
    disease=data3['Disease_GUID'].tolist()
    feature_dataframe['Incident_GUID']=insident
    feature_dataframe['Disease_GUID']=disease
    title_list.append('Incident_GUID')
    title_list.append('Disease_GUID')
    feature_dataframe.columns=title_list
    return feature_dataframe

def extract_single_value_features(data3):
#    data3.to_csv("Incident_data_concated.csv",index=False,header=True)  
    corpus=['true','false']
    list1=data3['Disease_OtherIsill'].tolist()
    label_list=[]
    for i in range(len(list1)):
        if list1[i]=='True':
            label_list.append("true")
        if list1[i]=='False':
            label_list.append("false")
#    print(label_list)    
    vectorizer = CountVectorizer()
    dt=vectorizer.fit_transform(corpus)
    title_list=vectorizer.get_feature_names()
    result=[]
    for i in range(len(label_list)):
        feature=vectorizer.transform([label_list[i]]).toarray()[0]
        result.append(feature)
    
    feature_dataframe=pd.DataFrame(result)
    insident=data3['Incident_GUID'].tolist()
    disease=data3['Disease_GUID'].tolist()
    feature_dataframe['Incident_GUID']=insident
    feature_dataframe['Disease_GUID']=disease
    title_list.append('Incident_GUID')
    title_list.append('Disease_GUID')
#    print(feature_dataframe)
#    print(title_list)
    feature_dataframe.columns=title_list
    feature_dataframe=feature_dataframe.drop(['false'], axis=1)
    return feature_dataframe

def extract_hometown_features(data3):
    corpus=['本区县','本市其他区县','本省其他市','外省','港澳台','外籍']
    list1=data3['Disease_Hometown'].tolist()
    # print(type(list1[0]))
    label_list=[]

   # [1：本区县;2：本市其他区县;3：本省其他市;4：外省;5：港澳台;6：外籍]
#[1: local districts and counties; 2: other districts and counties of the city; 3: other cities of the province; 4: other provinces; 5: Hong Kong, Macao and Taiwan; 6: foreign countries]
    for i in range(len(list1)):
        if list1[i]=='1':
            label_list.append("本区县")
        if list1[i]=='2':
            label_list.append("本市其他区县")
        if list1[i]=='3':
            label_list.append("本省其他市")
        if list1[i]=='4':
            label_list.append("外省")
        if list1[i]=='5':
            label_list.append("港澳台")
        if list1[i]=='6':
            label_list.append("外籍")
    vectorizer = CountVectorizer()
    dt=vectorizer.fit_transform(corpus)
    title_list=vectorizer.get_feature_names()
    result=[]
    for i in range(len(label_list)):
        feature=vectorizer.transform([label_list[i]]).toarray()[0]
        result.append(feature)
    
    feature_dataframe=pd.DataFrame(result)
    insident=data3['Incident_GUID'].tolist()
    disease=data3['Disease_GUID'].tolist()
    feature_dataframe['Incident_GUID']=insident
    feature_dataframe['Disease_GUID']=disease
    title_list.append('Incident_GUID')
    title_list.append('Disease_GUID')
    feature_dataframe.columns=title_list
    return feature_dataframe
        
def extract_constant_value_feature(data3):
    list2=data3['ExPosure_EatNum'].tolist()    
    list3=[]
    for i in range(len(list2)):
        list3.append(list2[i].split("|")[0])
    data5=data3[['Incident_GUID','Disease_GUID','Disease_Age','Disease_FoodborneCount']]
    data5['ExPosure_EatNum']=list3
    return data5
def extract_0_1_value_feature(data3):
    corpus=['num1','num0','num2']
    list1=data3['ExPosure_OtherIsill'].tolist()
    for i in range(len(list1)):
        list1[i]=list1[i].split("|")[0]
    # print(type(list1[0]))
    label_list=[]
    for i in range(len(list1)):
        if list1[i]=='1':
            label_list.append("num1")
        if list1[i]=='2':
            label_list.append("num2")
        if list1[i]=='0':
            label_list.append("num0")
    vectorizer = CountVectorizer()
    dt=vectorizer.fit_transform(corpus)
    title_list=vectorizer.get_feature_names()
    result=[]
    for i in range(len(label_list)):
        feature=vectorizer.transform([label_list[i]]).toarray()[0]
        result.append(feature)
    
    feature_dataframe=pd.DataFrame(result)
    insident=data3['Incident_GUID'].tolist()
    disease=data3['Disease_GUID'].tolist()
    feature_dataframe['Incident_GUID']=[insident[0]]*len(feature_dataframe)
    feature_dataframe['Disease_GUID']=disease
    title_list.append('Incident_GUID')
    title_list.append('Disease_GUID')
    feature_dataframe.columns=title_list
    feature_dataframe=feature_dataframe.drop(['num0','num2'], axis=1)
    return feature_dataframe

def distance_compute_2(x,y):
    #culculate distance
    d1=np.sqrt(np.sum(np.square(x-y)))
    return d1
def compute_distance(location_list):
    #Calculate the distance between two cases (age difference, etc.) in the outbreak）
    order_list=list(combinations([i for i in range(len(location_list))],2))
    result=0
    if(len(order_list))==0:
        return 0
    for couple in order_list:
        if location_list[couple[0]] == None: 
            x_value=[0]
        else:
            x_value=str(location_list[couple[0]])
        if location_list[couple[1]] == None: 
            y_value=[0]
        else:
            y_value=str(location_list[couple[1]])
        x=np.array(x_value).astype(float)
        y=np.array(y_value).astype(float)
        result+=distance_compute_2(x,y)
    result=result/len(order_list)
    return result

def compute_distance_location(location_list,class_id2coordinates):
    #Calculate the distance between two cases in an outbreak (geographic difference)
    for i in range(len(location_list)):
        location_list[i]=class_id2coordinates.get(location_list[i])
    order_list=list(combinations([i for i in range(len(location_list))],2))
    result=0
    if(len(order_list))==0:
        return 0
    for couple in order_list:
        if location_list[couple[0]] == None: 
            x_value=[0,0]
        else:
            x_value=str(location_list[couple[0]]).split(",")
        if location_list[couple[1]] == None: 
            y_value=[0,0]
        else:
            y_value=str(location_list[couple[1]]).split(",")
        x=np.array(x_value).astype(float)
        y=np.array(y_value).astype(float)
        result+=distance_compute_2(x,y)
    result=result/len(order_list)
#     print(result)
    return result
   
def extract_age_feature(data1):
    Disease_Age_list=data1["Disease_Age"].tolist()
    Incident_GUID_list=data1['Incident_GUID'].tolist()
    Incident2Disease_Age={}
    for i in range(len(Incident_GUID_list)):
        if Incident_GUID_list[i] not in Incident2Disease_Age:
            Incident2Disease_Age[Incident_GUID_list[i]]=[Disease_Age_list[i]]
        else:
            Incident2Disease_Age[Incident_GUID_list[i]].append(Disease_Age_list[i])
    Age_list=[]
    for incident in Incident2Disease_Age.keys():
        list1=Incident2Disease_Age[incident]
   
        Age_list.append(compute_distance(list1))
    data4=pd.DataFrame({'Incident_GUID':list(Incident2Disease_Age.keys()),'Disease_Age':Age_list})
    return data4
    
def extract_buy_district_feature(data1):
    ExPosure_BuyDistrict_list=data1["ExPosure_BuyDistrict"].tolist()
    Incident_GUID_list=data1['Incident_GUID'].tolist()
    Incident2ExPosure_BuyDistrict={}
    for i in range(len(Incident_GUID_list)):
        if Incident_GUID_list[i] not in Incident2ExPosure_BuyDistrict:
            Incident2ExPosure_BuyDistrict[Incident_GUID_list[i]]=[ExPosure_BuyDistrict_list[i]]
        else:
            Incident2ExPosure_BuyDistrict[Incident_GUID_list[i]].append(ExPosure_BuyDistrict_list[i])   
    #Convert address to latitude and longitude SysCityAreas.csv It is a comparison table
    data2=pd.read_csv("syscode/SysCityAreas.csv",dtype=object,encoding="gbk")
    data2[['Class_Id','Coordinates']]
    class_id_list=data2['Class_Id'].tolist()
    coordinates_list=data2['Coordinates'].tolist()
    class_id2coordinates={}
    for i in range(len(class_id_list)):
        class_id2coordinates[class_id_list[i]]=coordinates_list[i]
    class_id2coordinates['-1']='0,0'
    class_id2coordinates['0']='0,0'
    
    BuyDistrict_list=[]
    for incident in Incident2ExPosure_BuyDistrict.keys():
        list1=Incident2ExPosure_BuyDistrict[incident]
        BuyDistrict_list.append(compute_distance_location(list1,class_id2coordinates))
        
    data4=pd.DataFrame({'Incident_GUID':list(Incident2ExPosure_BuyDistrict.keys()),'ExPose_BuyDistrict':BuyDistrict_list})
    data4['ExPose_BuyDistrict']=data4['ExPose_BuyDistrict'].fillna('0.0')
    return data4
def timestr_to_timestamp(a):
    #Date format to time stamp
    timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp   
def extract_sicktime_feature(data):
    Disease_SickTime_list=data['Disease_SickTime'].tolist()
    for i in range(len(Disease_SickTime_list)):
        Disease_SickTime_list[i]=timestr_to_timestamp(Disease_SickTime_list[i])
    data2=data[["Incident_GUID","Disease_GUID"]]
    data2['Disease_SickTime']=Disease_SickTime_list
    Incident2SickTime={}
    Incident_list=data2['Incident_GUID'].tolist()
    SickTime_list=data2['Disease_SickTime'].tolist()
    for i in range(len(Incident_list)):
        if Incident_list[i] not in Incident2SickTime:
            Incident2SickTime[Incident_list[i]]=[SickTime_list[i]]
        else:
            Incident2SickTime[Incident_list[i]].append(SickTime_list[i])
    SickTime_var=[]
    for incident in Incident2SickTime.keys():
        list1=Incident2SickTime[incident]
        for i in range(len(list1)):
            list1[i]=str(list1[i])
        list2 = map(eval, list1)
        SickTime_var.append(np.std(list(list2)))
    data4=pd.DataFrame({'Incident_GUID':list(Incident2SickTime.keys()),'Disease_SickTime':SickTime_var})
    return data4
   
def extract_treattime_feature(data):
    Disease_TreatTime_list=data['Disease_TreatTime'].tolist()
    for i in range(len(Disease_TreatTime_list)):
        Disease_TreatTime_list[i]=timestr_to_timestamp(Disease_TreatTime_list[i])
    data2=data[["Incident_GUID","Disease_GUID"]]
    data2['Disease_TreatTime']=Disease_TreatTime_list
    Incident2TreatTime={}
    Incident_list=data2['Incident_GUID'].tolist()
    TreatTime_list=data2['Disease_TreatTime'].tolist()
    for i in range(len(Incident_list)):
        if Incident_list[i] not in Incident2TreatTime:
            Incident2TreatTime[Incident_list[i]]=[TreatTime_list[i]]
        else:
            Incident2TreatTime[Incident_list[i]].append(TreatTime_list[i])
    TreatTime_var=[]
    for incident in Incident2TreatTime.keys():
        list1=Incident2TreatTime[incident]
        for i in range(len(list1)):
            list1[i]=str(list1[i])
        list2 = map(eval, list1)
        TreatTime_var.append(np.std(list(list2)))
    data5=pd.DataFrame({'Incident_GUID':list(Incident2TreatTime.keys()),'Disease_TreatTime':TreatTime_var})
    return data5
def extract_eattime_feature(data):
    ExPosure_Eattime_list1=data['ExPosure_Eattime'].tolist()
    ExPosure_Eattime_list=[]
    for i in range(len(ExPosure_Eattime_list1)):
        ExPosure_Eattime_list.append(ExPosure_Eattime_list1[i].split("|")[0])
    for i in range(len(ExPosure_Eattime_list)):
        ExPosure_Eattime_list[i]=timestr_to_timestamp(ExPosure_Eattime_list[i])
    data2=data[["Incident_GUID","Disease_GUID"]]
    data2['ExPosure_Eattime']=ExPosure_Eattime_list
    Incident2Eattime={}
    Incident_list=data2['Incident_GUID'].tolist()
    Eattime_list=data2['ExPosure_Eattime'].tolist()
    for i in range(len(Incident_list)):
        if Incident_list[i] not in Incident2Eattime:
            Incident2Eattime[Incident_list[i]]=[Eattime_list[i]]
        else:
            Incident2Eattime[Incident_list[i]].append(Eattime_list[i])
    Eattime_var=[]
    for incident in Incident2Eattime.keys():
        list1=Incident2Eattime[incident]
        for i in range(len(list1)):
            list1[i]=str(list1[i])
        list2 = map(eval, list1)
        Eattime_var.append(np.std(list(list2)))
    data6=pd.DataFrame({'Incident_GUID':list(Incident2Eattime.keys()),'ExPosure_Eattime':Eattime_var})
    return data6
def extract_time_feature():
    #Time feature extraction: the date is converted into time stamp, and the variance of time stamp in the same outbreak event is calculated as the feature
    data=pd.read_csv("{root}/data_single_location.csv".format(root=root),dtype=object)
    Disease_SickTime_list=data['Disease_SickTime'].tolist()
    Disease_TreatTime_list=data['Disease_TreatTime'].tolist()
    ExPosure_Eattime_list1=data['ExPosure_Eattime'].tolist()
    ExPosure_Eattime_list=[]
    for i in range(len(ExPosure_Eattime_list1)):
        ExPosure_Eattime_list.append(ExPosure_Eattime_list1[i].split("|")[0])
    for i in range(len(Disease_SickTime_list)):
        Disease_SickTime_list[i]=timestr_to_timestamp(Disease_SickTime_list[i])
    for i in range(len(Disease_TreatTime_list)):
        Disease_TreatTime_list[i]=timestr_to_timestamp(Disease_TreatTime_list[i])
    for i in range(len(ExPosure_Eattime_list)):
        ExPosure_Eattime_list[i]=timestr_to_timestamp(ExPosure_Eattime_list[i])
    data2=data[["Incident_GUID","Disease_GUID"]]
    data2['Disease_SickTime']=Disease_SickTime_list
    data2['Disease_TreatTime']=Disease_TreatTime_list
    data2['ExPosure_Eattime']=ExPosure_Eattime_list
    data2.to_csv("{des}/timestamps.csv".format(des=des),index=False,header=True)
    data3=pd.read_csv("{des}/timestamps.csv".format(des=des),dtype=object)


    #sick time
    Incident2SickTime={}
    Incident_list=data3['Incident_GUID'].tolist()
    SickTime_list=data3['Disease_SickTime'].tolist()
    for i in range(len(Incident_list)):
        if Incident_list[i] not in Incident2SickTime:
            Incident2SickTime[Incident_list[i]]=[SickTime_list[i]]
        else:
            Incident2SickTime[Incident_list[i]].append(SickTime_list[i])
    SickTime_var=[]
    for incident in Incident2SickTime.keys():
        list1=Incident2SickTime[incident]
        list2 = map(eval, list1)
        SickTime_var.append(np.std(list(list2)))
    data4=pd.DataFrame({'Incident_GUID':list(Incident2SickTime.keys()),'Disease_SickTime':SickTime_var})
    data4.to_csv("{des}/Disease_SickTime_Feature.csv".format(des=des),index=False,header=True)
    
    #treat time
    Incident2TreatTime={}
    Incident_list=data3['Incident_GUID'].tolist()
    TreatTime_list=data3['Disease_TreatTime'].tolist()
    for i in range(len(Incident_list)):
        if Incident_list[i] not in Incident2TreatTime:
            Incident2TreatTime[Incident_list[i]]=[TreatTime_list[i]]
        else:
            Incident2TreatTime[Incident_list[i]].append(TreatTime_list[i])
    TreatTime_var=[]
    for incident in Incident2TreatTime.keys():
        list1=Incident2TreatTime[incident]
        list2 = map(eval, list1)
        TreatTime_var.append(np.std(list(list2)))
    data5=pd.DataFrame({'Incident_GUID':list(Incident2TreatTime.keys()),'Disease_TreatTime':TreatTime_var})
    data5.to_csv("{des}/Disease_TreatTime_Feature.csv".format(des=des),index=False,header=True)

    #eat time
    Incident2Eattime={}
    Incident_list=data3['Incident_GUID'].tolist()
    Eattime_list=data3['ExPosure_Eattime'].tolist()
    for i in range(len(Incident_list)):
        if Incident_list[i] not in Incident2Eattime:
            Incident2Eattime[Incident_list[i]]=[Eattime_list[i]]
        else:
            Incident2Eattime[Incident_list[i]].append(Eattime_list[i])
    Eattime_var=[]
    for incident in Incident2Eattime.keys():
        list1=Incident2Eattime[incident]
        list2 = map(eval, list1)
        Eattime_var.append(np.std(list(list2)))
    data6=pd.DataFrame({'Incident_GUID':list(Incident2Eattime.keys()),'ExPosure_Eattime':Eattime_var})
    data6.to_csv("{des}/ExPosure_Eattime_Feature.csv".format(des=des),index=False,header=True)
    
def extract_eat_district_feature(data1):
    ExPosure_EatDistrict_list=data1["ExPosure_EatDistrict"].tolist()
    Incident_GUID_list=data1['Incident_GUID'].tolist()
    Incident2ExPosure_EatDistrict={}
    for i in range(len(Incident_GUID_list)):
        if Incident_GUID_list[i] not in Incident2ExPosure_EatDistrict:
            Incident2ExPosure_EatDistrict[Incident_GUID_list[i]]=[ExPosure_EatDistrict_list[i]]
        else:
            Incident2ExPosure_EatDistrict[Incident_GUID_list[i]].append(ExPosure_EatDistrict_list[i])
    #Convert address to latitude and longitude SysCityAreas.csv It is a comparison table
    data2=pd.read_csv("syscode/SysCityAreas.csv",dtype=object,encoding="gbk")
    data2[['Class_Id','Coordinates']]
    class_id_list=data2['Class_Id'].tolist()
    coordinates_list=data2['Coordinates'].tolist()
    class_id2coordinates={}
    for i in range(len(class_id_list)):
        class_id2coordinates[class_id_list[i]]=coordinates_list[i]
    class_id2coordinates['-1']='0,0'
    class_id2coordinates['0']='0,0'
    
    EatDistrict_list=[]
    for incident in Incident2ExPosure_EatDistrict.keys():
        list1=Incident2ExPosure_EatDistrict[incident]
    #     print(list1)
        EatDistrict_list.append(compute_distance_location(list1,class_id2coordinates))
        
    data9=pd.DataFrame({'Incident_GUID':list(Incident2ExPosure_EatDistrict.keys()),'ExPosure_EatDistrict':EatDistrict_list})
    data9['ExPosure_EatDistrict']=data9['ExPosure_EatDistrict'].fillna('0.0')
    return data9
    
def extract_disease_district_feature(data7):
    Disease_District_list=data7["Disease_District"].tolist()
    Incident_GUID_list=data7['Incident_GUID'].tolist()
    Incident2Disease_District={}
    for i in range(len(Incident_GUID_list)):
        if Incident_GUID_list[i] not in Incident2Disease_District:
            Incident2Disease_District[Incident_GUID_list[i]]=[Disease_District_list[i]]
        else:
            Incident2Disease_District[Incident_GUID_list[i]].append(Disease_District_list[i])
    #Convert address to latitude and longitude SysCityAreas.csv It is a comparison table      
    data8=pd.read_csv("syscode/SysCityAreas.csv",dtype=object,encoding="gbk")
    data8[['Class_Id','Coordinates']]
    class_id_list=data8['Class_Id'].tolist()
    coordinates_list=data8['Coordinates'].tolist()
    class_id2coordinates={}
    for i in range(len(class_id_list)):
        class_id2coordinates[class_id_list[i]]=coordinates_list[i]
    class_id2coordinates['-1']='0,0'
    class_id2coordinates['0']='0,0'

    Disease_District_list=[]
    for incident in Incident2Disease_District.keys():
        list1=Incident2Disease_District[incident]
    #     print(list1)
        Disease_District_list.append(compute_distance_location(list1,class_id2coordinates))
        
    data9=pd.DataFrame({'Incident_GUID':list(Incident2Disease_District.keys()),'Disease_District':Disease_District_list})
    data9['Disease_District']=data9['Disease_District'].fillna('0.0')
    return data9


def compute_distance_string(location_list):
   #Function of extracting character string
    b=filter(lambda x: x !="未填写",location_list)
    localtion_list_filtered=list(b)
    order_list=list(combinations([i for i in range(len(localtion_list_filtered))],2))
    result=0
    if(len(order_list))==0:
        return 0
    if(len(order_list))==1:
        return 0
    for couple in order_list:
        if localtion_list_filtered[couple[0]] == None: 
            x_value=[""]
        else:
            x_value=str(localtion_list_filtered[couple[0]])
        if localtion_list_filtered[couple[1]] == None: 
            y_value=[""]
        else:
            y_value=str(localtion_list_filtered[couple[1]])
        result+=fuzz.token_set_ratio(x_value,y_value)
    result=result/len(order_list)
    return result
def compute_distance_sting_1(localtion_list_filtered):
    order_list=list(combinations([i for i in range(len(localtion_list_filtered))],2))
    result=0
    if(len(order_list))==0:
        return 0
    if(len(order_list))==1:
        return 0
    for couple in order_list:
        if localtion_list_filtered[couple[0]] == None: 
            x_value=[""]
        else:
            x_value=str(localtion_list_filtered[couple[0]])
        if localtion_list_filtered[couple[1]] == None: 
            y_value=[""]
        else:
            y_value=str(localtion_list_filtered[couple[1]])
        result+=fuzz.token_set_ratio(x_value,y_value)
    result=result/len(order_list)
#     print(result)
    return result    

def extract_string_feature(data,option):
    #The extracted string features include work unit, case address, eating place, purchasing place and food name
    if option=="Disease_PatientUnit":
        Disease_PatientUnit_list=data['Disease_PatientUnit'].tolist()
        Incident_GUID_list=data['Incident_GUID'].tolist()
        Incident2Disease_PatientUnit={}
        for i in range(len(Incident_GUID_list)):
            if Incident_GUID_list[i] not in Incident2Disease_PatientUnit:
                Incident2Disease_PatientUnit[Incident_GUID_list[i]]=[Disease_PatientUnit_list[i]]
            else:
                Incident2Disease_PatientUnit[Incident_GUID_list[i]].append(Disease_PatientUnit_list[i])    
        PatientUnit_list=[]
        for incident in Incident2Disease_PatientUnit.keys():
            list1=Incident2Disease_PatientUnit[incident]
            PatientUnit_list.append(compute_distance_string(list1))    
        data1=pd.DataFrame({'Incident_GUID':list(Incident2Disease_PatientUnit.keys()),'Disease_PatientUnit':PatientUnit_list})
        return data1
    if option=="Disease_Address":
        Disease_Address_list=data['Disease_Address'].tolist()
        Incident_GUID_list=data['Incident_GUID'].tolist()
        Incident2Disease_Address={}
        for i in range(len(Incident_GUID_list)):
            if Incident_GUID_list[i] not in Incident2Disease_Address:
                Incident2Disease_Address[Incident_GUID_list[i]]=[Disease_Address_list[i]]
            else:
                Incident2Disease_Address[Incident_GUID_list[i]].append(Disease_Address_list[i])
        Address_list=[]
        for incident in Incident2Disease_Address.keys():
            list2=Incident2Disease_Address[incident]
            Address_list.append(compute_distance_sting_1(list2))  
        data2=pd.DataFrame({'Incident_GUID':list(Incident2Disease_Address.keys()),'Disease_Address':Address_list})
        return data2
    if option=="ExPosure_EatAddress":
        ExPosure_EatAddress_list=data['ExPosure_EatAddress'].tolist()
        Incident_GUID_list=data['Incident_GUID'].tolist()
        Incident2ExPosure_EatAddress={}
        for i in range(len(Incident_GUID_list)):
            if Incident_GUID_list[i] not in Incident2ExPosure_EatAddress:
                Incident2ExPosure_EatAddress[Incident_GUID_list[i]]=[ExPosure_EatAddress_list[i]]
            else:
                Incident2ExPosure_EatAddress[Incident_GUID_list[i]].append(ExPosure_EatAddress_list[i])
        EatAddress_list=[]
        for incident in Incident2ExPosure_EatAddress.keys():
            list3=Incident2ExPosure_EatAddress[incident]
            EatAddress_list.append(compute_distance_sting_1(list3))
        data3=pd.DataFrame({'Incident_GUID':list(Incident2ExPosure_EatAddress.keys()),'ExPosure_EatAddress':EatAddress_list})
        return data3
    if option=="ExPosure_Name":
        ExPosure_Name_list=data['ExPosure_Name'].tolist()
        Incident_GUID_list=data['Incident_GUID'].tolist()
        Incident2ExPosure_Name={}
        for i in range(len(Incident_GUID_list)):
            if Incident_GUID_list[i] not in Incident2ExPosure_Name:
                Incident2ExPosure_Name[Incident_GUID_list[i]]=[ExPosure_Name_list[i]]
            else:
                Incident2ExPosure_Name[Incident_GUID_list[i]].append(ExPosure_Name_list[i])
        Name_list=[]
        for incident in Incident2ExPosure_Name.keys():
            list4=Incident2ExPosure_Name[incident]
            Name_list.append(compute_distance_sting_1(list4))
        data4=pd.DataFrame({'Incident_GUID':list(Incident2ExPosure_Name.keys()),'ExPosure_Name':Name_list})
        return data4
    if option=="ExPosure_BuyAddress":
        ExPosure_BuyAddress_list=data['ExPosure_BuyAddress'].fillna('未填写').tolist()
        Incident_GUID_list=data['Incident_GUID'].tolist()
        Incident2ExPosure_BuyAddress={}
        for i in range(len(Incident_GUID_list)):
            if Incident_GUID_list[i] not in Incident2ExPosure_BuyAddress:
                Incident2ExPosure_BuyAddress[Incident_GUID_list[i]]=[ExPosure_BuyAddress_list[i]]
            else:
                Incident2ExPosure_BuyAddress[Incident_GUID_list[i]].append(ExPosure_BuyAddress_list[i])
        BuyAddress_list=[]
        for incident in Incident2ExPosure_BuyAddress.keys():
            list5=Incident2ExPosure_BuyAddress[incident]
            BuyAddress_list.append(compute_distance_string(list5))
        data5=pd.DataFrame({'Incident_GUID':list(Incident2ExPosure_BuyAddress.keys()),'ExPosure_BuyAddress':BuyAddress_list})
        return data5

#is buy domestic,is eat domestic 
def extract_buy_domestic_feature(data3):
    corpus=['true','false']
    list1=data3['ExPosure_IsBuyDomestic'].tolist()
    label_list=[]
    for i in range(len(list1)):
        if list1[i]=='1':
            label_list.append("true")
        elif list1[i]=='0':
            label_list.append("false")
        else:
            label_list.append("false")
        
    vectorizer = CountVectorizer()
    dt=vectorizer.fit_transform(corpus)
    title_list=vectorizer.get_feature_names()
    result=[]
    for i in range(len(label_list)):
        feature=vectorizer.transform([label_list[i]]).toarray()[0]
        result.append(feature)
    
    feature_dataframe=pd.DataFrame(result)
    insident=data3['Incident_GUID'].tolist()
    disease=data3['Disease_GUID'].tolist()
    feature_dataframe['Incident_GUID']=insident
    feature_dataframe['Disease_GUID']=disease
    title_list.append('Incident_GUID')
    title_list.append('Disease_GUID')
    feature_dataframe.columns=title_list
    feature_dataframe=feature_dataframe.drop(['false'], axis=1)
    return feature_dataframe

def extract_eat_domestic_feature(data3):
    corpus=['true','false']
    list1=data3['ExPosure_IsEatDomestic'].tolist()
    label_list=[]
    for i in range(len(list1)):
        if list1[i]=='1':
            label_list.append("true")
        elif list1[i]=='0':
            label_list.append("false") 
        else:
            label_list.append("false")
    vectorizer = CountVectorizer()
    dt=vectorizer.fit_transform(corpus)
    title_list=vectorizer.get_feature_names()
    result=[]
    for i in range(len(label_list)):
        feature=vectorizer.transform([label_list[i]]).toarray()[0]
        result.append(feature)
    
    feature_dataframe=pd.DataFrame(result)
    insident=data3['Incident_GUID'].tolist()
    disease=data3['Disease_GUID'].tolist()
    feature_dataframe['Incident_GUID']=insident
    feature_dataframe['Disease_GUID']=disease
    title_list.append('Incident_GUID')
    title_list.append('Disease_GUID')
    feature_dataframe.columns=title_list
    feature_dataframe=feature_dataframe.drop(['false'], axis=1)
    return feature_dataframe

def cancat(loaded_data2,data):
    #Case feature merging function (adding columns of data)

#De duplication
    loaded_data2=loaded_data2.drop(['Incident_GUID'],axis=1)
#    loaded_data2.drop_duplicates(subset=["Disease_GUID"],keep="first",inplace=True)
    return pd.merge(data,loaded_data2,on="Disease_GUID")
def incident_feature_concat(loaded_data,data):
    #Event feature merging function (adding columns of data)
    loaded_data1 = loaded_data.groupby(by=['Incident_GUID']).sum()
    return pd.merge(data,loaded_data1,on="Incident_GUID")
def extract_feature(data):
    #In the whole process of feature extraction, some vectorization operations need to provide their own codes (corresponding feature name codes in the database) as corpus
#Action means to load data from different directories according to different operations and save the data in different directories
    start13=symptom_feature_extraction(data)
    ExPosure_ProcessingCode_corpus=['23023001','23023002','23023003','23023004','23023005']
    start11=extract_multiple_value_features(data,"ExPosure_ProcessingCode",ExPosure_ProcessingCode_corpus)
    Disease_Occupation_corpus=['23009001','23009002','23009003','23009004','23009006','23009007','23009008','23009009','23009010','23009011','23009012','23009014','23009015','23009016','23009017','23009018','23009019']
    start4=extract_multiple_value_features(data,"Disease_Occupation",Disease_Occupation_corpus)
#    start4.to_csv("Incident_data_concated.csv",index=False,header=True)    
    start5=extract_single_value_features(data)
    start3=extract_hometown_features(data)
    start=extract_constant_value_feature(data)
    start10=extract_0_1_value_feature(data)
    start15=extract_age_feature(data)
    start20=extract_buy_district_feature(data)
    
    start18=extract_sicktime_feature(data)
    start19=extract_treattime_feature(data)
    start24=extract_eattime_feature(data)
    start23=extract_eat_district_feature(data)
    start16=extract_disease_district_feature(data)
    start17=extract_string_feature(data,"Disease_PatientUnit")
    start14=extract_string_feature(data,"Disease_Address")
    start22=extract_string_feature(data,"ExPosure_EatAddress")
    start25=extract_string_feature(data,"ExPosure_Name")
    start21=extract_string_feature(data,"ExPosure_BuyAddress")
    Diagnosis_Code_corpus=['23012001','23012002','23012003','23012004','23012005','23012007','23012008','23012010','23012011']
    start2=extract_multiple_value_features(data,'Diagnosis_Code',Diagnosis_Code_corpus)
    ExPosure_BuyPlaceTypeCode_corpus=['23024001','23024002','23024002001','23024002002','23024002003','23024002005','23024003','23024003001','23024003002','23024003003','23024004','23024004001','23024004002','23024004003','23024004004','23024005','23024005001','23024006','nan',]
    start6=extract_multiple_value_features(data,'ExPosure_BuyPlaceTypeCode',ExPosure_BuyPlaceTypeCode_corpus)
    ExPosure_EatPlaceTypeCode_corpus=['23015001','23015001001','23015002','23015002001','23015002002','23015002003','23015002005','23015003','23015003001','23015003002','23015003003','23015004','23015004001','23015004002','23015004003','23015004004','23015005','23015005001','23015006','23015006001','23015007','nan']
    start7=extract_multiple_value_features(data,"ExPosure_EatPlaceTypeCode",ExPosure_EatPlaceTypeCode_corpus)
    start8=extract_buy_domestic_feature(data)
    start9=extract_eat_domestic_feature(data)
    ExPosure_TypeCode_corpus=['23022001','23022002','23022003','23022004','23022005','23022006','23022007','23022008','23022009','23022010','23022011','23022012','23022013','23022014','23022015','23022016','23022017','23022018','23022019','23022020','23022021','23022022']
    start12=extract_multiple_value_features(data,'ExPosure_TypeCode',ExPosure_TypeCode_corpus)
    
    
    Incident_list_temp=start["Incident_GUID"].tolist()
    data1=start[["Disease_GUID",'Disease_FoodborneCount','ExPosure_EatNum']]
    #合并病例特征
    data1=cancat(start2,data1)
    data1=cancat(start3,data1)
    data1=cancat(start4,data1)
    data1=cancat(start5,data1)
    data1=cancat(start6,data1)
    data1=cancat(start7,data1)
        
    data1=cancat(start8,data1)
        
    data1=cancat(start9,data1)
    data1=cancat(start10,data1)
    data1=cancat(start11,data1)
    data1=cancat(start12,data1)
    data1=cancat(start13,data1)
    #The obtained pathological features were preserved
    data1.insert(0,'Incident_GUID',Incident_list_temp)
    col_list=[column for column in data1]
    col_list.remove("Incident_GUID")
    col_list.remove("Disease_GUID")
    #Convert data type to float
    for col in col_list:
        data1[col]=data1[col].astype(float)
    #The case characteristics were integrated according to their respective outbreak events, and the average value was obtained to obtain the characteristics of the outbreak events
    data2=data1.groupby("Incident_GUID").agg('mean')
    #According to different operations, the characteristics of outbreak time were combined
    data2=incident_feature_concat(start14,data2)
    data2=incident_feature_concat(start15,data2)
    data2=incident_feature_concat(start16,data2)
    data2=incident_feature_concat(start17,data2)
    data2=incident_feature_concat(start18,data2)
    data2=incident_feature_concat(start19,data2)
    data2=incident_feature_concat(start20,data2)
    data2=incident_feature_concat(start21,data2)
    data2=incident_feature_concat(start22,data2)
    data2=incident_feature_concat(start23,data2)
    data2=incident_feature_concat(start24,data2)
    data2=incident_feature_concat(start25,data2)
    #Finally, all that can be used as model input is obtained_ feature_ concated_ data_ with_ label.csv
    return data2
    
    
    
    
    
    
    
    
    
    
    