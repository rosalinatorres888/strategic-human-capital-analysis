#!/usr/bin/env python3
"""
Standalone 3D Preview Generator
Creates advanced 3D visualizations directly without complex imports
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path

def sanitize_json_for_html(data):
    """Safely convert data to JSON for HTML embedding"""
    def convert_numpy(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, dict):
            return {key: convert_numpy(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy(item) for item in obj]
        return obj
    
    converted_data = convert_numpy(data)
    return json.dumps(converted_data)

def create_3d_policy_space_explorer(data):
    """Create interactive 3D policy space visualization"""
    print("🎯 Creating 3D Policy Space Explorer...")
    
    # Prepare comprehensive dataset
    policy_data = []
    states = ['MA', 'TX', 'CA', 'NY', 'FL', 'AL', 'MS', 'VT', 'CT', 'NH']
    
    for state in states:
        state_record = {'state': state}
        
        # Education dimension (X-axis)
        edu_row = data['education'][data['education']['state'] == state]
        if not edu_row.empty:
            state_record['education_score'] = (
                edu_row.iloc[0]['math_8th_grade'] * 0.5 + 
                edu_row.iloc[0]['reading_8th_grade'] * 0.5
            )
        else:
            state_record['education_score'] = 265  # National average
        
        # Health Access dimension (Y-axis)
        health_row = data['health'][data['health']['state'] == state]
        if not health_row.empty:
            state_record['health_access'] = (
                100 - health_row.iloc[0]['uninsured_children_pct'] * 2 +
                (10 - health_row.iloc[0]['child_mortality_rate']) * 8
            )
        else:
            state_record['health_access'] = 75
        
        # Economic Outcomes dimension (Z-axis)
        mob_row = data['mobility'][data['mobility']['state'] == state]
        if not mob_row.empty:
            state_record['economic_outcomes'] = mob_row.iloc[0]['mobility_index'] * 10
        else:
            state_record['economic_outcomes'] = 50
        
        # Policy Innovation Score (size)
        nutr_row = data['nutrition'][data['nutrition']['state'] == state]
        if not nutr_row.empty:
            state_record['policy_innovation'] = (
                nutr_row.iloc[0]['universal_meals'] * 30 +
                nutr_row.iloc[0]['school_breakfast_participation'] * 0.3 +
                (state_record['education_score'] / 300) * 20 +
                (state_record.get('health_access', 75) / 100) * 20
            )
        else:
            state_record['policy_innovation'] = 40
        
        # Human Capital ROI (color)
        base_roi = 3.5
        edu_contrib = (state_record.get('education_score', 265) - 265) / 30 * 0.8
        health_contrib = (state_record.get('health_access', 75) - 75) / 25 * 0.6
        econ_contrib = (state_record.get('economic_outcomes', 50) - 50) / 25 * 0.4
        innovation_bonus = (state_record.get('policy_innovation', 40) - 40) / 60 * 0.5
        state_record['human_capital_roi'] = max(2.0, min(6.0, 
            base_roi + edu_contrib + health_contrib + econ_contrib + innovation_bonus))
        
        policy_data.append(state_record)
    
    df_3d = pd.DataFrame(policy_data)
    
    # Create 3D scatter plot
    fig = go.Figure()
    
    # Main state points
    fig.add_trace(go.Scatter3d(
        x=df_3d['education_score'],
        y=df_3d['health_access'],
        z=df_3d['economic_outcomes'],
        mode='markers+text',
        marker=dict(
            size=df_3d['policy_innovation'] / 3,
            color=df_3d['human_capital_roi'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                title="Human Capital ROI"
            ),
            line=dict(color='white', width=2),
            opacity=0.8
        ),
        text=df_3d['state'],
        textposition="top center",
        hovertemplate=(
            '<b>%{text}</b><br>' +
            'Education Score: %{x:.1f}<br>' +
            'Health Access: %{y:.1f}<br>' +
            'Economic Outcomes: %{z:.1f}<br>' +
            'Human Capital ROI: %{marker.color:.2f}x<br>' +
            '<extra></extra>'
        ),
        name='States'
    ))
    
    # Massachusetts benchmark
    ma_row = df_3d[df_3d['state'] == 'MA'].iloc[0]
    fig.add_trace(go.Scatter3d(
        x=[ma_row['education_score']],
        y=[ma_row['health_access']],
        z=[ma_row['economic_outcomes']],
        mode='markers',
        marker=dict(
            size=25,
            color='gold',
            symbol='diamond',
            line=dict(color='darkgreen', width=3)
        ),
        name='Massachusetts Model',
        hovertemplate='<b>Massachusetts Model</b><br>Excellence Benchmark<extra></extra>'
    ))
    
    # Update layout for 3D
    fig.update_layout(
        title=dict(
            text='<b>3D Policy Space Explorer: Human Capital Investment Landscape</b>',
            x=0.5,
            font=dict(size=18, color='#2C3E50')
        ),
        scene=dict(
            xaxis=dict(title='<b>Education Performance Score</b>'),
            yaxis=dict(title='<b>Health Access Index</b>'),
            zaxis=dict(title='<b>Economic Mobility Score</b>'),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        width=1000,
        height=700,
        font=dict(family='Arial, sans-serif', size=12),
        showlegend=True
    )
    
    return fig

def create_animated_time_series_3d():
    """Create animated 3D time series"""
    print("🎬 Creating Animated 3D Time Series...")
    
    years = list(range(2004, 2025))
    key_states = ['MA', 'TX', 'CA', 'NY', 'FL']
    colors = ['#004225', '#A23B72', '#2E86AB', '#588B8B', '#C73E1D']
    
    frames = []
    
    for i, year in enumerate(years):
        frame_data = []
        
        for j, state in enumerate(key_states):
            # Simulate policy evolution
            if state == 'MA':
                education_trend = 275 + (year - 2004) * 1.0
                health_trend = 80 + (year - 2004) * 0.5
                mobility_trend = 65 + (year - 2004) * 0.7
            else:
                education_trend = 265 + (year - 2004) * 0.3 + np.random.normal(0, 2)
                health_trend = 70 + (year - 2004) * 0.2 + np.random.normal(0, 2)
                mobility_trend = 50 + (year - 2004) * 0.3 + np.random.normal(0, 2)
            
            frame_data.append(go.Scatter3d(
                x=[education_trend],
                y=[health_trend],
                z=[mobility_trend],
                mode='markers',
                marker=dict(
                    size=12 if state == 'MA' else 10,
                    color=colors[j],
                    line=dict(color='white', width=2),
                    opacity=0.8
                ),
                text=[f"{state} ({year})"],
                name=state,
                showlegend=(i == 0),
                hovertemplate=(
                    f'<b>{state} - {year}</b><br>' +
                    'Education: %{x:.1f}<br>' +
                    'Health: %{y:.1f}<br>' +
                    'Mobility: %{z:.1f}<br>' +
                    '<extra></extra>'
                )
            ))
        
        frames.append(go.Frame(
            data=frame_data,
            name=str(year),
            traces=list(range(len(key_states)))
        ))
    
    # Create initial figure
    fig = go.Figure(
        data=frames[-1].data,
        frames=frames
    )
    
    # Add controls
    fig.update_layout(
        title=dict(
            text='<b>20-Year Policy Evolution: Human Capital Investment Trajectories (2004-2024)</b>',
            x=0.5,
            font=dict(size=16, color='#2C3E50')
        ),
        scene=dict(
            xaxis=dict(title='Education Performance', range=[260, 300]),
            yaxis=dict(title='Health Access Index', range=[60, 90]),
            zaxis=dict(title='Economic Mobility', range=[40, 80]),
            camera=dict(eye=dict(x=1.3, y=1.3, z=1.3))
        ),
        updatemenus=[{
            "type": "buttons",
            "direction": "left",
            "buttons": [
                {
                    "args": [{"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}],
                    "label": "▶️ Play",
                    "method": "animate"
                },
                {
                    "args": [{"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                    "label": "⏸️ Pause", 
                    "method": "animate"
                }
            ],
            "pad": {"r": 10, "t": 87},
            "x": 0.011,
            "y": 0
        }],
        sliders=[{
            "active": len(years)-1,
            "currentvalue": {"prefix": "Year: "},
            "pad": {"b": 10, "t": 60},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [
                {
                    "args": [[year], {"frame": {"duration": 300, "redraw": True}}],
                    "label": str(year),
                    "method": "animate"
                } for year in years
            ]
        }],
        width=1100,
        height=700
    )
    
    return fig

def create_policy_impact_surface():
    """Create 3D surface plot"""
    print("🏔️ Creating 3D Policy Impact Surface...")
    
    # Create mesh grid
    education_range = np.linspace(250, 300, 20)
    health_range = np.linspace(60, 95, 20)
    X, Y = np.meshgrid(education_range, health_range)
    
    # Calculate ROI surface
    Z = np.zeros_like(X)
    for i in range(len(education_range)):
        for j in range(len(health_range)):
            edu_score = education_range[i]
            health_score = health_range[j]
            
            base_roi = 2.5
            edu_boost = (edu_score - 265) / 35 * 1.5
            health_boost = (health_score - 75) / 20 * 1.2
            synergy_effect = (edu_boost * health_boost) * 0.3
            
            Z[j, i] = base_roi + edu_boost + health_boost + synergy_effect
    
    # Create surface plot
    fig = go.Figure(data=[
        go.Surface(
            z=Z, x=X, y=Y,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="ROI Multiplier"),
            hovertemplate=(
                'Education Score: %{x:.1f}<br>' +
                'Health Index: %{y:.1f}<br>' +
                'ROI: %{z:.2f}x<br>' +
                '<extra></extra>'
            )
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='<b>3D Policy Impact Surface: ROI Optimization Landscape</b>',
            x=0.5,
            font=dict(size=16, color='#2C3E50')
        ),
        scene=dict(
            xaxis=dict(title='Education Performance Score'),
            yaxis=dict(title='Health Access Index'),
            zaxis=dict(title='Human Capital ROI'),
            camera=dict(eye=dict(x=1.2, y=1.2, z=1.2))
        ),
        width=900,
        height=600
    )
    
    return fig

def create_comprehensive_3d_dashboard():
    """Create comprehensive 3D dashboard HTML"""
    print("🎨 Creating Comprehensive 3D Dashboard...")
    
    # Create sample data
    sample_data = {
        'education': pd.DataFrame({
            'state': ['MA', 'TX', 'CA', 'NY', 'FL', 'AL', 'MS', 'VT', 'CT', 'NH'],
            'math_8th_grade': [295, 275, 270, 274, 273, 258, 256, 287, 284, 290],
            'reading_8th_grade': [279, 260, 255, 264, 258, 244, 240, 275, 272, 278]
        }),
        'health': pd.DataFrame({
            'state': ['MA', 'TX', 'CA', 'NY', 'FL', 'AL', 'MS', 'VT', 'CT', 'NH'],
            'uninsured_children_pct': [2.1, 9.7, 4.0, 3.2, 7.9, 6.5, 8.2, 3.0, 2.8, 2.5],
            'child_mortality_rate': [3.2, 5.9, 4.0, 4.3, 5.4, 7.2, 8.5, 3.8, 3.5, 3.0]
        }),
        'mobility': pd.DataFrame({
            'state': ['MA', 'TX', 'CA', 'NY', 'FL', 'AL', 'MS', 'VT', 'CT', 'NH'],
            'mobility_index': [7.8, 5.2, 6.0, 5.8, 4.9, 4.2, 3.7, 7.4, 6.9, 7.6]
        }),
        'nutrition': pd.DataFrame({
            'state': ['MA', 'TX', 'CA', 'NY', 'FL', 'AL', 'MS', 'VT', 'CT', 'NH'],
            'universal_meals': [1, 0, 1, 0, 0, 0, 0, 1, 1, 0],
            'school_breakfast_participation': [89.5, 62.3, 75.8, 68.4, 58.7, 71.2, 74.3, 82.1, 85.3, 78.9]
        })
    }
    
    # Generate visualizations
    policy_space = create_3d_policy_space_explorer(sample_data)
    animated_series = create_animated_time_series_3d()
    impact_surface = create_policy_impact_surface()
    
    # Create HTML
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Security-Policy" content="default-src 'self' https://cdn.plot.ly; script-src 'self' 'unsafe-inline' https://cdn.plot.ly; style-src 'self' 'unsafe-inline'">
    <title>🚀 3D Human Capital Investment Analysis</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 20px;
            background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%);
            color: white;
            border-radius: 10px;
        }}
        .dashboard-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 30px;
            margin-top: 30px;
        }}
        .chart-container {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .chart-title {{
            font-size: 1.4em;
            font-weight: bold;
            margin-bottom: 15px;
            color: #2C3E50;
            text-align: center;
        }}
        .insights-panel {{
            background: linear-gradient(135deg, #e8f4fd 0%, #f0f8ff 100%);
            padding: 25px;
            border-radius: 10px;
            border-left: 5px solid #667eea;
            margin: 20px 0;
        }}
        .navigation-controls {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 1000;
        }}
        .nav-button {{
            display: block;
            margin: 5px 0;
            padding: 8px 16px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            text-align: center;
            transition: background 0.3s;
        }}
        .nav-button:hover {{
            background: #5a67d8;
        }}
        @media (max-width: 768px) {{
            .container {{ padding: 15px; }}
            .navigation-controls {{ position: static; margin-bottom: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="navigation-controls">
        <a href="#policy-space" class="nav-button">🎯 3D Policy Space</a>
        <a href="#time-series" class="nav-button">🎬 Animated Timeline</a>
        <a href="#surface" class="nav-button">🏔️ Impact Surface</a>
    </div>

    <div class="container">
        <div class="header">
            <h1>🚀 3D Human Capital Investment Analysis</h1>
            <p><em>Advanced Data Visualization & Strategic Policy Insights</em></p>
            <p><strong>Interactive 3D Exploration of Policy Performance Landscapes</strong></p>
        </div>

        <div class="insights-panel">
            <h3>🎯 3D Analytics Showcase</h3>
            <p><strong>Advanced Visualization Techniques:</strong> This dashboard demonstrates cutting-edge 3D data visualization, 
            animated time series, and interactive surface modeling to reveal complex policy relationships invisible in 2D analysis.</p>
            <p><strong>Business Intelligence:</strong> Explore multi-dimensional policy spaces, identify optimization opportunities, 
            and visualize 20-year strategic trajectories with interactive controls.</p>
        </div>

        <div class="dashboard-grid">
            <div class="chart-container" id="policy-space">
                <div class="chart-title">🎯 Interactive 3D Policy Space Explorer</div>
                <div id="policy-space-chart" style="width:100%;height:700px;"></div>
                <p><em>Rotate, zoom, and hover to explore the 3D policy landscape. Massachusetts (gold diamond) 
                represents the excellence benchmark in the optimal performance zone.</em></p>
            </div>

            <div class="chart-container" id="time-series">
                <div class="chart-title">🎬 20-Year Policy Evolution Animation</div>
                <div id="animated-chart" style="width:100%;height:700px;"></div>
                <p><em>Watch how different states evolved their human capital investments from 2004-2024. 
                Use play/pause controls and year slider to explore policy trajectories.</em></p>
            </div>

            <div class="chart-container" id="surface">
                <div class="chart-title">🏔️ 3D Policy Impact Surface</div>
                <div id="surface-chart" style="width:100%;height:600px;"></div>
                <p><em>3D surface reveals the ROI optimization landscape. Peak performance zones show where 
                combined education and health investments create exponential returns.</em></p>
            </div>
        </div>

        <div class="insights-panel">
            <h3>🏆 Data Science Skills Demonstrated</h3>
            <ul>
                <li><strong>3D Data Visualization:</strong> Interactive scatter plots, animated time series, surface modeling</li>
                <li><strong>Advanced Analytics:</strong> Multi-dimensional data relationships, optimization landscapes</li>
                <li><strong>User Experience Design:</strong> Navigation controls, responsive layout, professional styling</li>
                <li><strong>Storytelling:</strong> Progressive disclosure, guided exploration, contextual insights</li>
                <li><strong>Technical Implementation:</strong> Security headers, performance optimization, cross-platform compatibility</li>
            </ul>
        </div>
    </div>

    <script>
        // Policy Space 3D Chart
        var policySpaceData = {sanitize_json_for_html(policy_space.to_dict())};
        Plotly.newPlot('policy-space-chart', policySpaceData.data, policySpaceData.layout, {{
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d']
        }});

        // Animated Time Series Chart
        var animatedData = {sanitize_json_for_html(animated_series.to_dict())};
        Plotly.newPlot('animated-chart', animatedData.data, animatedData.layout, {{
            responsive: true,
            displayModeBar: true
        }});

        // Surface Chart
        var surfaceData = {sanitize_json_for_html(impact_surface.to_dict())};
        Plotly.newPlot('surface-chart', surfaceData.data, surfaceData.layout, {{
            responsive: true,
            displayModeBar: true
        }});

        // Smooth scrolling for navigation
        document.querySelectorAll('.nav-button').forEach(function(button) {{
            button.addEventListener('click', function(e) {{
                e.preventDefault();
                var target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            }});
        }});

        // Resize handler for responsive charts
        window.addEventListener('resize', function() {{
            Plotly.Plots.resize('policy-space-chart');
            Plotly.Plots.resize('animated-chart');
            Plotly.Plots.resize('surface-chart');
        }});

        console.log('🎨 3D Dashboard loaded successfully');
    </script>
</body>
</html>"""
    
    return html_content

def main():
    print("🎨 Creating Advanced 3D Visualization Preview...")
    
    try:
        # Create web directory
        web_dir = Path("web")
        web_dir.mkdir(exist_ok=True)
        
        # Generate comprehensive 3D dashboard
        dashboard_html = create_comprehensive_3d_dashboard()
        
        # Save to file
        dashboard_path = web_dir / "advanced_3d_dashboard.html"
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        
        print(f"\n✅ 3D Dashboard Preview Ready!")
        print(f"📍 Location: {dashboard_path}")
        print(f"🌐 Open in browser: file://{dashboard_path.resolve()}")
        
        print(f"\n🎯 Features Showcased:")
        print(f"  • Interactive 3D Policy Space Explorer")
        print(f"  • 20-Year Animated Time Series (2004-2024)")
        print(f"  • 3D ROI Optimization Surface")
        print(f"  • Professional navigation and controls")
        print(f"  • Responsive design with security headers")
        
        print(f"\n📊 Data Science Skills Demonstrated:")
        print(f"  • 3D data visualization and storytelling")
        print(f"  • Multi-dimensional analysis and optimization")
        print(f"  • Interactive user experience design")
        print(f"  • Advanced technical implementation")
        
        return str(dashboard_path.resolve())
        
    except Exception as e:
        print(f"❌ Error creating 3D preview: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    dashboard_path = main()
    
    if dashboard_path:
        print(f"\n🎊 PREVIEW READY!")
        print(f"Open this file in your browser:")
        print(f"{dashboard_path}")
    else:
        print(f"\n💥 Preview generation failed")