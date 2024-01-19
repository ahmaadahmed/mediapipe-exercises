import cv2
import mediapipe as mp

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Open a video capture object
video_path = r"C:\Users\pc\Videos\Download Videos\The Perfect Push Up  Do it right!.mp4"

cap = cv2.VideoCapture(video_path)

# Variable to track push-up count
push_up_count = 0
in_push_up_position = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image to get pose landmarks
    results = pose.process(rgb_frame)

    # Check if key landmarks are detected
    if results.pose_landmarks is not None:
        # Extract relevant landmarks for push-up detection (e.g., shoulder, elbow, wrist)
        shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]

        # Logic to check if the person is in a push-up position
        if shoulder.y < elbow.y and elbow.y < wrist.y:
            if not in_push_up_position:
                # Entering push-up position
                in_push_up_position = True
                push_up_count += 1
                print(f'Push-up Count: {push_up_count}')
        else:
            in_push_up_position = False

    # Draw landmarks using OpenCV (if needed)
    if results.pose_landmarks is not None:
        for landmark in results.pose_landmarks.landmark:
            height, width, _ = frame.shape
            cx, cy = int(landmark.x * width), int(landmark.y * height)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

     # Display push-up count on the frame
    cv2.putText(frame, f'Push-ups: {push_up_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

     # Display the frame
    cv2.imshow('Push-up Counter', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()

# Print the final push-up count
print(f'Total Push-ups: {push_up_count}')



