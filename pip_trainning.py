from sklearn.model_selection import train_test_split ,RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import r2_score , log_loss, root_mean_squared_error , confusion_matrix
from sklearn.linear_model import ridge_regression
from sklearn.ensemble import RandomForestRegressor
import xgboost
import pandas as pd

first_train_num=["Year", "Kilometers_Driven", "Engine", "Power", "Seats","Consumation","car_age","km/age"]
first_train_cat=["Fuel_Type", "Transmission", "Owner_Type", "Location","Brand","Model"]
Grid_pipe = {
"model__n_estimators": [100,200,300],
"model__max_depth" : [None, 10,20],
"model__min_samples_split": [2,5],
"model__min_samples_leaf":[1,2]
}
path = r"Data\data_to_train.csv"
model = RandomForestRegressor(random_state=40)



def pip_test(csv_path=path,model=model,grid=Grid_pipe,num=first_train_num,cat=first_train_cat):

    data=pd.read_csv(csv_path, sep=',')
    x=data.drop(columns="Price")
    y=data["Price"]

    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2, random_state=42)

    numeric_features = num
    categorical_features = cat

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
        ]
    )
    pipe = Pipeline([
        ("pre", preprocessor),
        ("model",model)

    ])

    

    random_search= RandomizedSearchCV(
        estimator=pipe,
        param_distributions=grid,
        n_jobs = -1,
        verbose=1,
        cv=5,
        scoring="neg_root_mean_squared_error"
    )

    train = random_search.fit(x_train, y_train)
    y_pred = train.predict(x_test)
    r2 = r2_score(y_test, y_pred)
    rmse = root_mean_squared_error(y_test,y_pred)
    
    return train.best_score_, train.best_params_, train.best_estimator_,r2,rmse

score,params,estimator,r2,rmse = pip_test()
print(r2)