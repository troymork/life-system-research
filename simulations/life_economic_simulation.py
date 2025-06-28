#!/usr/bin/env python3
"""
LIFE System Economic Transition and Wealth Circulation Simulation
================================================================

This module implements sophisticated economic modeling for the LIFE System,
simulating the transition from traditional accumulation-based economics
to regenerative circulation-based economics.

Author: Manus AI
Date: June 28, 2025
Version: 1.0
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum
import json
import sqlite3
from datetime import datetime, timedelta
import math
import random
from collections import defaultdict

class EconomicPhase(Enum):
    """Phases of economic transition"""
    TRADITIONAL = "traditional"
    FOUNDATION = "foundation"
    GROWTH = "growth"
    INTEGRATION = "integration"
    MATURATION = "maturation"

class ResourceType(Enum):
    """Types of resources in the economic system"""
    MATERIAL = "material"
    ENERGY = "energy"
    KNOWLEDGE = "knowledge"
    CARE = "care"
    CREATIVITY = "creativity"
    COORDINATION = "coordination"

class CirculationMechanism(Enum):
    """Mechanisms that drive wealth circulation"""
    PRODUCTIVITY_MULTIPLIER = "productivity_multiplier"
    REGENERATIVE_BONUS = "regenerative_bonus"
    COLLABORATION_REWARD = "collaboration_reward"
    DIVERSITY_INCENTIVE = "diversity_incentive"
    FLOW_ACCELERATION = "flow_acceleration"
    STAGNATION_ACTIVATION = "stagnation_activation"

@dataclass
class EconomicTransaction:
    """Represents a single economic transaction"""
    transaction_id: str
    from_agent: str
    to_agent: str
    resource_type: ResourceType
    amount: float
    purpose: str
    timestamp: datetime
    circulation_multiplier: float = 1.0
    regenerative_bonus: float = 0.0
    collaboration_participants: List[str] = field(default_factory=list)
    environmental_impact: float = 0.0  # Positive = beneficial, negative = harmful
    
    def get_total_value(self) -> float:
        """Calculate total value including all bonuses"""
        base_value = self.amount
        multiplied_value = base_value * self.circulation_multiplier
        final_value = multiplied_value + self.regenerative_bonus
        return final_value

@dataclass
class WealthAccount:
    """Represents an agent's wealth account in the LIFE System"""
    agent_id: str
    resource_balances: Dict[ResourceType, float] = field(default_factory=dict)
    circulation_velocity: float = 0.0  # Resources flowing per time period
    stagnation_level: float = 0.0  # 0.0 = highly active, 1.0 = completely stagnant
    productivity_multiplier: float = 1.0
    regenerative_score: float = 0.0
    collaboration_index: float = 0.0
    diversity_bonus: float = 0.0
    
    def __post_init__(self):
        """Initialize resource balances"""
        if not self.resource_balances:
            for resource_type in ResourceType:
                self.resource_balances[resource_type] = 100.0  # Starting balance
    
    def get_total_wealth(self) -> float:
        """Calculate total wealth across all resource types"""
        return sum(self.resource_balances.values())
    
    def update_circulation_velocity(self, transactions: List[EconomicTransaction]):
        """Update circulation velocity based on recent transactions"""
        recent_transactions = [t for t in transactions 
                             if (t.from_agent == self.agent_id or t.to_agent == self.agent_id)
                             and t.timestamp > datetime.now() - timedelta(days=30)]
        
        total_flow = sum(t.amount for t in recent_transactions)
        self.circulation_velocity = total_flow / 30  # Daily average
        
        # Update stagnation level (inverse of circulation)
        max_possible_flow = self.get_total_wealth() * 0.1  # 10% per day max
        if max_possible_flow > 0:
            self.stagnation_level = max(0.0, 1.0 - (self.circulation_velocity / max_possible_flow))
        else:
            self.stagnation_level = 1.0

class WealthCirculationEngine:
    """
    Core engine that implements wealth circulation mechanisms
    replacing traditional anti-hoarding protocols
    """
    
    def __init__(self):
        self.accounts: Dict[str, WealthAccount] = {}
        self.transaction_history: List[EconomicTransaction] = []
        self.circulation_mechanisms: Dict[CirculationMechanism, bool] = {
            mechanism: True for mechanism in CirculationMechanism
        }
        
        # Circulation parameters
        self.base_productivity_multiplier = 1.2
        self.max_productivity_multiplier = 3.0
        self.regenerative_bonus_rate = 0.15
        self.collaboration_bonus_rate = 0.1
        self.diversity_bonus_rate = 0.05
        self.stagnation_activation_threshold = 0.7
        
        # Economic metrics
        self.total_circulation_velocity = 0.0
        self.abundance_index = 0.0
        self.regenerative_impact = 0.0
        self.cooperation_level = 0.0
        
        # Initialize database for transaction tracking
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize SQLite database for transaction tracking"""
        self.conn = sqlite3.connect(':memory:')
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE transactions (
                id TEXT PRIMARY KEY,
                from_agent TEXT,
                to_agent TEXT,
                resource_type TEXT,
                amount REAL,
                purpose TEXT,
                timestamp TEXT,
                circulation_multiplier REAL,
                regenerative_bonus REAL,
                environmental_impact REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE wealth_accounts (
                agent_id TEXT PRIMARY KEY,
                material_balance REAL,
                energy_balance REAL,
                knowledge_balance REAL,
                care_balance REAL,
                creativity_balance REAL,
                coordination_balance REAL,
                circulation_velocity REAL,
                stagnation_level REAL,
                productivity_multiplier REAL,
                regenerative_score REAL,
                last_updated TEXT
            )
        ''')
        
        self.conn.commit()
    
    def create_account(self, agent_id: str, initial_balances: Optional[Dict[ResourceType, float]] = None):
        """Create a new wealth account for an agent"""
        account = WealthAccount(agent_id=agent_id)
        
        if initial_balances:
            account.resource_balances.update(initial_balances)
        
        self.accounts[agent_id] = account
        self._save_account_to_db(account)
        
        return account
    
    def _save_account_to_db(self, account: WealthAccount):
        """Save account state to database"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO wealth_accounts 
            (agent_id, material_balance, energy_balance, knowledge_balance, 
             care_balance, creativity_balance, coordination_balance,
             circulation_velocity, stagnation_level, productivity_multiplier,
             regenerative_score, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            account.agent_id,
            account.resource_balances[ResourceType.MATERIAL],
            account.resource_balances[ResourceType.ENERGY],
            account.resource_balances[ResourceType.KNOWLEDGE],
            account.resource_balances[ResourceType.CARE],
            account.resource_balances[ResourceType.CREATIVITY],
            account.resource_balances[ResourceType.COORDINATION],
            account.circulation_velocity,
            account.stagnation_level,
            account.productivity_multiplier,
            account.regenerative_score,
            datetime.now().isoformat()
        ))
        
        self.conn.commit()
    
    def process_transaction(self, from_agent: str, to_agent: str, 
                          resource_type: ResourceType, amount: float,
                          purpose: str, collaboration_participants: List[str] = None) -> EconomicTransaction:
        """
        Process a transaction with wealth circulation mechanisms
        """
        if from_agent not in self.accounts or to_agent not in self.accounts:
            raise ValueError("Both agents must have accounts")
        
        from_account = self.accounts[from_agent]
        to_account = self.accounts[to_agent]
        
        # Check if sender has sufficient resources
        if from_account.resource_balances[resource_type] < amount:
            raise ValueError("Insufficient resources for transaction")
        
        # Calculate circulation multipliers and bonuses
        circulation_multiplier = self._calculate_circulation_multiplier(
            from_account, to_account, purpose, collaboration_participants or []
        )
        
        regenerative_bonus = self._calculate_regenerative_bonus(
            amount, purpose, resource_type
        )
        
        # Create transaction
        transaction = EconomicTransaction(
            transaction_id=f"tx_{len(self.transaction_history):06d}",
            from_agent=from_agent,
            to_agent=to_agent,
            resource_type=resource_type,
            amount=amount,
            purpose=purpose,
            timestamp=datetime.now(),
            circulation_multiplier=circulation_multiplier,
            regenerative_bonus=regenerative_bonus,
            collaboration_participants=collaboration_participants or [],
            environmental_impact=self._calculate_environmental_impact(purpose, amount)
        )
        
        # Execute transaction
        self._execute_transaction(transaction)
        
        # Record transaction
        self.transaction_history.append(transaction)
        self._save_transaction_to_db(transaction)
        
        # Update circulation metrics
        self._update_circulation_metrics()
        
        return transaction
    
    def _calculate_circulation_multiplier(self, from_account: WealthAccount, 
                                        to_account: WealthAccount, purpose: str,
                                        collaboration_participants: List[str]) -> float:
        """Calculate productivity multiplier for circulation"""
        multiplier = self.base_productivity_multiplier
        
        # Flow bonus: Resources in motion generate more value
        if from_account.circulation_velocity > 0.1:
            flow_bonus = min(0.5, from_account.circulation_velocity * 0.1)
            multiplier += flow_bonus
        
        # Collaboration bonus: Multi-party transactions get higher multipliers
        if len(collaboration_participants) > 0:
            collaboration_bonus = min(0.3, len(collaboration_participants) * self.collaboration_bonus_rate)
            multiplier += collaboration_bonus
        
        # Diversity bonus: Transactions between different resource types
        if from_account.diversity_bonus > 0:
            multiplier += from_account.diversity_bonus * self.diversity_bonus_rate
        
        # Stagnation activation: Encourage movement of stagnant resources
        if from_account.stagnation_level > self.stagnation_activation_threshold:
            stagnation_bonus = (from_account.stagnation_level - self.stagnation_activation_threshold) * 0.5
            multiplier += stagnation_bonus
        
        # Purpose-based bonuses
        purpose_bonuses = {
            'education': 0.2,
            'healthcare': 0.2,
            'environmental_restoration': 0.3,
            'renewable_energy': 0.25,
            'community_building': 0.15,
            'innovation': 0.2,
            'care_work': 0.25
        }
        
        if purpose in purpose_bonuses:
            multiplier += purpose_bonuses[purpose]
        
        return min(self.max_productivity_multiplier, multiplier)
    
    def _calculate_regenerative_bonus(self, amount: float, purpose: str, 
                                    resource_type: ResourceType) -> float:
        """Calculate regenerative bonus for beneficial activities"""
        base_bonus = amount * self.regenerative_bonus_rate
        
        # Higher bonuses for regenerative activities
        regenerative_multipliers = {
            'environmental_restoration': 2.0,
            'renewable_energy': 1.8,
            'ecosystem_healing': 2.2,
            'biodiversity_enhancement': 2.0,
            'carbon_sequestration': 1.9,
            'soil_regeneration': 1.7,
            'water_restoration': 1.8,
            'waste_reduction': 1.5
        }
        
        multiplier = regenerative_multipliers.get(purpose, 1.0)
        
        # Knowledge and care resources get additional bonuses
        if resource_type in [ResourceType.KNOWLEDGE, ResourceType.CARE]:
            multiplier *= 1.2
        
        return base_bonus * multiplier
    
    def _calculate_environmental_impact(self, purpose: str, amount: float) -> float:
        """Calculate environmental impact of transaction"""
        impact_scores = {
            'environmental_restoration': 0.8,
            'renewable_energy': 0.7,
            'ecosystem_healing': 0.9,
            'education': 0.3,
            'healthcare': 0.2,
            'community_building': 0.4,
            'innovation': 0.1,
            'care_work': 0.2,
            'resource_extraction': -0.6,
            'fossil_fuel_use': -0.8,
            'waste_generation': -0.5,
            'pollution': -0.7
        }
        
        base_impact = impact_scores.get(purpose, 0.0)
        return base_impact * amount
    
    def _execute_transaction(self, transaction: EconomicTransaction):
        """Execute the actual resource transfer"""
        from_account = self.accounts[transaction.from_agent]
        to_account = self.accounts[transaction.to_agent]
        
        # Calculate actual amounts with multipliers
        base_amount = transaction.amount
        multiplied_amount = base_amount * transaction.circulation_multiplier
        bonus_amount = transaction.regenerative_bonus
        
        # Deduct from sender (base amount only)
        from_account.resource_balances[transaction.resource_type] -= base_amount
        
        # Add to receiver (multiplied amount + bonus)
        to_account.resource_balances[transaction.resource_type] += multiplied_amount + bonus_amount
        
        # Update productivity multipliers based on circulation activity
        from_account.productivity_multiplier = min(
            self.max_productivity_multiplier,
            from_account.productivity_multiplier + 0.01
        )
        
        to_account.productivity_multiplier = min(
            self.max_productivity_multiplier,
            to_account.productivity_multiplier + 0.005
        )
        
        # Update regenerative scores
        if transaction.environmental_impact > 0:
            from_account.regenerative_score += transaction.environmental_impact * 0.1
            to_account.regenerative_score += transaction.environmental_impact * 0.05
        
        # Update collaboration indices
        if len(transaction.collaboration_participants) > 0:
            collaboration_boost = len(transaction.collaboration_participants) * 0.02
            from_account.collaboration_index += collaboration_boost
            to_account.collaboration_index += collaboration_boost
        
        # Save updated accounts
        self._save_account_to_db(from_account)
        self._save_account_to_db(to_account)
    
    def _save_transaction_to_db(self, transaction: EconomicTransaction):
        """Save transaction to database"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions 
            (id, from_agent, to_agent, resource_type, amount, purpose,
             timestamp, circulation_multiplier, regenerative_bonus, environmental_impact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            transaction.transaction_id,
            transaction.from_agent,
            transaction.to_agent,
            transaction.resource_type.value,
            transaction.amount,
            transaction.purpose,
            transaction.timestamp.isoformat(),
            transaction.circulation_multiplier,
            transaction.regenerative_bonus,
            transaction.environmental_impact
        ))
        
        self.conn.commit()
    
    def _update_circulation_metrics(self):
        """Update system-wide circulation metrics"""
        if not self.accounts:
            return
        
        # Update circulation velocity for all accounts
        for account in self.accounts.values():
            account.update_circulation_velocity(self.transaction_history)
        
        # Calculate system-wide metrics
        total_velocity = sum(account.circulation_velocity for account in self.accounts.values())
        self.total_circulation_velocity = total_velocity / len(self.accounts)
        
        # Calculate abundance index (total wealth growth rate)
        total_wealth = sum(account.get_total_wealth() for account in self.accounts.values())
        if hasattr(self, '_previous_total_wealth'):
            wealth_growth = (total_wealth - self._previous_total_wealth) / self._previous_total_wealth
            self.abundance_index = max(0.0, wealth_growth)
        self._previous_total_wealth = total_wealth
        
        # Calculate regenerative impact
        recent_transactions = [t for t in self.transaction_history 
                             if t.timestamp > datetime.now() - timedelta(days=30)]
        if recent_transactions:
            total_impact = sum(t.environmental_impact for t in recent_transactions)
            self.regenerative_impact = total_impact / len(recent_transactions)
        
        # Calculate cooperation level
        collaborative_transactions = [t for t in recent_transactions 
                                    if len(t.collaboration_participants) > 0]
        if recent_transactions:
            self.cooperation_level = len(collaborative_transactions) / len(recent_transactions)
    
    def simulate_stagnation_activation(self):
        """Activate stagnant resources through gentle incentives"""
        for agent_id, account in self.accounts.items():
            if account.stagnation_level > self.stagnation_activation_threshold:
                # Create incentive for resource movement
                stagnation_penalty = account.stagnation_level * 0.01
                
                # Reduce stagnant resources slightly
                for resource_type in ResourceType:
                    if account.resource_balances[resource_type] > 50:  # Only if above minimum
                        reduction = account.resource_balances[resource_type] * stagnation_penalty
                        account.resource_balances[resource_type] -= reduction
                
                # Add to community pool or redistribute
                self._redistribute_stagnant_resources(agent_id, stagnation_penalty)
    
    def _redistribute_stagnant_resources(self, stagnant_agent: str, penalty_rate: float):
        """Redistribute stagnant resources to active participants"""
        stagnant_account = self.accounts[stagnant_agent]
        
        # Find most active accounts
        active_accounts = [(agent_id, account) for agent_id, account in self.accounts.items()
                          if account.circulation_velocity > 0.1 and agent_id != stagnant_agent]
        
        if not active_accounts:
            return
        
        # Sort by circulation velocity
        active_accounts.sort(key=lambda x: x[1].circulation_velocity, reverse=True)
        
        # Redistribute to top active accounts
        redistribution_targets = active_accounts[:min(3, len(active_accounts))]
        
        for resource_type in ResourceType:
            stagnant_amount = stagnant_account.resource_balances[resource_type] * penalty_rate
            
            if stagnant_amount > 0:
                per_target_amount = stagnant_amount / len(redistribution_targets)
                
                for target_agent_id, target_account in redistribution_targets:
                    target_account.resource_balances[resource_type] += per_target_amount
    
    def get_circulation_report(self) -> Dict:
        """Generate comprehensive circulation report"""
        if not self.accounts:
            return {}
        
        # Account summaries
        account_summaries = []
        for agent_id, account in self.accounts.items():
            account_summaries.append({
                'agent_id': agent_id,
                'total_wealth': account.get_total_wealth(),
                'circulation_velocity': account.circulation_velocity,
                'stagnation_level': account.stagnation_level,
                'productivity_multiplier': account.productivity_multiplier,
                'regenerative_score': account.regenerative_score,
                'collaboration_index': account.collaboration_index
            })
        
        # Transaction analysis
        recent_transactions = [t for t in self.transaction_history 
                             if t.timestamp > datetime.now() - timedelta(days=30)]
        
        transaction_analysis = {
            'total_transactions': len(recent_transactions),
            'total_value_transferred': sum(t.amount for t in recent_transactions),
            'average_circulation_multiplier': np.mean([t.circulation_multiplier for t in recent_transactions]) if recent_transactions else 0,
            'total_regenerative_bonus': sum(t.regenerative_bonus for t in recent_transactions),
            'collaborative_transactions': len([t for t in recent_transactions if len(t.collaboration_participants) > 0])
        }
        
        # System metrics
        system_metrics = {
            'total_circulation_velocity': self.total_circulation_velocity,
            'abundance_index': self.abundance_index,
            'regenerative_impact': self.regenerative_impact,
            'cooperation_level': self.cooperation_level,
            'active_accounts': len([a for a in self.accounts.values() if a.circulation_velocity > 0.05]),
            'stagnant_accounts': len([a for a in self.accounts.values() if a.stagnation_level > 0.7])
        }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'account_summaries': account_summaries,
            'transaction_analysis': transaction_analysis,
            'system_metrics': system_metrics
        }

class EconomicTransitionSimulator:
    """
    Simulates the transition from traditional to LIFE System economics
    """
    
    def __init__(self, num_agents: int = 100, simulation_days: int = 365):
        self.num_agents = num_agents
        self.simulation_days = simulation_days
        self.current_day = 0
        self.current_phase = EconomicPhase.TRADITIONAL
        
        # Initialize systems
        self.circulation_engine = WealthCirculationEngine()
        self.agents: List[str] = []
        
        # Transition parameters
        self.phase_transition_days = {
            EconomicPhase.TRADITIONAL: 0,
            EconomicPhase.FOUNDATION: 90,    # Days 0-90
            EconomicPhase.GROWTH: 180,       # Days 90-180
            EconomicPhase.INTEGRATION: 270, # Days 180-270
            EconomicPhase.MATURATION: 365   # Days 270-365
        }
        
        # Metrics tracking
        self.daily_metrics: List[Dict] = []
        self.phase_summaries: Dict[EconomicPhase, Dict] = {}
        
        # Initialize simulation
        self._initialize_agents()
        self._initialize_traditional_economy()
    
    def _initialize_agents(self):
        """Create agents for the simulation"""
        for i in range(self.num_agents):
            agent_id = f"agent_{i:03d}"
            self.agents.append(agent_id)
            
            # Create account with random initial balances
            initial_balances = {}
            for resource_type in ResourceType:
                # Traditional economy starts with unequal distribution
                if resource_type == ResourceType.MATERIAL:
                    # Pareto distribution (80/20 rule)
                    initial_balances[resource_type] = np.random.pareto(1.16) * 50 + 10
                else:
                    initial_balances[resource_type] = random.uniform(20, 100)
            
            self.circulation_engine.create_account(agent_id, initial_balances)
    
    def _initialize_traditional_economy(self):
        """Set up traditional economic patterns"""
        # In traditional economy, wealth tends to accumulate
        # Simulate this by reducing circulation incentives
        self.circulation_engine.base_productivity_multiplier = 1.0
        self.circulation_engine.regenerative_bonus_rate = 0.0
        self.circulation_engine.collaboration_bonus_rate = 0.0
        
        # Disable most circulation mechanisms initially
        for mechanism in CirculationMechanism:
            self.circulation_engine.circulation_mechanisms[mechanism] = False
    
    def run_simulation(self):
        """Run the complete economic transition simulation"""
        print(f"Starting Economic Transition Simulation")
        print(f"Agents: {self.num_agents}, Days: {self.simulation_days}")
        print("=" * 60)
        
        for day in range(self.simulation_days):
            self.current_day = day
            
            # Check for phase transitions
            self._check_phase_transition()
            
            # Simulate daily economic activity
            self._simulate_daily_activity()
            
            # Collect metrics
            self._collect_daily_metrics()
            
            # Progress reporting
            if day % 30 == 0:  # Monthly reports
                self._print_progress_report()
        
        # Generate final report
        self._generate_final_report()
    
    def _check_phase_transition(self):
        """Check if it's time to transition to next phase"""
        for phase, start_day in self.phase_transition_days.items():
            if self.current_day == start_day and phase != self.current_phase:
                self._transition_to_phase(phase)
                break
    
    def _transition_to_phase(self, new_phase: EconomicPhase):
        """Transition to a new economic phase"""
        print(f"\nDay {self.current_day}: Transitioning to {new_phase.value.upper()} phase")
        
        # Save summary of previous phase
        if self.current_phase != EconomicPhase.TRADITIONAL:
            self.phase_summaries[self.current_phase] = self._get_phase_summary()
        
        self.current_phase = new_phase
        
        # Configure systems for new phase
        if new_phase == EconomicPhase.FOUNDATION:
            self._configure_foundation_phase()
        elif new_phase == EconomicPhase.GROWTH:
            self._configure_growth_phase()
        elif new_phase == EconomicPhase.INTEGRATION:
            self._configure_integration_phase()
        elif new_phase == EconomicPhase.MATURATION:
            self._configure_maturation_phase()
    
    def _configure_foundation_phase(self):
        """Configure systems for foundation phase"""
        # Enable basic circulation mechanisms
        self.circulation_engine.base_productivity_multiplier = 1.1
        self.circulation_engine.regenerative_bonus_rate = 0.05
        self.circulation_engine.circulation_mechanisms[CirculationMechanism.PRODUCTIVITY_MULTIPLIER] = True
        self.circulation_engine.circulation_mechanisms[CirculationMechanism.REGENERATIVE_BONUS] = True
    
    def _configure_growth_phase(self):
        """Configure systems for growth phase"""
        # Enable collaboration mechanisms
        self.circulation_engine.base_productivity_multiplier = 1.2
        self.circulation_engine.regenerative_bonus_rate = 0.1
        self.circulation_engine.collaboration_bonus_rate = 0.05
        self.circulation_engine.circulation_mechanisms[CirculationMechanism.COLLABORATION_REWARD] = True
        self.circulation_engine.circulation_mechanisms[CirculationMechanism.DIVERSITY_INCENTIVE] = True
    
    def _configure_integration_phase(self):
        """Configure systems for integration phase"""
        # Enable advanced circulation mechanisms
        self.circulation_engine.base_productivity_multiplier = 1.3
        self.circulation_engine.regenerative_bonus_rate = 0.15
        self.circulation_engine.collaboration_bonus_rate = 0.1
        self.circulation_engine.circulation_mechanisms[CirculationMechanism.FLOW_ACCELERATION] = True
    
    def _configure_maturation_phase(self):
        """Configure systems for maturation phase"""
        # Enable all circulation mechanisms
        self.circulation_engine.base_productivity_multiplier = 1.5
        self.circulation_engine.regenerative_bonus_rate = 0.2
        self.circulation_engine.collaboration_bonus_rate = 0.15
        for mechanism in CirculationMechanism:
            self.circulation_engine.circulation_mechanisms[mechanism] = True
    
    def _simulate_daily_activity(self):
        """Simulate one day of economic activity"""
        # Number of transactions per day scales with phase
        phase_transaction_multipliers = {
            EconomicPhase.TRADITIONAL: 0.5,
            EconomicPhase.FOUNDATION: 0.7,
            EconomicPhase.GROWTH: 1.0,
            EconomicPhase.INTEGRATION: 1.3,
            EconomicPhase.MATURATION: 1.5
        }
        
        base_transactions_per_day = self.num_agents * 0.3  # 30% of agents transact daily
        daily_transactions = int(base_transactions_per_day * 
                               phase_transaction_multipliers[self.current_phase])
        
        for _ in range(daily_transactions):
            self._simulate_transaction()
        
        # Run stagnation activation if enabled
        if self.circulation_engine.circulation_mechanisms[CirculationMechanism.STAGNATION_ACTIVATION]:
            self.circulation_engine.simulate_stagnation_activation()
    
    def _simulate_transaction(self):
        """Simulate a single transaction"""
        # Select random agents
        from_agent = random.choice(self.agents)
        to_agent = random.choice([a for a in self.agents if a != from_agent])
        
        # Select resource type based on phase
        if self.current_phase == EconomicPhase.TRADITIONAL:
            # Traditional economy focuses on material resources
            resource_weights = {
                ResourceType.MATERIAL: 0.6,
                ResourceType.ENERGY: 0.3,
                ResourceType.KNOWLEDGE: 0.05,
                ResourceType.CARE: 0.03,
                ResourceType.CREATIVITY: 0.01,
                ResourceType.COORDINATION: 0.01
            }
        else:
            # LIFE System economy has more balanced resource flows
            resource_weights = {
                ResourceType.MATERIAL: 0.25,
                ResourceType.ENERGY: 0.2,
                ResourceType.KNOWLEDGE: 0.2,
                ResourceType.CARE: 0.15,
                ResourceType.CREATIVITY: 0.1,
                ResourceType.COORDINATION: 0.1
            }
        
        resource_type = np.random.choice(
            list(resource_weights.keys()),
            p=list(resource_weights.values())
        )
        
        # Determine transaction amount
        from_account = self.circulation_engine.accounts[from_agent]
        max_amount = from_account.resource_balances[resource_type] * 0.2  # Max 20% of balance
        amount = random.uniform(1.0, max(1.0, max_amount))
        
        # Select purpose based on phase
        if self.current_phase in [EconomicPhase.TRADITIONAL, EconomicPhase.FOUNDATION]:
            purposes = ['trade', 'service', 'payment', 'exchange']
        else:
            purposes = ['education', 'healthcare', 'environmental_restoration', 
                      'renewable_energy', 'community_building', 'innovation', 'care_work']
        
        purpose = random.choice(purposes)
        
        # Determine collaboration participants
        collaboration_participants = []
        if (self.current_phase in [EconomicPhase.GROWTH, EconomicPhase.INTEGRATION, EconomicPhase.MATURATION] 
            and random.random() < 0.3):  # 30% chance of collaboration
            num_collaborators = random.randint(1, 3)
            collaboration_participants = random.sample(
                [a for a in self.agents if a not in [from_agent, to_agent]], 
                min(num_collaborators, len(self.agents) - 2)
            )
        
        # Execute transaction
        try:
            self.circulation_engine.process_transaction(
                from_agent, to_agent, resource_type, amount, purpose, collaboration_participants
            )
        except ValueError:
            # Transaction failed (insufficient resources), skip
            pass
    
    def _collect_daily_metrics(self):
        """Collect daily metrics for analysis"""
        circulation_report = self.circulation_engine.get_circulation_report()
        
        # Calculate additional metrics
        accounts = list(self.circulation_engine.accounts.values())
        wealth_distribution = [account.get_total_wealth() for account in accounts]
        
        gini_coefficient = self._calculate_gini_coefficient(wealth_distribution)
        
        daily_metrics = {
            'day': self.current_day,
            'phase': self.current_phase.value,
            'total_circulation_velocity': circulation_report['system_metrics']['total_circulation_velocity'],
            'abundance_index': circulation_report['system_metrics']['abundance_index'],
            'regenerative_impact': circulation_report['system_metrics']['regenerative_impact'],
            'cooperation_level': circulation_report['system_metrics']['cooperation_level'],
            'gini_coefficient': gini_coefficient,
            'active_accounts': circulation_report['system_metrics']['active_accounts'],
            'stagnant_accounts': circulation_report['system_metrics']['stagnant_accounts'],
            'total_wealth': sum(wealth_distribution),
            'average_wealth': np.mean(wealth_distribution),
            'wealth_std': np.std(wealth_distribution)
        }
        
        self.daily_metrics.append(daily_metrics)
    
    def _calculate_gini_coefficient(self, wealth_distribution: List[float]) -> float:
        """Calculate Gini coefficient for wealth inequality"""
        if not wealth_distribution:
            return 0.0
        
        # Sort wealth values
        sorted_wealth = sorted(wealth_distribution)
        n = len(sorted_wealth)
        
        # Calculate Gini coefficient
        cumsum = np.cumsum(sorted_wealth)
        return (n + 1 - 2 * sum(cumsum) / cumsum[-1]) / n if cumsum[-1] > 0 else 0.0
    
    def _get_phase_summary(self) -> Dict:
        """Get summary statistics for current phase"""
        phase_metrics = [m for m in self.daily_metrics if m['phase'] == self.current_phase.value]
        
        if not phase_metrics:
            return {}
        
        return {
            'duration_days': len(phase_metrics),
            'avg_circulation_velocity': np.mean([m['total_circulation_velocity'] for m in phase_metrics]),
            'avg_abundance_index': np.mean([m['abundance_index'] for m in phase_metrics]),
            'avg_regenerative_impact': np.mean([m['regenerative_impact'] for m in phase_metrics]),
            'avg_cooperation_level': np.mean([m['cooperation_level'] for m in phase_metrics]),
            'final_gini_coefficient': phase_metrics[-1]['gini_coefficient'],
            'wealth_growth': (phase_metrics[-1]['total_wealth'] - phase_metrics[0]['total_wealth']) / phase_metrics[0]['total_wealth']
        }
    
    def _print_progress_report(self):
        """Print monthly progress report"""
        if not self.daily_metrics:
            return
        
        latest_metrics = self.daily_metrics[-1]
        
        print(f"\nDay {self.current_day} ({self.current_phase.value.upper()} phase):")
        print(f"  Circulation Velocity: {latest_metrics['total_circulation_velocity']:.3f}")
        print(f"  Abundance Index: {latest_metrics['abundance_index']:.3f}")
        print(f"  Cooperation Level: {latest_metrics['cooperation_level']:.3f}")
        print(f"  Wealth Inequality (Gini): {latest_metrics['gini_coefficient']:.3f}")
        print(f"  Active Accounts: {latest_metrics['active_accounts']}/{self.num_agents}")
    
    def _generate_final_report(self):
        """Generate comprehensive final report"""
        print("\n" + "=" * 60)
        print("ECONOMIC TRANSITION SIMULATION - FINAL REPORT")
        print("=" * 60)
        
        # Phase summaries
        for phase, summary in self.phase_summaries.items():
            print(f"\n{phase.value.upper()} PHASE SUMMARY:")
            print(f"  Duration: {summary['duration_days']} days")
            print(f"  Avg Circulation Velocity: {summary['avg_circulation_velocity']:.3f}")
            print(f"  Avg Abundance Index: {summary['avg_abundance_index']:.3f}")
            print(f"  Avg Cooperation Level: {summary['avg_cooperation_level']:.3f}")
            print(f"  Final Wealth Inequality: {summary['final_gini_coefficient']:.3f}")
            print(f"  Wealth Growth: {summary['wealth_growth']:.1%}")
        
        # Overall transformation
        if self.daily_metrics:
            initial_metrics = self.daily_metrics[0]
            final_metrics = self.daily_metrics[-1]
            
            print(f"\nOVERALL TRANSFORMATION:")
            print(f"  Circulation Velocity: {initial_metrics['total_circulation_velocity']:.3f} → {final_metrics['total_circulation_velocity']:.3f}")
            print(f"  Cooperation Level: {initial_metrics['cooperation_level']:.3f} → {final_metrics['cooperation_level']:.3f}")
            print(f"  Wealth Inequality: {initial_metrics['gini_coefficient']:.3f} → {final_metrics['gini_coefficient']:.3f}")
            print(f"  Total Wealth Growth: {(final_metrics['total_wealth'] / initial_metrics['total_wealth'] - 1):.1%}")
        
        # Success indicators
        print(f"\nSUCCESS INDICATORS:")
        final_report = self.circulation_engine.get_circulation_report()
        print(f"  ✓ Wealth Circulation Established: {final_metrics['total_circulation_velocity'] > 1.0}")
        print(f"  ✓ Cooperation Achieved: {final_metrics['cooperation_level'] > 0.5}")
        print(f"  ✓ Inequality Reduced: {final_metrics['gini_coefficient'] < initial_metrics['gini_coefficient']}")
        print(f"  ✓ Abundance Created: {final_metrics['abundance_index'] > 0.1}")
        print(f"  ✓ Regenerative Impact: {final_metrics['regenerative_impact'] > 0.0}")

if __name__ == "__main__":
    # Run comprehensive economic transition simulation
    print("LIFE System Economic Transition Simulation")
    print("=" * 50)
    
    # Create and run simulation
    simulator = EconomicTransitionSimulator(num_agents=50, simulation_days=365)
    simulator.run_simulation()
    
    print("\nSimulation completed successfully!")
    print("Economic transition from traditional to LIFE System demonstrated.")

