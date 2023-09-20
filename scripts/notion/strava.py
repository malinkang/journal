import datetime
import stravalib

client_id = "67037"
client_secret = "9ea364fa0db767d52770b3a3deaf0f5e1ceafb51"
refresh_token = "6145d313d69e93ba801fd6754ad1363157f72972"

client = stravalib.Client()
response= client.refresh_access_token(
    client_id=client_id,
    client_secret=client_secret,
    refresh_token=refresh_token,
)
print(response)
filters = {"before": datetime.datetime.utcnow()}
activities = client.get_activities(**filters)
for activity in activities:
    print(activity)
    print(activity.id)
    print(activity.athlete)
    print(activity.type)
    print(activity.start_date)
    print(activity.start_date_local)
    print(activity.distance)
    print(activity.moving_time)
    print(activity.elapsed_time)
    print(activity.timezone)
    print(activity.location_city)
    break
