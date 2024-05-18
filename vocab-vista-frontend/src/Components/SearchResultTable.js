import React, { useState } from 'react';
import { Button, Spinner } from 'react-bootstrap';

const SearchResultTable = ({ bookData, openModal, setWordData }) => {
  const [loading, setLoading] = useState(false);

  const fetchWords = (bookId) => {
    setLoading(true);

    fetch(`http://192.168.1.247:105/books/${bookId}/words/`)
      .then(response => response.json())
      .then(data => {
        setWordData(data);
        setLoading(false);
        openModal();
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  };

  const constructThumbnailLink = (coverId) => {
    return `https://covers.openlibrary.org/b/id/${coverId}-M.jpg`
  }

  return (
    <div>
      <table className='table table-striped'>
        <tbody>
          {bookData.map((item, index) => (
            <tr key={index}>
              <td style ={{ textAlign: 'center' }}>
                  <img src={constructThumbnailLink(item[1]['editions']['docs'][0]['cover_i'])} />
              </td>
              <td>
                <div style={{ display: 'flex', flexDirection: 'row' }}>
                  <div>
                    <h1>{item[1]['title']}</h1>
                    <h3>{item[1]['author_name'].join(', ')}</h3>
                    <p>{item[1]['editions']['docs'][0]['publish_date'][0]}</p>
                    <p>{item[1]['editions']['docs'][0]['publisher'][0]}</p>
                  </div>
                  <Button
                    onClick={() => fetchWords(item[1]['editions']['docs'][0]['ia'])}
                    className='btn-primary'
                    variant='primary' size='lg' 
                    style={{ marginLeft: 'auto', alignSelf: 'center', marginRight: '75px' }}
                    disabled={loading}>
                      {loading ? (
                        <>
                          <Spinner animation="border" size="sm" /> Loading...
                        </>
                      ) : (
                        'Extract Words'
                      )}
                  </Button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
export default SearchResultTable;