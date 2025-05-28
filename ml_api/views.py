import os
import json
import joblib
import pandas as pd
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from .models import HousePrediction
from sklearn.linear_model import LinearRegression

# Path to the model file inside ml_api folder
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_api', 'house_price_model.pkl')

# Load model once at the top level
# model = joblib.load(MODEL_PATH)
model = None  # temporarily disable loading

@csrf_exempt
def predict_house_price(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            fields = ['crim', 'zn', 'indus', 'chas', 'nox', 'rm', 'age',
                      'dis', 'rad', 'tax', 'ptratio', 'b', 'lstat']
            features = [data[field] for field in fields]

            prediction = model.predict([features])[0]

            # Save input and prediction to DB
            HousePrediction.objects.create(
                **{field: data[field] for field in fields},
                predicted_price=round(prediction, 2)
            )

            return JsonResponse({'predicted_price': round(prediction, 2)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)


@csrf_exempt
# @user_passes_test(lambda u: u.is_superuser)
def retrain_model_view(request):
    if request.method == 'POST':
        try:
            # Load original dataset
            df_csv = pd.read_csv("https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv")

            # Load saved user inputs from DB
            qs = HousePrediction.objects.all().values()
            df_db = pd.DataFrame.from_records(qs)

            # Rename predicted_price to medv to match CSV format
            if not df_db.empty:
                df_db = df_db.rename(columns={'predicted_price': 'medv'})
                df_db = df_db[df_csv.columns]  # match columns to CSV

            # Combine both datasets
            df_combined = pd.concat([df_csv, df_db], ignore_index=True)

            # Drop rows with any missing values in features or target
            df_combined = df_combined.dropna()

            # Split into X and y
            X = df_combined.drop("medv", axis=1)
            y = df_combined["medv"]

            # Train model
            model = LinearRegression()
            model.fit(X, y)

            # Save updated model
            joblib.dump(model, MODEL_PATH)

            return JsonResponse({'message': 'Model retrained successfully!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST allowed'}, status=405)

