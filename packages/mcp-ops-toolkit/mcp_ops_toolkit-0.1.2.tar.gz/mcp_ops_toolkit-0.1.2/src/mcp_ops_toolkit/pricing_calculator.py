import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple

class PricingCalculator:
    """Pricing calculator that uses external pricing rules"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize pricing calculator
        
        Args:
            config_path: Optional path to pricing rules JSON file.
                        If not provided, will look for 'config/pricing_rules.json' under FILE_PATH
        """
        # Get FILE_PATH from environment variable, if not set, use user's home directory as default
        self.file_path = os.getenv("FILE_PATH", os.path.expanduser("~"))
        self.config_path = config_path or str(Path(self.file_path) / 'config' / 'pricing_rules.json')
        self.pricing_rules = self._load_pricing_rules()
        
    def _load_pricing_rules(self) -> Dict:
        """Load pricing rules from JSON configuration file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(
                f"Pricing rules file not found at {self.config_path}. "
                f"Please ensure the file exists or set correct FILE_PATH environment variable."
            )
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in pricing rules file: {self.config_path}")
        except Exception as e:
            raise ValueError(f"Failed to load pricing rules: {str(e)}")
            
    def _get_pricing_tiers(self) -> List[Dict[str, Union[int, float, None, str]]]:
        """Get pricing tiers from loaded configuration"""
        return self.pricing_rules['concurrent_pricing']['tiers']
        
    def calculate_cost(self, concurrent_docs: int) -> Tuple[float, List[Dict[str, Union[int, float, str]]]]:
        """
        Calculate cost based on concurrent documents count
        
        Args:
            concurrent_docs: Number of concurrent documents
            
        Returns:
            Tuple containing:
                - float: Total cost
                - List[Dict]: Calculation details for each pricing tier
                
        Raises:
            ValueError: If concurrent_docs is negative
        """
        if concurrent_docs < 0:
            raise ValueError("Concurrent documents count cannot be negative")
            
        tiers = self._get_pricing_tiers()
        cost = 0
        calculation_details = []
        remaining_docs = concurrent_docs
        prev_max = 0
        
        for tier in tiers:
            max_concurrent = tier['max_concurrent']
            price_per_unit = tier['price_per_unit']
            
            # Handle last tier (no upper limit)
            if max_concurrent is None:
                if remaining_docs > 0:
                    tier_cost = remaining_docs * price_per_unit
                    calculation_details.append({
                        'tier': tier['description'],
                        'docs_in_tier': remaining_docs,
                        'price_per_unit': price_per_unit,
                        'tier_cost': tier_cost
                    })
                    cost += tier_cost
                break
                
            # Calculate docs in current tier
            docs_in_tier = min(
                remaining_docs,
                max_concurrent - prev_max
            )
            
            if docs_in_tier > 0:
                tier_cost = docs_in_tier * price_per_unit
                calculation_details.append({
                    'tier': tier['description'],
                    'docs_in_tier': docs_in_tier,
                    'price_per_unit': price_per_unit,
                    'tier_cost': tier_cost
                })
                cost += tier_cost
                remaining_docs -= docs_in_tier
                
            if remaining_docs <= 0:
                break
                
            prev_max = max_concurrent
            
        return cost, calculation_details
