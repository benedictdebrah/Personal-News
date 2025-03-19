# Personal News Scraper  

A lightweight Python application that scrapes news articles from CitiNewsroom, extracts content, and stores it in a SQLite database.  

## Features  
✅ Scrapes up to **100 news articles** per run  
✅ Stores **titles, links, content, and images** in a database  
✅ **Cleans up** old articles automatically  
✅ **Detailed logging** with rotating log files  
✅ **Automated scheduling** using **cron**  

## Requirements  
- Python **3.9+**  
- SQLite  
- Virtual environment (Recommended)  

## Installation  
1️⃣ Clone the repository:  
```sh
git clone https://github.com/your-username/personal-news.git
cd personal-news
```  
2️⃣ Create and activate a virtual environment:  
```sh
python -m venv .venv  
source .venv/bin/activate  # macOS/Linux  
```  
3️⃣ Install dependencies:  
```sh
pip install -r requirements.txt  
```  

## Running the Scraper  
Run the scraper manually anytime:  
```sh
python -m app.main  
```  

## ⏳ Automating with Cron (macOS/Linux)  
To schedule the scraper to run **daily at 3 AM UTC**:  

1️⃣ Open the crontab editor:  
```sh
crontab -e  
```  
2️⃣ Add this line at the bottom:  
```sh
0 3 * * * /Users/benedictdebrah/Desktop/Personal-News/.venv/bin/python -m app.main >> /Users/benedictdebrah/Desktop/Personal-News/cron.log 2>&1  
```  
3️⃣ Save and exit.  

**Explanation:**  
- `0 3 * * *` → Runs at **3 AM UTC** daily  
- The script output is logged to `cron.log`  

To check if the cron job is running:  
```sh
crontab -l  
```  

## Logging  
- Logs are stored in `news_scraper.log`  
- Uses **rotating log files** (keeps up to 3 backups)  
- Logs **timestamps, severity levels, and errors**  

To view logs:  
```sh
cat news_scraper.log  
```  

## Database Structure  
Stores articles in **SQLite** (`database.db`).  

**InfoData Table**  
- `id` - Unique ID  
- `title` - Article title  
- `link` - Article URL  
- `created_at` - Timestamp  
- `is_deleted` - Soft delete flag  

**NewsData Table**  
- `id` - Unique ID  
- `title` - Article title  
- `content` - Full text  
- `featured_image` - Image URL  
- `info_id` - Linked to InfoData  

## Error Handling  
- ✅ Handles **network timeouts** (30 sec)  
- ✅ Detects **missing content & duplicates**  
- ✅ **Catches database errors**  
- ✅ Logs **all issues** for debugging  

## Next Steps  
 **Build an MCP (Model Conntext Protocol) to connect the database**  

## 🤝 Contributing  
1️⃣ Fork the repository  
2️⃣ Create a feature branch  
3️⃣ Commit your changes  
4️⃣ Push to the branch  
5️⃣ Submit a Pull Request  

## 📜 License  
Licensed under the **MIT License**.  

