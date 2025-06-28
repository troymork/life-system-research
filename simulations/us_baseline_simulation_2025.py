#!/usr/bin/env python3
"""
US Baseline Socio-Economic Model (2025)
Comprehensive simulation of current US socio-economic structures
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field
import json
import random
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

@dataclass
class USEconomicIndicators:
    """Current US economic indicators for 2025 baseline"""
    gdp_total: float = 28.78e12  # $28.78 trillion (2025 projection)
    gdp_per_capita: float = 85000  # $85,000 per capita
    unemployment_rate: float = 0.038  # 3.8%
    inflation_rate: float = 0.025  # 2.5%
    federal_debt: float = 35.0e12  # $35 trillion
    median_household_income: float = 75000  # $75,000
    poverty_rate: float = 0.115  # 11.5%
    gini_coefficient: float = 0.485  # High inequality
    homeownership_rate: float = 0.658  # 65.8%
    healthcare_costs_gdp: float = 0.185  # 18.5% of GDP
    education_costs_gdp: float = 0.065  # 6.5% of GDP
    infrastructure_grade: str = "C-"  # ASCE Infrastructure Report Card
    
@dataclass
class USSocialIndicators:
    """Current US social indicators for 2025 baseline"""
    population: int = 340000000  # 340 million
    life_expectancy: float = 78.5  # years
    mental_health_issues: float = 0.21  # 21% with mental health conditions
    social_mobility_index: float = 0.27  # Low social mobility (0-1 scale)
    trust_in_government: float = 0.24  # 24% trust in federal government
    trust_in_institutions: float = 0.32  # 32% trust in major institutions
    civic_engagement: float = 0.42  # 42% civic participation
    social_cohesion_index: float = 0.35  # Low social cohesion
    crime_rate: float = 0.0038  # 3.8 per 1000 people (violent crime)
    drug_overdose_deaths: int = 110000  # Annual overdose deaths
    homelessness: int = 650000  # Homeless population
    food_insecurity: float = 0.108  # 10.8% food insecure
    
@dataclass
class USEnvironmentalIndicators:
    """Current US environmental indicators for 2025 baseline"""
    co2_emissions_per_capita: float = 15.2  # tons CO2 per person per year
    renewable_energy_percent: float = 0.22  # 22% renewable energy
    water_stress_index: float = 0.34  # Medium-high water stress
    air_quality_index: float = 0.68  # Moderate air quality (0-1 scale)
    biodiversity_loss_rate: float = 0.015  # 1.5% annual species loss
    waste_generation_per_capita: float = 2.0  # tons per person per year
    recycling_rate: float = 0.32  # 32% recycling rate
    deforestation_rate: float = 0.002  # 0.2% annual forest loss
    soil_degradation: float = 0.25  # 25% of agricultural land degraded
    climate_resilience_index: float = 0.45  # Medium climate resilience

@dataclass
class USSystemicChallenges:
    """Current systemic challenges in US society"""
    wealth_concentration_top1: float = 0.32  # Top 1% owns 32% of wealth
    wealth_concentration_top10: float = 0.70  # Top 10% owns 70% of wealth
    student_debt_total: float = 1.75e12  # $1.75 trillion student debt
    medical_bankruptcy_rate: float = 0.66  # 66% of bankruptcies medical-related
    housing_affordability_crisis: float = 0.38  # 38% spend >30% income on housing
    infrastructure_investment_gap: float = 2.6e12  # $2.6 trillion gap
    political_polarization_index: float = 0.78  # High polarization (0-1 scale)
    misinformation_susceptibility: float = 0.45  # 45% susceptible to misinformation
    social_isolation_rate: float = 0.35  # 35% report chronic loneliness
    economic_anxiety_index: float = 0.62  # 62% economically anxious
    climate_change_denial: float = 0.23  # 23% deny climate change
    democratic_backsliding_risk: float = 0.34  # Medium risk of democratic erosion

class USBaselineAgent:
    """Agent representing an individual in current US socio-economic system"""
    
    def __init__(self, agent_id: str, demographic_profile: Dict[str, Any]):
        self.agent_id = agent_id
        self.age = demographic_profile['age']
        self.income_level = demographic_profile['income_level']  # quintile 1-5
        self.education_level = demographic_profile['education_level']
        self.geographic_region = demographic_profile['geographic_region']
        self.race_ethnicity = demographic_profile['race_ethnicity']
        self.employment_status = demographic_profile['employment_status']
        
        # Economic status
        self.annual_income = self._calculate_income()
        self.wealth = self._calculate_wealth()
        self.debt = self._calculate_debt()
        self.housing_cost_burden = self._calculate_housing_burden()
        self.healthcare_costs = self._calculate_healthcare_costs()
        
        # Calculate environmental impact first (needed for health)
        self.environmental_impact = self._calculate_environmental_impact()
        self.climate_vulnerability = self._calculate_climate_vulnerability()
        
        # Calculate health status (needed for life satisfaction)
        self.health_status = self._calculate_health_status()
        
        # Social wellbeing (depends on health_status)
        self.life_satisfaction = self._calculate_life_satisfaction()
        self.stress_level = self._calculate_stress_level()
        self.social_connections = self._calculate_social_connections()
        self.civic_engagement = self._calculate_civic_engagement()
        self.trust_level = self._calculate_trust_level()
        
        # Economic behavior
        self.consumption_rate = self._calculate_consumption_rate()
        self.savings_rate = self._calculate_savings_rate()
        self.investment_behavior = self._calculate_investment_behavior()
        
    def _calculate_income(self) -> float:
        """Calculate annual income based on demographic profile"""
        base_incomes = {1: 25000, 2: 45000, 3: 75000, 4: 120000, 5: 250000}
        base = base_incomes[self.income_level]
        
        # Adjust for education
        education_multipliers = {
            'less_than_high_school': 0.7,
            'high_school': 0.9,
            'some_college': 1.0,
            'bachelors': 1.3,
            'graduate': 1.6
        }
        
        # Adjust for age (career progression)
        age_multiplier = min(1.5, 0.5 + (self.age - 22) * 0.02)
        
        # Adjust for race/ethnicity (reflecting current disparities)
        race_multipliers = {
            'white': 1.0,
            'black': 0.75,
            'hispanic': 0.78,
            'asian': 1.15,
            'native_american': 0.68,
            'other': 0.85
        }
        
        income = base * education_multipliers.get(self.education_level, 1.0)
        income *= age_multiplier
        income *= race_multipliers.get(self.race_ethnicity, 1.0)
        
        # Add random variation
        income *= random.uniform(0.8, 1.2)
        
        return max(15000, income)  # Minimum wage floor
    
    def _calculate_wealth(self) -> float:
        """Calculate net wealth based on income and demographics"""
        # Wealth accumulation is highly unequal in current system
        if self.income_level == 5:  # Top quintile
            wealth_multiplier = random.uniform(8, 25)
        elif self.income_level == 4:
            wealth_multiplier = random.uniform(3, 8)
        elif self.income_level == 3:
            wealth_multiplier = random.uniform(1, 4)
        elif self.income_level == 2:
            wealth_multiplier = random.uniform(0.2, 1.5)
        else:  # Bottom quintile
            wealth_multiplier = random.uniform(-0.5, 0.5)  # Often negative wealth
        
        # Age factor (wealth accumulation over time)
        age_factor = max(0.1, (self.age - 25) / 40)
        
        wealth = self.annual_income * wealth_multiplier * age_factor
        
        # Race wealth gap (reflecting current disparities)
        race_wealth_multipliers = {
            'white': 1.0,
            'black': 0.13,  # Massive wealth gap
            'hispanic': 0.19,
            'asian': 0.85,
            'native_american': 0.08,
            'other': 0.4
        }
        
        wealth *= race_wealth_multipliers.get(self.race_ethnicity, 1.0)
        
        return wealth
    
    def _calculate_debt(self) -> float:
        """Calculate total debt burden"""
        debt = 0
        
        # Student loan debt
        if self.education_level in ['bachelors', 'graduate']:
            if self.education_level == 'bachelors':
                debt += random.uniform(20000, 50000)
            else:  # graduate
                debt += random.uniform(40000, 120000)
        
        # Credit card debt
        if self.income_level <= 3:
            debt += random.uniform(2000, 15000)
        
        # Medical debt
        debt += random.uniform(0, 25000) * (0.3 if self.income_level <= 2 else 0.1)
        
        # Mortgage debt (if homeowner)
        if random.random() < 0.658:  # Homeownership rate
            if self.income_level >= 3:
                debt += random.uniform(150000, 400000)
        
        return debt
    
    def _calculate_housing_burden(self) -> float:
        """Calculate housing cost as percentage of income"""
        if self.income_level <= 2:
            return random.uniform(0.35, 0.65)  # Housing crisis for low income
        elif self.income_level == 3:
            return random.uniform(0.25, 0.45)
        else:
            return random.uniform(0.15, 0.35)
    
    def _calculate_healthcare_costs(self) -> float:
        """Calculate annual healthcare costs"""
        base_cost = 5000  # Average per person
        
        # Age factor
        age_multiplier = 1 + (self.age - 30) * 0.02
        
        # Income factor (better insurance for higher income)
        income_multiplier = max(0.5, 1.5 - (self.income_level - 1) * 0.2)
        
        return base_cost * age_multiplier * income_multiplier
    
    def _calculate_life_satisfaction(self) -> float:
        """Calculate life satisfaction (0-1 scale)"""
        # Base satisfaction
        satisfaction = 0.6
        
        # Income effect (diminishing returns)
        income_effect = min(0.3, np.log(self.annual_income / 30000) * 0.1)
        satisfaction += income_effect
        
        # Debt burden effect
        debt_burden = self.debt / max(1, self.annual_income)
        satisfaction -= min(0.3, debt_burden * 0.2)
        
        # Housing burden effect
        satisfaction -= (self.housing_cost_burden - 0.3) * 0.5 if self.housing_cost_burden > 0.3 else 0
        
        # Health effect
        satisfaction += (self.health_status - 0.5) * 0.3
        
        return max(0.1, min(1.0, satisfaction))
    
    def _calculate_stress_level(self) -> float:
        """Calculate stress level (0-1 scale, higher is more stress)"""
        stress = 0.4  # Base stress level
        
        # Economic stress
        if self.income_level <= 2:
            stress += 0.3
        
        # Debt stress
        debt_to_income = self.debt / max(1, self.annual_income)
        stress += min(0.3, debt_to_income * 0.2)
        
        # Housing stress
        if self.housing_cost_burden > 0.3:
            stress += (self.housing_cost_burden - 0.3) * 0.5
        
        # Healthcare stress
        healthcare_burden = self.healthcare_costs / max(1, self.annual_income)
        stress += min(0.2, healthcare_burden * 0.3)
        
        return max(0.1, min(1.0, stress))
    
    def _calculate_social_connections(self) -> float:
        """Calculate social connection strength (0-1 scale)"""
        connections = 0.5  # Base level
        
        # Income effect (higher income = more social opportunities)
        connections += (self.income_level - 3) * 0.05
        
        # Age effect (middle age has most connections)
        age_factor = 1 - abs(self.age - 45) / 45
        connections *= age_factor
        
        # Employment effect
        if self.employment_status == 'unemployed':
            connections -= 0.2
        
        # Stress effect
        connections -= self.stress_level * 0.3
        
        return max(0.1, min(1.0, connections))
    
    def _calculate_civic_engagement(self) -> float:
        """Calculate civic engagement level (0-1 scale)"""
        engagement = 0.42  # National average
        
        # Education effect
        education_multipliers = {
            'less_than_high_school': 0.5,
            'high_school': 0.8,
            'some_college': 1.0,
            'bachelors': 1.3,
            'graduate': 1.5
        }
        engagement *= education_multipliers.get(self.education_level, 1.0)
        
        # Income effect
        engagement += (self.income_level - 3) * 0.05
        
        # Age effect (older people more engaged)
        if self.age > 35:
            engagement += (self.age - 35) * 0.005
        
        return max(0.05, min(1.0, engagement))
    
    def _calculate_trust_level(self) -> float:
        """Calculate trust in institutions (0-1 scale)"""
        trust = 0.28  # Low baseline trust
        
        # Income effect (higher income = more trust)
        trust += (self.income_level - 3) * 0.02
        
        # Education effect
        if self.education_level in ['bachelors', 'graduate']:
            trust += 0.05
        
        # Age effect (older people less trusting currently)
        if self.age > 50:
            trust -= 0.1
        
        # Race effect (reflecting current disparities in treatment)
        race_trust_adjustments = {
            'white': 0.05,
            'black': -0.15,
            'hispanic': -0.08,
            'asian': 0.02,
            'native_american': -0.20,
            'other': -0.05
        }
        trust += race_trust_adjustments.get(self.race_ethnicity, 0)
        
        return max(0.05, min(1.0, trust))
    
    def _calculate_health_status(self) -> float:
        """Calculate health status (0-1 scale)"""
        health = 0.7  # Base health
        
        # Age effect
        health -= (self.age - 30) * 0.005
        
        # Income effect (healthcare access)
        health += (self.income_level - 3) * 0.05
        
        # Environmental effect
        health -= self.environmental_impact * 0.1
        
        return max(0.2, min(1.0, health))
    
    def _calculate_environmental_impact(self) -> float:
        """Calculate environmental impact per capita (0-1 scale, higher is worse)"""
        impact = 0.6  # Base US impact (high globally)
        
        # Income effect (higher income = higher consumption)
        impact += (self.income_level - 3) * 0.08
        
        # Geographic effect
        region_impacts = {
            'northeast': 0.9,
            'southeast': 1.1,
            'midwest': 1.0,
            'southwest': 1.2,
            'west': 0.8
        }
        impact *= region_impacts.get(self.geographic_region, 1.0)
        
        return max(0.3, min(1.0, impact))
    
    def _calculate_climate_vulnerability(self) -> float:
        """Calculate vulnerability to climate change (0-1 scale)"""
        vulnerability = 0.4  # Base vulnerability
        
        # Income effect (lower income = higher vulnerability)
        vulnerability += (3 - self.income_level) * 0.05
        
        # Geographic effect
        region_vulnerabilities = {
            'northeast': 0.3,
            'southeast': 0.8,  # Hurricanes, sea level rise
            'midwest': 0.4,    # Extreme weather
            'southwest': 0.9,  # Heat, drought, wildfires
            'west': 0.7       # Wildfires, drought
        }
        vulnerability *= region_vulnerabilities.get(self.geographic_region, 1.0)
        
        # Age effect (elderly more vulnerable)
        if self.age > 65:
            vulnerability += 0.2
        
        return max(0.1, min(1.0, vulnerability))
    
    def _calculate_consumption_rate(self) -> float:
        """Calculate consumption rate relative to income"""
        # Higher income = lower consumption rate (more savings)
        base_rate = 0.95 - (self.income_level - 1) * 0.05
        
        # Debt effect (high debt = high consumption to service debt)
        debt_burden = min(2.0, self.debt / max(1, self.annual_income))
        base_rate += debt_burden * 0.1
        
        return max(0.7, min(1.2, base_rate))
    
    def _calculate_savings_rate(self) -> float:
        """Calculate savings rate"""
        return max(0.0, 1.0 - self.consumption_rate)
    
    def _calculate_investment_behavior(self) -> float:
        """Calculate investment sophistication (0-1 scale)"""
        if self.income_level <= 2:
            return random.uniform(0.0, 0.2)  # Little to no investment
        elif self.income_level == 3:
            return random.uniform(0.1, 0.4)  # Basic investment
        elif self.income_level == 4:
            return random.uniform(0.3, 0.7)  # Moderate investment
        else:  # Top quintile
            return random.uniform(0.6, 1.0)  # Sophisticated investment
    
    def update_annual(self, year: int, economic_conditions: Dict[str, float]):
        """Update agent status annually based on economic conditions"""
        # Income growth/decline
        gdp_growth = economic_conditions.get('gdp_growth', 0.02)
        inflation = economic_conditions.get('inflation', 0.025)
        unemployment = economic_conditions.get('unemployment', 0.038)
        
        # Real income change
        real_income_change = gdp_growth - inflation
        
        # Employment risk
        if self.employment_status == 'employed':
            unemployment_risk = unemployment * (2 if self.income_level <= 2 else 0.5)
            if random.random() < unemployment_risk:
                self.employment_status = 'unemployed'
                self.annual_income *= 0.3  # Unemployment benefits
        elif self.employment_status == 'unemployed':
            reemployment_chance = 0.4 if self.income_level <= 2 else 0.7
            if random.random() < reemployment_chance:
                self.employment_status = 'employed'
                self.annual_income = self._calculate_income()
        
        # Income adjustment for employed
        if self.employment_status == 'employed':
            self.annual_income *= (1 + real_income_change + random.uniform(-0.02, 0.02))
        
        # Wealth changes
        if self.savings_rate > 0:
            self.wealth += self.annual_income * self.savings_rate
            # Investment returns (volatile in current system)
            investment_return = random.uniform(-0.15, 0.12)  # -15% to +12%
            self.wealth *= (1 + investment_return * self.investment_behavior)
        
        # Debt changes
        debt_service_rate = 0.05  # 5% annual debt service
        debt_payment = min(self.debt * debt_service_rate, self.annual_income * 0.3)
        self.debt = max(0, self.debt - debt_payment)
        
        # New debt accumulation (medical, credit card)
        if self.income_level <= 2:
            new_debt = random.uniform(0, 5000)  # Financial stress
            self.debt += new_debt
        
        # Update derived metrics
        self.life_satisfaction = self._calculate_life_satisfaction()
        self.stress_level = self._calculate_stress_level()
        self.health_status = self._calculate_health_status()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary for analysis"""
        return {
            'agent_id': self.agent_id,
            'age': self.age,
            'income_level': self.income_level,
            'annual_income': self.annual_income,
            'wealth': self.wealth,
            'debt': self.debt,
            'life_satisfaction': self.life_satisfaction,
            'stress_level': self.stress_level,
            'health_status': self.health_status,
            'social_connections': self.social_connections,
            'civic_engagement': self.civic_engagement,
            'trust_level': self.trust_level,
            'environmental_impact': self.environmental_impact,
            'climate_vulnerability': self.climate_vulnerability,
            'employment_status': self.employment_status,
            'education_level': self.education_level,
            'race_ethnicity': self.race_ethnicity,
            'geographic_region': self.geographic_region
        }

class USBaselineSimulation:
    """Comprehensive simulation of current US socio-economic system"""
    
    def __init__(self, population_size: int = 10000):
        self.population_size = population_size
        self.agents = []
        self.economic_indicators = USEconomicIndicators()
        self.social_indicators = USSocialIndicators()
        self.environmental_indicators = USEnvironmentalIndicators()
        self.systemic_challenges = USSystemicChallenges()
        self.simulation_history = []
        
        # Initialize population
        self._initialize_population()
        
    def _initialize_population(self):
        """Initialize representative US population"""
        print(f"Initializing US population of {self.population_size:,} agents...")
        
        # Demographic distributions based on US Census data
        age_distribution = self._generate_age_distribution()
        income_distribution = [0.20, 0.20, 0.20, 0.20, 0.20]  # Quintiles
        education_distribution = {
            'less_than_high_school': 0.12,
            'high_school': 0.28,
            'some_college': 0.29,
            'bachelors': 0.20,
            'graduate': 0.11
        }
        race_distribution = {
            'white': 0.60,
            'hispanic': 0.19,
            'black': 0.13,
            'asian': 0.06,
            'native_american': 0.01,
            'other': 0.01
        }
        region_distribution = {
            'northeast': 0.17,
            'southeast': 0.38,
            'midwest': 0.21,
            'southwest': 0.12,
            'west': 0.12
        }
        employment_distribution = {
            'employed': 0.962,  # 96.2% employment rate
            'unemployed': 0.038
        }
        
        for i in range(self.population_size):
            # Generate demographic profile
            profile = {
                'age': np.random.choice(age_distribution),
                'income_level': np.random.choice(range(1, 6), p=income_distribution),
                'education_level': np.random.choice(
                    list(education_distribution.keys()),
                    p=list(education_distribution.values())
                ),
                'race_ethnicity': np.random.choice(
                    list(race_distribution.keys()),
                    p=list(race_distribution.values())
                ),
                'geographic_region': np.random.choice(
                    list(region_distribution.keys()),
                    p=list(region_distribution.values())
                ),
                'employment_status': np.random.choice(
                    list(employment_distribution.keys()),
                    p=list(employment_distribution.values())
                )
            }
            
            agent = USBaselineAgent(f"agent_{i:06d}", profile)
            self.agents.append(agent)
        
        print(f"✅ Population initialized with realistic demographic distribution")
    
    def _generate_age_distribution(self) -> List[int]:
        """Generate realistic age distribution"""
        ages = []
        # US age distribution approximation
        for _ in range(self.population_size):
            rand = random.random()
            if rand < 0.18:  # Under 18
                age = random.randint(0, 17)
            elif rand < 0.45:  # 18-44
                age = random.randint(18, 44)
            elif rand < 0.70:  # 45-64
                age = random.randint(45, 64)
            else:  # 65+
                age = random.randint(65, 95)
            ages.append(age)
        return ages
    
    def run_baseline_simulation(self, years: int = 5) -> Dict[str, Any]:
        """Run 5-year baseline simulation of current US system"""
        print(f"🇺🇸 Starting {years}-Year US Baseline Simulation (2025-{2025+years})")
        print("="*80)
        
        results = {
            'yearly_metrics': [],
            'agent_trajectories': [],
            'systemic_trends': [],
            'crisis_events': []
        }
        
        for year in range(years):
            current_year = 2025 + year
            print(f"\n📅 Year {current_year} (Year {year + 1} of simulation)")
            
            # Generate economic conditions for the year
            economic_conditions = self._generate_economic_conditions(year)
            
            # Check for crisis events
            crisis_events = self._check_crisis_events(year, economic_conditions)
            if crisis_events:
                results['crisis_events'].extend(crisis_events)
                print(f"🚨 Crisis events: {[c['name'] for c in crisis_events]}")
            
            # Update all agents
            for agent in self.agents:
                agent.update_annual(current_year, economic_conditions)
            
            # Calculate yearly metrics
            yearly_metrics = self._calculate_yearly_metrics(current_year, economic_conditions)
            results['yearly_metrics'].append(yearly_metrics)
            
            # Print key metrics
            self._print_yearly_summary(yearly_metrics)
            
            # Store agent trajectories (sample)
            if year % 2 == 0:  # Every other year
                sample_agents = random.sample(self.agents, min(100, len(self.agents)))
                trajectories = [agent.to_dict() for agent in sample_agents]
                results['agent_trajectories'].append({
                    'year': current_year,
                    'agents': trajectories
                })
        
        # Calculate final assessment
        final_assessment = self._calculate_baseline_assessment(results)
        results['final_assessment'] = final_assessment
        
        print("\n" + "="*80)
        print("🇺🇸 US BASELINE SIMULATION COMPLETE")
        print("="*80)
        self._print_final_baseline_results(final_assessment)
        
        return results
    
    def _generate_economic_conditions(self, year: int) -> Dict[str, float]:
        """Generate economic conditions for each year"""
        # Base conditions with some volatility
        conditions = {
            'gdp_growth': max(-0.05, min(0.08, np.random.normal(0.025, 0.02))),
            'inflation': max(0.005, min(0.08, np.random.normal(0.025, 0.01))),
            'unemployment': max(0.02, min(0.12, np.random.normal(0.038, 0.015))),
            'interest_rates': max(0.01, min(0.08, np.random.normal(0.04, 0.01))),
            'stock_market_return': np.random.normal(0.08, 0.15),  # Volatile
            'housing_price_growth': max(-0.1, min(0.2, np.random.normal(0.05, 0.08)))
        }
        
        # Add recession risk (20% chance per year)
        if random.random() < 0.2:
            conditions['gdp_growth'] = random.uniform(-0.08, -0.02)
            conditions['unemployment'] *= random.uniform(1.5, 3.0)
            conditions['stock_market_return'] = random.uniform(-0.4, -0.1)
            print(f"📉 Economic downturn conditions generated")
        
        return conditions
    
    def _check_crisis_events(self, year: int, economic_conditions: Dict[str, float]) -> List[Dict[str, Any]]:
        """Check for various crisis events"""
        crises = []
        
        # Economic crisis
        if economic_conditions['gdp_growth'] < -0.03:
            crises.append({
                'name': 'Economic Recession',
                'type': 'economic',
                'severity': abs(economic_conditions['gdp_growth']) * 10,
                'duration': random.randint(6, 24),  # months
                'impact': 'High unemployment, reduced consumer spending, business failures'
            })
        
        # Healthcare crisis (10% chance per year)
        if random.random() < 0.1:
            crises.append({
                'name': 'Healthcare System Strain',
                'type': 'healthcare',
                'severity': random.uniform(0.3, 0.8),
                'duration': random.randint(3, 12),
                'impact': 'Increased medical costs, reduced access to care'
            })
        
        # Climate crisis (15% chance per year, increasing)
        climate_risk = 0.15 + year * 0.03  # Increasing risk over time
        if random.random() < climate_risk:
            crises.append({
                'name': 'Extreme Weather Event',
                'type': 'climate',
                'severity': random.uniform(0.4, 0.9),
                'duration': random.randint(1, 6),
                'impact': 'Infrastructure damage, displacement, economic losses'
            })
        
        # Social unrest (8% chance per year)
        if random.random() < 0.08:
            crises.append({
                'name': 'Social Unrest',
                'type': 'social',
                'severity': random.uniform(0.2, 0.7),
                'duration': random.randint(1, 4),
                'impact': 'Reduced social cohesion, political instability'
            })
        
        return crises
    
    def _calculate_yearly_metrics(self, year: int, economic_conditions: Dict[str, float]) -> Dict[str, Any]:
        """Calculate comprehensive yearly metrics"""
        agent_data = [agent.to_dict() for agent in self.agents]
        df = pd.DataFrame(agent_data)
        
        metrics = {
            'year': year,
            'economic_conditions': economic_conditions,
            
            # Economic metrics
            'median_income': df['annual_income'].median(),
            'mean_income': df['annual_income'].mean(),
            'income_gini': self._calculate_gini(df['annual_income'].values),
            'wealth_gini': self._calculate_gini(df['wealth'].values),
            'poverty_rate': (df['annual_income'] < 30000).mean(),
            'median_wealth': df['wealth'].median(),
            'mean_wealth': df['wealth'].mean(),
            'total_debt': df['debt'].sum(),
            'debt_to_income_ratio': (df['debt'] / df['annual_income']).median(),
            
            # Social metrics
            'life_satisfaction_avg': df['life_satisfaction'].mean(),
            'stress_level_avg': df['stress_level'].mean(),
            'health_status_avg': df['health_status'].mean(),
            'social_connections_avg': df['social_connections'].mean(),
            'civic_engagement_avg': df['civic_engagement'].mean(),
            'trust_level_avg': df['trust_level'].mean(),
            
            # Environmental metrics
            'environmental_impact_avg': df['environmental_impact'].mean(),
            'climate_vulnerability_avg': df['climate_vulnerability'].mean(),
            
            # Inequality metrics
            'wealth_top_1_percent': self._calculate_wealth_concentration(df, 0.01),
            'wealth_top_10_percent': self._calculate_wealth_concentration(df, 0.10),
            'income_top_1_percent': self._calculate_income_concentration(df, 0.01),
            'income_top_10_percent': self._calculate_income_concentration(df, 0.10),
            
            # Employment metrics
            'unemployment_rate': (df['employment_status'] == 'unemployed').mean(),
            
            # Demographic breakdowns
            'metrics_by_race': self._calculate_demographic_metrics(df, 'race_ethnicity'),
            'metrics_by_income_level': self._calculate_demographic_metrics(df, 'income_level'),
            'metrics_by_region': self._calculate_demographic_metrics(df, 'geographic_region')
        }
        
        return metrics
    
    def _calculate_gini(self, values: np.ndarray) -> float:
        """Calculate Gini coefficient"""
        values = np.array(values)
        values = values[values >= 0]  # Remove negative values
        if len(values) == 0:
            return 0
        
        values = np.sort(values)
        n = len(values)
        cumsum = np.cumsum(values)
        return (n + 1 - 2 * np.sum(cumsum) / cumsum[-1]) / n
    
    def _calculate_wealth_concentration(self, df: pd.DataFrame, percentile: float) -> float:
        """Calculate wealth concentration in top percentile"""
        total_wealth = df['wealth'].sum()
        if total_wealth <= 0:
            return 0
        
        top_threshold = df['wealth'].quantile(1 - percentile)
        top_wealth = df[df['wealth'] >= top_threshold]['wealth'].sum()
        return top_wealth / total_wealth
    
    def _calculate_income_concentration(self, df: pd.DataFrame, percentile: float) -> float:
        """Calculate income concentration in top percentile"""
        total_income = df['annual_income'].sum()
        top_threshold = df['annual_income'].quantile(1 - percentile)
        top_income = df[df['annual_income'] >= top_threshold]['annual_income'].sum()
        return top_income / total_income
    
    def _calculate_demographic_metrics(self, df: pd.DataFrame, group_col: str) -> Dict[str, Dict[str, float]]:
        """Calculate metrics by demographic group"""
        metrics = {}
        for group in df[group_col].unique():
            group_df = df[df[group_col] == group]
            metrics[str(group)] = {
                'median_income': group_df['annual_income'].median(),
                'median_wealth': group_df['wealth'].median(),
                'life_satisfaction': group_df['life_satisfaction'].mean(),
                'stress_level': group_df['stress_level'].mean(),
                'health_status': group_df['health_status'].mean(),
                'unemployment_rate': (group_df['employment_status'] == 'unemployed').mean()
            }
        return metrics
    
    def _print_yearly_summary(self, metrics: Dict[str, Any]):
        """Print yearly summary"""
        print(f"  💰 Median Income: ${metrics['median_income']:,.0f}")
        print(f"  📊 Income Gini: {metrics['income_gini']:.3f}")
        print(f"  🏠 Wealth Gini: {metrics['wealth_gini']:.3f}")
        print(f"  😊 Life Satisfaction: {metrics['life_satisfaction_avg']:.2f}/1.0")
        print(f"  😰 Stress Level: {metrics['stress_level_avg']:.2f}/1.0")
        print(f"  🏥 Health Status: {metrics['health_status_avg']:.2f}/1.0")
        print(f"  🤝 Social Connections: {metrics['social_connections_avg']:.2f}/1.0")
        print(f"  🗳️ Civic Engagement: {metrics['civic_engagement_avg']:.2f}/1.0")
        print(f"  🔒 Trust Level: {metrics['trust_level_avg']:.2f}/1.0")
        print(f"  💼 Unemployment: {metrics['unemployment_rate']:.1%}")
    
    def _calculate_baseline_assessment(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate final baseline assessment"""
        final_year = results['yearly_metrics'][-1]
        first_year = results['yearly_metrics'][0]
        
        assessment = {
            'simulation_period': '2025-2030',
            'final_year_metrics': final_year,
            
            # Economic performance
            'income_growth': (final_year['median_income'] - first_year['median_income']) / first_year['median_income'],
            'wealth_growth': (final_year['median_wealth'] - first_year['median_wealth']) / max(1, first_year['median_wealth']),
            'inequality_change': final_year['income_gini'] - first_year['income_gini'],
            'poverty_rate_change': final_year['poverty_rate'] - first_year['poverty_rate'],
            
            # Social performance
            'wellbeing_change': final_year['life_satisfaction_avg'] - first_year['life_satisfaction_avg'],
            'stress_change': final_year['stress_level_avg'] - first_year['stress_level_avg'],
            'health_change': final_year['health_status_avg'] - first_year['health_status_avg'],
            'social_cohesion_change': final_year['social_connections_avg'] - first_year['social_connections_avg'],
            'civic_engagement_change': final_year['civic_engagement_avg'] - first_year['civic_engagement_avg'],
            'trust_change': final_year['trust_level_avg'] - first_year['trust_level_avg'],
            
            # Crisis resilience
            'total_crises': len(results['crisis_events']),
            'crisis_types': list(set([c['type'] for c in results['crisis_events']])),
            'average_crisis_severity': np.mean([c['severity'] for c in results['crisis_events']]) if results['crisis_events'] else 0,
            
            # Systemic challenges
            'wealth_concentration_top_1': final_year['wealth_top_1_percent'],
            'wealth_concentration_top_10': final_year['wealth_top_10_percent'],
            'racial_wealth_gap': self._calculate_racial_wealth_gap(final_year),
            'regional_disparities': self._calculate_regional_disparities(final_year),
            
            # Overall system performance score
            'overall_performance_score': self._calculate_overall_performance_score(final_year)
        }
        
        return assessment
    
    def _calculate_racial_wealth_gap(self, metrics: Dict[str, Any]) -> Dict[str, float]:
        """Calculate racial wealth gaps"""
        race_metrics = metrics['metrics_by_race']
        white_wealth = race_metrics.get('white', {}).get('median_wealth', 0)
        
        gaps = {}
        for race, race_data in race_metrics.items():
            if race != 'white' and white_wealth > 0:
                race_wealth = race_data.get('median_wealth', 0)
                gaps[race] = race_wealth / white_wealth if white_wealth > 0 else 0
        
        return gaps
    
    def _calculate_regional_disparities(self, metrics: Dict[str, Any]) -> Dict[str, float]:
        """Calculate regional economic disparities"""
        region_metrics = metrics['metrics_by_region']
        incomes = [data['median_income'] for data in region_metrics.values()]
        
        return {
            'income_coefficient_of_variation': np.std(incomes) / np.mean(incomes),
            'max_min_income_ratio': max(incomes) / min(incomes) if min(incomes) > 0 else 0
        }
    
    def _calculate_overall_performance_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall system performance score (0-100)"""
        # Economic factors (40% weight)
        economic_score = (
            min(100, metrics['median_income'] / 1000) * 0.3 +  # Income level
            max(0, 100 - metrics['income_gini'] * 200) * 0.4 +  # Inequality (inverted)
            max(0, 100 - metrics['poverty_rate'] * 500) * 0.3   # Poverty (inverted)
        ) * 0.4
        
        # Social factors (40% weight)
        social_score = (
            metrics['life_satisfaction_avg'] * 100 * 0.3 +
            (1 - metrics['stress_level_avg']) * 100 * 0.2 +
            metrics['health_status_avg'] * 100 * 0.2 +
            metrics['social_connections_avg'] * 100 * 0.15 +
            metrics['civic_engagement_avg'] * 100 * 0.1 +
            metrics['trust_level_avg'] * 100 * 0.05
        ) * 0.4
        
        # Environmental factors (20% weight)
        environmental_score = (
            max(0, 100 - metrics['environmental_impact_avg'] * 100) * 0.6 +
            max(0, 100 - metrics['climate_vulnerability_avg'] * 100) * 0.4
        ) * 0.2
        
        return economic_score + social_score + environmental_score
    
    def _print_final_baseline_results(self, assessment: Dict[str, Any]):
        """Print final baseline results"""
        print(f"\n📊 BASELINE PERFORMANCE ASSESSMENT:")
        print(f"   Overall System Performance: {assessment['overall_performance_score']:.1f}/100")
        print(f"   Median Income Growth: {assessment['income_growth']:.1%}")
        print(f"   Wealth Inequality (Gini): {assessment['final_year_metrics']['wealth_gini']:.3f}")
        print(f"   Income Inequality (Gini): {assessment['final_year_metrics']['income_gini']:.3f}")
        print(f"   Poverty Rate: {assessment['final_year_metrics']['poverty_rate']:.1%}")
        
        print(f"\n🏥 SOCIAL WELLBEING METRICS:")
        print(f"   Life Satisfaction: {assessment['final_year_metrics']['life_satisfaction_avg']:.2f}/1.0")
        print(f"   Stress Level: {assessment['final_year_metrics']['stress_level_avg']:.2f}/1.0")
        print(f"   Health Status: {assessment['final_year_metrics']['health_status_avg']:.2f}/1.0")
        print(f"   Social Connections: {assessment['final_year_metrics']['social_connections_avg']:.2f}/1.0")
        print(f"   Trust in Institutions: {assessment['final_year_metrics']['trust_level_avg']:.2f}/1.0")
        
        print(f"\n🚨 CRISIS RESILIENCE:")
        print(f"   Total Crises: {assessment['total_crises']}")
        print(f"   Crisis Types: {', '.join(assessment['crisis_types'])}")
        print(f"   Average Crisis Severity: {assessment['average_crisis_severity']:.2f}/1.0")
        
        print(f"\n⚖️ SYSTEMIC CHALLENGES:")
        print(f"   Wealth Concentration (Top 1%): {assessment['wealth_concentration_top_1']:.1%}")
        print(f"   Wealth Concentration (Top 10%): {assessment['wealth_concentration_top_10']:.1%}")
        
        # Grade the system
        score = assessment['overall_performance_score']
        if score >= 80:
            grade = "GOOD - System functioning well"
        elif score >= 60:
            grade = "FAIR - Significant challenges present"
        elif score >= 40:
            grade = "POOR - Major systemic problems"
        else:
            grade = "FAILING - System in crisis"
        
        print(f"\n🎯 SYSTEM GRADE: {grade}")

def main():
    """Run US baseline simulation"""
    print("🇺🇸 US Socio-Economic Baseline Simulation (2025-2030)")
    print("="*80)
    
    # Create simulation with representative population
    simulation = USBaselineSimulation(population_size=5000)
    
    # Run 5-year baseline
    results = simulation.run_baseline_simulation(years=5)
    
    # Save results
    with open('/home/ubuntu/us_baseline_simulation_results.json', 'w') as f:
        # Convert to JSON-serializable format
        json_results = {
            'final_assessment': results['final_assessment'],
            'yearly_summaries': [
                {
                    'year': m['year'],
                    'median_income': m['median_income'],
                    'income_gini': m['income_gini'],
                    'life_satisfaction': m['life_satisfaction_avg'],
                    'stress_level': m['stress_level_avg'],
                    'unemployment': m['unemployment_rate']
                }
                for m in results['yearly_metrics']
            ],
            'total_crises': len(results['crisis_events']),
            'simulation_summary': {
                'population_size': simulation.population_size,
                'simulation_years': 5,
                'final_performance_score': results['final_assessment']['overall_performance_score']
            }
        }
        json.dump(json_results, f, indent=2)
    
    print(f"\n📁 Results saved to: /home/ubuntu/us_baseline_simulation_results.json")
    print("🎉 US Baseline Simulation Complete!")
    
    return results

if __name__ == "__main__":
    main()

