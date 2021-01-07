| file/folder               | description                                                  |
| ------------------------- | ------------------------------------------------------------ |
| /model                    | Stored model                                                 |
| /predict_data             | Store the query results of forecast data                     |
| /syscode                  | Storage table of geographical location, longitude and latitude |
| /train_data               | Data set and query results of training data                  |
| data_preprocessing.py     | Data preprocessing correlation function                      |
| feature_extraction.py     | Correlation function of feature extraction and feature selection |
| get_data_from_database.py | Connect database and query related functions                 |
| model_predict.py          | Correlation function of model prediction and output prediction results |
| model_trian.py            | Model training, parameter optimization, feature selection, correlation function |
|                           |                                                              |

dataset：

train_data/流调数据.csv

train_data/系统数据.csv

description：

Data preprocessing, feature selection and feature merging all take the case data frame in the same outbreak event as input, and unnecessary intermediate results are no longer saved.

The case list in each outbreak data is used as the input of database query function. After data preprocessing, feature selection and feature combination, a training data or prediction data is obtained. After the training set is obtained, feature selection is carried out on the training set, and the result of feature selection (index is saved). After the model is trained, the test set is processed in the same way to predict the effect of the model. When using the model for prediction, the same operation is carried out.

model_train.py:

| functionn name                                      | input                                                        | output              | description                                                  |
| --------------------------------------------------- | ------------------------------------------------------------ | ------------------- | ------------------------------------------------------------ |
| read_data(action)                                   | action(str):"system"or "liudiao"                             | incident_dict(dict) | The corresponding relationship between the outbreak event and the case, and the outbreak event label was stored in dict |
| train(incident_dict, fine_tuning=False ,save=False) | incident_dict(dict),fine_tuning:whether to tune the parameters and save the model | none                | Generating data set, dividing test set, training set, feature selection, parameter tuning, saving model |

model_train.py:

| function name                                   | input                                                        | Output                   | Description   |
| ----------------------------------------------- | ------------------------------------------------------------ | ------------------------ | ------------- |
| predict(model_input, output_type):              | model_input（np.array）：Processed model input, output_type(str):output type“label”or "probability" | y_predict predict result | model predict |
| main(outbreak_ID,bus_disease_GUID ,output_type) | outbreak_ID(str)：Name of outbreak, bus_disease_GUID(list):Case list ，output_type(str):type of output“label”or "probability" | output：predict result   | model predict |
|                                                 |                                                              |                          |               |

