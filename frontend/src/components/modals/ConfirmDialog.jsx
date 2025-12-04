import React from 'react';
import usePetriNetStore from '../../hooks/usePetriNet';

/**
 * Confirm Dialog Modal - Xác nhận các actions quan trọng
 */
const ConfirmDialog = () => {
  const { modals, closeModal, confirmAction } = usePetriNetStore();
  
  if (!modals?.confirm || !confirmAction) return null;
  
  const handleConfirm = () => {
    if (confirmAction.onConfirm) {
      confirmAction.onConfirm();
    }
    closeModal('confirm');
  };
  
  const handleCancel = () => {
    if (confirmAction.onCancel) {
      confirmAction.onCancel();
    }
    closeModal('confirm');
  };
  
  return (
    <div className="modal-backdrop" onClick={handleCancel}>
      <div 
        className="modal-content max-w-md p-6"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="mb-4">
          <h2 className="text-xl font-bold text-gray-800 mb-2">
            {confirmAction.title || 'Xác nhận'}
          </h2>
          <p className="text-gray-600">
            {confirmAction.message || 'Bạn có chắc chắn muốn thực hiện hành động này?'}
          </p>
        </div>
        
        <div className="flex gap-3 justify-end">
          <button
            onClick={handleCancel}
            className="btn-secondary"
          >
            Hủy
          </button>
          <button
            onClick={handleConfirm}
            className="btn-danger"
          >
            Xác nhận
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmDialog;


