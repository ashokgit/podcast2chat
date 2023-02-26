from googleapiclient.discovery import build
import json

# Set up the API client
api_key = 'AIzaSyDA34ktENe_yO0nbXKq-ixrUYRNPOEeyv4'
youtube = build('youtube', 'v3', developerKey=api_key)

# Make a request to the API
channel_id = 'UC2D2CMWXMOVWx7giW1n3LIg'
folder = './data/AndrewHuberMan/'

# Request the channel's about information
channel_response = youtube.channels().list(
    part='snippet',
    id=channel_id
).execute()

# Extract the channel's about information
channel_about = channel_response['items'][0]['snippet']['description']

request = youtube.search().list(
    part='snippet',
    channelId=channel_id,
    type='video',
    videoDuration='long',
    maxResults=500
)
response = request.execute()

# Parse the response
videos = []
for item in response['items']:
    video_id = item['id']['videoId']
    video_title = item['snippet']['title']
    video_description = item['snippet']['description']
    videos.append({'id': video_id,
                   'title': video_title,
                   'description': video_description})

# Output the video data
print(json.dumps(videos, indent=2))

with open(folder+'about.txt', 'w') as f:
    f.write('Channel About:\n{}\n\n'.format(channel_about))
# Write the video data to a text file
with open(folder+'videos.txt', 'w') as f:
    json.dump(videos, f, indent=2)
