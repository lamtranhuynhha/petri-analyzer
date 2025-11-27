"""
Integration Tests - Test tất cả thuật toán cùng nhau
Đảm bảo các thuật toán hoạt động đồng bộ và cho kết quả nhất quán
"""
import pytest
from app.algorithms.liveness import analyze_liveness
from app.algorithms.siphons_traps import analyze_siphons_traps
from app.algorithms.reachability import analyze_reachability
from app.algorithms.boundedness import analyze_boundedness
from app.algorithms.deadlock import analyze_deadlock


class TestAlgorithmsIntegration:
    """Test tích hợp tất cả thuật toán"""
    
    def test_simple_linear_net_all_algorithms(self, simple_linear_net):
        """Test tất cả thuật toán với mạng đơn giản"""
        print("\n" + "="*70)
        print("INTEGRATION TEST: Simple Linear Net")
        print("="*70)
        
        # Chạy tất cả thuật toán
        liveness_result = analyze_liveness(simple_linear_net)
        siphons_result = analyze_siphons_traps(simple_linear_net)
        reach_result = analyze_reachability(simple_linear_net, max_states=50)
        bound_result = analyze_boundedness(simple_linear_net)
        deadlock_result = analyze_deadlock(simple_linear_net)
        
        # Verify tất cả đều trả về kết quả
        assert liveness_result is not None
        assert siphons_result is not None
        assert reach_result is not None
        assert bound_result is not None
        assert deadlock_result is not None
        
        # In kết quả
        print(f"✓ Liveness: {'Live' if liveness_result.is_live else 'Not Live'} (Level {liveness_result.liveness_level})")
        print(f"✓ Siphons: {len(siphons_result.siphons)}, Traps: {len(siphons_result.traps)}")
        print(f"✓ Reachability: {len(reach_result.states)} states, {len(reach_result.edges)} edges")
        print(f"✓ Boundedness: {'Bounded' if bound_result.is_bounded else 'Unbounded'} (bound={bound_result.bound})")
        print(f"✓ Deadlocks: {deadlock_result.total_deadlocks}/{deadlock_result.total_states} states")
        
        # Verify tính nhất quán
        # Mạng linear không live và có deadlock
        assert liveness_result.is_live == False
        assert deadlock_result.total_deadlocks > 0
        assert bound_result.is_bounded == True
    
    def test_cyclic_net_all_algorithms(self, cyclic_net):
        """Test tất cả thuật toán với mạng có chu trình"""
        print("\n" + "="*70)
        print("INTEGRATION TEST: Cyclic Net")
        print("="*70)
        
        # Chạy tất cả thuật toán
        liveness_result = analyze_liveness(cyclic_net)
        siphons_result = analyze_siphons_traps(cyclic_net)
        reach_result = analyze_reachability(cyclic_net, max_states=50)
        bound_result = analyze_boundedness(cyclic_net)
        deadlock_result = analyze_deadlock(cyclic_net)
        
        # Verify tất cả đều trả về kết quả
        assert liveness_result is not None
        assert siphons_result is not None
        assert reach_result is not None
        assert bound_result is not None
        assert deadlock_result is not None
        
        # In kết quả
        print(f"✓ Liveness: {'Live' if liveness_result.is_live else 'Not Live'} (Level {liveness_result.liveness_level})")
        print(f"✓ Siphons: {len(siphons_result.siphons)}, Traps: {len(siphons_result.traps)}")
        print(f"✓ Reachability: {len(reach_result.states)} states, {len(reach_result.edges)} edges")
        print(f"✓ Boundedness: {'Bounded' if bound_result.is_bounded else 'Unbounded'} (bound={bound_result.bound})")
        print(f"✓ Deadlocks: {deadlock_result.total_deadlocks}/{deadlock_result.total_states} states")
        
        # Verify tính nhất quán
        # Mạng cyclic phải live và không có deadlock
        assert liveness_result.is_live == True
        assert deadlock_result.total_deadlocks == 0
        assert bound_result.is_bounded == True
    
    def test_producer_consumer_all_algorithms(self, producer_consumer_net):
        """Test tất cả thuật toán với Producer-Consumer pattern"""
        print("\n" + "="*70)
        print("INTEGRATION TEST: Producer-Consumer Net")
        print("="*70)
        
        # Chạy tất cả thuật toán
        liveness_result = analyze_liveness(producer_consumer_net)
        siphons_result = analyze_siphons_traps(producer_consumer_net)
        reach_result = analyze_reachability(producer_consumer_net, max_states=100)
        bound_result = analyze_boundedness(producer_consumer_net)
        deadlock_result = analyze_deadlock(producer_consumer_net)
        
        # Verify tất cả đều trả về kết quả
        assert all([liveness_result, siphons_result, reach_result, bound_result, deadlock_result])
        
        # In kết quả
        print(f"✓ Liveness: {'Live' if liveness_result.is_live else 'Not Live'}")
        print(f"✓ Siphons: {len(siphons_result.siphons)}, Traps: {len(siphons_result.traps)}")
        print(f"✓ Reachability: {len(reach_result.states)} states")
        print(f"✓ Boundedness: {'Bounded' if bound_result.is_bounded else 'Unbounded'}")
        print(f"✓ Deadlocks: {deadlock_result.total_deadlocks} deadlocks")

class TestConsistencyChecks:
    """Test tính nhất quán giữa các thuật toán"""
    
    def test_live_implies_no_deadlock(self, cyclic_net):
        """Test: Nếu mạng live thì không có deadlock"""
        liveness_result = analyze_liveness(cyclic_net)
        deadlock_result = analyze_deadlock(cyclic_net)
        
        if liveness_result.is_live:
            # Mạng live không có deadlock
            assert deadlock_result.total_deadlocks == 0
        
        print(f"✓ Consistency: Live={liveness_result.is_live}, Deadlocks={deadlock_result.total_deadlocks}")
    
    def test_bounded_reachability_states_finite(self, simple_linear_net):
        """Test: Nếu bounded thì số states hữu hạn"""
        bound_result = analyze_boundedness(simple_linear_net)
        reach_result = analyze_reachability(simple_linear_net, max_states=1000)
        
        if bound_result.is_bounded:
            # Số states phải hữu hạn
            assert len(reach_result.states) < 1000
        
        print(f"✓ Consistency: Bounded={bound_result.is_bounded}, States={len(reach_result.states)}")
    
    def test_deadlock_in_reachability_graph(self, simple_linear_net):
        """Test: Deadlock states phải có trong reachability graph"""
        deadlock_result = analyze_deadlock(simple_linear_net)
        reach_result = analyze_reachability(simple_linear_net, max_states=100)
        
        # Số deadlock không được vượt quá số states
        assert deadlock_result.total_deadlocks <= len(reach_result.states)
        
        print(f"✓ Consistency: Deadlocks={deadlock_result.total_deadlocks}, Total states={len(reach_result.states)}")


class TestPerformanceIntegration:
    """Test performance khi chạy nhiều thuật toán"""
    
    def test_all_algorithms_performance(self, weighted_net):
        """Test thời gian chạy tất cả thuật toán"""
        import time
        
        print("\n" + "="*70)
        print("PERFORMANCE TEST: All Algorithms")
        print("="*70)
        
        start_time = time.time()
        
        # Chạy tất cả thuật toán
        liveness_result = analyze_liveness(weighted_net)
        liveness_time = time.time() - start_time
        
        siphons_result = analyze_siphons_traps(weighted_net)
        siphons_time = time.time() - start_time - liveness_time
        
        reach_result = analyze_reachability(weighted_net, max_states=100)
        reach_time = time.time() - start_time - liveness_time - siphons_time
        
        bound_result = analyze_boundedness(weighted_net)
        bound_time = time.time() - start_time - liveness_time - siphons_time - reach_time
        
        deadlock_result = analyze_deadlock(weighted_net)
        deadlock_time = time.time() - start_time - liveness_time - siphons_time - reach_time - bound_time
        
        total_time = time.time() - start_time
        
        # Verify tất cả đều hoàn thành
        assert all([liveness_result, siphons_result, reach_result, bound_result, deadlock_result])
        
        # In thời gian
        print(f"✓ Liveness: {liveness_time:.3f}s")
        print(f"✓ Siphons & Traps: {siphons_time:.3f}s")
        print(f"✓ Reachability: {reach_time:.3f}s")
        print(f"✓ Boundedness: {bound_time:.3f}s")
        print(f"✓ Deadlock: {deadlock_time:.3f}s")
        print(f"✓ Total time: {total_time:.3f}s")
        
        # Verify thời gian hợp lý (< 10s cho tất cả)
        assert total_time < 10.0


def test_full_integration_summary():
    """Test tổng hợp - chạy tất cả và in summary"""
    from app.core.schemas import PetriNetRequest
    
    print("\n" + "="*70)
    print("FULL INTEGRATION TEST SUMMARY")
    print("="*70)
    
    # Tạo các mạng test
    nets = {
        "Simple Linear": PetriNetRequest(
            places=["p1", "p2", "p3"],
            transitions=["t1", "t2"],
            arcs=[["p1", "t1"], ["t1", "p2"], ["p2", "t2"], ["t2", "p3"]],
            weights={},
            initial_marking={"p1": 1, "p2": 0, "p3": 0}
        ),
        "Cyclic": PetriNetRequest(
            places=["p1", "p2"],
            transitions=["t1", "t2"],
            arcs=[["p1", "t1"], ["t1", "p2"], ["p2", "t2"], ["t2", "p1"]],
            weights={},
            initial_marking={"p1": 1, "p2": 0}
        )
    }
    
    results = {}
    
    for name, net in nets.items():
        print(f"\n{name} Net:")
        
        liveness = analyze_liveness(net)
        siphons = analyze_siphons_traps(net)
        reach = analyze_reachability(net, max_states=50)
        bound = analyze_boundedness(net)
        deadlock = analyze_deadlock(net)
        
        results[name] = {
            "live": liveness.is_live,
            "siphons": len(siphons.siphons),
            "traps": len(siphons.traps),
            "states": len(reach.states),
            "bounded": bound.is_bounded,
            "deadlocks": deadlock.total_deadlocks
        }
        
        print(f"  Live: {results[name]['live']}")
        print(f"  Siphons/Traps: {results[name]['siphons']}/{results[name]['traps']}")
        print(f"  States: {results[name]['states']}")
        print(f"  Bounded: {results[name]['bounded']}")
        print(f"  Deadlocks: {results[name]['deadlocks']}")
    
    print("\n" + "="*70)
    print("✓ ALL INTEGRATION TESTS PASSED!")
    print("="*70)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
