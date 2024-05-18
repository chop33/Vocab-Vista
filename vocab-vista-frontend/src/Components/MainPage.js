import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { Button } from 'react-bootstrap';
import SearchResultTable from './SearchResultTable.js'
import VocabModal from './VocabModal.js';

const MainPage = () => {
    const [bookData, setBookData] = useState({});
    const [searchText, setSearchText] = useState('');
    const [showModal, setShowModal] = useState(false);
    const [wordData, setWordData] = useState({});

    useEffect(() => {
    }, [searchText]);

    const handleOpenModal = () => {
        setShowModal(true);
    };
    
    const handleCloseModal = () => {
        setShowModal(false);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('http://192.168.1.247:105/books/', {
            query: searchText
        })
        .then(response => {
            setBookData(response['data']['docs']);
        })
        .catch(error => {
            console.error('Error fetching data: ', error);
        });
        console.log('Search text:', searchText);
    };

    return (
        <div>
            <div className='custom-container'>
                <h1 className='title'>Vocab Vista</h1>
                <div className="search-box">
                    <form onSubmit={handleSubmit}>  
                        <input
                            type="text" 
                            placeholder="Search..." 
                            value={searchText}
                            onChange={(e) => setSearchText(e.target.value)}
                        />
                        <Button type='submit' className='btn-primary'>Search</Button>
                    </form>
                </div>
            </div>
            <div>
                <h1 style={{ marginLeft: '20px', marginBottom: '20px' }}>Results</h1>
                <SearchResultTable
                    bookData={Object.entries(bookData)}
                    openModal={handleOpenModal}
                    setWordData={setWordData}
                />
            </div>
            <VocabModal
                showModal={showModal}
                closeModal={handleCloseModal}
                wordData={wordData}
            />
        </div>
    );
}

export default MainPage;