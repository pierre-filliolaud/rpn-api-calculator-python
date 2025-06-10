# RPN Calculator UI

A web-based React UI for the RPN Calculator API.

## Features

- Input field for Reverse Polish Notation (RPN) expressions
- Submit button to send the expression to the API
- Display area for results and error messages
- Styled with Tailwind CSS

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)

### Installation

1. Navigate to the webapp directory:
   ```
   cd src/main/webapp
   ```

2. Install dependencies:
   ```
   npm install
   ```

### Running the Application

1. Start the development server:
   ```
   npm start
   ```

2. Open your browser and navigate to [http://localhost:3000](http://localhost:3000)

## Usage

1. Enter a Reverse Polish Notation expression in the input field (e.g., "3 4 +")
2. Click the "Calculate" button
3. The result will be displayed below the form
4. If there's an error in the expression, an error message will be displayed

## API Integration

The UI makes POST requests to the `/api/calculations/` endpoint with the following payload:

```json
{
  "expression": "3 4 +",
  "result": 7
}
```

The expression is evaluated locally before being sent to the API to ensure it's valid.

## Development

- The UI is built with React and uses functional components with hooks
- Styling is done with Tailwind CSS
- API requests are made using Axios