import pm4py, json
import pandas as pd
from datetime import datetime

df = pd.read_csv("temp/event_log.csv")

log = pm4py.format_dataframe(df, case_id='case_id', activity_key='event_label', timestamp_key='start_time')

variants = pm4py.get_variants(log)
total = sum(variants.values())
variant_probs = {str(v): cnt/total for v,cnt in variants.items()}

activities = df['event_label'].unique()
print("Activities found:", activities)

mean_sec = {}
std_sec = {}

for activity in activities:
    activity_rows = df[df['event_label'] == activity].copy()
    if len(activity_rows) > 0:
        activity_rows['start_time'] = pd.to_datetime(activity_rows['start_time'])
        activity_rows['completion_time'] = pd.to_datetime(activity_rows['completion_time'])
        durations = (activity_rows['completion_time'] - activity_rows['start_time']).dt.total_seconds()
        mean_sec[activity] = float(durations.mean()) if not durations.isna().all() else 3600
        std_sec[activity] = float(durations.std()) if not durations.isna().all() else 1800
        
        print(f"Activity {activity}: mean={mean_sec[activity]:.0f}s, std={std_sec[activity]:.0f}s")

with open("pm_params.json","w") as f:
    json.dump({
      "variant_probs": variant_probs,
      "mean_sec": mean_sec,
      "std_sec": std_sec
    }, f, indent=2)
print("pm_params.json written")