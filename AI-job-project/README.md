🤖 AI Career Intelligence Platform
AI Job Market Analysis & Salary Prediction System

A Machine Learning-powered Career Intelligence Platform that analyzes global AI job market trends, predicts salaries, explores country-wise opportunities, and provides structured career roadmaps for aspiring AI professionals.

📌 Project Overview

The AI industry is rapidly growing, creating thousands of new job opportunities worldwide.

This project helps students, job seekers, and professionals understand:

Current AI job market trends
Salary expectations
Skill demand across industries
Country-wise salary comparisons
Career growth opportunities
Learning roadmaps for AI careers

The platform combines Data Analytics, Machine Learning, and Interactive Dashboards into a single solution.

🎯 Project Objectives

The main objectives of this project are:

1. AI Job Market Analysis

Analyze global AI job data to identify:

High-paying roles
Popular AI specializations
Hiring trends
Work mode preferences
Experience-based salary growth
2. Salary Prediction

Predict AI salaries using Machine Learning based on:

Country
Job Role
Experience Level
Education
Industry
Company Size
Skill Demand
Career Growth
3. Career Roadmaps

Provide structured learning paths for:

Data Scientist
Machine Learning Engineer
NLP Engineer
Computer Vision Engineer
AI Research Scientist
Data Analyst
4. Career Intelligence Dashboard

Deliver data-driven career guidance through an interactive dashboard.

🧠 Machine Learning Model
Target Variable
salary_usd
Algorithm Used
Random Forest Regressor
Why Random Forest?

Random Forest was selected because it:

Handles categorical and numerical data effectively
Reduces overfitting
Provides high prediction accuracy
Performs well on large datasets
Model Performance
Metric	Value
R² Score	0.9217
Accuracy	92.17%
Model	Random Forest Regressor
📊 Dataset Information
Dataset Size
90,000 Records
35 Features
Dataset File
data/global_ai_jobs.csv
Important Features
Feature
country
job_role
ai_specialization
experience_level
experience_years
salary_usd
education_required
industry
company_size
work_mode
skill_demand_score
career_growth_score
🚀 Platform Features
🏠 Home Dashboard

Provides:

Market Overview
Key Statistics
Platform Introduction
Navigation Dashboard
📈 Market Analysis

Analyze:

Top Paying AI Roles
Salary Distribution
Experience vs Salary
Country Salary Analysis
AI Specialization Trends
Education Impact
Company Size Analysis
💰 Salary Predictor

Predict salaries based on:

Country
Job Role
AI Specialization
Experience
Education
Industry
Company Size
Work Mode

Outputs:

Predicted Salary
Salary Range
Model Confidence
Market Comparison
🛣️ Career Roadmaps

Provides:

Learning Timeline

Step-by-step learning plans.

Career Snapshot

Displays:

Growth Score
Skill Demand
Average Salary
Job Opportunities
Job Strategy

Guidance for:

Building Portfolio
Internship Preparation
Interview Readiness
🌍 Country Analysis

Analyze:

Highest Paying Countries
Salary Comparison
Job Openings
AI Adoption Rates
Cost of Living Impact
🛠 Technologies Used
Frontend
Streamlit
Data Analysis
Pandas
NumPy
Visualization
Plotly
Streamlit Charts
Machine Learning
Scikit-Learn
Random Forest Regressor
Model Storage
Joblib
📂 Project Structure
AI_JOB_MARKET_PROJECT/

│
├── assets/
│   └── style.css
│
├── data/
│   ├── global_ai_jobs.csv
│   └── roadmaps.csv
│
├── models/
│   ├── salary_model.pkl
│   └── label_encoders.pkl
│
├── pages/
│   ├── Market_Analysis.py
│   ├── Salary_Predictor.py
│   └── Career_Roadmaps.py
│
├── app.py
├── train_model.py
├── requirements.txt
└── README.md

⚙️ Installation

Clone Repository
git clone https://github.com/your-username/AI-Career-Intelligence-Platform.git

cd AI-Career-Intelligence-Platform

Install Dependencies

pip install -r requirements.txt

Run Application

streamlit run app.py

📈 Results
Key Findings

✅ AI Engineer and Research Scientist roles offer the highest salaries.

✅ Salary increases significantly with experience.

✅ Countries with higher AI adoption rates generally offer higher salaries.

✅ Skill demand strongly influences salary growth.

✅ Remote and Hybrid work modes remain highly popular.

🎓 Academic Contribution

This project demonstrates practical implementation of:

Data Science
Machine Learning
Data Visualization
Predictive Analytics
Career Recommendation Systems

It serves as a real-world application of AI-driven career intelligence