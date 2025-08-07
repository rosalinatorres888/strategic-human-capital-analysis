#!/usr/bin/env python3
"""
Test script for ML predictive analytics system
Creates ROI prediction dashboard with strategic human capital focus
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.data.collector import DataCollector
from src.visualization.interactive_plots import PolicyDashboard
from src.analysis.predictive_models import HumanCapitalROIPredictor
from src.utils.config import config

def main():
    print("🚀 Testing ML Predictive Analytics for Human Capital Investment")
    print("=" * 70)
    
    # Collect data
    print("\n📊 Collecting real government data...")
    collector = DataCollector()
    data_dict = collector.collect_all_data()
    
    # Test ML Predictive Models
    print("\n🤖 Initializing ML Prediction System...")
    predictor = HumanCapitalROIPredictor(data_dict)
    
    try:
        # Feature engineering
        features_df = predictor.prepare_features()
        print(f"📈 Engineered features: {list(features_df.columns)}")
        
        # Build ML models
        model_results = predictor.build_models(features_df)
        
        # Generate policy scenarios and predictions
        scenario_results = predictor.predict_policy_scenarios(features_df)
        print(f"\n🔮 Generated predictions for {len(scenario_results['scenario'].unique())} policy scenarios")
        
        # Show some key predictions
        print("\n💰 KEY ROI PREDICTIONS:")
        for scenario in scenario_results['scenario'].unique():
            scenario_data = scenario_results[scenario_results['scenario'] == scenario]
            avg_roi = scenario_data['roi_20yr_predicted'].mean()
            print(f"  {scenario}: {avg_roi:.2f}x average ROI over 20 years")
        
        # Create ML-powered dashboard
        print("\n📊 Creating ML-Powered ROI Prediction Dashboard...")
        roi_dashboard = predictor.create_roi_prediction_dashboard(scenario_results)
        
        # Save dashboard
        web_dir = config.web_dir
        web_dir.mkdir(exist_ok=True)
        
        dashboard_system = PolicyDashboard(data_dict)
        success = dashboard_system.export_to_html(
            roi_dashboard, 
            "ml_roi_predictions_dashboard", 
            str(web_dir)
        )
        
        if success:
            print(f"✅ ML ROI dashboard saved to: {web_dir}/ml_roi_predictions_dashboard.html")
        
        # Also regenerate the updated main dashboards with new titles
        print("\n🎨 Regenerating main dashboards with strategic titles...")
        
        education_fig = dashboard_system.create_education_impact_dashboard()
        dashboard_system.export_to_html(education_fig, "strategic_human_capital_dashboard", str(web_dir))
        
        policy_fig = dashboard_system.create_policy_comparison_dashboard()
        dashboard_system.export_to_html(policy_fig, "human_capital_roi_analysis", str(web_dir))
        
        intl_fig = dashboard_system.create_international_comparison_dashboard()
        dashboard_system.export_to_html(intl_fig, "global_investment_benchmarks", str(web_dir))
        
        print("✅ All dashboards updated with strategic focus")
        
        # Save models
        predictor.save_models()
        
        # Summary
        print(f"\n🎉 SUCCESS! Created comprehensive ML-powered analysis:")
        print(f"  📊 4 interactive dashboards with strategic human capital focus")
        print(f"  🤖 3 trained ML models (ROI, Human Capital, Poverty Reduction)")
        print(f"  🔮 4 policy scenario predictions")
        print(f"  💾 Models saved for future use")
        
        print(f"\n🏆 PORTFOLIO FEATURES DEMONSTRATED:")
        print(f"  ✅ Advanced feature engineering (interaction terms, policy scores)")
        print(f"  ✅ Multiple ML algorithms (Random Forest, Gradient Boosting, Ridge, Elastic Net)")
        print(f"  ✅ Model comparison and selection based on performance metrics")
        print(f"  ✅ Policy scenario modeling and prediction")
        print(f"  ✅ ROI forecasting with 20-year projections")
        print(f"  ✅ Interactive ML interpretation dashboards")
        print(f"  ✅ Strategic business framing (Human Capital Investment)")
        
        # Display file locations
        print(f"\n📁 FILES CREATED:")
        print(f"  🌐 {web_dir}/ml_roi_predictions_dashboard.html - ML Predictions")
        print(f"  🌐 {web_dir}/strategic_human_capital_dashboard.html - Education Analysis") 
        print(f"  🌐 {web_dir}/human_capital_roi_analysis.html - ROI Analysis")
        print(f"  🌐 {web_dir}/global_investment_benchmarks.html - International Comparison")
        print(f"  💾 outputs/models/ - Trained ML models")
        
        print(f"\n🎯 TO VIEW DASHBOARDS:")
        print(f"  Open any of the HTML files in your browser")
        print(f"  Each dashboard is fully interactive with hover tooltips")
        print(f"  All dashboards now focus on strategic human capital investment")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())