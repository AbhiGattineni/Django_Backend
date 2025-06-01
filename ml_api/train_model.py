import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib
import os

# Load dataset
url = "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"
data = pd.read_csv(url)

# Split features and target
X = data.drop("medv", axis=1)
y = data["medv"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Save model to current directory (ml_api/)
model_path = os.path.join(os.path.dirname(__file__), 'house_price_model.pkl')
joblib.dump(model, model_path)

