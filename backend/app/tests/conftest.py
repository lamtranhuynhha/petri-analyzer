"""
Mẫu test cho tất cả tests
"""
import pytest
from app.core.schemas import PetriNetRequest


@pytest.fixture
def simple_linear_net():
    """
    Mạng Petri đơn giản dạng chuỗi: p1 -> t1 -> p2 -> t2 -> p3
    - Không có chu trình
    - Bounded
    - Có deadlock state cuối cùng
    """
    return PetriNetRequest(
        places=["p1", "p2", "p3"],
        transitions=["t1", "t2"],
        arcs=[
            ["p1", "t1"],
            ["t1", "p2"],
            ["p2", "t2"],
            ["t2", "p3"]
        ],
        weights={},
        initial_marking={"p1": 1, "p2": 0, "p3": 0}
    )


@pytest.fixture
def cyclic_net():
    """
    Mạng Petri có chu trình: p1 <-> t1 <-> p2 <-> t2 <-> p1
    - Có chu trình
    - Live
    - Bounded
    - Không có deadlock
    """
    return PetriNetRequest(
        places=["p1", "p2"],
        transitions=["t1", "t2"],
        arcs=[
            ["p1", "t1"],
            ["t1", "p2"],
            ["p2", "t2"],
            ["t2", "p1"]
        ],
        weights={},
        initial_marking={"p1": 1, "p2": 0}
    )


@pytest.fixture
def producer_consumer_net():
    """
    Mạng Petri Producer-Consumer pattern
    - Producer: p1 -> t1 -> buffer
    - Consumer: buffer -> t2 -> p2
    """
    return PetriNetRequest(
        places=["producer", "buffer", "consumer"],
        transitions=["t_produce", "t_consume"],
        arcs=[
            ["producer", "t_produce"],
            ["t_produce", "buffer"],
            ["buffer", "t_consume"],
            ["t_consume", "consumer"]
        ],
        weights={},
        initial_marking={"producer": 2, "buffer": 0, "consumer": 0}
    )


@pytest.fixture
def unbounded_net():
    """
    Mạng Petri unbounded: t1 tạo token vô hạn tại p1
    - p1 -> t1 -> p1, p2
    - Token tại p1 tăng vô hạn
    """
    return PetriNetRequest(
        places=["p1", "p2"],
        transitions=["t1"],
        arcs=[
            ["p1", "t1"],
            ["t1", "p1"],
            ["t1", "p2"]
        ],
        weights={},
        initial_marking={"p1": 1, "p2": 0}
    )


@pytest.fixture
def deadlock_net():
    """
    Mạng Petri có nhiều deadlock states
    - Two transitions cạnh tranh resource
    """
    return PetriNetRequest(
        places=["p1", "p2", "p3"],
        transitions=["t1", "t2"],
        arcs=[
            ["p1", "t1"],
            ["t1", "p3"],
            ["p2", "t2"],
            ["t2", "p3"]
        ],
        weights={},
        initial_marking={"p1": 1, "p2": 1, "p3": 0}
    )
    

@pytest.fixture
def weighted_net():
    """
    Mạng Petri có weighted arcs
    - Test khả năng xử lý trọng số khác nhau
    """
    return PetriNetRequest(
        places=["p1", "p2", "p3"],
        transitions=["t1", "t2"],
        arcs=[
            ["p1", "t1"],
            ["t1", "p2"],
            ["p2", "t2"],
            ["t2", "p3"]
        ],
        weights={
            "p1->t1": 2,  # t1 cần 2 token từ p1
            "t1->p2": 3,  # t1 tạo 3 token vào p2
            "p2->t2": 2   # t2 cần 2 token từ p2
        },
        initial_marking={"p1": 4, "p2": 0, "p3": 0}
    )


@pytest.fixture
def empty_net():
    """
    Mạng Petri rỗng - edge case test
    """
    return PetriNetRequest(
        places=["p1"],
        transitions=[],
        arcs=[],
        weights={},
        initial_marking={"p1": 0}
    )


@pytest.fixture
def single_place_net():
    """
    Mạng Petri chỉ có 1 place, 1 transition
    """
    return PetriNetRequest(
        places=["p1"],
        transitions=["t1"],
        arcs=[
            ["p1", "t1"],
            ["t1", "p1"]
        ],
        weights={},
        initial_marking={"p1": 1}
    )
