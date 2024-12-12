# Project CasperV2

## Dependencies and Downloads

To run this project, you are required to have Docker and pip installed on your PC.

### Steps to Set Up

1. **Compose the API**:
   - Navigate to the `ApiReminder` directory.
   - Run `docker compose up`.
   - Ensure that ports 8080 and 5432 are free before composing.

2. **Install Requirements**:
   - Activate a virtual environment for the project.
   - Navigate to the root of the project.
   - Run `pip install -r requirements.txt` to install all required dependencies.

3. **Voice Mode Setup**:
   - Download a Vosk model from [this link](https://alphacephei.com/vosk/models).
   - The model used during development is `vosk-model-en-us-0.22`.
   - Unpack the downloaded file in the root folder of the project.

## Running the Application

The entry point of the program is `summaryAgent.py`. To run the application, use the following command:

### Optional Argument

- `-m "mode"` with choices `"voice"` or `"text"`.

## Modes

### Voice Mode

In voice mode, the application is operated entirely by voice commands and will respond with voice feedback to the user's requests.

**KNOWN PROBLEMS**: The voice model 0.22 is generally effective but may occasionally produce random sentences.

### Text Mode

In text mode, the application is operated entirely through the console with no voice feedback. This is the easiest way to communicate with the agent.

## Agent Purpose

The agent is equipped with tools to create and manage small reminders for the user, helping them in their day-to-day work. It functions like a TODO manager for work or a more complicated way to create and manage a shopping list, if you like to do things the hard way
