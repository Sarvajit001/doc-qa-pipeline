#!/bin/bash

# ============================================================
# DOC-QA PIPELINE — COMPLETE TEST COMMANDS
# Usage: bash test_commands.sh
# Or run individual curl commands directly
# ============================================================

BASE_URL="http://localhost:5000"
API_KEY="mysecretkey123"   # change this to your actual API key

# ============================================================
# /ask ENDPOINT — RAG PIPELINE
# ============================================================

echo "===== /ask — TXT FILE ====="

# Basic question from txt
curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is RAG?", "filepath": "sample.txt"}'

echo ""

# Question in document
curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is machine learning?", "filepath": "sample.txt"}'

echo ""

# Question NOT in document — guardrail test
curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "Who is Virat Kohli?", "filepath": "sample.txt"}'

echo ""

# Code generation — guardrail test
curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "Write a python function to add two numbers", "filepath": "sample.txt"}'

echo ""

# Conversation memory — turn 1
curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is machine learning?", "filepath": "sample.txt", "session_id": "test-session-1"}'

echo ""

# Conversation memory — turn 2 (follow up)
curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "Can you explain it simpler?", "filepath": "sample.txt", "session_id": "test-session-1"}'

echo ""

# Conversation memory — turn 3 (another follow up)
curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "Give me one real world example of it", "filepath": "sample.txt", "session_id": "test-session-1"}'

echo ""

echo "===== /ask — PDF FILE ====="

curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is Django?", "filepath": "sample.pdf"}'

echo ""

curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is Flask?", "filepath": "sample.pdf"}'

echo ""

curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is FastAPI?", "filepath": "sample.pdf"}'

echo ""

# Not in PDF — guardrail test
curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is the capital of France?", "filepath": "sample.pdf"}'

echo ""

echo "===== /ask — EXCEL FILE ====="

curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is Pandas?", "filepath": "sample.xlsx"}'

echo ""

curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is TensorFlow?", "filepath": "sample.xlsx"}'

echo ""

curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is Matplotlib?", "filepath": "sample.xlsx"}'

echo ""

# Not in Excel — guardrail test
curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "Who is Elon Musk?", "filepath": "sample.xlsx"}'

echo ""

echo "===== /ask — WORD FILE ====="

curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is React?", "filepath": "sample.docx"}'

echo ""

curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is TypeScript?", "filepath": "sample.docx"}'

echo ""

curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is Node.js?", "filepath": "sample.docx"}'

echo ""

# Not in Word doc — guardrail test
curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is machine learning?", "filepath": "sample.docx"}'

echo ""

# ============================================================
# /ask — AUTHENTICATION TESTS
# ============================================================

echo "===== /ask — AUTH TESTS ====="

# No API key — should return 401
curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?", "filepath": "sample.txt"}'

echo ""

# Wrong API key — should return 401
curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: wrongkey" \
  -d '{"question": "What is RAG?", "filepath": "sample.txt"}'

echo ""

# Missing question field — should return 400
curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"filepath": "sample.txt"}'

echo ""

# Missing filepath field — should return 400
curl -X POST $BASE_URL/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is RAG?"}'

echo ""

# ============================================================
# /history and /clear ENDPOINTS
# ============================================================

echo "===== HISTORY AND CLEAR ====="

# View history for test-session-1
curl -X GET $BASE_URL/history/test-session-1 \
  -H "X-API-Key: $API_KEY"

echo ""

# Clear history for test-session-1
curl -X DELETE $BASE_URL/clear/test-session-1 \
  -H "X-API-Key: $API_KEY"

echo ""

# Verify history is cleared
curl -X GET $BASE_URL/history/test-session-1 \
  -H "X-API-Key: $API_KEY"

echo ""

# ============================================================
# /agent ENDPOINT — TOOL CALLING AGENT
# ============================================================

echo "===== /agent — CALCULATOR TOOL ====="

# Pure math — should use calculator
curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is 47 times 89?"}'

echo ""

curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is 18 percent of 950?"}'

echo ""

curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is 250 divided by 5?"}'

echo ""

curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is square root of 144?"}'

echo ""

echo "===== /agent — DOCUMENT SEARCH TOOL — TXT ====="

curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is RAG according to the document?", "filepath": "sample.txt"}'

echo ""

curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What does the document say about deep learning?", "filepath": "sample.txt"}'

echo ""

curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is an AI agent according to the document?", "filepath": "sample.txt"}'

echo ""

echo "===== /agent — DOCUMENT SEARCH TOOL — PDF ====="

curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is Django according to the document?", "filepath": "sample.pdf"}'

echo ""

curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What does the document say about FastAPI?", "filepath": "sample.pdf"}'

echo ""

echo "===== /agent — DOCUMENT SEARCH TOOL — EXCEL ====="

curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What does the document say about Pandas?", "filepath": "sample.xlsx"}'

echo ""

curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is Scikit-learn according to the document?", "filepath": "sample.xlsx"}'

echo ""

echo "===== /agent — DOCUMENT SEARCH TOOL — WORD ====="

curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is React according to the document?", "filepath": "sample.docx"}'

echo ""

curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What does the document say about TypeScript?", "filepath": "sample.docx"}'

echo ""

echo "===== /agent — MULTI STEP (BOTH TOOLS) ====="

# Both tools — search document then calculate
curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is TypeScript according to the document, and what is 3 times 7?", "filepath": "sample.docx"}'

echo ""

curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is Pandas according to the document, and what is 25 percent of 200?", "filepath": "sample.xlsx"}'

echo ""

curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is RAG, and what is 100 divided by 4?", "filepath": "sample.txt"}'

echo ""

echo "===== /agent — GUARDRAIL TESTS ====="

# Code generation — should refuse
curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "Write a python function to sort a list"}'

echo ""

# Not in document — should say I dont know
curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "Who is Virat Kohli?", "filepath": "sample.txt"}'

echo ""

curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is the capital of Karnataka?", "filepath": "sample.txt"}'

echo ""

# General knowledge — no filepath, no tool needed
curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What is the capital of France?"}'

echo ""

echo "===== /agent — AUTH TESTS ====="

# No API key — should return 401
curl -X POST $BASE_URL/agent \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?", "filepath": "sample.txt"}'

echo ""

echo "===== ALL TESTS DONE ====="