import React, { useState } from 'react';
import axios from 'axios';

// Utility function to evaluate RPN expressions
const evaluateRPN = (expression) => {
  const tokens = expression.trim().split(/\s+/);
  const stack = [];
  
  for (const token of tokens) {
    if (['+', '-', '*', '/'].includes(token)) {
      if (stack.length < 2) {
        throw new Error('Invalid expression: not enough operands');
      }
      
      const b = stack.pop();
      const a = stack.pop();
      
      switch (token) {
        case '+': stack.push(a + b); break;
        case '-': stack.push(a - b); break;
        case '*': stack.push(a * b); break;
        case '/': 
          if (b === 0) throw new Error('Division by zero');
          stack.push(a / b); 
          break;
        default: break;
      }
    } else {
      const num = parseFloat(token);
      if (isNaN(num)) {
        throw new Error(`Invalid token: ${token}`);
      }
      stack.push(num);
    }
  }
  
  if (stack.length !== 1) {
    throw new Error('Invalid expression: too many operands');
  }
  
  return stack[0];
};

function Calculator() {
  const [expression, setExpression] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setIsLoading(true);
    
    try {
      // First, evaluate the expression locally
      const calculatedResult = evaluateRPN(expression);
      
      // Then, send both the expression and result to the API
      const response = await axios.post('/api/calculations/', {
        expression,
        result: calculatedResult
      });
      
      setResult(response.data.result);
    } catch (err) {
      setError(err.message || 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="expression" className="block text-sm font-medium text-gray-700 mb-1">
            RPN Expression
          </label>
          <input
            id="expression"
            type="text"
            value={expression}
            onChange={(e) => setExpression(e.target.value)}
            placeholder="e.g., 3 4 +"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required
          />
        </div>
        
        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {isLoading ? 'Calculating...' : 'Calculate'}
        </button>
      </form>
      
      {error && (
        <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      
      {result !== null && !error && (
        <div className="mt-4">
          <h3 className="text-lg font-medium text-gray-900">Result</h3>
          <div className="mt-2 p-3 bg-gray-100 rounded text-2xl font-bold text-center">
            {result}
          </div>
        </div>
      )}
    </div>
  );
}

export default Calculator;