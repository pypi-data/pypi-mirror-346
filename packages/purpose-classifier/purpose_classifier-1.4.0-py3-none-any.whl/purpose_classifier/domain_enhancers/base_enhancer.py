"""
Base Enhancer for Purpose Code Classification.

This module provides a base class for all purpose code enhancers,
defining the interface and common functionality.
"""

import os
import logging
from purpose_classifier.semantic_pattern_matcher import SemanticPatternMatcher

logger = logging.getLogger(__name__)

class BaseEnhancer:
    """
    Base class for all domain-specific enhancers.
    
    Provides common functionality for enhancing purpose code classification
    based on domain-specific rules and patterns.
    """

    def __init__(self, matcher=None):
        """
        Initialize the base enhancer.

        Args:
            matcher: Optional SemanticPatternMatcher instance to use
        """
        if matcher:
            # Use the provided matcher
            self.matcher = matcher
            logger.info(f"Using provided matcher for {self.__class__.__name__}")
        else:
            # Get the absolute path to the word embeddings file
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            embeddings_path = os.path.join(base_dir, 'models', 'word_embeddings.pkl')

            # Initialize semantic pattern matcher with explicit embeddings path
            try:
                self.matcher = SemanticPatternMatcher(embeddings_path)
                
                # Log whether embeddings were loaded
                if hasattr(self.matcher, 'embeddings') and self.matcher.embeddings:
                    logger.info(f"Word embeddings loaded successfully for {self.__class__.__name__}")
                else:
                    logger.warning(f"Word embeddings not loaded for {self.__class__.__name__}")
            except Exception as e:
                logger.warning(f"Failed to load matcher for {self.__class__.__name__}: {str(e)}")
                self.matcher = None

        # Initialize common attributes
        self.context_patterns = []
        self.confidence_thresholds = {
            'high': 0.95,
            'medium': 0.80,
            'low': 0.60
        }

    def enhance_classification(self, result, narration, message_type=None):
        """
        Enhance classification based on domain-specific rules.
        
        Args:
            result: The classification result to enhance
            narration: The narration text
            message_type: Optional message type (MT103, MT202, MT202COV, MT205, MT205COV)
            
        Returns:
            dict: The enhanced classification result
        """
        # Base implementation returns the original result
        # Subclasses should override this method
        return result

    def _create_enhanced_result(self, original_result, purpose_code, confidence, reason):
        """
        Create an enhanced result based on the original result.
        
        Args:
            original_result: The original classification result
            purpose_code: The new purpose code
            confidence: The confidence score
            reason: The reason for the enhancement
            
        Returns:
            dict: The enhanced classification result
        """
        enhanced_result = original_result.copy()
        enhanced_result['purpose_code'] = purpose_code
        enhanced_result['original_purpose_code'] = original_result.get('purpose_code', 'OTHR')
        enhanced_result['original_confidence'] = original_result.get('confidence', 0.0)
        enhanced_result['confidence'] = confidence
        enhanced_result['enhancer'] = self.__class__.__name__
        enhanced_result['enhancement_applied'] = reason
        enhanced_result['enhanced'] = True
        
        return enhanced_result

    def should_override_classification(self, result, narration):
        """
        Determine if the enhancer should override the current classification.
        
        Args:
            result: The current classification result
            narration: The narration text
            
        Returns:
            bool: True if the enhancer should override the classification
        """
        # Base implementation returns False
        # Subclasses should override this method
        return False 