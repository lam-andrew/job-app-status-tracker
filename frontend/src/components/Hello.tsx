import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Hello: React.FC = () => {
    const [message, setMessage] = useState<string>('Loading...');

    useEffect(() => {
        axios.get(`${process.env.REACT_APP_BACKEND_ENDPOINT}/hello`)
            .then(response => {
                setMessage(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the hello message:', error);
                setMessage('Failed to load message.');
            });
    }, []);

    return (
        <div>
            {message}
        </div>
    );
};

export default Hello;
