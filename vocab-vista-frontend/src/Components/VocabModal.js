import React from 'react'
import { Button, Modal } from 'react-bootstrap'

const VocabModal = ({ showModal, closeModal, wordData }) => {
    return (
        <Modal show={showModal} onHide={closeModal}>
            <Modal.Header closeButton>
                <Modal.Title>Extracted Words</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <ul style={{ maxHeight: '400px', overflowY: 'auto' }}>
                    {Object.values(wordData).map((word, index) => (
                        <li key={index}>{word}</li>
                    ))}
                </ul>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={closeModal}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    );
  };
  export default VocabModal;