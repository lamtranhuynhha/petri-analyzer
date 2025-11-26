"""
Tests cho thuật toán Reachability Graph
"""
import pytest
from app.algorithms.reachability import analyze_reachability


class TestReachability:
    """Test suite cho thuật toán reachability graph"""
    
    def test_simple_linear_net_reachability(self, simple_linear_net):
        """Test reachability graph của mạng đơn giản"""
        result = analyze_reachability(simple_linear_net, max_states=100)
        
        assert result is not None
        assert hasattr(result, 'states')
        assert hasattr(result, 'edges')
        assert hasattr(result, 'initial_marking')
        
        # Phải có ít nhất 1 state (initial state)
        assert len(result.states) > 0
        assert result.initial_marking is not None
        
        print(f"✓ Simple linear net: {len(result.states)} states, {len(result.edges)} edges")
    
    def test_cyclic_net_reachability(self, cyclic_net):
        """Test reachability graph của mạng có chu trình"""
        result = analyze_reachability(cyclic_net, max_states=50)
        
        assert result is not None
        assert len(result.states) > 0
        
        # Mạng cyclic phải có ít nhất 2 states
        assert len(result.states) >= 2
        
        print(f"✓ Cyclic net: {len(result.states)} states, {len(result.edges)} edges")
    
    def test_producer_consumer_reachability(self, producer_consumer_net):
        """Test reachability graph của Producer-Consumer"""
        result = analyze_reachability(producer_consumer_net, max_states=100)
        
        assert result is not None
        assert len(result.states) > 0
        
        print(f"✓ Producer-Consumer: {len(result.states)} states, {len(result.edges)} edges")
    
    def test_mutual_exclusion_reachability(self, mutual_exclusion_net):
        """Test reachability graph của Mutual Exclusion"""
        result = analyze_reachability(mutual_exclusion_net, max_states=100)
        
        assert result is not None
        assert len(result.states) > 0
        
        print(f"✓ Mutual Exclusion: {len(result.states)} states, {len(result.edges)} edges")
    
    def test_empty_net_single_state(self, empty_net):
        """Test edge case: mạng rỗng - chỉ có 1 state"""
        result = analyze_reachability(empty_net, max_states=10)
        
        assert result is not None
        # Mạng rỗng chỉ có initial state
        assert len(result.states) == 1
        assert len(result.edges) == 0
        
        print(f"✓ Empty net: {len(result.states)} state (expected 1)")
    
    def test_single_place_net_reachability(self, single_place_net):
        """Test edge case: mạng 1 place"""
        result = analyze_reachability(single_place_net, max_states=50)
        
        assert result is not None
        assert len(result.states) > 0
        
        print(f"✓ Single place net: {len(result.states)} states")
    
    def test_states_format(self, simple_linear_net):
        """Test format của states"""
        result = analyze_reachability(simple_linear_net, max_states=50)
        
        assert isinstance(result.states, list)
        
        # Mỗi state phải là dict
        for state in result.states:
            assert isinstance(state, dict)
            # Mỗi place phải có giá trị integer
            for place, tokens in state.items():
                assert isinstance(place, str)
                assert isinstance(tokens, int)
                assert tokens >= 0
        
        print(f"✓ States format check passed")
    
    def test_edges_format(self, cyclic_net):
        """Test format của edges"""
        result = analyze_reachability(cyclic_net, max_states=50)
        
        assert isinstance(result.edges, list)
        
        # Mỗi edge phải có source, target, transition
        for edge in result.edges:
            assert isinstance(edge, dict)
            assert 'source' in edge
            assert 'target' in edge
            assert 'transition' in edge
            
            # Source và target phải là dict (markings)
            assert isinstance(edge['source'], dict)
            assert isinstance(edge['target'], dict)
            assert isinstance(edge['transition'], str)
        
        print(f"✓ Edges format check passed")
    
    def test_max_states_limit(self, cyclic_net):
        """Test giới hạn max_states"""
        max_limit = 10
        result = analyze_reachability(cyclic_net, max_states=max_limit)
        
        assert result is not None
        # Số states không được vượt quá max_limit
        assert len(result.states) <= max_limit
        
        print(f"✓ Max states limit: {len(result.states)}/{max_limit}")
    
    def test_weighted_net_reachability(self, weighted_net):
        """Test reachability với weighted arcs"""
        result = analyze_reachability(weighted_net, max_states=100)
        
        assert result is not None
        assert len(result.states) > 0
        
        print(f"✓ Weighted net: {len(result.states)} states, {len(result.edges)} edges")


class TestReachabilityGraphProperties:
    """Test các thuộc tính của reachability graph"""
    
    def test_initial_marking_in_states(self, simple_linear_net):
        """Test initial marking phải có trong danh sách states"""
        result = analyze_reachability(simple_linear_net, max_states=50)
        
        # Initial marking phải là state đầu tiên
        assert result.initial_marking in result.states
        
        print(f"✓ Initial marking is in states")
    
    def test_edges_connect_valid_states(self, cyclic_net):
        """Test tất cả edges phải kết nối các states hợp lệ"""
        result = analyze_reachability(cyclic_net, max_states=50)
        
        for edge in result.edges:
            # Source và target phải có trong danh sách states
            assert edge['source'] in result.states
            assert edge['target'] in result.states
        
        print(f"✓ All edges connect valid states")
    
    def test_no_duplicate_states(self, simple_linear_net):
        """Test không có state trùng lặp"""
        result = analyze_reachability(simple_linear_net, max_states=50)
        
        # Chuyển states thành tuple để so sánh
        state_tuples = [tuple(sorted(s.items())) for s in result.states]
        
        # Số lượng unique states phải bằng tổng số states
        assert len(set(state_tuples)) == len(state_tuples)
        
        print(f"✓ No duplicate states")
    
    def test_reachability_from_deadlock(self, deadlock_net):
        """Test reachability graph của mạng có deadlock"""
        result = analyze_reachability(deadlock_net, max_states=100)
        
        assert result is not None
        assert len(result.states) > 0
        
        print(f"✓ Deadlock net reachability: {len(result.states)} states")


class TestReachabilityEdgeCases:
    """Test các edge cases đặc biệt"""
    
    def test_unbounded_net_limited_states(self, unbounded_net):
        """Test mạng unbounded với giới hạn states"""
        max_limit = 20
        result = analyze_reachability(unbounded_net, max_states=max_limit)
        
        assert result is not None
        # Phải dừng lại khi đạt max_limit
        assert len(result.states) <= max_limit
        
        print(f"✓ Unbounded net limited: {len(result.states)}/{max_limit} states")
    
    def test_large_initial_marking(self):
        """Test mạng với initial marking lớn"""
        from app.core.schemas import PetriNetRequest
        
        net = PetriNetRequest(
            places=["p1", "p2", "p3"],
            transitions=["t1", "t2"],
            arcs=[
                ["p1", "t1"],
                ["t1", "p2"],
                ["p2", "t2"],
                ["t2", "p3"]
            ],
            weights={},
            initial_marking={"p1": 10, "p2": 0, "p3": 0}
        )
        
        result = analyze_reachability(net, max_states=100)
        
        assert result is not None
        assert len(result.states) > 0
        
        print(f"✓ Large initial marking: {len(result.states)} states")
    
    def test_multiple_initial_tokens(self):
        """Test mạng với nhiều tokens ban đầu ở nhiều places"""
        from app.core.schemas import PetriNetRequest
        
        net = PetriNetRequest(
            places=["p1", "p2", "p3"],
            transitions=["t1", "t2"],
            arcs=[
                ["p1", "t1"],
                ["t1", "p3"],
                ["p2", "t2"],
                ["t2", "p3"]
            ],
            weights={},
            initial_marking={"p1": 2, "p2": 2, "p3": 0}
        )
        
        result = analyze_reachability(net, max_states=100)
        
        assert result is not None
        assert len(result.states) > 0
        
        print(f"✓ Multiple initial tokens: {len(result.states)} states")
    
    def test_complex_net_reachability(self):
        """Test mạng phức tạp hơn"""
        from app.core.schemas import PetriNetRequest
        
        net = PetriNetRequest(
            places=["p1", "p2", "p3", "p4", "p5"],
            transitions=["t1", "t2", "t3", "t4"],
            arcs=[
                ["p1", "t1"],
                ["t1", "p2"],
                ["p2", "t2"],
                ["t2", "p3"],
                ["p3", "t3"],
                ["t3", "p4"],
                ["p4", "t4"],
                ["t4", "p5"]
            ],
            weights={},
            initial_marking={"p1": 2, "p2": 0, "p3": 0, "p4": 0, "p5": 0}
        )
        
        result = analyze_reachability(net, max_states=200)
        
        assert result is not None
        assert len(result.states) > 0
        
        print(f"✓ Complex net: {len(result.states)} states, {len(result.edges)} edges")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])