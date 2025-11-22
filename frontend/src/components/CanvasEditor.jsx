import React, { useCallback, useRef, useEffect } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  addEdge,
  MarkerType,
} from 'reactflow';
import 'reactflow/dist/style.css';

import usePetriNetStore from '../hooks/usePetriNet';
import PlaceNode from './nodes/PlaceNode';
import TransitionNode from './nodes/TransitionNode';
import ArcEdge from './edges/ArcEdge';

/**
 * Main Canvas Editor với React Flow
 * Hỗ trợ drawing tools: Select, Place, Transition, Arc, Token
 */
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
    setSelectedElement,
  } = usePetriNetStore();
  
  const reactFlowWrapper = useRef(null);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [reactFlowInstance, setReactFlowInstance] = React.useState(null);
  
  // Arc drawing state
  const [connectingArc, setConnectingArc] = React.useState(null);
  
  // Custom node types
  const nodeTypes = React.useMemo(
    () => ({
      place: PlaceNode,
      transition: TransitionNode,
    }),
    []
  );
  
  // Custom edge types
  const edgeTypes = React.useMemo(
    () => ({
      arc: ArcEdge,
    }),
    []
  );
  
  // Sync stores to React Flow nodes/edges
  useEffect(() => {
    // Convert places to nodes
    const placeNodes = places.map((place) => ({
      id: place.id,
      type: 'place',
      position: place.position || { x: Math.random() * 500, y: Math.random() * 400 },
      data: { 
        label: place.label || place.id,
        tokens: place.tokens || 0,
      },
    }));
    
    // Convert transitions to nodes
    const transitionNodes = transitions.map((trans) => ({
      id: trans.id,
      type: 'transition',
      position: trans.position || { x: Math.random() * 500, y: Math.random() * 400 },
      data: { 
        label: trans.label || trans.id,
      },
    }));
    
    setNodes([...placeNodes, ...transitionNodes]);
  }, [places, transitions, setNodes]);
  
  useEffect(() => {
    // Convert arcs to edges
    const flowEdges = arcs.map((arc) => ({
      id: arc.id,
      source: arc.source,
      target: arc.target,
      type: 'arc',
      markerEnd: {
        type: MarkerType.ArrowClosed,
        width: 20,
        height: 20,
      },
      data: {
        weight: arc.weight || 1,
        source: arc.source,
        target: arc.target,
      },
    }));
    
    setEdges(flowEdges);
  }, [arcs, setEdges]);
  
  // Handle canvas click - Add place or transition
  const onPaneClick = useCallback(
    (event) => {
      if (!reactFlowInstance) return;
      
      const bounds = reactFlowWrapper.current?.getBoundingClientRect();
      if (!bounds) return;
      
      const position = reactFlowInstance.project({
        x: event.clientX - bounds.left,
        y: event.clientY - bounds.top,
      });
      
      if (selectedTool === 'place') {
        const id = `p${Date.now()}`;
        addPlace({
          id,
          label: id,
          tokens: 0,
          position,
        });
      } else if (selectedTool === 'transition') {
        const id = `t${Date.now()}`;
        addTransition({
          id,
          label: id,
          position,
        });
      }
    },
    [reactFlowInstance, selectedTool, addPlace, addTransition]
  );
  
  // Handle node click - Token tool or selection
  const onNodeClick = useCallback(
    (event, node) => {
      event.stopPropagation();
      
      if (selectedTool === 'token' && node.type === 'place') {
        // Add token with left click, remove with right click
        const currentTokens = node.data.tokens || 0;
        const newTokens = event.shiftKey ? Math.max(0, currentTokens - 1) : currentTokens + 1;
        updatePlace(node.id, { tokens: newTokens });
      } else if (selectedTool === 'arc') {
        // Start or complete arc connection
        if (!connectingArc) {
          setConnectingArc({ source: node.id });
        } else if (connectingArc.source !== node.id) {
          // Complete arc
          const source = connectingArc.source;
          const target = node.id;
          
          // Validate arc: place->transition or transition->place
          const sourceNode = nodes.find(n => n.id === source);
          const targetNode = node;
          
          const isValid = 
            (sourceNode.type === 'place' && targetNode.type === 'transition') ||
            (sourceNode.type === 'transition' && targetNode.type === 'place');
          
          if (isValid) {
            addArc({
              id: `a${Date.now()}`,
              source,
              target,
              weight: 1,
            });
          } else {
            alert('Arc phải kết nối giữa Place và Transition!');
          }
          
          setConnectingArc(null);
        }
      } else {
        // Selection
        setSelectedElement({
          type: node.type,
          id: node.id,
          data: node.data,
        });
      }
    },
    [selectedTool, connectingArc, nodes, updatePlace, addArc, setSelectedElement]
  );
  
  // Handle edge click - Selection
  const onEdgeClick = useCallback(
    (event, edge) => {
      event.stopPropagation();
      setSelectedElement({
        type: 'arc',
        id: edge.id,
        data: edge.data,
      });
    },
    [setSelectedElement]
  );
  
  // Handle node drag end - Update position in store
  const onNodeDragStop = useCallback(
    (event, node) => {
      if (node.type === 'place') {
        updatePlace(node.id, { position: node.position });
      } else if (node.type === 'transition') {
        // updateTransition would go here
      }
    },
    [updatePlace]
  );
  
  // Cancel arc drawing on Escape
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        setConnectingArc(null);
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);
  
  return (
    <div className="flex-1 relative" ref={reactFlowWrapper}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        onEdgeClick={onEdgeClick}
        onNodeDragStop={onNodeDragStop}
        onPaneClick={onPaneClick}
        onInit={setReactFlowInstance}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
        snapToGrid
        snapGrid={[15, 15]}
        defaultEdgeOptions={{
          type: 'arc',
          animated: false,
        }}
        minZoom={0.2}
        maxZoom={4}
        className="bg-canvas-bg"
      >
        <Background color="#e2e8f0" gap={20} />
        <Controls />
        <MiniMap
          nodeColor={(node) => {
            if (node.type === 'place') return '#60a5fa';
            if (node.type === 'transition') return '#1e293b';
            return '#94a3b8';
          }}
          maskColor="rgba(0, 0, 0, 0.1)"
        />
      </ReactFlow>
      
      {/* Arc drawing indicator */}
      {connectingArc && (
        <div className="absolute top-4 left-1/2 transform -translate-x-1/2 bg-blue-600 text-white px-4 py-2 rounded shadow-lg z-50">
          Drawing arc from <strong>{connectingArc.source}</strong>. Click target node or press ESC to cancel.
        </div>
      )}
      
      {/* Tool hint */}
      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-white px-4 py-2 rounded shadow text-sm text-gray-600 border border-gray-300">
        {selectedTool === 'select' && 'Select và drag nodes'}
        {selectedTool === 'place' && 'Click để thêm Place'}
        {selectedTool === 'transition' && 'Click để thêm Transition'}
        {selectedTool === 'arc' && 'Click source → target để tạo Arc'}
        {selectedTool === 'token' && 'Click Place để +1 token, Shift+Click để -1'}
      </div>
    </div>
  );
};

export default CanvasEditor;


