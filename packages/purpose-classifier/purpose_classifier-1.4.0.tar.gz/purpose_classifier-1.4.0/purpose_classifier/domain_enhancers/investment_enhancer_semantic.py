"""
Semantic Investment Enhancer for Purpose Code Classification.

This module provides a specialized enhancer for investment-related transactions,
using semantic pattern matching to identify investment-related transactions with high accuracy.
"""

import logging
import re
import itertools
from purpose_classifier.domain_enhancers.semantic_enhancer import SemanticEnhancer

logger = logging.getLogger(__name__)

class InvestmentEnhancerSemantic(SemanticEnhancer):
    """
    Specialized enhancer for investment-related transactions.

    Uses semantic pattern matching to identify investment-related transactions
    with high accuracy and confidence.
    """

    def __init__(self, matcher=None):
        """
        Initialize with optional matcher.

        Args:
            matcher: Optional SemanticPatternMatcher instance to use
        """
        super().__init__(matcher=matcher)

        # Initialize investment-specific patterns and contexts
        self._initialize_patterns()

    def _initialize_patterns(self):
        """Initialize investment-specific patterns and contexts."""
        # Direct investment keywords (highest confidence)
        self.investment_keywords = [
            'investment', 'investing', 'invest', 'investment account', 'investment portfolio',
            'investment management', 'asset management', 'portfolio management',
            'wealth management', 'investment fund', 'mutual fund', 'etf',
            'exchange traded fund', 'retirement account', 'ira', '401k', 'pension',
            'stock purchase', 'bond purchase', 'share purchase', 'equity purchase',
            'securities purchase', 'investment deposit', 'investment contribution'
        ]

        # Direct securities keywords (highest confidence)
        self.securities_keywords = [
            'securities', 'security', 'stock', 'stocks', 'share', 'shares',
            'equity', 'equities', 'bond', 'bonds', 'treasury bond', 'corporate bond',
            'government bond', 'municipal bond', 'debenture', 'note', 'treasury note',
            'brokerage', 'broker', 'trading account', 'securities account',
            'securities trading', 'securities transaction', 'securities settlement'
        ]

        # Map keywords to purpose codes
        self.direct_keywords = {
            'INVS': self.investment_keywords,
            'SECU': self.securities_keywords
        }

        # Semantic context patterns for investments
        self.investment_contexts = [
            {"keywords": ["investment", "account"], "proximity": 5, "weight": 1.0},
            {"keywords": ["investment", "portfolio"], "proximity": 5, "weight": 1.0},
            {"keywords": ["investment", "management"], "proximity": 5, "weight": 0.9},
            {"keywords": ["asset", "management"], "proximity": 5, "weight": 0.9},
            {"keywords": ["portfolio", "management"], "proximity": 5, "weight": 0.9},
            {"keywords": ["wealth", "management"], "proximity": 5, "weight": 0.9},
            {"keywords": ["investment", "fund"], "proximity": 5, "weight": 0.9},
            {"keywords": ["mutual", "fund"], "proximity": 5, "weight": 0.9},
            {"keywords": ["retirement", "account"], "proximity": 5, "weight": 0.9},
            {"keywords": ["retirement", "fund"], "proximity": 5, "weight": 0.9},
            {"keywords": ["stock", "purchase"], "proximity": 5, "weight": 0.9},
            {"keywords": ["bond", "purchase"], "proximity": 5, "weight": 0.9},
            {"keywords": ["share", "purchase"], "proximity": 5, "weight": 0.9},
            {"keywords": ["equity", "purchase"], "proximity": 5, "weight": 0.9},
            {"keywords": ["securities", "purchase"], "proximity": 5, "weight": 0.9},
            {"keywords": ["investment", "deposit"], "proximity": 5, "weight": 0.8},
            {"keywords": ["investment", "contribution"], "proximity": 5, "weight": 0.8},
            {"keywords": ["stock", "bond"], "proximity": 10, "weight": 0.9},  # Stock and bond combination
            {"keywords": ["equity", "bond"], "proximity": 10, "weight": 0.9},  # Equity and bond combination
            {"keywords": ["stock", "equity"], "proximity": 10, "weight": 0.8}  # Stock and equity combination
        ]

        # Semantic context patterns for securities
        self.securities_contexts = [
            {"keywords": ["securities", "account"], "proximity": 5, "weight": 1.0},
            {"keywords": ["securities", "trading"], "proximity": 5, "weight": 1.0},
            {"keywords": ["securities", "transaction"], "proximity": 5, "weight": 0.9},
            {"keywords": ["securities", "settlement"], "proximity": 5, "weight": 0.9},
            {"keywords": ["stock", "trading"], "proximity": 5, "weight": 0.9},
            {"keywords": ["bond", "trading"], "proximity": 5, "weight": 0.9},
            {"keywords": ["share", "trading"], "proximity": 5, "weight": 0.9},
            {"keywords": ["equity", "trading"], "proximity": 5, "weight": 0.9},
            {"keywords": ["brokerage", "account"], "proximity": 5, "weight": 0.9},
            {"keywords": ["broker", "account"], "proximity": 5, "weight": 0.9},
            {"keywords": ["trading", "account"], "proximity": 5, "weight": 0.8},
            {"keywords": ["stock", "exchange"], "proximity": 5, "weight": 0.8},
            {"keywords": ["securities", "exchange"], "proximity": 5, "weight": 0.8},
            {"keywords": ["bond", "market"], "proximity": 5, "weight": 0.8},
            {"keywords": ["stock", "market"], "proximity": 5, "weight": 0.8},
            {"keywords": ["equity", "market"], "proximity": 5, "weight": 0.8},
            {"keywords": ["securities", "market"], "proximity": 5, "weight": 0.8},
            {"keywords": ["treasury", "bond"], "proximity": 5, "weight": 0.9},
            {"keywords": ["corporate", "bond"], "proximity": 5, "weight": 0.9},
            {"keywords": ["government", "bond"], "proximity": 5, "weight": 0.9}
        ]

        # Investment-related terms for semantic similarity matching
        self.semantic_terms = [
            # Investment terms
            {"term": "investment", "purpose_code": "INVS", "threshold": 0.7, "weight": 1.0},
            {"term": "investing", "purpose_code": "INVS", "threshold": 0.7, "weight": 0.9},
            {"term": "portfolio", "purpose_code": "INVS", "threshold": 0.7, "weight": 0.8},
            {"term": "fund", "purpose_code": "INVS", "threshold": 0.7, "weight": 0.7},
            {"term": "mutual", "purpose_code": "INVS", "threshold": 0.7, "weight": 0.8},
            {"term": "retirement", "purpose_code": "INVS", "threshold": 0.7, "weight": 0.8},
            {"term": "pension", "purpose_code": "INVS", "threshold": 0.7, "weight": 0.8},
            {"term": "asset", "purpose_code": "INVS", "threshold": 0.7, "weight": 0.7},
            {"term": "wealth", "purpose_code": "INVS", "threshold": 0.7, "weight": 0.7},
            {"term": "management", "purpose_code": "INVS", "threshold": 0.7, "weight": 0.6},

            # Securities terms
            {"term": "securities", "purpose_code": "SECU", "threshold": 0.7, "weight": 1.0},
            {"term": "security", "purpose_code": "SECU", "threshold": 0.7, "weight": 0.9},
            {"term": "stock", "purpose_code": "SECU", "threshold": 0.7, "weight": 0.9},
            {"term": "share", "purpose_code": "SECU", "threshold": 0.7, "weight": 0.9},
            {"term": "equity", "purpose_code": "SECU", "threshold": 0.7, "weight": 0.9},
            {"term": "bond", "purpose_code": "SECU", "threshold": 0.7, "weight": 0.9},
            {"term": "treasury", "purpose_code": "SECU", "threshold": 0.7, "weight": 0.8},
            {"term": "corporate", "purpose_code": "SECU", "threshold": 0.7, "weight": 0.7},
            {"term": "government", "purpose_code": "SECU", "threshold": 0.7, "weight": 0.7},
            {"term": "municipal", "purpose_code": "SECU", "threshold": 0.7, "weight": 0.7},
            {"term": "debenture", "purpose_code": "SECU", "threshold": 0.7, "weight": 0.8},
            {"term": "brokerage", "purpose_code": "SECU", "threshold": 0.7, "weight": 0.8},
            {"term": "broker", "purpose_code": "SECU", "threshold": 0.7, "weight": 0.8},
            {"term": "trading", "purpose_code": "SECU", "threshold": 0.7, "weight": 0.7},
            {"term": "exchange", "purpose_code": "SECU", "threshold": 0.7, "weight": 0.7},
            {"term": "market", "purpose_code": "SECU", "threshold": 0.7, "weight": 0.6}
        ]

        # Negative indicators (patterns that suggest it's NOT an investment)
        self.negative_indicators = {
            'INVS': [
                'not investment', 'non-investment', 'excluding investment',
                'investment free', 'no investment', 'without investment',
                'investment tax', 'tax on investment',  # These are tax payments, not investments
                'donation', 'donate', 'donating', 'charitable', 'charity', 'charities',
                'nonprofit', 'non-profit', 'non profit', 'foundation', 'fundraiser',
                'fundraising', 'relief fund', 'disaster relief', 'humanitarian',
                'humanitarian aid', 'philanthropy', 'philanthropic', 'benevolent',
                'benevolence', 'giving', 'charitable giving', 'charitable organization',
                'nonprofit organization', 'non-profit organization', 'ngo', 'red cross',
                'unicef', 'salvation army', 'doctors without borders', 'oxfam',
                'care international', 'world vision', 'save the children', 'amnesty international',
                'donor', 'donr'
            ],
            'SECU': [
                'not securities', 'non-securities', 'excluding securities',
                'securities free', 'no securities', 'without securities',
                'securities tax', 'tax on securities',  # These are tax payments, not securities
                'donation', 'donate', 'donating', 'charitable', 'charity', 'charities',
                'nonprofit', 'non-profit', 'non profit', 'foundation', 'fundraiser',
                'fundraising', 'relief fund', 'disaster relief', 'humanitarian',
                'humanitarian aid', 'philanthropy', 'philanthropic', 'benevolent',
                'benevolence', 'giving', 'charitable giving', 'charitable organization',
                'nonprofit organization', 'non-profit organization', 'ngo', 'red cross',
                'unicef', 'salvation army', 'doctors without borders', 'oxfam',
                'care international', 'world vision', 'save the children', 'amnesty international',
                'donor', 'donr'
            ]
        }

        # Compile regex patterns for stock/bond combinations
        self.stock_bond_pattern = re.compile(r'\b(stock|stocks|share|shares|equity|equities)\b.*?\b(bond|bonds|debenture|note|notes)\b', re.IGNORECASE)
        self.bond_stock_pattern = re.compile(r'\b(bond|bonds|debenture|note|notes)\b.*?\b(stock|stocks|share|shares|equity|equities)\b', re.IGNORECASE)

    def enhance_classification(self, result, narration, message_type=None):
        """
        Enhance classification for investment-related transactions.

        Args:
            result: Initial classification result
            narration: Transaction narration
            message_type: Optional message type

        Returns:
            dict: Enhanced classification result
        """
        logger.debug(f"Investment enhancer called with narration: {narration}")

        # Get current purpose code and confidence
        purpose_code = result.get('purpose_code', 'OTHR')
        confidence = result.get('confidence', 0.0)

        # Don't override if already classified as INVS or SECU with high confidence
        if purpose_code in ['INVS', 'SECU'] and confidence >= 0.8:
            logger.debug(f"Already classified as {purpose_code} with high confidence: {confidence}")
            return result

        # EARLY CHECK: Check for negative indicators before any other processing
        narration_lower = narration.lower()

        # Check for charitable donation indicators first - if found, skip this enhancer completely
        donation_indicators = [
            'donation', 'donate', 'donating', 'charitable', 'charity', 'charities',
            'nonprofit', 'non-profit', 'non profit', 'foundation', 'fundraiser',
            'fundraising', 'relief fund', 'disaster relief', 'humanitarian',
            'humanitarian aid', 'philanthropy', 'philanthropic', 'benevolent',
            'benevolence', 'giving', 'charitable giving', 'charitable organization',
            'nonprofit organization', 'non-profit organization', 'ngo', 'red cross',
            'unicef', 'salvation army', 'doctors without borders', 'oxfam',
            'care international', 'world vision', 'save the children', 'amnesty international',
            'donor', 'donr'
        ]

        # If any donation indicator is found, skip this enhancer completely
        if any(indicator in narration_lower for indicator in donation_indicators):
            logger.debug(f"Skipping investment enhancer due to donation indicator in: {narration}")
            return result

        # Skip interbank-related payments
        interbank_terms = ['interbank', 'nostro', 'vostro', 'correspondent bank', 'bank to bank',
                          'rtgs', 'real time gross settlement', 'financial institution',
                          'liquidity management', 'reserve requirement']
        if any(term in narration_lower for term in interbank_terms):
            logger.debug(f"Skipping interbank-related payment: {narration}")
            return result

        # Check for negative indicators
        for purpose, indicators in self.negative_indicators.items():
            for indicator in indicators:
                if indicator in narration_lower:
                    logger.debug(f"Negative indicator for {purpose} found: {indicator}")
                    if purpose_code == purpose:
                        # If current purpose code matches the negative indicator, reduce confidence
                        result['confidence'] = max(0.3, confidence * 0.7)
                        result['reason'] = f"Negative indicator found: {indicator}"
                        return result

        # Check for stock/bond combinations (highest priority)
        if self.stock_bond_pattern.search(narration_lower) or self.bond_stock_pattern.search(narration_lower):
            logger.info(f"Stock/bond combination detected in narration")
            return self._create_enhanced_result(result, 'INVS', 0.95, "Stock/bond combination detected")

        # Direct keyword matching (high confidence)
        for purpose, keywords in self.direct_keywords.items():
            matched, keyword_confidence, keyword = self.direct_keyword_match(narration, purpose)
            if matched:
                logger.info(f"{purpose} keyword match: {keyword} with confidence {keyword_confidence}")
                return self._create_enhanced_result(result, purpose, keyword_confidence, f"Direct {purpose} keyword match: {keyword}")

        # Semantic context pattern matching
        invs_context_score = self.context_match(narration, self.investment_contexts)
        secu_context_score = self.context_match(narration, self.securities_contexts)

        # Count the number of distinct context patterns matched
        invs_context_matches = self.count_context_matches(narration, self.investment_contexts)
        secu_context_matches = self.count_context_matches(narration, self.securities_contexts)

        # Enforce 3-word rule: only apply if at least 3 distinct context patterns matched
        if (invs_context_score >= 0.7 and invs_context_matches >= 3) or (secu_context_score >= 0.7 and secu_context_matches >= 3):
            if invs_context_score > secu_context_score and invs_context_matches >= 3:
                logger.info(f"Investment context match with score: {invs_context_score:.2f} and {invs_context_matches} patterns")
                return self._create_enhanced_result(result, 'INVS', min(0.95, invs_context_score),
                                                  f"Investment context match with score: {invs_context_score:.2f} and {invs_context_matches} patterns (3+ word rule enforced)")
            elif secu_context_matches >= 3:
                logger.info(f"Securities context match with score: {secu_context_score:.2f} and {secu_context_matches} patterns")
                return self._create_enhanced_result(result, 'SECU', min(0.95, secu_context_score),
                                                  f"Securities context match with score: {secu_context_score:.2f} and {secu_context_matches} patterns (3+ word rule enforced)")

        # Log if we had high scores but insufficient context matches
        if (invs_context_score >= 0.7 and invs_context_matches < 3) or (secu_context_score >= 0.7 and secu_context_matches < 3):
            logger.debug(f"Insufficient context matches despite high scores: INVS={invs_context_matches}, SECU={secu_context_matches} (3+ word rule enforced)")

        # Semantic similarity matching with 3-word minimum requirement
        matched, sem_confidence, sem_purpose_code, sem_matches = self.semantic_similarity_match(narration, self.semantic_terms)

        # Only apply if we have at least 3 semantic matches (enforcing 3-word rule)
        if matched and sem_purpose_code in ['INVS', 'SECU'] and len(sem_matches) >= 3:
            logger.info(f"{sem_purpose_code} semantic match with confidence: {sem_confidence:.2f} and {len(sem_matches)} matching terms")
            return self._create_enhanced_result(result, sem_purpose_code, sem_confidence,
                                              f"Semantic similarity matches: {len(sem_matches)} terms (3+ word rule enforced)")
        elif matched and sem_purpose_code in ['INVS', 'SECU'] and len(sem_matches) < 3:
            logger.debug(f"Insufficient semantic matches for {sem_purpose_code}: only {len(sem_matches)} terms (3+ word rule enforced)")
            # Don't apply the enhancement if fewer than 3 words match

        # Message type specific analysis
        if message_type:
            enhanced_result = self.analyze_message_type(result, narration, message_type)
            if enhanced_result != result:
                return enhanced_result

        # Check if we should override the current classification
        if self.should_override_classification(result, narration):
            # Determine which investment type to use for override
            if invs_context_score > secu_context_score:
                logger.info(f"Overriding {purpose_code} with INVS based on context analysis")
                return self._create_enhanced_result(result, 'INVS', 0.85, "Context analysis override")
            else:
                logger.info(f"Overriding {purpose_code} with SECU based on context analysis")
                return self._create_enhanced_result(result, 'SECU', 0.85, "Context analysis override")

        # Boost confidence if already classified as investment but with low confidence
        if purpose_code in ['INVS', 'SECU'] and confidence < 0.7:
            max_context_score = max(invs_context_score, secu_context_score)
            if max_context_score >= 0.5:
                enhanced_confidence = min(0.9, confidence + (max_context_score * 0.3))
                logger.info(f"Boosting {purpose_code} confidence from {confidence:.2f} to {enhanced_confidence:.2f}")
                return self._create_enhanced_result(result, purpose_code, enhanced_confidence, "Confidence boost from context analysis")

        # No investment pattern detected
        logger.debug("No investment pattern detected")
        return result

    def analyze_message_type(self, result, narration, message_type):
        """
        Analyze message type for investment-related patterns.

        Args:
            result: Current classification result
            narration: Transaction narration
            message_type: Message type

        Returns:
            dict: Enhanced classification result
        """
        narration_lower = narration.lower()

        # MT103 specific patterns (customer transfers)
        if message_type == 'MT103':
            # Check for investment-related keywords in MT103
            if any(keyword in narration_lower for keyword in ['investment', 'investing', 'stock', 'bond', 'securities']):
                if 'purchase' in narration_lower or 'buy' in narration_lower or 'acquire' in narration_lower:
                    logger.info(f"MT103 investment purchase detected")
                    return self._create_enhanced_result(result, 'INVS', 0.9, "MT103 investment purchase")

        # MT202 specific patterns (financial institution transfers)
        elif message_type == 'MT202' or message_type == 'MT202COV':
            # Check for securities-related keywords in MT202
            if any(keyword in narration_lower for keyword in ['securities', 'settlement', 'clearing', 'custody']):
                logger.info(f"MT202 securities settlement detected")
                return self._create_enhanced_result(result, 'SECU', 0.9, "MT202 securities settlement")

        # No message type specific pattern detected
        return result

    def should_override_classification(self, result, narration):
        """
        Determine if investment classification should override existing classification.

        Args:
            result: Current classification result
            narration: Transaction narration

        Returns:
            bool: True if should override
        """
        narration_lower = narration.lower()
        purpose_code = result.get('purpose_code', 'OTHR')
        confidence = result.get('confidence', 0.0)

        # Skip interbank-related payments
        interbank_terms = ['interbank', 'nostro', 'vostro', 'correspondent bank', 'bank to bank',
                          'rtgs', 'real time gross settlement', 'financial institution',
                          'liquidity management', 'reserve requirement']
        if any(term in narration_lower for term in interbank_terms):
            return False

        # Don't override INTC purpose code
        if purpose_code == 'INTC':
            return False

        # Check for strong investment context
        invs_context_score = self.context_match(narration, self.investment_contexts)
        secu_context_score = self.context_match(narration, self.securities_contexts)
        max_context_score = max(invs_context_score, secu_context_score)

        # Check if current classification has low confidence
        if confidence < 0.7 and max_context_score >= 0.6:
            return True

        # Don't override other classifications unless very strong evidence
        return False

    def count_context_matches(self, narration, context_patterns):
        """
        Count the number of distinct context patterns that match in the narration.
        This is used to enforce the 3-word rule for context matching.

        Args:
            narration: The narration text
            context_patterns: List of context patterns to check

        Returns:
            int: Number of distinct context patterns that match
        """
        if not narration or not context_patterns:
            return 0

        narration_lower = narration.lower()
        match_count = 0

        for pattern in context_patterns:
            keywords = pattern.get('keywords', [])
            proximity = pattern.get('proximity', 5)

            # Check if all keywords are present within the specified proximity
            if len(keywords) >= 2:  # Only count patterns with at least 2 keywords
                all_present = True
                for i in range(len(keywords)):
                    if keywords[i] not in narration_lower:
                        all_present = False
                        break

                if all_present:
                    # Check proximity if all keywords are present
                    tokens = narration_lower.split()
                    positions = []

                    for keyword in keywords:
                        # Find all positions of this keyword
                        keyword_positions = []
                        for i, token in enumerate(tokens):
                            if keyword in token:
                                keyword_positions.append(i)

                        if keyword_positions:
                            positions.append(keyword_positions)
                        else:
                            all_present = False
                            break

                    if all_present and positions:
                        # Check if any combination of positions satisfies the proximity requirement
                        for combo in itertools.product(*positions):
                            if max(combo) - min(combo) <= proximity:
                                match_count += 1
                                break

        return match_count

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
        if purpose_code == 'INVS':
            result['category_purpose_code'] = 'INVS'  # Direct mapping for INVS
        elif purpose_code == 'SECU':
            result['category_purpose_code'] = 'SECU'  # Direct mapping for SECU

        result['category_confidence'] = confidence

        # Add enhancement metadata
        result['enhanced'] = True
        result['enhancer'] = 'investment'
        result['reason'] = reason
        result['original_purpose_code'] = original_result.get('purpose_code')
        result['original_confidence'] = original_result.get('confidence')

        # Set force flags to prevent other enhancers from overriding
        # But don't set force flags for interbank-related narrations
        narration = original_result.get('narration', '')
        if narration:
            narration_lower = narration.lower()
            interbank_terms = ['interbank', 'nostro', 'vostro', 'correspondent bank', 'bank to bank',
                              'rtgs', 'real time gross settlement', 'financial institution',
                              'liquidity management', 'reserve requirement']
            if not any(term in narration_lower for term in interbank_terms) and confidence >= 0.9:
                result['force_purpose_code'] = True
                result['force_category_purpose_code'] = True

        return result
