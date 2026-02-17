# API Reference

This document provides a detailed reference for the Super-Intelligence Agent API endpoints.

## Base URL
`http://localhost:8000` (or your deployed service URL)

## Endpoints

### `GET /`

**Description**: Checks the status of the API.

**Response**: 
```json
{
  "status": "online",
  "message": "Super-Intelligence Agent API is running."
}
```

### `POST /chat`

**Description**: Sends a query to the autonomous agent system and receives a response. This endpoint supports different agent types and allows specifying the LLM model to use.

**Request Body**:

| Field        | Type   | Description                                                                 | Required | Example                               |
|--------------|--------|-----------------------------------------------------------------------------|----------|---------------------------------------|
| `query`      | string | The natural language query or task for the agent.                           | Yes      | "What is the capital of France?"      |
| `agent_type` | string | The type of agent to use (`crewai`, `langgraph`, `autogen`, `pydanticai`). | No       | "crewai"                              |
| `model`      | string | The specific LLM model to use (e.g., `mistral/mistral-large-latest`). If not specified, defaults to `gpt-4o`. | No       | "mistral/mistral-large-latest"        |

**Example Request**:

```json
{
  "query": "Explain the concept of quantum entanglement in simple terms.",
  "agent_type": "crewai",
  "model": "deepseek/deepseek-chat"
}
```

**Response**: 

| Field      | Type   | Description                                            |
|------------|--------|--------------------------------------------------------|
| `content`  | string | The agent's response to the query.                     |
| `metadata` | object | Additional metadata from the agent or LLM interaction. |

**Example Response**:

```json
{
  "content": "Quantum entanglement is a phenomenon where two or more particles become linked in such a way that they share the same fate, regardless of the distance separating them...",
  "metadata": {
    "crew_result": "..."
  }
}
```

## Error Handling

- **`400 Bad Request`**: Returned for invalid `agent_type` or malformed request bodies.
- **`500 Internal Server Error`**: Returned for unexpected errors during agent execution or LLM communication. The `detail` field will contain a description of the error.
