# 🔍 DATA RESCUE – Data Quality Detective

A Python-powered desktop application that analyzes CSV datasets, detects data quality issues, identifies statistical outliers, and helps clean messy data through an interactive graphical interface.

**DATA RESCUE** is designed to make data cleaning easier by providing a visual dashboard for identifying missing values, duplicate records, invalid emails, incorrect dates, negative values, and potential outliers.

## 🚀 Features

- 📂 **CSV File Import** – Load your own CSV datasets.
- 🧪 **Built-in Sample Dataset** – Test the application without uploading a file.
- 📊 **Data Quality Dashboard** – View records, columns, missing cells, duplicates and quality score.
- 🔎 **Missing Value Detection** – Identify missing values across dataset columns.
- 🔁 **Duplicate Detection** – Find exact duplicate records.
- 📧 **Email Validation** – Detect invalid email formats.
- 📅 **Date Validation** – Identify incorrectly formatted dates.
- ⚠️ **Negative Value Detection** – Flag negative values in common numeric fields.
- 📈 **Outlier Detection** – Identify potential statistical outliers using the IQR method.
- 🧹 **Data Cleaning** – Trim whitespace, standardize selected fields and remove exact duplicate rows.
- 📤 **Export Cleaned CSV** – Save the cleaned dataset.
- 📄 **HTML Report Generation** – Generate a detailed data quality report.
- 🎨 **Modern GUI** – Dark-themed desktop interface with multiple analysis tabs.

## 🛠 Technologies Used

- Python 3
- Tkinter – Graphical User Interface
- CSV – Dataset handling
- Statistics – Statistical calculations
- HTML – Report generation
- Regular Expressions – Email validation
- Collections – Data analysis
- Math – Numeric processing

## 📂 Project Structure

```text
data-quality-rescue-tool/
│
├── data_rescue.py
└── README.md
```

## ⚙️ Installation

### 1. Install Python

Install Python 3.x from:

https://www.python.org/downloads/

Make sure Python is added to PATH during installation.

### 2. Clone the Repository

```bash
git clone https://github.com/ravigautam7739/data-quality-rescue-tool.git
```

### 3. Navigate to the Project Folder

```bash
cd data-quality-rescue-tool
```

### 4. Run the Application

```bash
python data_rescue.py
```

**No external Python packages are required.** The application uses Python's built-in libraries, including Tkinter.

## 🖥️ Application Modules

### 1. Overview Dashboard
Displays important dataset metrics and a detailed data quality summary.

### 2. Flagged Records
Shows records containing:
- Invalid email addresses
- Invalid date values
- Negative numeric values

### 3. Outlier Detection
Identifies potential outliers in numeric columns using the Interquartile Range (IQR) method.

### 4. Raw Dataset
Displays the imported dataset in a structured table.

### 5. Data Cleaning
Provides functionality to:
- Remove unnecessary whitespace
- Standardize email formatting
- Normalize selected text categories
- Remove exact duplicate rows

### 6. Export Options
- Export cleaned data as CSV.
- Generate a downloadable HTML quality report.

## 🧠 How It Works

1. Launch the application.
2. Load the built-in sample dataset or import your own CSV file.
3. The application analyzes the dataset.
4. Review the quality score and identified issues.
5. Explore flagged records and potential outliers.
6. Export the cleaned dataset.
7. Generate an HTML report for documentation.

## 📊 Data Quality Analysis

The application evaluates:

| Quality Check | Description |
|---|---|
| Missing Values | Identifies blank cells |
| Duplicate Records | Detects exact duplicate rows |
| Email Validation | Checks email format |
| Date Validation | Checks supported date formats |
| Negative Values | Flags negative values in selected fields |
| Outlier Detection | Uses IQR statistical analysis |
| Quality Score | Calculates an overall quality indicator |

**Note:** Outliers are statistical flags and are not necessarily incorrect values.

## 🎯 Use Cases

- Data preprocessing
- Exploratory data analysis
- CSV data cleaning
- Data quality auditing
- Business reporting
- Data analytics learning
- Preparing datasets for machine learning

## ⚠️ Important Notes

- Supports CSV files.
- The application does not modify your original CSV file.
- Cleaning and export operations generate a separate cleaned CSV.
- Outlier detection uses the IQR method.
- The quality score is an application-defined indicator, not a universal data quality standard.
- Large datasets may require additional processing time.

## 🔮 Future Improvements

- Missing value imputation
- Advanced anomaly detection
- Interactive data visualizations
- Excel file support
- Automated column type detection
- Machine learning-based data validation
- Additional export formats
- Advanced data profiling

## 👨‍💻 Author

**Ravi Gautam**

GitHub: https://github.com/ravigautam7739

## ⭐ Support

If you find this project useful, consider giving this repository a ⭐ star.

Follow for more Python, Data Science, AI, Automation and Computer Vision projects!

---

*Built with Python to make data cleaning smarter and easier.*
