"""
Interactive dashboard components for development economics analysis.
Creates compelling, interactive visualizations that tell the policy story.
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from datetime import datetime

from .plotly_themes import PolicyTheme
from ..utils.security import sanitize_json_for_html, safe_file_write


class PolicyDashboard:
    """
    Interactive dashboard creator for policy analysis
    """
    
    def __init__(self, data_dict: Dict[str, pd.DataFrame]):
        self.data = data_dict
        self.theme = PolicyTheme()
        
    def create_education_impact_dashboard(self) -> go.Figure:
        """
        Create comprehensive education impact analysis dashboard
        """
        # Get education data
        education_df = self.data.get('education', pd.DataFrame())
        mobility_df = self.data.get('mobility', pd.DataFrame())
        
        if education_df.empty or mobility_df.empty:
            raise ValueError("Education and mobility data required")
        
        # Create subplot structure
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'NAEP Scores: Massachusetts vs National Average',
                'Economic Mobility by State',
                'Education Performance vs Economic Outcomes',
                'Policy Impact Correlation Matrix'
            ),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "scatter"}, {"type": "heatmap"}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Chart 1: NAEP Scores Comparison
        ma_data = education_df[education_df['state'] == 'MA'].iloc[0]
        national_avg_math = education_df['math_8th_grade'].mean()
        national_avg_reading = education_df['reading_8th_grade'].mean()
        
        categories = ['Math (8th Grade)', 'Reading (8th Grade)']
        ma_scores = [ma_data['math_8th_grade'], ma_data['reading_8th_grade']]
        national_scores = [national_avg_math, national_avg_reading]
        
        fig.add_trace(
            go.Bar(
                name='Massachusetts',
                x=categories,
                y=ma_scores,
                marker_color=self.theme.COLORS['massachusetts'],
                showlegend=True
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                name='National Average',
                x=categories,
                y=national_scores,
                marker_color=self.theme.COLORS['national'],
                showlegend=True
            ),
            row=1, col=1
        )
        
        # Chart 2: Economic Mobility by State
        mobility_sorted = mobility_df.sort_values('mobility_index', ascending=True)
        
        colors = [self.theme.COLORS['massachusetts'] if state == 'MA' 
                 else self.theme.COLORS['neutral'] 
                 for state in mobility_sorted['state']]
        
        fig.add_trace(
            go.Bar(
                name='Economic Mobility Index',
                x=mobility_sorted['state'],
                y=mobility_sorted['mobility_index'],
                marker_color=colors,
                showlegend=False,
                hovertemplate='<b>%{x}</b><br>Mobility Index: %{y:.1f}<extra></extra>'
            ),
            row=1, col=2
        )
        
        # Chart 3: Education vs Economic Outcomes Scatter
        merged_data = pd.merge(education_df, mobility_df, on='state', how='inner')
        
        fig.add_trace(
            go.Scatter(
                name='States',
                x=merged_data['math_8th_grade'],
                y=merged_data['mobility_index'],
                mode='markers+text',
                marker=dict(
                    size=12,
                    color=[self.theme.COLORS['massachusetts'] if state == 'MA' 
                          else self.theme.COLORS['education'] 
                          for state in merged_data['state']],
                    line=dict(color='white', width=2)
                ),
                text=merged_data['state'],
                textposition='top center',
                showlegend=False,
                hovertemplate='<b>%{text}</b><br>Math Score: %{x}<br>Mobility: %{y:.1f}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # Chart 4: Correlation Heatmap
        if len(merged_data) > 3:  # Need sufficient data for correlations
            corr_data = merged_data[['math_8th_grade', 'reading_8th_grade', 'mobility_index', 'income_25th_percentile']].corr()
            
            fig.add_trace(
                go.Heatmap(
                    z=corr_data.values,
                    x=['Math Score', 'Reading Score', 'Mobility', 'Income 25th %ile'],
                    y=['Math Score', 'Reading Score', 'Mobility', 'Income 25th %ile'],
                    colorscale='RdYlBu_r',
                    showscale=True,
                    name='Correlations',
                    hovertemplate='<b>%{y} vs %{x}</b><br>Correlation: %{z:.2f}<extra></extra>'
                ),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text='<b>Strategic Human Capital Investment: Massachusetts Model vs Current National Policies</b>',
                x=0.5,
                font=dict(size=18, color='#2C3E50')
            ),
            height=800,
            width=1200,
            showlegend=True,
            legend=dict(orientation='h', yanchor='top', y=-0.05, xanchor='center', x=0.5),
            font=dict(family='Arial, sans-serif', size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white'
        )
        
        # Update axes
        fig.update_xaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
        
        return fig
        
    def create_policy_comparison_dashboard(self) -> go.Figure:
        """
        Create comprehensive policy comparison dashboard
        """
        # Combine data for analysis
        all_data = []
        
        for state in ['MA', 'TX', 'CA', 'NY', 'FL']:
            state_data = {'state': state}
            
            # Education data
            if 'education' in self.data:
                edu_row = self.data['education'][self.data['education']['state'] == state]
                if not edu_row.empty:
                    state_data['math_score'] = edu_row.iloc[0]['math_8th_grade']
                    state_data['reading_score'] = edu_row.iloc[0]['reading_8th_grade']
            
            # Mobility data  
            if 'mobility' in self.data:
                mob_row = self.data['mobility'][self.data['mobility']['state'] == state]
                if not mob_row.empty:
                    state_data['mobility_index'] = mob_row.iloc[0]['mobility_index']
            
            # Health data
            if 'health' in self.data:
                health_row = self.data['health'][self.data['health']['state'] == state]
                if not health_row.empty:
                    state_data['child_mortality'] = health_row.iloc[0]['child_mortality_rate']
                    state_data['uninsured_children'] = health_row.iloc[0]['uninsured_children_pct']
            
            # Nutrition data
            if 'nutrition' in self.data:
                nutr_row = self.data['nutrition'][self.data['nutrition']['state'] == state]
                if not nutr_row.empty:
                    state_data['free_lunch_eligible'] = nutr_row.iloc[0]['free_lunch_eligible_pct']
                    state_data['universal_meals'] = nutr_row.iloc[0]['universal_meals']
            
            if len(state_data) > 1:  # More than just state name
                all_data.append(state_data)
        
        df = pd.DataFrame(all_data)
        
        if df.empty:
            raise ValueError("No data available for dashboard creation")
        
        # Create 2x2 dashboard
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Academic Performance by State',
                'Health Outcomes vs Policy Investment',
                'Universal Programs Impact',
                'Comprehensive Policy Effectiveness'
            ),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "scatter"}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Chart 1: Academic Performance
        if 'math_score' in df.columns and 'reading_score' in df.columns:
            fig.add_trace(
                go.Bar(
                    name='Math Score',
                    x=df['state'],
                    y=df['math_score'],
                    marker_color=self.theme.COLORS['education'],
                    showlegend=True
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Bar(
                    name='Reading Score',
                    x=df['state'],
                    y=df['reading_score'],
                    marker_color=self.theme.COLORS['success'],
                    showlegend=True
                ),
                row=1, col=1
            )
        
        # Chart 2: Health vs Investment
        if 'child_mortality' in df.columns and 'uninsured_children' in df.columns:
            fig.add_trace(
                go.Scatter(
                    name='Health Outcomes',
                    x=df['uninsured_children'],
                    y=df['child_mortality'],
                    mode='markers+text',
                    marker=dict(
                        size=15,
                        color=[self.theme.COLORS['massachusetts'] if state == 'MA' 
                              else self.theme.COLORS['health'] for state in df['state']],
                        line=dict(color='white', width=2)
                    ),
                    text=df['state'],
                    textposition='top center',
                    showlegend=False,
                    hovertemplate='<b>%{text}</b><br>Uninsured: %{x:.1f}%<br>Child Mortality: %{y:.1f}<extra></extra>'
                ),
                row=1, col=2
            )
        
        # Chart 3: Universal Programs Impact
        if 'universal_meals' in df.columns and 'free_lunch_eligible' in df.columns:
            universal_states = df[df['universal_meals'] == 1]
            non_universal_states = df[df['universal_meals'] == 0]
            
            fig.add_trace(
                go.Bar(
                    name='Universal Meal States',
                    x=universal_states['state'],
                    y=universal_states['free_lunch_eligible'],
                    marker_color=self.theme.COLORS['success'],
                    showlegend=True
                ),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Bar(
                    name='Non-Universal States',
                    x=non_universal_states['state'],
                    y=non_universal_states['free_lunch_eligible'],
                    marker_color=self.theme.COLORS['poverty'],
                    showlegend=True
                ),
                row=2, col=1
            )
        
        # Chart 4: Comprehensive Effectiveness
        if 'mobility_index' in df.columns and 'math_score' in df.columns:
            # Create comprehensive policy score
            df['policy_score'] = (
                df['math_score'] / df['math_score'].max() * 0.3 +
                (df['mobility_index'] / df['mobility_index'].max()) * 0.3 +
                ((100 - df['uninsured_children']) / 100 if 'uninsured_children' in df.columns else 0) * 0.2 +
                (df['universal_meals'] if 'universal_meals' in df.columns else 0) * 0.2
            ) * 100
            
            fig.add_trace(
                go.Scatter(
                    name='Policy Effectiveness',
                    x=df['state'],
                    y=df['policy_score'],
                    mode='markers+lines',
                    marker=dict(
                        size=15,
                        color=df['policy_score'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Policy Score", x=1.1)
                    ),
                    line=dict(color=self.theme.COLORS['education'], width=3),
                    showlegend=False,
                    hovertemplate='<b>%{x}</b><br>Policy Score: %{y:.1f}<extra></extra>'
                ),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text='<b>Human Capital ROI Analysis: Evidence-Based Investment Strategy vs Status Quo</b>',
                x=0.5,
                font=dict(size=18, color='#2C3E50')
            ),
            height=800,
            width=1200,
            showlegend=True,
            legend=dict(orientation='h', yanchor='top', y=-0.05, xanchor='center', x=0.5),
            font=dict(family='Arial, sans-serif', size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white'
        )
        
        # Update axes
        fig.update_xaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
        
        return fig
        
    def create_international_comparison_dashboard(self) -> go.Figure:
        """
        Create international comparison dashboard
        """
        intl_df = self.data.get('international', pd.DataFrame())
        
        if intl_df.empty:
            raise ValueError("International data required")
        
        # Create comparative analysis
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Education Investment vs Child Poverty',
                'PISA Performance Comparison',
                'Social Mobility International Ranking',
                'Massachusetts in Global Context'
            ),
            specs=[[{"type": "scatter"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "scatter"}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Chart 1: Investment vs Poverty
        colors = [self.theme.COLORS['massachusetts'] if country == 'Massachusetts' 
                 else self.theme.COLORS['international'] 
                 for country in intl_df['country']]
        
        fig.add_trace(
            go.Scatter(
                name='Countries/States',
                x=intl_df['education_spending_gdp'],
                y=intl_df['child_poverty_rate'],
                mode='markers+text',
                marker=dict(size=12, color=colors, line=dict(color='white', width=2)),
                text=intl_df['country'],
                textposition='top center',
                showlegend=False,
                hovertemplate='<b>%{text}</b><br>Education Spending: %{x:.1f}% GDP<br>Child Poverty: %{y:.1f}%<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Chart 2: PISA Performance
        sorted_pisa = intl_df.sort_values('pisa_math_score', ascending=True)
        colors_pisa = [self.theme.COLORS['massachusetts'] if country == 'Massachusetts' 
                      else self.theme.COLORS['international'] 
                      for country in sorted_pisa['country']]
        
        fig.add_trace(
            go.Bar(
                name='PISA Math Score',
                x=sorted_pisa['country'],
                y=sorted_pisa['pisa_math_score'],
                marker_color=colors_pisa,
                showlegend=False,
                hovertemplate='<b>%{x}</b><br>PISA Score: %{y}<extra></extra>'
            ),
            row=1, col=2
        )
        
        # Chart 3: Social Mobility
        sorted_mobility = intl_df.sort_values('social_mobility_index', ascending=False)
        colors_mobility = [self.theme.COLORS['massachusetts'] if country == 'Massachusetts' 
                          else self.theme.COLORS['international'] 
                          for country in sorted_mobility['country']]
        
        fig.add_trace(
            go.Bar(
                name='Social Mobility',
                x=sorted_mobility['country'],
                y=sorted_mobility['social_mobility_index'],
                marker_color=colors_mobility,
                showlegend=False,
                hovertemplate='<b>%{x}</b><br>Mobility Index: %{y:.1f}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # Chart 4: Massachusetts Global Context
        ma_row = intl_df[intl_df['country'] == 'Massachusetts'].iloc[0]
        
        metrics = ['Education Spending\n(% GDP)', 'Child Poverty\nRate (%)', 
                  'PISA Math\nScore', 'Social Mobility\nIndex']
        ma_values = [ma_row['education_spending_gdp'], ma_row['child_poverty_rate'],
                    ma_row['pisa_math_score'], ma_row['social_mobility_index']]
        global_avg = [intl_df['education_spending_gdp'].mean(), 
                     intl_df['child_poverty_rate'].mean(),
                     intl_df['pisa_math_score'].mean(), 
                     intl_df['social_mobility_index'].mean()]
        
        fig.add_trace(
            go.Bar(
                name='Massachusetts',
                x=metrics,
                y=ma_values,
                marker_color=self.theme.COLORS['massachusetts'],
                showlegend=True
            ),
            row=2, col=2
        )
        
        fig.add_trace(
            go.Bar(
                name='International Average',
                x=metrics,
                y=global_avg,
                marker_color=self.theme.COLORS['international'],
                showlegend=True
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text='<b>Global Human Capital Investment Benchmarks: Strategic Policy Performance</b>',
                x=0.5,
                font=dict(size=18, color='#2C3E50')
            ),
            height=800,
            width=1200,
            showlegend=True,
            legend=dict(orientation='h', yanchor='top', y=-0.05, xanchor='center', x=0.5),
            font=dict(family='Arial, sans-serif', size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white'
        )
        
        # Update axes
        fig.update_xaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
        
        return fig
    
    def export_to_html(self, fig: go.Figure, filename: str, output_dir: str = "web") -> bool:
        """
        Export figure to secure HTML file
        """
        try:
            # Generate HTML with security measures
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Security-Policy" content="default-src 'self' https://cdn.plot.ly; script-src 'self' 'unsafe-inline' https://cdn.plot.ly; style-src 'self' 'unsafe-inline'">
    <meta http-equiv="X-Content-Type-Options" content="nosniff">
    <meta http-equiv="X-Frame-Options" content="DENY">
    <title>Development Economics Analysis - {filename}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            margin: 20px; 
            background-color: #f8f9fa; 
        }}
        .container {{ 
            max-width: 1400px; 
            margin: 0 auto; 
            background: white; 
            padding: 20px; 
            border-radius: 10px; 
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
        }}
        .header {{ 
            text-align: center; 
            margin-bottom: 30px; 
            color: #2C3E50; 
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Development Economics Policy Analysis</h1>
            <p><em>Evidence-based insights for poverty reduction</em></p>
        </div>
        <div id="plotly-div" style="width:100%;height:800px;"></div>
    </div>
    
    <script>
        var plotly_data = {sanitize_json_for_html(fig.to_dict())};
        Plotly.newPlot('plotly-div', plotly_data.data, plotly_data.layout, {{responsive: true}});
    </script>
</body>
</html>
"""
            
            # Save securely
            from pathlib import Path
            output_path = Path(output_dir) / f"{filename}.html"
            return safe_file_write(output_path, html_content)
            
        except Exception as e:
            print(f"Error exporting to HTML: {e}")
            return False