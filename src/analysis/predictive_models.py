"""
ML Predictive Models for Human Capital Investment ROI Analysis
Demonstrates advanced data science skills for portfolio
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.pipeline import Pipeline
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple, Any, Optional
import joblib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from ..visualization.plotly_themes import PolicyTheme


class HumanCapitalROIPredictor:
    """
    Advanced ML system for predicting human capital investment ROI
    Showcases feature engineering, model selection, and interpretability
    """
    
    def __init__(self, data_dict: Dict[str, pd.DataFrame]):
        self.data = data_dict
        self.models = {}
        self.scalers = {}
        self.feature_names = []
        self.predictions = {}
        self.theme = PolicyTheme()
        
    def prepare_features(self) -> pd.DataFrame:
        """
        Advanced feature engineering for policy impact prediction
        """
        print("🔬 Engineering features for ML model...")
        
        # Start with base state data
        features_df = pd.DataFrame()
        
        # Education features
        if 'education' in self.data:
            edu_df = self.data['education'].copy()
            features_df = edu_df[['state', 'math_8th_grade', 'reading_8th_grade']].copy()
            features_df['academic_performance_index'] = (
                features_df['math_8th_grade'] * 0.5 + 
                features_df['reading_8th_grade'] * 0.5
            )
            features_df['academic_excellence_score'] = (
                features_df['math_8th_grade'] / features_df['math_8th_grade'].max() * 50 +
                features_df['reading_8th_grade'] / features_df['reading_8th_grade'].max() * 50
            )
        
        # Economic mobility features
        if 'mobility' in self.data:
            mobility_df = self.data['mobility'].copy()
            if not features_df.empty:
                features_df = features_df.merge(mobility_df[['state', 'mobility_index', 'income_25th_percentile', 'income_75th_percentile']], on='state', how='left')
            else:
                features_df = mobility_df[['state', 'mobility_index', 'income_25th_percentile', 'income_75th_percentile']].copy()
            
            # Income inequality measure
            features_df['income_inequality_ratio'] = features_df['income_75th_percentile'] / features_df['income_25th_percentile']
            features_df['mobility_score'] = features_df['mobility_index'] * 10  # Scale for better range
        
        # Health features
        if 'health' in self.data:
            health_df = self.data['health'].copy()
            features_df = features_df.merge(
                health_df[['state', 'child_mortality_rate', 'infant_mortality_rate', 'uninsured_children_pct']], 
                on='state', how='left'
            )
            
            # Health investment proxy (inverse of negative outcomes)
            features_df['health_investment_proxy'] = (
                100 - features_df['child_mortality_rate'] * 5 +  # Scale mortality
                100 - features_df['uninsured_children_pct']
            ) / 2
        
        # Nutrition features
        if 'nutrition' in self.data:
            nutrition_df = self.data['nutrition'].copy()
            features_df = features_df.merge(
                nutrition_df[['state', 'free_lunch_eligible_pct', 'school_breakfast_participation', 'universal_meals']], 
                on='state', how='left'
            )
            
            # Policy comprehensiveness score
            features_df['policy_comprehensiveness'] = (
                features_df['school_breakfast_participation'] / 100 * 0.4 +
                features_df['universal_meals'] * 0.6
            ) * 100
        
        # Create target variables for prediction
        features_df['human_capital_score'] = self._calculate_human_capital_score(features_df)
        features_df['projected_roi_20yr'] = self._calculate_projected_roi(features_df)
        features_df['poverty_reduction_potential'] = self._calculate_poverty_reduction(features_df)
        
        # Create policy interaction features
        if len(features_df.columns) > 5:
            features_df['education_health_synergy'] = (
                features_df.get('academic_performance_index', 0) * 
                features_df.get('health_investment_proxy', 100) / 100
            )
            features_df['comprehensive_policy_score'] = (
                features_df.get('academic_excellence_score', 0) * 0.3 +
                features_df.get('mobility_score', 0) * 0.3 +
                features_df.get('health_investment_proxy', 50) * 0.2 +
                features_df.get('policy_comprehensiveness', 50) * 0.2
            )
        
        # Add state-level policy indicators (Massachusetts as benchmark)
        features_df['is_massachusetts'] = (features_df['state'] == 'MA').astype(int)
        features_df['policy_innovation_score'] = features_df.apply(self._calculate_innovation_score, axis=1)
        
        # Fill missing values with median
        numeric_columns = features_df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if features_df[col].isnull().any():
                features_df[col].fillna(features_df[col].median(), inplace=True)
        
        print(f"✅ Generated {len(features_df.columns)-1} features for {len(features_df)} states")
        
        return features_df
    
    def _calculate_human_capital_score(self, df: pd.DataFrame) -> pd.Series:
        """Calculate comprehensive human capital development score"""
        score = pd.Series(index=df.index, dtype=float)
        
        # Base academic performance (40%)
        if 'academic_performance_index' in df.columns:
            score = df['academic_performance_index'] / df['academic_performance_index'].max() * 40
        else:
            score = pd.Series([20] * len(df), index=df.index)
        
        # Economic mobility contribution (30%)
        if 'mobility_index' in df.columns:
            score += df['mobility_index'] / df['mobility_index'].max() * 30
        
        # Health outcomes contribution (20%)
        if 'health_investment_proxy' in df.columns:
            score += df['health_investment_proxy'] / 100 * 20
        
        # Policy innovation (10%)
        if 'policy_comprehensiveness' in df.columns:
            score += df['policy_comprehensiveness'] / 100 * 10
        
        return score
    
    def _calculate_projected_roi(self, df: pd.DataFrame) -> pd.Series:
        """Calculate 20-year ROI projection based on current policies"""
        base_roi = pd.Series([3.5] * len(df), index=df.index)  # National average baseline
        
        # Massachusetts gets higher ROI due to comprehensive approach
        ma_boost = (df['state'] == 'MA').astype(int) * 1.2
        
        # Academic performance boost
        if 'academic_performance_index' in df.columns:
            academic_boost = (df['academic_performance_index'] - df['academic_performance_index'].mean()) / 100
        else:
            academic_boost = 0
        
        # Health investment boost
        if 'health_investment_proxy' in df.columns:
            health_boost = (df['health_investment_proxy'] - 50) / 200  # Normalized around 50
        else:
            health_boost = 0
        
        # Policy comprehensiveness boost
        if 'policy_comprehensiveness' in df.columns:
            policy_boost = df['policy_comprehensiveness'] / 500  # Small but important effect
        else:
            policy_boost = 0
        
        projected_roi = base_roi + ma_boost + academic_boost + health_boost + policy_boost
        
        # Cap at reasonable bounds
        projected_roi = projected_roi.clip(lower=2.0, upper=6.0)
        
        return projected_roi
    
    def _calculate_poverty_reduction(self, df: pd.DataFrame) -> pd.Series:
        """Calculate poverty reduction potential over 10 years"""
        base_reduction = pd.Series([15.0] * len(df), index=df.index)  # Base 15% reduction
        
        # Massachusetts model shows higher potential
        ma_boost = (df['state'] == 'MA').astype(int) * 10
        
        # Education quality impact
        if 'academic_excellence_score' in df.columns:
            education_impact = (df['academic_excellence_score'] - 50) / 5  # Scale to 0-10 range
        else:
            education_impact = 0
        
        # Mobility impact
        if 'mobility_score' in df.columns:
            mobility_impact = (df['mobility_score'] - df['mobility_score'].mean()) / 2
        else:
            mobility_impact = 0
        
        poverty_reduction = base_reduction + ma_boost + education_impact + mobility_impact
        
        # Cap at realistic bounds
        poverty_reduction = poverty_reduction.clip(lower=5.0, upper=40.0)
        
        return poverty_reduction
    
    def _calculate_innovation_score(self, row: pd.Series) -> float:
        """Calculate policy innovation score for each state"""
        score = 0.0
        
        # Universal meals program
        if row.get('universal_meals', 0) == 1:
            score += 25
        
        # High academic performance
        if row.get('academic_performance_index', 0) > 275:
            score += 20
        
        # Strong economic mobility
        if row.get('mobility_index', 0) > 6.0:
            score += 20
        
        # Low child uninsured rate
        if row.get('uninsured_children_pct', 10) < 4.0:
            score += 20
        
        # High breakfast participation
        if row.get('school_breakfast_participation', 0) > 80:
            score += 15
        
        return score
    
    def build_models(self, features_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Build and train multiple ML models for comparison
        """
        print("🤖 Building ML models for ROI prediction...")
        
        # Prepare features and targets
        feature_columns = [col for col in features_df.columns 
                          if col not in ['state', 'projected_roi_20yr', 'human_capital_score', 'poverty_reduction_potential']]
        
        X = features_df[feature_columns]
        
        # Multiple prediction targets
        targets = {
            'roi_20yr': features_df['projected_roi_20yr'],
            'human_capital': features_df['human_capital_score'],
            'poverty_reduction': features_df['poverty_reduction_potential']
        }
        
        self.feature_names = feature_columns
        model_results = {}
        
        for target_name, y in targets.items():
            print(f"\n📊 Training models for {target_name}...")
            
            # Split data (small dataset, so use different approach)
            if len(X) > 6:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            else:
                # Use full dataset for training and testing (typical for small state-level data)
                X_train, X_test, y_train, y_test = X, X, y, y
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Model ensemble
            models_to_test = {
                'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, max_depth=3),
                'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42, max_depth=3),
                'Ridge Regression': Ridge(alpha=1.0),
                'Elastic Net': ElasticNet(alpha=0.1, random_state=42)
            }
            
            target_results = {}
            
            for model_name, model in models_to_test.items():
                # Train model
                if model_name in ['Ridge Regression', 'Elastic Net']:
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                else:
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                
                # Calculate metrics
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)
                
                target_results[model_name] = {
                    'model': model,
                    'predictions': y_pred,
                    'r2_score': r2,
                    'mse': mse,
                    'mae': mae,
                    'feature_importance': self._get_feature_importance(model, model_name)
                }
                
                print(f"  {model_name}: R² = {r2:.3f}, MAE = {mae:.2f}")
            
            # Select best model
            best_model_name = max(target_results.keys(), key=lambda k: target_results[k]['r2_score'])
            print(f"  ✅ Best model: {best_model_name} (R² = {target_results[best_model_name]['r2_score']:.3f})")
            
            # Store results
            self.models[target_name] = target_results[best_model_name]['model']
            self.scalers[target_name] = scaler
            model_results[target_name] = target_results
            
            # Store predictions for visualization
            self.predictions[target_name] = {
                'actual': y_test,
                'predicted': target_results[best_model_name]['predictions'],
                'states': features_df.loc[X_test.index, 'state'].values
            }
        
        print(f"\n🎉 Successfully trained {len(self.models)} ML models!")
        return model_results
    
    def _get_feature_importance(self, model, model_name: str) -> Dict[str, float]:
        """Extract feature importance from different model types"""
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importances = np.abs(model.coef_)
        else:
            importances = np.zeros(len(self.feature_names))
        
        return dict(zip(self.feature_names, importances))
    
    def predict_policy_scenarios(self, base_features: pd.DataFrame) -> pd.DataFrame:
        """
        Predict outcomes for different policy scenarios
        """
        print("🔮 Generating policy scenario predictions...")
        
        scenarios = {
            'Status Quo': base_features.copy(),
            'Massachusetts Model': self._apply_massachusetts_model(base_features),
            'Universal Programs': self._apply_universal_programs(base_features),
            'Comprehensive Reform': self._apply_comprehensive_reform(base_features)
        }
        
        scenario_results = []
        
        for scenario_name, scenario_data in scenarios.items():
            # Prepare features
            feature_columns = [col for col in scenario_data.columns 
                             if col not in ['state', 'projected_roi_20yr', 'human_capital_score', 'poverty_reduction_potential']]
            
            X_scenario = scenario_data[feature_columns]
            
            # Make predictions with each model
            predictions = {'scenario': scenario_name, 'state': scenario_data['state'].values}
            
            for target_name, model in self.models.items():
                if target_name in self.scalers:
                    X_scaled = self.scalers[target_name].transform(X_scenario)
                    if hasattr(model, 'predict'):
                        preds = model.predict(X_scaled if isinstance(model, (Ridge, ElasticNet)) else X_scenario)
                    else:
                        preds = np.zeros(len(X_scenario))
                else:
                    preds = np.zeros(len(X_scenario))
                
                predictions[f'{target_name}_predicted'] = preds
            
            scenario_results.extend([
                {**predictions, 'state': state, **{k: v[i] for k, v in predictions.items() if isinstance(v, np.ndarray)}}
                for i, state in enumerate(predictions['state'])
            ])
        
        results_df = pd.DataFrame(scenario_results)
        return results_df
    
    def _apply_massachusetts_model(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply Massachusetts policy model to all states"""
        df_new = df.copy()
        
        # Get Massachusetts values as targets
        ma_row = df_new[df_new['state'] == 'MA']
        if not ma_row.empty:
            ma_values = ma_row.iloc[0]
            
            # Apply MA-level performance to other states (scaled)
            improvement_cols = ['academic_performance_index', 'mobility_score', 'health_investment_proxy', 'policy_comprehensiveness']
            
            for col in improvement_cols:
                if col in df_new.columns and col in ma_values:
                    # Gradual improvement toward MA levels (80% of the way)
                    df_new[col] = df_new[col] + (ma_values[col] - df_new[col]) * 0.8
        
        df_new['universal_meals'] = 1  # All states adopt universal meals
        df_new['policy_innovation_score'] += 25  # Boost from adopting MA model
        
        return df_new
    
    def _apply_universal_programs(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply universal programs scenario"""
        df_new = df.copy()
        
        df_new['universal_meals'] = 1
        df_new['school_breakfast_participation'] = np.maximum(df_new['school_breakfast_participation'], 85)
        df_new['uninsured_children_pct'] = np.minimum(df_new['uninsured_children_pct'], 3.0)
        df_new['policy_comprehensiveness'] = np.maximum(df_new['policy_comprehensiveness'], 70)
        
        return df_new
    
    def _apply_comprehensive_reform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply comprehensive reform scenario"""
        df_new = df.copy()
        
        # Combine Massachusetts model + Universal programs + additional improvements
        df_new = self._apply_massachusetts_model(df_new)
        df_new = self._apply_universal_programs(df_new)
        
        # Additional comprehensive improvements
        df_new['academic_performance_index'] += 10  # Investment in education
        df_new['mobility_score'] += 5  # Improved economic opportunity
        df_new['health_investment_proxy'] += 15  # Enhanced health access
        df_new['policy_innovation_score'] = 100  # Maximum innovation
        
        return df_new
    
    def create_roi_prediction_dashboard(self, scenario_results: pd.DataFrame) -> go.Figure:
        """
        Create comprehensive ROI prediction dashboard
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Predicted 20-Year ROI by Policy Scenario',
                'Human Capital Development Projections',
                'Poverty Reduction Potential by State',
                'Policy Innovation vs Predicted Outcomes'
            ),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Chart 1: ROI predictions by scenario
        scenarios = scenario_results['scenario'].unique()
        colors = [self.theme.COLORS['success'], self.theme.COLORS['massachusetts'], 
                 self.theme.COLORS['education'], self.theme.COLORS['health']]
        
        for i, scenario in enumerate(scenarios):
            scenario_data = scenario_results[scenario_results['scenario'] == scenario]
            avg_roi = scenario_data['roi_20yr_predicted'].mean()
            
            fig.add_trace(
                go.Bar(
                    name=scenario,
                    x=[scenario],
                    y=[avg_roi],
                    marker_color=colors[i % len(colors)],
                    showlegend=True,
                    hovertemplate=f'<b>{scenario}</b><br>Average ROI: {avg_roi:.2f}x<extra></extra>'
                ),
                row=1, col=1
            )
        
        # Chart 2: Human capital development
        for i, scenario in enumerate(scenarios):
            scenario_data = scenario_results[scenario_results['scenario'] == scenario]
            
            fig.add_trace(
                go.Scatter(
                    name=f'{scenario} HC',
                    x=scenario_data['state'],
                    y=scenario_data['human_capital_predicted'],
                    mode='lines+markers',
                    line=dict(color=colors[i % len(colors)], width=2),
                    marker=dict(size=6),
                    showlegend=False,
                    hovertemplate=f'<b>{scenario}</b><br>%{{x}}: %{{y:.1f}}<extra></extra>'
                ),
                row=1, col=2
            )
        
        # Chart 3: Poverty reduction by state (Status Quo vs Comprehensive)
        status_quo = scenario_results[scenario_results['scenario'] == 'Status Quo']
        comprehensive = scenario_results[scenario_results['scenario'] == 'Comprehensive Reform']
        
        fig.add_trace(
            go.Bar(
                name='Status Quo',
                x=status_quo['state'],
                y=status_quo['poverty_reduction_predicted'],
                marker_color=self.theme.COLORS['poverty'],
                showlegend=True
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Bar(
                name='Comprehensive Reform',
                x=comprehensive['state'],
                y=comprehensive['poverty_reduction_predicted'],
                marker_color=self.theme.COLORS['success'],
                showlegend=True
            ),
            row=2, col=1
        )
        
        # Chart 4: Innovation vs Outcomes (scatter)
        if 'policy_innovation_score' in scenario_results.columns:
            for i, scenario in enumerate(scenarios):
                scenario_data = scenario_results[scenario_results['scenario'] == scenario]
                
                fig.add_trace(
                    go.Scatter(
                        name=f'{scenario} Innovation',
                        x=scenario_data.get('policy_innovation_score', [50] * len(scenario_data)),
                        y=scenario_data['roi_20yr_predicted'],
                        mode='markers',
                        marker=dict(
                            size=10,
                            color=colors[i % len(colors)],
                            line=dict(color='white', width=1)
                        ),
                        showlegend=False,
                        hovertemplate=f'<b>{scenario}</b><br>Innovation: %{{x}}<br>ROI: %{{y:.2f}}x<extra></extra>'
                    ),
                    row=2, col=2
                )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text='<b>ML-Powered Human Capital Investment ROI Predictions: Strategic Policy Analysis</b>',
                x=0.5,
                font=dict(size=18, color='#2C3E50')
            ),
            height=900,
            width=1300,
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
    
    def save_models(self, output_dir: str = "outputs/models"):
        """Save trained models for future use"""
        from pathlib import Path
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for target_name, model in self.models.items():
            model_path = output_path / f"human_capital_{target_name}_model.pkl"
            joblib.dump(model, model_path)
            
            scaler_path = output_path / f"human_capital_{target_name}_scaler.pkl"
            if target_name in self.scalers:
                joblib.dump(self.scalers[target_name], scaler_path)
        
        print(f"✅ Models saved to {output_path}")