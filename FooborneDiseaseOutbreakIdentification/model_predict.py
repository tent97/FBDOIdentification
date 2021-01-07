# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.model_selection import cross_val_score 
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import data_preprocessing
import feature_extraction
import get_data_from_database
import model_predict
def predict(model_input,output_type):
    #load model
    loaded_model = joblib.load("model/FBDO.joblib.dat")
    #The model can output 0-1 label and probability
    if output_type=="label":
        y_predict=loaded_model.predict(model_input)
        return y_predict[0]
    elif output_type=="probability":
        y_predict=loaded_model.predict_proba(model_input)
        return y_predict[0][1]
    else:
        return 0
def main(outbreak_ID,bus_disease_GUID,output_type):
    #outbreak_ ID: the ID string of the outbreak

#bus_ disease_ GUID ：outbreak_ Case ID list contained in ID []

#The output format can be "label" or "probability" to output label or probability

#Query bus from database_ disease_ To generate query results
    data=get_data_from_database.get_data_from_database(outbreak_ID,bus_disease_GUID,"predict")
    data1=data_preprocessing.combine_same_disease_GUID(data)
    data2=feature_extraction.extract_feature(data1)
    data2=data2.fillna('0.0')
    #load feature
    res=""
    f = open("model/feature_selection_resut.txt", "r")
    ff=f.readlines()
    for line in ff:
        line=line.rstrip("\n")
        res+=line
    
    res=res[1:-1]
    index_list=res.split(" ")
    index_list = list(filter(None, index_list))
    for i in range(len(index_list)):
        index_list[i]=int(index_list[i])
    predict_feature_selected=np.array(data2)[:,index_list]
    #model predict
    output=model_predict.predict(predict_feature_selected,output_type)
    if output_type=="label":
        print("the label is: ")
        print(output)
    if output_type=="probability":
        print("the probability is: ")
        print(output)
    return output

if __name__ == "__main__":
    outbreak="北京市_OUTBREAK_124"
    case_list=['59fdc8ef13654b7eb348a05f3a3661cc','f7626c60b39741acbe48a5c39a7b4589','1ed2ca05096343faae55f1dc468cf7f7','ce73b94ddea24d4ba15d77779ad9fabd']
    output=main(outbreak,case_list,"label")