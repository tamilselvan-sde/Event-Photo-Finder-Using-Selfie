# Event Photo Finder Using Selfie 📸

Effortlessly find your photos from event albums using just a selfie! **Event Photo Finder Using Selfie** uses facial recognition technology to identify your photos from a large collection of images uploaded by the event photographer.

## 🚀 Features

- **Bulk Photo Upload**: Photographers can upload 100+ event photos to Google Photos via the app.
- **Selfie Search**: Attendees upload a selfie, and the app matches their face with event photos using facial recognition.
- **User-Friendly Interface**: Built with Streamlit for easy navigation.
- **Real-Time Matching**: Instantly fetches and displays matching photos.
- **Photo Sharing**: Download or share your matched photos directly.

---

## 📋 Installation and Setup

Follow these steps to install and run the application:

### 1. Clone the Repository
```bash
git clone https://github.com/tamilmech/Event-Photo-Finder-Using-Selfie.git
cd Event-Photo-Finder-Using-Selfie
```

### 2. Install Dependencies
Ensure you have Python installed on your system. Create a virtual environment (optional) and install the required libraries:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Start the Streamlit app locally:
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
Event-Photo-Finder-Using-Selfie/
├── app.py                  # Main application code
├── requirements.txt        # Required Python libraries
├── sample_images/          # Folder for testing group photos
├── selfies/                # Folder for testing selfies
```

---

## 🧰 How to Use

1. **Photographer**:
   - Upload event photos via the app to a directory.
   - Photos are processed, and faces are stored in the database.

2. **Attendee**:
   - Visit the app's URL (e.g., hosted on Streamlit Cloud or Heroku).
   - Upload your selfie to search for matching photos.
   - View and download your matching photos instantly.

---

## 🧑💻 Technical Stack

- **Backend**:
  - Google Photos API: For managing and storing event photos.
  - Google Vision API: For facial recognition and matching.
  - SQLite: To store photo metadata.
- **Frontend**:
  - Streamlit: For the user-friendly interface.
- **Hosting**:
  - Local hosting during development.
  - Cloud hosting (Heroku/Google Cloud/AWS) for live deployment.

---

## 📊 Workflow

1. **Upload Event Photos**:
   - The photographer uploads event photos via the app.
   - The app processes the photos, detects faces, and stores metadata in the database.

2. **Upload a Selfie**:
   - Users upload their selfies via the Streamlit app.
   - The app extracts facial features using the Google Vision API.

3. **Search Photos**:
   - The app matches the selfie’s facial features with event photos stored in the database.

4. **Display Results**:
   - Matching photos are displayed in a user-friendly interface.
   - Users can download or share their photos.

---

## 🗓 Development Timeline

| **Phase**                  | **Task**                         | **Duration** |
|----------------------------|-----------------------------------|--------------|
| Phase 1                    | Setup and API Integration         | 5 days       |
| Phase 2                    | Bulk Photo Upload & Processing    | 7 days       |
| Phase 3                    | Selfie Search and Matching        | 10 days      |
| Phase 4                    | Streamlit UI Development          | 7 days       |
| Phase 5                    | Testing and Deployment            | 5 days       |
| **Total Duration**         |                                   | **~1 month** |

---

## 📊 Cost Estimation

| **Service**              | **Cost**                          |
|--------------------------|------------------------------------|
| Google Photos API        | Free within quota                |
| Google Vision API        | Free tier: 1,000 units/month      |
| Cloud Hosting (Heroku)   | Free for basic apps               |

---

## 🎉 Benefits

- **Efficiency**: Instantly find photos from large event albums.
- **Ease of Use**: Simple selfie-based photo searching.
- **Scalability**: Handles large-scale events.
- **Customizable**: Add features like watermarks or social media sharing.

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

---

## 📧 Contact

For queries or suggestions, reach out at [stselvan9095@gmail.com].


