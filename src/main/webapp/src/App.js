import React from 'react';
import Calculator from './components/Calculator';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">RPN Calculator</h1>
        <p className="text-gray-600 text-center mt-2">
          Enter a Reverse Polish Notation expression (e.g., "3 4 +")
        </p>
      </header>
      <main className="w-full max-w-md">
        <Calculator />
      </main>
      <footer className="mt-8 text-sm text-gray-500">
        &copy; {new Date().getFullYear()} RPN Calculator
      </footer>
    </div>
  );
}

export default App;