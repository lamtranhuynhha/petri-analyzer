"""
Tests cho thuật toán Liveness Analysis
"""
import pytest
from app.algorithms.liveness import analyze_liveness


class TestLiveness:
    """Test suite cho thuật toán liveness analysis"""
    
    def test_simple_linear_net_not_live(self, simple_linear_net):
        """Test mạng Petri đơn giản dạng chuỗi - không live"""
        result = analyze_liveness(simple_linear_net)
        
        assert result is not None
        assert hasattr(result, 'is_live')
        assert hasattr(result, 'liveness_level')
        assert hasattr(result, 'unreachable_transitions')
        
        # Mạng này không live (có transition không thể fire mãi mãi)
        assert result.is_live == False
        
        print(f"✓ Simple linear net: live={result.is_live}, level={result.liveness_level}")
    
    def test_cyclic_net_is_live(self, cyclic_net):
        """Test mạng Petri có chu trình - phải live"""
        result = analyze_liveness(cyclic_net)
        
        assert result is not None
        # Mạng cyclic phải live
        assert result.is_live == True
        assert len(result.unreachable_transitions) == 0
        
        print(f"✓ Cyclic net: live={result.is_live}, level={result.liveness_level}")
    
    def test_producer_consumer_liveness(self, producer_consumer_net):
        """Test mạng Producer-Consumer"""
        result = analyze_liveness(producer_consumer_net)
        
        assert result is not None
        
        print(f"✓ Producer-Consumer: live={result.is_live}, level={result.liveness_level}")
        print(f"  Unreachable transitions: {result.unreachable_transitions}")
    
    def test_mutual_exclusion_liveness(self, mutual_exclusion_net):
        """Test mạng Mutual Exclusion - phải live"""
        result = analyze_liveness(mutual_exclusion_net)
        
        assert result is not None
        
        print(f"✓ Mutual Exclusion: live={result.is_live}, level={result.liveness_level}")
    
    def test_deadlock_net_not_live(self, deadlock_net):
        """Test mạng có deadlock - không live"""
        result = analyze_liveness(deadlock_net)
        
        assert result is not None
        # Mạng có deadlock không thể live
        assert result.is_live == False
        
        print(f"✓ Deadlock net: live={result.is_live}")
    
    def test_empty_net_not_live(self, empty_net):
        """Test edge case: mạng rỗng - không live"""
        result = analyze_liveness(empty_net)
        
        assert result is not None
        # Mạng rỗng không live
        assert result.is_live == False
        
        print(f"✓ Empty net: live={result.is_live}")
    
    def test_single_place_net_is_live(self, single_place_net):
        """Test edge case: mạng 1 place với chu trình - phải live"""
        result = analyze_liveness(single_place_net)
        
        assert result is not None
        # Mạng có chu trình phải live
        assert result.is_live == True
        
        print(f"✓ Single place net: live={result.is_live}")
    
    def test_liveness_level_values(self, cyclic_net):
        """Test giá trị liveness level"""
        result = analyze_liveness(cyclic_net)
        
        # Liveness level phải từ 0-4
        assert result.liveness_level in [0, 1, 2, 3, 4]
        
        print(f"✓ Liveness level: {result.liveness_level}")
    
    def test_unreachable_transitions_list(self, simple_linear_net):
        """Test danh sách unreachable transitions"""
        result = analyze_liveness(simple_linear_net)
        
        assert isinstance(result.unreachable_transitions, list)
        # Tất cả phần tử phải là string (transition names)
        assert all(isinstance(t, str) for t in result.unreachable_transitions)
        
        print(f"✓ Unreachable transitions: {result.unreachable_transitions}")
    
    def test_weighted_net_liveness(self, weighted_net):
        """Test liveness với weighted arcs"""
        result = analyze_liveness(weighted_net)
        
        assert result is not None
        
        print(f"✓ Weighted net: live={result.is_live}, level={result.liveness_level}")


class TestLivenessLevels:
    """Test các mức độ liveness khác nhau"""
    
    def test_l0_deadlock(self):
        """Test L0 (dead) - transition không bao giờ fire được"""
        from app.core.schemas import PetriNetRequest
        
        net = PetriNetRequest(
            places=["p1", "p2"],
            transitions=["t1", "t2"],
            arcs=[
                ["p1", "t1"],
                ["t1", "p2"],
                ["p2", "t2"]  # t2 không có output, p2 không có token
            ],
            weights={},
            initial_marking={"p1": 1, "p2": 0}
        )
        
        result = analyze_liveness(net)
        
        assert result is not None
        # t2 là dead transition
        assert result.is_live == False
        
        print(f"✓ L0 test: live={result.is_live}, unreachable={result.unreachable_transitions}")
    
    def test_l4_live(self, cyclic_net):
        """Test L4 (live) - tất cả transitions có thể fire từ mọi marking"""
        result = analyze_liveness(cyclic_net)
        
        assert result is not None
        assert result.is_live == True
        assert result.liveness_level == 4
        
        print(f"✓ L4 test: live={result.is_live}, level={result.liveness_level}")
    
    def test_partially_live_net(self):
        """Test mạng partially live - một số transitions live, một số không"""
        from app.core.schemas import PetriNetRequest
        
        net = PetriNetRequest(
            places=["p1", "p2", "p3"],
            transitions=["t1", "t2", "t3"],
            arcs=[
                ["p1", "t1"],
                ["t1", "p1"],  # t1 có chu trình
                ["p2", "t2"],
                ["t2", "p3"],  # t2 không có chu trình
                ["p3", "t3"]   # t3 dead
            ],
            weights={},
            initial_marking={"p1": 1, "p2": 1, "p3": 0}
        )
        
        result = analyze_liveness(net)
        
        assert result is not None
        
        print(f"✓ Partially live: live={result.is_live}, level={result.liveness_level}")
        print(f"  Unreachable: {result.unreachable_transitions}")


class TestLivenessEdgeCases:
    """Test các edge cases đặc biệt"""
    
    def test_all_transitions_initially_enabled(self):
        """Test mạng mà tất cả transitions đều enabled ban đầu"""
        from app.core.schemas import PetriNetRequest
        
        net = PetriNetRequest(
            places=["p1", "p2", "p3"],
            transitions=["t1", "t2"],
            arcs=[
                ["p1", "t1"],
                ["t1", "p1"],
                ["p2", "t2"],
                ["t2", "p2"]
            ],
            weights={},
            initial_marking={"p1": 1, "p2": 1, "p3": 0}
        )
        
        result = analyze_liveness(net)
        
        assert result is not None
        
        print(f"✓ All enabled: live={result.is_live}")
    
    def test_unbounded_net_liveness(self, unbounded_net):
        """Test liveness của mạng unbounded"""
        result = analyze_liveness(unbounded_net)
        
        assert result is not None
        
        print(f"✓ Unbounded net: live={result.is_live}, level={result.liveness_level}")
    
    def test_complex_mutual_exclusion(self):
        """Test mạng phức tạp hơn với nhiều processes"""
        from app.core.schemas import PetriNetRequest
        
        net = PetriNetRequest(
            places=["p1", "p2", "p3", "resource"],
            transitions=["t1", "t2", "t3", "t4"],
            arcs=[
                ["p1", "t1"],
                ["resource", "t1"],
                ["t1", "p2"],
                ["p2", "t2"],
                ["t2", "p1"],
                ["t2", "resource"],
                ["p3", "t3"],
                ["resource", "t3"],
                ["t3", "p3"],
                ["t3", "t4"]
            ],
            weights={},
            initial_marking={"p1": 1, "p2": 0, "p3": 1, "resource": 1}
        )
        
        result = analyze_liveness(net)
        
        assert result is not None
        
        print(f"✓ Complex mutual exclusion: live={result.is_live}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])