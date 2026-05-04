# 🎓 Student Placement Prediction - Streamlit App

A machine learning-powered web application to predict student placement outcomes using the Support Vector Machine (SVM) model.

## 📊 Model Information

- **Algorithm**: Support Vector Machine (SVM)
- **ROC-AUC Score**: 0.833 (Best performer)
- **Training Data**: 32 student records with class balancing via SMOTE
- **Classes**: Placed (1) / Not Placed (0)

## ✨ Features

- 📚 Academic performance input (CGPA, 10th & 12th percentages)
- 💻 Technical skills assessment (coding level, DSA, languages)
- 🏆 Experience tracking (internships, projects, hackathons)
- 📜 Certifications & achievements
- 🗣️ Soft skills evaluation (communication, confidence)
- 🔮 Real-time placement prediction with confidence scores
- 📋 Input summary for verification

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Streamlit App
```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 📋 How It Works

1. **Fill in your details** - Enter your academic performance, skills, and experience
2. **Select appropriate levels** - Choose from predefined options for ease of input
3. **Click "Predict Placement"** - Get instant prediction with confidence score
4. **View recommendations** - Receive actionable feedback based on prediction

## 🎯 Input Fields

### Academic Information
- CGPA (1.0 - 10.0)
- 10th Percentage
- 12th/Diploma Percentage
- Active Backlogs (Yes/No)
- Willingness to Improve

### Technical Skills
- Coding Skill Level (Beginner, Intermediate, Advanced)
- DSA Knowledge (Basic, Medium, High)
- Number of Internships
- Number of Projects
- Programming Languages Known (1-8)
- Hackathons Participation (Yes/No)
- Technical Certifications (Yes/No)

### Soft Skills
- Communication Skills (1-5 rating)
- Interview Confidence (1-5 rating)
- Logical Reasoning (Low, Medium, High)

## 📁 Project Structure

```
ml_model_train_test/
├── app.py                          # Streamlit application
├── requirements.txt                # Python dependencies
├── primary_data_ml_improved.ipynb   # Training notebook
├── primary_data_ml.ipynb           # Original notebook
├── student_responses.csv           # Training data
└── saved_models/
    ├── best_model.pkl             # SVM model (used in app)
    ├── scaler.pkl                 # Feature scaler
    ├── feature_names.pkl          # Feature names for preprocessing
    ├── all_models.pkl             # All 5 trained models
    └── results.pkl                # Model performance metrics
```

## 🔧 Model Details

The SVM model was trained with:
- **Data Preprocessing**: Column name cleaning, missing value imputation, categorical encoding
- **Class Balancing**: SMOTE (Synthetic Minority Over-sampling Technique) to handle 90.6% vs 9.4% imbalance
- **Feature Scaling**: StandardScaler normalization for optimal SVM performance
- **Evaluation**: ROC-AUC preferred metric for imbalanced classification

## ⚠️ Important Notes

1. **Preprocessing Order**: The app follows the exact preprocessing steps from the training notebook
2. **Feature Scaling**: Input features are automatically scaled using the saved scaler
3. **Model Consistency**: Uses the SVM model selected for its superior ROC-AUC score
4. **Error Handling**: If prediction fails, check that all fields are filled correctly

## 📊 Output Interpretation

- **Prediction = 1 (PLACED)**: Model predicts you will get placed
- **Prediction = 0 (NOT PLACED)**: Model suggests you need to improve specific areas
- **Confidence Score**: Relative certainty of the prediction

## 🛠️ Troubleshooting

### Issue: "Error loading model"
- Ensure `saved_models/` directory exists with pickle files
- Check file paths are correct

### Issue: "Prediction Error"
- Verify all input fields are filled
- Check that numeric values are within valid ranges
- Ensure feature preprocessing matches training data

### Issue: Streamlit won't load
- Verify Streamlit is installed: `pip install streamlit`
- Check port 8501 is available
- Try running: `streamlit run app.py --logger.level=debug`

## 📚 Training Information

See `primary_data_ml_improved.ipynb` for:
- Complete preprocessing pipeline
- Class imbalance analysis
- SMOTE implementation details
- All 5 model comparisons (Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, SVM)
- Feature importance analysis
- ROC-AUC curves

## 👨‍💻 Developer Notes

- **Language**: Python 3.8+
- **Framework**: Streamlit 1.28.1
- **ML Libraries**: scikit-learn, imbalanced-learn
- **Data Processing**: pandas, numpy

## 📝 License

Educational project for student placement prediction.

## 🎓 Credits

Built as part of university semester project for placement prediction analysis.
