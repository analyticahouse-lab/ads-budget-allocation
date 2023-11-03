import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('sample_data/test.csv')

# Clean the 'Conv. rate' column by removing the percentage sign (%) and converting to float
df['Conv. rate'] = df['Conv. rate'].str.rstrip('%').astype(float) / 100

hourly_performance = df.groupby(['Hour of the day', 'Campaign']).agg({
    'Conv. rate': 'mean',
    'Clicks': 'mean',
    'Cost': 'mean'
}).reset_index()

hourly_performance = hourly_performance.sort_values(by='Conv. rate', ascending=False)

budget_recommendation = {}
for index, row in hourly_performance.iterrows():
    hour = row['Hour of the day']
    campaign_name = row['Campaign']
    conversion_rate = row['Conv. rate']
    if conversion_rate < 0.05:
        budget_recommendation[hour] = {
            'Recommendation': "Pause",
            'Value': f"Potential Cost Saving: ${row['Cost']:.2f}",
        }
    elif conversion_rate > 0.10:
        budget_recommendation[hour] = {
            'Recommendation': "Increase",
            'Value': f"Potential Conversion Rate: {conversion_rate:.2%}",
        }

plt.figure(figsize=(12, 6))
bar_plot = plt.bar(hourly_performance['Hour of the day'], hourly_performance['Conv. rate'], color='blue')
plt.xlabel('Hour of the Day')
plt.ylabel('Conversion Rate')
plt.title('Hourly Performance')
plt.xticks(rotation=45)
plt.tight_layout()

for hour, recommendation in budget_recommendation.items():
    x = hour
    y = 0
    text = f"{recommendation['Recommendation']}\n{recommendation['Value']}"
    plt.text(x, y, text, fontsize=9, ha='center', va='top', rotation=90, color='red')

plt.show()
