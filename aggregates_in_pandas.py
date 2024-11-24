import pandas as pd
import matplotlib.pyplot as plt

# Read the data
ad_clicks = pd.read_csv('ad_clicks.csv')

# 1. Examine first few rows
print(ad_clicks.head())

# 2. Count views by source
views_by_source = ad_clicks.groupby('utm_source').user_id.count()
print(views_by_source)

# 3. Create is_click column
ad_clicks['is_click'] = ~ad_clicks.ad_click_timestamp.isnull()

# 4. Group by source and is_click
clicks_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index()

# 5. Pivot the data
clicks_pivot = clicks_by_source.pivot(index='utm_source', columns='is_click', values='user_id').reset_index()
clicks_pivot.columns = ['utm_source', 'no_click', 'click']

# 6. Calculate click-through rate
clicks_pivot['percent_clicked'] = clicks_pivot['click'] / (clicks_pivot['click'] + clicks_pivot['no_click']) * 100
print(clicks_pivot)

# 7. Compare number of users in each experimental group
exp_group_counts = ad_clicks.groupby('experimental_group').user_id.count()
print(exp_group_counts)

# 8. Compare click rates between groups
group_clicks = ad_clicks.groupby(['experimental_group', 'is_click']).user_id.count().reset_index()
group_clicks_pivot = group_clicks.pivot(index='experimental_group', columns='is_click', values='user_id').reset_index()
group_clicks_pivot.columns = ['experimental_group', 'no_click', 'click']
group_clicks_pivot['percent_clicked'] = group_clicks_pivot['click'] / (group_clicks_pivot['click'] + group_clicks_pivot['no_click']) * 100
print(group_clicks_pivot)

# 9. Split into A and B groups
a_clicks = ad_clicks[ad_clicks.experimental_group == 'A']
b_clicks = ad_clicks[ad_clicks.experimental_group == 'B']

# 10 & 11. Calculate and compare daily click rates
def get_daily_clicks(data):
    daily_clicks = data.groupby(['day', 'is_click']).user_id.count().reset_index()
    daily_pivot = daily_clicks.pivot(index='day', columns='is_click', values='user_id').reset_index()
    daily_pivot.columns = ['day', 'no_click', 'click']
    daily_pivot['percent_clicked'] = daily_pivot['click'] / (daily_pivot['click'] + daily_pivot['no_click']) * 100
    return daily_pivot

a_daily_clicks = get_daily_clicks


plt.figure(figsize=(10, 6))
plt.plot(a_daily_clicks.index, a_daily_clicks['percent_clicked'], label='Ad A', marker='o')
plt.plot(b_daily_clicks.index, b_daily_clicks['percent_clicked'], label='Ad B', marker='o')
plt.title('Daily Click-through Rates: Ad A vs Ad B')
plt.xlabel('Day of Week')
plt.ylabel('Click-through Rate (%)')
plt.legend()
plt.grid(True)