import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
import os
import user_data_manager
warnings.filterwarnings('ignore')

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="PlacePredict",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CUSTOM CSS FOR NAVBAR & STYLING
# ============================================
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
    load_css(css_path)
except Exception as e:
    pass

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if 'page' not in st.session_state:
    st.session_state.page = 'Home'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'mobile_menu_open' not in st.session_state:
    st.session_state.mobile_menu_open = False

def toggle_menu():
    st.session_state.mobile_menu_open = not st.session_state.mobile_menu_open

def close_menu():
    st.session_state.mobile_menu_open = False

# ============================================
# NAVBAR NAVIGATION
# ============================================

if not st.session_state.logged_in:
    col_logo, col_empty, col1, col2, col3, col4 = st.columns([2, 4, 1, 1, 1, 1.5])
    with col_logo:
        st.markdown("<h3 class='navbar-logo' style='color: #1e3a8a; font-weight: 800; margin: 0; padding-top: 5px;'>🎓 PlacePredict</h3>", unsafe_allow_html=True)
    with col1:
        if st.button("🏠 Home", width="stretch", key="nav_home"):
            st.session_state.page = 'Home'
    with col2:
        if st.button("📊 EDA", width="stretch", key="nav_eda"):
            st.session_state.page = 'EDA'
    with col3:
        if st.button("🎓 Predict", width="stretch", key="nav_predict"):
            st.session_state.page = 'Predict'
    with col4:
        if st.button("🔑 Login / Sign Up", width="stretch", key="nav_login"):
            st.session_state.page = 'Login'
else:
    col_logo, col_empty, col1, col2, col3, col4, col5 = st.columns([2, 3, 1, 1, 1, 1.5, 1])
    with col_logo:
        st.markdown("<h3 class='navbar-logo' style='color: #1e3a8a; font-weight: 800; margin: 0; padding-top: 5px;'>🎓 PlacePredict</h3>", unsafe_allow_html=True)
    with col1:
        if st.button("🏠 Home", width="stretch", key="nav_home_in"):
            st.session_state.page = 'Home'
    with col2:
        if st.button("📊 EDA", width="stretch", key="nav_eda_in"):
            st.session_state.page = 'EDA'
    with col3:
        if st.button("🎓 Predict", width="stretch", key="nav_predict_in"):
            st.session_state.page = 'Predict'
    with col4:
        if st.button("👤 User Profile", width="stretch", key="nav_profile"):
            st.session_state.page = 'Dashboard'
    with col5:
        if st.button("🚪 Logout", width="stretch", key="nav_logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.page = 'Home'
            st.rerun()

st.divider()

# ============================================
# PAGE: HOME
# ============================================
if st.session_state.page == 'Home':
    st.write("") # Top spacing
    
    col_text, col_img = st.columns([1.2, 1], gap="large")
    
    with col_text:
        st.markdown('<div class="hero-text" style="text-align: left; margin-bottom: 0;">🎓 PlacePredict</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subtext" style="text-align: left; margin-top: 0.5rem; margin-bottom: 2rem;">AI-Powered Placement Prediction & Analysis</div>', unsafe_allow_html=True)
        
        st.write("""
        ### Why Placement Prediction Matters 🎯
        
        Understanding your employability before interview season begins is crucial. 
        Get a realistic assessment of your placement chances with our advanced SVM model.
        """)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Explore Data 📊", width='stretch', key="btn_eda_hero"):
                st.session_state.page = 'EDA'
                st.rerun()
        with col_btn2:
            if st.button("Predict Now 🎓", width='stretch', type="primary", key="btn_predict_hero"):
                st.session_state.page = 'Predict'
                st.rerun()
        
    with col_img:
        hero_jpg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "hero.jpg")
        hero_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "hero.png")
        if os.path.exists(hero_jpg):
            st.image(hero_jpg, use_column_width='always')
        elif os.path.exists(hero_png):
            st.image(hero_png, use_column_width='always')
            
    st.divider()
    
    st.subheader("⚡ Quick Insights")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('''
            <div class="metric-box">
                <div class="metric-value">85%</div>
                <div class="metric-label">Model Accuracy</div>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown('''
            <div class="metric-box">
                <div class="metric-value">500+</div>
                <div class="metric-label">Tech Jobs Added Monthly</div>
            </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown('''
            <div class="metric-box">
                <div class="metric-value">3x</div>
                <div class="metric-label">Higher Interview Success</div>
            </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown('''
            <div class="metric-box">
                <div class="metric-value">100%</div>
                <div class="metric-label">Personalized Feedback</div>
            </div>
        ''', unsafe_allow_html=True)

    st.divider()
    
    st.subheader("🎯 What You Can Do Here")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>🔮 Placement Predictor</h3>
            <p>Get instant placement predictions by filling in your academic performance, 
            technical skills, experience, and soft skills. Our SVM model will predict your 
            placement outcome with high accuracy.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Predict 🎓", width='stretch'):
            st.session_state.page = 'Predict'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>📊 EDA & Visualization</h3>
            <p>Explore comprehensive data analysis and visualization of student placement patterns. 
            View 15+ interactive charts showing correlations, distributions, trends, and key insights.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to EDA 📊", width='stretch'):
            st.session_state.page = 'EDA'
            st.rerun()

# ============================================
# PAGE: PREDICT
# ============================================
elif st.session_state.page == 'Predict':
    
    # Load model
    @st.cache_resource
    def load_model_artifacts():
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(base_dir, 'saved_models/best_model.pkl'), 'rb') as f:
                model = pickle.load(f)
            with open(os.path.join(base_dir, 'saved_models/scaler.pkl'), 'rb') as f:
                scaler = pickle.load(f)
            with open(os.path.join(base_dir, 'saved_models/feature_names.pkl'), 'rb') as f:
                feature_names = pickle.load(f)
            return model, scaler, feature_names
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            st.stop()
    
    model, scaler, feature_names = load_model_artifacts()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="header-text">🎓 PlacePredict</div>', unsafe_allow_html=True)
        st.markdown("**Predict your placement outcome using Machine Learning (SVM Model)**")
    with col2:
        st.info("🤖 Model: SVM\n📊 ROC-AUC: 0.833")
    
    st.divider()
    
    st.subheader("📚 Academic Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        default_cgpa = 7.0
        if st.session_state.logged_in and 'cgpa' in st.session_state.current_user:
            try:
                default_cgpa = float(st.session_state.current_user['cgpa'])
            except ValueError:
                pass
        
        cgpa = st.slider(
            "CGPA",
            min_value=1.0,
            max_value=10.0,
            value=default_cgpa,
            step=0.1,
            help="Your current CGPA"
        )
    
    with col2:
        tenth_percentage = st.selectbox(
            "10th Percentage",
            ["Below 70%", "70–80%", "80–90%", "Above 90%"],
            help="Your 10th board percentage"
        )
    
    with col3:
        twelfth_percentage = st.selectbox(
            "12th / Diploma Percentage",
            ["Below 70%", "70–80%", "80–90%", "Above 90%"],
            help="Your 12th board or diploma percentage"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        active_backlogs = st.selectbox(
            "Any Active Backlogs?",
            ["No", "Yes"],
            help="Do you have any active backlogs?"
        )
    
    with col2:
        willing_to_improve = st.selectbox(
            "Willing to Improve Skills Based on Feedback?",
            ["Yes", "No"],
            help="Are you willing to improve your skills?"
        )
    
    st.subheader("💻 Technical Skills & Experience")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        coding_skill = st.selectbox(
            "Coding Skill Level",
            ["Beginner", "Intermediate", "Advanced"],
            help="Your programming proficiency"
        )
    
    with col2:
        dsa_knowledge = st.selectbox(
            "Data Structures & Algorithms Knowledge",
            ["Basic", "Medium", "High"],
            help="Your DSA understanding level"
        )
    
    with col3:
        num_internships = st.slider(
            "Number of Internships Completed",
            min_value=0,
            max_value=5,
            value=1,
            step=1
        )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num_projects = st.slider(
            "Number of Academic/Personal Projects",
            min_value=0,
            max_value=10,
            value=1,
            step=1
        )
    
    with col2:
        hackathons = st.selectbox(
            "Hackathons / Coding Competitions Participated",
            ["No", "Yes"],
            help="Have you participated in hackathons?"
        )
    
    with col3:
        certifications = st.selectbox(
            "Technical Certifications Completed",
            ["No", "Yes"],
            help="Do you have any certifications?"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_languages = st.slider(
            "Number of Programming Languages Known",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            help="How many programming languages do you know?"
        )
    
    with col2:
        st.info("Popular: Python, Java, C++, JavaScript")
    
    st.subheader("🗣️ Soft Skills & Confidence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        communication_skills = st.slider(
            "Communication Skills (1-5)",
            min_value=1,
            max_value=5,
            value=3,
            step=1,
            help="Rate your communication skills (1=Poor, 5=Excellent)"
        )
    
    with col2:
        confidence_level = st.slider(
            "Confidence Level for Interviews (1-5)",
            min_value=1,
            max_value=5,
            value=3,
            step=1,
            help="Rate your interview confidence (1=Low, 5=High)"
        )
    
    logical_reasoning = st.selectbox(
        "Aptitude / Logical Reasoning Skill",
        ["Low", "Medium", "High"],
        help="Your logical reasoning ability"
    )
    
    # Preprocessing function
    def preprocess_input(data_dict):
        df = pd.DataFrame([data_dict])
        
        percentage_map = {
            "Below 70%": "Below 70%",
            "70–80%": "70–80%",
            "80–90%": "80–90%",
            "Above 90%": "Above 90%"
        }
        
        skill_map = {
            "Beginner": "Beginner",
            "Intermediate": "Intermediate",
            "Advanced": "Advanced"
        }
        
        dsa_map = {
            "Basic": "Basic",
            "Medium": "Medium",
            "High": "High"
        }
        
        reasoning_map = {
            "Low": "Low",
            "Medium": "Medium",
            "High": "High"
        }
        
        df["10th Percentage"] = df["10th Percentage"].map(percentage_map)
        df["12th / Diploma Percentage"] = df["12th / Diploma Percentage"].map(percentage_map)
        df["Coding Skill Level"] = df["Coding Skill Level"].map(skill_map)
        df["Data Structures & Algorithms Knowledge"] = df["Data Structures & Algorithms Knowledge"].map(dsa_map)
        df["Aptitude / Logical Reasoning Skill"] = df["Aptitude / Logical Reasoning Skill"].map(reasoning_map)
        
        df["Any Active Backlogs?"] = df["Any Active Backlogs?"].map({"No": 0, "Yes": 1})
        df["Hackathons / Coding Competitions Participated"] = df["Hackathons / Coding Competitions Participated"].map({"No": 0, "Yes": 1})
        df["Technical Certifications Completed"] = df["Technical Certifications Completed"].map({"No": 0, "Yes": 1})
        df["Willing to Improve Skills Based on Feedback?"] = df["Willing to Improve Skills Based on Feedback?"].map({"No": 0, "Yes": 1})
        
        df = pd.get_dummies(df, drop_first=True)
        
        for feature in feature_names:
            if feature not in df.columns:
                df[feature] = 0
        
        df = df[feature_names]
        df_scaled = scaler.transform(df)

        # Return numeric array (models were trained on numpy arrays)
        return df_scaled
    
    st.divider()
    
    if st.button("🔮 Predict Placement", width="stretch", key="predict_btn"):
        
        input_data = {
            "CGPA": cgpa,
            "10th Percentage": tenth_percentage,
            "12th / Diploma Percentage": twelfth_percentage,
            "Any Active Backlogs?": active_backlogs,
            "Coding Skill Level": coding_skill,
            "Data Structures & Algorithms Knowledge": dsa_knowledge,
            "Aptitude / Logical Reasoning Skill": logical_reasoning,
            "Number of Internships Completed": num_internships,
            "Number of Academic / Personal Projects": num_projects,
            "Hackathons / Coding Competitions Participated": hackathons,
            "Technical Certifications Completed": certifications,
            "Communication Skills": communication_skills,
            "Confidence Level for Interviews": confidence_level,
            "Programming Languages Known": num_languages,
            "Willing to Improve Skills Based on Feedback?": willing_to_improve
        }
        
        try:
            X_processed = preprocess_input(input_data)
            prediction = model.predict(X_processed)[0]
            prediction_proba = model.decision_function(X_processed)[0]
            confidence = abs(prediction_proba) / (abs(prediction_proba) + 1)
            
            st.divider()
            
            if prediction == 1:
                st.markdown(f"""
                    <div class="prediction-success">
                        <h3>✅ PREDICTION: PLACED</h3>
                        <p><b>Placement Probability: {confidence:.2%}</b></p>
                        <p>Based on the SVM model analysis, you have a {confidence:.2%} chance of getting placed.</p>
                    </div>
                """, unsafe_allow_html=True)
                st.success("🎉 Great news! Focus on maintaining your skills and confidence during interviews.")
            else:
                st.markdown(f"""
                    <div class="prediction-danger">
                        <h3>❌ PREDICTION: NOT PLACED</h3>
                        <p><b>Need to Improve: {(1-confidence):.2%}</b></p>
                        <p>Based on the SVM model analysis, you may need to work on specific areas.</p>
                    </div>
                """, unsafe_allow_html=True)
                st.warning("""
                📌 Recommendations to improve placement chances:
                - Focus on improving DSA and coding skills
                - Complete 1-2 real-world projects
                - Participate in hackathons/competitions
                - Enhance communication skills
                - Get relevant certifications
                - Build a strong portfolio
                - Practice mock interviews
                """)
            
            st.divider()
            
            with st.expander("📋 View Input Summary"):
                summary_df = pd.DataFrame([input_data]).T
                summary_df.columns = ["Value"]
                summary_df["Value"] = summary_df["Value"].astype(str)
                st.dataframe(summary_df, width='stretch')
                
            if st.session_state.logged_in:
                st.divider()
                email = st.session_state.current_user['email']
                success, msg = user_data_manager.save_prediction(email, input_data, prediction, confidence)
                if success:
                    st.success("✅ Prediction automatically saved! You can view your history in your User Profile.")
                else:
                    st.error("❌ " + msg)
            else:
                st.info("💡 Login to save your predictions and track your progress!")

            
        except Exception as e:
            st.error(f"❌ Prediction Error: {str(e)}")
            st.info("Please check if all fields are filled correctly and try again.")

# ============================================
# PAGE: EDA
# ============================================
elif st.session_state.page == 'EDA':
    
    st.markdown('<div class="header-text">📊 Exploratory Data Analysis & Preprocessing</div>', unsafe_allow_html=True)
    st.markdown("**Comprehensive analysis of student placement patterns and data preparation steps**")
    
    st.divider()

    st.subheader("🧹 Data Cleaning & Preprocessing Steps")
    st.markdown("""
    Before building our machine learning model and visualizing the data, we performed several essential 
    preprocessing steps on the Kaggle dataset to ensure data quality and model reliability.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="eda-step-card">
            <div class="eda-step-title">1. Handling Missing Values</div>
            <div class="eda-step-content">
                We identified and handled missing values in critical columns. For numerical features like CGPA, we used mean/median imputation. For categorical features, we used mode imputation or dropped records if the missing data was too substantial.
            </div>
        </div>
        <div class="eda-step-card">
            <div class="eda-step-title">2. Categorical Encoding</div>
            <div class="eda-step-content">
                Machine learning models require numerical input. We applied One-Hot Encoding (OHE) for nominal variables and Label/Ordinal Encoding for ordinal variables (like Skill Levels: Beginner, Intermediate, Advanced).
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="eda-step-card">
            <div class="eda-step-title">3. Feature Scaling</div>
            <div class="eda-step-content">
                Features like CGPA and Number of Internships exist on different scales. We applied StandardScaler to normalize these numerical features so that our Support Vector Machine (SVM) model could perform optimally without bias.
            </div>
        </div>
        <div class="eda-step-card">
            <div class="eda-step-title">4. Class Balancing (SMOTE)</div>
            <div class="eda-step-content">
                Our original dataset had an imbalance between Placed and Not Placed students. We used Synthetic Minority Over-sampling Technique (SMOTE) to generate synthetic examples for the minority class, ensuring a robust model.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    st.subheader("📈 Interactive Visualizations")
    
    @st.cache_data
    def load_data():
        try:
            df = pd.read_csv("../preprocessing_eda_kaggledata/students_cleaned_for_eda.csv")
            return df
        except:
            try:
                df = pd.read_csv("preprocessing_eda_kaggledata/students_cleaned_for_eda.csv")
                return df
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")
                st.stop()
    
    df_eda = load_data()
    
    st.info(f"📊 Dataset Shape: {df_eda.shape[0]} students × {df_eda.shape[1]} features")
    
    st.divider()
    
    # CHART 1
    st.subheader("1️⃣ Placement Status Distribution")
    st.markdown("""
    <div class="chart-description">
    📌 <b>Insight:</b> This bar chart shows the overall distribution of placed vs not placed students.
    It gives you a quick overview of placement success rate in the dataset.
    </div>
    """, unsafe_allow_html=True)
    
    placement_counts = df_eda['Placement Status'].value_counts()
    fig = px.bar(x=placement_counts.index, y=placement_counts.values, 
                 labels={'x': 'Placement Status', 'y': 'Count'},
                 title='Placement Status Distribution',
                 color=placement_counts.index,
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(showlegend=False, template='plotly_white', height=500, font=dict(size=12))
    st.plotly_chart(fig, width="stretch")
    
    # CHART 2
    st.subheader("2️⃣ Placed vs Not Placed Ratio")
    st.markdown("""
    <div class="chart-description">
    📌 <b>Insight:</b> Pie chart showing the percentage split between placed and not placed students.
    </div>
    """, unsafe_allow_html=True)
    
    placement_pie = df_eda['Placement Status'].value_counts()
    fig = px.pie(names=placement_pie.index, values=placement_pie.values,
                 title='Placed vs Not Placed Ratio',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(template='plotly_white', height=500, font=dict(size=12))
    st.plotly_chart(fig, width="stretch")
    
    # CHART 3
    st.subheader("3️⃣ Box Plot: Average GPA vs Placement Status")
    st.markdown("""
    <div class="chart-description">
    📌 <b>Insight:</b> Box plot comparing GPA distribution for placed vs not placed students.
    </div>
    """, unsafe_allow_html=True)
    
    fig = px.box(df_eda, x='Placement Status', y='Average GPA', 
                 title='Average GPA vs Placement Status',
                 color='Placement Status',
                 color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(template='plotly_white', height=500, font=dict(size=12))
    st.plotly_chart(fig, width="stretch")
    
    # CHART 4
    st.subheader("4️⃣ Violin Plot: GPA Distribution by Placement")
    st.markdown("""
    <div class="chart-description">
    📌 <b>Insight:</b> Detailed view of GPA distribution showing density and outliers.
    </div>
    """, unsafe_allow_html=True)
    
    fig = px.violin(df_eda, x='Placement Status', y='Average GPA',
                    title='GPA Trend Distribution by Placement',
                    color='Placement Status',
                    color_discrete_sequence=px.colors.qualitative.Set1,
                    box=True, points='outliers')
    fig.update_layout(template='plotly_white', height=500, font=dict(size=12))
    st.plotly_chart(fig, width="stretch")
    
    # CHART 5
    st.subheader("5️⃣ Histogram: Attendance Percentage Distribution")
    st.markdown("""
    <div class="chart-description">
    📌 <b>Insight:</b> Shows how attendance percentages are distributed across all students.
    </div>
    """, unsafe_allow_html=True)
    
    fig = px.histogram(df_eda, x='Attendance (%)', nbins=30,
                       title='Attendance Percentage Distribution',
                       color_discrete_sequence=['#FF6B6B'])
    fig.update_layout(template='plotly_white', height=500, font=dict(size=12),
                      xaxis_title='Attendance (%)', yaxis_title='Count')
    st.plotly_chart(fig, width="stretch")
    
    # CHART 6
    st.subheader("6️⃣ Scatter Plot: Average GPA vs Skill Count")
    st.markdown("""
    <div class="chart-description">
    📌 <b>Insight:</b> Shows relationship between academic performance and technical skills.
    </div>
    """, unsafe_allow_html=True)
    
    fig = px.scatter(df_eda, x='Average GPA', y='Skill_Count',
                     color='Placement Status',
                     title='Average GPA vs Skill Count',
                     color_discrete_sequence=px.colors.qualitative.Vivid,
                     size_max=10)
    fig.update_layout(template='plotly_white', height=500, font=dict(size=12))
    st.plotly_chart(fig, width="stretch")
    
    # CHART 7
    st.subheader("7️⃣ Bubble Chart: GPA vs Skills (Bubble Size = Attendance)")
    st.markdown("""
    <div class="chart-description">
    📌 <b>Insight:</b> 3D bubble chart showing GPA, Skill Count, and Attendance together.
    </div>
    """, unsafe_allow_html=True)
    
    fig = px.scatter(df_eda, x='Average GPA', y='Skill_Count', 
                     size='Attendance (%)', color='Placement Status',
                     title='GPA vs Skills (Bubble Size = Attendance)',
                     color_discrete_sequence=px.colors.qualitative.Plotly)
    fig.update_layout(template='plotly_white', height=500, font=dict(size=12))
    st.plotly_chart(fig, width="stretch")
    
    # CHART 8
    st.subheader("8️⃣ Stacked Bar Chart: Internship Status vs Placement")
    st.markdown("""
    <div class="chart-description">
    📌 <b>Insight:</b> Shows whether doing internships impacts placement success.
    </div>
    """, unsafe_allow_html=True)
    
    internship_placement = df_eda.groupby(['Internship Done', 'Placement Status']).size().reset_index(name='count')
    fig = px.bar(internship_placement, x='Internship Done', y='count', color='Placement Status',
                 title='Internship Status vs Placement Outcome',
                 color_discrete_sequence=px.colors.qualitative.Set2,
                 barmode='stack')
    fig.update_layout(template='plotly_white', height=500, font=dict(size=12))
    st.plotly_chart(fig, width="stretch")
    
    # CHART 9
    st.subheader("9️⃣ Sunburst Chart: Branch-wise Placement Distribution")
    st.markdown("""
    <div class="chart-description">
    📌 <b>Insight:</b> Hierarchical view showing placement distribution across engineering branches.
    </div>
    """, unsafe_allow_html=True)
    
    branch_placement = df_eda.groupby('Branch')['Placement Status'].value_counts().reset_index(name='count')
    fig = px.sunburst(branch_placement, 
                      path=['Branch', 'Placement Status'], 
                      values='count',
                      color='count', 
                      color_continuous_scale='Viridis',
                      title='Branch-wise Placement Distribution')
    fig.update_layout(template='plotly_white', height=600, font=dict(size=12))
    st.plotly_chart(fig, width="stretch")
    
    # CHART 10
    st.subheader("🔟 Treemap: Skill Count Contribution to Placement")
    st.markdown("""
    <div class="chart-description">
    📌 <b>Insight:</b> Treemap showing how different skill counts contribute to placement.
    </div>
    """, unsafe_allow_html=True)
    
    skill_placement = df_eda.groupby('Skill_Count')['Placement Status'].value_counts().reset_index(name='count')
    fig = px.treemap(skill_placement, 
                     path=['Skill_Count', 'Placement Status'], 
                     values='count',
                     color='count', 
                     color_continuous_scale='Plasma',
                     title='Skill Count Contribution to Placement')
    fig.update_layout(template='plotly_white', height=600, font=dict(size=12))
    st.plotly_chart(fig, width="stretch")
    
    # CHART 11
    st.subheader("1️⃣1️⃣ Heatmap: Feature Correlation Matrix")
    st.markdown("""
    <div class="chart-description">
    📌 <b>Insight:</b> Correlation matrix showing relationships between all numeric features.
    </div>
    """, unsafe_allow_html=True)
    
    numeric_cols_list = df_eda.select_dtypes(include=['int64', 'float64']).columns.tolist()
    corr_matrix = df_eda[numeric_cols_list].corr()
    fig = go.Figure(data=go.Heatmap(z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.columns,
                                    colorscale='RdBu'))
    fig.update_layout(title='Feature Correlation Matrix', template='plotly_white', height=600, font=dict(size=11))
    st.plotly_chart(fig, width="stretch")
    
    # CHART 12
    st.subheader("1️⃣2️⃣ Line Chart: Semester-wise Average GPA Trend")
    st.markdown("""
    <div class="chart-description">
    📌 <b>Insight:</b> Shows how average GPA changes across semesters.
    </div>
    """, unsafe_allow_html=True)
    
    semester_cols = [col for col in df_eda.columns if 'Sem' in col and 'GPA' in col]
    if semester_cols:
        semester_avg = df_eda[semester_cols].mean()
        semester_nums = [col.split()[0] for col in semester_cols]
        fig = px.line(x=semester_nums, y=semester_avg.values,
                      title='Semester-wise Average GPA Trend',
                      markers=True, color_discrete_sequence=['#FF6B6B'])
        fig.update_layout(xaxis_title='Semester', yaxis_title='Average GPA', template='plotly_white', height=500, font=dict(size=12))
        st.plotly_chart(fig, width="stretch")
    
    # CHART 13
    st.subheader("1️⃣3️⃣ Density Plot: GPA Distribution Density")
    st.markdown("""
    <div class="chart-description">
    📌 <b>Insight:</b> Smooth density curve showing the distribution of GPAs.
    </div>
    """, unsafe_allow_html=True)
    
    fig = px.histogram(df_eda, x='Average GPA', nbins=40, histnorm='density',
                       title='GPA Distribution Density',
                       color_discrete_sequence=['#4ECDC4'],
                       marginal='box')
    fig.update_layout(template='plotly_white', height=500, font=dict(size=12),
                      xaxis_title='Average GPA', yaxis_title='Density')
    st.plotly_chart(fig, width="stretch")
    
    # CHART 14
    st.subheader("1️⃣4️⃣ Funnel Chart: Student Journey to Placement")
    st.markdown("""
    <div class="chart-description">
    📌 <b>Insight:</b> Shows the conversion/attrition at each stage of the placement pipeline.
    </div>
    """, unsafe_allow_html=True)
    
    funnel_data = pd.DataFrame({
        'Stage': ['Total Students', 'High Attendance', 'Good GPA', 'With Skills', 'Placed'],
        'Count': [
            len(df_eda),
            len(df_eda[df_eda['Attendance (%)'] >= 75]),
            len(df_eda[df_eda['Average GPA'] >= 3.0]),
            len(df_eda[df_eda['Skill_Count'] >= 2]),
            len(df_eda[df_eda['Placement Status'] == 'Placed'])
        ]
    })
    fig = px.funnel(funnel_data, x='Count', y='Stage',
                    title='Student Journey to Placement',
                    color_discrete_sequence=['#FFD93D'])
    fig.update_layout(template='plotly_white', height=500, font=dict(size=12))
    st.plotly_chart(fig, width="stretch")
    
    # CHART 15
    st.subheader("1️⃣5️⃣ Radar Chart: Comparison of Placed vs Not Placed")
    st.markdown("""
    <div class="chart-description">
    📌 <b>Insight:</b> Multi-dimensional comparison showing average scores across key metrics.
    </div>
    """, unsafe_allow_html=True)
    
    placed = df_eda[df_eda['Placement Status'] == 'Placed']
    not_placed = df_eda[df_eda['Placement Status'] != 'Placed']
    
    categories = ['Average GPA', 'Skill Count', 'Attendance %', 'Club Count']
    placed_vals = [
        placed['Average GPA'].mean() / 4.0 * 100,
        placed['Skill_Count'].mean() / 10 * 100,
        placed['Attendance (%)'].mean(),
        placed['Club_Count'].mean() / 5 * 100
    ]
    not_placed_vals = [
        not_placed['Average GPA'].mean() / 4.0 * 100,
        not_placed['Skill_Count'].mean() / 10 * 100,
        not_placed['Attendance (%)'].mean(),
        not_placed['Club_Count'].mean() / 5 * 100
    ]
    
    fig = go.Figure(data=[
        go.Scatterpolar(r=placed_vals, theta=categories, fill='toself', name='Placed', line=dict(color='#00CC96')),
        go.Scatterpolar(r=not_placed_vals, theta=categories, fill='toself', name='Not Placed', line=dict(color='#EF553B'))
    ])
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                      title='Comparison of Placed vs Not Placed Profiles',
                      template='plotly_white', height=600, font=dict(size=12))
    st.plotly_chart(fig, width="stretch")
    
    st.divider()
    
    st.subheader("📊 Key Statistics Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(df_eda), "👥")
    
    with col2:
        placed_count = len(df_eda[df_eda['Placement Status'] == 'Placed'])
        placement_rate = (placed_count / len(df_eda)) * 100
        st.metric("Placement Rate", f"{placement_rate:.1f}%", "📈")
    
    with col3:
        avg_gpa = df_eda['Average GPA'].mean()
        st.metric("Avg GPA", f"{avg_gpa:.2f}/10", "🎓")
    
    with col4:
        avg_skills = df_eda['Skill_Count'].mean()
        st.metric("Avg Skills", f"{avg_skills:.1f}", "💻")

# ============================================
# PAGE: LOGIN
# ============================================
elif st.session_state.page == 'Login':
    
    st.markdown('<div class="header-text">🔑 Welcome Back</div>', unsafe_allow_html=True)
    st.markdown("**Log in to access your dashboard and track your placement predictions**")
    
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.subheader("Login to Your Account")
            
            email = st.text_input("Email Address", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            submitted = st.form_submit_button("🔑 Login", width="stretch")
            
            if submitted:
                if not email or not password:
                    st.error("❌ Please enter both email and password")
                else:
                    success, user_data = user_data_manager.authenticate_user(email, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.current_user = user_data
                        st.session_state.page = 'Dashboard'
                        st.success("✅ Login successful! Redirecting to Dashboard...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password")
                        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #475569;'>New to the platform?</p>", unsafe_allow_html=True)
        if st.button("📝 Create a New Account", width="stretch"):
            st.session_state.page = 'Sign Up'
            st.rerun()

# ============================================
# PAGE: SIGN UP
# ============================================
elif st.session_state.page == 'Sign Up':
    
    st.markdown('<div class="header-text">📝 Create Your Account</div>', unsafe_allow_html=True)
    st.markdown("**Join our placement prediction community and track your progress**")
    
    st.divider()
    
    with st.form("signup_form"):
        st.subheader("📋 Registration Form")
        
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name", placeholder="Enter your first name")
        
        with col2:
            last_name = st.text_input("Last Name", placeholder="Enter your last name")
        
        email = st.text_input("Email Address", placeholder="your.email@example.com")
        
        col1, col2 = st.columns(2)
        
        with col1:
            phone = st.text_input("Phone Number", placeholder="+91 XXXXXXXXXX")
        
        with col2:
            college = st.text_input("College/University", placeholder="Your institution name")
        
        branch = st.selectbox("Engineering Branch", 
                             ["CSE", "ECE", "MECH", "CIVIL", "EEE", "IT", "Other"])
        
        year = st.selectbox("Current Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
        
        cgpa = st.slider("Current CGPA", 1.0, 10.0, 7.0, 0.1)
        
        password = st.text_input("Create Password", type="password", placeholder="Minimum 8 characters")
        
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
        
        agree = st.checkbox("I agree to the Terms and Conditions")
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            submitted = st.form_submit_button("✅ Sign Up", width="stretch")
        
        if submitted:
            # Validation
            if not all([first_name, last_name, email, phone, college]):
                st.error("❌ Please fill in all required fields")
            elif len(password) < 8:
                st.error("❌ Password must be at least 8 characters long")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            elif not agree:
                st.error("❌ You must agree to the terms and conditions")
            else:
                success, msg = user_data_manager.create_user(
                    first_name, last_name, email, phone, college, branch, year, cgpa, password
                )
                if success:
                    st.success("✅ " + msg)
                    st.balloons()
                    st.info(f"""
                    **Welcome, {first_name} {last_name}!**
                    
                    Your account has been created. You can now login to:
                    - 🎓 Use the Placement Predictor to get predictions
                    - 📊 View detailed analytics and charts
                    - 💾 Save your prediction history
                    - 📈 Track your progress over time
                    """)
                else:
                    st.error("❌ " + msg)
                    
    st.markdown("<br>", unsafe_allow_html=True)
    switch_col1, switch_col2, switch_col3 = st.columns([1, 2, 1])
    with switch_col2:
        st.markdown("<p style='text-align: center; color: #475569;'>Already have an account?</p>", unsafe_allow_html=True)
        if st.button("🔑 Login to Your Account", width="stretch"):
            st.session_state.page = 'Login'
            st.rerun()
    
    st.divider()
    
    st.subheader("❓ Why Sign Up?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📊 Track Progress
        - Save all your predictions
        - Monitor improvement over time
        - Compare with other students
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Personalized Insights
        - Get tailored recommendations
        - Identify weak areas
        - Receive improvement suggestions
        """)
    
    with col3:
        st.markdown("""
        ### 🏆 Community Benefits
        - Connect with peers
        - Share success stories
        - Access exclusive resources
        """)

# ============================================
# PAGE: PROFILE
# ============================================
elif st.session_state.page == 'Dashboard':
    if not st.session_state.logged_in:
        st.warning("Please login to view your profile.")
        if st.button("Go to Login"):
            st.session_state.page = 'Login'
            st.rerun()
    else:
        user = st.session_state.current_user
        
        st.markdown(f'<div class="header-text">👤 Welcome, {user["first_name"]}!</div>', unsafe_allow_html=True)
        st.markdown("**Your Personal Placement Dashboard**")
        
        st.divider()
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("""
            <div class="feature-box" style="margin-top: 0;">
                <h3>📋 Profile Details</h3>
            </div>
            """, unsafe_allow_html=True)
            st.write(f"**Name:** {user['first_name']} {user['last_name']}")
            st.write(f"**Email:** {user['email']}")
            st.write(f"**College:** {user['college']}")
            st.write(f"**Branch:** {user['branch']}")
            st.write(f"**Year:** {user['year']}")
            st.write(f"**Current CGPA:** {user['cgpa']}")
            
            if st.button("Edit Profile (Coming Soon)"):
                st.info("Profile editing will be available in the next update!")
                
        with col2:
            st.markdown("""
            <div class="feature-box" style="margin-top: 0; background: linear-gradient(135deg, #1f77b4 0%, #00d2ff 100%);">
                <h3>📈 Prediction History</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Reload user data to get fresh predictions
            users = user_data_manager.load_users()
            current_user_latest = users.get(user['email'], {})
            predictions = current_user_latest.get('predictions', [])
            
            if not predictions:
                st.info("You haven't made any predictions yet. Go to the Predict page to get started!")
                if st.button("Go to Predict"):
                    st.session_state.page = 'Predict'
                    st.rerun()
            else:
                # Show predictions in a table
                df_preds = pd.DataFrame(predictions)
                df_preds['confidence'] = (df_preds['confidence'] * 100).round(2).astype(str) + '%'
                df_preds['prediction'] = df_preds['prediction'].map({1: 'Placed ✅', 0: 'Not Placed ❌'})
                
                # Format the table a bit nicely
                st.dataframe(
                    df_preds[['timestamp', 'prediction', 'confidence']],
                    column_config={
                        "timestamp": "Date & Time",
                        "prediction": "Result",
                        "confidence": "Probability"
                    },
                    hide_index=True,
                    width='stretch'
                )
                
                if len(predictions) > 1:
                    st.subheader("Your Progress Over Time")
                    
                    # Create a line chart for confidence
                    df_chart = pd.DataFrame(predictions)
                    df_chart['timestamp'] = pd.to_datetime(df_chart['timestamp'])
                    df_chart['confidence_pct'] = df_chart['confidence'] * 100
                    
                    fig = px.line(
                        df_chart, 
                        x='timestamp', 
                        y='confidence_pct',
                        markers=True,
                        title='Placement Probability Trend',
                        labels={'timestamp': 'Date', 'confidence_pct': 'Probability (%)'}
                    )
                    fig.update_layout(template='plotly_white')
                    fig.update_traces(line_color='#00d2ff', marker=dict(size=10, color='#1f77b4'))
                    st.plotly_chart(fig, width='stretch')


# ============================================
# FOOTER
# ============================================
st.divider()
st.markdown("""
    <div style="text-align: center; color: #475569; font-size: 0.85rem; padding: 2rem;">
        <p>🔬 Powered by Machine Learning (SVM) | ROC-AUC: 0.833</p>
        <p>📊 PlacePredict | Built with Streamlit</p>
        <p>© 2026 All Rights Reserved | Privacy Policy | Terms of Service</p>
    </div>
""", unsafe_allow_html=True)
