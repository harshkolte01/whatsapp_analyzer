# WhatsApp Chat Analyzer

A Streamlit web application to analyze your WhatsApp chats.

## Features

- **Upload Chat File**: Easily upload your exported WhatsApp `.txt` file.
- **Overall & User-Specific Analysis**: View statistics for the entire chat or filter by a specific person.
- **Top Statistics**:
  - Total messages exchanged.
  - Total words used.
  - Total media files shared.
  - Total links shared.
- **Timelines**:
  - **Monthly Timeline**: Track chat activity over the months.
  - **Daily Timeline**: See a day-by-day message count.
- **Activity Analysis**:
  - **Most Busy Day & Month**: Bar charts showing the most active days of the week and months of the year.
  - **Weekly Activity Heatmap**: A heatmap visualizing chat frequency by day and time period.
- **User Engagement**:
  - **Most Busy Users**: A bar chart and a data table showing the most active users and their percentage contribution.
- **Content Insights**:
  - **WordCloud**: A visual representation of the most frequently used words.
  - **Most Common Words**: A bar chart of the top 20 most common words.
  - **Emoji Analysis**: A data table and a pie chart showing the most used emojis.

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd whatsapp-analyzer
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

4.  Open your browser and go to the local URL provided by Streamlit (usually `http://localhost:8501`).