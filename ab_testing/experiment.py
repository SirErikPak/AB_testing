"""
Experiment module for A/B testing.

This module provides classes and functions for managing A/B test experiments.
"""

import random
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Variant:
    """Represents a variant in an A/B test.
    
    Attributes:
        name: Name of the variant (e.g., 'control', 'treatment')
        weight: Weight for random assignment (higher weight = higher probability)
        conversions: Number of successful conversions
        exposures: Number of total exposures (users shown this variant)
        metadata: Optional metadata for the variant
    """
    name: str
    weight: float = 1.0
    conversions: int = 0
    exposures: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def conversion_rate(self) -> float:
        """Calculate the conversion rate for this variant."""
        if self.exposures == 0:
            return 0.0
        return self.conversions / self.exposures
    
    def record_exposure(self) -> None:
        """Record an exposure for this variant."""
        self.exposures += 1
    
    def record_conversion(self) -> None:
        """Record a conversion for this variant."""
        self.conversions += 1


class Experiment:
    """Main class for managing A/B test experiments.
    
    This class handles variant assignment, data collection, and basic analysis.
    
    Attributes:
        name: Name of the experiment
        variants: List of variants in the experiment
        seed: Random seed for reproducible variant assignment
    """
    
    def __init__(self, name: str, variants: List[Variant], seed: Optional[int] = None):
        """Initialize an experiment.
        
        Args:
            name: Name of the experiment
            variants: List of Variant objects
            seed: Optional random seed for reproducibility
        
        Raises:
            ValueError: If less than 2 variants are provided
        """
        if len(variants) < 2:
            raise ValueError("Experiment must have at least 2 variants")
        
        self.name = name
        self.variants = variants
        self.created_at = datetime.now()
        self._random = random.Random(seed)
        
        # Normalize weights
        total_weight = sum(v.weight for v in self.variants)
        if total_weight <= 0:
            raise ValueError("Total weight must be positive")
        
        for variant in self.variants:
            variant.weight = variant.weight / total_weight
    
    def assign_variant(self, user_id: Optional[str] = None) -> Variant:
        """Assign a variant to a user.
        
        Args:
            user_id: Optional user ID for deterministic assignment
        
        Returns:
            The assigned Variant object
        """
        if user_id is not None:
            # Deterministic assignment based on user_id
            hash_val = hash(user_id + self.name)
            rand_val = (hash_val % 10000) / 10000
        else:
            # Random assignment
            rand_val = self._random.random()
        
        cumulative_weight = 0.0
        for variant in self.variants:
            cumulative_weight += variant.weight
            if rand_val <= cumulative_weight:
                variant.record_exposure()
                return variant
        
        # Fallback (shouldn't reach here with proper weights)
        variant = self.variants[-1]
        variant.record_exposure()
        return variant
    
    def record_conversion(self, variant_name: str) -> bool:
        """Record a conversion for a specific variant.
        
        Args:
            variant_name: Name of the variant to record conversion for
        
        Returns:
            True if conversion was recorded, False if variant not found
        """
        for variant in self.variants:
            if variant.name == variant_name:
                variant.record_conversion()
                return True
        return False
    
    def get_variant(self, variant_name: str) -> Optional[Variant]:
        """Get a variant by name.
        
        Args:
            variant_name: Name of the variant
        
        Returns:
            The Variant object or None if not found
        """
        for variant in self.variants:
            if variant.name == variant_name:
                return variant
        return None
    
    def get_results(self) -> Dict[str, Dict[str, Any]]:
        """Get the current results of the experiment.
        
        Returns:
            Dictionary mapping variant names to their statistics
        """
        results = {}
        for variant in self.variants:
            results[variant.name] = {
                'exposures': variant.exposures,
                'conversions': variant.conversions,
                'conversion_rate': variant.conversion_rate,
                'weight': variant.weight,
            }
        return results
    
    def get_summary(self) -> str:
        """Get a human-readable summary of the experiment.
        
        Returns:
            String summary of the experiment
        """
        summary = [f"Experiment: {self.name}"]
        summary.append(f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        summary.append(f"Variants: {len(self.variants)}")
        summary.append("")
        
        for variant in self.variants:
            summary.append(f"  {variant.name}:")
            summary.append(f"    Exposures: {variant.exposures}")
            summary.append(f"    Conversions: {variant.conversions}")
            summary.append(f"    Conversion Rate: {variant.conversion_rate:.2%}")
            summary.append("")
        
        return "\n".join(summary)
