# Cloud-Enchanced Toxicity Detection System

## Overview

The Toxicity Detection Desktop Application is designed to detect toxicity statistics in text content across seven categories: severe, obscene, threat, etc. The application leverages a pre-trained toxicity detection model to analyze the input text and provide insights into its toxicity level in various categories. The application consists of a desktop client and a backend API hosted on an AWS EC2 instance.

## Features

- **Toxicity Detection**: The core feature of the application is to identify the toxicity level of input text across different categories. The pre-trained model processes the text and assigns toxicity scores to each category, allowing users to understand the potential harmfulness of the content.

- **Seven Toxicity Categories**: The application assesses text content in seven different categories: severe, obscene, threat, and others. This comprehensive approach provides a nuanced understanding of the content's nature.

- **Web Scraping**: The application also offers web scraping capabilities to extract tweet text from tweet links. This feature enables users to directly analyze content from tweets and assess its toxicity.

## Components

The Toxicity Detection Desktop Application comprises the following components:

1. **Desktop Client**: This is the user-facing interface where users can input text or tweet links for toxicity analysis. The desktop client communicates with the backend API to process the text and retrieve toxicity scores.

2. **Backend API**: The backend API is hosted on an AWS EC2 instance. It receives input text from the desktop client and interacts with the pre-trained toxicity detection model. Once the analysis is complete, the API returns toxicity scores and category information to the desktop client for display.

3. **Pre-trained Model**: The toxicity detection model is pre-trained and integrated into the backend API. It processes the input text and calculates toxicity scores for each category. The model's output is used to generate the toxicity statistics displayed to the user.

## Note

- The application's focus is on computation in the cloud, as the pre-trained model handles the toxicity analysis. Thus, the emphasis is on the accurate and efficient processing of text.

Thank you for using the Toxicity Detection Desktop Application! If you encounter any issues or have feedback, please reach out to me at [nilaykumarpatel86@gmail.com](mailto:nilaykumarpatel86@gmail.com).
