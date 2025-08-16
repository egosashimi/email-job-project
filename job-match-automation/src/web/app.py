"""
Web interface for job match automation.
Provides a simple web interface to view job matches and update application status.
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import sys
import sqlite3
from datetime import datetime, timedelta

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from storage.database import DatabaseManager

# Create Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize database manager
db = DatabaseManager()


@app.route('/')
def index():
    """Main page showing recent job matches."""
    # Get filter parameters
    days = request.args.get('days', 7, type=int)
    min_match = request.args.get('min_match', 0, type=int)
    recommendation = request.args.get('recommendation', '')
    
    # Calculate date filter
    since_date = datetime.now() - timedelta(days=days)
    
    # Query database for recent matches
    try:
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            
            # Build query with filters
            query = '''
                SELECT j.*, a.match_percentage, a.recommendation, a.reasoning, ap.status
                FROM jobs j
                LEFT JOIN analyses a ON j.id = a.job_id
                LEFT JOIN applications ap ON j.id = ap.job_id
                WHERE j.discovered_at > ?
            '''
            params = [since_date.isoformat()]
            
            if min_match > 0:
                query += ' AND a.match_percentage >= ?'
                params.append(min_match)
            
            if recommendation:
                query += ' AND a.recommendation = ?'
                params.append(recommendation)
            
            query += ' ORDER BY j.discovered_at DESC LIMIT 50'
            
            cursor.execute(query, params)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            jobs = [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"Error querying database: {e}")
        jobs = []
    
    # Get unique recommendations for filter dropdown
    recommendations = ['STRONG_MATCH', 'POSSIBLE_MATCH', 'REACH', 'SKIP']
    
    return render_template('index.html', 
                         jobs=jobs, 
                         days=days, 
                         min_match=min_match, 
                         recommendation=recommendation,
                         recommendations=recommendations)


@app.route('/job/<job_id>')
def job_details(job_id):
    """Show details for a specific job."""
    try:
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            
            # Get job details
            cursor.execute('''
                SELECT j.*, a.match_percentage, a.strengths, a.weaknesses, 
                       a.hidden_opportunities, a.red_flags, a.recommendation, a.reasoning,
                       ap.status, ap.notes
                FROM jobs j
                LEFT JOIN analyses a ON j.id = a.job_id
                LEFT JOIN applications ap ON j.id = ap.job_id
                WHERE j.id = ?
            ''', (job_id,))
            
            columns = [description[0] for description in cursor.description]
            row = cursor.fetchone()
            
            if row:
                job = dict(zip(columns, row))
                # Parse JSON fields
                import json
                for field in ['strengths', 'weaknesses', 'hidden_opportunities', 'red_flags']:
                    if job[field]:
                        try:
                            job[field] = json.loads(job[field])
                        except:
                            job[field] = []
            else:
                job = None
    except Exception as e:
        print(f"Error querying database: {e}")
        job = None
    
    return render_template('job_details.html', job=job)


@app.route('/update_status', methods=['POST'])
def update_status():
    """Update application status for a job."""
    job_id = request.form.get('job_id')
    status = request.form.get('status')
    notes = request.form.get('notes', '')
    
    if not job_id or not status:
        return jsonify({'success': False, 'error': 'Missing job_id or status'})
    
    try:
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if application record exists
            cursor.execute('SELECT id FROM applications WHERE job_id = ?', (job_id,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record
                cursor.execute('''
                    UPDATE applications 
                    SET status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE job_id = ?
                ''', (status, notes, job_id))
            else:
                # Create new record
                cursor.execute('''
                    INSERT INTO applications (job_id, status, notes, applied_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ''', (job_id, status, notes))
            
            conn.commit()
            
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error updating status: {e}")
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics."""
    try:
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            
            # Get total jobs
            cursor.execute('SELECT COUNT(*) FROM jobs')
            total_jobs = cursor.fetchone()[0]
            
            # Get recent jobs (last 7 days)
            since_date = datetime.now() - timedelta(days=7)
            cursor.execute('SELECT COUNT(*) FROM jobs WHERE discovered_at > ?', (since_date.isoformat(),))
            recent_jobs = cursor.fetchone()[0]
            
            # Get match distribution
            cursor.execute('''
                SELECT a.recommendation, COUNT(*) 
                FROM analyses a
                JOIN jobs j ON a.job_id = j.id
                WHERE j.discovered_at > ?
                GROUP BY a.recommendation
            ''', (since_date.isoformat(),))
            match_distribution = dict(cursor.fetchall())
            
            # Get application status distribution
            cursor.execute('''
                SELECT ap.status, COUNT(*) 
                FROM applications ap
                JOIN jobs j ON ap.job_id = j.id
                WHERE j.discovered_at > ?
                GROUP BY ap.status
            ''', (since_date.isoformat(),))
            application_distribution = dict(cursor.fetchall())
            
            stats = {
                'total_jobs': total_jobs,
                'recent_jobs': recent_jobs,
                'match_distribution': match_distribution,
                'application_distribution': application_distribution
            }
            
            return jsonify(stats)
    except Exception as e:
        print(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/stats')
def stats():
    """Statistics page."""
    return render_template('stats.html')


# Create templates directory and basic templates
def create_templates():
    """Create basic HTML templates."""
    # Create templates directory
    os.makedirs('src/web/templates', exist_ok=True)
    os.makedirs('src/web/static', exist_ok=True)
    
    # Create base template
    base_template = '''<!DOCTYPE html>
<html>
<head>
    <title>Job Match Automation</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="{{ url_for('index') }}">Job Match Automation</a>
            <div class="navbar-nav">
                <a class="nav-link" href="{{ url_for('index') }}">Jobs</a>
                <a class="nav-link" href="{{ url_for('stats') }}">Stats</a>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>'''
    
    # Create index template
    index_template = '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-md-12">
        <h1>Job Matches</h1>
        
        <div class="card mb-4">
            <div class="card-body">
                <form method="GET" class="row g-3">
                    <div class="col-md-3">
                        <label for="days" class="form-label">Days Back</label>
                        <select class="form-select" id="days" name="days">
                            <option value="1" {% if days == 1 %}selected{% endif %}>1 Day</option>
                            <option value="7" {% if days == 7 %}selected{% endif %}>7 Days</option>
                            <option value="30" {% if days == 30 %}selected{% endif %}>30 Days</option>
                            <option value="90" {% if days == 90 %}selected{% endif %}>90 Days</option>
                        </select>
                    </div>
                    
                    <div class="col-md-3">
                        <label for="min_match" class="form-label">Min Match %</label>
                        <select class="form-select" id="min_match" name="min_match">
                            <option value="0" {% if min_match == 0 %}selected{% endif %}>All</option>
                            <option value="60" {% if min_match == 60 %}selected{% endif %}>60%+</option>
                            <option value="70" {% if min_match == 70 %}selected{% endif %}>70%+</option>
                            <option value="80" {% if min_match == 80 %}selected{% endif %}>80%+</option>
                        </select>
                    </div>
                    
                    <div class="col-md-3">
                        <label for="recommendation" class="form-label">Recommendation</label>
                        <select class="form-select" id="recommendation" name="recommendation">
                            <option value="">All</option>
                            {% for rec in recommendations %}
                            <option value="{{ rec }}" {% if recommendation == rec %}selected{% endif %}>{{ rec }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="col-md-3">
                        <label class="form-label">&nbsp;</label>
                        <div>
                            <button type="submit" class="btn btn-primary">Filter</button>
                            <a href="{{ url_for('index') }}" class="btn btn-secondary">Clear</a>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        
        <div class="row">
            {% for job in jobs %}
            <div class="col-md-12 mb-3">
                <div class="card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <h5 class="card-title">
                                <a href="{{ url_for('job_details', job_id=job.id) }}">{{ job.company }} - {{ job.title }}</a>
                            </h5>
                            <span class="badge bg-{% if job.recommendation == 'STRONG_MATCH' %}success{% elif job.recommendation == 'POSSIBLE_MATCH' %}warning{% elif job.recommendation == 'REACH' %}info{% else %}secondary{% endif %}">
                                {{ job.match_percentage }}% - {{ job.recommendation }}
                            </span>
                        </div>
                        <p class="card-text">
                            <small class="text-muted">
                                {{ job.source }} • {{ job.discovered_at }}
                            </small>
                        </p>
                        <p class="card-text">
                            {{ job.description[:200] }}{% if job.description|length > 200 %}...{% endif %}
                        </p>
                        <a href="{{ job.url }}" class="btn btn-outline-primary" target="_blank">View Job</a>
                        <a href="{{ url_for('job_details', job_id=job.id) }}" class="btn btn-outline-secondary">Details</a>
                    </div>
                </div>
            </div>
            {% else %}
            <div class="col-md-12">
                <div class="alert alert-info">
                    No job matches found with the current filters.
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}'''
    
    # Create job details template
    job_details_template = '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-md-12">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="{{ url_for('index') }}">Jobs</a></li>
                <li class="breadcrumb-item active">{{ job.company }} - {{ job.title }}</li>
            </ol>
        </nav>
        
        <div class="row">
            <div class="col-md-8">
                <h1>{{ job.company }} - {{ job.title }}</h1>
                
                <div class="card mb-4">
                    <div class="card-header">
                        <div class="d-flex justify-content-between align-items-center">
                            <span>Job Details</span>
                            <span class="badge bg-{% if job.recommendation == 'STRONG_MATCH' %}success{% elif job.recommendation == 'POSSIBLE_MATCH' %}warning{% elif job.recommendation == 'REACH' %}info{% else %}secondary{% endif %}">
                                {{ job.match_percentage }}% - {{ job.recommendation }}
                            </span>
                        </div>
                    </div>
                    <div class="card-body">
                        <dl class="row">
                            <dt class="col-sm-3">Company</dt>
                            <dd class="col-sm-9">{{ job.company }}</dd>
                            
                            <dt class="col-sm-3">Source</dt>
                            <dd class="col-sm-9">{{ job.source }}</dd>
                            
                            <dt class="col-sm-3">Location</dt>
                            <dd class="col-sm-9">{{ job.location }}</dd>
                            
                            <dt class="col-sm-3">Remote</dt>
                            <dd class="col-sm-9">{{ 'Yes' if job.remote_option else 'No' }}</dd>
                            
                            <dt class="col-sm-3">Salary</dt>
                            <dd class="col-sm-9">
                                {% if job.salary_min and job.salary_max %}
                                    ${{ job.salary_min|int|format_thousands }} - ${{ job.salary_max|int|format_thousands }}
                                {% elif job.salary_min %}
                                    From ${{ job.salary_min|int|format_thousands }}
                                {% elif job.salary_max %}
                                    Up to ${{ job.salary_max|int|format_thousands }}
                                {% else %}
                                    Not specified
                                {% endif %}
                            </dd>
                            
                            <dt class="col-sm-3">Experience</dt>
                            <dd class="col-sm-9">
                                {% if job.experience_years %}
                                    {{ job.experience_years }} years
                                {% else %}
                                    Not specified
                                {% endif %}
                            </dd>
                        </dl>
                        
                        <h5>Description</h5>
                        <p>{{ job.description }}</p>
                        
                        <a href="{{ job.url }}" class="btn btn-primary" target="_blank">View Original Job Posting</a>
                    </div>
                </div>
                
                {% if job.strengths or job.weaknesses %}
                <div class="card mb-4">
                    <div class="card-header">Analysis</div>
                    <div class="card-body">
                        {% if job.strengths %}
                        <h5>Strengths</h5>
                        <ul>
                            {% for strength in job.strengths %}
                            <li>{{ strength }}</li>
                            {% endfor %}
                        </ul>
                        {% endif %}
                        
                        {% if job.weaknesses %}
                        <h5>Weaknesses</h5>
                        <ul>
                            {% for weakness in job.weaknesses %}
                            <li>{{ weakness }}</li>
                            {% endfor %}
                        </ul>
                        {% endif %}
                        
                        {% if job.hidden_opportunities %}
                        <h5>Hidden Opportunities</h5>
                        <ul>
                            {% for opportunity in job.hidden_opportunities %}
                            <li>{{ opportunity }}</li>
                            {% endfor %}
                        </ul>
                        {% endif %}
                        
                        {% if job.red_flags %}
                        <h5>Red Flags</h5>
                        <ul>
                            {% for flag in job.red_flags %}
                            <li>{{ flag }}</li>
                            {% endfor %}
                        </ul>
                        {% endif %}
                        
                        <h5>Reasoning</h5>
                        <p>{{ job.reasoning }}</p>
                    </div>
                </div>
                {% endif %}
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">Application Status</div>
                    <div class="card-body">
                        <form id="statusForm">
                            <input type="hidden" name="job_id" value="{{ job.id }}">
                            
                            <div class="mb-3">
                                <label for="status" class="form-label">Status</label>
                                <select class="form-select" id="status" name="status">
                                    <option value="PENDING" {% if job.status == 'PENDING' %}selected{% endif %}>Pending</option>
                                    <option value="APPLIED" {% if job.status == 'APPLIED' %}selected{% endif %}>Applied</option>
                                    <option value="REJECTED" {% if job.status == 'REJECTED' %}selected{% endif %}>Rejected</option>
                                    <option value="INTERVIEW" {% if job.status == 'INTERVIEW' %}selected{% endif %}>Interview</option>
                                    <option value="OFFER" {% if job.status == 'OFFER' %}selected{% endif %}>Offer</option>
                                </select>
                            </div>
                            
                            <div class="mb-3">
                                <label for="notes" class="form-label">Notes</label>
                                <textarea class="form-control" id="notes" name="notes" rows="3">{{ job.notes }}</textarea>
                            </div>
                            
                            <button type="submit" class="btn btn-primary">Update Status</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
document.getElementById('statusForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('{{ url_for("update_status") }}', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Status updated successfully!');
        } else {
            alert('Error updating status: ' + data.error);
        }
    })
    .catch(error => {
        alert('Error updating status: ' + error);
    });
});
</script>
{% endblock %}'''
    
    # Create stats template
    stats_template = '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-md-12">
        <h1>Statistics</h1>
        
        <div class="row" id="stats-container">
            <div class="col-md-12">
                <div class="alert alert-info">
                    Loading statistics...
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
fetch('{{ url_for("api_stats") }}')
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('stats-container');
        container.innerHTML = `
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Total Jobs</h5>
                        <p class="card-text display-4">${data.total_jobs}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Recent Jobs (7 days)</h5>
                        <p class="card-text display-4">${data.recent_jobs}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Application Status</h5>
                        <ul class="list-group">
                            ${Object.entries(data.application_distribution).map(([status, count]) => 
                                `<li class="list-group-item d-flex justify-content-between align-items-center">
                                    ${status}
                                    <span class="badge bg-primary rounded-pill">${count}</span>
                                </li>`
                            ).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        `;
    })
    .catch(error => {
        document.getElementById('stats-container').innerHTML = 
            `<div class="col-md-12">
                <div class="alert alert-danger">
                    Error loading statistics: ${error}
                </div>
            </div>`;
    });
</script>
{% endblock %}'''
    
    # Write templates to files
    with open('src/web/templates/base.html', 'w') as f:
        f.write(base_template)
    
    with open('src/web/templates/index.html', 'w') as f:
        f.write(index_template)
    
    with open('src/web/templates/job_details.html', 'w') as f:
        f.write(job_details_template)
    
    with open('src/web/templates/stats.html', 'w') as f:
        f.write(stats_template)


# Add template filter for formatting numbers
@app.template_filter('format_thousands')
def format_thousands(value):
    """Format number with thousands separator."""
    try:
        return f"{int(value):,}"
    except:
        return value


def main():
    """Run the web interface."""
    # Create templates
    create_templates()
    
    # Run the Flask app
    app.run(host='127.0.0.1', port=5000, debug=True)


if __name__ == "__main__":
    main()