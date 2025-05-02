# Telegram OSINT Project

A Python-based tool to perform Telegram Open Source Intelligence (OSINT) by searching public Telegram channels and groups for user-defined keywords, extracting channel usernames, and discovering similar channels for deeper threat intelligence and content discovery.

---

## 🔍 Features

* **Keyword-driven Search**: Search Telegram channels, groups, and titles using a customizable list of keywords.
* **Username Extraction**: Automatically extract and deduplicate Telegram usernames (@usernames) from search results.
* **Similar Channel Discovery**: For each public channel, fetch recommended similar channels via Telethon.
* **Configurable via Files**: Manage API credentials (`config.json`) and keyword lists (`keywords.txt`) separately.
* **JSON Output**: Save results in a structured `results.json` for easy analysis and integration.

---

## 🚀 Quickstart

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/telegram-osint.git
cd telegram-osint
```

### 2. Prepare Python Environment

* Ensure you have **Python 3.7+** installed.
* Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

### 3. Obtain Telegram API Credentials

1. Go to [my.telegram.org](https://my.telegram.org) and log in with your phone number.
2. Navigate to **API development tools** and create a new application.
3. Copy the **API ID** and **API Hash**.
4. Create a `config.json` file in the project root:

   ```json
   {
     "api_id": YOUR_API_ID,
     "api_hash": "YOUR_API_HASH"
   }
   ```

### 4. Generate Your Keyword List

* Create a file named `keywords.txt` in the root directory.
* Using ChatGPT or any brainstorming method, generate a **wordlist of 15 related keywords** for your topic of interest (e.g., jobs, fraud, malware, etc.), one keyword per line.

  **Example** **:**

  ```text
  jobs
  remote jobs
  tech jobs
  freelance jobs
  IT jobs
  data science jobs
  developer jobs
  engineering jobs
  marketing jobs
  design jobs
  software engineer jobs
  part-time jobs
  full-time jobs
  work from home jobs
  startup jobs
  ```

### 5. Run the OSINT Script

```bash
python3 telegram_osint.py
```

* The script will:

  1. Read your keywords from `keywords.txt`.
  2. Search Telegram via `@tgdb_bot` in `/group`, `/channel`, and `/title` modes.
  3. Extract and deduplicate usernames + types.
  4. Limit to the first 200 channels for similarity lookup.
  5. Fetch similar channels for each public channel.
  6. Save the consolidated data to `results.json`.

---

## 📂 Output Format

The final `results.json` will contain an array of objects:

```json
[
  {
    "username": "@infosec_today",
    "channel_name": "Cyber Intel News",
    "similar_channels": [
      { "username": "@cyberintelnews", "title": "Cyber Intel News", "id": 987654321 },
      { "username": "@threatalerts",     "title": "Threat Alerts",     "id": 876543210 }
    ]
  },
  {
    "username": "@tech_watch",
    "channel_name": "Technology Updates",
    "similar_channels": []
  }
]
```

---

## 🛠️ Requirements

Listed in `requirements.txt`:

```
Telethon==1.33.1
requests==2.32.3
prettytable==3.9.0
termcolor==2.4.0
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

Be sure to follow code style conventions and add tests where applicable.
