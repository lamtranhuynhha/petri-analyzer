import React from 'react';
import { FaTimes, FaGithub, FaFilePdf } from 'react-icons/fa';
import usePetriNetStore from '../../hooks/usePetriNet';

const WelcomeModal = () => {
  const { modals, closeModal } = usePetriNetStore();
  
  // Kiểm tra trạng thái modal 'welcome'
  if (!modals.welcome) return null;
  
  return (
    <div className="modal-backdrop" onClick={() => closeModal('welcome')}>
      <div 
        className="modal-content max-w-lg p-0 overflow-hidden relative"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header với Background màu primary */}
        <div className="bg-primary-600 p-6 text-white text-center relative">
          <button 
            onClick={() => closeModal('welcome')}
            className="absolute top-4 right-4 text-white/80 hover:text-white transition-colors"
          >
            <FaTimes size={20} />
          </button>
          <h2 className="text-2xl font-bold">Welcome to Petri Analyzer</h2>
        </div>

        {/* Content */}
        <div className="p-8">
          <p className="text-gray-600 leading-relaxed mb-6 text-center">
            Dự án này được phát triển nhằm xây dựng một công cụ trực quan hóa 
            và phân tích Petri net, hỗ trợ trong học tập và nghiên cứu.
          </p>

          <div className="space-y-3">
            {/* Github Link */}
            <a 
              href="https://github.com/lamtranhuynhha/petri-analyzer" // Thay link của bạn vào đây
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center gap-4 p-4 rounded-lg border border-gray-200 hover:border-gray-800 hover:bg-gray-50 transition-all group"
            >
              <FaGithub className="text-3xl text-gray-700 group-hover:text-black" />
              <div className="flex-1">
                <div className="font-semibold text-gray-800">Github Repository</div>
                <div className="text-sm text-gray-500">Source code & Documentation</div>
              </div>
            </a>

            {/* Tài liệu tham khảo Link */}
            <a 
              href="#" // Thay link tài liệu của bạn vào đây
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center gap-4 p-4 rounded-lg border border-gray-200 hover:border-red-200 hover:bg-red-50 transition-all group"
            >
              <FaFilePdf className="text-3xl text-red-500 group-hover:text-red-600" />
              <div className="flex-1">
                <div className="font-semibold text-gray-800">Tài liệu tham khảo</div>
                <div className="text-sm text-gray-500">Báo cáo & Hướng dẫn sử dụng</div>
              </div>
            </a>
          </div>
        </div>
        
        {/* Footer */}
        <div className="bg-gray-50 p-4 text-center border-t border-gray-100">
          <button 
            onClick={() => closeModal('welcome')}
            className="text-sm text-gray-500 hover:text-gray-800 font-medium"
          >
            Đóng cửa sổ này
          </button>
        </div>
      </div>
    </div>
  );
};

export default WelcomeModal;