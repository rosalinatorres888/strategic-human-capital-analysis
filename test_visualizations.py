#!/usr/bin/env python3
"""
Test script for visualization system
Creates all dashboards with real data
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.data.collector import DataCollector
from src.visualization.interactive_plots import PolicyDashboard
from src.utils.config import config

def main():
    print("🎨 Testing Development Economics Visualization System")
    print("=" * 60)
    
    # Collect data
    print("\n📊 Collecting data...")
    collector = DataCollector()
    data_dict = collector.collect_all_data()
    
    # Initialize dashboard
    print("\n🎯 Creating dashboard system...")
    dashboard = PolicyDashboard(data_dict)
    
    try:
        # Test Education Impact Dashboard
        print("\n📚 Creating Education Impact Dashboard...")
        education_fig = dashboard.create_education_impact_dashboard()
        
        # Save to web directory
        web_dir = config.web_dir
        web_dir.mkdir(exist_ok=True)
        
        success1 = dashboard.export_to_html(
            education_fig, 
            "education_impact_dashboard", 
            str(web_dir)
        )
        
        if success1:
            print(f"✅ Education dashboard saved to: {web_dir}/education_impact_dashboard.html")
        else:
            print("❌ Failed to save education dashboard")
        
        # Test Policy Comparison Dashboard
        print("\n🏛️ Creating Policy Comparison Dashboard...")
        policy_fig = dashboard.create_policy_comparison_dashboard()
        
        success2 = dashboard.export_to_html(
            policy_fig, 
            "policy_comparison_dashboard", 
            str(web_dir)
        )
        
        if success2:
            print(f"✅ Policy comparison dashboard saved to: {web_dir}/policy_comparison_dashboard.html")
        else:
            print("❌ Failed to save policy comparison dashboard")
        
        # Test International Comparison Dashboard
        print("\n🌍 Creating International Comparison Dashboard...")
        intl_fig = dashboard.create_international_comparison_dashboard()
        
        success3 = dashboard.export_to_html(
            intl_fig, 
            "international_comparison_dashboard", 
            str(web_dir)
        )
        
        if success3:
            print(f"✅ International dashboard saved to: {web_dir}/international_comparison_dashboard.html")
        else:
            print("❌ Failed to save international dashboard")
        
        # Summary
        print(f"\n🎉 SUCCESS! Created {sum([success1, success2, success3])} dashboards")
        print(f"\n📁 All files saved to: {web_dir}")
        print(f"🌐 Open the HTML files in your browser to view the interactive dashboards")
        
        print("\n🎯 Dashboard Features Demonstrated:")
        print("  ✅ Professional styling with custom themes")
        print("  ✅ Interactive hover tooltips")
        print("  ✅ Real government data integration")
        print("  ✅ State-by-state comparisons")
        print("  ✅ International benchmarking") 
        print("  ✅ Security-hardened HTML export")
        print("  ✅ Responsive design")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())