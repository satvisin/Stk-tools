# Stk-tools 🛠️

A collection of useful tools for various development and testing tasks. This repository contains utilities designed to help with API testing, load testing, and other common development workflows.

## 🔧 Available Tools

### Load Testing Tools (`LoadTest/`)

#### 1. Professional Load Test (`LoadTest.py`)
A comprehensive load testing tool with advanced features:

**Features:**
- ✅ Concurrent request execution with configurable workers
- 📊 Professional performance charts and visualizations
- 📋 Detailed HTML and text reports
- ⏱️ Response time analysis (min, max, average, percentiles)
- 📈 Throughput measurement
- 🎯 Success rate monitoring
- 🏷️ Status code breakdown
- 📁 Automatic report generation in `reports/` directory

**Key Metrics Tracked:**
- Response times (average, median, 95th/99th percentile)
- Success rates and error rates
- Throughput (requests per second)
- Status code distribution
- Performance ratings and recommendations

**Usage:**
```bash
cd LoadTest
pip install -r requirements.txt
python LoadTest.py
```

**Configuration:**
Edit the configuration section in `LoadTest.py`:
- `BEARER_TOKEN`: Authentication token
- `URL`: Target endpoint
- `NUM_REQUESTS`: Total number of requests
- `MAX_WORKERS`: Concurrent workers
- `TIMEOUT_SECONDS`: Request timeout

#### 2. Simple API Test (`simple_test.py`)
A lightweight script for quick API endpoint testing:

**Features:**
- 🚀 Quick API endpoint validation
- 🔍 Basic response inspection
- ⚡ Minimal setup required
- 🛡️ Error handling for timeouts and connection issues

**Usage:**
```bash
cd LoadTest
python simple_test.py
```

## 📋 Requirements

### Python Dependencies
All Python tools require the following packages (install via `pip install -r LoadTest/requirements.txt`):

- `requests` - HTTP library for API calls
- `tqdm` - Progress bars for load testing
- `matplotlib` - Chart generation
- `pandas` - Data analysis and manipulation
- `datetime` - Date and time handling

### System Requirements
- Python 3.6 or higher
- Internet connection for API testing
- Sufficient disk space for report generation

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Stk-tools
   ```

2. **Install dependencies:**
   ```bash
   cd LoadTest
   pip install -r requirements.txt
   ```

3. **Run a simple test:**
   ```bash
   python simple_test.py
   ```

4. **Run comprehensive load test:**
   ```bash
   python LoadTest.py
   ```

## 📊 Sample Output

The load testing tools generate:
- **Console output** with real-time progress and summary
- **Performance charts** (PNG format) with response time distributions
- **Detailed reports** (TXT format) with comprehensive metrics
- **Professional summaries** with performance ratings and recommendations

---

**Made with ❤️ by @satvisin**