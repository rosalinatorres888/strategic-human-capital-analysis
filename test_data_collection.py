#!/usr/bin/env python3
"""
Test script for data collection system
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.data.collector import DataCollector
from src.utils.config import config

def main():
    print("🚀 Testing Development Economics Data Collection System")
    print("=" * 60)
    
    # Initialize data collector
    collector = DataCollector()
    
    try:
        # Test individual data sources
        print("\n📊 Testing NAEP Education Data Collection...")
        education_data = collector.fetch_naep_data()
        print(f"✅ Collected {len(education_data)} education records")
        print(education_data.head())
        
        print("\n💰 Testing Economic Mobility Data Collection...")
        mobility_data = collector.fetch_economic_mobility_data()
        print(f"✅ Collected {len(mobility_data)} mobility records")
        print(mobility_data.head())
        
        print("\n🏥 Testing Health Outcomes Data Collection...")
        health_data = collector.fetch_health_outcomes_data()
        print(f"✅ Collected {len(health_data)} health records")
        print(health_data.head())
        
        print("\n🍎 Testing School Nutrition Data Collection...")
        nutrition_data = collector.fetch_school_nutrition_data()
        print(f"✅ Collected {len(nutrition_data)} nutrition records")
        print(nutrition_data.head())
        
        print("\n🌍 Testing International Comparison Data Collection...")
        international_data = collector.fetch_international_comparison_data()
        print(f"✅ Collected {len(international_data)} international records")
        print(international_data.head())
        
        # Test comprehensive collection
        print("\n🔄 Testing Comprehensive Data Collection...")
        all_datasets = collector.collect_all_data()
        
        print(f"\n🎉 SUCCESS! Collected {len(all_datasets)} datasets:")
        for name, df in all_datasets.items():
            print(f"  - {name}: {len(df)} records")
            
        print(f"\n📁 Data saved to: {config.data_dir}")
        print(f"📋 Check the cache files in: {config.data_dir / 'raw'}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())