import React from 'react';
import PropTypes from 'prop-types';
import usePetriNetStore from '../../hooks/usePetriNet';

/**
 * Confirm Dialog Modal - Xác nhận các actions quan trọng
 */
const ConfirmDialog = () => {
  const { modals = {}, closeModal, confirmAction = {} } = usePetriNetStore();
  
  // Early return if modal is not open
  if (!modals?.confirm) return null;
  
  const handleConfirm = () => {
    try {
      if (typeof confirmAction?.onConfirm === 'function') {
        confirmAction.onConfirm();
      }
    } catch (error) {
      console.error('Error in confirm action:', error);
    } finally {
      closeModal('confirm');
    }
  };
  
  const handleCancel = () => {
    try {
      if (typeof confirmAction?.onCancel === 'function') {
        confirmAction.onCancel();
      }
    } catch (error) {
      console.error('Error in cancel action:', error);
    } finally {
      closeModal('confirm');
    }
  };
  
  const {
    title = 'Xác nhận',
    message = 'Bạn có chắc chắn muốn thực hiện hành động này?',
    confirmText = 'Xác nhận',
    cancelText = 'Hủy',
    isDanger = true
  } = confirmAction;
  
  return (
    <div className="modal-backdrop" onClick={handleCancel}>
      <div 
        className="modal-content max-w-md p-6"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="mb-4">
          <h2 className="text-xl font-bold text-gray-800 mb-2">
            {title}
          </h2>
          <p className="text-gray-600">
            {message}
          </p>
        </div>
        
        <div className="flex gap-3 justify-end">
          <button
            onClick={handleCancel}
            className="btn-secondary"
          >
            {cancelText}
          </button>
          <button
            onClick={handleConfirm}
            className={isDanger ? 'btn-danger' : 'btn-primary'}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
};

ConfirmDialog.propTypes = {
  modals: PropTypes.shape({
    confirm: PropTypes.bool
  }),
  closeModal: PropTypes.func.isRequired,
  confirmAction: PropTypes.shape({
    title: PropTypes.string,
    message: PropTypes.string,
    confirmText: PropTypes.string,
    cancelText: PropTypes.string,
    isDanger: PropTypes.bool,
    onConfirm: PropTypes.func,
    onCancel: PropTypes.func
  })
};

ConfirmDialog.defaultProps = {
  modals: {},
  confirmAction: {}
};

export default ConfirmDialog;


