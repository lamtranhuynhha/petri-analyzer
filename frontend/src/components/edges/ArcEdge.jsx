import React from 'react';
import { getStraightPath, EdgeLabelRenderer, BaseEdge } from 'reactflow';
import usePetriNetStore from '../../hooks/usePetriNet';

/**
 * Custom Arc Edge cho React Flow
 * Hiển thị mũi tên với weight label (ẩn nếu weight = 1)
 */
const ArcEdge = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  style = {},
  markerEnd,
  data,
  selected,
}) => {
  const { setSelectedElement, weights } = usePetriNetStore();
  
  const [edgePath, labelX, labelY] = getStraightPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });
  
  // Lấy weight từ data hoặc từ store
  const weight = data?.weight || 1;
  
  const handleClick = () => {
    // Get the weight from the store to ensure it's up to date
    const weightKey = JSON.stringify([data.source, data.target]);
    const currentWeight = weights[weightKey] || data.weight || 1;
    
    setSelectedElement({
      type: 'arc',
      id,
      data: { 
        ...data, 
        weight: currentWeight, 
        source: data.source, 
        target: data.target 
      }
    });
  };
  
  return (
    <>
      <BaseEdge
        path={edgePath}
        markerEnd={markerEnd}
        style={{
          ...style,
          stroke: selected ? '#3b82f6' : '#64748b',
          strokeWidth: selected ? 3 : 1.5,
        }}
        className="arc-edge transition-all duration-200"
      />
      
      {/* Weight label - chỉ hiển thị nếu weight > 1 */}
      {weight > 1 && (
        <EdgeLabelRenderer>
          <div
            style={{
              position: 'absolute',
              transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
              pointerEvents: 'all',
            }}
            className="nodrag nopan"
            onClick={handleClick}
          >
            <div className={`
              px-2 py-0.5 rounded-full text-xs font-semibold
              bg-white border-2 shadow-sm cursor-pointer
              transition-all duration-200
              ${selected ? 'border-blue-500 text-blue-600' : 'border-gray-400 text-gray-700'}
              hover:border-blue-400 hover:text-blue-500
            `}>
              {weight}
            </div>
          </div>
        </EdgeLabelRenderer>
      )}
      
      {/* Invisible wider path for easier clicking */}
      <path
        d={edgePath}
        fill="none"
        stroke="transparent"
        strokeWidth={20}
        onClick={handleClick}
        className="cursor-pointer"
      />
    </>
  );
};

export default ArcEdge;


