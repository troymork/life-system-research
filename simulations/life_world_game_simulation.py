#!/usr/bin/env python3
"""
LIFE System World Game and Planetary Coordination Simulation
===========================================================

This module implements the World Game - a comprehensive planetary resource
optimization and coordination system that enables democratic global governance
while preserving local autonomy.

Author: Manus AI
Date: June 28, 2025
Version: 1.0
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, Any
from enum import Enum
import json
import sqlite3
from datetime import datetime, timedelta
import math
import random
from collections import defaultdict
import networkx as nx
from scipy.optimize import linprog
import uuid

class ResourceCategory(Enum):
    """Global resource categories tracked by World Game"""
    ENERGY = "energy"
    FOOD = "food"
    WATER = "water"
    MATERIALS = "materials"
    KNOWLEDGE = "knowledge"
    HUMAN_CAPACITY = "human_capacity"
    ECOSYSTEM_HEALTH = "ecosystem_health"
    TECHNOLOGY = "technology"

class ChallengeType(Enum):
    """Types of global challenges"""
    CLIMATE_CRISIS = "climate_crisis"
    RESOURCE_SCARCITY = "resource_scarcity"
    ECOSYSTEM_COLLAPSE = "ecosystem_collapse"
    SOCIAL_INEQUALITY = "social_inequality"
    TECHNOLOGICAL_DISRUPTION = "technological_disruption"
    PANDEMIC = "pandemic"
    NATURAL_DISASTER = "natural_disaster"
    ECONOMIC_INSTABILITY = "economic_instability"

class DecisionScope(Enum):
    """Scope of decisions in the World Game"""
    LOCAL = "local"           # Single community
    BIOREGIONAL = "bioregional"  # Multiple communities in region
    CONTINENTAL = "continental"   # Multiple bioregions
    PLANETARY = "planetary"       # Global coordination

class VotingMethod(Enum):
    """Voting methods for different decision types"""
    CONSENSUS = "consensus"
    MAJORITY = "majority"
    WEIGHTED = "weighted"
    EXPERTISE_WEIGHTED = "expertise_weighted"
    STAKE_WEIGHTED = "stake_weighted"

@dataclass
class GlobalResource:
    """Represents a global resource in the World Game"""
    resource_id: str
    category: ResourceCategory
    total_available: float
    current_allocation: Dict[str, float] = field(default_factory=dict)
    regeneration_rate: float = 0.0
    depletion_rate: float = 0.0
    sustainability_threshold: float = 0.0
    critical_threshold: float = 0.0
    
    def get_utilization_rate(self) -> float:
        """Calculate current utilization rate"""
        total_allocated = sum(self.current_allocation.values())
        return total_allocated / self.total_available if self.total_available > 0 else 0.0
    
    def is_sustainable(self) -> bool:
        """Check if current usage is sustainable"""
        return self.get_utilization_rate() <= self.sustainability_threshold
    
    def is_critical(self) -> bool:
        """Check if resource is in critical state"""
        return self.get_utilization_rate() >= self.critical_threshold

@dataclass
class GlobalChallenge:
    """Represents a global challenge requiring coordination"""
    challenge_id: str
    challenge_type: ChallengeType
    severity: float  # 0.0 to 1.0
    affected_regions: List[str]
    required_resources: Dict[ResourceCategory, float]
    time_sensitivity: float  # Days until critical
    coordination_complexity: float  # 0.0 to 1.0
    success_probability: float = 0.0
    
    def calculate_urgency(self) -> float:
        """Calculate urgency score for prioritization"""
        time_factor = max(0.1, 1.0 - (self.time_sensitivity / 365))  # More urgent if less time
        severity_factor = self.severity
        complexity_factor = 1.0 - self.coordination_complexity  # Less urgent if more complex
        
        return (time_factor * 0.4 + severity_factor * 0.4 + complexity_factor * 0.2)

@dataclass
class CommunityNode:
    """Represents a community in the planetary network"""
    community_id: str
    name: str
    population: int
    location: Tuple[float, float]  # Latitude, longitude
    bioregion: str
    
    # Resource capabilities
    resource_production: Dict[ResourceCategory, float] = field(default_factory=dict)
    resource_consumption: Dict[ResourceCategory, float] = field(default_factory=dict)
    resource_storage: Dict[ResourceCategory, float] = field(default_factory=dict)
    
    # Expertise and specializations
    expertise_areas: List[str] = field(default_factory=list)
    innovation_capacity: float = 0.0
    coordination_capacity: float = 0.0
    
    # Network connections
    partner_communities: Set[str] = field(default_factory=set)
    trust_relationships: Dict[str, float] = field(default_factory=dict)
    
    # Participation metrics
    participation_level: float = 1.0
    decision_weight: float = 1.0
    
    def get_resource_surplus(self, resource: ResourceCategory) -> float:
        """Calculate surplus/deficit for a resource"""
        production = self.resource_production.get(resource, 0.0)
        consumption = self.resource_consumption.get(resource, 0.0)
        return production - consumption
    
    def can_contribute_to_challenge(self, challenge: GlobalChallenge) -> bool:
        """Check if community can contribute to addressing a challenge"""
        for resource, required_amount in challenge.required_resources.items():
            if self.get_resource_surplus(resource) > required_amount * 0.1:  # Can contribute 10%
                return True
        return False

class WorldGameEngine:
    """
    Core engine for the World Game planetary coordination system
    """
    
    def __init__(self):
        # Network structure
        self.communities: Dict[str, CommunityNode] = {}
        self.bioregions: Dict[str, List[str]] = defaultdict(list)
        self.network_graph = nx.Graph()
        
        # Global resources
        self.global_resources: Dict[str, GlobalResource] = {}
        
        # Active challenges
        self.active_challenges: Dict[str, GlobalChallenge] = {}
        self.resolved_challenges: List[GlobalChallenge] = []
        
        # Decision tracking
        self.active_proposals: Dict[str, Dict] = {}
        self.decision_history: List[Dict] = []
        
        # Optimization parameters
        self.optimization_objectives = {
            'efficiency': 0.25,      # Resource utilization efficiency
            'sustainability': 0.30,  # Long-term sustainability
            'equity': 0.25,         # Fair distribution
            'resilience': 0.20      # System resilience
        }
        
        # Performance metrics
        self.coordination_effectiveness = 0.0
        self.resource_optimization_score = 0.0
        self.democratic_participation_rate = 0.0
        self.challenge_resolution_rate = 0.0
        
        # Initialize database
        self._initialize_database()
        
        # Initialize planetary resources
        self._initialize_global_resources()
    
    def _initialize_database(self):
        """Initialize SQLite database for World Game data"""
        self.conn = sqlite3.connect(':memory:')
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE communities (
                id TEXT PRIMARY KEY,
                name TEXT,
                population INTEGER,
                latitude REAL,
                longitude REAL,
                bioregion TEXT,
                participation_level REAL,
                decision_weight REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE global_resources (
                id TEXT PRIMARY KEY,
                category TEXT,
                total_available REAL,
                regeneration_rate REAL,
                depletion_rate REAL,
                sustainability_threshold REAL,
                critical_threshold REAL,
                current_utilization REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE challenges (
                id TEXT PRIMARY KEY,
                type TEXT,
                severity REAL,
                time_sensitivity REAL,
                coordination_complexity REAL,
                status TEXT,
                created_date TEXT,
                resolved_date TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE decisions (
                id TEXT PRIMARY KEY,
                proposal_title TEXT,
                decision_scope TEXT,
                voting_method TEXT,
                participants INTEGER,
                votes_for INTEGER,
                votes_against INTEGER,
                abstentions INTEGER,
                result TEXT,
                implementation_status TEXT,
                created_date TEXT,
                decided_date TEXT
            )
        ''')
        
        self.conn.commit()
    
    def _initialize_global_resources(self):
        """Initialize global resource tracking"""
        resource_configs = {
            ResourceCategory.ENERGY: {
                'total_available': 1000000.0,  # Renewable energy capacity
                'regeneration_rate': 0.001,    # Daily regeneration
                'sustainability_threshold': 0.8,
                'critical_threshold': 0.95
            },
            ResourceCategory.FOOD: {
                'total_available': 500000.0,   # Global food production capacity
                'regeneration_rate': 0.003,    # Seasonal regeneration
                'sustainability_threshold': 0.7,
                'critical_threshold': 0.9
            },
            ResourceCategory.WATER: {
                'total_available': 800000.0,   # Freshwater resources
                'regeneration_rate': 0.002,    # Natural water cycle
                'sustainability_threshold': 0.6,
                'critical_threshold': 0.85
            },
            ResourceCategory.MATERIALS: {
                'total_available': 300000.0,   # Sustainable materials
                'regeneration_rate': 0.0005,   # Recycling and regeneration
                'sustainability_threshold': 0.75,
                'critical_threshold': 0.9
            },
            ResourceCategory.KNOWLEDGE: {
                'total_available': float('inf'),  # Knowledge is infinite
                'regeneration_rate': 0.01,        # Continuous creation
                'sustainability_threshold': 1.0,
                'critical_threshold': 1.0
            },
            ResourceCategory.HUMAN_CAPACITY: {
                'total_available': 100000.0,   # Available human hours
                'regeneration_rate': 0.004,    # Rest and recovery
                'sustainability_threshold': 0.8,
                'critical_threshold': 0.95
            },
            ResourceCategory.ECOSYSTEM_HEALTH: {
                'total_available': 100.0,      # Ecosystem health index
                'regeneration_rate': 0.001,    # Natural regeneration
                'sustainability_threshold': 0.7,
                'critical_threshold': 0.3
            },
            ResourceCategory.TECHNOLOGY: {
                'total_available': 50000.0,    # Technology capacity
                'regeneration_rate': 0.005,    # Innovation and development
                'sustainability_threshold': 0.9,
                'critical_threshold': 0.98
            }
        }
        
        for category, config in resource_configs.items():
            resource = GlobalResource(
                resource_id=f"global_{category.value}",
                category=category,
                total_available=config['total_available'],
                regeneration_rate=config['regeneration_rate'],
                sustainability_threshold=config['sustainability_threshold'],
                critical_threshold=config['critical_threshold']
            )
            
            self.global_resources[resource.resource_id] = resource
            self._save_resource_to_db(resource)
    
    def add_community(self, community_id: str, name: str, population: int,
                     location: Tuple[float, float], bioregion: str) -> CommunityNode:
        """Add a community to the World Game network"""
        community = CommunityNode(
            community_id=community_id,
            name=name,
            population=population,
            location=location,
            bioregion=bioregion
        )
        
        # Initialize resource capabilities based on population and location
        self._initialize_community_resources(community)
        
        # Add to network structures
        self.communities[community_id] = community
        self.bioregions[bioregion].append(community_id)
        self.network_graph.add_node(community_id, **{
            'name': name,
            'population': population,
            'bioregion': bioregion
        })
        
        # Save to database
        self._save_community_to_db(community)
        
        return community
    
    def _initialize_community_resources(self, community: CommunityNode):
        """Initialize resource production/consumption for a community"""
        base_production = community.population * 0.1
        base_consumption = community.population * 0.08
        
        # Vary by resource type and add some randomness
        for category in ResourceCategory:
            if category == ResourceCategory.KNOWLEDGE:
                # Knowledge production scales with population and education
                production = base_production * random.uniform(0.5, 2.0)
                consumption = base_consumption * random.uniform(0.3, 0.8)
            elif category == ResourceCategory.ECOSYSTEM_HEALTH:
                # Ecosystem health depends on community practices
                production = random.uniform(0.1, 1.0)
                consumption = random.uniform(0.05, 0.5)
            else:
                production = base_production * random.uniform(0.3, 1.5)
                consumption = base_consumption * random.uniform(0.5, 1.2)
            
            community.resource_production[category] = production
            community.resource_consumption[category] = consumption
            community.resource_storage[category] = production * 10  # 10 days storage
        
        # Set expertise areas
        expertise_options = [
            'renewable_energy', 'sustainable_agriculture', 'water_management',
            'ecosystem_restoration', 'education', 'healthcare', 'technology',
            'governance', 'conflict_resolution', 'disaster_response'
        ]
        
        num_expertise = random.randint(2, 4)
        community.expertise_areas = random.sample(expertise_options, num_expertise)
        
        # Set capacity metrics
        community.innovation_capacity = random.uniform(0.3, 1.0)
        community.coordination_capacity = random.uniform(0.4, 1.0)
    
    def connect_communities(self, community1_id: str, community2_id: str, trust_level: float = 0.5):
        """Create connection between two communities"""
        if community1_id not in self.communities or community2_id not in self.communities:
            raise ValueError("Both communities must exist")
        
        # Add to network graph
        self.network_graph.add_edge(community1_id, community2_id, trust=trust_level)
        
        # Update community relationships
        self.communities[community1_id].partner_communities.add(community2_id)
        self.communities[community2_id].partner_communities.add(community1_id)
        
        self.communities[community1_id].trust_relationships[community2_id] = trust_level
        self.communities[community2_id].trust_relationships[community1_id] = trust_level
    
    def create_global_challenge(self, challenge_type: ChallengeType, severity: float,
                              affected_regions: List[str], time_sensitivity: float) -> GlobalChallenge:
        """Create a new global challenge requiring coordination"""
        challenge_id = f"challenge_{len(self.active_challenges):04d}"
        
        # Determine required resources based on challenge type
        required_resources = self._calculate_challenge_requirements(challenge_type, severity)
        
        challenge = GlobalChallenge(
            challenge_id=challenge_id,
            challenge_type=challenge_type,
            severity=severity,
            affected_regions=affected_regions,
            required_resources=required_resources,
            time_sensitivity=time_sensitivity,
            coordination_complexity=self._calculate_coordination_complexity(affected_regions)
        )
        
        self.active_challenges[challenge_id] = challenge
        self._save_challenge_to_db(challenge)
        
        return challenge
    
    def _calculate_challenge_requirements(self, challenge_type: ChallengeType, 
                                        severity: float) -> Dict[ResourceCategory, float]:
        """Calculate resource requirements for a challenge"""
        base_requirements = {
            ChallengeType.CLIMATE_CRISIS: {
                ResourceCategory.ENERGY: 1000 * severity,
                ResourceCategory.TECHNOLOGY: 500 * severity,
                ResourceCategory.HUMAN_CAPACITY: 800 * severity,
                ResourceCategory.KNOWLEDGE: 300 * severity
            },
            ChallengeType.RESOURCE_SCARCITY: {
                ResourceCategory.MATERIALS: 800 * severity,
                ResourceCategory.TECHNOLOGY: 400 * severity,
                ResourceCategory.HUMAN_CAPACITY: 600 * severity,
                ResourceCategory.KNOWLEDGE: 200 * severity
            },
            ChallengeType.ECOSYSTEM_COLLAPSE: {
                ResourceCategory.ECOSYSTEM_HEALTH: 50 * severity,
                ResourceCategory.KNOWLEDGE: 400 * severity,
                ResourceCategory.HUMAN_CAPACITY: 700 * severity,
                ResourceCategory.MATERIALS: 300 * severity
            },
            ChallengeType.PANDEMIC: {
                ResourceCategory.HUMAN_CAPACITY: 1000 * severity,
                ResourceCategory.KNOWLEDGE: 600 * severity,
                ResourceCategory.MATERIALS: 400 * severity,
                ResourceCategory.TECHNOLOGY: 300 * severity
            },
            ChallengeType.NATURAL_DISASTER: {
                ResourceCategory.HUMAN_CAPACITY: 800 * severity,
                ResourceCategory.MATERIALS: 600 * severity,
                ResourceCategory.FOOD: 400 * severity,
                ResourceCategory.WATER: 500 * severity
            }
        }
        
        return base_requirements.get(challenge_type, {
            ResourceCategory.HUMAN_CAPACITY: 500 * severity,
            ResourceCategory.KNOWLEDGE: 200 * severity
        })
    
    def _calculate_coordination_complexity(self, affected_regions: List[str]) -> float:
        """Calculate coordination complexity based on affected regions"""
        num_regions = len(affected_regions)
        
        # More regions = higher complexity
        region_complexity = min(1.0, num_regions / 10)
        
        # Calculate network distance complexity
        if len(affected_regions) > 1:
            affected_communities = []
            for region in affected_regions:
                affected_communities.extend(self.bioregions.get(region, []))
            
            if len(affected_communities) > 1:
                # Calculate average shortest path between affected communities
                try:
                    paths = []
                    for i, comm1 in enumerate(affected_communities):
                        for comm2 in affected_communities[i+1:]:
                            if self.network_graph.has_node(comm1) and self.network_graph.has_node(comm2):
                                try:
                                    path_length = nx.shortest_path_length(self.network_graph, comm1, comm2)
                                    paths.append(path_length)
                                except nx.NetworkXNoPath:
                                    paths.append(10)  # High penalty for disconnected communities
                    
                    if paths:
                        avg_path_length = np.mean(paths)
                        network_complexity = min(1.0, avg_path_length / 5)
                    else:
                        network_complexity = 0.5
                except:
                    network_complexity = 0.5
            else:
                network_complexity = 0.1
        else:
            network_complexity = 0.1
        
        return (region_complexity * 0.6 + network_complexity * 0.4)
    
    def create_proposal(self, title: str, description: str, scope: DecisionScope,
                       proposed_actions: List[Dict], proposer_community: str) -> str:
        """Create a new proposal for community voting"""
        proposal_id = f"proposal_{len(self.active_proposals):04d}"
        
        proposal = {
            'proposal_id': proposal_id,
            'title': title,
            'description': description,
            'scope': scope,
            'proposed_actions': proposed_actions,
            'proposer_community': proposer_community,
            'created_date': datetime.now(),
            'voting_deadline': datetime.now() + timedelta(days=7),  # 7 days to vote
            'votes': {'for': [], 'against': [], 'abstain': []},
            'status': 'active',
            'eligible_voters': self._determine_eligible_voters(scope, proposer_community)
        }
        
        self.active_proposals[proposal_id] = proposal
        return proposal_id
    
    def _determine_eligible_voters(self, scope: DecisionScope, proposer_community: str) -> List[str]:
        """Determine which communities can vote on a proposal"""
        if scope == DecisionScope.LOCAL:
            return [proposer_community]
        elif scope == DecisionScope.BIOREGIONAL:
            proposer_bioregion = self.communities[proposer_community].bioregion
            return self.bioregions[proposer_bioregion]
        elif scope == DecisionScope.CONTINENTAL:
            # For simplicity, include all communities in nearby bioregions
            proposer_bioregion = self.communities[proposer_community].bioregion
            eligible = list(self.bioregions[proposer_bioregion])
            # Add neighboring bioregions (simplified)
            for bioregion, communities in self.bioregions.items():
                if bioregion != proposer_bioregion and len(eligible) < 50:
                    eligible.extend(communities[:10])  # Add up to 10 from each region
            return eligible
        else:  # PLANETARY
            return list(self.communities.keys())
    
    def cast_vote(self, proposal_id: str, community_id: str, vote: str) -> bool:
        """Cast a vote on a proposal"""
        if proposal_id not in self.active_proposals:
            return False
        
        proposal = self.active_proposals[proposal_id]
        
        # Check if community is eligible to vote
        if community_id not in proposal['eligible_voters']:
            return False
        
        # Check if voting is still open
        if datetime.now() > proposal['voting_deadline']:
            return False
        
        # Remove any previous vote from this community
        for vote_type in ['for', 'against', 'abstain']:
            if community_id in proposal['votes'][vote_type]:
                proposal['votes'][vote_type].remove(community_id)
        
        # Cast new vote
        if vote in ['for', 'against', 'abstain']:
            proposal['votes'][vote].append(community_id)
            return True
        
        return False
    
    def finalize_proposal_voting(self, proposal_id: str) -> Dict:
        """Finalize voting on a proposal and determine outcome"""
        if proposal_id not in self.active_proposals:
            return {}
        
        proposal = self.active_proposals[proposal_id]
        
        # Calculate vote weights based on community characteristics
        weighted_votes = {'for': 0.0, 'against': 0.0, 'abstain': 0.0}
        
        for vote_type, communities in proposal['votes'].items():
            for community_id in communities:
                if community_id in self.communities:
                    community = self.communities[community_id]
                    # Weight based on population, participation, and expertise relevance
                    weight = (
                        math.log(community.population) * 0.4 +  # Population weight (logarithmic)
                        community.participation_level * 0.3 +   # Participation weight
                        community.decision_weight * 0.3         # General decision weight
                    )
                    weighted_votes[vote_type] += weight
        
        # Determine outcome
        total_votes = sum(weighted_votes.values())
        if total_votes == 0:
            result = 'failed_no_participation'
        else:
            for_percentage = weighted_votes['for'] / total_votes
            against_percentage = weighted_votes['against'] / total_votes
            
            # Require different thresholds based on scope
            scope_thresholds = {
                DecisionScope.LOCAL: 0.5,        # Simple majority
                DecisionScope.BIOREGIONAL: 0.6,  # 60% majority
                DecisionScope.CONTINENTAL: 0.7,  # 70% majority
                DecisionScope.PLANETARY: 0.75    # 75% majority
            }
            
            required_threshold = scope_thresholds[proposal['scope']]
            
            if for_percentage >= required_threshold:
                result = 'approved'
            elif against_percentage >= required_threshold:
                result = 'rejected'
            else:
                result = 'no_consensus'
        
        # Create decision record
        decision_record = {
            'proposal_id': proposal_id,
            'title': proposal['title'],
            'scope': proposal['scope'].value,
            'voting_method': 'weighted',
            'participants': len(proposal['eligible_voters']),
            'votes_for': len(proposal['votes']['for']),
            'votes_against': len(proposal['votes']['against']),
            'abstentions': len(proposal['votes']['abstain']),
            'weighted_for': weighted_votes['for'],
            'weighted_against': weighted_votes['against'],
            'weighted_abstain': weighted_votes['abstain'],
            'result': result,
            'implementation_status': 'pending' if result == 'approved' else 'not_applicable',
            'decided_date': datetime.now()
        }
        
        # Move to decision history
        self.decision_history.append(decision_record)
        del self.active_proposals[proposal_id]
        
        # Save to database
        self._save_decision_to_db(decision_record)
        
        # If approved, implement the proposal
        if result == 'approved':
            self._implement_proposal(proposal, decision_record)
        
        return decision_record
    
    def _implement_proposal(self, proposal: Dict, decision_record: Dict):
        """Implement an approved proposal"""
        for action in proposal['proposed_actions']:
            action_type = action.get('type')
            
            if action_type == 'resource_allocation':
                self._implement_resource_allocation(action)
            elif action_type == 'challenge_response':
                self._implement_challenge_response(action)
            elif action_type == 'network_expansion':
                self._implement_network_expansion(action)
            elif action_type == 'policy_change':
                self._implement_policy_change(action)
        
        # Update implementation status
        decision_record['implementation_status'] = 'completed'
    
    def _implement_resource_allocation(self, action: Dict):
        """Implement resource allocation action"""
        resource_id = action.get('resource_id')
        allocations = action.get('allocations', {})
        
        if resource_id in self.global_resources:
            resource = self.global_resources[resource_id]
            
            # Update allocations
            for community_id, amount in allocations.items():
                if community_id in self.communities:
                    resource.current_allocation[community_id] = amount
    
    def _implement_challenge_response(self, action: Dict):
        """Implement challenge response action"""
        challenge_id = action.get('challenge_id')
        response_plan = action.get('response_plan', {})
        
        if challenge_id in self.active_challenges:
            challenge = self.active_challenges[challenge_id]
            
            # Calculate success probability based on allocated resources
            allocated_resources = response_plan.get('allocated_resources', {})
            success_factors = []
            
            for resource_category, required_amount in challenge.required_resources.items():
                allocated_amount = allocated_resources.get(resource_category.value, 0.0)
                if required_amount > 0:
                    fulfillment_ratio = min(1.0, allocated_amount / required_amount)
                    success_factors.append(fulfillment_ratio)
            
            if success_factors:
                base_success_probability = np.mean(success_factors)
                
                # Adjust for coordination complexity
                coordination_bonus = 1.0 - challenge.coordination_complexity * 0.3
                challenge.success_probability = base_success_probability * coordination_bonus
                
                # If success probability is high enough, resolve the challenge
                if challenge.success_probability > 0.7:
                    self._resolve_challenge(challenge_id, True)
                elif challenge.success_probability < 0.3:
                    self._resolve_challenge(challenge_id, False)
    
    def _resolve_challenge(self, challenge_id: str, success: bool):
        """Resolve a global challenge"""
        if challenge_id in self.active_challenges:
            challenge = self.active_challenges[challenge_id]
            challenge.resolved_date = datetime.now()
            challenge.success = success
            
            # Move to resolved challenges
            self.resolved_challenges.append(challenge)
            del self.active_challenges[challenge_id]
            
            # Update challenge in database
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE challenges 
                SET status = ?, resolved_date = ?
                WHERE id = ?
            ''', ('resolved_success' if success else 'resolved_failure', 
                  challenge.resolved_date.isoformat(), challenge_id))
            self.conn.commit()
    
    def optimize_global_resources(self) -> Dict:
        """Optimize global resource allocation using linear programming"""
        if not self.communities or not self.global_resources:
            return {}
        
        # Prepare optimization problem
        communities = list(self.communities.keys())
        resources = list(self.global_resources.keys())
        
        num_communities = len(communities)
        num_resources = len(resources)
        
        # Decision variables: allocation[i][j] = amount of resource j allocated to community i
        num_variables = num_communities * num_resources
        
        # Objective function coefficients (maximize total utility)
        c = []
        for i, community_id in enumerate(communities):
            community = self.communities[community_id]
            for j, resource_id in enumerate(resources):
                resource = self.global_resources[resource_id]
                
                # Utility based on community need and resource scarcity
                need = community.resource_consumption.get(resource.category, 0.0)
                scarcity = resource.get_utilization_rate()
                utility = need * (1.0 + scarcity)  # Higher utility for scarce resources
                
                c.append(-utility)  # Negative because linprog minimizes
        
        # Constraints
        A_ub = []  # Inequality constraints (Ax <= b)
        b_ub = []
        
        # Resource availability constraints
        for j, resource_id in enumerate(resources):
            resource = self.global_resources[resource_id]
            constraint = [0.0] * num_variables
            
            for i in range(num_communities):
                var_index = i * num_resources + j
                constraint[var_index] = 1.0
            
            A_ub.append(constraint)
            b_ub.append(resource.total_available * resource.sustainability_threshold)
        
        # Non-negativity bounds
        bounds = [(0, None) for _ in range(num_variables)]
        
        # Solve optimization problem
        try:
            result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
            
            if result.success:
                # Extract allocation results
                allocation_results = {}
                for i, community_id in enumerate(communities):
                    allocation_results[community_id] = {}
                    for j, resource_id in enumerate(resources):
                        var_index = i * num_resources + j
                        allocation_results[community_id][resource_id] = result.x[var_index]
                
                # Update global resource allocations
                for resource_id in resources:
                    resource = self.global_resources[resource_id]
                    resource.current_allocation = {}
                    for community_id in communities:
                        amount = allocation_results[community_id][resource_id]
                        if amount > 0.01:  # Only store significant allocations
                            resource.current_allocation[community_id] = amount
                
                return {
                    'success': True,
                    'optimal_value': -result.fun,  # Convert back to positive
                    'allocations': allocation_results,
                    'resource_utilization': {
                        resource_id: resource.get_utilization_rate() 
                        for resource_id, resource in self.global_resources.items()
                    }
                }
            else:
                return {'success': False, 'message': 'Optimization failed'}
        
        except Exception as e:
            return {'success': False, 'message': f'Optimization error: {str(e)}'}
    
    def simulate_crisis_response(self, crisis_type: ChallengeType, severity: float) -> Dict:
        """Simulate response to a global crisis"""
        # Create crisis challenge
        affected_regions = random.sample(list(self.bioregions.keys()), 
                                       min(3, len(self.bioregions)))
        
        crisis = self.create_global_challenge(
            challenge_type=crisis_type,
            severity=severity,
            affected_regions=affected_regions,
            time_sensitivity=30  # 30 days to respond
        )
        
        # Simulate emergency coordination
        response_timeline = []
        
        # Day 1: Crisis detection and alert
        response_timeline.append({
            'day': 1,
            'event': 'crisis_detected',
            'description': f'{crisis_type.value} detected with severity {severity}',
            'affected_regions': affected_regions
        })
        
        # Day 2-3: Emergency proposal creation
        proposal_id = self.create_proposal(
            title=f"Emergency Response to {crisis_type.value}",
            description=f"Coordinate response to {crisis_type.value} affecting {len(affected_regions)} regions",
            scope=DecisionScope.PLANETARY,
            proposed_actions=[{
                'type': 'challenge_response',
                'challenge_id': crisis.challenge_id,
                'response_plan': {
                    'allocated_resources': {
                        category.value: amount * 1.5  # Emergency allocation
                        for category, amount in crisis.required_resources.items()
                    }
                }
            }],
            proposer_community=random.choice(list(self.communities.keys()))
        )
        
        response_timeline.append({
            'day': 2,
            'event': 'emergency_proposal_created',
            'proposal_id': proposal_id
        })
        
        # Day 3-5: Rapid voting simulation
        eligible_voters = self.active_proposals[proposal_id]['eligible_voters']
        
        # Simulate high participation rate during crisis
        participation_rate = 0.9
        voters = random.sample(eligible_voters, int(len(eligible_voters) * participation_rate))
        
        # Most communities vote in favor during crisis
        for community_id in voters:
            vote = 'for' if random.random() < 0.85 else 'against'  # 85% approval rate
            self.cast_vote(proposal_id, community_id, vote)
        
        response_timeline.append({
            'day': 5,
            'event': 'emergency_voting_completed',
            'participation_rate': participation_rate,
            'voters': len(voters)
        })
        
        # Finalize voting
        decision = self.finalize_proposal_voting(proposal_id)
        
        response_timeline.append({
            'day': 6,
            'event': 'decision_finalized',
            'result': decision['result'],
            'implementation_status': decision['implementation_status']
        })
        
        # Calculate response effectiveness
        if decision['result'] == 'approved':
            response_effectiveness = min(1.0, decision['weighted_for'] / (decision['weighted_for'] + decision['weighted_against']))
            
            # Update challenge success probability
            if crisis.challenge_id in self.active_challenges:
                crisis.success_probability = response_effectiveness * 0.8  # Crisis response bonus
                
                if crisis.success_probability > 0.6:
                    self._resolve_challenge(crisis.challenge_id, True)
                    response_timeline.append({
                        'day': 15,
                        'event': 'crisis_resolved',
                        'success': True,
                        'effectiveness': response_effectiveness
                    })
                else:
                    response_timeline.append({
                        'day': 30,
                        'event': 'crisis_ongoing',
                        'success': False,
                        'effectiveness': response_effectiveness
                    })
        else:
            response_timeline.append({
                'day': 30,
                'event': 'crisis_response_failed',
                'reason': 'proposal_rejected'
            })
        
        return {
            'crisis': {
                'type': crisis_type.value,
                'severity': severity,
                'affected_regions': affected_regions,
                'coordination_complexity': crisis.coordination_complexity
            },
            'response_timeline': response_timeline,
            'final_outcome': response_timeline[-1],
            'decision_record': decision
        }
    
    def get_system_metrics(self) -> Dict:
        """Get comprehensive World Game system metrics"""
        if not self.communities:
            return {}
        
        # Calculate coordination effectiveness
        total_connections = self.network_graph.number_of_edges()
        possible_connections = len(self.communities) * (len(self.communities) - 1) / 2
        network_density = total_connections / possible_connections if possible_connections > 0 else 0
        
        avg_trust = np.mean([
            np.mean(list(community.trust_relationships.values())) 
            for community in self.communities.values() 
            if community.trust_relationships
        ]) if any(c.trust_relationships for c in self.communities.values()) else 0
        
        self.coordination_effectiveness = (network_density * 0.4 + avg_trust * 0.6)
        
        # Calculate resource optimization score
        sustainable_resources = sum(1 for r in self.global_resources.values() if r.is_sustainable())
        total_resources = len(self.global_resources)
        self.resource_optimization_score = sustainable_resources / total_resources if total_resources > 0 else 0
        
        # Calculate democratic participation rate
        recent_decisions = [d for d in self.decision_history 
                          if d['decided_date'] > datetime.now() - timedelta(days=30)]
        
        if recent_decisions:
            total_eligible = sum(d['participants'] for d in recent_decisions)
            total_participated = sum(d['votes_for'] + d['votes_against'] + d['abstentions'] 
                                   for d in recent_decisions)
            self.democratic_participation_rate = total_participated / total_eligible if total_eligible > 0 else 0
        else:
            self.democratic_participation_rate = 0
        
        # Calculate challenge resolution rate
        total_challenges = len(self.resolved_challenges) + len(self.active_challenges)
        successful_resolutions = sum(1 for c in self.resolved_challenges if hasattr(c, 'success') and c.success)
        self.challenge_resolution_rate = successful_resolutions / total_challenges if total_challenges > 0 else 0
        
        # Resource status
        resource_status = {}
        for resource_id, resource in self.global_resources.items():
            resource_status[resource_id] = {
                'category': resource.category.value,
                'utilization_rate': resource.get_utilization_rate(),
                'is_sustainable': resource.is_sustainable(),
                'is_critical': resource.is_critical(),
                'total_allocated': sum(resource.current_allocation.values())
            }
        
        # Challenge status
        challenge_status = {
            'active_challenges': len(self.active_challenges),
            'resolved_challenges': len(self.resolved_challenges),
            'average_urgency': np.mean([c.calculate_urgency() for c in self.active_challenges.values()]) if self.active_challenges else 0,
            'average_complexity': np.mean([c.coordination_complexity for c in self.active_challenges.values()]) if self.active_challenges else 0
        }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'coordination_effectiveness': self.coordination_effectiveness,
            'resource_optimization_score': self.resource_optimization_score,
            'democratic_participation_rate': self.democratic_participation_rate,
            'challenge_resolution_rate': self.challenge_resolution_rate,
            'network_metrics': {
                'total_communities': len(self.communities),
                'total_connections': total_connections,
                'network_density': network_density,
                'average_trust': avg_trust,
                'bioregions': len(self.bioregions)
            },
            'resource_status': resource_status,
            'challenge_status': challenge_status,
            'governance_metrics': {
                'active_proposals': len(self.active_proposals),
                'recent_decisions': len(recent_decisions),
                'approval_rate': np.mean([1 if d['result'] == 'approved' else 0 for d in recent_decisions]) if recent_decisions else 0
            }
        }
    
    def _save_community_to_db(self, community: CommunityNode):
        """Save community to database"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO communities 
            (id, name, population, latitude, longitude, bioregion, participation_level, decision_weight)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            community.community_id, community.name, community.population,
            community.location[0], community.location[1], community.bioregion,
            community.participation_level, community.decision_weight
        ))
        self.conn.commit()
    
    def _save_resource_to_db(self, resource: GlobalResource):
        """Save resource to database"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO global_resources 
            (id, category, total_available, regeneration_rate, depletion_rate,
             sustainability_threshold, critical_threshold, current_utilization)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            resource.resource_id, resource.category.value, resource.total_available,
            resource.regeneration_rate, resource.depletion_rate,
            resource.sustainability_threshold, resource.critical_threshold,
            resource.get_utilization_rate()
        ))
        self.conn.commit()
    
    def _save_challenge_to_db(self, challenge: GlobalChallenge):
        """Save challenge to database"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO challenges 
            (id, type, severity, time_sensitivity, coordination_complexity, status, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            challenge.challenge_id, challenge.challenge_type.value, challenge.severity,
            challenge.time_sensitivity, challenge.coordination_complexity,
            'active', datetime.now().isoformat()
        ))
        self.conn.commit()
    
    def _save_decision_to_db(self, decision: Dict):
        """Save decision to database"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO decisions 
            (id, proposal_title, decision_scope, voting_method, participants,
             votes_for, votes_against, abstentions, result, implementation_status,
             created_date, decided_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            decision['proposal_id'], decision['title'], decision['scope'],
            decision['voting_method'], decision['participants'],
            decision['votes_for'], decision['votes_against'], decision['abstentions'],
            decision['result'], decision['implementation_status'],
            datetime.now().isoformat(), decision['decided_date'].isoformat()
        ))
        self.conn.commit()

class PlanetaryCoordinationSimulator:
    """
    Comprehensive simulator for planetary coordination scenarios
    """
    
    def __init__(self, num_communities: int = 100, num_bioregions: int = 10):
        self.num_communities = num_communities
        self.num_bioregions = num_bioregions
        
        # Initialize World Game engine
        self.world_game = WorldGameEngine()
        
        # Simulation parameters
        self.simulation_days = 365
        self.current_day = 0
        
        # Metrics tracking
        self.daily_metrics: List[Dict] = []
        
        # Initialize simulation
        self._initialize_planetary_network()
        self._initialize_baseline_challenges()
    
    def _initialize_planetary_network(self):
        """Initialize a realistic planetary network of communities"""
        print(f"Initializing planetary network with {self.num_communities} communities...")
        
        # Create bioregions
        bioregion_names = [
            'North_America_Pacific', 'North_America_Atlantic', 'South_America_Amazon',
            'Europe_Mediterranean', 'Africa_Sahel', 'Asia_Monsoon',
            'Australia_Outback', 'Arctic_Tundra', 'Pacific_Islands', 'Antarctic_Research'
        ]
        
        bioregions = bioregion_names[:self.num_bioregions]
        
        # Create communities distributed across bioregions
        for i in range(self.num_communities):
            community_id = f"community_{i:03d}"
            bioregion = bioregions[i % len(bioregions)]
            
            # Generate realistic community characteristics
            population = int(np.random.lognormal(5.5, 1.0))  # Log-normal distribution
            population = max(50, min(10000, population))  # Constrain to reasonable range
            
            # Generate location within bioregion (simplified)
            base_lat = (i % len(bioregions)) * 18 - 90  # Distribute across latitudes
            base_lon = ((i // len(bioregions)) % 20) * 18 - 180  # Distribute across longitudes
            
            location = (
                base_lat + random.uniform(-5, 5),
                base_lon + random.uniform(-5, 5)
            )
            
            name = f"{bioregion}_Community_{i % 20 + 1}"
            
            self.world_game.add_community(community_id, name, population, location, bioregion)
        
        # Create network connections
        print("Creating network connections...")
        communities = list(self.world_game.communities.keys())
        
        # Connect communities within bioregions (high trust)
        for bioregion, community_list in self.world_game.bioregions.items():
            for i, comm1 in enumerate(community_list):
                for comm2 in community_list[i+1:]:
                    if random.random() < 0.4:  # 40% chance of connection within bioregion
                        trust_level = random.uniform(0.6, 0.9)
                        self.world_game.connect_communities(comm1, comm2, trust_level)
        
        # Create inter-bioregional connections (lower trust)
        for _ in range(self.num_communities // 2):
            comm1 = random.choice(communities)
            comm2 = random.choice(communities)
            
            if (comm1 != comm2 and 
                self.world_game.communities[comm1].bioregion != self.world_game.communities[comm2].bioregion and
                not self.world_game.network_graph.has_edge(comm1, comm2)):
                
                trust_level = random.uniform(0.3, 0.7)
                self.world_game.connect_communities(comm1, comm2, trust_level)
        
        print(f"Network created: {len(communities)} communities, {self.world_game.network_graph.number_of_edges()} connections")
    
    def _initialize_baseline_challenges(self):
        """Initialize baseline global challenges"""
        baseline_challenges = [
            (ChallengeType.CLIMATE_CRISIS, 0.7, ['North_America_Pacific', 'Europe_Mediterranean'], 180),
            (ChallengeType.RESOURCE_SCARCITY, 0.5, ['Africa_Sahel', 'Asia_Monsoon'], 120),
            (ChallengeType.ECOSYSTEM_COLLAPSE, 0.6, ['South_America_Amazon', 'Pacific_Islands'], 90)
        ]
        
        for challenge_type, severity, regions, time_sensitivity in baseline_challenges:
            self.world_game.create_global_challenge(challenge_type, severity, regions, time_sensitivity)
    
    def run_planetary_simulation(self):
        """Run comprehensive planetary coordination simulation"""
        print("\nStarting Planetary Coordination Simulation")
        print("=" * 60)
        
        for day in range(self.simulation_days):
            self.current_day = day
            
            # Simulate daily activities
            self._simulate_daily_coordination()
            
            # Collect metrics
            self._collect_daily_metrics()
            
            # Monthly reports
            if day % 30 == 0:
                self._print_monthly_report()
            
            # Quarterly major events
            if day % 90 == 0 and day > 0:
                self._simulate_quarterly_events()
        
        # Generate final report
        self._generate_final_report()
    
    def _simulate_daily_coordination(self):
        """Simulate daily coordination activities"""
        # Random proposal creation (1% chance per day)
        if random.random() < 0.01:
            self._create_random_proposal()
        
        # Process active proposals (voting)
        for proposal_id in list(self.world_game.active_proposals.keys()):
            proposal = self.world_game.active_proposals[proposal_id]
            
            # Simulate daily voting activity
            eligible_voters = proposal['eligible_voters']
            daily_voters = random.sample(eligible_voters, min(5, len(eligible_voters)))
            
            for voter in daily_voters:
                if voter not in [v for votes in proposal['votes'].values() for v in votes]:
                    vote = random.choices(['for', 'against', 'abstain'], weights=[0.6, 0.3, 0.1])[0]
                    self.world_game.cast_vote(proposal_id, voter, vote)
            
            # Check if voting deadline reached
            if datetime.now() >= proposal['voting_deadline']:
                self.world_game.finalize_proposal_voting(proposal_id)
        
        # Challenge evolution
        for challenge in list(self.world_game.active_challenges.values()):
            challenge.time_sensitivity -= 1
            
            # Remove expired challenges
            if challenge.time_sensitivity <= 0:
                self.world_game._resolve_challenge(challenge.challenge_id, False)
        
        # Resource optimization (weekly)
        if self.current_day % 7 == 0:
            self.world_game.optimize_global_resources()
    
    def _create_random_proposal(self):
        """Create a random proposal for testing"""
        proposal_types = [
            {
                'title': 'Renewable Energy Expansion',
                'scope': DecisionScope.BIOREGIONAL,
                'actions': [{'type': 'resource_allocation', 'resource_id': 'global_energy'}]
            },
            {
                'title': 'Knowledge Sharing Initiative',
                'scope': DecisionScope.CONTINENTAL,
                'actions': [{'type': 'network_expansion'}]
            },
            {
                'title': 'Ecosystem Restoration Project',
                'scope': DecisionScope.PLANETARY,
                'actions': [{'type': 'resource_allocation', 'resource_id': 'global_ecosystem_health'}]
            }
        ]
        
        proposal_template = random.choice(proposal_types)
        proposer = random.choice(list(self.world_game.communities.keys()))
        
        self.world_game.create_proposal(
            title=proposal_template['title'],
            description=f"Proposed by {proposer} on day {self.current_day}",
            scope=proposal_template['scope'],
            proposed_actions=proposal_template['actions'],
            proposer_community=proposer
        )
    
    def _simulate_quarterly_events(self):
        """Simulate major quarterly events"""
        event_types = ['crisis', 'opportunity', 'innovation']
        event_type = random.choice(event_types)
        
        if event_type == 'crisis':
            # Simulate crisis response
            crisis_types = list(ChallengeType)
            crisis_type = random.choice(crisis_types)
            severity = random.uniform(0.4, 0.9)
            
            print(f"\nDay {self.current_day}: {crisis_type.value} crisis (severity: {severity:.2f})")
            response = self.world_game.simulate_crisis_response(crisis_type, severity)
            
            print(f"Crisis response: {response['final_outcome']['event']}")
        
        elif event_type == 'innovation':
            # Simulate technological breakthrough
            print(f"\nDay {self.current_day}: Technological breakthrough - enhancing coordination capacity")
            
            # Randomly improve some communities' coordination capacity
            communities = random.sample(list(self.world_game.communities.keys()), 
                                       min(10, len(self.world_game.communities)))
            
            for community_id in communities:
                community = self.world_game.communities[community_id]
                community.coordination_capacity = min(1.0, community.coordination_capacity + 0.1)
    
    def _collect_daily_metrics(self):
        """Collect daily metrics"""
        metrics = self.world_game.get_system_metrics()
        metrics['day'] = self.current_day
        self.daily_metrics.append(metrics)
    
    def _print_monthly_report(self):
        """Print monthly progress report"""
        if not self.daily_metrics:
            return
        
        latest_metrics = self.daily_metrics[-1]
        
        print(f"\nDay {self.current_day} Monthly Report:")
        print(f"  Coordination Effectiveness: {latest_metrics['coordination_effectiveness']:.3f}")
        print(f"  Resource Optimization: {latest_metrics['resource_optimization_score']:.3f}")
        print(f"  Democratic Participation: {latest_metrics['democratic_participation_rate']:.3f}")
        print(f"  Challenge Resolution Rate: {latest_metrics['challenge_resolution_rate']:.3f}")
        print(f"  Active Challenges: {latest_metrics['challenge_status']['active_challenges']}")
        print(f"  Network Density: {latest_metrics['network_metrics']['network_density']:.3f}")
    
    def _generate_final_report(self):
        """Generate comprehensive final report"""
        print("\n" + "=" * 60)
        print("PLANETARY COORDINATION SIMULATION - FINAL REPORT")
        print("=" * 60)
        
        if not self.daily_metrics:
            print("No metrics collected")
            return
        
        initial_metrics = self.daily_metrics[0]
        final_metrics = self.daily_metrics[-1]
        
        # Calculate improvements
        coordination_improvement = final_metrics['coordination_effectiveness'] - initial_metrics['coordination_effectiveness']
        resource_improvement = final_metrics['resource_optimization_score'] - initial_metrics['resource_optimization_score']
        participation_improvement = final_metrics['democratic_participation_rate'] - initial_metrics['democratic_participation_rate']
        
        print(f"\nSYSTEM EVOLUTION OVER {self.simulation_days} DAYS:")
        print(f"  Coordination Effectiveness: {initial_metrics['coordination_effectiveness']:.3f} → {final_metrics['coordination_effectiveness']:.3f} ({coordination_improvement:+.3f})")
        print(f"  Resource Optimization: {initial_metrics['resource_optimization_score']:.3f} → {final_metrics['resource_optimization_score']:.3f} ({resource_improvement:+.3f})")
        print(f"  Democratic Participation: {initial_metrics['democratic_participation_rate']:.3f} → {final_metrics['democratic_participation_rate']:.3f} ({participation_improvement:+.3f})")
        print(f"  Challenge Resolution Rate: {final_metrics['challenge_resolution_rate']:.3f}")
        
        print(f"\nNETWORK CHARACTERISTICS:")
        print(f"  Total Communities: {final_metrics['network_metrics']['total_communities']}")
        print(f"  Network Connections: {final_metrics['network_metrics']['total_connections']}")
        print(f"  Network Density: {final_metrics['network_metrics']['network_density']:.3f}")
        print(f"  Average Trust Level: {final_metrics['network_metrics']['average_trust']:.3f}")
        print(f"  Bioregions: {final_metrics['network_metrics']['bioregions']}")
        
        print(f"\nGOVERNANCE PERFORMANCE:")
        print(f"  Total Decisions Made: {len(self.world_game.decision_history)}")
        print(f"  Approval Rate: {final_metrics['governance_metrics']['approval_rate']:.3f}")
        print(f"  Average Participation: {final_metrics['democratic_participation_rate']:.3f}")
        
        print(f"\nRESOURCE MANAGEMENT:")
        sustainable_resources = sum(1 for r in final_metrics['resource_status'].values() if r['is_sustainable'])
        total_resources = len(final_metrics['resource_status'])
        print(f"  Sustainable Resources: {sustainable_resources}/{total_resources}")
        print(f"  Critical Resources: {sum(1 for r in final_metrics['resource_status'].values() if r['is_critical'])}")
        
        print(f"\nCHALLENGE MANAGEMENT:")
        print(f"  Challenges Resolved: {len(self.world_game.resolved_challenges)}")
        print(f"  Active Challenges: {len(self.world_game.active_challenges)}")
        print(f"  Resolution Success Rate: {final_metrics['challenge_resolution_rate']:.3f}")
        
        # Success indicators
        print(f"\nSUCCESS INDICATORS:")
        print(f"  ✓ Effective Coordination: {final_metrics['coordination_effectiveness'] > 0.6}")
        print(f"  ✓ Resource Sustainability: {final_metrics['resource_optimization_score'] > 0.7}")
        print(f"  ✓ Democratic Engagement: {final_metrics['democratic_participation_rate'] > 0.5}")
        print(f"  ✓ Crisis Response Capability: {final_metrics['challenge_resolution_rate'] > 0.6}")
        print(f"  ✓ Network Resilience: {final_metrics['network_metrics']['network_density'] > 0.1}")

if __name__ == "__main__":
    # Run comprehensive planetary coordination simulation
    print("LIFE System World Game and Planetary Coordination Simulation")
    print("=" * 60)
    
    # Create and run simulation
    simulator = PlanetaryCoordinationSimulator(num_communities=50, num_bioregions=8)
    simulator.run_planetary_simulation()
    
    print("\nSimulation completed successfully!")
    print("Planetary coordination and World Game capabilities demonstrated.")

