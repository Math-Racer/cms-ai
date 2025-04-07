# CMS-AI
# Generative AI-Powered Feedback System for DOMjudge

This application enhances the DOMjudge competitive programming system by providing real-time, generative AI-powered feedback for incorrect submissions. It integrates with DOMjudge to analyze user submissions and generate tailored hints to guide users toward the correct solution.

---

## **Features**

- **Real-Time Feedback**: Continuously monitors DOMjudge for new submissions and provides feedback within seconds.
- **Generative AI Integration**: Uses the `llama3.2` model via the Ollama platform to generate context-aware hints.
- **Seamless DOMjudge Integration**: Interacts with DOMjudge's REST API to retrieve submissions and post clarifications.
- **Customizable Question Repository**: Maintains a mapping of problem IDs to their descriptions for accurate hint generation.
- **Robust Logging**: Logs all interactions, including API calls, errors, and generated hints, for debugging and monitoring.

---

## **Folder Structure**

```
app/
├── .env                     # Environment variables for API configuration
├── app.py                   # Main application script
├── clueCreate.py            # Clue generation logic using AI
├── Dockerfile               # Default Dockerfile for containerization
├── Dockerfile.gpu           # Dockerfile for GPU-enabled systems
├── Dockerfile.ollama        # Dockerfile for Ollama integration
├── Dockerfile.py            # Lightweight Python-specific Dockerfile
├── requirements.txt         
├── questions/               
    └── questions.py         # Question repository with problem descriptions
```

---

## **Setup Instructions**

### **1. Prerequisites**
- Python 3.10 or higher
- Docker (for containerized deployment)
- Ollama installed locally or running in a container
- Access to a DOMjudge server with API credentials

### **2. Installation**

#### **Without Docker**
1. Clone the repository:
   ```
   git clone <repository-url>
   cd app
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Pull the AI model:
   ```
   ollama pull llama3.2
   ```
4. Configure the `.env` file:
   ```
   API_BASE_URL="http://localhost:12345/api/v4/"
   CID=1
   ```
5. Run the application:
   ```
   python app.py
   ```

#### **With Docker**
1. Build the Docker image:
   ```bash
   docker build -t ai-feedback-app -f Dockerfile.ollama .
   ```
2. Run the container:
   ```bash
   docker run --name ai-feedback-container -e WEBSITE_LINK=http://localhost:12345/api/v4/ -e CID=1 ai-feedback-app
   ```

---

## **How It Works**

1. **Polling Judgements**:
   - The application continuously polls DOMjudge for new judgements using the `pollJudgements` function in [`app.py`](app.py).
   - Submissions with non-accepted verdicts are identified for processing.

2. **Retrieving Submission Details**:
   - The `readSubmission` function fetches the source code, team ID, and problem ID for incorrect submissions.

3. **Generating Hints**:
   - The `clueCreate` function in [`clueCreate.py`](clueCreate.py) uses the `llama3.2` model to generate a one-line hint based on the submission and problem description.

4. **Posting Clarifications**:
   - The `postClar` function sends the generated hint back to DOMjudge as a clarification.

5. **Question Repository**:
   - The [`questions.py`](questions/questions.py) file maintains a dictionary of problem IDs and their descriptions. This ensures the AI model has the necessary context for generating accurate hints.

---

## **Environment Variables**

The application uses the following environment variables, defined in the `.env` file:

| Variable         | Description                                      | Default Value                     |
|-------------------|--------------------------------------------------|-----------------------------------|
| `API_BASE_URL`    | Base URL for the DOMjudge API                   | `http://localhost:12345/api/v4/` |
| `CID`             | Contest ID for DOMjudge                        | `1`                              |

---

## **Dockerfiles**

- **`Dockerfile`**: Default Dockerfile for containerizing the app.
- **`Dockerfile.gpu`**: Optimized for GPU-enabled systems to speed up AI inference.
- **`Dockerfile.ollama`**: Preloads the `llama3.2` model into the container.
- **`Dockerfile.py`**: Lightweight Python-specific Dockerfile for minimal setups.

---

## **Question Repository**

The [`questions.py`](questions/questions.py) file contains a dictionary mapping problem IDs to their descriptions. When uploading new questions to DOMjudge, ensure they are also added to this file in the following format:

```python
Question["<problem_id>"] = """
<problem_description>
"""
```

---

## **Logging**

Logs are stored in `app.log` and include:
- API requests and responses
- Errors and exceptions
- Generated hints and clarifications


---

## **License**
This project is licensed under the The MIT License (MIT). See the LICENSE file for details