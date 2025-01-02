import { DocumentCard } from '../docs/doccard';

export const SearchResults = ({ results, isLoading, error }) => {
  if (isLoading) {
    return (
      <div className="flex justify-center py-8">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        Error: {error}
      </div>
    );
  }

  if (!results.length) {
    return (
      <div className="text-center text-gray-600 py-8">
        No results found. Try a different search query.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {results.map((doc) => (
        <DocumentCard key={doc.id} document={doc} />
      ))}
    </div>
  );
};