import React from 'react';
import { Handle, Position } from 'reactflow';
import usePetriNetStore from '../../hooks/usePetriNet';

const PLACE_RADIUS = 18;
const PLACE_PADDING = 0;
const PLACE_CENTER = PLACE_RADIUS + PLACE_PADDING;
const PLACE_SVG_SIZE = PLACE_CENTER * 2;
const TOKEN_RADIUS = Math.max(3, PLACE_RADIUS * 0.15);
const TOKEN_FONT_SIZE = Math.round(PLACE_RADIUS * 0.6);

/**
 * Custom Place Node cho React Flow
 * Hiển thị hình tròn lớn với token count và label
 */
const PlaceNode = ({ id, data, selected }) => {
  const { updatePlace, setSelectedElement, currentMarking, selectedTool, firstSelectedNode } = usePetriNetStore();
  
  // Lấy số token hiện tại (ưu tiên từ simulation marking)
const tokens = (currentMarking && currentMarking[id] !== undefined) ? currentMarking[id] : (data.tokens || 0);
  
  // Kiểm tra nếu node đang được chọn để tạo arc
  const isArcSource = selectedTool === 'arc' && firstSelectedNode?.id === id;
  
  const handleClick = () => {
    if (selectedTool !== 'arc') {
      setSelectedElement({
        type: 'place',
        id,
        data: { ...data, tokens }
      });
    }
  };
  
  // Render tokens as dots - điều chỉnh vị trí tỉ lệ theo PLACE_RADIUS
  const renderTokens = () => {
    if (tokens === 0) return null;
    
    // Logic vẽ token thông minh hơn, dựa trên PLACE_RADIUS
    if (tokens <= 3) {
      // Định nghĩa vị trí tương đối so với tâm (PLACE_CENTER, PLACE_CENTER)
      let pos = [];
      const dxSmall = PLACE_RADIUS * 0.45;
      const dySmall = PLACE_RADIUS * 0.3;
      const dxLarge = PLACE_RADIUS * 0.55;
      const dyLarge = PLACE_RADIUS * 0.55;

      if (tokens === 1) pos = [[0, 0]];
      else if (tokens === 2) pos = [[-dxSmall, 0], [dxSmall, 0]];
      else if (tokens === 3) pos = [[-dxSmall, -dySmall], [dxSmall, -dySmall], [0, dySmall]];
      else if (tokens === 4) pos = [[-dxSmall, -dxSmall], [dxSmall, -dxSmall], [-dxSmall, dxSmall], [dxSmall, dxSmall]];
      else if (tokens === 5) pos = [[-dxLarge, -dxLarge], [dxLarge, -dxLarge], [-dxLarge, dxLarge], [dxLarge, dxLarge], [0, 0]];
      
      return pos.map((p, idx) => (
        <circle
          key={idx}
          cx={PLACE_CENTER + p[0]}
          cy={PLACE_CENTER + p[1]}
          r={TOKEN_RADIUS}
          fill="#1e293b"
        />
      ));
    } else {
      return (
        <text
          x={PLACE_CENTER}
          y={PLACE_CENTER + PLACE_RADIUS * 0.22}
          textAnchor="middle"
          fontSize={TOKEN_FONT_SIZE}
          fontWeight="bold"
          fill="#1e293b"
        >
          {tokens}
        </text>
      );
    }
  };
  
  return (
    <div
      onClick={handleClick}
      className={`place-node ${selected ? 'selected' : ''} ${isArcSource ? 'arc-source' : ''}`}
    >
      <svg width={PLACE_SVG_SIZE} height={PLACE_SVG_SIZE} className="place-svg">
        {/* Main circle - kích thước phụ thuộc PLACE_RADIUS */}
        <circle
          cx={PLACE_CENTER}
          cy={PLACE_CENTER}
          r={PLACE_RADIUS}
          fill="white"
          stroke={isArcSource ? '#10b981' : (selected ? '#3b82f6' : '#64748b')}
          strokeWidth={isArcSource ? 4 : (selected ? 3 : 1)}
          className="place-circle transition-all duration-200 hover:stroke-blue-400"
        />
        
        {/* Tokens */}
        {renderTokens()}
        
        {/* Hover effect circle */}
        <circle
          cx={PLACE_CENTER}
          cy={PLACE_CENTER}
          r={PLACE_RADIUS}
          fill="transparent"
          className="hover:fill-blue-50 hover:fill-opacity-20 transition-all duration-200 cursor-pointer"
        />
      </svg>
      
      {/* Label */}
      <div className="place-label text-sm font-medium text-gray-700 text-center">
        {data.label || id}
      </div>
      
      {/* Handles for connections (ẩn, chỉ để React Flow gắn edge) */}
      {/* Top side */}
      <Handle
        id="top-target"
        type="target"
        position={Position.Top}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />
      <Handle
        id="top-source"
        type="source"
        position={Position.Top}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />

      {/* Bottom side */}
      <Handle
        id="bottom-target"
        type="target"
        position={Position.Bottom}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />
      <Handle
        id="bottom-source"
        type="source"
        position={Position.Bottom}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />

      {/* Left side */}
      <Handle
        id="left-target"
        type="target"
        position={Position.Left}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />
      <Handle
        id="left-source"
        type="source"
        position={Position.Left}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />

      {/* Right side */}
      <Handle
        id="right-target"
        type="target"
        position={Position.Right}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />
      <Handle
        id="right-source"
        type="source"
        position={Position.Right}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />
    </div>
  );
};

export default PlaceNode;


