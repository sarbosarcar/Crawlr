import { FaSearch } from "react-icons/fa";

export const Header = () => {
  return (
    <header className="bg-gradient-to-r from-blue-500 to-purple-600 shadow-lg">
      <div className="container mx-auto px-4 py-6 flex items-center justify-between">
        {/* Logo and Title */}
        <div className="flex items-center space-x-3">
          <FaSearch className="text-white text-3xl" />
          <h1 className="text-3xl font-bold text-white">
            Document Search & Suggestions
          </h1>
        </div>


        {/* CTA Button */}
        <a
          href="#get-started"
          className="px-5 py-2 bg-white text-blue-600 font-semibold rounded-lg shadow-md hover:bg-gray-100 transition duration-300"
        >
          Get Started
        </a>
      </div>
    </header>
  );
};
