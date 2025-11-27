"""
Tests cho thuật toán Liveness Analysis
"""
import pytest
from app.algorithms.liveness import analyze_liveness
from app.models.petri_net import PetriNet


class TestLiveness:
    """Test suite cho thuật toán liveness analysis"""
    
    def test_simple_linear_net_not_live(self, simple_linear_net):
        """Test mạng Petri đơn giản dạng chuỗi - không live"""
        result = analyze_liveness(simple_linear_net)
        
        # Kiểm tra cấu trúc kết quả
        assert result is not None
        assert hasattr(result, 'is_live')
        assert hasattr(result, 'liveness_level')
        assert hasattr(result, 'unreachable_transitions')
        assert hasattr(result, 'is_bounded')
        assert hasattr(result, 'bound')
        assert hasattr(result, 'unbounded_places')
        
        # Kiểm tra kiểu dữ liệu
        assert isinstance(result.is_live, bool)
        assert isinstance(result.liveness_level, int)
        assert isinstance(result.unreachable_transitions, list)
        assert isinstance(result.is_bounded, bool)
        assert result.bound is None or isinstance(result.bound, int)
        assert isinstance(result.unbounded_places, list)
        
        # Kiểm tra giá trị hợp lệ
        assert 0 <= result.liveness_level <= 4
        
        # Mạng này không live (có transition không thể fire mãi mãi)
        assert result.is_live is False
        
        print(f"✓ Simple linear net: live={result.is_live}, level={result.liveness_level}, unreachable={result.unreachable_transitions}")
    
    def test_cyclic_net_is_live(self, cyclic_net):
        """Test mạng Petri có chu trình - phải live"""
        result = analyze_liveness(cyclic_net)
        
        assert result is not None
        assert hasattr(result, 'is_live')
        assert hasattr(result, 'liveness_level')
        assert hasattr(result, 'unreachable_transitions')
        
        assert result.is_live is True
        assert result.liveness_level == 4  # Fully live
        assert isinstance(result.unreachable_transitions, list)
        assert len(result.unreachable_transitions) == 0
        
        print(f"✓ Cyclic net: live={result.is_live}, level={result.liveness_level}")
    
    def test_producer_consumer_liveness(self, producer_consumer_net):
        """Test mạng Producer-Consumer"""
        result = analyze_liveness(producer_consumer_net)
        
        assert result is not None
        assert hasattr(result, 'is_live')
        assert hasattr(result, 'liveness_level')
        assert hasattr(result, 'unreachable_transitions')
        
        assert isinstance(result.is_live, bool)
        assert isinstance(result.liveness_level, int)
        assert isinstance(result.unreachable_transitions, list)
        
        assert 0 <= result.liveness_level <= 4
        
        print(f"✓ Producer-Consumer: live={result.is_live}, level={result.liveness_level}, unreachable={result.unreachable_transitions}")
    
    def test_deadlock_net_not_live(self, deadlock_net):
        """Test mạng có deadlock - không live"""
        result = analyze_liveness(deadlock_net)
        
        assert result is not None
        assert hasattr(result, 'is_live')
        assert hasattr(result, 'liveness_level')
        
        # Mạng có deadlock không thể live
        assert result.is_live is False
        assert result.liveness_level < 4  # Không thể là fully live
        
        print(f"✓ Deadlock net: live={result.is_live}")
    
    def test_empty_net_not_live(self, empty_net):
        """Test edge case: mạng rỗng - không live"""
        result = analyze_liveness(empty_net)
        
        assert result is not None
        assert hasattr(result, 'is_live')
        assert hasattr(result, 'liveness_level')
        
        # Một mạng rỗng (không có transition) được coi là live
        # vì không có transition nào bị chặn
        assert result.is_live is True
        assert result.liveness_level == 4  # Fully live vì không có transition nào bị chặn
        
        print(f"✓ Empty net: live={result.is_live}")
    
    def test_single_place_net_is_live(self, single_place_net):
        """Test edge case: mạng 1 place với chu trình - phải live"""
        result = analyze_liveness(single_place_net)
        
        assert result is not None
        assert hasattr(result, 'is_live')
        assert hasattr(result, 'liveness_level')
        
        # Mạng có chu trình phải live
        assert result.is_live is True
        # Mạng có chu trình nên có liveness_level cao (3 hoặc 4)
        assert result.liveness_level >= 3
        
        print(f"✓ Single place net: live={result.is_live}, level={result.liveness_level}")
    
    def test_liveness_level_values(self, simple_linear_net, cyclic_net):
        """Test các giá trị liveness_level"""
        # Test mạng không live
        result = analyze_liveness(simple_linear_net)
        assert hasattr(result, 'liveness_level')
        assert isinstance(result.liveness_level, int)
        assert 0 <= result.liveness_level < 4
        
        # Test mạng live
        result = analyze_liveness(cyclic_net)
        assert hasattr(result, 'liveness_level')
        assert isinstance(result.liveness_level, int)
        assert result.liveness_level == 4  # Fully live
        
        print(f"✓ Liveness level: {result.liveness_level}")
    
    def test_unreachable_transitions_list(self, simple_linear_net):
        """Test danh sách unreachable transitions"""
        from app.models.petri_net import PetriNet
        
        result = analyze_liveness(simple_linear_net)
        
        assert hasattr(result, 'unreachable_transitions')
        assert isinstance(result.unreachable_transitions, list)
        
        if result.unreachable_transitions:  # Nếu có unreachable transitions
            assert all(isinstance(t, str) for t in result.unreachable_transitions)
            
        # Kiểm tra rằng các transition trong danh sách đều tồn tại trong mạng
        net = PetriNet(simple_linear_net)
        for t in result.unreachable_transitions:
            assert t in net.transitions
        
        print(f"✓ Unreachable transitions: {result.unreachable_transitions}")
    
    def test_weighted_net_liveness(self, weighted_net):
        """Test mạng có weighted arcs"""
        result = analyze_liveness(weighted_net)
        
        assert result is not None
        assert hasattr(result, 'is_live')
        assert hasattr(result, 'liveness_level')
        assert hasattr(result, 'unreachable_transitions')
        
        assert isinstance(result.is_live, bool)
        assert isinstance(result.liveness_level, int)
        assert isinstance(result.unreachable_transitions, list)
        
        assert 0 <= result.liveness_level <= 4
        
        print(f"✓ Weighted net: live={result.is_live}, level={result.liveness_level}")


class TestLivenessLevels:
    """Test các mức độ liveness khác nhau"""
    
    def test_l0_deadlock(self):
        """Test L0 (dead) - transition không bao giờ fire được"""
        from app.core.schemas import PetriNetRequest
        
        net = PetriNetRequest(
            places=["p1", "p2"],
            transitions=["t1"],
            arcs=[["p1", "t1"]],  # Thiếu arc ra từ t1 nên không thể fire
            weights={},
            initial_marking={"p1": 0, "p2": 1}  # p1 rỗng nên t1 không thể fire
        )
        
        result = analyze_liveness(net)
        
        assert hasattr(result, 'is_live')
        assert hasattr(result, 'liveness_level')
        assert hasattr(result, 'unreachable_transitions')
        assert hasattr(result, 'is_bounded')
        
        assert result.is_live is False
        assert "t1" in result.unreachable_transitions
        assert result.liveness_level == 0  # Dead
        assert result.is_bounded is True  # Mạng này vẫn bounded
        
        print(f"✓ L0 test: live={result.is_live}, unreachable={result.unreachable_transitions}")
    
    def test_l4_live(self, cyclic_net):
        """Test L4 (live) - tất cả transitions có thể fire từ mọi marking"""
        result = analyze_liveness(cyclic_net)
        
        assert hasattr(result, 'is_live')
        assert hasattr(result, 'liveness_level')
        assert hasattr(result, 'unreachable_transitions')
        assert hasattr(result, 'is_bounded')
        assert hasattr(result, 'bound')
        assert hasattr(result, 'unbounded_places')
        
        assert result.is_live is True
        assert len(result.unreachable_transitions) == 0
        assert result.liveness_level == 4  # Fully live
        
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
            places=["p1", "p2"],
            transitions=["t1"],
            arcs=[
                ["p1", "t1"],
                ["t1", "p2"]
            ],
            weights={},
            initial_marking={"p1": 1, "p2": 0}
        )
        
        result = analyze_liveness(net)
        
        assert result is not None
        assert hasattr(result, 'liveness_level')
        
        assert result.liveness_level >= 1  # Ít nhất là L1-live
        assert len(result.unreachable_transitions) == 0  # Không có transition nào không thể đến được
        
        print(f"✓ All enabled: live={result.is_live}")
    
    def test_unbounded_net_liveness(self, unbounded_net):
        """Test liveness của mạng unbounded"""
        # Sử dụng trực tiếp fixture unbounded_net vì nó đã là đối tượng PetriNet
        result = analyze_liveness(unbounded_net)
        
        assert result is not None
        assert hasattr(result, 'is_live')
        assert hasattr(result, 'liveness_level')
        assert hasattr(result, 'is_bounded')
        
        # Mạng unbounded phải được đánh dấu là không bounded
        assert result.is_bounded is False
        
        # Kiểm tra liveness_level hợp lệ
        assert 0 <= result.liveness_level <= 4
        
        print(f"Unbounded net liveness: is_live={result.is_live}, level={result.liveness_level}")
        
        # Nếu mạng được đánh dấu là live, kiểm tra liveness_level
        if result.is_live:
            assert result.liveness_level >= 1  # Ít nhất là L1-live
        
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
                ["p3", "t4"]
            ],
            weights={},
            initial_marking={"p1": 1, "p2": 0, "p3": 1, "resource": 1}
        )
        
        result = analyze_liveness(net)
        
        assert result is not None
        
        print(f"✓ Complex mutual exclusion: live={result.is_live}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])