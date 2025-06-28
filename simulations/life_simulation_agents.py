#!/usr/bin/env python3
"""
LIFE System Comprehensive Simulation - Agent Models
==================================================

This module implements sophisticated agent-based models for simulating
individual and community behavior within the LIFE System framework.

Author: Manus AI
Date: June 28, 2025
Version: 1.0
"""

import random
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum
import json
import sqlite3
from datetime import datetime, timedelta
import math

class PersonalityType(Enum):
    """Personality types affecting agent behavior"""
    INNOVATOR = "innovator"
    COLLABORATOR = "collaborator"
    CAREGIVER = "caregiver"
    ORGANIZER = "organizer"
    CREATOR = "creator"
    ANALYST = "analyst"

class ValueSystem(Enum):
    """Core value systems that guide agent decisions"""
    ENVIRONMENTAL = "environmental"
    SOCIAL_EQUITY = "social_equity"
    INNOVATION = "innovation"
    COMMUNITY = "community"
    PERSONAL_GROWTH = "personal_growth"
    SPIRITUAL = "spiritual"

class SkillCategory(Enum):
    """Categories of skills agents can develop"""
    TECHNICAL = "technical"
    CREATIVE = "creative"
    SOCIAL = "social"
    ANALYTICAL = "analytical"
    PHYSICAL = "physical"
    LEADERSHIP = "leadership"

@dataclass
class Skill:
    """Represents a specific skill with proficiency level"""
    name: str
    category: SkillCategory
    proficiency: float  # 0.0 to 1.0
    learning_rate: float = 0.1
    decay_rate: float = 0.01
    
    def practice(self, hours: float) -> float:
        """Practice skill and improve proficiency"""
        improvement = hours * self.learning_rate * (1.0 - self.proficiency)
        self.proficiency = min(1.0, self.proficiency + improvement)
        return improvement
    
    def decay(self, days: int) -> float:
        """Natural skill decay over time"""
        decay = days * self.decay_rate * self.proficiency
        self.proficiency = max(0.0, self.proficiency - decay)
        return decay

@dataclass
class SocialConnection:
    """Represents a relationship between agents"""
    agent_id: str
    trust_level: float  # 0.0 to 1.0
    interaction_frequency: float  # interactions per day
    relationship_type: str  # family, friend, colleague, neighbor
    shared_activities: Set[str] = field(default_factory=set)
    collaboration_history: List[Dict] = field(default_factory=list)
    
    def strengthen_trust(self, amount: float):
        """Increase trust through positive interactions"""
        self.trust_level = min(1.0, self.trust_level + amount)
    
    def weaken_trust(self, amount: float):
        """Decrease trust through negative interactions"""
        self.trust_level = max(0.0, self.trust_level - amount)

class IndividualAgent:
    """
    Sophisticated individual agent model representing a person
    participating in the LIFE System
    """
    
    def __init__(self, agent_id: str, age: int, education_level: str, 
                 cultural_background: str, personality: PersonalityType,
                 primary_values: List[ValueSystem]):
        self.agent_id = agent_id
        self.age = age
        self.education_level = education_level
        self.cultural_background = cultural_background
        self.personality = personality
        self.primary_values = primary_values
        
        # Economic attributes
        self.contribution_score = 0.0
        self.trust_tokens = 100.0
        self.regenerative_credits = 0.0
        self.resource_balance = 1000.0  # Starting resources
        
        # Skills and capabilities
        self.skills: Dict[str, Skill] = {}
        self.learning_goals: List[str] = []
        self.current_projects: List[Dict] = []
        
        # Social connections
        self.social_network: Dict[str, SocialConnection] = {}
        self.community_memberships: Set[str] = set()
        
        # Behavioral state
        self.satisfaction_level = 0.5  # 0.0 to 1.0
        self.stress_level = 0.3  # 0.0 to 1.0
        self.motivation_level = 0.7  # 0.0 to 1.0
        
        # Decision-making parameters
        self.risk_tolerance = random.uniform(0.2, 0.8)
        self.cooperation_tendency = random.uniform(0.3, 0.9)
        self.innovation_openness = random.uniform(0.2, 0.8)
        
        # Initialize basic skills
        self._initialize_skills()
        
        # Activity tracking
        self.daily_activities: List[Dict] = []
        self.weekly_goals: List[Dict] = []
        self.monthly_reflections: List[Dict] = []
    
    def _initialize_skills(self):
        """Initialize agent with basic skills based on background"""
        base_skills = [
            ("communication", SkillCategory.SOCIAL, random.uniform(0.3, 0.7)),
            ("problem_solving", SkillCategory.ANALYTICAL, random.uniform(0.2, 0.6)),
            ("creativity", SkillCategory.CREATIVE, random.uniform(0.2, 0.8)),
            ("collaboration", SkillCategory.SOCIAL, random.uniform(0.3, 0.8)),
            ("learning", SkillCategory.ANALYTICAL, random.uniform(0.4, 0.8)),
        ]
        
        for skill_name, category, proficiency in base_skills:
            self.skills[skill_name] = Skill(
                name=skill_name,
                category=category,
                proficiency=proficiency,
                learning_rate=random.uniform(0.05, 0.15),
                decay_rate=random.uniform(0.005, 0.02)
            )
    
    def make_decision(self, options: List[Dict], context: Dict) -> Dict:
        """
        Multi-criteria decision making based on agent's values and situation
        """
        if not options:
            return None
        
        scored_options = []
        
        for option in options:
            score = self._evaluate_option(option, context)
            scored_options.append((option, score))
        
        # Add some randomness to prevent completely deterministic behavior
        randomness_factor = 0.1
        for i, (option, score) in enumerate(scored_options):
            noise = random.uniform(-randomness_factor, randomness_factor)
            scored_options[i] = (option, score + noise)
        
        # Sort by score and select best option
        scored_options.sort(key=lambda x: x[1], reverse=True)
        chosen_option = scored_options[0][0]
        
        # Record decision for learning
        self._record_decision(chosen_option, context, scored_options[0][1])
        
        return chosen_option
    
    def _evaluate_option(self, option: Dict, context: Dict) -> float:
        """Evaluate an option based on multiple criteria"""
        score = 0.0
        
        # Personal satisfaction factor
        personal_benefit = option.get('personal_benefit', 0.5)
        score += personal_benefit * 0.3
        
        # Community impact factor
        community_impact = option.get('community_impact', 0.5)
        score += community_impact * 0.25
        
        # Environmental impact factor
        environmental_impact = option.get('environmental_impact', 0.5)
        if ValueSystem.ENVIRONMENTAL in self.primary_values:
            score += environmental_impact * 0.3
        else:
            score += environmental_impact * 0.15
        
        # Economic viability factor
        economic_return = option.get('economic_return', 0.5)
        score += economic_return * 0.2
        
        # Risk assessment
        risk_level = option.get('risk_level', 0.5)
        risk_penalty = (risk_level - self.risk_tolerance) * 0.1
        score -= max(0, risk_penalty)
        
        # Social alignment factor
        social_approval = option.get('social_approval', 0.5)
        score += social_approval * 0.15
        
        # Skill development opportunity
        skill_development = option.get('skill_development', 0.0)
        score += skill_development * 0.1
        
        return max(0.0, min(1.0, score))
    
    def _record_decision(self, decision: Dict, context: Dict, score: float):
        """Record decision for learning and adaptation"""
        decision_record = {
            'timestamp': datetime.now().isoformat(),
            'decision': decision,
            'context': context,
            'score': score,
            'satisfaction_before': self.satisfaction_level,
            'stress_before': self.stress_level
        }
        self.daily_activities.append(decision_record)
    
    def interact_with_agent(self, other_agent: 'IndividualAgent', 
                          interaction_type: str, context: Dict) -> Dict:
        """Interact with another agent and update relationship"""
        if other_agent.agent_id not in self.social_network:
            # Create new connection
            self.social_network[other_agent.agent_id] = SocialConnection(
                agent_id=other_agent.agent_id,
                trust_level=0.5,
                interaction_frequency=0.1,
                relationship_type="acquaintance"
            )
        
        connection = self.social_network[other_agent.agent_id]
        
        # Determine interaction outcome based on compatibility
        compatibility = self._calculate_compatibility(other_agent)
        success_probability = 0.5 + (compatibility - 0.5) * 0.5
        
        interaction_successful = random.random() < success_probability
        
        if interaction_successful:
            trust_increase = random.uniform(0.01, 0.05)
            connection.strengthen_trust(trust_increase)
            self.satisfaction_level = min(1.0, self.satisfaction_level + 0.01)
        else:
            trust_decrease = random.uniform(0.01, 0.03)
            connection.weaken_trust(trust_decrease)
            self.stress_level = min(1.0, self.stress_level + 0.01)
        
        # Record interaction
        interaction_record = {
            'timestamp': datetime.now().isoformat(),
            'other_agent': other_agent.agent_id,
            'type': interaction_type,
            'successful': interaction_successful,
            'trust_change': trust_increase if interaction_successful else -trust_decrease,
            'context': context
        }
        
        connection.collaboration_history.append(interaction_record)
        connection.interaction_frequency += 0.1
        
        return interaction_record
    
    def _calculate_compatibility(self, other_agent: 'IndividualAgent') -> float:
        """Calculate compatibility with another agent"""
        compatibility = 0.5  # Base compatibility
        
        # Value alignment
        shared_values = set(self.primary_values) & set(other_agent.primary_values)
        value_bonus = len(shared_values) * 0.1
        compatibility += value_bonus
        
        # Personality compatibility
        personality_matrix = {
            PersonalityType.INNOVATOR: [PersonalityType.ANALYST, PersonalityType.CREATOR],
            PersonalityType.COLLABORATOR: [PersonalityType.ORGANIZER, PersonalityType.CAREGIVER],
            PersonalityType.CAREGIVER: [PersonalityType.COLLABORATOR, PersonalityType.ORGANIZER],
            PersonalityType.ORGANIZER: [PersonalityType.COLLABORATOR, PersonalityType.ANALYST],
            PersonalityType.CREATOR: [PersonalityType.INNOVATOR, PersonalityType.CREATOR],
            PersonalityType.ANALYST: [PersonalityType.INNOVATOR, PersonalityType.ORGANIZER]
        }
        
        if other_agent.personality in personality_matrix.get(self.personality, []):
            compatibility += 0.1
        
        # Age and cultural factors
        age_difference = abs(self.age - other_agent.age)
        age_penalty = min(0.1, age_difference / 200)  # Small penalty for large age gaps
        compatibility -= age_penalty
        
        if self.cultural_background == other_agent.cultural_background:
            compatibility += 0.05
        
        return max(0.0, min(1.0, compatibility))
    
    def contribute_to_community(self, community: 'CommunityAgent', 
                              contribution_type: str, effort_hours: float) -> Dict:
        """Make a contribution to a community"""
        # Calculate contribution value based on skills and effort
        relevant_skills = self._get_relevant_skills(contribution_type)
        skill_multiplier = sum(skill.proficiency for skill in relevant_skills) / max(1, len(relevant_skills))
        
        base_value = effort_hours * skill_multiplier
        
        # Apply personality and value modifiers
        if contribution_type == "environmental_restoration" and ValueSystem.ENVIRONMENTAL in self.primary_values:
            base_value *= 1.2
        elif contribution_type == "community_care" and self.personality == PersonalityType.CAREGIVER:
            base_value *= 1.3
        elif contribution_type == "innovation_project" and self.personality == PersonalityType.INNOVATOR:
            base_value *= 1.25
        
        contribution = {
            'agent_id': self.agent_id,
            'community_id': community.community_id,
            'type': contribution_type,
            'effort_hours': effort_hours,
            'base_value': base_value,
            'timestamp': datetime.now().isoformat(),
            'skills_used': [skill.name for skill in relevant_skills]
        }
        
        # Update agent state
        self.satisfaction_level = min(1.0, self.satisfaction_level + 0.02)
        self.motivation_level = min(1.0, self.motivation_level + 0.01)
        
        # Practice relevant skills
        for skill in relevant_skills:
            skill.practice(effort_hours / len(relevant_skills))
        
        return contribution
    
    def _get_relevant_skills(self, contribution_type: str) -> List[Skill]:
        """Get skills relevant to a specific contribution type"""
        skill_mappings = {
            "environmental_restoration": ["problem_solving", "collaboration"],
            "community_care": ["communication", "collaboration"],
            "innovation_project": ["creativity", "problem_solving"],
            "education": ["communication", "learning"],
            "governance": ["communication", "collaboration", "problem_solving"],
            "resource_management": ["problem_solving", "collaboration"]
        }
        
        relevant_skill_names = skill_mappings.get(contribution_type, ["collaboration"])
        return [self.skills[name] for name in relevant_skill_names if name in self.skills]
    
    def daily_update(self):
        """Update agent state at the end of each day"""
        # Natural stress and satisfaction decay
        self.stress_level = max(0.0, self.stress_level - 0.02)
        self.satisfaction_level = max(0.0, self.satisfaction_level - 0.01)
        
        # Skill decay
        for skill in self.skills.values():
            skill.decay(1)  # One day
        
        # Motivation adjustment based on recent activities
        if len(self.daily_activities) > 0:
            avg_satisfaction = sum(activity.get('satisfaction_before', 0.5) 
                                 for activity in self.daily_activities) / len(self.daily_activities)
            motivation_change = (avg_satisfaction - 0.5) * 0.1
            self.motivation_level = max(0.0, min(1.0, self.motivation_level + motivation_change))
        
        # Clear daily activities
        self.daily_activities = []
    
    def get_status_summary(self) -> Dict:
        """Get comprehensive status summary"""
        return {
            'agent_id': self.agent_id,
            'age': self.age,
            'personality': self.personality.value,
            'primary_values': [v.value for v in self.primary_values],
            'satisfaction_level': round(self.satisfaction_level, 3),
            'stress_level': round(self.stress_level, 3),
            'motivation_level': round(self.motivation_level, 3),
            'contribution_score': round(self.contribution_score, 2),
            'trust_tokens': round(self.trust_tokens, 2),
            'resource_balance': round(self.resource_balance, 2),
            'skill_count': len(self.skills),
            'social_connections': len(self.social_network),
            'community_memberships': len(self.community_memberships)
        }

class CommunityAgent:
    """
    Community-level agent representing a Local Life Circle
    implementing LIFE System principles
    """
    
    def __init__(self, community_id: str, name: str, location: str, 
                 founding_principles: List[str], max_population: int = 500):
        self.community_id = community_id
        self.name = name
        self.location = location
        self.founding_principles = founding_principles
        self.max_population = max_population
        
        # Member management
        self.members: Dict[str, IndividualAgent] = {}
        self.membership_applications: List[Dict] = []
        
        # Governance
        self.governance_structure = "consensus"  # consensus, majority, delegated
        self.decision_history: List[Dict] = []
        self.active_proposals: List[Dict] = []
        
        # Economic systems
        self.contribution_algorithm = ContributionAlgorithm()
        self.trust_network = TrustNetwork()
        self.resource_pool = ResourcePool()
        
        # Community metrics
        self.cohesion_level = 0.5  # 0.0 to 1.0
        self.sustainability_score = 0.5  # 0.0 to 1.0
        self.innovation_index = 0.5  # 0.0 to 1.0
        self.wellbeing_average = 0.5  # 0.0 to 1.0
        
        # Projects and initiatives
        self.active_projects: List[Dict] = []
        self.completed_projects: List[Dict] = []
        
        # External relationships
        self.partner_communities: Set[str] = set()
        self.trade_relationships: Dict[str, Dict] = {}
        
        # Initialize community systems
        self._initialize_systems()
    
    def _initialize_systems(self):
        """Initialize community systems and infrastructure"""
        # Set up basic resource categories
        self.resource_pool.add_category("food", 1000.0)
        self.resource_pool.add_category("housing", 100.0)
        self.resource_pool.add_category("energy", 500.0)
        self.resource_pool.add_category("materials", 300.0)
        self.resource_pool.add_category("knowledge", 0.0)  # Unlimited
        
        # Initialize basic governance proposals
        self._create_initial_proposals()
    
    def _create_initial_proposals(self):
        """Create initial governance proposals for community setup"""
        initial_proposals = [
            {
                'id': 'resource_sharing_policy',
                'title': 'Resource Sharing Policy',
                'description': 'Establish guidelines for community resource sharing',
                'type': 'policy',
                'status': 'active',
                'votes': {},
                'created_date': datetime.now().isoformat()
            },
            {
                'id': 'contribution_recognition',
                'title': 'Contribution Recognition Framework',
                'description': 'Define how community contributions are recognized and valued',
                'type': 'framework',
                'status': 'active',
                'votes': {},
                'created_date': datetime.now().isoformat()
            }
        ]
        
        self.active_proposals.extend(initial_proposals)
    
    def add_member(self, agent: IndividualAgent) -> bool:
        """Add a new member to the community"""
        if len(self.members) >= self.max_population:
            return False
        
        if agent.agent_id in self.members:
            return False
        
        # Community compatibility check
        compatibility = self._assess_member_compatibility(agent)
        if compatibility < 0.3:  # Minimum compatibility threshold
            return False
        
        # Add member
        self.members[agent.agent_id] = agent
        agent.community_memberships.add(self.community_id)
        
        # Initialize member in community systems
        self.trust_network.add_member(agent.agent_id)
        self.contribution_algorithm.register_member(agent.agent_id)
        
        # Update community metrics
        self._update_community_metrics()
        
        return True
    
    def _assess_member_compatibility(self, agent: IndividualAgent) -> float:
        """Assess how well a potential member fits with community values"""
        compatibility = 0.5  # Base compatibility
        
        # Check value alignment with founding principles
        principle_alignment = 0.0
        for principle in self.founding_principles:
            if principle == "environmental_sustainability" and ValueSystem.ENVIRONMENTAL in agent.primary_values:
                principle_alignment += 0.2
            elif principle == "social_equity" and ValueSystem.SOCIAL_EQUITY in agent.primary_values:
                principle_alignment += 0.2
            elif principle == "community_cooperation" and ValueSystem.COMMUNITY in agent.primary_values:
                principle_alignment += 0.2
            elif principle == "innovation" and ValueSystem.INNOVATION in agent.primary_values:
                principle_alignment += 0.2
        
        compatibility += principle_alignment
        
        # Check personality fit
        if agent.cooperation_tendency > 0.6:
            compatibility += 0.1
        
        if agent.personality in [PersonalityType.COLLABORATOR, PersonalityType.CAREGIVER]:
            compatibility += 0.1
        
        return max(0.0, min(1.0, compatibility))
    
    def make_collective_decision(self, proposal_id: str) -> Dict:
        """Process a collective decision using the community's governance structure"""
        proposal = None
        for p in self.active_proposals:
            if p['id'] == proposal_id:
                proposal = p
                break
        
        if not proposal:
            return {'error': 'Proposal not found'}
        
        # Collect votes from all members
        votes = {}
        for member_id, member in self.members.items():
            vote = self._get_member_vote(member, proposal)
            votes[member_id] = vote
        
        proposal['votes'] = votes
        
        # Determine outcome based on governance structure
        if self.governance_structure == "consensus":
            decision = self._consensus_decision(votes)
        elif self.governance_structure == "majority":
            decision = self._majority_decision(votes)
        else:  # delegated
            decision = self._delegated_decision(votes, proposal)
        
        # Record decision
        decision_record = {
            'proposal_id': proposal_id,
            'decision': decision,
            'votes': votes,
            'governance_method': self.governance_structure,
            'timestamp': datetime.now().isoformat(),
            'participation_rate': len(votes) / len(self.members)
        }
        
        self.decision_history.append(decision_record)
        
        # Remove from active proposals
        self.active_proposals = [p for p in self.active_proposals if p['id'] != proposal_id]
        
        # Implement decision if approved
        if decision['approved']:
            self._implement_decision(proposal, decision)
        
        return decision_record
    
    def _get_member_vote(self, member: IndividualAgent, proposal: Dict) -> Dict:
        """Get a member's vote on a proposal"""
        # Simulate member decision-making process
        options = [
            {'choice': 'approve', 'personal_benefit': 0.6, 'community_impact': 0.8},
            {'choice': 'reject', 'personal_benefit': 0.4, 'community_impact': 0.3},
            {'choice': 'abstain', 'personal_benefit': 0.5, 'community_impact': 0.5}
        ]
        
        context = {
            'proposal': proposal,
            'community_size': len(self.members),
            'member_tenure': 30  # days, simplified
        }
        
        decision = member.make_decision(options, context)
        
        return {
            'choice': decision['choice'],
            'confidence': random.uniform(0.5, 1.0),
            'reasoning': f"Based on {member.personality.value} personality and values"
        }
    
    def _consensus_decision(self, votes: Dict) -> Dict:
        """Make decision using consensus (requires 80% approval)"""
        approve_count = sum(1 for vote in votes.values() if vote['choice'] == 'approve')
        total_votes = len(votes)
        approval_rate = approve_count / total_votes if total_votes > 0 else 0
        
        return {
            'approved': approval_rate >= 0.8,
            'approval_rate': approval_rate,
            'method': 'consensus'
        }
    
    def _majority_decision(self, votes: Dict) -> Dict:
        """Make decision using majority rule (requires >50% approval)"""
        approve_count = sum(1 for vote in votes.values() if vote['choice'] == 'approve')
        total_votes = len(votes)
        approval_rate = approve_count / total_votes if total_votes > 0 else 0
        
        return {
            'approved': approval_rate > 0.5,
            'approval_rate': approval_rate,
            'method': 'majority'
        }
    
    def _delegated_decision(self, votes: Dict, proposal: Dict) -> Dict:
        """Make decision using delegated authority"""
        # Simplified: use weighted voting based on expertise and trust
        weighted_approval = 0.0
        total_weight = 0.0
        
        for member_id, vote in votes.items():
            member = self.members[member_id]
            weight = member.contribution_score + member.trust_tokens / 100
            total_weight += weight
            
            if vote['choice'] == 'approve':
                weighted_approval += weight
        
        approval_rate = weighted_approval / total_weight if total_weight > 0 else 0
        
        return {
            'approved': approval_rate > 0.6,
            'approval_rate': approval_rate,
            'method': 'delegated'
        }
    
    def _implement_decision(self, proposal: Dict, decision: Dict):
        """Implement an approved decision"""
        if proposal['type'] == 'policy':
            # Update community policies
            pass
        elif proposal['type'] == 'project':
            # Start new project
            self._start_project(proposal)
        elif proposal['type'] == 'resource_allocation':
            # Allocate resources
            self._allocate_resources(proposal)
    
    def _start_project(self, proposal: Dict):
        """Start a new community project"""
        project = {
            'id': proposal['id'],
            'title': proposal['title'],
            'description': proposal['description'],
            'start_date': datetime.now().isoformat(),
            'status': 'active',
            'participants': [],
            'resources_allocated': {},
            'progress': 0.0
        }
        
        self.active_projects.append(project)
    
    def process_contributions(self, contributions: List[Dict]):
        """Process member contributions and update scores"""
        for contribution in contributions:
            # Update contribution algorithm
            score = self.contribution_algorithm.calculate_score(contribution)
            
            # Update member's contribution score
            member_id = contribution['agent_id']
            if member_id in self.members:
                self.members[member_id].contribution_score += score
                
                # Award trust tokens based on contribution
                trust_reward = score * 0.1
                self.members[member_id].trust_tokens += trust_reward
                
                # Update trust network
                self.trust_network.record_contribution(member_id, contribution)
        
        # Update community metrics
        self._update_community_metrics()
    
    def _update_community_metrics(self):
        """Update community-level metrics based on member states"""
        if not self.members:
            return
        
        # Calculate average wellbeing
        total_satisfaction = sum(member.satisfaction_level for member in self.members.values())
        total_stress = sum(member.stress_level for member in self.members.values())
        self.wellbeing_average = (total_satisfaction / len(self.members) + 
                                (1.0 - total_stress / len(self.members))) / 2
        
        # Calculate cohesion based on trust network
        avg_trust = self.trust_network.get_average_trust()
        self.cohesion_level = avg_trust
        
        # Calculate innovation index based on member activities
        innovation_activities = sum(1 for member in self.members.values() 
                                  if member.personality == PersonalityType.INNOVATOR)
        self.innovation_index = min(1.0, innovation_activities / len(self.members) * 2)
        
        # Sustainability score based on resource efficiency
        self.sustainability_score = self.resource_pool.get_efficiency_score()
    
    def daily_update(self):
        """Update community state at the end of each day"""
        # Update all member agents
        for member in self.members.values():
            member.daily_update()
        
        # Update community systems
        self.trust_network.daily_update()
        self.resource_pool.daily_update()
        
        # Update community metrics
        self._update_community_metrics()
        
        # Process any pending decisions
        self._process_pending_decisions()
    
    def _process_pending_decisions(self):
        """Process any decisions that are ready for voting"""
        # Simplified: auto-process proposals older than 7 days
        cutoff_date = datetime.now() - timedelta(days=7)
        
        ready_proposals = []
        for proposal in self.active_proposals:
            proposal_date = datetime.fromisoformat(proposal['created_date'])
            if proposal_date < cutoff_date:
                ready_proposals.append(proposal['id'])
        
        for proposal_id in ready_proposals:
            self.make_collective_decision(proposal_id)
    
    def get_status_summary(self) -> Dict:
        """Get comprehensive community status summary"""
        return {
            'community_id': self.community_id,
            'name': self.name,
            'location': self.location,
            'member_count': len(self.members),
            'max_population': self.max_population,
            'cohesion_level': round(self.cohesion_level, 3),
            'wellbeing_average': round(self.wellbeing_average, 3),
            'sustainability_score': round(self.sustainability_score, 3),
            'innovation_index': round(self.innovation_index, 3),
            'active_projects': len(self.active_projects),
            'active_proposals': len(self.active_proposals),
            'partner_communities': len(self.partner_communities),
            'governance_structure': self.governance_structure
        }

# Supporting classes for community systems

class ContributionAlgorithm:
    """Implements the LIFE System contribution recognition algorithm"""
    
    def __init__(self):
        self.members: Set[str] = set()
        self.contribution_history: List[Dict] = []
        self.category_weights = {
            'direct_impact': 0.3,
            'collaboration': 0.2,
            'innovation': 0.15,
            'regeneration': 0.15,
            'knowledge_sharing': 0.1,
            'community_building': 0.1
        }
    
    def register_member(self, member_id: str):
        """Register a new member in the contribution system"""
        self.members.add(member_id)
    
    def calculate_score(self, contribution: Dict) -> float:
        """Calculate contribution score using multi-dimensional algorithm"""
        base_value = contribution.get('base_value', 1.0)
        contribution_type = contribution.get('type', 'general')
        
        # Apply category-specific multipliers
        multiplier = 1.0
        if contribution_type == "environmental_restoration":
            multiplier = self.category_weights['regeneration'] * 2
        elif contribution_type == "innovation_project":
            multiplier = self.category_weights['innovation'] * 2
        elif contribution_type == "community_care":
            multiplier = self.category_weights['community_building'] * 2
        elif contribution_type == "education":
            multiplier = self.category_weights['knowledge_sharing'] * 2
        
        # Collaboration bonus
        if contribution.get('collaborators', 0) > 0:
            collaboration_bonus = min(0.5, contribution['collaborators'] * 0.1)
            multiplier += collaboration_bonus
        
        score = base_value * multiplier
        
        # Record contribution
        self.contribution_history.append({
            'member_id': contribution['agent_id'],
            'score': score,
            'timestamp': datetime.now().isoformat(),
            'type': contribution_type
        })
        
        return score

class TrustNetwork:
    """Manages trust relationships within the community"""
    
    def __init__(self):
        self.trust_matrix: Dict[str, Dict[str, float]] = {}
        self.trust_events: List[Dict] = []
    
    def add_member(self, member_id: str):
        """Add a new member to the trust network"""
        if member_id not in self.trust_matrix:
            self.trust_matrix[member_id] = {}
    
    def record_contribution(self, member_id: str, contribution: Dict):
        """Record a contribution and update trust scores"""
        # Increase trust from all community members
        for other_member in self.trust_matrix:
            if other_member != member_id:
                if member_id not in self.trust_matrix[other_member]:
                    self.trust_matrix[other_member][member_id] = 0.5
                
                trust_increase = min(0.02, contribution.get('base_value', 1.0) * 0.01)
                self.trust_matrix[other_member][member_id] += trust_increase
                self.trust_matrix[other_member][member_id] = min(1.0, 
                    self.trust_matrix[other_member][member_id])
    
    def get_trust_level(self, from_member: str, to_member: str) -> float:
        """Get trust level between two members"""
        if from_member in self.trust_matrix and to_member in self.trust_matrix[from_member]:
            return self.trust_matrix[from_member][to_member]
        return 0.5  # Default neutral trust
    
    def get_average_trust(self) -> float:
        """Get average trust level in the community"""
        if not self.trust_matrix:
            return 0.5
        
        total_trust = 0.0
        count = 0
        
        for from_member, trust_dict in self.trust_matrix.items():
            for to_member, trust_level in trust_dict.items():
                total_trust += trust_level
                count += 1
        
        return total_trust / count if count > 0 else 0.5
    
    def daily_update(self):
        """Daily trust network maintenance"""
        # Gradual trust decay for inactive relationships
        decay_rate = 0.001
        
        for from_member in self.trust_matrix:
            for to_member in self.trust_matrix[from_member]:
                current_trust = self.trust_matrix[from_member][to_member]
                # Decay towards neutral (0.5)
                if current_trust > 0.5:
                    self.trust_matrix[from_member][to_member] -= decay_rate
                elif current_trust < 0.5:
                    self.trust_matrix[from_member][to_member] += decay_rate

class ResourcePool:
    """Manages community resource allocation and circulation"""
    
    def __init__(self):
        self.resources: Dict[str, float] = {}
        self.allocation_history: List[Dict] = []
        self.circulation_velocity = 0.0
    
    def add_category(self, category: str, initial_amount: float):
        """Add a resource category"""
        self.resources[category] = initial_amount
    
    def allocate_resource(self, category: str, amount: float, 
                         recipient: str, purpose: str) -> bool:
        """Allocate resources to a member or project"""
        if category not in self.resources or self.resources[category] < amount:
            return False
        
        self.resources[category] -= amount
        
        allocation = {
            'category': category,
            'amount': amount,
            'recipient': recipient,
            'purpose': purpose,
            'timestamp': datetime.now().isoformat()
        }
        
        self.allocation_history.append(allocation)
        return True
    
    def add_resource(self, category: str, amount: float, source: str):
        """Add resources to the pool"""
        if category not in self.resources:
            self.resources[category] = 0.0
        
        self.resources[category] += amount
        
        # Record as negative allocation (resource addition)
        allocation = {
            'category': category,
            'amount': -amount,  # Negative indicates addition
            'recipient': 'community_pool',
            'purpose': f'contribution_from_{source}',
            'timestamp': datetime.now().isoformat()
        }
        
        self.allocation_history.append(allocation)
    
    def get_efficiency_score(self) -> float:
        """Calculate resource utilization efficiency"""
        if not self.allocation_history:
            return 0.5
        
        # Calculate circulation velocity (allocations per day)
        recent_allocations = [a for a in self.allocation_history 
                            if datetime.fromisoformat(a['timestamp']) > 
                            datetime.now() - timedelta(days=30)]
        
        self.circulation_velocity = len(recent_allocations) / 30
        
        # Efficiency based on circulation and waste minimization
        efficiency = min(1.0, self.circulation_velocity / 10)  # Normalize
        return efficiency
    
    def daily_update(self):
        """Daily resource pool maintenance"""
        # Simulate natural resource regeneration for renewable categories
        renewable_categories = ['energy', 'knowledge']
        
        for category in renewable_categories:
            if category in self.resources:
                if category == 'energy':
                    self.resources[category] += 10.0  # Daily energy generation
                elif category == 'knowledge':
                    self.resources[category] += 1.0   # Knowledge accumulation

if __name__ == "__main__":
    # Example usage and testing
    print("LIFE System Agent Models - Test Run")
    print("=" * 50)
    
    # Create test agents
    agent1 = IndividualAgent(
        agent_id="agent_001",
        age=35,
        education_level="university",
        cultural_background="western",
        personality=PersonalityType.COLLABORATOR,
        primary_values=[ValueSystem.ENVIRONMENTAL, ValueSystem.COMMUNITY]
    )
    
    agent2 = IndividualAgent(
        agent_id="agent_002",
        age=28,
        education_level="college",
        cultural_background="eastern",
        personality=PersonalityType.INNOVATOR,
        primary_values=[ValueSystem.INNOVATION, ValueSystem.SOCIAL_EQUITY]
    )
    
    # Create test community
    community = CommunityAgent(
        community_id="community_001",
        name="Green Valley Collective",
        location="California, USA",
        founding_principles=["environmental_sustainability", "social_equity", "community_cooperation"]
    )
    
    # Add agents to community
    print(f"Adding agent1 to community: {community.add_member(agent1)}")
    print(f"Adding agent2 to community: {community.add_member(agent2)}")
    
    # Test agent interaction
    interaction = agent1.interact_with_agent(agent2, "collaboration", {"project": "community_garden"})
    print(f"Agent interaction result: {interaction['successful']}")
    
    # Test contribution
    contribution = agent1.contribute_to_community(community, "environmental_restoration", 4.0)
    print(f"Contribution made: {contribution['base_value']:.2f} value")
    
    # Process contributions
    community.process_contributions([contribution])
    
    # Test decision making
    decision_result = community.make_collective_decision("resource_sharing_policy")
    print(f"Community decision: {decision_result['decision']['approved']}")
    
    # Print status summaries
    print("\nAgent 1 Status:")
    print(json.dumps(agent1.get_status_summary(), indent=2))
    
    print("\nCommunity Status:")
    print(json.dumps(community.get_status_summary(), indent=2))
    
    print("\nAgent models successfully implemented and tested!")

