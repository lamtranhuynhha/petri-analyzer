import React, { useCallback, useRef, useEffect, useMemo } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  MarkerType,
  applyNodeChanges,
  applyEdgeChanges,
  ConnectionLineType
} from 'reactflow';
import 'reactflow/dist/style.css';

import usePetriNetStore from '../hooks/usePetriNet';
import PlaceNode from './nodes/PlaceNode';
import TransitionNode from './nodes/TransitionNode';
import ArcEdge from './edges/ArcEdge';

// Hàm helper để tạo Label tự động tăng (p1, p2, t1, t2...)
const generateNextLabel = (prefix, elements) => {
  let maxIndex = 0;
  
  elements.forEach(el => {
    // Kiểm tra xem label hiện tại có bắt đầu bằng prefix không (ví dụ "p1" bắt đầu bằng "p")
    const label = el.label || '';
    if (label.startsWith(prefix)) {
      // Lấy phần số phía sau (ví dụ "p12" -> 12)
      const numberPart = parseInt(label.substring(prefix.length));
      if (!isNaN(numberPart) && numberPart > maxIndex) {
        maxIndex = numberPart;
      }
    }
  });

  return `${prefix}${maxIndex + 1}`;
};

const CanvasEditor = () => {
  const {
    selectedTool,
    places,
    transitions,
    arcs,
    addPlace,
    addTransition,
    addArc,
    updatePlace,
    updateTransition,
    setSelectedElement,
    deleteArc,
    deletePlace,
    deleteTransition
  } = usePetriNetStore();
  
  const reactFlowWrapper = useRef(null);
  const [nodes, setNodes] = useNodesState([]);
  const [edges, setEdges] = useEdgesState([]);
  const [reactFlowInstance, setReactFlowInstance] = React.useState(null);

  // ... (Giữ nguyên phần nodeTypes, edgeTypes, useEffect sync data như câu trả lời trước) ...
  const nodeTypes = useMemo(() => ({
    place: PlaceNode,
    transition: TransitionNode,
  }), []);

  const edgeTypes = useMemo(() => ({
    arc: ArcEdge,
  }), []);

  // Sync Store -> React Flow
  useEffect(() => {
    const newNodes = [
      ...places.map((p) => ({
        id: p.id,
        type: 'place',
        position: p.position || { x: 0, y: 0 },
        data: { label: p.label, tokens: p.tokens },
      })),
      ...transitions.map((t) => ({
        id: t.id,
        type: 'transition',
        position: t.position || { x: 0, y: 0 },
        data: { label: t.label, livenessLevel: t.livenessLevel },
      })),
    ];

    if (JSON.stringify(newNodes.map(n => n.id)) !== JSON.stringify(nodes.map(n => n.id))) {
       setNodes(newNodes);
    } else {
       setNodes((nds) => nds.map(node => {
         const source = newNodes.find(n => n.id === node.id);
         if (source) return { ...node, data: source.data };
         return node;
       }));
    }

    const newEdges = arcs.map((arc) => ({
      id: arc.id,
      source: arc.source,
      target: arc.target,
      type: 'arc',
      markerEnd: { type: MarkerType.ArrowClosed, width: 20, height: 20 },
      data: { weight: arc.weight },
    }));
    
    setEdges(newEdges);
  }, [places, transitions, arcs, setNodes, setEdges]);

  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    [setNodes]
  );

  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    [setEdges]
  );

  const onNodeDragStop = useCallback((event, node) => {
    if (node.type === 'place') {
      updatePlace(node.id, { position: node.position });
    } else if (node.type === 'transition') {
      updateTransition(node.id, { position: node.position });
    }
  }, [updatePlace, updateTransition]);

  const onConnect = useCallback((params) => {
    const { source, target } = params;
    const sourceNode = reactFlowInstance.getNode(source);
    const targetNode = reactFlowInstance.getNode(target);

    if (!sourceNode || !targetNode) return;
    if (sourceNode.type === targetNode.type) return;

    addArc({
      id: `a${Date.now()}`,
      source,
      target,
      weight: 1
    });
  }, [reactFlowInstance, addArc]);

  // --- PHẦN QUAN TRỌNG ĐÃ CHỈNH SỬA: Tạo ID và Label tuần tự ---
  const onPaneClick = useCallback((event) => {
    if (!reactFlowInstance || !selectedTool) return;
    
    if (selectedTool === 'select') {
      setSelectedElement(null);
      return;
    }

    const position = reactFlowInstance.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
    });

    if (selectedTool === 'place') {
      // 1. Tạo label tuần tự: p1, p2...
      const nextLabel = generateNextLabel('p', places);
      // 2. ID vẫn nên là unique để tránh lỗi React Flow, nhưng có thể dùng label làm ID nếu muốn
      // Ở đây tôi dùng label làm ID luôn cho đẹp, nhưng bạn phải đảm bảo không bao giờ trùng.
      // Để an toàn nhất: ID = label (nếu quản lý tốt) hoặc ID = `p-${Date.now()}`
      const id = nextLabel; 

      addPlace({
        id: id,
        label: nextLabel, // Hiển thị p1, p2
        tokens: 0,
        position,
      });
    } else if (selectedTool === 'transition') {
      // Tương tự cho transition: t1, t2...
      const nextLabel = generateNextLabel('t', transitions);
      const id = nextLabel;

      addTransition({
        id: id,
        label: nextLabel,
        position,
      });
    }
  }, [reactFlowInstance, selectedTool, addPlace, addTransition, setSelectedElement, places, transitions]);
  // -------------------------------------------------------------

  const onNodeClick = useCallback((event, node) => {
    if (selectedTool === 'token' && node.type === 'place') {
      event.preventDefault(); 
      const currentTokens = node.data.tokens || 0;
      const newTokens = event.shiftKey ? Math.max(0, currentTokens - 1) : currentTokens + 1;
      updatePlace(node.id, { tokens: newTokens });
    } else {
      setSelectedElement({
        type: node.type,
        id: node.id,
        data: node.data,
      });
    }
  }, [selectedTool, updatePlace, setSelectedElement]);

  const onNodesDelete = useCallback(
    (nodesToDelete) => {
      nodesToDelete.forEach((node) => {
        if (node.type === 'place') {
          deletePlace(node.id);
        } else if (node.type === 'transition') {
          deleteTransition(node.id);
        }
      });
      // Reset selection sau khi xóa
      setSelectedElement(null);
    },
    [deletePlace, deleteTransition, setSelectedElement]
  );
  
  const onEdgesDelete = useCallback(
    (edgesToDelete) => {
      edgesToDelete.forEach((edge) => {
        deleteArc(edge.id);
      });
      setSelectedElement(null);
    },
    [deleteArc, setSelectedElement]
  );

  return (
    <div className="flex-1 relative" ref={reactFlowWrapper}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeDragStop={onNodeDragStop}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        onPaneClick={onPaneClick}
        onNodesDelete={onNodesDelete}
        onEdgesDelete={onEdgesDelete}
        onInit={setReactFlowInstance}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        connectionLineType={ConnectionLineType.SmoothStep}
        fitView
        snapToGrid
        minZoom={0.1}
        className="bg-canvas-bg"
        nodesConnectable={selectedTool === 'select' || selectedTool === 'arc'}
        nodesDraggable={selectedTool === 'select'}
      >
        <Background color="#e2e8f0" gap={20} />
        <Controls />
        <MiniMap 
            nodeColor={(n) => n.type === 'place' ? '#3b82f6' : '#1e293b'} 
            maskColor="rgba(0, 0, 0, 0.1)"
        />
      </ReactFlow>

      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-white/90 backdrop-blur px-4 py-2 rounded shadow text-sm text-gray-600 border border-gray-200">
        Mode: <strong>{selectedTool.toUpperCase()}</strong>
        {selectedTool === 'token' && <span className="ml-2 text-xs text-gray-500">(Click: +1, Shift+Click: -1)</span>}
      </div>
    </div>
  );
};

export default CanvasEditor;