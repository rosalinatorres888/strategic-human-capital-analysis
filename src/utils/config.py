"""
Configuration management for development economics analysis project.
Handles API keys, settings, and environment variables securely.
"""

import os
from pathlib import Path
from typing import Dict, Any
import json


class Config:
    """Secure configuration management class"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "data"
        self.output_dir = self.project_root / "outputs"
        self.web_dir = self.project_root / "web"
        
        # API Configuration
        self.api_config = {
            'census_api_key': os.getenv('CENSUS_API_KEY', ''),
            'education_api_key': os.getenv('EDUCATION_API_KEY', ''),
            'world_bank_api_key': os.getenv('WORLD_BANK_API_KEY', ''),
            'request_timeout': 30,
            'max_retries': 3,
            'rate_limit_delay': 1.0  # seconds between requests
        }
        
        # Data Source URLs
        self.data_sources = {
            'naep_api': 'https://www.nationsreportcard.gov/profiles/api/',
            'census_api': 'https://api.census.gov/data',
            'world_bank_api': 'https://api.worldbank.org/v2',
            'oecd_api': 'https://stats.oecd.org/SDMX-JSON',
            'cdc_wonder': 'https://wonder.cdc.gov/wonder/help/API.html',
            'usda_nutrition': 'https://www.fns.usda.gov/pd/child-nutrition-tables'
        }
        
        # Visualization settings
        self.viz_config = {
            'default_theme': 'plotly_white',
            'color_palette': {
                'education': '#2E86AB',
                'health': '#A23B72', 
                'nutrition': '#F18F01',
                'poverty': '#C73E1D',
                'success': '#588B8B',
                'neutral': '#8D8D8D'
            },
            'figure_size': (12, 8),
            'dpi': 300,
            'font_family': 'Arial, sans-serif'
        }
        
    def get_api_key(self, service: str) -> str:
        """Safely retrieve API key for a service"""
        key = self.api_config.get(f'{service}_api_key', '')
        if not key:
            print(f"Warning: No API key found for {service}")
        return key
        
    def validate_directories(self):
        """Ensure all required directories exist"""
        directories = [
            self.data_dir / "raw",
            self.data_dir / "processed", 
            self.data_dir / "external",
            self.output_dir / "figures",
            self.output_dir / "reports",
            self.output_dir / "models",
            self.web_dir / "assets"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
    def save_config(self, filename: str = "config.json"):
        """Save non-sensitive config to file"""
        safe_config = {
            'data_sources': self.data_sources,
            'viz_config': self.viz_config,
            'directories': {
                'data': str(self.data_dir),
                'output': str(self.output_dir),
                'web': str(self.web_dir)
            }
        }
        
        config_path = self.project_root / filename
        with open(config_path, 'w') as f:
            json.dump(safe_config, f, indent=2)


# Global config instance
config = Config()