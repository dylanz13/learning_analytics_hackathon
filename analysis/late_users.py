import pandas as pd

def classify_night_owl(df, threshold):    
    """Returns list of users who are active late
    param df: Pandas dataframe from https://canvas.instructure.com/doc/api/file.data_service_caliper_navigation_events.html, assumed to be cleaned
    param threashold: threashold which is the fraction of "late" usage to classify an individual as a late owl
    return: String array of night owl users
    """
    
     # Define later hours (20 to 24 and 0 to 5)
    later_hours = list(range(0, 6)) + list(range(20, 25))
    
    # Define non-class hours (before 9 AM and after 4 PM)
    non_class_hours = list(range(0, 10)) + list(range(16, 25))
    
    # Filter out class hours to focus on natural habits
    df_non_class = df[df['hour'].isin(non_class_hours)]
    
    # Calculate total events per user outside class hours
    total_events_per_user = df_non_class.groupby('actor_id').size().reset_index(name='total_events')

    # Calculate events during later hours outside class hours
    later_events_per_user = df_non_class[df_non_class['hour'].isin(later_hours)].groupby('actor_id').size().reset_index(name='later_events')

    # Merge the two DataFrames
    user_activity = pd.merge(total_events_per_user, later_events_per_user, on='actor_id', how='left').fillna(0)
    

    # Calculate each user's contribution to the overall later hour events outside class hours
    user_activity['later_contribution'] = user_activity['later_events'] / user_activity['total_events']
    
    # Set the threshold for "active later"
    user_activity['active_later'] = user_activity['later_contribution'] > threshold

    # Get the list of actor_ids that are active later
    active_later_ids = user_activity[user_activity['active_later']]['actor_id'].tolist()

    return active_later_ids