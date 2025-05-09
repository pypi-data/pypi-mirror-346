"""
Semantic Charitable Donation Enhancer for Purpose Code Classification.

This module provides a specialized enhancer for charitable donation transactions,
using semantic pattern matching to identify donation-related transactions with high accuracy.
"""

import logging
from purpose_classifier.domain_enhancers.semantic_enhancer import SemanticEnhancer

logger = logging.getLogger(__name__)

class CharitableDonationEnhancerSemantic(SemanticEnhancer):
    """
    Specialized enhancer for charitable donation transactions.

    Uses semantic pattern matching to identify donation-related transactions
    with high accuracy and confidence.
    """

    def __init__(self, matcher=None):
        """
        Initialize with optional matcher.

        Args:
            matcher: Optional SemanticPatternMatcher instance to use
        """
        super().__init__(matcher=matcher)

        # Initialize donation-specific patterns and contexts
        self._initialize_patterns()

    def _initialize_patterns(self):
        """Initialize donation-specific patterns and contexts."""
        # Direct donation keywords (highest confidence)
        self.donation_keywords = [
            'donation', 'donate', 'donating', 'charitable', 'charity', 'charities',
            'charitable donation', 'charitable contribution', 'charity donation',
            'nonprofit', 'non-profit', 'non profit', 'foundation', 'fundraiser',
            'fundraising', 'relief fund', 'disaster relief', 'humanitarian',
            'humanitarian aid', 'philanthropy', 'philanthropic', 'benevolent',
            'benevolence', 'giving', 'charitable giving', 'charitable organization',
            'nonprofit organization', 'non-profit organization', 'ngo', 'red cross',
            'unicef', 'salvation army', 'doctors without borders', 'oxfam',
            'care international', 'world vision', 'save the children', 'amnesty international',
            # Additional charity organizations
            'cancer research', 'american cancer society', 'american heart association',
            'american red cross', 'habitat for humanity', 'make a wish', 'st jude',
            'saint jude', 'childrens hospital', "children's hospital", 'wounded warrior',
            'special olympics', 'feeding america', 'food bank', 'homeless shelter',
            'animal shelter', 'humane society', 'aspca', 'peta', 'wwf', 'greenpeace',
            'nature conservancy', 'sierra club', 'aclu', 'planned parenthood',
            'boys and girls club', 'girl scouts', 'boy scouts', 'united way',
            'goodwill', 'salvation army', 'catholic charities', 'jewish federation',
            'islamic relief', 'lutheran services', 'methodist relief', 'baptist relief',
            'episcopal relief', 'presbyterian relief', 'mormon relief', 'quaker relief',
            'buddhist relief', 'hindu relief', 'sikh relief', 'interfaith relief',
            # Additional donation terms
            'donation to', 'donate to', 'donating to', 'charitable gift', 'charity gift',
            'gift to charity', 'gift to foundation', 'donation for', 'donate for',
            'donating for', 'charitable fund', 'charity fund', 'relief donation',
            'disaster donation', 'humanitarian donation', 'philanthropic donation',
            'benevolent donation', 'giving to', 'charitable giving to', 'charity giving',
            'nonprofit donation', 'non-profit donation', 'ngo donation', 'foundation donation'
        ]

        # Map keywords to purpose codes
        self.direct_keywords = {
            'DONR': self.donation_keywords
        }

        # Semantic context patterns for donations
        self.context_patterns = [
            # Basic donation patterns
            {"purpose_code": "DONR", "keywords": ["charitable", "donation"], "proximity": 5, "weight": 1.0},
            {"purpose_code": "DONR", "keywords": ["charity", "donation"], "proximity": 5, "weight": 1.0},
            {"purpose_code": "DONR", "keywords": ["charitable", "contribution"], "proximity": 5, "weight": 1.0},
            {"purpose_code": "DONR", "keywords": ["charity", "contribution"], "proximity": 5, "weight": 1.0},
            {"purpose_code": "DONR", "keywords": ["nonprofit", "donation"], "proximity": 5, "weight": 1.0},
            {"purpose_code": "DONR", "keywords": ["non-profit", "donation"], "proximity": 5, "weight": 1.0},
            {"purpose_code": "DONR", "keywords": ["non", "profit", "donation"], "proximity": 5, "weight": 1.0},
            {"purpose_code": "DONR", "keywords": ["foundation", "donation"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["relief", "fund"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["disaster", "relief"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["humanitarian", "aid"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["charitable", "giving"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["charitable", "organization"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["nonprofit", "organization"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["non-profit", "organization"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["non", "profit", "organization"], "proximity": 5, "weight": 0.9},

            # Charity organization patterns
            {"purpose_code": "DONR", "keywords": ["red", "cross"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["salvation", "army"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["doctors", "without", "borders"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["save", "children"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["amnesty", "international"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["cancer", "research"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["heart", "association"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["habitat", "humanity"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["make", "wish"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["st", "jude"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["saint", "jude"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["children", "hospital"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["wounded", "warrior"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["special", "olympics"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["feeding", "america"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["food", "bank"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["homeless", "shelter"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["animal", "shelter"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["humane", "society"], "proximity": 5, "weight": 0.9},

            # Donation reference patterns
            {"purpose_code": "DONR", "keywords": ["donation", "ref"], "proximity": 5, "weight": 0.8},
            {"purpose_code": "DONR", "keywords": ["donation", "reference"], "proximity": 5, "weight": 0.8},
            {"purpose_code": "DONR", "keywords": ["donation", "id"], "proximity": 5, "weight": 0.8},
            {"purpose_code": "DONR", "keywords": ["donation", "number"], "proximity": 5, "weight": 0.8},
            {"purpose_code": "DONR", "keywords": ["donation", "receipt"], "proximity": 5, "weight": 0.8},
            {"purpose_code": "DONR", "keywords": ["donation", "tax"], "proximity": 5, "weight": 0.8},
            {"purpose_code": "DONR", "keywords": ["donation", "deductible"], "proximity": 5, "weight": 0.8},
            {"purpose_code": "DONR", "keywords": ["tax", "deductible", "donation"], "proximity": 5, "weight": 0.9},

            # Donation to/for patterns
            {"purpose_code": "DONR", "keywords": ["donation", "to", "charity"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "to", "foundation"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "charity"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "relief"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "disaster"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "humanitarian"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "children"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "hospital"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "research"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "cancer"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "heart"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "homeless"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "animal"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "environment"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "education"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "school"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "university"], "proximity": 5, "weight": 0.9},
            {"purpose_code": "DONR", "keywords": ["donation", "for", "college"], "proximity": 5, "weight": 0.9},

            # Specific donation patterns
            {"purpose_code": "DONR", "keywords": ["charitable", "donation", "for"], "proximity": 5, "weight": 1.0},
            {"purpose_code": "DONR", "keywords": ["charity", "donation", "for"], "proximity": 5, "weight": 1.0},
            {"purpose_code": "DONR", "keywords": ["donation", "to", "charity", "foundation"], "proximity": 5, "weight": 1.0},
            {"purpose_code": "DONR", "keywords": ["donation", "to", "relief", "fund"], "proximity": 5, "weight": 1.0},
            {"purpose_code": "DONR", "keywords": ["donation", "to", "disaster", "relief"], "proximity": 5, "weight": 1.0},
            {"purpose_code": "DONR", "keywords": ["donation", "to", "humanitarian", "aid"], "proximity": 5, "weight": 1.0}
        ]

        # Donation-related terms for semantic similarity matching
        self.semantic_terms = [
            # Basic donation terms
            {"term": "donation", "purpose_code": "DONR", "threshold": 0.7, "weight": 1.0},
            {"term": "donate", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "donating", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "charitable", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "charity", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "nonprofit", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.8},
            {"term": "foundation", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.8},
            {"term": "relief", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.8},
            {"term": "humanitarian", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.8},
            {"term": "philanthropy", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.8},
            {"term": "giving", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.7},
            {"term": "benevolent", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.7},
            {"term": "fundraiser", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.7},
            {"term": "fundraising", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.7},

            # Charity organization terms
            {"term": "red cross", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "salvation army", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "doctors without borders", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "unicef", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "oxfam", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "care international", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "world vision", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "save the children", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "amnesty international", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "cancer research", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "heart association", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "habitat for humanity", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "make a wish", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "st jude", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},
            {"term": "children hospital", "purpose_code": "DONR", "threshold": 0.7, "weight": 0.9},

            # Donation phrases
            {"term": "donation to charity", "purpose_code": "DONR", "threshold": 0.7, "weight": 1.0},
            {"term": "donation to foundation", "purpose_code": "DONR", "threshold": 0.7, "weight": 1.0},
            {"term": "donation for relief", "purpose_code": "DONR", "threshold": 0.7, "weight": 1.0},
            {"term": "donation for disaster", "purpose_code": "DONR", "threshold": 0.7, "weight": 1.0},
            {"term": "charitable donation for", "purpose_code": "DONR", "threshold": 0.7, "weight": 1.0},
            {"term": "charity donation for", "purpose_code": "DONR", "threshold": 0.7, "weight": 1.0},
            {"term": "donation to relief fund", "purpose_code": "DONR", "threshold": 0.7, "weight": 1.0},
            {"term": "donation to disaster relief", "purpose_code": "DONR", "threshold": 0.7, "weight": 1.0},
            {"term": "donation to humanitarian aid", "purpose_code": "DONR", "threshold": 0.7, "weight": 1.0}
        ]

        # Negative indicators (patterns that suggest it's NOT a donation)
        self.negative_indicators = [
            'not donation', 'non-donation', 'excluding donation',
            'donation free', 'no donation', 'without donation',
            'donation tax', 'tax on donation',  # These are tax payments, not donations
            'donation refund', 'refund of donation', 'donation return',
            'donation cancellation', 'cancel donation', 'cancelled donation',
            'donation reversal', 'reverse donation', 'reversed donation',
            'donation chargeback', 'chargeback of donation', 'donation dispute',
            'disputed donation', 'donation error', 'erroneous donation',
            'donation correction', 'corrected donation', 'donation adjustment',
            'adjusted donation', 'donation fee', 'fee for donation',
            'donation processing fee', 'donation service fee', 'donation platform fee'
        ]

    def enhance_classification(self, result, narration, message_type=None):
        """
        Enhance classification for charitable donation transactions.

        Args:
            result: Initial classification result
            narration: Transaction narration
            message_type: Optional message type

        Returns:
            dict: Enhanced classification result
        """
        logger.info(f"DONATION DEBUG: Charitable donation enhancer called with narration: {narration}")

        # Get current purpose code and confidence
        purpose_code = result.get('purpose_code', 'OTHR')
        confidence = result.get('confidence', 0.0)

        # Don't override if already classified as DONR with high confidence
        if purpose_code == 'DONR' and confidence >= 0.8:
            logger.debug(f"Already classified as DONR with high confidence: {confidence}")
            return result

        # Check for negative indicators
        narration_lower = narration.lower()
        for indicator in self.negative_indicators:
            if indicator in narration_lower:
                logger.debug(f"Negative indicator for DONR found: {indicator}")
                if purpose_code == 'DONR':
                    # If current purpose code matches the negative indicator, reduce confidence
                    result['confidence'] = max(0.3, confidence * 0.7)
                    result['reason'] = f"Negative indicator found: {indicator}"
                    return result

        # Direct keyword matching (high confidence)
        matched, keyword_confidence, keyword = self.direct_keyword_match(narration, 'DONR')
        if matched:
            logger.info(f"DONR keyword match: {keyword} with confidence {keyword_confidence}")
            return self._create_enhanced_result(result, 'DONR', keyword_confidence, f"Direct DONR keyword match: {keyword}")

        # Semantic context pattern matching
        donation_context_score = self.context_match(narration, self.context_patterns)
        if donation_context_score >= 0.7:
            logger.info(f"Donation context match with score: {donation_context_score:.2f}")
            return self._create_enhanced_result(result, 'DONR', min(0.95, donation_context_score),
                                              f"Donation context match with score: {donation_context_score:.2f}")

        # Semantic similarity matching with 3-word rule
        matched, sem_confidence, sem_purpose_code, sem_matches = self.semantic_similarity_match(narration, self.semantic_terms)
        if matched and sem_purpose_code == 'DONR':
            # Apply 3-word rule for semantic matching
            if len(sem_matches) >= 3:
                logger.info(f"DONR semantic match with confidence: {sem_confidence:.2f} (3+ word rule enforced)")
                return self._create_enhanced_result(result, 'DONR', sem_confidence,
                                                f"Semantic similarity matches: {len(sem_matches)} terms (3+ word rule enforced)")
            else:
                logger.debug(f"DONR semantic match with only {len(sem_matches)} terms (less than 3-word rule)")
                # If less than 3 words match but confidence is high, still consider it but with reduced confidence
                if sem_confidence >= 0.8:
                    reduced_confidence = sem_confidence * 0.8  # Reduce confidence by 20%
                    logger.info(f"DONR semantic match with reduced confidence: {reduced_confidence:.2f} (less than 3-word rule)")
                    return self._create_enhanced_result(result, 'DONR', reduced_confidence,
                                                    f"Semantic similarity matches: {len(sem_matches)} terms (less than 3-word rule)")
                else:
                    logger.debug(f"Insufficient semantic match confidence: {sem_confidence:.2f}")
                    return result

        # No donation pattern detected
        logger.debug("No donation pattern detected")
        return result

    def _create_enhanced_result(self, original_result, purpose_code, confidence, reason):
        """
        Create an enhanced result dictionary.

        Args:
            original_result: Original classification result
            purpose_code: Enhanced purpose code
            confidence: Enhanced confidence
            reason: Reason for enhancement

        Returns:
            dict: Enhanced classification result
        """
        # Create a copy of the original result
        result = original_result.copy()

        # Update with enhanced values
        result['purpose_code'] = purpose_code
        result['confidence'] = confidence

        # Set category purpose code based on purpose code
        result['category_purpose_code'] = 'CHAR'  # Charitable donations map to Charity Payment (CHAR)
        result['category_confidence'] = confidence
        result['category_enhancement_applied'] = "charitable_donation_category_mapping"

        # Add enhancement metadata
        result['enhanced'] = True
        result['enhancer'] = 'charitable_donation'
        result['reason'] = reason
        result['original_purpose_code'] = original_result.get('purpose_code')
        result['original_confidence'] = original_result.get('confidence')

        # Set force flags to prevent other enhancers from overriding
        if confidence >= 0.9:
            result['force_purpose_code'] = True
            result['force_category_purpose_code'] = True

        return result
