import React from 'react';
import PropTypes from 'prop-types';
import { FaTimes, FaFileDownload } from 'react-icons/fa';
import usePetriNetStore from '../../hooks/usePetriNet';

/**
 * Export Modal - Chọn format và export
 * @param {Object} props - Component props
 * @param {Function} [props.onExport] - Callback function when export is triggered
 */
const ExportModal = ({ onExport = () => {} }) => {
  const { modals = {}, closeModal } = usePetriNetStore();
  const [selectedFormat, setSelectedFormat] = React.useState('json');
  const [includeAnalysis, setIncludeAnalysis] = React.useState(false);
  const [isExporting, setIsExporting] = React.useState(false);
  
  // Early return if modal is not open
  if (!modals?.export) return null;
  
  const formats = [
    { id: 'json', label: 'JSON', icon: '📄', desc: 'JavaScript Object Notation' },
    { id: 'pnml', label: 'PNML', icon: '📄', desc: 'Petri Net Markup Language (XML)' },
    { id: 'png', label: 'PNG', icon: '🖼️', desc: 'Portable Network Graphics' },
    { id: 'svg', label: 'SVG', icon: '🖼️', desc: 'Scalable Vector Graphics' },
  ];
  
  const handleExport = async () => {
    if (isExporting) return;
    
    setIsExporting(true);
    
    try {
      if (typeof onExport === 'function') {
        await Promise.resolve(onExport(selectedFormat, { includeAnalysis }));
      }
    } catch (err) {
      console.error('Export failed:', err);
      // Just close the modal on error
    } finally {
      setIsExporting(false);
      closeModal('export');
    }
  };
  
  return (
    <div className="modal-backdrop" onClick={() => closeModal('export')}>
      <div 
        className="modal-content max-w-lg p-6"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-800">Export Petri Net</h2>
          <button
            onClick={() => closeModal('export')}
            className="text-gray-500 hover:text-gray-700"
          >
            <FaTimes size={20} />
          </button>
        </div>
        
        {/* Format selection */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Chọn định dạng:
          </label>
          <div className="grid grid-cols-2 gap-3">
            {formats.map(format => (
              <button
                key={format.id}
                onClick={() => setSelectedFormat(format.id)}
                className={`
                  p-3 rounded border-2 text-left transition-all duration-200
                  ${selectedFormat === format.id
                    ? 'border-primary-600 bg-primary-50'
                    : 'border-gray-300 hover:border-primary-300'
                  }
                `}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-2xl">{format.icon}</span>
                  <span className="font-semibold">{format.label}</span>
                </div>
                <div className="text-xs text-gray-600">{format.desc}</div>
              </button>
            ))}
          </div>
        </div>
        
        {/* Options */}
        {(selectedFormat === 'json' || selectedFormat === 'pnml') && (
          <div className="mb-4">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={includeAnalysis}
                onChange={(e) => setIncludeAnalysis(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm text-gray-700">
                Bao gồm kết quả phân tích
              </span>
            </label>
          </div>
        )}
        
        {/* Actions */}
        <div className="flex gap-3 justify-end pt-4 border-t">
          <button
            onClick={() => closeModal('export')}
            className="btn-secondary"
          >
            Hủy
          </button>
          <button
            onClick={handleExport}
            disabled={isExporting}
            className={`btn-primary w-full flex items-center justify-center gap-2 ${
              isExporting ? 'opacity-70 cursor-not-allowed' : ''
            }`}
          >
            {isExporting ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Đang xử lý...
              </>
            ) : (
              <>
                <FaFileDownload />
                Export {formats.find(f => f.id === selectedFormat)?.label || ''}
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

ExportModal.propTypes = {
  onExport: PropTypes.func
};

ExportModal.defaultProps = {
  onExport: () => {}
};

export default ExportModal;


