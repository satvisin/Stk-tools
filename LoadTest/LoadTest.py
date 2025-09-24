import requests
import concurrent.futures
import time
from tqdm import tqdm
import json
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os

# ====== CONFIGURATION ======
BEARER_TOKEN = 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwMTktMDEtMDEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJ1bWJyZWxsYS1hdXRoei9hdXRoc3ZjIiwic3ViIjoib3JnLzgyNTgxMzkvdXNlci8xMjI5MjQ2NyIsImV4cCI6MTc1Mjg0NjQ0OSwibmJmIjoxNzUyODQ2MTQ5LCJpYXQiOjE3NTI4NDYxNDksInNjb3BlIjoicm9sZTpyb290LWFkbWluIiwiYXV0aHpfZG9uZSI6ZmFsc2V9.C8v5BQ5UtNeS6n1rmkp52Vow6BOmo7gpUWkEO3Mmsbw8MgtAv2HSFKH0-BexJy2vHlEqyj18hh3nGiQhsiIjV-qAbJKNUPljFs__AnprfpWZoALxjJVhtVUCLZApXkzjIBnzFRAtqFUnsFwAJ30ca9sUr0qQnoN_2ZARTG18slovcLzHmXOMLa9-8RmyGWrI0SQWaeq-OFy8Vq3M6ryt7mbCmtkCGWNPQsfTMR23QroeJZBBcaPh8KhHCoedqgFkQAoMUBCaCzfX9rhdM6K5mdxtpYv47ceA6s28LNsVlZG4Jj922j_DvYJ-jNRcsFKS5ieIbDaWOnfVvdkrRIXu_A'
URL = 'https://int.apigw.umbrella.com/reports/v2/fileevents/details?from=1752278400000&to=1752846182000&limit=50&offset=0&transactionid=5699bb623458b46d'
NUM_REQUESTS = 100
MAX_WORKERS = 100  # Reasonable number of concurrent workers
TIMEOUT_SECONDS = 30  # Request timeout

def make_request():
    headers = {
        'Authorization': BEARER_TOKEN,
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://dashboard.int.sse.cisco.com',
        'pragma': 'no-cache',
        'referer': 'https://dashboard.int.sse.cisco.com/',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
    }
    start_time = time.time()
    try:
        response = requests.get(URL, headers=headers, timeout=TIMEOUT_SECONDS)
        response_time = time.time() - start_time
        return {
            'status_code': response.status_code,
            'response_time': response_time,
            'response_size': len(response.text),
            'success': 200 <= response.status_code < 300
        }
    except requests.exceptions.Timeout:
        return {
            'status_code': 'TIMEOUT',
            'response_time': time.time() - start_time,
            'response_size': 0,
            'success': False
        }
    except requests.exceptions.ConnectionError:
        return {
            'status_code': 'CONNECTION_ERROR',
            'response_time': time.time() - start_time,
            'response_size': 0,
            'success': False
        }
    except Exception as e:
        return {
            'status_code': f'ERROR: {str(e)}',
            'response_time': time.time() - start_time,
            'response_size': 0,
            'success': False
        }

def generate_charts(results, test_duration):
    """Generate professional charts for the load test report"""
    # Create reports directory if it doesn't exist
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    # Extract data for charts
    response_times = [r['response_time'] for r in results]
    status_codes = [r['status_code'] for r in results]
    
    # Set up the plot style for professional appearance
    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10
    
    # Chart 1: Response Time Distribution
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Load Test Performance Report', fontsize=16, fontweight='bold')
    
    # Response Time Histogram
    ax1.hist(response_times, bins=20, color='skyblue', alpha=0.7, edgecolor='black')
    ax1.set_title('Response Time Distribution', fontweight='bold')
    ax1.set_xlabel('Response Time (seconds)')
    ax1.set_ylabel('Frequency')
    ax1.grid(True, alpha=0.3)
    
    # Response Time Over Time
    ax2.plot(range(len(response_times)), response_times, color='blue', linewidth=1, alpha=0.7)
    ax2.set_title('Response Time Over Time', fontweight='bold')
    ax2.set_xlabel('Request Number')
    ax2.set_ylabel('Response Time (seconds)')
    ax2.grid(True, alpha=0.3)
    
    # Status Code Distribution
    status_counts = pd.Series(status_codes).value_counts()
    colors = ['green' if isinstance(code, int) and 200 <= code < 300 else 'red' if isinstance(code, int) and code >= 400 else 'orange' for code in status_counts.index]
    ax3.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', colors=colors)
    ax3.set_title('Status Code Distribution', fontweight='bold')
    
    # Performance Metrics Table
    ax4.axis('tight')
    ax4.axis('off')
    
    # Calculate metrics
    avg_response_time = sum(response_times) / len(response_times)
    min_response_time = min(response_times)
    max_response_time = max(response_times)
    p95_response_time = sorted(response_times)[int(0.95 * len(response_times))]
    success_rate = sum(1 for r in results if r['success']) / len(results) * 100
    throughput = len(results) / test_duration
    
    metrics_data = [
        ['Metric', 'Value'],
        ['Total Requests', f"{len(results)}"],
        ['Test Duration', f"{test_duration:.2f} seconds"],
        ['Average Response Time', f"{avg_response_time:.3f} seconds"],
        ['Min Response Time', f"{min_response_time:.3f} seconds"],
        ['Max Response Time', f"{max_response_time:.3f} seconds"],
        ['95th Percentile', f"{p95_response_time:.3f} seconds"],
        ['Success Rate', f"{success_rate:.1f}%"],
        ['Throughput', f"{throughput:.2f} req/sec"]
    ]
    
    table = ax4.table(cellText=metrics_data[1:], colLabels=metrics_data[0], 
                     cellLoc='center', loc='center', colWidths=[0.4, 0.6])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)
    
    # Style the table
    for i in range(len(metrics_data)):
        if i == 0:  # Header row
            for j in range(len(metrics_data[0])):
                table[(i, j)].set_facecolor('#4CAF50')
                table[(i, j)].set_text_props(weight='bold', color='white')
        else:
            for j in range(len(metrics_data[0])):
                table[(i, j)].set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')
    
    ax4.set_title('Performance Metrics Summary', fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    # Save the chart
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    chart_filename = f'reports/load_test_report_{timestamp}.png'
    plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    return chart_filename

def generate_detailed_report(results, test_duration, start_time):
    """Generate a detailed professional report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f'reports/load_test_detailed_report_{timestamp}.txt'
    
    # Calculate comprehensive metrics
    response_times = [r['response_time'] for r in results]
    status_codes = [r['status_code'] for r in results]
    
    avg_response_time = sum(response_times) / len(response_times)
    min_response_time = min(response_times)
    max_response_time = max(response_times)
    median_response_time = sorted(response_times)[len(response_times) // 2]
    p95_response_time = sorted(response_times)[int(0.95 * len(response_times))]
    p99_response_time = sorted(response_times)[int(0.99 * len(response_times))]
    
    success_count = sum(1 for r in results if r['success'])
    success_rate = success_count / len(results) * 100
    error_rate = 100 - success_rate
    throughput = len(results) / test_duration
    
    # Count status codes
    status_counts = {}
    for code in status_codes:
        status_counts[code] = status_counts.get(code, 0) + 1
    
    # Generate report content
    report_content = f"""
{'='*80}
                    LOAD TEST PERFORMANCE REPORT
{'='*80}

EXECUTIVE SUMMARY
{'-'*40}
Test conducted on: {datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")}
Target Endpoint: {URL}
Total Test Duration: {test_duration:.2f} seconds
Total Requests Sent: {NUM_REQUESTS}
Concurrent Workers: {MAX_WORKERS}

KEY PERFORMANCE INDICATORS
{'-'*40}
✓ Success Rate: {success_rate:.1f}% ({success_count}/{NUM_REQUESTS} requests)
✗ Error Rate: {error_rate:.1f}%
⚡ Throughput: {throughput:.2f} requests/second
⏱️  Average Response Time: {avg_response_time:.3f} seconds

RESPONSE TIME ANALYSIS
{'-'*40}
Minimum Response Time:     {min_response_time:.3f} seconds
Maximum Response Time:     {max_response_time:.3f} seconds
Median Response Time:      {median_response_time:.3f} seconds
95th Percentile:          {p95_response_time:.3f} seconds
99th Percentile:          {p99_response_time:.3f} seconds

STATUS CODE BREAKDOWN
{'-'*40}"""

    for status, count in sorted(status_counts.items(), key=lambda x: str(x[0])):
        percentage = (count / NUM_REQUESTS) * 100
        status_type = "✓ SUCCESS" if isinstance(status, int) and 200 <= status < 300 else "✗ ERROR"
        report_content += f"\n{status}: {count} requests ({percentage:.1f}%) - {status_type}"

    report_content += f"""

PERFORMANCE ASSESSMENT
{'-'*40}
Overall Performance: {'EXCELLENT' if success_rate >= 99 else 'GOOD' if success_rate >= 95 else 'ACCEPTABLE' if success_rate >= 90 else 'POOR'}
Reliability Score: {success_rate:.1f}/100

Response Time Rating: {'EXCELLENT' if avg_response_time < 0.5 else 'GOOD' if avg_response_time < 1.0 else 'ACCEPTABLE' if avg_response_time < 2.0 else 'POOR'}
Average Response: {avg_response_time:.3f}s

Throughput Rating: {'HIGH' if throughput > 50 else 'MEDIUM' if throughput > 20 else 'LOW'}
Requests/Second: {throughput:.2f}

RECOMMENDATIONS
{'-'*40}"""

    if success_rate < 95:
        report_content += "\n• ⚠️  Success rate below 95% - investigate error causes"
    if avg_response_time > 2.0:
        report_content += "\n• ⚠️  High response times detected - check server performance"
    if throughput < 20:
        report_content += "\n• ⚠️  Low throughput - consider optimizing concurrent connections"
    if success_rate >= 99 and avg_response_time < 1.0:
        report_content += "\n• ✅ Excellent performance - system performing optimally"

    report_content += f"""

TEST CONFIGURATION
{'-'*40}
Endpoint: {URL}
Total Requests: {NUM_REQUESTS}
Concurrent Workers: {MAX_WORKERS}
Request Timeout: {TIMEOUT_SECONDS} seconds
Test Start: {datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")}
Test End: {datetime.fromtimestamp(start_time + test_duration).strftime("%Y-%m-%d %H:%M:%S")}

{'='*80}
Report generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
{'='*80}
"""

    # Write report to file
    with open(report_filename, 'w') as f:
        f.write(report_content)
    
    return report_filename, report_content

def main():
    start_time = time.time()
    print(f"Starting load test with {NUM_REQUESTS} requests using {MAX_WORKERS} workers...")
    print("Generating professional report at completion...\n")
    
    # Store all results for detailed analysis
    all_results = []
    
    # Detailed counters for different status codes
    status_counts = {}
    success_count = 0
    client_error_count = 0  # 4xx
    server_error_count = 0  # 5xx
    network_error_count = 0  # Timeouts, connection errors, etc.
    
    # Initialize progress bar
    with tqdm(total=NUM_REQUESTS, desc="Requests", unit="req") as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(make_request) for _ in range(NUM_REQUESTS)]
            
            # Process completed requests and update progress bar
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                all_results.append(result)
                status = result['status_code']
                
                # Count by status code categories
                if isinstance(status, int):
                    # Track individual status codes
                    status_counts[status] = status_counts.get(status, 0) + 1
                    
                    if 200 <= status < 300:
                        success_count += 1
                    elif 400 <= status < 500:
                        client_error_count += 1
                    elif 500 <= status < 600:
                        server_error_count += 1
                else:
                    # Network/timeout errors
                    status_counts[status] = status_counts.get(status, 0) + 1
                    network_error_count += 1
                
                # Update progress bar with status
                pbar.set_postfix({
                    "Last": status,
                    "2xx": success_count,
                    "4xx": client_error_count,
                    "5xx": server_error_count,
                    "Net": network_error_count
                })
                pbar.update(1)
    
    test_duration = time.time() - start_time
    
    # Generate professional reports
    print("\n🔄 Generating professional performance report...")
    
    try:
        chart_file = generate_charts(all_results, test_duration)
        print(f"📊 Performance charts saved: {chart_file}")
    except Exception as e:
        print(f"⚠️  Could not generate charts: {e}")
        chart_file = None
    
    try:
        report_file, _ = generate_detailed_report(all_results, test_duration, start_time)
        print(f"📋 Detailed report saved: {report_file}")
        
        # Display report in console
        print("\n" + "="*80)
        print("LOAD TEST SUMMARY REPORT")
        print("="*80)
        
        # Extract key metrics for console display
        success_rate = (success_count / NUM_REQUESTS) * 100
        avg_response_time = sum(r['response_time'] for r in all_results) / len(all_results)
        throughput = NUM_REQUESTS / test_duration
        
        print(f"✅ Success Rate: {success_rate:.1f}% ({success_count}/{NUM_REQUESTS})")
        print(f"⚡ Throughput: {throughput:.2f} requests/second")
        print(f"⏱️  Average Response Time: {avg_response_time:.3f} seconds")
        print(f"🕐 Total Test Duration: {test_duration:.2f} seconds")
        
        print("\n📁 Reports generated in 'reports/' directory:")
        if chart_file:
            print(f"   • {chart_file}")
        print(f"   • {report_file}")
        
    except Exception as e:
        print(f"⚠️  Could not generate detailed report: {e}")
        
        # Fallback basic summary
        print(f"\n{'='*60}")
        print("BASIC LOAD TEST RESULTS")
        print(f"{'='*60}")
        print(f"Total Requests: {NUM_REQUESTS}")
        print(f"Total Time: {test_duration:.2f} seconds")
        print(f"Average Rate: {NUM_REQUESTS/test_duration:.2f} requests/second")
        print("STATUS CODE BREAKDOWN:")
        print(f"  Success (2xx): {success_count}")
        print(f"  Client Errors (4xx): {client_error_count}")
        print(f"  Server Errors (5xx): {server_error_count}")
        print(f"  Network Errors: {network_error_count}")
        
        print("\nDETAILED STATUS CODES:")
        for status, count in sorted(status_counts.items(), key=lambda x: str(x[0])):
            percentage = (count / NUM_REQUESTS) * 100
            print(f"  {status}: {count} ({percentage:.1f}%)")
        
        print(f"{'='*60}")

if __name__ == '__main__':
    main()