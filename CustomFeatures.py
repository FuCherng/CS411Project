#----------------------------------------#
# Function that computes custom features #
#----------------------------------------#
def CalculateFeatures(VideoEvents=[], ForumEvents=[]):

    # Initialize features dict
    Features = {}

    # Features for video events
    if len(VideoEvents)>0:
        # Calculate custom features
        #  Keys: TimeStamp, EventType, VideoID, CurrentTime, OldTime, NewTime, SeekType, OldSpeed, NewSpeed
        TimeStamps = VideoEvents['TimeStamp']
        TimeStampDiffs = [x[0]-x[1] for x in zip(TimeStamps[1:],TimeStamps[:-1])]
        DurationOfVideoActivity = TimeStamps[-1] - TimeStamps[0]
        AverageVideoTimeDiffs = sum(TimeStampDiffs)/max(1,len(TimeStampDiffs))
        EventTypes = VideoEvents['EventType']
        NumberOfVideoSeek = EventTypes.count('Video.Seek')
        NumberOfVideoLoad = EventTypes.count('Video.Load')
        NumberOfVideoPlay = EventTypes.count('Video.Play')
        NumberOfVideoDownload = EventTypes.count('Video.Download')
        NumberOfVideoPauseSeek = EventTypes.count('Video.Pause') + EventTypes.count('Video.Seek')
        NumberOfVideoSpeedChange = EventTypes.count('Video.SpeedChange')

        # Append features to dictionary
        Features.update({
            'DurationOfVideoActivity' : DurationOfVideoActivity,
            'AverageVideoTimeDiffs' : AverageVideoTimeDiffs,
            'NumberOfVideoSeek' : NumberOfVideoSeek,
            'NumberOfVideoLoad' : NumberOfVideoLoad,
            'NumberOfVideoPlay' : NumberOfVideoPlay,
            'NumberOfVideoDownload' : NumberOfVideoDownload,
            'NumberOfVideoPauseSeek' : NumberOfVideoPauseSeek,
            'NumberOfVideoSpeedChange' : NumberOfVideoSpeedChange
        })

    # Features for forum events
    if len(ForumEvents)>0:
        # Calculate custom features
        # Keys: TimeStamp, EventType, PostType, PostID, PostLength
        EventTypes = ForumEvents['EventType']
        NumberOfThreadViews = EventTypes.count('Forum.Thread.View')
        NumberOfPostsEvent = EventTypes.count('Forum.Thread.PostOn') + EventTypes.count('Forum.Post.Upvote') + EventTypes.count('Forum.Post.Downvote')
        NumberOfSubscribe = EventTypes.count('Forum.Subscribe') + EventTypes.count('Forum.ThreadSubscribe')
        NumberOfLaunch = EventTypes.count('Forum.Thread.Launch')

        # Postlength = 0
        # for i in ForumEvents['PostLength']:
        #     if i != "None":
        #         Postlength += i

        NumberOfComments = EventTypes.count('Forum.Comment.Upvote') + EventTypes.count('Forum.Comment.Downvote')
        FTimeStamps = ForumEvents['TimeStamp']
        DurationOfForumActivity = FTimeStamps[-1] - FTimeStamps[0]
        # Append features to dictionary
        Features.update({
            'DurationOfForumActivity' : DurationOfForumActivity,
            'NumberOfThreadViews' : NumberOfThreadViews,
            'NumberOfPostsEvent' : NumberOfPostsEvent,
            'NumberOfSubscribe' : NumberOfSubscribe,
            'NumberOfLaunch' : NumberOfLaunch,
            'NumberOfComments' : NumberOfComments
            # #'Postlength' : Postlength
        })
    return Features