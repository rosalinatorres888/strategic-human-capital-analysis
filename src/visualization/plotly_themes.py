"""
Professional Plotly themes for policy analysis visualizations.
Creates consistent, publication-quality styling across all charts.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from typing import Dict, List, Optional, Any


class PolicyTheme:
    """
    Professional theme system for policy analysis visualizations
    """
    
    # Professional color palette for policy analysis
    COLORS = {
        'education': '#2E86AB',      # Professional blue
        'health': '#A23B72',         # Deep magenta  
        'nutrition': '#F18F01',      # Vibrant orange
        'poverty': '#C73E1D',        # Alert red
        'success': '#588B8B',        # Sage green
        'neutral': '#8D8D8D',        # Professional gray
        'massachusetts': '#004225',   # Massachusetts green
        'national': '#CC0000',       # National red
        'international': '#1f77b4'   # International blue
    }
    
    # Extended palette for multiple series
    EXTENDED_PALETTE = [
        '#2E86AB', '#A23B72', '#F18F01', '#588B8B', '#C73E1D',
        '#8D8D8D', '#004225', '#CC0000', '#1f77b4', '#ff7f0e',
        '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'
    ]
    
    @classmethod
    def get_layout(cls, 
                   title: str = "",
                   width: int = 1000,
                   height: int = 600,
                   font_size: int = 12,
                   show_legend: bool = True) -> Dict[str, Any]:
        """
        Get professional layout configuration
        """
        return {
            'title': {
                'text': f'<b>{title}</b>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {
                    'size': font_size + 4,
                    'family': 'Arial, sans-serif',
                    'color': '#2C3E50'
                }
            },
            'width': width,
            'height': height,
            'font': {
                'family': 'Arial, sans-serif',
                'size': font_size,
                'color': '#34495E'
            },
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'white',
            'showlegend': show_legend,
            'legend': {
                'orientation': 'h',
                'yanchor': 'top',
                'y': -0.1,
                'xanchor': 'center',
                'x': 0.5,
                'font': {'size': font_size - 1}
            },
            'margin': {'l': 80, 'r': 80, 't': 100, 'b': 80},
            'hovermode': 'closest'
        }
    
    @classmethod
    def style_axes(cls, fig: go.Figure, 
                   x_title: str = "",
                   y_title: str = "",
                   grid: bool = True) -> go.Figure:
        """
        Apply professional axis styling
        """
        fig.update_xaxes(
            title=f'<b>{x_title}</b>',
            showgrid=grid,
            gridwidth=1,
            gridcolor='rgba(128, 128, 128, 0.2)',
            showline=True,
            linewidth=1,
            linecolor='#BDC3C7',
            tickfont={'size': 11}
        )
        
        fig.update_yaxes(
            title=f'<b>{y_title}</b>',
            showgrid=grid,
            gridwidth=1,
            gridcolor='rgba(128, 128, 128, 0.2)',
            showline=True,
            linewidth=1,
            linecolor='#BDC3C7',
            tickfont={'size': 11}
        )
        
        return fig
    
    @classmethod
    def create_comparison_chart(cls,
                                data: Dict[str, List[float]],
                                categories: List[str],
                                title: str,
                                y_title: str,
                                comparison_type: str = "bar") -> go.Figure:
        """
        Create professional comparison chart
        """
        if comparison_type == "bar":
            fig = go.Figure()
            
            colors_used = []
            for i, (series_name, values) in enumerate(data.items()):
                color = cls.EXTENDED_PALETTE[i % len(cls.EXTENDED_PALETTE)]
                colors_used.append(color)
                
                fig.add_trace(go.Bar(
                    name=series_name,
                    x=categories,
                    y=values,
                    marker_color=color,
                    marker_line=dict(color='white', width=1),
                    hovertemplate=f'<b>{series_name}</b><br>' +
                                 '%{x}: %{y:.1f}<br>' +
                                 '<extra></extra>'
                ))
                
        elif comparison_type == "line":
            fig = go.Figure()
            
            for i, (series_name, values) in enumerate(data.items()):
                color = cls.EXTENDED_PALETTE[i % len(cls.EXTENDED_PALETTE)]
                
                fig.add_trace(go.Scatter(
                    name=series_name,
                    x=categories,
                    y=values,
                    mode='lines+markers',
                    line=dict(color=color, width=3),
                    marker=dict(color=color, size=8),
                    hovertemplate=f'<b>{series_name}</b><br>' +
                                 '%{x}: %{y:.1f}<br>' +
                                 '<extra></extra>'
                ))
        
        # Apply theme
        layout = cls.get_layout(title=title, height=500)
        fig.update_layout(**layout)
        fig = cls.style_axes(fig, y_title=y_title)
        
        return fig
    
    @classmethod
    def create_state_comparison(cls,
                               states: List[str],
                               massachusetts_data: List[float],
                               national_data: List[float],
                               metric: str,
                               title: str) -> go.Figure:
        """
        Create Massachusetts vs National comparison
        """
        fig = go.Figure()
        
        # Massachusetts data
        fig.add_trace(go.Bar(
            name='Massachusetts',
            x=states,
            y=massachusetts_data,
            marker_color=cls.COLORS['massachusetts'],
            marker_line=dict(color='white', width=1),
            hovertemplate='<b>Massachusetts</b><br>' +
                         '%{x}: %{y:.1f}<br>' +
                         '<extra></extra>'
        ))
        
        # National average
        fig.add_trace(go.Bar(
            name='National Average',
            x=states,
            y=national_data,
            marker_color=cls.COLORS['national'],
            marker_line=dict(color='white', width=1),
            hovertemplate='<b>National Average</b><br>' +
                         '%{x}: %{y:.1f}<br>' +
                         '<extra></extra>'
        ))
        
        # Apply theme
        layout = cls.get_layout(title=title, height=600)
        fig.update_layout(**layout)
        fig = cls.style_axes(fig, y_title=metric)
        
        return fig
        
    @classmethod  
    def create_scatter_plot(cls,
                           x_data: List[float],
                           y_data: List[float],
                           labels: List[str],
                           title: str,
                           x_title: str,
                           y_title: str,
                           size_data: Optional[List[float]] = None,
                           color_data: Optional[List[float]] = None) -> go.Figure:
        """
        Create professional scatter plot with optional sizing and coloring
        """
        fig = go.Figure()
        
        # Determine marker properties
        marker_props = {
            'size': size_data if size_data else [12] * len(x_data),
            'color': cls.COLORS['education'],
            'line': dict(color='white', width=2)
        }
        
        if color_data:
            marker_props['color'] = color_data
            marker_props['colorscale'] = 'Viridis'
            marker_props['showscale'] = True
            marker_props['colorbar'] = dict(title="Impact Score")
        
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data,
            mode='markers',
            marker=marker_props,
            text=labels,
            textposition="top center",
            hovertemplate='<b>%{text}</b><br>' +
                         f'{x_title}: %{{x:.1f}}<br>' +
                         f'{y_title}: %{{y:.1f}}<br>' +
                         '<extra></extra>'
        ))
        
        # Apply theme
        layout = cls.get_layout(title=title, height=600)
        fig.update_layout(**layout)
        fig = cls.style_axes(fig, x_title=x_title, y_title=y_title)
        
        return fig
    
    @classmethod
    def create_heatmap(cls,
                      z_data: List[List[float]],
                      x_labels: List[str],
                      y_labels: List[str], 
                      title: str,
                      color_title: str = "Value") -> go.Figure:
        """
        Create professional heatmap
        """
        fig = go.Figure(data=go.Heatmap(
            z=z_data,
            x=x_labels,
            y=y_labels,
            colorscale='RdYlBu_r',
            showscale=True,
            colorbar=dict(title=color_title),
            hoverongaps=False,
            hovertemplate='<b>%{y} vs %{x}</b><br>' +
                         f'{color_title}: %{{z:.2f}}<br>' +
                         '<extra></extra>'
        ))
        
        # Apply theme
        layout = cls.get_layout(title=title, height=500)
        fig.update_layout(**layout)
        
        return fig
    
    @classmethod
    def create_time_series(cls,
                          dates: List[str],
                          data_series: Dict[str, List[float]],
                          title: str,
                          y_title: str) -> go.Figure:
        """
        Create professional time series chart
        """
        fig = go.Figure()
        
        for i, (series_name, values) in enumerate(data_series.items()):
            color = cls.EXTENDED_PALETTE[i % len(cls.EXTENDED_PALETTE)]
            
            fig.add_trace(go.Scatter(
                name=series_name,
                x=dates,
                y=values,
                mode='lines+markers',
                line=dict(color=color, width=3),
                marker=dict(color=color, size=6),
                hovertemplate=f'<b>{series_name}</b><br>' +
                             '%{x}<br>' +
                             f'{y_title}: %{{y:.1f}}<br>' +
                             '<extra></extra>'
            ))
        
        # Apply theme
        layout = cls.get_layout(title=title, height=500)
        fig.update_layout(**layout)
        fig = cls.style_axes(fig, x_title="Year", y_title=y_title)
        
        return fig
    
    @classmethod
    def add_annotations(cls, fig: go.Figure, 
                       annotations: List[Dict[str, Any]]) -> go.Figure:
        """
        Add professional annotations to figure
        """
        for ann in annotations:
            fig.add_annotation(
                x=ann['x'],
                y=ann['y'],
                text=f"<b>{ann['text']}</b>",
                showarrow=ann.get('showarrow', True),
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor=ann.get('color', '#2C3E50'),
                font=dict(
                    size=ann.get('fontsize', 12),
                    color=ann.get('color', '#2C3E50')
                ),
                bgcolor="rgba(255, 255, 255, 0.8)",
                bordercolor=ann.get('color', '#2C3E50'),
                borderwidth=1
            )
        return fig