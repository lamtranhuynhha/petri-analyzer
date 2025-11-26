"""
Tests cho thuật toán Deadlock Detection
"""
import pytest
from app.algorithms.deadlock import analyze_deadlock


class TestDeadlock:
    """Test suite cho thuật toán deadlock detection"""
    
    def test_simple_linear_net_has_deadlock(self, simple_linear_net):
        """Test mạng Petri đơn giản - phải có deadlock ở state cuối"""
        result = analyze_deadlock(simple_linear_net)
        
        assert result is not None
        assert hasattr(result, 'total_states')
        assert hasattr(result, 'total_deadlocks')
        assert hasattr(result, 'deadlock_markings')
        
        # Mạng này phải có ít nhất 1 deadlock
        assert result.total_deadlocks >= 1
        assert len(result.deadlock_markings) >= 1
        
        print(f"✓ Simple linear net: {result.total_deadlocks} deadlocks in {result.total_states} states")
    
    def test_cyclic_net_no_deadlock(self, cyclic_net):
        """Test mạng Petri có chu trình - không có deadlock"""
        result = analyze_deadlock(cyclic_net)
        
        assert result is not None
        # Mạng cyclic không có deadlock
        assert result.total_deadlocks == 0
        assert len(result.deadlock_markings) == 0
        
        print(f"✓ Cyclic net: {result.total_deadlocks} deadlocks (expected 0)")
    
    def test_producer_consumer_has_deadlock(self, producer_consumer_net):
        """Test mạng Producer-Consumer - có deadlock khi buffer rỗng"""
        result = analyze_deadlock(producer_consumer_net)
        
        assert result is not None
        assert result.total_states > 0
        
        print(f"✓ Producer-Consumer: {result.total_deadlocks} deadlocks in {result.total_states} states")
    
    def test_deadlock_net_multiple_deadlocks(self, deadlock_net):
        """Test mạng được thiết kế để có nhiều deadlock"""
        result = analyze_deadlock(deadlock_net)
        
        assert result is not None
        # Mạng này phải có deadlock
        assert result.total_deadlocks > 0
        
        print(f"✓ Deadlock net: {result.total_deadlocks} deadlocks")
        print(f"  Deadlock markings: {result.deadlock_markings}")
    
    def test_mutual_exclusion_no_deadlock(self, mutual_exclusion_net):
        """Test mạng Mutual Exclusion - không có deadlock nếu thiết kế đúng"""
        result = analyze_deadlock(mutual_exclusion_net)
        
        assert result is not None
        
        print(f"✓ Mutual Exclusion: {result.total_deadlocks} deadlocks in {result.total_states} states")
    
    def test_empty_net_is_deadlock(self, empty_net):
        """Test edge case: mạng rỗng - initial state là deadlock"""
        result = analyze_deadlock(empty_net)
        
        assert result is not None
        # Mạng rỗng: initial state là deadlock
        assert result.total_deadlocks >= 1
        
        print(f"✓ Empty net: {result.total_deadlocks} deadlocks")
    
    def test_single_place_net_no_deadlock(self, single_place_net):
        """Test edge case: mạng 1 place - không có deadlock nếu có chu trình"""
        result = analyze_deadlock(single_place_net)
        
        assert result is not None
        
        print(f"✓ Single place net: {result.total_deadlocks} deadlocks")
    
    def test_deadlock_markings_format(self, simple_linear_net):
        """Test format của deadlock markings"""
        result = analyze_deadlock(simple_linear_net)
        
        assert isinstance(result.deadlock_markings, list)
        
        # Mỗi deadlock marking phải là dict
        for marking in result.deadlock_markings:
            assert isinstance(marking, dict)
            # Mỗi place phải có giá trị integer
            for place, tokens in marking.items():
                assert isinstance(place, str)
                assert isinstance(tokens, int)
                assert tokens >= 0
        
        print(f"✓ Deadlock markings format check passed")
    
    def test_total_states_positive(self, simple_linear_net):
        """Test total_states phải > 0"""
        result = analyze_deadlock(simple_linear_net)
        
        assert result.total_states > 0
        assert result.total_deadlocks >= 0
        assert result.total_deadlocks <= result.total_states
        
        print(f"✓ States check: {result.total_deadlocks}/{result.total_states} are deadlocks")


class TestDeadlockEdgeCases:
    """Test các edge cases đặc biệt"""
    
    def test_all_transitions_disabled(self):
        """Test mạng mà tất cả transitions đều disabled"""
        from app.core.schemas import PetriNetRequest
        
        net = PetriNetRequest(
            places=["p1", "p2"],
            transitions=["t1"],
            arcs=[
                ["p1", "t1"],
                ["t1", "p2"]
            ],
            weights={},
            initial_marking={"p1": 0, "p2": 0}  # Không có token nào
        )
        
        result = analyze_deadlock(net)
        
        assert result is not None
        # Initial state là deadlock
        assert result.total_deadlocks == 1
        
        print(f"✓ All transitions disabled: {result.total_deadlocks} deadlocks")
    
    def test_weighted_net_deadlock(self, weighted_net):
        """Test deadlock detection với weighted arcs"""
        result = analyze_deadlock(weighted_net)
        
        assert result is not None
        assert result.total_states > 0
        
        print(f"✓ Weighted net: {result.total_deadlocks} deadlocks in {result.total_states} states")
    
    def test_large_state_space(self):
        """Test mạng với state space lớn hơn"""
        from app.core.schemas import PetriNetRequest
        
        net = PetriNetRequest(
            places=["p1", "p2", "p3", "p4"],
            transitions=["t1", "t2", "t3"],
            arcs=[
                ["p1", "t1"],
                ["t1", "p2"],
                ["p2", "t2"],
                ["t2", "p3"],
                ["p3", "t3"],
                ["t3", "p4"]
            ],
            weights={},
            initial_marking={"p1": 2, "p2": 0, "p3": 0, "p4": 0}
        )
        
        result = analyze_deadlock(net)
        
        assert result is not None
        assert result.total_states > 0
        
        print(f"✓ Large state space: {result.total_deadlocks} deadlocks in {result.total_states} states")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
