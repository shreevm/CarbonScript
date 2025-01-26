## **CarbonScript **

**CarbonScript** is an application that allows users to upload Python scripts, analyze the script for its contents, and calculate the CO2 emissions produced while executing the script. It also utilizes the Gemini AI model to extract insights from the Python script.

---

## **Features**

- Upload a Python file for analysis.
- Display the entire Python script in an editable text area.
- Analyze the Python script with insights provided by the Gemini AI model.
- Display the CO2 emissions calculated during the execution of the script.

---

## **Requirements**

### **Backend (Flask API)**

1. **Python 3.x**  
2. Install required Python libraries using `pip`:

   ```bash
   pip install flask flask-cors codecarbon google-generativeai

---

## **Gemini API Key Setup**

1. Sign up or log in to [Google Cloud Platform](https://cloud.google.com/).
2. Go to the **API & Services** section and create a new project if you haven't already.
3. Navigate to **API & Services > Credentials**.
4. Click on **Create Credentials** and select **API Key**.
5. Copy the generated API key.

Once you have the API key, replace the placeholder in the `app.py` file with your actual API key:

```python
GOOGLE_API_KEY = 'YOUR_API_KEY_HERE'
```
---
## **Backend Setup**

Clone the repository or navigate to your existing project folder.

Create a new virtual environment (optional but recommended):

```
python3 -m venv venv
```
Install the required Python libraries mentioned above.

Set up the Gemini API Key in the app.py file (as described above).

Run the Flask API:
```
python app.py
```
The server will run locally on http://localhost:5000.
