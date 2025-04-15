import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Sample data for the Student Profile Management System
students = [
    {'name': 'Caron', 'semester': 'Sem1', 'grade': 75, 'avg_grade': 76.5, 'eca_hours': 2},
    {'name': 'Nikesh', 'semester': 'Sem1', 'grade': 60, 'avg_grade': 82.5, 'eca_hours': 30},
    {'name': 'Kriti', 'semester': 'Sem1', 'grade': 85, 'avg_grade': 62.5, 'eca_hours': 5},
    {'name': 'Raish', 'semester': 'Sem2', 'grade': 78, 'avg_grade': 55, 'eca_hours': 40},
    {'name': 'Anush', 'semester': 'Sem2', 'grade': 65, 'avg_grade': None, 'eca_hours': None},
    {'name': 'Samyam', 'semester': 'Sem2', 'grade': 80, 'avg_grade': None, 'eca_hours': None},
]

# Convert to DataFrame
students_df = pd.DataFrame(students)

def display_student_overview(df):
    print("🎓 Student Profiles Summary:")
    print(df[['name', 'semester', 'grade', 'avg_grade', 'eca_hours']])

def plot_grade_trends(df):
    print("\n📊 Grade Trends by Semester:")
    grade_trend_df = df.pivot(index='semester', columns='name', values='grade')
    grade_trend_df.plot(marker='o', title="Grade Trends Over Semesters")
    plt.xlabel("Semester")
    plt.ylabel("Grade")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_eca_vs_grade(df):
    print("\n⚖️ ECA Hours vs Academic Performance:")

    eca_df = df.dropna(subset=['avg_grade', 'eca_hours'])

    colors = plt.cm.tab10.colors
    student_colors = dict(zip(eca_df['name'], colors))

    plt.figure(figsize=(8, 6))
    for _, row in eca_df.iterrows():
        plt.scatter(row['eca_hours'], row['avg_grade'],
                    color=student_colors[row['name']],
                    label=row['name'],
                    s=100)

    # Remove duplicate labels
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    # Regression line
    m, b = np.polyfit(eca_df['eca_hours'], eca_df['avg_grade'], 1)
    plt.plot(eca_df['eca_hours'], m * eca_df['eca_hours'] + b, color='black', linestyle='--', label='Trend Line')

    plt.title("ECA Involvement vs Average Grade")
    plt.xlabel("ECA Hours")
    plt.ylabel("Average Grade")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    correlation = eca_df['eca_hours'].corr(eca_df['avg_grade'])
    print(f"📈 Correlation between ECA hours and academic performance: {correlation:.2f}")

def check_performance_alerts(df, threshold=60):
    print("\n🚨 Performance Alerts:")
    alert_df = df[df['avg_grade'].fillna(100) < threshold]
    
    if not alert_df.empty:
        print("⚠️ Students below performance threshold:")
        for _, row in alert_df.iterrows():
            print(f"🔔 Recommend support for {row['name']} (Avg Grade: {row['avg_grade']})")
    else:
        print("✅ All students meet the performance standards.")

def admin_analytics_dashboard():
    print("📘 Student Profile Management Dashboard")
    display_student_overview(students_df)
    plot_grade_trends(students_df)
    plot_eca_vs_grade(students_df)
    check_performance_alerts(students_df)

# Run the Dashboard
admin_analytics_dashboard()