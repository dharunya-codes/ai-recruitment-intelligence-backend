/**
 * LM-Inspect AI - Centralized Backend & API Configuration
 *
 * This configuration defines where and how the frontend connects to the future
 * AI-powered Computer Vision, OCR, and Legal Metrology Rule Engine backend.
 *
 * TO CONNECT YOUR REAL BACKEND:
 * 1. Set VITE_API_BASE_URL in .env (e.g. http://localhost:8000/api/v1 or https://api.legalmetrology.gov.in)
 * 2. Set VITE_USE_MOCK=false in .env
 */

export const API_CONFIG = {
  /**
   * Base URL for the AI / Backend REST API.
   * Configurable via VITE_API_BASE_URL environment variable.
   */
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',

  /**
   * Master Mock Toggle.
   * When true, requests use the internal mock service with simulated network latency.
   * When false, requests are routed to the real backend API endpoints.
   */
  USE_MOCK: import.meta.env.VITE_USE_MOCK !== 'false',

  /**
   * Request timeout in milliseconds (default: 45 seconds for AI heavy operations).
   */
  TIMEOUT_MS: 45000,

  /**
   * Defined API REST Endpoints matching the target AI Inspection Pipeline:
   *
   *   Product Image (POST /images/upload)
   *     ↓
   *   OCR & Layout Parsing (POST /declarations/extract)
   *     ↓
   *   Legal Metrology Rule Engine (POST /rules/validate)
   *     ↓
   *   Compliance Dossier & Violations (GET /inspections/:id/compliance)
   */
  ENDPOINTS: {
    // 1. Image Upload
    UPLOAD_IMAGE: '/images/upload',

    // 2. Full Pipeline Trigger
    ANALYZE_PRODUCT: '/inspections/analyze',

    // 3. OCR & AI Declaration Detection
    EXTRACT_DECLARATIONS: '/declarations/extract',

    // 4. Legal Metrology Rule Validation Engine
    VALIDATE_DECLARATIONS: '/rules/validate',

    // 5. Compliance Results & Dossier
    GET_COMPLIANCE_RESULT: (id: string) => `/inspections/${id}/compliance`,

    // 6. Violations Register
    GET_VIOLATIONS: '/violations',

    // 7. Portal Analytics & Management
    GET_DASHBOARD: '/dashboard/stats',
    GET_HISTORY: '/inspections/history',
    GET_PRODUCT: (id: string) => `/products/${id}`,
    GENERATE_REPORT: (id: string) => `/inspections/${id}/report`,
    GET_ANALYTICS: '/analytics/summary',
  },
};
