#!/usr/bin/env python3
"""
Rent Enhancer for Purpose Code Classifier

This enhancer specifically handles rent-related narrations to ensure they are
correctly classified as RENT with the category purpose code SUPP.
"""

import re
import logging
from collections import defaultdict

from purpose_classifier.domain_enhancers.base_enhancer import BaseEnhancer

# Configure logger
logger = logging.getLogger(__name__)

class RentEnhancer(BaseEnhancer):
    """
    Enhancer for rent-related narrations.
    Ensures rent payments are correctly classified as RENT with category purpose code SUPP.
    """

    def __init__(self, matcher=None):
        """
        Initialize with optional matcher.
        
        Args:
            matcher: Optional SemanticPatternMatcher instance to use
        """
        super().__init__(matcher=matcher)
        
        # Define rent-related keywords
        self.rent_keywords = [
            'rent', 'rental', 'lease', 'apartment', 'housing', 'accommodation',
            'tenant', 'landlord', 'property', 'monthly payment', 'quarterly payment',
            'residential', 'commercial', 'office space', 'living space'
        ]
        
        # Define rent-related patterns
        self.rent_patterns = [
            r'\b(rent|rental|lease)\b.*?\b(payment|fee|invoice|bill)\b',
            r'\b(payment|fee|invoice|bill)\b.*?\b(rent|rental|lease)\b',
            r'\b(pay(ing|ment)?|transfer(ing)?)\b.*?\b(for|to)\b.*?\b(rent|rental|lease)\b',
            r'\b(apartment|housing|accommodation)\b.*?\b(payment|fee|rent)\b',
            r'\b(payment|fee|rent)\b.*?\b(apartment|housing|accommodation)\b',
            r'\b(monthly|quarterly)\b.*?\b(rent|rental|lease)\b',
            r'\b(rent|rental|lease)\b.*?\b(monthly|quarterly)\b',
            r'\b(tenant|landlord)\b.*?\b(payment|fee|rent)\b',
            r'\b(payment|fee|rent)\b.*?\b(tenant|landlord)\b',
            r'\b(residential|commercial|office)\b.*?\b(rent|rental|lease)\b',
            r'\b(rent|rental|lease)\b.*?\b(residential|commercial|office)\b'
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.rent_patterns]
        
        # Define negative indicators (terms that suggest it's NOT rent-related)
        self.negative_indicators = [
            'salary', 'payroll', 'wage', 'bonus', 'commission',
            'dividend', 'interest', 'loan', 'mortgage', 'purchase',
            'buying', 'acquisition', 'investment', 'securities'
        ]
        
        # Initialize context patterns
        self.context_patterns = [
            {'purpose_code': 'RENT', 'keywords': ['rent', 'payment'], 'proximity': 5, 'weight': 0.9},
            {'purpose_code': 'RENT', 'keywords': ['rental', 'fee'], 'proximity': 5, 'weight': 0.9},
            {'purpose_code': 'RENT', 'keywords': ['lease', 'payment'], 'proximity': 5, 'weight': 0.9},
            {'purpose_code': 'RENT', 'keywords': ['apartment', 'rent'], 'proximity': 5, 'weight': 0.9},
            {'purpose_code': 'RENT', 'keywords': ['monthly', 'rent'], 'proximity': 5, 'weight': 0.9},
            {'purpose_code': 'RENT', 'keywords': ['tenant', 'payment'], 'proximity': 5, 'weight': 0.9},
            {'purpose_code': 'RENT', 'keywords': ['landlord', 'payment'], 'proximity': 5, 'weight': 0.9},
            {'purpose_code': 'RENT', 'keywords': ['property', 'rent'], 'proximity': 5, 'weight': 0.9},
            {'purpose_code': 'RENT', 'keywords': ['office', 'rent'], 'proximity': 5, 'weight': 0.9},
            {'purpose_code': 'RENT', 'keywords': ['residential', 'rent'], 'proximity': 5, 'weight': 0.9},
            {'purpose_code': 'RENT', 'keywords': ['commercial', 'rent'], 'proximity': 5, 'weight': 0.9}
        ]

    def enhance_classification(self, result, narration, message_type=None):
        """
        Enhance classification for rent-related transactions.

        Args:
            result: Initial classification result
            narration: Transaction narration
            message_type: Optional message type

        Returns:
            dict: Enhanced classification result
        """
        logger.debug(f"Rent enhancer called with narration: {narration}")

        # Get current purpose code and confidence
        purpose_code = result.get('purpose_code', 'OTHR')
        confidence = result.get('confidence', 0.0)

        # Don't override high confidence classifications (except SALA which might be misclassified)
        if confidence >= 0.95 and purpose_code != 'SALA':
            logger.debug(f"Not overriding high confidence classification: {purpose_code} ({confidence})")
            return result

        narration_lower = narration.lower()

        # Check for negative indicators
        for indicator in self.negative_indicators:
            if indicator.lower() in narration_lower:
                logger.debug(f"Negative indicator found: {indicator}")
                # This is clearly not rent-related
                return result

        # Check for exact rent-related patterns
        pattern_match = any(pattern.search(narration_lower) for pattern in self.compiled_patterns)
        
        if pattern_match:
            logger.info(f"Rent pattern matched in narration: {narration}")
            enhanced_result = self._create_enhanced_result(result, 'RENT', 0.95, "rent_pattern_match")
            
            # Ensure category purpose code is set to SUPP for rent payments
            enhanced_result['category_purpose_code'] = "SUPP"
            enhanced_result['category_confidence'] = 0.95
            enhanced_result['category_enhancement_applied'] = "rent_category_mapping"
            
            return enhanced_result

        # Check for semantic similarity to rent terms
        if hasattr(self, 'matcher') and self.matcher:
            # Calculate semantic similarity to rent terms
            semantic_score = 0.0
            best_term = None
            
            for term in self.rent_keywords:
                score = self.matcher.get_similarity(term, narration_lower)
                if score > semantic_score:
                    semantic_score = score
                    best_term = term
            
            # If semantic score is high enough, consider it a match
            if semantic_score >= 0.65:
                logger.info(f"Rent semantic match ({best_term}, {semantic_score:.2f}) in narration: {narration}")
                enhanced_result = self._create_enhanced_result(result, 'RENT', 0.85, f"rent_semantic_match:{best_term}")
                
                # Ensure category purpose code is set to SUPP for rent payments
                enhanced_result['category_purpose_code'] = "SUPP"
                enhanced_result['category_confidence'] = 0.85
                enhanced_result['category_enhancement_applied'] = "rent_category_mapping"
                
                return enhanced_result

        # No rent pattern detected
        logger.debug("No rent pattern detected")
        return result

    def should_override_classification(self, result, narration):
        """
        Determine if rent classification should override existing classification.

        Args:
            result: Current classification result
            narration: Transaction narration

        Returns:
            bool: True if should override
        """
        narration_lower = narration.lower()
        purpose_code = result.get('purpose_code', 'OTHR')
        confidence = result.get('confidence', 0.0)
        
        # Always override SALA classifications that mention rent
        if purpose_code == 'SALA' and any(term in narration_lower for term in ['rent', 'rental', 'lease']):
            return True
        
        # Don't override high confidence classifications
        if confidence >= 0.85 and purpose_code != 'SALA':
            return False
        
        # Check for strong rent indicators
        strong_indicators = [
            'rent payment', 'rental payment', 'lease payment',
            'apartment rent', 'housing rent', 'office rent',
            'monthly rent', 'quarterly rent'
        ]
        
        if any(indicator in narration_lower for indicator in strong_indicators):
            return True
        
        return False
