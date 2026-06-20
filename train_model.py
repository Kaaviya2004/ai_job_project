import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score

print("Loading Dataset...")

df = pd.read_csv("data/global_ai_jobs.csv")

features = [
    'country',
    'job_role',
    'ai_specialization',
    'experience_level',
    'experience_years',
    'education_required',
    'industry',
    'company_size',
    'work_mode',
    'skill_demand_score',
    'career_growth_score'
]

target = 'salary_usd'

print("Encoding Data...")

label_encoders = {}

categorical_cols = df[features].select_dtypes(include=['object']).columns

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

X = df[features]
y = df[target]

print("Splitting Dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Random Forest Model...")

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Making Predictions...")

predictions = model.predict(X_test)

r2 = r2_score(y_test, predictions)

print(f"\nR2 Score: {r2:.4f}")

joblib.dump(model, "models/salary_model.pkl")
joblib.dump(label_encoders, "models/label_encoders.pkl")

print("\nModel Saved Successfully!")