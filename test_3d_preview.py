#!/usr/bin/env python3
"""
Test Preview Script for Advanced 3D Visualizations
Creates sample data and generates 3D dashboard for preview
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from visualization.advanced_3d import Advanced3DVisualizer

def create_sample_data():
    """Create sample data for testing 3D visualizations"""
    
    # Sample education data
    education_data = pd.DataFrame({
        'state': ['MA', 'TX', 'CA', 'NY', 'FL', 'AL', 'MS', 'VT', 'CT', 'NH'],
        'math_8th_grade': [295, 275, 270, 274, 273, 258, 256, 287, 284, 290],
        'reading_8th_grade': [279, 260, 255, 264, 258, 244, 240, 275, 272, 278]
    })
    
    # Sample health data
    health_data = pd.DataFrame({
        'state': ['MA', 'TX', 'CA', 'NY', 'FL', 'AL', 'MS', 'VT', 'CT', 'NH'],
        'uninsured_children_pct': [2.1, 9.7, 4.0, 3.2, 7.9, 6.5, 8.2, 3.0, 2.8, 2.5],
        'child_mortality_rate': [3.2, 5.9, 4.0, 4.3, 5.4, 7.2, 8.5, 3.8, 3.5, 3.0]
    })
    
    # Sample mobility data
    mobility_data = pd.DataFrame({
        'state': ['MA', 'TX', 'CA', 'NY', 'FL', 'AL', 'MS', 'VT', 'CT', 'NH'],
        'mobility_index': [7.8, 5.2, 6.0, 5.8, 4.9, 4.2, 3.7, 7.4, 6.9, 7.6]
    })
    
    # Sample nutrition data
    nutrition_data = pd.DataFrame({
        'state': ['MA', 'TX', 'CA', 'NY', 'FL', 'AL', 'MS', 'VT', 'CT', 'NH'],
        'universal_meals': [1, 0, 1, 0, 0, 0, 0, 1, 1, 0],
        'school_breakfast_participation': [89.5, 62.3, 75.8, 68.4, 58.7, 71.2, 74.3, 82.1, 85.3, 78.9]
    })
    
    return {
        'education': education_data,
        'health': health_data,
        'mobility': mobility_data,
        'nutrition': nutrition_data
    }

def main():
    print("🎨 Creating Advanced 3D Visualization Preview...")
    
    try:
        # Create sample data
        print("📊 Generating sample policy data...")
        sample_data = create_sample_data()
        
        # Initialize 3D visualizer
        print("🚀 Initializing Advanced 3D Visualizer...")
        visualizer = Advanced3DVisualizer(sample_data)
        
        # Create web directory
        web_dir = Path("web")
        web_dir.mkdir(exist_ok=True)
        
        # Export 3D dashboard
        print("🎯 Generating comprehensive 3D dashboard...")
        success = visualizer.export_3d_dashboard(str(web_dir))
        
        if success:
            dashboard_path = web_dir / "advanced_3d_dashboard.html"
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
            
        else:
            print("❌ Failed to create 3D dashboard")
            return None
            
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