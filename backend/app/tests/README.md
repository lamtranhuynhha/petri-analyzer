# Test Suite - Petri Net Analyzer

Hệ thống test đầy đủ cho tất cả thuật toán phân tích mạng Petri.

## 📁 Cấu trúc Tests

```
tests/
├── conftest.py                 # Fixtures chung (sample Petri nets)
├── test_algorithms.py          # Integration tests (test tất cả thuật toán cùng nhau)
├── test_boundedness.py         # Tests cho thuật toán Boundedness
├── test_deadlock.py            # Tests cho thuật toán Deadlock Detection
├── test_liveness.py            # Tests cho thuật toán Liveness Analysis
├── test_reachability.py        # Tests cho thuật toán Reachability Graph
├── test_siphons_traps.py       # Tests cho thuật toán Siphons & Traps
└── README.md                   # File này
```

## 🎯 Loại Tests

### 1. **Unit Tests** (Từng thuật toán riêng)
- `test_boundedness.py` 
- `test_deadlock.py` 
- `test_liveness.py` 
- `test_reachability.py` 
- `test_siphons_traps.py`

### 2. **Integration Tests** (Tất cả thuật toán)
- `test_algorithms.py` - Test tích hợp, consistency checks, performance tests

### 3. **Fixtures** (Test data)
- `conftest.py`

## 🚀 Cách chạy Tests

### Chạy TẤT CẢ tests
```bash
cd backend
pytest app/tests/ -v
```

### Chạy test cho TỪNG thuật toán
```bash
# Boundedness
pytest app/tests/test_boundedness.py -v

# Deadlock
pytest app/tests/test_deadlock.py -v

# Liveness
pytest app/tests/test_liveness.py -v

# Reachability
pytest app/tests/test_reachability.py -v

# Siphons & Traps
pytest app/tests/test_siphons_traps.py -v
```

### Chạy Integration Tests
```bash
pytest app/tests/test_algorithms.py -v
```

### Chạy với OUTPUT chi tiết
```bash
pytest app/tests/ -v -s
```

### Chạy test CỤ THỂ
```bash
# Chạy một test class
pytest app/tests/test_boundedness.py::TestBoundedness -v

# Chạy một test function
pytest app/tests/test_boundedness.py::TestBoundedness::test_simple_linear_net_bounded -v
```

## 📊 Test Coverage

Mỗi thuật toán được test với:
- ✅ **Basic functionality** - Chức năng cơ bản
- ✅ **Edge cases** - Các trường hợp đặc biệt
- ✅ **Format validation** - Kiểm tra format output
- ✅ **Consistency checks** - Kiểm tra tính nhất quán
- ✅ **Performance tests** - Kiểm tra hiệu năng

## 🧪 Sample Petri Nets (Fixtures)

### 1. `simple_linear_net`
Mạng đơn giản dạng chuỗi: `p1 -> t1 -> p2 -> t2 -> p3`
- Không có chu trình
- Bounded
- Có deadlock state

### 2. `cyclic_net`
Mạng có chu trình: `p1 <-> t1 <-> p2 <-> t2 <-> p1`
- Live
- Bounded
- Không có deadlock

### 3. `producer_consumer_net`
Pattern Producer-Consumer
- Producer: `p1 -> t1 -> buffer`
- Consumer: `buffer -> t2 -> p2`

### 4. `unbounded_net`
Mạng unbounded
- Token tại p1 tăng vô hạn

### 5. `deadlock_net`
Mạng có nhiều deadlock states

### 6. `weighted_net`
Mạng có weighted arcs

### 7. `empty_net`
Mạng rỗng (edge case)

### 8. `single_place_net`
Mạng chỉ có 1 place (edge case)

## 📈 Kết quả mong đợi

### Boundedness Tests
```
✓ Simple linear net: bounded=True, bound=1
✓ Cyclic net: bounded=True, bound=1
✓ Unbounded net: bounded=False
```

### Deadlock Tests
```
✓ Simple linear net: 1 deadlocks in 4 states
✓ Cyclic net: 0 deadlocks (expected 0)
```

### Liveness Tests
```
✓ Simple linear net: live=False, level=0
✓ Cyclic net: live=True, level=4
```

### Reachability Tests
```
✓ Simple linear net: 4 states, 3 edges
✓ Cyclic net: 2 states, 2 edges
```

### Siphons & Traps Tests
```
✓ Simple linear net: Siphons: X, Traps: Y
✓ Cyclic net: Siphons: X, Traps: Y
```

## ⚡ Performance Benchmarks

Thời gian chạy mong đợi (trên máy trung bình):
- **Boundedness**: < 0.5s per test
- **Deadlock**: < 0.5s per test
- **Liveness**: < 0.5s per test
- **Reachability**: < 1.0s per test
- **Siphons & Traps**: < 0.5s per test
- **All Integration Tests**: < 10s total

## Viết Test Mới

### Template cho test mới
```python
def test_new_feature(self, simple_linear_net):
    """Test mô tả"""
    result = analyze_algorithm(simple_linear_net)
    
    # Assertions
    assert result is not None
    assert hasattr(result, 'expected_attribute')
    
    # Print kết quả
    print(f"✓ Test passed: {result}")
```

## Tài liệu tham khảo

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)

## Checklist trước khi commit

- [ ] Tất cả tests pass: `pytest app/tests/ -v`
