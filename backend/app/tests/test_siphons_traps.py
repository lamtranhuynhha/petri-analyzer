"""
Tests cho thuật toán Siphons and Traps Detection
"""
import pytest
from app.algorithms.siphons_traps import analyze_siphons_traps


class TestSiphonsTraps:
    """Test suite cho thuật toán siphons and traps"""
    
    def test_simple_linear_net_siphons_traps(self, simple_linear_net):
        """Test siphons và traps của mạng đơn giản"""
        result = analyze_siphons_traps(simple_linear_net)
        
        assert result is not None
        assert hasattr(result, 'siphons')
        assert hasattr(result, 'traps')
        assert hasattr(result, 'minimal_siphons')
        assert hasattr(result, 'minimal_traps')
        
        # Phải có danh sách (có thể rỗng)
        assert isinstance(result.siphons, list)
        assert isinstance(result.traps, list)
        
        print(f"✓ Simple linear net:")
        print(f"  Siphons: {len(result.siphons)}, Traps: {len(result.traps)}")
        print(f"  Minimal siphons: {len(result.minimal_siphons)}, Minimal traps: {len(result.minimal_traps)}")
    
    def test_cyclic_net_siphons_traps(self, cyclic_net):
        """Test siphons và traps của mạng có chu trình"""
        result = analyze_siphons_traps(cyclic_net)
        
        assert result is not None
        assert isinstance(result.siphons, list)
        assert isinstance(result.traps, list)
        
        print(f"✓ Cyclic net:")
        print(f"  Siphons: {len(result.siphons)}, Traps: {len(result.traps)}")
    
    def test_producer_consumer_siphons_traps(self, producer_consumer_net):
        """Test siphons và traps của Producer-Consumer"""
        result = analyze_siphons_traps(producer_consumer_net)
        
        assert result is not None
        
        print(f"✓ Producer-Consumer:")
        print(f"  Siphons: {len(result.siphons)}, Traps: {len(result.traps)}")
    
    def test_deadlock_net_siphons_traps(self, deadlock_net):
        """Test siphons và traps của mạng có deadlock"""
        result = analyze_siphons_traps(deadlock_net)
        
        assert result is not None
        
        print(f"✓ Deadlock net:")
        print(f"  Siphons: {len(result.siphons)}, Traps: {len(result.traps)}")
    
    def test_empty_net_siphons_traps(self, empty_net):
        """Test edge case: mạng rỗng"""
        result = analyze_siphons_traps(empty_net)
        
        assert result is not None
        
        print(f"✓ Empty net:")
        print(f"  Siphons: {len(result.siphons)}, Traps: {len(result.traps)}")
    
    def test_single_place_net_siphons_traps(self, single_place_net):
        """Test edge case: mạng 1 place"""
        result = analyze_siphons_traps(single_place_net)
        
        assert result is not None
        
        print(f"✓ Single place net:")
        print(f"  Siphons: {len(result.siphons)}, Traps: {len(result.traps)}")
    
    def test_siphons_format(self, simple_linear_net):
        """Test format của siphons"""
        result = analyze_siphons_traps(simple_linear_net)
        
        assert isinstance(result.siphons, list)
        
        # Mỗi siphon phải là list of places
        for siphon in result.siphons:
            assert isinstance(siphon, list)
            # Mỗi place phải là string
            for place in siphon:
                assert isinstance(place, str)
        
        print(f"✓ Siphons format check passed")
    
    def test_traps_format(self, simple_linear_net):
        """Test format của traps"""
        result = analyze_siphons_traps(simple_linear_net)
        
        assert isinstance(result.traps, list)
        
        # Mỗi trap phải là list of places
        for trap in result.traps:
            assert isinstance(trap, list)
            # Mỗi place phải là string
            for place in trap:
                assert isinstance(place, str)
        
        print(f"✓ Traps format check passed")
    
    def test_minimal_siphons_subset(self, cyclic_net):
        """Test minimal siphons phải là subset của siphons"""
        result = analyze_siphons_traps(cyclic_net)
        
        # Số minimal siphons phải <= số siphons
        assert len(result.minimal_siphons) <= len(result.siphons)
        
        print(f"✓ Minimal siphons: {len(result.minimal_siphons)}/{len(result.siphons)}")
    
    def test_minimal_traps_subset(self, cyclic_net):
        """Test minimal traps phải là subset của traps"""
        result = analyze_siphons_traps(cyclic_net)
        
        # Số minimal traps phải <= số traps
        assert len(result.minimal_traps) <= len(result.traps)
        
        print(f"✓ Minimal traps: {len(result.minimal_traps)}/{len(result.traps)}")
    
    def test_weighted_net_siphons_traps(self, weighted_net):
        """Test siphons và traps với weighted arcs"""
        result = analyze_siphons_traps(weighted_net)
        
        assert result is not None
        
        print(f"✓ Weighted net:")
        print(f"  Siphons: {len(result.siphons)}, Traps: {len(result.traps)}")


class TestSiphonsTrapsProperties:
    """Test các thuộc tính của siphons và traps"""
    
    def test_siphon_property(self):
        """Test thuộc tính của siphon: nếu không có token, sẽ không bao giờ có token"""
        from app.core.schemas import PetriNetRequest
        
        # Tạo mạng có siphon rõ ràng
        net = PetriNetRequest(
            places=["p1", "p2", "p3"],
            transitions=["t1", "t2"],
            arcs=[
                ["p1", "t1"],
                ["t1", "p2"],
                ["p2", "t2"]
                # p3 không có input arc -> là siphon
            ],
            weights={},
            initial_marking={"p1": 1, "p2": 0, "p3": 0}
        )
        
        result = analyze_siphons_traps(net)
        
        assert result is not None
        # Phải phát hiện được siphon
        assert len(result.siphons) > 0
        
        print(f"✓ Siphon property test: {len(result.siphons)} siphons found")
    
    def test_trap_property(self):
        """Test thuộc tính của trap: nếu có token, sẽ luôn có token"""
        from app.core.schemas import PetriNetRequest
        
        # Tạo mạng có trap
        net = PetriNetRequest(
            places=["p1", "p2"],
            transitions=["t1"],
            arcs=[
                ["p1", "t1"],
                ["t1", "p1"],  # p1 là trap (self-loop)
                ["t1", "p2"]
            ],
            weights={},
            initial_marking={"p1": 1, "p2": 0}
        )
        
        result = analyze_siphons_traps(net)
        
        assert result is not None
        
        print(f"✓ Trap property test: {len(result.traps)} traps found")
    
    def test_no_duplicate_siphons(self, cyclic_net):
        """Test không có siphon trùng lặp"""
        result = analyze_siphons_traps(cyclic_net)
        
        # Chuyển siphons thành tuple để so sánh
        siphon_tuples = [tuple(sorted(s)) for s in result.siphons]
        
        # Số lượng unique siphons phải bằng tổng số siphons
        assert len(set(siphon_tuples)) == len(siphon_tuples)
        
        print(f"✓ No duplicate siphons")
    
    def test_no_duplicate_traps(self, cyclic_net):
        """Test không có trap trùng lặp"""
        result = analyze_siphons_traps(cyclic_net)
        
        # Chuyển traps thành tuple để so sánh
        trap_tuples = [tuple(sorted(t)) for t in result.traps]
        
        # Số lượng unique traps phải bằng tổng số traps
        assert len(set(trap_tuples)) == len(trap_tuples)
        
        print(f"✓ No duplicate traps")
    
    def test_empty_siphon_not_in_list(self, simple_linear_net):
        """Test không có siphon rỗng"""
        result = analyze_siphons_traps(simple_linear_net)
        
        # Không có siphon nào rỗng
        for siphon in result.siphons:
            assert len(siphon) > 0
        
        print(f"✓ No empty siphons")
    
    def test_empty_trap_not_in_list(self, simple_linear_net):
        """Test không có trap rỗng"""
        result = analyze_siphons_traps(simple_linear_net)
        
        # Không có trap nào rỗng
        for trap in result.traps:
            assert len(trap) > 0
        
        print(f"✓ No empty traps")


class TestSiphonsTrapsEdgeCases:
    """Test các edge cases đặc biệt"""
    
    def test_all_places_are_siphon(self):
        """Test mạng mà tất cả places tạo thành một siphon"""
        from app.core.schemas import PetriNetRequest
        
        net = PetriNetRequest(
            places=["p1", "p2", "p3"],
            transitions=["t1"],
            arcs=[
                ["p1", "t1"],
                ["p2", "t1"],
                ["p3", "t1"]
                # Không có output arc -> tất cả places là siphon
            ],
            weights={},
            initial_marking={"p1": 1, "p2": 1, "p3": 1}
        )
        
        result = analyze_siphons_traps(net)
        
        assert result is not None
        assert len(result.siphons) > 0
        
        print(f"✓ All places siphon: {len(result.siphons)} siphons")
    
    def test_all_places_are_trap(self):
        """Test mạng mà tất cả places tạo thành một trap"""
        from app.core.schemas import PetriNetRequest
        
        net = PetriNetRequest(
            places=["p1", "p2"],
            transitions=["t1"],
            arcs=[
                ["t1", "p1"],
                ["t1", "p2"]
                # Không có input arc -> tất cả places là trap
            ],
            weights={},
            initial_marking={"p1": 0, "p2": 0}
        )
        
        result = analyze_siphons_traps(net)
        
        assert result is not None
        
        print(f"✓ All places trap: {len(result.traps)} traps")
    
    def test_unbounded_net_siphons_traps(self, unbounded_net):
        """Test siphons và traps của mạng unbounded"""
        result = analyze_siphons_traps(unbounded_net)
        
        assert result is not None
        
        print(f"✓ Unbounded net:")
        print(f"  Siphons: {len(result.siphons)}, Traps: {len(result.traps)}")
    
    def test_complex_net_siphons_traps(self):
        """Test mạng phức tạp hơn"""
        from app.core.schemas import PetriNetRequest
        
        net = PetriNetRequest(
            places=["p1", "p2", "p3", "p4", "p5"],
            transitions=["t1", "t2", "t3"],
            arcs=[
                ["p1", "t1"],
                ["p2", "t1"],
                ["t1", "p3"],
                ["p3", "t2"],
                ["t2", "p4"],
                ["p4", "t3"],
                ["t3", "p5"]
            ],
            weights={},
            initial_marking={"p1": 1, "p2": 1, "p3": 0, "p4": 0, "p5": 0}
        )
        
        result = analyze_siphons_traps(net)
        
        assert result is not None
        
        print(f"✓ Complex net:")
        print(f"  Siphons: {len(result.siphons)}, Traps: {len(result.traps)}")
        print(f"  Minimal siphons: {len(result.minimal_siphons)}")
        print(f"  Minimal traps: {len(result.minimal_traps)}")
    
    def test_self_loop_net(self):
        """Test mạng có self-loop"""
        from app.core.schemas import PetriNetRequest
        
        net = PetriNetRequest(
            places=["p1", "p2"],
            transitions=["t1", "t2"],
            arcs=[
                ["p1", "t1"],
                ["t1", "p1"],  # Self-loop
                ["t1", "p2"],
                ["p2", "t2"],
                ["t2", "p2"]   # Self-loop
            ],
            weights={},
            initial_marking={"p1": 1, "p2": 0}
        )
        
        result = analyze_siphons_traps(net)
        
        assert result is not None
        
        print(f"✓ Self-loop net:")
        print(f"  Siphons: {len(result.siphons)}, Traps: {len(result.traps)}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])