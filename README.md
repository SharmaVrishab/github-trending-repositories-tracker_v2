# 📈 GitHub Trending Repositories Scraper

A Python script that fetches **trending GitHub repositories** created in the last 7 days using the **GitHub OAuth Device Flow** for secure authentication.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Issues](https://img.shields.io/github/issues/yourusername/github-trending-scraper.svg)](https://github.com/yourusername/github-trending-scraper/issues)

## ✨ Features

- 🔐 **Secure Authentication**: Uses OAuth Device Flow (no password required)
- ⭐ **Trending Repositories**: Fetches repositories with highest star growth
- 📅 **Recent Focus**: Filters repos created in the last 7 days
- 🎯 **Language Filtering**: Optional filtering by programming language
- 📊 **Rich Information**: Displays repo name, stars, description, and URL
- 🚀 **Easy Setup**: Simple installation and configuration

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- A GitHub account
- Git (for cloning the repository)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SharmaVrishab/github-trending-repositories-tracker_v2
   cd github-trending-scraper
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Setup

### 1. Create GitHub OAuth App

1. Go to [GitHub Settings → Developer settings → OAuth Apps](https://github.com/settings/developers)
2. Click **"New OAuth App"**
3. Fill in the application details:
   - **Application name**: `GitHub Trending Scraper` (or your preferred name)
   - **Homepage URL**: `http://localhost`
   - **Authorization callback URL**: `http://localhost`
4. Click **"Register application"**
5. Copy the **Client ID** from the app settings page

### 2. Configure Environment Variables

**Option A: Environment Variable (Recommended)**
```bash
# Linux/Mac
export GITHUB_CLIENT_ID="your_client_id_here"

# Windows Command Prompt
set GITHUB_CLIENT_ID=your_client_id_here

# Windows PowerShell
$env:GITHUB_CLIENT_ID="your_client_id_here"
```

**Option B: Configuration File**
Create a `config.env` file in the project root:
```env
GITHUB_CLIENT_ID=your_client_id_here
```

## 🎮 Usage

### Basic Usage

Run the script to fetch trending repositories:

```bash
python trending_repos.py
```

### First-Time Setup

1. Run the script
2. Follow the authentication flow:
   - A device code will be displayed
   - Visit the GitHub device activation URL
   - Enter the device code
   - Authorize the application
3. The script will automatically fetch and display trending repositories

### Sample Output

```
🔐 Authenticating with GitHub...
📱 Please visit: https://github.com/login/device
🔑 Enter code: ABCD-1234
✅ Authentication successful!

📈 Top Trending Repositories (Last 7 Days):

⭐ 2,847 stars | awesome-ai-tools
   🔗 https://github.com/user/awesome-ai-tools
   📝 A curated list of awesome AI tools and resources

⭐ 1,923 stars | react-native-awesome
   🔗 https://github.com/user/react-native-awesome
   📝 Collection of awesome React Native components

⭐ 1,456 stars | python-data-viz
   🔗 https://github.com/user/python-data-viz
   📝 Beautiful data visualization examples in Python
```

## 🛠️ Configuration Options

### Language Filtering

To filter repositories by programming language, modify the search query in `trending_repos.py`:

```python
# Example: Only Python repositories
search_url = f"{BASE_URL}/search/repositories?q=created:>={seven_days_ago}+language:Python&sort=stars&order=desc"

# Example: Only JavaScript repositories  
search_url = f"{BASE_URL}/search/repositories?q=created:>={seven_days_ago}+language:JavaScript&sort=stars&order=desc"
```

### Customize Results Count

Change the number of repositories displayed by modifying the loop in the script:

```python
# Display top 10 repositories instead of 5
for i, repo in enumerate(repos[:10]):
```

## 📁 Project Structure

```
github-trending-scraper/
│
├── trending_repos.py        # Main Python script
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore file
├── config.env              # Environment variables (optional)
```

## 🔧 Dependencies

- **requests**: HTTP library for API calls
- **python-dotenv** (optional): Load environment variables from `.env` file

## 🐛 Troubleshooting

### Common Issues

**❌ "Client ID not found"**
- Ensure you've set the `GITHUB_CLIENT_ID` environment variable
- Double-check the Client ID from your GitHub OAuth App settings

**❌ "Authentication failed"**
- Make sure you're entering the device code correctly
- Check that you've authorized the application in GitHub
- Verify your internet connection

**❌ "API rate limit exceeded"**
- GitHub has API rate limits. Wait a few minutes before trying again
- Authenticated requests have higher rate limits than unauthenticated ones

### Getting Help

If you encounter issues:

1. Check the [Issues](https://github.com/yourusername/github-trending-scraper/issues) page
2. Create a new issue with:
   - Error message
   - Python version
   - Operating system
   - Steps to reproduce

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/github-trending-scraper.git

# Create development branch
git checkout -b feature/your-feature-name

# Install development dependencies
pip install -r requirements.txt
```

## 📋 Future Enhancements

- [ ] Export results to CSV/JSON
- [ ] Web interface with Flask/FastAPI
- [ ] Database storage for historical tracking
- [ ] Email notifications for trending repos
- [ ] Support for GitHub Enterprise
- [ ] Advanced filtering options
- [ ] Graphical charts and analytics

## 🙏 Acknowledgments

- [GitHub API](https://docs.github.com/en/rest) for providing the data
- [Requests](https://docs.python-requests.org/) library for HTTP handling
- The open-source community for inspiration

## 📞 Contact

- **Author**: Vrishab
- **GitHub**: (https://github.com/sharmavrishab)
- **Project Link**: (https://github.com/SharmaVrishab/github-trending-repositories-tracker_v2)

---

⭐ **Found this helpful?** Give it a star to show your support!

**Happy coding!** 🚀
