import React, { useEffect, useCallback } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import TopBar from './components/TopBar';
import LeftToolbar from './components/LeftToolbar';
import CanvasEditor from './components/CanvasEditor';
import RightSidebar from './components/RightSidebar/RightSidebar';
import ConfirmDialog from './components/modals/ConfirmDialog';
import ExportModal from './components/modals/ExportModal';
import ReachabilityGraphModal from './components/modals/ReachabilityGraphModal';
import WelcomeModal from './components/modals/WelcomeModal';

import usePetriNetStore from './hooks/usePetriNet';
import * as api from './services/api';
import dagre from 'dagre';

// Auto-layout bằng dagre: sắp xếp các node theo hướng trái -> phải để đồ thị rõ ràng hơn
const applyDagreLayout = (net, options = {}) => {
  if (!net) return net;

  const g = new dagre.graphlib.Graph();
  g.setGraph({
    rankdir: options.rankdir || 'LR', // Left-to-Right
    nodesep: options.nodesep || 80,
    ranksep: options.ranksep || 120,
  });
  g.setDefaultEdgeLabel(() => ({}));

  const places = net.places || [];
  const transitions = net.transitions || [];
  const arcs = net.arcs || [];

  // Khai báo node với kích thước gần đúng với UI
  places.forEach((p) => {
    g.setNode(p.id, { width: 80, height: 80 }); // PlaceNode ~ 80x80
  });

  transitions.forEach((t) => {
    g.setNode(t.id, { width: 64, height: 100 }); // TransitionNode ~ 64x100
  });

  // Khai báo cạnh
  arcs.forEach((a) => {
    if (a.source && a.target) {
      g.setEdge(a.source, a.target);
    }
  });

  // Chạy layout
  dagre.layout(g);

  // Tính bounding box để scale cho phù hợp với kích thước mong muốn
  const dagreNodes = [
    ...(places || []).map((p) => ({ id: p.id, n: g.node(p.id) })),
    
    ...(transitions || []).map((t) => ({ id: t.id, n: g.node(t.id) })),
  ].filter(({ n }) => !!n);

  if (dagreNodes.length === 0) {
    return net;
  }

  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  dagreNodes.forEach(({ n }) => {
    minX = Math.min(minX, n.x);
    maxX = Math.max(maxX, n.x);
    minY = Math.min(minY, n.y);
    maxY = Math.max(maxY, n.y);
  });

  const rangeX = maxX - minX || 1;
  const rangeY = maxY - minY || 1;

  const targetWidth = options.targetWidth || 1200;
  const targetHeight = options.targetHeight || 700;
  const marginX = options.marginX || 50;
  const marginY = options.marginY || 50;

  const scale = Math.min(targetWidth / rangeX, targetHeight / rangeY, 1); // không phóng to quá 1

  const placedPlaces = (places || []).map((p) => {
    const n = g.node(p.id);
    if (!n) return p;
    const x = (n.x - minX) * scale + marginX;
    const y = (n.y - minY) * scale + marginY;
    return {
      ...p,
      position: { x, y },
    };
  });

  const placedTransitions = (transitions || []).map((t) => {
    const n = g.node(t.id);
    if (!n) return t;
    const x = (n.x - minX) * scale + marginX;
    const y = (n.y - minY) * scale + marginY;
    return {
      ...t,
      position: { x, y },
    };
  });

  return {
    ...net,
    places: placedPlaces,
    transitions: placedTransitions,
  };
};

/**
 * Main App Component - Assembly tất cả components và xử lý business logic
 */
function App() {
  const {
    resetNet,
    loadPetriNet,
    getPetriNetData,
    getPetriNetDataGraphic,
    setAnalysisResult,
    setLoading,
    updateStatus,
    undo,
    canUndo,
    setSelectedTool,
    places,
    transitions,
    setSelectedElement,
  } = usePetriNetStore();
  
  // File operations
  const handleSave = useCallback(() => {
    try {
      const data = getPetriNetData();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `petri-net-${Date.now()}.json`;
      a.click();
      URL.revokeObjectURL(url);
      toast.success('Đã lưu file JSON');
    } catch (error) {
      console.error('Error saving file:', error);
      toast.error('Lỗi khi lưu file');
    }
  }, [getPetriNetData]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ctrl+Z: Undo
      if (e.ctrlKey && e.key === 'z' && !e.shiftKey) {
        e.preventDefault();
        if (canUndo()) undo();
      }
      
      // Ctrl+S: Save
      if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        handleSave();
      }
      
      // Tool shortcuts
      if (!e.ctrlKey && !e.altKey && !e.metaKey) {
        if (e.key === 's' || e.key === 'S') setSelectedTool('select');
        if (e.key === 'p' || e.key === 'P') setSelectedTool('place');
        if (e.key === 't' || e.key === 'T') setSelectedTool('transition');
        if (e.key === 'a' || e.key === 'A') setSelectedTool('arc');
        if (e.key === 'k' || e.key === 'K') setSelectedTool('token');
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [
    canUndo, 
    undo, 
    handleSave, 
    places, 
    transitions, 
    setSelectedElement, 
    setSelectedTool
  ]);

  const handleNew = () => {
    resetNet();
    toast.success('Đã tạo Petri Net mới');
  };
  
  const handleOpen = async (file) => {
    try {
      setLoading('upload', true);
      const result = await api.uploadPetriNet(file);
      
      if (result.data?.parsed_net) {
        let net = result.data.parsed_net;

        // Chỉ áp dụng dagre layout cho file PNML (để JSON tự vẽ giữ nguyên vị trí)
        if (file.name.toLowerCase().endsWith('.pnml')) {
          net = applyDagreLayout(net);
        }

        loadPetriNet(net);
        toast.success(`Đã mở file: ${file.name}`);
      }
    } catch (error) {
      console.error('Error opening file:', error);
      toast.error('Lỗi khi mở file: ' + (error.message || 'Unknown error'));
    } finally {
      setLoading('upload', false);
    }
  };
  
  const handleExport = async (format, options = {}) => {
    try {
      const data = getPetriNetDataGraphic();
      
      if (format === 'json') {
        const exportData = options.includeAnalysis
          ? { ...data, analysis: usePetriNetStore.getState().analysisResults }
          : data;
        
        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `petri-net-export-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
        toast.success('Đã export JSON');
      } else if (format === 'pnml') {
        const result = await api.exportPetriNet(data, 'pnml');
        // Download file from result
        const blob = result;
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `petri-net-export-${Date.now()}.pnml`;
        a.click();
        URL.revokeObjectURL(url);
        toast.success('Đã export PNML');
      } else if (format === 'png' || format === 'svg') {
        // Export canvas as image
        const result = await api.exportPetriNet(data, format);
        // Download file from result
        const blob = result;
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `petri-net-export-${Date.now()}.${format}`;
        a.click();
        URL.revokeObjectURL(url);
        toast.success(`Đã export ${format}`);
      } else if (format === 'rg') {
        // Export reachability graph
        toast.info('Chức năng export RG đang được phát triển');
      }
    } catch (error) {
      console.error('Error exporting:', error);
      toast.error('Lỗi khi export: ' + (error.message || 'Unknown error'));
    }
  };
  
  // Analysis operations
  const handleAnalyze = async (type) => {
    const data = getPetriNetData();
    
    // Validate có net không
    if (!data.places || data.places.length === 0) {
      toast.warning('Vui lòng vẽ Petri Net trước khi phân tích!');
      return;
    }
    
    try {
      setLoading(type, true);
      
      switch (type) {
        case 'reachability': {
          const result = await api.analyzeReachability(data);
          console.log("Data: ",data);

          // Hỗ trợ cả hai dạng: { result: {...} } hoặc trả phẳng {...}
          const rgResult = result?.result || result;

          // Log để dễ debug nếu structure khác kỳ vọng
          console.log('Reachability analysis raw result:', result);
          console.log('Reachability parsed rgResult:', rgResult);

          const stateCount = rgResult
            ? (
                rgResult.total_states ??
                (Array.isArray(rgResult.states)
                  ? rgResult.states.length
                  : (rgResult.states ? Object.keys(rgResult.states).length : 0))
              )
            : 0;

          // Nếu chưa có graph_image, gọi API visualization để lấy ảnh SVG
          if (!rgResult?.graph_image) {
            try {
              const blob = await api.getReachabilityGraphImage(rgResult, 'svg');
              const url = URL.createObjectURL(blob);
              rgResult.graph_image = url; // gán URL tạm thời để modal hiển thị
              // Mở tab mới xem đồ thị
              window.open(url, '_blank');
            } catch (imgErr) {
              console.error('Lỗi khi lấy ảnh RG:', imgErr);
              // Không có ảnh thì không mở tab, chỉ lưu kết quả
            }
          } else {
            // Nếu backend đã trả URL ảnh, mở tab mới
            window.open(rgResult.graph_image, '_blank');
          }

          setAnalysisResult('reachability', rgResult);
          updateStatus({
            stateCount,
            hasWarning: rgResult?.truncated || false,
            warningMessage: rgResult?.truncated ? 'State explosion detected' : '',
          });
          toast.success(`Đã build RG với ${stateCount} states`);

          break;
        }
        
        case 'deadlock': {
          const result = await api.analyzeDeadlock(data);
          setAnalysisResult('deadlock', result);
          toast.success(`Tìm thấy ${result.total_deadlocks} deadlock states`);
          break;
        }
        
        case 'boundedness': {
          const result = await api.analyzeBoundedness(data);
          setAnalysisResult('boundedness', result);
          updateStatus({
            isBounded: result?.is_bounded,
          });
          toast.success(
            result.result?.is_bounded
              ? 'Net is BOUNDED'
              : 'Net is UNBOUNDED'
          );
          break;
        }
        
        case 'liveness': {
          const result = await api.analyzeLiveness(data);
          setAnalysisResult('liveness', result);
          toast.success('Đã phân tích liveness');
          break;
        }
        
        case 'siphonsTraps': {
          const result = await api.analyzeSiphonsTraps(data);
          setAnalysisResult('siphonsTraps', result);
          toast.success(
            `Tìm thấy ${result.result?.minimal_siphons?.length || 0} siphons, ` +
            `${result.result?.minimal_traps?.length || 0} traps`
          );
          break;
        }
        
        default:
          toast.warning('Unknown analysis type');
      }
    } catch (error) {
      console.error(`Error analyzing ${type}:`, error);
      toast.error(`Lỗi khi phân tích ${type}: ` + (error.message || 'Unknown error'));
    } finally {
      setLoading(type, false);
    }
  };
  
  return (
    <div className="h-screen w-screen flex flex-col overflow-hidden">
      {/* Top Bar */}
      <TopBar
        onNew={handleNew}
        onOpen={handleOpen}
        onSave={handleSave}
        onExport={handleExport}
      />
      
      {/* Main Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Toolbar */}
        <LeftToolbar />
        
        {/* Canvas Editor */}
        <CanvasEditor />
        
        {/* Right Sidebar */}
        <RightSidebar onAnalyze={handleAnalyze} />
      </div>
      
      {/* Modals */}
      <ConfirmDialog />
      <ExportModal onExport={handleExport} />
      <ReachabilityGraphModal />

      <WelcomeModal />
      
      {/* Toast Notifications */}
      <ToastContainer
        position="bottom-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
    </div>
  );
}

export default App;


