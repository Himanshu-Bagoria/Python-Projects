import cv2
import face_recognition
import numpy as np
import os
import pickle
from datetime import datetime
import streamlit as st
from PIL import Image
import time

class FaceRecognitionSystem:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.faces_dir = os.path.join(data_dir, "faces")
        self.encodings_file = os.path.join(data_dir, "face_encodings.pkl")
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
        
        # Create directories
        os.makedirs(self.faces_dir, exist_ok=True)
        
        # Load existing encodings
        self.load_encodings()
    
    def load_encodings(self):
        """Load existing face encodings from file"""
        try:
            if os.path.exists(self.encodings_file):
                with open(self.encodings_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_face_encodings = data.get('encodings', [])
                    self.known_face_names = data.get('names', [])
                    self.known_face_ids = data.get('ids', [])
                print(f"Loaded {len(self.known_face_encodings)} face encodings")
        except Exception as e:
            print(f"Error loading encodings: {e}")
            self.known_face_encodings = []
            self.known_face_names = []
            self.known_face_ids = []
    
    def save_encodings(self):
        """Save face encodings to file"""
        try:
            data = {
                'encodings': self.known_face_encodings,
                'names': self.known_face_names,
                'ids': self.known_face_ids
            }
            with open(self.encodings_file, 'wb') as f:
                pickle.dump(data, f)
            return True
        except Exception as e:
            print(f"Error saving encodings: {e}")
            return False
    
    def add_employee_face(self, employee_id, employee_name, image_file):
        """Add a new employee's face to the recognition system"""
        try:
            # Save image file
            image_path = os.path.join(self.faces_dir, f"{employee_id}.jpg")
            
            # Convert PIL Image to OpenCV format if needed
            if isinstance(image_file, Image.Image):
                image_file.save(image_path)
                image = cv2.imread(image_path)
            else:
                # If it's already a file path
                image = cv2.imread(image_file)
                cv2.imwrite(image_path, image)
            
            if image is None:
                return False, "Could not read image file"
            
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Find face encodings
            face_encodings = face_recognition.face_encodings(rgb_image)
            
            if len(face_encodings) == 0:
                return False, "No face detected in the image"
            
            if len(face_encodings) > 1:
                return False, "Multiple faces detected. Please use an image with only one face."
            
            # Add encoding
            self.known_face_encodings.append(face_encodings[0])
            self.known_face_names.append(employee_name)
            self.known_face_ids.append(employee_id)
            
            # Save encodings
            if self.save_encodings():
                return True, "Face registered successfully"
            else:
                return False, "Error saving face encoding"
                
        except Exception as e:
            return False, f"Error processing face: {str(e)}"
    
    def recognize_face(self, image):
        """Recognize face in an image"""
        try:
            # Convert to RGB if needed
            if len(image.shape) == 3 and image.shape[2] == 3:
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                rgb_image = image
            
            # Find face locations and encodings
            face_locations = face_recognition.face_locations(rgb_image)
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            
            recognized_faces = []
            
            for face_encoding, face_location in zip(face_encodings, face_locations):
                # Compare with known faces
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                
                if len(matches) > 0 and True in matches:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index] and face_distances[best_match_index] < 0.6:  # Threshold
                        name = self.known_face_names[best_match_index]
                        employee_id = self.known_face_ids[best_match_index]
                        confidence = 1 - face_distances[best_match_index]
                        
                        recognized_faces.append({
                            'employee_id': employee_id,
                            'name': name,
                            'confidence': confidence,
                            'location': face_location
                        })
            
            return recognized_faces
            
        except Exception as e:
            print(f"Error in face recognition: {e}")
            return []
    
    def capture_and_recognize(self):
        """Capture image from webcam and recognize faces"""
        try:
            # Initialize webcam
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                return None, "Could not access webcam"
            
            st.info("Webcam activated. Press 'q' to quit or wait for detection...")
            
            # Create placeholder for video feed
            video_placeholder = st.empty()
            status_placeholder = st.empty()
            
            recognized_faces = []
            start_time = time.time()
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Display frame
                video_placeholder.image(frame, channels="BGR", use_column_width=True)
                
                # Recognize faces every few frames for performance
                if time.time() - start_time > 1:  # Check every second
                    recognized_faces = self.recognize_face(frame)
                    if recognized_faces:
                        status_placeholder.success(f"Recognized: {recognized_faces[0]['name']} "
                                                 f"(Confidence: {recognized_faces[0]['confidence']:.2f})")
                        break
                    start_time = time.time()
                
                # Check if user wants to quit (in Streamlit context)
                if st.button("Stop Recognition", key="stop_recognition"):
                    break
            
            cap.release()
            video_placeholder.empty()
            status_placeholder.empty()
            
            return recognized_faces, "Recognition completed"
            
        except Exception as e:
            return None, f"Error in face recognition: {str(e)}"
    
    def get_registered_faces(self):
        """Get list of registered employee faces"""
        return list(zip(self.known_face_ids, self.known_face_names))
    
    def remove_employee_face(self, employee_id):
        """Remove an employee's face from the recognition system"""
        try:
            # Find index of employee
            if employee_id in self.known_face_ids:
                index = self.known_face_ids.index(employee_id)
                
                # Remove from lists
                self.known_face_encodings.pop(index)
                self.known_face_names.pop(index)
                self.known_face_ids.pop(index)
                
                # Remove image file
                image_path = os.path.join(self.faces_dir, f"{employee_id}.jpg")
                if os.path.exists(image_path):
                    os.remove(image_path)
                
                # Save updated encodings
                self.save_encodings()
                return True, "Face removed successfully"
            else:
                return False, "Employee face not found"
                
        except Exception as e:
            return False, f"Error removing face: {str(e)}"
    
    def update_employee_face(self, employee_id, employee_name, image_file):
        """Update an existing employee's face"""
        # First remove the existing face
        self.remove_employee_face(employee_id)
        
        # Then add the new face
        return self.add_employee_face(employee_id, employee_name, image_file)

def draw_face_boxes(image, recognized_faces):
    """Draw bounding boxes around recognized faces"""
    image_copy = image.copy()
    
    for face in recognized_faces:
        top, right, bottom, left = face['location']
        name = face['name']
        confidence = face['confidence']
        
        # Draw rectangle
        cv2.rectangle(image_copy, (left, top), (right, bottom), (0, 255, 0), 2)
        
        # Draw label
        label = f"{name} ({confidence:.2f})"
        cv2.rectangle(image_copy, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(image_copy, label, (left + 6, bottom - 6), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
    
    return image_copy