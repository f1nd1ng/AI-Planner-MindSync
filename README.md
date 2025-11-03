# MindSync – Emotion-Aware Smart Task Planner

MindSync is a productivity tool that adapts your daily schedule based on your emotional state.
By combining emotion analysis with intelligent task prioritization, the system helps users work efficiently, avoid burnout, and maintain balanced energy levels throughout the day.

# Video Demo Link: 
  ```sh
      https://drive.google.com/drive/folders/1HUsj8wtO9cyOZb3akl2ilCr5BGRageDc?gad_source=1&gad_campaignid=23198035368&gbraid=0AAAABB4biwptoqK5BULvr6ipNUOaimcgw&gclid=CjwKCAiAwqHIBhAEEiwAx9cTedRiS2XR7oww274hCTNCI07LyJVQp5tPRzGzraVVP91R7MPm0DZxOBoClOAQAvD_BwE
  ```

## Interaction logs: the prompts used and the chat history with the AI.

  ```sh
    https://chatgpt.com/c/68ff8b1c-a8a8-8323-9d18-341a1213caac
  ```

## Features

- **Emotion Check-In** : Describe how you feel, and the system detects your mood using emotion classification.
- **Task Input & Duration Estimation** : Add tasks with approximate time requirements.
- **Smart Scheduling Engine** : Automatically orders tasks based on your detected mood and energy levels.
- **Visual Calendar Preview** : View schedule in an interactive calendar layout.
- **No Login Required** : Lightweight and private by default.

## Built With

-Frontend       : React + Vite + CSS

-Backend        : FastAPI (Python)

-AI Model       : HuggingFace Transformer (Emotion Model)

-Visualization  : FullCalendar.js

## Setup Instructions 

### Project Setup
1.Navigate to the base directory:

2. Create a virtual environment:
   ```sh
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Navigate to the backend directory:
   ```sh
   cd credit_backend/
   ```
6. Run in backend
  ```sh
  streamlit run app.py  
  ```
7. Open another terminal, go to backend
   ```sh
   # from backend folder                                                   
    uvicorn backend_api:app --reload --port 8000
   ```
Backend will start at:
  ```sh
  http://127.0.0.1:8000
  ```
### Frontend Setup (credit_frontend/)
1. Navigate to the frontend directory:
   ```sh
   cd credit_frontend/
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the frontend development server:
   ```sh
   npm run dev
   ```
Frontend will start at:
  ```sh
  http://127.0.0.1:5173
  ```

## Future Scope

-Google Calendar Sync

-User Accounts + Cloud Storage

-Personalized Productivity Recommendations

-Voice-based emotion input

## Contributor 

-Ramanu Rishita- [f1nd1ng](https://github.com/f1nd1ng)

   
