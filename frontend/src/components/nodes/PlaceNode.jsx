import React from 'react';
import { Handle, Position } from 'reactflow';
import usePetriNetStore from '../../hooks/usePetriNet';

/**
 * Custom Place Node cho React Flow
 * Hiển thị hình tròn với token count và label
 */
const PlaceNode = ({ id, data, selected }) => {
  const { updatePlace, setSelectedElement, currentMarking } = usePetriNetStore();
  
  // Lấy số token hiện tại (ưu tiên từ simulation marking)
  const tokens = currentMarking[id] !== undefined ? currentMarking[id] : (data.tokens || 0);
  
  const handleClick = () => {
    setSelectedElement({
      type: 'place',
      id,
      data: { ...data, tokens }
    });
  };
  
  // Render tokens as dots
  const renderTokens = () => {
    if (tokens === 0) return null;
    
    if (tokens <= 5) {
      // Hiển thị dots
      const positions = [
        [0, 0], // 1 token ở giữa
        [-8, 0], [8, 0], // 2 tokens
        [-8, -8], [8, -8], [0, 8], // 3 tokens
        [-8, -8], [8, -8], [-8, 8], [8, 8], // 4 tokens
        [-12, -12], [12, -12], [-12, 12], [12, 12], [0, 0], // 5 tokens
      ];
      
      const dotPositions = positions.slice(0, tokens);
      
      return dotPositions.map((pos, idx) => (
        <circle
          key={idx}
          cx={30 + pos[0]}
          cy={30 + pos[1]}
          r="3"
          fill="#1e293b"
          className="token-dot"
        />
      ));
    } else {
      // Hiển thị số nếu > 5
      return (
        <text
          x="30"
          y="35"
          textAnchor="middle"
          className="text-sm font-bold fill-gray-900"
        >
          {tokens}
        </text>
      );
    }
  };
  
  return (
    <div
      onClick={handleClick}
      className={`place-node ${selected ? 'selected' : ''}`}
    >
      <svg width="60" height="60" className="place-svg">
        {/* Main circle */}
        <circle
          cx="30"
          cy="30"
          r="25"
          fill="white"
          stroke={selected ? '#3b82f6' : '#64748b'}
          strokeWidth={selected ? 3 : 2}
          className="place-circle transition-all duration-200"
        />
        
        {/* Tokens */}
        {renderTokens()}
        
        {/* Hover effect circle */}
        <circle
          cx="30"
          cy="30"
          r="25"
          fill="transparent"
          className="hover:fill-blue-50 hover:fill-opacity-30 transition-all duration-200"
        />
      </svg>
      
      {/* Label */}
      <div className="place-label text-xs font-medium text-gray-700 text-center mt-1">
        {data.label || id}
      </div>
      
      {/* Handles for connections */}
      <Handle
        type="target"
        position={Position.Top}
        className="w-2 h-2 !bg-blue-500"
      />
      <Handle
        type="source"
        position={Position.Bottom}
        className="w-2 h-2 !bg-blue-500"
      />
      <Handle
        type="target"
        position={Position.Left}
        className="w-2 h-2 !bg-blue-500"
      />
      <Handle
        type="source"
        position={Position.Right}
        className="w-2 h-2 !bg-blue-500"
      />
    </div>
  );
};

export default PlaceNode;


