# Route-Finder-streamlit
Project Overview: Route Finder (Europe)
Objective
The goal of this project was to develop a Streamlit-based Python web application that helps users find cycling or hiking routes based on either uploaded GPX files or manually entered parameters. The app should be capable of matching or suggesting similar routes—preferably within European regions—using either local GPX data or external APIs. Additional features include elevation profile visualization and machine learning–based personalized recommendations.

Requirements
✅ A Streamlit web app with a user-friendly interface.


✅ Support for GPX file upload, with route parsing (distance, elevation gain, coordinates).


✅ Option for manual input of route parameters: distance, elevation gain, and surface type.


✅ Ability to match user input with similar existing routes.


✅ Integration with an API (e.g., OpenRouteService) to fetch live routes using coordinate input.


✅ Display of elevation profile charts for the selected or uploaded routes.


✅ A recommendation system using machine learning to suggest routes based on past behavior or user preferences.


✅ Logging of all user interactions for future personalization and analysis.



What I Built
🔹 A complete Streamlit application that supports two modes of input: GPX upload and manual entry.


🔹 GPX parser that extracts route metrics and elevation profiles.


🔹 Route matcher that finds the closest match from local GPX files using distance and elevation similarity scoring.


🔹 Integration with OpenRouteService API to fetch real-time routes between coordinates.


🔹 Interactive elevation profile charts using Plotly.


🔹 A machine learning–based recommender system using K-Nearest Neighbors to suggest personalized routes based on previous inputs.


🔹 User logging with CSV export for user behavior tracking and preference analysis.


🔹 Modular and clean code structure using Python packages and utility files.



Conclusion
The project successfully meets all the original functional and non-functional requirements. It is extendable, user-centric, and integrates both static and dynamic route-matching techniques. The combination of GPX file analysis, API integration, visualization, and machine learning provides a robust platform for route discovery and personalization.
