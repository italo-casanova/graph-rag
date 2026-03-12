# Graph-RAG Legal Document Assistant

Sistema de **Retrieval Augmented Generation (RAG)** híbrido que combina
**grafos semánticos + búsqueda vectorial** para analizar documentos
legales como contratos, propuestas y adendas.

El sistema permite:

-   Ingestar documentos PDF
-   Construir embeddings semánticos
-   Crear una **taxonomía de conceptos legales**
-   Relacionar documentos mediante un **grafo de conocimiento**
-   Recuperar información usando **Graph + Vector Retrieval**
-   Generar respuestas usando un **LLM**

------------------------------------------------------------------------

# Arquitectura General

El sistema utiliza una arquitectura **Hybrid Graph + Vector RAG**.

    User Query
         │
         ▼
    Entity Extraction (LLM)
         │
         ▼
    Taxonomy Concepts
         │
         ▼
    Graph Retrieval (Gremlin)
         │
         ▼
    Candidate Documents
         │
         ▼
    Vector Similarity Search (pgvector)
         │
         ▼
    Relevant Chunks
         │
         ▼
    LLM Answer Generation

Este enfoque combina:

-   **estructura semántica (grafo)**
-   **similitud semántica (vectores)**

------------------------------------------------------------------------

# Grafos y Taxonomías

Un RAG basado únicamente en vectores tiene varias limitaciones:

-   No modela **relaciones semánticas explícitas**
-   No preserva **estructura conceptual**
-   Puede recuperar textos similares pero **irrelevantes al dominio**

Las **taxonomías** permiten estructurar el dominio legal en jerarquías
conceptuales:

    Document
     ├ Contract
     │   ├ LoanContract
     │   ├ ServiceContract
     │
     ├ Regulation
     │   ├ BankingRegulation
     │
     ├ Proposal
     └ Invoice

Esto permite:

-   clasificar documentos
-   restringir el espacio de búsqueda
-   preservar semántica del dominio

El **grafo** modela relaciones entre conceptos y documentos.

    (Concept: Contract)
            │
            │ mentions
            ▼
    (Document: BanBif Loan Contract)

Esto permite:

-   recuperación por concepto
-   navegación semántica
-   razonamiento multi‑salto (multi-hop)

------------------------------------------------------------------------

# Ventajas de Graph + Vector RAG

  Característica            Vector RAG   Graph + Vector RAG
  ------------------------- ------------ --------------------
  Similaridad semántica     ✔            ✔
  Relaciones conceptuales   ✘            ✔
  Filtrado por dominio      limitado     fuerte
  Interpretabilidad         baja         alta
  Explicabilidad            baja         alta
  Multi-hop reasoning       ✘            ✔

------------------------------------------------------------------------

# Comandos

## Linux / macOS

Requisitos:

-   Docker
-   Docker Compose
-   Make
-   Python

Ejecutar:

    make dev

Este comando:

1.  Levanta contenedores
2.  Instala modelos de Ollama
3.  Inicializa PostgreSQL
4.  Ejecuta ingesta de documentos
5.  Levanta la API

------------------------------------------------------------------------

## Windows (PowerShell)

Requisitos:

-   Docker Desktop
-   Python

Ejecutar:

    powershell -ExecutionPolicy Bypass -File run.ps1

Este script:

1.  levanta contenedores Docker
2.  instala modelos Ollama
3.  inicializa PostgreSQL
4.  ejecuta ingestión de documentos
5.  levanta la API

------------------------------------------------------------------------

# Endpoint de Consulta

    POST /query

Ejemplo:

    curl -X POST http://localhost:5000/query -H "Content-Type: application/json" --data-raw '{"question":"¿Cuáles son las obligaciones del prestatario según un contrato de BanBif?"}'

Respuesta:

    {
     "answer": "..."
    }
