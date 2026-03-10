# Blood Glucose Analytics System — Diet, Activity, and Glycemic Response Analysis

This project analyzes continuous glucose monitoring (CGM) data together with dietary and activity records to understand how different foods and behaviors influence blood glucose levels.

The goal of the system is to transform messy real-world health data into structured insights that help identify glucose spikes, dietary patterns, and potential metabolic risks.

---

## Overview

Blood glucose levels are influenced by many factors including food intake, physical activity, and metabolic responses. However, analyzing these relationships is difficult because the data typically comes from multiple inconsistent sources.

This project builds an end-to-end analytics pipeline that integrates:

- Continuous Glucose Monitoring (CGM) sensor data
- Unstructured food diary records
- Activity and behavioral data

The system processes these datasets, aligns them temporally, detects glucose spikes, and generates interpretable insights about dietary impact on glucose levels.

---

## Data Sources

The project works with multiple types of real-world health data.

### Continuous Glucose Monitoring (CGM) Data
Time-series glucose readings collected from CGM sensors.

Typical attributes include:

- Timestamp
- Blood glucose level (mg/dL)
- Sensor metadata

These readings typically occur every **5–15 minutes**, producing dense time-series data.

---

### Food Diary Records

Participants recorded their food consumption in various formats, including:

- Word documents
- Excel spreadsheets
- PDFs
- Manual logs

Food records contained information such as:

- Meal time
- Food name
- Portion descriptions
- Notes about ingredients or preparation

Because these records were unstructured, extensive preprocessing was required.

---

### Activity Data

Additional contextual data included:

- Physical activity
- Exercise sessions
- Daily routines

These variables were used to understand how activity influences glucose behavior.

---

## Key Challenges

Working with real-world health data introduced several technical challenges:

- Inconsistent file formats across participants
- Missing or incomplete records
- Non-standard column headers
- Irregular timestamps
- Unstructured food descriptions

The project focused heavily on building **robust preprocessing and normalization pipelines** to handle these issues.

---

## System Architecture

The pipeline processes data through several stages.

Data Ingestion  
↓  
Data Cleaning and Normalization  
↓  
Temporal Alignment of CGM and Food Records  
↓  
Glucose Spike Detection  
↓  
Dietary Pattern Analysis  
↓  
Visualization and Insight Generation

---

## Key Features

### Data Integration

Merged time-series CGM data with unstructured food diaries and activity logs to create a unified analytical dataset.

---

### Data Preprocessing

Implemented preprocessing pipelines to handle inconsistent data formats using techniques such as:

- Dynamic header detection
- Regex-based parsing
- Timestamp normalization
- Missing value handling

---

### Temporal Alignment

Aligned food intake records with glucose measurements using sliding time windows to identify potential cause-and-effect relationships.

---

### Glucose Spike Detection

Developed spike detection algorithms using threshold-based and window-based analysis to identify significant glucose excursions.

Metrics analyzed include:

- Peak glucose levels
- Duration of elevated glucose
- Rate of glucose increase

---

### Dietary Impact Analysis

Classified foods into categories based on their observed glycemic response.

The system identifies:

- High-risk foods associated with glucose spikes
- Low-impact foods with stable glucose responses
- Individual variability across participants

---

### Visualization

Generated visualizations to help interpret patterns in glucose responses over time.

Examples include:

- Glucose time-series plots
- Spike frequency charts
- Food-to-glucose correlation plots

---

## Tech Stack

Programming Language  
Python

Data Processing  
Pandas  
NumPy  

Data Analysis  
Time-series analysis  
Statistical modeling

Text Processing  
Regular expressions (regex)

Visualization  
Matplotlib

Data Sources  
Continuous Glucose Monitoring (CGM) datasets  
Unstructured food diary records

---

## Example Insights Generated

Examples of insights the system can identify include:

- Foods frequently associated with glucose spikes
- Time-of-day patterns in glycemic response
- Individual differences in metabolic responses
- Relationships between physical activity and glucose stability

---

## Why This Project Matters

Understanding glycemic responses is critical for managing diabetes, metabolic health, and personalized nutrition.

This project demonstrates how data engineering and analytics techniques can transform messy real-world health data into interpretable insights that support evidence-based health decisions.

---

## Repository Structure


