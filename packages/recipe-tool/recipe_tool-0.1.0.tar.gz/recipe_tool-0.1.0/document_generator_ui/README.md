 # Document Generator UI

 This project provides a FastAPI backend and a static single-page application (SPA) frontend for the Document Generator. It is a separate project that builds on the `recipe-tool` library, allowing users to:
   - Upload or load an outline JSON file describing the document structure and resources.
   - Visually edit document sections (titles, prompts, resource assignments, nesting).
   - Manage reference resources (upload, list, assign, remove).
   - Trigger generation of the final Markdown document via the Recipe Executor and download the output.

 > Note: You must have the **recipe-tool** project installed (e.g., via `pip install -e ../`) so the backend can import and invoke the Recipe Executor.

 ## Prerequisites

 - Python 3.11 or later
 - The `recipe-tool` project installed in editable mode:
   ```bash
   pip install -e ../
   ```

 ## Install Dependencies

 Install web dependencies for this project:

 ```bash
 pip install fastapi uvicorn
 ```

 ## Run the Server

 Launch the FastAPI backend and serve the SPA:

 ```bash
 uvicorn document_generator_ui.server.main:app --reload
 ```

 Open your browser to:

 ```
 http://127.0.0.1:8000
 ```

 In the browser console, you should see:

 ```
 Hello, world from Document Generator UI!
 ```

 Later versions will include API endpoints for loading/saving outlines, managing resources, and invoking generation. This is the v0 static SPA proof of concept.