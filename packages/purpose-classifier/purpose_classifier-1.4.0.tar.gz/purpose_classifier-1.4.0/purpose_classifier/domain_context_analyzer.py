"""
Domain Context Analyzer for Purpose Code Classification.

This module provides functionality to analyze the context of specific terms
across different domains (cross-border, loan, trade, etc.) to improve
semantic understanding and classification accuracy.
"""

import logging
from purpose_classifier.semantic_pattern_matcher import SemanticPatternMatcher

logger = logging.getLogger(__name__)

class DomainContextAnalyzer:
    """
    Analyzes the context of specific terms across different domains.
    
    This class helps determine the most likely domain context for ambiguous terms
    like "settlement" by analyzing surrounding words and semantic relationships.
    """
    
    def __init__(self, matcher=None):
        """
        Initialize the domain context analyzer.
        
        Args:
            matcher: Optional SemanticPatternMatcher instance to use
        """
        if matcher:
            self.matcher = matcher
        else:
            # Initialize a new matcher
            self.matcher = SemanticPatternMatcher()
            
        # Define domain-specific context indicators
        self.domain_indicators = {
            'cross_border': [
                'cross border', 'cross-border', 'international', 'foreign', 'overseas',
                'global', 'transnational', 'wire transfer', 'swift', 'iban',
                'international settlement', 'cross border settlement', 'cross-border settlement',
                'international transfer', 'cross border transfer', 'cross-border transfer',
                'international payment', 'cross border payment', 'cross-border payment'
            ],
            'loan': [
                'loan', 'credit', 'mortgage', 'financing', 'borrowing', 'lending',
                'principal', 'interest', 'repayment', 'installment', 'amortization',
                'loan settlement', 'credit settlement', 'mortgage settlement',
                'loan repayment', 'credit repayment', 'mortgage repayment'
            ],
            'trade': [
                'trade', 'goods', 'merchandise', 'commercial', 'import', 'export',
                'invoice', 'purchase', 'sale', 'supplier', 'buyer', 'seller',
                'trade settlement', 'commercial settlement', 'invoice settlement',
                'trade payment', 'commercial payment', 'invoice payment'
            ],
            'securities': [
                'securities', 'stocks', 'bonds', 'shares', 'equities', 'investment',
                'portfolio', 'trading', 'brokerage', 'custody', 'dividend',
                'securities settlement', 'stock settlement', 'bond settlement',
                'securities transaction', 'stock transaction', 'bond transaction'
            ],
            'forex': [
                'forex', 'fx', 'foreign exchange', 'currency', 'exchange rate', 'conversion',
                'spot', 'forward', 'swap', 'option', 'derivative',
                'forex settlement', 'fx settlement', 'currency settlement',
                'forex transaction', 'fx transaction', 'currency transaction'
            ],
            'interbank': [
                'interbank', 'bank to bank', 'correspondent', 'nostro', 'vostro', 'loro',
                'liquidity', 'clearing', 'settlement', 'funding', 'reserve',
                'interbank settlement', 'bank to bank settlement', 'correspondent settlement',
                'interbank transfer', 'bank to bank transfer', 'correspondent transfer'
            ]
        }
        
        # Define ambiguous terms that need context analysis
        self.ambiguous_terms = {
            'settlement': {
                'cross_border': 0.7,  # Default weights for each domain
                'loan': 0.6,
                'trade': 0.9,  # Trade has highest default weight for settlement
                'securities': 0.8,
                'forex': 0.8,
                'interbank': 0.7
            },
            'transfer': {
                'cross_border': 0.9,  # Cross-border has highest default weight for transfer
                'loan': 0.5,
                'trade': 0.6,
                'securities': 0.7,
                'forex': 0.7,
                'interbank': 0.8
            },
            'payment': {
                'cross_border': 0.8,
                'loan': 0.7,
                'trade': 0.8,
                'securities': 0.6,
                'forex': 0.6,
                'interbank': 0.7
            }
        }
        
    def analyze_term_context(self, term, narration):
        """
        Analyze the context of a specific term in the narration.
        
        Args:
            term: The ambiguous term to analyze
            narration: The narration text
            
        Returns:
            tuple: (domain, confidence, reason)
        """
        if term not in self.ambiguous_terms:
            return (None, 0.0, f"Term '{term}' is not in the list of ambiguous terms")
            
        narration_lower = narration.lower()
        
        # Skip if the term is not in the narration
        if term not in narration_lower:
            return (None, 0.0, f"Term '{term}' not found in narration")
            
        # Calculate domain scores based on context indicators
        domain_scores = {}
        domain_matches = {}
        
        for domain, indicators in self.domain_indicators.items():
            # Start with the default weight for this term and domain
            base_weight = self.ambiguous_terms[term].get(domain, 0.5)
            domain_scores[domain] = base_weight
            domain_matches[domain] = []
            
            # Check for exact matches of domain indicators
            for indicator in indicators:
                if indicator in narration_lower:
                    # Strong boost for exact matches
                    domain_scores[domain] += 0.3
                    domain_matches[domain].append(f"exact:{indicator}")
                    
            # Check for semantic matches if no exact matches were found
            if not domain_matches[domain]:
                words = self.matcher.tokenize(narration_lower)
                for indicator in indicators:
                    indicator_words = indicator.split()
                    for word in words:
                        # Skip the ambiguous term itself
                        if word == term:
                            continue
                            
                        # Check semantic similarity with each indicator word
                        for indicator_word in indicator_words:
                            try:
                                similarity = self.matcher.semantic_similarity(word, indicator_word)
                                if similarity > 0.8:  # High similarity threshold
                                    domain_scores[domain] += 0.2
                                    domain_matches[domain].append(f"semantic:{word}~{indicator_word}:{similarity:.2f}")
                                elif similarity > 0.7:  # Medium similarity threshold
                                    domain_scores[domain] += 0.1
                                    domain_matches[domain].append(f"semantic:{word}~{indicator_word}:{similarity:.2f}")
                            except Exception as e:
                                logger.debug(f"Error calculating similarity: {str(e)}")
                                continue
        
        # Find the domain with the highest score
        best_domain = max(domain_scores.items(), key=lambda x: x[1])
        domain_name, score = best_domain
        
        # Only return a domain if the score is above a threshold
        if score > 0.7:
            matches = domain_matches[domain_name]
            reason = f"Domain '{domain_name}' for term '{term}' with score {score:.2f}"
            if matches:
                reason += f" based on matches: {', '.join(matches[:3])}"
            return (domain_name, score, reason)
        else:
            return (None, score, f"No strong domain context found for term '{term}' (best: {domain_name}, score: {score:.2f})")
            
    def get_purpose_code_for_domain(self, domain, term):
        """
        Get the most likely purpose code for a domain and term.
        
        Args:
            domain: The domain context
            term: The ambiguous term
            
        Returns:
            tuple: (purpose_code, confidence)
        """
        # Map domains to purpose codes
        domain_to_purpose = {
            'cross_border': 'XBCT',
            'loan': 'LOAN',
            'trade': 'CORT',
            'securities': 'SECU',
            'forex': 'FREX',
            'interbank': 'INTC'
        }
        
        # Default confidence based on domain and term
        domain_term_confidence = {
            'cross_border': {'settlement': 0.85, 'transfer': 0.95, 'payment': 0.90},
            'loan': {'settlement': 0.85, 'transfer': 0.75, 'payment': 0.80},
            'trade': {'settlement': 0.95, 'transfer': 0.85, 'payment': 0.90},
            'securities': {'settlement': 0.90, 'transfer': 0.85, 'payment': 0.80},
            'forex': {'settlement': 0.90, 'transfer': 0.85, 'payment': 0.80},
            'interbank': {'settlement': 0.85, 'transfer': 0.90, 'payment': 0.85}
        }
        
        if domain in domain_to_purpose:
            purpose_code = domain_to_purpose[domain]
            confidence = domain_term_confidence.get(domain, {}).get(term, 0.8)
            return (purpose_code, confidence)
        else:
            return (None, 0.0)
