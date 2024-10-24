import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Curl counter variables
counter = 0
stage = None

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle
    return angle

# Path to the local video file
video_path = 'pushhhh.mp4'

# Start capturing the video from the local file
cap = cv2.VideoCapture(0)

# Variable to check if the video is paused
paused = False

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        if not paused:
            ret, frame = cap.read()

            # If the frame was not retrieved, break the loop (end of video)
            if not ret:
                break

            # Recolor the frame to RGB
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Make detection
            results = pose.process(image_rgb)

            # Recolor back to BGR
            frame = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates for the left side
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]


                # Get coordinates for the right side
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # Calculate right arm angle
                right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_sholder_angle = calculate_angle(right_elbow, right_shoulder, left_shoulder)
                left_sholder_angle = calculate_angle(left_elbow, left_shoulder, right_shoulder)

                # Visualize angles on the frame
                cv2.putText(frame, str(left_elbow_angle),
                            tuple(np.multiply(left_elbow, [frame.shape[1], frame.shape[0]]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(frame, str(right_elbow_angle),
                            tuple(np.multiply(right_elbow, [frame.shape[1], frame.shape[0]]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(frame, str(left_sholder_angle),
                            tuple(np.multiply(left_shoulder, [frame.shape[1], frame.shape[0]]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(frame, str(right_sholder_angle),
                            tuple(np.multiply(right_shoulder , [frame.shape[1], frame.shape[0]]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                if left_elbow_angle > 140 and right_elbow_angle >140 and left_sholder_angle>100 and right_sholder_angle >100:
                    stage = "up"
                if left_elbow_angle <80 and right_elbow_angle <80 and left_sholder_angle<175 and right_sholder_angle<175 and stage=='up':
                    stage = "down"
                    counter += 1
                    print(counter)
            except:
                pass

            # Render pose landmarks
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        # Display the resulting frame
        cv2.imshow('Pose Estimation', frame)

        # Keyboard inputs
        key = cv2.waitKey(10) & 0xFF
        if key == ord('q'):
            break  # Exit the loop when 'q' is pressed
        elif key == ord(' '):
            paused = not paused  # Pause or resume when spacebar is pressed

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
