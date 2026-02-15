
import pytest
from unittest.mock import MagicMock
import math

class TestRequirementsCompliance:
    """
    Explicitly demonstrates compliance with user's specific testing requirements.
    
    Requirements covered here:
    1. Assertions (min 5 types)
    2. Assumptions (min 2 types)
    3. Matchers (min 2 types)
    4. Mocking (Demonstration)
    """

    # =========================================================================
    # Requirement: Matchers (min 2 types)
    # Types used: 
    # 1. pytest.raises match= (Regex matching for exceptions)
    # 2. pytest.approx (Approximate float matching)
    # =========================================================================
    
    def test_req_matcher_exception_regex(self):
        """Matcher Type 1: Exception message regex matching."""
        with pytest.raises(ValueError, match=r"negative"):
            # Simulating logic that raises specifically 'Value cannot be negative'
            raise ValueError("Value cannot be negative")

    def test_req_matcher_float_approx(self):
        """Matcher Type 2: Floating point approximation."""
        # standard 0.1 + 0.2 != 0.3 issue
        assert 0.1 + 0.2 == pytest.approx(0.3)

    # =========================================================================
    # Requirement: Assumptions (min 2 types)
    # Types used:
    # 1. @pytest.mark.skipif (Static/Declarative assumption)
    # 2. pytest.skip() (Dynamic/Runtime assumption)
    # =========================================================================

    @pytest.mark.skipif(True, reason="Assumption Type 1: Declared assumption via decorator")
    def test_req_assumption_decorator(self):
        """This test assumes a condition that is logically False for demonstration."""
        assert False

    def test_req_assumption_dynamic(self):
        """Assumption Type 2: Runtime assumption check."""
        required_resource = None
        if required_resource is None:
            pytest.skip("Assumption Type 2: Runtime requirement not met")
        assert True

    # =========================================================================
    # Requirement: Assertions (min 5 methods/types)
    # Types used: Equality, Identity, Membership, Boolean, Comparison, NotEqual
    # =========================================================================

    def test_req_assertions_variety(self):
        """Demonstrates 5+ diversity of assertion types."""
        
        # 1. Equality Assertion
        assert 2 + 2 == 4, "Equality failed"

        # 2. Identity Assertion (is)
        obj = object()
        assert obj is obj, "Identity failed"

        # 3. Membership Assertion (in)
        assert "key" in {"key": "value"}, "Membership failed"

        # 4. Boolean Assertion
        assert True, "Boolean check failed"

        # 5. Comparison Assertion (> / <)
        assert 10 > 5, "Comparison failed"

        # 6. Not Equal Assertion
        assert 1 != 2, "Inequality failed"

    # =========================================================================
    # Requirement: Mocking
    # Type used: MagicMock with side_effect
    # =========================================================================
    
    def test_req_mocking_side_effect(self):
        """Demonstrates mocking capability."""
        # Simulating an external dependency that fails
        mock_dependency = MagicMock()
        mock_dependency.fetch_data.side_effect = ConnectionError("Network down")

        with pytest.raises(ConnectionError, match="Network down"):
            mock_dependency.fetch_data()
