import { useState } from 'react';

const Response = () => {
    const [response, setResponse] = useState('');

    // Function to fetch response from the LLM (FastAPI)
    const fetchResponse = async () => {
        try {
            const res = await fetch('http://localhost:8000/your-endpoint');
            const data = await res.json();
            setResponse(data.response);
        } catch (error) {
            console.error('Error fetching response:', error);
        }
    };

    return (
        <div className="w-full mx-auto p-16 bg-white  dark:bg-gray-800 dark:text-white">
            <div className="">
                <h2 className="text-2xl font-bold mb-4">LLM Response</h2>
                <div className="w-full p-4 resize-none border-none align-top focus:outline-none focus:ring-0 sm:text-sm dark:bg-gray-800 dark:text-white">
                    {response ? (
                        <div>
                            <p>{response}</p>
                            <div className="mt-4">
                                <h3 className="text-lg font-semibold">Source References:</h3>
                                {/* Assuming response contains source references */}
                                <ul className="list-disc list-inside">
                                    {response.sources && response.sources.map((source, index) => (
                                        <li key={index}>{source}</li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    ) : (
                        <p>No response yet. Click the button to fetch response.</p>
                    )}
                </div>
                <button
        type="button"
        className="rounded bg-indigo-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-indigo-700"
      >
        Fetch response
      </button>
            </div>
        </div>
    );
};

export default Response;