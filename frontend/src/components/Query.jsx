import { useState } from "react";

export default function Query() {
  
  const [query, setQuery] = useState("");

  return (
    <div className="w-full mx-auto p-16 bg-white  dark:bg-gray-800 dark:text-white">
      <label htmlFor="OrderNotes" className="sr-only">Enter Query</label>

      <div
        className="overflow-hidden border border-gray-200 shadow-sm focus-within:border-blue-600 focus-within:ring-1 focus-within:ring-blue-600 dark:border-gray-700"
      >
        {/* Bind the textarea value to the state */}
        <textarea
          id="OrderNotes"
          className="w-full p-4 resize-none border-none align-top focus:outline-none focus:ring-0 sm:text-sm dark:bg-gray-800 dark:text-white"
          rows="4"
          placeholder="Enter your query here..."
          value={query} 
          onChange={(e) => setQuery(e.target.value)} 
        ></textarea>

        <div className="flex items-center justify-end gap-2 bg-white p-3 dark:bg-gray-800">
          {/* Adding onClick handler to clear the textarea */}
          <button
            type="button"
            className="rounded bg-gray-200 px-3 py-1.5 text-sm font-medium text-gray-700 hover:text-gray-600 dark:bg-gray-700 dark:text-gray-200 dark:hover:text-gray-100"
            onClick={() => setQuery("")} 
          >
            Clear
          </button>

          <button
            type="button"
            className="rounded bg-indigo-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-indigo-700"
          >
            Add
          </button>
        </div>
      </div>
    </div>
  );
}
