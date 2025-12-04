import React, { useCallback } from 'react';
import { getStraightPath, useStore, EdgeLabelRenderer, BaseEdge } from 'reactflow';
import usePetriNetStore from '../../hooks/usePetriNet';

const useNode = (id) => {
  const node = useStore(useCallback((s) => s.nodeInternals.get(id), [id]));
  return node;
};

function getCircleIntersection(node, targetPosition) {
  const r = node.width ? node.width / 2 : 20; 
  const x = node.positionAbsolute.x + node.width / 2;
  const y = node.positionAbsolute.y + node.height / 2;
  const dx = targetPosition.x - x;
  const dy = targetPosition.y - y;
  const angle = Math.atan2(dy, dx);
  return { x: x + r * Math.cos(angle), y: y + r * Math.sin(angle) };
}

function getRectangleIntersection(node, targetPosition) {
  const w = node.width || 40;
  const h = node.height || 40;
  const x = node.positionAbsolute.x + w / 2;
  const y = node.positionAbsolute.y + h / 2;
  const dx = targetPosition.x - x;
  const dy = targetPosition.y - y;
  if (dx === 0 && dy === 0) return { x, y };
  const slope = dy / (dx || 0.0001);
  if (Math.abs(dx) * h > Math.abs(dy) * w) {
    if (dx > 0) return { x: x + w / 2, y: y + (w / 2) * slope };
    else return { x: x - w / 2, y: y - (w / 2) * slope };
  } else {
    if (dy > 0) return { x: x + (h / 2) / slope, y: y + h / 2 };
    else return { x: x - (h / 2) / slope, y: y - h / 2 };
  }
}

function getEdgeParams(source, target) {
  const sourceCenter = {
    x: source.positionAbsolute.x + source.width / 2,
    y: source.positionAbsolute.y + source.height / 2,
  };
  const targetCenter = {
    x: target.positionAbsolute.x + target.width / 2,
    y: target.positionAbsolute.y + target.height / 2,
  };
  let sourceIntersection, targetIntersection;
  if (source.type === 'place') sourceIntersection = getCircleIntersection(source, targetCenter);
  else sourceIntersection = getRectangleIntersection(source, targetCenter);
  if (target.type === 'place') targetIntersection = getCircleIntersection(target, sourceCenter);
  else targetIntersection = getRectangleIntersection(target, sourceCenter);
  return { sx: sourceIntersection.x, sy: sourceIntersection.y, tx: targetIntersection.x, ty: targetIntersection.y };
}

const ArcEdge = (props) => {
  const { id, source, target, markerEnd, style, data } = props;
  const sourceNode = useNode(source);
  const targetNode = useNode(target);
  
  //LẤY WEIGHTS TRỰC TIẾP TỪ STORE
  const weights = usePetriNetStore((state) => state.weights);

  if (!sourceNode || !targetNode) return null;

  //TÌM WEIGHT
  const weightKey = JSON.stringify([source, target]);
  const weight = weights?.[weightKey] !== undefined ? weights[weightKey] : (data?.weight || 1);

  const { sx, sy, tx, ty } = getEdgeParams(sourceNode, targetNode);

  let edgePath = '';
  let labelX, labelY;
  
  //KIỂM TRA ĐỘ CONG TỪ DATA
  const curvature = data?.curvature || 0;

  // Tính vector hướng của dây
  const dx = tx - sx;
  const dy = ty - sy;
  const len = Math.sqrt(dx * dx + dy * dy) || 1;

  // Offset để đẩy chữ ra khỏi dây (cho dây thẳng)
  const textOffset = 8; 
  const normalX = dy / len;  
  const normalY = -dx / len;

  if (curvature === 0) {
    [edgePath] = getStraightPath({ sourceX: sx, sourceY: sy, targetX: tx, targetY: ty });
    
    const midX = (sx + tx) / 2;
    const midY = (sy + ty) / 2;
    labelX = midX + normalX * textOffset;
    labelY = midY + normalY * textOffset;

  } else {
    // --- VẼ CONG ---
    const offsetX = (-dy / len) * curvature;
    const offsetY = (dx / len) * curvature;
    const controlX = ((sx + tx) / 2) + offsetX;
    const controlY = ((sy + ty) / 2) + offsetY;

    edgePath = `M ${sx},${sy} Q ${controlX},${controlY} ${tx},${ty}`;

    // Đỉnh cong
    const peakX = ((sx + tx) / 2) + offsetX * 0.5;
    const peakY = ((sy + ty) / 2) + offsetY * 0.5;

    
    const curveDirX = offsetX / (Math.abs(curvature) || 1);
    const curveDirY = offsetY / (Math.abs(curvature) || 1);

    labelX = peakX + curveDirX * textOffset;
    labelY = peakY + curveDirY * textOffset;
  }

  if (isNaN(labelX) || isNaN(labelY)) return null;

  return (
    <>
      <BaseEdge path={edgePath} markerEnd={markerEnd} style={style} />
      
      <EdgeLabelRenderer>
        <div
          style={{
            position: 'absolute',
            transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px)`,
            pointerEvents: 'all',
            zIndex: 1000,
          }}
          className="nodrag nopan"
        >
          <div className="flex items-center justify-center">
            <span className="text-xs font-bold text-black-600">
              {weight}
            </span>
          </div>
        </div>
      </EdgeLabelRenderer>
    </>
  );
};

export default ArcEdge;