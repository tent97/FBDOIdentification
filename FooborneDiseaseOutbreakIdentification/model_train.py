# -*- coding: utf-8 -*-
import pymssql
import pandas as pd
import numpy as np
import get_data_from_database
import data_preprocessing
import feature_extraction
import xgboost
import random
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import  recall_score
from sklearn.metrics import f1_score
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.model_selection import cross_val_score 
from sklearn.feature_selection import SelectKBest,chi2

def read_data(action):
    if action=="liudiao":
        data=pd.read_csv("train_data/流调数据.csv",dtype=object)
        incident_list=data["ID"].tolist()
        disease_list=data["Disease_GUID"].tolist()
        incident_dict={}
        for i in range(len(incident_list)):
            if incident_list[i] not in incident_dict:
                incident_dict[incident_list[i]]={}
                incident_dict[incident_list[i]]["disease_list"]=[]
                incident_dict[incident_list[i]]["label"]=1
        disease2incident={}
        for i in range(len(disease_list)):
            disease2incident[disease_list[i]]=incident_list[i]
        for item in disease2incident:
            incident_dict[disease2incident[item]]["disease_list"].append(item)
        return incident_dict
    if action=="system":
        data1=pd.read_csv("train_data/系统数据.csv",dtype=object)
        data2=pd.read_csv("train_data/系统数据病例与事件对应表.csv",dtype=object)
        incident_list=data2["事件GUID"].tolist()
        disease_list=data2["病例GUID"].tolist()
        incident_dict={}
        for i in range(len(incident_list)):
            if incident_list[i] not in incident_dict:
                incident_dict[incident_list[i]]={}
                incident_dict[incident_list[i]]["disease_list"]=[]
                incident_dict[incident_list[i]]["label"]=0
        for i in range(len(incident_list)):
            incident_dict[incident_list[i]]["disease_list"].append(disease_list[i])
        incident_list1=data1["事件guid"].tolist()
        label_list=data1["状态"].tolist()
        incident2label={}
        for i in range(len(incident_list1)):
            if label_list[i]=="已排除":
                incident2label[incident_list1[i]]=0
            else:
                incident2label[incident_list1[i]]=1
        for item in incident_dict:
            incident_dict[item]["label"]=incident2label[item]
        return incident_dict
def train(incident_dict,fine_tuning=False,save=False):
    #incident_dict={incident1{disease_list:[1,2,3,4],label:1 or 0}}
    incident_list=[]
    label_list=[]
    for item in incident_dict:
        incident_list.append(item)
        label_list.append(incident_dict[item]["label"])
    incident_list=np.array(incident_list)
    incident_list=incident_list.reshape(-1,1)
    #split data
    X_train, X_test, y_train, y_test = train_test_split(incident_list, label_list, test_size=0.2, random_state=0)
    y_train=np.array(y_train).astype(int)
    y_test=np.array(y_test).astype(int)
    train_incident_list=np.array(X_train).reshape(1,-1)
    test_incident_list=np.array(X_test).reshape(1,-1)
    processed_train_data=[]
    processed_test_data=[]
    y_train_1=[]
    y_test_1=[]
    #Each piece of data in the dataset is used as input, query database, feature extraction, feature integration and feature selection to get the input of each piece of training data
    for incident in train_incident_list[0]:
        #return a dataframe
        try:
            data=get_data_from_database.get_data_from_database(incident,incident_dict[incident]["disease_list"],"train")
        except:
            continue
        y_train_1.append(int(incident_dict[incident]["label"]))
        data1=data_preprocessing.combine_same_disease_GUID(data)
        data2=feature_extraction.extract_feature(data1)
        data2=data2.fillna('0.0')
        processed_train_data.append(data2.values[0])
    #feature selection
    processed_train_data=np.array(processed_train_data)
    y_train_1=np.array(y_train_1)

    train_feature_selected=SelectKBest(chi2,k=20).fit_transform(processed_train_data,y_train_1)
    feature_selected=SelectKBest(chi2,k=20).fit(processed_train_data,y_train_1).get_support(indices=True)
    for i in range(len(feature_selected)):
        feature_selected[i]=int(feature_selected[i])
    print(feature_selected)
    filename = 'model/feature_selection_resut.txt'
    with open(filename, 'w') as file_object:
        file_object.write(str(feature_selected))
    
    if fine_tuning:
        learning_rate =0.1 
        n_estimators=100
        max_depth=5
        min_child_weight=1 
        gamma=0 
        subsample=0.8 
        colsample_bytree=0.8
        scale_pos_weight=1
        #Tune max_depth and min_child_weight
        param_grid = {
           'max_depth':range(3,10,2),
           'min_child_weight':range(1,6,2)
        }
        model = XGBClassifier(booster='gbtree',objective='binary:logistic',n_estimators=n_estimators,learning_rate=learning_rate,max_depth=max_depth,
                              min_child_weight=min_child_weight,gamma=gamma,subsample=subsample,
                              colsample_bytree=colsample_bytree,scale_pos_weight=scale_pos_weight,
                              max_delta_step=2)
        inner_cv = KFold(n_splits=4, shuffle=True, random_state=0)
        clf = GridSearchCV(estimator=model, param_grid=param_grid, cv=inner_cv) 
        clf.fit(train_feature_selected, y_train_1)
        print(clf.best_score_)
        print(clf.best_params_)
        max_depth=clf.best_params_['max_depth']
        min_child_weight=clf.best_params_['min_child_weight']
        #Tune gamma
        param_grid1 = {
            'gamma':[i/10.0 for i in range(0,5)]
        }
        model1 = XGBClassifier(booster='gbtree',objective='binary:logistic',n_estimators=n_estimators,learning_rate=learning_rate,max_depth=max_depth,
                              min_child_weight=min_child_weight,gamma=gamma,subsample=subsample,
                              colsample_bytree=colsample_bytree,scale_pos_weight=scale_pos_weight,
                              max_delta_step=2)
        inner_cv = KFold(n_splits=4, shuffle=True, random_state=0)
        clf1 = GridSearchCV(estimator=model1, param_grid=param_grid1, cv=inner_cv) 
        clf1.fit(train_feature_selected, y_train_1)
        print(clf1.best_score_)
        print(clf1.best_params_)
        gamma=clf1.best_params_['gamma']
        
        # Tune subsample and colsample_bytree
        param_grid2 = {
            'subsample':[i/10.0 for i in range(6,10)],
            'colsample_bytree':[i/10.0 for i in range(6,10)]
        }
        model2 = XGBClassifier(booster='gbtree',objective='binary:logistic',n_estimators=n_estimators,learning_rate=learning_rate,max_depth=max_depth,
                              min_child_weight=min_child_weight,gamma=gamma,subsample=subsample,
                              colsample_bytree=colsample_bytree,scale_pos_weight=scale_pos_weight,
                              max_delta_step=2)
        inner_cv = KFold(n_splits=4, shuffle=True, random_state=0)
        clf2 = GridSearchCV(estimator=model2, param_grid=param_grid2, cv=inner_cv) 
        clf2.fit(train_feature_selected, y_train_1)
        print(clf2.best_score_)
        print(clf2.best_params_)
        subsample=clf2.best_params_['subsample']
        colsample_bytree=clf2.best_params_['colsample_bytree']
        
        # Tuning Regularization Parameters
        param_grid3 = {
            'reg_alpha':[1e-5, 1e-2, 0.1, 1, 100]
        }
        model3 = XGBClassifier(booster='gbtree',objective='binary:logistic',n_estimators=n_estimators,learning_rate=learning_rate,max_depth=max_depth,
                              min_child_weight=min_child_weight,gamma=gamma,subsample=subsample,
                              colsample_bytree=colsample_bytree,scale_pos_weight=scale_pos_weight,
                              max_delta_step=2)
        inner_cv = KFold(n_splits=4, shuffle=True, random_state=0)
        clf3 = GridSearchCV(estimator=model3, param_grid=param_grid3, cv=inner_cv) 
        clf3.fit(train_feature_selected, y_train_1)
        print(clf3.best_score_)
        print(clf3.best_params_)
        reg_alpha=clf3.best_params_['reg_alpha']
        
        clf_xgboost = XGBClassifier(booster='gbtree',objective='binary:logistic',n_estimators=n_estimators,learning_rate=learning_rate,max_depth=max_depth,
                              min_child_weight=min_child_weight,gamma=gamma,subsample=subsample,
                              colsample_bytree=colsample_bytree,scale_pos_weight=scale_pos_weight,
                              max_delta_step=2,reg_alpha=reg_alpha)
        clf_xgboost.fit(train_feature_selected,y_train_1)
        for incident in test_incident_list[0]:
            #return a dataframe
            try:
                data=get_data_from_database.get_data_from_database(incident,incident_dict[incident]["disease_list"],"train")
            except:
                continue
            y_test_1.append(int(incident_dict[incident]["label"]))
            data1=data_preprocessing.combine_same_disease_GUID(data)
            data2=feature_extraction.extract_feature(data1)
            data2=data2.fillna('0.0')
            processed_test_data.append(data2.values[0])
        #特征选择
        processed_test_data=np.array(processed_test_data)
        test_feature_selected=processed_test_data[:,feature_selected]
        y_predict=clf_xgboost.predict(test_feature_selected)
        print(recall_score(y_test_1,y_predict))
        f1=f1_score(y_test_1,y_predict)
        print(f1)
        print(clf_xgboost)
    else:    
        clf_xgboost = XGBClassifier(booster='gbtree',objective='binary:logistic',n_estimators=50,learning_rate=0.05,max_depth=4,max_delta_step=2)
        clf_xgboost.fit(train_feature_selected,y_train_1)
        for incident in test_incident_list[0]:
        #return a dataframe
            try:
                data=get_data_from_database.get_data_from_database(incident,incident_dict[incident]["disease_list"],"train")
            except:
                continue
            y_test_1.append(int(incident_dict[incident]["label"]))
            data1=data_preprocessing.combine_same_disease_GUID(data)
            data2=feature_extraction.extract_feature(data1)
            data2=data2.fillna('0.0')
            processed_test_data.append(data2.values[0])
        #feature selection
        processed_test_data=np.array(processed_test_data)
        test_feature_selected=processed_test_data[:,feature_selected]
        y_predict=clf_xgboost.predict(test_feature_selected)
        print(recall_score(y_test_1,y_predict))
        f1=f1_score(y_test_1,y_predict)
        print(f1)
    #save model
    if save:
        joblib.dump(clf_xgboost, "model/FBDO.joblib.dat")
    #The current model directory for the use of flow data and system data training model
if __name__ == "__main__":
    dict1=read_data("liudiao")
    dict2=read_data("system")
    dict3 = dict1.copy()
    #Dict3 is the whole data set. Due to the long training time, some data are randomly selected and stored in dict4，
    dict3.update(dict2)
    dict4={}
    count=0
#    for item in dict3:
#        dict4[item]=dict3[item]
#        count+=1
#        if count==200:
#            break
    for i in range(200):
        key=random.choice(list(dict3.keys()))
        dict4[key]=dict3[key]
#    for item in dict4:
#        print(dict4[item]["label"])
    train(dict4,fine_tuning=True,save=True)        
    
