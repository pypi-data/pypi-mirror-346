from vipentium.starter.startz import *
from vipentium.testcases.coreex import *
from datetime import datetime

# --------------------------------------------------------------
# Advanced Reporting: JSON and HTML reports
# --------------------------------------------------------------
def generate_json_report(report_file, suite_summary, results):
    # Metadata: capture when the report was generated and some environment details
    metadata = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "framework": "vipentium",
        "framework_version": "1.1.0",  # Update as needed
        "python_version": sys.version.split()[0],
        "os": os.name
    }

    # Calculate statistics from the summary
    total_tests = suite_summary.get("total", 0)
    passed_tests = suite_summary.get("passed", 0)
    failed_tests = suite_summary.get("failed", 0)
    # Calculate average duration per test if total is provided.
    average_duration = suite_summary.get("duration", 0) / total_tests if total_tests > 0 else 0
    # Calculate pass percentage.
    success_rate = f"{(passed_tests / total_tests * 100):.2f}%" if total_tests > 0 else "N/A"

    statistics = {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "average_duration": average_duration,
        "success_rate": success_rate
    }

    # Build the advanced report structure
    report = {
        "metadata": metadata,
        "summary": suite_summary,
        "statistics": statistics,
        "results": results
    }

    # Write to file using sort_keys and pretty-print formatting
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, sort_keys=True)

    print(color_text(f"Advanced JSON report generated at {report_file}", MAGENTA))



def generate_html_report(report_file, suite_summary, results):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Favicon using the VIPENTIUM SVG -->
    <link rel="icon" href="https://raw.githubusercontent.com/Suresh-pyhobbyist/vipentium/f8a137e0de4e89fc4600b08a3d3f6dd51258f06b/vipentium.svg" type="image/svg+xml">
    <title>Vipentium Report</title>
    
    <!-- Bulma CSS for modern styling -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.3/css/bulma.min.css">
    <!-- DataTables with Bulma theme -->
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.24/css/dataTables.bulma.min.css">
    <!-- AOS for animations -->
    <link href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css" rel="stylesheet">
    
    <style>
      /* Ultra modern styling */
      body {{
          background-color: #f5f5f5;
      }}
      /* Sticky navbar with gradient using the new colors */
      .navbar {{
          background: white;
          position: sticky;
          top: 0;
          z-index: 1000;
      }}
      .navbar-item, .navbar-link {{
          color: black!important;
      }}
      /* Hero Section with a smooth gradient background */
      .hero {{
          background: linear-gradient(135deg, #2BC241, #76E322);
          color: #fff;
      }}
      /* Card styling */
      .card {{
          border-radius: 12px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }}
      /* Chart container responsivity */
      .chart-container {{
          position: relative;
          margin: auto;
          height: 300px;
          width: 300px;
      }}
      /* Modal custom style */
      .modal-card {{
          border-radius: 12px;
      }}
      /* Table container for horizontal scroll */
      .table-container {{
          overflow-x: auto;
      }}
    </style>
    
    <!-- jQuery, DataTables, and Chart.js -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.24/js/dataTables.bulma.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- AOS for animations -->
    <script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
  </head>
  <body>
    <!-- Sticky Navigation Bar -->
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <a class="navbar-item" href="#">
          <img src="https://raw.githubusercontent.com/Suresh-pyhobbyist/vipentium/f8a137e0de4e89fc4600b08a3d3f6dd51258f06b/vipentium.svg" alt="vipentium" width="30" height="30">
          <span style="margin-left: 10px; font-weight: bold;">Vipentium Report</span>
        </a>
        <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div id="navMenu" class="navbar-menu">
        <div class="navbar-start">
          <a class="navbar-item" href="#summary">Summary</a>
          <a class="navbar-item" href="#overview">Overview</a>
          <a class="navbar-item" href="#details">Details</a>
        </div>
      </div>
    </nav>
    
    <!-- Hero Section: Summary Cards -->
    <section class="hero is-medium" id="summary">
      <div class="hero-body" data-aos="fade-down">
        <div class="container has-text-centered">
          <h1 class="title">Test Summary</h1>
          <div class="columns is-multiline">
            <div class="column is-one-quarter" data-aos="fade-up">
              <div class="card">
                <div class="card-content">
                  <p class="title">{suite_summary['total']}</p>
                  <p class="subtitle">Total Tests</p>
                </div>
              </div>
            </div>
            <div class="column is-one-quarter" data-aos="fade-up" data-aos-delay="100">
              <div class="card">
                <div class="card-content">
                  <p class="title" style="color:#2BC241;">{suite_summary['passed']}</p>
                  <p class="subtitle">Passed</p>
                </div>
              </div>
            </div>
            <div class="column is-one-quarter" data-aos="fade-up" data-aos-delay="200">
              <div class="card">
                <div class="card-content">
                  <p class="title has-text-danger">{suite_summary['failed']}</p>
                  <p class="subtitle">Failed</p>
                </div>
              </div>
            </div>
            <div class="column is-one-quarter" data-aos="fade-up" data-aos-delay="300">
              <div class="card">
                <div class="card-content">
                  <p class="title">{suite_summary['duration']:.2f}s</p>
                  <p class="subtitle">Total Duration</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Overview Section: Charts -->
    <section class="section" id="overview">
      <div class="container">
        <div class="columns">
          <!-- Left Column: Doughnut Chart -->
          <div class="column is-half" data-aos="fade-right">
            <h2 class="title is-4">Test Overview</h2>
            <div class="card">
              <div class="card-image">
                <div class="chart-container" style="padding:20px;">
                  <canvas id="testChart"></canvas>
                </div>
              </div>
            </div>
          </div>
          <!-- Right Column: Bar Chart Trend -->
          <div class="column is-half" data-aos="fade-left">
            <h2 class="title is-4">Pass/Fail Trend</h2>
            <div class="card">
              <div class="card-image">
                <div class="chart-container" style="padding:20px;">
                  <canvas id="trendChart"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Test Details Section -->
    <section class="section" id="details">
      <div class="container" data-aos="fade-up">
        <h2 class="title is-4">Test Details</h2>
        <div class="table-container">
          <table id="resultsTable" class="table is-striped is-hoverable is-fullwidth">
            <thead>
              <tr>
                <th>Test</th>
                <th>Status</th>
                <th>Duration (s)</th>
                <th>Message</th>
              </tr>
            </thead>
            <tbody>
    """
    # Build table rows from the test results.
    for r in results:
        safe_message = r['message'].replace('"', '&quot;')
        status = "✅ PASS" if r["success"] else "❌ FAIL"
        html += f"""              <tr class="result-row" data-message="{safe_message}">
                <td>{r['test']}</td>
                <td>{status}</td>
                <td>{r['duration']:.2f}</td>
                <td>{r['message']}</td>
              </tr>
    """
    html += f"""            </tbody>
          </table>
        </div>
      </div>
    </section>
    
    <!-- Modal for Test Detail -->
    <div class="modal" id="detailModal">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Test Detail</p>
          <button class="delete" aria-label="close" id="modalClose"></button>
        </header>
        <section class="modal-card-body">
          <p id="modalContent"></p>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-info" id="modalOk">OK</button>
        </footer>
      </div>
    </div>
    
    <!-- Footer -->
    <footer class="footer">
      <div class="content has-text-centered">
        <p>Vipentium Report - Generated on {timestamp}</p>
      </div>
    </footer>
    
    <script>
      // Initialize AOS animations.
      AOS.init();

      // Bulma navbar burger for mobile.
      document.addEventListener('DOMContentLoaded', () => {{
        const burger = document.querySelector('.navbar-burger');
        const menu = document.getElementById('navMenu');
        burger.addEventListener('click', () => {{
          burger.classList.toggle('is-active');
          menu.classList.toggle('is-active');
        }});
      }});
      
      // Initialize DataTable.
      $(document).ready(function() {{
        $('#resultsTable').DataTable({{
          "order": [[ 2, "asc" ]],
          "paging": true,
          "searching": true,
          "info": false
        }});
      }});
      
      // Chart.js Doughnut Chart for test overview.
      const ctx = document.getElementById('testChart').getContext('2d');
      const testChart = new Chart(ctx, {{
        type: 'doughnut',
        data: {{
          labels: ['Passed', 'Failed'],
          datasets: [{{
            data: [{suite_summary['passed']}, {suite_summary['failed']}],
            backgroundColor: ['#2BC241', '#ff3860'],
            borderWidth: 0
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              position: 'bottom'
            }},
            title: {{
              display: true,
              text: 'Test Results'
            }}
          }}
        }}
      }});
      
      // Chart.js Bar Chart for pass/fail trend (dummy data).
      const ctxTrend = document.getElementById('trendChart').getContext('2d');
      const trendChart = new Chart(ctxTrend, {{
        type: 'bar',
        data: {{
          labels: ['Run 1', 'Run 2', 'Run 3', 'Run 4', 'Run 5'],
          datasets: [
            {{
              label: 'Passed',
              data: [ {suite_summary['passed'] * 0.8:.0f}, {suite_summary['passed']:.0f}, {suite_summary['passed'] * 1.1:.0f}, {suite_summary['passed'] * 0.9:.0f}, {suite_summary['passed']:.0f} ],
              backgroundColor: '#2BC241'
            }},
            {{
              label: 'Failed',
              data: [ {suite_summary['failed'] * 1.1:.0f}, {suite_summary['failed']:.0f}, {suite_summary['failed'] * 0.9:.0f}, {suite_summary['failed'] * 1.2:.0f}, {suite_summary['failed']:.0f} ],
              backgroundColor: '#ff3860'
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              position: 'bottom'
            }},
            title: {{
              display: true,
              text: 'Pass/Fail Trend'
            }}
          }},
          scales: {{
            x: {{
              beginAtZero: true,
              stacked: true
            }},
            y: {{
              beginAtZero: true,
              stacked: true
            }}
          }}
        }}
      }});
      
      // Modal: Open on table row click.
      $(document).on('click', '.result-row', function() {{
        const message = $(this).data('message');
        $('#modalContent').text(message);
        $('#detailModal').addClass('is-active');
      }});
      
      // Modal: Close on clicking the close buttons.
      $('#modalClose, #modalOk').on('click', function() {{
        $('#detailModal').removeClass('is-active');
      }});
    </script>
  </body>
</html>
    """
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"HTML report generated at {report_file}")
