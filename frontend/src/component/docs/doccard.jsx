export const DocumentCard = ({ document }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
      <h2 className="text-xl font-semibold mb-2 text-gray-900">
        {document.title}
      </h2>
      <p className="text-gray-600 mb-4">
        {document.excerpt}
      </p>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
            Score: {document.score}
          </span>
          <span className="text-gray-500 text-sm">
            Source: {document.source}
          </span>
        </div>
        <a
          href={document.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 hover:text-blue-800"
        >
          View Source →
        </a>
      </div>
    </div>
  );
};