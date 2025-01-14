from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from .form import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect

import tensorflow as tf
from django.shortcuts import render
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib

# Load the model
model = tf.keras.models.load_model('C:/Users/HP/Desktop/PregnancyModelChatBot/maternalRiskPrediction.h5')

# Load the scaler used during training
scaler = joblib.load('C:/Users/HP/Desktop/PregnancyModelChatBot/scaler.pkl')


# Create your views here.

def home(request):
    return render(request, 'app/home.html')

def risk(request):
    return render(request, 'app/risk.html')

def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'app/inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chatBot')  # Redirect to 'chatPage'
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'app/connexion.html')


def predictRisk(request):
    if request.method == 'POST':
        try:
            # Collect inputs from the form
            age = float(request.POST.get('Age'))
            systolicBP = float(request.POST.get('SystolicBP'))
            diastolicBP = float(request.POST.get('DiastolicBP'))
            bS = float(request.POST.get('BS'))
            bodyTemp = float(request.POST.get('BodyTemp'))
            heartRate = float(request.POST.get('HeartRate'))

            # Combine inputs into an array
            input_data = np.array([[age, systolicBP, diastolicBP, bS, bodyTemp, heartRate]])

            # Scale the input data
            scaled_data = scaler.transform(input_data)

            # Make prediction
            predictions = model.predict(scaled_data)
            predicted_class = np.argmax(predictions, axis=1)[0]

            # Decode the predicted class
            risk_levels = {
                0: ('Low Risk', 'green'),
                1: ('Mid Risk', 'orange'),
                2: ('High Risk', 'red')
            }
            predicted_risk, risk_color = risk_levels[predicted_class]

            # Render result with modal display
            return render(request, 'app/risk.html', {
                'prediction': predicted_risk,
                'risk_color': risk_color
            })
        except Exception as e:
            return render(request, 'app/risk.html', {'error': str(e)})

    return render(request, 'app/risk.html')


    from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')
