"""
Semantic Enhancer Base Class for Purpose Code Classification.

This module provides a base class for all semantic enhancers, combining
BaseEnhancer functionality with semantic pattern matching capabilities.
"""

import os
import logging
from purpose_classifier.semantic_pattern_matcher import SemanticPatternMatcher

logger = logging.getLogger(__name__)

class SemanticEnhancer:
    """
    Base class for all semantic enhancers.

    Combines enhancer functionality with semantic pattern matching capabilities
    for improved purpose code classification accuracy.
    """

    def __init__(self, matcher=None):
        """
        Initialize the semantic enhancer.

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
            self.matcher = SemanticPatternMatcher(embeddings_path)

            # Log whether embeddings were loaded
            if self.matcher.embeddings:
                logger.info(f"Word embeddings loaded successfully for {self.__class__.__name__}")
            else:
                logger.warning(f"Word embeddings not loaded for {self.__class__.__name__}")

        # Initialize common patterns and contexts
        self.context_patterns = []
        self.direct_keywords = {}
        self.semantic_terms = []
        self.confidence_thresholds = {
            'direct_match': 0.95,
            'context_match': 0.80,  # Reduced from 0.85 to 0.80
            'semantic_match': 0.70  # Reduced from 0.75 to 0.70
        }

        # Minimum requirements for semantic coherence
        self.semantic_coherence = {
            'min_matches': 3,           # Minimum number of matching words required (increased from 2 to 3)
            'min_context_words': 3,     # Minimum number of context words required (increased from 2 to 3)
            'min_similarity': 0.75,     # Minimum similarity threshold (increased from 0.7 to 0.75)
            'coherence_threshold': 0.65  # Minimum coherence between matched words (increased from 0.6 to 0.65)
        }

    def enhance_classification(self, result, narration, message_type=None):
        """
        Base implementation of semantic enhancement with improved contextual requirements.
        Ensures that classifications are based on sufficient contextual evidence and
        defaults to OTHR when there isn't enough context for a confident prediction.

        Args:
            result: Initial classification result
            narration: Transaction narration
            message_type: Optional message type

        Returns:
            dict: Enhanced classification result
        """
        # Skip processing if narration is too short
        if not narration or len(narration.split()) < self.semantic_coherence['min_context_words']:
            return result

        narration_lower = narration.lower()

        # Track all potential matches for conflict resolution
        potential_matches = []

        # Check for direct keyword matches first (highest confidence)
        for purpose_code in self.direct_keywords:
            matched, confidence, keyword = self.direct_keyword_match(
                narration_lower, purpose_code
            )
            if matched:
                match_result = {
                    'purpose_code': purpose_code,
                    'confidence': confidence,
                    'enhancer': self.__class__.__name__.lower(),
                    'reason': f"Direct keyword match: {keyword}",
                    'match_type': 'direct',
                    'match_count': len(keyword.split(','))
                }

                # If we have a high-confidence multi-word match, return immediately
                if confidence > 0.9 and match_result['match_count'] >= 2:
                    return match_result

                potential_matches.append(match_result)

        # Check for context pattern matches next
        for pattern in self.context_patterns:
            try:
                purpose_code = pattern.get('purpose_code')
                matched, confidence, pattern_info = self.context_match_for_purpose(
                    narration_lower, purpose_code
                )
                if matched:
                    match_result = {
                        'purpose_code': purpose_code,
                        'confidence': confidence,
                        'enhancer': self.__class__.__name__.lower(),
                        'reason': f"Context pattern match: {pattern_info.get('matched_keywords', pattern_info['keywords'])}",
                        'match_type': 'context',
                        'match_count': len(pattern_info.get('matched_keywords', pattern_info['keywords']))
                    }

                    # If we have a high-confidence context match with multiple keywords, return immediately
                    if confidence > 0.85 and match_result['match_count'] >= 2:
                        return match_result

                    potential_matches.append(match_result)
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error in context_match_for_purpose: {str(e)}")
                continue

        # Check for semantic similarity matches last
        try:
            matched, confidence, purpose_code, matches = self.semantic_similarity_match(
                narration_lower, self.semantic_terms
            )
            if matched and purpose_code:
                # Count unique words and terms that matched
                unique_words = set(match[0] for match in matches if match[2] == purpose_code)
                unique_terms = set(match[1] for match in matches if match[2] == purpose_code)

                match_result = {
                    'purpose_code': purpose_code,
                    'confidence': confidence,
                    'enhancer': self.__class__.__name__.lower(),
                    'reason': f"Semantic similarity match: {len(unique_words)} words matched {len(unique_terms)} terms",
                    'match_type': 'semantic',
                    'match_count': len(unique_words)
                }

                # If we have a high-confidence semantic match with multiple words, return immediately
                if confidence > 0.8 and len(unique_words) >= 2:
                    return match_result

                potential_matches.append(match_result)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in semantic_similarity_match: {str(e)}")

        # If we have potential matches, select the best one
        if potential_matches:
            # Sort by confidence and match count
            sorted_matches = sorted(
                potential_matches,
                key=lambda m: (m['confidence'], m['match_count']),
                reverse=True
            )

            best_match = sorted_matches[0]

            # Only return if we have sufficient confidence and match count
            if (best_match['confidence'] > 0.7 and best_match['match_count'] >= 2) or \
               (best_match['confidence'] > 0.9 and best_match['match_count'] >= 1):
                return best_match

            # If we have multiple matches for the same purpose code, boost confidence
            if len(sorted_matches) >= 2 and sorted_matches[0]['purpose_code'] == sorted_matches[1]['purpose_code']:
                best_match['confidence'] = min(0.95, best_match['confidence'] * 1.1)
                best_match['reason'] += f" (boosted by multiple match types)"
                return best_match

        # No confident matches found, return original result
        # If original result is OTHR with low confidence, keep it
        if result.get('purpose_code') == 'OTHR' and result.get('confidence', 0) < 0.5:
            return result

        # If we have a potential match but not confident enough, default to OTHR
        if potential_matches and result.get('purpose_code') != 'OTHR':
            othr_result = result.copy()
            othr_result['purpose_code'] = 'OTHR'
            othr_result['confidence'] = 0.5
            othr_result['enhancer'] = self.__class__.__name__.lower()
            othr_result['reason'] = "Insufficient contextual evidence for confident classification"
            othr_result['original_purpose_code'] = result.get('purpose_code')
            othr_result['original_confidence'] = result.get('confidence')
            return othr_result

        return result

    def direct_keyword_match(self, narration, purpose_code):
        """
        Check for direct keyword matches with additional context validation.
        Requires multiple words or phrases for a match to ensure semantic coherence.

        Args:
            narration: Transaction narration
            purpose_code: Purpose code to check keywords for

        Returns:
            tuple: (matched, confidence, keyword)
        """
        narration_lower = narration.lower()
        words = narration_lower.split()

        # Skip short narrations that don't have enough context
        if len(words) < self.semantic_coherence['min_context_words']:
            return (False, 0.0, None)

        if purpose_code not in self.direct_keywords:
            return (False, 0.0, None)

        # Find all matching keywords
        matched_keywords = []
        for keyword in self.direct_keywords[purpose_code]:
            keyword_lower = keyword.lower()
            # Check if it's a multi-word keyword
            if ' ' in keyword_lower:
                if keyword_lower in narration_lower:
                    matched_keywords.append(keyword)
            # For single words, ensure they're not just part of another word
            elif any(word == keyword_lower for word in words):
                matched_keywords.append(keyword)

        # If we have enough matches, return success
        if len(matched_keywords) >= self.semantic_coherence['min_matches']:
            # Join matched keywords for the reason
            matched_str = ", ".join(matched_keywords)
            return (True, self.confidence_thresholds['direct_match'], matched_str)

        # If we have only one match but it's a multi-word phrase (which has more context)
        elif len(matched_keywords) == 1 and ' ' in matched_keywords[0].lower() and len(matched_keywords[0].lower().split()) >= 2:
            return (True, self.confidence_thresholds['direct_match'], matched_keywords[0])

        return (False, 0.0, None)

    def context_match(self, narration, context_patterns):
        """
        Check for context pattern matches.

        Args:
            narration: Transaction narration
            context_patterns: List of context pattern dictionaries
                Each dict has keys: 'keywords', 'proximity', 'weight'

        Returns:
            float: Match score between 0 and 1
        """
        words = self.matcher.tokenize(narration.lower())
        total_score = 0.0
        max_weight = sum(pattern['weight'] for pattern in context_patterns)

        for pattern in context_patterns:
            keywords = pattern['keywords']
            proximity = pattern['proximity']
            weight = pattern['weight']

            # Check if all keywords are within proximity
            if self.matcher.keywords_in_proximity(words, keywords, proximity):
                total_score += weight

        return total_score / max_weight if max_weight > 0 else 0.0

    def context_match_for_purpose(self, narration, purpose_code, message_type=None):
        """
        Check for context pattern matches for a specific purpose code.
        Ensures that there are enough contextual keywords to make a reliable match.

        Args:
            narration: Transaction narration
            purpose_code: Purpose code to check context for
            message_type: Optional message type (not used in base implementation)

        Returns:
            tuple: (matched, confidence, pattern)
        """
        # Filter context patterns for this purpose code
        relevant_patterns = [p for p in self.context_patterns
                           if p.get('purpose_code') == purpose_code]

        if not relevant_patterns:
            return (False, 0.0, None)

        words = self.matcher.tokenize(narration)

        # Skip short narrations that don't have enough context
        if len(words) < self.semantic_coherence['min_context_words']:
            return (False, 0.0, None)

        # Check each pattern
        for pattern in relevant_patterns:
            # Check if pattern has required keys
            if 'keywords' not in pattern or 'proximity' not in pattern or 'weight' not in pattern:
                continue

            keywords = pattern['keywords']
            proximity = pattern['proximity']
            weight = pattern['weight']

            # Require at least min_matches keywords for a match
            if len(keywords) < self.semantic_coherence['min_matches']:
                continue

            # Check if keywords are in proximity
            if self.matcher.keywords_in_proximity(words, keywords, proximity):
                # Calculate how many keywords actually matched
                matched_keywords = []
                for keyword in keywords:
                    if any(word.lower() == keyword.lower() for word in words):
                        matched_keywords.append(keyword)
                    elif self.matcher and hasattr(self.matcher, 'embeddings'):
                        # Try semantic matching
                        for word in words:
                            try:
                                similarity = self.matcher.semantic_similarity(word, keyword)
                                if similarity >= self.semantic_coherence['min_similarity']:
                                    matched_keywords.append(keyword)
                                    break
                            except:
                                continue

                # Require at least min_matches keywords to match
                if len(matched_keywords) >= self.semantic_coherence['min_matches']:
                    confidence = min(self.confidence_thresholds['context_match'], weight)
                    # Add matched keywords to pattern for logging
                    pattern_copy = pattern.copy()
                    pattern_copy['matched_keywords'] = matched_keywords
                    return (True, confidence, pattern_copy)

        return (False, 0.0, None)

    def semantic_similarity_match(self, narration, semantic_terms):
        """
        Check for semantic similarity matches with enhanced coherence requirements.
        Requires multiple matching terms with sufficient semantic similarity to ensure
        the match is contextually relevant and not based on a single generic word.

        Args:
            narration: Transaction narration
            semantic_terms: List of semantic term dictionaries
                Each dict has keys: 'term', 'purpose_code', 'threshold', 'weight'

        Returns:
            tuple: (matched, confidence, purpose_code, matches)
        """
        narration_lower = narration.lower()
        words = self.matcher.tokenize(narration_lower)

        # Skip short narrations that don't have enough context
        if len(words) < self.semantic_coherence['min_context_words']:
            return (False, 0.0, None, [])

        # Check semantic similarity
        matches = []
        for term_data in semantic_terms:
            term = term_data['term']
            purpose_code = term_data['purpose_code']
            threshold = term_data.get('threshold', self.semantic_coherence['min_similarity'])
            weight = term_data.get('weight', 1.0)

            for word in words:
                try:
                    similarity = self.matcher.semantic_similarity(word, term)
                    if similarity >= threshold:
                        matches.append((word, term, purpose_code, similarity, weight))
                except Exception as e:
                    continue

        if matches:
            # Group matches by purpose code
            purpose_matches = {}
            for match in matches:
                word, term, purpose_code, similarity, weight = match
                if purpose_code not in purpose_matches:
                    purpose_matches[purpose_code] = []
                purpose_matches[purpose_code].append((word, term, similarity, weight))

            # Find purpose code with highest weighted similarity and enough matches
            best_purpose_code = None
            best_confidence = 0.0
            best_match_count = 0

            for purpose_code, code_matches in purpose_matches.items():
                # Check if we have enough matches for this purpose code
                if len(code_matches) < self.semantic_coherence['min_matches']:
                    continue

                # Check for semantic coherence between matched words
                coherence_score = self._calculate_coherence(code_matches)
                if coherence_score < self.semantic_coherence['coherence_threshold']:
                    continue

                # Calculate weighted similarity
                total_weight = sum(m[3] for m in code_matches)
                weighted_similarity = sum(m[2] * m[3] for m in code_matches) / total_weight

                # Apply a bonus for having more matches
                match_count_bonus = min(0.1, (len(code_matches) - 1) * 0.05)  # 5% per additional match, up to 10%
                adjusted_similarity = weighted_similarity * (1.0 + match_count_bonus)

                confidence = min(self.confidence_thresholds['semantic_match'], adjusted_similarity)

                if confidence > best_confidence or (confidence == best_confidence and len(code_matches) > best_match_count):
                    best_confidence = confidence
                    best_purpose_code = purpose_code
                    best_match_count = len(code_matches)

            if best_purpose_code:
                return (True, best_confidence, best_purpose_code, matches)

        return (False, 0.0, None, [])

    def _calculate_coherence(self, matches):
        """
        Calculate semantic coherence between matched words.

        Args:
            matches: List of (word, term, similarity, weight) tuples

        Returns:
            float: Coherence score between 0 and 1
        """
        if len(matches) < 2:
            return 0.0

        # Extract words and terms
        words = [m[0] for m in matches]
        terms = [m[1] for m in matches]

        # Calculate pairwise similarities between matched words
        total_similarity = 0.0
        pair_count = 0

        for i in range(len(words)):
            for j in range(i+1, len(words)):
                try:
                    similarity = self.matcher.semantic_similarity(words[i], words[j])
                    total_similarity += similarity
                    pair_count += 1
                except:
                    continue

        # Calculate pairwise similarities between matched terms
        for i in range(len(terms)):
            for j in range(i+1, len(terms)):
                try:
                    similarity = self.matcher.semantic_similarity(terms[i], terms[j])
                    total_similarity += similarity
                    pair_count += 1
                except:
                    continue

        return total_similarity / pair_count if pair_count > 0 else 0.0

    def load_word_embeddings(self, embeddings_path):
        """
        Load word embeddings for semantic similarity matching.

        Args:
            embeddings_path: Path to word embeddings file

        Returns:
            bool: True if embeddings were loaded successfully
        """
        return self.matcher.load_word_embeddings(embeddings_path)

    def calculate_confidence(self, match_scores, weights=None):
        """
        Calculate overall confidence score from multiple match scores.

        Args:
            match_scores (dict): Dictionary of {pattern_name: score}
            weights (dict, optional): Dictionary of {pattern_name: weight}

        Returns:
            float: Confidence score between 0 and 1
        """
        if not match_scores:
            return 0.0

        if weights is None:
            weights = {name: 1.0 for name in match_scores}

        total_weight = sum(weights.values())
        weighted_score = sum(score * weights.get(name, 1.0)
                            for name, score in match_scores.items())

        return weighted_score / total_weight if total_weight > 0 else 0.0

    def should_override_classification(self, result, narration):
        """
        Determine if classification should override existing classification.

        Args:
            result: Current classification result
            narration: Transaction narration

        Returns:
            bool: True if should override
        """
        # Subclasses should override this method
        return False

    def _create_enhanced_result(self, original_result, purpose_code, confidence, reason):
        """
        Create an enhanced result dictionary.

        Args:
            original_result: Original classification result
            purpose_code: New purpose code
            confidence: New confidence score
            reason: Reason for enhancement

        Returns:
            dict: Enhanced classification result
        """
        # Create a copy of the original result
        result = original_result.copy()

        # Update with enhanced values
        result['purpose_code'] = purpose_code
        result['confidence'] = confidence

        # Add enhancement metadata
        result['enhanced'] = True
        result['enhancer'] = self.__class__.__name__.lower()
        result['reason'] = reason
        result['original_purpose_code'] = original_result.get('purpose_code')
        result['original_confidence'] = original_result.get('confidence')

        return result
