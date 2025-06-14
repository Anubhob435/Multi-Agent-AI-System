# web_interface.py
# Interactive Web UI for Multi-Agent AI System

from flask import Flask, render_template, request, jsonify, stream_template
import json
import time
from main import run_goal
from automated_evaluation import AgentSystemEvaluator

app = Flask(__name__)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/run_goal', methods=['POST'])
def api_run_goal():
    """API endpoint to run a goal"""
    try:
        data = request.json
        goal = data.get('goal', '')
        
        if not goal:
            return jsonify({'error': 'Goal is required'}), 400
        
        # Run the goal
        result = run_goal(goal)
        
        return jsonify({
            'success': True,
            'result': result,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/evaluate', methods=['POST'])
def api_evaluate():
    """API endpoint to run full evaluation"""
    try:
        evaluator = AgentSystemEvaluator()
        results = evaluator.run_full_evaluation()
        
        return jsonify({
            'success': True,
            'evaluation': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/agent_status')
def agent_status():
    """Get system status and metrics"""
    try:
        # Load latest evaluation results
        import os
        import glob
        
        eval_files = glob.glob('evals/evaluation_results_*.json')
        latest_eval = None
        
        if eval_files:
            latest_file = max(eval_files, key=os.path.getctime)
            with open(latest_file, 'r') as f:
                latest_eval = json.load(f)
        
        return jsonify({
            'status': 'active',
            'latest_evaluation': latest_eval,
            'available_agents': [
                'spacex_agent',
                'weather_agent', 
                'summary_agent',
                'google_adk_agent'
            ]
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
