from flask import Flask, render_template, request

app = Flask(__name__)

# Function to perform face recognition
def perform_face_recognition():
    import cv2
    import face_recognition

    # Load the known images and encode their faces
    known_faces = []
    known_names = []

    # Example: Loading
    #  known images
    image_1 = face_recognition.load_image_file("image.png")
    encoding_1 = face_recognition.face_encodings(image_1)[0]
    known_faces.append(encoding_1)
    known_names.append("Face Detected, Press Q")

    # Initialize the video capture
    video_capture = cv2.VideoCapture(0)
    

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Find faces in the frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Iterate over detected faces
        for face_encoding in face_encodings:
            # Compare each face encoding with known faces
            matches = face_recognition.compare_faces(known_faces, face_encoding)

            name = "Unknown, press Q"

            # Check if there's a match
            if True in matches:
                alpha = 1
                # Find the index of the matched face
                matched_index = matches.index(True)
                name = known_names[matched_index]

            # Draw a box around the face and display the name
            top, right, bottom, left = face_recognition.face_locations(frame)[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        # Display the resulting image
        cv2.imshow('Video', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture
    video_capture.release()
    cv2.destroyAllWindows()

    if alpha == 1:
       return True
       

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # Perform face recognition
    match = perform_face_recognition()

    if match:
        return "Login successful"
    else:
        return "Login failed: Your face was not recognized. Please try again."


if __name__ == '__main__':
    app.run()