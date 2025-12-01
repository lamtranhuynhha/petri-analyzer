import React, { useEffect } from 'react';
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

/**
 * Main App Component - Assembly tất cả components và xử lý business logic
 */
function App() {
  const {
    resetNet,
    loadPetriNet,
    getPetriNetData,
    setAnalysisResult,
    setLoading,
    updateStatus,
    undo,
    redo,
    canUndo,
    canRedo,
    setSelectedTool,
  } = usePetriNetStore();
  
  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ctrl+Z: Undo
      if (e.ctrlKey && e.key === 'z' && !e.shiftKey) {
        e.preventDefault();
        if (canUndo()) undo();
      }
      
      // Ctrl+Y hoặc Ctrl+Shift+Z: Redo
      if ((e.ctrlKey && e.key === 'y') || (e.ctrlKey && e.shiftKey && e.key === 'z')) {
        e.preventDefault();
        if (canRedo()) redo();
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
  }, [canUndo, canRedo, undo, redo, setSelectedTool]);
  
  // File operations
  const handleNew = () => {
    resetNet();
    toast.success('Đã tạo Petri Net mới');
  };
  
  const handleOpen = async (file) => {
    try {
      setLoading('upload', true);
      const result = await api.uploadPetriNet(file);
      
      if (result.data?.parsed_net) {
        loadPetriNet(result.data.parsed_net);
        toast.success(`Đã mở file: ${file.name}`);
      }
    } catch (error) {
      console.error('Error opening file:', error);
      toast.error('Lỗi khi mở file: ' + (error.message || 'Unknown error'));
    } finally {
      setLoading('upload', false);
    }
  };
  
  const handleSave = () => {
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
  };
  
  const handleExport = async (format, options = {}) => {
    try {
      const data = getPetriNetData();
      
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
        toast.success('Đã export PNML');
      } else if (format === 'png' || format === 'svg') {
        // Export canvas as image
        toast.info('Chức năng export ảnh đang được phát triển');
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
          // SỬA: Bỏ .result đi
          setAnalysisResult('reachability', result); 
          updateStatus({
            // SỬA: Truy cập trực tiếp result.states
            stateCount: result?.states?.length || 0,
            hasWarning: false, // Backend hiện tại chưa trả về field 'truncated' trong ReachabilityResult
            warningMessage: '',
          });
          toast.success(`Đã build RG với ${result?.states?.length || 0} states`);
          break;
        }

        case 'deadlock': {
          // Đoạn này bạn đang làm ĐÚNG với cấu trúc backend
          const result = await api.analyzeDeadlock(data);
          setAnalysisResult('deadlock', result);
          toast.success(`Tìm thấy ${result.total_deadlocks} deadlock states`);
          break;
        }

        case 'boundedness': {
          const result = await api.analyzeBoundedness(data);
          // SỬA: Bỏ .result
          setAnalysisResult('boundedness', result);
          updateStatus({
            // SỬA: Truy cập trực tiếp result.is_bounded
            isBounded: result?.is_bounded,
          });
          toast.success(
            result?.is_bounded ? 'Net is BOUNDED' : 'Net is UNBOUNDED'
          );
          break;
        }

        case 'liveness': {
          const result = await api.analyzeLiveness(data);
          // SỬA: Bỏ .result
          setAnalysisResult('liveness', result);
          toast.success('Đã phân tích liveness');
          break;
        }

        case 'siphonsTraps': {
          const result = await api.analyzeSiphonsTraps(data);
          // SỬA: Bỏ .result
          setAnalysisResult('siphonsTraps', result);
          toast.success(
            // SỬA: Truy cập trực tiếp
            `Tìm thấy ${result?.minimal_siphons?.length || 0} siphons, ` +
            `${result?.minimal_traps?.length || 0} traps`
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


