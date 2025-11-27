"""
Tests cho thuật toán Boundedness Analysis
"""
import pytest
from app.algorithms.boundedness import analyze_boundedness


class TestBoundedness:
    """Test suite cho thuật toán boundedness"""
    
    def test_simple_linear_net_bounded(self, simple_linear_net):
        """Test mạng Petri đơn giản dạng chuỗi - phải bounded"""
        result = analyze_boundedness(simple_linear_net)
        
        assert result is not None
        assert hasattr(result, 'is_bounded')
        assert hasattr(result, 'bound')
        assert hasattr(result, 'unbounded_places')
        
        # Mạng này phải bounded
        assert result.is_bounded == True
        assert result.bound is not None
        assert len(result.unbounded_places) == 0
        
        print(f"✓ Simple linear net: bounded={result.is_bounded}, bound={result.bound}")
    
    def test_cyclic_net_bounded(self, cyclic_net):
        """Test mạng Petri có chu trình - phải bounded"""
        result = analyze_boundedness(cyclic_net)
        
        assert result is not None
        assert result.is_bounded == True
        assert len(result.unbounded_places) == 0
        
        print(f"✓ Cyclic net: bounded={result.is_bounded}, bound={result.bound}")
    
    def test_unbounded_net(self, unbounded_net):
        """Test mạng Petri unbounded - phải phát hiện unbounded"""
        result = analyze_boundedness(unbounded_net)
        
        assert result is not None
        assert hasattr(result, 'is_bounded')
        
        # Mạng này phải unbounded
        assert result.is_bounded == False
        assert len(result.unbounded_places) > 0
        
        print(f"✓ Unbounded net: bounded={result.is_bounded}")
        print(f"  Unbounded places: {result.unbounded_places}")
    
    def test_producer_consumer_bounded(self, producer_consumer_net):
        """Test mạng Producer-Consumer - phải bounded"""
        result = analyze_boundedness(producer_consumer_net)
        
        assert result is not None
        assert result.is_bounded == True
        
        print(f"✓ Producer-Consumer: bounded={result.is_bounded}, bound={result.bound}")
    
    def test_weighted_net_bounded(self, weighted_net):
        """Test mạng có weighted arcs"""
        result = analyze_boundedness(weighted_net)
        
        assert result is not None
        assert hasattr(result, 'is_bounded')
        
        print(f"✓ Weighted net: bounded={result.is_bounded}, bound={result.bound}")
    
    def test_empty_net(self, empty_net):
        """Test edge case: mạng rỗng"""
        result = analyze_boundedness(empty_net)
        
        assert result is not None
        # Mạng rỗng phải bounded (không có transition nào fire được)
        assert result.is_bounded == True
        
        print(f"✓ Empty net: bounded={result.is_bounded}")
    
    def test_single_place_net(self, single_place_net):
        """Test edge case: mạng chỉ có 1 place và 1 transition"""
        result = analyze_boundedness(single_place_net)
        
        assert result is not None
        assert result.is_bounded == True
        
        print(f"✓ Single place net: bounded={result.is_bounded}, bound={result.bound}")
    
    def test_bound_value_correctness(self, simple_linear_net):
        """Test giá trị bound có đúng không"""
        result = analyze_boundedness(simple_linear_net)
        
        # Bound phải là số nguyên dương hoặc None (nếu unbounded)
        if result.is_bounded:
            assert isinstance(result.bound, int)
            assert result.bound > 0
        
        print(f"✓ Bound value check: bound={result.bound}")
    
    def test_unbounded_places_list(self, unbounded_net):
        """Test danh sách unbounded places có đúng không"""
        result = analyze_boundedness(unbounded_net)
        
        if not result.is_bounded:
            assert isinstance(result.unbounded_places, list)
            assert len(result.unbounded_places) > 0
            # Tất cả phần tử phải là string (place names)
            assert all(isinstance(p, str) for p in result.unbounded_places)
        
        print(f"✓ Unbounded places: {result.unbounded_places}")


class TestBoundednessEdgeCases:
    """Test các edge cases đặc biệt"""
    
    def test_all_places_empty_marking(self):
        """Test mạng với tất cả places có marking = 0"""
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
            initial_marking={"p1": 0, "p2": 0, "p3": 0}
        )
        
        result = analyze_boundedness(net)
        
        assert result is not None
        assert result.is_bounded == True
        
        print(f"✓ All empty marking: bounded={result.is_bounded}")
    
    def test_high_initial_marking(self):
        """Test mạng với initial marking lớn"""
        from app.core.schemas import PetriNetRequest
        
        net = PetriNetRequest(
            places=["p1", "p2"],
            transitions=["t1"],
            arcs=[
                ["p1", "t1"],
                ["t1", "p2"]
            ],
            weights={},
            initial_marking={"p1": 100, "p2": 0}
        )
        
        result = analyze_boundedness(net)
        
        assert result is not None
        assert result.is_bounded == True
        
        print(f"✓ High initial marking: bounded={result.is_bounded}, bound={result.bound}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
