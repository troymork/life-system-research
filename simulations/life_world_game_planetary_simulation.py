#!/usr/bin/env python3
"""
LIFE System World Game and Planetary Coordination Simulation
Comprehensive simulation of global resource optimization and crisis response
"""

import numpy as np
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field
import matplotlib.pyplot as plt
from collections import defaultdict
import math

@dataclass
class GlobalResource:
    """Represents a planetary resource with tracking and optimization"""
    name: str
    total_available: float
    current_allocation: Dict[str, float] = field(default_factory=dict)
    regeneration_rate: float = 0.0
    depletion_rate: float = 0.0
    critical_threshold: float = 0.2
    sustainability_score: float = 1.0
    
    def get_utilization_rate(self) -> float:
        """Calculate current utilization rate"""
        total_allocated = sum(self.current_allocation.values())
        return total_allocated / self.total_available if self.total_available > 0 else 0
    
    def update_sustainability(self):
        """Update sustainability score based on utilization"""
        utilization = self.get_utilization_rate()
        if utilization > 0.8:
            self.sustainability_score *= 0.98
        elif utilization < 0.6:
            self.sustainability_score *= 1.01
        self.sustainability_score = max(0.1, min(1.0, self.sustainability_score))

@dataclass
class Bioregion:
    """Represents a bioregional network in the planetary system"""
    name: str
    population: int
    communities: List[str] = field(default_factory=list)
    resource_needs: Dict[str, float] = field(default_factory=dict)
    resource_production: Dict[str, float] = field(default_factory=dict)
    cooperation_level: float = 0.8
    resilience_score: float = 0.7
    innovation_capacity: float = 0.6
    
    def calculate_self_sufficiency(self, resource_name: str) -> float:
        """Calculate self-sufficiency for a specific resource"""
        need = self.resource_needs.get(resource_name, 0)
        production = self.resource_production.get(resource_name, 0)
        return production / need if need > 0 else 1.0
    
    def update_resilience(self, crisis_impact: float):
        """Update resilience based on crisis response"""
        adaptation_factor = self.cooperation_level * self.innovation_capacity
        resilience_change = adaptation_factor * 0.1 - crisis_impact * 0.05
        self.resilience_score = max(0.1, min(1.0, self.resilience_score + resilience_change))

@dataclass
class GlobalCrisis:
    """Represents a planetary crisis requiring coordinated response"""
    name: str
    crisis_type: str  # pandemic, climate, conflict, economic
    severity: float  # 0.0 to 1.0
    affected_regions: List[str]
    resource_impacts: Dict[str, float]  # resource_name -> impact_multiplier
    duration_days: int
    response_effectiveness: float = 0.0
    
    def get_impact_on_region(self, region_name: str) -> float:
        """Calculate crisis impact on specific region"""
        if region_name in self.affected_regions:
            return self.severity * (1.0 - self.response_effectiveness)
        return self.severity * 0.3 * (1.0 - self.response_effectiveness)

class WorldGameOptimizer:
    """Advanced optimization engine for planetary resource allocation"""
    
    def __init__(self):
        self.optimization_history = []
        self.efficiency_metrics = {}
        
    def optimize_global_allocation(self, resources: Dict[str, GlobalResource], 
                                 bioregions: Dict[str, Bioregion]) -> Dict[str, Dict[str, float]]:
        """Optimize resource allocation across all bioregions"""
        allocation_plan = {}
        
        for resource_name, resource in resources.items():
            allocation_plan[resource_name] = self._optimize_single_resource(
                resource, bioregions
            )
        
        # Calculate and store efficiency metrics
        self._calculate_efficiency_metrics(allocation_plan, resources, bioregions)
        
        return allocation_plan
    
    def _optimize_single_resource(self, resource: GlobalResource, 
                                bioregions: Dict[str, Bioregion]) -> Dict[str, float]:
        """Optimize allocation for a single resource using multi-objective optimization"""
        total_need = sum(region.resource_needs.get(resource.name, 0) 
                        for region in bioregions.values())
        
        if total_need == 0:
            return {}
        
        allocation = {}
        remaining_resource = resource.total_available
        
        # Priority-based allocation considering need, cooperation, and resilience
        region_priorities = []
        for region_name, region in bioregions.items():
            need = region.resource_needs.get(resource.name, 0)
            if need > 0:
                # Multi-criteria priority calculation
                priority = (
                    need * 0.4 +  # Basic need weight
                    (1.0 - region.cooperation_level) * need * 0.3 +  # Support struggling regions
                    region.resilience_score * need * 0.2 +  # Reward resilient regions
                    region.innovation_capacity * need * 0.1  # Support innovation
                )
                region_priorities.append((region_name, priority, need))
        
        # Sort by priority (highest first)
        region_priorities.sort(key=lambda x: x[1], reverse=True)
        
        # Allocate resources based on priority and availability
        for region_name, priority, need in region_priorities:
            if remaining_resource <= 0:
                break
                
            # Calculate fair allocation considering global constraints
            allocation_amount = min(need, remaining_resource * 0.8)  # Reserve 20% for emergencies
            allocation[region_name] = allocation_amount
            remaining_resource -= allocation_amount
        
        return allocation
    
    def _calculate_efficiency_metrics(self, allocation_plan: Dict[str, Dict[str, float]], 
                                    resources: Dict[str, GlobalResource], 
                                    bioregions: Dict[str, Bioregion]):
        """Calculate comprehensive efficiency metrics"""
        total_efficiency = 0
        resource_count = 0
        
        for resource_name, allocations in allocation_plan.items():
            resource = resources[resource_name]
            total_allocated = sum(allocations.values())
            utilization_efficiency = total_allocated / resource.total_available
            
            # Calculate needs fulfillment efficiency
            total_need = sum(region.resource_needs.get(resource_name, 0) 
                           for region in bioregions.values())
            fulfillment_efficiency = total_allocated / total_need if total_need > 0 else 1.0
            
            # Combined efficiency score
            resource_efficiency = (utilization_efficiency + fulfillment_efficiency) / 2
            total_efficiency += resource_efficiency
            resource_count += 1
        
        self.efficiency_metrics['overall_efficiency'] = total_efficiency / resource_count if resource_count > 0 else 0
        self.efficiency_metrics['waste_reduction'] = self._calculate_waste_reduction(allocation_plan, resources)
        self.efficiency_metrics['needs_fulfillment'] = self._calculate_needs_fulfillment(allocation_plan, bioregions)

    def _calculate_waste_reduction(self, allocation_plan: Dict[str, Dict[str, float]], 
                                 resources: Dict[str, GlobalResource]) -> float:
        """Calculate waste reduction percentage"""
        total_waste = 0
        total_available = 0
        
        for resource_name, allocations in allocation_plan.items():
            resource = resources[resource_name]
            allocated = sum(allocations.values())
            waste = resource.total_available - allocated
            total_waste += waste
            total_available += resource.total_available
        
        waste_percentage = total_waste / total_available if total_available > 0 else 0
        return (1.0 - waste_percentage) * 100  # Convert to waste reduction percentage

    def _calculate_needs_fulfillment(self, allocation_plan: Dict[str, Dict[str, float]], 
                                   bioregions: Dict[str, Bioregion]) -> float:
        """Calculate overall needs fulfillment percentage"""
        total_need = 0
        total_fulfilled = 0
        
        for resource_name, allocations in allocation_plan.items():
            for region_name, allocation in allocations.items():
                region = bioregions[region_name]
                need = region.resource_needs.get(resource_name, 0)
                total_need += need
                total_fulfilled += min(allocation, need)
        
        return (total_fulfilled / total_need * 100) if total_need > 0 else 100

class CrisisResponseSystem:
    """Advanced crisis response and management system"""
    
    def __init__(self):
        self.response_protocols = {}
        self.response_history = []
        
    def respond_to_crisis(self, crisis: GlobalCrisis, resources: Dict[str, GlobalResource], 
                         bioregions: Dict[str, Bioregion]) -> Dict[str, Any]:
        """Coordinate comprehensive crisis response"""
        response_plan = {
            'immediate_actions': [],
            'resource_reallocations': {},
            'support_measures': [],
            'effectiveness_score': 0.0
        }
        
        # Immediate response actions based on crisis type
        if crisis.crisis_type == 'pandemic':
            response_plan['immediate_actions'] = [
                'Activate global health monitoring network',
                'Redistribute medical supplies and equipment',
                'Implement coordinated public health measures',
                'Establish emergency communication protocols'
            ]
            response_plan['resource_reallocations'] = self._reallocate_for_pandemic(
                crisis, resources, bioregions
            )
            
        elif crisis.crisis_type == 'climate':
            response_plan['immediate_actions'] = [
                'Deploy emergency climate adaptation resources',
                'Coordinate evacuation and relocation support',
                'Activate renewable energy emergency protocols',
                'Implement ecosystem restoration measures'
            ]
            response_plan['resource_reallocations'] = self._reallocate_for_climate(
                crisis, resources, bioregions
            )
            
        elif crisis.crisis_type == 'conflict':
            response_plan['immediate_actions'] = [
                'Activate conflict mediation protocols',
                'Ensure equitable resource distribution',
                'Deploy peacekeeping and humanitarian aid',
                'Establish neutral communication channels'
            ]
            response_plan['resource_reallocations'] = self._reallocate_for_conflict(
                crisis, resources, bioregions
            )
        
        # Calculate response effectiveness
        response_plan['effectiveness_score'] = self._calculate_response_effectiveness(
            crisis, response_plan, bioregions
        )
        
        # Update crisis response effectiveness
        crisis.response_effectiveness = response_plan['effectiveness_score']
        
        # Record response for learning
        self.response_history.append({
            'crisis': crisis,
            'response': response_plan,
            'timestamp': datetime.now()
        })
        
        return response_plan
    
    def _reallocate_for_pandemic(self, crisis: GlobalCrisis, resources: Dict[str, GlobalResource], 
                               bioregions: Dict[str, Bioregion]) -> Dict[str, Dict[str, float]]:
        """Reallocate resources for pandemic response"""
        reallocation = {}
        
        # Prioritize medical resources to affected regions
        if 'medical_supplies' in resources:
            medical_resource = resources['medical_supplies']
            reallocation['medical_supplies'] = {}
            
            # Calculate emergency allocation
            total_affected_population = sum(
                bioregions[region].population for region in crisis.affected_regions
            )
            
            for region_name in crisis.affected_regions:
                region = bioregions[region_name]
                allocation_ratio = region.population / total_affected_population
                emergency_allocation = medical_resource.total_available * 0.6 * allocation_ratio
                reallocation['medical_supplies'][region_name] = emergency_allocation
        
        return reallocation
    
    def _reallocate_for_climate(self, crisis: GlobalCrisis, resources: Dict[str, GlobalResource], 
                              bioregions: Dict[str, Bioregion]) -> Dict[str, Dict[str, float]]:
        """Reallocate resources for climate crisis response"""
        reallocation = {}
        
        # Prioritize energy and infrastructure resources
        for resource_name in ['renewable_energy', 'infrastructure_materials']:
            if resource_name in resources:
                resource = resources[resource_name]
                reallocation[resource_name] = {}
                
                for region_name in crisis.affected_regions:
                    region = bioregions[region_name]
                    # Allocate based on vulnerability and population
                    vulnerability_factor = 1.0 - region.resilience_score
                    allocation = resource.total_available * 0.4 * vulnerability_factor
                    reallocation[resource_name][region_name] = allocation
        
        return reallocation
    
    def _reallocate_for_conflict(self, crisis: GlobalCrisis, resources: Dict[str, GlobalResource], 
                               bioregions: Dict[str, Bioregion]) -> Dict[str, Dict[str, float]]:
        """Reallocate resources for conflict resolution"""
        reallocation = {}
        
        # Focus on basic needs and mediation resources
        for resource_name in ['food_security', 'water_access', 'communication_infrastructure']:
            if resource_name in resources:
                resource = resources[resource_name]
                reallocation[resource_name] = {}
                
                # Equal distribution to reduce resource-based conflicts
                allocation_per_region = resource.total_available * 0.5 / len(crisis.affected_regions)
                for region_name in crisis.affected_regions:
                    reallocation[resource_name][region_name] = allocation_per_region
        
        return reallocation
    
    def _calculate_response_effectiveness(self, crisis: GlobalCrisis, response_plan: Dict[str, Any], 
                                        bioregions: Dict[str, Bioregion]) -> float:
        """Calculate overall response effectiveness score"""
        effectiveness_factors = []
        
        # Response speed factor (immediate actions)
        speed_factor = len(response_plan['immediate_actions']) / 4.0  # Normalize to 4 expected actions
        effectiveness_factors.append(min(1.0, speed_factor))
        
        # Resource allocation effectiveness
        if response_plan['resource_reallocations']:
            allocation_factor = len(response_plan['resource_reallocations']) / 3.0  # Normalize to 3 resource types
            effectiveness_factors.append(min(1.0, allocation_factor))
        else:
            effectiveness_factors.append(0.5)  # Partial effectiveness if no reallocation
        
        # Regional cooperation factor
        affected_cooperation = np.mean([
            bioregions[region].cooperation_level for region in crisis.affected_regions
        ])
        effectiveness_factors.append(affected_cooperation)
        
        # Crisis severity adjustment (harder to respond to severe crises)
        severity_adjustment = 1.0 - (crisis.severity * 0.3)
        effectiveness_factors.append(severity_adjustment)
        
        # Calculate weighted average
        return np.mean(effectiveness_factors)

class PlanetaryCoordinationSimulation:
    """Comprehensive planetary coordination and World Game simulation"""
    
    def __init__(self):
        self.resources = self._initialize_global_resources()
        self.bioregions = self._initialize_bioregions()
        self.world_game = WorldGameOptimizer()
        self.crisis_system = CrisisResponseSystem()
        self.simulation_history = []
        self.current_day = 0
        
    def _initialize_global_resources(self) -> Dict[str, GlobalResource]:
        """Initialize planetary resources with realistic parameters"""
        return {
            'renewable_energy': GlobalResource(
                name='renewable_energy',
                total_available=100000.0,  # Terawatt hours
                regeneration_rate=0.02,    # 2% daily regeneration
                critical_threshold=0.3
            ),
            'fresh_water': GlobalResource(
                name='fresh_water',
                total_available=50000.0,   # Billion cubic meters
                regeneration_rate=0.01,    # 1% daily regeneration
                critical_threshold=0.4
            ),
            'food_security': GlobalResource(
                name='food_security',
                total_available=80000.0,   # Million tons equivalent
                regeneration_rate=0.015,   # 1.5% daily regeneration
                critical_threshold=0.25
            ),
            'medical_supplies': GlobalResource(
                name='medical_supplies',
                total_available=30000.0,   # Standardized units
                regeneration_rate=0.005,   # 0.5% daily regeneration
                critical_threshold=0.35
            ),
            'infrastructure_materials': GlobalResource(
                name='infrastructure_materials',
                total_available=60000.0,   # Million tons
                regeneration_rate=0.008,   # 0.8% daily regeneration
                critical_threshold=0.3
            ),
            'communication_infrastructure': GlobalResource(
                name='communication_infrastructure',
                total_available=40000.0,   # Network capacity units
                regeneration_rate=0.012,   # 1.2% daily regeneration
                critical_threshold=0.2
            )
        }
    
    def _initialize_bioregions(self) -> Dict[str, Bioregion]:
        """Initialize bioregional networks with diverse characteristics"""
        bioregions = {}
        
        # Define bioregional characteristics
        region_configs = [
            ('North_America', 400000000, 0.85, 0.8, 0.9),
            ('Europe', 350000000, 0.9, 0.85, 0.85),
            ('East_Asia', 800000000, 0.8, 0.75, 0.95),
            ('South_Asia', 900000000, 0.7, 0.6, 0.7),
            ('Africa', 600000000, 0.75, 0.65, 0.8),
            ('South_America', 300000000, 0.8, 0.7, 0.75),
            ('Oceania', 50000000, 0.9, 0.85, 0.8),
            ('Middle_East', 200000000, 0.65, 0.6, 0.7)
        ]
        
        for name, population, cooperation, resilience, innovation in region_configs:
            # Generate realistic resource needs based on population
            base_need_per_capita = {
                'renewable_energy': 0.08,
                'fresh_water': 0.05,
                'food_security': 0.06,
                'medical_supplies': 0.02,
                'infrastructure_materials': 0.04,
                'communication_infrastructure': 0.03
            }
            
            resource_needs = {
                resource: population * per_capita * random.uniform(0.8, 1.2)
                for resource, per_capita in base_need_per_capita.items()
            }
            
            # Generate resource production (some regions are net producers)
            resource_production = {}
            for resource in resource_needs:
                production_factor = random.uniform(0.3, 1.5)  # Some regions produce more than they need
                resource_production[resource] = resource_needs[resource] * production_factor
            
            bioregions[name] = Bioregion(
                name=name,
                population=population,
                communities=[f"{name}_community_{i}" for i in range(1, 6)],
                resource_needs=resource_needs,
                resource_production=resource_production,
                cooperation_level=cooperation,
                resilience_score=resilience,
                innovation_capacity=innovation
            )
        
        return bioregions
    
    def run_comprehensive_simulation(self, days: int = 365) -> Dict[str, Any]:
        """Run comprehensive planetary coordination simulation"""
        print(f"🌍 Starting Comprehensive Planetary Coordination Simulation for {days} days...")
        
        simulation_results = {
            'daily_metrics': [],
            'crisis_responses': [],
            'optimization_results': [],
            'final_assessment': {}
        }
        
        # Simulate random crises during the year
        scheduled_crises = self._generate_crisis_schedule(days)
        
        for day in range(days):
            self.current_day = day
            daily_metrics = {}
            
            # Check for scheduled crises
            if day in scheduled_crises:
                crisis = scheduled_crises[day]
                print(f"Day {day}: 🚨 {crisis.name} crisis detected!")
                response = self.crisis_system.respond_to_crisis(crisis, self.resources, self.bioregions)
                simulation_results['crisis_responses'].append({
                    'day': day,
                    'crisis': crisis,
                    'response': response
                })
                
                # Apply crisis impacts to bioregions
                for region_name, region in self.bioregions.items():
                    impact = crisis.get_impact_on_region(region_name)
                    region.update_resilience(impact)
            
            # Run daily World Game optimization
            if day % 7 == 0:  # Weekly optimization cycles
                allocation_plan = self.world_game.optimize_global_allocation(
                    self.resources, self.bioregions
                )
                simulation_results['optimization_results'].append({
                    'day': day,
                    'allocation_plan': allocation_plan,
                    'efficiency_metrics': self.world_game.efficiency_metrics.copy()
                })
            
            # Update resource regeneration and sustainability
            for resource in self.resources.values():
                resource.total_available *= (1 + resource.regeneration_rate)
                resource.update_sustainability()
            
            # Calculate daily metrics
            daily_metrics = self._calculate_daily_metrics()
            simulation_results['daily_metrics'].append({
                'day': day,
                'metrics': daily_metrics
            })
            
            # Progress reporting
            if day % 30 == 0:
                print(f"Day {day}: Global Efficiency: {daily_metrics.get('global_efficiency', 0):.1%}, "
                      f"Crisis Response Effectiveness: {daily_metrics.get('crisis_response_avg', 0):.1%}")
        
        # Calculate final assessment
        simulation_results['final_assessment'] = self._calculate_final_assessment(simulation_results)
        
        print("🎉 Planetary Coordination Simulation Complete!")
        self._print_final_results(simulation_results['final_assessment'])
        
        return simulation_results
    
    def _generate_crisis_schedule(self, days: int) -> Dict[int, GlobalCrisis]:
        """Generate realistic crisis schedule for simulation"""
        crises = {}
        
        # Generate 3-5 crises over the simulation period
        num_crises = random.randint(3, 5)
        crisis_days = sorted(random.sample(range(30, days-30), num_crises))
        
        crisis_types = ['pandemic', 'climate', 'conflict']
        crisis_templates = {
            'pandemic': {
                'name': 'Global Health Emergency',
                'severity': random.uniform(0.6, 0.9),
                'duration_days': random.randint(60, 120),
                'resource_impacts': {
                    'medical_supplies': 2.5,
                    'food_security': 1.3,
                    'communication_infrastructure': 1.2
                }
            },
            'climate': {
                'name': 'Extreme Climate Event',
                'severity': random.uniform(0.5, 0.8),
                'duration_days': random.randint(30, 90),
                'resource_impacts': {
                    'renewable_energy': 1.8,
                    'fresh_water': 2.0,
                    'infrastructure_materials': 2.2
                }
            },
            'conflict': {
                'name': 'Resource Conflict',
                'severity': random.uniform(0.4, 0.7),
                'duration_days': random.randint(45, 150),
                'resource_impacts': {
                    'food_security': 1.5,
                    'infrastructure_materials': 1.4,
                    'communication_infrastructure': 1.6
                }
            }
        }
        
        for i, day in enumerate(crisis_days):
            crisis_type = random.choice(crisis_types)
            template = crisis_templates[crisis_type].copy()
            
            # Select affected regions (2-4 regions per crisis)
            affected_regions = random.sample(
                list(self.bioregions.keys()), 
                random.randint(2, 4)
            )
            
            crisis = GlobalCrisis(
                name=template['name'],
                crisis_type=crisis_type,
                severity=template['severity'],
                affected_regions=affected_regions,
                resource_impacts=template['resource_impacts'],
                duration_days=template['duration_days']
            )
            
            crises[day] = crisis
        
        return crises
    
    def _calculate_daily_metrics(self) -> Dict[str, float]:
        """Calculate comprehensive daily metrics"""
        metrics = {}
        
        # Global efficiency metrics
        if hasattr(self.world_game, 'efficiency_metrics') and self.world_game.efficiency_metrics:
            metrics['global_efficiency'] = self.world_game.efficiency_metrics.get('overall_efficiency', 0)
            metrics['waste_reduction'] = self.world_game.efficiency_metrics.get('waste_reduction', 0) / 100
            metrics['needs_fulfillment'] = self.world_game.efficiency_metrics.get('needs_fulfillment', 0) / 100
        
        # Resource sustainability metrics
        sustainability_scores = [resource.sustainability_score for resource in self.resources.values()]
        metrics['resource_sustainability'] = np.mean(sustainability_scores)
        
        # Bioregional cooperation and resilience
        cooperation_levels = [region.cooperation_level for region in self.bioregions.values()]
        resilience_scores = [region.resilience_score for region in self.bioregions.values()]
        metrics['global_cooperation'] = np.mean(cooperation_levels)
        metrics['global_resilience'] = np.mean(resilience_scores)
        
        # Crisis response effectiveness
        if self.crisis_system.response_history:
            recent_responses = [r['response']['effectiveness_score'] 
                             for r in self.crisis_system.response_history[-5:]]  # Last 5 responses
            metrics['crisis_response_avg'] = np.mean(recent_responses)
        else:
            metrics['crisis_response_avg'] = 1.0  # No crises yet
        
        # Planetary carrying capacity adherence
        resource_utilizations = [resource.get_utilization_rate() for resource in self.resources.values()]
        metrics['carrying_capacity_adherence'] = 1.0 - max(0, np.mean(resource_utilizations) - 0.8) / 0.2
        
        return metrics
    
    def _calculate_final_assessment(self, simulation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive final assessment"""
        assessment = {}
        
        # Extract final metrics
        if simulation_results['daily_metrics']:
            final_metrics = simulation_results['daily_metrics'][-1]['metrics']
            assessment['final_global_efficiency'] = final_metrics.get('global_efficiency', 0) * 100
            assessment['final_waste_reduction'] = final_metrics.get('waste_reduction', 0) * 100
            assessment['final_needs_fulfillment'] = final_metrics.get('needs_fulfillment', 0) * 100
            assessment['final_carrying_capacity_adherence'] = final_metrics.get('carrying_capacity_adherence', 0) * 100
        
        # Crisis response analysis
        if simulation_results['crisis_responses']:
            crisis_effectiveness = [cr['response']['effectiveness_score'] 
                                  for cr in simulation_results['crisis_responses']]
            assessment['average_crisis_response_effectiveness'] = np.mean(crisis_effectiveness) * 100
            assessment['total_crises_handled'] = len(simulation_results['crisis_responses'])
            
            # Categorize crisis response effectiveness
            pandemic_responses = [cr for cr in simulation_results['crisis_responses'] 
                                if cr['crisis'].crisis_type == 'pandemic']
            climate_responses = [cr for cr in simulation_results['crisis_responses'] 
                               if cr['crisis'].crisis_type == 'climate']
            conflict_responses = [cr for cr in simulation_results['crisis_responses'] 
                                if cr['crisis'].crisis_type == 'conflict']
            
            if pandemic_responses:
                assessment['pandemic_response_effectiveness'] = np.mean([
                    cr['response']['effectiveness_score'] for cr in pandemic_responses
                ]) * 100
            
            if climate_responses:
                assessment['climate_response_effectiveness'] = np.mean([
                    cr['response']['effectiveness_score'] for cr in climate_responses
                ]) * 100
            
            if conflict_responses:
                assessment['conflict_response_effectiveness'] = np.mean([
                    cr['response']['effectiveness_score'] for cr in conflict_responses
                ]) * 100
        
        # Optimization performance
        if simulation_results['optimization_results']:
            optimization_efficiencies = [opt['efficiency_metrics'].get('overall_efficiency', 0) 
                                       for opt in simulation_results['optimization_results']]
            assessment['average_optimization_efficiency'] = np.mean(optimization_efficiencies) * 100
        
        # Overall system performance grade
        performance_factors = [
            assessment.get('final_global_efficiency', 0) / 100,
            assessment.get('final_needs_fulfillment', 0) / 100,
            assessment.get('average_crisis_response_effectiveness', 0) / 100,
            assessment.get('final_carrying_capacity_adherence', 0) / 100
        ]
        assessment['overall_system_performance'] = np.mean(performance_factors) * 100
        
        return assessment
    
    def _print_final_results(self, assessment: Dict[str, Any]):
        """Print comprehensive final results"""
        print("\n" + "="*80)
        print("🌍 PLANETARY COORDINATION SIMULATION - FINAL RESULTS")
        print("="*80)
        
        print(f"\n🎯 GLOBAL OPTIMIZATION PERFORMANCE:")
        print(f"   Resource Allocation Efficiency: {assessment.get('final_global_efficiency', 0):.1f}%")
        print(f"   Waste Reduction Achievement: {assessment.get('final_waste_reduction', 0):.1f}%")
        print(f"   Global Needs Fulfillment: {assessment.get('final_needs_fulfillment', 0):.1f}%")
        print(f"   Planetary Carrying Capacity Adherence: {assessment.get('final_carrying_capacity_adherence', 0):.1f}%")
        
        print(f"\n🚨 CRISIS RESPONSE EFFECTIVENESS:")
        print(f"   Total Crises Handled: {assessment.get('total_crises_handled', 0)}")
        print(f"   Average Response Effectiveness: {assessment.get('average_crisis_response_effectiveness', 0):.1f}%")
        
        if 'pandemic_response_effectiveness' in assessment:
            print(f"   Pandemic Response: {assessment['pandemic_response_effectiveness']:.1f}%")
        if 'climate_response_effectiveness' in assessment:
            print(f"   Climate Crisis Response: {assessment['climate_response_effectiveness']:.1f}%")
        if 'conflict_response_effectiveness' in assessment:
            print(f"   Conflict Resolution: {assessment['conflict_response_effectiveness']:.1f}%")
        
        print(f"\n🌟 OVERALL SYSTEM PERFORMANCE:")
        performance = assessment.get('overall_system_performance', 0)
        print(f"   Comprehensive Performance Score: {performance:.1f}%")
        
        if performance >= 90:
            grade = "EXCEPTIONAL - Ready for global deployment"
        elif performance >= 80:
            grade = "EXCELLENT - Minor optimizations needed"
        elif performance >= 70:
            grade = "GOOD - Some improvements required"
        elif performance >= 60:
            grade = "SATISFACTORY - Significant enhancements needed"
        else:
            grade = "NEEDS IMPROVEMENT - Major revisions required"
        
        print(f"   System Grade: {grade}")
        
        print("\n" + "="*80)

def main():
    """Run the comprehensive World Game and Planetary Coordination simulation"""
    print("🚀 Initializing LIFE System Planetary Coordination Simulation...")
    
    # Create and run simulation
    simulation = PlanetaryCoordinationSimulation()
    results = simulation.run_comprehensive_simulation(days=365)
    
    # Save results for analysis
    with open('/home/ubuntu/planetary_simulation_results.json', 'w') as f:
        # Convert results to JSON-serializable format
        json_results = {
            'final_assessment': results['final_assessment'],
            'total_optimizations': len(results['optimization_results']),
            'total_crises': len(results['crisis_responses']),
            'simulation_days': len(results['daily_metrics'])
        }
        json.dump(json_results, f, indent=2)
    
    print(f"\n📊 Detailed results saved to: /home/ubuntu/planetary_simulation_results.json")
    print("🎉 World Game and Planetary Coordination Simulation Complete!")
    
    return results

if __name__ == "__main__":
    main()

